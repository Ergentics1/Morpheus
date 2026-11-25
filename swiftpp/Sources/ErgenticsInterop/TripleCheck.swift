import Foundation
import ErgenticsCXX
import ErgenticsSwift

/// Outcome of a single Swift++ Triple-Check turn comparing Pure Swift 6.4 vs Live Swift <-> C++20 Interop.
public struct TripleCheckItem: Sendable, Equatable {
    public let id: String
    public let category: String // "D", "R", "P", "Seam", "Correspondence", "RCT"
    public let passed: Bool
    public let maxDelta: Double
    public let detail: String
}

/// Complete audit snapshot returned by running all Triple-Check verifiers.
public struct TripleCheckSuiteReport: Sendable {
    public let items: [TripleCheckItem]
    public let cal12: Rung1CalibrationReport
    public let cal24: Rung1CalibrationReport
    public let cal40: Rung1CalibrationReport
    public let covLambdaMin: Double
    public let signingCensus: SigningCensusReport
    public let twoAdicRCT: TwoAdicRCTReport
    public let windingNullRCT: WindingNullRCTReport
    public let fluxWindow: FluxWindowReport
    public let edoComparison: EDOComparisonReport
    public let tuneReport: TuneCheckReport

    public var allPassed: Bool {
        items.allSatisfy(\.passed)
    }

    public var maxObservedDelta: Double {
        items.map(\.maxDelta).max() ?? 0.0
    }
}

/// Live Swift 6.4 <-> C++20 interop bridge and Triple-Check cross-verifier.
public enum TripleCheckBridge {

    // MARK: - Keyed PRNG Interop Conversions

    public static func toCxxKey(_ key: PRNGKey) -> ergentics.PRNGKey {
        ergentics.PRNGKey(
            suite_hash: key.suiteHash,
            experiment_hash: key.experimentHash,
            trial_index: key.trialIndex,
            seed: key.seed
        )
    }

    public static func toCxxCalibration(_ cal: Rung1CalibrationReport) -> ergentics.Rung1CalibrationReport {
        ergentics.Rung1CalibrationReport(
            code: cal.code.rawValue,
            total_variation: cal.totalVariation,
            kl_divergence: cal.klDivergence,
            ks_distance: cal.ksDistance,
            wasserstein_1: cal.wasserstein1,
            mean: cal.mean,
            variance: cal.variance,
            skewness: cal.skewness,
            excess_kurtosis: cal.excessKurtosis,
            cov_1sigma: cal.cov1Sigma,
            cov_2sigma: cal.cov2Sigma,
            cov_3sigma: cal.cov3Sigma,
            simplex_error: cal.simplexError
        )
    }

    public static func fromCxxCalibration(_ c: ergentics.Rung1CalibrationReport) -> Rung1CalibrationReport {
        Rung1CalibrationReport(
            code: InvariantCode(rawValue: c.code) ?? .outOfDomain,
            totalVariation: c.total_variation,
            klDivergence: c.kl_divergence,
            ksDistance: c.ks_distance,
            wasserstein1: c.wasserstein_1,
            mean: c.mean,
            variance: c.variance,
            skewness: c.skewness,
            excessKurtosis: c.excess_kurtosis,
            cov1Sigma: c.cov_1sigma,
            cov2Sigma: c.cov_2sigma,
            cov3Sigma: c.cov_3sigma,
            simplexError: c.simplex_error
        )
    }

    public static func toCxxPolicy(_ p: SeamPolicy) -> ergentics.SeamPolicy {
        ergentics.SeamPolicy(
            max_tv: p.maxTV,
            max_abs_excess_kurtosis: p.maxAbsExcessKurtosis,
            min_cov_eigenvalue: p.minCovEigenvalue,
            flux_min: p.fluxMin,
            flux_max: p.fluxMax
        )
    }

    // MARK: - D-Type Triple-Check

    public static func checkSummationAntiCancellation() -> TripleCheckItem {
        let xs = [1e16, 1.0, -1e16, 1.0, 1e16, 1.0, -1e16, 1.0]
        let sw = runSummationSweep(xs)
        let cx = xs.withUnsafeBufferPointer { buf in
            ergentics.run_summation_sweep(buf.baseAddress, buf.count)
        }
        let dNF = abs(sw.naiveForward - cx.naive_forward)
        let dNR = abs(sw.naiveReverse - cx.naive_reverse)
        let dKH = abs(sw.kahan - cx.kahan)
        let dNM = abs(sw.neumaier - cx.neumaier)
        let maxD = max(max(dNF, dNR), max(dKH, dNM))
        let trapped = abs(sw.naiveForward - 4.0) > 1.0 && abs(cx.naive_forward - 4.0) > 1.0
        let recovered = abs(sw.neumaier - 4.0) < 1e-12 && abs(cx.neumaier - 4.0) < 1e-12
        let ok = sw.allFinite && cx.all_finite && trapped && recovered && maxD < 1e-12
        return TripleCheckItem(
            id: "D-1", category: "D", passed: ok, maxDelta: maxD,
            detail: String(format: "naive=%.1f neumaier=%.1f spread=%.1f delta=%.2e", sw.naiveForward, sw.neumaier, sw.maxOrderSpread, maxD)
        )
    }

    /// Turn-by-turn live interleaved Swift <-> C++20 PLR move check across all 72 directed edges.
    public static func checkInterleavedPLRMoves() -> TripleCheckItem {
        var mismatches = 0
        for v: Int32 in 0..<24 {
            for mv: Int32 in 0..<3 {
                let s1 = applyPLRMove(vertex: v, moveId: mv)
                let c1 = ergentics.apply_plr_move(v, mv)
                if s1.targetVertex != c1.target_vertex ||
                   s1.voiceStep != c1.voice_step ||
                   s1.arrivingPitch != c1.arriving_pitch ||
                   s1.departingPitch != c1.departing_pitch {
                    mismatches += 1
                }
                // Live cross-language involution check: Swift forward -> C++ reverse must return to v with opposite step.
                let backCxx = ergentics.apply_plr_move(s1.targetVertex, mv)
                let backSw = applyPLRMove(vertex: c1.target_vertex, moveId: mv)
                if backCxx.target_vertex != v || backSw.targetVertex != v ||
                   (s1.voiceStep + backCxx.voice_step) != 0 || (c1.voice_step + backSw.voiceStep) != 0 {
                    mismatches += 1
                }
            }
        }
        return TripleCheckItem(
            id: "D-2", category: "D", passed: mismatches == 0, maxDelta: Double(mismatches),
            detail: "72 directed PLR edges + bidirectional Swift<->C++ involution round-trip: mismatches=\(mismatches)"
        )
    }

    public static func checkIharaBassAndExactPrimes() -> (item: TripleCheckItem, w12: WindingDistribution, w24: WindingDistribution, w40: WindingDistribution) {
        let uVals = [0.137, 0.29]
        var maxRes = 0.0
        var maxUDelta = 0.0
        for u in uVals {
            let rs = iharaBassResidual(u: u)
            let rc = ergentics.ihara_bass_residual(u)
            maxRes = max(maxRes, max(rs, rc))
            maxUDelta = max(maxUDelta, abs(rs - rc))
        }

        let w6s = computeExactWindingDistribution(m: 6)
        let w8s = computeExactWindingDistribution(m: 8)
        let w12s = computeExactWindingDistribution(m: 12)
        let w16s = computeExactWindingDistribution(m: 16)
        let w24s = computeExactWindingDistribution(m: 24)
        let w40s = computeExactWindingDistribution(m: 40)

        let w6c = ergentics.compute_exact_winding_distribution(6)
        let w8c = ergentics.compute_exact_winding_distribution(8)
        let w12c = ergentics.compute_exact_winding_distribution(12)
        let w16c = ergentics.compute_exact_winding_distribution(16)
        let w24c = ergentics.compute_exact_winding_distribution(24)
        let w40c = ergentics.compute_exact_winding_distribution(40)

        var binMismatches = 0
        func compareBins(_ s: WindingDistribution, _ c: ergentics.WindingDistribution) {
            if s.totalPrimes != c.total_primes ||
               s.totalClosedWalks != c.total_closed_walks ||
               s.nonMultiple12Closed != c.non_multiple_12_closed {
                binMismatches += 1
            }
            for i: Int32 in 0..<17 {
                if s.primeCounts[Int(i)] != ergentics.winding_prime_count(c, i) { binMismatches += 1 }
                if s.closedCounts[Int(i)] != ergentics.winding_closed_count(c, i) { binMismatches += 1 }
            }
        }
        compareBins(w6s, w6c)
        compareBins(w8s, w8c)
        compareBins(w12s, w12c)
        compareBins(w16s, w16c)
        compareBins(w24s, w24c)
        compareBins(w40s, w40c)

        // Correspondence C-1: |m * pi(m) - 2^(m+1)| / 2^(m/2) <= 48.
        let pntTarget40 = Double(1 << 41)
        let c1NormErr40 = abs(40.0 * Double(w40s.totalPrimes) - pntTarget40) / Double(1 << 20)

        let countsOK = (w6s.totalPrimes == 32 && w8s.totalPrimes == 78 &&
                        w12s.totalPrimes == 576 && w16s.totalPrimes == 8196 &&
                        w24s.totalPrimes == 1_394_120 && w40s.totalPrimes == 54_975_717_792 &&
                        w40s.nonMultiple12Closed == 0)
        let ok = countsOK && binMismatches == 0 && maxRes < 1e-10 && c1NormErr40 <= 48.0
        let item = TripleCheckItem(
            id: "D-3/C-1", category: "D", passed: ok, maxDelta: max(maxUDelta, Double(binMismatches)),
            detail: String(format: "pi(40)=%lld bins_diff=%d IB_res=%.2e C1_norm_err=%.4f<=48", w40s.totalPrimes, binMismatches, maxRes, c1NormErr40)
        )
        return (item, w12s, w24s, w40s)
    }

    public static func checkTuneTheorem(maxLen: Int32 = 12) -> (TripleCheckItem, TuneCheckReport) {
        let s = verifyTuneTheorem(maxLen: maxLen)
        let c = ergentics.verify_tune_theorem(maxLen)
        let match = (s.rootedPrimesChecked == c.rooted_primes_checked &&
                     s.decodeFailures == c.decode_failures &&
                     s.periodicTuneFailures == c.periodic_tune_failures &&
                     s.lemmaL1 == c.lemma_l1 && s.lemmaL2 == c.lemma_l2 && s.lemmaL3 == c.lemma_l3 &&
                     s.backtrackCounterexampleConfirmed == c.backtrack_counterexample_confirmed)
        let ok = match && s.lemmaL1 && s.lemmaL2 && s.lemmaL3 &&
                 s.backtrackCounterexampleConfirmed &&
                 s.rootedPrimesChecked > 0 && s.decodeFailures == 0 && s.periodicTuneFailures == 0
        let item = TripleCheckItem(
            id: "D-4/C-4", category: "D", passed: ok, maxDelta: match ? 0.0 : 1.0,
            detail: "checked=\(s.rootedPrimesChecked) decode_fail=\(s.decodeFailures) NEG-M4=\(s.backtrackCounterexampleConfirmed)"
        )
        return (item, s)
    }

    // MARK: - R-Type Triple-Check

    public static func checkRuntimeGlobalInvariants(w40: WindingDistribution) -> (TripleCheckItem, Double) {
        let covS = buildTonnetzCovariancePerStep()
        var covC = [Double](repeating: 0.0, count: 4)
        covC.withUnsafeMutableBufferPointer { ergentics.build_tonnetz_covariance_per_step($0.baseAddress) }

        let repS = checkSymmetricPD(covS, n: 2)
        let repC = covC.withUnsafeBufferPointer { ergentics.check_symmetric_pd($0.baseAddress, 2, 1e-12, 1e-12) }

        // Cross-check negative cases: off-diagonal spike & NaN poisoning.
        let spiked = [1.0, 2.5, 2.5, 1.0]
        let spS = checkSymmetricPD(spiked, n: 2)
        let spC = spiked.withUnsafeBufferPointer { ergentics.check_symmetric_pd($0.baseAddress, 2, 1e-12, 1e-12) }

        let poisoned = [1.0, Double.nan, 0.0, 1.0]
        let nanS = checkSymmetricPD(poisoned, n: 2)
        let nanC = poisoned.withUnsafeBufferPointer { ergentics.check_symmetric_pd($0.baseAddress, 2, 1e-12, 1e-12) }

        // Laplacian PSD nullity == 1.
        let lapS = buildLaplacianMatrix()
        var lapC = [Double](repeating: 0.0, count: 576)
        lapC.withUnsafeMutableBufferPointer { ergentics.build_laplacian_matrix($0.baseAddress) }
        let lRepS = checkSymmetricPSDNullity(lapS, n: 24, expectedNullity: 1)
        let lRepC = lapC.withUnsafeBufferPointer { ergentics.check_symmetric_psd_nullity($0.baseAddress, 24, 1, 1e-12, 1e-9) }

        // Twisted Hermitian check.
        let twS = buildTwistedAdjacencyComplex(phi: 1.2345)
        var twC = [Double](repeating: 0.0, count: 2 * 576)
        twC.withUnsafeMutableBufferPointer { ergentics.build_twisted_adjacency_complex(1.2345, $0.baseAddress) }
        let hS = checkHermitianComplex(twS, n: 24)
        var hCErr = 0.0
        let hCOK = twC.withUnsafeBufferPointer { ergentics.check_hermitian_complex($0.baseAddress, 24, 1e-12, &hCErr) }

        // Exact integer conservation sum_w pi(40, w) == pi(40).
        let consS = checkExactIntegerConservation(w40.primeCounts, expectedTotal: w40.totalPrimes)
        let consC = w40.primeCounts.withUnsafeBufferPointer {
            ergentics.check_exact_integer_conservation($0.baseAddress, $0.count, w40.totalPrimes)
        }

        let delta = max(
            abs(repS.lambdaMin - repC.lambda_min),
            max(abs(spS.lambdaMin - spC.lambda_min), abs(lRepS.lambdaMax - lRepC.lambda_max))
        )
        let ok = (repS.code == .ok && repC.code == 0 &&
                  spS.code == .notPositiveDefinite && spC.code == 4 && spS.diagonalPositive && !spS.choleskyOK &&
                  nanS.code == .nonFinite && nanC.code == 2 &&
                  lRepS.code == .ok && lRepC.code == 0 && lRepS.zeroEigenvalueCount == 1 && lRepC.zero_eigenvalue_count == 1 &&
                  hS.ok && hCOK &&
                  consS.code == .ok && consC.code == 0 &&
                  delta < 1e-12)
        let item = TripleCheckItem(
            id: "R-1", category: "R", passed: ok, maxDelta: delta,
            detail: String(format: "cov_lmin=%.6f spike_lmin=%.2f lap_nullity=%d delta=%.2e", repS.lambdaMin, spS.lambdaMin, lRepS.zeroEigenvalueCount, delta)
        )
        return (item, repS.lambdaMin)
    }

    // MARK: - P-Type, Correspondence & RCT Triple-Check

    public static func checkRung1Calibration(
        w12: WindingDistribution, w24: WindingDistribution, w40: WindingDistribution
    ) -> (TripleCheckItem, Rung1CalibrationReport, Rung1CalibrationReport, Rung1CalibrationReport) {
        func calPair(_ wd: WindingDistribution) -> (Rung1CalibrationReport, Rung1CalibrationReport) {
            let probs = wd.primeCounts.map { Double($0) / Double(wd.totalPrimes) }
            let sigma2 = Double(wd.lengthM) / 24.0
            let s = evaluateDiscreteGaussianCalibration(probs: probs, wMin: wd.wMin, sigma2: sigma2)
            let cRaw = probs.withUnsafeBufferPointer {
                ergentics.evaluate_discrete_gaussian_calibration($0.baseAddress, $0.count, wd.wMin, sigma2)
            }
            return (s, fromCxxCalibration(cRaw))
        }
        let (s12, c12) = calPair(w12)
        let (s24, c24) = calPair(w24)
        let (s40, c40) = calPair(w40)

        func calDelta(_ a: Rung1CalibrationReport, _ b: Rung1CalibrationReport) -> Double {
            max(
                max(abs(a.totalVariation - b.totalVariation), abs(a.klDivergence - b.klDivergence)),
                max(abs(a.ksDistance - b.ksDistance), max(abs(a.wasserstein1 - b.wasserstein1), abs(a.excessKurtosis - b.excessKurtosis)))
            )
        }
        let maxD = max(calDelta(s12, c12), max(calDelta(s24, c24), calDelta(s40, c40)))
        let monotoneTV = s40.totalVariation < s24.totalVariation && s24.totalVariation < s12.totalVariation
        let monotoneKurt = abs(s40.excessKurtosis) < abs(s24.excessKurtosis) && abs(s24.excessKurtosis) < abs(s12.excessKurtosis)
        let edgeworthOK = 40.0 * abs(s40.excessKurtosis) < 10.0 && abs(s40.skewness) < 1e-12 && abs(s40.variance - 40.0 / 24.0) < 1e-3
        let ok = s40.code == .ok && c40.code == .ok && monotoneTV && monotoneKurt && edgeworthOK && maxD < 1e-12

        let item = TripleCheckItem(
            id: "P-1/C-2", category: "P", passed: ok, maxDelta: maxD,
            detail: String(format: "m=40 TV=%.5f KL=%.5f ex_kurt=%.4f (m*|k|=%.2f<10) delta=%.2e", s40.totalVariation, s40.klDivergence, s40.excessKurtosis, 40.0 * abs(s40.excessKurtosis), maxD)
        )
        return (item, s12, s24, s40)
    }

    public static func checkFluxWindowAndEDO() -> (TripleCheckItem, FluxWindowReport, EDOComparisonReport) {
        let fwS = evaluateFluxWindow()
        let fwC = ergentics.evaluate_flux_window()
        var cycMatch = true
        for n: Int32 in 1...12 {
            if fwS.cyclicRamanujan[Int(n)] != ergentics.flux_cyclic_is_ramanujan(fwC, n) {
                cycMatch = false
            }
        }
        let edoS = evaluateEDORamanujanComparison()
        let edoC = ergentics.evaluate_edo_ramanujan_comparison()

        let delta = max(
            max(abs(fwS.edgeLow - fwC.edge_low), abs(fwS.maxEigAtPi - fwC.max_eig_at_pi)),
            max(abs(edoS.lambdaMax12 - edoC.lambda_max_12), max(abs(edoS.lambdaMax31 - edoC.lambda_max_31), abs(edoS.lambdaMax53 - edoC.lambda_max_53)))
        )
        let ok = cycMatch &&
                 fwS.cyclicRamanujan[1] && fwS.cyclicRamanujan[2] && !fwS.cyclicRamanujan[3] && !fwS.cyclicRamanujan[12] &&
                 fwS.minEigAt2PiOver3 < 1e-12 &&
                 edoS.ramanujan12 && edoS.ramanujan31 && !edoS.ramanujan53 &&
                 edoS.ramanujan12 == edoC.ramanujan_12 && edoS.ramanujan31 == edoC.ramanujan_31 && edoS.ramanujan53 == edoC.ramanujan_53 &&
                 delta < 1e-12
        let item = TripleCheckItem(
            id: "C-3/NEG-M2/M3", category: "Correspondence", passed: ok, maxDelta: delta,
            detail: String(format: "phi_c=%.4f dirac=%.1e 12/31/53=%.4f/%.4f/%.4f delta=%.2e", fwS.edgeLow, fwS.minEigAt2PiOver3, edoS.lambdaMax12, edoS.lambdaMax31, edoS.lambdaMax53, delta)
        )
        return (item, fwS, edoS)
    }

    public static func checkRCTs() -> (items: [TripleCheckItem], sc: SigningCensusReport, rct2: TwoAdicRCTReport, rct3: WindingNullRCTReport) {
        // RCT-1: Exact 8192 signing census.
        let scS = runSigningCensusExact()
        let scC = ergentics.run_signing_census_exact()
        let scDelta = max(abs(scS.bestMaxEig - scC.best_max_eig), abs(scS.voiceParityMaxEig - scC.voice_parity_max_eig))
        let scOK = scS.passed && scC.passed &&
                   scS.ramanujanNontrivial == scC.ramanujan_nontrivial &&
                   scS.voiceParityRank == scC.voice_parity_rank &&
                   scS.voiceParityRank == 7372 && scDelta < 1e-12
        let item1 = TripleCheckItem(
            id: "RCT-1/NEG-M9", category: "RCT", passed: scOK, maxDelta: scDelta,
            detail: String(format: "ram=%lld/8191 rank=%lld/8192 best=%.6f vp=%.6f delta=%.2e", scS.ramanujanNontrivial, scS.voiceParityRank, scS.bestMaxEig, scS.voiceParityMaxEig, scDelta)
        )

        // RCT-2: Keyed 2-adic slope doubling vs non-fixed control discs.
        let kTreat = PRNGKey(suite: "prime-cadences", experiment: "RCT-2-treat", trialIndex: 0, seed: 20261125)
        let kCtrl = PRNGKey(suite: "prime-cadences", experiment: "RCT-2-ctrl", trialIndex: 0, seed: 20261125)
        let r2S = runTwoAdicSlopeRCT(treatmentKey: kTreat, controlKey: kCtrl, nSamples: 2000)
        let r2C = ergentics.run_two_adic_slope_rct(toCxxKey(kTreat), toCxxKey(kCtrl), 2000)
        let r2OK = r2S.passed && r2C.passed &&
                   r2S.treatmentSlope2Hits == r2C.treatment_slope2_hits &&
                   r2S.controlSlope1Hits == r2C.control_slope1_hits
        let item2 = TripleCheckItem(
            id: "RCT-2/NEG-M10", category: "RCT", passed: r2OK, maxDelta: r2OK ? 0.0 : 1.0,
            detail: "treat_slope2=\(r2S.treatmentSlope2Hits)/\(r2S.treatmentSamples) ctrl_slope1=\(r2S.controlSlope1Hits)/\(r2S.controlSamples)"
        )

        // RCT-3: Keyed MC non-backtracking walk null vs exact N_12(w)/N_12 and pi(12,w)/pi(12).
        let kRct3 = PRNGKey(suite: "prime-cadences", experiment: "RCT-3-winding-null", trialIndex: 0, seed: 20261125)
        let r3S = runWindingNullRCT(m: 12, key: kRct3, nWalks: 100_000)
        let r3C = ergentics.run_winding_null_rct(12, toCxxKey(kRct3), 100_000)
        let r3Delta = max(abs(r3S.mcVsExactClosedTV - r3C.mc_vs_exact_closed_tv), abs(r3S.exactClosedVsPrimeTV - r3C.exact_closed_vs_prime_tv))
        let r3OK = r3S.passed && r3C.passed &&
                   r3S.closedWalksObserved == r3C.closed_walks_observed &&
                   r3S.nonMultiple12Observed == 0 && r3C.non_multiple_12_observed == 0 &&
                   r3S.exactClosedVsPrimeTV > 0.0 && r3Delta < 1e-14
        let item3 = TripleCheckItem(
            id: "RCT-3", category: "RCT", passed: r3OK, maxDelta: r3Delta,
            detail: String(format: "closed=%lld/100000 mc_tv=%.5f mobius_tv=%.5f delta=%.2e", r3S.closedWalksObserved, r3S.mcVsExactClosedTV, r3S.exactClosedVsPrimeTV, r3Delta)
        )

        return ([item1, item2, item3], scS, r2S, r3S)
    }

    // MARK: - Seam (D <-> R <-> P) Triple-Check

    public static func checkSeamReplayAndHandoff(cal12: Rung1CalibrationReport, cal40: Rung1CalibrationReport) -> TripleCheckItem {
        // 1. Word-for-word bit-exact KeyedPRNG lockstep between Pure Swift 6.4 and C++20.
        let key = PRNGKey(suite: "prime-cadences", experiment: "seam-replay", trialIndex: 7, seed: 20261125)
        var swRng = KeyedPRNG(key: key)
        var cxRng = ergentics.cxx_make_prng(key.suiteHash, key.experimentHash, key.trialIndex, key.seed)
        var prngMismatches = 0
        for _ in 0..<256 {
            if swRng.nextUInt64() != ergentics.cxx_prng_next_u64(&cxRng) { prngMismatches += 1 }
            if swRng.nextBounded(72) != ergentics.cxx_prng_next_bounded(&cxRng, 72) { prngMismatches += 1 }
            if swRng.nextUnitDouble().bitPattern != ergentics.cxx_prng_next_unit(&cxRng).bitPattern { prngMismatches += 1 }
        }

        // 2. Cross-language guarded P -> R -> D seam handoff (Swift cal -> C++ gate AND C++ cal -> Swift gate).
        let cov = buildTonnetzCovariancePerStep()
        let spiked = [1.0, 2.5, 2.5, 1.0]
        let pol = SeamPolicy(maxTV: 0.05, maxAbsExcessKurtosis: 0.25, minCovEigenvalue: 1e-6, fluxMin: 0.0, fluxMax: 6.283185307179586)
        let polC = toCxxPolicy(pol)
        let cal40C = toCxxCalibration(cal40)
        let cal12C = toCxxCalibration(cal12)

        let okS = guardedFluxKernelHandoff(calibration: cal40, cov2x2RowMajor: cov, fluxPhi: Double.pi, policy: pol)
        let okC = cov.withUnsafeBufferPointer { ergentics.guarded_flux_kernel_handoff(cal40C, $0.baseAddress, Double.pi, polC) }

        let badCovS = guardedFluxKernelHandoff(calibration: cal40, cov2x2RowMajor: spiked, fluxPhi: Double.pi, policy: pol)
        let badCovC = spiked.withUnsafeBufferPointer { ergentics.guarded_flux_kernel_handoff(cal40C, $0.baseAddress, Double.pi, polC) }

        let badKurtS = guardedFluxKernelHandoff(calibration: cal12, cov2x2RowMajor: cov, fluxPhi: Double.pi, policy: pol)
        let badKurtC = cov.withUnsafeBufferPointer { ergentics.guarded_flux_kernel_handoff(cal12C, $0.baseAddress, Double.pi, polC) }

        let badOODS = guardedFluxKernelHandoff(calibration: cal40, cov2x2RowMajor: cov, fluxPhi: -0.5, policy: pol)
        let badOODC = cov.withUnsafeBufferPointer { ergentics.guarded_flux_kernel_handoff(cal40C, $0.baseAddress, -0.5, polC) }

        let outDelta = abs(okS.deterministicOutput - okC.deterministic_output)
        let gatesOK = okS.allowed && okC.allowed && okS.code == .ok && okC.code == 0 &&
                      !badCovS.allowed && !badCovC.allowed && badCovS.code == .rejectIndefiniteCov && badCovC.code == 4 &&
                      !badKurtS.allowed && !badKurtC.allowed && badKurtS.code == .rejectUncalibratedKurtosis && badKurtC.code == 3 &&
                      !badOODS.allowed && !badOODC.allowed && badOODS.code == .rejectOODFlux && badOODC.code == 5

        let ok = prngMismatches == 0 && gatesOK && outDelta < 1e-12
        return TripleCheckItem(
            id: "SEAM-1", category: "Seam", passed: ok, maxDelta: max(outDelta, Double(prngMismatches)),
            detail: String(format: "prng_bit_diff=%d handoff_out=%.6f delta=%.2e", prngMismatches, okS.deterministicOutput, outDelta)
        )
    }

    // MARK: - ADPIE Cycle 2B: Section 7 & Eisenstein Arithmetic Triple-Check

    public static func checkSection7AndArithmetic() -> [TripleCheckItem] {
        // 1. Thm 7.7: Sandpile group exact Bareiss + Iliopoulos-Bezout modular SNF + F_p nullity guard.
        let snfS = computeSandpileGroupSNF()
        let snfC = ergentics.compute_sandpile_group_snf()
        var snfMatch = snfS.passed && snfC.passed &&
                       snfS.nontrivialCount == snfC.nontrivial_count &&
                       snfS.groupOrder == snfC.group_order &&
                       snfS.divisibilityChainOK && snfC.divisibility_chain_ok
        for i: Int32 in 0..<snfS.nontrivialCount {
            if snfS.invariantFactors[Int(i)] != ergentics.sandpile_factor(snfC, i) { snfMatch = false }
        }
        let itemSNF = TripleCheckItem(
            id: "S7-1/Thm7.7", category: "D", passed: snfMatch, maxDelta: snfMatch ? 0.0 : 1.0,
            detail: "K(X)=\(snfS.invariantFactors) |K|=\(snfS.groupOrder) F_p_ranks_ok=\(snfS.divisibilityChainOK)"
        )

        // 2. Prop 7.2 & Thm 7.8 (NEG-M7): Aut(X), 13 involutions, Dhar-burning gonality = 6.
        let gonS = verifyGonalityAndAutomorphisms()
        let gonC = ergentics.verify_gonality_and_automorphisms()
        let gonMatch = gonS.passed && gonC.passed &&
                       gonS.autOrder == gonC.aut_order &&
                       gonS.involutionCount == gonC.involution_count &&
                       gonS.treeQuotientCount == gonC.tree_quotient_count &&
                       gonS.minQuotientBetti == gonC.min_quotient_betti &&
                       gonS.divisorsDegLe5Tested == gonC.divisors_deg_le5_tested &&
                       gonS.rank1DegLe5Found == gonC.rank1_deg_le5_found &&
                       gonS.computedGonality == gonC.computed_gonality
        let itemGon = TripleCheckItem(
            id: "S7-2/NEG-M7", category: "D", passed: gonMatch, maxDelta: gonMatch ? 0.0 : 1.0,
            detail: "|Aut|=\(gonS.autOrder) inv=\(gonS.involutionCount) trees=\(gonS.treeQuotientCount) min_b1=\(gonS.minQuotientBetti) deg<=5=\(gonS.divisorsDegLe5Tested) gon=\(gonS.computedGonality)"
        )

        // 3. Thm 3.5 & Props 7.9-7.10 (NEG-M5/M6): P_44(u) & F_{2^k} genus-5 complete intersections A, B.
        let f2S = verifyF2CurvesAndWeil()
        let f2C = ergentics.verify_f2_curves_and_weil()
        var f2Match = f2S.passed && f2C.passed &&
                      f2S.cofactorA0Deg4Places == f2C.cofactor_a0_deg4_places
        for i: Int32 in 0..<6 {
            if f2S.p44PointCounts[Int(i)] != ergentics.f2_p44_count(f2C, i) { f2Match = false }
        }
        for i: Int32 in 0..<5 {
            if f2S.curveACounts[Int(i)] != ergentics.f2_curve_a_count(f2C, i) { f2Match = false }
            if f2S.curveBCounts[Int(i)] != ergentics.f2_curve_b_count(f2C, i) { f2Match = false }
        }
        let f2Delta = abs(f2S.weilFactorMaxResidual - f2C.weil_factor_max_residual)
        let itemF2 = TripleCheckItem(
            id: "S7-3/NEG-M5/M6", category: "D", passed: f2Match && f2Delta < 1e-12, maxDelta: f2Delta,
            detail: String(format: "P44=%@ a0_B4=%lld #A=%@ #B=%@ res=%.1e", "\(f2S.p44PointCounts)", f2S.cofactorA0Deg4Places, "\(f2S.curveACounts)", "\(f2S.curveBCounts)", f2S.weilFactorMaxResidual)
        )

        // 4. Prop 3.7 (NEG-M1): 12 Tonnetz-axis Eisenstein multiplier rings.
        let eisS = verifyEisenstein12Maps()
        let eisC = ergentics.verify_eisenstein_12_maps()
        let eisMatch = eisS.passed && eisC.passed &&
                       eisS.tonnetzMapCount == eisC.tonnetz_map_count &&
                       eisS.minConductor == eisC.min_conductor &&
                       eisS.maxConductor == eisC.max_conductor &&
                       eisS.anyKernelIsIdeal == eisC.any_kernel_is_ideal
        let itemEis = TripleCheckItem(
            id: "S3-1/NEG-M1", category: "D", passed: eisMatch, maxDelta: eisMatch ? 0.0 : 1.0,
            detail: "maps=\(eisS.tonnetzMapCount) conductor=[\(eisS.minConductor),\(eisS.maxConductor)] ideal=\(eisS.anyKernelIsIdeal)"
        )

        // 5. Thms 7.1 & 7.13 (NEG-M8): 13 Schreier generators, Bruhat-Tits ball r<=7, gamma_0 trace obstruction.
        let schS = verifySchottkyGroup()
        let schC = ergentics.verify_schottky_group()
        let schMatch = schS.passed && schC.passed &&
                       schS.schreierCount == schC.schreier_count &&
                       schS.schreierHyperbolic == schC.schreier_hyperbolic &&
                       schS.btBallR7Words == schC.bt_ball_r7_words &&
                       schS.btBallR7Distinct == schC.bt_ball_r7_distinct &&
                       schS.gamma0Tr == schC.gamma0_tr &&
                       schS.gamma0Det == schC.gamma0_det
        let itemSch = TripleCheckItem(
            id: "S7-4/NEG-M8", category: "D", passed: schMatch, maxDelta: schMatch ? 0.0 : 1.0,
            detail: "schreier=\(schS.schreierHyperbolic)/\(schS.schreierCount) BT_r7=\(schS.btBallR7Distinct)/\(schS.btBallR7Words) g0_tr=\(schS.gamma0Tr) g0_det=\(schS.gamma0Det)"
        )

        return [itemSNF, itemGon, itemF2, itemEis, itemSch]
    }

    // MARK: - ADPIE Cycle 4: Original Mathematical Novelties (Theorems A, B, C & NEG-M11)

    public static func checkNoveltyTheorems() -> (items: [TripleCheckItem], edge40: EdgeworthWindingReport, axes40: TonnetzAxisCumulantReport) {
        // 1. Novelty 1 (Theorem A, Theorem B, Corollary B.1, NEG-M11):
        // Exhaustive check of ALL 3-note chord classes under maximal S_max(c_0) for 5 <= N <= 32.
        let tunS = verifyNoveltyTuneClassification(nMax: 32)
        let tunC = ergentics.verify_novelty_tune_classification(32)
        let tunMatch = tunS.passed && tunC.passed &&
                       tunS.chordsTested == tunC.chords_tested &&
                       tunS.maxLinkIntersection == tunC.max_link_intersection &&
                       tunS.tOrbitFailures == tunC.t_orbit_failures &&
                       tunS.tiOctatonicFailures == tunC.ti_octatonic_failures &&
                       tunS.tiUnexpectedFailures == tunC.ti_unexpected_failures &&
                       tunS.negM11Verified && tunC.neg_m11_verified
        let itemTun = TripleCheckItem(
            id: "NOV-1/ThmA+B/NEG-M11", category: "D", passed: tunMatch, maxDelta: tunMatch ? 0.0 : 1.0,
            detail: "N<=32 chords=\(tunS.chordsTested) max|L0∩Lt|=\(tunS.maxLinkIntersection)<=2 T_fail=\(tunS.tOrbitFailures) TI_oct=\(tunS.tiOctatonicFailures)/4 TI_unexp=\(tunS.tiUnexpectedFailures) NEG-M11=\(tunS.negM11Verified)"
        )

        // 2. Novelty 2 (Theorem C, Correspondence C-2' & C-2''):
        // Exact 4th- and 6th-order Edgeworth winding calibration across m = 24 -> 40.
        let e24S = evaluateEdgeworthWindingCalibration(m: 24)
        let e24C = ergentics.evaluate_edgeworth_winding_calibration(24)
        let e40S = evaluateEdgeworthWindingCalibration(m: 40)
        let e40C = ergentics.evaluate_edgeworth_winding_calibration(40)
        let eDelta = max(
            max(abs(e40S.tvGaussian - e40C.tv_gaussian), abs(e40S.tvEdgeworth4 - e40C.tv_edgeworth4)),
            max(abs(e40S.tvEdgeworth6 - e40C.tv_edgeworth6), abs(e40S.mTimesExcessKurtosis - e40C.m_times_excess_kurtosis))
        )
        let eDelta24 = max(abs(e24S.tvEdgeworth4 - e24C.tv_edgeworth4), abs(e24S.tvEdgeworth6 - e24C.tv_edgeworth6))
        let maxEDelta = max(eDelta, eDelta24)
        let edgeOK = e24S.passed && e24C.passed && e40S.passed && e40C.passed &&
                     e40S.tvEdgeworth4 < e24S.tvEdgeworth4 &&
                     e40S.tvEdgeworth6 < e24S.tvEdgeworth6 &&
                     maxEDelta < 1e-13
        let itemEdge = TripleCheckItem(
            id: "NOV-2/C-2'/C-2''", category: "Correspondence", passed: edgeOK, maxDelta: maxEDelta,
            detail: String(format: "m=40 m*k4=%.4f(-8.5) TV0=%.3e TV4=%.3e(%.1fx) TV6=%.3e(%.1fx) delta=%.2e",
                           e40S.mTimesExcessKurtosis, e40S.tvGaussian, e40S.tvEdgeworth4, e40S.tvGain4,
                           e40S.tvEdgeworth6, e40S.tvGain6, maxEDelta)
        )

        // 3. Novelty 2 (Theorem C, 2D Tonnetz Isotropy across armchair W=-u, v and zigzag 4u+3v at m=40).
        let axS = verifyTonnetzAxisCumulants(m: 40)
        let axC = ergentics.verify_tonnetz_axis_cumulants(40)
        let axDelta = max(
            max(abs(axS.mExKurtU - axC.m_ex_kurt_u), abs(axS.mExKurtV - axC.m_ex_kurt_v)),
            max(abs(axS.mExKurtZigzag - axC.m_ex_kurt_zigzag), abs(axS.m2Std6Zigzag - axC.m2_std6_zigzag))
        )
        let axOK = axS.passed && axC.passed &&
                   axS.totalPrimes == axC.total_primes &&
                   axS.badDivisibilityCount == 0 && axC.bad_divisibility_count == 0 &&
                   axDelta < 1e-12
        let itemAx = TripleCheckItem(
            id: "NOV-3/ThmC-2D", category: "P", passed: axOK, maxDelta: axDelta,
            detail: String(format: "m=40 m*k4(u,v,4u+3v)=(%.3f,%.3f,%.3f) spread=%.4f delta=%.2e",
                           axS.mExKurtU, axS.mExKurtV, axS.mExKurtZigzag, axS.maxIsotropySpread4th, axDelta)
        )

        return ([itemTun, itemEdge, itemAx], e40S, axS)
    }

    /// Run the complete Swift++ Triple-Check SWE-sweep across D, R, P, Correspondence, RCT, Seam, Section 7, and Novelty Theorems.
    public static func runFullSuite() -> TripleCheckSuiteReport {
        var items = [TripleCheckItem]()
        items.append(checkSummationAntiCancellation())
        items.append(checkInterleavedPLRMoves())
        let (d3, w12, w24, w40) = checkIharaBassAndExactPrimes()
        items.append(d3)
        let (d4, tune) = checkTuneTheorem(maxLen: 12)
        items.append(d4)
        let (r1, covLMin) = checkRuntimeGlobalInvariants(w40: w40)
        items.append(r1)
        let (p1, cal12, cal24, cal40) = checkRung1Calibration(w12: w12, w24: w24, w40: w40)
        items.append(p1)
        let (c3, fw, edo) = checkFluxWindowAndEDO()
        items.append(c3)
        let (rctItems, sc, rct2, rct3) = checkRCTs()
        items.append(contentsOf: rctItems)
        items.append(checkSeamReplayAndHandoff(cal12: cal12, cal40: cal40))
        items.append(contentsOf: checkSection7AndArithmetic())
        let (novItems, _, _) = checkNoveltyTheorems()
        items.append(contentsOf: novItems)

        return TripleCheckSuiteReport(
            items: items,
            cal12: cal12,
            cal24: cal24,
            cal40: cal40,
            covLambdaMin: covLMin,
            signingCensus: sc,
            twoAdicRCT: rct2,
            windingNullRCT: rct3,
            fluxWindow: fw,
            edoComparison: edo,
            tuneReport: tune
        )
    }
}

