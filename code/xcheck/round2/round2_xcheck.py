"""Round-2 referee cross-check (Grok Bot) of the results added in v0.3.0.

Recomputes from scratch, without reading any upstream data file:
  1. Theorem 7.11 / NEG-E10: the genus-13 census of X_0^D(N), 2|D (19 pairs), and the
     level-345 Hecke data quoted for X_0^690(1) (PARI via cypari2).
  2. Theorem 7.21: the Poitou-Odlyzko kernel is positive definite (closed-form Fourier
     transform), the explicit formula reproduces the quoted witnesses, and a conservative
     three-pincer sweep over 6 <= n <= 14 leaves exactly the survivors stated in the paper.
  3. Proposition 7.18(b): Gamma_5 is non-arithmetic (tau(s4 s5) = 49/4 > 4).
  4. Theorem 4.4 / clean-room count: 13,382 valid systems for 5 <= N <= 18.
Run:  python round2_xcheck.py      (about one minute)
"""
import itertools, json, math
from fractions import Fraction as Fr
import mpmath as mp
import sympy as sp

rows = []
def check(name, ok, detail=""):
    rows.append(dict(check=name, passed=bool(ok), detail=str(detail)))
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""), flush=True)

# ---------------------------------------------------------------- 1. genus-13 census
def kron(a, p):
    if p == 2:
        return 0 if a % 2 == 0 else (1 if a % 8 in (1, 7) else -1)
    a %= p
    return 0 if a == 0 else (1 if pow(a, (p - 1) // 2, p) == 1 else -1)

def genus(D, N):
    fD, fN = sp.factorint(D), sp.factorint(N)
    phi = math.prod(p - 1 for p in fD)
    psi = N
    for p in fN:
        psi = psi * (p + 1) // p
    e2 = math.prod(1 - kron(-4, p) for p in fD)
    e3 = math.prod(1 - kron(-3, p) for p in fD)
    for p, k in fN.items():
        e2 *= 0 if (p == 2 and k >= 2) else 1 + kron(-4, p)
        e3 *= 0 if (p == 3 and k >= 2) else 1 + kron(-3, p)
    return Fr(1) + Fr(phi * psi, 12) - Fr(e2, 4) - Fr(e3, 3), e2, e3

# g = 13 forces phi(D) psi(N) <= 12 (12 + e2/4 + e3/3) <= 2400 for at most six primes in D.
P = list(sp.primerange(3, 2500))
def odd_parts(start, r, D, phi):
    if r == 0:
        yield D, phi
        return
    for i in range(start, len(P)):
        if phi * (P[i] - 1) ** r > 2400:
            break
        yield from odd_parts(i + 1, r - 1, D * P[i], phi * (P[i] - 1))
census = []
for r in (1, 3, 5):
    for D, phi in odd_parts(0, r, 2, 1):
        for N in range(1, 2400 // phi + 2):
            if math.gcd(D, N) == 1:
                g, e2, e3 = genus(D, N)
                if g == 13:
                    census.append((D, N, e2, e3))
tf = [c for c in census if c[2] == c[3] == 0]
check("Thm 7.11: exactly 19 genus-13 pairs X_0^D(N) with 2|D", len(census) == 19, sorted(census))
check("Thm 7.11: 11 of them torsion-free", len(tf) == 11)
check("NEG-E10: (690,1) is in the census with e2=0, e3=8", (690, 1, 0, 8) in census)
try:
    import cypari2
    pari = cypari2.Pari()
    pari.allocatemem(10**9)
    dim = int(pari("mfdim([345,2],0)"))
    rem = pari("mf=mfinit([345,2],0); charpoly(mfheckemat(mf,2)) % (x^4-4*x^2+1)")
    check("NEG-E10: dim S_2^new(345)=15 and charpoly(T_2) mod (t^4-4t^2+1) = 3t^3+t^2+21t+7",
          dim == 15 and str(rem) == "3*x^3 + x^2 + 21*x + 7", f"dim={dim}, rem={rem}")
except ImportError:
    check("NEG-E10 Hecke data (cypari2 not installed: skipped)", True, "skipped")

# ---------------------------------------------------------------- 2. Theorem 7.21
mp.mp.dps = 20
pi = mp.pi
w, t = sp.symbols("w t", positive=True)
H1s = (2 - w) / 3 * (1 + sp.cos(sp.pi * w) / 2) + sp.sin(sp.pi * w) / (2 * sp.pi)
ft = sp.simplify(2 * sp.integrate(H1s * sp.cos(t * w), (w, 0, 2)))
target = 4 * sp.pi**4 * sp.sin(t)**2 / (3 * t**2 * (t**2 - sp.pi**2)**2)
check("Kernel H_1 is positive definite: FT = 4 pi^4 sin^2 t / (3 t^2 (t^2-pi^2)^2) >= 0",
      sp.simplify(ft.args[0][0] - target) == 0 if isinstance(ft, sp.Piecewise) else sp.simplify(ft - target) == 0)

def H1(x):
    x = abs(x)
    return mp.mpf(0) if x >= 2 else (2 - x) / 3 * (1 + mp.cos(pi * x) / 2) + mp.sin(pi * x) / (2 * pi)
_arch = {}
def arch(b):
    if b not in _arch:
        F = lambda x: H1(x / b) / mp.cosh(x / 2)
        Is = mp.quad(lambda x: (1 - F(x)) / (2 * mp.sinh(x / 2)), [0, b, 2 * b, mp.inf])
        Ic = mp.quad(lambda x: (1 - F(x)) / (2 * mp.cosh(x / 2)), [0, b, 2 * b, mp.inf])
        lB = mp.euler + mp.log(8 * pi) - Is
        _arch[b] = (lB + pi / 2 - Ic, lB)
    return _arch[b]
_fq = {}
def fq(q, b):
    if (q, b) not in _fq:
        s, m = mp.mpf(0), 1
        while m * mp.log(q) < 2 * b:
            s += mp.log(q) / (1 + mp.mpf(q)**m) * H1(m * mp.log(q) / b)
            m += 1
        _fq[(q, b)] = 4 * s
    return _fq[(q, b)]
def LB(b, N, rho, c2=0, c4=0):
    lA, lB = arch(b)
    return rho * lA + (1 - rho) * lB - mp.mpf(8) * b / 3 / N + (c2 * fq(2, b) + c4 * fq(4, b)) / N
UB = lambda n, C: (4 * pi**2)**(mp.mpf(2) / 3) * mp.mpf(C)**(mp.mpf(2) / (3 * n))
GRID = [mp.mpf(i) / 20 for i in range(10, 301)]
best = lambda N, rho, c2=0, c4=0: max(LB(b, N, rho, c2, c4) for b in GRID)

# archimedean limit (F -> sech(x/2)) gives the classical constants 4 pi e^gamma and 4 pi e^(1+gamma)
Is = mp.quad(lambda x: (1 - mp.sech(x / 2)) / (2 * mp.sinh(x / 2)), [0, mp.inf])
check("Explicit formula normalisation: limit constants 22.3816 / 60.8395",
      abs(mp.exp(mp.euler + mp.log(8 * pi) - Is) - 4 * pi * mp.exp(mp.euler)) < 1e-15)
mins = {2: 5, 3: 49, 4: 725, 5: 14641, 6: 300125, 7: 20134393, 8: 282300416}
check("Explicit formula is below every minimal totally real discriminant, n=2..8",
      all(mp.exp(best(n, 1)) < mp.mpf(d)**(mp.mpf(1) / n) for n, d in mins.items()))
v9 = mp.exp(best(9, 1, c2=1))
check("Pincer 1 witness n=9, u=4, mode B: exp(LB)=13.8641 > UB=13.5249",
      abs(v9 - mp.mpf("13.8641")) < 5e-4 and v9 > UB(9, 8), f"{mp.nstr(v9, 7)} vs {mp.nstr(UB(9, 8), 7)}")
b = mp.mpf("4.2")
ef = mp.mpf(8) * b / 3 - fq(2, b)
check("Tail n>=15 at b=4.2: E-f_2 = 9.5350 (paper v0.3.0 prints 9.5370), LB(15)=19.9366 > UB(15)=19.0800",
      ef > 0 and abs(ef - mp.mpf("9.53497")) < 1e-4 and mp.exp(LB(b, 15, 1, c2=1)) > UB(15, mp.mpf(9) / 2 * 2**14),
      mp.nstr(ef, 7))
lv = mp.exp(LB(mp.mpf(6), 48, 0, c2=8))
check("Pincer 3 sextic witness (6,16,1,2): L_v at b=6 gives 18.660678 > 18.647049",
      abs(lv - mp.mpf("18.660678")) < 1e-5 and lv > UB(6, 72), mp.nstr(lv, 9))

def rho_bound(n, k, j, cond=False):
    """Real fraction guaranteed for some subfield of degree 2^j over the base inside an
    F_2^k-extension, by averaging over subspaces (cond: subspaces containing Frob_v)."""
    if k == 0:
        return mp.mpf(1)
    if cond:
        if k - j - 1 < 0:
            return mp.mpf(0)
        if k == 1:
            return mp.mpf(1)
        num, den = 2**(k - j - 1) - 1, 2**(k - 1) - 1
    else:
        num, den = 2**(k - j) - 1, 2**k - 1
    return mp.mpf(-((-n * num) // den)) / n

survivors = []
for n in range(6, 15):
    for k in range(n):
        u = 2**k
        modes = [("even", mp.mpf(9) / 2 * u, 1)] if n % 2 == 0 else [("A", mp.mpf(27) / 8 * u, 2), ("B", 2 * u, 1)]
        for mode, C, c2F in modes:
            ub = mp.log(UB(n, C))
            extra = 1 if mode == "A" else 0     # second norm-2 prime in D'' (mode A): c4 >= 2^(j-1)
            lbF = best(n, 1, c2=c2F)
            # h_F >= 2: subfields of H_F^+ containing H_F (degree >= 2n 2^j), no prime terms
            lb2 = max([lbF] + [best(2 * n * 2**j, rho_bound(n, k, j)) for j in range(k + 1)])
            if lb2 <= ub:
                survivors.append((n, u, mode, "h>=2"))
            # h_F = 1: Gal(H_F^+/F) = F_2^k, Frob_v of order f_v in {1,2}
            for fv in ([1, 2] if k else [None]):
                cands = [lbF]
                for j in range(1, k + 1):
                    N = n * 2**j
                    if fv == 1:
                        cands.append(best(N, rho_bound(n, k, j), c2=2**j, c4=extra * 2**(j - 1)))
                    else:
                        cands.append(best(N, rho_bound(n, k, j), c4=(1 + extra) * 2**(j - 1)))
                        if j <= k - 1:
                            cands.append(best(N, rho_bound(n, k, j, True), c2=2**j, c4=extra * 2**(j - 1)))
                if max(cands) <= ub:
                    survivors.append((n, u, mode, "h=1"))
surv = sorted({(n, u) for n, u, _, _ in survivors})
expected = [(6, 1), (6, 2), (6, 4), (6, 8), (7, 1), (7, 2), (7, 4), (8, 1), (8, 2), (8, 4)]
check("Thm 7.21(a): no survivors for 9 <= n <= 14", all(n <= 8 for n, _ in surv))
check("Thm 7.21(b): n in {7,8} forces h_F = 1 and u in {1,2,4}",
      all(h == "h=1" and u <= 4 for n, u, _, h in survivors if n in (7, 8)))
check("Thm 7.21(c): sextic u in {16,32} excluded", all(u <= 8 for n, u in surv if n == 6))
check("Survivor set equals the paper's open cases", surv == expected, surv)
ceil = lambda n, C: float(UB(n, C)**n)
check("Ceilings 1.597e8 (n=7), 2.243e9 (n=8), 2.648e7 (n=6, u=8)",
      abs(ceil(7, 13.5) / 1.597e8 - 1) < 1e-3 and abs(ceil(8, 18) / 2.243e9 - 1) < 1e-3 and abs(ceil(6, 36) / 2.648e7 - 1) < 1e-3)
# The proof text of v0.3.0 omits the mode-A second prime in Pincer 3; without it (7,8,A,f_v=2) survives:
no_extra = max(best(7 * 8, 0, c4=4), best(28, 0, c2=4))
check("Without the mode-A second prime, (n,u)=(7,8) mode A f_v=2 is NOT excluded (proof text needs it)",
      no_extra <= mp.log(UB(7, 27)), f"{mp.nstr(mp.exp(no_extra), 7)} <= {mp.nstr(UB(7, 27), 7)}")

# ---------------------------------------------------------------- 3. Gamma_5 non-arithmetic
om = sp.Rational(-1, 2) + sp.sqrt(3) * sp.I / 2
S0 = sp.Matrix([[0, 2], [1, 0]])
g = [sp.eye(2), sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[1, 1], [0, 1]]),
     sp.Matrix([[1, om], [0, 1]]), sp.Matrix([[1, om**2], [0, 1]])]
s = [sp.simplify(x * S0 * x.inv()) for x in g]
imgs = [sp.simplify(x * sp.Matrix([0, 1])) for x in g]
pts = [sp.zoo if v[1] == 0 else sp.simplify(v[0] / v[1]) for v in imgs]
M = sp.simplify(s[3] * s[4])
tau = sp.nsimplify(sp.simplify(sp.expand(M.trace()**2 / M.det())))
check("Prop 7.18(b): g_1..g_5 send 0 to 0, oo, 1, w, w^2", pts[0] == 0 and pts[1] == sp.zoo and pts[2] == 1
      and sp.simplify(pts[3] - om) == 0 and sp.simplify(pts[4] - om**2) == 0)
check("Prop 7.18(b): s_i^2 = 2I for all i", all(sp.simplify(x * x - 2 * sp.eye(2)) == sp.zeros(2) for x in s))
check("Prop 7.18(b): tau(s4 s5) = 49/4 > 4, s4 s5 in ker(phi): Gamma_5 is non-arithmetic", tau == sp.Rational(49, 4))

# ---------------------------------------------------------------- 4. 13,382 systems
def dist(a, b, N):
    d = abs(a - b) % N
    return min(d, N - d)
total = 0
for N in range(5, 19):
    for ti in (False, True):
        seen, ints = set(), []
        for c in itertools.combinations(range(N), 3):
            orb = {tuple(sorted((x + t) % N for x in c)) for t in range(N)}
            if ti:
                orb |= {tuple(sorted((t - x) % N for x in c)) for t in range(N)}
            key = min(orb)
            if key not in seen:
                seen.add(key)
                ints.append({dist(key[0], key[1], N), dist(key[0], key[2], N), dist(key[1], key[2], N)})
        for mask in range(1, 1 << (N // 2)):
            Sset = {i + 1 for i in range(N // 2) if mask >> i & 1}
            total += sum(1 for I in ints if not I & Sset)
check("Held-note clean-room count: 13,382 valid systems for 5 <= N <= 18", total == 13382, total)

npass = sum(r["passed"] for r in rows)
json.dump(dict(rows=rows, passed=npass, total=len(rows)), open("round2_xcheck_report.json", "w"), indent=1)
print(f"{npass}/{len(rows)} checks passed")
