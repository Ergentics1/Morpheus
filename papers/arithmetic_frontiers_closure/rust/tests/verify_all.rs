use arithmetic_frontiers_closure_rust as af;

#[test]
fn test_r1_cubic_lame_noncongruence() {
    af::run_suite_r1_cubic_lame();
}

#[test]
fn test_r2_q33_level4_full_congruence_both_twins() {
    af::run_suite_r2_q33_level4_congruence();
}

#[test]
fn test_r3_genus25_brandt_b3_all_9_curves() {
    af::run_suite_r3_genus25_brandt_b3_atlas();
}

#[test]
fn test_r4_degree8_poitou_odlyzko_closure() {
    af::run_suite_r4_degree8_poitou_closure();
}

#[test]
fn test_r5_runtime_fault_injection_guards() {
    af::run_suite_r5_runtime_fault_guards();
}

#[test]
fn test_r6_splitmix64_cross_language_seam_parity() {
    let (xor_d, fnv_d) = af::run_suite_r6_splitmix64_seam_parity();
    assert!(xor_d != 0 && fnv_d != 0);
}
