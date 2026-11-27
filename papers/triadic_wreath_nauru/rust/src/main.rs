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
    assert!(verify_all_18_shimura_levels_excluded(), "Gate 5 (0/19 2-adic Borel Shimura levels) failed");
    assert!(verify_eisenstein_nauru_and_su2(), "Gate 6 (Eisenstein-Nauru {{6,3}}_(2,2) & SU(2) Wilson) failed");
    assert!(verify_hurwitz_b2_dic6_k44(), "Gate 7 (Hurwitz B_2 Dic_6 32 surj / K_{{4,4}} / index 3) failed");
    assert!(verify_all_19_3adic_shimura_levels_excluded(), "Gate 8 (0/19 3-adic Borel Shimura Manin T_3) failed");
    println!(
        "TriadicNauru Rust Verifier: ALL 8 CORE SUITES PASS (|Aut|=144, Dhar={tested} deg<=5 -> gon=6, B_3 mod-5=8640, 0/19 2-adic Shimura, Eis-Nauru 36/36, Hurwitz B_2 32 surj -> K_{{4,4}} idx 3, 0/19 3-adic Shimura)."
    );
}
