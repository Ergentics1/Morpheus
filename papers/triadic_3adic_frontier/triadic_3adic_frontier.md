# The 3-Adic Dicyclic Companion, Exact Level $3\mathfrak{P}_5$ and Level $(3)$ Congruence on Nauru, and the Real-Quadratic Lamé Shimura Curve Atlas

**Paper #09 (`PC-III`)** · **Companion & Sequel to Paper #01 ([*Prime Cadences*](../../prime_cadences_paper.md), `v0.3.1`) and Paper #08 ([`PC-II`](../triadic_wreath_nauru/triadic_wreath_nauru.md), `v0.7.1`)**  
**Author:** Ergentics · **Date:** November 2026 · **License:** Paper & Data [CC BY 4.0](../../LICENSE-paper) · Code [MIT](../../LICENSE)  
**Canonical PDF:** [`paper/triadic_3adic_frontier.pdf`](paper/triadic_3adic_frontier.pdf) · **LaTeX Source:** [`paper/triadic_3adic_frontier.tex`](paper/triadic_3adic_frontier.tex) · **arXiv Bundle:** [`arxiv/triadic-3adic-frontier-arxiv.tar.gz`](arxiv/triadic-3adic-frontier-arxiv.tar.gz)

---

## Abstract

We resolve the higher-degree arithmetic, tropical-metric, $3$-adic moduli, and explicit-formula frontiers opened by *Prime Cadences* (Paper #01, `v0.3.1`) and its companion *Uniform Triadic Wreath Products, the Nauru Graph, and Dual-Prime $D=6$ Arithmeticity* (Paper #08 / `PC-II`, `v0.7.1`), backed by four independent zero-shared-data continuous-integration verification planes (**Pure Python**, **Zero-Crate Rust**, **Zero-Heap Hardware-`FENV` C++20**, and **Live Kernel-Compiled Zero-Mathlib Lean 4.36.0**).

1. **Pillar I (Rational $2$-Adic Nauru Congruence, Twin Duality & Metric Gonality):** We prove universal algebraic twin duality $\tau((bt)a) = 3 - x$ on $B(x) = (-3, -x(3-x)/F)$ swapping $\rho_6 \leftrightarrow \rho_{12}$, separate the genuine level-$3\mathfrak{P}_5$ congruence Shimura curve $(B_5, \frac{5}{2}, \rho_6) \cong (B_5, \frac{1}{2}, \rho_{12})$ ($|\mathrm{Ad}_{15}| = |\mathrm{joint}| = 3{,}600 = 144\times 25$, unique normal Sylow-$5$ $U_5$ annihilated since $\gcd(25, 144) = 1$) from both non-congruence $V_4$-covers ($B_3(\frac{3}{2}) \to X^6(\Gamma(3)) \leftrightarrow K_{3,3}$ at level $3$ vs. $(B_5, \frac{1}{2}, \rho_6) \to X^{10}(\Gamma(3\mathfrak{P}_5))/V_4 \leftrightarrow K_{3,3}$ only at level $3\mathfrak{P}_5$), re-certify all historical `PC-II` errata repairs (`NEG-M19`, `NEG-M23`, `NEG-M24`: $\pi_Y(18)=28{,}560$, $\pi_Y(22)=380{,}664$, $|[G,G]|/|G^{\mathrm{ab}}|=6/24$), and prove unconditional metric gonality $\operatorname{sn}(Y) = \operatorname{dgon}(Y) = \operatorname{gon}(\Gamma_{\mathrm{eq}}(Y)) = 6 \le \operatorname{gon}(\Gamma(Y)) \le \operatorname{gon}(\mathcal{C}_Y)$ via $132/132$ continuous Dhar cells.
2. **Pillar II (Complete Real-Quadratic & Cubic Lamé Nauru Atlas, `NEG-M25`):** We classify all $6$ primitive real-quadratic moduli across $4$ fields—all with $\mathrm{Ram}_{\mathrm{fin}}(B(x)) = \varnothing$—and resolve every field's exact congruence status: non-congruence $\mathbb{Z}/3\mathbb{Z}$-cover of the Cube Shimura curve $X^{17}(\Gamma(v^2)) \leftrightarrow Q_3$ over $\mathbb{Q}(\sqrt{17})$; strictly non-congruence Eichler-$\mathfrak{q}_7$ cover of $X^1(\mathfrak{q}_7) \leftrightarrow \Theta_3$ over $\mathbb{Q}(\sqrt{2})$ ($\mathcal{E}(\mathfrak{q}_7)$, $T_8\text{-}\det = 49\cdot 8^4$, non-isomorphic Galois kernels $C_6 \times C_2$ vs. $A_4$, obstructed by $4 \nmid 1$); strictly non-congruence over $\mathbb{Q}(\sqrt{3})$ via Eichler-$\mathfrak{p}_3$ $2$-part obstruction ($|\mathrm{Ad}_3^1|=243, |\mathrm{Ad}_3^+|=486, |\mathrm{Ad}_3|=972$); and a **second genuine congruence Shimura curve of exact level $(3) = \mathfrak{p}_3\mathfrak{p}_3'$ for BOTH $\rho_6$ and $\rho_{12}$ over $\mathbb{Q}(\sqrt{7})$** ($|\mathrm{Ad}_{(3)}| = |\mathrm{joint}| = 576$, $|\ker| = 1$, $144/144$), alongside the complete census of all $4$ irreducible totally real cubic moduli ($d_F \in \{148, 316\}$).
3. **Pillar III (Complete Rational $3$-Adic $\mathrm{Dic}_6$ Frontier on $T_4(\mathbb{Q}_3)$, `NEG-M26`):** We classify all $18$ connected $4$-regular $\mathrm{Dic}_6$ Cayley graphs ($12$ strictly Ramanujan $Z$ with exact $\pi_Z(4..16)$, $6$ boundary), collapse metric gonality $\operatorname{sn}(Z) = \operatorname{dgon}(Z) = \operatorname{gon}(\Gamma_{\mathrm{eq}}(Z)) = 8 \le \operatorname{gon}(\Gamma(Z)) \le \operatorname{gon}(\mathcal{C}_Z)$ via the optimal $4$-path scramble $\mathcal{S}_4$ ($h = e = 8$, $276/276$ touching, $156$ Edmonds–Karp cuts `{8: 48, 10: 108}`), exhaustive Dhar (`0/98,280` deg 6, `0/475,020` deg 7), and $168/168$ continuous metric Dhar cells on both $D_8 = \langle x^3\rangle + \langle x^3\rangle y$ and `PC-II`'s $D_{\mathrm{Dic}_6}$, classify all $5/10$ rational arithmetic Fricke–Vogt moduli $B_Z(u,v)$ via $4 \mid mn$, prove universal rational non-congruence (`0/80` realizations across both modular adjoint and diagonal-$\pm 1$ CRT true left-multiplication $\Gamma(M)$, closed unconditionally at all levels via Riehm's theorem and Burnside's Basis Theorem), reconcile Hurwitz $B_2(4,4)$ level-$8$ true left-multiplication ($|L_8/\{\pm 1\}| = 64$ already attains $|\ker^1| = 3$ across $16/16$, matching `PC-II` Thm 7.2) with level-$16$ adjoint ($\mathrm{Ad}_{16} = 1{,}024$), and pair the $19$-curve ($9$ torsion-free) genus-$25$ Borel Shimura census with `PC-II` Theorem 7.3's `0/19` Manin $T_3$ exclusion (`NEG-M20`).
4. **Section 5 (Hardware-`FENV` Poitou–Odlyzko Strict-Positivity Audit, `NEG-M27`):** We certify witness $(6,16,1,2)$ via hardware `FE_DOWNWARD`/`FE_UPWARD` outward intervals ($18.6606783717 > 18.6470485626$, gap $\ge +0.013629809157 > 0$), reject sign-changing facade kernels ($f_{\mathrm{bad}}(\pm 1) = -0.60 < 0$), and preserve the degree-$8$ $(8,1,1,E)$ gap ($12.5937296518$ at $b = 3.0$, exact continuous peak $12.5955757277$ at $b^* = 3.039865 < 13.1423854579$).

---

## 1. Summary Table

| Track | Principal Object | Headline Resolution | CI Planes |
| :--- | :--- | :--- | :--- |
| **Pillar I** | Rational $2$-adic Nauru $Y$ | Twin duality $\tau((bt)a)=3-x$; level $3\mathfrak{P}_5$ cong. $(B_5, \frac{5}{2}, \rho_6)$ (`3600`, $\gcd(25,144)=1$); $B_3(\frac{3}{2}) \to X^6(\Gamma(3))$ vs. $B_5(\frac{1}{2}, \rho_6) \to X^{10}(\Gamma(3\mathfrak{P}_5))/V_4$; $\pi_Y(18)=28{,}560, \pi_Y(22)=380{,}664$; $\operatorname{sn}=\operatorname{dgon}=\operatorname{gon}_{\mathrm{eq}}=6$ (`132/132` cells) | Py, Rust, C++, Lean |
| **Pillar II** | Real-quadratic & cubic Lamé atlas | $6$ real-quad moduli ($4$ fields, $\mathrm{Ram}_{\mathrm{fin}}=\varnothing$): $\mathbb{Q}(\sqrt{17})$ ($Q_3$, `ker=3`), $\mathbb{Q}(\sqrt{2})$ ($\mathcal{E}(\mathfrak{q}_7) \to \Theta_3$, $C_6 \times C_2 / A_4$, $4 \nmid 1$), $\mathbb{Q}(\sqrt{3})$ ($\mathcal{E}(\mathfrak{p}_3)$, $2$-part $1<4$), **$\mathbb{Q}(\sqrt{7})$ CONG level $(3)$** (`576`, `144/144` both $\rho_6, \rho_{12}$); $4$ cubic moduli ($d_F \in \{148, 316\}$) | Py, Rust, Lean |
| **Pillar III** | $3$-adic $\mathrm{Dic}_6$ on $T_4(\mathbb{Q}_3)$ | $18$ Cayley ($12$ Ram. $Z$, $6$ bnd.); $\pi_Z(4..16)$; $\operatorname{sn}=\operatorname{dgon}=\operatorname{gon}_{\mathrm{eq}}=8$ ($\mathcal{S}_4$, $D_8$, `0/475,020` deg 7); $5/10$ Fricke–Vogt ($4 \mid mn$); `0/80` cong. (CRT $\Gamma(M)$ + Riehm mod 8); Hurwitz $L_8/\{\pm 1\}=64$ vs. $\mathrm{Ad}_{16}=1024 \to K_{4,4}$; $19$ ($9$ TF) genus-25 (`0/19` by `PC-II` Thm 7.3) | Py, Rust, C++, Lean |
| **Audit** | Poitou–Odlyzko `FENV` gate | Strict Bochner pos. `18.6606783717 > 18.6470485626` (gap $\ge +0.013629809157$); $f_{\mathrm{bad}}(\pm 1) = -0.60$ rejected; $(8,1,1,E)$ gap preserved (`12.593730` at $b=3.0$, continuous peak `12.595576` at $b^*=3.0399 < 13.142385$) | Py, Rust, C++ `FENV` |

---

## 2. Pillar I: Rational $2$-Adic Nauru Congruence, Twin Duality & Metric Gonality

### Proposition 2.1 (Universal Algebraic Twin Duality $\tau((bt)a) = 3 - x$) `[E; G4N, X, Lean 4]`
In $B(x) = (-3, -x(3-x)/F)$ ($a = \frac{1+i}{2}, b = j, t = ui + vk$ commuting with $b$ in $PB^\times$),
$$\tau(ta) = \frac{3u^2}{u^2 - Bv^2} = x, \qquad \tau((bt)a) = \frac{-3Bv^2}{u^2 - Bv^2} = 3 - x.$$
Taking $t = xi + k$ ($\operatorname{nrd}(t) = 9x$) and substituting $t \mapsto bt$ swaps the two edge-inverting surjections $\rho_6 \leftrightarrow \rho_{12}$ (`ord(t_0 a_Y) = 6`, `ord(t_1 a_Y) = 12`), giving canonical isomorphisms $(B(x), \rho_6) \cong (B(3-x), \rho_{12})$.

### Theorem 2.2 (Exact Level $3\mathfrak{P}_5$ Congruence & Separation of Rational $V_4$-Covers) `[E; G4N, X, Lean 4]`

| Curve $(B, x)$ | Mod $M$ | $|\mathrm{Ad}_M|$ | Joint $\rho_6$ | $\ker \rho_6$ | Ovlp $\rho_6$ | Joint $\rho_{12}$ | $\ker \rho_{12}$ | Ovlp $\rho_{12}$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $B_3$, $x=\frac{3}{2}$ ($D=6$) | $3$ | `36` | `144` | `4 (V_4)` | `36/144` | `144` | `4 (V_4)` | `36/144` |
| $B_3$, $x=\frac{3}{2}$ ($D=6$) | $9$ | `972` | `3,888` | `4 (V_4)` | `36/144` | `3,888` | `4 (V_4)` | `36/144` |
| $B_3$, $x=\frac{3}{2}$ ($D=6$) | $15$ | `2,160` | `8,640` | `4 (V_4)` | `36/144` | `8,640` | `4 (V_4)` | `36/144` |
| $B_5$, $x=\frac{5}{2}$ ($D=10$) | $3$ | `24` | `144` | `6` | `24/144` | `576` | `24` | `6/144` |
| $B_5$, $x=\frac{5}{2}$ ($D=10$) | $5$ | `300` | `3,600` | `12` | `12/144` | `3,600` | `12` | `12/144` |
| **$B_5$, $x=\frac{5}{2}$ ($D=10$)** | **$15$** | **`3,600`** | **`3,600`** | **`1 (CONG)`** | **`144/144`** | `14,400` | `4 (V_4)` | `36/144` |
| $B_5$, $x=\frac{1}{2}$ ($D=10$) | $3$ | `24` | `576` | `24` | `6/144` | `144` | `6` | `24/144` |
| $B_5$, $x=\frac{1}{2}$ ($D=10$) | $5$ | `300` | `3,600` | `12` | `12/144` | `3,600` | `12` | `12/144` |
| **$B_5$, $x=\frac{1}{2}$ ($D=10$)** | **$15$** | **`3,600`** | `14,400` | `4 (V_4)` | `36/144` | **`3,600`** | **`1 (CONG)`** | **`144/144`** |

- **$(B_5, \frac{5}{2}, \rho_6) \cong (B_5, \frac{1}{2}, \rho_{12})$:** Genuine congruence Shimura curve of exact level $3\mathfrak{P}_5$ (`|U_5| = 25`, $\gcd(25, 144) = 1$, Lean 4 `thm13`).
- **$B_3(\frac{3}{2})$ vs. $(B_5, \frac{1}{2}, \rho_6)$:** Both have congruence kernel $V_4$ and dual quotient $Y/V_4 \cong K_{3,3}$ ($V=6, E=9\times 4$), but $B_3(\frac{3}{2})$ covers $X^6(\Gamma(3))$ already at level $3$, while $(B_5, \frac{1}{2}, \rho_6)$ reaches only `6/144` (`overlap1 = 3/36`, `|Ad_3^1| = 12`) at level $3$ and reaches `36/144` (`overlap1 = 9/36`, `|Ad_15^1| = 900`) only at level $3\mathfrak{P}_5$, covering $X^{10}(\Gamma(3\mathfrak{P}_5))/V_4$.

### Propositions 2.3 & 2.4 (Nauru Cadences, $\langle T,P,L,R\rangle$, & Unconditional Metric Gonality) `[E; G4N, X, Lean 4]`
- Exact Nauru cadences $\pi_Y(6..24) = (24, 108, 216, 564, 2232, 8820, \mathbf{28560}, 104292, \mathbf{380664}, 1401744)$; at $m = 18$, $N_{18}(Y) = 514{,}224 \in [501{,}786, 546{,}842]$ whereas the historical `31,824` forces $572{,}976 > 546{,}842$ (`NEG-M24`, Lean 4 `thm14`).
- $\langle T, P, L, R\rangle \cong (\mathbb{Z}/12\mathbb{Z} \times D_{12})/\langle(6, (LR)^6)\rangle$ has order `144`, $|[G,G]| = 6$, $|G^{\mathrm{ab}}| = 24$ (Lean 4 `thm18`, `thm19`).
- The $24$-star scramble on $Y$ has $h = 6$ (`4` exact 1-perfect codes incl. `{3,7,11,13,17,21}`) and uniform Edmonds–Karp egg-cut $e = 6$ (`{6: 168}`), while $D_{\mathrm{hex}} = \{0,1,2,14,19,12\}$ passes all `24 + 108 = 132/132` continuous equilateral metric Dhar cells ($\le 3$ steps):
  $$\operatorname{sn}(Y) = \operatorname{dgon}(Y) = \operatorname{gon}(\Gamma_{\mathrm{eq}}(Y)) = 6 \le \operatorname{gon}(\Gamma(Y)) \le \operatorname{gon}(\mathcal{C}_Y).$$

---

## 3. Pillar II: Complete Real-Quadratic & Cubic Lamé Nauru Atlas (`NEG-M25`)

### Proposition 3.1 & Theorem 3.2 (All 6 Real-Quadratic Moduli & $\mathbb{Q}(\sqrt{7})$ Level $(3)$ Breakthrough) `[E; G4N, X, Lean 4]`

| Field ($D_F$) | Modulus Polynomial(s) | $\zeta_F(-1)$ | $2,3$ Split | $\mathrm{Ram}_{\mathrm{fin}}$ | Verdict | Exact Obstruction / Level Certificate |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| $\mathbb{Q}(\sqrt{17})$ (`17`) | $2x^2-5x+1,\; 2x^2-7x+4$ | `1/3` | split, inert | $\varnothing$ | Non-cong | $\mathcal{O}_{17}^{\max}\bmod v^2$: `|Ad|=48, |ker|=3`, $Y/C_3 \cong Q_3$ (Lean 4 `thm08`); $\mathrm{SL}_2(\mathbb{F}_9)$ perfect |
| $\mathbb{Q}(\sqrt{2})$ (`8`) | $2x^2-4x+1,\; 2x^2-8x+7$ | `1/12` | ram, inert | $\varnothing$ | Non-cong | $\mathcal{E}(\mathfrak{q}_7)$ ($T_8\text{-}\det = 49\cdot 8^4$): `|Ad|=588, |Ad^1|=147, |ker|=12`, $Y/\ker_{12} \cong \Theta_3$ with non-isomorphic kernels $C_6 \times C_2$ ($\rho_6$) vs. $A_4$ ($\rho_{12}$); 2-part $4 \nmid 1$ (Lean 4 `thm15`) |
| $\mathbb{Q}(\sqrt{3})$ (`12`) | $2x^2-6x+3$ (self-twin) | `1/6` | ram, ram | $\varnothing$ | Non-cong | $\mathcal{E}(\mathfrak{p}_3)$ ($T_8\text{-}\det = 9\cdot 12^4$): `|Ad^1|=243` ($1<4$), `|Ad^+|=486` ($2<8$), `|Ad|=972` ($4<16$, `|ker|=4`, Lean 4 `thm15`) |
| **$\mathbb{Q}(\sqrt{7})$ (`28`)** | **$2x^2-6x+1$ (self-twin)** | **`2/3`** | **ram, split** | **$\varnothing$** | **CONG $(3)$** | **$\mathcal{O}_7^{\max}\bmod (3)=\mathfrak{p}_3\mathfrak{p}_3'$: `|Ad|=|joint|=576, |ker|=1` (`144/144` for BOTH $\rho_6, \rho_{12}$)** |

### Proposition 3.3 (Complete Totally Real Cubic Census) `[E; G4N, X]`
Exactly $4$ primitive irreducible totally real cubic moduli $2x^3 - c_2 x^2 + c_1 x - c_0 = 0$ have all three roots in $(0, 3)$:
1. $d_F = 316$ ($2 = v_1 v_2^2$): $2x^3 - 9x^2 + 10x - 1$ ($z \equiv 2 \bmod 16$) and $2x^3 - 9x^2 + 10x - 2$ ($z \equiv 10 \bmod 16$).
2. $d_F = 148$ ($2 = v^3$): $2x^3 - 8x^2 + 8x - 1$ and $2x^3 - 10x^2 + 14x - 5$ (zero reciprocal roots mod $16$).

---

## 4. Pillar III: Complete Solution of the Rational $3$-Adic $\mathrm{Dic}_6$ Frontier on $T_4(\mathbb{Q}_3)$

### Theorems 4.1 & 4.2 (Cayley Dichotomy, $\pi_Z(4..16)$, & Unconditional Metric Gonality Collapse $8$) `[E; G4N, X, Lean 4]`
- `18/55` connected $4$-regular $\mathrm{Dic}_6$ Cayley graphs: `12` Ramanujan $Z$ ($\det(xI - A_Z) = x^6(x^2-16)(x^2-9)^2(x^2-3)^4(x^2-1)^2$, $|\mathrm{Aut}(Z)|=96$, $\lambda_{\mathrm{nt}}=3<2\sqrt{3}$) + `6` boundary ($\lambda_{\mathrm{nt}}=2\sqrt{3}$).
- Exact $96\times 96$ Hashimoto prime cadences: $\pi_Z(4..16) = (60, 240, 1560, 11616, 90172, 681504, 5379960)$ (normalized deviations $\in [-0.26, +0.60]$).
- All `43` involutions in $\mathrm{Aut}(Z)$ satisfy $\beta_1(Z/\langle\sigma\rangle) \in \{7^2, 11^{24}, 13^{17}\}$ (never hyperelliptic).
- Exhaustive Dhar certifies `0/98,280` rank-$1$ divisors at degree $6$ and `0/475,020` at degree $7$ (Rust + zero-heap C++20).
- Optimal $4$-path scramble $\mathcal{S}_4$ ($E_0 = \{0,1,2,20\}$): `24` distinct eggs, `276/276` touching (`120` intersecting, `156` disjoint; Lean 4 `thm04`), $h(\mathcal{S}_4) = 8$ (witness `{0,1,2,5,8,17,19,23}`, Lean 4 `thm05`), Edmonds–Karp cuts `{8: 48, 10: 108}` ($e(\mathcal{S}_4) = 8$).
- Both $D_8 = \langle x^3\rangle + \langle x^3\rangle y = \{0,3,6,9,12,15,18,21\}$ ($\le 2$ steps, Lean 4 `thm06`) and `PC-II`'s $D_{\mathrm{Dic}_6} = \{0,1,6,7,12,13,18,19\}$ ($\le 3$ steps) pass all `168/168` continuous equilateral metric Dhar cells:
  $$\operatorname{sn}(Z) = \operatorname{dgon}(Z) = \operatorname{gon}(\Gamma_{\mathrm{eq}}(Z)) = 8 \le \operatorname{gon}(\Gamma(Z)) \le \operatorname{gon}(\mathcal{C}_Z).$$

### Theorems 4.3 & 4.4 (Fricke–Vogt $4 \mid mn$, `0/80` CRT Non-Congruence, Hurwitz Level-$8$ vs. $\mathrm{Ad}_{16}$ Reconciliation `NEG-M26`, & Riehm Closure) `[E; G4N, X, Lean 4]`
In $B_Z(u,v) = (-\frac{1-u}{u}, -\frac{1-v}{v}/\mathbb{Q})$ ($u=\frac{m}{12}, v=\frac{n}{12}$), $\tau(t_x t_y) = \frac{(12-m)(12-n)}{36} \in \mathbb{Z}[\frac{1}{3}] \iff 4 \mid mn$ (Lean 4 `thm11`–`thm12`), leaving exactly $5/10$ canonical curves:

| $(m,n)$ | Curve $(D,N)$ | HNF `rd` | CRT Moduli (Sylow-reduced) | $|\prod L|$ (pre-$\pm 1$) | Proj. Order | $\Gamma^1\ \ker^1$ | Cong |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| `(4,4)` | $B_2$ Hurwitz `(2,1)` | `2` | `16: 1024` (already `8: 128`, proj. `64`) | `1,024` | `512` | `{3: 16}` | `0/16` |
| `(2,4)` | $B_5(2)$ `(5,2)` | `10` | `16: 2048; 5: 150 → 6` | `12,288` | `6,144` | `{6: 16}` | `0/16` |
| `(4,5)` | $B_{70}$ `(70,1)` | `70` | `8: 768; 5: 150 → 6; 7: 392 → 8` | `36,864` | `18,432` | `{2: 8, 6: 8}` | `0/16` |
| `(2,2)` | $B_2(5)$ `(2,5)` | `10` | `8: 768; 5: 100 → 4` | `3,072` | `1,536` | `{12: 16}` | `0/16` |
| `(1,4)` | $B_2(11)$ `(2,11)` | `22` | `8: 768; 11: 1210 → 10` | `7,680` | `3,840` | `{4: 8, 12: 8}` | `0/16` |

- **Hurwitz Level-$8$ vs. $\mathrm{Ad}_{16}$ Reconciliation (`NEG-M26`):** Under adjoint action $\mathrm{Ad}_M$, $[\mathcal{O}_2, \mathcal{O}_2] \subseteq \mathfrak{P}_2$ absorbs a factor of $2$, so `Ad_4 (32)` and `Ad_8 (128)` both give `{3: 8, 6: 8}` and only `Ad_16 (1024)` reaches `{3: 16}`. Under true left-multiplication $\Gamma(M)$, **`L_8/\{\pm 1\}` (`order 64`, signed `128`) ALREADY attains `ker^1 = {3: 16}`** (`8` at level 4 + `8` at level 8, matching `PC-II` Thm 7.2's `16/16` split across all `32 = 2×16` surjections), stabilizing identically at `L_16/\{\pm 1\}` (`512`). All `16/16` cover $Z/C_3 \cong K_{4,4}$ (Lean 4 `thm07`).
- **All-Level Closure:** All `80/80` realizations have unique normal $C_3 \trianglelefteq \rho(\Delta_Z^1)$ (`ord3 = 2`). For $B_{70}, B_2(5), B_2(11)$, Riehm's theorem (`O_70^1 mod 8`: `|G|=768, |[G,G]|=256, |G^ab|=3, -I ∈ [G,G]`) + Burnside's Basis Theorem forces $\varphi(P_2) = 1$ at every level $2^k$.
- **Genus-25 Borel Census (Prop 4.5):** Exactly `19` curves (`16` at $\omega=2$ with `8` TF, `3` at $\omega=4$ with `1` TF `(1110, 1)`, `0` at $\omega \ge 6$ since $\varphi(30030)=5760>600$, Lean 4 `thm17`); all `19/19` are already excluded for $Z$ by `PC-II` Theorem 7.3's zero-PARI Manin $T_3$ audit (`NEG-M20`).

---

## 5. Poitou–Odlyzko Strict-Positivity Audit (`NEG-M27`) & Open Frontier

- **Witness `(6,16,1,2)` (`b = 6.0`):** Hardware `FENV` outward interval certifies $\exp(\mathrm{LB}) - \mathrm{UB}(6,16) \in [+0.013629809157, +0.013629809162] > 0$ (`18.66067837170957 > 18.64704856255016`, `|GL64 - GL128| <= 1.43e-14`).
- **Anti-Facade Gate:** Sign-changing $f_{\mathrm{bad}}(t)$ (`c_1 = -0.3, c_2 = +0.3`) attains $f_{\mathrm{bad}}(\pm 1) = -0.60 < 0$ and is deterministically rejected across Python, Rust, and C++20 `FENV`.
- **Degree-8 `(8,1,1,E)` Gap Honesty:** $\mathrm{UB}_{\max}(8,1) = 13.1423854579$. Under $H_1$, $\exp(\mathrm{LB})$ gives `12.5937296518` at $b = 3.0$ and attains its exact continuous optimum **`12.5955757277`** at **`b* = 3.039865`** (margin `> 0.5468` below ceiling).

### Genuine Open Frontier (3 Problems)
1. **Congruence status of the $4$ totally real cubic Lamé Nauru curves** ($d_F \in \{148, 316\}$) via $\mathbb{Z}$-rank-$12$ maximal orders.
2. **Real-quadratic $3$-adic $\mathrm{Dic}_6$ moduli** $(u,v)$ on the Fricke–Vogt surface $B_Z(u,v)$.
3. **New arithmetic input beyond Bochner-positive Poitou–Odlyzko test functions** to close the degree-$8$ $(8,1,1,E)$ gap in Paper #01 Theorem 7.21.
