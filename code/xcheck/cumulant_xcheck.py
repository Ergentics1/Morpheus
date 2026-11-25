"""Grok Bot cross-check of [X] Theorem C (higher winding cumulants) and the m=40 benchmarks.
(1) exact Rayleigh-Schroedinger series of the Perron eigenvalue of the twisted adjacency matrix of X
    (24x24, 2D homology voltages (u,v) per directed edge, built from scratch here), then
    log(lambda_+/2) with lambda_+ = (mu + sqrt(mu^2-8))/2 (Ihara), as an exact rational series;
(2) exact distribution of W=-u, v, 4u+3v over prime cadences of length 40 by transfer DP + Moebius."""
import itertools, json, sys
from fractions import Fraction as F
import sympy as sp
sys.path.insert(0, '../deep')
from common import V, IX, OPS, tri

# --- lattice model: pc(a,b)=7a+4b, period lattice <(4,-4),(0,3)>, voltages (u,v) -----------------
def pc(p): return (7*p[0] + 4*p[1]) % 12
def lat(c):
    r, q = c; p = ((7*r) % 12, 0)
    return frozenset({p, (p[0]+1, p[1]), (p[0], p[1]+1)}) if q == 'M' else frozenset({p, (p[0]+1, p[1]), (p[0]+1, p[1]-1)})
def flip(t, o):
    s = list(t)
    for u, v in itertools.combinations(s, 2):
        d = (v[0]-u[0], v[1]-u[1])
        k = {(1,0):'P',(-1,0):'P',(0,1):'R',(0,-1):'R',(1,-1):'L',(-1,1):'L'}.get(d)
        if k == o:
            w = [x for x in s if x != u and x != v][0]
            return frozenset({u, v, (u[0]+v[0]-w[0], u[1]+v[1]-w[1])})
def voltage(c, o):
    d = OPS[o](c); t1 = flip(lat(c), o); t0 = lat(d)
    a = sorted(t0); b = sorted(t1)
    dv = (b[0][0]-a[0][0], b[0][1]-a[0][1])
    assert all((y[0]-x[0], y[1]-x[1]) == dv for x, y in zip(a, b))
    assert {pc(p) for p in t1} == tri(d)
    A, B = dv; assert A % 4 == 0; u = A // 4; w = B + 4*u; assert w % 3 == 0
    return IX[c], IX[d], (u, w // 3)
E = [voltage(c, o) for c in V for o in 'PLR']
# Hermitian check: reverse edge carries the negative voltage
vol = {(i, j): x for i, j, x in E}
assert all(vol[(j, i)] == (-x[0], -x[1]) for (i, j), x in vol.items())

def perron_series(f, order=6):
    """f: edge voltage -> integer weight; series of top eigenvalue of A(t)=sum exp(i t f) in t."""
    n = 24; eps = sp.Symbol('e')  # eps = i t
    Ak = [sp.zeros(n, n) for _ in range(order + 1)]
    for i, j, x in E:
        w = f(x)
        for k in range(order + 1): Ak[k][j, i] += sp.Rational(w**k, sp.factorial(k))
    v0 = sp.Matrix([1]*n) / n  # left/right eigvec (A0 symmetric), normalise <1,v>=1
    one = sp.Matrix([1]*n)
    M = Ak[0] - 3*sp.eye(n)
    # solve on complement of ones via augmented system
    Maug = M.row_join(one).col_join(one.T.row_join(sp.zeros(1, 1)))
    Minv = Maug.inv()
    vs = [sp.Matrix([1]*n)]; mus = [sp.Integer(3)]
    for m_ in range(1, order + 1):
        rhs = sp.zeros(n, 1)
        for k in range(1, m_ + 1): rhs -= Ak[k] * vs[m_ - k]
        mu = (one.T * (-rhs))[0] / n
        for k in range(1, m_): mu -= 0  # <1,v_j>=0 for j>0
        for k in range(1, m_): rhs += mus[k] * vs[m_ - k]
        rhs += mu * vs[0]
        sol = Minv * rhs.col_join(sp.zeros(1, 1))
        vs.append(sol[:n, 0]); mus.append(sp.nsimplify(mu))
    t = sp.Symbol('t')
    mu_t = sum(mus[k] * (sp.I*t)**k for k in range(order + 1))
    lam = (mu_t + sp.sqrt(mu_t**2 - 8)) / 2
    ser = sp.series(sp.log(lam / 2), t, 0, order + 1).removeO()
    ser = sp.expand(sp.simplify(ser))
    c2 = sp.nsimplify(ser.coeff(t, 2)); c4 = sp.nsimplify(ser.coeff(t, 4)); c6 = sp.nsimplify(ser.coeff(t, 6))
    k2, k4, k6 = -2*c2, 24*c4, -720*c6
    return dict(k2=str(k2), k4=str(k4), k6=str(k6), k4_over_k2sq=str(sp.nsimplify(k4/k2**2)),
                k6_over_k2cu=str(sp.nsimplify(k6/k2**3)), odd=[str(ser.coeff(t, k)) for k in (1, 3, 5)])

AXES = {'W=-u': lambda x: -x[0], 'v': lambda x: x[1], '4u+3v': lambda x: 4*x[0] + 3*x[1],
        'u+v': lambda x: x[0] + x[1], '2u+v': lambda x: 2*x[0] + x[1], 'u+2v': lambda x: x[0] + 2*x[1]}

def prime_distribution(f, m):
    """exact counts of prime cadences (unrooted) of length m by value of the functional f."""
    from sympy import mobius, divisors
    out = {}
    def closed(L):
        # closed non-backtracking walks of length L by total voltage, via 72x72 edge transfer DP
        idx = {(i, j): k for k, (i, j, _) in enumerate(E)}
        succ = [[idx[(j, l)] for (jj, l, _) in E if jj == j and l != i] for (i, j, _) in E]
        tot = {}
        for s in range(72):
            cur = {(s, f(E[s][2])): 1}
            for _ in range(L - 1):
                nxt = {}
                for (e, w), c in cur.items():
                    for e2 in succ[e]:
                        key = (e2, w + f(E[e2][2])); nxt[key] = nxt.get(key, 0) + c
                cur = nxt
            for (e, w), c in cur.items():
                if s in succ[e]: tot[w] = tot.get(w, 0) + c
        return tot  # rooted at an edge = rooted at (vertex, first move)
    cache = {}
    res = {}
    for d in divisors(m):
        mu = mobius(d)
        if mu == 0: continue
        L = m // d
        if L not in cache: cache[L] = closed(L)
        for w, c in cache[L].items():
            res[w * d] = res.get(w * d, 0) + mu * c
    assert all(c % m == 0 for c in res.values())
    return {w: c // m for w, c in res.items() if c}

def cumulants(dist):
    n = sum(dist.values()); mean = F(sum(w*c for w, c in dist.items()), n)
    mom = lambda k: F(sum((w - mean)**k * c for w, c in dist.items()), n)
    m2, m4, m6, m3 = mom(2), mom(4), mom(6), mom(3)
    k4 = m4 - 3*m2**2; k6 = m6 - 15*m4*m2 - 10*m3**2 + 30*m2**3
    return n, mean, m2, k4, k6

if __name__ == '__main__':
    out = {'series': {}, 'm40': {}}
    for name, f in AXES.items():
        out['series'][name] = perron_series(f)
        print(name, out['series'][name], flush=True)
    M = 40
    for name in ('W=-u', 'v', '4u+3v'):
        dist = prime_distribution(AXES[name], M)
        n, mean, m2, k4, k6 = cumulants(dist)
        out['m40'][name] = dict(total_primes=n, mean=float(mean), var_over_m=float(m2 / M),
                               m_kappa_ex=float(M * k4 / m2**2), m2_k6_over_k2cu=float(M*M*k6/m2**3))
        print(name, out['m40'][name], flush=True)
    json.dump(out, open("cumulant_xcheck.json", "w"), indent=1, default=str)
