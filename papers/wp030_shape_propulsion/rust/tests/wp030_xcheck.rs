use std::f64::consts::PI;
use wp030_rust::*;

#[test]
fn test_d1_h1_h3_earth_benchmark_and_c137() {
    let r = 7.0e6;
    let l = 100.0;
    let da_par = da_par_exact(MU_EARTH, r, l);
    let da_perp = da_perp_exact(MU_EARTH, r, l);
    assert!((da_par - (-3.320_286_896_6e-9)).abs() < 1e-18);
    assert!((da_perp - 1.660_143_447_3e-9).abs() < 1e-18);

    // Naive subtraction cliff at eps = 1e-7
    let eps = 1e-7_f64;
    let exact = (2.0 * eps * eps) * (1.0 - eps * eps / 3.0) / ((1.0 - eps * eps).powi(2));
    let naive = (1.0 / 3.0) * (1.0 / (1.0 + eps).powi(2) + 1.0 / (1.0 - eps).powi(2) - 2.0);
    let rel_err = (naive - exact).abs() / exact;
    assert!(rel_err > 1e-3, "Expected severe naive cancellation error, got {rel_err}");

    // C137 continuum bound on [1e-4, 0.05]
    let mut c137_max = 0.0_f64;
    for i in 0..=10_000 {
        let e = 1e-4 + (0.05 - 1e-4) * (i as f64) / 10_000.0;
        let ratio = (1.0 - e * e / 3.0) / (1.0 - e * e).powi(2);
        c137_max = c137_max.max((ratio - 1.0).abs());
    }
    assert!(c137_max <= 4.188e-3);
}

#[test]
fn test_d3_equilateral_hopf_kinetic_divergence_and_envelopes() {
    let mut rng = SplitMix64::new(0x5750_3033_305F_4433);
    for _ in 0..500 {
        let th0 = rng.uniform(-PI, PI);
        let beta = rng.uniform(-1.35, 1.35);
        let chi = rng.uniform(0.0, 2.0 * PI);
        let dth0 = rng.uniform(-2.0, 2.0);
        let db = rng.uniform(-2.0, 2.0);
        let l = rng.uniform(0.25, 4.0);
        let r_j = 2.0_f64.sqrt() * l;
        let i0 = r_j * r_j;
        let dchi = -2.0 * dth0 / beta.cos();

        let (rs, drs) = hopf_equilateral_pos_vel(r_j, th0, beta, chi, dth0, db, dchi);
        let com = rs[0].add(rs[1]).add(rs[2]);
        assert!(com.abs() < 1e-13);

        let inertia: f64 = rs.iter().map(|r| r.norm2()).sum();
        assert!((inertia - i0).abs() < 1e-12);

        let q = beta.sin();
        let q_mass = rs[0].mul(rs[0]).add(rs[1].mul(rs[1])).add(rs[2].mul(rs[2]));
        let q_pred = C64::cis(2.0 * th0).scale(i0 * q);
        assert!(q_mass.sub(q_pred).abs() < 1e-12);

        let spin: f64 = rs.iter().zip(drs.iter()).map(|(r, dr)| r.conj().mul(*dr).im).sum();
        assert!(spin.abs() < 1e-12);

        let t_exact: f64 = 0.5 * drs.iter().map(|dr| dr.norm2()).sum::<f64>();
        let t_pred = 0.125 * i0 * db * db + 0.5 * i0 * (q * q / (1.0 - q * q)) * dth0 * dth0;
        assert!((t_exact - t_pred).abs() < 1e-11);
    }

    // Exact kinetic ratio at q = 0.95 is 361/39 = 9.2564102564...
    let q95 = 0.95_f64;
    assert!((q95 * q95 / (1.0 - q95 * q95) - 361.0 / 39.0).abs() < 1e-13);
}

#[test]
fn test_d4_collision_free_holonomy_minus_90_deg() {
    let r_j = 2.0_f64.sqrt();
    let beta = PI / 3.0;
    let (r_init, _) = hopf_equilateral_pos_vel(r_j, 0.0, beta, 0.0, 0.0, 0.0, 0.0);
    // Traverse chi: 0 -> -2*pi with dth0/dchi = -0.5*cos(beta) = -0.25 => th0_f = +pi/2
    let th0_f = -0.5 * beta.cos() * (-2.0 * PI);
    let (r_final, _) = hopf_equilateral_pos_vel(r_j, th0_f, beta, -2.0 * PI, 0.0, 0.0, 0.0);
    for (rf, ri) in r_final.iter().zip(r_init.iter()) {
        let ratio = rf.div(*ri);
        assert!(ratio.sub(C64::new(0.0, -1.0)).abs() < 1e-13, "Expected -i (-90 deg), got {ratio:?}");
    }
    // Verify strictly positive collision-free minimum separation along entire loop
    let mut min_sep = 1e9_f64;
    for k in 0..400 {
        let chi = -2.0 * PI * (k as f64) / 400.0;
        let th0 = -0.5 * beta.cos() * chi;
        let (rs, _) = hopf_equilateral_pos_vel(r_j, th0, beta, chi, 0.0, 0.0, 0.0);
        let sep = rs[0].sub(rs[1]).abs().min(rs[1].sub(rs[2]).abs()).min(rs[2].sub(rs[0]).abs());
        min_sep = min_sep.min(sep);
    }
    let exact_min = (2.0 - 3.0_f64.sqrt()).sqrt();
    assert!((min_sep - exact_min).abs() < 1e-4);
}

#[test]
fn test_r1_coupled_4body_hopf_matches_python_crossplane() {
    let res95 = run_coupled_4body_hopf(0.95, 0.2, 5, 1571);
    assert!(res95.eq5_ppm < 0.01, "Eq. (5) ppm too high: {}", res95.eq5_ppm);
    assert!(res95.max_abs_dj < 1e-11, "|dJ| drift: {}", res95.max_abs_dj);
    assert!(res95.max_abs_s < 2e-5, "|S| drift: {}", res95.max_abs_s);
    assert!((res95.de_orb - 6.930_00e-3).abs() < 1e-5, "dE mismatch: {}", res95.de_orb);
    assert!((res95.min_sep_over_l - (2.0 * 0.05_f64).sqrt()).abs() < 2e-3);
    assert!((res95.max_rad_over_l - (2.0 * 1.95 / 3.0_f64).sqrt()).abs() < 2e-3);
    assert!((res95.t_track_ratio - 361.0 / 39.0).abs() < 1e-3);

    // Hard boom-radius cap max_rad <= L achieved at q = 0.50
    let res50 = run_coupled_4body_hopf(0.50, 0.2, 5, 1571);
    assert!((res50.max_rad_over_l - 1.0).abs() < 1e-3);
    assert!((res50.min_sep_over_l - 1.0).abs() < 1e-3);
    assert!(res50.eq5_ppm < 0.01);

    // Circular control orbit e0 = 0 confirms Theorem 1 barrier
    let res_circ = run_coupled_4body_hopf(0.95, 0.0, 5, 1571);
    assert!(res_circ.de_orb.abs() < 1e-5);
}

#[test]
fn test_r2_unassisted_landis_tether_tumbles_vs_hopf() {
    let l25 = run_unassisted_landis_tether(0.25, 5, 2000);
    let l50 = run_unassisted_landis_tether(0.50, 5, 2000);
    assert!(l25.net_tumble_deg > 3600.0, "Expected violent tumble, got {}", l25.net_tumble_deg);
    assert!(l50.net_tumble_deg > 1000.0, "Expected tumble, got {}", l50.net_tumble_deg);
    assert!(l25.max_abs_dj < 1e-11);
    assert!(l50.max_abs_dj < 1e-11);
    let hopf = run_coupled_4body_hopf(0.95, 0.2, 5, 1571);
    assert!(hopf.de_orb > 1.5 * l25.de_orb.max(l50.de_orb));
}

#[test]
fn test_d6_table1_underground_perigees_and_valid_budgets() {
    // Paper Table 1 Regimes A & B have underground perigees
    let rp_a = 7.0e6 * (1.0 - 0.10);
    let rp_b = 7.0e6 * (1.0 - 0.25);
    assert!(rp_a < R_EARTH_MEAN);
    assert!(rp_b < R_EARTH_MEAN);

    // Valid Earth Regime B (rp = 6800 km, e = 0.25 => a = 9066.67 km, L = 20 km, M = 1000 kg)
    let a: f64 = 6.8e6 / 0.75;
    let e: f64 = 0.25;
    let l: f64 = 20.0e3;
    let m: f64 = 1000.0;
    let p: f64 = a * (1.0 - e * e);
    let t_orb = 2.0 * PI * (a.powi(3) / MU_EARTH).sqrt();
    let de = (2.0 * MU_EARTH * m * l * l / p.powi(3)) * (3.0 * e + e.powi(3));
    let v_c = (MU_EARTH / a).sqrt();
    let dv_yr = (de / (m * v_c)) * (SEC_PER_YEAR / t_orb);
    assert!((dv_yr - 220.223_439).abs() < 1e-3, "Valid Regime B dv/yr = {dv_yr}");

    // Regime A tension typo: exact 3*mu*(M/3)*L/rp^3 = 0.15941 N vs paper's 0.0012 N (>130x off)
    let t_a_rp = 3.0 * MU_EARTH * (m / 3.0) * 100.0 / rp_a.powi(3);
    assert!((t_a_rp - 0.159_41).abs() < 1e-4);

    // Regime C Bennu tension = 3.13e-5 N (> 1e-6 N) and (L/R)^2 boost = 7.84e6
    let t_bennu = 3.0 * MU_BENNU * (m / 3.0) * 100.0 / 2500.0_f64.powi(3);
    assert!((t_bennu - 3.130_88e-5).abs() < 1e-8);
    assert!(((7.0e6_f64 / 2500.0).powi(2) - 7.84e6).abs() < 1e-6);
}

#[test]
fn test_p1_keyed_rct_bit_exact_seam_parity() {
    let mut rng = SplitMix64::new(0x5750_3033_305F_5243);
    let first_u64 = rng.next_u64();
    // Exact bit-for-bit seam parity with Python wp030_audit.py SplitMix64
    assert_eq!(first_u64, 0xe9de_083b_69c6_7979);
    let tol = 1.0e-8;
    let mut arm_a = 0usize;
    let mut arm_b = 0usize;
    let mut b01 = 0usize;
    let mut c10 = 0usize;

    for idx in 0..1600 {
        let stratum = idx % 4;
        let (ok_a, ok_b) = match stratum {
            0 => {
                let eps = 10.0_f64.powf(rng.uniform(-8.0, -4.0));
                let r_ref = (2.0 * eps * eps) * (1.0 - eps * eps / 3.0) / (1.0 - eps * eps).powi(2);
                let naive = (1.0 / 3.0) * (1.0 / (1.0 + eps).powi(2) + 1.0 / (1.0 - eps).powi(2) - 2.0);
                ((naive - r_ref).abs() / r_ref <= tol, true)
            }
            1 => {
                let eps = 10.0_f64.powf(rng.uniform(-8.0, -4.0));
                let s = (1.0 + eps * eps).sqrt();
                let r_ref = (eps * eps) * (2.0 / 3.0) * (s * s + s + 1.0) / (s * s * s * (s + 1.0));
                let naive = (2.0 / 3.0) * (1.0 - 1.0 / (s * s * s));
                ((naive - r_ref).abs() / r_ref <= tol, true)
            }
            2 => {
                let th = 10.0_f64.powf(rng.uniform(-8.0, -4.0));
                let r_ref = 2.0 * PI * (0.5 * th).sin().powi(2);
                let naive = PI * (1.0 - th.cos());
                ((naive - r_ref).abs() / r_ref <= tol, true)
            }
            _ => {
                let e = rng.uniform(1e-3, 0.30);
                let exact_eta = 1.0 - ((1.0 - e) / (1.0 + e)).powi(3);
                let poly_eta = (6.0 * e + 2.0 * e.powi(3)) / (1.0 + e).powi(3);
                ((1.0 - exact_eta).abs() <= 0.05, (exact_eta - poly_eta).abs() < 1e-14)
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
    eprintln!("Rust RCT seam first_u64 = 0x{first_u64:016x} | Arm A = {arm_a}/1600 | Arm B = {arm_b}/1600 | b01 = {b01} | c10 = {c10}");
    assert_eq!(arm_a, 72);
    assert_eq!(arm_b, 1600);
    assert_eq!(b01, 1528);
    assert_eq!(c10, 0);
}
