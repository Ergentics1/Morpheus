use std::f64::consts::PI;
use wp033_rust::*;

#[test]
fn test_d1_k11_c149_and_theorem_g3_didymos() {
    let g2_em = solve_l2_quintic(MU_EM);
    assert!(g2_em >= 0.167_832_751_007_869_1 && g2_em <= 0.167_832_751_007_869_3);
    assert!((g2_em * R_EM_KM - 64_514.91).abs() < 0.05);

    // Theorem G3: Didymos-Dimorphos L2 exact nonlinear 3-mass Halo gap (omega_xy^2 - omega_z^2)
    let g2_dd = solve_l2_quintic(MU_DD);
    assert!((g2_dd * R_DD_M - 180.50).abs() < 0.05);
    let x_dd = 1.0 - MU_DD + g2_dd;
    let dd_gap = |l_m: f64, ax: char| -> f64 {
        let (uxx, uyy, uzz) = exact_hess_triad_l2(x_dd, MU_DD, l_m / R_DD_M, ax);
        let (uxxt, uyyt) = (1.0 + uxx, 1.0 + uyy);
        let b = 4.0 - uxxt - uyyt;
        let c = uxxt * uyyt;
        let wxy2 = 0.5 * (b + (b * b - 4.0 * c).sqrt());
        wxy2 - (-uzz)
    };
    let g0 = dd_gap(0.0, 'y');
    assert!(dd_gap(50.0, 'x') > g0, "x-aligned widens gap (wrong sign!)");
    assert!(dd_gap(50.0, 'z') > g0, "z-aligned widens gap (wrong sign!)");
    assert!(dd_gap(50.0, 'y') < 0.0, "y-aligned closes & crosses exact 1:1 Halo resonance!");
    assert!(dd_gap(40.0, 'y') > 0.0 && dd_gap(41.0, 'y') < 0.0);
}

#[test]
fn test_r1_42ode_halo_symplectic_broucke_and_wu_impact() {
    let (x0, z0, vy0, t_h) = (1.173_423_634_6, 0.0800, -0.184_529_258_5, 3.361_069_13);
    let mut st = [0.0; 42];
    st[0] = x0; st[2] = z0; st[4] = vy0;
    for i in 0..6 { st[6 + 6 * i + i] = 1.0; }
    let dt = t_h / 800.0;
    for _ in 0..800 { st = rk4_42(&st, dt, MU_EM); }

    let mut m = [[0.0; 6]; 6];
    for i in 0..6 { for j in 0..6 { m[i][j] = st[6 + 6 * i + j]; } }
    let om = [
        [0.0, -2.0, 0.0, 1.0, 0.0, 0.0],
        [2.0, 0.0, 0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, -1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, -1.0, 0.0, 0.0, 0.0],
    ];
    let mut symp_err = 0.0_f64;
    for i in 0..6 {
        for j in 0..6 {
            let mut val = 0.0;
            for k in 0..6 { for l in 0..6 { val += m[k][i] * om[k][l] * m[l][j]; } }
            symp_err = symp_err.max((val - om[i][j]).abs());
        }
    }
    assert!(symp_err < 1e-7);

    let tr_m: f64 = (0..6).map(|i| m[i][i]).sum();
    let mut tr_m2 = 0.0;
    for i in 0..6 { for k in 0..6 { tr_m2 += m[i][k] * m[k][i]; } }
    let s_nu = (tr_m - 2.0) / 2.0;
    let p_nu = (s_nu * s_nu - (tr_m2 + 2.0) / 4.0) / 2.0;
    let disc = (s_nu * s_nu - 4.0 * p_nu).sqrt();
    let nu1 = 0.5 * (s_nu + disc);
    let nu2 = 0.5 * (s_nu - disc);
    let lam_u = nu1 + (nu1 * nu1 - 1.0).sqrt();
    assert!((nu1 - 373.3613).abs() < 0.01);
    assert!((nu2 - 0.8409).abs() < 0.001);
    assert!((lam_u - 746.7213).abs() < 0.02);

    // W^u lunar-impact verification (Catch 33-1: < R_Moon = 1737.4 km)
    let mut vu = [1.0, 0.2, 0.1, 0.1, 0.1, 0.1];
    for _ in 0..25 {
        let mut nxt = [0.0; 6];
        for i in 0..6 { for j in 0..6 { nxt[i] += m[i][j] * vu[j]; } }
        let n: f64 = nxt.iter().map(|c| c * c).sum::<f64>().sqrt();
        for i in 0..6 { vu[i] = nxt[i] / n; }
    }
    if vu[0] < 0.0 { for c in &mut vu { *c = -*c; } }
    let mut s_wu = [x0 - 1e-4 * vu[0], -1e-4 * vu[1], z0 - 1e-4 * vu[2], -1e-4 * vu[3], vy0 - 1e-4 * vu[4], -1e-4 * vu[5]];
    let mut min_moon_km = 1e9_f64;
    for _ in 0..2000 {
        s_wu = rk4_6(&s_wu, 0.005, MU_EM);
        let dm = ((s_wu[0] - (1.0 - MU_EM)).powi(2) + s_wu[1].powi(2) + s_wu[2].powi(2)).sqrt() * R_EM_KM;
        min_moon_km = min_moon_km.min(dm);
        if dm < 400.0 { break; }
    }
    assert!(min_moon_km < R_MOON_KM, "Expected direct lunar impact < 1737.4 km, got {min_moon_km}");
}

#[test]
fn test_d2_bennu_tag_density_catch_and_c151_c152() {
    let g_surf = MU_BENNU / (R_BENNU * R_BENNU);
    let m_h = 5.0_f64;
    let ah = PI * 0.15_f64 * 0.15;
    let a0 = (ah * 0.08 + 0.02 - m_h * g_surf) / m_h;
    let vt = 0.090_f64;
    let z_const_cm = (vt * vt / (2.0 * a0)) * 100.0;
    assert!((z_const_cm - 80.20).abs() < 0.05);

    // Whole-asteroid rho=1190 gives 11.58 cm; Walsh/Lauretta 2022 subsurface rho=600 gives 18.3 cm!
    let chi_1190 = (1.60 * 1190.0 * ah / (2.0 * m_h)) * vt * vt / a0;
    let z_1190 = z_const_cm * chi_1190.ln_1p() / chi_1190;
    assert!((z_1190 - 11.58).abs() < 0.05);
    let chi_600 = (1.60 * 600.0 * ah / (2.0 * m_h)) * vt * vt / a0;
    let z_600 = z_const_cm * chi_600.ln_1p() / chi_600;
    assert!(z_600 > 18.0 && z_600 < 18.6);
}

#[test]
fn test_p1_keyed_rct_bit_exact_seam_parity() {
    let mut rng = SplitMix64::new(0x5750_3033_335F_5243);
    let first_u64 = rng.next_u64();
    assert_eq!(first_u64, 0xda93_92ed_940a_41ee);
    let tol = 1e-8_f64;
    let (mut arm_a, mut arm_b, mut b01, mut c10) = (0usize, 0usize, 0usize, 0usize);
    for idx in 0..1600 {
        let (ok_a, ok_b) = match idx % 4 {
            0 => {
                let sv = 10.0_f64.powf(rng.uniform(-8.0, -4.0));
                let c2 = 1.0 / sv;
                let r_ref = 2.0 * (1.0 - sv) / (3.0 - 2.0 * sv + (9.0 - 8.0 * sv).sqrt());
                let naive = 0.5 * (2.0 - 3.0 * c2 + (9.0 * c2 * c2 - 8.0 * c2).sqrt());
                ((naive - r_ref).abs() / r_ref <= tol, true)
            }
            1 => {
                let u = 10.0_f64.powf(rng.uniform(-8.0, -4.0));
                let sq = (1.0 - 4.0 * u * u).sqrt();
                let r_ref = (2.0 * u * u) / (1.0 + sq);
                let naive = 1.0 - 0.5 * (1.0 + sq);
                ((naive - r_ref).abs() / r_ref <= tol, true)
            }
            2 => {
                let chi = 10.0_f64.powf(rng.uniform(-12.0, -7.0));
                let r_ref = chi.ln_1p() / chi;
                let naive = (1.0 + chi).ln() / chi;
                ((naive - r_ref).abs() / r_ref <= tol, true)
            }
            _ => {
                let h_v = rng.uniform(75.0, 130.0);
                let g_s = MU_BENNU / (R_BENNU * R_BENNU);
                let eta = 2.0 * g_s * h_v / 0.01;
                let dx = (OMEGA_BENNU * (56.0_f64.to_radians()).cos() * h_v * h_v / 0.10)
                    * 4.0 * (2.0 + (1.0 + eta).sqrt()) / (3.0 * ((1.0 + eta).sqrt() + 1.0).powi(2));
                (dx <= 8.0, dx > 8.0)
            }
        };
        arm_a += usize::from(ok_a);
        arm_b += usize::from(ok_b);
        if !ok_a && ok_b { b01 += 1; } else if ok_a && !ok_b { c10 += 1; }
    }
    eprintln!("WP033 Rust RCT seam first_u64 = 0x{first_u64:016x} | Arm A = {arm_a}/1600 | Arm B = {arm_b}/1600 | b01 = {b01} | c10 = {c10}");
    assert_eq!(arm_a, 520);
    assert_eq!(arm_b, 1600);
    assert_eq!(b01, 1080);
    assert_eq!(c10, 0);
}
