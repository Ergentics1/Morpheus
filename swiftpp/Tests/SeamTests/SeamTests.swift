import XCTest
import ErgenticsCXX
import ErgenticsSwift
import ErgenticsInterop

final class SeamTests: XCTestCase {

    func testKeyedPRNGBitExactReplayAndOrderInvariance() {
        let kA = PRNGKey(suite: "prime-cadences", experiment: "exp-A", trialIndex: 0, seed: 42)
        let kB = PRNGKey(suite: "prime-cadences", experiment: "exp-B", trialIndex: 0, seed: 42)

        // Order-invariance check: drawing A then B vs B then A produces bit-identical sequences.
        var a1 = KeyedPRNG(key: kA)
        var b1 = KeyedPRNG(key: kB)
        let seqA1 = (0..<32).map { _ in a1.nextUInt64() }
        let seqB1 = (0..<32).map { _ in b1.nextUInt64() }

        var b2 = KeyedPRNG(key: kB)
        var a2 = KeyedPRNG(key: kA)
        let seqB2 = (0..<32).map { _ in b2.nextUInt64() }
        let seqA2 = (0..<32).map { _ in a2.nextUInt64() }

        XCTAssertEqual(seqA1, seqA2)
        XCTAssertEqual(seqB1, seqB2)
        XCTAssertNotEqual(seqA1, seqB1)

        // Bit-for-bit equality against C++20 KeyedPRNG over UInt64, bounded, unit double, and normal double.
        var cxA = ergentics.cxx_make_prng(kA.suiteHash, kA.experimentHash, kA.trialIndex, kA.seed)
        for v in seqA1 {
            XCTAssertEqual(v, ergentics.cxx_prng_next_u64(&cxA))
        }
        for _ in 0..<32 {
            let swN = a1.nextNormalDouble()
            let cxN = ergentics.cxx_prng_next_normal(&cxA)
            XCTAssertEqual(swN, cxN, accuracy: 1e-13)
        }
    }

    func testGuardedPtoRtoDSeamBoundary() {
        let w12 = computeExactWindingDistribution(m: 12)
        let w40 = computeExactWindingDistribution(m: 40)
        let p12 = w12.primeCounts.map { Double($0) / Double(w12.totalPrimes) }
        let p40 = w40.primeCounts.map { Double($0) / Double(w40.totalPrimes) }
        let cal12 = evaluateDiscreteGaussianCalibration(probs: p12, wMin: w12.wMin, sigma2: 12.0 / 24.0)
        let cal40 = evaluateDiscreteGaussianCalibration(probs: p40, wMin: w40.wMin, sigma2: 40.0 / 24.0)

        let item = TripleCheckBridge.checkSeamReplayAndHandoff(cal12: cal12, cal40: cal40)
        XCTAssertTrue(item.passed, item.detail)

        // Verify NaN flux and NaN calibration both fail closed at the seam across both lanes.
        let cov = buildTonnetzCovariancePerStep()
        let pol = SeamPolicy(maxTV: 0.05, maxAbsExcessKurtosis: 0.25, minCovEigenvalue: 1e-6, fluxMin: 0.0, fluxMax: 6.283185307179586)
        let nanFluxS = guardedFluxKernelHandoff(calibration: cal40, cov2x2RowMajor: cov, fluxPhi: .nan, policy: pol)
        let nanFluxC = cov.withUnsafeBufferPointer {
            ergentics.guarded_flux_kernel_handoff(TripleCheckBridge.toCxxCalibration(cal40), $0.baseAddress, .nan, TripleCheckBridge.toCxxPolicy(pol))
        }
        XCTAssertFalse(nanFluxS.allowed || nanFluxC.allowed)
        XCTAssertEqual(nanFluxS.code, .rejectNonFinite)
        XCTAssertEqual(nanFluxC.code, 1)
    }
}
