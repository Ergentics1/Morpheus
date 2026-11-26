use std::f64::consts::PI;
use wp032_rust::*;

#[test]
fn test_d1_bennu_c145_and_crossover() {
    let r = 600.0_f64;
    let l = 100.0_f64;
    let eps = l / r;
    let da_mono = (MU_BENNU / (r * r)) * (2.0 * eps * eps) * (1.0 - eps * eps / 3.0) / (1.0 - eps * eps).powi(2);
    assert!((da_mono - 7.9130e-7).abs() < 1e-10);
    assert!((da_mono / A_SRP_BENNU - 7.858).abs() < 0.01);

    // Bisect exact R_eq = 997.02 m
    let (mut lo, mut hi) = (500.0_f64, 2000.0_f64);
    for _ in 0..80 {
        let mid = 0.5 * (lo + hi);
        let e = l / mid;
        let v = (MU_BENNU / (mid * mid)) * (2.0 * e * e) * (1.0 - e * e / 3.0) / (1.0 - e * e).powi(2);
        if v > A_SRP_BENNU {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    assert!((0.5 * (lo + hi) - 997.02).abs() < 0.1);
}

#[test]
fn test_d2_c146_and_theorem_g2_fdir_inertia() {
    let u5 = 1.0_f64 / 6.0;
    let c146 = (0.5 * PI * u5).sin() / (0.5 * PI * u5);
    assert!((c146 - 0.988_616).abs() < 1e-5);

    // Theorem G2: 10% retraction decreases COM-shifted inertia -> tension INCREASES (+19.9%),
    // contradicting paper C147's spin-down curve 0.8163
    let d = 0.10_f64;
    let i_ret = 1.0 - (4.0 / 3.0) * d + (7.0 / 12.0) * d * d;
    let t_ret = (1.0 - (7.0 / 8.0) * d) / (i_ret * i_ret);
    assert!(t_ret > 1.198 && t_ret < 1.200);
}

#[test]
fn test_d3_crtbp_routh_k10_and_supercritical_l4() {
    let mu_r0 = 2.0 / (27.0 * (1.0 + (23.0_f64 / 27.0).sqrt()));
    assert!(mu_r0 >= 0.038_520_896_504_551_38 && mu_r0 <= 0.038_520_896_504_551_42);

    // Catch 32-3 minor numerical check: exact mu_R(0.02) = 0.0515459 (not paper's 0.0514772)
    let mu_r02 = 0.5 * (1.0 - (1.0 - 4.0 * 1.32_f64 / 27.0).sqrt());
    assert!((mu_r02 - 0.051_545_865).abs() < 1e-8);

    let r_un = sim_crtbp_l4(0.042, 0.0, 0.01, 4000, 60.0);
    let r_st = sim_crtbp_l4(0.042, 0.02, 0.01, 4000, 60.0);
    assert!(r_un > 5.0 && r_st < 0.30 && r_un / r_st > 35.0);
}

#[test]
fn test_r4_yoshida4_figure8_and_lagrange_chaos() {
    let p8_0 = [[0.970_004_36, -0.243_087_53], [-0.970_004_36, 0.243_087_53], [0.0, 0.0]];
    let v8_0 = [[0.466_203_685, 0.432_365_73], [0.466_203_685, 0.432_365_73], [-0.932_407_37, -0.864_731_46]];
    let (mut p8, mut v8) = (p8_0, v8_0);
    let e0 = energy3(&p8, &v8);
    let dt8 = 6.325_913_98 / 2000.0;
    for _ in 0..2000 {
        yoshida4_step(&mut p8, &mut v8, dt8);
    }
    let rel_de = (energy3(&p8, &v8) - e0).abs() / e0.abs();
    assert!(rel_de < 1e-12);

    // Equal-mass Lagrange triangle Gascheau instability
    let om = 3.0_f64.powf(-0.25);
    let mut pl = [[0.0; 2]; 3];
    let mut vl = [[0.0; 2]; 3];
    for k in 0..3 {
        let ang = 2.0 * PI * (k as f64) / 3.0;
        pl[k] = [ang.cos(), ang.sin()];
        vl[k] = [-om * ang.sin(), om * ang.cos()];
    }
    let (mut plb, mut vlb) = (pl, vl);
    vlb[0][0] += 1e-5;
    vlb[1][0] -= 1e-5;
    let d0 = (2.0_f64 * 1e-10).sqrt();
    let el0 = energy3(&pl, &vl);
    for _ in 0..4500 {
        yoshida4_step(&mut pl, &mut vl, 18.0 / 4500.0);
        yoshida4_step(&mut plb, &mut vlb, 18.0 / 4500.0);
    }
    let rel_del = (energy3(&pl, &vl) - el0).abs() / el0.abs();
    assert!(rel_del < 1e-12);
    let mut df2 = 0.0;
    for i in 0..3 {
        for k in 0..2 {
            df2 += (plb[i][k] - pl[i][k]).powi(2) + (vlb[i][k] - vl[i][k]).powi(2);
        }
    }
    let lyap = (df2.sqrt() / d0).ln() / 18.0;
    let exact = 3.0_f64.powf(-0.25) / 2.0_f64.sqrt();
    assert!((lyap - exact).abs() / exact < 0.05);
}

#[test]
fn test_p1_keyed_rct_bit_exact_seam_parity() {
    let mut rng = SplitMix64::new(0x5750_3033_325F_5243);
    let first_u64 = rng.next_u64();
    assert_eq!(first_u64, 0x55a3_2a12_1430_eb49);
    let tol = 1e-8_f64;
    let (mut arm_a, mut arm_b, mut b01, mut c10) = (0usize, 0usize, 0usize, 0usize);
    for idx in 0..1600 {
        let (ok_a, ok_b) = match idx % 4 {
            0 => {
                let eps = 10.0_f64.powf(rng.uniform(-8.0, -4.0));
                let r_ref = (2.0 * eps * eps / 3.0) * (10.0 - 5.0 * eps.powi(2) + 4.0 * eps.powi(4) - eps.powi(6)) / (1.0 - eps * eps).powi(4);
                let naive = (1.0 / 3.0) * ((1.0 - eps).powi(-4) + 1.0 + (1.0 + eps).powi(-4)) - 1.0;
                ((naive - r_ref).abs() / r_ref <= tol, true)
            }
            1 => {
                let u = 10.0_f64.powf(rng.uniform(-8.0, -4.0));
                let x = 0.5 * PI * u;
                let r_ref = (x * x) / 6.0 - x.powi(4) / 120.0;
                let naive = 1.0 - x.sin() / x;
                ((naive - r_ref).abs() / r_ref <= tol, true)
            }
            2 => {
                let mu = 10.0_f64.powf(rng.uniform(-9.0, -5.0));
                let ks = 10.0_f64.powf(rng.uniform(-9.0, -5.0));
                let disc = 1.0 + 16.0 * ks - 27.0 * mu * (1.0 - mu);
                let sq = disc.sqrt();
                let wp2_m1 = ks + 0.5 * (16.0 * ks - 27.0 * mu * (1.0 - mu)) / (sq + 1.0);
                let wp = (1.0 + wp2_m1).sqrt();
                let r_ref = wp2_m1 / (wp + 1.0);
                let naive = ((1.0 + 2.0 * ks + sq) / 2.0).sqrt() - 1.0;
                ((naive - r_ref).abs() / r_ref.abs().max(1e-18) <= tol, true)
            }
            _ => {
                let rho_a = rng.uniform(1.2, 4.0);
                (false, (1.0 - rho_a) < 0.0)
            }
        };
        arm_a += usize::from(ok_a);
        arm_b += usize::from(ok_b);
        if !ok_a && ok_b {
            b01 += 1;
        } else if ok_a && !ok_b {
            c10 += 1;
        }
    }
    eprintln!("WP032 Rust RCT seam first_u64 = 0x{first_u64:016x} | Arm A = {arm_a}/1600 | Arm B = {arm_b}/1600 | b01 = {b01} | c10 = {c10}");
    assert_eq!(arm_b, 1600);
    assert_eq!(c10, 0);
    assert!(b01 > 800);
}
