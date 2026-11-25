/// Theorem 4.2 (all 131,136 rooted primes of length <= 16 in 12-EDO) and
/// Theorem 4.3 / Correspondence C-4 (all 6,028 general N-EDO systems up to N <= 72
/// via the exact held-note link-graph cycle criterion).
use std::collections::{BTreeSet, HashMap, HashSet};

fn apply_plr_12(v: usize, mv: usize) -> (usize, usize) {
    let r = v % 12;
    if v < 12 {
        match mv {
            0 => (12 + r, (r + 3) % 12),
            1 => (12 + (r + 4) % 12, (r + 11) % 12),
            _ => (12 + (r + 9) % 12, (r + 9) % 12),
        }
    } else {
        match mv {
            0 => (r, (r + 4) % 12),
            1 => ((r + 8) % 12, (r + 8) % 12),
            _ => ((r + 3) % 12, (r + 10) % 12),
        }
    }
}

fn build_triad_mask_lut() -> [i8; 4096] {
    let mut lut = [-1i8; 4096];
    for r in 0..12usize {
        let m1 = (1usize << r) | (1usize << ((r + 4) % 12)) | (1usize << ((r + 7) % 12));
        lut[m1] = r as i8;
        let m2 = (1usize << r) | (1usize << ((r + 3) % 12)) | (1usize << ((r + 7) % 12));
        lut[m2] = (12 + r) as i8;
    }
    lut
}

fn is_primitive(seq: &[u8]) -> bool {
    let m = seq.len();
    for d in 1..m {
        if m % d != 0 {
            continue;
        }
        let mut per = true;
        for i in 0..m {
            if seq[i] != seq[i % d] {
                per = false;
                break;
            }
        }
        if per {
            return false;
        }
    }
    true
}

#[derive(Debug, Clone)]
pub struct Tune16Report {
    pub rooted_primes_checked: u64, // total for even m in 6..=16 (exact: 174,864)
    pub rooted_primes_len_16: u64,  // length m = 16 alone (exact: 131,136)
    pub decode_failures: u64,
    pub periodic_tune_failures: u64,
    pub passed: bool,
}

/// Exhaustive Theorem 4.2 decoder check over all 131,136 rooted primes of length <= 16.
pub fn verify_tune_theorem_up_to_16() -> Tune16Report {
    let lut = build_triad_mask_lut();
    let mut plr_target = [[0u8; 3]; 24];
    let mut plr_arrive = [[0u8; 3]; 24];
    for v in 0..24 {
        for mv in 0..3 {
            let (t, a) = apply_plr_12(v, mv);
            plr_target[v][mv] = t as u8;
            plr_arrive[v][mv] = a as u8;
        }
    }

    let decode_tune = |tune: &[u8], out: &mut [i8]| -> bool {
        let m = tune.len();
        for x in out.iter_mut() {
            *x = -1;
        }
        let mut any_three = false;
        for i in 0..m {
            let a = tune[(i + m - 2) % m];
            let b = tune[(i + m - 1) % m];
            let c = tune[i];
            if a != b && b != c && a != c {
                let t = lut[(1usize << a) | (1usize << b) | (1usize << c)];
                if t >= 0 {
                    out[i] = t;
                    any_three = true;
                }
            }
        }
        if !any_three {
            let mut held = -1i8;
            let mut matches = 0;
            for h in 0..12u8 {
                let mut ok = true;
                for i in 0..m {
                    let prev = tune[(i + m - 1) % m];
                    let cur = tune[i];
                    if prev == cur || prev == h || cur == h
                        || lut[(1usize << prev) | (1usize << cur) | (1usize << h)] < 0
                    {
                        ok = false;
                        break;
                    }
                }
                if ok {
                    held = h as i8;
                    matches += 1;
                }
            }
            if matches != 1 {
                return false;
            }
            let h = held as u8;
            for i in 0..m {
                let prev = tune[(i + m - 1) % m];
                let cur = tune[i];
                out[i] = lut[(1usize << prev) | (1usize << cur) | (1usize << h)];
            }
            return true;
        }
        let mut start = 0;
        while out[start] < 0 {
            start += 1;
        }
        for step in 1..m {
            let idx = (start + step) % m;
            if out[idx] >= 0 {
                continue;
            }
            let prev_v = out[(idx + m - 1) % m] as usize;
            let arr = tune[idx];
            let mut next_v = -1i8;
            for mv in 0..3 {
                if plr_arrive[prev_v][mv] == arr {
                    next_v = plr_target[prev_v][mv] as i8;
                    break;
                }
            }
            if next_v < 0 {
                return false;
            }
            out[idx] = next_v;
        }
        true
    };

    let mut checked = 0u64;
    let mut checked_16 = 0u64;
    let mut decode_fail = 0u64;
    let mut periodic_fail = 0u64;

    // Check all 24 starting vertices explicitly for exact sum_{m in {6,8,10,12,14,16}} m*pi(m) = 174,864.
    for target_m in (6..=16usize).step_by(2) {
        let before = checked;
        let mut chords = vec![0u8; target_m];
        let mut tune = vec![0u8; target_m];
        let mut decoded = vec![-1i8; target_m];

        // Exact DFS over rooted walks starting at start_v = 0..23.
        for start_v in 0..24u8 {
            #[allow(clippy::too_many_arguments)]
            fn dfs(
                depth: usize,
                target_m: usize,
                start_v: u8,
                cur_v: u8,
                last_mv: usize,
                first_mv: usize,
                plr_target: &[[u8; 3]; 24],
                plr_arrive: &[[u8; 3]; 24],
                chords: &mut [u8],
                tune: &mut [u8],
                decoded: &mut [i8],
                decode_tune: &dyn Fn(&[u8], &mut [i8]) -> bool,
                checked: &mut u64,
                decode_fail: &mut u64,
                periodic_fail: &mut u64,
            ) {
                if depth == target_m {
                    if cur_v != start_v || last_mv == first_mv {
                        return;
                    }
                    if !is_primitive(chords) {
                        return;
                    }
                    *checked += 1;
                    if !is_primitive(tune) {
                        *periodic_fail += 1;
                    }
                    if !decode_tune(tune, decoded)
                        || !decoded
                            .iter()
                            .zip(chords.iter())
                            .all(|(&d, &c)| d == c as i8)
                    {
                        *decode_fail += 1;
                    }
                    return;
                }
                for mv in 0..3 {
                    if depth > 0 && mv == last_mv {
                        continue;
                    }
                    let nv = plr_target[cur_v as usize][mv];
                    chords[depth] = nv;
                    tune[depth] = plr_arrive[cur_v as usize][mv];
                    dfs(
                        depth + 1,
                        target_m,
                        start_v,
                        nv,
                        mv,
                        if depth == 0 { mv } else { first_mv },
                        plr_target,
                        plr_arrive,
                        chords,
                        tune,
                        decoded,
                        decode_tune,
                        checked,
                        decode_fail,
                        periodic_fail,
                    );
                }
            }
            dfs(
                0,
                target_m,
                start_v,
                start_v,
                99,
                99,
                &plr_target,
                &plr_arrive,
                &mut chords,
                &mut tune,
                &mut decoded,
                &decode_tune,
                &mut checked,
                &mut decode_fail,
                &mut periodic_fail,
            );
        }
        if target_m == 16 {
            checked_16 = checked - before;
        }
    }

    let passed = checked == 174_864 && checked_16 == 131_136 && decode_fail == 0 && periodic_fail == 0;
    Tune16Report {
        rooted_primes_checked: checked,
        rooted_primes_len_16: checked_16,
        decode_failures: decode_fail,
        periodic_tune_failures: periodic_fail,
        passed,
    }
}

/// Union-Find cycle detector on an undirected simple graph.
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

fn sorted_triple(a: u16, b: u16, c: u16) -> [u16; 3] {
    let mut v = [a, b, c];
    v.sort_unstable();
    v
}

fn sorted_pair(a: u16, b: u16) -> (u16, u16) {
    if a < b { (a, b) } else { (b, a) }
}

fn circ_dist(a: u16, b: u16, n: u16) -> u16 {
    let d1 = (a + n - b) % n;
    let d2 = (b + n - a) % n;
    d1.min(d2)
}

#[derive(Debug, Clone)]
pub struct GeneralTuneReport {
    pub n_max: u16,
    pub systems_tested: usize,
    pub failures: usize,
    pub passed: bool,
}

/// Exact Theorem 4.3 held-note link-graph criterion across all 3-note step systems for 5 <= N <= n_max,
/// S in {{1}, {1, 2}}, symmetry in {T, T/I}. For n_max = 72, verifies all 6,028 systems.
pub fn verify_general_tune_criterion(n_max: u16) -> GeneralTuneReport {
    let mut systems_tested = 0usize;
    let mut failures = 0usize;

    for n in 5..=n_max {
        // Deduplicate 3-note chord classes up to transposition T.
        let mut class_set: BTreeSet<[u16; 3]> = BTreeSet::new();
        for a in 1..n {
            for b in (a + 1)..n {
                let mut best = [n, n, n];
                for t in 0..n {
                    let cand = sorted_triple(
                        (n - t) % n,
                        (a + n - t) % n,
                        (b + n - t) % n,
                    );
                    if cand < best {
                        best = cand;
                    }
                }
                class_set.insert(best);
            }
        }
        let classes: Vec<[u16; 3]> = class_set.into_iter().collect();

        for &s_max in &[1u16, 2u16] {
            let steps: Vec<i32> = if s_max == 1 {
                vec![1, -1]
            } else {
                vec![1, -1, 2, -2]
            };
            let is_step = |d: u16| -> bool { d == 1 || (s_max == 2 && d == 2) };

            for &cls in &classes {
                // Step-free chord check (invariant under T and T/I).
                if is_step(circ_dist(cls[0], cls[1], n))
                    || is_step(circ_dist(cls[1], cls[2], n))
                    || is_step(circ_dist(cls[0], cls[2], n))
                {
                    continue;
                }

                for &inv in &[false, true] {
                    let mut ch_set: HashSet<[u16; 3]> = HashSet::with_capacity((2 * n) as usize);
                    for t in 0..n {
                        ch_set.insert(sorted_triple(
                            (cls[0] + t) % n,
                            (cls[1] + t) % n,
                            (cls[2] + t) % n,
                        ));
                        if inv {
                            ch_set.insert(sorted_triple(
                                (n + t - cls[0]) % n,
                                (n + t - cls[1]) % n,
                                (n + t - cls[2]) % n,
                            ));
                        }
                    }

                    // Check at least one legal step move exists in the chord graph.
                    let mut has_edge = false;
                    'edge_chk: for &c in &ch_set {
                        for idx in 0..3 {
                            let a = c[idx];
                            let o1 = c[(idx + 1) % 3];
                            let o2 = c[(idx + 2) % 3];
                            for &st in &steps {
                                let np = ((a as i32 + st).rem_euclid(n as i32)) as u16;
                                if np != o1 && np != o2 && ch_set.contains(&sorted_triple(np, o1, o2)) {
                                    has_edge = true;
                                    break 'edge_chk;
                                }
                            }
                        }
                    }
                    if !has_edge {
                        continue;
                    }
                    systems_tested += 1;

                    // Criterion 1 (two moving voices, one held note h vs h2).
                    let mut links: Vec<HashSet<(u16, u16)>> = vec![HashSet::new(); n as usize];
                    for &c in &ch_set {
                        links[c[0] as usize].insert((c[1], c[2]));
                        links[c[1] as usize].insert((c[0], c[2]));
                        links[c[2] as usize].insert((c[0], c[1]));
                    }
                    let mut bad = false;
                    'two_voice: for h in 0..n {
                        if links[h as usize].len() < 3 {
                            continue;
                        }
                        for h2 in (h + 1)..n {
                            if links[h2 as usize].len() < 3 {
                                continue;
                            }
                            let common: Vec<(u16, u16)> = links[h as usize]
                                .iter()
                                .copied()
                                .filter(|p| links[h2 as usize].contains(p))
                                .collect();
                            if common.len() < 3 {
                                continue;
                            }
                            let node_idx: HashMap<(u16, u16), usize> = common
                                .iter()
                                .enumerate()
                                .map(|(i, &p)| (p, i))
                                .collect();
                            let mut edges: Vec<(usize, usize)> = Vec::new();
                            for (pi, &(p0, p1)) in common.iter().enumerate() {
                                for &(a, keep) in &[(p0, p1), (p1, p0)] {
                                    for &st in &steps {
                                        let np = ((a as i32 + st).rem_euclid(n as i32)) as u16;
                                        if np == keep || np == h || np == h2 {
                                            continue;
                                        }
                                        let q = sorted_pair(np, keep);
                                        if let Some(&qi) = node_idx.get(&q) {
                                            if pi < qi {
                                                edges.push((pi, qi));
                                            }
                                        }
                                    }
                                }
                            }
                            if graph_has_cycle(common.len(), &edges) {
                                bad = true;
                                break 'two_voice;
                            }
                        }
                    }

                    // Criterion 2 (one moving voice, two held notes H vs H2).
                    if !bad {
                        let mut comp: HashMap<(u16, u16), Vec<u16>> = HashMap::new();
                        for &c in &ch_set {
                            comp.entry((c[0], c[1])).or_default().push(c[2]);
                            comp.entry((c[0], c[2])).or_default().push(c[1]);
                            comp.entry((c[1], c[2])).or_default().push(c[0]);
                        }
                        let hs: Vec<Vec<u16>> = comp
                            .into_values()
                            .filter(|v| v.len() >= 3)
                            .map(|mut v| {
                                v.sort_unstable();
                                v.dedup();
                                v
                            })
                            .filter(|v| v.len() >= 3)
                            .collect();
                        'one_voice: for i in 0..hs.len() {
                            for j in (i + 1)..hs.len() {
                                let common: Vec<u16> = hs[i]
                                    .iter()
                                    .copied()
                                    .filter(|x| hs[j].binary_search(x).is_ok())
                                    .collect();
                                if common.len() < 3 {
                                    continue;
                                }
                                let mut edges: Vec<(usize, usize)> = Vec::new();
                                for (xi, &x) in common.iter().enumerate() {
                                    for &st in &steps {
                                        let nx = ((x as i32 + st).rem_euclid(n as i32)) as u16;
                                        if let Ok(nxi) = common.binary_search(&nx) {
                                            if xi < nxi {
                                                edges.push((xi, nxi));
                                            }
                                        }
                                    }
                                }
                                if graph_has_cycle(common.len(), &edges) {
                                    bad = true;
                                    break 'one_voice;
                                }
                            }
                        }
                    }

                    if bad {
                        failures += 1;
                    }
                }
            }
        }
    }

    let expected_ok = if n_max == 72 {
        systems_tested == 6028 && failures == 0
    } else {
        failures == 0
    };
    GeneralTuneReport {
        n_max,
        systems_tested,
        failures,
        passed: expected_ok,
    }
}
