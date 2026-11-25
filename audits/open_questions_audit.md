# Audit: open questions round

**47/47 PASS**

| # | check | result | detail |
|---|---|---|---|
| 1 | word PLRLPRPL = +-[[-5,12],[12,-80]] (same element of PGL2), det 2^8, tau = tr^2/det = 7225/256 > 4 | PASS |  |
| 2 | tau(gamma^m) is rational and > 4 for m = 1..30 (eigenvalue ratio real, positive, not 1) | PASS |  |
| 3 | PLRLPRPL lies in K (even length, trivial image in the PLR group) | PASS |  |
| 4 | compact place: for 2000 random Hamilton quaternions 0 <= trd^2/nrd <= 4 (max 3.990906) | PASS |  |
| 5 | PLRLPRPL acts trivially on all 24 chords (so it lies in K) | PASS |  |
| 6 | edge-length lemma (order 2): at points fixed by z->-z away from the fixed-region boundary, |z^2-c^2| = |z-c|^2 (slope 2), 1015 samples | PASS |  |
| 7 | control: discs NOT fixed by z->-z (|2c|>r) have slope 1 there, as expected (1197 samples) | PASS |  |
| 8 | X has 24 vertices of valence 3 and 36 edges (no valence-2 points to smooth) | PASS |  |
| 9 | zeta_F(-1) by Siegel formula: Q(sqrt5) 1/30, Q(sqrt2) 1/12, Q(sqrt17) 1/3, Q(sqrt41) 4/3, Q(sqrt137) 8 | PASS |  |
| 10 | bound: |zeta_F(-1)| >= d^(3/2)/(2 pi^2)^2 > 24 for d > 444 (so the quadratic scan is complete) | PASS |  |
| 11 | mass scan: quadratic (d<=1200) 3 mass candidates, all with torsion; cubic (d<=5200) 6 candidates, 5 pass the (corrected) torsion test; quartic (d<=60000) 7, 2 pass {'2': {'total': 365, 'norm2': 242, 'hplus1': 39, 'integral_target': 5, 'mass_cands': 3, 'survivors': 0}, '3': {'total': 177, 'norm2': 121, 'hplus1': 68, 'integral_target': 6, 'mass_cands': 6, 'survivors': 5}, '4': {'total': 476, 'norm2': 203, 'hplus1': 68, 'integral_target': 8, 'mass_cands': 7, 'survivors': 2}} | PASS |  |
| 12 | Q(sqrt41), level v.p5 and Q(sqrt137), level v: F(i) is ramified at v (Q2(i)/Q2 ramified) and split at p5 (i in Q5): units of order 4 exist | PASS |  |
| 13 | cubic/quartic bounds: (48*(2pi^2)^3)^(2/3) < 5200, (96*(2pi^2)^4)^(2/3) < 60000 | PASS |  |
| 14 | no genus-4 curve over F2 (non-hyperelliptic, all 3*2^16 quadric-cubic pairs) has L = octic | PASS |  |
| 15 | genus-5 curve A (3 quadrics in P^4, smooth) has L = (1-u+2u^2) * octic [2, 16, 14, 20, 22] | PASS |  |
| 16 | genus-5 curve B (3 quadrics in P^4, smooth) has L = (1+u+2u^2) * octic [4, 16, 4, 20, 44] | PASS |  |
| 17 | genus 5 with factor 1+2u^2 (a=0) is impossible: negative number of degree-4 points [3, 7, 2, -1, 6] | PASS |  |
| 18 | census cross-check: among all 7829 genus-5 curves over F2 exactly the two classes above have the octic as a factor | PASS |  |
| 19 | tune theorem, brute force: all step systems N<=24 (S={1},{1,2}, T and T/I classes) injective on closed non-backtracking walks systems tested 364 ok 364 collisions 0 capped 0 | PASS |  |
| 20 | tune theorem, exact held-note criterion: 6028 systems with N<=72 all satisfy it | PASS |  |
| 21 | two independent implementations of the criterion agree on all N<=24 systems | PASS |  |
| 22 | 12-tone consonant triads are one of the systems (24 chords, 3-regular) | PASS |  |
| 23 | LMFDB spectral test (recomputed): completed cases 3.3.733.1, 3.3.148.1, 3.3.469.1, 3.3.316.1, 3.3.316.1, 4.4.2777.1 have dim 11 but |a_v| spectrum != that of X 6 | PASS |  |
| 24 | chord graph X: characteristic polynomial contains (t^4-4t^2+1)^2 (eigenvalues +-2cos(pi/12), +-2cos(5pi/12)) | PASS |  |
| 25 | Brandt graphs at v, computed directly for all choices of D'', N, v (469 x2, 316 x2, 2777 level p71, 2777 level p8^2, and 733, 148): 12 classes, trivial units, mass 12, symmetric 3-regular B(v), no factor t^4-4t^2+1, so the reduction graph is not X ['733', '148', '469', '469', '316', '316', '2777a', '2777b'] | PASS |  |
| 26 | second method: Brandt matrix recomputed by counting elements of norm pi*nu in transporters (theta coefficients) agrees with the neighbour graph in all 10 torsion-free cases | PASS |  |
| 27 | corrected torsion test agrees with the direct computation: the 7 torsion-test survivors are exactly the configurations with 12 classes and trivial units | PASS |  |
| 28 | torsion configurations (quadratic 41 x4, 137 x2; cubic 564; quartic 13448 x2, 13676, 6809, 10273): class number 13-18 > 12 with unit groups of order 2 or 3, weighted mass exactly 12, so no reduction graph X | PASS |  |
| 29 | independent validation: Brandt spectra equal LMFDB Hecke eigenvalues in all 6 LMFDB-available cases (733, 148, 469, 316 x2, 2777 level p71) and PARI modular-form a_2 for X_0^26(9), X_0^570(1) | PASS |  |
| 30 | LMFDB cross-check extended: 2777 at level p8^2 (separate scheduled LMFDB query) has |a_v| spectrum equal to the Brandt spectrum; with the six above, 7 torsion-free configurations agree | PASS |  |
| 31 | degree bound: Odlyzko unconditional Table 4 (162 rows) plus the prime of norm 2 gives d^(1/n) above (8pi^2)^(2/3)(9/4)^(2/(3n)) for all 15 <= n <= 200, not for n = 14 (kernel H >= 0 checked) | PASS |  |
| 32 | general scan (any h+) restricted to h+=1 reproduces the earlier field list: quadratic 41, 137; cubic 148, 316, 469, 564, 733; quartic 2777, 6809, 10273, 13448, 13676 | PASS |  |
| 33 | field counts within the bounds: 178 real quadratic, 411 totally real cubic, 1994 totally real quartic fields (PARI nflist), of which 117, 297, 980 have a prime of norm 2 | PASS |  |
| 34 | zeta_F(-1) by Siegel's formula equals the PARI value for all 117 real quadratic fields with a prime of norm 2 | PASS |  |
| 35 | h+ > 1, degree <= 4: all 55 configurations computed; class count = mass formula, theta recount agrees, the bipartite double has exactly h+ components, none isomorphic to X (44 torsion-free) | PASS |  |
| 36 | generalised Brandt code reproduces the h+=1 runs (733: 12 classes, same charpoly; Q(sqrt137): 13 classes with torsion; 2777 at p71: same charpoly) | PASS |  |
| 37 | degree 5: the LMFDB list (2507 totally real quintic fields) covers every d <= 3625942 (next field has d = 3626944); 4 fields with mass solutions, 4 configurations, all computed by the generalised Brandt code, mass and theta checks pass, none gives X | PASS |  |
| 38 | degree 6 (partial): all 300 totally real sextic fields with d <= 8256125 (LMFDB, sorted list); this covers every sextic field with h+ = h, which must have d <= 6620853; no mass solution | PASS |  |
| 39 | prefilter is sound: for 12 random prefiltered quintic fields the exact |zeta_F(-1)| (PARI) exceeds 12*u*2^(n-1) and the Euler-product lower bound used | PASS |  |
| 40 | held notes, lemma: no link graph Lk(b) contains a 4-cycle, all chord classes (T and T/I), N = 5..60 | PASS |  |
| 41 | held notes, one moving voice: brute force over all step sets for N <= 22 agrees exactly with the family (8|N, class of {0,N/8,N/2}, N/4 in S); 17 exceptional systems; for S within {1,2} only N=8, S={2} | PASS |  |
| 42 | held notes, independent brute force: all closed non-backtracking walks of length <= 8, all step sets, N <= 12 (954 tunes): every collision is in the predicted family | PASS |  |
| 43 | torsion structure: q+1 = 3|Gamma_x| + r forces |Gamma_x|=1, r=0 for q=2 and |Gamma_x|=1, r=2 for q=4; for q=8 an order-3 element of PGL2(F8) acts on P^1(F8) without fixed points (three free orbits) | PASS |  |
| 44 | citation web-verified: Lewin 1987 (ISBN 0300034938) | PASS |  |
| 45 | citation web-verified: Cohn 2012 (ISBN 9780199772698, OUP DOI) | PASS |  |
| 46 | citation web-verified: Honda 1968 (JMSJ 20:83-95, DOI 10.2969/jmsj/02010083) | PASS |  |
| 47 | citation web-verified: Dragutinovic 2024 (JPAA 228, 107522) | PASS |  |

Random samples use a keyed stream per check (`random.Random(k)`), so each check replays independently of the others.
