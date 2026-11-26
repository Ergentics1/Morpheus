use morpheus_rust::{
    cyclotomic::verify_theorem_3_4,
    keyed_prng::{KeyedPrng, PrngKey},
    swe_sweep::run_fourth_language_cross_oracle,
    tower::verify_tower_and_artin_ihara,
    tune_general::{verify_general_tune_criterion, verify_tune_theorem_up_to_16},
};

#[test]
fn test_theorem_3_4_exact_cyclotomic() {
    let r = verify_theorem_3_4();
    assert!(r.passed, "{r:?}");
    assert_eq!(r.m7_isomorphism_014_edges, 36);
}

#[test]
fn test_theorem_7_4_tower_and_cor_7_5_artin_ihara() {
    let r = verify_tower_and_artin_ihara();
    assert!(r.passed, "{r:?}");
    assert_eq!(r.edges_voltage_verified, 36);
}

#[test]
fn test_theorem_4_2_all_rooted_primes_up_to_16() {
    let r = verify_tune_theorem_up_to_16();
    assert!(r.passed, "{r:?}");
    assert_eq!(r.rooted_primes_checked, 174_864);
    assert_eq!(r.rooted_primes_len_16, 131_136);
    assert_eq!(r.decode_failures, 0);
    assert_eq!(r.periodic_tune_failures, 0);
}

#[test]
fn test_theorem_4_3_all_6028_systems_up_to_n72() {
    let r = verify_general_tune_criterion(72);
    assert!(r.passed, "{r:?}");
    assert_eq!(r.systems_tested, 6028);
    assert_eq!(r.failures, 0);
}

#[test]
fn test_fourth_language_swe_sweep_and_keyed_prng_replay() {
    let r = run_fourth_language_cross_oracle();
    assert!(r.passed, "{r:?}");
    assert_eq!(r.pi40, 54_975_717_792);

    // Order-invariance and bit-exact replay of KeyedPRNG.
    let k1 = PrngKey::new("prime-cadences", "seam-replay", 7, 20261125);
    let k2 = PrngKey::new("prime-cadences", "other-exp", 7, 20261125);
    let mut a = KeyedPrng::from_key(k1);
    let mut b = KeyedPrng::from_key(k2);
    let v1 = a.next_u64();
    let v2 = b.next_u64();
    assert_eq!(v1, r.prng_first_word);
    assert_ne!(v1, v2);
    let mut a_rep = KeyedPrng::from_key(k1);
    assert_eq!(a_rep.next_u64(), v1);
}

#[test]
fn test_novelty_1_theorems_a_and_b_all_s_up_to_n72() {
    let r = morpheus_rust::novelty::verify_novelty_theorems_a_and_b(72);
    assert!(r.passed, "{r:?}");
    assert_eq!(r.max_link_intersection, 2);
    assert_eq!(r.t_orbit_failures, 0);
    assert_eq!(r.ti_octatonic_failures, 9);
    assert_eq!(r.ti_unexpected_failures, 0);
    assert_eq!(r.octatonic_witness_ns, vec![8, 16, 24, 32, 40, 48, 56, 64, 72]);
    assert!(r.neg_m11_verified);
}

#[test]
fn test_novelty_2_theorem_c_edgeworth_and_2d_isotropy() {
    let r = morpheus_rust::novelty::verify_novelty_theorem_c(40);
    assert!(r.passed, "{r:?}");
    assert_eq!(r.bad_divisibility, 0);
    assert!(r.tv_gain_4 > 10.0);
    assert!(r.tv_gain_6 > 70.0);
    assert!(r.max_isotropy_spread_4th < 0.02);
}

#[test]
fn test_novelty_3_theorem_d_three_pincer_obstruction() {
    let r = morpheus_rust::section7_cycle5::verify_theorem_d_pincer();
    assert!(r.passed, "{r:?}");
    assert_eq!(r.deg9_to_14_survivors, 0);
    assert_eq!(r.deg7_max_surviving_u, 4);
    assert_eq!(r.deg7_hge2_survivors, 0);
    assert_eq!(r.deg8_max_surviving_u, 4);
    assert_eq!(r.deg8_hge2_survivors, 0);
    assert_eq!(r.deg6_max_surviving_u, 8);
    assert!(r.deg6_u16_h1_dead && r.deg6_u16_hge2_dead);
    assert!(r.deg6_u16_h1_margin > 0.013);
}

#[test]
fn test_thm_7_11_and_neg_e10_pure_rust_manin_t2() {
    let r = morpheus_rust::section7_cycle5::verify_shimura_manin_t2();
    assert!(r.passed, "{r:?}");
    assert_eq!(r.total_pairs, 19);
    assert_eq!(r.torsion_free_pairs, 11);
    assert!(r.neg_e10_detected);
    assert_eq!(r.neg_e10_phi, 176);
    assert_eq!(r.neg_e10_e3, 8);
    assert_eq!(r.gamma_h_count, 4);
    assert_eq!(r.full_rank_levels, r.distinct_levels_checked);
    assert_eq!(r.m345_manin_dim, 45);
    assert_eq!(r.m345_px_rank, 45);
}

#[test]
fn test_props_7_3_7_17_7_18a_siegel_and_pgl2_f8() {
    let r = morpheus_rust::section7_cycle5::verify_section7_arithmetic_cycle5();
    assert!(r.passed, "{r:?}");
    assert_eq!(r.quad_hplus1_solutions, 3);
    assert_eq!(r.quad_d41_solutions, 2);
    assert_eq!(r.quad_d137_solutions, 1);
    assert_eq!(r.pgl2_f8_order, 504);
    assert_eq!(r.pgl2_f8_order3_count, 56);
    assert_eq!(r.pgl2_f8_order3_free_count, 56);
    assert_eq!(r.gamma0_powers_obstructed, 12);
}

