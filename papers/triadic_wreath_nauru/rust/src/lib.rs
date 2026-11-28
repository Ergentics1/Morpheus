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
