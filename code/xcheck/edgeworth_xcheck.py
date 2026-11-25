"""Grok Bot cross-check of the [X] m=40 Edgeworth calibration (C-2, C-2', C-2'') for W=-u,
and of the angular law (1470+cos 6a)/4 on arbitrary axes."""
import json, math
import sympy as sp
from cumulant_xcheck import AXES, prime_distribution, perron_series
M = 40
dist = {int(k): int(v) for k, v in prime_distribution(AXES["W=-u"], M).items()}
n = sum(dist.values()); ws = sorted(dist); p = [dist[w] / n for w in ws]
k2, k4, k6 = M / 24, -17 * M / 1152, 1469 * M / 55296   # leading-order cumulant rates
s = math.sqrt(k2)
def He(k, z): return [1, z, z*z-1, z**3-3*z, z**4-6*z*z+3, z**5-10*z**3+15*z, z**6-15*z**4+45*z*z-15][k]
def He8(z): return z**8-28*z**6+210*z**4-420*z*z+105
def q(w, order):
    z = w / s; g = math.exp(-z*z/2) / math.sqrt(2*math.pi) / s
    l4, l6 = k4 / k2**2, k6 / k2**3
    corr = 1
    if order >= 4: corr += l4 / 24 * He(4, z)
    if order >= 6: corr += l6 / 720 * He(6, z) + l4**2 / 1152 * He8(z)
    return g * corr
def metrics(order, clip=True, normalise=True):
    Q = [q(w, order) for w in ws]
    if clip: Q = [max(0.0, x) for x in Q]
    if normalise: t = sum(Q); Q = [x / t for x in Q]
    tv = 0.5 * sum(abs(a - b) for a, b in zip(p, Q))
    mix = [(a + b) / 2 for a, b in zip(p, Q)]
    js = 0.5 * sum(a * math.log(a / c) for a, c in zip(p, mix) if a > 0) + 0.5 * sum(b * math.log(b / c) for b, c in zip(Q, mix) if b > 0)
    return tv, js
out = {'support': [ws[0], ws[-1]]}
for o, name in ((2, 'C-2'), (4, "C-2'"), (6, "C-2''")):
    for norm in (True, False):
        tv, js = metrics(o, normalise=norm)
        out[f'{name} norm={norm}'] = dict(TV=tv, JSD=js)
# angular law: Q-metric angle of each axis relative to W=-u
ser = {k: perron_series(f) for k, f in AXES.items()}
# kappa2 is a quadratic form in the functional coefficients (a,b) of a*u+b*v: fit from three axes
K = {k: sp.Rational(ser[k]['k2']) for k in ser}
# k2(a,b) = A a^2 + 2B ab + C b^2 : u -> (1,0) [W=-u same], v -> (0,1), u+v -> (1,1)
A, C = K['W=-u'], K['v']; B = (K['u+v'] - A - C) / 2
coef = {'W=-u': (-1, 0), 'v': (0, 1), '4u+3v': (4, 3), 'u+v': (1, 1), '2u+v': (2, 1), 'u+2v': (1, 2)}
def ip(x, y): return A*x[0]*y[0] + B*(x[0]*y[1] + x[1]*y[0]) + C*x[1]*y[1]
ang = {}
for k, c in coef.items():
    cosang = float(ip(c, coef['W=-u']) / sp.sqrt(ip(c, c) * ip(coef['W=-u'], coef['W=-u'])))
    a = math.acos(max(-1, min(1, cosang)))
    pred = (1470 + math.cos(6 * a + math.pi)) / 4   # W=-u is an armchair axis (cos 6a = -1)
    ang[k] = dict(angle_deg=math.degrees(a), predicted=pred, exact=float(sp.Rational(ser[k]['k6_over_k2cu'])))
out['angular_law'] = ang
out['angular_law_max_err'] = max(abs(v['predicted'] - v['exact']) for v in ang.values())
json.dump(out, open('edgeworth_xcheck.json', 'w'), indent=1, default=float)
print("angular_law_max_err", out["angular_law_max_err"])

# --- [X] convention: q normalised over w in [-24,24], mass outside the 17-point window [-8,8]
#     counted in TV and JSD; same leading-order Edgeworth coefficients. Reproduces C-2, C-2', C-2''.
def x_convention(order):
    sig = math.sqrt(M / 24)
    c4, c6, c8 = -17 / (48 * M), 1469 / (2880 * M * M), 289 / (4608 * M * M)
    def wt(w):
        z2 = (w / sig) ** 2; base = math.exp(-z2 / 2)
        if order == 0: return base
        poly = 1 + c4 * (z2*z2 - 6*z2 + 3)
        if order >= 6: poly += c6 * (z2**3 - 15*z2*z2 + 45*z2 - 15) + c8 * (z2**4 - 28*z2**3 + 210*z2*z2 - 420*z2 + 105)
        return max(0.0, base * poly)
    Z = sum(wt(w) for w in range(-24, 25))
    win = range(-8, 9); P = [dist.get(w, 0) / n for w in win]; Q = [wt(w) / Z for w in win]
    qout = max(0.0, 1 - sum(Q))
    tv = 0.5 * (qout + sum(abs(a - b) for a, b in zip(P, Q)))
    js = 0.5 * math.log(2) * qout
    for a, b in zip(P, Q):
        mid = (a + b) / 2
        if a > 0: js += 0.5 * a * math.log(a / mid)
        if b > 0: js += 0.5 * b * math.log(b / mid)
    return tv, js
xc = {name: dict(zip(('TV', 'JSD'), x_convention(o))) for o, name in ((0, 'C-2'), (4, "C-2'"), (6, "C-2''"))}
target = {'C-2': (1.086473858410425e-2, 3.419013498562255e-4), "C-2'": (9.951305947214187e-4, 9.524112673283263e-6),
          "C-2''": (1.4427865711084327e-4, 4.76318040404968e-6)}
xc['max_rel_err_vs_X'] = max(abs(xc[k]['TV'] / target[k][0] - 1) for k in target)
xc['max_rel_err_vs_X_JSD'] = max(abs(xc[k]['JSD'] / target[k][1] - 1) for k in target)
out['x_convention'] = xc
json.dump(out, open('edgeworth_xcheck.json', 'w'), indent=1, default=float)
print(json.dumps(xc, indent=1, default=float))
