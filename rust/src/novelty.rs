/// ADPIE Cycle 4 Fourth-Language Verification of Original Mathematical Novelties:
///   1. Theorem A (universal |L_0 ∩ L_t| <= 2) and Theorem B (complete classification across
///      ALL 2^{floor(N/2)} step sets via maximal S_max(c_0)) for all 5 <= N <= 72, plus NEG-M11.
///   2. Theorem C (exact 4th/6th-order Edgeworth winding law C-2'/C-2'' and 2D Tonnetz
///      isotropy across armchair W=-u, armchair v, and zigzag 4u+3v at m = 40).
use std::collections::{BTreeSet, HashSet};
use crate::swe_sweep::{compute_exact_pi_and_winding, mobius_mu, sum_neumaier};

#[inline]
fn circ_dist(a: u16, b: u16, n: u16) -> u16 {
    let d = if a >= b { a - b } else { b - a };
    if 2 * d <= n { d } else { n - d }
}

#[inline]
fn sorted_triple(a: u16, b: u16, c: u16) -> [u16; 3] {
    let mut v = [a, b, c];
    v.sort_unstable();
    v
}

#[inline]
fn sorted_pair(a: u16, b: u16) -> (u16, u16) {
    if a < b { (a, b) } else { (b, a) }
}

fn graph_has_cycle(n_nodes: usize, edges: &[(usize, usize)]) -> bool {
    let mut par: Vec<usize> = (0..n_nodes).collect();
    fn find(par: &mut [usize], mut x: usize) -> usize {
        while par[x] != x {
            par[x] = par[par[x]];
            x = par[x];
        }
        x
    }
    for &(u, v) in edges {
        let ru = find(&mut par, u);
        let rv = find(&mut par, v);
        if ru == rv {
            return true;
        }
        par[ru] = rv;
    }
    false
}

fn is_octatonic_diameter_triple(n: u16, cls: [u16; 3]) -> bool {
    if n % 8 != 0 {
        return false;
    }
    let m = n / 8;
    let mut ivs = [
        circ_dist(cls[0], cls[1], n),
        circ_dist(cls[1], cls[2], n),
        circ_dist(cls[0], cls[2], n),
    ];
    ivs.sort_unstable();
    ivs == [m, 3 * m, 4 * m]
}

fn verify_neg_m11_explicit() -> bool {
    let n: u16 = 8;
    let mut ti_orbit: HashSet<[u16; 3]> = HashSet::new();
    for t in 0..n {
        ti_orbit.insert(sorted_triple(t % n, (t + 1) % n, (t + 4) % n));
        ti_orbit.insert(sorted_triple(t % n, (t + n - 1) % n, (t + n - 4) % n));
    }
    let cyc1 = [[0, 1, 4], [0, 3, 4], [0, 4, 5], [0, 4, 7]];
    let cyc2 = [[1, 2, 6], [2, 3, 6], [2, 5, 6], [2, 6, 7]];
    let expected_tune = [3u16, 5, 7, 1];

    let check_cycle = |cyc: &[[u16; 3]; 4]| -> Option<[u16; 4]> {
        let mut tune = [0u16; 4];
        for i in 0..4 {
            let c = cyc[i];
            if !ti_orbit.contains(&c) {
                return None;
            }
            if circ_dist(c[0], c[1], n) == 2
                || circ_dist(c[1], c[2], n) == 2
                || circ_dist(c[0], c[2], n) == 2
            {
                return None;
            }
            let nxt = cyc[(i + 1) % 4];
            let prv = cyc[(i + 3) % 4];
            if nxt == prv {
                return None;
            }
            let mut shared = 0usize;
            let mut depart = None;
            let mut arrive = None;
            for &x in &c {
                if nxt.contains(&x) {
                    shared += 1;
                } else {
                    depart = Some(x);
                }
            }
            for &y in &nxt {
                if !c.contains(&y) {
                    arrive = Some(y);
                }
            }
            if shared != 2 {
                return None;
            }
            let d = depart?;
            let a = arrive?;
            if circ_dist(d, a, n) != 2 {
                return None;
            }
            tune[i] = a;
        }
        if cyc[0] == cyc[2] && cyc[1] == cyc[3] {
            return None;
        }
        Some(tune)
    };

    let t1 = match check_cycle(&cyc1) {
        Some(t) => t,
        None => return false,
    };
    let t2 = match check_cycle(&cyc2) {
        Some(t) => t,
        None => return false,
    };
    if t1 != expected_tune || t2 != expected_tune {
        return false;
    }
    for c in &cyc1 {
        if cyc2.contains(c) {
            return false;
        }
    }
    true
}

#[derive(Debug, Clone)]
pub struct NoveltyTuneReport {
    pub n_max: u16,
    pub chords_tested: usize,
    pub max_link_intersection: usize,
    pub t_orbit_failures: usize,
    pub ti_octatonic_failures: usize,
    pub ti_unexpected_failures: usize,
    pub octatonic_witness_ns: Vec<u16>,
    pub neg_m11_verified: bool,
    pub passed: bool,
}

/// Exhaustive Theorem A & Theorem B check under maximal legal step sets S_max(c_0)
/// across all 5 <= N <= n_max (covers all 2^{floor(N/2)} step sets by monotonicity).
pub fn verify_novelty_theorems_a_and_b(n_max: u16) -> NoveltyTuneReport {
    let mut chords_tested = 0usize;
    let mut max_link_intersection = 0usize;
    let mut t_orbit_failures = 0usize;
    let mut ti_octatonic_failures = 0usize;
    let mut ti_unexpected_failures = 0usize;
    let mut octatonic_witness_ns = Vec::new();
    let neg_m11_verified = verify_neg_m11_explicit();

    for n in 5..=n_max {
        let mut classes: BTreeSet<[u16; 3]> = BTreeSet::new();
        for a in 1..n {
            for b in (a + 1)..n {
                let mut best = [n, n, n];
                for t in 0..n {
                    let c1 = sorted_triple((n - t) % n, (a + n - t) % n, (b + n - t) % n);
                    if c1 < best {
                        best = c1;
                    }
                    let c2 = sorted_triple(t % n, (t + n - a) % n, (t + n - b) % n);
                    if c2 < best {
                        best = c2;
                    }
                }
                classes.insert(best);
            }
        }

        let ni = n as usize;
        for cls in classes {
            chords_tested += 1;
            let d01 = circ_dist(cls[0], cls[1], n);
            let d12 = circ_dist(cls[1], cls[2], n);
            let d02 = circ_dist(cls[0], cls[2], n);
            let mut is_legal = vec![false; (n / 2 + 1) as usize];
            for s in 1..=(n / 2) {
                if s != d01 && s != d12 && s != d02 {
                    is_legal[s as usize] = true;
                }
            }

            let mut t_set: HashSet<[u16; 3]> = HashSet::with_capacity(ni);
            let mut ti_set: HashSet<[u16; 3]> = HashSet::with_capacity(2 * ni);
            for t in 0..n {
                let ct = sorted_triple((cls[0] + t) % n, (cls[1] + t) % n, (cls[2] + t) % n);
                t_set.insert(ct);
                ti_set.insert(ct);
                let ci = sorted_triple(
                    (n + t - cls[0]) % n,
                    (n + t - cls[1]) % n,
                    (n + t - cls[2]) % n,
                );
                ti_set.insert(ci);
            }

            // Theorem A: |L_0 ∩ L_t| <= 2 universally in full T/I orbit.
            let mut links: Vec<Vec<(u16, u16)>> = vec![Vec::with_capacity(6); ni];
            for &c in &ti_set {
                links[c[0] as usize].push(sorted_pair(c[1], c[2]));
                links[c[1] as usize].push(sorted_pair(c[0], c[2]));
                links[c[2] as usize].push(sorted_pair(c[0], c[1]));
            }
            for l in &mut links {
                l.sort_unstable();
                l.dedup();
            }
            for t in 1..ni {
                let mut common = 0usize;
                for p in &links[0] {
                    if links[t].binary_search(p).is_ok() {
                        common += 1;
                    }
                }
                if common > max_link_intersection {
                    max_link_intersection = common;
                }
            }

            // Theorem B: one-moving-voice held-note cycles under S_max(c_0).
            let has_one_voice_cycle = |orb: &HashSet<[u16; 3]>| -> bool {
                let mut comp_map: Vec<Vec<u16>> = vec![Vec::new(); ni * ni];
                for &c in orb {
                    comp_map[c[0] as usize * ni + c[1] as usize].push(c[2]);
                    comp_map[c[0] as usize * ni + c[2] as usize].push(c[1]);
                    comp_map[c[1] as usize * ni + c[2] as usize].push(c[0]);
                }
                let mut comp_list: Vec<Vec<u16>> = Vec::new();
                for mut v in comp_map {
                    if v.len() >= 3 {
                        v.sort_unstable();
                        v.dedup();
                        if v.len() >= 3 {
                            comp_list.push(v);
                        }
                    }
                }
                for i in 0..comp_list.len() {
                    for j in (i + 1)..comp_list.len() {
                        let a = &comp_list[i];
                        let b = &comp_list[j];
                        let mut common = Vec::new();
                        for &x in a {
                            if b.binary_search(&x).is_ok() {
                                common.push(x);
                            }
                        }
                        if common.len() < 3 {
                            continue;
                        }
                        let mut edges = Vec::new();
                        for u in 0..common.len() {
                            for v in (u + 1)..common.len() {
                                let d = circ_dist(common[u], common[v], n);
                                if is_legal[d as usize] {
                                    edges.push((u, v));
                                }
                            }
                        }
                        if graph_has_cycle(common.len(), &edges) {
                            return true;
                        }
                    }
                }
                false
            };

            if has_one_voice_cycle(&t_set) {
                t_orbit_failures += 1;
            }
            if has_one_voice_cycle(&ti_set) {
                if is_octatonic_diameter_triple(n, cls) {
                    ti_octatonic_failures += 1;
                    octatonic_witness_ns.push(n);
                } else {
                    ti_unexpected_failures += 1;
                }
            }
        }
    }

    let expected_oct = (n_max / 8) as usize;
    let passed = max_link_intersection == 2
        && t_orbit_failures == 0
        && ti_octatonic_failures == expected_oct
        && ti_unexpected_failures == 0
        && neg_m11_verified;

    NoveltyTuneReport {
        n_max,
        chords_tested,
        max_link_intersection,
        t_orbit_failures,
        ti_octatonic_failures,
        ti_unexpected_failures,
        octatonic_witness_ns,
        neg_m11_verified,
        passed,
    }
}

#[derive(Debug, Clone)]
pub struct NoveltyEdgeworthReport {
    pub m: usize,
    pub total_primes: i64,
    pub m_times_ex_kurt: f64,
    pub tv_gaussian: f64,
    pub tv_edgeworth4: f64,
    pub tv_edgeworth6: f64,
    pub tv_gain_4: f64,
    pub tv_gain_6: f64,
    pub m_ex_kurt_v: f64,
    pub m_ex_kurt_zigzag: f64,
    pub max_isotropy_spread_4th: f64,
    pub bad_divisibility: i64,
    pub passed: bool,
}

fn compute_axis_exact(s0: i32, s1: i32, s2: i32, div_k: i32, m: usize) -> (i64, i64, f64, f64) {
    let mut succ = [[0usize; 2]; 72];
    let mut step_s = [0i32; 72];
    let ms = [s0, s1, s2];
    for v in 0..24 {
        let r = v % 12;
        for mv in 0..3 {
            let e = 3 * v + mv;
            let tv = if v < 12 {
                step_s[e] = ms[mv];
                match mv {
                    0 => 12 + r,
                    1 => 12 + (r + 4) % 12,
                    _ => 12 + (r + 9) % 12,
                }
            } else {
                step_s[e] = -ms[mv];
                match mv {
                    0 => r,
                    1 => (r + 8) % 12,
                    _ => (r + 3) % 12,
                }
            };
            let mut idx = 0;
            for mv2 in 0..3 {
                if mv2 != mv {
                    succ[e][idx] = 3 * tv + mv2;
                    idx += 1;
                }
            }
        }
    }
    let max_step = s0.abs().max(s1.abs()).max(s2.abs());
    let max_s = max_step * (m as i32);
    let stride = (2 * max_s + 1) as usize;
    let off = max_s;
    let max_w = max_s / div_k;
    let w_stride = (2 * max_w + 1) as usize;

    let mut n_dw = vec![vec![0i64; w_stride]; m + 1];
    let mut bad_div = 0i64;
    let mut cur = vec![0i64; 72 * stride];
    let mut nxt = vec![0i64; 72 * stride];

    for e0 in 0..72 {
        cur.fill(0);
        cur[e0 * stride + (off + step_s[e0]) as usize] = 1;
        for d in 2..=m {
            nxt.fill(0);
            let slim = max_step * ((d - 1) as i32);
            for e in 0..72 {
                let base = e * stride;
                let e1 = succ[e][0];
                let e2 = succ[e][1];
                let ds1 = step_s[e1];
                let ds2 = step_s[e2];
                let b1 = e1 * stride;
                let b2 = e2 * stride;
                for s in -slim..=slim {
                    let c = cur[base + (off + s) as usize];
                    if c == 0 {
                        continue;
                    }
                    nxt[b1 + (off + s + ds1) as usize] += c;
                    nxt[b2 + (off + s + ds2) as usize] += c;
                }
            }
            std::mem::swap(&mut cur, &mut nxt);
            if d % 2 == 0 && m % d == 0 {
                let slim_d = max_step * (d as i32);
                for e in 0..72 {
                    if succ[e][0] != e0 && succ[e][1] != e0 {
                        continue;
                    }
                    let base = e * stride;
                    for s in -slim_d..=slim_d {
                        let c = cur[base + (off + s) as usize];
                        if c == 0 {
                            continue;
                        }
                        if s % div_k != 0 {
                            bad_div += c;
                        } else {
                            n_dw[d][(s / div_k + max_w) as usize] += c;
                        }
                    }
                }
            }
        }
    }

    let mut pi_w = vec![0i64; w_stride];
    let mut total_pi = 0i64;
    for w in -max_w..=max_w {
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
            acc += (mu as i64) * n_dw[d][(w / k + max_w) as usize];
        }
        let cnt = acc / (m as i64);
        pi_w[(w + max_w) as usize] = cnt;
        total_pi += cnt;
    }

    let inv_tot = 1.0 / (total_pi as f64);
    let mut t2 = vec![0.0; w_stride];
    let mut t4 = vec![0.0; w_stride];
    for w in -max_w..=max_w {
        let idx = (w + max_w) as usize;
        let p = (pi_w[idx] as f64) * inv_tot;
        let wd = w as f64;
        let w2 = wd * wd;
        t2[idx] = p * w2;
        t4[idx] = p * w2 * w2;
    }
    let m2 = sum_neumaier(&t2);
    let m4 = sum_neumaier(&t4);
    let dm = m as f64;
    (total_pi, bad_div, m2 / dm, dm * (m4 / (m2 * m2) - 3.0))
}

/// Fourth-language verification of Theorem C: exact Edgeworth C-2'/C-2'' TV gains
/// and 2D Tonnetz 4th-cumulant rotational isotropy across W = -u, v, and 4u + 3v at m = 40.
pub fn verify_novelty_theorem_c(m: usize) -> NoveltyEdgeworthReport {
    let (pi_m, bad_u, counts) = compute_exact_pi_and_winding(m);
    let inv_tot = 1.0 / (pi_m as f64);
    let probs: Vec<f64> = counts.iter().map(|&c| (c as f64) * inv_tot).collect();
    let dm = m as f64;
    let sig2 = dm / 24.0;
    let sig = sig2.sqrt();

    let t2: Vec<f64> = probs.iter().enumerate().map(|(i, &p)| p * ((i as i32 - 8) as f64).powi(2)).collect();
    let t4: Vec<f64> = probs.iter().enumerate().map(|(i, &p)| p * ((i as i32 - 8) as f64).powi(4)).collect();
    let m2 = sum_neumaier(&t2);
    let m4 = sum_neumaier(&t4);
    let m_ex_u = dm * (m4 / (m2 * m2) - 3.0);

    let c4 = -17.0 / (48.0 * dm);
    let c6 = 1469.0 / (2880.0 * dm * dm);
    let c8 = 289.0 / (4608.0 * dm * dm);

    let eval_tv = |order: usize| -> f64 {
        let weight = |wi: i32| -> f64 {
            let z = (wi as f64) / sig;
            let z2 = z * z;
            let base = (-0.5 * z2).exp();
            if order == 0 {
                return base;
            }
            let h4 = z2 * z2 - 6.0 * z2 + 3.0;
            let mut poly = 1.0 + c4 * h4;
            if order >= 6 {
                let h6 = z2 * z2 * z2 - 15.0 * z2 * z2 + 45.0 * z2 - 15.0;
                let h8 = z2 * z2 * z2 * z2 - 28.0 * z2 * z2 * z2 + 210.0 * z2 * z2 - 420.0 * z2 + 105.0;
                poly += c6 * h6 + c8 * h8;
            }
            (base * poly).max(0.0)
        };
        let mut znorm = 0.0;
        for w in -24i32..=24 {
            znorm += weight(w);
        }
        let q: Vec<f64> = (0..17).map(|i| weight(i as i32 - 8) / znorm).collect();
        let q_tail = (1.0 - sum_neumaier(&q)).max(0.0);
        0.5 * (q_tail + probs.iter().zip(q.iter()).map(|(p, qi)| (p - qi).abs()).sum::<f64>())
    };

    let tv0 = eval_tv(0);
    let tv4 = eval_tv(4);
    let tv6 = eval_tv(6);
    let gain4 = tv0 / tv4;
    let gain6 = tv0 / tv6;

    let (pi_v, bad_v, _, m_ex_v) = compute_axis_exact(-1, 2, -1, 9, m);
    let (pi_a, bad_a, _, m_ex_a) = compute_axis_exact(0, 1, -1, 1, m);
    let bad_div = bad_u + bad_v + bad_a;
    let spread = (m_ex_u - (-8.5))
        .abs()
        .max((m_ex_v - (-8.5)).abs())
        .max((m_ex_a - (-8.5)).abs());

    let passed = pi_m == pi_v
        && pi_m == pi_a
        && bad_div == 0
        && gain4 > 10.0
        && gain6 > 70.0
        && spread < 0.02;

    NoveltyEdgeworthReport {
        m,
        total_primes: pi_m,
        m_times_ex_kurt: m_ex_u,
        tv_gaussian: tv0,
        tv_edgeworth4: tv4,
        tv_edgeworth6: tv6,
        tv_gain_4: gain4,
        tv_gain_6: gain6,
        m_ex_kurt_v: m_ex_v,
        m_ex_kurt_zigzag: m_ex_a,
        max_isotropy_spread_4th: spread,
        bad_divisibility: bad_div,
        passed,
    }
}
