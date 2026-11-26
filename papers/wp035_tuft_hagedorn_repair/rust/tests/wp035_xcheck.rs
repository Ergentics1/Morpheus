use std::f64::consts::PI;
use wp035_rust::{
    delta_stirling, digamma_pos, gamma_cdf_at_mean, l_p_1_mult, lgamma_pos, riemann_zeta_int,
    SplitMix64, GAMMA_EM, SEED_WP035,
};

#[test]
fn d1_track_a_spectral_zeta_eq65_and_neg_w22() {
    let z3 = riemann_zeta_int(3);
    let z5 = riemann_zeta_int(5);
    let z7 = riemann_zeta_int(7);
    let zp0 = -0.5 * (2.0 * PI).ln();
    let zp_m2 = -z3 / (4.0 * PI * PI);
    let zp_m4 = 3.0 * z5 / (4.0 * PI.powi(4));
    let zp_m6 = -45.0 * z7 / (8.0 * PI.powi(6));

    let zp_s3 = zp_m2 - zp0;
    let zp_s5 = 2.0 * zp0 - 2.5 * zp_m2 + 0.5 * zp_m4;
    let spec5 = -2.5 * zp_m2 + 0.5 * zp_m4;
    let zp_s7 = -2.0 * zp0 + (49.0 / 18.0) * zp_m2 - (7.0 / 9.0) * zp_m4 + (1.0 / 18.0) * zp_m6;

    assert!((zp_s3 - 0.888_490_076_146).abs() < 1e-11);
    assert!((zp_s5 - (-1.757_764_018_038)).abs() < 1e-11);
    assert!((spec5 - 0.080_113_048_371).abs() < 1e-11);
    assert!((zp_s7 - 1.748_452_204_448).abs() < 1e-11);

    // Eq. (65) exact +zeta(3)/pi^2 vs Nielsen -2*zeta(3)
    let ratio_eq65 = (-2.0 * z3) / (z3 / (PI * PI));
    assert!((ratio_eq65 - (-2.0 * PI * PI)).abs() < 1e-12);

    // True L(3, 1) spectrum vs Eq. (65)
    let l31: Vec<i64> = (1..=6).map(|n| l_p_1_mult(3, n)).collect();
    assert_eq!(l31, vec![4, 4, 8, 20, 22, 28]);

    // NEG-W22 catch: exact S^3 ratio is 29.18 (not 30.2) and S^5 is 21.94 (not 22.9),
    // and dropping -zeta'_R(0) on S^3 flips sign to -0.030448.
    assert!(zp_m2 < 0.0);
    assert!(((zp_s3 / zp_m2).abs() - 29.180_1).abs() < 1e-3);
    assert!(((zp0 / zp_m2).abs() - 30.180_1).abs() < 1e-3);
    assert!(((zp_s5 / spec5).abs() - 21.941_0).abs() < 1e-3);
    assert!(((2.0 * zp0 / spec5).abs() - 22.941_0).abs() < 1e-3);
}

#[test]
fn d2_track_a_a5_wyler_f40_g2_and_beltrami() {
    let z3 = riemann_zeta_int(3);
    let z5 = riemann_zeta_int(5);
    let spec5: f64 = 0.080_113_048_371_333_91;
    let a5_der = 6.0 * 3.0_f64.sqrt() * (spec5 / 6.0).exp();
    let a5_used = 3.0_f64.sqrt() * (2.0 + z3 / (4.0 * PI * PI)) * (spec5 / 6.0).exp();
    assert!((a5_der / a5_used - 2.955_012).abs() < 1e-5);
    assert!(((3.0 * (a5_der - a5_used)).exp() / 1.197_7e9 - 1.0).abs() < 1e-3);

    // Wyler alpha & F40 witness + NEG-W24 10^(1/4) volume ratio
    let aw = (9.0 / (8.0 * PI.powi(4))) * (PI.powi(5) / 1920.0).powf(0.25);
    let pull_aw = (1.0 / aw - 137.035_999_177) / 2.1e-8;
    assert!((pull_aw - 3_965.29).abs() < 0.1);
    assert!((1.0 - 2.1_f64.powf(-19.0 / 4.0) - 0.970_525).abs() < 1e-5);
    let vol_ratio = (4.0 * PI) * (PI.powi(5) / 12.0).powf(0.25) / ((8.0 * PI * PI / 3.0).powi(2) * PI);
    assert!((vol_ratio / aw - 10.0_f64.powf(0.25)).abs() < 1e-13);

    // C157 g-2 three-way cancellation
    let c2_tuft = -13.0 * z3 / 48.0;
    let c3_tuft = 0.5 * (0.5 * (13.0 * z3 / 24.0).powi(2) - z5 / 4.0);
    let c2_qed = 197.0 / 144.0 + PI * PI / 12.0 - 0.5 * PI * PI * 2.0_f64.ln() + 0.75 * z3;
    let c3_qed = 1.181_241_456_587_200;
    let ac = 1.0 / 137.035_999_177;
    let sig_ae = 1.3e-13;
    assert!((((aw - ac) / (2.0 * PI)) / sig_ae - (-5_428.8)).abs() < 0.2);
    assert!((((c2_tuft - c2_qed) * (ac / PI).powi(2)) / sig_ae - 121_269.4).abs() < 0.5);
    assert!((((c3_tuft - c3_qed) * (ac / PI).powi(3)) / sig_ae - (-116_156.4)).abs() < 0.5);

    // Clifford-torus Beltrami ODE f_3(y) = y - 4y^2 + (10/3)y^3 at m = 3 (k = 5, lambda = 6)
    for i in 1..20 {
        let y = (i as f64) / 20.0;
        let f = y - 4.0 * y * y + (10.0 / 3.0) * y.powi(3);
        let fp = 1.0 - 8.0 * y + 10.0 * y * y;
        let fpp = -8.0 + 20.0 * y;
        let lhs = -4.0 * y * ((1.0 - y) * fpp - fp);
        assert!((lhs - 36.0 * f).abs() < 1e-13);
    }
}

#[test]
fn d3_track_b_r1_r2_r3_c159_c160_k13() {
    assert!((4.0 / 3.0_f64.powf(0.75) - 1.754_765_35).abs() < 1e-7);

    // Delta_Stirling at the three physical black-hole exponents
    assert!((delta_stirling(151.0 / 45.0) - 0.024_763).abs() < 1e-5);
    assert!((delta_stirling(257.0 / 90.0) - 0.029_067).abs() < 1e-5);
    assert!((delta_stirling(167.0 / 90.0) - 0.044_506).abs() < 1e-5);

    // C159 convexity defect on [1.8, 3.6] x [0.005, 0.15]
    let mut c159_max = 0.0_f64;
    for i in 0..=180 {
        let a = 1.8 + 1.8 * (i as f64) / 180.0;
        for j in 0..=150 {
            let d = 0.005 + 0.145 * (j as f64) / 150.0;
            c159_max = c159_max.max((a * (d - (1.0 + d).ln()) - 0.5 * a * d * d).abs());
        }
    }
    assert!(c159_max > 3.5e-3 && c159_max < 4.492e-3);

    // C160 Stirling remainder defect on [1.5, 8.0]
    let mut c160_max = 0.0_f64;
    for i in 0..=2600 {
        let a = 1.5 + 6.5 * (i as f64) / 2600.0;
        c160_max = c160_max.max((delta_stirling(a) - 1.0 / (12.0 * a)).abs());
    }
    assert!(c160_max > 7.0e-4 && c160_max < 8.281e-4);

    // K13 unique positive digamma root psi(x_min*) = 0
    let mut lo = 1.4_f64;
    let mut hi = 1.5_f64;
    for _ in 0..70 {
        let mid = 0.5 * (lo + hi);
        if digamma_pos(mid) < 0.0 {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    assert!((0.5 * (lo + hi) - 1.461_632_144_968_362_3).abs() < 1e-14);
}

#[test]
fn d4_theorem_g6_hagedorn_equivalence_breaking() {
    // QFT beta_c = 0 dispersion decays as Q_*^{-3/8}
    let disp_qft = |q_star: f64| -> f64 {
        let beta = (3.0 / q_star).powf(0.25);
        (4.0 / (beta * q_star)).sqrt()
    };
    assert!((disp_qft(1.0e4) / disp_qft(1.0e8) - 10.0_f64.powf(1.5)).abs() < 1e-12);

    // Hagedorn Gamma(alpha, alpha) dispersion, tail leakage, & WP 034 Beta(alpha, 1) bridge
    let regimes: [(f64, f64, f64); 3] = [
        (151.0 / 45.0, 0.427, 0.428),
        (257.0 / 90.0, 0.421, 0.422),
        (167.0 / 90.0, 0.402, 0.403),
    ];
    for &(alpha, leak_lo, leak_hi) in &regimes {
        let can_disp = 1.0 / alpha.sqrt();
        let trunc_disp = 1.0 / (alpha * (alpha + 2.0)).sqrt();
        assert!((trunc_disp / can_disp - 1.0 / (alpha + 2.0).sqrt()).abs() < 1e-15);
        let leak = 1.0 - gamma_cdf_at_mean(alpha, 20_000);
        assert!(leak > leak_lo && leak < leak_hi);
    }

    // Exact bridge to WP 034's 26.8556% dispersion
    let wp034_disp = 90.0 / 112_309.0_f64.sqrt();
    let a_ch: f64 = 257.0 / 90.0;
    assert!((1.0 / (a_ch * (a_ch + 2.0)).sqrt() - wp034_disp).abs() < 1e-15);
}

#[test]
fn p1_keyed_rct_1600_seam_parity() {
    let mut rng_chk = SplitMix64::new(SEED_WP035);
    // Bit-exact parity with Python wp035_audit.py
    assert_eq!(rng_chk.next_u64(), 0xcc61_7ec5_1b6f_b1e0);

    let mut rng = SplitMix64::new(SEED_WP035);
    let n_trials = 1_600usize;
    let mut arm_a_pass = 0usize;
    let mut arm_b_pass = 0usize;

    for _ in 0..n_trials {
        let u_r = rng.next_f64();
        let u_h = rng.next_f64();
        let u_a = rng.next_f64();
        let u_d = rng.next_f64();

        let r_scale = 1.20 + 1.80 * u_r;
        let u_lerch = 1.0e-3 + 0.249 * u_h;
        let alpha = 1.80 + 1.80 * u_a;
        let delta = 0.005 + 0.145 * u_d;

        if (r_scale.powf(-19.0 / 4.0) - 1.0).abs() <= 0.50 {
            arm_a_pass += 1;
        }
        let c158_def = (lgamma_pos(1.0 + u_lerch) - (-GAMMA_EM * u_lerch + (PI * PI / 12.0) * u_lerch * u_lerch)).abs();
        let c159_def = (alpha * (delta - (1.0 + delta).ln()) - 0.5 * alpha * delta * delta).abs();
        let c160_def = (delta_stirling(alpha) - 1.0 / (12.0 * alpha)).abs();
        let g6_err = ((1.0 / (alpha * (alpha + 2.0)).sqrt()) / (1.0 / alpha.sqrt()) - 1.0 / (alpha + 2.0).sqrt()).abs();
        if c158_def < 8.0e-3 && c159_def < 4.5e-3 && c160_def < 1.0e-3 && g6_err < 1e-14 {
            arm_b_pass += 1;
        }
    }

    assert_eq!(arm_a_pass, 0);
    assert_eq!(arm_b_pass, 1_600);
}
