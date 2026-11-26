//! Zero-crate independent Rust cross-verifier for Ergentics Working Paper 033
//! (Horizon Monograph ID: 3D Non-Planar CRTBP Halo/Lissajous Manifolds, Rotating-Symplectic
//! Floquet Station-Keeping, Theorem G3 Laplace-Constrained L2 Multipole Coupling, and
//! Bennu Nightingale TAG Regolith Sampling Guidance).
//!
//! Author: Gemini 4 Neon ([G4N] / [E->G4N]) for Morpheus (MIT License).

use std::f64::consts::PI;

pub const MU_EM: f64 = 0.012_150_585_6;
pub const R_EM_KM: f64 = 384_400.0;
pub const V_CHAR_EM: f64 = 1024.54;
pub const R_MOON_KM: f64 = 1737.4;
pub const MU_DD: f64 = 0.0091;
pub const R_DD_M: f64 = 1190.0;
pub const MU_BENNU: f64 = 4.892;
pub const R_BENNU: f64 = 246.0;
pub const OMEGA_BENNU: f64 = 2.0 * PI / (4.296 * 3600.0);

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

pub fn solve_l2_quintic(mu: f64) -> f64 {
    let mut g = (mu / 3.0).cbrt();
    for _ in 0..30 {
        let f = g.powi(5) + (3.0 - mu) * g.powi(4) + (3.0 - 2.0 * mu) * g.powi(3)
            - mu * g.powi(2) - 2.0 * mu * g - mu;
        let df = 5.0 * g.powi(4) + 4.0 * (3.0 - mu) * g.powi(3) + 3.0 * (3.0 - 2.0 * mu) * g.powi(2)
            - 2.0 * mu * g - 2.0 * mu;
        g -= f / df;
    }
    g
}

pub fn exact_hess_triad_l2(x: f64, mu: f64, l: f64, axis: char) -> (f64, f64, f64) {
    let offs = match axis {
        'x' => [(l, 0.0, 0.0), (-l, 0.0, 0.0), (0.0, 0.0, 0.0)],
        'y' => [(0.0, l, 0.0), (0.0, -l, 0.0), (0.0, 0.0, 0.0)],
        _ => [(0.0, 0.0, l), (0.0, 0.0, -l), (0.0, 0.0, 0.0)],
    };
    let (mut uxx, mut uyy, mut uzz) = (0.0, 0.0, 0.0);
    for (ox, oy, oz) in offs {
        for (m, sx) in [(1.0 - mu, -mu), (mu, 1.0 - mu)] {
            let (dx, dy, dz) = (x + ox - sx, oy, oz);
            let r2 = dx * dx + dy * dy + dz * dz;
            let r5 = r2 * r2 * r2.sqrt();
            uxx += (m / 3.0) * (3.0 * dx * dx - r2) / r5;
            uyy += (m / 3.0) * (3.0 * dy * dy - r2) / r5;
            uzz += (m / 3.0) * (3.0 * dz * dz - r2) / r5;
        }
    }
    (uxx, uyy, uzz)
}

pub fn crtbp_6(s: &[f64; 6], mu: f64) -> [f64; 6] {
    let (x, y, z, vx, vy, vz) = (s[0], s[1], s[2], s[3], s[4], s[5]);
    let (dx1, dx2) = (x + mu, x - 1.0 + mu);
    let r1_3 = (dx1 * dx1 + y * y + z * z).powf(1.5);
    let r2_3 = (dx2 * dx2 + y * y + z * z).powf(1.5);
    [
        vx, vy, vz,
        2.0 * vy + x - (1.0 - mu) * dx1 / r1_3 - mu * dx2 / r2_3,
        -2.0 * vx + y - (1.0 - mu) * y / r1_3 - mu * y / r2_3,
        -(1.0 - mu) * z / r1_3 - mu * z / r2_3,
    ]
}

pub fn rk4_6(s: &[f64; 6], dt: f64, mu: f64) -> [f64; 6] {
    let k1 = crtbp_6(s, mu);
    let mut s2 = [0.0; 6];
    for i in 0..6 { s2[i] = s[i] + 0.5 * dt * k1[i]; }
    let k2 = crtbp_6(&s2, mu);
    let mut s3 = [0.0; 6];
    for i in 0..6 { s3[i] = s[i] + 0.5 * dt * k2[i]; }
    let k3 = crtbp_6(&s3, mu);
    let mut s4 = [0.0; 6];
    for i in 0..6 { s4[i] = s[i] + dt * k3[i]; }
    let k4 = crtbp_6(&s4, mu);
    let mut out = [0.0; 6];
    for i in 0..6 { out[i] = s[i] + (dt / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]); }
    out
}

pub fn crtbp_42(st: &[f64; 42], mu: f64) -> [f64; 42] {
    let (x, y, z, vx, vy, vz) = (st[0], st[1], st[2], st[3], st[4], st[5]);
    let (dx1, dx2) = (x + mu, x - 1.0 + mu);
    let r1_2 = dx1 * dx1 + y * y + z * z;
    let r2_2 = dx2 * dx2 + y * y + z * z;
    let (r1, r2) = (r1_2.sqrt(), r2_2.sqrt());
    let (r1_3, r2_3) = (r1 * r1_2, r2 * r2_2);
    let (r1_5, r2_5) = (r1_3 * r1_2, r2_3 * r2_2);
    let (m1, m2) = (1.0 - mu, mu);
    let uxx = 1.0 - m1 / r1_3 - m2 / r2_3 + 3.0 * m1 * dx1 * dx1 / r1_5 + 3.0 * m2 * dx2 * dx2 / r2_5;
    let uyy = 1.0 - m1 / r1_3 - m2 / r2_3 + 3.0 * m1 * y * y / r1_5 + 3.0 * m2 * y * y / r2_5;
    let uzz = -m1 / r1_3 - m2 / r2_3 + 3.0 * m1 * z * z / r1_5 + 3.0 * m2 * z * z / r2_5;
    let uxy = 3.0 * m1 * dx1 * y / r1_5 + 3.0 * m2 * dx2 * y / r2_5;
    let uxz = 3.0 * m1 * dx1 * z / r1_5 + 3.0 * m2 * dx2 * z / r2_5;
    let uyz = 3.0 * m1 * y * z / r1_5 + 3.0 * m2 * y * z / r2_5;
    let a = [
        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        [uxx, uxy, uxz, 0.0, 2.0, 0.0],
        [uxy, uyy, uyz, -2.0, 0.0, 0.0],
        [uxz, uyz, uzz, 0.0, 0.0, 0.0],
    ];
    let mut out = [0.0; 42];
    out[0] = vx; out[1] = vy; out[2] = vz;
    out[3] = 2.0 * vy + x - m1 * dx1 / r1_3 - m2 * dx2 / r2_3;
    out[4] = -2.0 * vx + y - m1 * y / r1_3 - m2 * y / r2_3;
    out[5] = -m1 * z / r1_3 - m2 * z / r2_3;
    for i in 0..6 {
        for j in 0..6 {
            let mut sum = 0.0;
            for k in 0..6 { sum += a[i][k] * st[6 + 6 * k + j]; }
            out[6 + 6 * i + j] = sum;
        }
    }
    out
}

pub fn rk4_42(st: &[f64; 42], dt: f64, mu: f64) -> [f64; 42] {
    let k1 = crtbp_42(st, mu);
    let mut s2 = [0.0; 42];
    for i in 0..42 { s2[i] = st[i] + 0.5 * dt * k1[i]; }
    let k2 = crtbp_42(&s2, mu);
    let mut s3 = [0.0; 42];
    for i in 0..42 { s3[i] = st[i] + 0.5 * dt * k2[i]; }
    let k3 = crtbp_42(&s3, mu);
    let mut s4 = [0.0; 42];
    for i in 0..42 { s4[i] = st[i] + dt * k3[i]; }
    let k4 = crtbp_42(&s4, mu);
    let mut out = [0.0; 42];
    for i in 0..42 { out[i] = st[i] + (dt / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]); }
    out
}
