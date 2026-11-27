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
    assert!(verify_all_18_shimura_levels_excluded(), "Gate 5 (0/19 Borel Shimura levels) failed");
    println!(
        "TriadicNauru Rust Verifier: ALL 5 CORE SUITES PASS (|Aut|=144, Dhar={tested} deg<=5 -> gon=6, B_3 mod-5 joint=8640, 0/19 Shimura)."
    );
}
