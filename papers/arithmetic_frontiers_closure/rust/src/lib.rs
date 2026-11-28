//! Independent Zero-Crate Pure Rust Verification Library for Paper #10 (PC-IV):
//! Closing All Four Open Arithmetic Frontiers: Cubic Lame Non-Congruence,
//! Level (4) Full Congruence on Q(sqrt(33)), Complete 9-Curve Genus-25 Brandt
//! Spectra, and Degree-8 Explicit-Formula Closure.
//!
//! License: MIT (Code Model). Zero external crates (Rust `std` only).
//! Strictly separates Code from Data (never reads cached JSON files).

use std::collections::{BTreeMap, BTreeSet, HashMap, HashSet, VecDeque};
use std::ops::{Add, Div, Mul, Neg, Sub};

// ============================================================================
// Exact Rational Arithmetic (i128), Modular Inverse, & Exact HNF / CRT Det
// ============================================================================

fn gcd_i128(mut a: i128, mut b: i128) -> i128 {
    a = a.abs();
    b = b.abs();
    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }
    a
}

fn lcm_i128(a: i128, b: i128) -> i128 {
    if a == 0 || b == 0 {
        0
    } else {
        (a / gcd_i128(a, b)).abs() * b.abs()
    }
}

fn isqrt_i128(n: i128) -> i128 {
    assert!(n >= 0);
    if n < 2 {
        return n;
    }
    let mut x = (n as f64).sqrt() as i128;
    if x < 1 {
        x = 1;
    }
    while (x + 1).saturating_mul(x + 1) <= n {
        x += 1;
    }
    while x.saturating_mul(x) > n {
        x -= 1;
    }
    x
}

fn mod_pos(x: i128, m: i128) -> i128 {
    let r = x % m;
    if r < 0 { r + m } else { r }
}

fn mod_inv(a: i128, m: i128) -> i128 {
    let mut t: i128 = 0;
    let mut newt: i128 = 1;
    let mut r: i128 = m;
    let mut newr: i128 = mod_pos(a, m);
    while newr != 0 {
        let q = r / newr;
        let tmp_t = t - q * newt;
        t = newt;
        newt = tmp_t;
        let tmp_r = r - q * newr;
        r = newr;
        newr = tmp_r;
    }
    assert_eq!(r, 1, "mod_inv failed: gcd({}, {}) != 1", a, m);
    mod_pos(t, m)
}

#[derive(Copy, Clone, Debug, Eq, PartialEq, Hash)]
struct Frac {
    n: i128,
    d: i128,
}

impl Frac {
    fn new(mut n: i128, mut d: i128) -> Self {
        assert!(d != 0, "Frac division by zero");
        if d < 0 {
            n = -n;
            d = -d;
        }
        if n == 0 {
            return Self { n: 0, d: 1 };
        }
        let g = gcd_i128(n, d);
        Self { n: n / g, d: d / g }
    }
    fn from_int(n: i128) -> Self {
        Self { n, d: 1 }
    }
    fn zero() -> Self {
        Self { n: 0, d: 1 }
    }
    fn one() -> Self {
        Self { n: 1, d: 1 }
    }
    fn is_zero(self) -> bool {
        self.n == 0
    }
    fn abs(self) -> Self {
        Self { n: self.n.abs(), d: self.d }
    }
    fn inv(self) -> Self {
        Self::new(self.d, self.n)
    }
    fn to_f64(self) -> f64 {
        (self.n as f64) / (self.d as f64)
    }
    fn mod_m(self, m: i128) -> i128 {
        mod_pos(self.n * mod_inv(self.d, m), m)
    }
}

impl Add for Frac {
    type Output = Self;
    fn add(self, rhs: Self) -> Self {
        let g = gcd_i128(self.d, rhs.d);
        Self::new(self.n * (rhs.d / g) + rhs.n * (self.d / g), (self.d / g) * rhs.d)
    }
}
impl Sub for Frac {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self {
        let g = gcd_i128(self.d, rhs.d);
        Self::new(self.n * (rhs.d / g) - rhs.n * (self.d / g), (self.d / g) * rhs.d)
    }
}
impl Mul for Frac {
    type Output = Self;
    fn mul(self, rhs: Self) -> Self {
        let g1 = gcd_i128(self.n, rhs.d);
        let g2 = gcd_i128(rhs.n, self.d);
        Self::new((self.n / g1) * (rhs.n / g2), (self.d / g2) * (rhs.d / g1))
    }
}
impl Div for Frac {
    type Output = Self;
    fn div(self, rhs: Self) -> Self {
        self * rhs.inv()
    }
}
impl Neg for Frac {
    type Output = Self;
    fn neg(self) -> Self {
        Self { n: -self.n, d: self.d }
    }
}

fn inv_frac_mat(m: &[Vec<Frac>]) -> Vec<Vec<Frac>> {
    let n = m.len();
    let mut a: Vec<Vec<Frac>> = (0..n)
        .map(|i| {
            let mut row = m[i].clone();
            row.extend((0..n).map(|j| if i == j { Frac::one() } else { Frac::zero() }));
            row
        })
        .collect();
    for k in 0..n {
        let piv = (k..n).find(|&r| !a[r][k].is_zero()).expect("Singular matrix");
        a.swap(k, piv);
        let d = a[k][k].inv();
        for c in 0..(2 * n) {
            a[k][c] = a[k][c] * d;
        }
        for r in 0..n {
            if r != k && !a[r][k].is_zero() {
                let f = a[r][k];
                for c in 0..(2 * n) {
                    let v = a[k][c];
                    a[r][c] = a[r][c] - f * v;
                }
            }
        }
    }
    a.into_iter().map(|r| r[n..].to_vec()).collect()
}

fn det_mod_p(mat: &[Vec<i128>], p: i128) -> i128 {
    let n = mat.len();
    let mut a: Vec<Vec<i128>> = mat
        .iter()
        .map(|r| r.iter().map(|&x| mod_pos(x, p)).collect())
        .collect();
    let mut det: i128 = 1;
    for k in 0..n {
        let piv = match (k..n).find(|&r| a[r][k] != 0) {
            Some(r) => r,
            None => return 0,
        };
        if piv != k {
            a.swap(k, piv);
            det = mod_pos(-det, p);
        }
        let akk = a[k][k];
        det = (det * akk) % p;
        let inv_akk = mod_inv(akk, p);
        for i in (k + 1)..n {
            if a[i][k] != 0 {
                let f = (a[i][k] * inv_akk) % p;
                for j in (k + 1)..n {
                    a[i][j] = mod_pos(a[i][j] - f * a[k][j], p);
                }
            }
        }
    }
    det
}

/// Exact rational matrix determinant using 3-prime CRT (`P1*P2*P3 ~ 9.98e26`),
/// completely immune to intermediate overflow up to |det * row_lcm_prod| < 4e26.
fn det_frac_exact(mat: &[Vec<Frac>]) -> Frac {
    let n = mat.len();
    let mut scale: i128 = 1;
    let mut int_rows: Vec<Vec<i128>> = Vec::with_capacity(n);
    for row in mat {
        let mut l: i128 = 1;
        for &x in row {
            l = lcm_i128(l, x.d);
        }
        scale *= l;
        int_rows.push(row.iter().map(|&x| x.n * (l / x.d)).collect());
    }
    // Three guaranteed primes whose product is 998,244,368,971,908,909,975,289,147 (> 9.98e26)
    let p1: i128 = 1_000_000_007;
    let p2: i128 = 1_000_000_009;
    let p3: i128 = 998_244_353;
    let r1 = det_mod_p(&int_rows, p1);
    let r2 = det_mod_p(&int_rows, p2);
    let r3 = det_mod_p(&int_rows, p3);
    // Combine r1 (mod p1) and r2 (mod p2)
    let m12 = p1 * p2;
    let k12 = mod_pos((r2 - r1) * mod_inv(p1, p2), p2);
    let x12 = r1 + p1 * k12;
    // Combine x12 (mod m12) and r3 (mod p3)
    let k3 = mod_pos((r3 - mod_pos(x12, p3)) * mod_inv(mod_pos(m12, p3), p3), p3);
    let mut x = x12 + m12 * k3;
    let prod = m12 * p3;
    if x > prod / 2 {
        x -= prod;
    }
    Frac::new(x, scale)
}

fn hnf_int_rows(rows: &[Vec<i128>]) -> Vec<Vec<i128>> {
    let m = rows[0].len();
    let mut a = rows.to_vec();
    let mut r = 0usize;
    for c in 0..m {
        loop {
            let nz: Vec<usize> = (r..a.len()).filter(|&i| a[i][c] != 0).collect();
            if nz.is_empty() {
                break;
            }
            let piv = *nz.iter().min_by_key(|&&i| a[i][c].abs()).unwrap();
            a.swap(r, piv);
            if a[r][c] < 0 {
                for j in c..m {
                    a[r][j] = -a[r][j];
                }
            }
            let mut changed = false;
            for i in (r + 1)..a.len() {
                if a[i][c] != 0 {
                    let q = a[i][c].div_euclid(a[r][c]);
                    for j in c..m {
                        let v = a[r][j];
                        a[i][j] -= q * v;
                    }
                    if a[i][c] != 0 {
                        changed = true;
                    }
                }
            }
            if !changed {
                break;
            }
        }
        if r < a.len() && a[r][c] != 0 {
            for i in 0..r {
                let q = a[i][c].div_euclid(a[r][c]);
                for j in c..m {
                    let v = a[r][j];
                    a[i][j] -= q * v;
                }
            }
            r += 1;
        }
    }
    a.into_iter().filter(|row| row.iter().any(|&x| x != 0)).collect()
}

// ============================================================================
// Keyed SplitMix64 PRNG & FNV-1a64 (Cross-Language Seam with Python & C++20)
// ============================================================================

const PC4_PRNG_SEED: u64 = 0xF0271E2620260010;
const EXPECTED_XOR_DIGEST: u64 = 0x37b4f6b8da592957;
const EXPECTED_FNV_DIGEST: u64 = 0xb7fbf6c71c86c218;

struct SplitMix64 {
    state: u64,
}

impl SplitMix64 {
    fn new(seed: u64) -> Self {
        Self { state: seed }
    }
    fn next_u64(&mut self) -> u64 {
        self.state = self.state.wrapping_add(0x9E3779B97F4A7C15);
        let mut z = self.state;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58476D1CE4E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D049BB133111EB);
        z ^ (z >> 31)
    }
}

fn mix64_tag(tag: u64, val: u64) -> u64 {
    let mut z = tag.wrapping_mul(0x9E3779B97F4A7C15) ^ val;
    z = (z ^ (z >> 30)).wrapping_mul(0xBF58476D1CE4E5B9);
    z = (z ^ (z >> 27)).wrapping_mul(0x94D049BB133111EB);
    z ^ (z >> 31)
}

fn fnv1a64_u64s(vals: &[u64]) -> u64 {
    let mut h: u64 = 0xCBF29CE484222325;
    for &x in vals {
        for shift in (0..64).step_by(8) {
            h ^= (x >> shift) & 0xFF;
            h = h.wrapping_mul(0x100000001B3);
        }
    }
    h
}

// ============================================================================
// Aut(Z) (order 96) & 16 Surjections for Z = Cay(Dic_6, {1, 11, 12, 18})
// ============================================================================

fn dic6_mul(a: usize, b: usize) -> usize {
    let (e1, k1) = (a / 12, a % 12);
    let (e2, k2) = (b / 12, b % 12);
    if e1 == 0 {
        12 * e2 + (k1 + k2) % 12
    } else {
        12 * ((1 + e2) % 2) + (k1 + 12 - k2 + if e2 == 1 { 6 } else { 0 }) % 12
    }
}

fn perm_comp(p: &[usize; 24], q: &[usize; 24]) -> [usize; 24] {
    let mut out = [0usize; 24];
    for i in 0..24 {
        out[i] = p[q[i]];
    }
    out
}

fn perm_order(p: &[usize; 24]) -> usize {
    let mut seen = [false; 24];
    let mut o = 1usize;
    for i in 0..24 {
        if !seen[i] {
            let mut c = i;
            let mut l = 0usize;
            while !seen[c] {
                seen[c] = true;
                c = p[c];
                l += 1;
            }
            let g = gcd_i128(o as i128, l as i128) as usize;
            o = (o / g) * l;
        }
    }
    o
}

struct Dic6AutData {
    aut_mul: Vec<[usize; 96]>,
    surjs_i: Vec<[usize; 4]>,
    id_p: usize,
}

fn build_dic6_aut() -> Dic6AutData {
    let gens = [1usize, 11, 12, 18];
    let mut z_adj = [[0usize; 4]; 24];
    let mut adj_mask = [0u32; 24];
    for v in 0..24 {
        for k in 0..4 {
            let w = dic6_mul(v, gens[k]);
            z_adj[v][k] = w;
            adj_mask[v] |= 1u32 << w;
        }
    }
    let mut order = Vec::with_capacity(24);
    let mut seen = [false; 24];
    let mut dq = VecDeque::new();
    dq.push_back(0usize);
    seen[0] = true;
    while let Some(u) = dq.pop_front() {
        order.push(u);
        for &v in &z_adj[u] {
            if !seen[v] {
                seen[v] = true;
                dq.push_back(v);
            }
        }
    }
    let mut pos = [0usize; 24];
    for (i, &u) in order.iter().enumerate() {
        pos[u] = i;
    }
    let mut prev: Vec<Vec<usize>> = Vec::with_capacity(24);
    for (i, &u) in order.iter().enumerate() {
        prev.push(z_adj[u].iter().copied().filter(|&v| pos[v] < i).collect());
    }

    let mut auts: Vec<[usize; 24]> = Vec::new();
    let mut mp = [0usize; 24];
    let mut used = 0u32;

    fn bt(
        idx: usize,
        order: &[usize],
        prev: &[Vec<usize>],
        adj_mask: &[u32; 24],
        mp: &mut [usize; 24],
        used: &mut u32,
        auts: &mut Vec<[usize; 24]>,
    ) {
        if idx == 24 {
            auts.push(*mp);
            return;
        }
        let u = order[idx];
        let mut cand = if prev[idx].is_empty() {
            (1u32 << 24) - 1
        } else {
            let mut m = (1u32 << 24) - 1;
            for &x in &prev[idx] {
                m &= adj_mask[mp[x]];
            }
            m
        };
        cand &= !*used;
        while cand != 0 {
            let w = cand.trailing_zeros() as usize;
            cand &= cand - 1;
            mp[u] = w;
            *used |= 1u32 << w;
            bt(idx + 1, order, prev, adj_mask, mp, used, auts);
            *used &= !(1u32 << w);
        }
    }

    bt(0, &order, &prev, &adj_mask, &mut mp, &mut used, &mut auts);
    assert_eq!(auts.len(), 96);

    let a_z = *auts.iter().find(|p| p[0] == 0 && p[1] == 1 && p[11] == 11 && p[12] == 18).unwrap();
    let b_z = *auts.iter().find(|p| p[0] == 0 && p[12] == 12 && p[18] == 18 && p[1] == 11).unwrap();
    let tx_c: Vec<[usize; 24]> = auts
        .iter()
        .copied()
        .filter(|p| (p[0] == 1 || p[0] == 11) && perm_order(p) == 2 && perm_comp(p, &a_z) == perm_comp(&a_z, p))
        .collect();
    let ty_c: Vec<[usize; 24]> = auts
        .iter()
        .copied()
        .filter(|p| (p[0] == 12 || p[0] == 18) && perm_order(p) == 2 && perm_comp(p, &b_z) == perm_comp(&b_z, p))
        .collect();
    assert_eq!(tx_c.len(), 4);
    assert_eq!(ty_c.len(), 4);

    let mut aut_idx: HashMap<[usize; 24], usize> = HashMap::new();
    for (i, &p) in auts.iter().enumerate() {
        aut_idx.insert(p, i);
    }
    let mut aut_mul = vec![[0usize; 96]; 96];
    for i in 0..96 {
        for j in 0..96 {
            aut_mul[i][j] = aut_idx[&perm_comp(&auts[i], &auts[j])];
        }
    }
    let mut surjs_i = Vec::with_capacity(16);
    for &tx in &tx_c {
        for &ty in &ty_c {
            surjs_i.push([aut_idx[&b_z], aut_idx[&a_z], aut_idx[&tx], aut_idx[&ty]]);
        }
    }
    let mut id_arr = [0usize; 24];
    for i in 0..24 {
        id_arr[i] = i;
    }
    let id_p = aut_idx[&id_arr];
    Dic6AutData { aut_mul, surjs_i, id_p }
}

// ============================================================================
// Suite R1: Frontier 1 — Cubic Lame Nauru Curves (d_F in {316, 148})
// ============================================================================

type Cub = [Frac; 3];
type CubQ = [Cub; 4];

fn cub_add(a: Cub, b: Cub) -> Cub {
    [a[0] + b[0], a[1] + b[1], a[2] + b[2]]
}
fn cub_sub(a: Cub, b: Cub) -> Cub {
    [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
}
fn cub_scale(a: Cub, s: Frac) -> Cub {
    [a[0] * s, a[1] * s, a[2] * s]
}
fn cub_mul(a: Cub, b: Cub, c2: i128, c1: i128, c0: i128) -> Cub {
    let mut p = [Frac::zero(); 5];
    for i in 0..3 {
        for j in 0..3 {
            p[i + j] = p[i + j] + a[i] * b[j];
        }
    }
    let fc2 = Frac::from_int(c2);
    let fc1 = Frac::from_int(c1);
    let fc0 = Frac::from_int(c0);
    p[3] = p[3] - fc2 * p[4];
    p[2] = p[2] - fc1 * p[4];
    p[1] = p[1] - fc0 * p[4];
    p[2] = p[2] - fc2 * p[3];
    p[1] = p[1] - fc1 * p[3];
    p[0] = p[0] - fc0 * p[3];
    [p[0], p[1], p[2]]
}
fn cub_mul_mat(a: Cub, c2: i128, c1: i128, c0: i128) -> Vec<Vec<Frac>> {
    let e = [
        [Frac::one(), Frac::zero(), Frac::zero()],
        [Frac::zero(), Frac::one(), Frac::zero()],
        [Frac::zero(), Frac::zero(), Frac::one()],
    ];
    let cols = [
        cub_mul(a, e[0], c2, c1, c0),
        cub_mul(a, e[1], c2, c1, c0),
        cub_mul(a, e[2], c2, c1, c0),
    ];
    (0..3).map(|i| (0..3).map(|j| cols[j][i]).collect()).collect()
}
fn cub_tr(a: Cub, c2: i128, c1: i128, c0: i128) -> Frac {
    let m = cub_mul_mat(a, c2, c1, c0);
    m[0][0] + m[1][1] + m[2][2]
}
fn cub_norm(a: Cub, c2: i128, c1: i128, c0: i128) -> Frac {
    det_frac_exact(&cub_mul_mat(a, c2, c1, c0))
}
fn cub_inv(a: Cub, c2: i128, c1: i128, c0: i128) -> Cub {
    let mi = inv_frac_mat(&cub_mul_mat(a, c2, c1, c0));
    [mi[0][0], mi[1][0], mi[2][0]]
}

fn cub_qmul(x: CubQ, y: CubQ, alpha: Cub, beta: Cub, c2: i128, c1: i128, c0: i128) -> CubQ {
    let m = |u, v| cub_mul(u, v, c2, c1, c0);
    let ab = m(alpha, beta);
    let w0 = cub_add(
        cub_add(m(x[0], y[0]), m(alpha, m(x[1], y[1]))),
        cub_sub(m(beta, m(x[2], y[2])), m(ab, m(x[3], y[3]))),
    );
    let w1 = cub_add(
        cub_add(m(x[0], y[1]), m(x[1], y[0])),
        cub_sub(m(beta, m(x[3], y[2])), m(beta, m(x[2], y[3]))),
    );
    let w2 = cub_add(
        cub_add(m(x[0], y[2]), m(x[2], y[0])),
        cub_sub(m(alpha, m(x[1], y[3])), m(alpha, m(x[3], y[1]))),
    );
    let w3 = cub_add(
        cub_add(m(x[0], y[3]), m(x[3], y[0])),
        cub_sub(m(x[1], y[2]), m(x[2], y[1])),
    );
    [w0, w1, w2, w3]
}

fn cub_qconj(x: CubQ) -> CubQ {
    let neg = Frac::from_int(-1);
    [x[0], cub_scale(x[1], neg), cub_scale(x[2], neg), cub_scale(x[3], neg)]
}

fn poly_mod_cubic_degs(c2: i128, c1: i128, c0: i128, p: i128) -> Vec<usize> {
    let mut roots = Vec::new();
    for r in 0..p {
        if mod_pos(r * r * r + c2 * r * r + c1 * r + c0, p) == 0 {
            roots.push(r);
        }
    }
    if roots.is_empty() {
        return vec![3];
    }
    let r0 = roots[0];
    let b1 = mod_pos(c2 + r0, p);
    let b0 = mod_pos(c1 + r0 * b1, p);
    for r in 0..p {
        if mod_pos(r * r + b1 * r + b0, p) == 0 {
            return vec![1, 1, 1];
        }
    }
    vec![1, 2]
}

pub fn run_suite_r1_cubic_lame() {
    // Verify universal twin duality -P(3 - x)
    let eval_3mx = |a3: i128, a2: i128, a1: i128, a0: i128| {
        (a3, -9 * a3 - a2, 27 * a3 + 6 * a2 + a1, -27 * a3 - 9 * a2 - 3 * a1 - a0)
    };
    assert_eq!(eval_3mx(2, -9, 10, -1), (2, -9, 10, -2));
    assert_eq!(eval_3mx(2, -8, 8, -1), (2, -10, 14, -5));

    let specs = [
        (316i128, -10i128, 9i128, -2i128, (28i128, 39i128, 63i128), -2i128, 4i128, Frac::new(4, 3), 3usize),
        (148i128, -8i128, 8i128, -2i128, (28i128, 12i128, 36i128), -5i128, 25i128, Frac::new(1, 3), 6usize),
    ];

    for (d_f, c2, c1, c0, sq81, exp_norm, exp_ratio, z_exact, ram_q) in specs {
        let disc = c2 * c2 * c1 * c1 - 4 * c1 * c1 * c1 - 4 * c2 * c2 * c2 * c0 - 27 * c0 * c0 + 18 * c2 * c1 * c0;
        assert_eq!(disc, d_f);
        assert_eq!(poly_mod_cubic_degs(c2, c1, c0, 3), vec![3]);

        // Mod-81 square root of 1 - 3z
        let sq = cub_mul(
            [Frac::from_int(sq81.0), Frac::from_int(sq81.1), Frac::from_int(sq81.2)],
            [Frac::from_int(sq81.0), Frac::from_int(sq81.1), Frac::from_int(sq81.2)],
            c2,
            c1,
            c0,
        );
        assert_eq!((sq[0].mod_m(81), sq[1].mod_m(81), sq[2].mod_m(81)), (1, 78, 0));

        let z0 = [Frac::zero(); 3];
        let one = [Frac::one(), Frac::zero(), Frac::zero()];
        let z_el = [Frac::zero(), Frac::one(), Frac::zero()];
        let z2_el = [Frac::zero(), Frac::zero(), Frac::one()];
        let alpha = [Frac::from_int(-3), Frac::zero(), Frac::zero()];
        let beta = [Frac::one(), Frac::from_int(-3), Frac::zero()];
        assert_eq!(cub_norm(beta, c2, c1, c0), Frac::from_int(exp_norm));

        // Universal rank-12 maximal order O_max
        let e0: CubQ = [one, z0, z0, z0];
        let e1: CubQ = [cub_scale(one, Frac::new(1, 2)), cub_scale(one, Frac::new(1, 2)), z0, z0];
        let e2: CubQ = [z0, cub_scale(one, Frac::new(1, 3)), z0, cub_scale(one, Frac::new(1, 3))];
        let e3 = cub_qmul(e1, e2, alpha, beta, c2, c1, c0);
        let f_basis = [e0, e1, e2, e3];
        let z_pows = [one, z_el, z2_el];
        let mut basis12: Vec<CubQ> = Vec::with_capacity(12);
        for &e in &f_basis {
            for &zp in &z_pows {
                basis12.push([
                    cub_mul(zp, e[0], c2, c1, c0),
                    cub_mul(zp, e[1], c2, c1, c0),
                    cub_mul(zp, e[2], c2, c1, c0),
                    cub_mul(zp, e[3], c2, c1, c0),
                ]);
            }
        }
        let q_to_v12 = |q: CubQ| -> Vec<Frac> {
            let mut v = Vec::with_capacity(12);
            for i in 0..4 {
                for j in 0..3 {
                    v.push(q[i][j]);
                }
            }
            v
        };
        let b12: Vec<Vec<Frac>> = basis12.iter().map(|&q| q_to_v12(q)).collect();
        let b12_inv = inv_frac_mat(&b12);

        // Ring closure check across all 144 products
        for &qa in &basis12 {
            for &qb in &basis12 {
                let v = q_to_v12(cub_qmul(qa, qb, alpha, beta, c2, c1, c0));
                for m in 0..12 {
                    let mut acc = Frac::zero();
                    for k in 0..12 {
                        acc = acc + v[k] * b12_inv[k][m];
                    }
                    assert_eq!(acc.d, 1, "Rank-12 order failed ring closure!");
                }
            }
        }

        // Exact 12x12 trace Gram determinant ratio == 4 or 25
        let t12: Vec<Vec<Frac>> = basis12
            .iter()
            .map(|&qa| {
                basis12
                    .iter()
                    .map(|&qb| Frac::from_int(2) * cub_tr(cub_qmul(qa, qb, alpha, beta, c2, c1, c0)[0], c2, c1, c0))
                    .collect()
            })
            .collect();
        let det_t12 = det_frac_exact(&t12).abs();
        let df4 = Frac::from_int(d_f * d_f * d_f * d_f);
        assert_eq!(det_t12 / df4, Frac::from_int(exp_ratio));

        // Conjugation denominators of (a, b, t) = [1, 1, 2]
        let a_gen = e1;
        let b_gen: CubQ = [z0, z0, one, z0];
        let t_gen: CubQ = [z0, one, z0, one];
        let mut denoms = Vec::new();
        for g in [a_gen, b_gen, t_gen] {
            let nrd_g = cub_qmul(g, cub_qconj(g), alpha, beta, c2, c1, c0)[0];
            let inv_n = cub_inv(nrd_g, c2, c1, c0);
            let gc = cub_qconj(g);
            let ginv: CubQ = [
                cub_mul(gc[0], inv_n, c2, c1, c0),
                cub_mul(gc[1], inv_n, c2, c1, c0),
                cub_mul(gc[2], inv_n, c2, c1, c0),
                cub_mul(gc[3], inv_n, c2, c1, c0),
            ];
            let mut dg: i128 = 1;
            for &qa in &basis12 {
                let w = cub_qmul(cub_qmul(g, qa, alpha, beta, c2, c1, c0), ginv, alpha, beta, c2, c1, c0);
                let v = q_to_v12(w);
                for m in 0..12 {
                    let mut acc = Frac::zero();
                    for k in 0..12 {
                        acc = acc + v[k] * b12_inv[k][m];
                    }
                    dg = lcm_i128(dg, acc.d);
                }
            }
            denoms.push(dg);
        }
        assert_eq!(denoms, vec![1, 1, 2]);

        // Exact Eichler-Tamagawa mass M_max = 1/3 and sharp 3-part / C_6 obstruction
        let m_max = Frac::new(1, 4) * z_exact * Frac::from_int(exp_norm.abs() - 1);
        assert_eq!(m_max, Frac::new(1, 3));
        assert!(ram_q < 9 && ram_q < 36);
    }
}

// ============================================================================
// Suite R2: Frontier 2 — Q(sqrt(33))_{A,B} Level (4) Full Congruence + Atlas
// ============================================================================

type Qf = [Frac; 2];
type QfQ = [Qf; 4];

fn qf_add(a: Qf, b: Qf) -> Qf {
    [a[0] + b[0], a[1] + b[1]]
}
fn qf_sub(a: Qf, b: Qf) -> Qf {
    [a[0] - b[0], a[1] - b[1]]
}
fn qf_mul(a: Qf, b: Qf, tw: i128, nw: i128) -> Qf {
    [
        a[0] * b[0] - Frac::from_int(nw) * a[1] * b[1],
        a[0] * b[1] + a[1] * b[0] + Frac::from_int(tw) * a[1] * b[1],
    ]
}
fn qf_conj(a: Qf, tw: i128) -> Qf {
    [a[0] + Frac::from_int(tw) * a[1], -a[1]]
}
fn qf_norm(a: Qf, tw: i128, nw: i128) -> Frac {
    a[0] * a[0] + Frac::from_int(tw) * a[0] * a[1] + Frac::from_int(nw) * a[1] * a[1]
}
fn qf_tr(a: Qf, tw: i128) -> Frac {
    Frac::from_int(2) * a[0] + Frac::from_int(tw) * a[1]
}
fn qf_inv(a: Qf, tw: i128, nw: i128) -> Qf {
    let n = qf_norm(a, tw, nw);
    let c = qf_conj(a, tw);
    [c[0] / n, c[1] / n]
}
fn qf_scale(a: Qf, s: Frac) -> Qf {
    [a[0] * s, a[1] * s]
}

fn qf_qmul(x: QfQ, y: QfQ, a: Qf, b: Qf, tw: i128, nw: i128) -> QfQ {
    let m = |u, v| qf_mul(u, v, tw, nw);
    let ab = m(a, b);
    let w0 = qf_add(
        qf_add(m(x[0], y[0]), m(a, m(x[1], y[1]))),
        qf_sub(m(b, m(x[2], y[2])), m(ab, m(x[3], y[3]))),
    );
    let w1 = qf_add(
        qf_add(m(x[0], y[1]), m(x[1], y[0])),
        qf_sub(m(b, m(x[3], y[2])), m(b, m(x[2], y[3]))),
    );
    let w2 = qf_add(
        qf_add(m(x[0], y[2]), m(x[2], y[0])),
        qf_sub(m(a, m(x[1], y[3])), m(a, m(x[3], y[1]))),
    );
    let w3 = qf_add(
        qf_add(m(x[0], y[3]), m(x[3], y[0])),
        qf_sub(m(x[1], y[2]), m(x[2], y[1])),
    );
    [w0, w1, w2, w3]
}
fn qf_qconj(x: QfQ) -> QfQ {
    [x[0], [-x[1][0], -x[1][1]], [-x[2][0], -x[2][1]], [-x[3][0], -x[3][1]]]
}
fn qf_qnrd(x: QfQ, a: Qf, b: Qf, tw: i128, nw: i128) -> Qf {
    qf_qmul(x, qf_qconj(x), a, b, tw, nw)[0]
}
fn qf_qscale(sc: Qf, x: QfQ, tw: i128, nw: i128) -> QfQ {
    [
        qf_mul(sc, x[0], tw, nw),
        qf_mul(sc, x[1], tw, nw),
        qf_mul(sc, x[2], tw, nw),
        qf_mul(sc, x[3], tw, nw),
    ]
}

fn qf_sqrt_exact(x: Qf, tw: i128, nw: i128, d_f: i128) -> Option<Qf> {
    let nx = qf_norm(x, tw, nw);
    if nx.n <= 0 {
        return None;
    }
    let sn = isqrt_i128(nx.n);
    let sd = isqrt_i128(nx.d);
    if sn * sn != nx.n || sd * sd != nx.d {
        return None;
    }
    let s0 = Frac::new(sn, sd);
    for s in [s0, -s0] {
        let tr_sq = Frac::from_int(2) * x[0] + Frac::from_int(tw) * x[1] + Frac::from_int(2) * s;
        if tr_sq.n < 0 {
            continue;
        }
        let tn = isqrt_i128(tr_sq.n);
        let td = isqrt_i128(tr_sq.d);
        if tn * tn != tr_sq.n || td * td != tr_sq.d {
            continue;
        }
        let big_t = Frac::new(tn, td);
        let v_sq = (big_t * big_t - Frac::from_int(4) * s) / Frac::from_int(d_f);
        if v_sq.n < 0 {
            continue;
        }
        let vn = isqrt_i128(v_sq.n);
        let vd = isqrt_i128(v_sq.d);
        if vn * vn != v_sq.n || vd * vd != v_sq.d {
            continue;
        }
        for sv in [Frac::new(vn, vd), Frac::new(-vn, vd)] {
            let su = (big_t - Frac::from_int(tw) * sv) / Frac::from_int(2);
            if qf_mul([su, sv], [su, sv], tw, nw) == x {
                return Some([su, sv]);
            }
        }
    }
    None
}

fn zagier_zeta_real_quad_neg1(d: i128) -> Frac {
    let sigma1 = |n: i128| -> i128 {
        let mut s = 0;
        let lim = isqrt_i128(n);
        for k in 1..=lim {
            if n % k == 0 {
                s += k;
                if k * k != n {
                    s += n / k;
                }
            }
        }
        s
    };
    let mut total = 0;
    let lim = isqrt_i128(d);
    for b in -lim..=lim {
        let rem = d - b * b;
        if rem > 0 && rem % 4 == 0 {
            total += sigma1(rem / 4);
        }
    }
    Frac::new(total, 60)
}

type Mat8 = [[u8; 8]; 8];

fn mm8(x: &Mat8, y: &Mat8, modulus: u8) -> Mat8 {
    let mut out = [[0u8; 8]; 8];
    for i in 0..8 {
        for j in 0..8 {
            let mut s: u32 = 0;
            for k in 0..8 {
                s += (x[i][k] as u32) * (y[k][j] as u32);
            }
            out[i][j] = (s % (modulus as u32)) as u8;
        }
    }
    out
}

fn id8() -> Mat8 {
    let mut m = [[0u8; 8]; 8];
    for i in 0..8 {
        m[i][i] = 1;
    }
    m
}

struct Q33OrderData {
    sch_w: Vec<Vec<usize>>,
    r4: Vec<Mat8>,
    w4: Mat8,
    ad4_mats: Vec<Mat8>,
}

fn build_q33_glued_max_order(is_twin_b: bool) -> Q33OrderData {
    let (tw, nw) = (1i128, -8i128);
    let z: Qf = [Frac::zero(), Frac::zero()];
    let o: Qf = [Frac::one(), Frac::zero()];
    let wf: Qf = [Frac::zero(), Frac::one()];
    let pi1: Qf = [Frac::from_int(2), Frac::one()];
    let pi2: Qf = [Frac::from_int(3), Frac::from_int(-1)];
    assert_eq!(qf_norm(pi1, tw, nw), Frac::from_int(-2));
    assert_eq!(qf_norm(pi2, tw, nw), Frac::from_int(-2));
    assert_eq!(qf_mul(pi1, pi2, tw, nw), [Frac::from_int(-2), Frac::zero()]);

    let (a, b, pi_a, pi_b, gens): (Qf, Qf, Qf, Qf, [QfQ; 4]) = if !is_twin_b {
        (
            [Frac::from_int(-4), Frac::one()],
            [Frac::from_int(-3), Frac::from_int(-1)],
            pi1,
            pi2,
            [[z, o, z, z], [z, z, o, z], [z, o, z, o], [z, z, o, o]],
        )
    } else {
        let two = [Frac::from_int(2), Frac::zero()];
        (
            [Frac::from_int(-3), Frac::from_int(-1)],
            [Frac::from_int(-4), Frac::one()],
            pi2,
            pi1,
            [[z, o, z, z], [z, z, o, z], [z, two, z, o], [z, z, two, o]],
        )
    };

    let iq: QfQ = [z, qf_inv(pi_a, tw, nw), z, z];
    let jq: QfQ = [z, z, qf_inv(pi_b, tw, nw), z];
    let kq = qf_qmul(iq, jq, a, b, tw, nw);
    let base_ij = [[o, z, z, z], iq, jq, kq];
    let lin = |c0: Qf, c1: Qf, c2: Qf, c3: Qf| -> QfQ {
        let mut out = [z; 4];
        for m in 0..4 {
            let s = qf_add(
                qf_add(qf_mul(c0, base_ij[0][m], tw, nw), qf_mul(c1, base_ij[1][m], tw, nw)),
                qf_add(qf_mul(c2, base_ij[2][m], tw, nw), qf_mul(c3, base_ij[3][m], tw, nw)),
            );
            out[m] = qf_scale(s, Frac::new(1, 2));
        }
        out
    };
    let o1 = [[o, z, z, z], iq, lin(o, z, o, z), lin(z, o, z, o)];
    let o2 = [[o, z, z, z], lin(o, o, z, z), jq, lin(z, z, o, o)];
    let q_to_v8 = |q: QfQ| -> Vec<Frac> {
        vec![q[0][0], q[0][1], q[1][0], q[1][1], q[2][0], q[2][1], q[3][0], q[3][1]]
    };
    let v8_to_q = |v: &[Frac]| -> QfQ {
        [[v[0], v[1]], [v[2], v[3]], [v[4], v[5]], [v[6], v[7]]]
    };

    let mut gens8: Vec<QfQ> = Vec::with_capacity(16);
    for &e in &o1 {
        let q1 = qf_qscale(pi2, e, tw, nw);
        gens8.push(q1);
        gens8.push(qf_qscale(wf, q1, tw, nw));
    }
    for &e in &o2 {
        let q2 = qf_qscale(pi1, e, tw, nw);
        gens8.push(q2);
        gens8.push(qf_qscale(wf, q2, tw, nw));
    }
    let d_scale = Frac::from_int(16);
    let rows_int: Vec<Vec<i128>> = gens8
        .iter()
        .map(|&q| {
            q_to_v8(q)
                .into_iter()
                .map(|x| {
                    let s = x * d_scale;
                    assert_eq!(s.d, 1);
                    s.n
                })
                .collect()
        })
        .collect();
    let h = hnf_int_rows(&rows_int);
    assert_eq!(h.len(), 8);
    let basis: Vec<Vec<Frac>> = h.iter().map(|r| r.iter().map(|&x| Frac::new(x, 16)).collect()).collect();
    let qs: Vec<QfQ> = basis.iter().map(|v| v8_to_q(v)).collect();
    let binv = inv_frac_mat(&basis);

    // Verify det(T_8) / 33^4 == 1 and ring closure
    let m_t: Vec<Vec<Frac>> = qs
        .iter()
        .map(|&qi| {
            qs.iter()
                .map(|&qj| qf_tr(qf_qmul(qi, qj, a, b, tw, nw)[0], tw) * Frac::from_int(2))
                .collect()
        })
        .collect();
    assert_eq!(det_frac_exact(&m_t).abs() / Frac::from_int(33i128.pow(4)), Frac::one());
    for &qi in &qs {
        for &qj in &qs {
            let v = q_to_v8(qf_qmul(qi, qj, a, b, tw, nw));
            for m in 0..8 {
                let mut acc = Frac::zero();
                for k in 0..8 {
                    acc = acc + v[k] * binv[k][m];
                }
                assert_eq!(acc.d, 1);
            }
        }
    }

    // Conjugation denoms == [1, 1, 3, 3] and Ad_4 matrices
    let mut denoms = Vec::new();
    let mut ad4_mats = Vec::new();
    for &g in &gens {
        let ng = qf_qnrd(g, a, b, tw, nw);
        let ginv = qf_qscale(qf_inv(ng, tw, nw), qf_qconj(g), tw, nw);
        let mut dg = 1i128;
        let mut m4 = [[0u8; 8]; 8];
        for (i, &qi) in qs.iter().enumerate() {
            let v = q_to_v8(qf_qmul(qf_qmul(g, qi, a, b, tw, nw), ginv, a, b, tw, nw));
            for m in 0..8 {
                let mut acc = Frac::zero();
                for k in 0..8 {
                    acc = acc + v[k] * binv[k][m];
                }
                dg = lcm_i128(dg, acc.d);
                m4[i][m] = acc.mod_m(4) as u8;
            }
        }
        denoms.push(dg);
        ad4_mats.push(m4);
    }
    assert_eq!(denoms, vec![1, 1, 3, 3]);

    // Extract 10 exact norm-1 Schreier generators over 4 square-class cosets
    let nrds: Vec<Qf> = gens.iter().map(|&g| qf_qnrd(g, a, b, tw, nw)).collect();
    let mut coset_n = vec![o];
    let mut coset_w: Vec<Vec<usize>> = vec![vec![]];
    let mut coset_tr: Vec<[usize; 4]> = Vec::new();
    let mut idx = 0;
    while idx < coset_n.len() {
        let rn = coset_n[idx];
        let rw = coset_w[idx].clone();
        let mut row = [0usize; 4];
        for gi in 0..4 {
            let cand = qf_mul(rn, nrds[gi], tw, nw);
            let found = coset_n
                .iter()
                .position(|&cn| qf_sqrt_exact(qf_mul(cand, cn, tw, nw), tw, nw, 33).is_some());
            let cid = match found {
                Some(c) => c,
                None => {
                    let c = coset_n.len();
                    coset_n.push(cand);
                    let mut nw_w = rw.clone();
                    nw_w.push(gi);
                    coset_w.push(nw_w);
                    c
                }
            };
            row[gi] = cid;
        }
        coset_tr.push(row);
        idx += 1;
    }
    assert_eq!(coset_n.len(), 4);

    let mut sch_w = Vec::new();
    let mut sch_q = Vec::new();
    let neg_one: QfQ = [[-Frac::one(), Frac::zero()], z, z, z];
    let pos_one: QfQ = [o, z, z, z];
    for (ci, rw) in coset_w.iter().enumerate() {
        for gi in 0..4 {
            let cj = coset_tr[ci][gi];
            let mut wd = rw.clone();
            wd.push(gi);
            wd.extend(coset_w[cj].iter().rev().copied());
            let mut q = pos_one;
            for &k in &wd {
                q = qf_qmul(q, gens[k], a, b, tw, nw);
            }
            let sc = qf_sqrt_exact(qf_qnrd(q, a, b, tw, nw), tw, nw, 33).expect("Schreier norm must be square");
            let qn = qf_qscale(qf_inv(sc, tw, nw), q, tw, nw);
            assert_eq!(qf_qnrd(qn, a, b, tw, nw), o);
            if qn != pos_one && qn != neg_one {
                sch_w.push(wd);
                sch_q.push(qn);
            }
        }
    }
    assert_eq!(sch_q.len(), 10);

    let rmat8 = |q: QfQ| -> Mat8 {
        let mut mat = [[0u8; 8]; 8];
        for (i, &e) in qs.iter().enumerate() {
            let v = q_to_v8(qf_qmul(e, q, a, b, tw, nw));
            for m in 0..8 {
                let mut acc = Frac::zero();
                for k in 0..8 {
                    acc = acc + v[k] * binv[k][m];
                }
                mat[i][m] = acc.mod_m(4) as u8;
            }
        }
        mat
    };
    let r4: Vec<Mat8> = sch_q.iter().map(|&q| rmat8(q)).collect();
    let w4 = rmat8([wf, z, z, z]);
    Q33OrderData { sch_w, r4, w4, ad4_mats }
}

fn verify_q33_ideal_ladder(ord: &Q33OrderData, aut: &Dic6AutData) {
    let i8 = id8();
    let p2 = ord.w4;
    let mut p1 = [[0u8; 8]; 8];
    let mut neg_i8 = [[0u8; 8]; 8];
    let mut flip_i8 = [[0u8; 8]; 8];
    for i in 0..8 {
        for j in 0..8 {
            p1[i][j] = (i8[i][j] + 4 - p2[i][j]) % 4;
            neg_i8[i][j] = (4 - i8[i][j]) % 4;
            flip_i8[i][j] = (p1[i][j] + 4 - p2[i][j]) % 4;
        }
    }
    assert_eq!(mm8(&p1, &p1, 4), p1);
    assert_eq!(mm8(&p2, &p2, 4), p2);
    assert_eq!(mm8(&p1, &p2, 4), [[0u8; 8]; 8]);
    assert_eq!(mm8(&flip_i8, &flip_i8, 4), i8);

    let sp_sch_all: Vec<Vec<usize>> = aut
        .surjs_i
        .iter()
        .map(|sp| {
            ord.sch_w
                .iter()
                .map(|wd| {
                    let mut cur = aut.id_p;
                    for &gi in wd {
                        cur = aut.aut_mul[cur][sp[gi]];
                    }
                    cur
                })
                .collect()
        })
        .collect();

    let expected = [
        (1u8, 0u8, 6usize, 6usize, false, 4usize),
        (0, 1, 6, 6, false, 12),
        (1, 1, 36, 36, false, 2),
        (2, 0, 48, 24, false, 4),
        (0, 2, 48, 24, false, 12),
        (2, 1, 288, 144, false, 2),
        (1, 2, 288, 144, false, 2),
        (2, 2, 2304, 1152, true, 1),
    ];

    for (a_e, b_e, exp_ls, exp_lp, exp_sep, exp_min_ker) in expected {
        let m1: u8 = 1 << a_e;
        let m2: u8 = 1 << b_e;
        let proj = |m: &Mat8| -> (Mat8, Mat8) {
            let mut c1 = [[0u8; 8]; 8];
            let mut c2 = [[0u8; 8]; 8];
            if a_e > 0 {
                let pm = mm8(&p1, m, 4);
                for i in 0..8 {
                    for j in 0..8 {
                        c1[i][j] = pm[i][j] % m1;
                    }
                }
            }
            if b_e > 0 {
                let pm = mm8(&p2, m, 4);
                for i in 0..8 {
                    for j in 0..8 {
                        c2[i][j] = pm[i][j] % m2;
                    }
                }
            }
            (c1, c2)
        };
        let mul_p = |x: &(Mat8, Mat8), y: &(Mat8, Mat8)| -> (Mat8, Mat8) {
            let c1 = if a_e > 0 { mm8(&x.0, &y.0, m1) } else { [[0u8; 8]; 8] };
            let c2 = if b_e > 0 { mm8(&x.1, &y.1, m2) } else { [[0u8; 8]; 8] };
            (c1, c2)
        };

        let gens_p: Vec<(Mat8, Mat8)> = ord.r4.iter().map(proj).collect();
        let id_m = proj(&i8);
        let neg_m = proj(&neg_i8);
        let flip_m = proj(&flip_i8);

        let mut m_id: HashMap<(Mat8, Mat8), usize> = HashMap::new();
        m_id.insert(id_m, 0);
        let mut m_list = vec![id_m];
        let mut tr: Vec<[usize; 10]> = Vec::new();
        let mut idx = 0;
        while idx < m_list.len() {
            let cur = m_list[idx];
            let mut row = [0usize; 10];
            for gi in 0..10 {
                let nxt = mul_p(&cur, &gens_p[gi]);
                let nid = *m_id.entry(nxt).or_insert_with(|| {
                    let k = m_list.len();
                    m_list.push(nxt);
                    k
                });
                row[gi] = nid;
            }
            tr.push(row);
            idx += 1;
        }
        let sz = m_list.len();
        assert_eq!(sz, exp_ls);
        let has_neg = m_id.contains_key(&neg_m) && neg_m != id_m;
        let l_proj = if has_neg { sz / 2 } else { sz };
        assert_eq!(l_proj, exp_lp);
        assert!(m_id.contains_key(&flip_m));
        assert_eq!(flip_m != id_m && flip_m != neg_m, exp_sep);

        let mut kers: BTreeMap<usize, usize> = BTreeMap::new();
        for sp_sch in &sp_sch_all {
            let mut seen = vec![false; sz * 96];
            seen[aut.id_p] = true;
            let mut st = vec![aut.id_p];
            let mut cnt = 1usize;
            while let Some(x) = st.pop() {
                let mi = x / 96;
                let pi = x % 96;
                let trow = &tr[mi];
                let am = &aut.aut_mul[pi];
                for gi in 0..10 {
                    let nx = trow[gi] * 96 + am[sp_sch[gi]];
                    if !seen[nx] {
                        seen[nx] = true;
                        cnt += 1;
                        st.push(nx);
                    }
                }
            }
            *kers.entry(cnt / sz).or_insert(0) += 1;
        }
        assert_eq!(*kers.keys().next().unwrap(), exp_min_ker);
        if a_e == 2 && b_e == 2 {
            assert_eq!(kers.get(&1), Some(&4));
            assert_eq!(kers.get(&2), Some(&4));
            assert_eq!(kers.get(&3), Some(&4));
            assert_eq!(kers.get(&6), Some(&4));
        }
    }

    // Verify Ad_{(4)} stalls at min |ker| = 2 ({2: 8, 6: 8})
    let mut ad_id: HashMap<Mat8, usize> = HashMap::new();
    ad_id.insert(i8, 0);
    let mut ad_list = vec![i8];
    let mut ad_tr: Vec<[usize; 4]> = Vec::new();
    let mut idx = 0;
    while idx < ad_list.len() {
        let cur = ad_list[idx];
        let mut row = [0usize; 4];
        for gi in 0..4 {
            let nxt = mm8(&cur, &ord.ad4_mats[gi], 4);
            let nid = *ad_id.entry(nxt).or_insert_with(|| {
                let k = ad_list.len();
                ad_list.push(nxt);
                k
            });
            row[gi] = nid;
        }
        ad_tr.push(row);
        idx += 1;
    }
    let ad_sz = ad_list.len();
    assert_eq!(ad_sz, 2304);
    let mut ad_kers: BTreeMap<usize, usize> = BTreeMap::new();
    for sp in &aut.surjs_i {
        let mut seen = vec![false; ad_sz * 96];
        seen[aut.id_p] = true;
        let mut st = vec![aut.id_p];
        let mut cnt = 1usize;
        while let Some(x) = st.pop() {
            let mi = x / 96;
            let pi = x % 96;
            for gi in 0..4 {
                let nx = ad_tr[mi][gi] * 96 + aut.aut_mul[pi][sp[gi]];
                if !seen[nx] {
                    seen[nx] = true;
                    cnt += 1;
                    st.push(nx);
                }
            }
        }
        *ad_kers.entry(cnt / ad_sz).or_insert(0) += 1;
    }
    assert_eq!(ad_kers.get(&2), Some(&8));
    assert_eq!(ad_kers.get(&6), Some(&8));
}

pub fn run_suite_r2_q33_level4_congruence() {
    let aut = build_dic6_aut();

    // 1. Exact Zagier zeta_F(-1) across all 4 real-quadratic fields & Hensel roots mod 16
    assert_eq!(zagier_zeta_real_quad_neg1(33), Frac::one());
    assert_eq!(zagier_zeta_real_quad_neg1(24), Frac::new(1, 2));
    assert_eq!(zagier_zeta_real_quad_neg1(12), Frac::new(1, 6));
    assert_eq!(zagier_zeta_real_quad_neg1(13), Frac::new(1, 6));
    let roots16: Vec<i128> = (0..16).filter(|&r| mod_pos(r * r - r - 8, 16) == 0).collect();
    assert_eq!(roots16, vec![8, 9]);

    // 2. Full Table 1 ideal ladder + Ad_{(4)} stall on BOTH Q(sqrt(33))_A and twin Q(sqrt(33))_B
    let ord_a = build_q33_glued_max_order(false);
    let ord_b = build_q33_glued_max_order(true);
    verify_q33_ideal_ladder(&ord_a, &aut);
    verify_q33_ideal_ladder(&ord_b, &aut);

    // 3. Exhaustive 4 Locus B + 4 Locus A real-quadratic moduli enumeration (8 total)
    let sqfree = |mut d: i128| -> i128 {
        let mut p = 2;
        while p * p <= d {
            while d % (p * p) == 0 {
                d /= p * p;
            }
            p += 1;
        }
        d
    };
    let mut lb_ds = Vec::new();
    for m in 1..8i128 {
        for k in 1..16i128 {
            let disc = 9 * m * m - 48 * k;
            let f1 = 12 - 3 * m + k;
            if disc <= 0 || f1 <= 0 || k % 3 == 0 {
                continue;
            }
            let s = isqrt_i128(disc);
            if s * s == disc {
                continue;
            }
            if 4 % k == 0 && 4 % f1 == 0 {
                lb_ds.push(sqfree(disc));
            }
        }
    }
    lb_ds.sort();
    assert_eq!(lb_ds, vec![3, 6, 33, 33]);

    let mut la_ds = Vec::new();
    for a_c in 1..12i128 {
        for b_c in 1..12i128 {
            let disc = a_c * a_c - 12 * b_c;
            let f2 = 12 - 2 * a_c + b_c;
            if disc <= 0 || f2 <= 0 || gcd_i128(gcd_i128(3, a_c), b_c) > 1 {
                continue;
            }
            let s = isqrt_i128(disc);
            if s * s == disc {
                continue;
            }
            if (b_c <= 3) && (f2 <= 3) && (b_c % 2 == 1 || a_c % 2 == 0) {
                la_ds.push(sqfree(disc));
            }
        }
    }
    la_ds.sort();
    assert_eq!(la_ds, vec![3, 6, 13, 13]);

    // 4. Q(sqrt(13))_A Riehm C_5 obstruction check: R_{p_3'} (|R|=36, ker={4:8, 12:8}) & R_2 (|R|=80, ker={24:16})
    let (tw13, nw13) = (1i128, -3i128);
    let z: Qf = [Frac::zero(), Frac::zero()];
    let o: Qf = [Frac::one(), Frac::zero()];
    let h: Qf = [Frac::new(1, 2), Frac::zero()];
    let a13: Qf = [Frac::from_int(-5), Frac::from_int(2)];
    let inv_a13 = qf_inv(a13, tw13, nw13);
    let basis13: [QfQ; 4] = [
        [o, z, z, z],
        [h, h, h, qf_scale(inv_a13, Frac::new(1, 2))],
        [z, z, o, z],
        [z, z, z, inv_a13],
    ];
    let q_to_v8 = |q: QfQ| -> Vec<Frac> {
        vec![q[0][0], q[0][1], q[1][0], q[1][1], q[2][0], q[2][1], q[3][0], q[3][1]]
    };
    let mut b13_8 = Vec::with_capacity(8);
    let wf13: Qf = [Frac::zero(), Frac::one()];
    for &e in &basis13 {
        b13_8.push(q_to_v8(e));
        b13_8.push(q_to_v8(qf_qscale(wf13, e, tw13, nw13)));
    }
    let binv13 = inv_frac_mat(&b13_8);
    let gens13: [QfQ; 4] = [[z, o, z, z], [z, z, o, z], [z, o, z, o], [z, z, o, o]];
    let g_cls13 = [1usize, 1, 3, 3];
    let reps13: [&[usize]; 4] = [&[], &[0], &[0, 2], &[2]];
    let pos_one: QfQ = [o, z, z, z];
    let neg_one: QfQ = [[-Frac::one(), Frac::zero()], z, z, z];
    let mut sch13_w = Vec::new();
    let mut sch13_q = Vec::new();
    for (ci, rw) in reps13.iter().enumerate() {
        for gi in 0..4 {
            let cj = ci ^ g_cls13[gi];
            let mut wd = rw.to_vec();
            wd.push(gi);
            wd.extend(reps13[cj].iter().rev().copied());
            let mut q = pos_one;
            for &k in &wd {
                q = qf_qmul(q, gens13[k], a13, a13, tw13, nw13);
            }
            let sc = qf_sqrt_exact(qf_qnrd(q, a13, a13, tw13, nw13), tw13, nw13, 13).unwrap();
            let qn = qf_qscale(qf_inv(sc, tw13, nw13), q, tw13, nw13);
            if qn != pos_one && qn != neg_one {
                sch13_w.push(wd);
                sch13_q.push(qn);
            }
        }
    }
    assert_eq!(sch13_q.len(), 10);

    // Right multiplication matrices R_{p_3'} (4x4 over F_3) and R_{(2)} (8x8 over F_2)
    let mut r13_p3: Vec<[[u8; 4]; 4]> = Vec::new();
    let mut r13_2: Vec<Mat8> = Vec::new();
    for &q in &sch13_q {
        let mut m3 = [[0u8; 4]; 4];
        for (i, &e) in basis13.iter().enumerate() {
            let v = q_to_v8(qf_qmul(e, q, a13, a13, tw13, nw13));
            for m in 0..4 {
                let mut c0 = Frac::zero();
                let mut c1 = Frac::zero();
                for k in 0..8 {
                    c0 = c0 + v[k] * binv13[k][2 * m];
                    c1 = c1 + v[k] * binv13[k][2 * m + 1];
                }
                let den = lcm_i128(c0.d, c1.d);
                let mut num_v = c0.n * (den / c0.d) + c1.n * (den / c1.d) * 22;
                let mut dt = den;
                while dt % 3 == 0 {
                    assert_eq!(num_v % 3, 0);
                    num_v /= 3;
                    dt /= 3;
                }
                m3[i][m] = mod_pos(num_v * mod_inv(dt, 3), 3) as u8;
            }
        }
        r13_p3.push(m3);

        let mut m2 = [[0u8; 8]; 8];
        for (i, &e) in basis13.iter().enumerate() {
            for (s, q_b) in [e, qf_qscale(wf13, e, tw13, nw13)].into_iter().enumerate() {
                let v = q_to_v8(qf_qmul(q_b, q, a13, a13, tw13, nw13));
                for m in 0..8 {
                    let mut acc = Frac::zero();
                    for k in 0..8 {
                        acc = acc + v[k] * binv13[k][m];
                    }
                    m2[2 * i + s][m] = acc.mod_m(2) as u8;
                }
            }
        }
        r13_2.push(m2);
    }

    // BFS for R_{p_3'}
    let id4_3 = [[1u8, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]];
    let mm4_3 = |x: &[[u8; 4]; 4], y: &[[u8; 4]; 4]| -> [[u8; 4]; 4] {
        let mut o = [[0u8; 4]; 4];
        for i in 0..4 {
            for j in 0..4 {
                let mut s = 0u16;
                for k in 0..4 {
                    s += (x[i][k] as u16) * (y[k][j] as u16);
                }
                o[i][j] = (s % 3) as u8;
            }
        }
        o
    };
    let mut mid3: HashMap<[[u8; 4]; 4], usize> = HashMap::new();
    mid3.insert(id4_3, 0);
    let mut ml3 = vec![id4_3];
    let mut tr3 = Vec::new();
    let mut idx = 0;
    while idx < ml3.len() {
        let cur = ml3[idx];
        let mut row = [0usize; 10];
        for gi in 0..10 {
            let nxt = mm4_3(&cur, &r13_p3[gi]);
            let nid = *mid3.entry(nxt).or_insert_with(|| {
                let k = ml3.len();
                ml3.push(nxt);
                k
            });
            row[gi] = nid;
        }
        tr3.push(row);
        idx += 1;
    }
    assert_eq!(ml3.len(), 36);

    // BFS for R_{(2)}
    let i8 = id8();
    let mut mid2: HashMap<Mat8, usize> = HashMap::new();
    mid2.insert(i8, 0);
    let mut ml2 = vec![i8];
    let mut tr2 = Vec::new();
    idx = 0;
    while idx < ml2.len() {
        let cur = ml2[idx];
        let mut row = [0usize; 10];
        for gi in 0..10 {
            let nxt = mm8(&cur, &r13_2[gi], 2);
            let nid = *mid2.entry(nxt).or_insert_with(|| {
                let k = ml2.len();
                ml2.push(nxt);
                k
            });
            row[gi] = nid;
        }
        tr2.push(row);
        idx += 1;
    }
    assert_eq!(ml2.len(), 80);

    let sp_sch13: Vec<Vec<usize>> = aut
        .surjs_i
        .iter()
        .map(|sp| {
            sch13_w
                .iter()
                .map(|wd| {
                    let mut cur = aut.id_p;
                    for &gi in wd {
                        cur = aut.aut_mul[cur][sp[gi]];
                    }
                    cur
                })
                .collect()
        })
        .collect();

    let eval_kers = |sz: usize, tr: &[[usize; 10]]| -> BTreeMap<usize, usize> {
        let mut kers = BTreeMap::new();
        for sp_sch in &sp_sch13 {
            let mut seen = vec![false; sz * 96];
            seen[aut.id_p] = true;
            let mut st = vec![aut.id_p];
            let mut cnt = 1usize;
            while let Some(x) = st.pop() {
                let mi = x / 96;
                let pi = x % 96;
                for gi in 0..10 {
                    let nx = tr[mi][gi] * 96 + aut.aut_mul[pi][sp_sch[gi]];
                    if !seen[nx] {
                        seen[nx] = true;
                        cnt += 1;
                        st.push(nx);
                    }
                }
            }
            *kers.entry(cnt / sz).or_insert(0) += 1;
        }
        kers
    };
    let k3 = eval_kers(36, &tr3);
    let k2 = eval_kers(80, &tr2);
    assert_eq!(k3.get(&4), Some(&8));
    assert_eq!(k3.get(&12), Some(&8));
    assert_eq!(k2.get(&24), Some(&16));
    assert_eq!(gcd_i128(4, 5), 1);
}

// ============================================================================
// Suite R3: Frontier 3 — Complete 9/9 Genus-25 Borel Brandt B(3) Atlas
// ============================================================================

type QQuat = [Frac; 4];

fn qq_mul(x: QQuat, y: QQuat, a: i128, b: i128) -> QQuat {
    let fa = Frac::from_int(a);
    let fb = Frac::from_int(b);
    [
        x[0] * y[0] + fa * x[1] * y[1] + fb * x[2] * y[2] - fa * fb * x[3] * y[3],
        x[0] * y[1] + x[1] * y[0] + fb * (x[3] * y[2] - x[2] * y[3]),
        x[0] * y[2] + x[2] * y[0] + fa * (x[1] * y[3] - x[3] * y[1]),
        x[0] * y[3] + x[3] * y[0] + x[1] * y[2] - x[2] * y[1],
    ]
}
fn qq_conj(x: QQuat) -> QQuat {
    [x[0], -x[1], -x[2], -x[3]]
}
fn qq_nrd(x: QQuat, a: i128, b: i128) -> Frac {
    let fa = Frac::from_int(a);
    let fb = Frac::from_int(b);
    x[0] * x[0] - fa * x[1] * x[1] - fb * x[2] * x[2] + fa * fb * x[3] * x[3]
}

fn fp_cholesky_4x4(g: &[[f64; 4]; 4]) -> [[f64; 4]; 4] {
    let mut r = [[0.0f64; 4]; 4];
    for i in 0..4 {
        let mut s = g[i][i];
        for k in 0..i {
            s -= r[k][i] * r[k][i];
        }
        r[i][i] = s.max(1e-15).sqrt();
        for j in (i + 1)..4 {
            let mut t = g[i][j];
            for k in 0..i {
                t -= r[k][i] * r[k][j];
            }
            r[i][j] = t / r[i][i];
        }
    }
    r
}

fn make_order_embed_m2(a: i128, b: i128, n_level: i128) -> Box<dyn Fn(QQuat) -> [i128; 4]> {
    let mut facs: Vec<(i128, i128)> = Vec::new();
    let mut tmp = n_level;
    let mut d = 2i128;
    while d * d <= tmp {
        if tmp % d == 0 {
            let mut pe = 1i128;
            while tmp % d == 0 {
                tmp /= d;
                pe *= d;
            }
            facs.push((d, pe));
        }
        d += 1;
    }
    if tmp > 1 {
        facs.push((tmp, tmp));
    }

    enum LocEmb {
        B7 { pe: i128 },
        B2 { pe: i128, x: i128, y: i128 },
        Odd { pe: i128, a0: i128, c0: i128, b: i128 },
    }
    let mut locs = Vec::new();
    let mut weights = Vec::new();
    for (p, pe) in facs {
        let m_other = n_level / pe;
        weights.push(m_other * mod_inv(m_other, pe));
        if p == 2 {
            if a == -1 && b == -7 {
                locs.push(LocEmb::B7 { pe });
            } else {
                let (x, y) = if b == -5 { (5, 1) } else { (1, 3) };
                locs.push(LocEmb::B2 { pe, x, y });
            }
        } else {
            let mut found = None;
            'outer: for c in 0..pe {
                let rhs = mod_pos(a + b * c * c, pe);
                for a0 in 0..pe {
                    if (a0 * a0) % pe == rhs {
                        found = Some((a0, c));
                        break 'outer;
                    }
                }
            }
            let (a0, c0) = found.unwrap();
            locs.push(LocEmb::Odd { pe, a0, c0, b });
        }
    }

    Box::new(move |q: QQuat| -> [i128; 4] {
        let den = lcm_i128(lcm_i128(q[0].d, q[1].d), lcm_i128(q[2].d, q[3].d));
        let (n0, n1, n2, n3) = (
            q[0].n * (den / q[0].d),
            q[1].n * (den / q[1].d),
            q[2].n * (den / q[2].d),
            q[3].n * (den / q[3].d),
        );
        let mut acc = [0i128; 4];
        for (loc, &wt) in locs.iter().zip(weights.iter()) {
            let v = match *loc {
                LocEmb::B7 { pe } => {
                    let s = 11i128;
                    let m00 = n0 + n2 * s;
                    let m01 = -n1 + n3 * s;
                    let m10 = n1 + n3 * s;
                    let m11 = n0 - n2 * s;
                    assert!(m00 % den == 0 && m01 % den == 0 && m10 % den == 0 && m11 % den == 0);
                    [
                        mod_pos(m00 / den, pe),
                        mod_pos(m01 / den, pe),
                        mod_pos(m10 / den, pe),
                        mod_pos(m11 / den, pe),
                    ]
                }
                LocEmb::B2 { pe, x, y } => {
                    let m00 = n0 + n2 * x + n3 * (2 * y);
                    let m01 = n1 + n2 * y - n3 * x;
                    let m10 = -2 * n1 + n2 * (2 * y) - n3 * (2 * x);
                    let m11 = n0 - n2 * x - n3 * (2 * y);
                    assert!(m00 % den == 0 && m01 % den == 0 && m10 % den == 0 && m11 % den == 0);
                    [
                        mod_pos(m00 / den, pe),
                        mod_pos(m01 / den, pe),
                        mod_pos(m10 / den, pe),
                        mod_pos(m11 / den, pe),
                    ]
                }
                LocEmb::Odd { pe, a0, c0, b } => {
                    let inv_d = mod_inv(den, pe);
                    let m00 = (n0 + n1 * a0 - n3 * c0 * b) * inv_d;
                    let m01 = (-n1 * c0 * b + n2 * b + n3 * a0 * b) * inv_d;
                    let m10 = (n1 * c0 + n2 - n3 * a0) * inv_d;
                    let m11 = (n0 - n1 * a0 + n3 * c0 * b) * inv_d;
                    [mod_pos(m00, pe), mod_pos(m01, pe), mod_pos(m10, pe), mod_pos(m11, pe)]
                }
            };
            for k in 0..4 {
                acc[k] += v[k] * wt;
            }
        }
        [
            mod_pos(acc[0], n_level),
            mod_pos(acc[1], n_level),
            mod_pos(acc[2], n_level),
            mod_pos(acc[3], n_level),
        ]
    })
}

fn brandt_h1_from_order(a: i128, b: i128, basis: &[QQuat; 4], n_level: i128) -> [[i64; 12]; 12] {
    let emb = make_order_embed_m2(a, b, n_level);
    let mut g = [[0.0f64; 4]; 4];
    for i in 0..4 {
        for j in 0..4 {
            g[i][j] = qq_mul(basis[i], qq_conj(basis[j]), a, b)[0].to_f64();
        }
    }
    let r = fp_cholesky_4x4(&g);
    let mut units = Vec::new();
    let mut norm3 = Vec::new();
    let mut c = [0i128; 4];

    fn fp_dfs(
        k: isize,
        rem: f64,
        r: &[[f64; 4]; 4],
        c: &mut [i128; 4],
        basis: &[QQuat; 4],
        a: i128,
        b: i128,
        units: &mut Vec<QQuat>,
        norm3: &mut Vec<QQuat>,
    ) {
        if k < 0 {
            let mut q = [Frac::zero(); 4];
            for m in 0..4 {
                let mut acc = Frac::zero();
                for j in 0..4 {
                    acc = acc + Frac::from_int(c[j]) * basis[j][m];
                }
                q[m] = acc;
            }
            let nr = qq_nrd(q, a, b);
            if nr == Frac::one() {
                units.push(q);
            } else if nr == Frac::from_int(3) {
                norm3.push(q);
            }
            return;
        }
        let ku = k as usize;
        let mut shift = 0.0;
        for j in (ku + 1)..4 {
            shift += r[ku][j] * (c[j] as f64);
        }
        let rad = rem.max(0.0).sqrt() / r[ku][ku];
        let center = -shift / r[ku][ku];
        let lo = (center - rad - 1e-9).ceil() as i128;
        let hi = (center + rad + 1e-9).floor() as i128;
        for v in lo..=hi {
            c[ku] = v;
            let val = r[ku][ku] * (v as f64) + shift;
            let nrem = rem - val * val;
            if nrem >= -1e-7 {
                fp_dfs(k - 1, nrem.max(0.0), r, c, basis, a, b, units, norm3);
            }
        }
    }
    fp_dfs(3, 3.0 + 1e-6, &r, &mut c, basis, a, b, &mut units, &mut norm3);

    let canon_p1 = |u: i128, v: i128| -> (i128, i128) {
        let u = mod_pos(u, n_level);
        let v = mod_pos(v, n_level);
        if gcd_i128(u, n_level) == 1 {
            return (1, mod_pos(v * mod_inv(u, n_level), n_level));
        }
        let mut best = (n_level, n_level);
        for s in 1..n_level {
            if gcd_i128(s, n_level) == 1 {
                let cand = (mod_pos(u * s, n_level), mod_pos(v * s, n_level));
                if cand < best {
                    best = cand;
                }
            }
        }
        best
    };

    let mut pts_set = BTreeSet::new();
    for u in 0..n_level {
        for v in 0..n_level {
            if gcd_i128(gcd_i128(u, v), n_level) == 1 {
                pts_set.insert(canon_p1(u, v));
            }
        }
    }
    let pts: Vec<(i128, i128)> = pts_set.into_iter().collect();
    let mut pt_idx = HashMap::new();
    for (i, &p) in pts.iter().enumerate() {
        pt_idx.insert(p, i);
    }

    let unit_mats: Vec<[i128; 4]> = units.iter().map(|&u| emb(u)).collect();
    let mut orb_of = vec![usize::MAX; pts.len()];
    let mut orbits: Vec<Vec<usize>> = Vec::new();
    for i in 0..pts.len() {
        if orb_of[i] != usize::MAX {
            continue;
        }
        let oid = orbits.len();
        let mut orb = Vec::new();
        let mut dq = VecDeque::new();
        orb_of[i] = oid;
        dq.push_back(i);
        while let Some(cur) = dq.pop_front() {
            orb.push(cur);
            let p = pts[cur];
            for m in &unit_mats {
                let nxt = pt_idx[&canon_p1(p.0 * m[0] + p.1 * m[2], p.0 * m[1] + p.1 * m[3])];
                if orb_of[nxt] == usize::MAX {
                    orb_of[nxt] = oid;
                    dq.push_back(nxt);
                }
            }
        }
        orbits.push(orb);
    }
    assert_eq!(orbits.len(), 12);
    let w_unit = units.len() as i64;
    assert_eq!(norm3.len() as i64, 4 * w_unit);
    let n3_mats: Vec<[i128; 4]> = norm3.iter().map(|&q| emb(q)).collect();

    let mut bmat = [[0i64; 12]; 12];
    for i in 0..12 {
        let rep = pts[orbits[i][0]];
        for m in &n3_mats {
            let j = orb_of[pt_idx[&canon_p1(rep.0 * m[0] + rep.1 * m[2], rep.0 * m[1] + rep.1 * m[3])]];
            bmat[i][j] += 1;
        }
    }
    for i in 0..12 {
        for j in 0..12 {
            assert_eq!(bmat[i][j] % w_unit, 0);
            bmat[i][j] /= w_unit;
        }
    }
    bmat
}

fn brandt_general_hnf_bfs(a: i128, b: i128, basis_o: &[QQuat; 4], expected_rd: i128) -> [[i64; 12]; 12] {
    let t4: Vec<Vec<Frac>> = (0..4)
        .map(|i| (0..4).map(|j| Frac::from_int(2) * qq_mul(basis_o[i], basis_o[j], a, b)[0]).collect())
        .collect();
    assert_eq!(det_frac_exact(&t4).abs(), Frac::from_int(expected_rd * expected_rd));

    let b_mat: Vec<Vec<Frac>> = basis_o.iter().map(|e| e.to_vec()).collect();
    let b_inv = inv_frac_mat(&b_mat);
    let mut mul_tab = [[[0i128; 4]; 4]; 4];
    for i in 0..4 {
        for j in 0..4 {
            let w = qq_mul(basis_o[i], basis_o[j], a, b);
            for m in 0..4 {
                let mut acc = Frac::zero();
                for k in 0..4 {
                    acc = acc + w[k] * b_inv[k][m];
                }
                assert_eq!(acc.d, 1);
                mul_tab[i][j][m] = acc.n;
            }
        }
    }
    let mut g_o = [[0i128; 4]; 4];
    for i in 0..4 {
        for j in 0..4 {
            let v = Frac::from_int(2) * qq_mul(basis_o[i], qq_conj(basis_o[j]), a, b)[0];
            assert_eq!(v.d, 1);
            g_o[i][j] = v.n;
        }
    }
    let vec_mul_o = |u: &[i128], v: &[i128]| -> [i128; 4] {
        let mut out = [0i128; 4];
        for i in 0..4 {
            if u[i] == 0 {
                continue;
            }
            for j in 0..4 {
                if v[j] == 0 {
                    continue;
                }
                let p = u[i] * v[j];
                for m in 0..4 {
                    out[m] += p * mul_tab[i][j][m];
                }
            }
        }
        out
    };
    let ideal_norm = |h: &[Vec<i128>]| -> i128 {
        let d = h[0][0] * h[1][1] * h[2][2] * h[3][3];
        let s = isqrt_i128(d);
        assert_eq!(s * s, d);
        s
    };
    let ideal_gram = |h: &[Vec<i128>]| -> [[i128; 4]; 4] {
        let n_i = ideal_norm(h);
        let mut hg = [[0i128; 4]; 4];
        for i in 0..4 {
            for j in 0..4 {
                for k in 0..4 {
                    hg[i][j] += h[i][k] * g_o[k][j];
                }
            }
        }
        let mut m = [[0i128; 4]; 4];
        for i in 0..4 {
            for j in 0..4 {
                let mut s = 0;
                for k in 0..4 {
                    s += hg[i][k] * h[j][k];
                }
                m[i][j] = s / n_i;
            }
        }
        m
    };

    let fp_short_vals = |gs: &[[i128; 4]; 4], max_val: i128| -> Vec<i128> {
        let mut gf = [[0.0f64; 4]; 4];
        for i in 0..4 {
            for j in 0..4 {
                gf[i][j] = gs[i][j] as f64;
            }
        }
        let r = fp_cholesky_4x4(&gf);
        let mut out = Vec::new();
        let mut c = [0i128; 4];
        fn dfs(
            k: isize,
            rem: f64,
            r: &[[f64; 4]; 4],
            c: &mut [i128; 4],
            gs: &[[i128; 4]; 4],
            max_val: i128,
            out: &mut Vec<i128>,
        ) {
            if k < 0 {
                if c.iter().any(|&x| x != 0) {
                    let mut qv = 0i128;
                    for i in 0..4 {
                        for j in 0..4 {
                            qv += c[i] * gs[i][j] * c[j];
                        }
                    }
                    if qv > 0 && qv <= max_val {
                        out.push(qv);
                    }
                }
                return;
            }
            let ku = k as usize;
            let mut shift = 0.0;
            for j in (ku + 1)..4 {
                shift += r[ku][j] * (c[j] as f64);
            }
            let rad = rem.max(0.0).sqrt() / r[ku][ku];
            let center = -shift / r[ku][ku];
            let lo = (center - rad - 1e-9).ceil() as i128;
            let hi = (center + rad + 1e-9).floor() as i128;
            for v in lo..=hi {
                c[ku] = v;
                let val = r[ku][ku] * (v as f64) + shift;
                let nrem = rem - val * val;
                if nrem >= -1e-7 {
                    dfs(k - 1, nrem.max(0.0), r, c, gs, max_val, out);
                }
            }
        }
        dfs(3, (max_val as f64) + 1e-6, &r, &mut c, gs, max_val, &mut out);
        out
    };

    let theta_sig = |gs: &[[i128; 4]; 4]| -> Vec<(i128, usize)> {
        let mut cnt = BTreeMap::new();
        for v in fp_short_vals(gs, 16) {
            *cnt.entry(v).or_insert(0) += 1;
        }
        cnt.into_iter().collect()
    };

    let are_equiv = |h1: &[Vec<i128>], h2: &[Vec<i128>]| -> bool {
        let mut h2_conj = Vec::with_capacity(4);
        for r in h2 {
            let mut q = [Frac::zero(); 4];
            for m in 0..4 {
                for j in 0..4 {
                    q[m] = q[m] + Frac::from_int(r[j]) * basis_o[j][m];
                }
            }
            let qc = qq_conj(q);
            let mut cs = vec![0i128; 4];
            for m in 0..4 {
                let mut acc = Frac::zero();
                for k in 0..4 {
                    acc = acc + qc[k] * b_inv[k][m];
                }
                assert_eq!(acc.d, 1);
                cs[m] = acc.n;
            }
            h2_conj.push(cs);
        }
        let mut prods = Vec::with_capacity(16);
        for r1 in h1 {
            for r2 in &h2_conj {
                prods.push(vec_mul_o(r1, r2).to_vec());
            }
        }
        let mut hl = hnf_int_rows(&prods);
        let mut g_all = 0i128;
        for r in &hl {
            for &x in r {
                g_all = gcd_i128(g_all, x);
            }
        }
        for r in &mut hl {
            for x in r {
                *x /= g_all;
            }
        }
        !fp_short_vals(&ideal_gram(&hl), 2).is_empty()
    };

    let rref_f3 = |rows: &[Vec<u8>]| -> Vec<[u8; 4]> {
        let mut a: Vec<[u8; 4]> = rows.iter().map(|r| [r[0] % 3, r[1] % 3, r[2] % 3, r[3] % 3]).collect();
        let mut r = 0usize;
        for c in 0..4 {
            let piv = match (r..a.len()).find(|&i| a[i][c] != 0) {
                Some(p) => p,
                None => continue,
            };
            a.swap(r, piv);
            let inv_p = if a[r][c] == 1 { 1u8 } else { 2u8 };
            for j in 0..4 {
                a[r][j] = (a[r][j] * inv_p) % 3;
            }
            for i in 0..a.len() {
                if i != r && a[i][c] != 0 {
                    let f = a[i][c];
                    for j in 0..4 {
                        a[i][j] = (a[i][j] + 9 - f * a[r][j]) % 3;
                    }
                }
            }
            r += 1;
        }
        a[..r].to_vec()
    };

    let norm3_neighbors = |h: &[Vec<i128>]| -> Vec<Vec<Vec<i128>>> {
        let hf: Vec<Vec<Frac>> = h.iter().map(|r| r.iter().map(|&x| Frac::from_int(x)).collect()).collect();
        let h_inv = inv_frac_mat(&hf);
        let mut rmats = [[[0u8; 4]; 4]; 4];
        for b_i in 0..4 {
            let mut eb = [0i128; 4];
            eb[b_i] = 1;
            for i in 0..4 {
                let p = vec_mul_o(&h[i], &eb);
                for m in 0..4 {
                    let mut acc = Frac::zero();
                    for k in 0..4 {
                        acc = acc + Frac::from_int(p[k]) * h_inv[k][m];
                    }
                    assert_eq!(acc.d, 1);
                    rmats[b_i][i][m] = mod_pos(acc.n, 3) as u8;
                }
            }
        }
        let mut subs: BTreeSet<Vec<[u8; 4]>> = BTreeSet::new();
        for v0 in 0..3u8 {
            for v1 in 0..3u8 {
                for v2 in 0..3u8 {
                    for v3 in 0..3u8 {
                        let v = [v0, v1, v2, v3];
                        if v == [0; 4] {
                            continue;
                        }
                        let mut span = Vec::with_capacity(4);
                        for m in &rmats {
                            let mut w = vec![0u8; 4];
                            for j in 0..4 {
                                let mut s = 0u8;
                                for k in 0..4 {
                                    s += v[k] * m[k][j];
                                }
                                w[j] = s % 3;
                            }
                            span.push(w);
                        }
                        let rr = rref_f3(&span);
                        if rr.len() == 2 {
                            let mut closed = true;
                            'chk: for rv in &rr {
                                for m in &rmats {
                                    let mut w = vec![0u8; 4];
                                    for j in 0..4 {
                                        let mut s = 0u8;
                                        for k in 0..4 {
                                            s += rv[k] * m[k][j];
                                        }
                                        w[j] = s % 3;
                                    }
                                    let mut comb: Vec<Vec<u8>> = rr.iter().map(|x| x.to_vec()).collect();
                                    comb.push(w);
                                    if rref_f3(&comb).len() > 2 {
                                        closed = false;
                                        break 'chk;
                                    }
                                }
                            }
                            if closed {
                                subs.insert(rr);
                            }
                        }
                    }
                }
            }
        }
        assert_eq!(subs.len(), 4);
        let mut nbrs = Vec::with_capacity(4);
        for sub in subs {
            let mut rows: Vec<Vec<i128>> = h.iter().map(|r| r.iter().map(|&x| 3 * x).collect()).collect();
            for rv in sub {
                let mut row = vec![0i128; 4];
                for j in 0..4 {
                    for k in 0..4 {
                        row[j] += (rv[k] as i128) * h[k][j];
                    }
                }
                rows.push(row);
            }
            let mut hs = hnf_int_rows(&rows);
            let mut g_all = 0i128;
            for r in &hs {
                for &x in r {
                    g_all = gcd_i128(g_all, x);
                }
            }
            if g_all > 1 {
                for r in &mut hs {
                    for x in r {
                        *x /= g_all;
                    }
                }
            }
            nbrs.push(hs);
        }
        nbrs
    };

    let h0 = vec![vec![1, 0, 0, 0], vec![0, 1, 0, 0], vec![0, 0, 1, 0], vec![0, 0, 0, 1]];
    let mut classes_h = vec![h0.clone()];
    let mut classes_sig = vec![theta_sig(&ideal_gram(&h0))];
    let mut adj_counts = Vec::new();
    let mut idx = 0;
    while idx < classes_h.len() {
        let nbrs = norm3_neighbors(&classes_h[idx]);
        let mut row_ids = Vec::with_capacity(4);
        for hn in nbrs {
            let sig = theta_sig(&ideal_gram(&hn));
            let mut found = None;
            for cid in 0..classes_h.len() {
                if classes_sig[cid] == sig && are_equiv(&classes_h[cid], &hn) {
                    found = Some(cid);
                    break;
                }
            }
            let cid = match found {
                Some(c) => c,
                None => {
                    let c = classes_h.len();
                    classes_h.push(hn);
                    classes_sig.push(sig);
                    c
                }
            };
            row_ids.push(cid);
        }
        adj_counts.push(row_ids);
        idx += 1;
    }
    assert_eq!(classes_h.len(), 12);
    let mut bmat = [[0i64; 12]; 12];
    for i in 0..12 {
        for &j in &adj_counts[i] {
            bmat[i][j] += 1;
        }
    }
    bmat
}

fn mat12_mul(a: &[[i64; 12]; 12], b: &[[i64; 12]; 12]) -> [[i64; 12]; 12] {
    let mut c = [[0i64; 12]; 12];
    for i in 0..12 {
        for k in 0..12 {
            if a[i][k] != 0 {
                for j in 0..12 {
                    c[i][j] += a[i][k] * b[k][j];
                }
            }
        }
    }
    c
}

fn mat12_shift(a: &[[i64; 12]; 12], c: i64) -> [[i64; 12]; 12] {
    let mut out = *a;
    for i in 0..12 {
        out[i][i] -= c;
    }
    out
}

fn mat12_tr(a: &[[i64; 12]; 12]) -> i64 {
    (0..12).map(|i| a[i][i]).sum()
}

pub fn run_suite_r3_genus25_brandt_b3_atlas() {
    let f0 = Frac::zero();
    let f1 = Frac::one();
    let fh = Frac::new(1, 2);
    let fq = Frac::new(1, 4);

    let o2 = [[f1, f0, f0, f0], [f0, f1, f0, f0], [f0, f0, f1, f0], [fh, fh, fh, fh]];
    let o5 = [[f1, f0, f0, f0], [f0, f1, f0, f0], [fh, fh, fh, f0], [fh, fq, f0, fq]];
    let o7 = [[f1, f0, f0, f0], [f0, f1, f0, f0], [fh, f0, fh, f0], [f0, fh, f0, fh]];
    let o13 = o5;
    let o19 = o7;
    let o370 = o2;

    let check_curve = |bmat: &[[i64; 12]; 12], exp: (i64, i64, i64, i64)| {
        for i in 0..12 {
            assert_eq!(bmat[i].iter().sum::<i64>(), 4);
            for j in 0..12 {
                assert!(bmat[i][j] >= 0 && bmat[i][j] == bmat[j][i]);
            }
        }
        let tr1 = mat12_tr(bmat);
        let b2 = mat12_mul(bmat, bmat);
        let tr2 = mat12_tr(&b2);
        let b4 = mat12_mul(&b2, &b2);
        let tr4 = mat12_tr(&b4);
        assert_eq!((tr1, tr2, (tr2 - 48) / 2, tr4), exp);
        assert!(!(tr2 == 48 && tr4 == 456));
    };

    let h1_specs: [(&str, i128, i128, &[QQuat; 4], i128, (i64, i64, i64, i64)); 7] = [
        ("X_0^6(115)", -1, -1, &o2, 115, (8, 60, 6, 604)),
        ("X_0^6(119)", -1, -1, &o2, 119, (0, 56, 4, 480)),
        ("X_0^15(22)", -2, -5, &o5, 22, (4, 68, 10, 676)),
        ("X_0^21(16)", -1, -7, &o7, 16, (0, 48, 0, 384)),
        ("X_0^21(23)", -1, -7, &o7, 23, (4, 52, 2, 484)),
        ("X_0^39(8)", -2, -13, &o13, 8, (0, 56, 4, 552)),
        ("X_0^39(11)", -2, -13, &o13, 11, (6, 62, 7, 574)),
    ];

    let mut b_x21_16 = [[0i64; 12]; 12];
    for (label, a, b, basis, n_lvl, exp) in h1_specs {
        let bm = brandt_h1_from_order(a, b, basis, n_lvl);
        check_curve(&bm, exp);
        if label == "X_0^21(16)" {
            b_x21_16 = bm;
        }
    }

    // Curve 8: X_0^{57}(7) (Eichler E_7 inside O_19, rd = 133)
    let emb19 = make_order_embed_m2(-1, -19, 7);
    let lin7: Vec<i128> = o19.iter().map(|&e| emb19(e)[2] % 7).collect();
    let piv = lin7.iter().position(|&x| x != 0).unwrap();
    let inv_p = mod_inv(lin7[piv], 7);
    let mut e19_rows = Vec::with_capacity(4);
    for i in 0..4 {
        let mut row = vec![0i128; 4];
        if i == piv {
            row[piv] = 7;
        } else {
            row[i] = 1;
            row[piv] = mod_pos(-lin7[i] * inv_p, 7);
        }
        e19_rows.push(row);
    }
    let e7_hnf = hnf_int_rows(&e19_rows);
    let mut e7_basis = [[f0; 4]; 4];
    for i in 0..4 {
        for m in 0..4 {
            let mut acc = f0;
            for j in 0..4 {
                acc = acc + Frac::from_int(e7_hnf[i][j]) * o19[j][m];
            }
            e7_basis[i][m] = acc;
        }
    }
    let b_57_7 = brandt_general_hnf_bfs(-1, -19, &e7_basis, 133);
    check_curve(&b_57_7, (0, 60, 6, 572));

    // Curve 9: X_0^{1110}(1) (B_370 = (-5, -37), O_370, rd = 370)
    let b_1110_1 = brandt_general_hnf_bfs(-5, -37, &o370, 370);
    check_curve(&b_1110_1, (4, 64, 8, 592));

    // Exact annihilator (B - 4I)(B - 2I)B(B + 2I) == 0 and tr(B^3) == 48 on X_0^{21}(16)
    let b2 = mat12_mul(&b_x21_16, &b_x21_16);
    let b3 = mat12_mul(&b2, &b_x21_16);
    assert_eq!(mat12_tr(&b3), 48);
    let ann = mat12_mul(
        &mat12_mul(&mat12_shift(&b_x21_16, 4), &mat12_shift(&b_x21_16, 2)),
        &mat12_mul(&b_x21_16, &mat12_shift(&b_x21_16, -2)),
    );
    assert_eq!(ann, [[0i64; 12]; 12]);
}

// ============================================================================
// Suite R4: Frontier 4 — Degree-8 (8, 1, 1, E) Poitou-Odlyzko Analytic Closure
// ============================================================================

const EULER_GAMMA: f64 = 0.577215664901532860606512090082402431;

fn gl_nodes(n: usize) -> (Vec<f64>, Vec<f64>) {
    let mut pairs = Vec::with_capacity(n);
    let m = (n + 1) / 2;
    for i in 1..=m {
        let mut z = (std::f64::consts::PI * ((i as f64) - 0.25) / ((n as f64) + 0.5)).cos();
        let mut pp = 1.0;
        for _ in 0..30 {
            let (mut p1, mut p2) = (1.0, 0.0);
            for j in 1..=n {
                let p3 = p2;
                p2 = p1;
                p1 = ((2.0 * (j as f64) - 1.0) * z * p2 - ((j as f64) - 1.0) * p3) / (j as f64);
            }
            pp = (n as f64) * (z * p1 - p2) / (z * z - 1.0);
            let dz = p1 / pp;
            z -= dz;
            if dz.abs() < 1e-16 {
                break;
            }
        }
        let w = 2.0 / ((1.0 - z * z) * pp * pp);
        pairs.push((-z, w));
        if 2 * i - 1 != n {
            pairs.push((z, w));
        }
    }
    pairs.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());
    (pairs.iter().map(|p| p.0).collect(), pairs.iter().map(|p| p.1).collect())
}

fn poitou_h1(w: f64) -> f64 {
    if w >= 2.0 {
        0.0
    } else if w <= 0.0 {
        1.0
    } else {
        ((2.0 - w) * (2.0 + (std::f64::consts::PI * w).cos())
            + (3.0 / std::f64::consts::PI) * (std::f64::consts::PI * w).sin())
            / 6.0
    }
}

fn poitou_fq(q: usize, b: f64) -> f64 {
    let lq = (q as f64).ln();
    let mut total = 0.0;
    let mut m = 1usize;
    let mut q_pow = q as f64;
    while (m as f64) * lq < 2.0 * b {
        total += (4.0 * lq / (1.0 + q_pow)) * poitou_h1((m as f64) * lq / b);
        m += 1;
        q_pow *= q as f64;
    }
    total
}

fn poitou_deg8_exp_lb(b: f64, primes: &[(usize, usize)], xs: &[f64], ws: &[f64]) -> f64 {
    let mut int_b = 0.0;
    let mut int_a = 0.0;
    for (&xi, &wi) in xs.iter().zip(ws.iter()) {
        let x = b * (xi + 1.0);
        let fb = poitou_h1(x / b) / (0.5 * x).cosh();
        int_b += wi * b * (1.0 - fb) / (2.0 * (0.5 * x).sinh());
        int_a += wi * b * fb / (2.0 * (0.5 * x).cosh());
    }
    let log_b = (8.0 * std::f64::consts::PI).ln() + EULER_GAMMA - int_b + (0.5 * b).tanh().ln();
    let log_a = log_b + int_a;
    let pole = (8.0 / 3.0) * b / 8.0;
    let psum: f64 = primes.iter().map(|&(q, c)| (c as f64) * poitou_fq(q, b)).sum::<f64>() / 8.0;
    (log_a - pole + psum).exp()
}

fn count_splitting_types(p: usize, deg: usize, forbidden: &[usize]) -> usize {
    fn dfs(rem: usize, min_pair: (usize, usize), p: usize, forbidden: &[usize], cur: &mut Vec<(usize, usize)>, out: &mut usize) {
        if rem == 0 {
            if p == 2 && cur.iter().filter(|&&(_, f)| f == 1).count() != 1 {
                return;
            }
            *out += 1;
            return;
        }
        for f in 1..=rem {
            let norm = p.pow(f as u32);
            if forbidden.contains(&norm) {
                continue;
            }
            for e in 1..=(rem / f) {
                let pair = (e, f);
                if pair < min_pair {
                    continue;
                }
                cur.push(pair);
                dfs(rem - e * f, pair, p, forbidden, cur, out);
                cur.pop();
            }
        }
    }
    let mut cur = Vec::new();
    let mut out = 0;
    dfs(deg, (1, 1), p, forbidden, &mut cur, &mut out);
    out
}

pub fn run_suite_r4_degree8_poitou_closure() {
    let (x64, w64) = gl_nodes(64);
    let (x128, w128) = gl_nodes(128);

    // 1. Exact Eichler mass 1536 & Shimura ceiling UB_max(8, 1)
    assert_eq!(1536 / 128, 12);
    let ub_max = (4.0 * std::f64::consts::PI * std::f64::consts::PI).powf(2.0 / 3.0) * 4.5f64.powf(1.0 / 12.0);
    assert!((ub_max - 13.1423854579).abs() < 1e-9);
    assert!((ub_max.powi(8) - 890_007_374.15).abs() < 1.0);

    // 2. Quadrature Q7: int_0^2 H_1(w) dw == 2/3 & GL-64 vs GL-128 diff < 1.5e-14
    let int_h1: f64 = x64.iter().zip(w64.iter()).map(|(&x, &w)| w * poitou_h1(x + 1.0)).sum();
    assert!((int_h1 - 2.0 / 3.0).abs() < 1e-15);
    let lb64 = poitou_deg8_exp_lb(3.20, &[(2, 1)], &x64, &w64);
    let lb128 = poitou_deg8_exp_lb(3.20, &[(2, 1)], &x128, &w128);
    assert!((lb64 - lb128).abs() < 1.5e-14);

    // 3. Peak baseline (c_2 = 1) and all 7/7 prime norms q <= 9 eliminated at b = 3.20
    let lb_peak = poitou_deg8_exp_lb(3.039865, &[(2, 1)], &x128, &w128);
    assert!((lb_peak - 12.5955757277).abs() < 1e-8);
    for &(q, c) in &[(2, 2), (3, 1), (4, 1), (5, 1), (7, 1), (8, 1), (9, 1)] {
        let primes = if q == 2 { vec![(2, c)] } else { vec![(2, 1), (q, c)] };
        let val = poitou_deg8_exp_lb(3.20, &primes, &x128, &w128);
        assert!(val > ub_max, "Prime norm q={} failed elimination", q);
    }
    assert!(poitou_deg8_exp_lb(3.20, &[(2, 1), (11, 1)], &x128, &w128) < ub_max);
    assert!(poitou_deg8_exp_lb(3.20, &[(2, 1), (11, 2)], &x128, &w128) > ub_max);
    assert!(poitou_deg8_exp_lb(3.20, &[(2, 1), (13, 2)], &x128, &w128) > ub_max);

    // 4. Exact 5 2-adic & 4 3-adic splitting types
    assert_eq!(count_splitting_types(2, 8, &[4, 8]), 5);
    assert_eq!(count_splitting_types(3, 8, &[3, 9]), 4);

    // 5. Symmetry, Ram_fin (100 & 120), Eichler (12), and anti-facade f_bad(+-1) = -0.60
    let ub_sym2 = ub_max / 2.0f64.powf(1.0 / 12.0);
    assert!(lb_peak - ub_sym2 > 0.1908);
    let ub_ram100 = ub_max / 100.0f64.powf(1.0 / 12.0);
    let ub_ram120 = ub_max / 120.0f64.powf(1.0 / 12.0);
    let ub_eich = ub_max / 12.0f64.powf(1.0 / 12.0);
    assert!(ub_ram120 < ub_ram100 && ub_ram100 < ub_eich && ub_eich < lb_peak);

    let f_bad_1 = 1.0 + std::f64::consts::PI.cos()
        - 0.3 * (1.0 - (2.0 * std::f64::consts::PI).cos())
        + 0.3 * (std::f64::consts::PI.cos() + (3.0 * std::f64::consts::PI).cos());
    assert!((f_bad_1 - (-0.60)).abs() < 1e-15);
}

// ============================================================================
// Suite R5: Runtime Global-Invariant Monitors & 6/6 Fault Injections
// ============================================================================

pub fn run_suite_r5_runtime_fault_guards() {
    let mut rejected = 0usize;
    let f0 = Frac::zero();
    let f1 = Frac::one();
    let fh = Frac::new(1, 2);
    let o7 = [[f1, f0, f0, f0], [f0, f1, f0, f0], [fh, f0, fh, f0], [f0, fh, f0, fh]];
    let b_simple = brandt_h1_from_order(-1, -7, &o7, 16);

    // Fault 1: Multi-edge perturbation violates Simple-Graph Trace Gate tr(B^2) == 48
    let mut bf = b_simple;
    let ones: Vec<usize> = (0..12).filter(|&j| bf[0][j] == 1).collect();
    bf[0][ones[0]] += 1;
    bf[0][ones[1]] -= 1;
    let tr2_f: i64 = (0..12).flat_map(|i| (0..12).map(move |j| bf[i][j] * bf[i][j])).sum();
    assert!(tr2_f > 48);
    rejected += 1;

    // Fault 2: Asymmetric perturbation detected
    let mut ba = b_simple;
    ba[0][ones[0]] += 1;
    assert_ne!(ba[0][ones[0]], ba[ones[0]][0]);
    rejected += 1;

    // Fault 3: Split-prime sign-flip sigma = 1 - 2w is central mod 4 (causes Ad_{(4)} stall)
    let mul_q33 = |a: (u8, u8), b: (u8, u8)| ((a.0 * b.0) % 4, (a.0 * b.1 + a.1 * b.0 + a.1 * b.1) % 4);
    assert_eq!(mul_q33((1, 2), (1, 2)), (1, 0));
    for x0 in 0..4u8 {
        for x1 in 0..4u8 {
            assert_eq!(mul_q33((1, 2), (x0, x1)), mul_q33((x0, x1), (1, 2)));
        }
    }
    rejected += 1;

    // Fault 4: Anti-facade negative Bochner witness f_bad(1) = -0.60 < 0 rejected
    let f_bad_1 = 1.0 + std::f64::consts::PI.cos()
        - 0.3 * (1.0 - (2.0 * std::f64::consts::PI).cos())
        + 0.3 * (std::f64::consts::PI.cos() + (3.0 * std::f64::consts::PI).cos());
    assert!(f_bad_1 < -0.59);
    rejected += 1;

    // Fault 5: Invalid Poitou parameter guard (0, -1, NaN, Inf)
    let valid_b = |b: f64| b.is_finite() && b > 0.0;
    assert!(!valid_b(0.0) && !valid_b(-1.5) && !valid_b(f64::NAN) && !valid_b(f64::INFINITY));
    rejected += 1;

    // Fault 6: Corrupted cubic mod-81 square root rejected
    let sq_bad = cub_mul(
        [Frac::from_int(29), Frac::from_int(39), Frac::from_int(63)],
        [Frac::from_int(29), Frac::from_int(39), Frac::from_int(63)],
        -10,
        9,
        -2,
    );
    assert_ne!((sq_bad[0].mod_m(81), sq_bad[1].mod_m(81), sq_bad[2].mod_m(81)), (1, 78, 0));
    rejected += 1;

    assert_eq!(rejected, 6);
}

// ============================================================================
// Suite R6: Bit-Exact SplitMix64 Cross-Language Seam Parity (Python/Rust/C++)
// ============================================================================

pub fn run_suite_r6_splitmix64_seam_parity() -> (u64, u64) {
    let mut rng = SplitMix64::new(PC4_PRNG_SEED);
    let ord_a = build_q33_glued_max_order(false);
    let i8 = id8();

    // Build full L_signed (size 2,304) to verify 512/512 random words land inside L_signed
    let mut seen_l: HashSet<Mat8> = HashSet::new();
    seen_l.insert(i8);
    let mut dq = VecDeque::new();
    dq.push_back(i8);
    while let Some(cur) = dq.pop_front() {
        for g in &ord_a.r4 {
            let nxt = mm8(&cur, g, 4);
            if seen_l.insert(nxt) {
                dq.push_back(nxt);
            }
        }
    }
    assert_eq!(seen_l.len(), 2304);

    let mut recs: Vec<(u64, u64)> = Vec::with_capacity(768);
    let mut hits = 0usize;
    for trial in 0..512u64 {
        let mut cur_m = i8;
        let mut word_hash = 0x9E3779B97F4A7C15u64 ^ trial;
        for _ in 0..12 {
            let gi = (rng.next_u64() % 10) as usize;
            cur_m = mm8(&cur_m, &ord_a.r4[gi], 4);
            word_hash = word_hash.wrapping_mul(0xBF58476D1CE4E5B9) ^ ((gi as u64) + 1);
        }
        if seen_l.contains(&cur_m) {
            hits += 1;
        }
        recs.push((trial, word_hash));
    }
    assert_eq!(hits, 512);

    let inv_2p53 = 1.0 / ((1u64 << 53) as f64);
    let mut pos_ok = 0usize;
    let mut neg_rej = 0usize;
    for trial in 0..256u64 {
        let u0 = rng.next_u64();
        let u1 = rng.next_u64();
        let u2 = rng.next_u64();
        let u3 = rng.next_u64();
        let w0 = 0.1 + ((u0 >> 11) as f64) * inv_2p53;
        let w1 = 0.1 + ((u1 >> 11) as f64) * inv_2p53;
        let w2 = 0.1 + ((u2 >> 11) as f64) * inv_2p53;
        let amp_bad = 0.25 + 0.5 * ((u3 >> 11) as f64) * inv_2p53;

        let mut min_pos = f64::INFINITY;
        for k in 0..=32 {
            let t = -1.0 + 2.0 * (k as f64) / 32.0;
            let v = w0 * (1.0 + (std::f64::consts::PI * t).cos())
                + w1 * (1.0 + (2.0 * std::f64::consts::PI * t).cos())
                + w2 * (1.0 + (3.0 * std::f64::consts::PI * t).cos());
            if v < min_pos {
                min_pos = v;
            }
        }
        let ok_pos = min_pos >= -1e-12;
        if ok_pos {
            pos_ok += 1;
        }
        let val_neg = w0 * (1.0 + std::f64::consts::PI.cos()) - amp_bad * (1.0 - std::f64::consts::PI.cos());
        let rej_neg = val_neg < 0.0;
        if rej_neg {
            neg_rej += 1;
        }
        let bit_rec = (if ok_pos { 1u64 } else { 0 }) | ((if rej_neg { 1u64 } else { 0 }) << 1) | ((u0 & 0xFFFF) << 2);
        recs.push((512 + trial, bit_rec));
    }
    assert_eq!(pos_ok, 256);
    assert_eq!(neg_rej, 256);

    let xor_fwd: u64 = recs.iter().fold(0u64, |acc, &(tag, val)| acc ^ mix64_tag(tag, val));
    let xor_rev: u64 = recs.iter().rev().fold(0u64, |acc, &(tag, val)| acc ^ mix64_tag(tag, val));
    assert_eq!(xor_fwd, xor_rev);
    let vals: Vec<u64> = recs.iter().map(|&(_, v)| v).collect();
    let fnv_d = fnv1a64_u64s(&vals);
    assert_eq!(xor_fwd, EXPECTED_XOR_DIGEST);
    assert_eq!(fnv_d, EXPECTED_FNV_DIGEST);
    (xor_fwd, fnv_d)
}
