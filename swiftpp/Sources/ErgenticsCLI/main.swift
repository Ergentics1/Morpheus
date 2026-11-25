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

struct EdgeworthExportRecord: Encodable {
    struct RegimeParams: Encodable {
        let m: Int32
    }
    struct ExactCumulants: Encodable {
        let kappa2_over_m_exact: Double
        let kappa4_std_coeff_exact: Double
        let kappa6_std_armchair_exact: Double
        let kappa6_std_zigzag_exact: Double
    }
    struct WindingMetrics: Encodable {
        let total_primes: Int64
        let variance: Double
        let var_abs_error: Double
        let excess_kurtosis: Double
        let m_times_excess_kurtosis: Double
        let tv_gaussian_c2: Double
        let kl_gaussian_c2: Double
        let jsd_gaussian_c2: Double
        let tv_edgeworth4_c2_prime: Double
        let jsd_edgeworth4_c2_prime: Double
        let tv_edgeworth6_c2_double_prime: Double
        let jsd_edgeworth6_c2_double_prime: Double
        let tv_gain_4th: Double
        let tv_gain_6th: Double
    }
    struct Tonnetz2DIsotropy: Encodable {
        let bad_divisibility_count: Int64
        let k2_over_m_u: Double
        let k2_over_m_v: Double
        let k2_over_m_zigzag: Double
        let m_ex_kurt_u: Double
        let m_ex_kurt_v: Double
        let m_ex_kurt_zigzag: Double
        let max_isotropy_spread_4th: Double
        let m2_std6_u: Double
        let m2_std6_v: Double
        let m2_std6_zigzag: Double
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
    let regime_params: RegimeParams
    let exact_theory: ExactCumulants
    let winding_metrics: WindingMetrics
    let tonnetz_2d_isotropy: Tonnetz2DIsotropy
    let bound_check: BoundCheck
}

var exportPath: String?
var exportEdgeworthPath: String?
var codeCommit = "working-tree"
let args = CommandLine.arguments
var idx = 1
while idx < args.count {
    if args[idx] == "--export-calibration", idx + 1 < args.count {
        exportPath = args[idx + 1]
        idx += 2
    } else if args[idx] == "--export-edgeworth", idx + 1 < args.count {
        exportEdgeworthPath = args[idx + 1]
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

if let ePath = exportEdgeworthPath {
    let (_, e40, ax40) = TripleCheckBridge.checkNoveltyTheorems()
    let rec = EdgeworthExportRecord(
        schema_version: "1.0.0",
        correspondence_id: "C-2'/C-2''",
        code_commit: codeCommit,
        implementation: "swiftpp",
        regime_params: .init(m: 40),
        exact_theory: .init(
            kappa2_over_m_exact: 1.0 / 24.0,
            kappa4_std_coeff_exact: -8.5,
            kappa6_std_armchair_exact: 1469.0 / 4.0,
            kappa6_std_zigzag_exact: 1471.0 / 4.0
        ),
        winding_metrics: .init(
            total_primes: e40.totalPrimes,
            variance: e40.variance,
            var_abs_error: e40.varAbsError,
            excess_kurtosis: e40.excessKurtosis,
            m_times_excess_kurtosis: e40.mTimesExcessKurtosis,
            tv_gaussian_c2: e40.tvGaussian,
            kl_gaussian_c2: e40.klGaussian,
            jsd_gaussian_c2: e40.jsdGaussian,
            tv_edgeworth4_c2_prime: e40.tvEdgeworth4,
            jsd_edgeworth4_c2_prime: e40.jsdEdgeworth4,
            tv_edgeworth6_c2_double_prime: e40.tvEdgeworth6,
            jsd_edgeworth6_c2_double_prime: e40.jsdEdgeworth6,
            tv_gain_4th: e40.tvGain4,
            tv_gain_6th: e40.tvGain6
        ),
        tonnetz_2d_isotropy: .init(
            bad_divisibility_count: ax40.badDivisibilityCount,
            k2_over_m_u: ax40.k2OverMU,
            k2_over_m_v: ax40.k2OverMV,
            k2_over_m_zigzag: ax40.k2OverMZigzag,
            m_ex_kurt_u: ax40.mExKurtU,
            m_ex_kurt_v: ax40.mExKurtV,
            m_ex_kurt_zigzag: ax40.mExKurtZigzag,
            max_isotropy_spread_4th: ax40.maxIsotropySpread4th,
            m2_std6_u: ax40.m2Std6U,
            m2_std6_v: ax40.m2Std6V,
            m2_std6_zigzag: ax40.m2Std6Zigzag
        ),
        bound_check: .init(
            bound_formula: "|m * kappa_ex + 17/2| < 0.01 and TV_Edge4 < TV_Gauss / 10 and TV_Edge6 < TV_Gauss / 70",
            observed: e40.tvEdgeworth6,
            threshold: e40.tvGaussian / 70.0,
            passed: e40.passed && ax40.passed
        )
    )
    let encoder = JSONEncoder()
    encoder.outputFormatting = [.prettyPrinted, .sortedKeys, .withoutEscapingSlashes]
    do {
        let data = try encoder.encode(rec)
        let url = URL(fileURLWithPath: ePath)
        try FileManager.default.createDirectory(at: url.deletingLastPathComponent(), withIntermediateDirectories: true)
        try data.write(to: url)
        print("Exported Edgeworth calibration JSON record to \(ePath)")
    } catch {
        FileHandle.standardError.write(Data("Failed to export Edgeworth JSON: \(error)\n".utf8))
        exit(2)
    }
}

exit(report.allPassed ? 0 : 1)

