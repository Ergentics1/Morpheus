#pragma once
#include <cstdint>
#include <cstddef>

namespace ergentics {

// Theorem 7.7: Exact integer Smith Normal Form of reduced Tonnetz Laplacian (Sandpile / Critical Group K(X)).
struct SandpileSNFReport {
    int32_t nontrivial_count;        // expected 5
    int64_t invariant_factors[8];    // expected [2, 2, 8, 736, 6624]
    int64_t group_order;             // expected 156,008,448 = 2^15 * 3^2 * 23^2
    bool divisibility_chain_ok;      // R-Type exact d_i | d_{i+1} check across all 23 factors
    bool passed;
};

// Proposition 7.2 & Theorem 7.8 (NEG-M7): Exhaustive Aut(X), 13 involutions (Chan's criterion),
// and exact Dhar-burning Baker-Norine divisorial gonality gon(X) = 6.
struct GonalityAutReport {
    int32_t aut_order;               // expected 24 (Prop 7.2)
    int32_t involution_count;        // expected 13
    int32_t tree_quotient_count;     // expected 0 (Chan's criterion -> non-hyperelliptic)
    int32_t min_quotient_betti;      // >= 1 across all 13 involutions
    int64_t divisors_deg_le5_tested; // 20,475 effective divisors D >= (C) of degree <= 5
    int64_t rank1_deg_le5_found;     // expected 0 -> gon(X) >= 6
    bool witness_deg6_rank1_ok;      // 2C + 2Am + Db + Abm has r(D) >= 1 -> gon(X) = 6
    int32_t computed_gonality;       // expected 6
    bool passed;
};

// Proposition 7.9 (NEG-M5) & Proposition 7.10 (NEG-M6): Exact P_44(u) Weil polynomial point counts,
// genus-5 cofactor obstruction (a=0 -> -1 degree-4 places), and direct F_{2^k} point counts on curves A, B in P^4.
struct F2CurvesReport {
    int64_t p44_point_counts[6];     // N_1..N_6 = [3, 39, 9, 75, 33, 27] -> N_6 < N_2 (NEG-M5)
    int64_t cofactor_a0_deg4_places; // expected -1 (NEG-M6 obstruction)
    int64_t curve_a_counts[5];       // #A(F_{2^k}) for k = 1..5
    int64_t curve_b_counts[5];       // #B(F_{2^k}) for k = 1..5
    int64_t expected_a_counts[5];    // from L_A = (1 - u + 2u^2) * L_4
    int64_t expected_b_counts[5];    // from L_B = (1 + u + 2u^2) * L_4
    double weil_factor_max_residual; // max |det(I-uA+2u^2I) - (1-u)(1-2u)(1+u)(1+2u)P_44(u)|
    bool passed;
};

// Proposition 3.7 (NEG-M1): Exhaustive 12 Tonnetz-axis maps Z[omega] -> Z_12 multiplier ring conductors.
struct Eisenstein12MapsReport {
    int32_t tonnetz_map_count;       // expected 12
    int32_t min_conductor;           // expected 12
    int32_t max_conductor;           // expected 12
    bool any_kernel_is_ideal;        // expected false
    bool passed;
};

// Theorem 7.1 & Theorem 7.13 (NEG-M8): 13 Schreier generators of K, Bruhat-Tits ball radius-7
// simple transitivity (382 words -> 382 distinct vertices), and exact gamma_0 trace obstruction.
struct SchottkyGroupReport {
    int32_t schreier_count;          // expected 13
    int32_t schreier_hyperbolic;     // expected 13
    int32_t schreier_in_kernel;      // expected 13
    int32_t bt_ball_r7_words;        // expected 382
    int32_t bt_ball_r7_distinct;     // expected 382 (simple transitivity)
    int64_t gamma0_tr;               // expected 85
    int64_t gamma0_det;              // expected 256
    bool gamma0_tau_gt_4;            // 85^2 = 7225 > 4*256 = 1024
    bool passed;
};

SandpileSNFReport compute_sandpile_group_snf();
GonalityAutReport verify_gonality_and_automorphisms();
F2CurvesReport verify_f2_curves_and_weil();
Eisenstein12MapsReport verify_eisenstein_12_maps();
SchottkyGroupReport verify_schottky_group();

// Swift C++ interop helpers for fixed-size struct array access.
inline int64_t sandpile_factor(const SandpileSNFReport& r, int32_t i) {
    return (i >= 0 && i < 8) ? r.invariant_factors[i] : 0;
}
inline int64_t f2_p44_count(const F2CurvesReport& r, int32_t i) {
    return (i >= 0 && i < 6) ? r.p44_point_counts[i] : 0;
}
inline int64_t f2_curve_a_count(const F2CurvesReport& r, int32_t i) {
    return (i >= 0 && i < 5) ? r.curve_a_counts[i] : 0;
}
inline int64_t f2_curve_b_count(const F2CurvesReport& r, int32_t i) {
    return (i >= 0 && i < 5) ? r.curve_b_counts[i] : 0;
}

} // namespace ergentics
