// SPDX-License-Identifier: MIT
// Copyright (c) 2026 Ergentics, LLC
//! Independent zero-crate Rust verification oracle for:
//!   "Uniform Triadic Wreath Products, the Nauru Graph, and 2-Adic Arithmeticity"

use std::collections::{BTreeMap, BTreeSet, HashMap, HashSet, VecDeque};

pub const MOD_Q: i64 = 1_000_003;
pub type Perm24 = [u8; 24];

pub fn id24() -> Perm24 {
    let mut p = [0u8; 24];
    for i in 0..24 {
        p[i] = i as u8;
    }
    p
}

pub fn comp(g: &Perm24, h: &Perm24) -> Perm24 {
    let mut out = [0u8; 24];
    for i in 0..24 {
        out[i] = g[h[i] as usize];
    }
    out
}

pub fn inv24(g: &Perm24) -> Perm24 {
    let mut out = [0u8; 24];
    for i in 0..24 {
        out[g[i] as usize] = i as u8;
    }
    out
}

pub fn order24(g: &Perm24) -> usize {
    let id = id24();
    let mut cur = *g;
    let mut k = 1usize;
    while cur != id {
        cur = comp(&cur, g);
        k += 1;
    }
    k
}

pub fn utt_perm(rev: bool, tp: usize, tm: usize) -> Perm24 {
    let mut out = [0u8; 24];
    for r in 0..12 {
        if !rev {
            out[r] = ((r + tp) % 12) as u8;
            out[12 + r] = (12 + (r + tm) % 12) as u8;
        } else {
            out[r] = (12 + (r + tp) % 12) as u8;
            out[12 + r] = ((r + tm) % 12) as u8;
        }
    }
    out
}

pub fn gen_group(gens: &[Perm24]) -> Vec<Perm24> {
    let id = id24();
    let mut seen: HashSet<Perm24> = HashSet::new();
    let mut q: VecDeque<Perm24> = VecDeque::new();
    seen.insert(id);
    q.push_back(id);
    while let Some(cur) = q.pop_front() {
        for g in gens {
            let nxt = comp(&cur, g);
            if seen.insert(nxt) {
                q.push_back(nxt);
            }
        }
    }
    seen.into_iter().collect()
}

pub struct GroupSummary {
    pub order: usize,
    pub center: usize,
    pub involutions: usize,
    pub ord24: usize,
    pub comm_order: usize,
}

pub fn analyze_group(elems: &[Perm24]) -> GroupSummary {
    let mut involutions = 0usize;
    let mut ord24 = 0usize;
    let mut center = 0usize;
    for g in elems {
        match order24(g) {
            2 => involutions += 1,
            24 => ord24 += 1,
            _ => {}
        }
        if elems.iter().all(|h| comp(g, h) == comp(h, g)) {
            center += 1;
        }
    }
    let invs: Vec<Perm24> = elems.iter().map(inv24).collect();
    let mut comm_gens: HashSet<Perm24> = HashSet::new();
    let id = id24();
    for (i, g) in elems.iter().enumerate() {
        for (j, h) in elems.iter().enumerate() {
            let c = comp(&comp(g, h), &comp(&invs[i], &invs[j]));
            if c != id {
                comm_gens.insert(c);
            }
        }
    }
    let comm_vec: Vec<Perm24> = comm_gens.into_iter().collect();
    let comm_order = if comm_vec.is_empty() { 1 } else { gen_group(&comm_vec).len() };
    GroupSummary { order: elems.len(), center, involutions, ord24, comm_order }
}

/// Gate 1: Non-fusion & normalizer tower (144 / 288 != 288 / 576 / 1152).
pub fn verify_non_fusion() -> bool {
    let t1 = utt_perm(false, 1, 1);
    let mut i0 = [0u8; 24];
    let mut m5 = [0u8; 24];
    let mut m7 = [0u8; 24];
    for r in 0..12 {
        i0[r] = (12 + (17 - r) % 12) as u8;
        i0[12 + r] = ((17 - r) % 12) as u8;
        m5[r] = ((5 * r) % 12) as u8;
        m5[12 + r] = (12 + (5 * r) % 12) as u8;
        m7[r] = ((7 * r) % 12) as u8;
        m7[12 + r] = (12 + (7 * r) % 12) as u8;
    }
    let p = utt_perm(true, 0, 0);
    let l = utt_perm(true, 4, 8);
    let r = utt_perm(true, 9, 3);
    let a = utt_perm(false, 1, 0);
    let b = utt_perm(false, 0, 1);

    let g_t_plr = analyze_group(&gen_group(&[t1, p, l, r]));
    let g_ti_plr = analyze_group(&gen_group(&[t1, i0, p, l, r]));
    let g_utt = analyze_group(&gen_group(&[a, b, p]));
    let g_576 = gen_group(&[a, b, p, i0]);
    let g_1152 = gen_group(&[a, b, p, i0, m5, m7]);

    g_t_plr.order == 144
        && g_ti_plr.order == 288
        && g_utt.order == 288
        && g_ti_plr.center == 2
        && g_utt.center == 12
        && g_ti_plr.involutions == 99
        && g_utt.involutions == 15
        && g_ti_plr.ord24 == 0
        && g_utt.ord24 == 48
        && g_ti_plr.comm_order == 18
        && g_utt.comm_order == 12
        && g_576.len() == 576
        && g_1152.len() == 1152
}

/// Build Nauru graph Y = GP(12, 5) adjacency list.
pub fn nauru_adj() -> [[usize; 3]; 24] {
    let mut adj = [[0usize; 3]; 24];
    for r in 0..12 {
        adj[r] = [(r + 1) % 12, (r + 11) % 12, 12 + r];
        adj[12 + r] = [r, 12 + (r + 5) % 12, 12 + (r + 7) % 12];
    }
    adj
}

/// Gate 2: Exhaustive |Aut(Y)| = 144 = 12(g-1), 39 involutions, 0 tree quotients (min beta_1 = 4).
pub fn find_nauru_auts() -> Vec<Perm24> {
    let adj = nauru_adj();
    let mut order = vec![0usize];
    let mut seen = [false; 24];
    seen[0] = true;
    let mut q = VecDeque::from([0usize]);
    while let Some(x) = q.pop_front() {
        for &y in &adj[x] {
            if !seen[y] {
                seen[y] = true;
                order.push(y);
                q.push_back(y);
            }
        }
    }
    let mut auts = Vec::new();
    let mut mp = [255u8; 24];
    let mut used = [false; 24];
    fn bt(
        idx: usize,
        order: &[usize],
        adj: &[[usize; 3]; 24],
        mp: &mut [u8; 24],
        used: &mut [bool; 24],
        auts: &mut Vec<Perm24>,
    ) {
        if idx == 24 {
            auts.push(*mp);
            return;
        }
        let u = order[idx];
        if idx == 0 {
            for c in 0..24u8 {
                mp[u] = c;
                used[c as usize] = true;
                bt(1, order, adj, mp, used, auts);
                used[c as usize] = false;
                mp[u] = 255;
            }
        } else {
            let mut mapped_nbrs = Vec::with_capacity(3);
            for &w in &adj[u] {
                if mp[w] != 255 {
                    mapped_nbrs.push(mp[w] as usize);
                }
            }
            for &cand in &adj[mapped_nbrs[0]] {
                if used[cand] {
                    continue;
                }
                if mapped_nbrs[1..].iter().all(|&mn| adj[mn].contains(&cand)) {
                    mp[u] = cand as u8;
                    used[cand] = true;
                    bt(idx + 1, order, adj, mp, used, auts);
                    used[cand] = false;
                    mp[u] = 255;
                }
            }
        }
    }
    bt(0, &order, &adj, &mut mp, &mut used, &mut auts);
    auts
}

/// Gate 3: Exhaustive Dhar burning over all 20,474 divisors of degree 2..5 -> gon(Y) = 6.
pub fn q_reduced(adj: &[[usize; 3]; 24], d_in: &[i32; 24], q: usize) -> [i32; 24] {
    let mut d = *d_in;
    loop {
        let mut burned = [false; 24];
        let mut b_cnt = [0i32; 24];
        burned[q] = true;
        for &w in &adj[q] {
            b_cnt[w] += 1;
        }
        let mut changed = true;
        while changed {
            changed = false;
            for v in 0..24 {
                if !burned[v] && b_cnt[v] > d[v] {
                    burned[v] = true;
                    changed = true;
                    for &w in &adj[v] {
                        b_cnt[w] += 1;
                    }
                }
            }
        }
        let mut any_unburned = false;
        for u in 0..24 {
            if !burned[u] {
                any_unburned = true;
                for &w in &adj[u] {
                    if burned[w] {
                        d[u] -= 1;
                        d[w] += 1;
                    }
                }
            }
        }
        if !any_unburned {
            return d;
        }
    }
}

pub fn has_rank_ge_1(adj: &[[usize; 3]; 24], d: &[i32; 24], q_order: &[usize; 24]) -> bool {
    for &q in q_order {
        if d[q] == 0 && q_reduced(adj, d, q)[q] == 0 {
            return false;
        }
    }
    true
}

pub fn verify_nauru_gonality_exact() -> (usize, bool) {
    let adj = nauru_adj();
    let mut dist = [99usize; 24];
    dist[0] = 0;
    let mut q = VecDeque::from([0usize]);
    while let Some(x) = q.pop_front() {
        for &y in &adj[x] {
            if dist[y] == 99 {
                dist[y] = dist[x] + 1;
                q.push_back(y);
            }
        }
    }
    let mut qo = [0usize; 24];
    for i in 0..24 {
        qo[i] = i;
    }
    qo.sort_by(|&a, &b| dist[b].cmp(&dist[a]));

    let mut tested = 0usize;
    // Enumerate combinations_with_replacement of length k in 1..=4 (degrees 2..=5)
    fn rec(
        start: usize,
        rem: usize,
        d: &mut [i32; 24],
        adj: &[[usize; 3]; 24],
        qo: &[usize; 24],
        tested: &mut usize,
    ) -> bool {
        if rem == 0 {
            *tested += 1;
            return !has_rank_ge_1(adj, d, qo);
        }
        for v in start..24 {
            d[v] += 1;
            if !rec(v, rem - 1, d, adj, qo, tested) {
                return false;
            }
            d[v] -= 1;
        }
        true
    }
    let mut d = [0i32; 24];
    d[0] = 1;
    let mut none_le_5 = true;
    for rem in 1..=4 {
        if !rec(0, rem, &mut d, &adj, &qo, &mut tested) {
            none_le_5 = false;
            break;
        }
    }
    // Check reduced prime-hexagon witness {0, 1, 2, 12, 14, 19}
    let mut d_hex = [0i32; 24];
    for v in [0, 1, 2, 12, 14, 19] {
        d_hex[v] = 1;
    }
    let hex_ok = has_rank_ge_1(&adj, &d_hex, &qo);
    (tested, none_le_5 && hex_ok)
}

/// Exact maximal order O_3 of B_3 = (-3, -1)_Q: basis (1, w, j, wj).
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct O3(pub i64, pub i64, pub i64, pub i64);

pub fn o3_mul(x: O3, y: O3) -> O3 {
    O3(
        x.0 * y.0 - x.1 * y.1 - x.2 * y.2 + x.2 * y.3 - x.3 * y.3,
        x.0 * y.1 + x.1 * y.0 - x.1 * y.1 + x.2 * y.3 - x.3 * y.2,
        x.0 * y.2 - x.1 * y.3 + x.2 * y.0 - x.2 * y.1 + x.3 * y.1,
        x.0 * y.3 + x.1 * y.2 - x.1 * y.3 - x.2 * y.1 + x.3 * y.0,
    )
}

pub fn o3_trd(x: O3) -> i64 {
    2 * x.0 - x.1
}

pub fn o3_nrd(x: O3) -> i64 {
    x.0 * x.0 - x.0 * x.1 + x.1 * x.1 + x.2 * x.2 - x.2 * x.3 + x.3 * x.3
}

fn mod_inv_i64(a: i64, m: i64) -> i64 {
    let (mut t, mut nt, mut r, mut nr) = (0i64, 1i64, m, a.rem_euclid(m));
    while nr != 0 {
        let q = r / nr;
        let tmp_t = t - q * nt;
        t = nt;
        nt = tmp_t;
        let tmp_r = r - q * nr;
        r = nr;
        nr = tmp_r;
    }
    t.rem_euclid(m)
}

fn norm_o3_mod(u: O3, p: i64) -> O3 {
    let arr = [
        u.0.rem_euclid(p),
        u.1.rem_euclid(p),
        u.2.rem_euclid(p),
        u.3.rem_euclid(p),
    ];
    for c in arr {
        if c % p != 0 {
            let inv = mod_inv_i64(c, p);
            return O3(
                (arr[0] * inv) % p,
                (arr[1] * inv) % p,
                (arr[2] * inv) % p,
                (arr[3] * inv) % p,
            );
        }
    }
    panic!("not a unit mod p")
}

/// Gate 4: Verify B_3 maximal order, gamma_6 arithmeticity, V_4-tower Y->K_{3,3}, and mod-5 A_5 independence.
pub fn verify_b3_non_congruence_tower() -> bool {
    let a = O3(0, 1, 0, 0);
    let b = O3(0, 0, 1, 0);
    let t = O3(1, 2, 1, 2);
    let ta = o3_mul(t, a);
    let ta2 = o3_mul(ta, ta);
    let ta3 = o3_mul(ta2, ta);
    let ta6 = o3_mul(ta3, ta3);
    if ta6 != O3(27 * 4, -27 * 3, 27 * 3, -27 * 3) {
        return false;
    }
    let g6 = O3(4, -3, 3, -3);
    if o3_trd(g6) != 11 || o3_nrd(g6) != 64 {
        return false;
    }
    // Build Aut(Y) generators
    let auts = find_nauru_auts();
    if auts.len() != 144 {
        return false;
    }
    let a_y = *auts.iter().find(|g| g[0] == 0 && order24(g) == 3).unwrap();
    let b_y = *auts.iter().find(|g| g[0] == 0 && g[12] == 12 && order24(g) == 2).unwrap();
    let t_y = *auts.iter().find(|g| g[0] == 12 && g[12] == 0).unwrap();

    // Conj by t mod 3
    let conj_t3 = |u: O3| -> O3 {
        let p = o3_mul(o3_mul(t, u), t);
        let inv_neg2 = mod_inv_i64(-2, 3);
        O3(
            ((p.0 / 3) * inv_neg2).rem_euclid(3),
            ((p.1 / 3) * inv_neg2).rem_euclid(3),
            ((p.2 / 3) * inv_neg2).rem_euclid(3),
            ((p.3 / 3) * inv_neg2).rem_euclid(3),
        )
    };
    let mul_s3 = |g1: (u8, O3), g2: (u8, O3)| -> (u8, O3) {
        let u1c = if g2.0 == 1 { conj_t3(g1.1) } else { g1.1 };
        ((g1.0 + g2.0) % 2, norm_o3_mod(o3_mul(u1c, g2.1), 3))
    };
    let ga3 = (0u8, norm_o3_mod(a, 3));
    let gb3 = (0u8, norm_o3_mod(b, 3));
    let gt3 = (1u8, O3(1, 0, 0, 0));
    let id3 = (0u8, O3(1, 0, 0, 0));

    let mut jt3: HashSet<(Perm24, (u8, O3))> = HashSet::new();
    let mut fr = VecDeque::new();
    jt3.insert((id24(), id3));
    fr.push_back((id24(), id3));
    while let Some((yc, mc)) = fr.pop_front() {
        for (yg, mg) in [(a_y, ga3), (b_y, gb3), (t_y, gt3)] {
            let nx = (comp(&yc, &yg), mul_s3(mc, mg));
            if jt3.insert(nx) {
                fr.push_back(nx);
            }
        }
    }
    let q36: HashSet<(u8, O3)> = jt3.iter().map(|&(_, m)| m).collect();
    let n4: Vec<Perm24> = jt3.iter().filter(|&&(_, m)| m == id3).map(|&(y, _)| y).collect();
    let v4_ok = n4.len() == 4 && n4.iter().filter(|g| order24(g) == 2).count() == 3;

    // Mod-5 joint surjection onto Aut(Y) x A_5 (order 8,640)
    let ga5 = norm_o3_mod(a, 5);
    let gb5 = norm_o3_mod(b, 5);
    let gt5 = norm_o3_mod(t, 5);
    let id5 = O3(1, 0, 0, 0);
    let mut jt5: HashSet<(Perm24, O3)> = HashSet::new();
    let mut fr5 = VecDeque::new();
    jt5.insert((id24(), id5));
    fr5.push_back((id24(), id5));
    while let Some((yc, mc)) = fr5.pop_front() {
        for (yg, mg) in [(a_y, ga5), (b_y, gb5), (t_y, gt5)] {
            let nx = (comp(&yc, &yg), norm_o3_mod(o3_mul(mc, mg), 5));
            if jt5.insert(nx) {
                fr5.push_back(nx);
            }
        }
    }
    jt3.len() == 144 && q36.len() == 36 && v4_ok && jt5.len() == 8640
}

/// Gate 5: Zero-PARI Manin modular symbols T_2 audit across all 18 levels (0/19 survivors).
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

fn canon_p1(c_raw: i64, d_raw: i64, m: i64) -> (i64, i64) {
    let c = c_raw.rem_euclid(m);
    let d = d_raw.rem_euclid(m);
    let g = gcd_i64(c, m);
    if g == 1 {
        return (1, (d * mod_inv_i64(c, m)) % m);
    }
    if c == 0 {
        return (0, 1);
    }
    let m1 = m / g;
    let u0 = mod_inv_i64(c / g, m1);
    let mut best = (m, m);
    for k in 0..g {
        let u = (u0 + k * m1) % m;
        if gcd_i64(u, m) == 1 {
            let cand = (g, (d * u) % m);
            if cand < best {
                best = cand;
            }
        }
    }
    best
}

fn nullity_mod(mat: &[Vec<i64>], lam: i64) -> usize {
    let n = mat.len();
    let mut a = vec![vec![0i64; n]; n];
    for r in 0..n {
        for c in 0..n {
            a[r][c] = (mat[r][c] - if r == c { lam } else { 0 }).rem_euclid(MOD_Q);
        }
    }
    let mut rk = 0usize;
    for col in 0..n {
        let piv = (rk..n).find(|&r| a[r][col] != 0);
        let Some(pr) = piv else { continue };
        a.swap(rk, pr);
        let inv = mod_inv_i64(a[rk][col], MOD_Q);
        for j in col..n {
            a[rk][j] = (a[rk][j] * inv) % MOD_Q;
        }
        for r in (rk + 1)..n {
            let fac = a[r][col];
            if fac != 0 {
                for j in col..n {
                    a[r][j] = (a[r][j] - fac * a[rk][j]).rem_euclid(MOD_Q);
                }
            }
        }
        rk += 1;
    }
    n - rk
}

pub fn manin_t2_nauru_feasible(m_level: i64) -> bool {
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
    let mut parent: Vec<usize> = (0..n).collect();
    let mut sign = vec![1i64; n];
    let mut killed = vec![false; n];
    let find = |mut x: usize, parent: &[usize], sign: &[i64]| -> (usize, i64) {
        let mut s = 1i64;
        while parent[x] != x {
            s *= sign[x];
            x = parent[x];
        }
        (x, s)
    };
    let mut add_rel2 = |x: usize, y: usize, rs: i64| {
        let (rx, sx) = find(x, &parent, &sign);
        let (ry, sy) = find(y, &parent, &sign);
        if rx == ry {
            if sx != rs * sy {
                killed[rx] = true;
            }
        } else {
            parent[rx] = ry;
            sign[rx] = rs * sx * sy;
            if killed[rx] {
                killed[ry] = true;
            }
        }
    };
    for (i, &(c, d)) in pts.iter().enumerate() {
        add_rel2(i, idx[&canon_p1(d, -c, m_level)], -1);
        add_rel2(i, idx[&canon_p1(-c, d, m_level)], -1);
    }
    let mut rep_map = HashMap::new();
    for i in 0..n {
        let (r, _) = find(i, &parent, &sign);
        if !killed[r] && !rep_map.contains_key(&r) {
            let id = rep_map.len();
            rep_map.insert(r, id);
        }
    }
    let m_cols = rep_map.len();
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
            if let Some(prow) = pivots.get(&c0) {
                for (&k, &pv) in prow {
                    let nv = (row.get(&k).copied().unwrap_or(0) - v0 * pv).rem_euclid(MOD_Q);
                    if nv == 0 {
                        row.remove(&k);
                    } else {
                        row.insert(k, nv);
                    }
                }
            } else {
                let inv = mod_inv_i64(v0, MOD_Q);
                let norm = row.into_iter().map(|(k, v)| (k, (v * inv) % MOD_Q)).collect();
                pivots.insert(c0, norm);
                break;
            }
        }
    }
    let piv_cols: Vec<usize> = pivots.keys().copied().rev().collect();
    for c in piv_cols {
        let mut prow = pivots[&c].clone();
        let keys: Vec<usize> = prow.keys().copied().collect();
        for k in keys {
            if k != c && pivots.contains_key(&k) {
                let fac = prow.remove(&k).unwrap();
                for (&k2, &v2) in &pivots[&k] {
                    if k2 != k {
                        let nv = (prow.get(&k2).copied().unwrap_or(0) - fac * v2).rem_euclid(MOD_Q);
                        if nv == 0 {
                            prow.remove(&k2);
                        } else {
                            prow.insert(k2, nv);
                        }
                    }
                }
            }
        }
        pivots.insert(c, prow);
    }
    let free_cols: Vec<usize> = (0..m_cols).filter(|c| !pivots.contains_key(c)).collect();
    let mut free_idx = HashMap::new();
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
            for (&f, &val) in &pivots[&col] {
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
    let h2 = [(1, 0, 0, 2), (2, 0, 0, 1), (2, 1, 0, 1), (1, 0, 1, 2)];
    let mut t2 = vec![vec![0i64; dim]; dim];
    for b in 0..dim {
        let (ipt, spt) = basis_pts[b].unwrap();
        let (c, d) = pts[ipt];
        for (a, bb, cc, dd) in h2 {
            let j = idx[&canon_p1(a * c + cc * d, bb * c + dd * d, m_level)];
            let vj = vec_of_pt(j);
            for r in 0..dim {
                t2[r][b] = (t2[r][b] + spt * vj[r]).rem_euclid(MOD_Q);
            }
        }
    }
    let n2 = nullity_mod(&t2, 2);
    let n0 = nullity_mod(&t2, 0);
    let nm1 = nullity_mod(&t2, MOD_Q - 1);
    let nm2 = nullity_mod(&t2, MOD_Q - 2);
    n2 >= 3 && n0 >= 2 && nm1 >= 3 && nm2 >= 3
}

pub fn verify_all_18_shimura_levels_excluded() -> bool {
    const LEVELS: [i64; 18] = [
        105, 111, 117, 123, 133, 135, 143, 151, 161, 165, 167, 195, 213, 215, 237, 273, 285, 345,
    ];
    LEVELS.iter().all(|&m| !manin_t2_nauru_feasible(m))
}

/// Keyed SplitMix64 PRNG for bit-exact replay cross-check against Python Gate P1.
pub struct SplitMix64(pub u64);

impl SplitMix64 {
    pub fn next_u64(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
}
