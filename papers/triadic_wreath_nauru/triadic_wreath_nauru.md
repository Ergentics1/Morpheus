# Uniform Triadic Wreath Products, the Nauru Graph, and $2$-Adic Arithmeticity

**Author:** Ergentics · **Date:** November 2026 · **Series:** Morpheus Paper #08 (`PC-II`, sequel to [*Prime Cadences*](../../prime_cadences_paper.md)) · **Edition:** `v0.5.1` (Round-1 `[GB]` reconciled)  
**Canonical PDF:** [`paper/triadic_wreath_nauru.pdf`](paper/triadic_wreath_nauru.pdf) (0 LaTeX warnings/hboxes) · **arXiv Bundle:** [`arxiv/triadic-wreath-nauru-arxiv.tar.gz`](arxiv/triadic-wreath-nauru-arxiv.tar.gz)

> **Abstract.** We resolve the structural relationship between David Lewin's melodic $T/I$ group, the neo-Riemannian $PLR$ harmonic group, and Julian Hook's Uniform Triadic Transformation wreath product $\mathrm{UTT} = \mathbb{Z}_{12} \wr \mathbb{Z}_2$ (order $288$), and uncover a $2$-adic arithmetic universe inside its Galois twists. First, $\langle T, PLR\rangle \cong (\mathbb{Z}_{12}\times D_{12})/\mathbb{Z}_2$ has order $144$ ($|[G,G]| = 6$, $|G^{\mathrm{ab}}| = 24$) — the exact index-$2$ even-parity subgroup of $\mathrm{UTT}$, missing odd-parity elements such as Hook's order-$24$ Hamiltonian cycle $Q = \langle -,1,0\rangle$ (`NEG-M16`). Meanwhile, $T/I$ and $PLR$ **do** fuse by Crans–Fiore–Satyendra duality ($C_{\mathrm{Sym}(24)}(T/I) = PLR$, sharing $\{e, T_6 = (LR)^6\}$) into $\langle T/I, PLR\rangle \cong (D_{12}\times D_{12})/\mathbb{Z}_2$ of order $288$, yet this group is **neither equal nor isomorphic** to $\mathrm{UTT}$ (`NEG-M15`). Instead, $I_0 \notin \mathrm{UTT}$ normalizes $\mathrm{UTT}$ via $I_0\langle\sigma,t^+,t^-\rangle I_0^{-1} = \langle\sigma,-t^-,-t^+\rangle$, generating $\mathrm{UTT}\rtimes\langle I_0\rangle$ (order $576$), which sits at index $2$ inside **two distinct, non-isomorphic** order-$1{,}152$ extensions (`NEG-M19`): the full normalizer $N_{\mathrm{Sym}(24)}(T) = N_{\mathrm{Sym}(24)}(\mathrm{UTT}) = \mathrm{UTT}\rtimes\mathbb{Z}_{12}^\times$ ($247$ involutions, $|[G,G]|=72$) and Hook's quasi-uniform wreath product $Q\mathrm{UTT} \cong D_{12}\wr\mathbb{Z}_2$ ($219$ involutions, $|[G,G]|=144$, which does *not* normalize $\mathrm{UTT}$). Second, an exhaustive census of all $24$ simply transitive order-$24$ subgroups of $\mathrm{UTT}$ ($8$ isomorphism classes indexed by $u \in \mathbb{Z}_{12}^\times$) proves that $PLR \cong D_{12}$ is the **unique** subgroup admitting $3$-involution Coxeter triples ($192$ total, $168$ Ramanujan), whereas the split $M_5$ ($S_3\times\mathbb{Z}_4$) and $M_7$ ($\mathbb{Z}_3\times D_4$) twists canonically construct the **Nauru graph** $Y = \mathrm{GP}(12,5)$ with sharper Ramanujan gap $\lambda_{\mathrm{nt}} = 2.000 < \sqrt{5} < 2\sqrt{2}$. Third, in sharp contrast to the non-arithmetic Tonnetz curve $C_X$ of Paper #01, the Nauru graph overturns every $2$-adic obstruction: its integral spectrum splits $\zeta_Y(u)^{-1}$ completely into quadratic $\mathbb{F}_2$ Weil factors hitting all five elliptic isogeny classes, its Raynaud/sandpile group is pure $5$-smooth ($|K(Y)| = 162{,}000{,}000 = 2^7\cdot 3^4\cdot 5^6$), its divisorial gonality $\operatorname{gon}(Y) = 6$ is witnessed by a single reduced prime hexagon, and $|\operatorname{Aut}(Y)| = 144 = 12(g-1)$ lifts via the Lamé amalgam $\tilde{\Gamma} = S_3 *_{\mathbb{Z}_2} V_4 \subset \mathrm{PGL}_2(\mathbb{Q}_2)$. Expressing $\tilde{\Gamma}$ through the single modulus $x = \tau(ta)$ yields universal Fricke–Vogt polynomials and ambient quaternion algebra $B(x) = \left(\frac{-3,\, x(x-3)}{\mathbb{Q}(x)}\right)$, proving that rational arithmetic Nauru curves occur **if and only if** $x \in \{\frac{1}{2}, \frac{3}{2}, \frac{5}{2}\}$ inside $B_3 = (-3,-1)_{\mathbb{Q}}$ ($D=6$) and $B_5 = (-3,-5)_{\mathbb{Q}}$ ($D=10$). At $x = \frac{3}{2}$ ($\tau(\gamma_6) = \frac{121}{64} < 4$), $\Gamma_Y \trianglelefteq_{V_4} \Gamma(3)$ is an explicit **arithmetic non-congruence** Klein $V_4$-cover of the genus-$4$ principal level-$3$ Shimura curve $X^6(\Gamma(3))$ (dual graph $K_{3,3}$); at $x = \frac{5}{2}$, $\Gamma_Y \trianglelefteq_{S_3} \Gamma_5(3)$ covers $X^{10}(\Gamma(3))$ ($K_4$) through the cube $Q_3$ — explaining why all $19$ Borel-level genus-$13$ Shimura curves $X_0^D(N)$ fail (`NEG-M18`). Finally, the unique dicyclic companion $\mathrm{Dic}_6 \subset \mathrm{UTT}$ produces $12/18$ strictly Ramanujan $4$-regular bipartite Cayley graphs ($g = 25$, $\lambda_{\mathrm{nt}} = 3 < 2\sqrt{3}$, open $3$-adic arithmeticity on $T_4$). Verified across three zero-shared-data planes: pure Python (`12/12` gates), zero-Mathlib Lean 4.36.0 (`22/22` theorems), and zero-crate Rust (`6/6` tests), with Round-1 independent audit by Grok Bot (`[GB]`).

---

## 1. Introduction

Paper #01 ([*Prime Cadences*](../../prime_cadences_paper.md)) analyzed the $3$-regular neo-Riemannian Tonnetz $X = \mathrm{Cay}(D_{12}, \{P, L, R\})$, culminating in three sharp $2$-adic obstructions in Section 7: (i) an irreducible octic factor $(1+4u^2+9u^4+16u^6+16u^8)^2$ over $\mathbb{F}_2$ demanding genus $\ge 5$; (ii) the exotic prime $23$ inside the Néron component group $|K(X)| = 156{,}008{,}448 = 2^{15}\cdot 3^2\cdot 23^2$; and (iii) non-arithmeticity ($\tau(\gamma_0) = 7225/256 > 4$) barring $C_X$ from every torsion-free arithmetic uniformization and every Borel-level Shimura curve $X_0^D(N)$ over $\mathbb{Q}$.

This sequel resolves whether Lewin's melodic $T/I$ group and the $PLR$ harmonic group fuse into Hook's Uniform Triadic Transformation wreath product $\mathrm{UTT} = \mathbb{Z}_{12} \wr \mathbb{Z}_2$, classifies all $24$ simply transitive order-$24$ subgroups of $\mathrm{UTT}$, and reveals that the split $M_5/M_7$ Galois twist produces the **Nauru graph $Y = \mathrm{GP}(12,5)$**, whose Lamé-type $2$-adic Mumford uniformizations admit exact rational arithmetic realizations ($x \in \{\frac12, \frac32, \frac52\}$) overturning every obstruction of Paper #01.

---

## 2. Fusion of Lewin $T/I$ and $PLR$ — But Not into Hook's Wreath Product

Label the $24$ major and minor triads as $(r, +) = \{r, r+4, r+7\}$ and $(r, -) = \{r, r+3, r+7\}$ ($r \in \mathbb{Z}_{12}$). Hook's $\mathrm{UTT} = \mathbb{Z}_{12} \wr \mathbb{Z}_2$ (order $288$) acts by $\langle +, t^+, t^-\rangle(r, \pm) = (r + t^\pm, \pm)$ and $\langle -, t^+, t^-\rangle(r, \pm) = (r + t^\pm, \mp)$, containing $T_1 = \langle +, 1, 1\rangle$, $P = \langle -, 0, 0\rangle$, $L = \langle -, 4, 8\rangle$, and $R = \langle -, 9, 3\rangle$, whereas Lewin's inversion $I_0(x) = -x \pmod{12}$ acts by $I_0(r, \pm) = (5 - r, \mp)$.

- **Theorem 2.1 (`NEG-M16` — Even-parity obstruction):** The parity map $\varepsilon(\langle\sigma, t^+, t^-\rangle) = (t^+ + t^-) \bmod 2$ is a surjective homomorphism $\mathrm{UTT} \to \mathbb{Z}_2$ (Lean 4 Theorem 1). Every generator of $\langle T, PLR\rangle$ lies in $\ker(\varepsilon)$, so $\langle T, PLR\rangle = \ker(\varepsilon) \cong (\mathbb{Z}_{12}\times D_{12})/\mathbb{Z}_2$ has order **$144$**, commutator subgroup $[PLR, PLR] = \langle (LR)^2\rangle \cong \mathbb{Z}_6$ (order **$6$**), abelianization order **$24$**, and misses odd-parity elements such as Hook's order-$24$ Hamiltonian cycle $Q = \langle -, 1, 0\rangle$ (Lean 4 Theorem 2).
- **Theorem 2.2 (`NEG-M15`, `NEG-M19` — Fusion into $(D_{12}\times D_{12})/\mathbb{Z}_2$, Crans–Fiore–Satyendra duality, and the order-$1{,}152$ bifurcation):** By Crans–Fiore–Satyendra duality, $T/I$ and $PLR$ are mutual centralizers in $\mathrm{Sym}(24)$ ($C_{\mathrm{Sym}(24)}(T/I) = PLR$, $C_{\mathrm{Sym}(24)}(PLR) = T/I$) sharing only $\{e, T_6 = (LR)^6\}$ (Lean 4 Theorem 21), so they **do** fuse into $\langle T/I, PLR\rangle \cong (D_{12}\times D_{12})/\mathbb{Z}_2$ of order $24 \cdot 24 / 2 = 288$ — **but not into $\mathrm{UTT}$**. Instead, $I_0 \notin \mathrm{UTT}$ (Lean 4 Theorem 3) normalizes $\mathrm{UTT}$ via $I_0 \langle\sigma, t^+, t^-\rangle I_0^{-1} = \langle\sigma, -t^-, -t^+\rangle$ (Lean 4 Theorem 4), generating $\mathrm{UTT} \rtimes \langle I_0\rangle$ (order $576$), above which the lattice bifurcates into **two distinct, non-isomorphic** index-$2$ extensions of order $1{,}152$:
  - the full normalizer $N_{\mathrm{Sym}(24)}(T) = N_{\mathrm{Sym}(24)}(\mathrm{UTT}) = \mathrm{UTT}\rtimes\mathbb{Z}_{12}^\times$ (adjoining $M_5, M_7$; normalizes $\mathrm{UTT}$);
  - Hook's quasi-uniform wreath product $Q\mathrm{UTT} \cong D_{12}\wr\mathbb{Z}_2$ (adjoining mode-local major inversion $I_{\mathrm{maj}}$; does **not** normalize $\mathrm{UTT}$, Lean 4 Theorem 22).
  Their exact intersection is $\mathrm{UTT}\rtimes\langle I_0\rangle$ ($576$) and their join has order $2{,}304$ (index $2$ in $\mathrm{Aff}(\mathbb{Z}_{12})\wr\mathbb{Z}_2$, order $4{,}608$):

| Group | Order | $\|Z(G)\|$ | Involutions | Order-$24$ elems | $\|[G,G]\|$ / $\|G^{\mathrm{ab}}\|$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| $\langle T, PLR\rangle \cong (\mathbb{Z}_{12}\times D_{12})/\mathbb{Z}_2$ | $144$ | $12$ | $15$ | $0$ | $6$ / $24$ |
| $\mathrm{UTT} = \mathbb{Z}_{12}\wr\mathbb{Z}_2$ | $288$ | $12$ | $15$ | $48$ | $12$ / $24$ |
| $\langle T/I, PLR\rangle \cong (D_{12}\times D_{12})/\mathbb{Z}_2$ | $288$ | $2$ | $99$ | $0$ (max $12$) | $18$ / $16$ |
| $\mathrm{UTT}\rtimes\langle I_0\rangle$ | $576$ | $2$ | $171$ | $96$ | $72$ / $8$ |
| $N_{\mathrm{Sym}(24)}(T) = N_{\mathrm{Sym}(24)}(\mathrm{UTT})$ | $1{,}152$ | $2$ | $247$ | $192$ | $72$ / $16$ |
| Hook $Q\mathrm{UTT} \cong D_{12}\wr\mathbb{Z}_2$ | $1{,}152$ | $2$ | $219$ | $96$ | $144$ / $8$ |

---

## 3. Exhaustive 24-Subgroup UTT Census and the Nauru Graph

Any simply transitive order-$24$ subgroup $H \le \mathrm{UTT}$ has mode-preserving subgroup $H_+ = \{\langle +, r, ur\rangle : r \in \mathbb{Z}_{12}\}$ for a unique unit $u \in \mathbb{Z}_{12}^\times = \{1, 5, 7, 11\}$, extended by $g_0 = \langle -, 0, b\rangle$ with $(u - 1)b \equiv 0 \pmod{12}$.

**Theorem 3.1 (Complete 24-subgroup census):** All $24$ simply transitive subgroups partition into $8$ isomorphism classes:

| $u$ | Class | Count | Inv. | Coxeter triples (Ram.) | Mixed cubic (Ram.) | Best $\lambda_{\mathrm{nt}}$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| $1$ | $\mathbb{Z}_{12}\times\mathbb{Z}_2$ | $6$ | $3$ | $0$ ($0$) | $8$ ($8$) | $1 + \sqrt{3} \approx 2.732$ |
| $1$ | $\mathbb{Z}_{24}$ | $6$ | $1$ | $0$ ($0$) | $4$ ($0$) | $1 + 2\cos(\pi/12) \approx 2.932$ |
| $5$ | $S_3 \times \mathbb{Z}_4$ | $2$ | $7$ | $0$ ($0$) | $24$ ($24$) | **$2.000$ (Nauru)** |
| $5$ | $\mathbb{Z}_3 \rtimes \mathbb{Z}_8$ | $2$ | $1$ | $0$ ($0$) | $0$ ($0$) | — |
| $7$ | $\mathbb{Z}_3 \times D_4$ | $3$ | $5$ | $0$ ($0$) | $16$ ($16$) | **$2.000$ (Nauru)** |
| $7$ | $\mathbb{Z}_3 \times Q_8$ | $3$ | $1$ | $0$ ($0$) | $0$ ($0$) | — |
| $11$ | $D_{12}$ ($PLR$) | $1$ | $13$ | **$192$ ($168$)** | $24$ ($24$) | $\sqrt{5} \approx 2.236$ (Tonnetz) |
| $11$ | $\mathrm{Dic}_6$ | $1$ | $1$ | $0$ ($0$) | $0$ ($0$) | — ($4$-reg. $T_4$ twin) |

- $PLR \cong D_{12}$ is the **unique** simply transitive $\mathrm{UTT}$ subgroup admitting $3$-involution Coxeter triples ($168$ bipartite Ramanujan; $24$ non-bipartite using $\langle +,6,6\rangle$ fail at $1 + 2\cos(\pi/12) > 2\sqrt{2}$).
- The split $M_5$ ($S_3\times\mathbb{Z}_4$) and $M_7$ ($\mathbb{Z}_3\times D_4$) twists with $S_{\mathrm{Nauru}} = \{\langle -,6,6\rangle, \langle +,1,5\rangle, \langle +,11,7\rangle\}$ realize the **Nauru graph $Y = \mathrm{GP}(12, 5)$** under $u_r = (r,+)$, $v_r = (r+6,-)$, with sharper Ramanujan gap $\lambda_{\mathrm{nt}} = 2.000 < \sqrt{5} < 2\sqrt{2}$.

---

## 4. $\mathbb{F}_2$ Elliptic Weil Splitting, Prime Cadences, and Tropical Invariants

**Theorem 4.1:** $Y = \mathrm{GP}(12, 5)$ is bipartite, $3$-regular, girth $6$ (zero $4$-cycles; Lean 4 Theorems 5–8), with pure integer spectrum $\{+3^1, +2^6, +1^3, 0^4, -1^3, -2^6, -3^1\}$ and exact $\mathbb{F}_2$ elliptic Weil factorization:

$$\zeta_Y(u)^{-1} = (1-u^2)^{13}(1-4u^2)(1+2u^2)^4(1-u+2u^2)^3(1+u+2u^2)^3(1-2u+2u^2)^6(1+2u+2u^2)^6,$$

realizing **all five** elliptic curve isogeny classes over $\mathbb{F}_2$ (Lean 4 Theorem 10):

| $a_2$ | Mult. | Ihara factor | Smooth Weierstrass model over $\mathbb{F}_2$ | $\#E(\mathbb{F}_2)$ | Type |
| ---: | :---: | :--- | :--- | :---: | :--- |
| $+2$ | $6$ | $1 - 2u + 2u^2$ | $y^2 + y = x^3 + x + 1$ | $1$ | Supersingular |
| $+1$ | $3$ | $1 - u + 2u^2$ | $y^2 + xy = x^3 + x^2 + 1$ | $2$ | Ordinary |
| $0$ | $4$ | $1 + 2u^2$ | $y^2 + y = x^3$ | $3$ | Supersingular |
| $-1$ | $3$ | $1 + u + 2u^2$ | $y^2 + xy = x^3 + 1$ | $4$ | Ordinary |
| $-2$ | $6$ | $1 + 2u + 2u^2$ | $y^2 + y = x^3 + x$ | $5$ | Supersingular |

Exact directed prime cadence counts $\pi_Y(m)$ ($6 \le m \le 24$, even): `24, 108, 216, 564, 2232, 8820, 31824, 104292, 384792, 1401744`. The three free bipartition-swapping involutions $g_c: u_r \leftrightarrow v_{5r+c}$ ($c \in \{2, 6, 10\}$) make $Y$ the bipartite double of the $12$-vertex **Truncated Tetrahedron** $G_{12} = \mathrm{Cay}(A_4, \{s, r, r^{-1}\})$ (spectrum $\{+3^1, +2^3, 0^2, -1^3, -2^3\}$).

> **Remark 4.2 (Scope of integral Weil splitting and Bruhat–Tits uniformization):** Quadratic splitting into $\mathbb{F}_2$ elliptic Weil factors follows directly from integrality of $\operatorname{Spec}(A_Y) \subset \{0, \pm 1, \pm 2, \pm 3\}$; it eliminates Paper #01's irreducible genus-$4/5$ octic obstruction rather than constituting arithmetic evidence by itself. Likewise, *every* finite $(q+1)$-regular graph of genus $g \ge 2$ admits a Schottky uniformization $T_{q+1}/\Gamma$ on the Bruhat–Tits tree of $\mathrm{PGL}_2(\mathbb{Q}_q)$; true arithmeticity (commensurability with a definite quaternion order) is established for $Y$ solely in Sections 5–6 and remains open for the $3$-adic companion $Z$ in Section 7.

**Theorem 4.3 (Tropical Invariants):**
- **Raynaud component group:** $K(Y) \cong \mathbb{Z}/5 \oplus \mathbb{Z}/5 \oplus \mathbb{Z}/5 \oplus \mathbb{Z}/30 \oplus \mathbb{Z}/120 \oplus \mathbb{Z}/360$, of pure $5$-smooth order $|K(Y)| = 162{,}000{,}000 = 2^7\cdot 3^4\cdot 5^6$ (exact SNF, Python Gate D4, Lean 4 Theorem 11).
- **Divisorial gonality:** Exhaustive Dhar burning across all $20{,}474$ effective divisors of degrees $2 \le d \le 5$ with $D(u_0) \ge 1$ proves $\operatorname{gon}(Y) = 6$, attained by a single reduced prime hexagon $D_{\mathrm{hex}} = \mathrm{C} + \mathrm{C}\sharp + \mathrm{D} + \mathrm{f}\sharp\mathrm{m} + \mathrm{a}\flat\mathrm{m} + \mathrm{c}\sharp\mathrm{m}$ ($r = 1$). None of the $39$ involutions has a tree quotient ($\beta_1 \in \{4^6, 5^9, 6^{18}, 7^6\}$), so $C_Y$ is not hyperelliptic.

---

## 5. $2$-Adic Lamé Moduli Space and Rational Arithmetic Classification

**Proposition 5.1 (`NEG-M17`):** $|\operatorname{Aut}(Y)| = 144 = 12(g - 1)$ lifts via the Herrlich–Cornelissen–Kato Lamé amalgam $\tilde{\Gamma} = S_3 *_{\mathbb{Z}_2} V_4$ ($\chi = -\frac{1}{12}$, Lean 4 Theorem 12), whose index-$144$ kernel $\Gamma_Y$ is torsion-free of rank $13$. Split involutions $\det(b) \in -(\mathbb{Q}_2^\times)^2$ cannot lift $\tilde{\Gamma}$ into $\mathrm{PGL}_2(\mathbb{Q}_2)$ because $v_2(q^2 - p^2) \ge 3 \neq 1$ for all odd $p, q \in \mathbb{Z}_2$ (Lean 4 Theorem 14); non-split involutions $b_p = \begin{psmallmatrix}p & 1 \\ p+1 & -p\end{psmallmatrix}$ ($p \equiv 1 \pmod 4$) yield two disjoint $1$-parameter $\mathbb{Q}_2$-families.

**Theorem 5.2 (Universal Fricke–Vogt Law):** Every discrete embedding $\tilde{\Gamma} \hookrightarrow \mathrm{PGL}_2(L)$ acting properly on $T_3$ is determined up to conjugacy by $x = \tau(ta)$ ($v_2(x) = -1$), generates the ambient quaternion algebra

$$B(x) = \left(\frac{-3,\; x(x-3)}{\mathbb{Q}(x)}\right),$$

and satisfies exact universal trace polynomials $\tau(ta) = x$, $\tau(ta\cdot ta^2) = (x-1)^2$, $\tau((ta)^2 ta^2) = x(x-2)^2$, $\tau((ta)^3 ta^2) = (x^2-3x+1)^2$, and $\tau(\gamma_6) = (x^3 - 6x^2 + 9x - 2)^2$.

**Theorem 5.3 (Complete Rational Arithmetic Classification):** A rational modulus $x \in \mathbb{Q}$ produces an arithmetic Nauru curve $C_Y(x)/\mathbb{Q}_2$ over $\mathbb{Q}$ **if and only if** $x \in \{\frac{1}{2}, \frac{3}{2}, \frac{5}{2}\}$ (compactness $B(x)\otimes\mathbb{R}\cong\mathbb{H} \iff 0 < x < 3$; monic sextic integrality forces $x \in \mathbb{Z}[\frac{1}{2}]$; $v_2(x) = -1 \implies k \in \{1, 3, 5\}$, Lean 4 Theorem 15):

1. **$x = \frac{3}{2}$ in $B_3 = \left(\frac{-3,-1}{\mathbb{Q}}\right)$ ($D = 6$):** Maximal order $\mathcal{O}_3 = \mathbb{Z}[1,\omega,j,\omega j]$ (disc $3$), $t = (2\omega+1)(1+j)$ ($\operatorname{nrd} = 6$), Hensel-lifted $\mathbb{Q}_2$-embedding via $q = \frac{1+\sqrt{-7}}{2} \equiv 38 \pmod{64}$, shortest cadence $\gamma_6 = (ta)^6/27 = 4 - 3\omega + 3j - 3\omega j$ ($\operatorname{trd} = 11$, $\operatorname{nrd} = 64$, $\tau(\gamma_6) = \frac{121}{64} < 4$; Lean 4 Theorems 16–19).
2. **$x = \frac{5}{2}$ in $B_5 = \left(\frac{-3,-5}{\mathbb{Q}}\right)$ ($D = 10$):** Maximal order $\mathcal{O}_5 = \mathbb{Z}[1,\omega,t,\omega t]$ (disc $5$), $b = j$, $t = \frac{5i+k}{3}$ ($\operatorname{nrd} = 10$), $\tau(\gamma_6) = \frac{121}{64}$, $\tau(w_8) = \frac{169}{256}$.
3. **$x = \frac{1}{2}$ in $B_5 = \left(\frac{-3,-5}{\mathbb{Q}}\right)$ ($D = 10$):** Maximal order $\mathcal{O}_5 = \mathbb{Z}[1,\omega,t,\omega t]$, $b = j$, $t = \frac{i+k}{3}$ ($\operatorname{nrd} = 2$), $\gamma_6 = 7 + 5t + 5\omega t$ ($\operatorname{trd} = 9$, $\operatorname{nrd} = 64$, $\tau(\gamma_6) = \frac{81}{64} < 4$).
4. **Non-arithmetic rational witness ($x = \frac{9}{2}$):** $u = 0$ gives $t_0 = \begin{psmallmatrix}0 & 1 \\ -2 & 0\end{psmallmatrix}$, realizing $Y$ and $|\operatorname{Aut}| = 144$ with $\tau(\gamma_6) = \frac{4225}{64} \approx 66.02 > 4$.

---

## 6. Arithmetic Non-Congruence Shimura Covers and Borel-Level Exclusion

- **Theorem 6.1 (Explicit Non-Congruence Towers):**
  - At $x = \frac{3}{2}$ in $B_3$: $\Gamma_Y(\frac{3}{2}) \trianglelefteq_{V_4} \Gamma(3) \trianglelefteq_{18} \mathcal{O}_3[\frac{1}{2}]^1/\{\pm 1\} \trianglelefteq_2 \tilde{\Gamma}$, where $T_3/\Gamma(3) = K_{3,3}$ (genus-$4$ congruence Shimura curve $X^6(\Gamma(3))$). By Strong Approximation on $\mathrm{SL}_1(B_3)$, the congruence closure of $\Gamma(3)$ is $(1 + 3\mathcal{O}_{3,3})^1 \times \prod_{p \ge 5} \mathrm{SL}_2(\mathbb{Z}_p)$ (mod $\{\pm 1\}$), whose $p = 3$ factor is pro-$3$ and whose $p \ge 5$ factors are $2$-perfect (verified concretely by mod-$5$ joint surjection onto $\operatorname{Aut}(Y) \times A_5$ of order $8{,}640$). Thus **$\Gamma_Y(\frac{3}{2})$ is arithmetic yet non-congruence**.
  - At $x = \frac{5}{2}$ in $B_5$: $\Gamma_Y(\frac{5}{2}) \trianglelefteq_{\mathbb{Z}_3} \Gamma_{\mathrm{Cube}} \trianglelefteq_{\mathbb{Z}_2} \Gamma_5(3) \trianglelefteq_{S_4} \tilde{\Gamma}$, covering $X^{10}(\Gamma(3))$ ($K_4$, genus $3$) via $S_3$ through the cube $Q_3$ ($g = 5$), with mod-$9$ overlap $24$.
- **Theorem 6.2 (`NEG-M18` — Zero Borel-level realizations):** Zero-PARI Manin modular symbols $T_2$ across all $18$ distinct levels $M = DN/2 \in \{105, \dots, 345\}$ confirm `0/19` genus-$13$ Borel-level Shimura curves $X_0^D(N)$ over $\mathbb{Q}$ and `0/22` degree-$\le 4$ Brandt graphs match $Y$.

---

## 7. The $3$-Adic Companion $\mathrm{Dic}_6$ on $T_4$ and RCT Null Control

**Proposition 7.1:** $\mathrm{Dic}_6$ admits $18$ connected $4$-regular bipartite Cayley graphs of genus $25$ (uniformized on the $3$-adic Bruhat–Tits tree $T_4$ of $\mathrm{PGL}_2(\mathbb{Q}_3)$; $3$-adic arithmeticity open): $12$ are strictly Ramanujan at $\lambda_{\mathrm{nt}} = 3.000 < 2\sqrt{3} \approx 3.4641$ and $6$ lie on the exact boundary $2\sqrt{3}$. The canonical graph $Z = \mathrm{Cay}(\mathrm{Dic}_6, \{x, x^{-1}, y, y^3\})$ has girth $4$, $\mathbb{F}_3$-elliptic + $4\times(1+3u^2+9u^4)$ Ihara splitting, and Raynaud order $|K(Z)| = 429{,}923{,}020{,}800 = 2^{12}\cdot 3\cdot 5^2\cdot 7^2\cdot 13^4$.

**Keyed SplitMix64 RCT Control (`seed = 0x2ad1caa0125`, $N = 200$):** Random $24$-vertex $3$-regular bipartite graphs yield mean $\lambda_{\mathrm{nt}} = 2.5673$, min $\lambda_{\mathrm{nt}} = 2.3248$, $197/200$ Ramanujan, $1/200$ girth $\ge 6$, and **$0/200$** matching or beating Nauru's $\lambda_{\mathrm{nt}} = 2.000$ (bit-exact replay verified).

| Invariant | Tonnetz $X$ (Paper #01) | Nauru $Y = \mathrm{GP}(12, 5)$ | $\mathrm{Dic}_6$ Twin $Z$ |
| :--- | :--- | :--- | :--- |
| Bruhat–Tits tree | $T_3$ of $\mathrm{PGL}_2(\mathbb{Q}_2)$ | $T_3$ of $\mathrm{PGL}_2(\mathbb{Q}_2)$ | $T_4$ of $\mathrm{PGL}_2(\mathbb{Q}_3)$ |
| $\|V\| / \|E\| / g$ | $24 / 36 / 13$ | $24 / 36 / 13$ | $24 / 48 / 25$ |
| $\lambda_{\mathrm{nt}}$ vs. Ramanujan | $\sqrt{5} \approx 2.236 < 2\sqrt{2}$ | **$2.000 < 2\sqrt{2}$** | **$3.000 < 2\sqrt{3}$** |
| $\mathbb{F}_p$ Weil splitting | Octic ($g \ge 5$ req.) | **All $5/5$ $\mathbb{F}_2$-elliptic** | $\mathbb{F}_3$-ell. + $4\times g{=}2$ |
| Raynaud $\|K\|$ | $2^{15}\cdot 3^2\cdot 23^2$ | **$2^7\cdot 3^4\cdot 5^6$ ($5$-smooth)** | $2^{12}\cdot 3\cdot 5^2\cdot 7^2\cdot 13^4$ |
| Divisorial gonality | $6$ (non-reduced) | **$6$ (single prime hex)** | — |
| $\|\operatorname{Aut}(C)\|$ | $24$ | **$144 = 12(g - 1)$** | $4$-regular Cayley |
| Arithmetic over $\mathbb{Q}$? | No ($0$ anywhere) | **Yes: $x \in \{\frac{1}{2}, \frac{3}{2}, \frac{5}{2}\}$** | Open $3$-adic frontier |
| Congruence status | — | Non-congruence over $\Gamma(3)$ | Open |
