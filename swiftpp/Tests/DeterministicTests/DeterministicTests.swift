import XCTest
import ErgenticsCXX
import ErgenticsSwift
import ErgenticsInterop

final class DeterministicTests: XCTestCase {

    func testAntiCancellationSummationSweep() {
        let item = TripleCheckBridge.checkSummationAntiCancellation()
        XCTAssertTrue(item.passed, item.detail)

        // Adversarial mixed-order float sweep: naive forward != naive reverse, Neumaier recovers exact sum.
        let adv = [1e15, 0.25, -1e15, 0.25, 1e15, 0.25, -1e15, 0.25]
        let sw = runSummationSweep(adv)
        let cx = adv.withUnsafeBufferPointer { ergentics.run_summation_sweep($0.baseAddress, $0.count) }
        XCTAssertTrue(sw.allFinite && cx.all_finite)
        XCTAssertEqual(sw.neumaier, 1.0, accuracy: 1e-12)
        XCTAssertEqual(cx.neumaier, 1.0, accuracy: 1e-12)
        XCTAssertEqual(sw.neumaier, cx.neumaier, accuracy: 1e-15)
    }

    func testExactMobiusAndGCD() {
        for n: Int32 in 1...60 {
            XCTAssertEqual(mobiusMu(n), ergentics.mobius_mu(n), "Mobius mismatch at n=\(n)")
        }
        XCTAssertEqual(mobiusMu(1), 1)
        XCTAssertEqual(mobiusMu(4), 0)
        XCTAssertEqual(mobiusMu(6), 1)
        XCTAssertEqual(mobiusMu(30), -1)
        XCTAssertEqual(gcdInt64(48, 18), ergentics.gcd_i64(48, 18))
        XCTAssertEqual(gcdInt64(48, 18), 6)
    }

    func testInterleavedPLRMovesAndInvolution() {
        let item = TripleCheckBridge.checkInterleavedPLRMoves()
        XCTAssertTrue(item.passed, item.detail)
    }

    func testIharaBassAndExactPrimesUpTo40() {
        let (item, w12, w24, w40) = TripleCheckBridge.checkIharaBassAndExactPrimes()
        XCTAssertTrue(item.passed, item.detail)
        XCTAssertEqual(w12.totalPrimes, 576)
        XCTAssertEqual(w24.totalPrimes, 1_394_120)
        XCTAssertEqual(w40.totalPrimes, 54_975_717_792)
        XCTAssertEqual(w40.nonMultiple12Closed, 0)
    }

    func testTuneTheoremAndNegM4Counterexample() {
        let (item, rep) = TripleCheckBridge.checkTuneTheorem(maxLen: 12)
        XCTAssertTrue(item.passed, item.detail)
        XCTAssertTrue(rep.lemmaL1 && rep.lemmaL2 && rep.lemmaL3)
        XCTAssertTrue(rep.backtrackCounterexampleConfirmed)
        XCTAssertEqual(rep.decodeFailures, 0)
        XCTAssertEqual(rep.periodicTuneFailures, 0)
    }
}
