"""Grok Bot cross-check of the [X] held-note claims (Theorem A, Theorem B, Cor. B.1, NEG-M11).
Independent brute force; does not import the [X] verifiers or read their data."""
import itertools, json
from collections import defaultdict

def chord_classes(N):
    seen, out = set(), []
    for x in range(1, N):
        for y in range(1, N - x):
            z = N - x - y
            base = (0, x, x + y)
            for ti in (False, True):
                ch = set()
                for t in range(N):
                    ch.add(frozenset((a + t) % N for a in base))
                    if ti: ch.add(frozenset((t - a) % N for a in base))
                key = frozenset(ch)
                if (key, ti) in seen: continue
                seen.add((key, ti)); out.append(dict(x=x, y=y, z=z, ti=ti, chords=key))
    return out

def link(chords, h):
    return {frozenset(c - {h}) for c in chords if h in c}

def theorem_A(Nmax):
    worst = 0
    for N in range(3, Nmax + 1):
        for c in chord_classes(N):
            L = {h: link(c['chords'], h) for h in range(N)}
            for h1, h2 in itertools.combinations(range(N), 2):
                worst = max(worst, len(L[h1] & L[h2]))
    return worst

def one_voice_collisions(N, c, S):
    """held pair Q, moving voice graph on completions of Q; collisions = two different held pairs
    whose completion sets contain a common closed non-backtracking walk (cycle) of length>=3 in the step graph."""
    pm = {s % N for s in S} | {(-s) % N for s in S}
    if any((u - w) % N in pm for ch in c['chords'] for u in ch for w in ch if u != w):
        return None  # not step-free
    comp = defaultdict(set)
    for ch in c['chords']:
        for u, w in itertools.combinations(sorted(ch), 2):
            comp[frozenset((u, w))].add(next(iter(ch - {u, w})))
    # a one-voice closed walk holding Q is a cycle in the step graph on comp[Q];
    # two held pairs collide iff comp[Q] & comp[Q'] carries a cycle.
    def has_cycle(Vs):
        Vs = set(Vs); adj = {v: [w for w in Vs if (w - v) % N in pm] for v in Vs}
        seen = set()
        for s in Vs:
            if s in seen: continue
            stack = [(s, None)]; par = {s: None}; seen.add(s)
            while stack:
                v, p = stack.pop()
                for w in adj[v]:
                    if w == p: continue
                    if w in par: return True
                    par[w] = v; seen.add(w); stack.append((w, v))
        return False
    pairs = [q for q in comp if len(comp[q]) >= 3]
    hits = []
    for q1, q2 in itertools.combinations(pairs, 2):
        if q1 & q2: continue  # sharing a note: two voices would differ, handled by Thm A/(a)
        if has_cycle(comp[q1] & comp[q2]): hits.append((sorted(q1), sorted(q2)))
    return hits

def theorem_B(Nmax, all_S_upto):
    unexpected, found = [], []
    for N in range(5, Nmax + 1):
        half = N // 2
        for c in chord_classes(N):
            gaps = {min(d, N - d) for d in (c['x'], c['y'], c['z'])}
            Smax = [d for d in range(1, half + 1) if d not in gaps]
            if N <= all_S_upto:
                Ss = [S for r in range(1, len(Smax) + 1) for S in itertools.combinations(Smax, r)]
            else:
                Ss = [tuple(Smax)]
            for S in Ss:
                h = one_voice_collisions(N, c, S)
                if not h: continue
                pred = (N % 8 == 0 and c['ti'] and sorted((c['x'], c['y'], c['z'])) in
                        (sorted((N//8, 3*N//8, N//2)),) and (N//4) in S)
                (found if pred else unexpected).append((N, c['x'], c['y'], c['ti'], S))
    return found, unexpected

def corB1_check(found):
    def half_closed(S): return all((d // 2) in S for d in S if d % 2 == 0)
    return [f for f in found if half_closed(set(f[4]))]

def neg_m11():
    N, S = 8, {2}
    ch = set()
    for t in range(N):
        for a in ((0, 1, 4),):
            ch.add(frozenset((x + t) % N for x in a)); ch.add(frozenset((t - x) % N for x in a))
    A = [frozenset(s) for s in ({0,3,4},{0,5,4},{0,7,4},{0,1,4})]
    B = [frozenset(s) for s in ({2,3,6},{2,5,6},{2,7,6},{2,1,6})]
    def ok(walk, held):
        tune = []
        for i in range(4):
            a, b = walk[i], walk[(i + 1) % 4]
            if a not in ch or b not in ch or len(a & b) != 2 or not held <= (a & b): return None
            out, inn = next(iter(a - b)), next(iter(b - a))
            if min((inn - out) % N, (out - inn) % N) not in S: return None
            tune.append(inn)
        nb = all(walk[i] != walk[(i + 2) % 4] for i in range(4))
        return tune if nb else None
    return dict(chords=len(ch), tuneA=ok(A, {0, 4}), tuneB=ok(B, {2, 6}))

if __name__ == '__main__':
    out = {}
    out['thmA_max_link_intersection_N<=40'] = theorem_A(40)
    found, unexp = theorem_B(72, 24)
    out['thmB_family_hits'] = len(found)
    out['thmB_family_Ns_Smax'] = sorted({f[0] for f in found})
    out['thmB_unexpected'] = unexp
    out['corB1_violations'] = corB1_check(found)
    out['neg_m11'] = neg_m11()
    out['checks'] = {
        'thmA': out['thmA_max_link_intersection_N<=40'] <= 2,
        'thmB': not unexp and len(found) > 0,
        'corB1': not out['corB1_violations'],
        'negM11': out['neg_m11']['tuneA'] is not None and out['neg_m11']['tuneA'] == out['neg_m11']['tuneB'],
    }
    json.dump(out, open('held_xcheck.json', 'w'), indent=1, default=str)
    print(json.dumps(out, default=str)[:3000])
