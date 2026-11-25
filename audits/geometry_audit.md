# math_audit (geometry round)

**59/59 checks pass**

| # | script | check | result |
|---|---|---|---|
| 1 | schottky | tree: v0 has 3 neighbours (P^1(F_2)) | PASS |
| 2 | schottky | sigma_P^2 is scalar (involution in PGL2) | PASS |
| 3 | schottky | sigma_P moves v0 to a neighbour | PASS |
| 4 | schottky | sigma_P maps that neighbour back to v0 (edge inversion) | PASS |
| 5 | schottky | sigma_L^2 is scalar (involution in PGL2) | PASS |
| 6 | schottky | sigma_L moves v0 to a neighbour | PASS |
| 7 | schottky | sigma_L maps that neighbour back to v0 (edge inversion) | PASS |
| 8 | schottky | sigma_R^2 is scalar (involution in PGL2) | PASS |
| 9 | schottky | sigma_R moves v0 to a neighbour | PASS |
| 10 | schottky | sigma_R maps that neighbour back to v0 (edge inversion) | PASS |
| 11 | schottky | the three sigma_i send v0 to the three distinct neighbours | PASS |
| 12 | schottky | reduced words of length <=7 give pairwise distinct vertices | PASS |
| 13 | schottky | w and w[:-1] are adjacent in T (word path = geodesic) | PASS |
| 14 | schottky | ball count 1+3*(2^n-1) matches tree ball of radius 7 | PASS |
| 15 | schottky | BFS tree reaches all 24 triads | PASS |
| 16 | schottky | number of Schreier generators = 36-23 = 13 = rank pi_1(X) | PASS |
| 17 | schottky | every Schreier word stabilises C major (lies in K) | PASS |
| 18 | schottky | all 13 generators hyperbolic: 2 v2(tr) < v2(det) | PASS |
| 19 | schottky | translation length on T = length of the closed cycle in X | PASS |
| 20 | schottky | stab(C)=kernel: every word fixing C fixes all 24 triads | PASS |
| 21 | schottky | covering T->X: adjacent vertices map to PLR-adjacent triads | PASS |
| 22 | schottky | K has no inversions: all elements of K are even words (preserve bipartition) | PASS |
| 23 | schottky | genus = rank H1(X) = E-V+1 = 13 | PASS |
| 24 | schottky | special fibre: 24 P^1 meeting in 36 F2-nodes, #C0(F_2^n)=24*2^n-12, N1=36 = all F2-points are nodes | PASS |
| 25 | schottky | non-arithmetic witness: some generator is hyperbolic at the real place (tr^2>4|det|), impossible in a definite order | PASS |
| 26 | sandpile | spanning trees kappa = det reduced Laplacian = 156,008,448 = 2^15 3^2 23^2 | PASS |
| 27 | sandpile | |critical group| = product of invariant factors = kappa | PASS |
| 28 | sandpile | one zero invariant factor (connected) | PASS |
| 29 | sandpile | Fourier: kappa = (1/24)*6*prod_{k=1..11}(9-|f_k|^2) | PASS |
| 30 | sandpile | 23^2 comes from k=1,11 and 5,7: (9-(2-sqrt3))(9-(2+sqrt3)) = 46 | PASS |
| 31 | sandpile | 13 fundamental cycles | PASS |
| 32 | sandpile | cycles are closed (boundary 0) | PASS |
| 33 | sandpile | det(cycle pairing Q) = kappa (tropical Jacobian volume^2 = spanning trees) | PASS |
| 34 | sandpile | coker Q = critical group (same invariant factors) | PASS |
| 35 | sandpile | diag of Q = cycle lengths (6 or 8 here) | PASS |
| 36 | sandpile | divisorial gonality computed by exhaustive search | PASS |
| 37 | sandpile | witness has rank>=1 (pure-python recheck) | PASS |
| 38 | sandpile | Baker specialisation: gon(X) > 2  =>  the Mumford curve C is not hyperelliptic | PASS |
| 39 | tower | X is isomorphic to the Z/12 voltage cover of Theta with voltages P:4, L:0, R:1 | PASS |
| 40 | tower | 1/zeta_X(u) = prod_{k=0}^{11} L_Theta(u,chi_k)^{-1} (Artin-Ihara factorisation over the 12 characters) | PASS |
| 41 | tower | Chevalley-Weil: genus(C)=13 = 2 (trivial char) + 11*(g_H-1)=11 | PASS |
| 42 | tower | genus of Z/d intermediate curve = d+1 | PASS |
| 43 | curvesF2 | degree-44 polynomial, P(u)=q^22 u^44 P(1/(qu)) functional equation | PASS |
| 44 | curvesF2 | all inverse roots have |alpha|=sqrt2 (Riemann hypothesis holds; it is a q-Weil polynomial) | PASS |
| 45 | curvesF2 | N_2=39 > N_6=27: impossible since C(F_4) is a subset of C(F_64) -> no curve over F_2 has this zeta | PASS |
| 46 | curvesF2 | also degree-2 places count: (N_2-N_1)/2 integer and >=0 | PASS |
| 47 | curvesF2 | E1: y^2+xy=x^3+x^2+1: smooth genus 1, L = 2*u**2 - u + 1 | PASS |
| 48 | curvesF2 | E2: y^2+xy=x^3+1: smooth genus 1, L = 2*u**2 + u + 1 | PASS |
| 49 | curvesF2 | y^2+(x^2+x)y=x^5+x^3+x^2+x: smooth genus 2, L = 4*u**4 - u**2 + 1 | PASS |
| 50 | curvesF2 | y^2+(x^2+x+1)y=x^5+x^3+x^2+1: smooth genus 2, L = 4*u**4 + u**2 + 1 | PASS |
| 51 | curvesF2 | no hyperelliptic genus-4 curve over F2 has Jacobian in class 4.2.a_e_a_j | PASS |
| 52 | gon_check | pure-python: no rank-1 divisor of degree <=5 (vertex-transitivity => contains C) | PASS |
| 53 | gon_check | Chan criterion: none of the 13 involutions of X has a tree quotient (metric graph not hyperelliptic) | PASS |
| 54 | recheck_g6 | independent recount: genus-6 curve y^2+(x^6+x^5+x^4+x^3+1)y=x^13+x^3+x has L=(1-3u^2+4u^4)(octic) | PASS |
| 55 | audit | |Aut(X)|=24 => Aut(C)=N(K)/K = D12 (the T/I group) exactly | PASS |
| 56 | shimura | all torsion-free genus-13 CD curves X_0^D(N), 2|D, have dim S2^{D/2-new}=11 (Brandt class number 12 consistency) | PASS |
| 57 | shimura | none of the 18 genus-13 CD curves X_0^D(N) (2|D, any number of primes) has the chord-graph spectrum | PASS |
| 58 | shimura | none of the 4 Gamma_H level structures with 24 components has the chord-graph spectrum | PASS |
| 59 | shimura | torsion-free Gamma_H cases have 11 forms (consistency) | PASS |
