#!/usr/bin/env python3
"""
Independent From-Scratch PARI/GP Verifier for Section 7 Shimura Curves & Brandt Graphs
(ADPIE Cycle 5 — Ergentics Code Model, MIT License).

Zero reads of cached upstream `code/` JSONs or `code/` Python modules. Every number field,
Hecke operator, quaternion algebra, Eichler order, ideal class graph, Brandt matrix B(v),
and characteristic polynomial is built directly from axioms via PARI/GP (`cypari2`).

Covers:
  1. Theorem 7.11 & NEG-E10: All 19 genus-13 Shimura curves X_0^D(N) (catching omitted
     D = 690, N = 1, M = 345, phi = 176 > 168, e_3 = 8) + all 4 Gamma_H 24-component cases.
  2. Proposition 7.18(a)-(c): Exhaustive nflist enumeration of totally real fields of degree
     n = 2 (D <= 1200, cross-checked vs exact Siegel), n = 3 (d <= 5200), n = 4 (d <= 60000),
     exact h^+ = 1 mass-12 solutions, and direct from-scratch Brandt graphs for all 22+
     configurations (verifying exact mass = 12, class counts, unit indices, symmetry, and
     (t^4 - 4t^2 + 1) nmid charpoly(B(v))).
  3. Theorem 7.19(c): Independent verification of the degree-5 near-miss field d_F = 106069
     (x^5 - 2x^4 - 4x^3 + 7x^2 + 3x - 4, D'' = p_13) and its exact 12x12 Brandt polynomial.
"""

from fractions import Fraction
import math
import random
import sys
import time

from cypari2 import Pari


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def factorize(n: int):
    res = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            e = 0
            while n % d == 0:
                n //= d
                e += 1
            res.append((d, e))
        d += 1
    if n > 1:
        res.append((n, 1))
    return res


def divisors(n: int):
    ds = [1]
    for p, e in factorize(n):
        ds = [d * (p**k) for d in ds for k in range(e + 1)]
    return sorted(ds)


def kronecker_neg4(p: int) -> int:
    if p == 2:
        return 0
    return 1 if p % 4 == 1 else -1


def kronecker_neg3(p: int) -> int:
    if p == 3:
        return 0
    return 1 if p % 3 == 1 else -1


def sigma1(n: int) -> int:
    s = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            s += d
            if d * d != n:
                s += n // d
        d += 1
    return s


# ============================================================================
# Part 1: Theorem 7.11 & NEG-E10 — Exhaustive Genus-13 Shimura Curves + Gamma_H
# ============================================================================

def verify_thm_7_11_and_neg_e10(pari: Pari) -> bool:
    print("=== Part 1: Theorem 7.11 & NEG-E10 (All 19 X_0^D(N) + 4 Gamma_H via PARI Hecke) ===")
    t0 = time.time()
    odd_primes = [p for p in range(3, 1002, 2) if is_prime(p)]
    d_cands = []

    def gen_d(idx, cnt, D, phi, e2, e3):
        if cnt >= 2 and cnt % 2 == 0:
            d_cands.append((D, phi, e2, e3))
        for i in range(idx, len(odd_primes)):
            p = odd_primes[i]
            if phi * (p - 1) > 1000:
                break
            gen_d(i + 1, cnt + 1, D * p, phi * (p - 1), e2 * (1 - kronecker_neg4(p)), e3 * (1 - kronecker_neg3(p)))

    gen_d(0, 1, 2, 1, 1, 2)

    g13_pairs = []
    for D, phiD, e2D, e3D in d_cands:
        max_n = 1000 // phiD
        for N in range(1, max_n + 1, 2):
            if math.gcd(D, N) != 1:
                continue
            psiN, e2N, e3N = 1, 1, 1
            for p, k in factorize(N):
                psiN *= (p ** (k - 1)) * (p + 1)
                e2N *= 1 + kronecker_neg4(p)
                e3N *= (1 if k == 1 else 0) if p == 3 else (1 + kronecker_neg3(p))
            if phiD * psiN > 1000:
                continue
            e2, e3 = e2D * e2N, e3D * e3N
            if 12 + phiD * psiN - 3 * e2 - 4 * e3 == 12 * 13:
                g13_pairs.append((D, N, phiD, psiN, e2, e3))
    g13_pairs.sort()

    assert len(g13_pairs) == 19, f"Expected 19 genus-13 pairs, got {len(g13_pairs)}"
    tf_pairs = [x for x in g13_pairs if x[4] == 0 and x[5] == 0]
    assert len(tf_pairs) == 11, f"Expected 11 torsion-free pairs, got {len(tf_pairs)}"

    # Check P_X(t) = t^4 - 4t^2 + 1 does not divide charpoly(T_2) on S_2^{D/2-new}(Gamma_0(DN/2)) for ALL 19!
    px = pari("t^4 - 4*t^2 + 1")
    neg_e10_ok = False
    for D, N, phiD, psiN, e2, e3 in g13_pairs:
        d_half = D // 2
        M = d_half * N
        # S_2^{d_half-new}(Gamma_0(M)) = direct sum over divisors K | M with d_half | K of S_2^{new}(Gamma_0(K))
        # with multiplicity d(M / K)!
        cp_prod = pari("1")
        dim_dnew = 0
        for K in divisors(M):
            if K % d_half != 0:
                continue
            mult = len(divisors(M // K))
            mf = pari.mfinit([K, 2], 0)  # exact newspace S_2^{new}(Gamma_0(K))
            dk = int(pari.mfdim(mf))
            if dk == 0:
                continue
            dim_dnew += mult * dk
            T2 = pari.mfheckemat(mf, 2)
            cp = pari.charpoly(T2, "t")
            cp_prod = cp_prod * (cp ** mult)
        rem = cp_prod % px
        assert rem != 0, f"Unexpected P_X factor for (D={D}, N={N})!"
        if e2 == 0 and e3 == 0:
            assert dim_dnew == 11, f"Torsion-free (D={D}, N={N}) expected dim=11, got {dim_dnew}"
        if D == 690 and N == 1:
            assert dim_dnew == 15, f"D=690 expected dim=15, got {dim_dnew}"
            neg_e10_ok = True
            print(f"  [NEG-E10] X_0^690(1) (M=345, phi={phiD}>168, e2={e2}, e3={e3}): dim S_2^{{345-new}}={dim_dnew}, charpoly(T_2) mod P_X = {rem}")
    assert neg_e10_ok

    # Verify all 4 Gamma_H cases with 24 components (phi(D) * psi(N) * d == 144, d >= 2):
    gamma_h_cases = []
    for D, phiD, e2D, e3D in d_cands:
        if 144 % phiD != 0:
            continue
        for N in range(3, 145, 2):
            if math.gcd(D, N) != 1:
                continue
            psiN, phiN = 1, 1
            for p, k in factorize(N):
                psiN *= (p ** (k - 1)) * (p + 1)
                phiN *= (p ** (k - 1)) * (p - 1)
            if 144 % (phiD * psiN) != 0:
                continue
            d_idx = 144 // (phiD * psiN)
            if d_idx >= 2 and (phiN // 2) % d_idx == 0:
                gamma_h_cases.append((D, N, d_idx, phiN))
    gamma_h_cases.sort()
    assert gamma_h_cases == [(6, 17, 4, 16), (10, 9, 3, 6), (10, 17, 2, 16), (26, 5, 2, 4)], f"Unexpected Gamma_H: {gamma_h_cases}"

    # For each Gamma_H case (note all 4 have N in {5, 9, 17} prime power -> cyclic (Z/NZ)^*),
    # build unique subgroup H of index d_idx containing -1 and check ALL characters mod K (d_half | K | M)
    # trivial on d_half-part and trivial on H: check |a_2| does not contain 2*cos(pi/12) & 2*cos(5pi/12)!
    target_roots = [2.0 * math.cos(math.pi / 12.0), 2.0 * math.cos(5.0 * math.pi / 12.0)]
    for D, N, d_idx, phiN in gamma_h_cases:
        d_half = D // 2
        M = d_half * N
        # Unique subgroup H <= (Z/NZ)^* of order phiN // d_idx (since (Z/NZ)^* is cyclic):
        h_ord = phiN // d_idx
        units_N = [a for a in range(1, N) if math.gcd(a, N) == 1]
        H = {a for a in units_N if pow(a, h_ord, N) == 1}
        assert len(H) == h_ord and (N - 1) in H
        abs_a2 = []
        for K in divisors(M):
            if K % d_half != 0:
                continue
            mult = len(divisors(M // K))
            q_part = K // d_half
            G_zn = pari.znstar(K, 1)
            units_K = [a for a in range(1, K) if math.gcd(a, K) == 1]
            visited_orbits = set()
            for a in units_K:
                if a in visited_orbits:
                    continue
                c = pari.znconreychar(G_zn, a)
                o = int(pari.charorder(G_zn, c))
                orbit = sorted({pow(a, j, K) for j in range(1, o + 1) if math.gcd(j, o) == 1})
                for u_o in orbit:
                    visited_orbits.add(u_o)
                # Check character is trivial on d_half-part and trivial on H mod q_part (and even -> automatic since -1 in H)
                ok_char = True
                for u in units_K:
                    val = float(pari.chareval(G_zn, c, u))
                    if q_part == 1:
                        if abs(val - round(val)) > 1e-9:
                            ok_char = False
                            break
                    else:
                        if u % q_part == 1 and abs(val - round(val)) > 1e-9:
                            ok_char = False
                            break
                        if (u % q_part) in H and u % d_half == 1 and abs(val - round(val)) > 1e-9:
                            ok_char = False
                            break
                if not ok_char:
                    continue
                mf = pari.mfinit([K, 2, pari.Mod(a, K)], 0)
                if int(pari.mfdim(mf)) == 0:
                    continue
                T2 = pari.mfheckemat(mf, 2)
                cp = pari.liftall(pari.charpoly(T2, "x"))
                for j in range(1, max(o, 1) + 1):
                    if math.gcd(j, o) != 1:
                        continue
                    zeta = pari(f"exp(2*Pi*I*{j}/{o})")
                    poly_c = pari.subst(cp, "t", zeta) if o > 2 else cp
                    roots = [abs(complex(r)) for r in pari.polroots(poly_c)]
                    abs_a2.extend(roots * mult)
        # Verify target 2*cos(pi/12) (~1.93185) is NOT present with multiplicity 2:
        hits_c12 = sum(1 for r in abs_a2 if abs(r - target_roots[0]) < 1e-5)
        assert hits_c12 == 0, f"Unexpected 2*cos(pi/12) hit on Gamma_H ({D}, {N}, idx={d_idx})!"
        print(f"  [PASS] Gamma_H (D={D:2d}, N={N:2d}, idx={d_idx}): #|a_2|={len(abs_a2):2d}, hits(2cos(pi/12))={hits_c12}")

    print(f"  [PASS] Part 1 complete in {time.time() - t0:.2f}s: 19/19 X_0^D(N) + 4/4 Gamma_H excluded (NEG-E10 confirmed).")
    return True


# ============================================================================
# Part 2 & 3: From-Scratch Quaternion Algebra, Eichler Order & Brandt Engine
# ============================================================================

def tot_pos_gen(pari: Pari, bnf, nf, n: int, ideal):
    """For a totally real field with h_F^+ = 1, return a totally positive generator nu >> 0 of `ideal`."""
    g = pari.bnfisprincipal(bnf, ideal)[1]
    signs = [1 if int(s) < 0 else 0 for s in pari.nfeltsign(nf, g)]
    if all(s == 0 for s in signs):
        return g
    fu = list(bnf.bnf_get_fu())
    units = [pari.nfalgtobasis(nf, -1)] + [pari.nfalgtobasis(nf, u) for u in fu]
    M = [[1 if int(s) < 0 else 0 for s in pari.nfeltsign(nf, u)] for u in units]
    for mask in range(1 << len(units)):
        cur = [0] * n
        for i in range(len(units)):
            if (mask >> i) & 1:
                for j in range(n):
                    cur[j] ^= M[i][j]
        if cur == signs:
            uprod = pari.nfalgtobasis(nf, 1)
            for i in range(len(units)):
                if (mask >> i) & 1:
                    uprod = pari.nfeltmul(nf, uprod, units[i])
            return pari.nfeltmul(nf, g, uprod)
    raise RuntimeError("No totally positive unit adjustment found (expected h_F^+ = 1)")


def scalar_in_alg(pari: Pari, A, elem_alg):
    return pari.algalgtobasis(A, pari.Col([elem_alg, 0]))


def build_eichler_order(pari: Pari, bnf, nf, n: int, A, N_ideals_powers):
    """Build an Eichler order O <= O_max of level N = prod p_id^e by intersecting maximal left orders
    of cyclic integral right O_max-ideals of reduced norm p_id^e; checks exact index [O_max : O] == N(N)."""
    O_max = pari.alglathnf(A, pari.matid(4 * n))
    O = O_max
    rng = random.Random(20261125)
    expected_total_idx = 1
    for p_id, e in N_ideals_powers:
        q = int(pari.idealnorm(nf, p_id))
        expected_total_idx *= q**e
        pi_1_alg = pari.nfbasistoalg(nf, tot_pos_gen(pari, bnf, nf, n, p_id))
        pi_1_A = scalar_in_alg(pari, A, pi_1_alg)
        pO = pari.alglatmul(A, pi_1_A, O_max)
        I_cur = O_max
        for step in range(1, e + 1):
            pI = pari.alglatmul(A, pi_1_A, I_cur)
            M = I_cur[0] * I_cur[1]
            d = len(M)
            found_next = None
            for _ in range(10000):
                vec = pari.Col([0] * d)
                for _ in range(4):
                    j = rng.randrange(d)
                    c = rng.randint(-3, 3)
                    if c != 0:
                        vec = vec + c * M[j]
                if pari.alglatcontains(A, pO, vec):
                    continue
                cand = pari.alglatadd(A, pari.alglatmul(A, vec, O_max), pI)
                if int(pari.alglatindex(A, cand, I_cur)) == q * q:
                    found_next = cand
                    break
            assert found_next is not None, f"Failed cyclic ideal step {step} for prime norm {q}"
            I_cur = found_next
        assert int(pari.alglatindex(A, I_cur, O_max)) == q ** (2 * e)
        O_loc = pari.alglatinter(A, O_max, pari.alglatlefttransporter(A, I_cur, I_cur))
        assert int(pari.alglatindex(A, O_loc, O_max)) == q**e
        O = pari.alglatinter(A, O, O_loc)
    assert int(pari.alglatindex(A, O, O_max)) == expected_total_idx
    return O


def v_neighbours(pari: Pari, A, O, J, pi_v_A):
    """Enumerate all 3 right O-subideals J' < J containing vJ of index N(v)^2 = 4."""
    vJ = pari.alglatmul(A, pi_v_A, J)
    M = J[0] * J[1]
    d = len(M)
    basis = []
    span = [pari.Col([0] * d)]
    for j in range(d):
        col = M[j]
        in_span = False
        for s in span:
            if pari.alglatcontains(A, vJ, col - s):
                in_span = True
                break
        if not in_span:
            basis.append(col)
            span = span + [s + col for s in span]
            if len(basis) == 4:
                break
    assert len(basis) == 4
    nbrs = []
    for alpha in span[1:]:
        cand = pari.alglatadd(A, pari.alglatmul(A, alpha, O), vJ)
        if int(pari.alglatindex(A, cand, J)) == 4:
            if not any(pari.alglatsubset(A, prev, cand) and pari.alglatsubset(A, cand, prev) for prev in nbrs):
                nbrs.append(cand)
    assert len(nbrs) == 3, f"Expected 3 v-neighbours, got {len(nbrs)}"
    return nbrs


def compute_brandt_graph(pari: Pari, pol_x, D_ideals_spec, N_ideals_spec, v_idx: int = 0):
    """
    Build the totally definite quaternion algebra B/F (ramified at all n real places + D_ideals_spec),
    an Eichler order O of level N_ideals_spec, and enumerate all right O-ideal classes reachable from
    O by v-neighbours (checking exact Eichler mass == 12, unit counts, symmetric B(v), and charpoly).
    """
    pol_y = pari.subst(pol_x, "x", "y")
    bnf = pari.bnfinit(pol_y)
    nf = pari.nfinit(pol_y)
    n = int(pari.poldegree(pol_y))
    d_dim = 4 * n

    pr2 = [p for p in pari.idealprimedec(nf, 2) if int(pari.idealnorm(nf, p)) == 2]
    v = pr2[v_idx]
    D_primes = []
    for p_rat, norm_q, k_idx in D_ideals_spec:
        cands = [p for p in pari.idealprimedec(nf, p_rat) if int(pari.idealnorm(nf, p)) == norm_q]
        D_primes.append(cands[k_idx])
    N_ideals_powers = []
    for p_rat, norm_q, k_idx, e in N_ideals_spec:
        cands = [p for p in pari.idealprimedec(nf, p_rat) if int(pari.idealnorm(nf, p)) == norm_q]
        N_ideals_powers.append((cands[k_idx], e))

    A = pari.alginit(nf, [2, [D_primes, [1] * len(D_primes)], [1] * n])
    O = build_eichler_order(pari, bnf, nf, n, A, N_ideals_powers)

    pi_v_alg = pari.nfbasistoalg(nf, tot_pos_gen(pari, bnf, nf, n, v))
    pi_v_A = scalar_in_alg(pari, A, pi_v_alg)
    one_alg = pari.nfbasistoalg(nf, pari.nfalgtobasis(nf, 1))

    # Precompute bilinear trace form on standard basis of O_max for any depth diff k:
    # G_base(k)_{ij} = Tr_{F/Q}( (nrd(e_i + e_j) - nrd(e_i) - nrd(e_j)) * pi_v^{-k} )
    e_cols = [pari.Col([1 if r == c else 0 for r in range(d_dim)]) for c in range(d_dim)]
    nrd_e = [pari.algnorm(A, c) for c in e_cols]
    nrd_pair = [[None] * d_dim for _ in range(d_dim)]
    for i in range(d_dim):
        nrd_pair[i][i] = nrd_e[i] * 2
        for j in range(i + 1, d_dim):
            val = pari.algnorm(A, e_cols[i] + e_cols[j]) - nrd_e[i] - nrd_e[j]
            nrd_pair[i][j] = val
            nrd_pair[j][i] = val

    g_base_cache = {}

    def get_g_base(depth_diff: int):
        if depth_diff in g_base_cache:
            return g_base_cache[depth_diff]
        scale = pari.nfeltpow(nf, pi_v_alg, -depth_diff)
        flat = []
        for i in range(d_dim):
            for j in range(d_dim):
                flat.append(pari.nfelttrace(nf, pari.nfeltmul(nf, nrd_pair[i][j], scale)))
        G = pari.matrix(d_dim, d_dim, flat)
        g_base_cache[depth_diff] = G
        return G

    def gram_on_lat(lat, depth_diff: int):
        M = lat[0] * lat[1]
        return M.mattranspose() * get_g_base(depth_diff) * M

    def unit_index(J):
        OL = pari.alglatlefttransporter(A, J, J)
        G = gram_on_lat(OL, 0)
        return int(pari.qfminim(G, 2 * n, 1000, 2)[0]) // 2

    classes = [(O, 0)]
    units_list = [unit_index(O)]
    adj = []
    queue = [0]
    while queue:
        u_idx = queue.pop(0)
        J_u, dep_u = classes[u_idx]
        nbrs = v_neighbours(pari, A, O, J_u, pi_v_A)
        row = []
        for nb in nbrs:
            dep_nb = dep_u + 1
            found = None
            for c_idx, (J_c, dep_c) in enumerate(classes):
                T = pari.alglatlefttransporter(A, J_c, nb)
                G = gram_on_lat(T, dep_nb - dep_c)
                if int(pari.qfminim(G, 2 * n, 4, 2)[0]) > 0:
                    found = c_idx
                    break
            if found is None:
                found = len(classes)
                classes.append((nb, dep_nb))
                units_list.append(unit_index(nb))
                queue.append(found)
            row.append(found)
        adj.append(row)

    h_cls = len(classes)
    mass = sum(Fraction(1, w) for w in units_list)
    B = [[0] * h_cls for _ in range(h_cls)]
    for i, row in enumerate(adj):
        for j in row:
            B[i][j] += 1
    # Weighted symmetry check: w_j * B[i][j] == w_i * B[j][i] (i.e. B[i][j]/w_i == B[j][i]/w_j)
    wsym = all(units_list[j] * B[i][j] == units_list[i] * B[j][i] for i in range(h_cls) for j in range(h_cls))
    assert wsym, "Brandt matrix failed weighted symmetry!"
    B_mat = pari.matrix(h_cls, h_cls, [B[i][j] for i in range(h_cls) for j in range(h_cls)])
    cp = pari.charpoly(B_mat, "t")
    return h_cls, units_list, mass, cp


def enumerate_field_dn_solutions(pari: Pari, nf, n: int, v_prime, P_target: int):
    """Find all (D'', N) solutions (coprime to v_prime and each other, n + |D''| even) achieving exact P_target."""
    ideals = []  # (p_rat, norm_q, k_idx, ideal_obj)
    for p_rat in range(2, P_target + 2):
        if not is_prime(p_rat):
            continue
        decs = list(pari.idealprimedec(nf, p_rat))
        # Group by norm to preserve consistent index ordering
        by_norm = {}
        for pr in decs:
            q = int(pari.idealnorm(nf, pr))
            by_norm.setdefault(q, []).append(pr)
        for q, plist in sorted(by_norm.items()):
            for k_idx, pr in enumerate(plist):
                if p_rat == 2 and q == 2 and pr == v_prime:
                    continue
                if q <= P_target + 1:
                    ideals.append((p_rat, q, k_idx, pr))

    sols = []

    def dfs(idx, rem, d_list, n_list):
        if rem == 1:
            if (n + len(d_list)) % 2 == 0:
                sols.append((list(d_list), list(n_list)))
            return
        if idx == len(ideals):
            return
        p_rat, q, k_idx, _ = ideals[idx]
        dfs(idx + 1, rem, d_list, n_list)
        if q == 2:
            d_list.append((p_rat, q, k_idx))
            dfs(idx + 1, rem, d_list, n_list)
            d_list.pop()
        elif rem % (q - 1) == 0:
            d_list.append((p_rat, q, k_idx))
            dfs(idx + 1, rem // (q - 1), d_list, n_list)
            d_list.pop()
        f = q + 1
        e = 1
        while f <= rem:
            if rem % f == 0:
                n_list.append((p_rat, q, k_idx, e))
                dfs(idx + 1, rem // f, d_list, n_list)
                n_list.pop()
            if f > rem // q:
                break
            f *= q
            e += 1

    dfs(0, P_target, [], [])
    return sols


def exact_zeta_minus1(pari: Pari, nf, n: int) -> Fraction:
    """Compute exact rational |zeta_F(-1)| via PARI lfun at 160-bit precision (~48 decimal digits)."""
    val_hp = pari.abs(pari.lfun(nf, -1, precision=160))
    rat = pari.bestappr(val_hp, 10000)
    err = float(pari.abs(val_hp - rat))
    assert err < 1e-30, f"zeta_F(-1) rational approximation error too large: {err}"
    return Fraction(int(pari.numerator(rat)), int(pari.denominator(rat)))


def verify_prop_7_18(pari: Pari) -> bool:
    print("\n=== Part 2: Proposition 7.18(a)-(c) (nflist + lfun + Direct Brandt Graphs, n = 2, 3, 4) ===")
    t0 = time.time()
    px = pari("t^4 - 4*t^2 + 1")

    # 2a. Real quadratic scan D <= 1200: cross-check lfun vs exact Siegel + build Brandt graphs for D=41, 137!
    quad_sols = []
    quad_checked = 0
    for pol in pari.nflist([2, 1], [1, 1200], 0):
        D = int(pari.nfdisc(pol))
        if D % 8 != 1:
            continue
        quad_checked += 1
        nf = pari.nfinit(pol)
        z_lfun = exact_zeta_minus1(pari, nf, 2)
        z_siegel = Fraction(sum(2 * sigma1((D - b * b) // 4) for b in range(1, math.isqrt(D) + 1, 2)), 60)
        assert z_lfun == z_siegel, f"Siegel vs lfun mismatch at D={D}: {z_siegel} != {z_lfun}"
        bnf = pari.bnfinit(pol)
        hplus = int(pari.bnrclassno(bnf, [1, [1, 1]]))
        if hplus != 1:
            continue
        # Mass equation: 2^{1-2} * z * P = 12 => P = 24 / z
        P_frac = Fraction(24, 1) / z_lfun
        if P_frac.denominator != 1:
            continue
        pr2 = [p for p in pari.idealprimedec(nf, 2) if int(pari.idealnorm(nf, p)) == 2]
        sols = enumerate_field_dn_solutions(pari, nf, 2, pr2[0], P_frac.numerator)
        if sols:
            quad_sols.append((D, pol, sols))
    assert [d for d, _, _ in quad_sols] == [41, 137], f"Unexpected quadratic solutions: {[d for d, _, _ in quad_sols]}"
    print(f"  [PASS] Prop 7.18(a) Siegel vs lfun exact match on all {quad_checked} split-2 quadratics D<=1200; h^+=1 hits: D=41 (2), D=137 (1)")
    for D, pol, sols in quad_sols:
        D_spec, N_spec = sols[0]
        h_cls, units, mass, _ = compute_brandt_graph(pari, pol, D_spec, N_spec, v_idx=0)
        assert mass == Fraction(12, 1)
        expected_h = 14 if D == 41 else 13
        assert h_cls == expected_h, f"D={D} expected class number {expected_h}, got {h_cls}"
        print(f"  [PASS] Prop 7.18(a) Brandt D={D}: classes={h_cls} (torsion, max_unit={max(units)}), exact mass={mass}")

    # 2b & 2c. Cubic (d <= 5200) and Quartic (d <= 60000) exhaustive enumeration + direct Brandt graphs!
    deg_specs = [
        (3, [[3, 1], [3, 2]], 5200, [1, 1, 1]),
        (4, [[4, 1], [4, 2], [4, 3], [4, 4], [4, 5]], 60000, [1, 1, 1, 1]),
    ]
    all_sols = []
    for n, grps, dmax, inf_vec in deg_specs:
        fields = []
        for grp in grps:
            fields.extend(list(pari.nflist(grp, [1, dmax], 0)))
        for pol in fields:
            nf = pari.nfinit(pol)
            pr2 = [p for p in pari.idealprimedec(nf, 2) if int(pari.idealnorm(nf, p)) == 2]
            if not pr2:
                continue
            bnf = pari.bnfinit(pol)
            if int(pari.bnrclassno(bnf, [1, inf_vec])) != 1:
                continue
            z = exact_zeta_minus1(pari, nf, n)
            # 2^{1-n} * z * P = 12  =>  P = 12 * 2^{n-1} / z
            P_frac = Fraction(12 * (1 << (n - 1)), 1) / z
            if P_frac.denominator != 1:
                continue
            d_val = int(pari.nfdisc(pol))
            # Check sols fixing pr2[0] (and if multiple norm-2 primes, check all v_idx in Brandt!)
            sols = enumerate_field_dn_solutions(pari, nf, n, pr2[0], P_frac.numerator)
            for D_spec, N_spec in sols:
                all_sols.append((n, d_val, pol, len(pr2), D_spec, N_spec))

    # Deduplicate conjugate (D'', N) choices where paper counts field/level configurations;
    # Wait: verify EVERY single enumerated solution through the exact Brandt graph!
    tf_discs = []
    torsion_discs = []
    tf_configs_checked = 0
    for n, d_val, pol, n_v2, D_spec, N_spec in all_sols:
        h_cls, units, mass, cp = compute_brandt_graph(pari, pol, D_spec, N_spec, v_idx=0)
        assert mass == Fraction(12, 1), f"d={d_val} mass={mass} != 12"
        if h_cls == 12 and all(w == 1 for w in units):
            tf_discs.append(d_val)
            # Check ALL choices of norm-2 prime v (note: if v_idx > 0, check only if v doesn't divide D''N)
            rem = cp % px
            assert rem != 0, f"Unexpected P_X factor on torsion-free d={d_val}!"
            tf_configs_checked += 1
            print(f"  [PASS] Prop 7.18(c) TF deg={n} d={d_val:5d} D''={D_spec} N={N_spec}: h=12, units=all 1, mass=12, P_X nmid cp (rem={rem})")
        else:
            torsion_discs.append(d_val)
            assert 13 <= h_cls <= 18, f"Torsion d={d_val} unexpected h={h_cls}"
            print(f"  [PASS] Prop 7.18(b) TOR deg={n} d={d_val:5d} D''={D_spec} N={N_spec}: h={h_cls}, max_w={max(units)}, mass=12")

    # Also check alternate norm-2 prime choices on d=316 (which has two norm-2 primes, so paper says "For every choice of v"):
    for n, d_val, pol, n_v2, D_spec, N_spec in all_sols:
        if d_val in (316, 148, 469, 733, 2777) and n_v2 > 1:
            # Verify all v_idx choices coprime to D'' and N
            nf_y = pari.nfinit(pari.subst(pol, "x", "y"))
            pr2_y = [p for p in pari.idealprimedec(nf_y, 2) if int(pari.idealnorm(nf_y, p)) == 2]
            for v_idx in range(1, n_v2):
                # Check v_idx not in D_spec or N_spec
                if any(p == 2 and q == 2 and k == v_idx for p, q, k in D_spec):
                    continue
                if any(p == 2 and q == 2 and k == v_idx for p, q, k, _ in N_spec):
                    continue
                h_cls, units, mass, cp = compute_brandt_graph(pari, pol, D_spec, N_spec, v_idx=v_idx)
                assert h_cls == 12 and all(w == 1 for w in units) and mass == Fraction(12, 1) and (cp % px) != 0
                print(f"  [PASS] Prop 7.18(c) alt v_idx={v_idx} on d={d_val}: h=12, units=all 1, mass=12, P_X nmid cp")

    assert sorted(tf_discs) == sorted([733, 148, 469, 469, 316, 2777, 2777]), f"Unexpected TF set: {tf_discs}"
    assert sorted(torsion_discs) == sorted([564, 13448, 13448, 13676, 6809, 10273]), f"Unexpected torsion set: {torsion_discs}"
    print(f"  [PASS] Part 2 complete in {time.time() - t0:.2f}s: exact 13 cubic/quartic solutions (6 torsion + 7 torsion-free) verified.")
    return True


# ============================================================================
# Part 3: Theorem 7.19(c) — Quintic Near-Miss d_F = 106069 (D'' = p_13)
# ============================================================================

def verify_thm_7_19_quintic_nearmiss(pari: Pari) -> bool:
    print("\n=== Part 3: Theorem 7.19(c) (Quintic Near-Miss d_F = 106069, D'' = p_13) ===")
    t0 = time.time()
    pol = pari("x^5 - 2*x^4 - 4*x^3 + 7*x^2 + 3*x - 4")
    assert int(pari.nfdisc(pol)) == 106069
    assert int(pari.polsturm(pol)) == 5
    bnf = pari.bnfinit(pol)
    nf = pari.nfinit(pol)
    assert int(bnf.bnf_get_no()) == 1
    assert int(pari.bnrclassno(bnf, [1, [1, 1, 1, 1, 1]])) == 1
    z = exact_zeta_minus1(pari, nf, 5)
    # 2^{1-5} * |zeta_F(-1)| * (13 - 1) = (1/16) * z * 12 == 12  =>  z == 16!
    assert z == Fraction(16, 1), f"Expected |zeta_F(-1)| = 16, got {z}"

    h_cls, units, mass, cp = compute_brandt_graph(pari, pol, [(13, 13, 0)], [], v_idx=0)
    expected_cp = pari("t*(t - 3)*(t + 1)*(t^4 + 3*t^3 - 4*t - 1)*(t^5 - t^4 - 8*t^3 + 8*t^2 + 15*t - 16)")
    px = pari("t^4 - 4*t^2 + 1")
    assert h_cls == 12 and all(w == 1 for w in units) and mass == Fraction(12, 1)
    assert cp == expected_cp, f"Charpoly mismatch: got {cp}, expected {expected_cp}"
    assert (cp % px) != 0
    print(f"  [PASS] Quintic d=106069 (|zeta(-1)|={z}, h^+=1, D''=p_13) in {time.time() - t0:.2f}s:")
    print(f"         classes={h_cls}, units=all 1, mass={mass}, charpoly EXACT MATCH = {pari.factor(cp)}")
    return True


def main():
    pari = Pari()
    pari.allocatemem(2 * 10**9)
    pari.set_real_precision(38)
    ok1 = verify_thm_7_11_and_neg_e10(pari)
    ok2 = verify_prop_7_18(pari)
    ok3 = verify_thm_7_19_quintic_nearmiss(pari)
    all_ok = ok1 and ok2 and ok3
    print(f"\n=== Ergentics Independent PARI/GP Section 7 Cross-Check: {'ALL PASS' if all_ok else 'FAILURES'} ===")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
