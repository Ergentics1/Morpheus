use morpheus_lexicon_audit::{
    audit_text, compute_splitmix_seam, load_registry, repo_root, verify_all_six_gates,
    EXPECTED_SEQ_FNV, EXPECTED_XOR_DIGEST, NEGATIVE_TRAP1_TEXT, TIER1_BENCHMARK, TIER2_BENCHMARK,
    TIER3_BENCHMARK,
};

#[test]
fn test_l1_registry_and_full_suite() {
    let summary = verify_all_six_gates().expect("all 6 Rust lexicon gates must pass");
    assert!(summary.contains("60 concepts"));
    assert!(summary.contains("120 alias traps"));
}

#[test]
fn test_l3_negative_trap1_deprecated_aliases() {
    let reg = load_registry(&repo_root().join("data/lexicon/morpheus_universal_lexicon.json"))
        .expect("registry loads");
    let rep = audit_text(NEGATIVE_TRAP1_TEXT, &reg, "research").expect("audit ok");
    assert_eq!(rep.deprecated_hits, 4);
}

#[test]
fn test_l4_l5_readability_funnel_parity() {
    let reg = load_registry(&repo_root().join("data/lexicon/morpheus_universal_lexicon.json"))
        .expect("registry loads");
    let t3 = audit_text(TIER3_BENCHMARK, &reg, "atelier").expect("t3");
    let t2 = audit_text(TIER2_BENCHMARK, &reg, "research").expect("t2");
    let t1 = audit_text(TIER1_BENCHMARK, &reg, "atelier").expect("t1");
    assert!((t3.jwr_pct - 40.0).abs() < 1e-9);
    assert!((t2.jwr_pct - (6.0 * 100.0 / 70.0)).abs() < 1e-6);
    assert_eq!(t1.jwr_pct, 0.0);
    assert!((t1.fk_grade - 6.875862068965517).abs() < 1e-6 || (t1.fk_grade >= 5.0 && t1.fk_grade <= 12.5));
}

#[test]
fn test_l6_bit_exact_splitmix64_seam_parity() {
    let reg = load_registry(&repo_root().join("data/lexicon/morpheus_universal_lexicon.json"))
        .expect("registry loads");
    let (xor_d, seq_fnv) = compute_splitmix_seam(&reg).expect("seam");
    assert_eq!(xor_d, EXPECTED_XOR_DIGEST);
    assert_eq!(seq_fnv, EXPECTED_SEQ_FNV);
}
