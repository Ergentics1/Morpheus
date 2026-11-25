#include "ergentics_cxx.hpp"

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <vector>

using namespace ergentics;

namespace {

int g_failed = 0;

void expect(bool cond, const char* msg) {
    if (cond) {
        std::printf("  [PASS] %s\n", msg);
    } else {
        std::printf("  [FAIL] %s\n", msg);
        ++g_failed;
    }
}

} // namespace

int main() {
    std::printf("=== Lane 1: Standalone Pure C++20 SWE-Sweep ===\n");

    // 1. D-Type: Anti-cancellation summation & exact Mobius arithmetic.
    std::vector<double> cancel_seq = {1e16, 1.0, -1e16, 1.0, 1e16, 1.0, -1e16, 1.0};
    SummationSweepResult sw = run_summation_sweep(cancel_seq.data(), cancel_seq.size());
    expect(sw.all_finite && std::abs(sw.naive_forward - 4.0) > 1.0 && std::abs(sw.neumaier - 4.0) < 1e-12,
           "D-Type: catastrophic cancellation trapped in naive_forward and recovered by Neumaier");
    expect(mobius_mu(1) == 1 && mobius_mu(6) == 1 && mobius_mu(4) == 0 && mobius_mu(30) == -1,
           "D-Type: exact Mobius function values");

    // 2. D-Type: First-principles exact prime counts & winding up to m = 40 (no cached JSONs).
    WindingDistribution w6  = compute_exact_winding_distribution(6);
    WindingDistribution w8  = compute_exact_winding_distribution(8);
    WindingDistribution w16 = compute_exact_winding_distribution(16);
    WindingDistribution w40 = compute_exact_winding_distribution(40);
    expect(w6.total_primes == 32 && w8.total_primes == 78 && w16.total_primes == 8196,
           "D-Type: exact pi(6)=32, pi(8)=78, pi(16)=8196 from 72-edge transfer matrix");
    expect(w40.total_primes == 54975717792LL && w40.non_multiple_12_closed == 0,
           "D-Type: exact pi(40)=54,975,717,792 and 0 non-multiple-of-12 closed walks");
    expect(ihara_bass_residual(0.137) < 1e-10 && ihara_bass_residual(0.29) < 1e-10,
           "D-Type: Ihara-Bass determinant identity at multiple u values");

    // 3. D-Type: Tune theorem (Lemma 4.1, Theorem 4.2, negative control NEG-M4) up to m=12.
    TuneCheckReport tune = verify_tune_theorem(12);
    expect(tune.lemma_l1 && tune.lemma_l2 && tune.lemma_l3 && tune.backtrack_counterexample_confirmed,
           "D-Type: Lemmas L1/L2/L3 and NEG-M4 backtracking counterexample confirmed");
    expect(tune.rooted_primes_checked > 0 && tune.decode_failures == 0 && tune.periodic_tune_failures == 0,
           "D-Type: local tune decoder 0 failures across all rooted primes up to m=12");

    // 4. R-Type: Global matrix invariants, off-diagonal spike rejection, NaN poisoning, conservation.
    double gram[4], cov[4];
    build_tonnetz_gram(gram);
    build_tonnetz_covariance_per_step(cov);
    MatrixInvariantReport g_rep = check_symmetric_pd(gram, 2, 1e-12, 1e-12);
    MatrixInvariantReport c_rep = check_symmetric_pd(cov, 2, 1e-12, 1e-12);
    expect(g_rep.code == INV_OK && c_rep.code == INV_OK && c_rep.lambda_min > 0.02,
           "R-Type: Tonnetz Gram G and Cov=(1/2)G^-1 globally PD (Cholesky + Jacobi)");

    double spiked[4] = {1.0, 2.5, 2.5, 1.0}; // positive diagonals, indefinite global matrix!
    MatrixInvariantReport sp_rep = check_symmetric_pd(spiked, 2, 1e-12, 1e-12);
    expect(sp_rep.diagonal_positive && !sp_rep.cholesky_ok && sp_rep.lambda_min < 0.0 &&
           sp_rep.code == INV_NOT_POSITIVE_DEFINITE,
           "R-Type: off-diagonal spike rejected globally despite diag(P) > 0");

    double poisoned[4] = {1.0, std::nan(""), 0.0, 1.0};
    expect(check_symmetric_pd(poisoned, 2, 1e-12, 1e-12).code == INV_NON_FINITE,
           "R-Type: NaN poisoning rejected immediately");

    double lap[576];
    build_laplacian_matrix(lap);
    MatrixInvariantReport l_rep = check_symmetric_psd_nullity(lap, 24, 1, 1e-12, 1e-9);
    expect(l_rep.code == INV_OK && l_rep.zero_eigenvalue_count == 1,
           "R-Type: Laplacian 3I - A is globally PSD with exact nullity 1");

    double twisted[2 * 576];
    build_twisted_adjacency_complex(1.2345, twisted);
    double herm_err = 0.0;
    expect(check_hermitian_complex(twisted, 24, 1e-12, &herm_err),
           "R-Type: twisted adjacency A_phi is globally Hermitian");

    ExactConservationReport cons40 = check_exact_integer_conservation(w40.prime_counts, 17, w40.total_primes);
    expect(cons40.code == INV_OK, "R-Type: exact integer conservation sum_w pi(40,w) == pi(40)");

    // 5. P-Type: Rung-1 distributional calibration & Correspondence error decay (m=12 -> m=40).
    auto cal_for_dist = [](const WindingDistribution& wd) {
        double p[17];
        for (int i = 0; i < 17; ++i) p[i] = static_cast<double>(wd.prime_counts[i]) / static_cast<double>(wd.total_primes);
        return evaluate_discrete_gaussian_calibration(p, 17, wd.w_min, static_cast<double>(wd.length_m) / 24.0);
    };
    Rung1CalibrationReport cal12 = cal_for_dist(compute_exact_winding_distribution(12));
    Rung1CalibrationReport cal24 = cal_for_dist(compute_exact_winding_distribution(24));
    Rung1CalibrationReport cal40 = cal_for_dist(w40);
    expect(cal40.code == INV_OK && cal40.total_variation < cal24.total_variation &&
           cal24.total_variation < cal12.total_variation && cal40.total_variation < 0.02,
           "P-Type: Rung-1 TV distance decays monotonically m=12 -> 24 -> 40");
    expect(std::abs(cal12.skewness) < 1e-12 && std::abs(cal24.skewness) < 1e-12 && std::abs(cal40.skewness) < 1e-12 &&
           std::abs(cal40.excess_kurtosis) < std::abs(cal24.excess_kurtosis) &&
           std::abs(cal24.excess_kurtosis) < std::abs(cal12.excess_kurtosis) &&
           40.0 * std::abs(cal40.excess_kurtosis) < 10.0 &&
           std::abs(cal40.variance - 40.0 / 24.0) < 1e-3,
           "P-Type: Rung-1 Edgeworth O(1/m) excess-kurtosis decay, zero skewness, & variance correspondence C-2");

    // 6. Correspondence C-1/C-3 & EDO threshold (NEG-M2, NEG-M3).
    FluxWindowReport fw = evaluate_flux_window();
    expect(fw.cyclic_ramanujan[1] && fw.cyclic_ramanujan[2] && !fw.cyclic_ramanujan[3] && !fw.cyclic_ramanujan[12] &&
           fw.min_eig_at_2pi_3 < 1e-12,
           "Correspondence C-3 / NEG-M2: cyclic winding covers Ramanujan iff n<=2 & Dirac point at 2pi/3");

    EDOComparisonReport edo = evaluate_edo_ramanujan_comparison();
    expect(edo.ramanujan_12 && edo.ramanujan_31 && !edo.ramanujan_53,
           "Correspondence / NEG-M3: 12-EDO & 31-EDO Ramanujan; 53-EDO fails graph RH");

    // 7. RCT-1 (signing census), RCT-2 (keyed 2-adic slope), & RCT-3 (keyed MC non-backtracking walk null).
    SigningCensusReport sc = run_signing_census_exact();
    expect(sc.passed && sc.voice_parity_rank == 7372,
           "RCT-1 / NEG-M9: exact 8192 signing census (7675 Ramanujan, voice-parity rank 7372)");

    PRNGKey k_treat{fnv1a_64_cstr("prime-cadences"), fnv1a_64_cstr("RCT-2-treat"), 0, 20261125ULL};
    PRNGKey k_ctrl{fnv1a_64_cstr("prime-cadences"), fnv1a_64_cstr("RCT-2-ctrl"), 0, 20261125ULL};
    TwoAdicRCTReport rct2 = run_two_adic_slope_rct(k_treat, k_ctrl, 2000);
    expect(rct2.passed, "RCT-2 / NEG-M10: 2-adic slope 2 on fixed discs vs slope 1 on non-fixed controls");

    PRNGKey k_rct3{fnv1a_64_cstr("prime-cadences"), fnv1a_64_cstr("RCT-3-winding-null"), 0, 20261125ULL};
    WindingNullRCTReport rct3 = run_winding_null_rct(12, k_rct3, 100000);
    expect(rct3.passed && rct3.non_multiple_12_observed == 0 && rct3.exact_closed_vs_prime_tv > 0.0,
           "RCT-3: keyed MC closed walks match exact N_12(w)/N_12 null & isolate Mobius primitivity correction");

    // 8. Seam (D <-> R <-> P): bit-exact keyed PRNG & guarded P->R->D boundary.
    KeyedPRNG r1 = KeyedPRNG::from_key(k_treat);
    KeyedPRNG r2 = KeyedPRNG::from_key(k_treat);
    bool replay_ok = true;
    for (int i = 0; i < 64; ++i) {
        if (r1.next_u64() != r2.next_u64()) replay_ok = false;
    }
    expect(replay_ok, "Seam (D <-> P): keyed PRNG bit-exact replay");

    SeamPolicy pol{0.05, 0.25, 1e-6, 0.0, 6.283185307179586};
    SeamDecision ok_dec = guarded_flux_kernel_handoff(cal40, cov, 3.141592653589793, pol);
    SeamDecision bad_cov = guarded_flux_kernel_handoff(cal40, spiked, 3.141592653589793, pol);
    SeamDecision bad_ood = guarded_flux_kernel_handoff(cal40, cov, -1.0, pol);
    SeamDecision bad_kurt = guarded_flux_kernel_handoff(cal12, cov, 3.141592653589793, pol);
    Rung1CalibrationReport bad_cal = cal40;
    bad_cal.total_variation = 0.40;
    SeamDecision bad_tv = guarded_flux_kernel_handoff(bad_cal, cov, 3.141592653589793, pol);
    expect(ok_dec.allowed && ok_dec.code == SEAM_OK &&
           !bad_cov.allowed && bad_cov.code == SEAM_REJECT_INDEFINITE_COV &&
           !bad_ood.allowed && bad_ood.code == SEAM_REJECT_OOD_FLUX &&
           !bad_kurt.allowed && bad_kurt.code == SEAM_REJECT_UNCALIBRATED_KURTOSIS &&
           !bad_tv.allowed && bad_tv.code == SEAM_REJECT_UNCALIBRATED_TV,
           "Seam (P -> R -> D): guarded handoff allows calibrated PD m=40 and blocks indefinite/OOD/kurtosis/TV violations");

    // 9. ADPIE Cycle 2B: Section 7 & Eisenstein exact verifiers.
    SandpileSNFReport snf = compute_sandpile_group_snf();
    expect(snf.passed && snf.group_order == 156008448LL,
           "Thm 7.7: exact 23x23 Smith Normal Form K(X) = Z/2+Z/2+Z/8+Z/736+Z/6624 (|K|=156,008,448)");

    GonalityAutReport gon = verify_gonality_and_automorphisms();
    expect(gon.passed && gon.aut_order == 24 && gon.involution_count == 13 &&
           gon.tree_quotient_count == 0 && gon.computed_gonality == 6,
           "Prop 7.2 & Thm 7.8 / NEG-M7: |Aut(X)|=24, 13 involutions (0 tree quotients), Dhar gon(X)=6");

    F2CurvesReport f2 = verify_f2_curves_and_weil();
    expect(f2.passed && f2.p44_point_counts[5] == 27 && f2.cofactor_a0_deg4_places == -1,
           "Thm 3.5 & Props 7.9-7.10 / NEG-M5/M6: P_44 N_6=27<N_2=39, a=0 place=-1, & F_{2^k} counts on A,B (k<=5)");

    Eisenstein12MapsReport eis = verify_eisenstein_12_maps();
    expect(eis.passed,
           "Prop 3.7 / NEG-M1: all 12 Tonnetz-axis maps Z[omega]->Z_12 have multiplier conductor 12 (0 ideals)");

    SchottkyGroupReport sch = verify_schottky_group();
    expect(sch.passed && sch.bt_ball_r7_distinct == 382 && sch.gamma0_tr == 85 && sch.gamma0_det == 256,
           "Thms 7.1 & 7.13 / NEG-M8: 13 hyperbolic Schreier gens, 382 distinct BT r<=7 vertices, tau(g0)=7225/256>4");

    // 10. ADPIE Cycle 4: Original Novelty Theorems (Theorems A, B, C & NEG-M11).
    NoveltyTuneClassificationReport nov_tune = verify_novelty_tune_classification(32);
    expect(nov_tune.passed && nov_tune.max_link_intersection == 2 &&
           nov_tune.t_orbit_failures == 0 && nov_tune.ti_octatonic_failures == 4 &&
           nov_tune.ti_unexpected_failures == 0 && nov_tune.neg_m11_verified,
           "Novelty 1 (Thms A & B / NEG-M11): N<=32 max|L0∩Lt|=2, 0 T-fails, exact 4 octatonic T/I fails, NEG-M11 verified");

    EdgeworthWindingReport edge40 = evaluate_edgeworth_winding_calibration(40);
    expect(edge40.passed && edge40.tv_gain_4 > 10.0 && edge40.tv_gain_6 > 70.0 &&
           std::fabs(edge40.m_times_excess_kurtosis - (-8.5)) < 0.01,
           "Novelty 2 (Thm C / C-2' & C-2''): m=40 m*k4=-8.495 vs -17/2, Edgeworth TV gains >10x (4th) and >70x (6th)");

    TonnetzAxisCumulantReport ax40 = verify_tonnetz_axis_cumulants(40);
    expect(ax40.passed && ax40.bad_divisibility_count == 0 && ax40.max_isotropy_spread_4th < 0.02,
           "Novelty 2 (Thm C 2D Isotropy): m=40 exact coboundaries & universal -17/(2m) kurtosis across W=-u, v, 4u+3v");

    std::printf("=== Lane 1 C++20 Result: %s ===\n", g_failed == 0 ? "ALL PASS" : "FAILURES");
    return g_failed == 0 ? 0 : 1;
}

