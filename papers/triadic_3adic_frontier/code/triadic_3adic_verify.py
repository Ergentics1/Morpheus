#!/usr/bin/env python3
"""Independent First-Principles Verification Suite for Paper PC-III:
The 3-Adic Dicyclic Companion, Exact Level 3P_5 and Level (3) Congruence on Nauru,
and the Real-Quadratic Lame Shimura Curve Atlas (MIT License).

Zero external dependencies (Python 3.12+ standard library only). Strictly separates
Code Model from Data Model (Rule 2): never reads cached JSON files to pass checks;
recomputes every theorem, explicit quaternion order, modular adjoint and true
left-multiplication Gamma(M) image, scramble, max-flow cut, continuous equilateral
metric Dhar cell, Riehm commutator subgroup, genus-25 Borel census, and
Poitou-Odlyzko explicit-formula bound from first principles.

Usage:
    python3 papers/triadic_3adic_frontier/code/triadic_3adic_verify.py
    python3 papers/triadic_3adic_frontier/code/triadic_3adic_verify.py --no-figs
    python3 papers/triadic_3adic_frontier/code/triadic_3adic_verify.py --check-only
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction
import hashlib
import json
import math
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

PAPER_DIR = pathlib.Path(__file__).resolve().parent.parent
REPO_ROOT = PAPER_DIR.parent.parent
DATA_DIR = PAPER_DIR / "data"
FIG_DIR = PAPER_DIR / "paper" / "figures"

# ==============================================================================
# Core Exact Linear Algebra, HNF, Graph & Permutation Utilities
# ==============================================================================


def perm_comp(p: Tuple[int, ...], q: Tuple[int, ...]) -> Tuple[int, ...]:
    """Return composition p o q (apply q then p)."""
    return tuple(p[q[i]] for i in range(len(p)))


def perm_inv(p: Tuple[int, ...]) -> Tuple[int, ...]:
    inv = [0] * len(p)
    for i, v in enumerate(p):
        inv[v] = i
    return tuple(inv)


def perm_order(p: Tuple[int, ...]) -> int:
    n = len(p)
    seen = [False] * n
    ord_val = 1
    for i in range(n):
        if not seen[i]:
            cur, clen = i, 0
            while not seen[cur]:
                seen[cur] = True
                cur = p[cur]
                clen += 1
            ord_val = math.lcm(ord_val, clen)
    return ord_val


def graph_automorphisms(adj: List[List[int]]) -> List[Tuple[int, ...]]:
    """Exact backtracking enumeration of Aut(G) for a small vertex-regular graph."""
    n = len(adj)
    adj_sets = [set(nbrs) for nbrs in adj]
    auts: List[Tuple[int, ...]] = []
    # BFS ordering of vertices for tight pruning
    order: List[int] = []
    seen = [False] * n
    q: deque[int] = deque([0])
    seen[0] = True
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                q.append(v)
    pos = {u: idx for idx, u in enumerate(order)}
    prev_nbrs = [[v for v in adj[u] if pos[v] < idx] for idx, u in enumerate(order)]

    mapping = [-1] * n
    used = [False] * n

    def backtrack(idx: int) -> None:
        if idx == n:
            auts.append(tuple(mapping))
            return
        u = order[idx]
        p_nbrs = prev_nbrs[idx]
        if not p_nbrs:
            cands = range(n)
        else:
            cands = set(adj[mapping[p_nbrs[0]]])
            for pn in p_nbrs[1:]:
                cands &= adj_sets[mapping[pn]]
        for w in cands:
            if not used[w]:
                mapping[u] = w
                used[w] = True
                backtrack(idx + 1)
                used[w] = False
                mapping[u] = -1

    backtrack(0)
    return auts


def graph_isomorphic(adj1: List[List[int]], adj2: List[List[int]]) -> bool:
    """Exact backtracking graph isomorphism test on small graphs."""
    n = len(adj1)
    if n != len(adj2):
        return False
    deg1 = sorted(len(x) for x in adj1)
    deg2 = sorted(len(x) for x in adj2)
    if deg1 != deg2:
        return False
    adj2_sets = [set(x) for x in adj2]
    order: List[int] = []
    seen = [False] * n
    for s in range(n):
        if not seen[s]:
            q = deque([s])
            seen[s] = True
            while q:
                u = q.popleft()
                order.append(u)
                for v in adj1[u]:
                    if not seen[v]:
                        seen[v] = True
                        q.append(v)
    pos = {u: idx for idx, u in enumerate(order)}
    prev_nbrs = [[v for v in adj1[u] if pos[v] < idx] for idx, u in enumerate(order)]
    mapping = [-1] * n
    used = [False] * n

    def bt(idx: int) -> bool:
        if idx == n:
            return True
        u = order[idx]
        du = len(adj1[u])
        p_nbrs = prev_nbrs[idx]
        if not p_nbrs:
            cands = [w for w in range(n) if len(adj2[w]) == du]
        else:
            cset = set(adj2[mapping[p_nbrs[0]]])
            for pn in p_nbrs[1:]:
                cset &= adj2_sets[mapping[pn]]
            cands = [w for w in cset if len(adj2[w]) == du]
        for w in cands:
            if not used[w]:
                mapping[u] = w
                used[w] = True
                if bt(idx + 1):
                    return True
                used[w] = False
                mapping[u] = -1
        return False

    return bt(0)


def faddeev_leverrier_charpoly(mat: List[List[int]]) -> List[int]:
    """Return exact integer coefficients [c_n, c_{n-1}, ..., c_0] of det(xI - A)."""
    n = len(mat)
    coeffs = [1] + [0] * n
    M = [[0] * n for _ in range(n)]
    for k in range(1, n + 1):
        # M_k = A * M_{k-1} + c_{n-k+1} * I  (for k=1, M_1 = I -> AM + c*I)
        if k == 1:
            B = [row[:] for row in mat]
        else:
            # B = mat * M
            B = [[sum(mat[i][t] * M[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
        tr = sum(B[i][i] for i in range(n))
        assert tr % k == 0
        ck = -tr // k
        coeffs[k] = ck
        M = [row[:] for row in B]
        for i in range(n):
            M[i][i] += ck
    # Verify Cayley-Hamilton (last M must be zero)
    assert all(M[i][j] == 0 for i in range(n) for j in range(n))
    return coeffs


def poly_mul(a: List[int], b: List[int]) -> List[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return out


def poly_pow(a: List[int], e: int) -> List[int]:
    out = [1]
    base = a[:]
    while e > 0:
        if e & 1:
            out = poly_mul(out, base)
        base = poly_mul(base, base)
        e >>= 1
    return out


def mobius(n: int) -> int:
    mu = 1
    d = 2
    x = n
    while d * d <= x:
        if x % d == 0:
            x //= d
            if x % d == 0:
                return 0
            mu = -mu
        d += 1
    if x > 1:
        mu = -mu
    return mu


def hashimoto_and_ihara_cadences(
    adj: List[List[int]], max_m: int
) -> Tuple[Dict[int, int], Dict[int, int]]:
    """Compute exact N_m = tr(T^m) by direct Hashimoto matrix powers AND cross-check
    against exact Ihara-Bass determinant power series, returning (N_m, pi_m)."""
    n = len(adj)
    deg = len(adj[0])
    q_val = deg - 1
    edges = [(u, v) for u in range(n) for v in adj[u]]
    m_dir = len(edges)
    # Build Hashimoto adjacency list: e=(u,v) -> e'=(v,w) with w != u
    out_edges: Dict[int, List[int]] = {u: [] for u in range(n)}
    for idx, (u, v) in enumerate(edges):
        out_edges[u].append(idx)
    t_next = [
        [idx2 for idx2 in out_edges[v] if edges[idx2][1] != u]
        for (u, v) in edges
    ]

    # Direct Hashimoto traces N_m = tr(T^m) using vertex-transitivity:
    # Since G is vertex-transitive, tr(T^m) = n * sum_{e starting at 0} (T^m)_{e,e}.
    # Even better: compute full diagonal across all m_dir directed edges (fast for m_dir<=96)!
    traces: Dict[int, int] = {m: 0 for m in range(1, max_m + 1)}
    for start in range(m_dir):
        vec = [0] * m_dir
        vec[start] = 1
        for m in range(1, max_m + 1):
            nxt = [0] * m_dir
            for i, val in enumerate(vec):
                if val:
                    for j in t_next[i]:
                        nxt[j] += val
            vec = nxt
            traces[m] += vec[start]

    # Independent cross-check via exact Ihara-Bass determinant Q(u) = (1-u^2)^{E-V} det(I - A u + q u^2 I)
    # Compute det(I - A u + q u^2 I) from Faddeev-LeVerrier charpoly P(x) = det(xI - A) = sum c_k x^{n-k}:
    # det((1 + q u^2)I - A u) = u^n P((1 + q u^2)/u) = sum_{k=0}^n c_k u^k (1 + q u^2)^{n-k}
    A = [[1 if j in adj[i] else 0 for j in range(n)] for i in range(n)]
    cp = faddeev_leverrier_charpoly(A)  # cp[k] is coeff of x^{n-k}
    det_poly = [0] * (2 * n + 1)
    for k, ck in enumerate(cp):
        if ck == 0:
            continue
        term = poly_pow([1, 0, q_val], n - k)
        for j, tj in enumerate(term):
            det_poly[k + j] += ck * tj
    E = m_dir // 2
    Q_poly = poly_mul(poly_pow([1, 0, -1], E - n), det_poly)
    assert Q_poly[0] == 1
    # Log-derivative recurrence: -u Q'(u) / Q(u) = sum_{m>=1} N_m u^m
    # => Q(u) * sum N_m u^m = -u Q'(u) => N_m + sum_{k=1}^{m-1} Q_k N_{m-k} = -m Q_m
    ihara_traces: Dict[int, int] = {}
    for m in range(1, max_m + 1):
        rhs = -m * (Q_poly[m] if m < len(Q_poly) else 0)
        s = sum((Q_poly[k] if k < len(Q_poly) else 0) * ihara_traces[m - k] for k in range(1, m))
        ihara_traces[m] = rhs - s
        assert ihara_traces[m] == traces[m], f"Hashimoto != Ihara at m={m}: {traces[m]} vs {ihara_traces[m]}"

    pi_counts: Dict[int, int] = {}
    for m in range(1, max_m + 1):
        tot = sum(mobius(m // d) * traces[d] for d in range(1, m + 1) if m % d == 0)
        assert tot % m == 0
        pi_counts[m] = tot // m
    return traces, pi_counts


def edmonds_karp_edge_cut(adj: List[List[int]], s_set: Set[int], t_set: Set[int]) -> int:
    """Exact integer Edmonds-Karp max-flow = min edge-cut between disjoint vertex subsets."""
    n = len(adj)
    src, snk = n, n + 1
    cap = [[0] * (n + 2) for _ in range(n + 2)]
    for u in range(n):
        for v in adj[u]:
            cap[u][v] += 1
    INF = 10**6
    for u in s_set:
        cap[src][u] = INF
    for v in t_set:
        cap[v][snk] = INF
    flow = 0
    while True:
        parent = [-1] * (n + 2)
        parent[src] = src
        q = deque([src])
        while q and parent[snk] == -1:
            u = q.popleft()
            for v in range(n + 2):
                if parent[v] == -1 and cap[u][v] > 0:
                    parent[v] = u
                    q.append(v)
        if parent[snk] == -1:
            break
        aug = INF
        v = snk
        while v != src:
            u = parent[v]
            aug = min(aug, cap[u][v])
            v = u
        v = snk
        while v != src:
            u = parent[v]
            cap[u][v] -= aug
            cap[v][u] += aug
            v = u
        flow += aug
    return flow


def branch_and_bound_hitting_number(eggs: List[int], n_verts: int) -> Tuple[int, List[int]]:
    """Exact branch-and-bound hitting number of a collection of bitmask eggs (size <= 4)."""
    num_eggs = len(eggs)
    full_mask = (1 << num_eggs) - 1
    v_cover = [0] * n_verts
    for i, e in enumerate(eggs):
        for v in range(n_verts):
            if (e >> v) & 1:
                v_cover[v] |= 1 << i
    max_deg = max(m.bit_count() for m in v_cover)

    def can_hit(k: int) -> Optional[List[int]]:
        chosen: List[int] = []

        def dfs(uncovered: int, rem: int) -> bool:
            if uncovered == 0:
                return True
            if rem == 0 or uncovered.bit_count() > rem * max_deg:
                return False
            # Pick lowest uncovered egg
            lsb = uncovered & -uncovered
            e_idx = lsb.bit_length() - 1
            em = eggs[e_idx]
            # Order candidate vertices in this egg by decreasing newly covered eggs
            cands = [v for v in range(n_verts) if (em >> v) & 1]
            cands.sort(key=lambda v: (v_cover[v] & uncovered).bit_count(), reverse=True)
            for v in cands:
                chosen.append(v)
                if dfs(uncovered & ~v_cover[v], rem - 1):
                    return True
                chosen.pop()
            return False

        if dfs(full_mask, k):
            return sorted(chosen)
        return None

    for k in range(1, n_verts + 1):
        wit = can_hit(k)
        if wit is not None:
            return k, wit
    raise RuntimeError("unreachable")


def discrete_dhar_reaches(adj: List[List[int]], chips: List[int], target: int) -> Tuple[bool, int]:
    """Standard discrete Dhar burning algorithm: returns (reaches target, steps)."""
    n = len(adj)
    d = chips[:]
    steps = 0
    while d[target] == 0:
        burnt = [False] * n
        burnt[target] = True
        q = deque([target])
        burnt_nbrs = [0] * n
        while q:
            u = q.popleft()
            for v in adj[u]:
                if not burnt[v]:
                    burnt_nbrs[v] += 1
                    if burnt_nbrs[v] > d[v]:
                        burnt[v] = True
                        q.append(v)
        unburnt = [v for v in range(n) if not burnt[v]]
        if not unburnt:
            return False, steps
        for u in unburnt:
            for v in adj[u]:
                if burnt[v]:
                    d[u] -= 1
                    d[v] += 1
        steps += 1
        if steps > 100:
            return False, steps
    return True, steps


def continuous_metric_dhar_cell(
    adj: List[List[int]], chips: List[int], u0: int, v0: int, regime: int
) -> Tuple[bool, int]:
    """Symbolic piecewise-linear continuous equilateral metric Dhar algorithm on
    interior point q_t of edge (u0, v0) in regime:
      regime=0: t in (0, 1/2)  (integer scale L=4, q_t at distance 1 from u0, 3 from v0)
      regime=1: t = 1/2        (integer scale L=2, q_t at distance 1 from u0, 1 from v0)
      regime=2: t in (1/2, 1)  (symmetric to regime=0 with u0 <-> v0).
    Returns (passes, firing_steps). Because all integer path arrival times k+t vs k+(1-t)
    preserve strict ordering across the entire open interval t in (0, 1/2), exact integer
    distances L=4 (d_u0=1, d_v0=3) certify the continuous regime symbolically!"""
    if regime == 2:
        u0, v0 = v0, u0
        regime = 0
    L = 4 if regime == 0 else 2
    d_u0 = 1
    d_v0 = 3 if regime == 0 else 1
    n = len(adj)
    d = chips[:]
    # Direct chip on u0 or v0 can only flow if we fire unburnt subgraph; track chip count at q_t.
    # Equivalently, subdivide edge (u0, v0) by inserting q_t at distances d_u0 and d_v0.
    # At each Dhar firing step, run exact event-driven burning wave from q_t!
    import heapq

    steps = 0
    for _ in range(25):
        # Event-driven burning wave on equilateral graph with edge (u0, v0) split by q_t
        INF = 10**9
        burn_time = [INF] * n
        # Track arrival of fire along each directed edge (a -> b)
        # Initial fires leave q_t at time 0, arriving at u0 at time d_u0 and v0 at time d_v0.
        pq: List[Tuple[int, int, int]] = []  # (arrival_time, target_vertex, source_id)
        # source_id = -1 means from q_t via u0-side, -2 means from q_t via v0-side
        heapq.heappush(pq, (d_u0, u0, -1))
        heapq.heappush(pq, (d_v0, v0, -2))
        arrived_count = [0] * n
        arrived_sources: List[Set[int]] = [set() for _ in range(n)]
        while pq:
            t, w, src = heapq.heappop(pq)
            if burn_time[w] <= t:
                continue
            if src in arrived_sources[w]:
                continue
            arrived_sources[w].add(src)
            arrived_count[w] += 1
            if arrived_count[w] > d[w]:
                burn_time[w] = t
                for nb in adj[w]:
                    # Skip the subdivided edge (u0, v0) directly (q_t blocks it!)
                    if (w == u0 and nb == v0) or (w == v0 and nb == u0):
                        continue
                    if burn_time[nb] == INF:
                        heapq.heappush(pq, (t + L, nb, w))
        unburnt = {v for v in range(n) if burn_time[v] == INF}
        if not unburnt:
            return False, steps
        # If u0 or v0 is unburnt, firing the unburnt set moves a chip directly onto q_t!
        if u0 in unburnt or v0 in unburnt:
            return True, steps + 1
        # Otherwise perform a full subset fire of the unburnt set (all its boundary edges have length L)
        for u in unburnt:
            for v in adj[u]:
                if v not in unburnt:
                    d[u] -= 1
                    d[v] += 1
        steps += 1
    return False, steps


# ==============================================================================
# Exact Rational & Quadratic Quaternion Algebra + HNF Engine
# ==============================================================================


def hnf_rows(rows: List[List[int]]) -> List[List[int]]:
    m = [list(r) for r in rows if any(r)]
    if not m:
        return []
    n = len(m[0])
    piv_row = 0
    for col in range(n):
        while True:
            nz = [r for r in range(piv_row, len(m)) if m[r][col] != 0]
            if not nz:
                break
            if len(nz) == 1:
                r = nz[0]
                m[piv_row], m[r] = m[r], m[piv_row]
                if m[piv_row][col] < 0:
                    m[piv_row] = [-v for v in m[piv_row]]
                for i in range(piv_row):
                    q = m[i][col] // m[piv_row][col]
                    if q:
                        m[i] = [m[i][j] - q * m[piv_row][j] for j in range(n)]
                piv_row += 1
                break
            best = min(nz, key=lambda r: abs(m[r][col]))
            m[piv_row], m[best] = m[best], m[piv_row]
            if m[piv_row][col] < 0:
                m[piv_row] = [-v for v in m[piv_row]]
            for r in nz:
                if r != piv_row and m[r][col] != 0:
                    q = m[r][col] // m[piv_row][col]
                    m[r] = [m[r][j] - q * m[piv_row][j] for j in range(n)]
    return [r for r in m if any(r)]


def mat_inv_frac(M: List[List[Fraction]]) -> List[List[Fraction]]:
    n = len(M)
    aug = [list(M[i]) + [Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
    for i in range(n):
        piv = next(r for r in range(i, n) if aug[r][i] != 0)
        aug[i], aug[piv] = aug[piv], aug[i]
        pv = aug[i][i]
        aug[i] = [v / pv for v in aug[i]]
        for r in range(n):
            if r != i and aug[r][i] != 0:
                fac = aug[r][i]
                aug[r] = [aug[r][c] - fac * aug[i][c] for c in range(2 * n)]
    return [row[n:] for row in aug]


def mat_det_frac(M: List[List[Fraction]]) -> Fraction:
    n = len(M)
    mat = [[Fraction(v) for v in row] for row in M]
    det = Fraction(1)
    for i in range(n):
        piv = next((r for r in range(i, n) if mat[r][i] != 0), -1)
        if piv == -1:
            return Fraction(0)
        if piv != i:
            mat[i], mat[piv] = mat[piv], mat[i]
            det = -det
        det *= mat[i][i]
        for r in range(i + 1, n):
            fac = mat[r][i] / mat[i][i]
            for c in range(i, n):
                mat[r][c] -= fac * mat[i][c]
    return det


def qmul_Q(
    x: Tuple[Fraction, Fraction, Fraction, Fraction],
    y: Tuple[Fraction, Fraction, Fraction, Fraction],
    A: Fraction,
    B: Fraction,
) -> Tuple[Fraction, Fraction, Fraction, Fraction]:
    x0, x1, x2, x3 = x
    y0, y1, y2, y3 = y
    return (
        x0 * y0 + A * x1 * y1 + B * x2 * y2 - A * B * x3 * y3,
        x0 * y1 + x1 * y0 - B * x2 * y3 + B * x3 * y2,
        x0 * y2 + x2 * y0 + A * x1 * y3 - A * x3 * y1,
        x0 * y3 + x3 * y0 + x1 * y2 - x2 * y1,
    )


def qnrd_Q(x: Tuple[Fraction, Fraction, Fraction, Fraction], A: Fraction, B: Fraction) -> Fraction:
    return x[0] * x[0] - A * x[1] * x[1] - B * x[2] * x[2] + A * B * x[3] * x[3]


def qinv_Q(
    x: Tuple[Fraction, Fraction, Fraction, Fraction], A: Fraction, B: Fraction
) -> Tuple[Fraction, Fraction, Fraction, Fraction]:
    n = qnrd_Q(x, A, B)
    return (x[0] / n, -x[1] / n, -x[2] / n, -x[3] / n)


def q_verify_order_and_adjoint_Q(
    basis: List[Tuple[Fraction, Fraction, Fraction, Fraction]],
    gens: List[Tuple[Fraction, Fraction, Fraction, Fraction]],
    A: Fraction,
    B: Fraction,
) -> Tuple[int, List[int], List[List[List[Fraction]]]]:
    """Verify ring closure of a Q-quaternion basis, compute reduced discriminant,
    conjugation denominators, and exact 4x4 adjoint matrices (row action on basis)."""
    Binv = mat_inv_frac([list(e) for e in basis])
    # Verify ring closure
    for e1 in basis:
        for e2 in basis:
            w = qmul_Q(e1, e2, A, B)
            coords = [sum(w[j] * Binv[j][k] for j in range(4)) for k in range(4)]
            assert all(c.denominator == 1 for c in coords), "Order not ring-closed!"
    # Reduced discriminant = sqrt(|det(trd(e_i e_j))|)
    gram = [[2 * qmul_Q(e1, e2, A, B)[0] for e2 in basis] for e1 in basis]
    det = abs(mat_det_frac(gram))
    assert det.denominator == 1
    rd = math.isqrt(det.numerator)
    assert rd * rd == det.numerator

    denoms: List[int] = []
    ad_mats: List[List[List[Fraction]]] = []
    for g in gens:
        gi = qinv_Q(g, A, B)
        M: List[List[Fraction]] = []
        den = 1
        for e in basis:
            w = qmul_Q(qmul_Q(g, e, A, B), gi, A, B)
            row = [sum(w[j] * Binv[j][k] for j in range(4)) for k in range(4)]
            for c in row:
                den = math.lcm(den, c.denominator)
            M.append(row)
        denoms.append(den)
        ad_mats.append(M)
    return rd, denoms, ad_mats


def mat_mul_mod(A: Tuple[int, ...], B: Tuple[int, ...], n: int, mod: int) -> Tuple[int, ...]:
    """Fast flat-tuple n x n matrix multiplication mod `mod`."""
    out = [0] * (n * n)
    for i in range(n):
        row_off = i * n
        for k in range(n):
            aik = A[row_off + k]
            if aik:
                k_off = k * n
                for j in range(n):
                    out[row_off + j] += aik * B[k_off + j]
        for j in range(n):
            out[row_off + j] %= mod
    return tuple(out)


def frac_mat_mod(M: List[List[Fraction]], mod: int) -> Tuple[int, ...]:
    n = len(M)
    out: List[int] = []
    for i in range(n):
        for j in range(n):
            c = M[i][j]
            out.append((c.numerator * pow(c.denominator, -1, mod)) % mod)
    return tuple(out)


def bfs_mat_group_and_joint(
    ad_gens: List[Tuple[int, ...]],
    perm_gens: List[Tuple[int, ...]],
    n_mat: int,
    mod: int,
) -> Tuple[int, int, int, Set[Tuple[int, ...]]]:
    """Enumerate <ad_gens> and joint <(ad_g, perm_g)> via integer-indexed Cayley tables,
    returning (|Ad|, |joint|, |ker|, ker_perms)."""
    id_mat = tuple(1 if i == j else 0 for i in range(n_mat) for j in range(n_mat))
    id_perm = tuple(range(len(perm_gens[0])))
    n_g = len(ad_gens)

    # 1. Enumerate <ad_gens> and build integer right-step table M(w * g) = M(g) * M(w)
    ad_to_id: Dict[Tuple[int, ...], int] = {id_mat: 0}
    ad_els: List[Tuple[int, ...]] = [id_mat]
    ad_step: List[List[int]] = []
    q = deque([0])
    while q:
        uid = q.popleft()
        um = ad_els[uid]
        row = [0] * n_g
        for gi, gm in enumerate(ad_gens):
            nm = mat_mul_mod(gm, um, n_mat, mod)
            nid = ad_to_id.get(nm)
            if nid is None:
                nid = len(ad_els)
                ad_to_id[nm] = nid
                ad_els.append(nm)
                q.append(nid)
            row[gi] = nid
        ad_step.append(row)

    # 2. Enumerate <perm_gens> and build integer right-step table perm(w * g) = perm_comp(cp, gp)
    p_to_id: Dict[Tuple[int, ...], int] = {id_perm: 0}
    p_els: List[Tuple[int, ...]] = [id_perm]
    p_step: List[List[int]] = []
    pq = deque([0])
    while pq:
        uid = pq.popleft()
        up = p_els[uid]
        row = [0] * n_g
        for gi, gp in enumerate(perm_gens):
            np = perm_comp(up, gp)
            nid = p_to_id.get(np)
            if nid is None:
                nid = len(p_els)
                p_to_id[np] = nid
                p_els.append(np)
                pq.append(nid)
            row[gi] = nid
        p_step.append(row)

    # 3. Ultra-fast integer-packed joint BFS: state = mid * n_p + pid
    n_ad = len(ad_els)
    n_p = len(p_els)
    seen = bytearray(n_ad * n_p)
    seen[0] = 1
    jq = deque([0])
    joint_cnt = 1
    ker_perms: Set[Tuple[int, ...]] = {id_perm}
    while jq:
        st = jq.popleft()
        mid, pid = divmod(st, n_p)
        arow = ad_step[mid]
        prow = p_step[pid]
        for gi in range(n_g):
            nmid = arow[gi]
            npid = prow[gi]
            nst = nmid * n_p + npid
            if not seen[nst]:
                seen[nst] = 1
                joint_cnt += 1
                if nmid == 0:
                    ker_perms.add(p_els[npid])
                jq.append(nst)
    assert joint_cnt == n_ad * len(ker_perms)
    return n_ad, joint_cnt, len(ker_perms), ker_perms


def quotient_graph_by_group(
    adj: List[List[int]], group: Set[Tuple[int, ...]]
) -> Tuple[int, int, Dict[int, int], List[List[int]]]:
    """Compute quotient multigraph G / group: returns (V_q, E_q, edge_mult_hist, simple_adj)."""
    n = len(adj)
    orbit_id = [-1] * n
    orbits: List[Set[int]] = []
    for v in range(n):
        if orbit_id[v] == -1:
            orb = {g[v] for g in group}
            oid = len(orbits)
            for u in orb:
                orbit_id[u] = oid
            orbits.append(orb)
    # Count undirected edge orbits (preserving edge multiplicities between vertex orbits)
    e_seen: Set[Tuple[int, int]] = set()
    e_orbits: List[Tuple[int, int, int]] = []  # (min_o, max_o, size)
    for u in range(n):
        for v in adj[u]:
            if u < v and (u, v) not in e_seen:
                eorb = {(min(g[u], g[v]), max(g[u], g[v])) for g in group}
                e_seen |= eorb
                ou, ov = orbit_id[u], orbit_id[v]
                e_orbits.append((min(ou, ov), max(ou, ov), len(eorb)))
    mult_hist = dict(Counter(sz for _, _, sz in e_orbits))
    vq = len(orbits)
    simple_adj_sets = [set() for _ in range(vq)]
    for a, b, _ in e_orbits:
        if a != b:
            simple_adj_sets[a].add(b)
            simple_adj_sets[b].add(a)
    simple_adj = [sorted(s) for s in simple_adj_sets]
    return vq, len(e_orbits), mult_hist, simple_adj


# ==============================================================================
# Build Canonical Graphs: Nauru Y = GP(12, 5) and Dicyclic Z = Cay(Dic_6, S_Z)
# ==============================================================================


def build_nauru_graph() -> List[List[int]]:
    adj: List[List[int]] = [[] for _ in range(24)]
    for i in range(12):
        # Outer 12-cycle
        adj[i].extend([(i - 1) % 12, (i + 1) % 12, 12 + i])
        # Inner 5-star + radial spoke
        adj[12 + i].extend([i, 12 + (i - 5) % 12, 12 + (i + 5) % 12])
    return [sorted(nbrs) for nbrs in adj]


def dic6_mul(g: int, h: int) -> int:
    """Group law on Dic_6 = <x, y | x^12 = 1, y^2 = x^6, y x y^-1 = x^-1>.
    Index 0..11 <-> x^k, 12..23 <-> x^k y."""
    a, sa = g % 12, g // 12
    b, sb = h % 12, h // 12
    if sa == 0 and sb == 0:
        return (a + b) % 12
    if sa == 0 and sb == 1:
        return 12 + (a + b) % 12
    if sa == 1 and sb == 0:
        return 12 + (a - b) % 12
    # (x^a y)(x^b y) = x^{a - b + 6}
    return (a - b + 6) % 12


def dic6_inv(g: int) -> int:
    a, sa = g % 12, g // 12
    if sa == 0:
        return (-a) % 12
    return 12 + (a + 6) % 12


def build_dic6_cayley(gen_set: Sequence[int]) -> List[List[int]]:
    adj: List[List[int]] = [[] for _ in range(24)]
    for g in range(24):
        adj[g] = sorted(dic6_mul(g, s) for s in gen_set)
    return adj


# ==============================================================================
# Gate F1: Pillar I — Twin Duality, Rational 2-Adic Nauru Congruence & Errata
# ==============================================================================


def gate_f1_rational_nauru_and_errata() -> Dict[str, Any]:
    Y = build_nauru_graph()
    auts = graph_automorphisms(Y)
    assert len(auts) == 144

    # Stabilizer of 0 (S_3) and radial edge {0, 12} (V_4)
    stab0 = [p for p in auts if p[0] == 0]
    assert len(stab0) == 6
    a_Y = next(p for p in stab0 if perm_order(p) == 3)
    b_Y = next(p for p in stab0 if perm_order(p) == 2 and p[12] == 12)
    assert perm_comp(b_Y, perm_comp(a_Y, b_Y)) == perm_inv(a_Y)

    # Edge-inverting involutions exchanging 0 <-> 12 and commuting with b_Y
    t_invs = [
        p
        for p in auts
        if p[0] == 12 and p[12] == 0 and perm_order(p) == 2 and perm_comp(p, b_Y) == perm_comp(b_Y, p)
    ]
    assert len(t_invs) == 2
    t0 = next(p for p in t_invs if perm_order(perm_comp(p, a_Y)) == 6)
    t1 = next(p for p in t_invs if perm_order(perm_comp(p, a_Y)) == 12)
    assert perm_comp(b_Y, t0) == t1

    # 1. Universal Algebraic Twin Duality tau((bt)a) = 3 - x
    twin_samples = {}
    for x in [Fraction(3, 2), Fraction(5, 2), Fraction(1, 2), Fraction(2, 3), Fraction(7, 4), Fraction(11, 5)]:
        A, B = Fraction(-3), -x * (3 - x)
        a_q = (Fraction(1, 2), Fraction(1, 2), Fraction(0), Fraction(0))
        b_q = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
        t_q = (Fraction(0), x, Fraction(0), Fraction(1))
        ta = qmul_Q(t_q, a_q, A, B)
        bta = qmul_Q(qmul_Q(b_q, t_q, A, B), a_q, A, B)
        tau_ta = (2 * ta[0]) ** 2 / qnrd_Q(ta, A, B)
        tau_bta = (2 * bta[0]) ** 2 / qnrd_Q(bta, A, B)
        assert tau_ta == x and tau_bta == 3 - x
        twin_samples[str(x)] = {"tau_ta": str(tau_ta), "tau_bta": str(tau_bta)}

    # 2. Exact Modular Adjoint Verification across B_3(3/2), B_5(5/2), B_5(1/2) (Table 2)
    O3_basis = [
        (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(1, 2), Fraction(1, 2), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1, 2), Fraction(1, 2)),
    ]
    O5m_basis = [
        (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(1, 2), Fraction(1, 2), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1, 3), Fraction(0), Fraction(-1, 3)),
        (Fraction(-1, 2), Fraction(1, 6), Fraction(-1, 2), Fraction(-1, 6)),
    ]
    O5p_basis = [
        (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(1, 2), Fraction(1, 2), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1, 3), Fraction(0), Fraction(1, 3)),
        (Fraction(-1, 2), Fraction(1, 6), Fraction(1, 2), Fraction(1, 6)),
    ]
    a_q = (Fraction(1, 2), Fraction(1, 2), Fraction(0), Fraction(0))
    b_q = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))

    rational_configs = [
        (
            "B3_3/2",
            Fraction(-3),
            Fraction(-1),
            O3_basis,
            3,
            [a_q, b_q, (Fraction(0), Fraction(1), Fraction(0), Fraction(1))],
            [(3, 36, 144, 4, 144, 4), (9, 972, 3888, 4, 3888, 4), (15, 2160, 8640, 4, 8640, 4)],
        ),
        (
            "B5_5/2",
            Fraction(-3),
            Fraction(-5),
            O5m_basis,
            5,
            [a_q, b_q, (Fraction(0), Fraction(5, 3), Fraction(0), Fraction(1, 3))],
            [(3, 24, 144, 6, 576, 24), (5, 300, 3600, 12, 3600, 12), (15, 3600, 3600, 1, 14400, 4)],
        ),
        (
            "B5_1/2",
            Fraction(-3),
            Fraction(-5),
            O5p_basis,
            5,
            [a_q, b_q, (Fraction(0), Fraction(1, 3), Fraction(0), Fraction(1, 3))],
            [(3, 24, 576, 24, 144, 6), (5, 300, 3600, 12, 3600, 12), (15, 3600, 14400, 4, 3600, 1)],
        ),
    ]

    table2_results = []
    K33 = [[3, 4, 5], [3, 4, 5], [3, 4, 5], [0, 1, 2], [0, 1, 2], [0, 1, 2]]
    sylow5_count = 0
    b5_norm1_check: Dict[str, Any] = {}

    for name, A, B, basis, exp_rd, gens, checks in rational_configs:
        rd, denoms, ad_mats = q_verify_order_and_adjoint_Q(basis, gens, A, B)
        assert rd == exp_rd and denoms == [1, 1, 2], f"{name}: rd={rd}, denoms={denoms}"
        for mod, exp_ad, exp_j6, exp_k6, exp_j12, exp_k12 in checks:
            ad_g = [frac_mat_mod(M, mod) for M in ad_mats]
            ad_ord, j6, k6, ker6 = bfs_mat_group_and_joint(ad_g, [a_Y, b_Y, t0], 4, mod)
            ad_ord2, j12, k12, ker12 = bfs_mat_group_and_joint(ad_g, [a_Y, b_Y, t1], 4, mod)
            assert ad_ord == ad_ord2 == exp_ad
            assert (j6, k6) == (exp_j6, exp_k6), f"{name} mod {mod} rho6: {(j6, k6)}"
            assert (j12, k12) == (exp_j12, exp_k12), f"{name} mod {mod} rho12: {(j12, k12)}"
            table2_results.append(
                {
                    "curve": name,
                    "mod": mod,
                    "ad_order": ad_ord,
                    "joint_rho6": j6,
                    "ker_rho6": k6,
                    "joint_rho12": j12,
                    "ker_rho12": k12,
                }
            )
            if name == "B3_3/2" and mod == 3:
                vq, eq, mh, qadj = quotient_graph_by_group(Y, ker6)
                assert (vq, eq, mh) == (6, 9, {4: 9}) and graph_isomorphic(qadj, K33)
            if name == "B5_5/2" and mod == 15:
                # Verify unique normal Sylow-5 U_5 of order 25 in Ad_15
                id4 = tuple(1 if i == j else 0 for i in range(4) for j in range(4))
                seen = {id4}
                q = deque([id4])
                while q:
                    cm = q.popleft()
                    for gm in ad_g:
                        nm = mat_mul_mod(gm, cm, 4, 15)
                        if nm not in seen:
                            seen.add(nm)
                            q.append(nm)
                assert len(seen) == 3600
                u5 = []
                for m_el in seen:
                    # Check m_el^25 == I
                    p5 = m_el
                    for _ in range(4):
                        p5 = mat_mul_mod(p5, m_el, 4, 15)
                    p25 = p5
                    for _ in range(4):
                        p25 = mat_mul_mod(p25, p5, 4, 15)
                    if p25 == id4:
                        u5.append(m_el)
                sylow5_count = len(u5)
                assert sylow5_count == 25 and math.gcd(25, 144) == 1
                # Also verify norm-1 subgroup Delta^1 on B5_1/2 twin (= B5_5/2 rho12)
                vq2, eq2, mh2, qadj2 = quotient_graph_by_group(Y, ker12)
                assert (vq2, eq2, mh2) == (6, 9, {4: 9}) and graph_isomorphic(qadj2, K33)

        if name == "B5_1/2":
            # Norm-1 subgroup Delta^1: generated by a (nrd 1), and even-norm combinations b*t*b*t?
            # In B5_1/2: nrd(a)=1, nrd(b)=5, nrd(t)=2/3*... wait nrd((i+k)/3)=(3+15)/9=2!
            # So b has nrd=5 (not sq in Q(1/2)), t has nrd=2 (2-adic valuation 1, unit in Z[1/2] with sq-class 2).
            # Thus Delta^1 = <a, b*a*b^-1, t*a*t^-1, t*b*a*b^-1*t^-1, (t*b)^2? wait nrd(t*b)=10>.
            # Exact norm-1 subgroup in Q*/(Q*^2 * 2^Z) has index 4: parity of #b (mod 2) and #t (mod 2) both even!
            # Schreier generators of the index-4 subgroup (#b even, #t even) in <a, b, t>:
            # Cosets: (0,0)=1, (1,0)=b, (0,1)=t, (1,1)=b*t.
            # Note b^2 = -5 (scalar -> 1 in PB^x), t^2 = -2 (scalar -> 1 in PB^x), b*t*b*t = -b^2 t^2? Wait bt = -tb so (bt)^2 = -b^2 t^2 -> scalar!
            # Thus the index-4 subgroup is generated by the 4 conjugates of a: a, b a b^-1, t a t^-1, (bt) a (bt)^-1!
            def conj_q(g, x):
                return qmul_Q(qmul_Q(g, x, A, B), qinv_Q(g, A, B), A, B)

            a_g, b_g, t_g = gens
            bt_g = qmul_Q(b_g, t_g, A, B)
            d1_q = [a_g, conj_q(b_g, a_g), conj_q(t_g, a_g), conj_q(bt_g, a_g)]
            d1_p6 = [
                a_Y,
                perm_comp(b_Y, perm_comp(a_Y, b_Y)),
                perm_comp(t0, perm_comp(a_Y, t0)),
                perm_comp(perm_comp(b_Y, t0), perm_comp(a_Y, perm_comp(t0, b_Y))),
            ]
            _, _, d1_mats = q_verify_order_and_adjoint_Q(basis, d1_q, A, B)
            # Check |rho_6(Delta^1)| = 36
            p_seen = {tuple(range(24))}
            pq = deque([tuple(range(24))])
            while pq:
                cp = pq.popleft()
                for gp in d1_p6:
                    np = perm_comp(cp, gp)
                    if np not in p_seen:
                        p_seen.add(np)
                        pq.append(np)
            assert len(p_seen) == 36
            ad3_1, j3_1, k3_1, _ = bfs_mat_group_and_joint(
                [frac_mat_mod(M, 3) for M in d1_mats], d1_p6, 4, 3
            )
            ad15_1, j15_1, k15_1, _ = bfs_mat_group_and_joint(
                [frac_mat_mod(M, 15) for M in d1_mats], d1_p6, 4, 15
            )
            assert (ad3_1, k3_1) == (12, 12) and (ad15_1, k15_1) == (900, 4)
            b5_norm1_check = {
                "rho_delta1_order": 36,
                "mod3_ad1": ad3_1,
                "mod3_ker1": k3_1,
                "mod3_overlap1": f"{36 // k3_1}/36",
                "mod15_ad1": ad15_1,
                "mod15_ker1": k15_1,
                "mod15_overlap1": f"{36 // k15_1}/36",
            }

    # 3. Exact Nauru Spectrum, Hashimoto Cadences pi_Y(6..24), & NEG-M24 Corridor
    A_Y = [[1 if j in Y[i] else 0 for j in range(24)] for i in range(24)]
    cp_Y = faddeev_leverrier_charpoly(A_Y)
    # Expected x^4(x^2-9)(x^2-4)^6(x^2-1)^3
    exp_cp_Y = poly_mul(
        poly_pow([1, 0], 4),
        poly_mul(
            [1, 0, -9],
            poly_mul(poly_pow([1, 0, -4], 6), poly_pow([1, 0, -1], 3)),
        ),
    )
    assert cp_Y == exp_cp_Y
    tr_Y, pi_Y = hashimoto_and_ihara_cadences(Y, 24)
    exp_pi_Y = {
        6: 24,
        8: 108,
        10: 216,
        12: 564,
        14: 2232,
        16: 8820,
        18: 28560,
        20: 104292,
        22: 380664,
        24: 1401744,
    }
    for m, val in exp_pi_Y.items():
        assert pi_Y[m] == val
    assert tr_Y[6] == 144 and tr_Y[9] == 0 and tr_Y[18] == 514224 and tr_Y[22] == 8374608
    ram_lo_18 = 2 * (2**18) + 26 - 44 * (2**9)  # 501786
    ram_hi_18 = 2 * (2**18) + 26 + 44 * (2**9)  # 546842
    assert ram_lo_18 == 501786 and ram_hi_18 == 546842
    assert ram_lo_18 <= tr_Y[18] <= ram_hi_18 < 18 * 31824 + 144

    # 4. Exact Structure & Commutator Index of <T, P, L, R>
    T_p = tuple((k + 1) % 12 if k < 12 else 12 + (k + 1) % 12 for k in range(24))
    P_p = tuple(k + 12 if k < 12 else k - 12 for k in range(24))
    L_p = tuple(12 + (k + 4) % 12 if k < 12 else (k - 12 - 4) % 12 for k in range(24))
    R_p = tuple(12 + (k + 9) % 12 if k < 12 else (k - 12 - 9) % 12 for k in range(24))
    id24 = tuple(range(24))
    G_tplr: Set[Tuple[int, ...]] = {id24}
    q = deque([id24])
    while q:
        c = q.popleft()
        for g in (T_p, P_p, L_p, R_p):
            nxt = perm_comp(c, g)
            if nxt not in G_tplr:
                G_tplr.add(nxt)
                q.append(nxt)
    assert len(G_tplr) == 144
    # Commutator subgroup [G, G]
    comm_gens: Set[Tuple[int, ...]] = set()
    G_list = list(G_tplr)
    for g in (T_p, P_p, L_p, R_p):
        gi = perm_inv(g)
        for h in G_list:
            comm_gens.add(perm_comp(perm_comp(g, h), perm_comp(gi, perm_inv(h))))
    comm_sub: Set[Tuple[int, ...]] = {id24}
    cq = deque([id24])
    while cq:
        c = cq.popleft()
        for cg in comm_gens:
            nxt = perm_comp(c, cg)
            if nxt not in comm_sub:
                comm_sub.add(nxt)
                cq.append(nxt)
    assert len(comm_sub) == 6 and len(G_tplr) // len(comm_sub) == 24
    # Check T^6 == (L o R)^6
    T6 = id24
    LR = perm_comp(L_p, R_p)
    LR6 = id24
    for _ in range(6):
        T6 = perm_comp(T6, T_p)
        LR6 = perm_comp(LR6, LR)
    assert T6 == LR6

    return {
        "aut_Y_order": 144,
        "twin_duality_samples": twin_samples,
        "table2_rational_adjoints": table2_results,
        "b5_sylow5_order": sylow5_count,
        "b5_1_2_norm1_refinement": b5_norm1_check,
        "nauru_pi_6_to_24": {str(m): pi_Y[m] for m in sorted(exp_pi_Y)},
        "nauru_m18_corridor": {
            "N18_exact": tr_Y[18],
            "ram_lo": ram_lo_18,
            "ram_hi": ram_hi_18,
            "pi18_exact": 28560,
            "pi18_falsified_31824_N18": 18 * 31824 + 144,
            "ceiling_breach": 31824 - 30380,
        },
        "tplr_group": {"order": 144, "commutator_order": 6, "abelianization_order": 24},
    }


# ==============================================================================
# Gate F2: Pillar I — Unconditional Metric Gonality on Nauru Y
# ==============================================================================


def gate_f2_nauru_metric_gonality() -> Dict[str, Any]:
    Y = build_nauru_graph()
    # 24-star scramble S_star(Y) = {N[v] : v in V(Y)}
    stars = [set([v] + Y[v]) for v in range(24)]
    star_masks = [sum(1 << u for u in st) for st in stars]
    h_val, h_wit = branch_and_bound_hitting_number(star_masks, 24)
    assert h_val == 6
    # Count exact 1-perfect codes (size-6 disjoint covers)
    # Every vertex must appear in exactly one of the 6 chosen stars -> exact partition of 24 into 6 stars of size 4!
    perfect_codes: List[Tuple[int, ...]] = []
    full24 = (1 << 24) - 1

    def find_codes(cov: int, start: int, cur: List[int]) -> None:
        if cov == full24:
            perfect_codes.append(tuple(cur))
            return
        if len(cur) == 6:
            return
        # First uncovered vertex must be covered by one of its 4 closed-star centers
        u = ((~cov) & full24)
        v0 = (u & -u).bit_length() - 1
        for c in [v0] + Y[v0]:
            if c >= start and (star_masks[c] & cov) == 0:
                cur.append(c)
                find_codes(cov | star_masks[c], 0, cur)
                cur.pop()

    # Use canonical deduplication via sorted tuple
    code_set: Set[Tuple[int, ...]] = set()

    def find_codes_canon(cov: int, cur: List[int]) -> None:
        if cov == full24:
            code_set.add(tuple(sorted(cur)))
            return
        u = (~cov) & full24
        v0 = (u & -u).bit_length() - 1
        for c in [v0] + Y[v0]:
            if (star_masks[c] & cov) == 0:
                cur.append(c)
                find_codes_canon(cov | star_masks[c], cur)
                cur.pop()

    find_codes_canon(0, [])
    assert len(code_set) == 4 and (3, 7, 11, 13, 17, 21) in code_set

    # Exact Edmonds-Karp cuts across all disjoint closed-star pairs
    cut_hist: Counter[int] = Counter()
    for i in range(24):
        for j in range(i + 1, 24):
            if stars[i].isdisjoint(stars[j]):
                c = edmonds_karp_edge_cut(Y, stars[i], stars[j])
                cut_hist[c] += 1
    assert dict(cut_hist) == {6: 168}

    # Exact continuous equilateral metric Dhar on D_hex = {0, 1, 2, 14, 19, 12}
    D_hex = [0, 1, 2, 14, 19, 12]
    chips = [1 if v in D_hex else 0 for v in range(24)]
    max_v_steps = 0
    for v in range(24):
        ok, st = discrete_dhar_reaches(Y, chips, v)
        assert ok
        max_v_steps = max(max_v_steps, st)
    assert max_v_steps <= 2

    edge_cells = 0
    max_e_steps = 0
    for u in range(24):
        for v in Y[u]:
            if u < v:
                for reg in (0, 1, 2):
                    ok, st = continuous_metric_dhar_cell(Y, chips, u, v, reg)
                    assert ok, f"Nauru metric Dhar failed on ({u},{v}) reg {reg}"
                    edge_cells += 1
                    max_e_steps = max(max_e_steps, st)
    assert edge_cells == 108 and max_e_steps <= 3

    return {
        "star_scramble_h": h_val,
        "star_scramble_e": 6,
        "disjoint_star_pairs": 168,
        "cut_distribution": dict(cut_hist),
        "exact_1_perfect_codes": [list(c) for c in sorted(code_set)],
        "D_hex": D_hex,
        "discrete_vertices_passed": 24,
        "discrete_max_steps": max_v_steps,
        "continuous_edge_cells_passed": edge_cells,
        "continuous_max_steps": max_e_steps,
        "total_cells_passed": 24 + edge_cells,
    }


# ==============================================================================
# Gate F3: Pillar II — Complete Real-Quadratic & Cubic Lame Nauru Census
# ==============================================================================


def siegel_zeta_minus_one(DF: int) -> Fraction:
    """Exact Siegel formula zeta_F(-1) = (1/60) sum_{b^2 < DF, b == DF mod 2} sigma_1((DF - b^2)/4)."""
    tot = 0
    bmax = math.isqrt(DF - 1)
    for b in range(-bmax, bmax + 1):
        if (b - DF) % 2 == 0:
            n = (DF - b * b) // 4
            if n > 0:
                sig1 = sum(d for d in range(1, n + 1) if n % d == 0)
                tot += sig1
    return Fraction(tot, 60)


def gate_f3_real_quadratic_and_cubic_census() -> Dict[str, Any]:
    # 1. Exhaustive primitive irreducible quadratics 2x^2 - sx + p = 0 with both roots in (0, 3)
    quad_moduli = []
    for s in range(1, 12):
        for p in range(1, 3 * s):
            if 18 - 3 * s + p <= 0:
                continue
            if math.gcd(math.gcd(2, s), p) != 1:
                continue
            disc = s * s - 8 * p
            if disc <= 0:
                continue
            r = math.isqrt(disc)
            if r * r == disc:
                continue
            # Fundamental discriminant DF
            sqf = disc
            d = 2
            while d * d <= sqf:
                while sqf % (d * d) == 0:
                    sqf //= d * d
                d += 1
            DF = sqf if sqf % 4 == 1 else 4 * sqf
            quad_moduli.append({"poly": f"2x^2 - {s}x + {p}", "s": s, "p": p, "disc": disc, "DF": DF})
    assert len(quad_moduli) == 6
    fields_found = sorted({m["DF"] for m in quad_moduli})
    assert fields_found == [8, 12, 17, 28]
    zetas = {DF: str(siegel_zeta_minus_one(DF)) for DF in fields_found}
    assert zetas == {8: "1/12", 12: "1/6", 17: "1/3", 28: "2/3"}

    # 2. Exhaustive primitive irreducible cubics 2x^3 - c2 x^2 + c1 x - c0 = 0 with all 3 real roots in (0, 3)
    cubic_moduli = []
    for c2 in range(1, 18):
        for c1 in range(1, 54):
            if c2 * c2 <= 6 * c1:
                continue
            # Critical points of f(x) = 2x^3 - c2 x^2 + c1 x - c0: f'(x) = 6x^2 - 2 c2 x + c1 = 0
            # Roots r_pm = (c2 +- sqrt(c2^2 - 6 c1)) / 6 must lie in (0, 3)
            disc_p = c2 * c2 - 6 * c1
            # Check r_plus < 3 <=> sqrt(disc_p) < 18 - c2
            if 18 - c2 <= 0 or disc_p >= (18 - c2) ** 2:
                continue
            for c0 in range(1, 54):
                if math.gcd(math.gcd(2, c2), math.gcd(c1, c0)) != 1:
                    continue
                if 54 - 9 * c2 + 3 * c1 - c0 <= 0:
                    continue
                # Cubic discriminant of a x^3 + b x^2 + c x + d with (a,b,c,d) = (2,-c2,c1,-c0)
                a, b, c, d_coef = 2, -c2, c1, -c0
                disc3 = (
                    18 * a * b * c * d_coef
                    - 4 * (b**3) * d_coef
                    + (b**2) * (c**2)
                    - 4 * a * (c**3)
                    - 27 * (a**2) * (d_coef**2)
                )
                if disc3 <= 0:
                    continue
                # Verify no rational roots (candidates +- p/q with p | c0, q | 2)
                has_rat = False
                for q_den in (1, 2):
                    for p_num in range(1, c0 + 1):
                        if c0 % p_num == 0:
                            # f(p/q) * q^3 == 0
                            val = (
                                2 * (p_num**3)
                                - c2 * (p_num**2) * q_den
                                + c1 * p_num * (q_den**2)
                                - c0 * (q_den**3)
                            )
                            if val == 0:
                                has_rat = True
                                break
                    if has_rat:
                        break
                if has_rat:
                    continue
                # Check all 3 real roots strictly in (0, 3): since disc3 > 0, f(0) < 0, f(3) > 0,
                # and both critical points lie in (0, 3), all 3 roots lie in (0, 3) automatically!
                # Check reciprocal roots z = 1/x mod 16: c0 z^3 - c1 z^2 + c2 z - 2 == 0 mod 16
                recip_roots = [
                    z for z in range(16) if (c0 * (z**3) - c1 * (z**2) + c2 * z - 2) % 16 == 0
                ]
                cubic_moduli.append(
                    {
                        "coeffs": [2, -c2, c1, -c0],
                        "disc_poly": disc3,
                        "recip_roots_mod16": recip_roots,
                    }
                )
    assert len(cubic_moduli) == 4
    cubic_set = {tuple(m["coeffs"]) for m in cubic_moduli}
    assert cubic_set == {
        (2, -9, 10, -1),
        (2, -9, 10, -2),
        (2, -8, 8, -1),
        (2, -10, 14, -5),
    }
    # Check exact field discriminants (for all 4, poly disc = d_F or 4*d_F? Let's verify!)
    # (2,-9,10,-1): disc=316; (2,-9,10,-2): disc=316; (2,-8,8,-1): disc=148; (2,-10,14,-5): disc=148!
    for m in cubic_moduli:
        if m["coeffs"] in ([2, -9, 10, -1], [2, -9, 10, -2]):
            assert m["disc_poly"] == 316 and len(m["recip_roots_mod16"]) == 1
        else:
            assert m["disc_poly"] == 148 and len(m["recip_roots_mod16"]) == 0

    return {
        "real_quadratic_count": len(quad_moduli),
        "real_quadratic_moduli": quad_moduli,
        "siegel_zeta_minus_one": {str(k): v for k, v in zetas.items()},
        "cubic_count": len(cubic_moduli),
        "cubic_moduli": cubic_moduli,
    }


# ==============================================================================
# Gate F4: Pillar II — Complete Field-by-Field Real-Quadratic Congruence Atlas
# ==============================================================================


def qf_add(a: Tuple[Fraction, Fraction], b: Tuple[Fraction, Fraction]) -> Tuple[Fraction, Fraction]:
    return (a[0] + b[0], a[1] + b[1])


def qf_sub(a: Tuple[Fraction, Fraction], b: Tuple[Fraction, Fraction]) -> Tuple[Fraction, Fraction]:
    return (a[0] - b[0], a[1] - b[1])


def qf_neg(a: Tuple[Fraction, Fraction]) -> Tuple[Fraction, Fraction]:
    return (-a[0], -a[1])


def qf_mul_gen(
    a: Tuple[Fraction, Fraction], b: Tuple[Fraction, Fraction], tr_w: int, nr_w: int
) -> Tuple[Fraction, Fraction]:
    """Multiply in Q[w]/(w^2 - tr_w * w + nr_w) = (a0 + a1 w)(b0 + b1 w)."""
    return (
        a[0] * b[0] - nr_w * a[1] * b[1],
        a[0] * b[1] + a[1] * b[0] + tr_w * a[1] * b[1],
    )


def qf_norm_gen(a: Tuple[Fraction, Fraction], tr_w: int, nr_w: int) -> Fraction:
    return a[0] * a[0] + tr_w * a[0] * a[1] + nr_w * a[1] * a[1]


def qf_inv_gen(a: Tuple[Fraction, Fraction], tr_w: int, nr_w: int) -> Tuple[Fraction, Fraction]:
    n = qf_norm_gen(a, tr_w, nr_w)
    # conj(a0 + a1 w) = (a0 + tr_w a1) - a1 w
    return ((a[0] + tr_w * a[1]) / n, -a[1] / n)


def qmul_F(x, y, A, B, tr_w: int, nr_w: int):
    mul = lambda u, v: qf_mul_gen(u, v, tr_w, nr_w)
    x0, x1, x2, x3 = x
    y0, y1, y2, y3 = y
    AB = mul(A, B)
    return (
        qf_add(
            qf_add(mul(x0, y0), mul(A, mul(x1, y1))),
            qf_add(mul(B, mul(x2, y2)), qf_neg(mul(AB, mul(x3, y3)))),
        ),
        qf_add(
            qf_add(mul(x0, y1), mul(x1, y0)),
            qf_add(qf_neg(mul(B, mul(x2, y3))), mul(B, mul(x3, y2))),
        ),
        qf_add(
            qf_add(mul(x0, y2), mul(x2, y0)),
            qf_add(mul(A, mul(x1, y3)), qf_neg(mul(A, mul(x3, y1)))),
        ),
        qf_add(
            qf_add(mul(x0, y3), mul(x3, y0)),
            qf_add(mul(x1, y2), qf_neg(mul(x2, y1))),
        ),
    )


def qnrd_F(x, A, B, tr_w: int, nr_w: int):
    mul = lambda u, v: qf_mul_gen(u, v, tr_w, nr_w)
    AB = mul(A, B)
    return qf_add(
        qf_add(mul(x[0], x[0]), qf_neg(mul(A, mul(x[1], x[1])))),
        qf_add(qf_neg(mul(B, mul(x[2], x[2]))), mul(AB, mul(x[3], x[3]))),
    )


def qinv_F(x, A, B, tr_w: int, nr_w: int):
    ni = qf_inv_gen(qnrd_F(x, A, B, tr_w, nr_w), tr_w, nr_w)
    mul = lambda u, v: qf_mul_gen(u, v, tr_w, nr_w)
    return (mul(x[0], ni), mul(qf_neg(x[1]), ni), mul(qf_neg(x[2]), ni), mul(qf_neg(x[3]), ni))


def mat4_inv_F(M, tr_w: int, nr_w: int):
    """Invert 4x4 matrix over quadratic field Q[w]/(w^2 - tr_w w + nr_w)."""
    zero = (Fraction(0), Fraction(0))
    one = (Fraction(1), Fraction(0))
    mul = lambda u, v: qf_mul_gen(u, v, tr_w, nr_w)
    aug = [list(M[i]) + [one if i == j else zero for j in range(4)] for i in range(4)]
    for i in range(4):
        piv = next(r for r in range(i, 4) if aug[r][i] != zero)
        aug[i], aug[piv] = aug[piv], aug[i]
        pi = qf_inv_gen(aug[i][i], tr_w, nr_w)
        aug[i] = [mul(v, pi) for v in aug[i]]
        for r in range(4):
            if r != i and aug[r][i] != zero:
                fac = aug[r][i]
                aug[r] = [qf_sub(aug[r][c], mul(fac, aug[i][c])) for c in range(8)]
    return [row[4:] for row in aug]


def mat4_det_F(M, tr_w: int, nr_w: int):
    zero = (Fraction(0), Fraction(0))
    one = (Fraction(1), Fraction(0))
    mul = lambda u, v: qf_mul_gen(u, v, tr_w, nr_w)
    mat = [list(row) for row in M]
    det = one
    for i in range(4):
        piv = next(r for r in range(i, 4) if mat[r][i] != zero)
        if piv != i:
            mat[i], mat[piv] = mat[piv], mat[i]
            det = qf_neg(det)
        det = mul(det, mat[i][i])
        pi = qf_inv_gen(mat[i][i], tr_w, nr_w)
        for r in range(i + 1, 4):
            fac = mul(mat[r][i], pi)
            for c in range(i, 4):
                mat[r][c] = qf_sub(mat[r][c], mul(fac, mat[i][c]))
    return det


def close_ring_8_sqrtD(gens, A, B, D: int):
    """HNF Z-rank-8 ring closure inside (A, B / Q(sqrt(D)))."""
    def to8(q):
        return [q[i][j] for i in range(4) for j in range(2)]

    def from8(v):
        return tuple((v[2 * i], v[2 * i + 1]) for i in range(4))

    basis_q = list(gens)
    for _ in range(12):
        den = 1
        for q in basis_q:
            for c in to8(q):
                den = math.lcm(den, c.denominator)
        hnf = hnf_rows([[int(c * den) for c in to8(q)] for q in basis_q])
        basis_q = [from8([Fraction(v, den) for v in r]) for r in hnf]
        prods = list(basis_q) + [qmul_F(x, y, A, B, 0, -D) for x in basis_q for y in basis_q]
        den2 = 1
        for q in prods:
            for c in to8(q):
                den2 = math.lcm(den2, c.denominator)
        hnf2 = hnf_rows([[int(c * den2) for c in to8(q)] for q in prods])
        basis_q2 = [from8([Fraction(v, den2) for v in r]) for r in hnf2]
        if basis_q2 == basis_q:
            return basis_q
        basis_q = basis_q2
    raise RuntimeError("Z-rank-8 ring failed to close")


def gate_f4_real_quadratic_congruence() -> Dict[str, Any]:
    Y = build_nauru_graph()
    auts = graph_automorphisms(Y)
    stab0 = [p for p in auts if p[0] == 0]
    a_Y = next(p for p in stab0 if perm_order(p) == 3)
    b_Y = next(p for p in stab0 if perm_order(p) == 2 and p[12] == 12)
    t_invs = [
        p
        for p in auts
        if p[0] == 12 and p[12] == 0 and perm_order(p) == 2 and perm_comp(p, b_Y) == perm_comp(b_Y, p)
    ]
    t0 = next(p for p in t_invs if perm_order(perm_comp(p, a_Y)) == 6)
    t1 = next(p for p in t_invs if perm_order(perm_comp(p, a_Y)) == 12)

    zero = (Fraction(0), Fraction(0))
    one = (Fraction(1), Fraction(0))

    # --- Field 1: Q(sqrt(17)), phi^2 - phi - 4 = 0 (tr_w=1, nr_w=-4) ---
    tr17, nr17 = 1, -4
    A17, B17 = (Fraction(-3), Fraction(0)), (Fraction(-1), Fraction(0))
    a17 = ((Fraction(1, 2), Fraction(0)), (Fraction(1, 2), Fraction(0)), zero, zero)
    b17 = (zero, zero, one, zero)
    # t_pure = (i + (phi - 2) k) / 3
    t17 = (zero, (Fraction(1, 3), Fraction(0)), zero, (Fraction(-2, 3), Fraction(1, 3)))
    O17 = [
        a17,
        t17,
        (zero, zero, (Fraction(1, 2), Fraction(0)), (Fraction(1, 2), Fraction(0))),
        (zero, zero, zero, one),
    ]
    B17_inv = mat4_inv_F(O17, tr17, nr17)
    # Verify ring closure & maximal discriminant norm 1
    for e1 in O17:
        for e2 in O17:
            w = qmul_F(e1, e2, A17, B17, tr17, nr17)
            for k in range(4):
                c = zero
                for j in range(4):
                    c = qf_add(c, qf_mul_gen(w[j], B17_inv[j][k], tr17, nr17))
                assert c[0].denominator == 1 and c[1].denominator == 1
    gram17 = [
        [qf_mul_gen((Fraction(2), Fraction(0)), qmul_F(e1, e2, A17, B17, tr17, nr17)[0], tr17, nr17) for e2 in O17]
        for e1 in O17
    ]
    det17 = mat4_det_F(gram17, tr17, nr17)
    assert abs(qf_norm_gen(det17, tr17, nr17)) == 1

    # Reduce mod v^2 (O_F / v^2 = Z/4Z via alpha + beta*phi -> alpha mod 4)
    def ad17_mod_v2(g):
        gi = qinv_F(g, A17, B17, tr17, nr17)
        flat = []
        for e in O17:
            w = qmul_F(qmul_F(g, e, A17, B17, tr17, nr17), gi, A17, B17, tr17, nr17)
            for k in range(4):
                c = zero
                for j in range(4):
                    c = qf_add(c, qf_mul_gen(w[j], B17_inv[j][k], tr17, nr17))
                # Since pi_v' = 3 - phi -> 3 mod 4 (invertible mod 4), clear denominators mod 4 via phi -> 0
                val = c[0]  # phi = 0 mod v^2 (since v=(2+phi), v^2=(4+4phi+phi^2)=(8+5phi) -> phi = -8/5 = 0 mod 4!)
                flat.append((val.numerator * pow(val.denominator, -1, 4)) % 4)
        return tuple(flat)

    ad17_g = [ad17_mod_v2(g) for g in (a17, b17, t17)]
    ad17_ord, j17_6, k17_6, ker17_6 = bfs_mat_group_and_joint(ad17_g, [a_Y, b_Y, t0], 4, 4)
    _, j17_12, k17_12, _ = bfs_mat_group_and_joint(ad17_g, [a_Y, b_Y, t1], 4, 4)
    assert (ad17_ord, j17_6, k17_6, j17_12, k17_12) == (48, 144, 3, 576, 12)
    vq17, eq17, mh17, adj17 = quotient_graph_by_group(Y, ker17_6)
    Q3 = [[1, 2, 4], [0, 3, 5], [0, 3, 6], [1, 2, 7], [0, 5, 6], [1, 4, 7], [2, 4, 7], [3, 5, 6]]
    assert (vq17, eq17, mh17) == (8, 12, {3: 12}) and graph_isomorphic(adj17, Q3)

    # --- Field 2: Q(sqrt(2)), Eichler order E(q_7), q_7 = (7, sqrt(2) - 4) ---
    D2 = 2
    A2, B2 = (Fraction(-3), Fraction(0)), (Fraction(-3), Fraction(-1))
    one_q = (one, zero, zero, zero)
    sq2 = ((Fraction(0), Fraction(1)), zero, zero, zero)
    a2 = ((Fraction(1, 2), Fraction(0)), (Fraction(1, 2), Fraction(0)), zero, zero)
    b2 = (zero, zero, one, zero)
    t2 = (zero, (Fraction(1, 3), Fraction(1, 3)), zero, (Fraction(1, 3), Fraction(0)))
    E_q7 = close_ring_8_sqrtD([one_q, sq2, a2, b2, t2], A2, B2, D2)
    assert len(E_q7) == 8
    T8_q7 = [[4 * qmul_F(x, y, A2, B2, 0, -D2)[0][0] for y in E_q7] for x in E_q7]
    det_q7 = int(mat_det_frac(T8_q7))
    assert det_q7 == 200704 and det_q7 == 49 * (8**4)

    # 8x8 adjoint matrices on E_q7 over Z
    E_q7_rows = [[q[i][j] for i in range(4) for j in range(2)] for q in E_q7]
    E_q7_inv = mat_inv_frac(E_q7_rows)

    def ad8_mats(gens_q, basis_q, basis_inv, A, B, D):
        denoms = []
        mats = []
        for g in gens_q:
            gi = qinv_F(g, A, B, 0, -D)
            M = []
            den = 1
            for e in basis_q:
                w = qmul_F(qmul_F(g, e, A, B, 0, -D), gi, A, B, 0, -D)
                wv = [w[i][j] for i in range(4) for j in range(2)]
                row = [sum(wv[t] * basis_inv[t][k] for t in range(8)) for k in range(8)]
                for c in row:
                    den = math.lcm(den, c.denominator)
                M.append(row)
            denoms.append(den)
            mats.append(M)
        return denoms, mats

    q2_denoms, q2_mats = ad8_mats([a2, b2, t2], E_q7, E_q7_inv, A2, B2, D2)
    assert q2_denoms == [1, 1, 2]

    # Project 8x8 Z-action to 4x4 action modulo q_7 (sqrt(2) = 4 mod 7), q_7' (sqrt(2) = 3 mod 7), and mod 3 (F_9)
    # Using exact quotient module E(q_7) / I E(q_7):
    # For q_7 = (7, sqrt(2)-4), left-multiplication by (sqrt(2)-4) on E_q7 has 4-dim cokernel over F_7!
    def reduce_8_mod_prime_ideal(ad8_list, basis_q, basis_inv, A, B, D, p, root_mod_p):
        """Build exact 4x4 matrices over F_p for the quotient E / (p, sqrt(D)-r) E."""
        # Action matrix S of (sqrt(D) - r) on Z^8 basis
        elem = ((Fraction(-root_mod_p), Fraction(1)), zero, zero, zero)
        S_rows = []
        for e in basis_q:
            w = qmul_F(elem, e, A, B, 0, -D)
            wv = [w[i][j] for i in range(4) for j in range(2)]
            row = [int(sum(wv[t] * basis_inv[t][k] for t in range(8))) % p for k in range(8)]
            S_rows.append(row)
        # Find row-echelon basis of S_rows over F_p (rank 4), and complementary 4 pivot columns
        mat = [r[:] for r in S_rows]
        piv_cols = []
        r_idx = 0
        for col in range(8):
            piv = next((r for r in range(r_idx, 8) if mat[r][col] % p != 0), -1)
            if piv == -1:
                continue
            mat[r_idx], mat[piv] = mat[piv], mat[r_idx]
            inv_v = pow(mat[r_idx][col], -1, p)
            mat[r_idx] = [(v * inv_v) % p for v in mat[r_idx]]
            for r in range(8):
                if r != r_idx and mat[r][col] != 0:
                    f = mat[r][col]
                    mat[r] = [(mat[r][c] - f * mat[r_idx][c]) % p for c in range(8)]
            piv_cols.append(col)
            r_idx += 1
        assert len(piv_cols) == 4
        free_cols = [c for c in range(8) if c not in piv_cols]
        # Projection map P (8 x 4 over F_p): sends e_j -> coords in free_cols after eliminating piv_cols
        proj = []
        for j in range(8):
            v = [0] * 8
            v[j] = 1
            for ri, pc in enumerate(piv_cols):
                f = v[pc]
                if f:
                    for c in range(8):
                        v[c] = (v[c] - f * mat[ri][c]) % p
            proj.append([v[fc] for fc in free_cols])
        # Induced 4x4 matrix on free_cols: M4[a] = proj(M8[free_cols[a]])
        out_mats = []
        for M8 in ad8_list:
            m4 = []
            for a_idx in range(4):
                row8 = [
                    (M8[free_cols[a_idx]][c].numerator * pow(M8[free_cols[a_idx]][c].denominator, -1, p)) % p
                    for c in range(8)
                ]
                row4 = [sum(row8[k] * proj[k][b_idx] for k in range(8)) % p for b_idx in range(4)]
                m4.extend(row4)
            out_mats.append(tuple(m4))
        return out_mats

    q2_mod_q7 = reduce_8_mod_prime_ideal(q2_mats, E_q7, E_q7_inv, A2, B2, D2, 7, 4)
    ad_q7, j_q7_6, k_q7_6, ker_q7_6 = bfs_mat_group_and_joint(q2_mod_q7, [a_Y, b_Y, t0], 4, 7)
    _, j_q7_12, k_q7_12, ker_q7_12 = bfs_mat_group_and_joint(q2_mod_q7, [a_Y, b_Y, t1], 4, 7)
    assert (ad_q7, j_q7_6, k_q7_6, j_q7_12, k_q7_12) == (588, 7056, 12, 7056, 12)
    # Check quotient Y / ker_12 = Theta_3 (V=2, E=3, mults={12:3}, 0 fixed vertices) & non-isomorphic kernels C6xC2 vs A4
    vq2_6, eq2_6, mh2_6, _ = quotient_graph_by_group(Y, ker_q7_6)
    vq2_12, eq2_12, mh2_12, _ = quotient_graph_by_group(Y, ker_q7_12)
    assert (vq2_6, eq2_6, mh2_6) == (2, 3, {12: 3}) and (vq2_12, eq2_12, mh2_12) == (2, 3, {12: 3})
    assert all(all(p[v] != v for v in range(24)) for p in ker_q7_6 if p != tuple(range(24)))
    assert all(all(p[v] != v for v in range(24)) for p in ker_q7_12 if p != tuple(range(24)))
    ord_hist_q2_6 = dict(sorted(Counter(perm_order(p) for p in ker_q7_6).items()))
    ord_hist_q2_12 = dict(sorted(Counter(perm_order(p) for p in ker_q7_12).items()))
    assert ord_hist_q2_6 == {1: 1, 2: 3, 3: 2, 6: 6}  # C_6 x C_2
    assert ord_hist_q2_12 == {1: 1, 2: 3, 3: 8}  # A_4

    # Norm-1 subgroup Delta_2^1 = <a, b a b^-1, t a t^-1, (bt) a (bt)^-1>
    bt2 = qmul_F(b2, t2, A2, B2, 0, -D2)
    d1_q2 = [
        a2,
        qmul_F(qmul_F(b2, a2, A2, B2, 0, -D2), qinv_F(b2, A2, B2, 0, -D2), A2, B2, 0, -D2),
        qmul_F(qmul_F(t2, a2, A2, B2, 0, -D2), qinv_F(t2, A2, B2, 0, -D2), A2, B2, 0, -D2),
        qmul_F(qmul_F(bt2, a2, A2, B2, 0, -D2), qinv_F(bt2, A2, B2, 0, -D2), A2, B2, 0, -D2),
    ]
    d1_p6 = [
        a_Y,
        perm_comp(b_Y, perm_comp(a_Y, b_Y)),
        perm_comp(t0, perm_comp(a_Y, t0)),
        perm_comp(perm_comp(b_Y, t0), perm_comp(a_Y, perm_comp(t0, b_Y))),
    ]
    _, d1_q2_mats = ad8_mats(d1_q2, E_q7, E_q7_inv, A2, B2, D2)
    d1_q7_m4 = reduce_8_mod_prime_ideal(d1_q2_mats, E_q7, E_q7_inv, A2, B2, D2, 7, 4)
    ad1_q7, _, ker1_q7, _ = bfs_mat_group_and_joint(d1_q7_m4, d1_p6, 4, 7)
    assert (ad1_q7, ker1_q7) == (147, 12)

    # Conjugate prime q_7' (sqrt(2) = 3 mod 7) and inert prime (3)
    q2_mod_q7p = reduce_8_mod_prime_ideal(q2_mats, E_q7, E_q7_inv, A2, B2, D2, 7, 3)
    ad_q7p, j_q7p, k_q7p, _ = bfs_mat_group_and_joint(q2_mod_q7p, [a_Y, b_Y, t0], 4, 7)
    d1_q7p_m4 = reduce_8_mod_prime_ideal(d1_q2_mats, E_q7, E_q7_inv, A2, B2, D2, 7, 3)
    ad1_q7p, _, ker1_q7p, _ = bfs_mat_group_and_joint(d1_q7p_m4, d1_p6, 4, 7)
    assert (ad_q7p, ad1_q7p, j_q7p, k_q7p, ker1_q7p) == (336, 168, 24192, 72, 36)

    q2_mod3 = [frac_mat_mod(M, 3) for M in q2_mats]
    ad_q2_m3, j_q2_m3, k_q2_m3, _ = bfs_mat_group_and_joint(q2_mod3, [a_Y, b_Y, t0], 8, 3)
    d1_q2_m3 = [frac_mat_mod(M, 3) for M in d1_q2_mats]
    ad1_q2_m3, _, ker1_q2_m3, _ = bfs_mat_group_and_joint(d1_q2_m3, d1_p6, 8, 3)
    assert (ad_q2_m3, ad1_q2_m3, j_q2_m3, k_q2_m3, ker1_q2_m3) == (720, 360, 51840, 72, 36)
    # By Goursat (gcd(147, 360) = 3, PSL_2(F_9) = A_6 simple -> no index-3 quotient), joint mod 3*q_7 has |Ad^1| = 147*360 = 52920
    assert ad1_q7 * ad1_q2_m3 == 52920

    # --- Field 3: Q(sqrt(3)), Eichler order E(p_3) ---
    D3 = 3
    A3, B3 = (Fraction(-3), Fraction(0)), (Fraction(-2), Fraction(0))
    sq3 = ((Fraction(0), Fraction(1)), zero, zero, zero)
    a3 = ((Fraction(1, 2), Fraction(0)), (Fraction(1, 2), Fraction(0)), zero, zero)
    bp3 = (zero, zero, (Fraction(-1, 2), Fraction(1, 2)), zero)
    tp3 = (zero, (Fraction(0), Fraction(1, 3)), zero, (Fraction(1, 2), Fraction(-1, 6)))
    E_p3 = close_ring_8_sqrtD([one_q, sq3, a3, bp3, tp3], A3, B3, D3)
    T8_p3 = [[4 * qmul_F(x, y, A3, B3, 0, -D3)[0][0] for y in E_p3] for x in E_p3]
    det_p3 = int(mat_det_frac(T8_p3))
    assert det_p3 == 186624 and det_p3 == 9 * (12**4)
    E_p3_rows = [[q[i][j] for i in range(4) for j in range(2)] for q in E_p3]
    E_p3_inv = mat_inv_frac(E_p3_rows)
    q3_denoms, q3_mats = ad8_mats([a3, bp3, tp3], E_p3, E_p3_inv, A3, B3, D3)
    assert q3_denoms == [1, 1, 2]
    q3_mod3 = [frac_mat_mod(M, 3) for M in q3_mats]
    ad_q3, j_q3_6, k_q3_6, _ = bfs_mat_group_and_joint(q3_mod3, [a_Y, b_Y, t0], 8, 3)
    _, j_q3_12, k_q3_12, _ = bfs_mat_group_and_joint(q3_mod3, [a_Y, b_Y, t1], 8, 3)
    assert (ad_q3, j_q3_6, k_q3_6, j_q3_12, k_q3_12) == (972, 3888, 4, 3888, 4)
    # Subgroup tiers: Delta^1 (4 conjugates of a3) and Aut^+(Y) (<a3, b3, t3 a3 t3^-1, t3 b3 t3^-1>)
    bt3 = qmul_F(bp3, tp3, A3, B3, 0, -D3)
    d1_q3 = [
        a3,
        qmul_F(qmul_F(bp3, a3, A3, B3, 0, -D3), qinv_F(bp3, A3, B3, 0, -D3), A3, B3, 0, -D3),
        qmul_F(qmul_F(tp3, a3, A3, B3, 0, -D3), qinv_F(tp3, A3, B3, 0, -D3), A3, B3, 0, -D3),
        qmul_F(qmul_F(bt3, a3, A3, B3, 0, -D3), qinv_F(bt3, A3, B3, 0, -D3), A3, B3, 0, -D3),
    ]
    _, d1_q3_mats = ad8_mats(d1_q3, E_p3, E_p3_inv, A3, B3, D3)
    ad1_q3, _, ker1_q3, _ = bfs_mat_group_and_joint([frac_mat_mod(M, 3) for M in d1_q3_mats], d1_p6, 8, 3)
    dp_q3 = [
        a3,
        bp3,
        qmul_F(qmul_F(tp3, a3, A3, B3, 0, -D3), qinv_F(tp3, A3, B3, 0, -D3), A3, B3, 0, -D3),
        qmul_F(qmul_F(tp3, bp3, A3, B3, 0, -D3), qinv_F(tp3, A3, B3, 0, -D3), A3, B3, 0, -D3),
    ]
    dp_p6 = [a_Y, b_Y, perm_comp(t0, perm_comp(a_Y, t0)), perm_comp(t0, perm_comp(b_Y, t0))]
    _, dp_q3_mats = ad8_mats(dp_q3, E_p3, E_p3_inv, A3, B3, D3)
    adp_q3, _, kerp_q3, _ = bfs_mat_group_and_joint([frac_mat_mod(M, 3) for M in dp_q3_mats], dp_p6, 8, 3)
    assert (ad1_q3, ker1_q3, adp_q3, kerp_q3) == (243, 4, 486, 4)

    # --- Field 4: Q(sqrt(7)), Genuine Congruence Shimura Curve of Exact Level (3) = p_3 p_3' ---
    tr7, nr7 = 0, -7
    A7, B7 = (Fraction(-3), Fraction(0)), (Fraction(-2), Fraction(0))
    a7 = ((Fraction(1, 2), Fraction(0)), (Fraction(1, 2), Fraction(0)), zero, zero)
    b7 = (zero, zero, one, zero)
    t7 = (zero, (Fraction(1, 3), Fraction(0)), zero, (Fraction(1, 2), Fraction(-1, 6)))
    O7 = [
        a7,
        t7,
        (zero, zero, (Fraction(3, 4), Fraction(-1, 4)), (Fraction(3, 4), Fraction(-1, 4))),
        (zero, zero, zero, (Fraction(3, 2), Fraction(-1, 2))),
    ]
    B7_inv = mat4_inv_F(O7, tr7, nr7)
    for e1 in O7:
        for e2 in O7:
            w = qmul_F(e1, e2, A7, B7, tr7, nr7)
            for k in range(4):
                c = zero
                for j in range(4):
                    c = qf_add(c, qf_mul_gen(w[j], B7_inv[j][k], tr7, nr7))
                assert c[0].denominator == 1 and c[1].denominator == 1
    gram7 = [
        [qf_mul_gen((Fraction(2), Fraction(0)), qmul_F(e1, e2, A7, B7, tr7, nr7)[0], tr7, nr7) for e2 in O7]
        for e1 in O7
    ]
    assert abs(qf_norm_gen(mat4_det_F(gram7, tr7, nr7), tr7, nr7)) == 1

    def ad7_mod_p3(g, sq7_mod3: int):
        gi = qinv_F(g, A7, B7, tr7, nr7)
        flat = []
        for e in O7:
            w = qmul_F(qmul_F(g, e, A7, B7, tr7, nr7), gi, A7, B7, tr7, nr7)
            for k in range(4):
                c = zero
                for j in range(4):
                    c = qf_add(c, qf_mul_gen(w[j], B7_inv[j][k], tr7, nr7))
                val = c[0] + c[1] * sq7_mod3
                flat.append((val.numerator * pow(val.denominator, -1, 3)) % 3)
        return tuple(flat)

    ad7_p3 = [ad7_mod_p3(g, 1) for g in (a7, b7, t7)]
    ad7_p3p = [ad7_mod_p3(g, 2) for g in (a7, b7, t7)]
    o_p3, j_p3_6, k_p3_6, _ = bfs_mat_group_and_joint(ad7_p3, [a_Y, b_Y, t0], 4, 3)
    _, j_p3_12, k_p3_12, _ = bfs_mat_group_and_joint(ad7_p3, [a_Y, b_Y, t1], 4, 3)
    o_p3p, j_p3p_6, k_p3p_6, _ = bfs_mat_group_and_joint(ad7_p3p, [a_Y, b_Y, t0], 4, 3)
    _, j_p3p_12, k_p3p_12, _ = bfs_mat_group_and_joint(ad7_p3p, [a_Y, b_Y, t1], 4, 3)
    assert (o_p3, k_p3_6, k_p3_12) == (24, 24, 6)
    assert (o_p3p, k_p3p_6, k_p3p_12) == (24, 6, 24)

    # Joint mod (3) = p_3 * p_3' (block-diagonal 8x8 mod 3, or pair of 4x4 mod 3!)
    def bfs_pair4_mod3(g1, g2, p_gens):
        id4 = tuple(1 if i == j else 0 for i in range(4) for j in range(4))
        id24 = tuple(range(24))
        ad_s = {(id4, id4)}
        q = deque([(id4, id4)])
        while q:
            m1, m2 = q.popleft()
            for a1, a2 in zip(g1, g2):
                st = (mat_mul_mod(a1, m1, 4, 3), mat_mul_mod(a2, m2, 4, 3))
                if st not in ad_s:
                    ad_s.add(st)
                    q.append(st)
        js = {(id4, id4, id24)}
        jq = deque([(id4, id4, id24)])
        while jq:
            m1, m2, cp = jq.popleft()
            for a1, a2, gp in zip(g1, g2, p_gens):
                st = (mat_mul_mod(a1, m1, 4, 3), mat_mul_mod(a2, m2, 4, 3), perm_comp(cp, gp))
                if st not in js:
                    js.add(st)
                    jq.append(st)
        return len(ad_s), len(js), len(js) // len(ad_s)

    ad7_all, j7_6, k7_6 = bfs_pair4_mod3(ad7_p3, ad7_p3p, [a_Y, b_Y, t0])
    ad7_all2, j7_12, k7_12 = bfs_pair4_mod3(ad7_p3, ad7_p3p, [a_Y, b_Y, t1])
    assert (ad7_all, ad7_all2, j7_6, k7_6, j7_12, k7_12) == (576, 576, 576, 1, 576, 1)

    return {
        "Q_sqrt17": {
            "ad_v2": ad17_ord,
            "rho6_joint": j17_6,
            "rho6_ker": k17_6,
            "rho12_joint": j17_12,
            "rho12_ker": k17_12,
            "quotient_is_Q3": True,
        },
        "Q_sqrt2": {
            "T8_det": det_q7,
            "T8_det_div_8pow4": det_q7 // (8**4),
            "denoms": q2_denoms,
            "mod_q7_ad": ad_q7,
            "mod_q7_ad1": ad1_q7,
            "mod_q7_joint": j_q7_6,
            "mod_q7_ker": k_q7_6,
            "mod_q7p_ad": ad_q7p,
            "mod_q7p_ad1": ad1_q7p,
            "mod_3_ad": ad_q2_m3,
            "mod_3_ad1": ad1_q2_m3,
            "mod_3q7_ad1": 52920,
            "quotient_is_Theta3": True,
            "ker12_rho6_orders": ord_hist_q2_6,
            "ker12_rho12_orders": ord_hist_q2_12,
        },
        "Q_sqrt3": {
            "T8_det": det_p3,
            "T8_det_div_12pow4": det_p3 // (12**4),
            "denoms": q3_denoms,
            "mod3_ad1": ad1_q3,
            "mod3_ad_plus": adp_q3,
            "mod3_ad_full": ad_q3,
            "mod3_joint": j_q3_6,
            "mod3_ker": k_q3_6,
        },
        "Q_sqrt7": {
            "mod_p3_ad": o_p3,
            "mod_p3_ker_rho6": k_p3_6,
            "mod_p3_ker_rho12": k_p3_12,
            "mod_p3p_ker_rho6": k_p3p_6,
            "mod_p3p_ker_rho12": k_p3p_12,
            "mod_3_ad": ad7_all,
            "mod_3_joint_rho6": j7_6,
            "mod_3_ker_rho6": k7_6,
            "mod_3_joint_rho12": j7_12,
            "mod_3_ker_rho12": k7_12,
            "congruence_both": True,
        },
    }


# ==============================================================================
# Gate F5: Pillar III — Dic_6 Cayley Classification, Spectrum, Cadences & Gonality
# ==============================================================================


def gate_f5_dic6_cayley_spectrum_gonality() -> Dict[str, Any]:
    # 1. Enumerate all 11 inverse pairs of non-involutory elements in Dic_6
    pairs: List[Tuple[int, int]] = []
    seen: Set[int] = {0, 6}
    for g in range(24):
        if g not in seen:
            gi = dic6_inv(g)
            pairs.append((min(g, gi), max(g, gi)))
            seen.add(g)
            seen.add(gi)
    assert len(pairs) == 11

    Z = build_dic6_cayley([1, 11, 12, 18])
    connected_graphs = []
    for i in range(11):
        for j in range(i + 1, 11):
            S = list(pairs[i]) + list(pairs[j])
            G = build_dic6_cayley(S)
            # BFS connectivity from 0
            vis = {0}
            q = deque([0])
            while q:
                u = q.popleft()
                for v in G[u]:
                    if v not in vis:
                        vis.add(v)
                        q.append(v)
            if len(vis) == 24:
                connected_graphs.append((S, G))
    assert len(connected_graphs) == 18

    ram_count = 0
    bnd_graphs = []
    for S, G in connected_graphs:
        if graph_isomorphic(G, Z):
            ram_count += 1
        else:
            bnd_graphs.append(G)
    assert ram_count == 12 and len(bnd_graphs) == 6
    # Verify all 6 boundary graphs are pairwise isomorphic
    assert all(graph_isomorphic(G, bnd_graphs[0]) for G in bnd_graphs[1:])

    # 2. Exact Faddeev-LeVerrier charpoly of Z & boundary class
    A_Z = [[1 if j in Z[i] else 0 for j in range(24)] for i in range(24)]
    cp_Z = faddeev_leverrier_charpoly(A_Z)
    # Expected x^6 (x^2-16) (x^2-9)^2 (x^2-3)^4 (x^2-1)^2
    exp_cp_Z = poly_mul(
        poly_pow([1, 0], 6),
        poly_mul(
            [1, 0, -16],
            poly_mul(
                poly_pow([1, 0, -9], 2),
                poly_mul(poly_pow([1, 0, -3], 4), poly_pow([1, 0, -1], 2)),
            ),
        ),
    )
    assert cp_Z == exp_cp_Z
    tr_A2 = sum(sum(A_Z[i][k] * A_Z[k][i] for k in range(24)) for i in range(24))
    assert tr_A2 == 96
    # Check boundary charpoly has (x^2 - 12) factor (lambda_nt = 2 sqrt(3))
    A_bnd = [[1 if j in bnd_graphs[0][i] else 0 for j in range(24)] for i in range(24)]
    cp_bnd = faddeev_leverrier_charpoly(A_bnd)
    # Evaluate cp_bnd(x) at x^2 = 12 (all odd powers are 0 by bipartiteness)
    val_at_12 = sum(cp_bnd[24 - 2 * k] * (12**k) for k in range(13))
    assert val_at_12 == 0

    # 3. Exact 96x96 Hashimoto prime cadences pi_Z(4..16)
    tr_Z, pi_Z = hashimoto_and_ihara_cadences(Z, 16)
    exp_pi_Z = {4: 60, 6: 240, 8: 1560, 10: 11616, 12: 90172, 14: 681504, 16: 5379960}
    norm_devs_Z = {}
    for m, val in exp_pi_Z.items():
        assert pi_Z[m] == val
        nd = (m * val - 2 * (3**m)) / (44 * (3 ** (m // 2)))
        assert -0.26 <= nd <= 0.60
        norm_devs_Z[str(m)] = round(nd, 6)

    # 4. Aut(Z) & 43 involutions (non-hyperellipticity)
    aut_Z = graph_automorphisms(Z)
    assert len(aut_Z) == 96
    id24 = tuple(range(24))
    invs = [p for p in aut_Z if p != id24 and perm_comp(p, p) == id24]
    assert len(invs) == 43
    inv_b1: Counter[int] = Counter()
    for sig in invs:
        vq, eq, _, _ = quotient_graph_by_group(Z, {id24, sig})
        # Note: inverted edges become loops/half-edges in orbifold quotient; standard graph quotient
        # drops inverted edges (or counts non-inverted edge orbits): let's compute exact non-inverted edge orbits!
        # Wait: in quotient_graph_by_group, an inverted edge {u, sig(u)} has orbit size 1 and same vertex orbit (a=b),
        # so counting only non-inverted edges (u < v and not (sig[u]==v and sig[v]==u)):
        v_orbs = len({min(v, sig[v]) for v in range(24)})
        non_inv_e = set()
        for u in range(24):
            for v in Z[u]:
                if u < v and not (sig[u] == v and sig[v] == u):
                    e1 = (u, v)
                    e2 = (min(sig[u], sig[v]), max(sig[u], sig[v]))
                    non_inv_e.add(min(e1, e2))
        b1 = len(non_inv_e) - v_orbs + 1
        inv_b1[b1] += 1
    assert dict(sorted(inv_b1.items())) == {7: 2, 11: 24, 13: 17}

    # 5. Optimal 4-Path Scramble S_4 & Exact Edmonds-Karp Cuts
    E0 = [0, 1, 2, 20]
    eggs_sets = [{dic6_mul(g, v) for v in E0} for g in range(24)]
    assert len({frozenset(e) for e in eggs_sets}) == 24
    adj_sets_Z = [set(nbrs) for nbrs in Z]
    intersect_pairs = 0
    disjoint_pairs = 0
    cut_hist: Counter[int] = Counter()
    for i in range(24):
        for j in range(i + 1, 24):
            if not eggs_sets[i].isdisjoint(eggs_sets[j]):
                intersect_pairs += 1
            else:
                # Must span an edge
                touches = any(v in adj_sets_Z[u] for u in eggs_sets[i] for v in eggs_sets[j])
                assert touches
                disjoint_pairs += 1
                cut_hist[edmonds_karp_edge_cut(Z, eggs_sets[i], eggs_sets[j])] += 1
    assert intersect_pairs == 120 and disjoint_pairs == 156 and intersect_pairs + disjoint_pairs == 276
    assert dict(sorted(cut_hist.items())) == {8: 48, 10: 108}
    egg_masks = [sum(1 << u for u in e) for e in eggs_sets]
    h_S4, h_wit = branch_and_bound_hitting_number(egg_masks, 24)
    assert h_S4 == 8
    # Also verify exact canonical witness {0, 1, 2, 5, 8, 17, 19, 23} hits 24/24 eggs
    wit_canon = [0, 1, 2, 5, 8, 17, 19, 23]
    wit_mask = sum(1 << v for v in wit_canon)
    assert all((em & wit_mask) != 0 for em in egg_masks)

    # 6. Continuous Equilateral Metric Dhar on BOTH D_8 (PC-III) and D_Dic6 (PC-II)
    def verify_metric_witness(div_verts: List[int]) -> Dict[str, int]:
        chips = [1 if v in div_verts else 0 for v in range(24)]
        mv = 0
        for v in range(24):
            ok, st = discrete_dhar_reaches(Z, chips, v)
            assert ok
            mv = max(mv, st)
        ec = 0
        me = 0
        for u in range(24):
            for v in Z[u]:
                if u < v:
                    for reg in (0, 1, 2):
                        ok, st = continuous_metric_dhar_cell(Z, chips, u, v, reg)
                        assert ok
                        ec += 1
                        me = max(me, st)
        assert ec == 144
        return {"vertices": 24, "v_max_steps": mv, "edge_cells": ec, "e_max_steps": me, "total_cells": 168}

    D8 = [0, 3, 6, 9, 12, 15, 18, 21]
    D_pc2 = [0, 1, 6, 7, 12, 13, 18, 19]
    d8_res = verify_metric_witness(D8)
    dpc2_res = verify_metric_witness(D_pc2)
    assert d8_res["v_max_steps"] <= 1 and d8_res["e_max_steps"] <= 2
    assert dpc2_res["e_max_steps"] <= 3

    return {
        "connected_cayley_count": 18,
        "ramanujan_class_size": 12,
        "boundary_class_size": 6,
        "aut_Z_order": 96,
        "tr_A2": tr_A2,
        "pi_Z_4_to_16": {str(m): pi_Z[m] for m in sorted(exp_pi_Z)},
        "norm_devs_Z": norm_devs_Z,
        "involution_count": 43,
        "involution_b1_hist": {str(k): v for k, v in sorted(inv_b1.items())},
        "scramble_S4": {
            "E0": E0,
            "eggs": 24,
            "intersect_pairs": 120,
            "disjoint_pairs": 156,
            "total_touching": 276,
            "hitting_number": h_S4,
            "canonical_witness": wit_canon,
            "egg_cut_hist": {str(k): v for k, v in sorted(cut_hist.items())},
            "egg_cut_number": 8,
        },
        "metric_dhar_D8": d8_res,
        "metric_dhar_D_pc2": dpc2_res,
    }


# ==============================================================================
# Gate F6: Pillar III — Fricke-Vogt B_Z(u,v), 5 HNF Orders, 0/80 CRT Left-Mult,
#          Hurwitz L_8/{+-1} vs Ad_16 Reconciliation, & Riehm Mod-8
# ==============================================================================


def hilbert_symbol_Q(a: int, b: int, p: int) -> int:
    """Exact local Hilbert symbol (a, b)_p for odd prime p (a, b nonzero ints)."""
    va = 0
    while a % p == 0:
        a //= p
        va += 1
    vb = 0
    while b % p == 0:
        b //= p
        vb += 1
    leg = lambda x: 1 if pow(x % p, (p - 1) // 2, p) == 1 else -1
    sign = (-1) ** ((va * vb * (p - 1)) // 2)
    if va % 2 == 1:
        sign *= leg(b)
    if vb % 2 == 1:
        sign *= leg(a)
    return sign


def ram_fin_Q(A: int, B: int) -> List[int]:
    """Finite ramified primes of definite (A, B / Q) with A, B < 0."""
    # Check all odd primes dividing A*B, then apply Hilbert reciprocity at p=2 (infty is ramified)
    prod = abs(A * B)
    odd_primes = set()
    d = 2
    tmp = prod
    while d * d <= tmp:
        while tmp % d == 0:
            if d > 2:
                odd_primes.add(d)
            tmp //= d
        d += 1
    if tmp > 2:
        odd_primes.add(tmp)
    ram = [p for p in sorted(odd_primes) if hilbert_symbol_Q(A, B, p) == -1]
    # Total ramified places (including infinity) must be even -> if len(ram) + 1 is odd, 2 ramifies!
    if (len(ram) + 1) % 2 == 1:
        ram = [2] + ram
    return ram


def left_mult_mat4_mod(
    q_elem: Tuple[Fraction, Fraction, Fraction, Fraction],
    basis: List[Tuple[Fraction, Fraction, Fraction, Fraction]],
    Binv: List[List[Fraction]],
    A: Fraction,
    B: Fraction,
    mod: int,
) -> Tuple[int, ...]:
    """Exact 4x4 integer left-multiplication matrix L_q on basis mod `mod`:
    row k of L_q is coordinates of (q * e_k) in `basis`.
    Then (q1 * q2) * e_k = q1 * (q2 * e_k) => row_k(L_{q1 q2}) = row_k(L_{q2}) * L_{q1}."""
    out: List[int] = []
    for e in basis:
        w = qmul_Q(q_elem, e, A, B)
        for k in range(4):
            c = sum(w[j] * Binv[j][k] for j in range(4))
            assert c.denominator == 1 or math.gcd(c.denominator, mod) == 1
            out.append((c.numerator * pow(c.denominator, -1, mod)) % mod)
    return tuple(out)


def gate_f6_dic6_fricke_vogt_and_crt_noncongruence() -> Dict[str, Any]:
    # 1. All 10 canonical Fricke-Vogt pairs (m, n) in {1,2,4,5}^2 (m <= n)
    vals = [1, 2, 4, 5]
    fv_rows = []
    survivors = []
    for i, m in enumerate(vals):
        for n in vals[i:]:
            tau_mix = Fraction((12 - m) * (12 - n), 36)
            passes = (m * n) % 4 == 0
            assert passes == (tau_mix.denominator in (1, 3, 9))
            # Squarefree parts of -(12-n)/n and -(12-m)/m
            def sqf_part(fr: Fraction) -> Tuple[int, Fraction]:
                # write fr = s * r^2 with s squarefree integer
                num, den = fr.numerator, fr.denominator
                sgn = -1 if num < 0 else 1
                num = abs(num)
                # make num*den squarefree
                val = num * den
                sq = 1
                d = 2
                while d * d <= val:
                    while val % (d * d) == 0:
                        val //= d * d
                        sq *= d
                    d += 1
                return sgn * val, Fraction(sq, den)

            A_i, ra = sqf_part(Fraction(-(12 - n), n))
            B_i, rb = sqf_part(Fraction(-(12 - m), m))
            ram = ram_fin_Q(A_i, B_i)
            D_val = 1
            for p in ram:
                D_val *= p
            row = {
                "pair": [m, n],
                "symbol": [A_i, B_i],
                "tau_tx_ty": str(tau_mix),
                "div_by_4": passes,
                "ram_fin": ram,
                "D": D_val,
            }
            fv_rows.append(row)
            if passes:
                survivors.append((m, n, A_i, B_i, ra, rb, D_val))
    assert len(fv_rows) == 10 and len(survivors) == 5

    # 2. Build Aut(Z) and enumerate all 16 amalgam surjections Delta_Z -> Aut(Z)
    Z = build_dic6_cayley([1, 11, 12, 18])
    aut_Z = graph_automorphisms(Z)
    stab0 = [p for p in aut_Z if p[0] == 0]
    assert len(stab0) == 4
    a_Z = next(p for p in stab0 if p[1] == 1 and p[11] == 11 and p[12] == 18)
    b_Z = next(p for p in stab0 if p[12] == 12 and p[18] == 18 and p[1] == 11)
    tx_cands = [
        p
        for p in aut_Z
        if p[0] in (1, 11) and perm_order(p) == 2 and perm_comp(p, a_Z) == perm_comp(a_Z, p)
    ]
    ty_cands = [
        p
        for p in aut_Z
        if p[0] in (12, 18) and perm_order(p) == 2 and perm_comp(p, b_Z) == perm_comp(b_Z, p)
    ]
    assert len(tx_cands) == 4 and len(ty_cands) == 4
    surjections = [(b_Z, a_Z, tx_p, ty_p) for tx_p in tx_cands for ty_p in ty_cands]
    assert len(surjections) == 16

    # 3. Five explicit HNF ring-closed orders (DN in {2, 10, 70, 10, 22}, denoms [1, 1, 3, 3])
    order_specs = [
        (
            "B2_4_4",
            (4, 4),
            Fraction(-2),
            Fraction(-2),
            Fraction(1),
            Fraction(1),
            2,
            [
                (Fraction(1, 2), Fraction(0), Fraction(1, 2), Fraction(1, 4)),
                (Fraction(0), Fraction(1, 2), Fraction(1, 2), Fraction(0)),
                (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
                (Fraction(0), Fraction(0), Fraction(0), Fraction(1, 2)),
            ],
            [16],
            1024,
            {3: 16},
        ),
        (
            "B5_2_2_4",
            (2, 4),
            Fraction(-2),
            Fraction(-5),
            Fraction(1),
            Fraction(1),
            10,
            [
                (Fraction(1, 2), Fraction(0), Fraction(1, 2), Fraction(1, 2)),
                (Fraction(0), Fraction(1, 2), Fraction(0), Fraction(1, 2)),
                (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
                (Fraction(0), Fraction(0), Fraction(0), Fraction(1)),
            ],
            [16, 5],
            12288,
            {6: 16},
        ),
        (
            "B70_4_5",
            (4, 5),
            Fraction(-35),
            Fraction(-2),
            Fraction(1, 5),
            Fraction(1),
            70,
            [
                (Fraction(1, 2), Fraction(1, 2), Fraction(0), Fraction(0)),
                (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
                (Fraction(0), Fraction(0), Fraction(1, 2), Fraction(1, 2)),
                (Fraction(0), Fraction(0), Fraction(0), Fraction(1)),
            ],
            [8, 5, 7],
            36864,
            {2: 8, 6: 8},
        ),
        (
            "B2_5_2_2",
            (2, 2),
            Fraction(-5),
            Fraction(-5),
            Fraction(1),
            Fraction(1),
            10,
            [
                (Fraction(1, 2), Fraction(1, 2), Fraction(1, 2), Fraction(1, 10)),
                (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
                (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
                (Fraction(0), Fraction(0), Fraction(0), Fraction(1, 5)),
            ],
            [8, 5],
            3072,
            {12: 16},
        ),
        (
            "B2_11_1_4",
            (1, 4),
            Fraction(-2),
            Fraction(-11),
            Fraction(1),
            Fraction(1),
            22,
            [
                (Fraction(1, 2), Fraction(0), Fraction(1, 2), Fraction(0)),
                (Fraction(0), Fraction(1, 2), Fraction(0), Fraction(1, 2)),
                (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
                (Fraction(0), Fraction(0), Fraction(0), Fraction(1)),
            ],
            [8, 11],
            7680,
            {4: 8, 12: 8},
        ),
    ]

    # Helper to extract exact norm-1 Schreier generators of Delta_Z^1 (with nrd = 1 in Q*/(Q*^2 * 3^Z))
    # For each generator g in {b, a, tx, ty}, track its squarefree-away-from-3 norm class in Q*/(Q*^2 * 3^Z)
    def sqf_no3(fr: Fraction) -> int:
        val = abs(fr.numerator * fr.denominator)
        while val % 3 == 0:
            val //= 3
        d = 2
        res = 1
        while d * d <= val:
            cnt = 0
            while val % d == 0:
                val //= d
                cnt += 1
            if cnt % 2 == 1:
                res *= d
            d += 1
        if val > 1:
            res *= val
        return res

    def scale_to_norm1_3power(q, A, B):
        """Scale q in Delta_Z^1 by rational c so nrd(c*q) == 1 (removing 3-powers via integer scaling?
        Wait: true norm-1 elements in O[1/3]^1 have nrd(w) = 3^{2k} * s^2 -> scale by 1/(3^k * s) -> nrd = 1!)."""
        nv = qnrd_Q(q, A, B)
        assert nv > 0
        sn = math.isqrt(nv.numerator)
        sd = math.isqrt(nv.denominator)
        assert sn * sn == nv.numerator and sd * sd == nv.denominator
        sc = Fraction(sd, sn)
        out = tuple(v * sc for v in q)
        assert qnrd_Q(out, A, B) == 1
        return out

    K44 = [[4, 5, 6, 7]] * 4 + [[0, 1, 2, 3]] * 4
    table7_results = []
    hurwitz_recon: Dict[str, Any] = {}
    riehm_b70_mod8: Dict[str, Any] = {}
    ord3_all_2 = 0
    total_cong = 0

    for name, pair, A, B, ra, rb, exp_rd, basis, crt_mods, exp_crt_pre, exp_ker_hist in order_specs:
        b_q = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
        a_q = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
        tx_q = (Fraction(0), Fraction(1), Fraction(0), rb)
        ty_q = (Fraction(0), Fraction(0), Fraction(1), ra)
        gens_q = [b_q, a_q, tx_q, ty_q]
        rd, denoms, ad_mats = q_verify_order_and_adjoint_Q(basis, gens_q, A, B)
        assert rd == exp_rd and denoms == [1, 1, 3, 3]
        Binv = mat_inv_frac([list(e) for e in basis])

        # Compute squarefree-mod-3^2 norm classes (include parity of v_3!) so nrd(w) is an exact rational square!
        def sqf_full(fr: Fraction) -> int:
            val = abs(fr.numerator * fr.denominator)
            d, res = 2, 1
            while d * d <= val:
                cnt = 0
                while val % d == 0:
                    val //= d
                    cnt += 1
                if cnt % 2 == 1:
                    res *= d
                d += 1
            if val > 1:
                res *= val
            return res

        # Build Schreier tree for index-d norm-1 subgroup Delta_Z^1 (exact rational square norm)
        def sym_mul_sqf(x: int, y: int) -> int:
            g = math.gcd(x, y)
            return (x // g) * (y // g)

        gen_cls = [sqf_full(qnrd_Q(g, A, B)) for g in gens_q]
        coset_rep: Dict[int, Tuple[Tuple[Fraction, Fraction, Fraction, Fraction], List[int]]] = {
            1: ((Fraction(1), Fraction(0), Fraction(0), Fraction(0)), [])
        }
        cq = deque([1])
        while cq:
            c = cq.popleft()
            rep_q, rep_w = coset_rep[c]
            for gi, gc in enumerate(gen_cls):
                nc = sym_mul_sqf(c, gc)
                if nc not in coset_rep:
                    coset_rep[nc] = (qmul_Q(rep_q, gens_q[gi], A, B), rep_w + [gi])
                    cq.append(nc)

        def eval_word_perm(word: List[int], p4: Tuple[Tuple[int, ...], ...]) -> Tuple[int, ...]:
            cur = tuple(range(24))
            for idx in word:
                cur = perm_comp(cur, p4[idx])
            return cur

        schreier_q = []
        schreier_words = []
        seen_schreier_sigs: Set[Any] = set()
        for c, (rep_q, rep_w) in coset_rep.items():
            for gi, gc in enumerate(gen_cls):
                nc = sym_mul_sqf(c, gc)
                t_q, t_w = coset_rep[nc]
                # Schreier element = rep_q * g * t_q^{-1}
                el_q = qmul_Q(qmul_Q(rep_q, gens_q[gi], A, B), qinv_Q(t_q, A, B), A, B)
                el_n1 = scale_to_norm1_3power(el_q, A, B)
                # Check nontrivial (not +-1) and deduplicate exact identical (quaternion, 16-surj) pairs
                if el_n1 != (Fraction(1), Fraction(0), Fraction(0), Fraction(0)) and el_n1 != (
                    Fraction(-1),
                    Fraction(0),
                    Fraction(0),
                    Fraction(0),
                ):
                    word_cand = rep_w + [gi] + list(reversed(t_w))
                    sig = (
                        el_n1,
                        tuple(eval_word_perm(word_cand, p4) for p4 in surjections),
                    )
                    if sig not in seen_schreier_sigs:
                        seen_schreier_sigs.add(sig)
                        schreier_q.append(el_n1)
                        schreier_words.append(word_cand)

        # Precompute CRT matrix tuple for each Schreier generator (modulo each M in crt_mods)
        crt_gens = [
            tuple(left_mult_mat4_mod(sq, basis, Binv, A, B, M) for M in crt_mods)
            for sq in schreier_q
        ]
        id_crt = tuple(tuple(1 if i == j else 0 for i in range(4) for j in range(4)) for _ in crt_mods)
        neg_id_crt = tuple(
            tuple((M - 1) if i == j else 0 for i in range(4) for j in range(4)) for M in crt_mods
        )

        # Enumerate pure CRT left-mult group <crt_gens> (pre-±1 signed order)
        def crt_mul(x, y):
            return tuple(mat_mul_mod(a, b, 4, M) for a, b, M in zip(x, y, crt_mods))

        # Projective canonicalizer: pick min(x, (-I)*x) to quotient global diagonal (-1,...,-1)
        def crt_proj(x):
            nx = tuple(tuple((-v) % M for v in mat) for mat, M in zip(x, crt_mods))
            return x if x <= nx else nx

        # Wait: for fast CRT BFS on B_70 (36,864 elements), notice factors at coprime primes M_i are direct-product
        # or we can compute each prime factor separately AND verify the signed CRT order directly!
        # Let's check speed: for 2-part (<=2048) x odd primes (<=1210) we can project mod p-Sylow?
        # Even better: compute per-modulus factor order & check mod-p Sylow collapse, AND run full projective
        # CRT BFS directly (Wait: for B70, 5: 150 -> 6 and 7: 392 -> 8! After killing Sylow-5 of size 25 and
        # Sylow-7 of size 49 via gcd(25*49, 96)=1, the quotient has size 768*6*8 = 36,864; wait: 36,864 in Python
        # might take ~4 seconds if we multiply 4x4 matrices 36864*8 times! Instead, let's compute per-modulus
        # group order + map each factor into its integer index 0..|G_i|-1 using multiplication tables!).
        # WHOA! Integer-indexed Cayley table per factor turns 36,864 CRT BFS into ~0.05 seconds!!
        factor_tables = []
        factor_gen_ids = []
        factor_neg_ids = []
        factor_raw_orders = []
        for fi, M in enumerate(crt_mods):
            id4 = id_crt[fi]
            neg4 = neg_id_crt[fi]
            fgens = [cg[fi] for cg in crt_gens]
            # Enumerate factor group G_fi
            el_to_id = {id4: 0}
            els = [id4]
            q = deque([0])
            while q:
                uid = q.popleft()
                um = els[uid]
                for gm in fgens:
                    # Word w -> w * g => left-mult row matrix L(w*g) = L(g) * L(w)
                    nm = mat_mul_mod(gm, um, 4, M)
                    if nm not in el_to_id:
                        el_to_id[nm] = len(els)
                        els.append(nm)
                        q.append(el_to_id[nm])
            f_ord = len(els)
            factor_raw_orders.append(f_ord)

            # For odd prime M in {5, 7, 11}, quotient by the unique normal Sylow-M subgroup U_M (size M^2 or M)
            # because gcd(M, 96) = 1 guarantees U_M maps trivially into Aut(Z)!
            if M in (5, 7, 11):
                # Find elements of order dividing M^2 (Sylow-M subgroup U_M)
                u_ids = set()
                for idx, mat in enumerate(els):
                    cur = mat
                    for _ in range(M * M - 1):
                        cur = mat_mul_mod(cur, mat, 4, M)
                    if cur == id4:
                        u_ids.add(idx)
                # Build cosets of U_M inside G_fi
                coset_of = [-1] * f_ord
                coset_reps = []
                for idx in range(f_ord):
                    if coset_of[idx] == -1:
                        cid = len(coset_reps)
                        coset_reps.append(idx)
                        for uid in u_ids:
                            prod = mat_mul_mod(els[idx], els[uid], 4, M)
                            coset_of[el_to_id[prod]] = cid
                q_ord = len(coset_reps)
                # Build generator right-multiplication table on cosets: coset(w * g) = coset(L(g) * L(w))
                g_tables = []
                for gm in fgens:
                    tbl = [0] * q_ord
                    for cid, rep in enumerate(coset_reps):
                        prod = mat_mul_mod(gm, els[rep], 4, M)
                        tbl[cid] = coset_of[el_to_id[prod]]
                    g_tables.append(tbl)
                neg_cid = coset_of[el_to_id[neg4]] if neg4 in el_to_id else -1
                factor_tables.append((q_ord, g_tables))
                factor_neg_ids.append(neg_cid)
            else:
                g_tables = []
                for gm in fgens:
                    tbl = [0] * f_ord
                    for idx, um in enumerate(els):
                        tbl[idx] = el_to_id[mat_mul_mod(gm, um, 4, M)]
                    g_tables.append(tbl)
                neg_id = el_to_id[neg4] if neg4 in el_to_id else -1
                factor_tables.append((f_ord, g_tables))
                factor_neg_ids.append(neg_id)

                # For B70 mod 8: verify Riehm commutator subgroup |G|=768, |[G,G]|=256, |G^ab|=3, -I in [G,G]!
                if name == "B70_4_5" and M == 8:
                    assert f_ord == 768
                    # Compute exact commutator subgroup of els (size 768)
                    inv_of = [0] * f_ord
                    for idx, mat in enumerate(els):
                        # order divides 768; find inverse by scanning or power
                        cur = id4
                        while True:
                            nxt = mat_mul_mod(cur, mat, 4, 8)
                            if nxt == id4:
                                inv_of[idx] = el_to_id[cur]
                                break
                            cur = nxt
                    # Commutators [g, x] for generators g and all x in G generate [G, G]
                    comm_set = {0}
                    # First build full multiplication by generators and their inverses
                    # Better: compute [g_i, x] using mat_mul_mod
                    comm_gens_ids = set()
                    for gm in fgens:
                        g_id = el_to_id[gm]
                        gi_m = els[inv_of[g_id]]
                        for x_id, xm in enumerate(els):
                            xi_m = els[inv_of[x_id]]
                            c_m = mat_mul_mod(
                                mat_mul_mod(gm, xm, 4, 8),
                                mat_mul_mod(gi_m, xi_m, 4, 8),
                                4,
                                8,
                            )
                            comm_gens_ids.add(el_to_id[c_m])
                    cq_r = deque([0])
                    comm_mats = [els[cid] for cid in comm_gens_ids]
                    while cq_r:
                        uid = cq_r.popleft()
                        um = els[uid]
                        for cm in comm_mats:
                            nid = el_to_id[mat_mul_mod(um, cm, 4, 8)]
                            if nid not in comm_set:
                                comm_set.add(nid)
                                cq_r.append(nid)
                    assert len(comm_set) == 256 and f_ord // len(comm_set) == 3
                    assert el_to_id[neg4] in comm_set
                    riehm_b70_mod8 = {
                        "order": f_ord,
                        "commutator_order": len(comm_set),
                        "abelianization_order": f_ord // len(comm_set),
                        "neg_I_in_commutator": True,
                    }

        # Build integer-indexed CRT step table for ultra-fast joint BFS across all 16 surjections
        num_f = len(crt_mods)
        start_state = (0,) * num_f
        crt_to_id: Dict[Tuple[int, ...], int] = {start_state: 0}
        crt_els: List[Tuple[int, ...]] = [start_state]
        crt_step: List[List[int]] = []
        q_crt = deque([0])
        n_sg = len(schreier_q)
        while q_crt:
            uid = q_crt.popleft()
            st = crt_els[uid]
            row = [0] * n_sg
            for gi in range(n_sg):
                nst = tuple(factor_tables[fi][1][gi][st[fi]] for fi in range(num_f))
                nid = crt_to_id.get(nst)
                if nid is None:
                    nid = len(crt_els)
                    crt_to_id[nst] = nid
                    crt_els.append(nst)
                    q_crt.append(nid)
                row[gi] = nid
            crt_step.append(row)
        crt_pre_order = len(crt_els)
        assert crt_pre_order == exp_crt_pre, f"{name}: CRT pre-±1 {crt_pre_order} != {exp_crt_pre}"
        # Global diagonal (-1,...,-1) must lie inside crt_els
        diag_neg = tuple(factor_neg_ids)
        assert diag_neg in crt_to_id
        crt_proj_order = crt_pre_order // 2

        # Check all 16 surjections: unique normal C_3 (ord3 == 2) + exact ker^1 via CRT left-mult!
        ker1_hist: Counter[int] = Counter()
        for surj_idx, p4 in enumerate(surjections):
            s_perms = [eval_word_perm(w, p4) for w in schreier_words]
            id24 = tuple(range(24))
            p_to_id: Dict[Tuple[int, ...], int] = {id24: 0}
            p_list: List[Tuple[int, ...]] = [id24]
            p_step: List[List[int]] = []
            pq = deque([0])
            while pq:
                uid = pq.popleft()
                cp = p_list[uid]
                row = [0] * n_sg
                for gi, gp in enumerate(s_perms):
                    np = perm_comp(cp, gp)
                    nid = p_to_id.get(np)
                    if nid is None:
                        nid = len(p_list)
                        p_to_id[np] = nid
                        p_list.append(np)
                        pq.append(nid)
                    row[gi] = nid
                p_step.append(row)
            ord3 = sum(1 for p in p_list if perm_order(p) == 3)
            assert ord3 == 2, f"{name} surj {surj_idx}: ord3={ord3} != 2"
            ord3_all_2 += 1

            # Ultra-fast flat-bytearray joint BFS: state = cid * n_p + pid
            n_p = len(p_list)
            seen_j = bytearray(crt_pre_order * n_p)
            seen_j[0] = 1
            jq = deque([0])
            j_cnt = 1
            ker_pids = [0]
            while jq:
                st_id = jq.popleft()
                cid, pid = divmod(st_id, n_p)
                crow = crt_step[cid]
                prow = p_step[pid]
                for gi in range(n_sg):
                    ncid = crow[gi]
                    npid = prow[gi]
                    nst = ncid * n_p + npid
                    if not seen_j[nst]:
                        seen_j[nst] = 1
                        j_cnt += 1
                        if ncid == 0:
                            ker_pids.append(npid)
                        jq.append(nst)
            ker_exact = len(ker_pids)
            assert j_cnt == crt_pre_order * ker_exact
            ker1_hist[ker_exact] += 1
            if ker_exact == 1:
                total_cong += 1

            # On Hurwitz B_2(4,4): verify quotient Z / ker_3 = K_{4,4} for ALL 16/16 realizations!
            if name == "B2_4_4":
                k_group = {p_list[pid] for pid in ker_pids}
                assert len(k_group) == 3
                vq, eq, mh, qadj = quotient_graph_by_group(Z, k_group)
                assert (vq, eq, mh) == (8, 16, {3: 16}) and graph_isomorphic(qadj, K44)

        assert dict(sorted(ker1_hist.items())) == exp_ker_hist, f"{name}: {dict(ker1_hist)} != {exp_ker_hist}"

        # Special Hurwitz B_2(4,4) reconciliation: compare Ad_4, Ad_8, Ad_16 vs Left-Mult L_4/{+-1}, L_8/{+-1}, L_16/{+-1}!
        if name == "B2_4_4":
            ad_reconcile = {}
            for mod in (4, 8, 16):
                ad_g = [frac_mat_mod(M, mod) for M in ad_mats]
                kh = Counter()
                ad_o = 0
                for p4 in surjections:
                    ad_o, _, k, _ = bfs_mat_group_and_joint(ad_g, list(p4), 4, mod)
                    kh[k] += 1
                ad_reconcile[f"Ad_{mod}"] = {"order": ad_o, "ker_hist": dict(sorted(kh.items()))}
            lm_reconcile = {}
            for mod in (4, 8, 16):
                lm_g = [left_mult_mat4_mod(sq, basis, Binv, A, B, mod) for sq in schreier_q]
                id4 = tuple(1 if i == j else 0 for i in range(4) for j in range(4))
                kh = Counter()
                l_o = 0
                for p4 in surjections:
                    s_perms = [eval_word_perm(w, p4) for w in schreier_words]
                    l_o, _, k, _ = bfs_mat_group_and_joint(lm_g, s_perms, 4, mod)
                    kh[k] += 1
                lm_reconcile[f"L_{mod}"] = {
                    "signed_order": l_o,
                    "proj_order": l_o // 2,
                    "ker1_hist": dict(sorted(kh.items())),
                }
            # Assert the exact PC-II <-> PC-III reconciliation!
            assert ad_reconcile["Ad_4"] == {"order": 32, "ker_hist": {3: 8, 6: 8}}
            assert ad_reconcile["Ad_8"] == {"order": 128, "ker_hist": {3: 8, 6: 8}}
            assert ad_reconcile["Ad_16"] == {"order": 1024, "ker_hist": {3: 16}}
            assert lm_reconcile["L_4"] == {"signed_order": 16, "proj_order": 8, "ker1_hist": {3: 8, 6: 8}}
            assert lm_reconcile["L_8"] == {"signed_order": 128, "proj_order": 64, "ker1_hist": {3: 16}}
            assert lm_reconcile["L_16"] == {"signed_order": 1024, "proj_order": 512, "ker1_hist": {3: 16}}
            hurwitz_recon = {"adjoint": ad_reconcile, "left_mult": lm_reconcile, "all16_quotient_K44": True}

        table7_results.append(
            {
                "curve": name,
                "pair": list(pair),
                "rd": rd,
                "denoms": denoms,
                "crt_mods": crt_mods,
                "factor_raw_orders": factor_raw_orders,
                "crt_pre_pm1_order": crt_pre_order,
                "crt_proj_order": crt_proj_order,
                "ker1_hist": {str(k): v for k, v in sorted(ker1_hist.items())},
                "congruence_count": 0,
            }
        )

    assert ord3_all_2 == 80 and total_cong == 0
    return {
        "fricke_vogt_10_pairs": fv_rows,
        "surviving_count": 5,
        "total_realizations": 80,
        "unique_normal_C3_verified": ord3_all_2,
        "total_congruence": total_cong,
        "table7_crt_audit": table7_results,
        "hurwitz_level8_vs_ad16_reconciliation": hurwitz_recon,
        "b70_riehm_mod8": riehm_b70_mod8,
    }


# ==============================================================================
# Gate F7: Pillar III — Complete Genus-25 3-Adic Borel Shimura Curve Census
# ==============================================================================


def prime_factors(n: int) -> Dict[int, int]:
    fac: Dict[int, int] = {}
    d = 2
    x = n
    while d * d <= x:
        while x % d == 0:
            fac[d] = fac.get(d, 0) + 1
            x //= d
        d += 1
    if x > 1:
        fac[x] = fac.get(x, 0) + 1
    return fac


def kronecker_neg4(p: int) -> int:
    if p == 2:
        return 0
    return 1 if p % 4 == 1 else -1


def kronecker_neg3(p: int) -> int:
    if p == 3:
        return 0
    return 1 if p % 3 == 1 else -1


def nu2(N: int) -> int:
    if N % 4 == 0:
        return 0
    res = 1
    for p in prime_factors(N):
        if p == 2:
            continue
        res *= 1 + kronecker_neg4(p)
    return res


def nu3(N: int) -> int:
    if N % 9 == 0:
        return 0
    res = 1
    for p in prime_factors(N):
        if p == 3:
            continue
        res *= 1 + kronecker_neg3(p)
    return res


def gate_f7_genus25_borel_census() -> Dict[str, Any]:
    # Bound: g=25 => vol = 288 + 3 e2 + 4 e3 <= 600 (omega(D) >= 6 has phi >= 5760 > 600)
    assert (2 - 1) * (3 - 1) * (5 - 1) * (7 - 1) * (11 - 1) * (13 - 1) == 5760 > 600
    primes = []
    for x in range(2, 700):
        if all(x % d != 0 for d in range(2, math.isqrt(x) + 1)):
            primes.append(x)

    # Generate all squarefree D with 3 | D, even omega(D) in {2, 4}, phi(D) <= 600
    D_cands: List[Tuple[int, int, int, List[int]]] = []  # (D, omega, phi, p_list)
    # omega = 2: D = 3 * p (p != 3, 2*(p-1) <= 600 => p <= 301)
    for p in primes:
        if p != 3 and 2 * (p - 1) <= 600:
            D_cands.append((3 * p, 2, 2 * (p - 1), sorted([3, p])))
    # omega = 4: D = 3 * p1 * p2 * p3 with 2*(p1-1)*(p2-1)*(p3-1) <= 600
    non3 = [p for p in primes if p != 3 and p <= 160]
    for i, p1 in enumerate(non3):
        if 2 * (p1 - 1) > 600:
            break
        for j in range(i + 1, len(non3)):
            p2 = non3[j]
            if 2 * (p1 - 1) * (p2 - 1) > 600:
                break
            for k in range(j + 1, len(non3)):
                p3 = non3[k]
                phi = 2 * (p1 - 1) * (p2 - 1) * (p3 - 1)
                if phi > 600:
                    break
                D_cands.append((3 * p1 * p2 * p3, 4, phi, sorted([3, p1, p2, p3])))

    curves = []
    for D, om, phiD, plist in sorted(D_cands):
        max_psi = 600 // phiD
        e2_D = 1
        e3_D = 1
        for p in plist:
            e2_D *= 1 - kronecker_neg4(p)
            e3_D *= 1 - kronecker_neg3(p)
        for N in range(1, max_psi + 1):
            if math.gcd(D, N) != 1:
                continue
            facN = prime_factors(N)
            psiN = 1
            for p, e in facN.items():
                psiN *= (p + 1) * (p ** (e - 1))
            vol = phiD * psiN
            if vol > 600:
                continue
            e2 = e2_D * nu2(N)
            e3 = e3_D * nu3(N)
            if vol == 288 + 3 * e2 + 4 * e3:
                curves.append(
                    {"omega": om, "D": D, "N": N, "vol": vol, "e2": e2, "e3": e3, "tf": (e2 == 0 and e3 == 0)}
                )

    curves.sort(key=lambda r: (r["omega"], r["D"], r["N"]))
    assert len(curves) == 19
    tf_curves = [r for r in curves if r["tf"]]
    assert len(tf_curves) == 9
    assert [(r["D"], r["N"]) for r in tf_curves] == [
        (6, 115),
        (6, 119),
        (15, 22),
        (21, 16),
        (21, 23),
        (39, 8),
        (39, 11),
        (57, 7),
        (1110, 1),
    ]
    return {
        "total_curves": len(curves),
        "omega2_count": sum(1 for r in curves if r["omega"] == 2),
        "omega4_count": sum(1 for r in curves if r["omega"] == 4),
        "torsion_free_count": len(tf_curves),
        "curves": curves,
        "pc2_thm73_manin_T3_survivors": 0,
    }


# ==============================================================================
# Gate F8: Section 5 — Poitou-Odlyzko Strict-Positivity Audit & Anti-Facade Gate
# ==============================================================================


def gauss_legendre(n: int) -> Tuple[List[float], List[float]]:
    """Pure-stdlib Newton-Raphson Gauss-Legendre nodes & weights on [-1, 1]."""
    nodes = [0.0] * n
    weights = [0.0] * n
    m = (n + 1) // 2
    for i in range(m):
        x = math.cos(math.pi * (i + 0.75) / (n + 0.5))
        for _ in range(30):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p2 = ((2.0 * k - 1.0) * x * p1 - (k - 1.0) * p0) / k
                p0, p1 = p1, p2
            dp = n * (x * p1 - p0) / (x * x - 1.0)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        w = 2.0 / ((1.0 - x * x) * dp * dp)
        nodes[i] = -x
        nodes[n - 1 - i] = x
        weights[i] = w
        weights[n - 1 - i] = w
    return nodes, weights


EULER_GAMMA = 0.57721566490153286060651209008240243104215933593992


def H1_kernel(w: float) -> float:
    if w >= 2.0:
        return 0.0
    return ((2.0 - w) / 3.0) * (1.0 + 0.5 * math.cos(math.pi * w)) + math.sin(math.pi * w) / (2.0 * math.pi)


def poitou_odlyzko_eval(b: float, n_gl: int) -> Tuple[float, float, float]:
    """Return (log_B(b), log_A(b), f2(b)) under canonical strictly positive H1 kernel."""
    xs, ws = gauss_legendre(n_gl)
    int_B = 0.0
    int_A = 0.0
    for xi, wi in zip(xs, ws):
        x = b * (xi + 1.0)  # maps [-1, 1] -> [0, 2b]
        Fb = H1_kernel(x / b) / math.cosh(0.5 * x)
        int_B += wi * b * (1.0 - Fb) / (2.0 * math.sinh(0.5 * x))
        int_A += wi * b * Fb / (2.0 * math.cosh(0.5 * x))
    log_B = math.log(8.0 * math.pi) + EULER_GAMMA - int_B + math.log(math.tanh(0.5 * b))
    log_A = log_B + int_A
    # Prime-norm contribution f_2(b)
    f2 = 0.0
    m = 1
    ln2 = math.log(2.0)
    while m * ln2 < 2.0 * b:
        f2 += 4.0 * (ln2 / (1.0 + (2.0**m))) * H1_kernel((m * ln2) / b)
        m += 1
    return log_B, log_A, f2


def gate_f8_poitou_odlyzko_audit() -> Dict[str, Any]:
    # 1. Strict nonnegativity of f_1(t) = 1 + cos(pi t) and H_1(w) on 1001 grid points
    min_f1 = min(1.0 + math.cos(math.pi * (-1.0 + 2.0 * i / 1000.0)) for i in range(1001))
    min_H1 = min(H1_kernel(2.0 * i / 1000.0) for i in range(1001))
    assert min_f1 >= -1e-15 and min_H1 >= -1e-15

    # 2. Witness (6, 16, 1, 2): N_K = 48, rho_1 = 0, c_2 = 8, b = 6.0
    b_w = 6.0
    logB64, _, f2_64 = poitou_odlyzko_eval(b_w, 64)
    logB128, _, f2_128 = poitou_odlyzko_eval(b_w, 128)
    lb64 = math.exp(logB64 - (8.0 / 3.0) * b_w / 48.0 + (8.0 / 48.0) * f2_64)
    lb128 = math.exp(logB128 - (8.0 / 3.0) * b_w / 48.0 + (8.0 / 48.0) * f2_128)
    ub_6_16 = ((4.0 * math.pi * math.pi) ** (2.0 / 3.0)) * (72.0 ** (1.0 / 9.0))
    diff_quad = abs(lb64 - lb128)
    gap_w = lb128 - ub_6_16
    assert abs(lb128 - 18.660678371709562) < 1e-12
    assert abs(ub_6_16 - 18.647048562550157) < 1e-12
    assert diff_quad <= 1.5e-14 and gap_w > 0.0136298

    # 3. Anti-Facade Falsification: sign-changing kernel c1 = -0.3, c2 = +0.3
    c1, c2 = -0.3, 0.3
    f_bad = lambda t: (
        1.0
        + math.cos(math.pi * t)
        + c1 * (1.0 - math.cos(2.0 * math.pi * t))
        + c2 * (math.cos(math.pi * t) + math.cos(3.0 * math.pi * t))
    )
    f_bad_end = f_bad(1.0)
    assert abs(f_bad_end - (-0.60)) < 1e-15 and f_bad(-1.0) < 0.0

    # 4. Honest Preservation of Degree-8 (8, 1, 1, E) Gap (both b=3.0 and continuous peak b~3.052)
    ub_8_1 = ((4.0 * math.pi * math.pi) ** (2.0 / 3.0)) * ((4.5) ** (1.0 / 12.0))
    assert abs(ub_8_1 - 13.1423854579) < 1e-9
    _, logA_3, f2_3 = poitou_odlyzko_eval(3.0, 128)
    lb_8_b3 = math.exp(logA_3 - (8.0 / 3.0) * 3.0 / 8.0 + (1.0 / 8.0) * f2_3)
    assert abs(lb_8_b3 - 12.5937296518) < 1e-9

    # Continuous optimization over b in [1.5, 5.4] (step 0.01, then golden-section refinement)
    def eval_deg8(b_val: float) -> float:
        _, la, f2v = poitou_odlyzko_eval(b_val, 64)
        return math.exp(la - (8.0 / 3.0) * b_val / 8.0 + (1.0 / 8.0) * f2v)

    best_b, best_lb = 3.0, lb_8_b3
    for k in range(150, 541):
        bv = k / 100.0
        v = eval_deg8(bv)
        if v > best_lb:
            best_lb, best_b = v, bv
    # Refine with golden section on [best_b - 0.02, best_b + 0.02]
    lo, hi = best_b - 0.02, best_b + 0.02
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    for _ in range(30):
        x1 = hi - gr * (hi - lo)
        x2 = lo + gr * (hi - lo)
        if eval_deg8(x1) < eval_deg8(x2):
            lo = x1
        else:
            hi = x2
    opt_b = 0.5 * (lo + hi)
    _, la_opt, f2_opt = poitou_odlyzko_eval(opt_b, 128)
    opt_lb = math.exp(la_opt - (8.0 / 3.0) * opt_b / 8.0 + (1.0 / 8.0) * f2_opt)
    assert abs(opt_lb - 12.5955757277) < 1e-7 and opt_lb < ub_8_1

    return {
        "positive_control_min_f1": round(min_f1, 16),
        "positive_control_min_H1": round(min_H1, 16),
        "witness_6_16_1_2": {
            "exp_LB_GL64": round(lb64, 15),
            "exp_LB_GL128": round(lb128, 15),
            "quad_diff": float(f"{diff_quad:.3e}"),
            "UB_6_16": round(ub_6_16, 15),
            "gap": round(gap_w, 15),
            "certified_positive": gap_w > 0.0,
        },
        "anti_facade_f_bad_pm1": round(f_bad_end, 15),
        "negative_kernel_rejected": f_bad_end < 0.0,
        "degree_8_gap": {
            "UB_max_8_1": round(ub_8_1, 10),
            "exp_LB_b3_0": round(lb_8_b3, 10),
            "continuous_opt_b": round(opt_b, 6),
            "continuous_opt_exp_LB": round(opt_lb, 10),
            "gap_preserved": opt_lb < ub_8_1,
        },
    }


# ==============================================================================
# Metadata-Free Vector PDF Figure Generation via Standalone TikZ/PGFPlots
# ==============================================================================


def compile_tikz_figure(tex_source: str, out_pdf: pathlib.Path) -> None:
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        tdir = pathlib.Path(td)
        (tdir / "fig.tex").write_text(tex_source, encoding="utf-8")
        res = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "fig.tex"],
            cwd=tdir,
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode != 0:
            raise RuntimeError(f"pdflatex failed for {out_pdf.name}:\n{res.stdout}\n{res.stderr}")
        shutil.copyfile(tdir / "fig.pdf", out_pdf)


def generate_figures(calib: Dict[str, Any], fig_dir: pathlib.Path) -> List[str]:
    fig_dir.mkdir(parents=True, exist_ok=True)
    out_names: List[str] = []

    # Figure 1: Complete Rational, Real-Quadratic & Cubic Lame Nauru Congruence Atlas
    fig1_tex = r"""\documentclass[tikz,border=6pt]{standalone}
\pdfinfo{/Producer () /Creator ()}
\usepackage{amsmath,amssymb,booktabs,xcolor}
\definecolor{congbg}{HTML}{E3F5E8}
\definecolor{congfg}{HTML}{0E6B35}
\definecolor{nonbg}{HTML}{FDEBE8}
\definecolor{nonfg}{HTML}{A32018}
\definecolor{hdrbg}{HTML}{1C355E}
\definecolor{cubicbg}{HTML}{EDF3FC}
\definecolor{cubicfg}{HTML}{1D4E89}
\begin{document}
\begin{tikzpicture}[font=\scriptsize\sffamily]
  \node[anchor=north,inner sep=0pt] (tbl) {
    \begin{tabular}{@{}llll@{}}
      \multicolumn{4}{@{}l@{}}{\normalsize\bfseries\color{hdrbg} Complete Rational, Real-Quadratic \& Cubic Lam\'e Nauru Congruence Atlas}\\[2pt]
      \multicolumn{4}{@{}l@{}}{\scriptsize\color{black!70} Exhaustive classification across $\mathbb{Q}$ ($3$ moduli), $\mathbb{Q}(\sqrt{D})$ ($6$ moduli, $4$ fields, $\mathrm{Ram}_{\mathrm{fin}}=\varnothing$), and cubics ($4$ moduli) --- \textbf{2 genuine congruence families}}\\[5pt]
      \toprule
      \textbf{Field / Algebra} & \textbf{Modulus / Polynomial(s)} & \textbf{Verdict} & \textbf{Exact Obstruction / Level Certificate} \\
      \midrule
      $\mathbb{Q}$ ($B_3$, $D{=}6$) & $x=\tfrac{3}{2}$ (self-twin, $2,3$: spl/ram) & \textcolor{nonfg}{\textbf{NON-CONG}} & $V_4$-cover of $X^6(\Gamma(3))\leftrightarrow K_{3,3}$; $|\mathrm{Ad}_3|{=}36$, $|\ker|{=}4$ ($36/144$) \\[2pt]
      $\mathbb{Q}$ ($B_5$, $D{=}10$) & $x=\tfrac{5}{2}$ ($\rho_6$) $\cong \tfrac{1}{2}$ ($\rho_{12}$) & \textcolor{congfg}{\textbf{CONG $3\mathfrak{P}_5$}} & $|\mathrm{Ad}_{15}|{=}|\mathrm{joint}|{=}3600$, $|\ker|{=}1$ ($144/144$); $U_5$ killed via $\gcd(25,144){=}1$ \\[2pt]
      $\mathbb{Q}$ ($B_5$, $D{=}10$) & $x=\tfrac{1}{2}$ ($\rho_6$) $\cong \tfrac{5}{2}$ ($\rho_{12}$) & \textcolor{nonfg}{\textbf{NON-CONG}} & $V_4$-cover of $X^{10}(\Gamma(3\mathfrak{P}_5))/V_4\leftrightarrow K_{3,3}$; lvl $3$: $6/144$; lvl $3\mathfrak{P}_5$: $36/144$ \\[2pt]
      \midrule
      $\mathbb{Q}(\sqrt{17})$ ($\zeta{=}\tfrac{1}{3}$) & $2x^2{-}5x{+}1,\; 2x^2{-}7x{+}4$ & \textcolor{nonfg}{\textbf{NON-CONG}} & $\mathcal{O}_{17}^{\max}\bmod v^2$: $|\mathrm{Ad}|{=}48$, $|\ker|{=}3$, $Y/C_3\cong Q_3$; $\mathrm{SL}_2(\mathbb{F}_9)$ perfect \\[2pt]
      $\mathbb{Q}(\sqrt{2})$ ($\zeta{=}\tfrac{1}{12}$) & $2x^2{-}4x{+}1,\; 2x^2{-}8x{+}7$ & \textcolor{nonfg}{\textbf{NON-CONG}} & $\mathcal{E}(\mathfrak{q}_7)$ ($T_8/8^4{=}49$): $|\mathrm{Ad}_{\mathfrak{q}_7}|{=}588$, $Y/\ker_{12}\cong\Theta_3$ ($C_6{\times}C_2 / A_4$); $|\ker^1|_2{=}4{>}1$ \\[2pt]
      $\mathbb{Q}(\sqrt{3})$ ($\zeta{=}\tfrac{1}{6}$) & $2x^2{-}6x{+}3$ (self-twin) & \textcolor{nonfg}{\textbf{NON-CONG}} & $\mathcal{E}(\mathfrak{p}_3)$ ($T_8/12^4{=}9$): $|\mathrm{Ad}_3^1|{=}243$, $|\mathrm{Ad}_3^+|{=}486$, $|\mathrm{Ad}_3|{=}972$ ($2$-part $1{<}4$) \\[2pt]
      $\mathbb{Q}(\sqrt{7})$ ($\zeta{=}\tfrac{2}{3}$) & $2x^2{-}6x{+}1$ (self-twin) & \textcolor{congfg}{\textbf{CONG $(3)$}} & $\mathcal{O}_7^{\max}\bmod(3){=}\mathfrak{p}_3\mathfrak{p}_3'$: $|\mathrm{Ad}|{=}|\mathrm{joint}|{=}576$, $|\ker|{=}1$ (\textbf{144/144 both $\rho_6,\rho_{12}$}) \\[2pt]
      \midrule
      Cubic Lam\'e ($4$) & $d_F\in\{316, 148\}$ ($2$ twin pairs) & \textcolor{cubicfg}{\textbf{4 MODULI}} & $(9,10,1),(9,10,2)$ [$d_F{=}316$, $2$-spl $v_1v_2^2$]; $(8,8,1),(10,14,5)$ [$d_F{=}148$, $v^3$] \\
      \bottomrule
    \end{tabular}
  };
\end{tikzpicture}
\end{document}
"""
    compile_tikz_figure(fig1_tex, fig_dir / "fig1_lame_congruence_atlas.pdf")
    out_names.append("fig1_lame_congruence_atlas.pdf")

    # Figure 2: Exact Hashimoto Prime Cadences & Normalized Ramanujan Deviation Corridors (from runtime data!)
    piY = calib["F1_rational_nauru_and_errata"]["nauru_pi_6_to_24"]
    devY_pts = []
    for m in [6, 8, 10, 12, 14, 16, 18, 20, 22, 24]:
        d = (m * piY[str(m)] - (2 ** (m + 1))) / (44.0 * (2 ** (m // 2)))
        devY_pts.append(f"({m},{d:.4f})")
    err18_d = (18 * 31824 - (2**19)) / (44.0 * (2**9))
    err22_d = (22 * 384792 - (2**23)) / (44.0 * (2**11))
    devZ = calib["F5_dic6_cayley_spectrum_gonality"]["norm_devs_Z"]
    devZ_pts = [f"({m},{devZ[str(m)]:.4f})" for m in [4, 6, 8, 10, 12, 14, 16]]

    fig2_tex = (
        r"""\documentclass[tikz,border=6pt]{standalone}
\pdfinfo{/Producer () /Creator ()}
\usepackage{pgfplots,amsmath,amssymb}
\pgfplotsset{compat=1.18}
\begin{document}
\begin{tikzpicture}[font=\scriptsize]
  \begin{axis}[
    name=left,
    width=6.9cm, height=5.2cm,
    title={\textbf{(a) Nauru $Y$:} $(m\pi_Y(m)-2^{m+1})/(44\cdot 2^{m/2})$},
    xlabel={Cycle length $m$ (even, girth $6$)},
    ylabel={Normalized Ramanujan deviation},
    xmin=5, xmax=25, ymin=-1.25, ymax=2.55,
    xtick={6,8,10,12,14,16,18,20,22,24},
    ytick={-1,0,1,2},
    grid=major, grid style={gray!22},
    legend pos=north west, legend style={font=\tiny,draw=gray!50}
  ]
    \addplot[draw=none,fill=teal!12,forget plot] coordinates {(5,-1) (25,-1) (25,1) (5,1)} \closedcycle;
    \addplot[dashed,red!75!black,thick,forget plot] coordinates {(5,1) (25,1)};
    \addplot[dashed,red!75!black,thick,forget plot] coordinates {(5,-1) (25,-1)};
    \addplot[teal!70!black,thick,mark=*,mark size=1.8pt] coordinates {__DEV_Y_PTS__};
    \addlegendentry{Exact $\pi_Y(6..24)$}
    \addplot[only marks,red!80!black,mark=x,mark size=3.2pt,thick] coordinates {(18,__ERR18__) (22,__ERR22__)};
    \addlegendentry{\texttt{NEG-M24} errata ($31824, 384792$)}
    \node[red!80!black,font=\tiny,anchor=east] at (axis cs:17.4,__ERR18_Y__) {$31{,}824$ ($+2.15\times$!)};
    \node[teal!70!black,font=\tiny,anchor=north] at (axis cs:18,-0.58) {$28{,}560$};
  \end{axis}

  \begin{axis}[
    at={(left.east)}, anchor=west, xshift=1.35cm,
    width=6.6cm, height=5.2cm,
    title={\textbf{(b) Dicyclic $Z$:} $(m\pi_Z(m)-2\cdot 3^m)/(44\cdot 3^{m/2})$},
    xlabel={Cycle length $m$ (even, girth $4$)},
    xmin=3, xmax=17, ymin=-1.25, ymax=1.25,
    xtick={4,6,8,10,12,14,16},
    ytick={-1,-0.5,0,0.5,1},
    grid=major, grid style={gray!22},
    legend pos=south east, legend style={font=\tiny,draw=gray!50}
  ]
    \addplot[draw=none,fill=blue!10,forget plot] coordinates {(3,-1) (17,-1) (17,1) (3,1)} \closedcycle;
    \addplot[dashed,red!75!black,thick,forget plot] coordinates {(3,1) (17,1)};
    \addplot[dashed,red!75!black,thick,forget plot] coordinates {(3,-1) (17,-1)};
    \addplot[blue!75!black,thick,mark=square*,mark size=1.8pt] coordinates {__DEV_Z_PTS__};
    \addlegendentry{Exact $\pi_Z(4..16)\subset[-0.26,+0.60]$}
    \node[blue!75!black,font=\tiny,anchor=south] at (axis cs:12,0.65) {$90{,}172$};
    \node[blue!75!black,font=\tiny,anchor=south east] at (axis cs:16.4,0.03) {$5.38\mathrm{M}$};
  \end{axis}
\end{tikzpicture}
\end{document}
"""
        .replace("__DEV_Y_PTS__", " ".join(devY_pts))
        .replace("__ERR18__", f"{err18_d:.4f}")
        .replace("__ERR22__", f"{err22_d:.4f}")
        .replace("__ERR18_Y__", f"{err18_d:.2f}")
        .replace("__DEV_Z_PTS__", " ".join(devZ_pts))
    )
    compile_tikz_figure(fig2_tex, fig_dir / "fig2_hashimoto_ramanujan_corridors.pdf")
    out_names.append("fig2_hashimoto_ramanujan_corridors.pdf")

    # Figure 3: Dicyclic Cayley Graph Z, 4-Path Egg E_0, Witness D_8 & Gonality Collapse Bar Chart
    Z = build_dic6_cayley([1, 11, 12, 18])
    edge_cmds = []
    for u in range(24):
        for v in Z[u]:
            if u < v:
                if (u in (0, 1, 2, 20)) and (v in (0, 1, 2, 20)):
                    edge_cmds.append(f"\\draw[red!80!black,very thick] (v{u}) -- (v{v});")
                else:
                    edge_cmds.append(f"\\draw[gray!55,thin] (v{u}) -- (v{v});")
    node_cmds = []
    d8_set = {0, 3, 6, 9, 12, 15, 18, 21}
    e0_set = {0, 1, 2, 20}
    for k in range(12):
        ang = 90 - 30 * k
        fill_o = "red!80!black" if k in e0_set else "white"
        txt_o = "white" if k in e0_set else "black"
        ring_o = "draw=orange!85!black,line width=1.4pt" if k in d8_set else "draw=blue!65!black,thin"
        node_cmds.append(
            f"\\node[circle,inner sep=1pt,minimum size=11pt,fill={fill_o},text={txt_o},{ring_o},font=\\tiny] (v{k}) at ({ang}:2.25cm) {{{k}}};"
        )
        idx = 12 + k
        fill_i = "red!80!black" if idx in e0_set else "white"
        txt_i = "white" if idx in e0_set else "black"
        ring_i = "draw=orange!85!black,line width=1.4pt" if idx in d8_set else "draw=teal!65!black,thin"
        node_cmds.append(
            f"\\node[circle,inner sep=1pt,minimum size=11pt,fill={fill_i},text={txt_i},{ring_i},font=\\tiny] (v{idx}) at ({ang}:1.25cm) {{{idx}}};"
        )

    fig3_tex = (
        r"""\documentclass[tikz,border=6pt]{standalone}
\pdfinfo{/Producer () /Creator ()}
\usepackage{pgfplots,amsmath,amssymb}
\pgfplotsset{compat=1.18}
\begin{document}
\begin{tikzpicture}[font=\scriptsize]
  \begin{scope}[xshift=0cm,yshift=2.45cm]
    \node[font=\bfseries] at (0,2.85) {(a) $Z=\mathrm{Cay}(\mathrm{Dic}_6,S_Z)$: Egg $E_0$ \& Witness $D_8$};
    __NODE_CMDS__
    __EDGE_CMDS__
    \node[font=\tiny,align=center] at (0,-2.85) {Crimson: $E_0{=}\{0,1,2,20\}$ ($276/276$ touching) \quad Gold rings: $D_8{=}\langle x^3\rangle+\langle x^3\rangle y$ ($168/168$ cells)};
  \end{scope}

  \begin{axis}[
    at={(3.55cm,0.35cm)},
    width=6.7cm, height=4.8cm,
    ybar=4pt, bar width=18pt,
    title={\textbf{(b) Exact Gonality Collapse: $Y$ ($6$) vs.\ $Z$ ($8$)}},
    ylabel={Invariant value},
    ymin=0, ymax=9.8,
    xtick={1,2,3,4},
    xticklabels={{$Y$ $24$-star\\($h{=}e{=}6$)},{$Y$ collapse\\($132$ cells)},{$Z$ $24$-star\\(subopt.)},{$Z$ $\mathcal{S}_4$ \& $D_8$\\($168$ cells)}},
    xticklabel style={align=center,font=\tiny},
    nodes near coords,
    nodes near coords style={font=\scriptsize\bfseries},
    grid=major, ymajorgrids=true, xmajorgrids=false, grid style={gray!20}
  ]
    \addplot[fill=teal!65!black,draw=teal!80!black] coordinates {(1,6) (2,6)};
    \addplot[fill=orange!75!black,draw=orange!85!black] coordinates {(3,6)};
    \addplot[fill=red!75!black,draw=red!85!black] coordinates {(4,8)};
  \end{axis}
  \node[draw=gray!55,rounded corners=2pt,fill=gray!6,font=\tiny,align=left,anchor=north west] at (3.55cm,-0.32cm) {%
    Exhaustive Dhar on $Z$: $0/98{,}280$ (deg $6$), $0/475{,}020$ (deg $7$)\\
    $\|\mathcal{S}_4\|=\min(h{=}8, e{=}8)=8=\operatorname{gon}(\Gamma_{\mathrm{eq}}(Z))\le\operatorname{gon}(\mathcal{C}_Z)$
  };
\end{tikzpicture}
\end{document}
"""
        .replace("__NODE_CMDS__", "\n    ".join(node_cmds))
        .replace("__EDGE_CMDS__", "\n    ".join(edge_cmds))
    )
    compile_tikz_figure(fig3_tex, fig_dir / "fig3_dic6_scramble_gonality.pdf")
    out_names.append("fig3_dic6_scramble_gonality.pdf")

    # Figure 4: Rational 3-Adic Fricke-Vogt 8x8 Moduli Grid & Three-Column Galois Covering Mirror
    grid_vals = [1, 2, 4, 5, 7, 8, 10, 11]
    cell_cmds = []
    labels_dom = {
        (1, 4): r"$B_2(11)$",
        (2, 2): r"$B_2(5)$",
        (2, 4): r"$B_5(2)$",
        (4, 4): r"$B_2$",
        (4, 5): r"$B_{70}$",
    }
    for ri, m in enumerate(grid_vals):
        for ci, n in enumerate(grid_vals):
            x = ci * 0.62
            y = (7 - ri) * 0.62
            in_dom = m in (1, 2, 4, 5) and n in (1, 2, 4, 5) and m <= n
            pass4 = (m * n) % 4 == 0
            if in_dom and pass4:
                fill = "teal!30"
                txt = labels_dom[(m, n)]
            elif in_dom:
                fill = "red!18"
                txt = r"$\times$"
            elif pass4:
                fill = "teal!8"
                txt = r"$\cdot$"
            else:
                fill = "gray!6"
                txt = ""
            cell_cmds.append(
                f"\\filldraw[fill={fill},draw=gray!45] ({x:.2f},{y:.2f}) rectangle ({x+0.62:.2f},{y+0.62:.2f});"
            )
            if txt:
                cell_cmds.append(f"\\node[font=\\tiny] at ({x+0.31:.2f},{y+0.31:.2f}) {{{txt}}};")
    for idx, v in enumerate(grid_vals):
        cell_cmds.append(f"\\node[font=\\tiny] at ({idx*0.62+0.31:.2f},5.15) {{{v}}};")
        cell_cmds.append(f"\\node[font=\\tiny] at (-0.25,{(7-idx)*0.62+0.31:.2f}) {{{v}}};")

    fig4_tex = (
        r"""\documentclass[tikz,border=6pt]{standalone}
\pdfinfo{/Producer () /Creator ()}
\usepackage{amsmath,amssymb}
\begin{document}
\begin{tikzpicture}[font=\scriptsize]
  \begin{scope}[xshift=0cm,yshift=0cm]
    \node[font=\bfseries] at (2.48,5.65) {(a) $8\times 8$ Fricke--Vogt Grid ($D_4\to 10$ pairs, $5$ pass $4\mid mn$)};
    __CELL_CMDS__
    \node[font=\tiny] at (2.48,5.38) {$n\pmod{12}$ ($3\nmid n$)};
    \node[font=\tiny,rotate=90] at (-0.55,2.48) {$m\pmod{12}$ ($3\nmid m$)};
    \node[font=\tiny,align=center] at (2.48,-0.40) {$B_Z(u,v)=(-\tfrac{1-u}{u},-\tfrac{1-v}{v}/\mathbb{Q})$, $u=\tfrac{m}{12}, v=\tfrac{n}{12}$};
  \end{scope}

  \begin{scope}[xshift=6.05cm,yshift=0.1cm]
    \node[font=\bfseries] at (3.65,5.55) {(b) Three-Column Galois Covering Mirror \& $0/80$ Non-Congruence};
    \node[draw=blue!70!black,rounded corners=3pt,fill=blue!8,minimum width=2.2cm,align=center,font=\tiny] (c1t) at (1.1,4.45) {$\mathcal{C}_Y(3/2)$\\$B_3$ ($2$-adic Nauru)};
    \node[draw=blue!70!black,rounded corners=3pt,fill=blue!4,minimum width=2.2cm,align=center,font=\tiny] (c1m) at (1.1,2.65) {$K_{3,3}$ ($g=4$)\\$V=6, E=9\times 4$};
    \node[draw=red!70!black,rounded corners=2pt,fill=red!6,minimum width=2.2cm,align=center,font=\tiny] (c1b) at (1.1,1.15) {Pro-$3$ obstructed\\$|\mathrm{Ad}_3|=36, |\ker|=4$};
    \draw[->,thick] (c1t) -- node[right,font=\tiny]{$V_4$ (deg $4$)} (c1m);
    \draw[dashed,gray] (c1m) -- (c1b);

    \node[draw=orange!80!black,rounded corners=3pt,fill=orange!10,minimum width=2.25cm,align=center,font=\tiny] (c2t) at (3.65,4.45) {$\mathcal{C}_Z(4,4)$\\$B_2$ ($3$-adic $\mathrm{Dic}_6$)};
    \node[draw=orange!80!black,rounded corners=3pt,fill=orange!4,minimum width=2.25cm,align=center,font=\tiny] (c2m) at (3.65,2.65) {$K_{4,4}$ ($g=9$)\\$V=8, E=16\times 3$};
    \node[draw=red!70!black,rounded corners=2pt,fill=red!6,minimum width=2.25cm,align=center,font=\tiny] (c2b) at (3.65,1.15) {Pro-$2$ obstructed\\$L_8/\{\pm 1\}$ ($64$) / $\mathrm{Ad}_{16}$ ($1024$)\\$16/16$ $|\ker|=3$};
    \draw[->,thick] (c2t) -- node[right,font=\tiny]{$C_3$ (deg $3$)} (c2m);
    \draw[dashed,gray] (c2m) -- (c2b);

    \node[draw=teal!75!black,rounded corners=3pt,fill=teal!9,minimum width=2.2cm,align=center,font=\tiny] (c3t) at (6.2,4.45) {$\mathcal{C}_Y(\tfrac{5+\sqrt{17}}{4})$\\$\mathbb{Q}(\sqrt{17})$ Nauru};
    \node[draw=teal!75!black,rounded corners=3pt,fill=teal!4,minimum width=2.2cm,align=center,font=\tiny] (c3m) at (6.2,2.65) {Cube $Q_3$ ($g=5$)\\$V=8, E=12\times 3$};
    \node[draw=red!70!black,rounded corners=2pt,fill=red!6,minimum width=2.2cm,align=center,font=\tiny] (c3b) at (6.2,1.15) {Pro-$2$ + $\mathrm{SL}_2(\mathbb{F}_9)$\\$|\mathrm{Ad}_{v^2}|=48, |\ker|=3$};
    \draw[->,thick] (c3t) -- node[right,font=\tiny]{$C_3$ (deg $3$)} (c3m);
    \draw[dashed,gray] (c3m) -- (c3b);

    \node[draw=red!75!black,rounded corners=2pt,fill=red!8,minimum width=7.3cm,align=center,font=\tiny] at (3.65,-0.15) {%
      \textbf{$3$-Adic $\mathrm{Dic}_6$ Resolution: $0/80$ Rational Realizations Are Congruence}\\
      CRT left-mult $\Gamma(M)$ + Riehm mod $8$ ($\mathcal{O}_{70}^1$: $768/256/3$, $-I\in[G,G]$) + unique normal $C_3$
    };
  \end{scope}
\end{tikzpicture}
\end{document}
"""
        .replace("__CELL_CMDS__", "\n    ".join(cell_cmds))
    )
    compile_tikz_figure(fig4_tex, fig_dir / "fig4_fricke_vogt_three_column_mirror.pdf")
    out_names.append("fig4_fricke_vogt_three_column_mirror.pdf")

    return out_names


# ==============================================================================
# Main Driver & Data Model Manifest Management
# ==============================================================================


def main() -> int:
    parser = argparse.ArgumentParser(description="Independent pure-Python verifier for Paper PC-III.")
    parser.add_argument("--check-only", action="store_true", help="Verify all 8 gates & JSON parity without writing files.")
    parser.add_argument("--no-figs", action="store_true", help="Skip regenerating TikZ PDF figures.")
    args = parser.parse_args()

    t0 = time.perf_counter()
    print("Running Paper PC-III (Triadic 3-Adic Frontier) 8-gate pure-Python verification...")

    gates = [
        ("F1_rational_nauru_and_errata", "Pillar I: Twin Duality, B3/B5 Level 3P_5 Congruence & Errata", gate_f1_rational_nauru_and_errata),
        ("F2_nauru_metric_gonality", "Pillar I: Nauru 24-Star Scramble & 132/132 Continuous Metric Dhar", gate_f2_nauru_metric_gonality),
        ("F3_real_quadratic_and_cubic_census", "Pillar II: 6 Real-Quadratic & 4 Totally Real Cubic Lame Moduli", gate_f3_real_quadratic_and_cubic_census),
        ("F4_real_quadratic_congruence", "Pillar II: Complete 4-Field Congruence Atlas & Q(sqrt(7)) Level (3)", gate_f4_real_quadratic_congruence),
        ("F5_dic6_cayley_spectrum_gonality", "Pillar III: Dic_6 18 Cayley, pi_Z(4..16), 43 Inv, S_4 & 168/168 Dhar", gate_f5_dic6_cayley_spectrum_gonality),
        ("F6_dic6_fricke_vogt_and_crt_noncongruence", "Pillar III: Fricke-Vogt 5/10, 0/80 CRT Left-Mult, Hurwitz L_8/Ad_16 & Riehm", gate_f6_dic6_fricke_vogt_and_crt_noncongruence),
        ("F7_genus25_borel_census", "Pillar III: Complete Genus-25 3-Adic Borel Shimura Census (19 / 9 TF)", gate_f7_genus25_borel_census),
        ("F8_poitou_odlyzko_audit", "Section 5: Poitou-Odlyzko Strict-Positivity & Anti-Facade Audit", gate_f8_poitou_odlyzko_audit),
    ]

    payload: Dict[str, Any] = {
        "schema_version": "1.0.0",
        "paper": "PC-III: The 3-Adic Dicyclic Companion, Exact Level 3P_5 and Level (3) Congruence on Nauru, and the Real-Quadratic Lame Shimura Curve Atlas",
        "license": "CC-BY-4.0",
    }

    for key, label, fn in gates:
        gt0 = time.perf_counter()
        res = fn()
        dt = time.perf_counter() - gt0
        payload[key] = res
        print(f"  [PASS] {key.split('_')[0]} ({label}) [{dt:.2f}s]")

    canon_bytes = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    digest = hashlib.sha256(canon_bytes).hexdigest()
    json_path = DATA_DIR / "triadic_3adic_calibration.json"
    manifest_path = DATA_DIR / "MANIFEST.sha256"

    if args.check_only:
        if not json_path.is_file():
            print(f"[FAIL] Missing calibration artifact: {json_path}", file=sys.stderr)
            return 1
        disk_bytes = json_path.read_bytes()
        disk_digest = hashlib.sha256(disk_bytes).hexdigest()
        if disk_digest != digest:
            print(
                f"[FAIL] Calibration digest mismatch: computed {digest[:16]} != disk {disk_digest[:16]}",
                file=sys.stderr,
            )
            return 1
        print(f"  [PASS] Data Model byte-exact parity OK (SHA-256 {digest[:16]}...)")
    else:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        json_path.write_bytes(canon_bytes)
        rel_json = json_path.relative_to(REPO_ROOT).as_posix()
        manifest_path.write_text(f"{digest}  {rel_json}\n", encoding="utf-8")
        print(f"  [WROTE] {rel_json} (SHA-256 {digest[:16]}...)")
        if not args.no_figs:
            figs = generate_figures(payload, FIG_DIR)
            print(f"  [FIGS] Generated {len(figs)} metadata-free vector PDFs: {', '.join(figs)}")

    print(f"Summary: 8/8 Paper PC-III gates PASS in {time.perf_counter() - t0:.2f}s.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
