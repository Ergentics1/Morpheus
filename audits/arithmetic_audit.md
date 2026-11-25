# Stage 1 (Eisenstein, new angles) audit — 23/23 PASS

- PASS f_3 = 2 - i (Gaussian prime over 5) => eigenvalue sqrt5
- PASS f_4 = 1+2w = i sqrt3 (ramified Eisenstein prime) => eigenvalue sqrt3
- PASS f_2 = f_6 = 1
- PASS f_1,f_5,f_7,f_11 are units of Z[zeta12]; |f_5|^2 = 2+sqrt3 fundamental unit of Q(sqrt3)
- PASS Galois sigma_a f_k = f_{ak}
- PASS M11 (complex conjugation) is a graph automorphism (major<->minor)
- PASS M5,M7 (sigma5,sigma7) map the Tonnetz isomorphically onto the [014] flip graph
- PASS charpoly = (x-3)(x+3)(x-1)^3(x+1)^3(x^2-5)^2(x^2-3)^2(x^4-4x^2+1)^2
- PASS octic Weil factor T^8+4T^6+9T^4+16T^2+16 irreducible
- PASS E+ (lam=1): Weil polynomial (all roots |.|=sqrt2)
- PASS E- (lam=-1): Weil polynomial (all roots |.|=sqrt2)
- PASS S5 (lam=±sqrt5): Weil polynomial (all roots |.|=sqrt2)
- PASS S3 (lam=±sqrt3): Weil polynomial (all roots |.|=sqrt2)
- PASS E+/E- Frobenius field Q(sqrt-7)
- PASS S5 field contains Q(sqrt-3) (Eisenstein) and Q(sqrt5)
- PASS S3 field Q(sqrt3,sqrt-5)
- PASS explicit curves over F2 with trace +1 and -1 exist (brute force)
- PASS exhaustive: 12 Tonnetz-type homs Z[w]->Z12, all with multiplier-ring conductor 12, none an ideal
- PASS no cyclic Z12 quotient of Z[w], Z[i] (mod 4) or Z[zeta12] (mod 3, mod 4)
- PASS orders Z[f w] with cyclic Z12 quotient: exactly even f (f<=12)
- PASS Tonnetz = Z[sqrt-3]/(sqrt-3 (1+sqrt-3)): fifth=1+2s, M3=1+s, m3=s, semitone=1
- PASS that CM torus is C/Z[sqrt-3], j = 54000
- PASS equilateral (musical) Tonnetz torus: reduced form (9,-6,13), disc -432

External (LMFDB, fetched 2026-11-25): 1.2.ab (y^2+xy=x^3+x^2+1, Q(sqrt-7)), 1.2.b (y^2+xy=x^3+1), 2.2.a_ab (Jacobian of y^2+(x^2+x)y=x^5+x^3+x^2+x, End Q(sqrt-3,sqrt5), over F4 ~ (1.4.ab)^2 with M2(Q(sqrt-15))), 2.2.a_b (Jacobian of y^2+(x^2+x+1)y=x^5+x^3+x^2+1, End Q(sqrt3,sqrt-5), over F4 ~ (1.4.b)^2), 4.2.a_e_a_j (no Jacobian, field 8.0.5780865024.4), newform 49.2.a.a (CM -7, a_2 = 1).
