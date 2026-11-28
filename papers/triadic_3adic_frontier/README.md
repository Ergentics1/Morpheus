# Paper #09 (`PC-III`): The 3-Adic Dicyclic Companion, Exact Level $3\mathfrak{P}_5$ and Level $(3)$ Congruence on Nauru, and the Real-Quadratic Lamé Shimura Curve Atlas

**Companion & Sequel to Paper #01 ([*Prime Cadences*](../../prime_cadences_paper.md), `v0.3.1`) and Paper #08 ([`PC-II`](../triadic_wreath_nauru/README.md), `v0.7.1`)**

- **Read on GitHub (GFM mirror):** [`triadic_3adic_frontier.md`](triadic_3adic_frontier.md)
- **Canonical PDF (AMS `LaTeX`, `0` warnings/hboxes, `v0.8.0`):** [`paper/triadic_3adic_frontier.pdf`](paper/triadic_3adic_frontier.pdf)
- **AMS `LaTeX` & BibTeX source:** [`paper/triadic_3adic_frontier.tex`](paper/triadic_3adic_frontier.tex), [`paper/references.bib`](paper/references.bib), [`paper/triadic_3adic_frontier.bbl`](paper/triadic_3adic_frontier.bbl)
- **Neutral `0/0` arXiv bundle:** [`arxiv/triadic-3adic-frontier-arxiv.tar.gz`](arxiv/triadic-3adic-frontier-arxiv.tar.gz) (standalone compile verified)

## Summary of Main Results

1. **Pillar I — Rational $2$-Adic Nauru Congruence, Universal Twin Duality, & Unconditional Metric Gonality (`NEG-M23`, `NEG-M24`):**
   - Exact algebraic twin duality $\tau((bt)a) = 3 - x$ on $B(x) = (-3, -x(3-x)/F)$ exchanging $\rho_6 \leftrightarrow \rho_{12}$.
   - Exact level-$3\mathfrak{P}_5$ congruence on $(B_5, \frac{5}{2}, \rho_6) \cong (B_5, \frac{1}{2}, \rho_{12})$ (`|Ad_15| = |joint| = 3,600 = 144×25`, unique normal Sylow-$5$ $U_5$ killed via $\gcd(25, 144) = 1$) sharply separated from $B_3(\frac{3}{2}) \to X^6(\Gamma(3)) \leftrightarrow K_{3,3}$ (level $3$) and $(B_5, \frac{1}{2}, \rho_6) \to X^{10}(\Gamma(3\mathfrak{P}_5))/V_4 \leftrightarrow K_{3,3}$ (level $3\mathfrak{P}_5$).
   - Unconditional metric gonality $\operatorname{sn}(Y) = \operatorname{dgon}(Y) = \operatorname{gon}(\Gamma_{\mathrm{eq}}(Y)) = 6 \le \operatorname{gon}(\Gamma(Y)) \le \operatorname{gon}(\mathcal{C}_Y)$ (`24`-star scramble `h = e = 6`, `168` Edmonds–Karp cuts, `132/132` continuous Dhar cells on $D_{\mathrm{hex}}$).
2. **Pillar II — Complete Real-Quadratic & Totally Real Cubic Lamé Nauru Atlas (`NEG-M25`):**
   - Exactly `6` primitive real-quadratic moduli across `4` fields ($\mathbb{Q}(\sqrt{17}), \mathbb{Q}(\sqrt{2}), \mathbb{Q}(\sqrt{3}), \mathbb{Q}(\sqrt{7})$), all with $\mathrm{Ram}_{\mathrm{fin}}(B(x)) = \varnothing$:
     - $\mathbb{Q}(\sqrt{17})$: non-congruence $C_3$-cover of $X^{17}(\Gamma(v^2)) \leftrightarrow Q_3$ (`|Ad_{v^2}| = 48, |ker| = 3`);
     - $\mathbb{Q}(\sqrt{2})$: non-congruence Eichler-$\mathfrak{q}_7$ cover of $X^1(\mathfrak{q}_7) \leftrightarrow \Theta_3$ (`T_8-det = 49·8^4`, `|Ad| = 588`, `|ker^1| = 12` with **non-isomorphic Galois kernels** $C_6 \times C_2$ vs. $A_4$, obstructed by $4 \nmid 1$);
     - $\mathbb{Q}(\sqrt{3})$: non-congruence via Eichler-$\mathfrak{p}_3$ $2$-part obstruction (`T_8-det = 9·12^4`, `|Ad^1|=243, |Ad^+|=486, |Ad|=972`);
     - **$\mathbb{Q}(\sqrt{7})$: second genuine congruence Shimura curve of exact level $(3) = \mathfrak{p}_3\mathfrak{p}_3'$ for BOTH $\rho_6$ and $\rho_{12}$ (`|Ad_(3)| = |joint| = 576, |ker| = 1`, `144/144`)!**
   - Complete census of all `4` irreducible totally real cubic moduli ($d_F \in \{316, 148\}$).
3. **Pillar III — Complete Solution of the Rational $3$-Adic $\mathrm{Dic}_6$ Frontier on $T_4(\mathbb{Q}_3)$ (`NEG-M20`, `NEG-M26`):**
   - `18/55` connected $\mathrm{Dic}_6$ Cayley graphs (`12` Ramanujan $Z$ with exact $\pi_Z(4..16)$, `6` boundary), `43` involutions `{7:2, 11:24, 13:17}`.
   - Exact metric gonality collapse $\operatorname{sn}(Z) = \operatorname{dgon}(Z) = \operatorname{gon}(\Gamma_{\mathrm{eq}}(Z)) = 8 \le \operatorname{gon}(\mathcal{C}_Z)$ via $4$-path scramble $\mathcal{S}_4$ (`276/276` touching, `h = e = 8`, `156` cuts `{8:48, 10:108}`), exhaustive Dhar (`0/98,280` deg 6, `0/475,020` deg 7), and `168/168` continuous Dhar cells on both $D_8 = \langle x^3\rangle + \langle x^3\rangle y$ and `PC-II`'s $D_{\mathrm{Dic}_6}$.
   - Universal Fricke–Vogt $B_Z(u,v)$ (`4 | mn` isolates `5/10` canonical curves: $B_2, B_5(2), B_{70}, B_2(5), B_2(11)$); **`0/80` congruence** across all realizations via diagonal-$\pm 1$ CRT true left-multiplication $\Gamma(M)$, unique normal $C_3$, and Riehm mod-8 (`O_70^1`: `768/256/3, -I ∈ [G,G]`) + Burnside's Basis Theorem.
   - **Hurwitz Level-$8$ vs. $\mathrm{Ad}_{16}$ Reconciliation (`NEG-M26`):** True left-multiplication `L_8/\{\pm 1\}` (`order 64`) already collapses all `16/16` realizations to `|ker^1| = 3` (matching `PC-II` Thm 7.2's `16/16` split at $\Gamma(4)$ vs. $8\mathcal{O}_2$), while adjoint `Ad_8 (128)` stays `{3:8, 6:8}` and reaches `{3:16}` at `Ad_16 (1024)`; all `16/16` cover $Z/C_3 \cong K_{4,4}$.
   - Genus-25 Borel census (`19` curves, `9` TF), paired with `PC-II` Theorem 7.3's `0/19` Manin $T_3$ exclusion (`NEG-M20`).
4. **Section 5 — Hardware-`FENV` Poitou–Odlyzko Strict-Positivity Audit (`NEG-M27`):**
   - Certifies `(6,16,1,2)` outward gap `[+0.013629809157, +0.013629809162] > 0`, rejects sign-changing $f_{\mathrm{bad}}(\pm 1) = -0.60 < 0$, and preserves the degree-8 `(8,1,1,E)` gap (`12.593730` at $b=3.0$, continuous peak `12.595576` at $b^*=3.039865 < 13.142385$).

## Four-Plane Zero-Shared-Data CI Verification

| Plane | Path | License | Scope & Result |
| :--- | :--- | :--- | :--- |
| **Pure Python (zero deps)** | [`code/triadic_3adic_verify.py`](code/triadic_3adic_verify.py) | MIT | **8/8 gates (`F1`–`F8`) PASS** + `--check-only` & `--no-figs` modes + 4 runtime metadata-free TikZ vector PDFs |
| **Pure Rust (zero crates)** | [`rust/src/lib.rs`](rust/src/lib.rs) | MIT | **6/6 integration tests + 6/6 core suites PASS** (incl. `573,300` exhaustive deg-6/7 Dhar, `0/80` CRT left-mult, Hurwitz `L_8/\{\pm 1\}=64`, Riehm mod 8, $\mathcal{O}_7^{\max}$ mod `(3)`) |
| **Zero-Heap C++20 `FENV`** | [`cpp/fenv_oracle.cpp`](cpp/fenv_oracle.cpp) | MIT | **6/6 gates PASS** (`-O2 -std=c++20 -frounding-math -Wall -Wextra -Werror`; hardware `FE_DOWNWARD`/`FE_UPWARD` intervals, Jacobi $\le 2.11\times 10^{-15}$, `573,300` exhaustive Dhar, Poitou gap $> 0$, genus-25 census) |
| **Lean 4.36.0 (zero Mathlib)** | [`lean/Triadic3AdicFrontier/`](lean/Triadic3AdicFrontier.lean) | MIT | **20/20 theorems live kernel-compiled** (`-DwarningAsError=true -DautoImplicit=false`, `0 sorryAx`, `0 Lean.ofReduceBool`) |
| **Data Model (SHA-256)** | [`data/triadic_3adic_calibration.json`](data/triadic_3adic_calibration.json) | CC BY 4.0 | Immutable calibration record (`schema_version 1.0.0`) verified by repo-root-relative [`data/MANIFEST.sha256`](data/MANIFEST.sha256) |

### Reproduce Locally

```bash
python3 papers/triadic_3adic_frontier/code/triadic_3adic_verify.py --check-only
sha256sum -c papers/triadic_3adic_frontier/data/MANIFEST.sha256
(cd papers/triadic_3adic_frontier/rust && cargo test --release && cargo run --release)
g++ -O2 -std=c++20 -frounding-math -Wall -Wextra -Werror papers/triadic_3adic_frontier/cpp/fenv_oracle.cpp -o /tmp/pc3_fenv && /tmp/pc3_fenv && rm -f /tmp/pc3_fenv
(cd papers/triadic_3adic_frontier/lean && lake build && .lake/build/bin/triadic-3adic-lean)
```
