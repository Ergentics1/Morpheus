use std::f64::consts::{E, PI};
use wp034_rust::{
    cauchy_schlomilch, clausen2, erepr_mellin, eval_delta_re_three_ways, holder_ratio, jt_clock,
    re_dilog_unit, theorem_g5_best_uv, SplitMix64, SEED_WP034,
};

#[test]
fn d1_dilog_clausen_k12_and_neg_w19() {
    // K12 unique sign-change root
    let theta_star = PI * (1.0 - 1.0 / 3.0_f64.sqrt());
    let s_star = 2.0 / theta_star;
    assert!((theta_star - 1.327_793_289_355_575_4).abs() < 1e-14);
    assert!((s_star - 1.506_258_553_973_164_1).abs() < 1e-14);
    assert!(re_dilog_unit(theta_star).abs() < 1e-15);

    // Gieseking's constant Cl_2(pi/3)
    let gieseking = clausen2(PI / 3.0);
    assert!((gieseking - 1.014_941_606_409_653_6).abs() < 1e-12);

    // Partial sum failure at s = 1e6, N = 1e5
    let s_ps = 1.0e6_f64;
    let mut re_sum = 0.0_f64;
    let mut im_sum = 0.0_f64;
    for k in 1..=100_000u64 {
        let kf = k as f64;
        let ang = 2.0 * kf / s_ps;
        let inv_k2 = 1.0 / (kf * kf);
        re_sum += ang.cos() * inv_k2;
        im_sum -= ang.sin() * inv_k2;
    }
    let delta_re_ps = s_ps.powi(3) * (re_sum / (2.0 * s_ps * s_ps) - (PI * PI) / (12.0 * s_ps * s_ps));
    let im_scaled_ps = s_ps * im_sum / 2.0;
    assert!((delta_re_ps - (-5.099_864)).abs() < 1e-3);
    assert!((im_scaled_ps - (-12.086_816)).abs() < 1e-3);

    // NEG-W19: Naive f64 wipes out at 1e17; 106-bit DD EFT fails at 1e33 and wipes out at 1e77;
    // cancellation-free f64 remains exact (< 1e-15) across the entire range through s = 1e77.
    let exact_inf = -0.5 * PI;
    let (n16, d16, cf16) = eval_delta_re_three_ways(1.0e16);
    assert!((n16 - exact_inf).abs() / exact_inf.abs() > 0.25);
    assert!((d16 - exact_inf).abs() / exact_inf.abs() < 1e-15);
    assert!((cf16 - exact_inf).abs() / exact_inf.abs() < 1e-15);

    let (n17, d17, cf17) = eval_delta_re_three_ways(1.0e17);
    assert_eq!(n17, 0.0);
    assert!((d17 - exact_inf).abs() / exact_inf.abs() < 1e-15);
    assert!((cf17 - exact_inf).abs() / exact_inf.abs() < 1e-15);

    let (_n33, d33, cf33) = eval_delta_re_three_ways(1.0e33);
    assert!((d33 - exact_inf).abs() / exact_inf.abs() > 0.50);
    assert!((cf33 - exact_inf).abs() / exact_inf.abs() < 1e-15);

    let (_n77, d77, cf77) = eval_delta_re_three_ways(1.0e77);
    assert_eq!(d77, 0.0);
    assert!((cf77 - exact_inf).abs() / exact_inf.abs() < 1e-15);
}

#[test]
fn d2_sec52_f39_and_theorem_g5() {
    let s_star = PI * PI;
    let c = (-s_star).exp();
    let delta_eta = 4.0 * (-0.5 * s_star).exp() / (1.0 + c);

    // Eq. (5.24) boost variance bound holds with ratio pi/2 > 1
    let eta = 2.0 * (PI * PI) / s_star;
    let var_s = (c / ((1.0 + c) * (1.0 + c))) * s_star * s_star;
    let eq524_ratio = ((eta.abs() / PI) * var_s.sqrt()) / delta_eta;
    assert!((eq524_ratio - 0.5 * PI).abs() < 1e-14);

    // Paired vs cycle exhaustion at M = 10^4, r = 5
    let z_pair = 0.5 * delta_eta * 10_000.0 * (1.0 + c);
    let z_cyc_r5 = -0.5 * delta_eta * 10_000.0 * (5.0 - 3.0 - c);
    assert!((z_pair - 143.837_667_116_527_37).abs() < 1e-10);
    assert!((z_cyc_r5 - (-287.653_016_160_098_4)).abs() < 1e-10);
    assert!((1.0 + c) / (2.0 + c) > 0.5);
    assert!((1.0 + c) / (3.0 + c) < 0.5);

    // Theorem G5 ([G4N]): Finite-target strong exhaustions L = +1, +42, 0 on c = exp(-pi^2)
    let (_u1, _v1, err1) = theorem_g5_best_uv(1.0, c, delta_eta, 25_000);
    let (_u42, _v42, err42) = theorem_g5_best_uv(42.0, c, delta_eta, 25_000);
    let (_u0, _v0, err0) = theorem_g5_best_uv(0.0, c, delta_eta, 25_000);
    assert!(err1 < 1e-9);
    assert!(err42 < 1e-9);
    assert!(err0 < 1e-12);

    // Algebraic irrational seed c = 1/sqrt(2) (proved irrational in Lean 4)
    let c_alg = 1.0 / 2.0_f64.sqrt();
    let delta_alg = 4.0 * 2.0_f64.powf(-0.25) / (1.0 + c_alg);
    let (_ua, _va, erra) = theorem_g5_best_uv(1.0, c_alg, delta_alg, 25_000);
    assert!(erra < 1e-5);
}

#[test]
fn d3_schwarzschild_sen_c155_and_cs() {
    let alpha = 257.0 / 90.0_f64;
    let q = 257.0 / 302.0_f64;
    let x_star = (257.0 / 347.0_f64).sqrt();
    let rms_disp = 1.0 / (alpha * (alpha + 2.0)).sqrt();
    let q_over_x = q / x_star;

    assert!((x_star - 0.860_600_956_171_725_8).abs() < 1e-14);
    assert!((rms_disp - 90.0 / 112_309.0_f64.sqrt()).abs() < 1e-15);
    assert!((q_over_x - 89_179.0_f64.sqrt() / 302.0).abs() < 1e-15);
    assert!((1.0 - q_over_x - 0.011_163_802_014_606_4).abs() < 1e-13);

    // C155 max defect on [1e-3, 0.40]
    let mut max_def = 0.0_f64;
    for i in 0..=4000 {
        let d = 1.0e-3 + (0.40 - 1.0e-3) * (i as f64) / 4000.0;
        let g = 1.0 - (1.0 + d).sqrt() / (1.0 + 0.5 * d);
        max_def = max_def.max((g - d * d / 8.0).abs());
    }
    assert!(max_def > 6.0e-3 && max_def < 7.146e-3);

    // Cauchy-Schlomilch quadrature at s = 1000 and s = 10
    assert!((cauchy_schlomilch(1000.0, 20_000) - 1.0).abs() < 1e-14);
    assert!((cauchy_schlomilch(10.0, 20_000) - 1.0).abs() < 1e-14);
}

#[test]
fn d4_jt_c154_erepr_and_app_d3_c156() {
    // JT AdS_2 clock C154
    let mut max_c154 = 0.0_f64;
    for i in 0..=140 {
        let z = 0.02 + 0.28 * (i as f64) / 140.0;
        for j in 0..=140 {
            let ep = 0.05 + 0.35 * (j as f64) / 140.0;
            let norm = jt_clock(z, ep) / ((1.0 - ep) * z);
            let quad = 1.0 + (1.0 + ep - 2.0 * ep * ep) * z * z / 6.0;
            max_c154 = max_c154.max((norm - quad).abs());
        }
    }
    assert!(max_c154 > 6.0e-5 && max_c154 < 4.996e-4);

    // ER=EPR Mellin integral at (0.3, 1.7)
    let erepr_num = erepr_mellin(0.3, 1.7, 10_000);
    let erepr_exact = -1.0 / (2.0_f64 * 2.0);
    assert!((erepr_num - erepr_exact).abs() < 1e-14);

    // Appendix D.3 C156 + NEG-W21 domain catch
    let r_e = holder_ratio(0.5);
    let r_1e6 = holder_ratio(1.0 / (1.0 + 1.0e6_f64.ln()));
    assert!((r_e - 1.213_061_319_425_266_8).abs() < 1e-14);
    assert!((r_1e6 - 1.002_388_746_538_032_6).abs() < 1e-14);

    let mut max_c156 = 0.0_f64;
    for i in 0..=3400 {
        let u = 0.01 + 0.34 * (i as f64) / 3400.0;
        max_c156 = max_c156.max((holder_ratio(u) - (1.0 + 0.5 * u * u)).abs());
    }
    assert!(max_c156 > 2.2e-2 && max_c156 < 2.332e-2);
    assert!((13.0 / 7.0_f64).exp() > E);

    // Optimal beta* tightening at C_eps = 1
    let a_eps = PI.powi(4) / 15.0;
    let opt_pref = (4.0 / 3.0_f64.powf(0.75)) * a_eps.powf(0.25);
    let tightening = (1.0 + a_eps) / opt_pref;
    assert!((opt_pref - 2.801_212_839_031_1).abs() < 1e-12);
    assert!((tightening - 2.675_248_127_471_412).abs() < 1e-12);
}

#[test]
fn p1_keyed_rct_1600_seam_parity() {
    let mut rng_check = SplitMix64::new(SEED_WP034);
    let first_u64 = rng_check.next_u64();
    // Bit-exact parity with Python wp034_audit.py
    assert_eq!(first_u64, 0xb400_5f8b_fe2e_1bca);

    let mut rng = SplitMix64::new(SEED_WP034);
    let n_trials = 1_600usize;
    let mut arm_a_pass = 0usize;
    let mut arm_b_pass = 0usize;
    let c_val = (-(PI * PI)).exp();
    let pi2_6 = (PI * PI) / 6.0;
    let exact_target = -0.5 * PI;

    for _ in 0..n_trials {
        let u_s = rng.next_f64();
        let u_r = rng.next_f64();
        let u_d = rng.next_f64();
        let u_h = rng.next_f64();

        let s_val = 10.0_f64.powf(17.0 + 60.0 * u_s);
        let r_cyc = 4 + ((17.0 * u_r) as i64);
        let delta = 1.0e-3 + 0.399 * u_d;
        let u_hol = 0.01 + 0.34 * u_h;

        let th = 2.0 / s_val;
        let re_naive = pi2_6 - 0.25 * th * (2.0 * PI - th);
        let delta_naive = 0.5 * s_val * (re_naive - pi2_6);
        let cyc_ratio = (1.0 + c_val) / ((r_cyc as f64) - 1.0 + c_val);
        if (delta_naive - exact_target).abs() / exact_target.abs() < 1e-12 && cyc_ratio >= 0.5 {
            arm_a_pass += 1;
        }

        let delta_cf = -0.5 * PI + 0.5 / s_val;
        let c155_def = ((1.0 - (1.0 + delta).sqrt() / (1.0 + 0.5 * delta)) - delta * delta / 8.0).abs();
        let c156_def = (holder_ratio(u_hol) - (1.0 + 0.5 * u_hol * u_hol)).abs();
        if (delta_cf - exact_target).abs() / exact_target.abs() < 1e-14
            && cyc_ratio < 0.5
            && c155_def < 8.0e-3
            && c156_def < 2.5e-2
        {
            arm_b_pass += 1;
        }
    }

    assert_eq!(arm_a_pass, 0);
    assert_eq!(arm_b_pass, 1_600);
}
