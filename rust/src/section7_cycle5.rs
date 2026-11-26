//! ADPIE Cycle 5 Fourth-Language Verifier (Pure Rust, zero external crates):
//! 1. **Novelty 3 (Theorem D — Three-Pincer Hilbert Class Field Obstruction)** & `Thm 7.19(b)`:
//!    From-scratch 64-point Gauss-Legendre Poitou-Odlyzko verifier unconditionally killing
//!    ALL degrees `n >= 9`, forcing `h_F = 1, u <= 4` at `n = 7, 8`, and killing sextic `u in {16, 32}`.
//! 2. **Theorem 7.11 & `NEG-E10` (ZERO-PARI Pure-Rust Manin Modular Symbols `T_2`):**
//!    Exhaustive genus-13 enumeration (`19` pairs including omitted `X_0^690(1)`, `11` torsion-free,
//!    `4` `Gamma_H` cases) PLUS exact Manin modular symbols `M_2(Gamma_0(M))^-` over `F_1000003`
//!    proving `rank(T_2^4 - 4 T_2^2 + I) = dim` on ALL 19 genus-13 Shimura curves (including `M = 345`)!
//! 3. **Props 7.3, 7.17(b), 7.18(a):**
//!    Exact Siegel real-quadratic scan (`D <= 1200`, exact Gauss narrow class number `h^+`),
//!    exhaustive `|PGL_2(F_8)| = 504` census (`56/56` order-3 elements free on `P^1(F_8)`),
//!    and exact `i128` `gamma_0^k` trace obstruction (`k = 1..12`).

use std::collections::{BTreeMap, BTreeSet, HashMap};

const PI: f64 = 3.141592653589793238462643383279502884;
const EULER_GAMMA: f64 = 0.577215664901532860606512090082402431;
const MOD_Q: i64 = 1_000_003;

#[derive(Debug, Clone)]
pub struct TheoremDPincerReport {
    pub passed: bool,
    pub quadrature_self_check_ok: bool,
    pub q_explicit_formula_lb: f64,
    pub tail15_lb_b42: f64,
    pub tail15_ub: f64,
    pub tail15_e_minus_f2: f64,
    pub deg9_to_14_survivors: i32,
    pub worst_deg9_margin: f64,
    pub worst_deg10_margin: f64,
    pub deg7_max_surviving_u: i32,
    pub deg7_hge2_survivors: i32,
    pub deg7_max_root_disc: f64,
    pub deg8_max_surviving_u: i32,
    pub deg8_hge2_survivors: i32,
    pub deg8_max_root_disc: f64,
    pub deg6_max_surviving_u: i32,
    pub deg6_u16_h1_dead: bool,
    pub deg6_u16_hge2_dead: bool,
    pub deg6_u16_h1_margin: f64,
    pub deg6_u16_hge2_margin: f64,
    pub deg6_old_disc_ceiling: f64,
    pub deg6_new_disc_ceiling: f64,
}

#[derive(Debug, Clone)]
pub struct ShimuraManinT2Report {
    pub passed: bool,
    pub total_pairs: usize,
    pub torsion_free_pairs: usize,
    pub neg_e10_detected: bool,
    pub neg_e10_phi: i64,
    pub neg_e10_e3: i64,
    pub gamma_h_count: usize,
    pub distinct_levels_checked: usize,
    pub full_rank_levels: usize,
    pub m345_manin_dim: usize,
    pub m345_px_rank: usize,
    pub m345_tr_t2_mod_q: i64,
}

#[derive(Debug, Clone)]
pub struct Section7ArithmeticCycle5Report {
    pub passed: bool,
    pub quad_split2_scanned: usize,
    pub quad_hplus1_solutions: usize,
    pub quad_d41_solutions: usize,
    pub quad_d137_solutions: usize,
    pub pgl2_f8_order: usize,
    pub pgl2_f8_order3_count: usize,
    pub pgl2_f8_order3_free_count: usize,
    pub gamma0_powers_obstructed: usize,
}

// ============================================================================
// 1. Novelty 3 (Theorem D — Three-Pincer Hilbert Class Field Obstruction)
// ============================================================================

struct Gl64 {
    t: [f64; 64],
    w: [f64; 64],
    self_check_ok: bool,
}

impl Gl64 {
    fn compute() -> Self {
        let mut t = [0.0f64; 64];
        let mut w = [0.0f64; 64];
        let n = 64usize;
        for i in 0..(n / 2) {
            let mut x = (PI * (i as f64 + 0.75) / (n as f64 + 0.5)).cos();
            let mut dp = 0.0;
            for _ in 0..12 {
                let mut p0 = 1.0;
                let mut p1 = x;
                for k in 2..=n {
                    let dk = k as f64;
                    let p2 = ((2.0 * dk - 1.0) * x * p1 - (dk - 1.0) * p0) / dk;
                    p0 = p1;
                    p1 = p2;
                }
                dp = (n as f64) * (x * p1 - p0) / (x * x - 1.0);
                let dx = p1 / dp;
                x -= dx;
                if dx.abs() < 1e-16 {
                    break;
                }
            }
            let wi = 2.0 / ((1.0 - x * x) * dp * dp);
            t[i] = -x;
            t[n - 1 - i] = x;
            w[i] = wi;
            w[n - 1 - i] = wi;
        }
        let sum_w: f64 = w.iter().sum();
        let sum_x2: f64 = w.iter().zip(t.iter()).map(|(wi, ti)| wi * ti * ti).sum();
        let self_check_ok = (sum_w - 2.0).abs() < 1e-14 && (sum_x2 - 2.0 / 3.0).abs() < 1e-14;
        Self { t, w, self_check_ok }
    }
}

#[inline]
fn poitou_h1(u: f64) -> f64 {
    if u <= 0.0 {
        return 1.0;
    }
    if u >= 2.0 {
        return 0.0;
    }
    ((2.0 - u) * (1.0 + 0.5 * (PI * u).cos()) / 3.0) + (PI * u).sin() / (2.0 * PI)
}

#[derive(Clone, Copy)]
struct PoitouPoint {
    log_a: f64,
    log_b: f64,
    e_val: f64,
    f2: f64,
    f4: f64,
}

fn prime_boost(q: i64, b: f64) -> f64 {
    let lq = (q as f64).ln();
    let mut s = 0.0;
    let mut qm = q as f64;
    let mut m = 1usize;
    while (m as f64) * lq < 2.0 * b {
        s += (4.0 * lq / (1.0 + qm)) * poitou_h1((m as f64) * lq / b);
        qm *= q as f64;
        m += 1;
    }
    s
}

fn eval_poitou(gl: &Gl64, b: f64) -> PoitouPoint {
    let mut i_sinh = 0.0;
    let mut i_cosh = 0.0;
    for i in 0..64 {
        let u = 1.0 + gl.t[i];
        let x = b * u;
        let g = poitou_h1(u);
        let wi = gl.w[i];
        i_sinh += wi * b * (1.0 - g) / x.sinh();
        let ch = (0.5 * x).cosh();
        i_cosh += wi * b * g / (2.0 * ch * ch);
    }
    let i_tail = if b < 18.0 {
        (((2.0 * b).exp() + 1.0) / ((2.0 * b).exp() - 1.0)).ln()
    } else {
        2.0 * (-2.0 * b).exp()
    };
    let log_b = EULER_GAMMA + (4.0 * PI).ln() - i_sinh - i_tail;
    let log_a = log_b + i_cosh;
    PoitouPoint {
        log_a,
        log_b,
        e_val: (8.0 * b) / 3.0,
        f2: prime_boost(2, b),
        f4: prime_boost(4, b),
    }
}

fn best_lb_grid(grid: &[PoitouPoint], deg: f64, rho1: f64, cf2: f64, cf4: f64) -> f64 {
    let mut best = -1e9f64;
    for p in grid {
        let val = rho1 * p.log_a + (1.0 - rho1) * p.log_b - p.e_val / deg + cf2 * p.f2 + cf4 * p.f4;
        if val > best {
            best = val;
        }
    }
    best
}

pub fn verify_theorem_d_pincer() -> TheoremDPincerReport {
    let gl = Gl64::compute();
    let p2 = eval_poitou(&gl, 2.0);
    let mut q_psum = 0.0;
    for p in 2..=60 {
        if is_prime_i64(p) && (p as f64).ln() < 4.0 {
            q_psum += prime_boost(p, 2.0);
        }
    }
    let q_explicit_formula_lb = p2.log_a - p2.e_val + q_psum;

    let p42 = eval_poitou(&gl, 4.2);
    let tail15_e_minus_f2 = p42.e_val - p42.f2;
    let tail15_lb_b42 = (p42.log_a - tail15_e_minus_f2 / 15.0).exp();
    let tail15_ub = ((2.0 / 3.0) * (8.0 * PI * PI).ln() + (2.0 / 45.0) * (9.0 / 4.0f64).ln()).exp();

    let mut grid = Vec::with_capacity(231);
    for i in 0..=230 {
        grid.push(eval_poitou(&gl, 0.5 + 0.05 * (i as f64)));
    }

    let ub_log = |n: i32, u: i32, mode: i32| -> f64 {
        let c = match mode {
            0 => 4.5 * (u as f64),
            1 => (27.0 / 8.0) * (u as f64),
            _ => 2.0 * (u as f64),
        };
        (2.0 / 3.0) * (4.0 * PI * PI).ln() + (2.0 / (3.0 * (n as f64))) * c.ln()
    };

    let mut deg9_to_14_survivors = 0;
    let mut worst_deg9_margin = 1e9f64;
    let mut worst_deg10_margin = 1e9f64;
    let mut deg7_max_surviving_u = 0;
    let mut deg7_hge2_survivors = 0;
    let mut deg7_max_root_disc = 0.0f64;
    let mut deg8_max_surviving_u = 0;
    let mut deg8_hge2_survivors = 0;
    let mut deg8_max_root_disc = 0.0f64;
    let mut deg6_max_surviving_u = 0;
    let mut deg6_u16_h1_dead = false;
    let mut deg6_u16_hge2_dead = false;
    let mut deg6_u16_h1_margin = -1e9f64;
    let mut deg6_u16_hge2_margin = -1e9f64;
    let deg6_old_disc_ceiling = (6.0 * ub_log(6, 32, 0)).exp();
    let deg6_new_disc_ceiling = (6.0 * ub_log(6, 8, 0)).exp();

    for n in 6..=14 {
        let (mode_start, mode_end) = if n % 2 == 0 { (0, 0) } else { (1, 2) };
        let dn = n as f64;
        for mode in mode_start..=mode_end {
            for k in 0..n {
                let u = 1i32 << k;
                let ub = ub_log(n, u, mode);
                let cf2_f = (if mode == 1 { 2.0 } else { 1.0 }) / dn;
                let lb_f = best_lb_grid(&grid, dn, 1.0, cf2_f, 0.0);

                let mut sub_h1 = -1e9f64;
                for j in 1..=k {
                    let rho1 = if j < k {
                        let num = (n as i64) * ((1i64 << (k - j)) - 1);
                        let den = (1i64 << k) - 1;
                        ((num + den - 1) / den) as f64 / dn
                    } else {
                        0.0
                    };
                    let cf4 = (if mode == 1 { 2.0 } else { 1.0 }) / (2.0 * dn);
                    let val = best_lb_grid(&grid, dn * ((1i32 << j) as f64), rho1, 0.0, cf4);
                    if val > sub_h1 {
                        sub_h1 = val;
                    }
                }

                let lb_h1 = if k == 0 {
                    lb_f
                } else {
                    let cf4_extra = if mode == 1 { 1.0 / (2.0 * dn) } else { 0.0 };
                    let b1 = best_lb_grid(&grid, dn * (u as f64), 0.0, 1.0 / dn, cf4_extra);
                    let lb_fv1 = lb_f.max(b1).max(sub_h1);
                    let b2_lv = best_lb_grid(&grid, dn * ((u / 2) as f64), 0.0, 1.0 / dn, cf4_extra);
                    let b2_h = best_lb_grid(
                        &grid,
                        dn * (u as f64),
                        0.0,
                        0.0,
                        (if mode == 1 { 2.0 } else { 1.0 }) / (2.0 * dn),
                    );
                    let lb_fv2 = lb_f.max(b2_lv).max(b2_h).max(sub_h1);
                    lb_fv1.min(lb_fv2)
                };

                let mut lb_h2 = lb_f;
                for j in 0..=k {
                    let rho1 = if j == 0 {
                        1.0
                    } else if j < k {
                        let num = (n as i64) * ((1i64 << (k - j)) - 1);
                        let den = (1i64 << k) - 1;
                        ((num + den - 1) / den) as f64 / dn
                    } else {
                        0.0
                    };
                    let val = best_lb_grid(&grid, 2.0 * dn * ((1i32 << j) as f64), rho1, 0.0, 0.0);
                    if val > lb_h2 {
                        lb_h2 = val;
                    }
                }

                let m1 = lb_h1.exp() - ub.exp();
                let m2 = lb_h2.exp() - ub.exp();
                let dead1 = lb_h1 > ub;
                let dead2 = lb_h2 > ub;

                if n >= 9 {
                    if !dead1 || !dead2 {
                        deg9_to_14_survivors += 1;
                    }
                    if n == 9 {
                        worst_deg9_margin = worst_deg9_margin.min(m1).min(m2);
                    }
                    if n == 10 {
                        worst_deg10_margin = worst_deg10_margin.min(m1).min(m2);
                    }
                } else if n == 8 {
                    if !dead2 {
                        deg8_hge2_survivors += 1;
                    }
                    if !dead1 || !dead2 {
                        deg8_max_surviving_u = deg8_max_surviving_u.max(u);
                        deg8_max_root_disc = deg8_max_root_disc.max(ub.exp());
                    }
                } else if n == 7 {
                    if !dead2 {
                        deg7_hge2_survivors += 1;
                    }
                    if !dead1 || !dead2 {
                        deg7_max_surviving_u = deg7_max_surviving_u.max(u);
                        deg7_max_root_disc = deg7_max_root_disc.max(ub.exp());
                    }
                } else if n == 6 {
                    if u == 16 {
                        deg6_u16_h1_dead = dead1;
                        deg6_u16_hge2_dead = dead2;
                        deg6_u16_h1_margin = m1;
                        deg6_u16_hge2_margin = m2;
                    }
                    if !dead1 || !dead2 {
                        deg6_max_surviving_u = deg6_max_surviving_u.max(u);
                    }
                }
            }
        }
    }

    let passed = gl.self_check_ok
        && q_explicit_formula_lb <= 0.0
        && q_explicit_formula_lb > -1e-4
        && tail15_e_minus_f2 > 0.0
        && tail15_lb_b42 > tail15_ub
        && deg9_to_14_survivors == 0
        && worst_deg9_margin > 0.30
        && worst_deg10_margin > 0.90
        && deg7_max_surviving_u == 4
        && deg7_hge2_survivors == 0
        && deg8_max_surviving_u == 4
        && deg8_hge2_survivors == 0
        && deg6_max_surviving_u == 8
        && deg6_u16_h1_dead
        && deg6_u16_hge2_dead
        && deg6_u16_h1_margin > 0.01
        && deg6_u16_hge2_margin > 0.30;

    TheoremDPincerReport {
        passed,
        quadrature_self_check_ok: gl.self_check_ok,
        q_explicit_formula_lb,
        tail15_lb_b42,
        tail15_ub,
        tail15_e_minus_f2,
        deg9_to_14_survivors,
        worst_deg9_margin,
        worst_deg10_margin,
        deg7_max_surviving_u,
        deg7_hge2_survivors,
        deg7_max_root_disc,
        deg8_max_surviving_u,
        deg8_hge2_survivors,
        deg8_max_root_disc,
        deg6_max_surviving_u,
        deg6_u16_h1_dead,
        deg6_u16_hge2_dead,
        deg6_u16_h1_margin,
        deg6_u16_hge2_margin,
        deg6_old_disc_ceiling,
        deg6_new_disc_ceiling,
    }
}

// ============================================================================
// 2. Theorem 7.11 & NEG-E10: Pure-Rust Manin Modular Symbols T_2 (ZERO PARI!)
// ============================================================================

fn is_prime_i64(n: i64) -> bool {
    if n < 2 {
        return false;
    }
    if n % 2 == 0 {
        return n == 2;
    }
    let mut d = 3;
    while d * d <= n {
        if n % d == 0 {
            return false;
        }
        d += 2;
    }
    true
}

fn gcd_i64(mut a: i64, mut b: i64) -> i64 {
    a = a.abs();
    b = b.abs();
    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }
    a
}

fn mod_inv(a: i64, m: i64) -> i64 {
    let (mut t, mut new_t) = (0i64, 1i64);
    let (mut r, mut new_r) = (m, a.rem_euclid(m));
    while new_r != 0 {
        let q = r / new_r;
        let tmp_t = t - q * new_t;
        t = new_t;
        new_t = tmp_t;
        let tmp_r = r - q * new_r;
        r = new_r;
        new_r = tmp_r;
    }
    t.rem_euclid(m)
}

fn canon_p1(c_raw: i64, d_raw: i64, m: i64) -> (i64, i64) {
    let c = c_raw.rem_euclid(m);
    let d = d_raw.rem_euclid(m);
    let g = gcd_i64(c, m);
    if g == m {
        return (0, 1);
    }
    let m1 = m / g;
    let inv = mod_inv(c / g, m1);
    let mut best_d = m;
    for k in 0..g {
        let u = inv + k * m1;
        if gcd_i64(u, m) == 1 {
            let dd = (u * d) % m;
            if dd < best_d {
                best_d = dd;
            }
        }
    }
    (g, best_d)
}

/// Build the exact minus-space Manin modular symbols `M_2(Gamma_0(M))^-` over `F_Q`,
/// compute the Heilbronn-Merel Hecke matrix `T_2`, and return `(dim, rank(T_2^4 - 4 T_2^2 + I), tr(T_2) mod Q)`.
/// Since `S_2^{D/2-new}(Gamma_0(M)) <= S_2(Gamma_0(M)) <= M_2(Gamma_0(M))^-` is an exact Hecke submodule,
/// `rank(T_2^4 - 4 T_2^2 + I) == dim` mod `Q` proves unconditionally over `C` that NO eigenform in
/// `S_2^{D/2-new}(Gamma_0(M))` has `a_2` equal to a root of `t^4 - 4t^2 + 1`.
fn manin_minus_t2_px_rank(m_level: i64) -> (usize, usize, i64) {
    let mut pts_set = BTreeSet::new();
    for c in 0..m_level {
        for d in 0..m_level {
            if gcd_i64(gcd_i64(c, d), m_level) == 1 {
                pts_set.insert(canon_p1(c, d, m_level));
            }
        }
    }
    let pts: Vec<(i64, i64)> = pts_set.into_iter().collect();
    let n = pts.len();
    let mut idx = HashMap::with_capacity(n * 2);
    for (i, &p) in pts.iter().enumerate() {
        idx.insert(p, i);
    }

    // Union-find with sign for 2-term relations: x + x*S = 0 and x + x*I = 0.
    let mut parent: Vec<usize> = (0..n).collect();
    let mut sign: Vec<i64> = vec![1; n];
    let mut killed: Vec<bool> = vec![false; n];

    let find = |mut x: usize, parent: &[usize], sign: &[i64]| -> (usize, i64) {
        let mut s = 1i64;
        while parent[x] != x {
            s *= sign[x];
            x = parent[x];
        }
        (x, s)
    };

    let mut add_rel2 = |x: usize, y: usize, rel_sign: i64| {
        let (rx, sx) = find(x, &parent, &sign);
        let (ry, sy) = find(y, &parent, &sign);
        if rx == ry {
            if sx != rel_sign * sy {
                killed[rx] = true;
            }
        } else {
            parent[rx] = ry;
            sign[rx] = rel_sign * sx * sy;
            if killed[rx] {
                killed[ry] = true;
            }
        }
    };

    for (i, &(c, d)) in pts.iter().enumerate() {
        let i_s = idx[&canon_p1(d, -c, m_level)];
        let i_i = idx[&canon_p1(-c, d, m_level)];
        add_rel2(i, i_s, -1);
        add_rel2(i, i_i, -1);
    }

    let mut rep_map: HashMap<usize, usize> = HashMap::new();
    for i in 0..n {
        let (r, _) = find(i, &parent, &sign);
        if !killed[r] && !rep_map.contains_key(&r) {
            let next_id = rep_map.len();
            rep_map.insert(r, next_id);
        }
    }
    let m_cols = rep_map.len();

    // 3-term T relations: x + x*T + x*T^2 = 0 reduced mod MOD_Q.
    let mut pivots: BTreeMap<usize, BTreeMap<usize, i64>> = BTreeMap::new();
    for (i, &(c, d)) in pts.iter().enumerate() {
        let i1 = idx[&canon_p1(d, -c - d, m_level)];
        let i2 = idx[&canon_p1(-c - d, c, m_level)];
        let mut row: BTreeMap<usize, i64> = BTreeMap::new();
        for j in [i, i1, i2] {
            let (r, s) = find(j, &parent, &sign);
            if !killed[r] {
                let col = rep_map[&r];
                let nv = (row.get(&col).copied().unwrap_or(0) + s).rem_euclid(MOD_Q);
                if nv == 0 {
                    row.remove(&col);
                } else {
                    row.insert(col, nv);
                }
            }
        }
        while let Some((&c0, &v0)) = row.iter().next() {
            if v0 == 0 {
                row.remove(&c0);
                continue;
            }
            if let Some(prow) = pivots.get(&c0) {
                for (&k, &pv) in prow.iter() {
                    let nv = (row.get(&k).copied().unwrap_or(0) - v0 * pv).rem_euclid(MOD_Q);
                    if nv == 0 {
                        row.remove(&k);
                    } else {
                        row.insert(k, nv);
                    }
                }
            } else {
                let inv = mod_inv(v0, MOD_Q);
                let norm: BTreeMap<usize, i64> =
                    row.into_iter().map(|(k, v)| (k, (v * inv) % MOD_Q)).collect();
                pivots.insert(c0, norm);
                break;
            }
        }
    }

    // Back-substitute pivots so each pivot col expresses purely in terms of free cols.
    let piv_cols_desc: Vec<usize> = pivots.keys().copied().rev().collect();
    for c in piv_cols_desc {
        let mut prow = pivots[&c].clone();
        let keys: Vec<usize> = prow.keys().copied().collect();
        for k in keys {
            if k != c && pivots.contains_key(&k) {
                let fac = prow.remove(&k).unwrap();
                for (&k2, &v2) in pivots[&k].iter() {
                    if k2 == k {
                        continue;
                    }
                    let nv = (prow.get(&k2).copied().unwrap_or(0) - fac * v2).rem_euclid(MOD_Q);
                    if nv == 0 {
                        prow.remove(&k2);
                    } else {
                        prow.insert(k2, nv);
                    }
                }
            }
        }
        pivots.insert(c, prow);
    }

    let free_cols: Vec<usize> = (0..m_cols).filter(|c| !pivots.contains_key(c)).collect();
    let mut free_idx: HashMap<usize, usize> = HashMap::new();
    for (i, &c) in free_cols.iter().enumerate() {
        free_idx.insert(c, i);
    }
    let dim = free_cols.len();

    let vec_of_pt = |i: usize| -> Vec<i64> {
        let (r, s) = find(i, &parent, &sign);
        let mut v = vec![0i64; dim];
        if killed[r] {
            return v;
        }
        let col = rep_map[&r];
        if let Some(&fi) = free_idx.get(&col) {
            v[fi] = s.rem_euclid(MOD_Q);
        } else {
            for (&f, &val) in pivots[&col].iter() {
                if f != col {
                    v[free_idx[&f]] = (-s * val).rem_euclid(MOD_Q);
                }
            }
        }
        v
    };

    let mut basis_pts: Vec<Option<(usize, i64)>> = vec![None; dim];
    for i in 0..n {
        let (r, s) = find(i, &parent, &sign);
        if !killed[r] {
            let col = rep_map[&r];
            if let Some(&fi) = free_idx.get(&col) {
                if basis_pts[fi].is_none() {
                    basis_pts[fi] = Some((i, s));
                }
            }
        }
    }

    // Heilbronn-Merel determinant-2 matrices for T_2 (all coprime to odd M).
    let h2: [(i64, i64, i64, i64); 4] = [(1, 0, 0, 2), (2, 0, 0, 1), (2, 1, 0, 1), (1, 0, 1, 2)];
    let mut t2 = vec![vec![0i64; dim]; dim];
    for b in 0..dim {
        let (i_pt, s_pt) = basis_pts[b].unwrap();
        let (c, d) = pts[i_pt];
        for &(a, bb, cc, dd) in &h2 {
            let nc = a * c + cc * d;
            let nd = bb * c + dd * d;
            let j = idx[&canon_p1(nc, nd, m_level)];
            let vj = vec_of_pt(j);
            for r in 0..dim {
                t2[r][b] = (t2[r][b] + s_pt * vj[r]).rem_euclid(MOD_Q);
            }
        }
    }

    let mut tr_t2 = 0i64;
    for i in 0..dim {
        tr_t2 = (tr_t2 + t2[i][i]) % MOD_Q;
    }

    let matmul = |a: &[Vec<i64>], b: &[Vec<i64>]| -> Vec<Vec<i64>> {
        let mut out = vec![vec![0i64; dim]; dim];
        for i in 0..dim {
            for k in 0..dim {
                let aik = a[i][k];
                if aik == 0 {
                    continue;
                }
                for j in 0..dim {
                    out[i][j] = (out[i][j] + aik * b[k][j]) % MOD_Q;
                }
            }
        }
        out
    };

    let t2_2 = matmul(&t2, &t2);
    let t2_4 = matmul(&t2_2, &t2_2);
    let mut px = vec![vec![0i64; dim]; dim];
    for i in 0..dim {
        for j in 0..dim {
            let id = if i == j { 1 } else { 0 };
            px[i][j] = (t2_4[i][j] - 4 * t2_2[i][j] + id).rem_euclid(MOD_Q);
        }
    }

    // Exact rank of P_X(T_2) over F_MOD_Q via Gaussian elimination.
    let mut rk = 0usize;
    for col in 0..dim {
        let mut piv = None;
        for r in rk..dim {
            if px[r][col] != 0 {
                piv = Some(r);
                break;
            }
        }
        let Some(p_row) = piv else { continue };
        px.swap(rk, p_row);
        let inv = mod_inv(px[rk][col], MOD_Q);
        for j in col..dim {
            px[rk][j] = (px[rk][j] * inv) % MOD_Q;
        }
        for r in (rk + 1)..dim {
            let fac = px[r][col];
            if fac != 0 {
                for j in col..dim {
                    px[r][j] = (px[r][j] - fac * px[rk][j]).rem_euclid(MOD_Q);
                }
            }
        }
        rk += 1;
    }
    (dim, rk, tr_t2)
}

fn kronecker_neg4(p: i64) -> i64 {
    if p == 2 {
        0
    } else if p % 4 == 1 {
        1
    } else {
        -1
    }
}

fn kronecker_neg3(p: i64) -> i64 {
    if p == 3 {
        0
    } else if p % 3 == 1 {
        1
    } else {
        -1
    }
}

pub fn verify_shimura_manin_t2() -> ShimuraManinT2Report {
    let odd_primes: Vec<i64> = (3..=1001).step_by(2).filter(|&p| is_prime_i64(p)).collect();
    let mut d_cands: Vec<(i64, i64, i64, i64)> = Vec::new();

    fn gen_d(
        odd_primes: &[i64],
        idx: usize,
        cnt: usize,
        d_val: i64,
        phi_d: i64,
        e2_d: i64,
        e3_d: i64,
        out: &mut Vec<(i64, i64, i64, i64)>,
    ) {
        if cnt >= 2 && cnt % 2 == 0 {
            out.push((d_val, phi_d, e2_d, e3_d));
        }
        for i in idx..odd_primes.len() {
            let p = odd_primes[i];
            if phi_d * (p - 1) > 1000 {
                break;
            }
            gen_d(
                odd_primes,
                i + 1,
                cnt + 1,
                d_val * p,
                phi_d * (p - 1),
                e2_d * (1 - kronecker_neg4(p)),
                e3_d * (1 - kronecker_neg3(p)),
                out,
            );
        }
    }
    gen_d(&odd_primes, 0, 1, 2, 1, 1, 2, &mut d_cands);

    let mut total_pairs = 0usize;
    let mut torsion_free_pairs = 0usize;
    let mut neg_e10_detected = false;
    let mut neg_e10_phi = 0i64;
    let mut neg_e10_e3 = 0i64;
    let mut levels = BTreeSet::new();

    for &(d_val, phi_d, e2_d, e3_d) in &d_cands {
        let max_n = 1000 / phi_d;
        let mut n_val = 1i64;
        while n_val <= max_n {
            if gcd_i64(d_val, n_val) == 1 {
                let mut tmp = n_val;
                let mut psi_n = 1i64;
                let mut e2_n = 1i64;
                let mut e3_n = 1i64;
                let mut p = 3i64;
                while p * p <= tmp {
                    if tmp % p == 0 {
                        let mut k = 0;
                        let mut pk_m1 = 1i64;
                        while tmp % p == 0 {
                            if k >= 1 {
                                pk_m1 *= p;
                            }
                            tmp /= p;
                            k += 1;
                        }
                        psi_n *= pk_m1 * (p + 1);
                        e2_n *= 1 + kronecker_neg4(p);
                        e3_n *= if p == 3 {
                            if k == 1 { 1 } else { 0 }
                        } else {
                            1 + kronecker_neg3(p)
                        };
                    }
                    p += 2;
                }
                if tmp > 1 {
                    psi_n *= tmp + 1;
                    e2_n *= 1 + kronecker_neg4(tmp);
                    e3_n *= if tmp == 3 { 1 } else { 1 + kronecker_neg3(tmp) };
                }
                if phi_d * psi_n <= 1000 {
                    let e2 = e2_d * e2_n;
                    let e3 = e3_d * e3_n;
                    if 12 + phi_d * psi_n - 3 * e2 - 4 * e3 == 12 * 13 {
                        total_pairs += 1;
                        if e2 == 0 && e3 == 0 {
                            torsion_free_pairs += 1;
                        }
                        if d_val == 690 && n_val == 1 {
                            neg_e10_detected = true;
                            neg_e10_phi = phi_d;
                            neg_e10_e3 = e3;
                        }
                        levels.insert((d_val * n_val) / 2);
                    }
                }
            }
            n_val += 2;
        }
    }

    let mut gamma_h_count = 0usize;
    for &(d_val, phi_d, _, _) in &d_cands {
        if 144 % phi_d != 0 {
            continue;
        }
        let mut n_val = 3i64;
        while n_val <= 144 {
            if gcd_i64(d_val, n_val) == 1 {
                let mut tmp = n_val;
                let mut psi_n = 1i64;
                let mut phi_n = 1i64;
                let mut p = 3i64;
                while p * p <= tmp {
                    if tmp % p == 0 {
                        let mut k = 0;
                        let mut pk_m1 = 1i64;
                        while tmp % p == 0 {
                            if k >= 1 {
                                pk_m1 *= p;
                            }
                            tmp /= p;
                            k += 1;
                        }
                        psi_n *= pk_m1 * (p + 1);
                        phi_n *= pk_m1 * (p - 1);
                    }
                    p += 2;
                }
                if tmp > 1 {
                    psi_n *= tmp + 1;
                    phi_n *= tmp - 1;
                }
                if 144 % (phi_d * psi_n) == 0 {
                    let d_idx = 144 / (phi_d * psi_n);
                    if d_idx >= 2 && (phi_n / 2) % d_idx == 0 {
                        gamma_h_count += 1;
                    }
                }
            }
            n_val += 2;
        }
    }

    let mut full_rank_levels = 0usize;
    let mut m345_manin_dim = 0usize;
    let mut m345_px_rank = 0usize;
    let mut m345_tr_t2_mod_q = 0i64;
    for &m_level in &levels {
        let (dim, rk, tr1) = manin_minus_t2_px_rank(m_level);
        if rk == dim && dim > 0 {
            full_rank_levels += 1;
        }
        if m_level == 345 {
            m345_manin_dim = dim;
            m345_px_rank = rk;
            m345_tr_t2_mod_q = tr1;
        }
    }

    let passed = total_pairs == 19
        && torsion_free_pairs == 11
        && neg_e10_detected
        && neg_e10_phi == 176
        && neg_e10_e3 == 8
        && gamma_h_count == 4
        && levels.len() == 18
        && full_rank_levels == levels.len()
        && m345_manin_dim == 45
        && m345_px_rank == 45
        && m345_tr_t2_mod_q == (MOD_Q - 5);

    ShimuraManinT2Report {
        passed,
        total_pairs,
        torsion_free_pairs,
        neg_e10_detected,
        neg_e10_phi,
        neg_e10_e3,
        gamma_h_count,
        distinct_levels_checked: levels.len(),
        full_rank_levels,
        m345_manin_dim,
        m345_px_rank,
        m345_tr_t2_mod_q,
    }
}

// ============================================================================
// 3. Props 7.3, 7.17(b), 7.18(a): Siegel Quadratic Scan & PGL_2(F_8) Census
// ============================================================================

fn sigma1_i64(n: i64) -> i64 {
    let mut s = 0;
    let mut d = 1;
    while d * d <= n {
        if n % d == 0 {
            s += d;
            if d * d != n {
                s += n / d;
            }
        }
        d += 1;
    }
    s
}

fn isqrt_i64(n: i64) -> i64 {
    let mut r = (n as f64).sqrt() as i64;
    while (r + 1) * (r + 1) <= n {
        r += 1;
    }
    while r * r > n {
        r -= 1;
    }
    r
}

fn legendre_p(a: i64, p: i64) -> i64 {
    let x = a.rem_euclid(p);
    if x == 0 {
        return 0;
    }
    let mut res = 1i64;
    let mut e = (p - 1) / 2;
    let mut base = x;
    while e > 0 {
        if e & 1 == 1 {
            res = (res * base) % p;
        }
        base = (base * base) % p;
        e >>= 1;
    }
    if res == p - 1 { -1 } else { res }
}

fn is_fund_disc(d_val: i64) -> bool {
    if d_val <= 1 {
        return false;
    }
    if d_val % 4 == 1 {
        let mut p = 2;
        while p * p <= d_val {
            if d_val % (p * p) == 0 {
                return false;
            }
            p += 1;
        }
        return true;
    }
    if d_val % 4 == 0 {
        let m = d_val / 4;
        if m % 4 != 2 && m % 4 != 3 {
            return false;
        }
        let mut p = 2;
        while p * p <= m {
            if m % (p * p) == 0 {
                return false;
            }
            p += 1;
        }
        return true;
    }
    false
}

fn narrow_class_number_quad(d_val: i64) -> usize {
    let sd = isqrt_i64(d_val);
    let mut forms = BTreeSet::new();
    for b in 1..=sd {
        if (d_val - b * b) % 4 != 0 {
            continue;
        }
        let prod = (d_val - b * b) / 4;
        for d in 1..=prod {
            if prod % d == 0 && sd - b < 2 * d && 2 * d < sd + b {
                let c = prod / d;
                if gcd_i64(gcd_i64(d, b), c) == 1 {
                    forms.insert((d, b, -c));
                    forms.insert((-d, b, c));
                }
            }
        }
    }
    let step = |(_a, b, c): (i64, i64, i64)| -> (i64, i64, i64) {
        let ac = c.abs();
        let b_new = 2 * ac * ((sd + b) / (2 * ac)) - b;
        let c_new = (b_new * b_new - d_val) / (4 * c);
        (c, b_new, c_new)
    };
    let mut visited = BTreeSet::new();
    let mut cycles = 0usize;
    for &f in &forms {
        if visited.contains(&f) {
            continue;
        }
        cycles += 1;
        let mut cur = f;
        while visited.insert(cur) {
            cur = step(cur);
        }
    }
    cycles
}

fn count_quad_dn_solutions(d_val: i64, p_target: i64) -> usize {
    let mut norms = vec![2i64];
    for p in 3..=(p_target + 1) {
        if !is_prime_i64(p) {
            continue;
        }
        match legendre_p(d_val, p) {
            1 => {
                norms.push(p);
                norms.push(p);
            }
            0 => norms.push(p),
            _ => {
                if p * p <= p_target + 1 {
                    norms.push(p * p);
                }
            }
        }
    }
    fn dfs(norms: &[i64], idx: usize, rem: i64, d_cnt: usize, count: &mut usize) {
        if rem == 1 {
            if d_cnt % 2 == 0 {
                *count += 1;
            }
            return;
        }
        if idx == norms.len() {
            return;
        }
        let q = norms[idx];
        dfs(norms, idx + 1, rem, d_cnt, count);
        if q == 2 {
            dfs(norms, idx + 1, rem, d_cnt + 1, count);
        } else if rem % (q - 1) == 0 {
            dfs(norms, idx + 1, rem / (q - 1), d_cnt + 1, count);
        }
        let mut f = q + 1;
        while f <= rem {
            if rem % f == 0 {
                dfs(norms, idx + 1, rem / f, d_cnt, count);
            }
            if f > rem / q {
                break;
            }
            f *= q;
        }
    }
    let mut count = 0usize;
    dfs(&norms, 0, p_target, 0, &mut count);
    count
}

#[inline]
fn f8_mul(a: u8, b: u8) -> u8 {
    let mut p = 0u8;
    for i in 0..3 {
        if (b & (1 << i)) != 0 {
            p ^= a << i;
        }
    }
    if (p & 16) != 0 {
        p ^= 0b1011 << 1;
    }
    if (p & 8) != 0 {
        p ^= 0b1011;
    }
    p & 7
}

#[inline]
fn f8_inv(a: u8) -> u8 {
    let a2 = f8_mul(a, a);
    let a4 = f8_mul(a2, a2);
    f8_mul(a2, a4)
}

#[derive(Clone, Copy)]
struct F8Mat(u8, u8, u8, u8);

#[inline]
fn f8_mat_mul(x: F8Mat, y: F8Mat) -> F8Mat {
    F8Mat(
        f8_mul(x.0, y.0) ^ f8_mul(x.1, y.2),
        f8_mul(x.0, y.1) ^ f8_mul(x.1, y.3),
        f8_mul(x.2, y.0) ^ f8_mul(x.3, y.2),
        f8_mul(x.2, y.1) ^ f8_mul(x.3, y.3),
    )
}

#[inline]
fn f8_is_scalar(m: F8Mat) -> bool {
    m.1 == 0 && m.2 == 0 && m.0 == m.3 && m.0 != 0
}

#[inline]
fn f8_p1_act(m: F8Mat, pt: usize) -> usize {
    let (num, den) = if pt == 8 {
        (m.0, m.2)
    } else {
        let x = pt as u8;
        (f8_mul(m.0, x) ^ m.1, f8_mul(m.2, x) ^ m.3)
    };
    if den == 0 {
        8
    } else {
        f8_mul(num, f8_inv(den)) as usize
    }
}

pub fn verify_section7_arithmetic_cycle5() -> Section7ArithmeticCycle5Report {
    let mut quad_split2_scanned = 0usize;
    let mut quad_hplus1_solutions = 0usize;
    let mut quad_d41_solutions = 0usize;
    let mut quad_d137_solutions = 0usize;

    for d_val in 5..=1200 {
        if !is_fund_disc(d_val) || d_val % 8 != 1 {
            continue;
        }
        quad_split2_scanned += 1;
        let mut z60 = 0i64;
        let mut b = 1i64;
        while b * b < d_val {
            z60 += 2 * sigma1_i64((d_val - b * b) / 4);
            b += 2;
        }
        if 1440 % z60 != 0 {
            continue;
        }
        if narrow_class_number_quad(d_val) != 1 {
            continue;
        }
        let sols = count_quad_dn_solutions(d_val, 1440 / z60);
        quad_hplus1_solutions += sols;
        if d_val == 41 {
            quad_d41_solutions = sols;
        }
        if d_val == 137 {
            quad_d137_solutions = sols;
        }
    }

    let mut pgl2_f8_order = 0usize;
    let mut pgl2_f8_order3_count = 0usize;
    let mut pgl2_f8_order3_free_count = 0usize;
    for a in 0..8u8 {
        for b in 0..8u8 {
            for c in 0..8u8 {
                for d in 0..8u8 {
                    if (f8_mul(a, d) ^ f8_mul(b, c)) == 0 {
                        continue;
                    }
                    let lead = if a != 0 {
                        a
                    } else if b != 0 {
                        b
                    } else if c != 0 {
                        c
                    } else {
                        d
                    };
                    if lead != 1 {
                        continue;
                    }
                    pgl2_f8_order += 1;
                    let m = F8Mat(a, b, c, d);
                    if f8_is_scalar(m) {
                        continue;
                    }
                    let m2 = f8_mat_mul(m, m);
                    let m3 = f8_mat_mul(m2, m);
                    if f8_is_scalar(m3) {
                        pgl2_f8_order3_count += 1;
                        if (0..9).all(|pt| f8_p1_act(m, pt) != pt) {
                            pgl2_f8_order3_free_count += 1;
                        }
                    }
                }
            }
        }
    }

    let mut t_prev2: i128 = 2;
    let mut t_prev1: i128 = 85;
    let mut det_k: i128 = 256;
    let mut sdet_k: i128 = 16;
    let mut gamma0_powers_obstructed = 0usize;
    for k in 1..=12 {
        let tk = if k == 1 {
            t_prev1
        } else {
            85 * t_prev1 - 256 * t_prev2
        };
        if k >= 2 {
            t_prev2 = t_prev1;
            t_prev1 = tk;
            det_k *= 256;
            sdet_k *= 16;
        }
        let mut ok = tk > 2 * sdet_k;
        if k <= 9 {
            ok = ok && (tk * tk > 4 * det_k);
        }
        if ok {
            gamma0_powers_obstructed += 1;
        }
    }

    let passed = quad_hplus1_solutions == 3
        && quad_d41_solutions == 2
        && quad_d137_solutions == 1
        && pgl2_f8_order == 504
        && pgl2_f8_order3_count == 56
        && pgl2_f8_order3_free_count == 56
        && gamma0_powers_obstructed == 12;

    Section7ArithmeticCycle5Report {
        passed,
        quad_split2_scanned,
        quad_hplus1_solutions,
        quad_d41_solutions,
        quad_d137_solutions,
        pgl2_f8_order,
        pgl2_f8_order3_count,
        pgl2_f8_order3_free_count,
        gamma0_powers_obstructed,
    }
}
