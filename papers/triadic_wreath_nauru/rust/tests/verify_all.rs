// SPDX-License-Identifier: MIT
// Copyright (c) 2026 Ergentics, LLC

use triadic_nauru_rust::*;

#[test]
fn test_d1_non_fusion_and_normalizer_tower() {
    assert!(verify_non_fusion());
}

#[test]
fn test_d2_nauru_aut_order_144_and_involutions() {
    let auts = find_nauru_auts();
    assert_eq!(auts.len(), 144);
    let invs = auts.iter().filter(|g| order24(g) == 2).count();
    assert_eq!(invs, 39);
}

#[test]
fn test_d4_exhaustive_dhar_gonality_six() {
    let (tested, ok) = verify_nauru_gonality_exact();
    assert_eq!(tested, 20_474);
    assert!(ok);
}

#[test]
fn test_d6_d7_b3_arithmetic_non_congruence_tower() {
    assert!(verify_b3_non_congruence_tower());
}

#[test]
fn test_d7b_b5_congruence_x52_and_noncongruence_x12() {
    assert!(verify_b5_congruence_and_noncongruence_towers());
}

#[test]
fn test_d8_zero_pari_manin_t2_all_18_levels_excluded() {
    assert!(verify_all_18_shimura_levels_excluded());
}

#[test]
fn test_d9b_dic6_tropical_43_involutions_and_exact_gonality_eight() {
    let (checked, gon) = verify_dic6_tropical_invariants_exact();
    assert_eq!(checked, 157_166);
    assert_eq!(gon, 8);
}

#[test]
fn test_seam_splitmix64_bit_exact_replay() {
    let mut r1 = SplitMix64(0x2AD1C_AA0125);
    let mut r2 = SplitMix64(0x2AD1C_AA0125);
    for _ in 0..64 {
        assert_eq!(r1.next_u64(), r2.next_u64());
    }
}

#[test]
fn test_d10_eisenstein_nauru_and_su2() {
    assert!(verify_eisenstein_nauru_and_su2());
}

#[test]
fn test_d11_hurwitz_b2_dic6_32homs_and_k44() {
    assert!(verify_hurwitz_b2_dic6_k44());
}

#[test]
fn test_d12_zero_pari_manin_t3_all_19_genus25_excluded() {
    assert!(verify_all_19_3adic_shimura_levels_excluded());
}
