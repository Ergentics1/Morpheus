#pragma once
#include <cstdint>
#include <cstddef>

namespace ergentics {

// Novelty 1 (Theorem A, Theorem B, Corollary B.1, NEG-M11):
// Exhaustive check of ALL 3-note chord classes under maximal legal step sets S_max(c_0)
// for all 5 <= N <= n_max, confirming:
//   - Theorem A: max |L_0 ∩ L_t| <= 2 universally (zero 2-moving-voice collisions)
//   - Theorem B: zero T-orbit failures; ONLY T/I failures are N = 8m octatonic diameters (m, 3m, 4m)
//   - NEG-M11: explicit N = 8, S = {2}, c_0 = {0, 1, 4} prime 4-cycle collision
struct NoveltyTuneClassificationReport {
    int32_t n_max;
    int64_t chords_tested;
    int32_t max_link_intersection;   // expected 2 (Theorem A)
    int64_t t_orbit_failures;        // expected 0 (Theorem B)
    int64_t ti_octatonic_failures;   // expected n_max / 8 (N = 8, 16, ..., 8*floor(n_max/8))
    int64_t ti_unexpected_failures;  // expected 0 (Theorem B completeness)
    bool neg_m11_verified;           // N=8, S={2}, c0={0,1,4} disjoint 4-cycles, tune (3,5,7,1)
    bool passed;
};

// Novelty 2 (Theorem C, Correspondence C-2' and C-2''):
// Exact prime-cadence winding distribution vs Gaussian (C-2), 4th-order Edgeworth (-17/(48m) H4, C-2'),
// and 6th-order Edgeworth (+1469/(2880 m^2) H6 + 289/(4608 m^2) H8, C-2'').
struct EdgeworthWindingReport {
    int32_t length_m;
    int64_t total_primes;
    double variance;
    double var_abs_error;            // |Var(W) - m/24|
    double excess_kurtosis;          // exact kappa_4 / kappa_2^2
    double m_times_excess_kurtosis;  // converges to -17/2 = -8.5 exponentially via Ramanujan gap
    double tv_gaussian;              // C-2  O(1/m)
    double kl_gaussian;              // strictly positive Gaussian KL >= 0
    double jsd_gaussian;             // bounded Jensen-Shannon divergence >= 0
    double tv_edgeworth4;            // C-2' O(1/m^2)
    double jsd_edgeworth4;           // bounded JSD >= 0 (handles clipped tail zeros, NEG-E9)
    double tv_edgeworth6;            // C-2'' O(1/m^3)
    double jsd_edgeworth6;           // bounded JSD >= 0 (handles clipped tail zeros, NEG-E9)
    double tv_gain_4;                // tv_gaussian / tv_edgeworth4
    double tv_gain_6;                // tv_gaussian / tv_edgeworth6
    bool passed;
};

// Novelty 2 (Theorem C, 2D Tonnetz Isotropy & C_6 Hexagonal Symmetry Breaking):
// Exact prime-cadence cumulants across all 3 canonical Tonnetz axes at even length m:
//   - Armchair axis 1 (bond-parallel):      W = -u  (div 12, cos(6*alpha) = -1, kappa_2/m = 1/24)
//   - Armchair axis 2 (bond-parallel):      v       (div 9,  cos(6*alpha) = -1, kappa_2/m = 2/27)
//   - Zigzag axis (bond-perpendicular):     4u + 3v (div 1,  cos(6*alpha) = +1, kappa_2/m = 2)
struct TonnetzAxisCumulantReport {
    int32_t length_m;
    int64_t total_primes;
    int64_t bad_divisibility_count;  // must be 0 on all 3 axes (exact coboundary integrality)
    double k2_over_m_u;              // -> 1/24
    double k2_over_m_v;              // -> 2/27
    double k2_over_m_zigzag;         // -> 2
    double m_ex_kurt_u;              // -> -8.5
    double m_ex_kurt_v;              // -> -8.5
    double m_ex_kurt_zigzag;         // -> -8.5
    double max_isotropy_spread_4th;  // max |m*k4_std - (-8.5)| across all 3 axes
    double m2_std6_u;                // -> 1469/4 = 367.25
    double m2_std6_v;                // -> 1469/4 = 367.25
    double m2_std6_zigzag;           // -> 1471/4 = 367.75
    bool passed;
};

NoveltyTuneClassificationReport verify_novelty_tune_classification(int32_t n_max);
EdgeworthWindingReport evaluate_edgeworth_winding_calibration(int32_t m);
TonnetzAxisCumulantReport verify_tonnetz_axis_cumulants(int32_t m);

} // namespace ergentics
