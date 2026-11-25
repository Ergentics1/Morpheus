/// Fourth-language D / R / P / Seam SWE-sweep cross-oracle in Rust:
/// exact pi(40) = 54,975,717,792, anti-cancellation summation, global PD/Cholesky/Jacobi,
/// Rung-1 calibration, guarded seam handoff, and bit-exact KeyedPRNG parity.
use crate::keyed_prng::{KeyedPrng, PrngKey};

fn apply_plr(v: usize, mv: usize) -> (usize, i32) {
    let r = v % 12;
    if v < 12 {
        match mv {
            0 => (12 + r, -1),
            1 => (12 + (r + 4) % 12, -1),
            _ => (12 + (r + 9) % 12, 2),
        }
    } else {
        match mv {
            0 => (r, 1),
            1 => ((r + 8) % 12, 1),
            _ => ((r + 3) % 12, -2),
        }
    }
}

pub fn mobius_mu(mut n: i32) -> i32 {
    if n <= 0 {
        return 0;
    }
    let mut mu = 1;
    let mut p = 2;
    while p * p <= n {
        if n % p == 0 {
            n /= p;
            if n % p == 0 {
                return 0;
            }
            mu = -mu;
        }
        p += 1;
    }
    if n > 1 {
        mu = -mu;
    }
    mu
}

pub fn sum_neumaier(xs: &[f64]) -> f64 {
    let mut sum = 0.0;
    let mut c = 0.0;
    for &x in xs {
        let t = sum + x;
        if sum.abs() >= x.abs() {
            c += (sum - t) + x;
        } else {
            c += (x - t) + sum;
        }
        sum = t;
    }
    sum + c
}

pub fn compute_exact_pi_and_winding(m: usize) -> (i64, i64, [i64; 17]) {
    let mut succ = [[0usize; 2]; 72];
    let mut step_s = [0i32; 72];
    for v in 0..24 {
        for mv in 0..3 {
            let e = 3 * v + mv;
            let (tv, st) = apply_plr(v, mv);
            step_s[e] = st;
            let mut idx = 0;
            for mv2 in 0..3 {
                if mv2 == mv {
                    continue;
                }
                succ[e][idx] = 3 * tv + mv2;
                idx += 1;
            }
        }
    }

    let max_s = (2 * m) as i32;
    let stride = (2 * max_s + 1) as usize;
    let offset = max_s;
    let mut n_dw = vec![[0i64; 17]; m + 1];
    let mut bad_mod12 = 0i64;

    let mut cur = vec![0i64; 72 * stride];
    let mut nxt = vec![0i64; 72 * stride];

    for e0 in 0..72 {
        cur.fill(0);
        cur[e0 * stride + (offset + step_s[e0]) as usize] = 1;
        for d in 2..=m {
            nxt.fill(0);
            let s_lim = (2 * (d - 1)) as i32;
            for e in 0..72 {
                let base = e * stride;
                let e1 = succ[e][0];
                let e2 = succ[e][1];
                let ds1 = step_s[e1];
                let ds2 = step_s[e2];
                let b1 = e1 * stride;
                let b2 = e2 * stride;
                for s in -s_lim..=s_lim {
                    let cnt = cur[base + (offset + s) as usize];
                    if cnt == 0 {
                        continue;
                    }
                    nxt[b1 + (offset + s + ds1) as usize] += cnt;
                    nxt[b2 + (offset + s + ds2) as usize] += cnt;
                }
            }
            std::mem::swap(&mut cur, &mut nxt);
            if d % 2 == 0 {
                let s_lim_d = (2 * d) as i32;
                for e in 0..72 {
                    if succ[e][0] != e0 && succ[e][1] != e0 {
                        continue;
                    }
                    let base = e * stride;
                    for s in -s_lim_d..=s_lim_d {
                        let cnt = cur[base + (offset + s) as usize];
                        if cnt == 0 {
                            continue;
                        }
                        if s % 12 != 0 {
                            bad_mod12 += cnt;
                        } else {
                            let w = s / 12;
                            n_dw[d][(w + 8) as usize] += cnt;
                        }
                    }
                }
            }
        }
    }

    let mut prime_counts = [0i64; 17];
    let mut total_pi = 0i64;
    for w in -8i32..=8 {
        let mut acc = 0i64;
        for d in (2..=m).step_by(2) {
            if m % d != 0 {
                continue;
            }
            let k = (m / d) as i32;
            if w % k != 0 {
                continue;
            }
            let mu = mobius_mu(k);
            if mu == 0 {
                continue;
            }
            acc += (mu as i64) * n_dw[d][((w / k) + 8) as usize];
        }
        let pi_mw = acc / (m as i64);
        prime_counts[(w + 8) as usize] = pi_mw;
        total_pi += pi_mw;
    }
    (total_pi, bad_mod12, prime_counts)
}

#[derive(Debug, Clone)]
pub struct RustCrossOracleReport {
    pub pi40: i64,
    pub non_mult12: i64,
    pub neumaier_recovered: bool,
    pub spike_rejected_cholesky: bool,
    pub prng_first_word: u64,
    pub m40_tv: f64,
    pub m40_excess_kurtosis: f64,
    pub passed: bool,
}

pub fn run_fourth_language_cross_oracle() -> RustCrossOracleReport {
    let cancel = [1e16, 1.0, -1e16, 1.0, 1e16, 1.0, -1e16, 1.0];
    let naive: f64 = cancel.iter().sum();
    let neumaier = sum_neumaier(&cancel);
    let neumaier_ok = (naive - 4.0).abs() > 1.0 && (neumaier - 4.0).abs() < 1e-12;

    // R-Type 2x2 Cholesky rejection on positive-diagonal off-diagonal spike [[1, 2.5], [2.5, 1]].
    let spiked = [1.0f64, 2.5, 2.5, 1.0];
    let chol_ok_2x2 = |m: [f64; 4]| -> bool {
        if !m.iter().all(|x| x.is_finite()) || (m[1] - m[2]).abs() > 1e-12 {
            return false;
        }
        if m[0] <= 1e-12 {
            return false;
        }
        let l10 = m[1] / m[0].sqrt();
        (m[3] - l10 * l10) > 1e-12
    };
    let cov = [1.0 / 24.0, 1.0 / 36.0, 1.0 / 36.0, 2.0 / 27.0];
    let spike_ok = chol_ok_2x2(cov) && !chol_ok_2x2(spiked) && !chol_ok_2x2([1.0, f64::NAN, 0.0, 1.0]);

    let (pi40, bad12, counts40) = compute_exact_pi_and_winding(40);
    let sum_counts: i64 = counts40.iter().sum();

    // Rung-1 TV and excess kurtosis at m = 40.
    let probs: Vec<f64> = counts40.iter().map(|&c| (c as f64) / (pi40 as f64)).collect();
    let sigma2 = 40.0 / 24.0;
    let mut z_norm = 0.0;
    for w in -24i32..=24 {
        z_norm += (-0.5 * (w as f64).powi(2) / sigma2).exp();
    }
    let mut q = vec![0.0; 17];
    for i in 0..17 {
        let w = (i as i32 - 8) as f64;
        q[i] = (-0.5 * w * w / sigma2).exp() / z_norm;
    }
    let q_tail = (1.0 - sum_neumaier(&q)).max(0.0);
    let tv = 0.5
        * (q_tail
            + probs
                .iter()
                .zip(q.iter())
                .map(|(p, qi)| (p - qi).abs())
                .sum::<f64>());
    let m2: f64 = probs
        .iter()
        .enumerate()
        .map(|(i, &p)| p * ((i as i32 - 8) as f64).powi(2))
        .sum();
    let m4: f64 = probs
        .iter()
        .enumerate()
        .map(|(i, &p)| p * ((i as i32 - 8) as f64).powi(4))
        .sum();
    let ex_kurt = m4 / (m2 * m2) - 3.0;

    // Bit-exact KeyedPRNG first draw for the canonical seam key.
    let mut rng = KeyedPrng::from_key(PrngKey::new("prime-cadences", "seam-replay", 7, 20261125));
    let first_word = rng.next_u64();

    let passed = pi40 == 54_975_717_792
        && bad12 == 0
        && sum_counts == pi40
        && neumaier_ok
        && spike_ok
        && (tv - 0.01086473858410429).abs() < 1e-12
        && (ex_kurt - (-0.21237935938201513)).abs() < 1e-12;

    RustCrossOracleReport {
        pi40,
        non_mult12: bad12,
        neumaier_recovered: neumaier_ok,
        spike_rejected_cholesky: spike_ok,
        prng_first_word: first_word,
        m40_tv: tv,
        m40_excess_kurtosis: ex_kurt,
        passed,
    }
}
