import XCTest
import ErgenticsCXX
import ErgenticsSwift
import ErgenticsInterop

final class RuntimeTests: XCTestCase {

    func testGlobalMatrixInvariantsAndFaultInjection() {
        let w40 = computeExactWindingDistribution(m: 40)
        let (item, covLMin) = TripleCheckBridge.checkRuntimeGlobalInvariants(w40: w40)
        XCTAssertTrue(item.passed, item.detail)
        XCTAssertGreaterThan(covLMin, 0.02)
    }

    func testOffDiagonalSpikeTrapAndNaNPoisoning() {
        // Positive diagonals (1.0, 1.0) yet globally indefinite (lambda_min = -1.5): component checks miss this!
        let spiked = [1.0, 2.5, 2.5, 1.0]
        let sw = checkSymmetricPD(spiked, n: 2)
        let cx = spiked.withUnsafeBufferPointer { ergentics.check_symmetric_pd($0.baseAddress, 2, 1e-12, 1e-12) }
        XCTAssertTrue(sw.diagonalPositive && cx.diagonal_positive)
        XCTAssertFalse(sw.choleskyOK || cx.cholesky_ok)
        XCTAssertEqual(sw.code, .notPositiveDefinite)
        XCTAssertEqual(cx.code, 4)
        XCTAssertEqual(sw.lambdaMin, -1.5, accuracy: 1e-12)
        XCTAssertEqual(sw.lambdaMin, cx.lambda_min, accuracy: 1e-12)

        // Single NaN or Inf sample poisons covariance -> immediate INV_NON_FINITE.
        for bad in [Double.nan, Double.infinity, -Double.infinity] {
            let poisoned = [1.0, bad, bad, 1.0]
            let swB = checkSymmetricPD(poisoned, n: 2)
            let cxB = poisoned.withUnsafeBufferPointer { ergentics.check_symmetric_pd($0.baseAddress, 2, 1e-12, 1e-12) }
            XCTAssertEqual(swB.code, .nonFinite)
            XCTAssertEqual(cxB.code, 2)
        }
    }

    func testProbabilitySimplexAndAggregateConservation() {
        // Valid simplex passes in both lanes.
        let valid = [0.25, 0.5, 0.25]
        let sOK = checkProbabilitySimplex(valid)
        let cOK = valid.withUnsafeBufferPointer { ergentics.check_probability_simplex($0.baseAddress, $0.count, 1e-12) }
        XCTAssertEqual(sOK.code, .ok)
        XCTAssertEqual(cOK.code, 0)

        // Per-cell valid [0,1] values that violate aggregate sum == 1.0 must fail globally.
        let leak = [0.4, 0.4, 0.4]
        let sLeak = checkProbabilitySimplex(leak)
        let cLeak = leak.withUnsafeBufferPointer { ergentics.check_probability_simplex($0.baseAddress, $0.count, 1e-12) }
        XCTAssertEqual(sLeak.code, .conservationViolation)
        XCTAssertEqual(cLeak.code, 8)

        // Negative mass rejected explicitly.
        let neg = [-0.1, 0.6, 0.5]
        let sNeg = checkProbabilitySimplex(neg)
        let cNeg = neg.withUnsafeBufferPointer { ergentics.check_probability_simplex($0.baseAddress, $0.count, 1e-12) }
        XCTAssertEqual(sNeg.code, .negativeProbability)
        XCTAssertEqual(cNeg.code, 9)
    }
}
