use morpheus_rust::{
    cyclotomic::verify_theorem_3_4,
    swe_sweep::run_fourth_language_cross_oracle,
    tower::verify_tower_and_artin_ihara,
    tune_general::{verify_general_tune_criterion, verify_tune_theorem_up_to_16},
};

fn main() {
    let mut n_max: u16 = 72;
    let args: Vec<String> = std::env::args().collect();
    for i in 1..args.len() {
        if args[i] == "--n-max" && i + 1 < args.len() {
            if let Ok(v) = args[i + 1].parse::<u16>() {
                n_max = v;
            }
        }
    }

    println!("=== Morpheus Rust Exact Arithmetic & General N-EDO Verifier ===");

    let t34 = verify_theorem_3_4();
    println!(
        "  [{}] Thm 3.4 (Z[zeta_12] exact): f3=2-i:{} f4^2=-3:{} minpoly:{} unit:{} galois:{} M11:{} M7_014={}/36",
        if t34.passed { "PASS" } else { "FAIL" },
        t34.f3_is_2_minus_i,
        t34.f4_sq_is_minus_3,
        t34.f1_minpoly_zero,
        t34.f1_unit_norm_one,
        t34.galois_action_exact,
        t34.m11_is_automorphism,
        t34.m7_isomorphism_014_edges
    );

    let tow = verify_tower_and_artin_ihara();
    println!(
        "  [{}] Thm 7.4 & Cor 7.5 (Z/12 tower + Artin-Ihara in Z[z12][u]): edges={}/36 lifts=({},{},{}) blocks:{} full:{}",
        if tow.passed { "PASS" } else { "FAIL" },
        tow.edges_voltage_verified,
        tow.pl_cycle_len,
        tow.pr_cycle_len,
        tow.lr_cycle_len,
        tow.artin_order_blocks_exact,
        tow.full_weil_product_exact
    );

    let t16 = verify_tune_theorem_up_to_16();
    println!(
        "  [{}] Thm 4.2 (12-EDO m<=16): total_rooted={} (len16={}) decode_fail={} periodic_fail={}",
        if t16.passed { "PASS" } else { "FAIL" },
        t16.rooted_primes_checked,
        t16.rooted_primes_len_16,
        t16.decode_failures,
        t16.periodic_tune_failures
    );

    let gen = verify_general_tune_criterion(n_max);
    println!(
        "  [{}] Thm 4.3 / C-4 (general N<={} step systems): systems={} failures={}",
        if gen.passed { "PASS" } else { "FAIL" },
        gen.n_max,
        gen.systems_tested,
        gen.failures
    );

    let x4 = run_fourth_language_cross_oracle();
    println!(
        "  [{}] 4th-Language Cross-Oracle: pi(40)={} TV={:.6} ex_kurt={:.6} prng0=0x{:016x}",
        if x4.passed { "PASS" } else { "FAIL" },
        x4.pi40,
        x4.m40_tv,
        x4.m40_excess_kurtosis,
        x4.prng_first_word
    );

    let nov_ab = morpheus_rust::novelty::verify_novelty_theorems_a_and_b(n_max);
    println!(
        "  [{}] Novelty 1 (Thms A & B / NEG-M11, ALL S via S_max, N<={}): chords={} max|L0∩Lt|={} T_fail={} TI_oct={}({:?}) TI_unexp={} NEG-M11:{}",
        if nov_ab.passed { "PASS" } else { "FAIL" },
        nov_ab.n_max,
        nov_ab.chords_tested,
        nov_ab.max_link_intersection,
        nov_ab.t_orbit_failures,
        nov_ab.ti_octatonic_failures,
        nov_ab.octatonic_witness_ns,
        nov_ab.ti_unexpected_failures,
        nov_ab.neg_m11_verified
    );

    let nov_c = morpheus_rust::novelty::verify_novelty_theorem_c(40);
    println!(
        "  [{}] Novelty 2 (Thm C Edgeworth C-2'/C-2'' & 2D Isotropy m=40): m*k4(u,v,4u+3v)=({:.4},{:.4},{:.4}) TV0={:.3e} TV4={:.3e}({:.1}x) TV6={:.3e}({:.1}x)",
        if nov_c.passed { "PASS" } else { "FAIL" },
        nov_c.m_times_ex_kurt,
        nov_c.m_ex_kurt_v,
        nov_c.m_ex_kurt_zigzag,
        nov_c.tv_gaussian,
        nov_c.tv_edgeworth4,
        nov_c.tv_gain_4,
        nov_c.tv_edgeworth6,
        nov_c.tv_gain_6
    );

    let all_ok = t34.passed && tow.passed && t16.passed && gen.passed && x4.passed && nov_ab.passed && nov_c.passed;
    println!("Overall Rust Oracle Result: {}", if all_ok { "ALL PASS" } else { "FAILURES" });
    if !all_ok {
        std::process::exit(1);
    }
}

