# Paper #08 (`PC-II`): Uniform Triadic Wreath Products, the Nauru Graph, and Dual-Prime $D = 6$ Arithmeticity

**Companion & Sequel to Paper #01 ([*Prime Cadences*](../../prime_cadences_paper.md))**

- **Read on GitHub (GFM mirror):** [`triadic_wreath_nauru.md`](triadic_wreath_nauru.md)
- **Canonical PDF (23 pp, 0 LaTeX warnings/hboxes, `v0.7.0` Complete Resolution):** [`paper/triadic_wreath_nauru.pdf`](paper/triadic_wreath_nauru.pdf)
- **AMS LaTeX & BibTeX source:** [`paper/triadic_wreath_nauru.tex`](paper/triadic_wreath_nauru.tex), [`paper/references.bib`](paper/references.bib), [`paper/triadic_wreath_nauru.bbl`](paper/triadic_wreath_nauru.bbl)
- **Neutral `0/0` arXiv bundle:** [`arxiv/triadic-wreath-nauru-arxiv.tar.gz`](arxiv/triadic-wreath-nauru-arxiv.tar.gz) (8 members, standalone compile verified)

## Summary of Main Results

1. **Fusion of Lewin $T/I$ and $PLR$ — But Not into Hook's UTT Wreath Product, and the Order-`1,152` Bifurcation (`NEG-M15`, `NEG-M16`, `NEG-M19`):**
   - $\langle T, PLR\rangle \cong (\mathbb{Z}_{12} \times D_{12})/\mathbb{Z}_2$ has order `144` ($|[G,G]| = 6$, $|G^{\mathrm{ab}}| = 24$) — the exact index-$2$ even-parity subgroup $\ker(\varepsilon)$ of $\mathrm{UTT} = \mathbb{Z}_{12} \wr \mathbb{Z}_2$.
   - Crans–Fiore–Satyendra duality fuses $T/I$ and $PLR$ into $\langle T/I, PLR\rangle \cong (D_{12} \times D_{12})/\mathbb{Z}_2 \not\cong \mathrm{UTT}$ (`288`), while $I_0 \notin \mathrm{UTT}$ normalizes $\mathrm{UTT}$ to generate $\mathrm{UTT}\rtimes\langle I_0\rangle$ (`576`), bifurcating into two non-isomorphic order-`1,152` extensions: $N_{\mathrm{Sym}(24)}(T) = N_{\mathrm{Sym}(24)}(\mathrm{UTT})$ (`247` involutions) vs. Hook's $Q\mathrm{UTT} \cong D_{12}\wr\mathbb{Z}_2$ (`219` involutions).
2. **Exhaustive 24-Subgroup UTT Census & Eisenstein–Nauru $\{6,3\}_{(2,2)}$ Recovery (`F31`):**
   - $PLR \cong D_{12}$ is unique for $3$-involution Coxeter triples (`168/192` Ramanujan); the split $M_5/M_7$ twists yield the **Nauru graph $Y = \mathrm{GP}(12, 5)$** ($\lambda_{\mathrm{nt}} = 2.000 < \sqrt{5} < 2\sqrt{2}$).
   - Closed-form $36/36$-edge isomorphism $\{6,3\}_{(2,2)} \cong Y$ on $\mathbb{Z}[\omega]/(2(1-\omega)) \cong \mathbb{F}_4 \times \mathbb{F}_3$ ($N = 12$; falsifier `F31` $N(2(1+\omega)) = 4$), whose $12$ dual Bloch momenta hit graphene Dirac cones $K, K'$ ($\lambda = 0^4$) and Van Hove $M$-points ($\lambda = \pm 1^3$), decomposing $S_{\mathrm{Nauru}} \subset \langle T, PLR\rangle$ ($s = T_6 \circ P$, $g = T_3 \circ (LR)^2$) with $+30.90\%$ spectral-gap gain $\Delta_Y/\Delta_X = (3+\sqrt{5})/4$.
3. **Complete Reversal of Paper #01's $2$-Adic Obstructions, All-Primes $B_3/B_5$ Classification, & Compact $\mathrm{SU}(2)$ Wilson Holonomy (`NEG-M17`, `NEG-M18`, `NEG-M23`):**
   - **$\mathbb{F}_2$ Weil splitting & Kernel-Checked Tropical Invariants:** All `5/5` $\mathbb{F}_2$ elliptic isogeny classes realized; exact unimodular $23\times 23$ SNF $K(Y) \cong (\mathbb{Z}/5)^3 \oplus \mathbb{Z}/30 \oplus \mathbb{Z}/120 \oplus \mathbb{Z}/360$ ($|K(Y)| = 162{,}000{,}000 = 2^7\cdot 3^4\cdot 5^6$, Lean 4 Theorem 34); exhaustive divisorial gonality $\operatorname{gon}(Y) = 6$ via single reduced prime hexagon $D_{\mathrm{hex}}$; $0/39$ tree-quotient involutions.
   - **Lamé Moduli & Complete All-Primes $B_3/B_5$ Classification (`NEG-M23`):** Rational arithmetic Nauru curves occur iff $x \in \{\frac{1}{2}, \frac{3}{2}, \frac{5}{2}\}$ inside $B_3 = (-3,-1)_{\mathbb{Q}}$ ($D = 6$) and $B_5 = (-3,-5)_{\mathbb{Q}}$ ($D = 10$): **$x = \frac{5}{2}$ IS a genuine congruence Shimura curve** $\Gamma_Y(\frac{5}{2}) = \Gamma(3)\cap\Gamma(\mathfrak{P}_5) = \Gamma(3\mathfrak{P}_5) \trianglelefteq_{A_4\times C_3} \mathcal{O}_5[\frac12]^1/\{\pm 1\}$ ($\mathfrak{P}_5\mid 5\mid 10$), whereas **$x = \frac{3}{2}$ ($B_3$) and $x = \frac{1}{2}$ ($B_5$)** are strictly **non-congruence $V_4$-covers** of $K_{3,3}$ (Lean 4 Theorem 36), excluding all `19/19` Borel $X_0^D(N)$ and `22/22` Brandt graphs.
   - **Intrinsic $\mathrm{SU}(2)$ Wilson actions:** Every definite arithmetic uniformization yields exact rational $S_W(w) = 1 - \frac12\sqrt{\tau(w)} \in \{\frac{5}{16}, \frac{7}{16}, \frac{19}{32}, \frac{4}{9}\} \subset (0, 1)$, strictly separated from all four non-arithmetic hyperbolic walls ($\tau > 4$).
4. **Complete $3$-Adic Arithmetic & Tropical Resolution of $\mathrm{Dic}_6$ via Hurwitz $B_2$ ($D = 6, p = 3$; `NEG-M20`, `NEG-M21`, `NEG-M22`, `F33`):**
   - `18` connected bipartite $4$-regular Cayley graphs ($g = 25$): `12` strictly Ramanujan $Z$ ($\operatorname{tr}(A^4) = 912, |\operatorname{Aut}(Z)| = 96, Z/\langle x^4\rangle \cong K_{4,4}, \lambda_{\mathrm{nt}} = 3 < 2\sqrt{3}$, exact kernel-checked SNF $K(Z) \cong \mathbb{Z}/4 \oplus (\mathbb{Z}/52)^2 \oplus \mathbb{Z}/1820 \oplus \mathbb{Z}/21840$ in Lean 4 Theorem 35, `43` involutions $\beta_1 \in \{7^2, 11^{24}, 13^{17}\}$, exact divisorial gonality $\operatorname{gon}(Z) = 8$ via exhaustive `157,166`-divisor Dhar burning + Lean 4 Theorem 37) vs. `6` boundary $C_{12}[2K_1]$. Canonical $3$-adic Schottky lift fails at $\tau(w_4) = \frac{1156}{81} > 4$ (`NEG-M21`).
   - Swapping primes in $D = 6$ to the Hurwitz algebra $B_2 = (-1,-1)_{\mathbb{Q}}$ ($p = 3$) builds an explicit arithmetic genus-$25$ Mumford curve $C_Z/\mathbb{Q}_3$ with corrected relator $w_4 = (t_y b)(t_x a)(b t_y)(t_x a)/4 = 5 + 6i - 2j + 4k$ ($\tau = \frac{100}{81} < 4, S_W = \frac{4}{9}$, falsifier `F33`), Hensel $s = \sqrt{-2} \equiv 356{,}989 \pmod{3^{12}}$, universal all-lengths $T_4$ freeness, exact `32` surjections splitting `16/16` into $\Gamma(4)$ vs. level-$8\mathcal{O}_2$ inside $\mathcal{O}_2[\frac13]^1/\{\pm 1\} \trianglelefteq_4 \mathrm{Norm}_{B_2^\times}(\mathcal{O}_2[\frac13])/\mathbb{Q}^\times$ (`NEG-M22`) with universal double-coset congruence quotient $K_{4,4}$, constructive normality $q_{x^4} \in H_8$ across `32/32`, permanent mod-$16$ stabilization $|H_{16}|=64$, full mod-$5$ $A_5$ surjection (`|H_5|=60`, strict non-congruence cyclic $C_3$-cover index `3`), and `0/19` genus-$25$ $3$-adic Borel Shimura realizations via Manin $T_3$ (`NEG-M20`).

## Three-Plane Zero-Shared-Data Verification

| Plane | Path | License | Scope & Result |
| :--- | :--- | :--- | :--- |
| **Pure Python (zero deps)** | [`code/triadic_nauru_verify.py`](code/triadic_nauru_verify.py) | MIT | **15/15 D/R/P/Seam gates PASS** (incl. all-primes $B_3/B_5$ `NEG-M23`, exact `K(Z)` SNF, `43` involutions, `157,166`-divisor Dhar $\operatorname{gon}(Z)=8$, Eisenstein–Nauru `36/36`, $\mathrm{SU}(2)$ Wilson, Hurwitz $B_2$ `32` surj / $K_{4,4}$ / $q_{x^4} \in H_8$ / mod-16 / mod-5, 19-pair $3$-adic Manin $T_3$, `--check-only` & `--no-figs` modes) |
| **Lean 4.36.0 (zero Mathlib)** | [`lean/TriadicNauru/Core.lean`](lean/TriadicNauru/Core.lean), [`lean/TriadicNauru/SnfCertificates.lean`](lean/TriadicNauru/SnfCertificates.lean) | MIT | **37/37 theorems kernel-checked** (`0 sorryAx`, `0 Lean.ofReduceBool`, incl. direct $23\times 23$ unimodular SNF `thm34`–`thm35`, $B_5$ arithmetic `thm36`, constructive Dhar $\operatorname{gon}(Z)\le 8$ + 6-ring `thm37`) |
| **Pure Rust (zero crates)** | [`rust/src/lib.rs`](rust/src/lib.rs) | MIT | **11/11 integration tests + 10/10 core suites PASS** (`1.09s` release) |
| **Data Model (SHA-256)** | [`data/triadic_nauru_calibration.json`](data/triadic_nauru_calibration.json) | CC BY 4.0 | Immutable calibration record (`schema_version 1.2.0`) verified by repo-root-relative [`data/MANIFEST.sha256`](data/MANIFEST.sha256) |

### Reproduce Locally

```bash
python3 papers/triadic_wreath_nauru/code/triadic_nauru_verify.py --check-only
sha256sum -c papers/triadic_wreath_nauru/data/MANIFEST.sha256
(cd papers/triadic_wreath_nauru/lean && lake build && .lake/build/bin/triadic-nauru-lean)
(cd papers/triadic_wreath_nauru/rust && cargo test --release && cargo run --release)
```
