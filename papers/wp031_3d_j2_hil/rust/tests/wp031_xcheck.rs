use wp031_rust::*;

#[test]
fn test_d1_so3_holonomy_axis_and_c141() {
    let rtot = [[0.0, 1.0, 0.0], [0.0, 0.0, -1.0], [-1.0, 0.0, 0.0]];
    let mv = |v: [f64; 3]| -> [f64; 3] {
        [
            rtot[0][0] * v[0] + rtot[0][1] * v[1] + rtot[0][2] * v[2],
            rtot[1][0] * v[0] + rtot[1][1] * v[1] + rtot[1][2] * v[2],
            rtot[2][0] * v[0] + rtot[2][1] * v[1] + rtot[2][2] * v[2],
        ]
    };
    assert_eq!(mv([1.0, 0.0, 0.0]), [0.0, 0.0, -1.0]);
    assert_eq!(mv([1.0, 1.0, -1.0]), [1.0, 1.0, -1.0]);
    // Catch NEG-W18: fig1's printed axis [-1, 1, -1] is NOT fixed by R_tot
    assert_eq!(mv([-1.0, 1.0, -1.0]), [1.0, 1.0, 1.0]);

    let mut max_def = 0.0_f64;
    for i in 0..=200 {
        let eps = 1e-3 + 0.019 * (i as f64) / 200.0;
        for j in 0..=200 {
            let gam = 0.5 * std::f64::consts::PI * (j as f64) / 200.0;
            max_def = max_def.max((r3d_ratio(eps, gam) - 1.0).abs());
        }
    }
    assert!(max_def > 1.33e-3 && max_def < 1.463e-3);
}

#[test]
fn test_r1_3d_j2_point_mass_control_and_c142() {
    let sph = integrate_j2_point_mass(0.0, 3.0);
    let obl = integrate_j2_point_mass(0.05, 3.0);
    assert!(sph.max_djz < 1e-12 && sph.max_djperp < 1e-12);
    assert!(obl.max_djz < 1e-11);
    // Catch NEG-W17: L = 0 point-mass J2 baseline accounts for 99.96% of 3.0870 & 88% of -0.0366
    assert!((obl.max_djperp - 3.0859).abs() < 2e-3);
    assert!((obl.delta_l_norm - (-0.0322)).abs() < 1e-3);
    assert!((obl.i_end_deg - 44.3968).abs() < 1e-3);

    let a_ref = R_P_SAFE / 0.75;
    let earth_j2 = J2_E * (R_E / a_ref).powi(2);
    assert!((earth_j2 - 5.087565e-4).abs() < 1e-8);
}

#[test]
fn test_d2_k9_safe_perigee_and_dimensional_catch() {
    let e_opt = solve_k9_root();
    assert!((0.2817015579087739..=0.28170155790877416).contains(&e_opt));
    assert!(g_k9(e_opt).abs() < 1e-15);

    // Catch NEG-W16: printed prefactor is dimensionless, missing sqrt(mu / r_p)
    let pref_printed = T_YR * MU_E.sqrt() * L_REF * L_REF / (std::f64::consts::PI * R_P_SAFE.powf(3.5));
    let pref_exact = T_YR * MU_E * L_REF * L_REF / (std::f64::consts::PI * R_P_SAFE.powi(4));
    let v_cp = (MU_E / R_P_SAFE).sqrt();
    assert!((pref_exact / pref_printed - v_cp).abs() < 1e-9);

    assert!((pref_exact * f_safe_perigee(0.25) - 198.5826).abs() < 1e-4);
    assert!((pref_exact * f_safe_perigee(e_opt) - 199.8882).abs() < 1e-4);
    assert!((pref_exact * f_safe_perigee(0.40) - 186.6844).abs() < 1e-4);
}

#[test]
fn test_d3_f36_sizing_and_theorem_g4() {
    let e_hil = 0.25_f64;
    let a_hil = R_P_SAFE / (1.0 - e_hil);
    let p_hil = R_P_SAFE * (1.0 + e_hil);
    let t_orb = 2.0 * std::f64::consts::PI * (a_hil.powi(3) / MU_E).sqrt();
    let om_max = (MU_E * p_hil).sqrt() / (R_P_SAFE * R_P_SAFE);
    let om_spin = 2.0 * om_max;

    // F36 exact slack deficit
    let deficit = (1.0 - e_hil).powi(-3) - 1.0;
    assert!((deficit - 37.0 / 27.0).abs() < 1e-14);

    // C144 tapered Zylon sizing & resonance
    let m_tip = M_CRAFT / 3.0;
    let t_pk = m_tip * L_REF * (om_spin * om_spin + 3.0 * MU_E / R_P_SAFE.powi(3));
    let lam = RHO_ZYLON * (om_spin * L_REF).powi(2) / (2.0 * SIGMA_ALLOW);
    let m_zylon = RHO_ZYLON * (t_pk / SIGMA_ALLOW) * (4.0 * L_REF) * ((lam.exp() - 1.0) / lam);
    assert!((m_zylon - 6.7362).abs() < 5e-4);
    let f1 = (1.0 / (2.0 * L_REF)) * (SIGMA_ALLOW / RHO_ZYLON).sqrt();
    assert!((f1 * t_orb - 192.5462).abs() < 1e-3);

    // Theorem G4 (NEG-W15): exact quadrature parity, F_tan = 0, and heat barrier
    let de_full = (2.0 * MU_E * M_CRAFT * L_REF * L_REF / p_hil.powi(3)) * (3.0 * e_hil + e_hil.powi(3));
    let p_orb_full = de_full / t_orb;
    for &(q, expected_heat_min) in &[(0.50, 468.0), (0.80, 2253.0), (0.90, 6610.0)] {
        let g4 = theorem_g4_eval(q, om_spin);
        let rel_err = (g4.p_circ_num - g4.p_circ_exact).abs() / g4.p_circ_exact;
        assert!(rel_err < 1e-6);
        assert!(g4.f_tan_max < 1e-11);
        assert!(g4.t_min > 30.0);
        assert!(g4.p_heat_elec > expected_heat_min);
        assert!(g4.p_heat_elec / (q * p_orb_full) > 14.77);
    }
}

#[test]
fn test_p1_keyed_rct_bit_exact_seam_parity() {
    let mut rng = SplitMix64::new(SEED_WP031);
    let first_u64 = rng.next_u64();
    assert_eq!(first_u64, 0xc844_f9d6_84ec_259c);

    let mut rng = SplitMix64::new(SEED_WP031);
    let n_trials = 1600usize;
    let mut arm_a = 0usize;
    let mut arm_b = 0usize;
    let loss = 1.0 / ETA_ACT - ETA_REG;

    for _ in 0..n_trials {
        let u_e = rng.next_f64();
        let u_q = rng.next_f64();
        let u_eps = rng.next_f64();
        let u_gam = rng.next_f64();

        let e = 0.15 + 0.20 * u_e;
        let q = 0.10 + 0.60 * u_q;
        let eps = 1.0e-3 + 0.019 * u_eps;
        let gam = 0.5 * std::f64::consts::PI * u_gam;

        let om_min_ratio = (1.0 - e).powf(-1.5);
        let spin_a = (0.40 + 0.95 * u_eps) * om_min_ratio;
        if spin_a > om_min_ratio {
            arm_a += 1;
        }

        let r3d = r3d_ratio(eps, gam);
        let s_q = (1.0 - q * q).sqrt();
        let t_min_factor = (1.0 - q).sqrt() / (s_q * s_q);
        let p_heat_dimless = loss * q / (std::f64::consts::PI * s_q.powi(3));
        if (r3d - 1.0).abs() < 1.5e-3 && t_min_factor > 0.0 && p_heat_dimless > 0.0 {
            arm_b += 1;
        }
    }
    // Bit-exact Python <-> Rust RCT parity
    assert_eq!(arm_a, 592);
    assert_eq!(arm_b, 1600);
}
