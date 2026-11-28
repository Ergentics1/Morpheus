use triadic_3adic_frontier_rust::{
    verify_r1_nauru_hashimoto_tplr_gonality,
    verify_r2_rational_b3_b5_level_3p5,
    verify_r3_real_quad_cubic_and_q7_congruence,
    verify_r4_dic6_cayley_cadences_scramble_and_exhaustive_dhar,
    verify_r5_all80_crt_left_mult_hurwitz_and_riehm,
    verify_r6_genus25_and_poitou_odlyzko,
};

fn main() {
    println!("Running Paper PC-III Pure-Rust Zero-Crate Verification Suite (6 Core Suites)...");
    verify_r1_nauru_hashimoto_tplr_gonality();
    println!("  [PASS] R1: Nauru Hashimoto pi_Y(6..24), NEG-M24 corridor, <T,P,L,R> 6/24 & 168-cut star scramble");
    verify_r2_rational_b3_b5_level_3p5();
    println!("  [PASS] R2: Rational B_3(3/2), B_5(5/2) CONG 3P_5, & B_5(1/2) exact Table 2 adjoints");
    verify_r3_real_quad_cubic_and_q7_congruence();
    println!("  [PASS] R3: 6 real-quadratic & 4 cubic moduli + Q(sqrt(7)) O_7^max level (3) CONG (576, 144/144)");
    verify_r4_dic6_cayley_cadences_scramble_and_exhaustive_dhar();
    println!("  [PASS] R4: Dic_6 18 Cayley, pi_Z(4..16), 43 inv, 0/98,280 deg-6 & 0/475,020 deg-7 Dhar, S_4 & D_8");
    verify_r5_all80_crt_left_mult_hurwitz_and_riehm();
    println!("  [PASS] R5: All 5 Dic_6 curves 0/80 CRT left-mult, unique C_3, Hurwitz L_8/{{+-1}}=64 & O_70^1 Riehm mod 8");
    verify_r6_genus25_and_poitou_odlyzko();
    println!("  [PASS] R6: Poitou-Odlyzko GL-64/128 strict positivity, anti-facade rejection & degree-8 gap");
    println!("Summary: 6/6 Paper PC-III Pure-Rust core suites PASS.");
}
