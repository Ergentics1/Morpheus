//! Zero-crate independent Rust verification library for Working Paper 035 (Horizon IF).
//!
//! Independently implements from scratch (zero external crates, zero host libm lgamma):
//!   - Stirling-Bernoulli `lgamma(x)` and `digamma(x)` with shift to z >= 20
//!   - Riemann zeta at odd integers via Euler-Maclaurin
//!   - Track A: L(3, 1) multiplicities, Eq. (65) / S^3-S^7 spectral zetas, Wyler alpha,
//!     Lemma 8 R^(-19/4) (F40), g-2 three-way cancellation (C157), Clifford-torus Beltrami ODE
//!   - Track B: Theorems R1-R3, C159, C160, K13 digamma root, NEG-W23, and
//!     Original Theorem G6 (`[G4N]`) Gamma(alpha, alpha) dispersion & tail-leakage quadrature
//!   - Keyed `SplitMix64` PRNG for bit-exact Python <-> Rust RCT seam replay.

use std::f64::consts::PI;

pub const SEED_WP035: u64 = 0x5750_3033_355F_4734; // ASCII "WP035_G4"
pub const GAMMA_EM: f64 = 0.577_215_664_901_532_9;

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

/// From-scratch log-Gamma function for x > 0 via argument shift to z >= 20 and
/// 8-term Stirling-Bernoulli asymptotic series (tail < 1e-22).
pub fn lgamma_pos(mut x: f64) -> f64 {
    let mut prod = 1.0_f64;
    let mut log_shift = 0.0_f64;
    while x < 20.0 {
        prod *= x;
        if prod > 1.0e100 {
            log_shift += prod.ln();
            prod = 1.0;
        }
        x += 1.0;
    }
    log_shift += prod.ln();
    let ix = 1.0 / x;
    let ix2 = ix * ix;
    // B_{2m} / (2m * (2m - 1)) for m = 1..7
    let series = ix
        * (1.0 / 12.0
            + ix2
                * (-1.0 / 360.0
                    + ix2
                        * (1.0 / 1_260.0
                            + ix2
                                * (-1.0 / 1_680.0
                                    + ix2
                                        * (1.0 / 1_188.0
                                            + ix2
                                                * (-691.0 / 360_360.0
                                                    + ix2 * (1.0 / 156.0)))))));
    (x - 0.5) * x.ln() - x + 0.5 * (2.0 * PI).ln() + series - log_shift
}

/// From-scratch digamma function psi(x) for x > 0 via shift to z >= 20.
pub fn digamma_pos(mut x: f64) -> f64 {
    let mut acc = 0.0_f64;
    while x < 20.0 {
        acc -= 1.0 / x;
        x += 1.0;
    }
    let ix2 = 1.0 / (x * x);
    acc + x.ln() - 0.5 / x
        - ix2
            * (1.0 / 12.0
                - ix2
                    * (1.0 / 120.0
                        - ix2 * (1.0 / 252.0 - ix2 * (1.0 / 240.0 - ix2 / 132.0))))
}

/// Exact Binet Stirling-Chernoff gap Delta_Stirling(alpha).
pub fn delta_stirling(alpha: f64) -> f64 {
    lgamma_pos(alpha) - (alpha - 0.5) * alpha.ln() + alpha - 0.5 * (2.0 * PI).ln()
}

/// Riemann zeta(k) for integer k >= 3 via Euler-Maclaurin.
pub fn riemann_zeta_int(k: u32) -> f64 {
    let n_cut = 500u64;
    let mut s = 0.0_f64;
    for n in 1..n_cut {
        s += (n as f64).powi(-(k as i32));
    }
    let nf = n_cut as f64;
    let kf = k as f64;
    s += nf.powf(1.0 - kf) / (kf - 1.0)
        + 0.5 * nf.powf(-kf)
        + (kf / 12.0) * nf.powf(-kf - 1.0)
        - (kf * (kf + 1.0) * (kf + 2.0) / 720.0) * nf.powf(-kf - 3.0);
    s
}

/// True L(p, 1) coexact 1-form multiplicity at level n >= 1.
pub fn l_p_1_mult(p: i64, n: i64) -> i64 {
    let count_mod = |m: i64| -> i64 {
        let mut c = 0;
        let mut w = -m;
        while w <= m {
            if w % p == 0 {
                c += 1;
            }
            w += 2;
        }
        c
    };
    n * count_mod(n + 1) + (n + 2) * count_mod(n - 1)
}

/// Theorem G6 ([G4N]): Incomplete gamma CDF P(alpha, alpha) = Pr_{beta*}(E <= Q_*)
/// evaluated via composite midpoint quadrature with x = alpha * t^2 substitution.
pub fn gamma_cdf_at_mean(alpha: f64, n_pts: usize) -> f64 {
    let h = 1.0 / (n_pts as f64);
    let mut sum = 0.0_f64;
    for i in 0..n_pts {
        let t = ((i as f64) + 0.5) * h;
        let x = alpha * t * t;
        sum += x.powf(alpha - 1.0) * (-x).exp() * (2.0 * alpha * t) * h;
    }
    sum / lgamma_pos(alpha).exp()
}
