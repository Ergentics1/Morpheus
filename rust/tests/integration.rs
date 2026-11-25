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
