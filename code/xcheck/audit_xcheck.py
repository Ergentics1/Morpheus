"""Audit of the [X] cross-contributions (Ergentics' program) by Grok Bot.
Recomputes everything from scratch (no cached JSON is read). Run: python audit_xcheck.py"""
import math, json, sys
import sympy as sp
import held_xcheck as H
import cumulant_xcheck as Cx

checks = []
def ok(name, cond, info=''):
    checks.append((name, bool(cond), str(info))); print(('PASS' if cond else 'FAIL'), name, info, flush=True)

# --- held notes ----------------------------------------------------------------------------
ok('Thm A: common link edges of two notes <= 2 (all chord classes, N<=30)', H.theorem_A(30) <= 2)
found, unexp = H.theorem_B(24, 24)
ok('Thm B: every one-voice collision lies in the family 8|N, {0,N/8,N/2}, N/4 in S (all S, N<=24)', not unexp, len(found))
found72, unexp72 = H.theorem_B(72, 0)
ok('Thm B: with maximal step sets, collisions at exactly N=8,16,...,72 (N<=72)',
   not unexp72 and sorted({f[0] for f in found72}) == list(range(8, 73, 8)), len(found72))
ok('Cor B.1: no collision for halving-closed S', not H.corB1_check(found))
n11 = H.neg_m11()
ok('NEG-M11: N=8, S={2}, {0,1,4}: both 4-cycles valid and non-backtracking', n11['tuneA'] and n11['tuneB'])
ok('NEG-M11: same cyclic tune (3,5,7,1)', n11['tuneA'] == n11['tuneB'] and sorted(n11['tuneA']) == [1, 3, 5, 7])

# --- higher cumulants ------------------------------------------------------------------------
ser = {k: Cx.perron_series(f) for k, f in Cx.AXES.items()}
for k in ser:
    ok(f'Thm C: kappa4/kappa2^2 = -17/2 per step along {k}', sp.Rational(ser[k]['k4_over_k2sq']) == sp.Rational(-17, 2))
K = {k: sp.Rational(ser[k]['k2']) for k in ser}
A_, C_ = K['W=-u'], K['v']; B_ = (K['u+v'] - A_ - C_) / 2
coef = {'W=-u': (-1, 0), 'v': (0, 1), '4u+3v': (4, 3), 'u+v': (1, 1), '2u+v': (2, 1), 'u+2v': (1, 2)}
ip = lambda x, y: A_*x[0]*y[0] + B_*(x[0]*y[1] + x[1]*y[0]) + C_*x[1]*y[1]
for k, c in coef.items():
    cosA = ip(c, coef['4u+3v']) / sp.sqrt(ip(c, c) * ip(coef['4u+3v'], coef['4u+3v']))
    c6 = sp.chebyshevt(6, cosA)          # cos(6 alpha) as a polynomial in cos(alpha), exact
    ok(f'Thm C: kappa6/kappa2^3 = (1470+cos 6a)/4 along {k}', sp.simplify(sp.Rational(ser[k]['k6_over_k2cu']) - (1470 + c6) / 4) == 0)
w = ser['W=-u']
ok('Thm C: W rates 1/24, -17/1152, 1469/55296', (w['k2'], w['k4'], w['k6']) == ('1/24', '-17/1152', '1469/55296'))
ok('odd cumulants vanish on all six axes', all(set(ser[k]['odd']) == {'0'} for k in ser))
p = sp.Symbol('p'); lam = sp.sqrt(5 + 4*sp.cos(p/4)); Lw = sp.series(sp.log((lam + sp.sqrt(lam**2 - 8))/4), p, 0, 9).removeO()
kw = [sp.nsimplify(Lw.coeff(p, j) * (-1)**(j//2) * sp.factorial(j)) for j in (2, 4, 6, 8)]
ok('Prop (all cumulants of W): closed form reproduces the series; kappa8/m = -887099/7962624',
   kw == [sp.Rational(1, 24), sp.Rational(-17, 1152), sp.Rational(1469, 55296), sp.Rational(-887099, 7962624)], kw)

# --- exact m=40 benchmarks -------------------------------------------------------------------
def pi_trace(m):
    """prime count from tr B^m of the 72x72 Hashimoto matrix (exact integers), Moebius inversion."""
    n = 72; idx = {(i, j): k for k, (i, j, _) in enumerate(Cx.E)}
    B = sp.zeros(n, n)
    for k, (i, j, _) in enumerate(Cx.E):
        for (jj, l, _) in Cx.E:
            if jj == j and l != i: B[k, idx[(j, l)]] = 1
    tr = {}; M = sp.eye(n)
    for d in range(1, m + 1):
        M = M * B; tr[d] = M.trace()
    return sum(sp.mobius(m // d) * tr[d] for d in sp.divisors(m)) // m, tr
pi40, tr = pi_trace(40)
X = {'W=-u': -8.49517437528062, 'v': -8.489783268833136, '4u+3v': -8.490888952147122}
for k in X:
    dist = {int(a): int(b) for a, b in Cx.prime_distribution(Cx.AXES[k], 40).items()}
    n, mean, m2, k4, k6 = Cx.cumulants(dist)
    ok(f'm=40 {k}: total primes = 54,975,717,792 = pi(40) from tr B^m', n == pi40 == 54975717792)
    ok(f'm=40 {k}: m*kappa_ex matches the [X] record', abs(float(40*k4/m2**2) - X[k]) < 1e-9, float(40*k4/m2**2))
rooted = sum(m * (sum(sp.mobius(m // d) * tr[d] for d in sp.divisors(m)) // m) for m in range(6, 17))
ok('NEG-E8: rooted primes of length <= 16 total 174,864 (131,136 of length 16)', rooted == 174864, rooted)

# --- Edgeworth calibration -------------------------------------------------------------------
import edgeworth_xcheck as Ew
xc = Ew.out['x_convention']
for k in ('C-2', "C-2'", "C-2''"):
    ok(f'{k}: TV and JSD reproduce the [X] record', abs(xc[k]['TV']/Ew.target[k][0] - 1) < 1e-9 and abs(xc[k]['JSD']/Ew.target[k][1] - 1) < 1e-9)
ok('Edgeworth ladder decreases: TV(C-2) > TV(C-2\') > TV(C-2\'\')', xc['C-2']['TV'] > xc["C-2'"]['TV'] > xc["C-2''"]['TV'])

npass = sum(c[1] for c in checks)
print(f'\n{npass}/{len(checks)} checks passed')
json.dump([dict(name=a, passed=b, info=c) for a, b, c in checks], open('audit_xcheck_report.json', 'w'), indent=1)
sys.exit(0 if npass == len(checks) else 1)
