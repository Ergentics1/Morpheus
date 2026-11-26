#pragma once

#include <cstdint>

namespace ergentics {

/// Complete audit report for Novelty 3 (Theorem D — Three-Pincer Hilbert Class Field Obstruction)
/// and independent from-scratch Poitou-Odlyzko verification of Theorem 7.19(b).
struct TheoremDPincerReport {
    bool passed;
    bool quadrature_self_check_ok;
    double q_explicit_formula_lb;       // Weil-Poitou lower bound on Q at b=2.0 (must lie in [-1e-4, 0])
    double tail15_lb_b42;               // Universal monotone tail LB at n=15, b=4.2
    double tail15_ub;                   // Theorem 7.19(b) UB at n=15
    double tail15_e_minus_f2;           // E(4.2) - f_2(4.2) > 0 guarantees strict monotonicity for all n >= 15
    int32_t deg9_to_14_survivors;       // Must be 0 (unconditionally kills n = 9..14, sharpening n<=14 -> n<=8)
    double worst_deg9_margin;           // Tightest kill margin in degree 9 (u=4, odd_B, h_F=1)
    double worst_deg10_margin;          // Tightest kill margin in degree 10 (u=4, even, h_F=1)
    int32_t deg7_max_surviving_u;       // Must be 4 (only u in {1, 2, 4} with h_F = 1 survive)
    int32_t deg7_hge2_survivors;        // Must be 0 (forces h_F = 1 for all n = 7)
    double deg7_max_root_disc;          // Collapsed root-discriminant ceiling for n = 7 (14.8556...)
    int32_t deg8_max_surviving_u;       // Must be 4 (only u in {1, 2, 4} with h_F = 1 survive)
    int32_t deg8_hge2_survivors;        // Must be 0 (forces h_F = 1 for all n = 8)
    double deg8_max_root_disc;          // Collapsed root-discriminant ceiling for n = 8 (14.7518...)
    int32_t deg6_max_surviving_u;       // Must be 8 (kills u in {16, 32} unconditionally)
    int32_t deg6_u16_h1_dead;           // 1 if n=6, u=16, h_F=1 killed (via L_v deg 48 at b=6.0)
    int32_t deg6_u16_hge2_dead;         // 1 if n=6, u=16, h_F>=2 killed (via codim-3 subfield deg>=96, rho1>=1/6)
    double deg6_u16_h1_margin;          // Exact margin LB - UB at n=6, u=16, h_F=1 (~+0.013630)
    double deg6_u16_hge2_margin;        // Exact margin LB - UB at n=6, u=16, h_F>=2 (~+0.3734)
    double deg6_old_disc_ceiling;       // Prior Open (2) ceiling at u=32 (~6.673e7)
    double deg6_new_disc_ceiling;       // Theorem D collapsed ceiling at u=8 (~2.648e7)
};

/// Exhaustive genus-13 Shimura curve enumeration (Theorem 7.11 & NEG-E10 erratum).
struct ShimuraGenus13Report {
    bool passed;
    int32_t total_pairs;                // Exact exhaustive count: 19 (vs 18 in paper due to phi<=168 cutoff)
    int32_t torsion_free_pairs;         // Exact count with e_2 = e_3 = 0: 11
    int32_t neg_e10_detected;           // 1 iff (D=690, N=1) found with phi=176 > 168, e_2=0, e_3=8, g=13
    int32_t neg_e10_phi;                // 176
    int32_t neg_e10_e2;                 // 0
    int32_t neg_e10_e3;                 // 8
    int32_t gamma_h_count;              // Exact count of Gamma_H genus-13 cases: 4
};

/// Exact Siegel real-quadratic scan (Prop 7.18(a)), PGL_2(F_8) census (Prop 7.17(b)),
/// and Hamilton trace obstruction check (Prop 7.3).
struct Section7ArithmeticCycle5Report {
    bool passed;
    int32_t quad_split2_scanned;        // Real quadratic fundamental discriminants D <= 1200 with D = 1 mod 8
    int32_t quad_hplus1_solutions;      // Exact count of (D, D'', N) solutions with h_F^+ = 1: 3 (D=41 x2, D=137 x1)
    int32_t quad_d41_solutions;         // 2 (N = v' p_5a, N = v' p_5b)
    int32_t quad_d137_solutions;        // 1 (N = v')
    int32_t pgl2_f8_order;              // 504 = |PGL_2(F_8)|
    int32_t pgl2_f8_order3_count;       // 56 elements of order 3
    int32_t pgl2_f8_order3_free_count;  // 56 (ALL 56 act freely on P^1(F_8) in 3 orbits of size 3)
    int32_t gamma0_powers_obstructed;   // 12/12 powers k=1..12 satisfy tr(gamma0^k)^2 > 4 det(gamma0^k)
};

TheoremDPincerReport verify_theorem_d_pincer();
ShimuraGenus13Report verify_shimura_genus13_census();
Section7ArithmeticCycle5Report verify_section7_arithmetic_cycle5();

} // namespace ergentics
