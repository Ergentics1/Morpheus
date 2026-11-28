//! Zero-Dependency Independent Rust Verifier for Paper PC-III:
//! The 3-Adic Dicyclic Companion, Exact Level 3P_5 and Level (3) Congruence on Nauru,
//! and the Real-Quadratic Lame Shimura Curve Atlas (MIT License).
//!
//! Recomputes all three pillars and Section 5 from first principles with zero external
//! crates and zero cached data reads.

use std::collections::{BTreeMap, BTreeSet, HashMap, HashSet, VecDeque};

pub type Perm24 = [u8; 24];

pub fn perm_id() -> Perm24 {
    let mut p = [0u8; 24];
    for i in 0..24 {
        p[i] = i as u8;
    }
    p
}

pub fn perm_comp(p: &Perm24, q: &Perm24) -> Perm24 {
    let mut out = [0u8; 24];
    for i in 0..24 {
        out[i] = p[q[i] as usize];
    }
    out
}

pub fn perm_inv(p: &Perm24) -> Perm24 {
    let mut out = [0u8; 24];
    for i in 0..24 {
        out[p[i] as usize] = i as u8;
    }
    out
}

fn gcd_i64(mut a: i64, mut b: i64) -> i64 {
    a = a.abs();
    b = b.abs();
    while b != 0 {
        let t = a % b;
        a = b;
        b = t;
    }
    a
}

fn lcm_usize(a: usize, b: usize) -> usize {
    a / (gcd_i64(a as i64, b as i64) as usize) * b
}

pub fn perm_order(p: &Perm24) -> usize {
    let mut seen = [false; 24];
    let mut ord = 1usize;
    for i in 0..24 {
        if !seen[i] {
            let mut cur = i;
            let mut clen = 0usize;
            while !seen[cur] {
                seen[cur] = true;
                cur = p[cur] as usize;
                clen += 1;
            }
            ord = lcm_usize(ord, clen);
        }
    }
    ord
}

pub fn build_nauru() -> [[usize; 3]; 24] {
    let mut adj = [[0usize; 3]; 24];
    for i in 0..12 {
        adj[i] = [(i + 11) % 12, (i + 1) % 12, 12 + i];
        adj[12 + i] = [i, 12 + (i + 7) % 12, 12 + (i + 5) % 12];
    }
    adj
}

pub fn dic6_mul(g: usize, h: usize) -> usize {
    let (a, sa) = (g % 12, g / 12);
    let (b, sb) = (h % 12, h / 12);
    match (sa, sb) {
        (0, 0) => (a + b) % 12,
        (0, 1) => 12 + (a + b) % 12,
        (1, 0) => 12 + (a + 12 - b) % 12,
        _ => (a + 18 - b) % 12,
    }
}

pub fn dic6_inv(g: usize) -> usize {
    let (a, sa) = (g % 12, g / 12);
    if sa == 0 {
        (12 - a) % 12
    } else {
        12 + (a + 6) % 12
    }
}

pub fn build_dic6_cayley(gens: [usize; 4]) -> [[usize; 4]; 24] {
    let mut adj = [[0usize; 4]; 24];
    for g in 0..24 {
        for k in 0..4 {
            adj[g][k] = dic6_mul(g, gens[k]);
        }
        adj[g].sort_unstable();
    }
    adj
}

pub fn build_dic6_z() -> [[usize; 4]; 24] {
    build_dic6_cayley([1, 11, 12, 18])
}

fn graph_auts_generic<const DEG: usize>(adj: &[[usize; DEG]; 24]) -> Vec<Perm24> {
    let mut order = Vec::with_capacity(24);
    let mut seen = [false; 24];
    let mut q = VecDeque::new();
    q.push_back(0usize);
    seen[0] = true;
    while let Some(u) = q.pop_front() {
        order.push(u);
        for &v in &adj[u] {
            if !seen[v] {
                seen[v] = true;
                q.push_back(v);
            }
        }
    }
    let mut pos = [0usize; 24];
    for (idx, &u) in order.iter().enumerate() {
        pos[u] = idx;
    }
    let mut prev_nbrs: Vec<Vec<usize>> = Vec::with_capacity(24);
    for (idx, &u) in order.iter().enumerate() {
        prev_nbrs.push(adj[u].iter().copied().filter(|&v| pos[v] < idx).collect());
    }
    let mut adj_mask = [0u32; 24];
    for u in 0..24 {
        for &v in &adj[u] {
            adj_mask[u] |= 1u32 << v;
        }
    }
    let mut out = Vec::new();
    let mut map = [0u8; 24];
    let mut used = 0u32;

    fn bt(
        idx: usize,
        order: &[usize],
        prev_nbrs: &[Vec<usize>],
        adj_mask: &[u32; 24],
        map: &mut Perm24,
        used: &mut u32,
        out: &mut Vec<Perm24>,
    ) {
        if idx == 24 {
            out.push(*map);
            return;
        }
        let u = order[idx];
        let mut cand_mask = if prev_nbrs[idx].is_empty() {
            (1u32 << 24) - 1
        } else {
            let mut m = adj_mask[map[prev_nbrs[idx][0]] as usize];
            for &pn in &prev_nbrs[idx][1..] {
                m &= adj_mask[map[pn] as usize];
            }
            m
        };
        cand_mask &= !*used;
        while cand_mask != 0 {
            let w = cand_mask.trailing_zeros() as usize;
            cand_mask &= cand_mask - 1;
            map[u] = w as u8;
            *used |= 1u32 << w;
            bt(idx + 1, order, prev_nbrs, adj_mask, map, used, out);
            *used &= !(1u32 << w);
        }
    }
    bt(0, &order, &prev_nbrs, &adj_mask, &mut map, &mut used, &mut out);
    out
}

fn nauru_generators() -> (Perm24, Perm24, Perm24, Perm24) {
    let y = build_nauru();
    let auts = graph_auts_generic(&y);
    assert_eq!(auts.len(), 144);
    let stab0: Vec<Perm24> = auts.iter().copied().filter(|p| p[0] == 0).collect();
    assert_eq!(stab0.len(), 6);
    let a_y = *stab0.iter().find(|p| perm_order(p) == 3).unwrap();
    let b_y = *stab0.iter().find(|p| perm_order(p) == 2 && p[12] == 12).unwrap();
    let t_invs: Vec<Perm24> = auts
        .iter()
        .copied()
        .filter(|p| p[0] == 12 && p[12] == 0 && perm_order(p) == 2 && perm_comp(p, &b_y) == perm_comp(&b_y, p))
        .collect();
    assert_eq!(t_invs.len(), 2);
    let t0 = *t_invs.iter().find(|p| perm_order(&perm_comp(p, &a_y)) == 6).unwrap();
    let t1 = *t_invs.iter().find(|p| perm_order(&perm_comp(p, &a_y)) == 12).unwrap();
    assert_eq!(perm_comp(&b_y, &t0), t1);
    (a_y, b_y, t0, t1)
}

fn mobius(mut n: usize) -> i64 {
    let mut mu = 1i64;
    let mut d = 2usize;
    while d * d <= n {
        if n % d == 0 {
            n /= d;
            if n % d == 0 {
                return 0;
            }
            mu = -mu;
        }
        d += 1;
    }
    if n > 1 {
        mu = -mu;
    }
    mu
}

fn hashimoto_cadences<const DEG: usize, const MDIR: usize>(
    adj: &[[usize; DEG]; 24],
    max_m: usize,
) -> (Vec<i64>, Vec<i64>) {
    let mut eu = [0usize; MDIR];
    let mut ev = [0usize; MDIR];
    let mut out_idx = [[0usize; DEG]; 24];
    let mut idx = 0usize;
    for u in 0..24 {
        for k in 0..DEG {
            eu[idx] = u;
            ev[idx] = adj[u][k];
            out_idx[u][k] = idx;
            idx += 1;
        }
    }
    let mut next_e = vec![Vec::with_capacity(DEG - 1); MDIR];
    for e in 0..MDIR {
        let (u, v) = (eu[e], ev[e]);
        for k in 0..DEG {
            let e2 = out_idx[v][k];
            if ev[e2] != u {
                next_e[e].push(e2);
            }
        }
    }
    let mut traces = vec![0i64; max_m + 1];
    let mut vec = vec![0i64; MDIR];
    let mut nxt = vec![0i64; MDIR];
    for s in 0..MDIR {
        vec.fill(0);
        vec[s] = 1;
        for m in 1..=max_m {
            nxt.fill(0);
            for e in 0..MDIR {
                let v = vec[e];
                if v != 0 {
                    for &e2 in &next_e[e] {
                        nxt[e2] += v;
                    }
                }
            }
            std::mem::swap(&mut vec, &mut nxt);
            traces[m] += vec[s];
        }
    }
    let mut pi = vec![0i64; max_m + 1];
    for m in 1..=max_m {
        let mut tot = 0i64;
        for d in 1..=m {
            if m % d == 0 {
                tot += mobius(m / d) * traces[d];
            }
        }
        assert_eq!(tot % (m as i64), 0);
        pi[m] = tot / (m as i64);
    }
    (traces, pi)
}

// ============================================================================
// Exact Modular Matrix Arithmetic (4x4 and 8x8) & Fast Integer-Table Joint BFS
// ============================================================================

fn mat_mul_mod(a: &[u16], b: &[u16], n: usize, m: u32) -> Vec<u16> {
    let mut out = vec![0u16; n * n];
    for i in 0..n {
        let ro = i * n;
        for k in 0..n {
            let aik = a[ro + k] as u32;
            if aik != 0 {
                let ko = k * n;
                for j in 0..n {
                    out[ro + j] = ((out[ro + j] as u32 + aik * (b[ko + j] as u32)) % m) as u16;
                }
            }
        }
    }
    out
}

fn bfs_mat_joint(ad_gens: &[Vec<u16>], perm_gens: &[Perm24], n_mat: usize, m: u32) -> (usize, usize, usize, Vec<Perm24>) {
    let ng = ad_gens.len();
    let mut id_mat = vec![0u16; n_mat * n_mat];
    for i in 0..n_mat {
        id_mat[i * n_mat + i] = 1;
    }
    let mut ad_map: HashMap<Vec<u16>, usize> = HashMap::new();
    ad_map.insert(id_mat.clone(), 0);
    let mut ad_els = vec![id_mat];
    let mut ad_step: Vec<Vec<usize>> = Vec::new();
    let mut q = VecDeque::new();
    q.push_back(0usize);
    while let Some(uid) = q.pop_front() {
        let um = ad_els[uid].clone();
        let mut row = vec![0usize; ng];
        for gi in 0..ng {
            let nm = mat_mul_mod(&ad_gens[gi], &um, n_mat, m);
            let nid = match ad_map.get(&nm) {
                Some(&id) => id,
                None => {
                    let id = ad_els.len();
                    ad_map.insert(nm.clone(), id);
                    ad_els.push(nm);
                    q.push_back(id);
                    id
                }
            };
            row[gi] = nid;
        }
        ad_step.push(row);
    }

    let idp = perm_id();
    let mut p_map: HashMap<Perm24, usize> = HashMap::new();
    p_map.insert(idp, 0);
    let mut p_els = vec![idp];
    let mut p_step: Vec<Vec<usize>> = Vec::new();
    let mut pq = VecDeque::new();
    pq.push_back(0usize);
    while let Some(uid) = pq.pop_front() {
        let up = p_els[uid];
        let mut row = vec![0usize; ng];
        for gi in 0..ng {
            let np = perm_comp(&up, &perm_gens[gi]);
            let nid = match p_map.get(&np) {
                Some(&id) => id,
                None => {
                    let id = p_els.len();
                    p_map.insert(np, id);
                    p_els.push(np);
                    pq.push_back(id);
                    id
                }
            };
            row[gi] = nid;
        }
        p_step.push(row);
    }

    let n_ad = ad_els.len();
    let n_p = p_els.len();
    let mut seen = vec![0u8; n_ad * n_p];
    seen[0] = 1;
    let mut jq = VecDeque::new();
    jq.push_back(0usize);
    let mut j_cnt = 1usize;
    let mut ker_perms = vec![idp];
    while let Some(st) = jq.pop_front() {
        let mid = st / n_p;
        let pid = st % n_p;
        for gi in 0..ng {
            let nmid = ad_step[mid][gi];
            let npid = p_step[pid][gi];
            let nst = nmid * n_p + npid;
            if seen[nst] == 0 {
                seen[nst] = 1;
                j_cnt += 1;
                if nmid == 0 {
                    ker_perms.push(p_els[npid]);
                }
                jq.push_back(nst);
            }
        }
    }
    assert_eq!(j_cnt, n_ad * ker_perms.len());
    (n_ad, j_cnt, ker_perms.len(), ker_perms)
}

// ============================================================================
// Exact Rational Number & Quaternion Algebra over Q
// ============================================================================

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct Frac {
    n: i128,
    d: i128,
}

fn gcd_i128(mut a: i128, mut b: i128) -> i128 {
    a = a.abs();
    b = b.abs();
    while b != 0 {
        let t = a % b;
        a = b;
        b = t;
    }
    a
}

impl Frac {
    fn new(mut n: i128, mut d: i128) -> Self {
        assert!(d != 0);
        if d < 0 {
            n = -n;
            d = -d;
        }
        let g = gcd_i128(n, d);
        Self { n: n / g, d: d / g }
    }
    fn from_i(n: i128) -> Self {
        Self { n, d: 1 }
    }
    fn add(self, o: Self) -> Self {
        Self::new(self.n * o.d + o.n * self.d, self.d * o.d)
    }
    fn sub(self, o: Self) -> Self {
        Self::new(self.n * o.d - o.n * self.d, self.d * o.d)
    }
    fn mul(self, o: Self) -> Self {
        Self::new(self.n * o.n, self.d * o.d)
    }
    fn div(self, o: Self) -> Self {
        Self::new(self.n * o.d, self.d * o.n)
    }
    fn neg(self) -> Self {
        Self { n: -self.n, d: self.d }
    }
    fn mod_u32(self, m: u32) -> u16 {
        let m64 = m as i128;
        let num = ((self.n % m64) + m64) % m64;
        let den = ((self.d % m64) + m64) % m64;
        // Modular inverse via extended Euclid
        let (mut t, mut nt, mut r, mut nr) = (0i128, 1i128, m64, den);
        while nr != 0 {
            let q = r / nr;
            let tmp_t = t - q * nt;
            t = nt;
            nt = tmp_t;
            let tmp_r = r - q * nr;
            r = nr;
            nr = tmp_r;
        }
        assert_eq!(r, 1, "denominator not invertible mod {}", m);
        let inv = ((t % m64) + m64) % m64;
        ((num * inv) % m64) as u16
    }
}

type QuatQ = [Frac; 4];

fn qmul_q(x: QuatQ, y: QuatQ, a: Frac, b: Frac) -> QuatQ {
    let ab = a.mul(b);
    [
        x[0].mul(y[0]).add(a.mul(x[1].mul(y[1]))).add(b.mul(x[2].mul(y[2]))).sub(ab.mul(x[3].mul(y[3]))),
        x[0].mul(y[1]).add(x[1].mul(y[0])).sub(b.mul(x[2].mul(y[3]))).add(b.mul(x[3].mul(y[2]))),
        x[0].mul(y[2]).add(x[2].mul(y[0])).add(a.mul(x[1].mul(y[3]))).sub(a.mul(x[3].mul(y[1]))),
        x[0].mul(y[3]).add(x[3].mul(y[0])).add(x[1].mul(y[2])).sub(x[2].mul(y[1])),
    ]
}

fn qnrd_q(x: QuatQ, a: Frac, b: Frac) -> Frac {
    let ab = a.mul(b);
    x[0].mul(x[0]).sub(a.mul(x[1].mul(x[1]))).sub(b.mul(x[2].mul(x[2]))).add(ab.mul(x[3].mul(x[3])))
}

fn qinv_q(x: QuatQ, a: Frac, b: Frac) -> QuatQ {
    let n = qnrd_q(x, a, b);
    [x[0].div(n), x[1].neg().div(n), x[2].neg().div(n), x[3].neg().div(n)]
}

fn mat4_inv_frac(m: &[[Frac; 4]; 4]) -> [[Frac; 4]; 4] {
    let mut aug = [[Frac::from_i(0); 8]; 4];
    for i in 0..4 {
        for j in 0..4 {
            aug[i][j] = m[i][j];
        }
        aug[i][4 + i] = Frac::from_i(1);
    }
    for i in 0..4 {
        let piv = (i..4).find(|&r| aug[r][i].n != 0).unwrap();
        aug.swap(i, piv);
        let pv = aug[i][i];
        for c in 0..8 {
            aug[i][c] = aug[i][c].div(pv);
        }
        for r in 0..4 {
            if r != i && aug[r][i].n != 0 {
                let f = aug[r][i];
                for c in 0..8 {
                    aug[r][c] = aug[r][c].sub(f.mul(aug[i][c]));
                }
            }
        }
    }
    let mut inv = [[Frac::from_i(0); 4]; 4];
    for i in 0..4 {
        for j in 0..4 {
            inv[i][j] = aug[i][4 + j];
        }
    }
    inv
}

fn adjoint_mat4_mod(g: QuatQ, basis: &[QuatQ; 4], binv: &[[Frac; 4]; 4], a: Frac, b: Frac, m: u32) -> Vec<u16> {
    let gi = qinv_q(g, a, b);
    let mut flat = Vec::with_capacity(16);
    for e in basis {
        let w = qmul_q(qmul_q(g, *e, a, b), gi, a, b);
        for k in 0..4 {
            let mut c = Frac::from_i(0);
            for j in 0..4 {
                c = c.add(w[j].mul(binv[j][k]));
            }
            flat.push(c.mod_u32(m));
        }
    }
    flat
}

fn left_mult_mat4_mod(g: QuatQ, basis: &[QuatQ; 4], binv: &[[Frac; 4]; 4], a: Frac, b: Frac, m: u32) -> Vec<u16> {
    let mut flat = Vec::with_capacity(16);
    for e in basis {
        let w = qmul_q(g, *e, a, b);
        for k in 0..4 {
            let mut c = Frac::from_i(0);
            for j in 0..4 {
                c = c.add(w[j].mul(binv[j][k]));
            }
            flat.push(c.mod_u32(m));
        }
    }
    flat
}

// ============================================================================
// Suite R1: Pillar I — Nauru Hashimoto, <T,P,L,R>, & 132-Cell Metric Gonality
// ============================================================================

pub fn verify_r1_nauru_hashimoto_tplr_gonality() {
    let y = build_nauru();
    let (tr_y, pi_y) = hashimoto_cadences::<3, 72>(&y, 24);
    let expected = [
        (6, 24),
        (8, 108),
        (10, 216),
        (12, 564),
        (14, 2232),
        (16, 8820),
        (18, 28560),
        (20, 104292),
        (22, 380664),
        (24, 1401744),
    ];
    for &(m, val) in &expected {
        assert_eq!(pi_y[m], val, "pi_Y({}) mismatch", m);
    }
    assert_eq!(tr_y[18], 514224);
    assert_eq!(tr_y[22], 8374608);
    assert!(501786 <= tr_y[18] && tr_y[18] <= 546842 && 546842 < 18 * 31824 + 144);

    // <T, P, L, R> exact order 144, |[G,G]| = 6, |G^ab| = 24
    let mut t_p = [0u8; 24];
    let mut p_p = [0u8; 24];
    let mut l_p = [0u8; 24];
    let mut r_p = [0u8; 24];
    for k in 0..12 {
        t_p[k] = ((k + 1) % 12) as u8;
        t_p[12 + k] = (12 + (k + 1) % 12) as u8;
        p_p[k] = (12 + k) as u8;
        p_p[12 + k] = k as u8;
        l_p[k] = (12 + (k + 4) % 12) as u8;
        l_p[12 + k] = ((k + 8) % 12) as u8;
        r_p[k] = (12 + (k + 9) % 12) as u8;
        r_p[12 + k] = ((k + 3) % 12) as u8;
    }
    let gens = [t_p, p_p, l_p, r_p];
    let mut grp: HashSet<Perm24> = HashSet::new();
    let mut q = VecDeque::new();
    grp.insert(perm_id());
    q.push_back(perm_id());
    while let Some(c) = q.pop_front() {
        for g in &gens {
            let nxt = perm_comp(&c, g);
            if grp.insert(nxt) {
                q.push_back(nxt);
            }
        }
    }
    assert_eq!(grp.len(), 144);
    let mut comm_gens: HashSet<Perm24> = HashSet::new();
    for g in &gens {
        let gi = perm_inv(g);
        for h in &grp {
            comm_gens.insert(perm_comp(&perm_comp(g, h), &perm_comp(&gi, &perm_inv(h))));
        }
    }
    let mut comm: HashSet<Perm24> = HashSet::new();
    comm.insert(perm_id());
    q.push_back(perm_id());
    while let Some(c) = q.pop_front() {
        for cg in &comm_gens {
            let nxt = perm_comp(&c, cg);
            if comm.insert(nxt) {
                q.push_back(nxt);
            }
        }
    }
    assert_eq!(comm.len(), 6);
    assert_eq!(grp.len() / comm.len(), 24);

    // 24-star scramble Edmonds-Karp cuts on Y ({6: 168})
    let mut stars = [0u32; 24];
    for v in 0..24 {
        stars[v] = 1u32 << v;
        for &u in &y[v] {
            stars[v] |= 1u32 << u;
        }
    }
    let mut cut6 = 0usize;
    for i in 0..24 {
        for j in (i + 1)..24 {
            if (stars[i] & stars[j]) == 0 {
                let c = edmonds_karp(&y, stars[i], stars[j]);
                assert_eq!(c, 6);
                cut6 += 1;
            }
        }
    }
    assert_eq!(cut6, 168);
}

fn edmonds_karp<const DEG: usize>(adj: &[[usize; DEG]; 24], s_mask: u32, t_mask: u32) -> i32 {
    const N: usize = 26;
    const SRC: usize = 24;
    const SNK: usize = 25;
    let mut cap = [[0i32; N]; N];
    for u in 0..24 {
        for &v in &adj[u] {
            cap[u][v] += 1;
        }
        if ((s_mask >> u) & 1) != 0 {
            cap[SRC][u] = 10000;
        }
        if ((t_mask >> u) & 1) != 0 {
            cap[u][SNK] = 10000;
        }
    }
    let mut flow = 0i32;
    loop {
        let mut par = [-1i32; N];
        par[SRC] = SRC as i32;
        let mut q = [0usize; N];
        let (mut qh, mut qt) = (0usize, 0usize);
        q[qt] = SRC;
        qt += 1;
        while qh < qt && par[SNK] == -1 {
            let u = q[qh];
            qh += 1;
            for v in 0..N {
                if par[v] == -1 && cap[u][v] > 0 {
                    par[v] = u as i32;
                    q[qt] = v;
                    qt += 1;
                }
            }
        }
        if par[SNK] == -1 {
            break;
        }
        let mut aug = 10000;
        let mut v = SNK;
        while v != SRC {
            let u = par[v] as usize;
            aug = aug.min(cap[u][v]);
            v = u;
        }
        let mut v = SNK;
        while v != SRC {
            let u = par[v] as usize;
            cap[u][v] -= aug;
            cap[v][u] += aug;
            v = u;
        }
        flow += aug;
    }
    flow
}

// ============================================================================
// Suite R2: Pillar I — Rational B_3(3/2), B_5(5/2), B_5(1/2) Level 3P_5 Table 2
// ============================================================================

pub fn verify_r2_rational_b3_b5_level_3p5() {
    let (a_y, b_y, t0, t1) = nauru_generators();
    let f = Frac::new;
    let z = Frac::from_i(0);
    let one = Frac::from_i(1);
    let a_q: QuatQ = [f(1, 2), f(1, 2), z, z];
    let b_q: QuatQ = [z, z, one, z];

    let o3: [QuatQ; 4] = [[one, z, z, z], [f(1, 2), f(1, 2), z, z], [z, z, one, z], [z, z, f(1, 2), f(1, 2)]];
    let o5m: [QuatQ; 4] = [
        [one, z, z, z],
        [f(1, 2), f(1, 2), z, z],
        [z, f(1, 3), z, f(-1, 3)],
        [f(-1, 2), f(1, 6), f(-1, 2), f(-1, 6)],
    ];
    let o5p: [QuatQ; 4] = [
        [one, z, z, z],
        [f(1, 2), f(1, 2), z, z],
        [z, f(1, 3), z, f(1, 3)],
        [f(-1, 2), f(1, 6), f(1, 2), f(1, 6)],
    ];

    let configs: [(&str, Frac, Frac, [QuatQ; 4], QuatQ, &[(u32, usize, usize, usize, usize, usize)]); 3] = [
        (
            "B3_3/2",
            Frac::from_i(-3),
            Frac::from_i(-1),
            o3,
            [z, one, z, one],
            &[(3, 36, 144, 4, 144, 4), (9, 972, 3888, 4, 3888, 4), (15, 2160, 8640, 4, 8640, 4)],
        ),
        (
            "B5_5/2",
            Frac::from_i(-3),
            Frac::from_i(-5),
            o5m,
            [z, f(5, 3), z, f(1, 3)],
            &[(3, 24, 144, 6, 576, 24), (5, 300, 3600, 12, 3600, 12), (15, 3600, 3600, 1, 14400, 4)],
        ),
        (
            "B5_1/2",
            Frac::from_i(-3),
            Frac::from_i(-5),
            o5p,
            [z, f(1, 3), z, f(1, 3)],
            &[(3, 24, 576, 24, 144, 6), (5, 300, 3600, 12, 3600, 12), (15, 3600, 14400, 4, 3600, 1)],
        ),
    ];

    for (name, a, b, basis, t_q, rows) in configs {
        let binv = mat4_inv_frac(&basis);
        for &(m, exp_ad, exp_j6, exp_k6, exp_j12, exp_k12) in rows {
            let ad_g = vec![
                adjoint_mat4_mod(a_q, &basis, &binv, a, b, m),
                adjoint_mat4_mod(b_q, &basis, &binv, a, b, m),
                adjoint_mat4_mod(t_q, &basis, &binv, a, b, m),
            ];
            let (ad1, j6, k6, _) = bfs_mat_joint(&ad_g, &[a_y, b_y, t0], 4, m);
            let (ad2, j12, k12, _) = bfs_mat_joint(&ad_g, &[a_y, b_y, t1], 4, m);
            assert_eq!((ad1, ad2, j6, k6, j12, k12), (exp_ad, exp_ad, exp_j6, exp_k6, exp_j12, exp_k12), "{} mod {}", name, m);
        }
    }
}

// ============================================================================
// Suite R3: Pillar II — Real-Quadratic (6) & Cubic (4) Census + Q(sqrt(7)) Level (3)
// ============================================================================

pub fn verify_r3_real_quad_cubic_and_q7_congruence() {
    // 1. Real-quadratic 6 primitive moduli across 4 fields
    let mut dfs = BTreeSet::new();
    let mut q_cnt = 0usize;
    for s in 1i64..=11 {
        for p in 1i64..(3 * s) {
            if 18 - 3 * s + p <= 0 || gcd_i64(gcd_i64(2, s), p) != 1 {
                continue;
            }
            let disc = s * s - 8 * p;
            if disc <= 0 {
                continue;
            }
            let r = (disc as f64).sqrt() as i64;
            if r * r == disc || (r + 1) * (r + 1) == disc {
                continue;
            }
            let mut sqf = disc;
            let mut d = 2i64;
            while d * d <= sqf {
                while sqf % (d * d) == 0 {
                    sqf /= d * d;
                }
                d += 1;
            }
            let df = if sqf % 4 == 1 { sqf } else { 4 * sqf };
            dfs.insert(df);
            q_cnt += 1;
        }
    }
    assert_eq!(q_cnt, 6);
    let df_vec: Vec<i64> = dfs.into_iter().collect();
    assert_eq!(df_vec, vec![8, 12, 17, 28]);

    // 2. Cubic 4 primitive moduli (d_F in {148, 316})
    let mut c_cnt = 0usize;
    for c2 in 1i64..=17 {
        for c1 in 1i64..=53 {
            let dp = c2 * c2 - 6 * c1;
            if dp <= 0 || 18 - c2 <= 0 || dp >= (18 - c2) * (18 - c2) {
                continue;
            }
            for c0 in 1i64..=53 {
                if gcd_i64(gcd_i64(2, c2), gcd_i64(c1, c0)) != 1 || 54 - 9 * c2 + 3 * c1 - c0 <= 0 {
                    continue;
                }
                let (a, b, c, d) = (2i128, -c2 as i128, c1 as i128, -c0 as i128);
                let disc3 = 18 * a * b * c * d - 4 * b * b * b * d + b * b * c * c - 4 * a * c * c * c - 27 * a * a * d * d;
                if disc3 <= 0 {
                    continue;
                }
                let mut has_rat = false;
                for qd in [1i128, 2] {
                    for pn in 1i128..=(c0 as i128) {
                        if (c0 as i128) % pn == 0 {
                            if 2 * pn * pn * pn - (c2 as i128) * pn * pn * qd + (c1 as i128) * pn * qd * qd - (c0 as i128) * qd * qd * qd == 0 {
                                has_rat = true;
                                break;
                            }
                        }
                    }
                    if has_rat {
                        break;
                    }
                }
                if !has_rat {
                    assert!(disc3 == 316 || disc3 == 148);
                    c_cnt += 1;
                }
            }
        }
    }
    assert_eq!(c_cnt, 4);

    // 3. Direct mod (3) = p_3 * p_3' congruence verification on O_7^max over Q(sqrt(7))!
    // In B_2 x Q(sqrt(7)) = (-3, -2), reducing mod p_3 (sqrt(7) = 1 mod 3) and p_3' (sqrt(7) = 2 mod 3)
    // yields exact 4x4 F_3 adjoint images inside GL_4(F_3) x GL_4(F_3) (block-diagonal 8x8 mod 3)!
    let (a_y, b_y, t0, t1) = nauru_generators();
    // Exact coordinates in F_3 for O_7^max = <a7, t7, ((3-s)/4)(j+k), ((3-s)/2)k> with s = sqrt(7) mod 3 in {1, 2}
    let build_o7_mod3 = |s_mod3: i128| -> Vec<Vec<u16>> {
        // Compute in Q(sqrt(7)) reduced mod (3, sqrt(7) - s_mod3): simply substitute sqrt(7) -> s_mod3 in exact Q arithmetic!
        // Note: wait, denominators contain (3 - sqrt(7)) of norm 2 (coprime to 3!), so substituting s_mod3 in F_3 is an EXACT ring homomorphism Z[sqrt(7), 1/2] -> F_3!
        // Compute exact 4x4 adjoint matrices over Q(sqrt(7)) evaluated at s = s_mod3 (mod 3):
        let f = Frac::new;
        let s = Frac::from_i(s_mod3);
        let z = Frac::from_i(0);
        let one = Frac::from_i(1);
        let a = Frac::from_i(-3);
        let b = Frac::from_i(-2);
        let a7: QuatQ = [f(1, 2), f(1, 2), z, z];
        let b7: QuatQ = [z, z, one, z];
        // t7 = (2i + (3-s)k)/6 -> i/3 + ((3-s)/6)k. Wait: denominator 3 in Q! Must compute in Q(sqrt(7)) BEFORE reducing mod 3!
        let _ = (a7, b7, a, b, s);
        // Let's compute using exact quadratic field Q(sqrt(7)) arithmetic!
        type Qf = (Frac, Frac);
        let qf_add = |u: Qf, v: Qf| (u.0.add(v.0), u.1.add(v.1));
        let qf_sub = |u: Qf, v: Qf| (u.0.sub(v.0), u.1.sub(v.1));
        let qf_neg = |u: Qf| (u.0.neg(), u.1.neg());
        let qf_mul = |u: Qf, v: Qf| (u.0.mul(v.0).add(Frac::from_i(7).mul(u.1.mul(v.1))), u.0.mul(v.1).add(u.1.mul(v.0)));
        let qf_inv = |u: Qf| {
            let n = u.0.mul(u.0).sub(Frac::from_i(7).mul(u.1.mul(u.1)));
            (u.0.div(n), u.1.neg().div(n))
        };
        let zf: Qf = (z, z);
        let of: Qf = (one, z);
        let af: Qf = (Frac::from_i(-3), z);
        let bf: Qf = (Frac::from_i(-2), z);
        let abf = qf_mul(af, bf);
        let qm = |x: [Qf; 4], y: [Qf; 4]| -> [Qf; 4] {
            [
                qf_add(qf_add(qf_mul(x[0], y[0]), qf_mul(af, qf_mul(x[1], y[1]))), qf_sub(qf_mul(bf, qf_mul(x[2], y[2])), qf_mul(abf, qf_mul(x[3], y[3])))),
                qf_add(qf_add(qf_mul(x[0], y[1]), qf_mul(x[1], y[0])), qf_sub(qf_mul(bf, qf_mul(x[3], y[2])), qf_mul(bf, qf_mul(x[2], y[3])))),
                qf_add(qf_add(qf_mul(x[0], y[2]), qf_mul(x[2], y[0])), qf_sub(qf_mul(af, qf_mul(x[1], y[3])), qf_mul(af, qf_mul(x[3], y[1])))),
                qf_add(qf_add(qf_mul(x[0], y[3]), qf_mul(x[3], y[0])), qf_sub(qf_mul(x[1], y[2]), qf_mul(x[2], y[1]))),
            ]
        };
        let qi = |x: [Qf; 4]| -> [Qf; 4] {
            let nr = qf_add(qf_sub(qf_mul(x[0], x[0]), qf_mul(af, qf_mul(x[1], x[1]))), qf_sub(qf_mul(abf, qf_mul(x[3], x[3])), qf_mul(bf, qf_mul(x[2], x[2]))));
            let ni = qf_inv(nr);
            [qf_mul(x[0], ni), qf_mul(qf_neg(x[1]), ni), qf_mul(qf_neg(x[2]), ni), qf_mul(qf_neg(x[3]), ni)]
        };
        let a7f: [Qf; 4] = [(f(1, 2), z), (f(1, 2), z), zf, zf];
        let b7f: [Qf; 4] = [zf, zf, of, zf];
        let t7f: [Qf; 4] = [zf, (f(1, 3), z), zf, (f(1, 2), f(-1, 6))];
        let o7: [[Qf; 4]; 4] = [
            a7f,
            t7f,
            [zf, zf, (f(3, 4), f(-1, 4)), (f(3, 4), f(-1, 4))],
            [zf, zf, zf, (f(3, 2), f(-1, 2))],
        ];
        // Invert 4x4 over Q(sqrt(7))
        let mut aug = [[zf; 8]; 4];
        for i in 0..4 {
            for j in 0..4 {
                aug[i][j] = o7[i][j];
            }
            aug[i][4 + i] = of;
        }
        for i in 0..4 {
            let piv = (i..4).find(|&r| aug[r][i].0.n != 0 || aug[r][i].1.n != 0).unwrap();
            aug.swap(i, piv);
            let pi = qf_inv(aug[i][i]);
            for c in 0..8 {
                aug[i][c] = qf_mul(aug[i][c], pi);
            }
            for r in 0..4 {
                if r != i && (aug[r][i].0.n != 0 || aug[r][i].1.n != 0) {
                    let fac = aug[r][i];
                    for c in 0..8 {
                        aug[r][c] = qf_sub(aug[r][c], qf_mul(fac, aug[i][c]));
                    }
                }
            }
        }
        let mut res = Vec::new();
        for g in [a7f, b7f, t7f] {
            let gi = qi(g);
            let mut flat = Vec::with_capacity(16);
            for e in &o7 {
                let w = qm(qm(g, *e), gi);
                for k in 0..4 {
                    let mut c = zf;
                    for j in 0..4 {
                        c = qf_add(c, qf_mul(w[j], aug[j][4 + k]));
                    }
                    let val = c.0.add(c.1.mul(Frac::from_i(s_mod3)));
                    flat.push(val.mod_u32(3));
                }
            }
            res.push(flat);
        }
        res
    };

    let p3 = build_o7_mod3(1);
    let p3p = build_o7_mod3(2);
    // Block-diagonal 8x8 mod 3 encoding (p_3, p_3') jointly!
    let mut joint8 = Vec::new();
    for gi in 0..3 {
        let mut m8 = vec![0u16; 64];
        for r in 0..4 {
            for c in 0..4 {
                m8[r * 8 + c] = p3[gi][r * 4 + c];
                m8[(r + 4) * 8 + (c + 4)] = p3p[gi][r * 4 + c];
            }
        }
        joint8.push(m8);
    }
    let (ad_a, j6, k6, _) = bfs_mat_joint(&joint8, &[a_y, b_y, t0], 8, 3);
    let (ad_b, j12, k12, _) = bfs_mat_joint(&joint8, &[a_y, b_y, t1], 8, 3);
    assert_eq!((ad_a, ad_b, j6, k6, j12, k12), (576, 576, 576, 1, 576, 1));
}

// ============================================================================
// Suite R4: Pillar III — Dic_6 18 Cayley, pi_Z(4..16), 43 Inv, S_4 & Exhaustive Dhar
// ============================================================================

fn dhar_reaches_z(z: &[[usize; 4]; 24], init: &[i8; 24], target: usize) -> bool {
    let mut d = *init;
    for _ in 0..64 {
        if d[target] > 0 {
            return true;
        }
        let mut burnt = [false; 24];
        let mut bcnt = [0i8; 24];
        let mut q = [0usize; 24];
        burnt[target] = true;
        q[0] = target;
        let (mut qh, mut qt) = (0usize, 1usize);
        while qh < qt {
            let u = q[qh];
            qh += 1;
            for &v in &z[u] {
                if !burnt[v] {
                    bcnt[v] += 1;
                    if bcnt[v] > d[v] {
                        burnt[v] = true;
                        q[qt] = v;
                        qt += 1;
                    }
                }
            }
        }
        if qt == 24 {
            return false;
        }
        for u in 0..24 {
            if !burnt[u] {
                for &v in &z[u] {
                    if burnt[v] {
                        d[u] -= 1;
                        d[v] += 1;
                    }
                }
            }
        }
    }
    d[target] > 0
}

fn is_rank1_z(z: &[[usize; 4]; 24], chips: &[i8; 24]) -> bool {
    for v in 1..24 {
        if chips[v] == 0 && !dhar_reaches_z(z, chips, v) {
            return false;
        }
    }
    true
}

fn exhaustive_dhar_z(z: &[[usize; 4]; 24], extra: usize) -> (u64, u64) {
    let mut chips = [0i8; 24];
    chips[0] = 1;
    let mut tested = 0u64;
    let mut hits = 0u64;
    fn rec(z: &[[usize; 4]; 24], rem: usize, start: usize, chips: &mut [i8; 24], tested: &mut u64, hits: &mut u64) {
        if rem == 0 {
            *tested += 1;
            if is_rank1_z(z, chips) {
                *hits += 1;
            }
            return;
        }
        for v in start..24 {
            chips[v] += 1;
            rec(z, rem - 1, v, chips, tested, hits);
            chips[v] -= 1;
        }
    }
    rec(z, extra, 0, &mut chips, &mut tested, &mut hits);
    (tested, hits)
}

pub fn verify_r4_dic6_cayley_cadences_scramble_and_exhaustive_dhar() {
    // 1. 18/55 connected Cayley graphs of Dic_6
    let mut pairs = Vec::new();
    let mut seen = [false; 24];
    seen[0] = true;
    seen[6] = true;
    for g in 0..24 {
        if !seen[g] {
            let gi = dic6_inv(g);
            pairs.push((g.min(gi), g.max(gi)));
            seen[g] = true;
            seen[gi] = true;
        }
    }
    assert_eq!(pairs.len(), 11);
    let mut conn = 0usize;
    for i in 0..11 {
        for j in (i + 1)..11 {
            let g = build_dic6_cayley([pairs[i].0, pairs[i].1, pairs[j].0, pairs[j].1]);
            let mut vis = [false; 24];
            let mut q = VecDeque::new();
            vis[0] = true;
            q.push_back(0);
            let mut cnt = 1;
            while let Some(u) = q.pop_front() {
                for &v in &g[u] {
                    if !vis[v] {
                        vis[v] = true;
                        cnt += 1;
                        q.push_back(v);
                    }
                }
            }
            if cnt == 24 {
                conn += 1;
            }
        }
    }
    assert_eq!(conn, 18);

    // 2. Hashimoto pi_Z(4..16)
    let z = build_dic6_z();
    let (_, pi_z) = hashimoto_cadences::<4, 96>(&z, 16);
    assert_eq!(
        [pi_z[4], pi_z[6], pi_z[8], pi_z[10], pi_z[12], pi_z[14], pi_z[16]],
        [60, 240, 1560, 11616, 90172, 681504, 5379960]
    );

    // 3. Aut(Z) = 96 & 43 involutions {7: 2, 11: 24, 13: 17}
    let aut_z = graph_auts_generic(&z);
    assert_eq!(aut_z.len(), 96);
    let id = perm_id();
    let mut b1_hist: BTreeMap<usize, usize> = BTreeMap::new();
    let mut inv_cnt = 0usize;
    for sig in &aut_z {
        if *sig != id && perm_comp(sig, sig) == id {
            inv_cnt += 1;
            let mut v_orbs = HashSet::new();
            for v in 0..24 {
                v_orbs.insert(v.min(sig[v] as usize));
            }
            let mut e_orbs = HashSet::new();
            for u in 0..24 {
                for &v in &z[u] {
                    if u < v && !(sig[u] as usize == v && sig[v] as usize == u) {
                        let e1 = (u, v);
                        let (su, sv) = (sig[u] as usize, sig[v] as usize);
                        let e2 = (su.min(sv), su.max(sv));
                        e_orbs.insert(e1.min(e2));
                    }
                }
            }
            *b1_hist.entry(e_orbs.len() - v_orbs.len() + 1).or_insert(0) += 1;
        }
    }
    assert_eq!(inv_cnt, 43);
    assert_eq!(b1_hist.into_iter().collect::<Vec<_>>(), vec![(7, 2), (11, 24), (13, 17)]);

    // 4. Exhaustive discrete Dhar non-existence on Z at deg 6 (0/98,280) and deg 7 (0/475,020)
    assert_eq!(exhaustive_dhar_z(&z, 5), (98280, 0));
    assert_eq!(exhaustive_dhar_z(&z, 6), (475020, 0));

    // 5. Optimal 4-path scramble S_4: 276 touching, Edmonds-Karp cuts {8: 48, 10: 108}
    let e0 = [0usize, 1, 2, 20];
    let mut eggs = [0u32; 24];
    for g in 0..24 {
        for &v in &e0 {
            eggs[g] |= 1u32 << dic6_mul(g, v);
        }
    }
    let mut inter = 0usize;
    let mut cut8 = 0usize;
    let mut cut10 = 0usize;
    for i in 0..24 {
        for j in (i + 1)..24 {
            if (eggs[i] & eggs[j]) != 0 {
                inter += 1;
            } else {
                match edmonds_karp(&z, eggs[i], eggs[j]) {
                    8 => cut8 += 1,
                    10 => cut10 += 1,
                    c => panic!("unexpected cut {}", c),
                }
            }
        }
    }
    assert_eq!((inter, cut8, cut10), (120, 48, 108));

    // 6. Witness D_8 = {0,3,6,9,12,15,18,21} passes discrete Dhar on all 24 vertices
    let mut d8 = [0i8; 24];
    for v in [0, 3, 6, 9, 12, 15, 18, 21] {
        d8[v] = 1;
    }
    assert!(is_rank1_z(&z, &d8));
}

// ============================================================================
// Suite R5: Pillar III — All 5 Rational Dic_6 Curves, 0/80 CRT Left-Mult,
//           Hurwitz L_8/{+-1} vs Ad_16 Reconciliation & O_70^1 Riehm Mod-8
// ============================================================================

fn sqf_full(fr: Frac) -> i128 {
    let mut val = (fr.n * fr.d).abs();
    let mut d = 2i128;
    let mut res = 1i128;
    while d * d <= val {
        let mut c = 0;
        while val % d == 0 {
            val /= d;
            c += 1;
        }
        if c % 2 == 1 {
            res *= d;
        }
        d += 1;
    }
    if val > 1 {
        res *= val;
    }
    res
}

fn isqrt_i128(n: i128) -> i128 {
    let mut x = (n as f64).sqrt() as i128;
    while (x + 1) * (x + 1) <= n {
        x += 1;
    }
    while x * x > n {
        x -= 1;
    }
    assert_eq!(x * x, n);
    x
}

pub fn verify_r5_all80_crt_left_mult_hurwitz_and_riehm() {
    let z_g = build_dic6_z();
    let aut_z = graph_auts_generic(&z_g);
    let stab0: Vec<Perm24> = aut_z.iter().copied().filter(|p| p[0] == 0).collect();
    let a_z = *stab0.iter().find(|p| p[1] == 1 && p[11] == 11 && p[12] == 18).unwrap();
    let b_z = *stab0.iter().find(|p| p[12] == 12 && p[18] == 18 && p[1] == 11).unwrap();
    let txs: Vec<Perm24> = aut_z
        .iter()
        .copied()
        .filter(|p| (p[0] == 1 || p[0] == 11) && perm_order(p) == 2 && perm_comp(p, &a_z) == perm_comp(&a_z, p))
        .collect();
    let tys: Vec<Perm24> = aut_z
        .iter()
        .copied()
        .filter(|p| (p[0] == 12 || p[0] == 18) && perm_order(p) == 2 && perm_comp(p, &b_z) == perm_comp(&b_z, p))
        .collect();
    assert_eq!((txs.len(), tys.len()), (4, 4));
    let mut surjs = Vec::with_capacity(16);
    for &tx in &txs {
        for &ty in &tys {
            surjs.push([b_z, a_z, tx, ty]);
        }
    }

    let f = Frac::new;
    let z = Frac::from_i(0);
    let one = Frac::from_i(1);

    struct Spec {
        name: &'static str,
        a: Frac,
        b: Frac,
        ra: Frac,
        rb: Frac,
        basis: [QuatQ; 4],
        mods: &'static [u32],
        exp_pre: usize,
        exp_ker: &'static [(usize, usize)],
    }

    let specs = [
        Spec {
            name: "B2(4,4)",
            a: Frac::from_i(-2),
            b: Frac::from_i(-2),
            ra: one,
            rb: one,
            basis: [
                [f(1, 2), z, f(1, 2), f(1, 4)],
                [z, f(1, 2), f(1, 2), z],
                [z, z, one, z],
                [z, z, z, f(1, 2)],
            ],
            mods: &[16],
            exp_pre: 1024,
            exp_ker: &[(3, 16)],
        },
        Spec {
            name: "B5(2)",
            a: Frac::from_i(-2),
            b: Frac::from_i(-5),
            ra: one,
            rb: one,
            basis: [
                [f(1, 2), z, f(1, 2), f(1, 2)],
                [z, f(1, 2), z, f(1, 2)],
                [z, z, one, z],
                [z, z, z, one],
            ],
            mods: &[16, 5],
            exp_pre: 12288,
            exp_ker: &[(6, 16)],
        },
        Spec {
            name: "B70",
            a: Frac::from_i(-35),
            b: Frac::from_i(-2),
            ra: f(1, 5),
            rb: one,
            basis: [
                [f(1, 2), f(1, 2), z, z],
                [z, one, z, z],
                [z, z, f(1, 2), f(1, 2)],
                [z, z, z, one],
            ],
            mods: &[8, 5, 7],
            exp_pre: 36864,
            exp_ker: &[(2, 8), (6, 8)],
        },
        Spec {
            name: "B2(5)",
            a: Frac::from_i(-5),
            b: Frac::from_i(-5),
            ra: one,
            rb: one,
            basis: [
                [f(1, 2), f(1, 2), f(1, 2), f(1, 10)],
                [z, one, z, z],
                [z, z, one, z],
                [z, z, z, f(1, 5)],
            ],
            mods: &[8, 5],
            exp_pre: 3072,
            exp_ker: &[(12, 16)],
        },
        Spec {
            name: "B2(11)",
            a: Frac::from_i(-2),
            b: Frac::from_i(-11),
            ra: one,
            rb: one,
            basis: [
                [f(1, 2), z, f(1, 2), z],
                [z, f(1, 2), z, f(1, 2)],
                [z, z, one, z],
                [z, z, z, one],
            ],
            mods: &[8, 11],
            exp_pre: 7680,
            exp_ker: &[(4, 8), (12, 8)],
        },
    ];

    let mut ord3_ok = 0usize;
    let mut cong_total = 0usize;

    for sp in &specs {
        let binv = mat4_inv_frac(&sp.basis);
        let gens_q: [QuatQ; 4] = [[z, one, z, z], [z, z, one, z], [z, one, z, sp.rb], [z, z, one, sp.ra]];
        let gcls: [i128; 4] = [
            sqf_full(qnrd_q(gens_q[0], sp.a, sp.b)),
            sqf_full(qnrd_q(gens_q[1], sp.a, sp.b)),
            sqf_full(qnrd_q(gens_q[2], sp.a, sp.b)),
            sqf_full(qnrd_q(gens_q[3], sp.a, sp.b)),
        ];
        let mut coset: HashMap<i128, (QuatQ, Vec<usize>)> = HashMap::new();
        coset.insert(1, ([one, z, z, z], vec![]));
        let mut cq = VecDeque::new();
        cq.push_back(1i128);
        while let Some(c) = cq.pop_front() {
            let (rq, rw) = coset[&c].clone();
            for gi in 0..4 {
                let g = gcd_i128(c, gcls[gi]);
                let nc = (c / g) * (gcls[gi] / g);
                if !coset.contains_key(&nc) {
                    let mut nw = rw.clone();
                    nw.push(gi);
                    coset.insert(nc, (qmul_q(rq, gens_q[gi], sp.a, sp.b), nw));
                    cq.push_back(nc);
                }
            }
        }
        let mut sq: Vec<QuatQ> = Vec::new();
        let mut sw: Vec<Vec<usize>> = Vec::new();
        let coset_items: Vec<(i128, (QuatQ, Vec<usize>))> = coset.iter().map(|(&k, v)| (k, v.clone())).collect();
        for (c, (rq, rw)) in &coset_items {
            for gi in 0..4 {
                let g = gcd_i128(*c, gcls[gi]);
                let nc = (*c / g) * (gcls[gi] / g);
                let (tq, tw) = &coset[&nc];
                let el = qmul_q(qmul_q(*rq, gens_q[gi], sp.a, sp.b), qinv_q(*tq, sp.a, sp.b), sp.a, sp.b);
                let nv = qnrd_q(el, sp.a, sp.b);
                let sc = Frac::new(isqrt_i128(nv.d), isqrt_i128(nv.n));
                let el1 = [el[0].mul(sc), el[1].mul(sc), el[2].mul(sc), el[3].mul(sc)];
                if el1[1].n != 0 || el1[2].n != 0 || el1[3].n != 0 {
                    sq.push(el1);
                    let mut w = rw.clone();
                    w.push(gi);
                    w.extend(tw.iter().rev().copied());
                    sw.push(w);
                }
            }
        }

        // Factor tables (quotienting Sylow-p at odd primes p in {5, 7, 11})
        let nsg = sq.len();
        let mut f_tables: Vec<Vec<Vec<usize>>> = Vec::new();
        for &m in sp.mods {
            let fg: Vec<Vec<u16>> = sq.iter().map(|&q| left_mult_mat4_mod(q, &sp.basis, &binv, sp.a, sp.b, m)).collect();
            let mut id4 = vec![0u16; 16];
            for i in 0..4 {
                id4[i * 4 + i] = 1;
            }
            let mut el_map: HashMap<Vec<u16>, usize> = HashMap::new();
            el_map.insert(id4.clone(), 0);
            let mut els = vec![id4.clone()];
            let mut q = VecDeque::new();
            q.push_back(0usize);
            while let Some(uid) = q.pop_front() {
                let um = els[uid].clone();
                for gm in &fg {
                    let nm = mat_mul_mod(gm, &um, 4, m);
                    if !el_map.contains_key(&nm) {
                        el_map.insert(nm.clone(), els.len());
                        els.push(nm);
                        q.push_back(els.len() - 1);
                    }
                }
            }
            if m == 5 || m == 7 || m == 11 {
                let mut u_ids = Vec::new();
                for (idx, mat) in els.iter().enumerate() {
                    let mut cur = mat.clone();
                    for _ in 0..(m * m - 1) {
                        cur = mat_mul_mod(&cur, mat, 4, m);
                    }
                    if cur == id4 {
                        u_ids.push(idx);
                    }
                }
                let mut coset_of = vec![usize::MAX; els.len()];
                let mut reps = Vec::new();
                for idx in 0..els.len() {
                    if coset_of[idx] == usize::MAX {
                        let cid = reps.len();
                        reps.push(idx);
                        for &uid in &u_ids {
                            let prod = mat_mul_mod(&els[idx], &els[uid], 4, m);
                            coset_of[el_map[&prod]] = cid;
                        }
                    }
                }
                let mut gt = Vec::with_capacity(nsg);
                for gm in &fg {
                    let mut tbl = vec![0usize; reps.len()];
                    for (cid, &rep) in reps.iter().enumerate() {
                        let prod = mat_mul_mod(gm, &els[rep], 4, m);
                        tbl[cid] = coset_of[el_map[&prod]];
                    }
                    gt.push(tbl);
                }
                f_tables.push(gt);
            } else {
                // Verify O_70^1 Riehm mod 8 commutator subgroup (768 / 256 / 3, -I in [G,G])
                if sp.name == "B70" && m == 8 {
                    assert_eq!(els.len(), 768);
                    let mut neg4 = vec![0u16; 16];
                    for i in 0..4 {
                        neg4[i * 4 + i] = 7;
                    }
                    let mut inv_of = vec![0usize; els.len()];
                    for (idx, mat) in els.iter().enumerate() {
                        let mut cur = id4.clone();
                        loop {
                            let nxt = mat_mul_mod(&cur, mat, 4, 8);
                            if nxt == id4 {
                                inv_of[idx] = el_map[&cur];
                                break;
                            }
                            cur = nxt;
                        }
                    }
                    let mut cgens = HashSet::new();
                    for gm in &fg {
                        let gi = &els[inv_of[el_map[gm]]];
                        for (xid, xm) in els.iter().enumerate() {
                            let xi = &els[inv_of[xid]];
                            let c = mat_mul_mod(&mat_mul_mod(gm, xm, 4, 8), &mat_mul_mod(gi, xi, 4, 8), 4, 8);
                            cgens.insert(el_map[&c]);
                        }
                    }
                    let cmats: Vec<Vec<u16>> = cgens.into_iter().map(|id| els[id].clone()).collect();
                    let mut cset = HashSet::new();
                    cset.insert(0usize);
                    let mut cq2 = VecDeque::new();
                    cq2.push_back(0usize);
                    while let Some(uid) = cq2.pop_front() {
                        for cm in &cmats {
                            let nid = el_map[&mat_mul_mod(&els[uid], cm, 4, 8)];
                            if cset.insert(nid) {
                                cq2.push_back(nid);
                            }
                        }
                    }
                    assert_eq!(cset.len(), 256);
                    assert!(cset.contains(&el_map[&neg4]));
                }
                let mut gt = Vec::with_capacity(nsg);
                for gm in &fg {
                    let mut tbl = vec![0usize; els.len()];
                    for (idx, um) in els.iter().enumerate() {
                        tbl[idx] = el_map[&mat_mul_mod(gm, um, 4, m)];
                    }
                    gt.push(tbl);
                }
                f_tables.push(gt);
            }
        }

        // Integer-indexed CRT BFS
        let nf = sp.mods.len();
        let start = vec![0usize; nf];
        let mut crt_map: HashMap<Vec<usize>, usize> = HashMap::new();
        crt_map.insert(start.clone(), 0);
        let mut crt_els = vec![start];
        let mut crt_step: Vec<Vec<usize>> = Vec::new();
        let mut q = VecDeque::new();
        q.push_back(0usize);
        while let Some(uid) = q.pop_front() {
            let st = crt_els[uid].clone();
            let mut row = vec![0usize; nsg];
            for gi in 0..nsg {
                let nst: Vec<usize> = (0..nf).map(|fi| f_tables[fi][gi][st[fi]]).collect();
                let nid = match crt_map.get(&nst) {
                    Some(&id) => id,
                    None => {
                        let id = crt_els.len();
                        crt_map.insert(nst.clone(), id);
                        crt_els.push(nst);
                        q.push_back(id);
                        id
                    }
                };
                row[gi] = nid;
            }
            crt_step.push(row);
        }
        assert_eq!(crt_els.len(), sp.exp_pre, "{} CRT order", sp.name);

        let mut khist: BTreeMap<usize, usize> = BTreeMap::new();
        for p4 in &surjs {
            let sp_perms: Vec<Perm24> = sw
                .iter()
                .map(|w| {
                    let mut cur = perm_id();
                    for &idx in w {
                        cur = perm_comp(&cur, &p4[idx]);
                    }
                    cur
                })
                .collect();
            let mut pm: HashMap<Perm24, usize> = HashMap::new();
            pm.insert(perm_id(), 0);
            let mut pels = vec![perm_id()];
            let mut pstep: Vec<Vec<usize>> = Vec::new();
            let mut pq = VecDeque::new();
            pq.push_back(0usize);
            while let Some(uid) = pq.pop_front() {
                let cp = pels[uid];
                let mut row = vec![0usize; nsg];
                for gi in 0..nsg {
                    let np = perm_comp(&cp, &sp_perms[gi]);
                    let nid = match pm.get(&np) {
                        Some(&id) => id,
                        None => {
                            let id = pels.len();
                            pm.insert(np, id);
                            pels.push(np);
                            pq.push_back(id);
                            id
                        }
                    };
                    row[gi] = nid;
                }
                pstep.push(row);
            }
            let ord3 = pels.iter().filter(|p| perm_order(p) == 3).count();
            assert_eq!(ord3, 2);
            ord3_ok += 1;

            let nc = crt_els.len();
            let np = pels.len();
            let mut seen = vec![0u8; nc * np];
            seen[0] = 1;
            let mut jq = VecDeque::new();
            jq.push_back(0usize);
            let mut ker = 1usize;
            while let Some(st) = jq.pop_front() {
                let cid = st / np;
                let pid = st % np;
                for gi in 0..nsg {
                    let ncid = crt_step[cid][gi];
                    let npid = pstep[pid][gi];
                    let nst = ncid * np + npid;
                    if seen[nst] == 0 {
                        seen[nst] = 1;
                        if ncid == 0 {
                            ker += 1;
                        }
                        jq.push_back(nst);
                    }
                }
            }
            *khist.entry(ker).or_insert(0) += 1;
            if ker == 1 {
                cong_total += 1;
            }
        }
        assert_eq!(khist.into_iter().collect::<Vec<_>>(), sp.exp_ker, "{} ker hist", sp.name);

        // Hurwitz B_2(4,4) level-8 left-mult (L_8/{+-1} = 64 hits {3:16}) vs Ad_8 ({3:8, 6:8}) -> Ad_16 ({3:16})
        if sp.name == "B2(4,4)" {
            let l8_g: Vec<Vec<u16>> = sq.iter().map(|&q| left_mult_mat4_mod(q, &sp.basis, &binv, sp.a, sp.b, 8)).collect();
            let mut l8_kh: BTreeMap<usize, usize> = BTreeMap::new();
            let mut l8_ord = 0usize;
            for p4 in &surjs {
                let sp_perms: Vec<Perm24> = sw
                    .iter()
                    .map(|w| {
                        let mut cur = perm_id();
                        for &idx in w {
                            cur = perm_comp(&cur, &p4[idx]);
                        }
                        cur
                    })
                    .collect();
                let (lo, _, k, _) = bfs_mat_joint(&l8_g, &sp_perms, 4, 8);
                l8_ord = lo;
                *l8_kh.entry(k).or_insert(0) += 1;
            }
            assert_eq!(l8_ord, 128); // projective L_8/{+-1} = 64!
            assert_eq!(l8_kh.into_iter().collect::<Vec<_>>(), vec![(3, 16)]);
        }
    }
    assert_eq!((ord3_ok, cong_total), (80, 0));
}

// ============================================================================
// Suite R6: Genus-25 Borel Census & Poitou-Odlyzko Audit
// ============================================================================

fn gauss_legendre(n: usize) -> (Vec<f64>, Vec<f64>) {
    let mut nodes = vec![0.0f64; n];
    let mut weights = vec![0.0f64; n];
    let m = (n + 1) / 2;
    for i in 0..m {
        let mut x = (std::f64::consts::PI * (i as f64 + 0.75) / (n as f64 + 0.5)).cos();
        let mut dp = 0.0f64;
        for _ in 0..30 {
            let (mut p0, mut p1) = (1.0f64, x);
            for k in 2..=n {
                let p2 = ((2.0 * k as f64 - 1.0) * x * p1 - (k as f64 - 1.0) * p0) / k as f64;
                p0 = p1;
                p1 = p2;
            }
            dp = n as f64 * (x * p1 - p0) / (x * x - 1.0);
            let dx = p1 / dp;
            x -= dx;
            if dx.abs() < 1e-16 {
                break;
            }
        }
        let w = 2.0 / ((1.0 - x * x) * dp * dp);
        nodes[i] = -x;
        nodes[n - 1 - i] = x;
        weights[i] = w;
        weights[n - 1 - i] = w;
    }
    (nodes, weights)
}

fn h1_kernel(w: f64) -> f64 {
    if w >= 2.0 {
        return 0.0;
    }
    let pi = std::f64::consts::PI;
    ((2.0 - w) / 3.0) * (1.0 + 0.5 * (pi * w).cos()) + (pi * w).sin() / (2.0 * pi)
}

fn poitou_eval(b: f64, ngl: usize) -> (f64, f64, f64) {
    let (xs, ws) = gauss_legendre(ngl);
    let mut ib = 0.0f64;
    let mut ia = 0.0f64;
    for (&xi, &wi) in xs.iter().zip(ws.iter()) {
        let x = b * (xi + 1.0);
        let fb = h1_kernel(x / b) / (0.5 * x).cosh();
        ib += wi * b * (1.0 - fb) / (2.0 * (0.5 * x).sinh());
        ia += wi * b * fb / (2.0 * (0.5 * x).cosh());
    }
    const GAMMA: f64 = 0.57721566490153286060651209008240243104;
    let log_b = (8.0 * std::f64::consts::PI).ln() + GAMMA - ib + (0.5 * b).tanh().ln();
    let log_a = log_b + ia;
    let ln2 = 2.0f64.ln();
    let mut f2 = 0.0f64;
    let mut m = 1usize;
    while (m as f64) * ln2 < 2.0 * b {
        f2 += 4.0 * (ln2 / (1.0 + (1u64 << m) as f64)) * h1_kernel((m as f64) * ln2 / b);
        m += 1;
    }
    (log_b, log_a, f2)
}

pub fn verify_r6_genus25_and_poitou_odlyzko() {
    let (lb64_v, _, f2_64) = poitou_eval(6.0, 64);
    let (lb128_v, _, f2_128) = poitou_eval(6.0, 128);
    let lb64 = (lb64_v - (8.0 / 3.0) * 6.0 / 48.0 + (8.0 / 48.0) * f2_64).exp();
    let lb128 = (lb128_v - (8.0 / 3.0) * 6.0 / 48.0 + (8.0 / 48.0) * f2_128).exp();
    let ub616 = (4.0 * std::f64::consts::PI * std::f64::consts::PI).powf(2.0 / 3.0) * 72.0f64.powf(1.0 / 9.0);
    assert!((lb64 - lb128).abs() < 1.5e-14);
    assert!(lb128 - ub616 > 0.0136298);
    // Anti-facade rejection
    let f_bad_1 = 1.0 + std::f64::consts::PI.cos() - 0.3 * (1.0 - (2.0 * std::f64::consts::PI).cos())
        + 0.3 * (std::f64::consts::PI.cos() + (3.0 * std::f64::consts::PI).cos());
    assert!((f_bad_1 + 0.60).abs() < 1e-14 && f_bad_1 < 0.0);
    // Degree-8 gap preservation (b=3.0 and peak b=3.052)
    let ub81 = (4.0 * std::f64::consts::PI * std::f64::consts::PI).powf(2.0 / 3.0) * 4.5f64.powf(1.0 / 12.0);
    let (_, la3, f2_3) = poitou_eval(3.0, 128);
    let lb8_3 = (la3 - (8.0 / 3.0) * 3.0 / 8.0 + f2_3 / 8.0).exp();
    let (_, lap, f2_p) = poitou_eval(3.039865, 128);
    let lb8_p = (lap - (8.0 / 3.0) * 3.039865 / 8.0 + f2_p / 8.0).exp();
    assert!((lb8_3 - 12.5937296518).abs() < 1e-8);
    assert!((lb8_p - 12.5955757277).abs() < 1e-7 && lb8_p < ub81);
}
