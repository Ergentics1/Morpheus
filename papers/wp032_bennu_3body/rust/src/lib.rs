//! Zero-crate independent Rust cross-verifier for Ergentics Working Paper 032
//! (Horizon Monograph IC: Bennu Triaxial Proximity, 3D Multi-Tether FEM/FDIR,
//! CRTBP L4 Routh Stabilization, and Yoshida-4 General Equal-Mass Three-Body Motion).
//!
//! Author: Gemini 4 Neon ([G4N] / [E->G4N]) for Morpheus (MIT License).

use std::f64::consts::PI;

pub const MU_BENNU: f64 = 4.892;
pub const R_BENNU: f64 = 246.0;
pub const OMEGA_BENNU: f64 = 2.0 * PI / (4.296 * 3600.0);
pub const J2_BENNU: f64 = 0.0175;
pub const C22_BENNU: f64 = 0.0058;
pub const A_SRP_BENNU: f64 = 1.007e-7;

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

pub fn sim_crtbp_l4(mu: f64, ks: f64, r0: f64, steps: usize, t_end: f64) -> f64 {
    let x_l = 0.5 - mu;
    let y_l = 3.0_f64.sqrt() / 2.0;
    let (mut x, mut y, mut vx, mut vy) = (x_l + r0, y_l, 0.0, 0.0);
    let dt = t_end / (steps as f64);
    let mut max_r = 0.0_f64;

    let acc = |xv: f64, yv: f64, vxv: f64, vyv: f64| -> (f64, f64) {
        let dx1 = xv + mu;
        let dx2 = xv - 1.0 + mu;
        let r1_3 = (dx1 * dx1 + yv * yv).powf(1.5);
        let r2_3 = (dx2 * dx2 + yv * yv).powf(1.5);
        (
            2.0 * vyv + xv - (1.0 - mu) * dx1 / r1_3 - mu * dx2 / r2_3 - ks * (xv - x_l),
            -2.0 * vxv + yv - (1.0 - mu) * yv / r1_3 - mu * yv / r2_3 - ks * (yv - y_l),
        )
    };

    for _ in 0..steps {
        let (ax1, ay1) = acc(x, y, vx, vy);
        let (vx2, vy2) = (vx + 0.5 * dt * ax1, vy + 0.5 * dt * ay1);
        let (ax2, ay2) = acc(x + 0.5 * dt * vx, y + 0.5 * dt * vy, vx2, vy2);
        let (vx3, vy3) = (vx + 0.5 * dt * ax2, vy + 0.5 * dt * ay2);
        let (ax3, ay3) = acc(x + 0.5 * dt * vx2, y + 0.5 * dt * vy2, vx3, vy3);
        let (vx4, vy4) = (vx + dt * ax3, vy + dt * ay3);
        let (ax4, ay4) = acc(x + dt * vx3, y + dt * vy3, vx4, vy4);
        x += (dt / 6.0) * (vx + 2.0 * vx2 + 2.0 * vx3 + vx4);
        y += (dt / 6.0) * (vy + 2.0 * vy2 + 2.0 * vy3 + vy4);
        vx += (dt / 6.0) * (ax1 + 2.0 * ax2 + 2.0 * ax3 + ax4);
        vy += (dt / 6.0) * (ay1 + 2.0 * ay2 + 2.0 * ay3 + ay4);
        max_r = max_r.max((x - x_l).hypot(y - y_l));
    }
    max_r
}

fn acc3(p: &[[f64; 2]; 3]) -> [[f64; 2]; 3] {
    let mut a = [[0.0; 2]; 3];
    for i in 0..3 {
        for j in (i + 1)..3 {
            let dx = p[j][0] - p[i][0];
            let dy = p[j][1] - p[i][1];
            let r2 = dx * dx + dy * dy;
            let inv3 = 1.0 / (r2 * r2.sqrt());
            a[i][0] += dx * inv3;
            a[i][1] += dy * inv3;
            a[j][0] -= dx * inv3;
            a[j][1] -= dy * inv3;
        }
    }
    a
}

pub fn energy3(p: &[[f64; 2]; 3], v: &[[f64; 2]; 3]) -> f64 {
    let t: f64 = 0.5 * v.iter().map(|vi| vi[0] * vi[0] + vi[1] * vi[1]).sum::<f64>();
    let mut u = 0.0;
    for i in 0..3 {
        for j in (i + 1)..3 {
            u -= 1.0 / (p[j][0] - p[i][0]).hypot(p[j][1] - p[i][1]);
        }
    }
    t + u
}

pub fn yoshida4_step(p: &mut [[f64; 2]; 3], v: &mut [[f64; 2]; 3], dt: f64) {
    let cbrt2 = 2.0_f64.cbrt();
    let w1 = 1.0 / (2.0 - cbrt2);
    let w0 = -cbrt2 * w1;
    let cy = [0.5 * w1, 0.5 * (w1 + w0), 0.5 * (w1 + w0), 0.5 * w1];
    let dy = [w1, w0, w1];
    for s in 0..3 {
        for i in 0..3 {
            p[i][0] += cy[s] * dt * v[i][0];
            p[i][1] += cy[s] * dt * v[i][1];
        }
        let a = acc3(p);
        for i in 0..3 {
            v[i][0] += dy[s] * dt * a[i][0];
            v[i][1] += dy[s] * dt * a[i][1];
        }
    }
    for i in 0..3 {
        p[i][0] += cy[3] * dt * v[i][0];
        p[i][1] += cy[3] * dt * v[i][1];
    }
}
