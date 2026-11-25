import Foundation
import ErgenticsInterop
import ErgenticsSwift

struct CalibrationExportRecord: Encodable {
    struct PRNGKeyRecord: Encodable {
        let suite: String
        let experiment: String
        let seed: UInt64
    }
    struct RegimeParams: Encodable {
        let m: Int32
    }
    struct RInvariants: Encodable {
        let finite: Bool
        let conservation_exact: Bool
        let cov_pd_cholesky: Bool
        let lambda_min: Double
    }
    struct Metrics: Encodable {
        let tv: Double
        let kl: Double
        let ks: Double
        let w1: Double
        let skewness: Double
        let excess_kurtosis: Double
        let cov_1sigma: Double
        let cov_2sigma: Double
        let cov_3sigma: Double
    }
    struct RCTControl: Encodable {
        let control_id: String
        let n_trials: Int64
        let closed_observed: Int64
        let mc_vs_exact_closed_tv: Double
        let exact_closed_vs_prime_tv: Double
    }
    struct BoundCheck: Encodable {
        let bound_formula: String
        let observed: Double
        let threshold: Double
        let passed: Bool
    }

    let schema_version: String
    let correspondence_id: String
    let code_commit: String
    let implementation: String
    let prng_key: PRNGKeyRecord
    let regime_params: RegimeParams
    let r_invariants: RInvariants
    let metrics: Metrics
    let rct_control: RCTControl
    let bound_check: BoundCheck
}

var exportPath: String?
var codeCommit = "working-tree"
let args = CommandLine.arguments
var idx = 1
while idx < args.count {
    if args[idx] == "--export-calibration", idx + 1 < args.count {
        exportPath = args[idx + 1]
        idx += 2
    } else if args[idx] == "--commit", idx + 1 < args.count {
        codeCommit = args[idx + 1]
        idx += 2
    } else {
        idx += 1
    }
}

print("=== Morpheus Swift++ Triple-Check SWE-Sweep (Pure Swift 6.4 <-> C++20 Interop) ===")
let report = TripleCheckBridge.runFullSuite()
for item in report.items {
    let tag = item.passed ? "PASS" : "FAIL"
    print("  [\(tag)] [\(item.category)] \(item.id): \(item.detail)")
}
print(String(format: "Max cross-lane delta (Pure Swift vs C++20 Interop): %.3e", report.maxObservedDelta))
print("Overall Result: \(report.allPassed ? "ALL PASS" : "FAILURES")")

if let path = exportPath {
    let record = CalibrationExportRecord(
        schema_version: "1.0.0",
        correspondence_id: "C-2",
        code_commit: codeCommit,
        implementation: "swiftpp",
        prng_key: .init(suite: "prime-cadences", experiment: "RCT-3-winding-null", seed: 20261125),
        regime_params: .init(m: 40),
        r_invariants: .init(
            finite: report.cal40.code == .ok,
            conservation_exact: report.cal40.simplexError < 1e-12,
            cov_pd_cholesky: report.covLambdaMin > 0.0,
            lambda_min: report.covLambdaMin
        ),
        metrics: .init(
            tv: report.cal40.totalVariation,
            kl: report.cal40.klDivergence,
            ks: report.cal40.ksDistance,
            w1: report.cal40.wasserstein1,
            skewness: report.cal40.skewness,
            excess_kurtosis: report.cal40.excessKurtosis,
            cov_1sigma: report.cal40.cov1Sigma,
            cov_2sigma: report.cal40.cov2Sigma,
            cov_3sigma: report.cal40.cov3Sigma
        ),
        rct_control: .init(
            control_id: "RCT-3",
            n_trials: report.windingNullRCT.totalWalksSampled,
            closed_observed: report.windingNullRCT.closedWalksObserved,
            mc_vs_exact_closed_tv: report.windingNullRCT.mcVsExactClosedTV,
            exact_closed_vs_prime_tv: report.windingNullRCT.exactClosedVsPrimeTV
        ),
        bound_check: .init(
            bound_formula: "10/m (Edgeworth excess kurtosis)",
            observed: abs(report.cal40.excessKurtosis),
            threshold: 10.0 / 40.0,
            passed: abs(report.cal40.excessKurtosis) <= 10.0 / 40.0
        )
    )
    let encoder = JSONEncoder()
    encoder.outputFormatting = [.prettyPrinted, .sortedKeys, .withoutEscapingSlashes]
    do {
        let data = try encoder.encode(record)
        let url = URL(fileURLWithPath: path)
        try FileManager.default.createDirectory(at: url.deletingLastPathComponent(), withIntermediateDirectories: true)
        try data.write(to: url)
        print("Exported calibration JSON record to \(path)")
    } catch {
        FileHandle.standardError.write(Data("Failed to export calibration JSON: \(error)\n".utf8))
        exit(2)
    }
}

exit(report.allPassed ? 0 : 1)
