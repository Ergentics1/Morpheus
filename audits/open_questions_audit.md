# Audit: open questions round

**27/27 PASS**

| # | check | result | detail |
|---|---|---|---|
| 1 | word PLRLPRPL = +-[[-5,12],[12,-80]] (same element of PGL2), det 2^8, tau = tr^2/det = 7225/256 > 4 | PASS |  |
| 2 | tau(gamma^m) is rational and > 4 for m = 1..30 (eigenvalue ratio real, positive, not 1) | PASS |  |
| 3 | PLRLPRPL lies in K (even length, trivial image in the PLR group) | PASS |  |
| 4 | compact place: for 2000 random Hamilton quaternions 0 <= trd^2/nrd <= 4 (max 3.990906) | PASS |  |
| 5 | PLRLPRPL acts trivially on all 24 chords (so it lies in K) | PASS |  |
| 6 | edge-length lemma (order 2): at points fixed by z->-z away from the fixed-region boundary, |z^2-c^2| = |z-c|^2 (slope 2), 1028 samples | PASS |  |
| 7 | control: discs NOT fixed by z->-z (|2c|>r) have slope 1 there, as expected (1204 samples) | PASS |  |
| 8 | X has 24 vertices of valence 3 and 36 edges (no valence-2 points to smooth) | PASS |  |
| 9 | zeta_F(-1) by Siegel formula: Q(sqrt5) 1/30, Q(sqrt2) 1/12, Q(sqrt17) 1/3, Q(sqrt41) 4/3, Q(sqrt137) 8 | PASS |  |
| 10 | bound: |zeta_F(-1)| >= d^(3/2)/(2 pi^2)^2 > 24 for d > 444 (so the quadratic scan is complete) | PASS |  |
| 11 | mass scan: quadratic (d<=1200) 3 mass candidates, all with torsion; cubic (d<=5200) 6 candidates, 4 survive; quartic (d<=60000) 7, 2 survive | PASS | {'2': {'total': 365, 'norm2': 242, 'hplus1': 39, 'integral_target': 5, 'mass_cands': 3, 's |
| 12 | Q(sqrt41), level v.p5 and Q(sqrt137), level v: F(i) is ramified at v (Q2(i)/Q2 ramified) and split at p5 (i in Q5): units of order 4 exist | PASS |  |
| 13 | cubic/quartic bounds: (48*(2pi^2)^3)^(2/3) < 5200, (96*(2pi^2)^4)^(2/3) < 60000 | PASS |  |
| 14 | no genus-4 curve over F2 (non-hyperelliptic, all 3*2^16 quadric-cubic pairs) has L = octic | PASS |  |
| 15 | genus-5 curve A (3 quadrics in P^4, smooth) has L = (1-u+2u^2) * octic | PASS | [2, 16, 14, 20, 22] |
| 16 | genus-5 curve B (3 quadrics in P^4, smooth) has L = (1+u+2u^2) * octic | PASS | [4, 16, 4, 20, 44] |
| 17 | genus 5 with factor 1+2u^2 (a=0) is impossible: negative number of degree-4 points | PASS | [3, 7, 2, -1, 6] |
| 18 | census cross-check: among all 7829 genus-5 curves over F2 exactly the two classes above have the octic as a factor | PASS |  |
| 19 | tune theorem, brute force: all step systems N<=24 (S={1},{1,2}, T and T/I classes) injective on closed non-backtracking walks | PASS | systems tested 364 ok 364 collisions 0 capped 0 |
| 20 | tune theorem, exact held-note criterion: 6028 systems with N<=72 all satisfy it | PASS |  |
| 21 | two independent implementations of the criterion agree on all N<=24 systems | PASS |  |
| 22 | 12-tone consonant triads are one of the systems (24 chords, 3-regular) | PASS |  |
| 23 | LMFDB spectral test (recomputed): completed cases 3.3.733.1, 3.3.148.1 have dim 11 but |a_v| spectrum != that of X | PASS | 2 |
| 24 | citation web-verified: Lewin 1987 (ISBN 0300034938) | PASS |  |
| 25 | citation web-verified: Cohn 2012 (ISBN 9780199772698, OUP DOI) | PASS |  |
| 26 | citation web-verified: Honda 1968 (JMSJ 20:83-95, DOI 10.2969/jmsj/02010083) | PASS |  |
| 27 | citation web-verified: Dragutinovic 2024 (JPAA 228, 107522) | PASS |  |
