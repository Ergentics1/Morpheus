//! Independent zero-crate Rust 1.100.0 verification library for Working Paper 031 (Horizon IB).

pub const MU_E: f64 = 3.986004418e14;
pub const R_E: f64 = 6_378_137.0;
pub const J2_E: f64 = 1.08262668e-3;
pub const T_YR: f64 = 365.25 * 86_400.0;
pub const G0: f64 = 9.80665;
pub const R_P_SAFE: f64 = R_E + 600_000.0;
pub const L_REF: f64 = 20_000.0;
pub const M_CRAFT: f64 = 1_000.0;
pub const ETA_ACT: f64 = 0.88;
pub const ETA_REG: f64 = 0.80;
pub const SIGMA_ALLOW: f64 = 1.16e9;
pub const RHO_ZYLON: f64 = 1560.0;
pub const E_ZYLON: f64 = 270.0e9;
pub const SEED_WP031: u64 = 0x5750_3033_315F_4734; // "WP031_G4"

#[derive(Clone, Copy)]
pub struct SplitMix64 {
    state: u64,
}

impl SplitMix64 {
    pub fn new(seed: u64) -> Self {
        Self { state: seed }
    }

    pub fn next_u64(&mut self) -> u64 {
        self.state = self.state.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.state;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }

    pub fn next_f64(&mut self) -> f64 {
        ((self.next_u64() >> 11) as f64) * (1.0 / ((1u64 << 53) as f64))
    }
}

pub fn r3d_ratio(eps: f64, gam: f64) -> f64 {
    let r1 = (1.0 + 2.0 * eps * gam.cos() + eps * eps).sqrt();
    let r2 = (1.0 - 2.0 * eps * gam.cos() + eps * eps).sqrt();
    2.0 * (r1 * r1 + r1 * r2 + r2 * r2) / (3.0 * r1.powi(3) * r2.powi(3) * (r1 + r2))
}

pub fn f_safe_perigee(e: f64) -> f64 {
    (3.0 * e + e.powi(3)) * (1.0 - e) / (1.0 + e).powi(3)
}

pub fn g_k9(e: f64) -> f64 {
    3.0 - 12.0 * e + 6.0 * e * e - 4.0 * e.powi(3) - e.powi(4)
}

pub fn gp_k9(e: f64) -> f64 {
    -12.0 + 12.0 * e - 12.0 * e * e - 4.0 * e.powi(3)
}

pub fn solve_k9_root() -> f64 {
    let mut e = 0.28_f64;
    for _ in 0..12 {
        e -= g_k9(e) / gp_k9(e);
    }
    e
}

fn accel_j2(pos: [f64; 3], mu: f64, j2r2: f64) -> [f64; 3] {
    let [x, y, z] = pos;
    let r2 = x * x + y * y + z * z;
    let r = r2.sqrt();
    let r3 = r2 * r;
    let f0 = -mu / r3;
    let c = -1.5 * mu * j2r2 / (r2 * r3);
    let z2r2 = (z * z) / r2;
    [
        (f0 + c * (1.0 - 5.0 * z2r2)) * x,
        (f0 + c * (1.0 - 5.0 * z2r2)) * y,
        (f0 + c * (3.0 - 5.0 * z2r2)) * z,
    ]
}

pub struct J2Baseline {
    pub max_djz: f64,
    pub max_djperp: f64,
    pub delta_l_norm: f64,
    pub i_end_deg: f64,
}

/// Live 5-orbit 3D RK4 integration of a zero-size point mass (L = 0, M = 3) in oblate J2.
pub fn integrate_j2_point_mass(j2r2: f64, mass_scale: f64) -> J2Baseline {
    let mu = 1.0_f64;
    let i0 = 45.0_f64.to_radians();
    let v0 = (1.0 + 1.5 * j2r2).sqrt();
    let mut s = [1.0, 0.0, 0.0, 0.0, v0 * i0.cos(), v0 * i0.sin()];
    let dt = (2.0 * std::f64::consts::PI) / 2000.0;

    let deriv = |st: [f64; 6]| -> [f64; 6] {
        let a = accel_j2([st[0], st[1], st[2]], mu, j2r2);
        [st[3], st[4], st[5], a[0], a[1], a[2]]
    };
    let lvec = |st: [f64; 6]| -> [f64; 3] {
        [
            mass_scale * (st[1] * st[5] - st[2] * st[4]),
            mass_scale * (st[2] * st[3] - st[0] * st[5]),
            mass_scale * (st[0] * st[4] - st[1] * st[3]),
        ]
    };

    let l0 = lvec(s);
    let l0_norm = (l0[0] * l0[0] + l0[1] * l0[1] + l0[2] * l0[2]).sqrt();
    let mut max_djz = 0.0_f64;
    let mut max_djperp = 0.0_f64;

    for _ in 0..(5 * 2000) {
        let k1 = deriv(s);
        let mut s2 = [0.0; 6];
        for i in 0..6 {
            s2[i] = s[i] + 0.5 * dt * k1[i];
        }
        let k2 = deriv(s2);
        let mut s3 = [0.0; 6];
        for i in 0..6 {
            s3[i] = s[i] + 0.5 * dt * k2[i];
        }
        let k3 = deriv(s3);
        let mut s4 = [0.0; 6];
        for i in 0..6 {
            s4[i] = s[i] + dt * k3[i];
        }
        let k4 = deriv(s4);
        for i in 0..6 {
            s[i] += (dt / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]);
        }
        let lv = lvec(s);
        max_djz = max_djz.max((lv[2] - l0[2]).abs());
        max_djperp = max_djperp.max((lv[0] - l0[0]).hypot(lv[1] - l0[1]));
    }

    let lv = lvec(s);
    let ln = (lv[0] * lv[0] + lv[1] * lv[1] + lv[2] * lv[2]).sqrt();
    J2Baseline {
        max_djz,
        max_djperp,
        delta_l_norm: ln - l0_norm,
        i_end_deg: (lv[2] / ln).acos().to_degrees(),
    }
}

/// Complex number helper for zero-crate Theorem G4 quadrature.
#[derive(Clone, Copy)]
pub struct C64(pub f64, pub f64);

impl C64 {
    pub fn add(self, o: Self) -> Self { Self(self.0 + o.0, self.1 + o.1) }
    pub fn sub(self, o: Self) -> Self { Self(self.0 - o.0, self.1 - o.1) }
    pub fn mul(self, o: Self) -> Self { Self(self.0 * o.0 - self.1 * o.1, self.0 * o.1 + self.1 * o.0) }
    pub fn scale(self, s: f64) -> Self { Self(self.0 * s, self.1 * s) }
    pub fn conj(self) -> Self { Self(self.0, -self.1) }
    pub fn abs(self) -> f64 { self.0.hypot(self.1) }
    pub fn exp_i(th: f64) -> Self { Self(th.cos(), th.sin()) }
}

pub struct G4Point {
    pub p_circ_num: f64,
    pub p_circ_exact: f64,
    pub p_heat_elec: f64,
    pub t_min: f64,
    pub t_max: f64,
    pub f_tan_max: f64,
}

/// Independent numerical quadrature of Theorem G4 stationary-quadrupole spin-tensioned Hopf wave.
pub fn theorem_g4_eval(q: f64, om_spin: f64) -> G4Point {
    let m_tip = M_CRAFT / 3.0;
    let i0 = M_CRAFT * L_REF * L_REF;
    let s_q = (1.0 - q * q).sqrt();
    let b = (-s_q).acos();
    let om_w = om_spin / s_q;
    let inv_s2 = 1.0 / 2.0_f64.sqrt();
    let inv_s6 = 1.0 / 6.0_f64.sqrt();
    let to_rhos = |wp: C64, wm: C64| -> [C64; 3] {
        let z1 = wp.add(wm).scale(inv_s2);
        // (wp - wm) / (i sqrt(2)) = -i (wp - wm) / sqrt(2)
        let diff = wp.sub(wm);
        let z2 = C64(diff.1 * inv_s2, -diff.0 * inv_s2);
        [
            z1.scale(inv_s2).add(z2.scale(inv_s6)),
            z1.scale(-inv_s2).add(z2.scale(inv_s6)),
            z2.scale(-2.0 * inv_s6),
        ]
    };

    let n = 2000usize;
    let dpsi = 2.0 * std::f64::consts::PI / (n as f64);
    let mut p_in = 0.0_f64;
    let mut t_min = f64::INFINITY;
    let mut t_max = f64::NEG_INFINITY;
    let mut f_tan_max = 0.0_f64;

    for idx in 0..n {
        let psi = (idx as f64) * dpsi;
        let wp = C64::exp_i(-psi).scale(3.0_f64.sqrt() * L_REF * (0.5 * b).cos());
        let wm = C64::exp_i(psi).scale(3.0_f64.sqrt() * L_REF * (0.5 * b).sin());
        let dwp = C64(0.0, -om_w).mul(wp);
        let dwm = C64(0.0, om_w).mul(wm);
        let d2wp = wp.scale(-(om_w * om_w));
        let d2wm = wm.scale(-(om_w * om_w));
        let rs = to_rhos(wp, wm);
        let vs = to_rhos(dwp, dwm);
        let accs = to_rhos(d2wp, d2wm);
        for k in 0..3 {
            let rmag = rs[k].abs();
            let u_rad = rs[k].scale(1.0 / rmag);
            let v_rad = vs[k].mul(u_rad.conj()).0;
            let a_proj = accs[k].mul(u_rad.conj());
            let tk = -m_tip * a_proj.0;
            let ftan = (m_tip * a_proj.1).abs();
            t_min = t_min.min(tk);
            t_max = t_max.max(tk);
            f_tan_max = f_tan_max.max(ftan);
            let pw = -tk * v_rad;
            if pw > 0.0 {
                p_in += pw;
            }
        }
    }

    let p_circ_num = p_in / (n as f64);
    let p_circ_exact = (q / (std::f64::consts::PI * s_q.powi(3))) * i0 * om_spin.powi(3);
    let loss = 1.0 / ETA_ACT - ETA_REG;
    G4Point {
        p_circ_num,
        p_circ_exact,
        p_heat_elec: loss * p_circ_exact,
        t_min,
        t_max,
        f_tan_max,
    }
}
