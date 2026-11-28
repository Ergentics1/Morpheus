use arithmetic_frontiers_closure_rust as af;

fn main() {
    println!("Running Paper #10 (PC-IV) zero-crate Rust 6-suite independent verifier...");
    af::run_suite_r1_cubic_lame();
    println!("  [PASS] R1: Cubic Lame Nauru Curves (d_F=316,148) 12x12 Max Orders & 0/8 Obstruction");
    af::run_suite_r2_q33_level4_congruence();
    println!("  [PASS] R2: Q(sqrt(33))_A & Twin Q(sqrt(33))_B Level (4) Full Congruence (4/16 each) + Ad_(4) Stall");
    af::run_suite_r3_genus25_brandt_b3_atlas();
    println!("  [PASS] R3: Complete 9/9 Torsion-Free Genus-25 Borel Brandt B(3) & X_0^21(16) Annihilator");
    af::run_suite_r4_degree8_poitou_closure();
    println!("  [PASS] R4: Degree-8 (8,1,1,E) Poitou-Odlyzko Prime-Norm, Symmetry, Ram_fin & Eichler Closure");
    af::run_suite_r5_runtime_fault_guards();
    println!("  [PASS] R5: Runtime Global-Invariant Monitors & 6/6 Deterministic Fault Rejections");
    let (xor_d, fnv_d) = af::run_suite_r6_splitmix64_seam_parity();
    println!(
        "  [PASS] R6: Bit-Exact SplitMix64 RCT-PC4-1/2 Seam Parity (xor=0x{:016x}, fnv=0x{:016x})",
        xor_d, fnv_d
    );
    println!("Summary: 6/6 Paper #10 (PC-IV) Rust core suites PASS.");
}
