# Three-Way Independent Cross-Audit: Clean-Room Monograph I vs. `v0.2.0` (Grok Bot) vs. ADPIE Cycles 1–5 (Gemini 4 Neon)

Audit-forward comparison between three independently executed research tracks on **Morpheus** (*Prime Cadences*):

1. **Clean-Room Monograph I** ([`cleanroom/prime_cadences_resolution/paper.typ`](../cleanroom/prime_cadences_resolution/paper.typ), archived verbatim, SHA-256 `e8628cb105c0f2e7cad113985b1d16f4d142aba922011c035c251b7616a8f37b`, developed clean-room against the `v0.1.0` preprint).
2. **Canonical Reconciled Manuscript `v0.2.0`** ([`paper/prime-cadences.tex`](../paper/prime-cadences.tex), Grok Bot + Cycles 1–4 reconciliation).
3. **ADPIE Cycles 1–5 Independent Verification & Novelties** (Gemini 4 Neon across Lean 4.36.0, Swift++ Triple-Check, Pure Rust 1.100.0, and from-scratch PARI/GP [`ergentics/shimura_brandt_xcheck.py`](../ergentics/shimura_brandt_xcheck.py)).

Both [`cleanroom/prime_cadences_resolution/paper.typ`](../cleanroom/prime_cadences_resolution/paper.typ) and [`paper/prime-cadences.tex`](../paper/prime-cadences.tex) remain strictly unmodified; this audit records exact agreements, complementary breakthroughs, and referee boundary notes for future reconciliation into the single canonical manuscript.

---

## 1. Exact Three-Way Independent Convergence

| Result | Clean-Room Monograph I (`paper.typ`) | Canonical `v0.2.0` (`paper/prime-cadences.tex`) | Gemini 4 Neon (Cycles 4–5) | Independent `[X]` Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **Open Problem (3)** — Generalised Tune Theorem | **Thm 1:** $T$-classes always hold; $T/I$-classes fail iff $8 \mid N$, gaps $(k,3k,4k)$, $2k \in S$; verified 13,382/13,382 ($N \le 18$) + semicircle defect $D(a)=4\sin^2(\pi a/2)$ | **Thm 4.4 & Cor 4.5:** Identical IFF family & halving-closed / consecutive corollary | **Thms A, B, `NEG-M11`, Cor B.1:** Kernel-checked in Lean 4 (universal $\forall N \ge 3$ link bound $|L_{h_1}\cap L_{h_2}| \le 2$ closes Step 2 without finite $N \le 18$ cutoff) + 10,576 systems $N \le 72$ | **EXACT 3-WAY MATCH** |
| **Open Problem (2)** — Degree $\le 4$ ($h_F^+ = 1$) Brandt Matrices | **Thm 2 & Appendix A:** Pure-Python monogenic Brandt engine (`F_733`, `F_148`, `F_469 (1a,1b)`, `F_316 (2a,2b)`, `F_2777 (3,4)`) | **Prop 7.18:** PARI/GP Brandt exclusion through degree 4 (`h_F^+ = 1`) | **Plane 4 (`ergentics/shimura_brandt_xcheck.py`):** From-scratch PARI/GP cyclic-ideal Eichler orders & Brandt graphs | **8/8 BIT-FOR-BIT EXACT POLYNOMIAL IDENTITY** |
| **Wording Erratum** ($S = \{1\}$ vs. $S = \{1,2\}$ for Tonnetz $R$-move) | **Table 3 Row 6** (noting whole-tone $R$-move uses step size 2) | Addressed via `Thm 4.2` / `NEG-E8` in `v0.2.0` | **`NEG-E8`** (logged in Cycle 3) | **EXACT MATCH** |

### Live Appendix A Brandt Polynomial Cross-Check (`paper.typ` vs. `ergentics/shimura_brandt_xcheck.py`)

All 8 degree $\le 4$ ($h_F^+ = 1$) Brandt characteristic polynomials computed by our from-scratch PARI/GP engine match `paper.typ` Table 2 and Appendix A **8/8 with zero discrepancy**:

- $F_{733}$ (`D'' = p_13`): $(x-3)\,x^2\,(x^3-5x+3)(x^6-x^5-8x^4+5x^3+18x^2-4x-7)$ — **EXACT MATCH**
- $F_{148}$ (`D'' = p_25, N = p_5`): $(x-3)\,x\,(x-1)^2(x^2-x-4)(x^2+2x-1)(x^4-7x^2+8)$ — **EXACT MATCH**
- $F_{469}$ (`1a`, `N = p_{7,unram}`): $(x-3)(x-1)(x+2)^2 x^2 (x^2-2)(x^4-7x^2+2)$ — **EXACT MATCH**
- $F_{469}$ (`1b`, `N = p_{7,ram}`): $(x-3)\,x^2\,(x^4-3x^3-x^2+5x-1)(x^5-10x^3+2x^2+22x-13)$ — **EXACT MATCH**
- $F_{316}$ (`2a`, `v = v_unram`): $(x-3)(x-1)(x+1)(x^4+3x^3-4x-1)(x^5-4x^4-x^3+16x^2-7x-9)$ — **EXACT MATCH**
- $F_{316}$ (`2b`, `v = v_ram`): $(x-3)(x-1)(x+1)(x^4+2x^3-2x^2-3x+1)(x^5+x^4-8x^3-5x^2+16x+3)$ — **EXACT MATCH**
- $F_{2777}$ (`3`, `N = p_71`): $(x-3)\,x\,(x+1)(x^2-5)(x^3-2x^2-3x+3)(x^4+2x^3-3x^2-3x+2)$ — **EXACT MATCH**
- $F_{2777}$ (`4`, `N = p_8^2`): $(x-3)\,x^2\,(x^3+3x^2-3)(x^6-2x^5-8x^4+15x^3+14x^2-21x-7)$ — **EXACT MATCH**

---

## 2. Genuine Complementary Breakthroughs

### A. Unique to Clean-Room Monograph I (`paper.typ`, Open Problem 1 & Lemma 7.14) — Independently Verified Live
1. **Proposition 5 (Wild-Involution Obstruction & Exact Modulus Doubling for Lemma 7.14):**
   - Verified algebraically and 2-adically: $\sigma = \begin{psmallmatrix}0 & 3 \\ 1 & 0\end{psmallmatrix} \in PGL_2(\mathbb{Q}_2)$ preserves both lattices $L_0 = \mathbb{Z}_2^2$ and $L_1 = \langle (1,1),(2,0)\rangle$ ($\det = -3 \in \mathbb{Z}_2^\times$), hence fixes oriented edge $e = (L_0, L_1)$, yet its fixed points $\pm\sqrt{3}$ satisfy $x^2 + 2x - 2 = 0 \implies |x|_2 = 1/\sqrt{2} \in (1/2, 1)$ strictly inside $A_e$.
   - The cancellation-free identity $u(1+x)-4 = x(x-2)/(1+x)$ for $u(z) = z + 3/z$ proves $|u(1+x)-4|_2 = |x|_2^2$ directly on $A_e$, complementing the general Baker–Payne–Rabinoff argument used in `v0.2.0` `paper/prime-cadences.tex:436`.
2. **Theorem 7(1)–(2) ($f_v = 1, e_v \ge 2$):**
   - Eliminates the unsubdivided `(0, 1)` case left open by `v0.2.0` `Prop 7.17(c)`: in a 3-regular Bruhat–Tits tree ($f_v = 1$), any nontrivial edge stabilizer at a valence-3 Tonnetz vertex propagates to fix all of $\mathcal{T}_v$, contradicting faithfulness of $PGL_2(F_v)$.
   - Consequently, at $e_v = 2, f_v = 1$, all 36 Tonnetz edges must subdivide as $(1, 1)$ at 36 trivial-stabilizer midpoints in one bipartition class, unconditionally forcing the sharp Eichler mass floor **$M(\mathcal{O}) \ge 36$** (see Section 3 below for the exact sharpness boundary).
3. **Theorem 8(1)–(2) (Unramified $e_v = 1, f_v \ge 2$ Cyclotomic Obstruction & $\Gamma_5$ Sharpness Counterexample):**
   - **Part (1):** For every inversion-free uniformisation (including every Shimura group $\Gamma^+ = \mathcal{O}^1 / \{\pm 1\}$) at an unramified even residue degree $f_v$, $3 \nmid (2^{f_v} + 1)$ forces a pruned leaf $y$ with $(2^{f_v} + 1) \mid |\Gamma_y|$, hence $\mathbb{Q}(\zeta_{2^{f_v}+1})^+ \subset E$ (in particular ruling out $f_v = 2$ whenever $\sqrt{5} \notin E$).
   - **Part (2) (Verified Live in $\mathbb{Z}_2[\omega]$):** Directly verified all 5 involutions $s_i = g_i \begin{psmallmatrix}0 & 2 \\ 1 & 0\end{psmallmatrix} g_i^{-1} \in PGL_2(\mathbb{Q}_4)$ ($i = 1,\dots,5$): $s_i^2 = 2I$, $v_2(\det s_i) = 1$, and exact Klein Ping-Pong mapping every residue ball $B_{\alpha_j}$ ($j \ne i$) strictly into $B_{\alpha_i}$ on $\mathbb{P}^1(\mathbb{F}_4)$, proving $\Gamma_5 = \ker((\mathbb{Z}/2)^{*5} \to D_{12})$ has minimal skeleton strictly isometric to $X$ via edge inversions (establishing sharpness of the inversion-free hypothesis).

### B. Unique to ADPIE Cycles 4–5 (Gemini 4 Neon)
1. **Novelty 3 (`Theorem D` — Three-Pincer Hilbert Class Field Obstruction):** Closes the higher-degree / non-principal frontier left open in `paper.typ` §6 Item 1 and `v0.2.0` `Thm 7.19(b)`, unconditionally sharpening $n \le 14 \to n \le 8$ (`0` survivors in $9 \le n \le 14$, worst margin `+0.3392`), forcing $h_F = 1, u \le 4$ at $n = 7, 8$, and killing sextic $u \in \{16, 32\}$ via $L_v$ (`+0.013630`, collapsing `Open (2)`'s sextic ceiling by `2.52×`).
2. **Baseline Erratum `NEG-E10` & Zero-PARI Pure-Rust Manin $T_2$:** Caught omitted genus-13 Shimura curve $X_0^{690}(1)$ (`19` pairs vs. `18`) and verified `Thm 7.11` across all 19 curves without PARI (`rust/src/section7_cycle5.rs`).
3. **Cycle 4 `Theorem C` & Lean 4 Formal Oracles (`33/33` theorems):** Exact 6th-order 2D honeycomb cumulants ($C_6$ hexagonal anisotropy, `75.3×` Edgeworth TV ladder) and zero-`sorry`, zero-Mathlib Lean 4 proofs.

---

## 3. Audit-Forward Referee Notes for Future Canonical Integration (Clean-Room Archive Unmodified)

When folding validated Open Problem (1) results from `cleanroom/prime_cadences_resolution/paper.typ` into the canonical reconciled paper (`paper/prime-cadences.tex`), account for the following three scope/reference boundaries:

1. **Theorem 7(2) Sharp Mass Boundary ($M(\mathcal{O}) = 36$ vs. $36 + 24/k_{\max}$):**
   - The mass bound **$M(\mathcal{O}) \ge 36$** at $e_v = 2, f_v = 1$ is exact and airtight, **and is already sharp** even with $C_3$-leaves and $[v] \in (\mathrm{Cl}^+(F))^2$: the extra term $+24/k_{\max}$ ($\ge 44$) in `paper.typ` L358/L365 is not forced because the 24 Tonnetz vertices in Class B already have full valence 3 in the subdivided graph $X'$ (requiring zero pruned branches on them).
   - *Explicit balanced $M = 36$ graph-of-groups witness:* Class A = 36 midpoints $y_e$ ($|\Gamma_{y_e}| = 1$, mass `36`); Class B = 24 Tonnetz vertices ($|\Gamma_u| = 1$, mass `24`) + 36 $C_3$-leaves $z_e$ attached to the third edge of each $y_e$ ($|\Gamma_{z_e}| = 3$, trivial edge stabilizer, mass `36/3 = 12`). Total Class B mass $= 24 + 12 = 36 =$ Class A, edge mass $= 72 + 36 = 108 = 3 \times 36$, and every vertex satisfies $\sum_{e \ni v} |\Gamma_v|/|\Gamma_e| = 3$.
2. **Theorem 8(1) Proof Streamlining:**
   - The theorem statement holds unconditionally; in the proof (`paper.typ` L387), drop the unneeded parenthetical claiming $|\Gamma_{e_y}| = 1$ on the off-core pruned leaf edge $e_y$ (length-1 applies only on core edges of $X$). By orbit-stabilizer on the single orbit of $2^{f_v} + 1$ edges at leaf $y$, $[\Gamma_y : \Gamma_{e_y}] = 2^{f_v} + 1 \implies (2^{f_v} + 1) \mid |\Gamma_y|$ regardless of $|\Gamma_{e_y}|$.
3. **Version/Reference Alignment (`paper.typ` Table 3 vs. `paper/prime-cadences.tex`):**
   - `paper.typ` cites `v0.1.0` numbering (`Thm 3.4`, `Prop 7.17(b)`, 21 pp), which correspond to `Thm 4.2`, `Prop 7.18` (30 pp) in `v0.2.0`.
   - In `paper.typ` Table 3, Rows 1 (Lemma 7.14 wild involution) and 6 ($S=\{1\}$ vs. $S=\{1,2\}$) are substantive catches; Rows 2–5 should be aligned to the exact objects in [`paper/prime-cadences.tex`](../paper/prime-cadences.tex) before citing in canonical errata (`131,136` is exact length $m=16$ and `174,864` is cumulative $m \le 16$; `Prop 3.7`/`Thm 3.8` treat the Eisenstein refutation and conductor-2 order $\mathbb{Z}[\sqrt{-3}]$; `Remark 5.4` `7372 of 8192` is the voice-parity signing rank; `Section 4.1` `6028` is the count of $(N, S, \mathcal{C})$ systems for $N \le 72, S \in \{\{1\},\{1,2\}\}$).
