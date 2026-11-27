# Paper #08 (`PC-II`): Uniform Triadic Wreath Products, the Nauru Graph, and $2$-Adic Arithmeticity

**Companion & Sequel to Paper #01 ([*Prime Cadences*](../../prime_cadences_paper.md))**

- **Read on GitHub (GFM mirror):** [`triadic_wreath_nauru.md`](triadic_wreath_nauru.md)
- **Canonical PDF (15 pp, 0 LaTeX warnings/hboxes):** [`paper/triadic_wreath_nauru.pdf`](paper/triadic_wreath_nauru.pdf)
- **AMS LaTeX & BibTeX source:** [`paper/triadic_wreath_nauru.tex`](paper/triadic_wreath_nauru.tex), [`paper/references.bib`](paper/references.bib), [`paper/triadic_wreath_nauru.bbl`](paper/triadic_wreath_nauru.bbl)
- **Neutral `0/0` arXiv bundle:** [`arxiv/triadic-wreath-nauru-arxiv.tar.gz`](arxiv/triadic-wreath-nauru-arxiv.tar.gz) (standalone compile verified)

## Summary of Main Results

1. **Non-Fusion of Lewin $T/I$ and $PLR$ vs. Hook's UTT Wreath Product (`NEG-M15`, `NEG-M16`):**
   - $\langle T, PLR\rangle$ has order `144` — the exact index-$2$ even-parity subgroup $\ker(\varepsilon)$ of $\mathrm{UTT} = \mathbb{Z}_{12} \wr \mathbb{Z}_2$, missing odd-parity elements such as Hook's order-$24$ Hamiltonian cycle $Q = \langle -, 1, 0 \rangle$.
   - $\langle T/I, PLR\rangle \cong (D_{12} \times D_{12}) / \mathbb{Z}_2$ has order `288`, **neither equal nor isomorphic** to $\mathrm{UTT}$ ($|Z| = 2$ vs. $12$, $99$ vs. $15$ involutions, $0$ vs. $48$ order-$24$ elements, $|[G,G]| = 18$ vs. $12$). Instead, $I_0 \notin \mathrm{UTT}$ normalizes $\mathrm{UTT}$ via $I_0 \langle \sigma, t^+, t^-\rangle I_0^{-1} = \langle \sigma, -t^-, -t^+\rangle$, generating $\mathrm{UTT} \rtimes \langle I_0 \rangle$ (order `576`) inside $N_{\mathrm{Sym}(24)}(T) = \mathrm{UTT} \rtimes \mathbb{Z}_{12}^\times$ (order `1,152`).
2. **Exhaustive 24-Subgroup UTT Census & Nauru Emergence:**
   - All `24` simply transitive order-$24$ subgroups of $\mathrm{UTT}$ partition into `8` isomorphism classes indexed by $u \in \mathbb{Z}_{12}^\times = \{1, 5, 7, 11\}$.
   - $PLR \cong D_{12}$ is **unique** for $3$-involution Coxeter triples (`192` total, `168` bipartite Ramanujan, `24` non-bipartite failing at $1 + 2\cos(\pi/12) \approx 2.932$); every cubic Cayley graph of $\mathbb{Z}_{24}$ fails Ramanujan.
   - The split $M_5$ ($S_3 \times \mathbb{Z}_4$) and $M_7$ ($\mathbb{Z}_3 \times D_4$) Galois twists canonically construct the **Nauru graph $Y = \mathrm{GP}(12, 5)$** via $S_{\mathrm{Nauru}} = \{\langle -,6,6\rangle, \langle +,1,5\rangle, \langle +,11,7\rangle\}$ with sharper Ramanujan gap $\lambda_{\mathrm{nt}} = 2.000 < \sqrt{5} < 2\sqrt{2}$.
3. **Complete Reversal of Paper #01's $2$-Adic Obstructions:**
   - **$\mathbb{F}_2$ Weil splitting:** $100\%$ quadratic elliptic splitting hitting **all 5/5** elliptic curve isogeny classes over $\mathbb{F}_2$ ($a_2 \in \{-2, -1, 0, +1, +2\}$, zero higher-genus factors).
   - **Tropical geometry:** Pure $5$-smooth Raynaud/sandpile group $K(Y) \cong (\mathbb{Z}/5)^3 \oplus \mathbb{Z}/30 \oplus \mathbb{Z}/120 \oplus \mathbb{Z}/360$ ($|K(Y)| = 162{,}000{,}000 = 2^7\cdot 3^4\cdot 5^6$), exhaustive divisorial gonality $\operatorname{gon}(Y) = 6$ witnessed by a single reduced prime hexagon $D_{\mathrm{hex}} = \mathrm{C}+\mathrm{C}\sharp+\mathrm{D}+\mathrm{f}\sharp\mathrm{m}+\mathrm{a}\flat\mathrm{m}+\mathrm{c}\sharp\mathrm{m}$, and $0/39$ tree-quotient involutions ($\min\beta_1 = 4$, non-hyperelliptic).
   - **Lamé Moduli & Exact Rational Arithmetic Classification:** $|\operatorname{Aut}(Y)| = 144 = 12(g - 1)$ lifts via $\tilde{\Gamma} = S_3 *_{\mathbb{Z}_2} V_4 \subset \mathrm{PGL}_2(\mathbb{Q}_2)$ (split involutions obstructed by `NEG-M17`, $v_2(q^2-p^2)\ge 3$). Universal Fricke–Vogt polynomials and ambient quaternion algebra $B(x) = (-3, x(x-3))_{\mathbb{Q}(x)}$ prove that rational arithmetic Nauru curves occur **if and only if $x \in \{\frac{1}{2}, \frac{3}{2}, \frac{5}{2}\}$** inside $B_3 = (-3,-1)_{\mathbb{Q}}$ ($D = 6$) and $B_5 = (-3,-5)_{\mathbb{Q}}$ ($D = 10$).
   - **Explicit Arithmetic Non-Congruence Shimura Covers (`NEG-M18`):** At $x = \frac{3}{2}$, $\Gamma_Y \trianglelefteq_{V_4} \Gamma(3)$ is an explicit **non-congruence** Klein $V_4$-cover of the genus-$4$ principal level-$3$ Shimura curve $X^6(\Gamma(3))$ (dual graph $K_{3,3}$, $\tau(\gamma_6) = \frac{121}{64}$); at $x = \frac{5}{2}$, $\Gamma_Y \trianglelefteq_{S_3} \Gamma_5(3)$ covers $X^{10}(\Gamma(3))$ ($K_4$) through the cube $Q_3$ ($g = 5$). All `19/19` Borel-level genus-$13$ Shimura curves $X_0^D(N)$ and `22/22` degree-$\le 4$ Brandt graphs are excluded.
4. **$3$-Adic Companion ($\mathrm{Dic}_6$ on $T_4$ of $\mathrm{PGL}_2(\mathbb{Q}_3)$):**
   - `18` connected bipartite $4$-regular Cayley graphs ($g = 25$): `12/18` strictly Ramanujan at $\lambda_{\mathrm{nt}} = 3.000 < 2\sqrt{3}$ and `6/18` on the exact boundary $2\sqrt{3}$, with $|K(Z)| = 429{,}923{,}020{,}800 = 2^{12}\cdot 3\cdot 5^2\cdot 7^2\cdot 13^4$.

## Three-Plane Zero-Shared-Data Verification

| Plane | Path | License | Scope & Result |
| :--- | :--- | :--- | :--- |
| **Pure Python (zero deps)** | [`code/triadic_nauru_verify.py`](code/triadic_nauru_verify.py) | MIT | **12/12 D/R/P/Seam gates PASS** (incl. SplitMix64 $N=200$ RCT null control, 18-level Manin $T_2$, 4 TikZ/PGFPlots vector PDFs) |
| **Lean 4.36.0 (zero Mathlib)** | [`lean/TriadicNauru/Core.lean`](lean/TriadicNauru/Core.lean) | MIT | **20/20 theorems kernel-checked** (`0 sorryAx`, `0 Lean.ofReduceBool`) |
| **Pure Rust (zero crates)** | [`rust/src/lib.rs`](rust/src/lib.rs) | MIT | **6/6 integration tests + 5/5 core suites PASS** (`0.32s` release) |
| **Data Model (SHA-256)** | [`data/triadic_nauru_calibration.json`](data/triadic_nauru_calibration.json) | CC BY 4.0 | Immutable calibration record verified by [`data/MANIFEST.sha256`](data/MANIFEST.sha256) |

### Reproduce Locally

```bash
python3 papers/triadic_wreath_nauru/code/triadic_nauru_verify.py
(cd papers/triadic_wreath_nauru/lean && lake build && .lake/build/bin/triadic-nauru-lean)
(cd papers/triadic_wreath_nauru/rust && cargo test --release && cargo run --release)
```
