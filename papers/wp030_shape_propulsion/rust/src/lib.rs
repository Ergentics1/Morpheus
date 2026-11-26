//! Independent zero-crate Rust verifier for Ergentics Working Paper 030
//! ("Shape-Controlled Gravitational Propulsion Resolved", Horizon Monograph I).
//!
//! Author: Gemini 4 Neon ([G4N] / [E->G4N]) for Morpheus (MIT License).
//! Recomputes H1-H3 factorizations, equilateral-pole unitary Hopf basis (w+, w-),
//! exact zero-spin T_shape divergence, collision-free -90 deg holonomy, coupled
//! 4-body RK4, unassisted 2-mass Landis tether tumbling, Table 1 mission budgets,
//! and bit-exact SplitMix64 keyed-PRNG N=1,600 RCT from first principles.

use std::f64::consts::PI;

pub const MU_EARTH: f64 = 3.986_004_418e14;
pub const R_EARTH_MEAN: f64 = 6.371e6;
pub const SEC_PER_YEAR: f64 = 365.25 * 86400.0;
pub const MU_BENNU: f64 = 4.892;

#[derive(Clone, Copy, Debug)]
pub struct C64 {
    pub re: f64,
    pub im: f64,
}

impl C64 {
    #[inline]
    pub const fn new(re: f64, im: f64) -> Self {
        Self { re, im }
    }
    #[inline]
    pub fn add(self, o: Self) -> Self {
        Self::new(self.re + o.re, self.im + o.im)
    }
    #[inline]
    pub fn sub(self, o: Self) -> Self {
        Self::new(self.re - o.re, self.im - o.im)
    }
    #[inline]
    pub fn mul(self, o: Self) -> Self {
        Self::new(self.re * o.re - self.im * o.im, self.re * o.im + self.im * o.re)
    }
    #[inline]
    pub fn scale(self, s: f64) -> Self {
        Self::new(self.re * s, self.im * s)
    }
    #[inline]
    pub fn conj(self) -> Self {
        Self::new(self.re, -self.im)
    }
    #[inline]
    pub fn norm2(self) -> f64 {
        self.re * self.re + self.im * self.im
    }
    #[inline]
    pub fn abs(self) -> f64 {
        self.re.hypot(self.im)
    }
    #[inline]
    pub fn cis(theta: f64) -> Self {
        Self::new(theta.cos(), theta.sin())
    }
    #[inline]
    pub fn div(self, o: Self) -> Self {
        let d = o.norm2();
        self.mul(o.conj()).scale(1.0 / d)
    }
}

/// Deterministic 64-bit SplitMix64 keyed PRNG matching wp030_audit.py bit-for-bit.
pub struct SplitMix64 {
    state: u64,
}

impl SplitMix64 {
    pub const fn new(seed: u64) -> Self {
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

    pub fn uniform(&mut self, lo: f64, hi: f64) -> f64 {
        lo + (hi - lo) * self.next_f64()
    }
}

pub fn da_par_exact(mu: f64, r: f64, l: f64) -> f64 {
    let eps = l / r;
    let e2 = eps * eps;
    -(2.0 * mu * e2 / (r * r)) * (1.0 - e2 / 3.0) / ((1.0 - e2) * (1.0 - e2))
}

pub fn da_perp_exact(mu: f64, r: f64, l: f64) -> f64 {
    let eps = l / r;
    let e2 = eps * eps;
    let s = (1.0 + e2).sqrt();
    (mu * e2 / (r * r)) * (2.0 / 3.0) * (s * s + s + 1.0) / (s * s * s * (s + 1.0))
}

/// Map equilateral-pole Hopf coordinates (th0, beta, chi) & rates to 3 planar positions & velocities.
pub fn hopf_equilateral_pos_vel(
    r_j: f64,
    th0: f64,
    beta: f64,
    chi: f64,
    dth0: f64,
    db: f64,
    dchi: f64,
) -> ([C64; 3], [C64; 3]) {
    let cb = (0.5 * beta).cos();
    let sb = (0.5 * beta).sin();
    let ep = C64::cis(th0 + 0.5 * chi);
    let em = C64::cis(th0 - 0.5 * chi);
    let wp = ep.scale(r_j * cb);
    let wm = em.scale(r_j * sb);
    let dwp = C64::new(-0.5 * sb * db, cb * (dth0 + 0.5 * dchi)).mul(ep).scale(r_j);
    let dwm = C64::new(0.5 * cb * db, sb * (dth0 - 0.5 * dchi)).mul(em).scale(r_j);

    let s2 = 2.0_f64.sqrt();
    let is2 = 1.0 / s2;
    let is6 = 1.0 / 6.0_f64.sqrt();
    let s23 = (2.0_f64 / 3.0).sqrt();

    let inv_i_s2 = C64::new(0.0, -is2); // 1 / (i * sqrt(2)) = -i / sqrt(2)
    let z1 = wp.add(wm).scale(is2);
    let z2 = wp.sub(wm).mul(inv_i_s2);
    let dz1 = dwp.add(dwm).scale(is2);
    let dz2 = dwp.sub(dwm).mul(inv_i_s2);

    let rs = [
        z1.scale(is2).add(z2.scale(is6)),
        z1.scale(-is2).add(z2.scale(is6)),
        z2.scale(-s23),
    ];
    let drs = [
        dz1.scale(is2).add(dz2.scale(is6)),
        dz1.scale(-is2).add(dz2.scale(is6)),
        dz2.scale(-s23),
    ];
    (rs, drs)
}

#[derive(Debug)]
pub struct FourBodyResult {
    pub de_orb: f64,
    pub w_act: f64,
    pub eq5_ppm: f64,
    pub max_abs_dj: f64,
    pub max_abs_s: f64,
    pub a_f: f64,
    pub e_f: f64,
    pub p_f: f64,
    pub min_sep_over_l: f64,
    pub max_rad_over_l: f64,
    pub t_track_ratio: f64,
}

pub fn run_coupled_4body_hopf(q_max: f64, e0: f64, n_orbits: usize, steps_per_orbit: usize) -> FourBodyResult {
    let m = 3.0;
    let mp = 1000.0 * m;
    let g_const = 1.0 / (mp + m);
    let mu_tot = 1.0;
    let m_red = mp * m / (mp + m);
    let l = 0.02;
    let r_j = 2.0_f64.sqrt() * l;
    let i0 = (2.0 / 3.0) * m * l * l;
    let m_i = m / 3.0;
    let rp = 1.0 - e0;
    let vp = (mu_tot * (1.0 + e0) / rp).sqrt();
    let dt = (2.0 * PI) / (steps_per_orbit as f64);

    let q_and_dq = |rx: f64, ry: f64, vx: f64, vy: f64, ax: f64, ay: f64| -> (f64, f64) {
        if e0 == 0.0 {
            return (q_max, 0.0);
        }
        let r = rx.hypot(ry);
        let rdot = (rx * vx + ry * vy) / r;
        let rddot = (rx * ax + ry * ay + vx * vx + vy * vy - rdot * rdot) / r;
        let k = 80.0;
        let x = k * rdot;
        let q = -q_max * x.tanh();
        let sech2 = if x.abs() < 40.0 {
            let ch = x.cosh();
            1.0 / (ch * ch)
        } else {
            0.0
        };
        let dq = -q_max * k * sech2 * rddot;
        (q, dq)
    };

    let mut rx = rp;
    let mut ry = 0.0;
    let mut vx = 0.0;
    let mut vy = vp;
    let mut chi = 0.0;
    let mut s_spin = 0.0;

    let (q0, _) = q_and_dq(rx, ry, vx, vy, -rx / (rp * rp * rp), 0.0);
    let (rs0, _) = hopf_equilateral_pos_vel(r_j, 0.0, q0.asin(), chi, 0.0, 0.0, 0.0);
    let u0: f64 = rs0
        .iter()
        .map(|r| -g_const * mp * m_i / (rx + r.re).hypot(ry + r.im))
        .sum();
    let e_init = 0.5 * m_red * (vx * vx + vy * vy) + u0;
    let j0 = m_red * (rx * vy - ry * vx) + s_spin;

    let mut w_act = 0.0;
    let mut max_dj = 0.0_f64;
    let mut max_s = 0.0_f64;
    let mut max_t_ratio = 0.0_f64;
    let mut min_sep = 1e9_f64;
    let mut max_rad = 0.0_f64;

    let eval_rhs = |rxv: f64, ryv: f64, vxv: f64, vyv: f64, chiv: f64, sv: f64| {
        let r2 = rxv * rxv + ryv * ryv;
        let th_orb = ryv.atan2(rxv);
        let dth_orb = (rxv * vyv - ryv * vxv) / r2;
        let (q_pos, _) = q_and_dq(rxv, ryv, vxv, vyv, 0.0, 0.0);
        let bv = q_pos.asin();
        let (rs_pos, _) = hopf_equilateral_pos_vel(r_j, th_orb, bv, chiv, 0.0, 0.0, 0.0);
        let mut fx_tot = 0.0;
        let mut fy_tot = 0.0;
        let mut tau = 0.0;
        for r in &rs_pos {
            let dx = rxv + r.re;
            let dy = ryv + r.im;
            let d2 = dx * dx + dy * dy;
            let inv_d3 = 1.0 / (d2 * d2.sqrt());
            let fx = -g_const * mp * m_i * dx * inv_d3;
            let fy = -g_const * mp * m_i * dy * inv_d3;
            fx_tot += fx;
            fy_tot += fy;
            tau += r.re * fy - r.im * fx;
        }
        let ax = fx_tot / m_red;
        let ay = fy_tot / m_red;
        let (q, dq) = q_and_dq(rxv, ryv, vxv, vyv, ax, ay);
        let db = dq / bv.cos();
        let dchi = (2.0 / bv.cos()) * (sv / i0 - dth_orb);
        let (rs, drs) = hopf_equilateral_pos_vel(r_j, th_orb, bv, chiv, dth_orb, db, dchi);
        let mut p_act = 0.0;
        for (r, dr) in rs.iter().zip(drs.iter()) {
            let dx = rxv + r.re;
            let dy = ryv + r.im;
            let d2 = dx * dx + dy * dy;
            let inv_d3 = 1.0 / (d2 * d2.sqrt());
            let fx = -g_const * mp * m_i * dx * inv_d3;
            let fy = -g_const * mp * m_i * dy * inv_d3;
            p_act -= fx * dr.re + fy * dr.im;
        }
        let sep = rs[0]
            .sub(rs[1])
            .abs()
            .min(rs[1].sub(rs[2]).abs())
            .min(rs[2].sub(rs[0]).abs())
            / l;
        let rad = rs[0].abs().max(rs[1].abs()).max(rs[2].abs()) / l;
        (ax, ay, dchi, tau, p_act, (q * q) / (1.0 - q * q), sep, rad)
    };

    for _ in 0..(n_orbits * steps_per_orbit) {
        let (ax1, ay1, c1, t1, p1, tr1, s1, r1) = eval_rhs(rx, ry, vx, vy, chi, s_spin);
        let (vx2, vy2) = (vx + 0.5 * dt * ax1, vy + 0.5 * dt * ay1);
        let (ax2, ay2, c2, t2, p2, _, _, _) =
            eval_rhs(rx + 0.5 * dt * vx, ry + 0.5 * dt * vy, vx2, vy2, chi + 0.5 * dt * c1, s_spin + 0.5 * dt * t1);
        let (vx3, vy3) = (vx + 0.5 * dt * ax2, vy + 0.5 * dt * ay2);
        let (ax3, ay3, c3, t3, p3, _, _, _) =
            eval_rhs(rx + 0.5 * dt * vx2, ry + 0.5 * dt * vy2, vx3, vy3, chi + 0.5 * dt * c2, s_spin + 0.5 * dt * t2);
        let (vx4, vy4) = (vx + dt * ax3, vy + dt * ay3);
        let (ax4, ay4, c4, t4, p4, _, _, _) =
            eval_rhs(rx + dt * vx3, ry + dt * vy3, vx4, vy4, chi + dt * c3, s_spin + dt * t3);
        rx += (dt / 6.0) * (vx + 2.0 * vx2 + 2.0 * vx3 + vx4);
        ry += (dt / 6.0) * (vy + 2.0 * vy2 + 2.0 * vy3 + vy4);
        vx += (dt / 6.0) * (ax1 + 2.0 * ax2 + 2.0 * ax3 + ax4);
        vy += (dt / 6.0) * (ay1 + 2.0 * ay2 + 2.0 * ay3 + ay4);
        chi += (dt / 6.0) * (c1 + 2.0 * c2 + 2.0 * c3 + c4);
        s_spin += (dt / 6.0) * (t1 + 2.0 * t2 + 2.0 * t3 + t4);
        w_act += (dt / 6.0) * (p1 + 2.0 * p2 + 2.0 * p3 + p4);
        max_dj = max_dj.max((m_red * (rx * vy - ry * vx) + s_spin - j0).abs());
        max_s = max_s.max(s_spin.abs());
        max_t_ratio = max_t_ratio.max(tr1);
        min_sep = min_sep.min(s1);
        max_rad = max_rad.max(r1);
    }

    let th_f = ry.atan2(rx);
    let (qf, _) = q_and_dq(rx, ry, vx, vy, 0.0, 0.0);
    let (rsf, _) = hopf_equilateral_pos_vel(r_j, th_f, qf.asin(), chi, 0.0, 0.0, 0.0);
    let uf: f64 = rsf
        .iter()
        .map(|r| -g_const * mp * m_i / (rx + r.re).hypot(ry + r.im))
        .sum();
    let e_final = 0.5 * m_red * (vx * vx + vy * vy) + uf;
    let de = e_final - e_init;
    let eq5_ppm = (de - w_act).abs() / de.abs().max(1e-15) * 1e6;
    let h_f = rx * vy - ry * vx;
    let p_f = h_f * h_f / mu_tot;
    let e_kep = 0.5 * m_red * (vx * vx + vy * vy) - g_const * mp * m / rx.hypot(ry);
    let a_f = -0.5 * m_red * mu_tot / e_kep;
    let e_f = (1.0 - p_f / a_f).max(0.0).sqrt();

    FourBodyResult {
        de_orb: de,
        w_act,
        eq5_ppm,
        max_abs_dj: max_dj,
        max_abs_s: max_s,
        a_f,
        e_f,
        p_f,
        min_sep_over_l: min_sep,
        max_rad_over_l: max_rad,
        t_track_ratio: max_t_ratio,
    }
}

#[derive(Debug)]
pub struct LandisResult {
    pub de_orb: f64,
    pub net_tumble_deg: f64,
    pub max_abs_dj: f64,
}

pub fn run_unassisted_landis_tether(l_min_frac: f64, n_orbits: usize, steps_per_orbit: usize) -> LandisResult {
    let m = 3.0;
    let mp = 1000.0 * m;
    let g_const = 1.0 / (mp + m);
    let m_red = mp * m / (mp + m);
    let l_max = 0.02;
    let l_min = l_min_frac * l_max;
    let m_end = 0.5 * m;
    let e0: f64 = 0.2;
    let rp: f64 = 1.0 - e0;
    let vp: f64 = ((1.0 + e0) / rp).sqrt();
    let dt = (2.0 * PI) / (steps_per_orbit as f64);

    let length_at = |rx: f64, ry: f64, vx: f64, vy: f64| -> f64 {
        let r = rx.hypot(ry);
        let rdot = (rx * vx + ry * vy) / r;
        let s_sw = 0.5 * (1.0 - (20.0 * rdot).tanh());
        l_min + (l_max - l_min) * s_sw
    };

    let mut rx = rp;
    let mut ry = 0.0;
    let mut vx = 0.0;
    let mut vy = vp;
    let mut phi = 0.0;
    let l0 = length_at(rx, ry, vx, vy);
    let mut s_spin = m * l0 * l0 * (vp / rp);

    let u0 = -g_const * mp * m_end / (rx + l0).hypot(ry) - g_const * mp * m_end / (rx - l0).hypot(ry);
    let e_init = 0.5 * m_red * (vx * vx + vy * vy) + u0;
    let j0 = m_red * (rx * vy - ry * vx) + s_spin;
    let mut max_dj = 0.0_f64;
    let mut prev_th = 0.0;
    let mut th_unwrapped = 0.0;

    let eval_rhs = |rxv: f64, ryv: f64, vxv: f64, vyv: f64, ph: f64, sv: f64| {
        let lv = length_at(rxv, ryv, vxv, vyv);
        let x1 = lv * ph.cos();
        let y1 = lv * ph.sin();
        let mut fx_tot = 0.0;
        let mut fy_tot = 0.0;
        let mut tau = 0.0;
        for (x, y) in [(x1, y1), (-x1, -y1)] {
            let dx = rxv + x;
            let dy = ryv + y;
            let d2 = dx * dx + dy * dy;
            let inv_d3 = 1.0 / (d2 * d2.sqrt());
            let fx = -g_const * mp * m_end * dx * inv_d3;
            let fy = -g_const * mp * m_end * dy * inv_d3;
            fx_tot += fx;
            fy_tot += fy;
            tau += x * fy - y * fx;
        }
        (fx_tot / m_red, fy_tot / m_red, sv / (m * lv * lv), tau)
    };

    for _ in 0..(n_orbits * steps_per_orbit) {
        let (ax1, ay1, dp1, t1) = eval_rhs(rx, ry, vx, vy, phi, s_spin);
        let (vx2, vy2) = (vx + 0.5 * dt * ax1, vy + 0.5 * dt * ay1);
        let (ax2, ay2, dp2, t2) =
            eval_rhs(rx + 0.5 * dt * vx, ry + 0.5 * dt * vy, vx2, vy2, phi + 0.5 * dt * dp1, s_spin + 0.5 * dt * t1);
        let (vx3, vy3) = (vx + 0.5 * dt * ax2, vy + 0.5 * dt * ay2);
        let (ax3, ay3, dp3, t3) =
            eval_rhs(rx + 0.5 * dt * vx2, ry + 0.5 * dt * vy2, vx3, vy3, phi + 0.5 * dt * dp2, s_spin + 0.5 * dt * t2);
        let (vx4, vy4) = (vx + dt * ax3, vy + dt * ay3);
        let (ax4, ay4, dp4, t4) =
            eval_rhs(rx + dt * vx3, ry + dt * vy3, vx4, vy4, phi + dt * dp3, s_spin + dt * t3);
        rx += (dt / 6.0) * (vx + 2.0 * vx2 + 2.0 * vx3 + vx4);
        ry += (dt / 6.0) * (vy + 2.0 * vy2 + 2.0 * vy3 + vy4);
        vx += (dt / 6.0) * (ax1 + 2.0 * ax2 + 2.0 * ax3 + ax4);
        vy += (dt / 6.0) * (ay1 + 2.0 * ay2 + 2.0 * ay3 + ay4);
        phi += (dt / 6.0) * (dp1 + 2.0 * dp2 + 2.0 * dp3 + dp4);
        s_spin += (dt / 6.0) * (t1 + 2.0 * t2 + 2.0 * t3 + t4);
        let th = ry.atan2(rx);
        let mut dth = th - prev_th;
        if dth < -PI {
            dth += 2.0 * PI;
        } else if dth > PI {
            dth -= 2.0 * PI;
        }
        th_unwrapped += dth;
        prev_th = th;
        max_dj = max_dj.max((m_red * (rx * vy - ry * vx) + s_spin - j0).abs());
    }

    let lf = length_at(rx, ry, vx, vy);
    let uf = -g_const * mp * m_end / (rx + lf * phi.cos()).hypot(ry + lf * phi.sin())
        - g_const * mp * m_end / (rx - lf * phi.cos()).hypot(ry - lf * phi.sin());
    let e_final = 0.5 * m_red * (vx * vx + vy * vy) + uf;

    LandisResult {
        de_orb: e_final - e_init,
        net_tumble_deg: (phi - th_unwrapped).abs().to_degrees(),
        max_abs_dj: max_dj,
    }
}
