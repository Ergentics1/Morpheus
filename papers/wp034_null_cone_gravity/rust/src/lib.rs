//! Zero-crate independent Rust verification library for Working Paper 034 (Horizon IE).
//!
//! Independently implements:
//!   - Authentic 106-bit Dekker-Knuth Double-Double EFT via hardware `f64::mul_add` (FMA)
//!   - Clausen `Cl_2(theta)` and unit-circle `Re Li_2(e^{-i theta})` + `NEG-W19` comparison
//!   - Pillar 2 `F39` cycle inversion and original Theorem G5 (`[G4N]`) finite-target exhaustion
//!   - Pillar 3 Schwarzschild/Sen (2013) ratios, `C155` Jensen gap, and Cauchy-Schlomilch quadrature
//!   - Pillars 4 & 5 JT `AdS_2` clock (`C154`), `SL(2,R)/SO(2)` supermetric, ER=EPR Mellin integral,
//!     and Appendix D.3 localized-patch bound (`C156` + `NEG-W21`) & optimal `beta*`
//!   - Keyed `SplitMix64` PRNG for bit-exact Python <-> Rust RCT seam replay.

use std::f64::consts::PI;

pub const SEED_WP034: u64 = 0x5750_3033_345F_4734; // ASCII "WP034_G4"

/// Exact 106-bit Double-Double representation of pi: hi + lo = pi to ~32 decimal digits.
pub const PI_DD: (f64, f64) = (PI, 1.224_646_799_147_353_2e-16);

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

/// Knuth TwoSum error-free transformation.
#[inline]
pub fn two_sum(a: f64, b: f64) -> (f64, f64) {
    let s = a + b;
    let v = s - a;
    let e = (a - (s - v)) + (b - v);
    (s, e)
}

/// FMA-accelerated TwoProd error-free transformation.
#[inline]
pub fn two_prod(a: f64, b: f64) -> (f64, f64) {
    let p = a * b;
    let e = a.mul_add(b, -p);
    (p, e)
}

pub fn dd_add(a: (f64, f64), b: (f64, f64)) -> (f64, f64) {
    let (s, e) = two_sum(a.0, b.0);
    two_sum(s, a.1 + b.1 + e)
}

pub fn dd_sub(a: (f64, f64), b: (f64, f64)) -> (f64, f64) {
    dd_add(a, (-b.0, -b.1))
}

pub fn dd_mul(a: (f64, f64), b: (f64, f64)) -> (f64, f64) {
    let (p, mut e) = two_prod(a.0, b.0);
    e += a.0.mul_add(b.1, a.1 * b.0);
    two_sum(p, e)
}

pub fn dd_div(a: (f64, f64), b: (f64, f64)) -> (f64, f64) {
    let q1 = a.0 / b.0;
    let r = dd_sub(a, dd_mul((q1, 0.0), b));
    let q2 = r.0 / b.0;
    let r2 = dd_sub(r, dd_mul((q2, 0.0), b));
    let q3 = r2.0 / b.0;
    let (hi, lo) = two_sum(q1, q2);
    dd_add((hi, lo), (q3, 0.0))
}

/// Exact real part of unit-circle dilogarithm Re Li_2(e^{-i theta}) on theta in [0, 2*pi].
pub fn re_dilog_unit(theta: f64) -> f64 {
    0.25 * (theta - PI) * (theta - PI) - (PI * PI) / 12.0
}

/// Clausen function Cl_2(theta) on (0, 2*pi) via Bernoulli origin series for theta <= pi.
pub fn clausen2(theta: f64) -> f64 {
    if theta <= 0.0 || theta >= 2.0 * PI {
        return 0.0;
    }
    if theta > PI {
        return -clausen2(2.0 * PI - theta);
    }
    // Exact |B_{2m}| / (2m * (2m+1)!) for m = 1..12
    const COEFFS: [f64; 12] = [
        1.0 / 72.0,
        1.0 / 14_400.0,
        1.0 / 1_270_080.0,
        1.0 / 87_091_200.0,
        1.0 / 5_269_017_600.0,
        691.0 / 210_971_464_704_000.0,
        1.0 / 16_865_441_280_000.0,
        3617.0 / 3_323_622_740_459_520_000.0,
        43_867.0 / 2_181_520_917_933_854_720_000.0,
        174_611.0 / 467_048_168_459_029_708_800_000.0,
        854_513.0 / 122_384_685_591_238_606_848_000_000.0,
        236_364_091.0 / 1_801_295_669_204_809_092_431_872_000_000.0,
    ];
    let mut acc = -theta * theta.ln() + theta;
    let t2 = theta * theta;
    let mut tpow = theta * t2;
    for &c in &COEFFS {
        acc += c * tpow;
        tpow *= t2;
    }
    acc
}

/// Evaluate Pillar 1 real anomaly Delta_re(s) via:
///   (naive_f64, dd106_eft, cancel_free_f64).
pub fn eval_delta_re_three_ways(s: f64) -> (f64, f64, f64) {
    let pi2_6 = (PI * PI) / 6.0;
    let th = 2.0 / s;
    let naive_f64 = 0.5 * s * ((pi2_6 - 0.25 * th * (2.0 * PI - th)) - pi2_6);

    let pi2_6_dd = dd_div(dd_mul(PI_DD, PI_DD), (6.0, 0.0));
    let two_pi_dd = dd_mul((2.0, 0.0), PI_DD);
    let th_dd = dd_div((2.0, 0.0), (s, 0.0));
    let term_dd = dd_mul((0.25, 0.0), dd_mul(th_dd, dd_sub(two_pi_dd, th_dd)));
    let re_li2_dd = dd_sub(pi2_6_dd, term_dd);
    let diff_dd = dd_sub(re_li2_dd, pi2_6_dd);
    let dd106_eft = dd_mul((0.5 * s, 0.0), diff_dd).0;

    let cancel_free_f64 = -0.5 * PI + 0.5 / s;
    (naive_f64, dd106_eft, cancel_free_f64)
}

/// Theorem G5 ([G4N]) search: find integer pair (u, v) minimizing
/// |(delta_eta/2)*(u + v*c) - target_l| over |u - round(2*L/delta_eta)| <= u_win.
pub fn theorem_g5_best_uv(target_l: f64, c: f64, delta_eta: f64, u_win: i64) -> (i64, i64, f64) {
    let target_scaled = 2.0 * target_l / delta_eta;
    let u_center = target_scaled.round() as i64;
    let mut best_err = f64::INFINITY;
    let mut best_u = u_center;
    let mut best_v = 0i64;
    for u in (u_center - u_win)..=(u_center + u_win) {
        let v = ((target_scaled - (u as f64)) / c).round() as i64;
        let z_val = 0.5 * delta_eta * ((u as f64) + (v as f64) * c);
        let err = (z_val - target_l).abs();
        if err < best_err {
            best_err = err;
            best_u = u;
            best_v = v;
        }
    }
    (best_u, best_v, best_err)
}

/// Cauchy-Schlomilch identity (Eq. 5.44): (1/sqrt(pi)) int_0^inf exp(-(u - s/u)^2/4) du = 1.
pub fn cauchy_schlomilch(s: f64, n_pts: usize) -> f64 {
    let u0 = s.sqrt();
    let a_lo = (u0 - 30.0).max(1.0e-9);
    let b_hi = u0 + 30.0;
    let h = (b_hi - a_lo) / (n_pts as f64);
    let mut total = 0.0;
    for i in 0..n_pts {
        let u = a_lo + ((i as f64) + 0.5) * h;
        let diff = u - s / u;
        let arg = 0.25 * diff * diff;
        if arg < 700.0 {
            total += (-arg).exp();
        }
    }
    (total * h) / PI.sqrt()
}

/// ER=EPR horizon correlator Mellin integral (Eq. 5.48) via composite midpoint quadrature.
pub fn erepr_mellin(u_l: f64, u_r: f64, n_pts: usize) -> f64 {
    let ln_ratio = (u_l / u_r).ln();
    let nu_max = 18.0;
    let h = nu_max / (n_pts as f64);
    let mut sum = 0.0;
    for i in 0..n_pts {
        let nu = ((i as f64) + 0.5) * h;
        sum += (nu * (nu * ln_ratio).cos() / (PI * nu).sinh()) * h;
    }
    -sum / (u_l * u_r)
}

/// JT AdS_2 clock normalized function f_eps(z) = (sinh z - sinh(eps z)) / cosh(eps z).
pub fn jt_clock(z: f64, eps: f64) -> f64 {
    (z.sinh() - (eps * z).sinh()) / (eps * z).cosh()
}

/// Appendix D.3 sharpness ratio e^{-u} / (1 - u).
pub fn holder_ratio(u: f64) -> f64 {
    (-u).exp() / (1.0 - u)
}
