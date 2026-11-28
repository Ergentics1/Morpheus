// SPDX-License-Identifier: MIT
// Copyright (c) 2026 Ergentics, LLC

use triadic_nauru_rust::*;

fn main() {
    assert!(verify_non_fusion(), "Gate 1 (Non-fusion & normalizer tower) failed");
    let auts = find_nauru_auts();
    assert_eq!(auts.len(), 144, "Gate 2 (|Aut(Y)|=144) failed");
    let (tested, gon_ok) = verify_nauru_gonality_exact();
    assert!(tested == 20_474 && gon_ok, "Gate 3 (Exhaustive Dhar gon(Y)=6) failed");
    assert!(verify_b3_non_congruence_tower(), "Gate 4 (B_3 V_4 non-congruence tower) failed");
    assert!(verify_b5_congruence_and_noncongruence_towers(), "Gate 5 (B_5 x=5/2 congruence & x=1/2 non-congruence, NEG-M23) failed");
    assert!(verify_all_18_shimura_levels_excluded(), "Gate 6 (0/19 2-adic Borel Shimura levels) failed");
    assert!(verify_eisenstein_nauru_and_su2(), "Gate 7 (Eisenstein-Nauru {{6,3}}_(2,2) & SU(2) Wilson) failed");
    let (z_tested, z_gon) = verify_dic6_tropical_invariants_exact();
    assert!(z_tested == 157_166 && z_gon == 8, "Gate 8 (Dic_6 Z 43 involutions & exact gon(Z)=8) failed");
    assert!(verify_hurwitz_b2_dic6_k44(), "Gate 9 (Hurwitz B_2 Dic_6 32 surj / K_{{4,4}} / index 3) failed");
    assert!(verify_all_19_3adic_shimura_levels_excluded(), "Gate 10 (0/19 3-adic Borel Shimura Manin T_3) failed");
    let pi_y = verify_nauru_hashimoto_prime_cadences();
    assert_eq!(pi_y[6], 28_560, "Gate 11 (NEG-M24 pi_Y(18)=28560) failed");
    assert_eq!(pi_y[8], 380_664, "Gate 11 (NEG-M24 pi_Y(22)=380664) failed");
    println!(
        "TriadicNauru Rust Verifier: ALL 11 CORE SUITES PASS (|Aut(Y)|=144, pi_Y(18)=28560, pi_Y(22)=380664, gon(Y)=6 [{tested}], B_3+B_5 x=5/2 cong & x=1/2 non-cong, 0/19 2-adic Shimura, Eis-Nauru 36/36, Dic_6 43 invs & gon(Z)=8 [{z_tested}], Hurwitz B_2 32 surj -> K_{{4,4}} idx 3, 0/19 3-adic Shimura)."
    );
}
