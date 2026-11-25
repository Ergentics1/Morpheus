import XCTest
import ErgenticsCXX
import ErgenticsSwift
import ErgenticsInterop

final class CalibrationTests: XCTestCase {

    func testRung1DistributionalCalibrationAndCorrespondenceC2() {
        let w12 = computeExactWindingDistribution(m: 12)
        let w24 = computeExactWindingDistribution(m: 24)
        let w40 = computeExactWindingDistribution(m: 40)
        let (item, cal12, cal24, cal40) = TripleCheckBridge.checkRung1Calibration(w12: w12, w24: w24, w40: w40)
        XCTAssertTrue(item.passed, item.detail)

        // Verify Correspondence Principle decay across all Rung-1 distributional metrics (TV, KL, KS, W1, |ex_kurt|).
        XCTAssertLessThan(cal40.totalVariation, cal24.totalVariation)
        XCTAssertLessThan(cal24.totalVariation, cal12.totalVariation)
        XCTAssertLessThan(cal40.klDivergence, cal24.klDivergence)
        XCTAssertLessThan(cal24.klDivergence, cal12.klDivergence)
        XCTAssertLessThan(cal40.ksDistance, cal24.ksDistance)
        XCTAssertLessThan(cal24.ksDistance, cal12.ksDistance)
        XCTAssertLessThan(cal40.wasserstein1, cal24.wasserstein1)
        XCTAssertLessThan(cal24.wasserstein1, cal12.wasserstein1)
        XCTAssertLessThan(abs(cal40.excessKurtosis), abs(cal24.excessKurtosis))
        XCTAssertLessThan(abs(cal24.excessKurtosis), abs(cal12.excessKurtosis))

        // Verify explicit CorrespondenceCheck evaluator parity across Swift and C++20.
        let ccS = evaluateCorrespondence(deeperValue: cal40.variance, olderValue: 40.0 / 24.0, regimeParam: 1.0 / 40.0, boundValue: 1e-3)
        let ccC = ergentics.evaluate_correspondence(cal40.variance, 40.0 / 24.0, 1.0 / 40.0, 1e-3)
        XCTAssertTrue(ccS.withinBound && ccC.within_bound)
        XCTAssertEqual(ccS.absError, ccC.abs_error, accuracy: 1e-15)
    }

    func testFluxWindowAndEDORamanujanThreshold() {
        let (item, fw, edo) = TripleCheckBridge.checkFluxWindowAndEDO()
        XCTAssertTrue(item.passed, item.detail)
        XCTAssertTrue(fw.cyclicRamanujan[1] && fw.cyclicRamanujan[2])
        XCTAssertFalse(fw.cyclicRamanujan[3])
        XCTAssertTrue(edo.ramanujan12 && edo.ramanujan31 && !edo.ramanujan53)
    }

    func testAllThreePreRegisteredRCTs() {
        let (items, sc, rct2, rct3) = TripleCheckBridge.checkRCTs()
        for item in items {
            XCTAssertTrue(item.passed, "\(item.id): \(item.detail)")
        }
        XCTAssertEqual(sc.ramanujanNontrivial, 7675)
        XCTAssertEqual(sc.voiceParityRank, 7372)
        XCTAssertTrue(rct2.passed)
        XCTAssertTrue(rct3.passed)
        XCTAssertEqual(rct3.nonMultiple12Observed, 0)
        XCTAssertGreaterThan(rct3.exactClosedVsPrimeTV, 0.0)
    }

    func testNoveltyTheoremsTripleCheck() {
        let (items, edge40, axes40) = TripleCheckBridge.checkNoveltyTheorems()
        XCTAssertEqual(items.count, 3)
        for item in items {
            XCTAssertTrue(item.passed, "\(item.id): \(item.detail)")
            XCTAssertLessThan(item.maxDelta, 1e-12, "\(item.id) cross-lane delta too large")
        }
        XCTAssertEqual(edge40.mTimesExcessKurtosis, -8.5, accuracy: 0.01)
        XCTAssertGreaterThan(edge40.tvGain4, 10.0)
        XCTAssertGreaterThan(edge40.tvGain6, 70.0)
        XCTAssertEqual(axes40.badDivisibilityCount, 0)
        XCTAssertLessThan(axes40.maxIsotropySpread4th, 0.02)
    }
}

