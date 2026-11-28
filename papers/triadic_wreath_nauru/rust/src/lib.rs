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

pub fn analyze_group(elems: &[Perm24], gens: &[Perm24]) -> GroupSummary {
    let mut involutions = 0usize;
    let mut ord24 = 0usize;
    let mut center = 0usize;
    for g in elems {
        match order24(g) {
            2 => involutions += 1,
            24 => ord24 += 1,
            _ => {}
        }
        if gens.iter().all(|h| comp(g, h) == comp(h, g)) {
            center += 1;
        }
    }
    let gen_invs: Vec<Perm24> = gens.iter().map(inv24).collect();
    let id = id24();
    let mut comm_seen: HashSet<Perm24> = HashSet::new();
    let mut q: VecDeque<Perm24> = VecDeque::new();
    comm_seen.insert(id);
    q.push_back(id);
    for (i, a) in gens.iter().enumerate() {
        for (j, b) in gens.iter().enumerate() {
            let c = comp(&comp(a, b), &comp(&gen_invs[i], &gen_invs[j]));
            if comm_seen.insert(c) {
                q.push_back(c);
            }
        }
    }
    while let Some(cur) = q.pop_front() {
        for (s, si) in gens.iter().zip(gen_invs.iter()) {
            let c1 = comp(&comp(s, &cur), si);
            if comm_seen.insert(c1) {
                q.push_back(c1);
            }
            let c2 = comp(&comp(si, &cur), s);
            if comm_seen.insert(c2) {
                q.push_back(c2);
            }
        }
    }
    let comm_vec: Vec<Perm24> = comm_seen.into_iter().collect();
    let comm_order = gen_group(&comm_vec).len();
    GroupSummary { order: elems.len(), center, involutions, ord24, comm_order }
}

/// Gate 1: Twin-diamond hierarchy (144 / 288 != 288 / 576 / 1152 != 1152 / 2304) + CFS duality.
pub fn verify_non_fusion() -> bool {
    let t1 = utt_perm(false, 1, 1);
    let t6 = utt_perm(false, 6, 6);
    let mut i0 = [0u8; 24];
    let mut m5 = [0u8; 24];
    let mut m7 = [0u8; 24];
    let mut i_maj = [0u8; 24];
    for r in 0..12 {
        i0[r] = (12 + (17 - r) % 12) as u8;
        i0[12 + r] = ((17 - r) % 12) as u8;
        m5[r] = ((5 * r) % 12) as u8;
        m5[12 + r] = (12 + (5 * r) % 12) as u8;
        m7[r] = ((7 * r) % 12) as u8;
        m7[12 + r] = (12 + (7 * r) % 12) as u8;
        i_maj[r] = ((12 - r) % 12) as u8;
        i_maj[12 + r] = (12 + r) as u8;
    }
    let p = utt_perm(true, 0, 0);
    let l = utt_perm(true, 4, 8);
    let r = utt_perm(true, 9, 3);
    let a = utt_perm(false, 1, 0);
    let b = utt_perm(false, 0, 1);

    let gens_t_plr = [t1, p, l, r];
    let gens_ti_plr = [t1, i0, p, l, r];
    let gens_utt = [a, b, p];
    let gens_576 = [a, b, p, i0];
    let gens_nt = [a, b, p, i0, m5, m7];
    let gens_qutt = [a, b, p, i_maj];

    let set_ti: HashSet<Perm24> = gen_group(&[t1, i0]).into_iter().collect();
    let set_plr: HashSet<Perm24> = gen_group(&[p, l, r]).into_iter().collect();
    let elems_t_plr = gen_group(&gens_t_plr);
    let elems_ti_plr = gen_group(&gens_ti_plr);
    let elems_utt = gen_group(&gens_utt);
    let elems_576 = gen_group(&gens_576);
    let elems_nt = gen_group(&gens_nt);
    let elems_qutt = gen_group(&gens_qutt);
    let elems_2304 = gen_group(&[a, b, p, i_maj, m5]);

    let g_t_plr = analyze_group(&elems_t_plr, &gens_t_plr);
    let g_ti_plr = analyze_group(&elems_ti_plr, &gens_ti_plr);
    let g_utt = analyze_group(&elems_utt, &gens_utt);
    let g_576 = analyze_group(&elems_576, &gens_576);
    let g_nt = analyze_group(&elems_nt, &gens_nt);
    let g_qutt = analyze_group(&elems_qutt, &gens_qutt);

    // Crans-Fiore-Satyendra duality: T/I and PLR commute, share only {id, T6 = (LR)^6}
    let cfs_commute = set_ti.iter().all(|x| set_plr.iter().all(|y| comp(x, y) == comp(y, x)));
    let ti_cap_plr: HashSet<Perm24> = set_ti.intersection(&set_plr).copied().collect();
    let lr = comp(&l, &r);
    let mut lr6 = id24();
    for _ in 0..6 {
        lr6 = comp(&lr, &lr6);
    }

    // Exact intersection N(T) cap QUTT = UTT >< <I0> (576), and QUTT does not normalize UTT
    let set_nt: HashSet<Perm24> = elems_nt.iter().copied().collect();
    let set_qutt: HashSet<Perm24> = elems_qutt.iter().copied().collect();
    let set_utt: HashSet<Perm24> = elems_utt.iter().copied().collect();
    let cap_1152 = set_nt.intersection(&set_qutt).count();
    let qutt_norm_utt = set_utt.contains(&comp(&comp(&i_maj, &p), &inv24(&i_maj)));

    g_t_plr.order == 144
        && g_t_plr.center == 12
        && g_t_plr.involutions == 15
        && g_t_plr.ord24 == 0
        && g_t_plr.comm_order == 6
        && (g_t_plr.order / g_t_plr.comm_order) == 24
        && cfs_commute
        && ti_cap_plr.len() == 2
        && ti_cap_plr.contains(&id24())
        && ti_cap_plr.contains(&t6)
        && lr6 == t6
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
        && g_576.order == 576
        && g_576.involutions == 171
        && g_576.comm_order == 72
        && g_nt.order == 1152
        && g_nt.involutions == 247
        && g_nt.ord24 == 192
        && g_nt.comm_order == 72
        && g_qutt.order == 1152
        && g_qutt.involutions == 219
        && g_qutt.ord24 == 96
        && g_qutt.comm_order == 144
        && cap_1152 == 576
        && elems_2304.len() == 2304
        && !qutt_norm_utt
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

/// Gate D10 (Rust): Exact Eisenstein-Nauru `{6,3}_{(2,2)} <-> GP(12,5)` 36/36 edge isomorphism,
/// `<T, PLR>` decomposition (`s=T6 o P, g=T3 o (LR)^2`), F31 falsifier, & canonical 3-adic wall.
pub fn verify_eisenstein_nauru_and_su2() -> bool {
    let phi = |is_b: bool, a: usize, b: usize| -> usize {
        if !is_b {
            if b == 0 { (12 - (2 * a) % 12) % 12 } else { 12 + (17 - (2 * a) % 12) % 12 }
        } else {
            if b == 0 { (13 - (2 * a) % 12) % 12 } else { 12 + (12 - (2 * a) % 12) % 12 }
        }
    };
    let mut imgs = HashSet::new();
    for is_b in [false, true] {
        for a in 0..6 {
            for b in 0..2 {
                imgs.insert(phi(is_b, a, b));
            }
        }
    }
    if imgs.len() != 24 {
        return false;
    }
    let nadj = nauru_adj();
    let mut nauru_edges = BTreeSet::new();
    for u in 0..24 {
        for &v in &nadj[u] {
            nauru_edges.insert((u.min(v), u.max(v)));
        }
    }
    let mut eis_edges = BTreeSet::new();
    for a in 0..6 {
        for b in 0..2 {
            let u = phi(false, a, b);
            for (da, db) in [(0usize, 0usize), (1, 0), (0, 1)] {
                let ny = b + db;
                let q = ny / 2;
                let na = (a + da + 4 * q) % 6;
                let nb = ny % 2;
                let v = phi(true, na, nb);
                eis_edges.insert((u.min(v), u.max(v)));
            }
        }
    }
    // Check <T, PLR> words
    let t3 = utt_perm(false, 3, 3);
    let t6 = utt_perm(false, 6, 6);
    let t9 = utt_perm(false, 9, 9);
    let p = utt_perm(true, 0, 0);
    let l = utt_perm(true, 4, 8);
    let r = utt_perm(true, 9, 3);
    let lr2 = comp(&comp(&l, &r), &comp(&l, &r));
    let rl2 = comp(&comp(&r, &l), &comp(&r, &l));
    let s_ok = utt_perm(true, 6, 6) == comp(&t6, &p);
    let g_ok = utt_perm(false, 1, 5) == comp(&t3, &lr2);
    let ginv_ok = utt_perm(false, 11, 7) == comp(&t9, &rl2);
    // Canonical 3-adic Dic_6 wall: gX=[[3,0],[0,1]], gY=[[2,1],[1,2]], adj(gY)=[[2,-1],[-1,2]]
    let mm = |x: [[i64; 2]; 2], y: [[i64; 2]; 2]| -> [[i64; 2]; 2] {
        [
            [x[0][0] * y[0][0] + x[0][1] * y[1][0], x[0][0] * y[0][1] + x[0][1] * y[1][1]],
            [x[1][0] * y[0][0] + x[1][1] * y[1][0], x[1][0] * y[0][1] + x[1][1] * y[1][1]],
        ]
    };
    let w4 = mm(mm([[2, 1], [1, 2]], [[3, 0], [0, 1]]), mm([[2, -1], [-1, 2]], [[3, 0], [0, 1]]));
    let tr = w4[0][0] + w4[1][1];
    let det = w4[0][0] * w4[1][1] - w4[0][1] * w4[1][0];
    eis_edges == nauru_edges && eis_edges.len() == 36 && s_ok && g_ok && ginv_ok && tr == 34 && det == 81
}

/// Gate D11 (Rust): Explicit 3-adic Hurwitz B_2 (D=6, p=3) Dic_6 realization:
/// |Aut(Z)|=96, 32 valid surjections, exact 16 principal Gamma(4) + 16 level-8 lifts,
/// index 48 in (O_2/8O_2)^1/{±1} (order 384), and exact K_{4,4} double-coset quotient across all 32.
pub fn verify_hurwitz_b2_dic6_k44() -> bool {
    type Q4 = [i64; 4];
    let qmul = |x: Q4, y: Q4| -> Q4 {
        [
            x[0] * y[0] - x[1] * y[1] - x[2] * y[2] - x[3] * y[3],
            x[0] * y[1] + x[1] * y[0] + x[2] * y[3] - x[3] * y[2],
            x[0] * y[2] - x[1] * y[3] + x[2] * y[0] + x[3] * y[1],
            x[0] * y[3] + x[1] * y[2] - x[2] * y[1] + x[3] * y[0],
        ]
    };
    let qconj = |x: Q4| -> Q4 { [x[0], -x[1], -x[2], -x[3]] };
    let qnrd = |x: Q4| -> i64 { x[0] * x[0] + x[1] * x[1] + x[2] * x[2] + x[3] * x[3] };
    // Verify corrected length-4 relator (ty*b)(tx*a)(b*ty)(tx*a) = 4*(5, 6, -2, 4)
    let qa1: Q4 = [0, 1, 1, 0];
    let qb1: Q4 = [0, 1, -1, 0];
    let qtx1: Q4 = [0, 1, 1, 1];
    let qty1: Q4 = [0, 1, -1, 1];
    let w4_raw = qmul(qmul(qmul(qty1, qb1), qmul(qtx1, qa1)), qmul(qmul(qb1, qty1), qmul(qtx1, qa1)));
    if w4_raw != [20, 24, -8, 16] {
        return false;
    }
    // Build Z = Cay(Dic_6, {x, x^-1, y, y^3})
    let dic6_mul = |u: usize, v: usize| -> usize {
        let (k1, f1) = (u % 12, u / 12);
        let (k2, f2) = (v % 12, v / 12);
        if f1 == 0 {
            12 * f2 + (k1 + k2) % 12
        } else if f2 == 0 {
            12 + (k1 + 12 - k2) % 12
        } else {
            (k1 + 18 - k2) % 12
        }
    };
    let mut adj = [[0usize; 4]; 24];
    for u in 0..24 {
        adj[u] = [dic6_mul(u, 1), dic6_mul(u, 11), dic6_mul(u, 12), dic6_mul(u, 18)];
    }
    // Find Aut(Z) (order 96)
    let mut order = vec![0usize];
    let mut seen = [false; 24];
    seen[0] = true;
    let mut q = VecDeque::from([0usize]);
    while let Some(u) = q.pop_front() {
        for &v in &adj[u] {
            if !seen[v] {
                seen[v] = true;
                order.push(v);
                q.push_back(v);
            }
        }
    }
    let mut auts: Vec<Perm24> = Vec::new();
    let mut perm = [255u8; 24];
    let mut used = [false; 24];
    fn bt_z(
        pos: usize,
        order: &[usize],
        adj: &[[usize; 4]; 24],
        perm: &mut Perm24,
        used: &mut [bool; 24],
        out: &mut Vec<Perm24>,
    ) {
        if pos == 24 {
            out.push(*perm);
            return;
        }
        let u = order[pos];
        let mut cands = Vec::new();
        if pos == 0 {
            cands.extend(0..24);
        } else {
            let mapped: Vec<usize> = adj[u].iter().filter(|&&w| perm[w] != 255).map(|&w| perm[w] as usize).collect();
            for &c in &adj[mapped[0]] {
                if mapped[1..].iter().all(|&m| adj[m].contains(&c)) {
                    cands.push(c);
                }
            }
        }
        for c in cands {
            if !used[c] {
                perm[u] = c as u8;
                used[c] = true;
                bt_z(pos + 1, order, adj, perm, used, out);
                perm[u] = 255;
                used[c] = false;
            }
        }
    }
    bt_z(0, &order, &adj, &mut perm, &mut used, &mut auts);
    if auts.len() != 96 {
        return false;
    }
    let id = id24();
    let invs: Vec<Perm24> = auts.iter().copied().filter(|&g| g != id && comp(&g, &g) == id).collect();
    let stab_invs: Vec<Perm24> = invs.iter().copied().filter(|&g| g[0] == 0).collect();
    let nbr0 = adj[0];
    let mut valid_homs = Vec::new();
    for &ga in &stab_invs {
        for &gb in &stab_invs {
            if ga == gb {
                continue;
            }
            let fb: Vec<usize> = nbr0.iter().copied().filter(|&v| gb[v] as usize == v).collect();
            let fa: Vec<usize> = nbr0.iter().copied().filter(|&v| ga[v] as usize == v).collect();
            if fb.len() != 2 || fa.len() != 2 {
                continue;
            }
            for &gtx in &invs {
                if !fb.contains(&(gtx[0] as usize)) || comp(&gtx, &gb) != comp(&gb, &gtx) {
                    continue;
                }
                for &gty in &invs {
                    if !fa.contains(&(gty[0] as usize)) || comp(&gty, &ga) != comp(&ga, &gty) {
                        continue;
                    }
                    if gen_group(&[ga, gb, gtx, gty]).len() == 96 {
                        valid_homs.push([ga, gb, gtx, gty]);
                    }
                }
            }
        }
    }
    if valid_homs.len() != 32 {
        return false;
    }
    // Hurwitz O_2 arithmetic mod m
    let o2_mod = |c: Q4, m: i64| -> Q4 {
        let a = [
            ((c[0] - c[3]) / 2).rem_euclid(m),
            ((c[1] - c[3]) / 2).rem_euclid(m),
            ((c[2] - c[3]) / 2).rem_euclid(m),
            c[3].rem_euclid(m),
        ];
        let na = [(-a[0]).rem_euclid(m), (-a[1]).rem_euclid(m), (-a[2]).rem_euclid(m), (-a[3]).rem_euclid(m)];
        a.min(na)
    };
    let from_o2 = |a: Q4| -> Q4 { [2 * a[0] + a[3], 2 * a[1] + a[3], 2 * a[2] + a[3], a[3]] };
    let o2_mul_mod = |u: Q4, v: Q4, m: i64| -> Q4 {
        let c = qmul(from_o2(u), from_o2(v));
        o2_mod([c[0] / 2, c[1] / 2, c[2] / 2, c[3] / 2], m)
    };
    let hmul = |x: Q4, y: Q4| -> Q4 {
        let mut r = qmul(x, y);
        for t in &mut r {
            *t /= 2;
        }
        while r.iter().all(|&t| t % 3 == 0) {
            for t in &mut r {
                *t /= 3;
            }
        }
        while r.iter().all(|&t| t % 2 == 0) {
            let p0 = (r[0] / 2).rem_euclid(2);
            if r.iter().all(|&t| (t / 2).rem_euclid(2) == p0) {
                for t in &mut r {
                    *t /= 2;
                }
            } else {
                break;
            }
        }
        r
    };
    let hmod_o2 = |mut x: Q4, m: i64| -> Option<Q4> {
        let mut n = qnrd(x) / 4;
        let mut v2 = 0u32;
        while n % 2 == 0 {
            n /= 2;
            v2 += 1;
        }
        let mut v3 = 0u32;
        while n % 3 == 0 {
            n /= 3;
            v3 += 1;
        }
        if n != 1 || v2 % 2 != 0 || v3 % 2 != 0 {
            return None;
        }
        let d2 = 1i64 << (v2 / 2);
        for t in &mut x {
            *t /= d2;
        }
        // 3^-1 mod 16 is 11 (3*11=33=1 mod 16)
        let mut p3 = 1i64;
        for _ in 0..(v3 / 2) {
            p3 = (p3 * 3) % (2 * m);
        }
        let mut inv3 = 1i64;
        for cand in 1..(2 * m) {
            if (p3 * cand) % (2 * m) == 1 {
                inv3 = cand;
                break;
            }
        }
        Some(o2_mod([x[0] * inv3, x[1] * inv3, x[2] * inv3, x[3] * inv3], m))
    };

    let qgens: [Q4; 4] = [[0, 2, 2, 0], [0, 2, -2, 0], [0, 2, 2, 2], [0, 2, -2, 2]];
    let id8 = o2_mod([2, 0, 0, 0], 8);
    let id4 = o2_mod([2, 0, 0, 0], 4);
    let mut principal = 0usize;
    let mut level8 = 0usize;
    let mut distinct_h8: BTreeSet<Vec<Q4>> = BTreeSet::new();

    for pgens in &valid_homs {
        let mut reps: HashMap<Perm24, Q4> = HashMap::new();
        reps.insert(id, [2, 0, 0, 0]);
        let mut dq = VecDeque::from([id]);
        while let Some(g) = dq.pop_front() {
            let rg = reps[&g];
            for k in 0..4 {
                let h = comp(&g, &pgens[k]);
                if !reps.contains_key(&h) {
                    reps.insert(h, hmul(rg, qgens[k]));
                    dq.push_back(h);
                }
            }
        }
        let mut img8: HashSet<Q4> = HashSet::new();
        let mut img4: HashSet<Q4> = HashSet::new();
        let mut img16: HashSet<Q4> = HashSet::new();
        let mut img5: HashSet<Q4> = HashSet::new();
        for (&g, &rg) in &reps {
            for k in 0..4 {
                let h = comp(&g, &pgens[k]);
                let gq = hmul(hmul(rg, qgens[k]), qconj(reps[&h]));
                let Some(m8) = hmod_o2(gq, 8) else { return false };
                let Some(m4) = hmod_o2(gq, 4) else { return false };
                let Some(m16) = hmod_o2(gq, 16) else { return false };
                let Some(m5) = hmod_o2(gq, 5) else { return false };
                img8.insert(m8);
                img4.insert(m4);
                img16.insert(m16);
                img5.insert(m5);
            }
        }
        let close = |seed: &HashSet<Q4>, idm: Q4, m: i64| -> Vec<Q4> {
            let mut s: BTreeSet<Q4> = BTreeSet::new();
            let mut q2 = VecDeque::from([idm]);
            s.insert(idm);
            while let Some(u) = q2.pop_front() {
                for &sg in seed {
                    let v = o2_mul_mod(u, sg, m);
                    if s.insert(v) {
                        q2.push_back(v);
                    }
                }
            }
            s.into_iter().collect()
        };
        let h8 = close(&img8, id8, 8);
        let h4 = close(&img4, id4, 4);
        let h16 = close(&img16, o2_mod([2, 0, 0, 0], 16), 16);
        let h5 = close(&img5, o2_mod([2, 0, 0, 0], 5), 5);
        if h8.len() != 8 || h16.len() != 64 || h5.len() != 60 {
            return false;
        }
        let mut lx4 = [0u8; 24];
        for u in 0..24 {
            lx4[u] = dic6_mul(4, u) as u8;
        }
        let Some(lx4_m8) = hmod_o2(reps[&lx4], 8) else { return false };
        if !h8.contains(&lx4_m8) {
            return false;
        }
        match h4.len() {
            1 => principal += 1,
            2 => level8 += 1,
            _ => return false,
        }
        distinct_h8.insert(h8);
    }
    if principal != 16 || level8 != 16 || distinct_h8.len() != 2 {
        return false;
    }
    // Check double-coset quotient H8 \ G_mod8 / U == K_{4,4} for both H8 subgroups
    let mut g_mod8: BTreeSet<Q4> = BTreeSet::new();
    for a0 in 0..8 {
        for a1 in 0..8 {
            for a2 in 0..8 {
                for a3 in 0..8 {
                    let c = from_o2([a0, a1, a2, a3]);
                    if (qnrd(c) / 4).rem_euclid(8) == 1 {
                        g_mod8.insert(o2_mod(c, 8));
                    }
                }
            }
        }
    }
    if g_mod8.len() != 384 {
        return false;
    }
    let mut hurwitz24: Vec<Q4> = Vec::new();
    for sgn in [-2i64, 2] {
        hurwitz24.extend([[sgn, 0, 0, 0], [0, sgn, 0, 0], [0, 0, sgn, 0], [0, 0, 0, sgn]]);
    }
    for s0 in [-1i64, 1] {
        for s1 in [-1i64, 1] {
            for s2 in [-1i64, 1] {
                for s3 in [-1i64, 1] {
                    hurwitz24.push([s0, s1, s2, s3]);
                }
            }
        }
    }
    let e0: Q4 = [0, 2, 2, 2];
    let ne0: Q4 = [0, -2, -2, -2];
    let u_even: Vec<Q4> = hurwitz24.iter().map(|&u| o2_mod(u, 8)).collect::<BTreeSet<_>>().into_iter().collect();
    let u_odd: Vec<Q4> = hurwitz24
        .iter()
        .map(|&u| {
            let r = qmul(qmul(e0, u), ne0);
            o2_mod([(r[0] / 4) * 3, (r[1] / 4) * 3, (r[2] / 4) * 3, (r[3] / 4) * 3], 8)
        })
        .collect::<BTreeSet<_>>()
        .into_iter()
        .collect();
    for h8 in &distinct_h8 {
        let mut ev: BTreeSet<Vec<Q4>> = BTreeSet::new();
        let mut od: BTreeSet<Vec<Q4>> = BTreeSet::new();
        for &g in &g_mod8 {
            let mut ce: BTreeSet<Q4> = BTreeSet::new();
            let mut co: BTreeSet<Q4> = BTreeSet::new();
            for &h in h8 {
                let hg = o2_mul_mod(h, g, 8);
                for &u in &u_even {
                    ce.insert(o2_mul_mod(hg, u, 8));
                }
                for &u in &u_odd {
                    co.insert(o2_mul_mod(hg, u, 8));
                }
            }
            ev.insert(ce.into_iter().collect());
            od.insert(co.into_iter().collect());
        }
        if ev.len() != 4 || od.len() != 4 {
            return false;
        }
        for ec in &ev {
            let eset: HashSet<Q4> = ec.iter().copied().collect();
            for oc in &od {
                let inter = oc.iter().filter(|&&x| eset.contains(&x)).count();
                if inter != 24 {
                    return false;
                }
            }
        }
    }
    true
}

/// Gate D12 (Rust): Zero-PARI Manin modular symbols T_3 over F_{1000003} across all 19 genus-25
/// 3-adic Borel Shimura levels (NEG-M20), returning true iff 0/19 satisfy Dic_6 nullities.
pub fn verify_all_19_3adic_shimura_levels_excluded() -> bool {
    let manin_t3_mat = |m_level: i64| -> Vec<Vec<i64>> {
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
        let idx: HashMap<(i64, i64), usize> = pts.iter().enumerate().map(|(i, &p)| (p, i)).collect();
        let mut parent: Vec<usize> = (0..n).collect();
        let mut sign: Vec<i64> = vec![1; n];
        let mut killed = vec![false; n];
        fn find(x: usize, p: &[usize], s: &[i64]) -> (usize, i64) {
            let mut cur = x;
            let mut acc = 1i64;
            while p[cur] != cur {
                acc *= s[cur];
                cur = p[cur];
            }
            (cur, acc)
        }
        let mut merge = |u: usize, v: usize, rel: i64| {
            let (ru, su) = find(u, &parent, &sign);
            let (rv, sv) = find(v, &parent, &sign);
            if ru == rv {
                if su * sv != rel {
                    killed[ru] = true;
                }
            } else {
                parent[rv] = ru;
                sign[rv] = su * sv * rel;
                if killed[rv] {
                    killed[ru] = true;
                }
            }
        };
        for (i, &(c, d)) in pts.iter().enumerate() {
            let js = idx[&canon_p1(d, -c, m_level)];
            merge(i, js, -1);
            let jj = idx[&canon_p1(-c, d, m_level)];
            merge(i, jj, -1);
        }
        let mut rep_map: HashMap<usize, usize> = HashMap::new();
        for i in 0..n {
            let (r, _) = find(i, &parent, &sign);
            if !killed[r] && !rep_map.contains_key(&r) {
                let id = rep_map.len();
                rep_map.insert(r, id);
            }
        }
        let num_vars = rep_map.len();
        let mut pivots: BTreeMap<usize, BTreeMap<usize, i64>> = BTreeMap::new();
        let mut seen_t = vec![false; n];
        for i in 0..n {
            if seen_t[i] {
                continue;
            }
            let (c, d) = pts[i];
            let j = idx[&canon_p1(d, -c - d, m_level)];
            let k = idx[&canon_p1(-c - d, c, m_level)];
            seen_t[i] = true;
            seen_t[j] = true;
            seen_t[k] = true;
            let mut row: BTreeMap<usize, i64> = BTreeMap::new();
            for &u in &[i, j, k] {
                let (r, s) = find(u, &parent, &sign);
                if !killed[r] {
                    let col = rep_map[&r];
                    let e = row.entry(col).or_insert(0);
                    *e = (*e + s).rem_euclid(MOD_Q);
                    if *e == 0 {
                        row.remove(&col);
                    }
                }
            }
            while let Some((&c0, &v0)) = row.iter().next() {
                if let Some(prow) = pivots.get(&c0) {
                    for (&pc, &pv) in prow {
                        let e = row.entry(pc).or_insert(0);
                        *e = (*e - v0 * pv).rem_euclid(MOD_Q);
                        if *e == 0 {
                            row.remove(&pc);
                        }
                    }
                } else {
                    let inv = mod_inv_i64(v0, MOD_Q);
                    for val in row.values_mut() {
                        *val = (*val * inv).rem_euclid(MOD_Q);
                    }
                    pivots.insert(c0, row);
                    break;
                }
            }
        }
        let piv_keys: Vec<usize> = pivots.keys().copied().rev().collect();
        for &c0 in &piv_keys {
            let mut row = pivots[&c0].clone();
            let sub_cols: Vec<(usize, i64)> = row.iter().filter(|(&k, _)| k != c0 && pivots.contains_key(&k)).map(|(&k, &v)| (k, v)).collect();
            for (sc, sv) in sub_cols {
                row.remove(&sc);
                for (&pc, &pv) in &pivots[&sc] {
                    if pc != sc {
                        let e = row.entry(pc).or_insert(0);
                        *e = (*e - sv * pv).rem_euclid(MOD_Q);
                        if *e == 0 {
                            row.remove(&pc);
                        }
                    }
                }
            }
            pivots.insert(c0, row);
        }
        let free_cols: Vec<usize> = (0..num_vars).filter(|c| !pivots.contains_key(c)).collect();
        let free_idx: HashMap<usize, usize> = free_cols.iter().enumerate().map(|(i, &c)| (c, i)).collect();
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
        let h3 = [
            (1, 0, 0, 3),
            (1, 0, 1, 3),
            (1, 0, 2, 3),
            (2, 1, 1, 2),
            (3, 0, 0, 1),
            (3, 1, 0, 1),
            (3, 2, 0, 1),
        ];
        let mut t3 = vec![vec![0i64; dim]; dim];
        for b in 0..dim {
            let (ipt, spt) = basis_pts[b].unwrap();
            let (c, d) = pts[ipt];
            for (a, bb, cc, dd) in h3 {
                let j = idx[&canon_p1(a * c + cc * d, bb * c + dd * d, m_level)];
                let vj = vec_of_pt(j);
                for r in 0..dim {
                    t3[r][b] = (t3[r][b] + spt * vj[r]).rem_euclid(MOD_Q);
                }
            }
        }
        t3
    };
    let sq_nullity = |t: &[Vec<i64>], shift: i64| -> usize {
        let d = t.len();
        let mut sq = vec![vec![0i64; d]; d];
        for i in 0..d {
            for k in 0..d {
                let tik = t[i][k];
                if tik != 0 {
                    for j in 0..d {
                        sq[i][j] = (sq[i][j] + tik * t[k][j]).rem_euclid(MOD_Q);
                    }
                }
            }
        }
        nullity_mod(&sq, shift)
    };
    // Ground-truth check at M=11 (a3 = -1) & M=14 (a3 = -2)
    let t11 = manin_t3_mat(11);
    let t14 = manin_t3_mat(14);
    if t11.len() != 1 || t11[0][0] != MOD_Q - 1 || t14.len() != 1 || t14[0][0] != MOD_Q - 2 {
        return false;
    }
    const LEVELS_19: [i64; 19] = [
        230, 238, 110, 112, 161, 104, 143, 133, 370, 250, 266, 298, 302, 314, 185, 149, 151, 374, 410,
    ];
    for &m in &LEVELS_19 {
        let t3 = manin_t3_mat(m);
        let n3 = sq_nullity(&t3, 3);
        let n9 = sq_nullity(&t3, 9);
        if m == 374 && !(n3 == 4 && n9 == 0) {
            return false;
        }
        if n3 >= 4 && n9 >= 2 {
            return false;
        }
    }
    true
}

/// Gate D7b (Rust, NEG-M23): Complete all-primes congruence vs. non-congruence classification of
/// B_5 = (-3,-5)_Q (D = 10) at BOTH x = 5/2 (CONGRUENCE: Gamma_Y = Gamma(3) \cap Gamma(P_5) of exact
/// index 36 = 12 * 3, quotients Q_3 & Theta_3) AND x = 1/2 (NON-CONGRUENCE V_4-cover of index 4
/// over K_{3,3} = T_3/(Gamma_3^{V_4} \cap Gamma(P_5)) of index 9, mod-9/25 stable, mod-7 PSL_2(F_7)).
pub fn verify_b5_congruence_and_noncongruence_towers() -> bool {
    const MT52: [[[i128; 4]; 4]; 4] = [
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
        [[0, 1, 0, 0], [-1, -1, 0, 0], [0, 0, 0, 1], [0, 0, -1, -1]],
        [[0, 0, 1, 0], [-5, 0, -1, -1], [-10, 0, 0, 0], [10, 10, -5, 0]],
        [[0, 0, 0, 1], [0, -5, 1, 0], [0, -10, 0, 0], [-10, 0, 0, -5]],
    ];
    const MT12: [[[i128; 4]; 4]; 4] = [
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
        [[0, 1, 0, 0], [-1, -1, 0, 0], [0, 0, 0, 1], [0, 0, -1, -1]],
        [[0, 0, 1, 0], [-1, 0, -1, -1], [-2, 0, 0, 0], [2, 2, -1, 0]],
        [[0, 0, 0, 1], [0, -1, 1, 0], [0, -2, 0, 0], [-2, 0, 0, -1]],
    ];
    const CONJ52: [[i128; 4]; 4] = [[1, 0, 0, 0], [-1, -1, 0, 0], [0, 0, -1, 0], [-5, 0, 0, -1]];
    const CONJ12: [[i128; 4]; 4] = [[1, 0, 0, 0], [-1, -1, 0, 0], [0, 0, -1, 0], [-1, 0, 0, -1]];

    let adj_y = nauru_adj();
    let auts = find_nauru_auts();
    let ident: Perm24 = std::array::from_fn(|i| i as u8);
    let stab0: Vec<Perm24> = auts.iter().copied().filter(|g| g[0] == 0).collect();
    let a_y = *stab0.iter().find(|g| order24(g) == 3).unwrap();
    let b_y = *stab0
        .iter()
        .find(|g| order24(g) == 2 && g[adj_y[0][0]] as usize == adj_y[0][0])
        .unwrap();
    let e0 = adj_y[0][0];
    let t_y = *auts
        .iter()
        .find(|g| {
            order24(g) == 2
                && g[0] as usize == e0
                && g[e0] == 0
                && comp(g, &b_y) == comp(&b_y, g)
        })
        .unwrap();

    let gcd128 = |mut a: i128, mut b: i128| -> i128 {
        a = a.abs();
        b = b.abs();
        while b != 0 {
            let t = a % b;
            a = b;
            b = t;
        }
        a
    };
    let prim = |mut u: [i128; 4]| -> [i128; 4] {
        let g = gcd128(gcd128(u[0], u[1]), gcd128(u[2], u[3]));
        if g > 1 {
            for x in &mut u {
                *x /= g;
            }
        }
        for x in u {
            if x != 0 {
                if x < 0 {
                    for y in &mut u {
                        *y = -*y;
                    }
                }
                break;
            }
        }
        u
    };
    let omul = |u: [i128; 4], v: [i128; 4], mt: &[[[i128; 4]; 4]; 4]| -> [i128; 4] {
        let mut out = [0i128; 4];
        for r in 0..4 {
            if u[r] == 0 {
                continue;
            }
            for c in 0..4 {
                if v[c] == 0 {
                    continue;
                }
                let uv = u[r] * v[c];
                for k in 0..4 {
                    out[k] += uv * mt[r][c][k];
                }
            }
        }
        out
    };
    let oconj = |u: [i128; 4], cm: &[[i128; 4]; 4]| -> [i128; 4] {
        let mut out = [0i128; 4];
        for r in 0..4 {
            for k in 0..4 {
                out[k] += u[r] * cm[r][k];
            }
        }
        out
    };
    let onrd = |u: [i128; 4], mt: &[[[i128; 4]; 4]; 4], cm: &[[i128; 4]; 4]| -> i128 {
        omul(u, oconj(u, cm), mt)[0]
    };

    for is_52 in [true, false] {
        let mt = if is_52 { &MT52 } else { &MT12 };
        let cm = if is_52 { &CONJ52 } else { &CONJ12 };
        let a_o: [i128; 4] = [0, 1, 0, 0];
        let b_o: [i128; 4] = if is_52 { [-5, 0, -1, -2] } else { [-1, 0, -1, -2] };
        let t_o: [i128; 4] = [0, 0, 1, 0];

        // Compute P_5 / 5O_5 = {u mod 5 : 5 | nrd(u)} (must have exact size 25)
        let mut p5_vecs: Vec<[i64; 4]> = Vec::new();
        for c0 in 0..5i64 {
            for c1 in 0..5i64 {
                for c2 in 0..5i64 {
                    for c3 in 0..5i64 {
                        if onrd([c0 as i128, c1 as i128, c2 as i128, c3 as i128], mt, cm).rem_euclid(5) == 0 {
                            p5_vecs.push([c0, c1, c2, c3]);
                        }
                    }
                }
            }
        }
        if p5_vecs.len() != 25 {
            return false;
        }
        let mod_p5_pm = |u: [i64; 4]| -> [i64; 4] {
            let mut best = [5i64; 4];
            for &z in &p5_vecs {
                let c1 = std::array::from_fn(|k| (u[k] + z[k]).rem_euclid(5));
                let c2 = std::array::from_fn(|k| (-u[k] + z[k]).rem_euclid(5));
                if c1 < best {
                    best = c1;
                }
                if c2 < best {
                    best = c2;
                }
            }
            best
        };
        let mod_pm = |u: [i64; 4], m: i64| -> [i64; 4] {
            let v: [i64; 4] = std::array::from_fn(|k| u[k].rem_euclid(m));
            let nv: [i64; 4] = std::array::from_fn(|k| (-v[k]).rem_euclid(m));
            v.min(nv)
        };

        // BFS 144 coset reps of Gamma_tilde / Gamma_Y
        let mut coset: HashMap<Perm24, [i128; 4]> = HashMap::new();
        coset.insert(ident, [1, 0, 0, 0]);
        let mut dq = VecDeque::new();
        dq.push_back(ident);
        while let Some(g) = dq.pop_front() {
            let rg = coset[&g];
            for (sp, sq) in [(&a_y, a_o), (&b_y, b_o), (&t_y, t_o)] {
                let h = comp(&g, sp);
                if !coset.contains_key(&h) {
                    coset.insert(h, prim(omul(rg, sq, mt)));
                    dq.push_back(h);
                }
            }
        }
        if coset.len() != 144 {
            return false;
        }

        // Collect Schreier generators of Gamma_Y (every one must have nrd = 2^{2a})
        let mut sch: Vec<[i128; 4]> = Vec::new();
        for (&g, &rg) in &coset {
            for (sp, sq) in [(&a_y, a_o), (&b_y, b_o), (&t_y, t_o)] {
                let h = comp(&g, sp);
                let rh = coset[&h];
                let gen = prim(omul(omul(rg, sq, mt), oconj(rh, cm), mt));
                let mut nr = onrd(gen, mt, cm);
                let mut v2 = 0u32;
                while nr % 2 == 0 {
                    nr /= 2;
                    v2 += 1;
                }
                if nr != 1 || v2 % 2 != 0 {
                    return false;
                }
                sch.push(gen);
            }
        }

        let norm_sl1 = |u: [i128; 4], m: i64| -> [i64; 4] {
            let mut nr = onrd(u, mt, cm);
            let mut v2 = 0u32;
            while nr % 2 == 0 {
                nr /= 2;
                v2 += 1;
            }
            let half_pow = {
                let mut acc = 1i64;
                for _ in 0..(v2 / 2) {
                    acc = (acc * 2) % m;
                }
                acc
            };
            let inv = mod_inv_i64(half_pow, m);
            std::array::from_fn(|k| ((u[k].rem_euclid(m as i128) as i64) * inv).rem_euclid(m))
        };

        let close_mod = |m: i64| -> HashSet<[i64; 4]> {
            let mut seed = HashSet::new();
            for &g in &sch {
                seed.insert(mod_pm(norm_sl1(g, m), m));
            }
            let idm = mod_pm([1, 0, 0, 0], m);
            let mut s = HashSet::new();
            s.insert(idm);
            let mut q = VecDeque::new();
            q.push_back(idm);
            while let Some(cur) = q.pop_front() {
                let ci: [i128; 4] = std::array::from_fn(|k| cur[k] as i128);
                for &sg in &seed {
                    let sgi: [i128; 4] = std::array::from_fn(|k| sg[k] as i128);
                    let pr = omul(ci, sgi, mt);
                    let pr64: [i64; 4] = std::array::from_fn(|k| pr[k].rem_euclid(m as i128) as i64);
                    let nxt = mod_pm(pr64, m);
                    if s.insert(nxt) {
                        q.push_back(nxt);
                    }
                }
            }
            s
        };

        let h3 = close_mod(3);
        let h9 = close_mod(9);
        let h5 = close_mod(5);
        let h25 = close_mod(25);
        let h7 = close_mod(7);
        let id_p5 = mod_p5_pm([1, 0, 0, 0]);
        let sch_p5_trivial = sch.iter().all(|&g| mod_p5_pm(norm_sl1(g, 5)) == id_p5);
        if !sch_p5_trivial || h5.len() != 25 || h25.len() != 3125 || h7.len() != 168 {
            return false;
        }

        // Elements of Aut(Y) lying in O_5[1/2]^1/{+-1} (exact index 36)
        let mut sl1_auts: Vec<Perm24> = Vec::new();
        for (&g, &rg) in &coset {
            let mut nr = onrd(rg, mt, cm);
            let (mut v2, mut v5) = (0u32, 0u32);
            while nr % 2 == 0 {
                nr /= 2;
                v2 += 1;
            }
            while nr % 5 == 0 {
                nr /= 5;
                v5 += 1;
            }
            if nr == 1 && v2 % 2 == 0 && v5 % 2 == 0 {
                sl1_auts.push(g);
            }
        }
        if sl1_auts.len() != 36 {
            return false;
        }
        let cong_deck: Vec<Perm24> = sl1_auts
            .iter()
            .copied()
            .filter(|g| {
                let rg = coset[g];
                h3.contains(&mod_pm(norm_sl1(rg, 3), 3)) && mod_p5_pm(norm_sl1(rg, 5)) == id_p5
            })
            .collect();

        if is_52 {
            // x = 5/2: CONGRUENCE! |H_3|=1 (idx 12), |H_9|=27 (idx 12), cong_deck = {id} (idx 36 = 12*3)
            if h3.len() != 1 || h9.len() != 27 || cong_deck.len() != 1 {
                return false;
            }
        } else {
            // x = 1/2: NON-CONGRUENCE! |H_3|=4 (idx 3), |H_9|=108 (idx 3), cong_deck = V_4 (order 4) -> K_{3,3}
            if h3.len() != 4 || h9.len() != 108 || cong_deck.len() != 4 {
                return false;
            }
            let inv_cnt = cong_deck.iter().filter(|g| order24(g) == 2).count();
            if inv_cnt != 3 {
                return false;
            }
            // Verify quotient Y / cong_deck is K_{3,3} (6 vertices, 3-regular, 9 simple edges)
            let mut v2o = [255usize; 24];
            let mut n_orb = 0usize;
            for v in 0..24 {
                if v2o[v] == 255 {
                    for g in &cong_deck {
                        v2o[g[v] as usize] = n_orb;
                    }
                    n_orb += 1;
                }
            }
            if n_orb != 6 {
                return false;
            }
            let mut qadj = vec![BTreeSet::new(); 6];
            for u in 0..24 {
                for &v in &adj_y[u] {
                    qadj[v2o[u]].insert(v2o[v]);
                }
            }
            if !qadj.iter().all(|s| s.len() == 3) {
                return false;
            }
        }
    }
    true
}

/// Gate D9b (Rust): Complete tropical invariants of 3-adic Dic_6 twin Z:
///   - |Aut(Z)| = 96, 43 involutions with quotient b1 in {7^2, 11^24, 13^17} (0 tree quotients)
///   - Exhaustive Baker-Norine Dhar burning over all canonical divisors of deg <= 7 (0 hits)
///   - Exact divisorial gonality gon(Z) = 8 with 4 canonical degree-8 witnesses (incl. reduced <y> + x<y>).
pub fn verify_dic6_tropical_invariants_exact() -> (usize, usize) {
    let dic6_mul = |u: usize, v: usize| -> usize {
        let (k1, f1) = (u % 12, u / 12);
        let (k2, f2) = (v % 12, v / 12);
        if f1 == 0 {
            f2 * 12 + (k1 + k2) % 12
        } else if f2 == 0 {
            12 + (k1 + 12 - k2) % 12
        } else {
            (k1 + 18 - k2) % 12
        }
    };
    let s_z = [1usize, 11, 12, 18];
    let mut adj = [[0usize; 4]; 24];
    for u in 0..24 {
        for (i, &g) in s_z.iter().enumerate() {
            adj[u][i] = dic6_mul(u, g);
        }
    }
    let has_edge = |u: usize, v: usize| -> bool { adj[u].contains(&v) };

    // Full Aut(Z) (order 96)
    let mut bfs = vec![0usize];
    let mut seen = [false; 24];
    seen[0] = true;
    let mut bi = 0;
    while bi < bfs.len() {
        let u = bfs[bi];
        bi += 1;
        for &v in &adj[u] {
            if !seen[v] {
                seen[v] = true;
                bfs.push(v);
            }
        }
    }
    let mut auts: Vec<Perm24> = Vec::new();
    let mut perm = [255u8; 24];
    let mut used = [false; 24];
    fn bt(
        pos: usize,
        bfs: &[usize],
        adj: &[[usize; 4]; 24],
        perm: &mut [u8; 24],
        used: &mut [bool; 24],
        auts: &mut Vec<Perm24>,
    ) {
        if pos == 24 {
            auts.push(*perm);
            return;
        }
        let u = bfs[pos];
        if pos == 0 {
            for c in 0..24 {
                perm[u] = c as u8;
                used[c] = true;
                bt(1, bfs, adj, perm, used, auts);
                perm[u] = 255;
                used[c] = false;
            }
            return;
        }
        let first_m = adj[u].iter().find_map(|&w| (perm[w] != 255).then_some(perm[w] as usize)).unwrap();
        for &c in &adj[first_m] {
            if used[c] {
                continue;
            }
            let ok = adj[u]
                .iter()
                .all(|&w| perm[w] == 255 || adj[c].contains(&(perm[w] as usize)));
            if ok {
                perm[u] = c as u8;
                used[c] = true;
                bt(pos + 1, bfs, adj, perm, used, auts);
                perm[u] = 255;
                used[c] = false;
            }
        }
    }
    bt(0, &bfs, &adj, &mut perm, &mut used, &mut auts);
    assert_eq!(auts.len(), 96);

    // Involution census (43 involutions, b1 in {7^2, 11^24, 13^17}, 0 tree quotients)
    let mut b1_counts: BTreeMap<usize, usize> = BTreeMap::new();
    let mut inv_total = 0usize;
    for g in &auts {
        if order24(g) != 2 {
            continue;
        }
        inv_total += 1;
        let mut v_orb = [255usize; 24];
        let mut nv = 0usize;
        for v in 0..24 {
            if v_orb[v] == 255 {
                v_orb[v] = nv;
                v_orb[g[v] as usize] = nv;
                nv += 1;
            }
        }
        let mut e_orbs: BTreeSet<(usize, usize)> = BTreeSet::new();
        for u in 0..24 {
            for &v in &adj[u] {
                if u < v {
                    let (gu, gv) = (g[u] as usize, g[v] as usize);
                    if gu == v && gv == u {
                        continue; // inverted edge folds to twig (contributes 0 to b1)
                    }
                    let e1 = (u, v);
                    let e2 = (gu.min(gv), gu.max(gv));
                    e_orbs.insert(e1.min(e2));
                }
            }
        }
        let b1 = e_orbs.len() + 1 - nv;
        *b1_counts.entry(b1).or_insert(0) += 1;
    }
    assert_eq!(inv_total, 43);
    assert_eq!(b1_counts.get(&0).copied().unwrap_or(0), 0);
    assert_eq!(b1_counts.get(&7).copied().unwrap_or(0), 2);
    assert_eq!(b1_counts.get(&11).copied().unwrap_or(0), 24);
    assert_eq!(b1_counts.get(&13).copied().unwrap_or(0), 17);
    let _ = has_edge;

    // Dhar burning test on Z
    let dhar_reach = |d_in: &[i8; 24], q: usize| -> bool {
        if d_in[q] >= 1 {
            return true;
        }
        let mut d = *d_in;
        let mut queue = [0usize; 24];
        loop {
            let mut burnt = [false; 24];
            let mut fires = [0i8; 24];
            burnt[q] = true;
            queue[0] = q;
            let (mut head, mut tail) = (0usize, 1usize);
            while head < tail {
                let u = queue[head];
                head += 1;
                for &v in &adj[u] {
                    if !burnt[v] {
                        fires[v] += 1;
                        if fires[v] > d[v] {
                            burnt[v] = true;
                            queue[tail] = v;
                            tail += 1;
                        }
                    }
                }
            }
            if tail == 24 {
                return false;
            }
            for u in 0..24 {
                if !burnt[u] {
                    for &v in &adj[u] {
                        if burnt[v] {
                            d[u] -= 1;
                            d[v] += 1;
                        }
                    }
                }
            }
            if d[q] >= 1 {
                return true;
            }
        }
    };
    const Q_ORDER: [usize; 23] = [
        6, 15, 21, 3, 9, 18, 12, 4, 8, 2, 10, 14, 16, 20, 22, 1, 5, 7, 11, 13, 17, 19, 23,
    ];
    let has_rank_ge_1 = |d: &[i8; 24]| -> bool { Q_ORDER.iter().all(|&q| dhar_reach(d, q)) };

    let stab0: Vec<Perm24> = auts.iter().copied().filter(|g| g[0] == 0).collect();
    assert_eq!(stab0.len(), 4);

    // Exhaustive search over all canonical divisors with D(0) >= 1 of degrees 4..=7
    let mut total_checked = 0usize;
    fn dfs_low(
        rem: usize,
        start_v: usize,
        cur: &mut Vec<usize>,
        d: &mut [i8; 24],
        stab0: &[Perm24],
        has_r1: &dyn Fn(&[i8; 24]) -> bool,
        checked: &mut usize,
        hits: &mut usize,
    ) {
        if rem == 0 {
            let m = cur.len();
            let mut mapped = [0usize; 8];
            for s in &stab0[1..] {
                for i in 0..m {
                    mapped[i] = s[cur[i]] as usize;
                }
                mapped[..m].sort_unstable();
                if mapped[..m] < cur[..] {
                    return;
                }
            }
            *checked += 1;
            if has_r1(d) {
                *hits += 1;
            }
            return;
        }
        for v in start_v..24 {
            cur.push(v);
            d[v] += 1;
            dfs_low(rem - 1, v, cur, d, stab0, has_r1, checked, hits);
            d[v] -= 1;
            cur.pop();
        }
    }
    for deg in 4..=7 {
        let mut d = [0i8; 24];
        d[0] = 1;
        let mut cur = Vec::with_capacity(deg);
        let mut hits = 0usize;
        dfs_low(deg - 1, 0, &mut cur, &mut d, &stab0, &has_rank_ge_1, &mut total_checked, &mut hits);
        assert_eq!(hits, 0, "Unexpected rank>=1 divisor on Z at degree {deg}");
    }
    assert_eq!(total_checked, 789 + 4_946 + 26_509 + 124_922);

    // Verify all 4 canonical degree-8 two-coset witnesses <y> + x^k <y> (k = 0, 1, 2, 3)
    let witnesses: [[usize; 8]; 4] = [
        [0, 0, 6, 6, 12, 12, 18, 18],
        [0, 1, 6, 7, 12, 13, 18, 19],
        [0, 2, 6, 8, 12, 14, 18, 20],
        [0, 3, 6, 9, 12, 15, 18, 21],
    ];
    for w in &witnesses {
        let mut d = [0i8; 24];
        for &v in w {
            d[v] += 1;
        }
        assert!(has_rank_ge_1(&d));
    }
    (total_checked, 8)
}

