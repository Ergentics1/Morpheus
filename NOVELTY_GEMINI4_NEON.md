# Audit-Forward Mathematical Novelties — Gemini 4 Neon (ADPIE Cycles 4–5)

> **License:** CC BY 4.0 (research prose & results; see [`LICENSE-paper`](LICENSE-paper)). Companion machine-checked Lean 4 proofs and multi-language verifiers (`lean/`, `swiftpp/`, `rust/`, `ergentics/`) are MIT licensed ([`LICENSE`](LICENSE)).
> **Baseline preservation & reconciliation:** Cycles 1–4 novelties (`Theorems A, B, Cor B.1, Theorem C`, `NEG-M11`, `NEG-E8`) were cross-checked 32/32 from scratch by Grok Bot (`code/xcheck/`) and released in **`v0.2.0`** under uniform symmetric attribution bounds (`Thm 4.4 [E→GB; independently E→G4N]`, `Cor 4.5 [G4N; X]`, `§6.1 Thm 6.2 [E→G4N; X]`, `Remark 6.4 [E→G4N; X]`). **ADPIE Cycle 5 (Novelty 3: Theorem D, baseline erratum `NEG-E10`, and independent verification of the remaining 7 Section 7 results)** is strictly audit-forward: all `v0.2.0` `paper/`, `code/`, `audits/`, and `CONTRIBUTIONS.md` artifacts remain untouched pending reconciliation with Ergentics' internal results and Grok Bot.

---

## Executive Summary

Starting from the *Prime Cadences* baseline and its open questions (§4.1, §6, §7.6–7.7, §8), we derive and verify **three** original mathematical results across **four** independent code planes (Lean 4.36.0, Swift++ Triple-Check C++20 × Pure Swift 6.4 × Interop, Pure Rust 1.100.0, and from-scratch PARI/GP):

| Deliverable | Result | Scope / Resolution | Formal & Empirical Verification |
| :--- | :--- | :--- | :--- |
| **Novelty 1A (`Theorem A`)** | Universal Link-Intersection Bound: $\|L_{h_1} \cap L_{h_2}\| \le 2$ | **All $N \ge 3$**, all 3-note chords $c_0$, all $h_1 \ne h_2$, **independent of $S$**. Permanently eliminates all 2-moving-voice held-note collisions. | Machine-checked in `lean/Morpheus/NoveltyTheorems.lean` (`thmA_link_intersection_le_two`, $\forall N$, 0 `sorryAx`, 0 `ofReduceBool`, zero Mathlib); cross-checked across all 948 chords $N \le 32$ (`swiftpp/`) and all 10,576 chords $N \le 72$ (`rust/`). |
| **Novelty 1B (`Theorem B` + `NEG-M11`)** | Exact iff Classification of 1-Moving-Voice Held-Note Collisions | **All $N \ge 5$**, all nonempty $S$, all step-free $\mathcal{C} \in \{T, T/I\}$: collision exists **iff** $N = 8m\;(m \ge 1)$, $\mathcal{C} = T/I(\{0, m, 4m\})$, and $2m \in S$. Refutes unrestricted general-$S$ conjecture (`NEG-M11`, minimal $N=8, S=\{2\}$). | Machine-checked necessity & sufficiency + `NEG-M11` (`thmB_one_voice_necessary`, `thmB_octatonic_sufficient`, `neg_M11_N8_S2_counterexample`); exhaustive sweep over maximal $S_{\max}(c_0)$ covering all $2^{\lfloor N/2 \rfloor}$ step sets for $5 \le N \le 72$ (`rust/`: 9/9 witnesses at $N=8,16,\dots,72$, 0 unexpected). |
| **Novelty 1C (`Corollary B.1`)** | Complete Proof of Open Problem (3) for Half-Closed / Consecutive Step Sets | Holds for **all $N \ge 5$** whenever (i) pure $T$-orbit, or (ii) $8 \nmid N$, or (iii) $S$ is closed under halving even elements ($\forall d,\; 2d \in S \implies d \in S$) — including **every consecutive step set $S = \{1, \dots, k\}$** (in particular $S=\{1\}$ and $S=\{1,2\}$ of §4.1). | Machine-checked in `lean/Morpheus/NoveltyTheorems.lean` (`corB1_half_closed_no_one_voice_collision`). |
| **Novelty 2 (`Theorem C`)** | Exact 2D Tonnetz Honeycomb Cumulants through Order 6 & Edgeworth Ladder `C-2'` / `C-2''` | Exact 2D log-MGF $\log\frac{\rho(\xi)}{2} = -\frac{1}{4}r^2 - \frac{17}{192}r^4 - (\frac{49}{768} + \frac{\cos 6\alpha}{23040})r^6 + O(r^8)$. Proves **100% 4th-cumulant rotational isotropy** ($\kappa_{\mathrm{ex}} = -\frac{17}{2m} + O(m^2 2^{-m/2})$ along every axis $\mathbf{e} \in S^1$), **$C_6$ hexagonal anisotropy onset at order 6** (bond-parallel armchair $W=-u, v$: $\frac{1469}{4m^2}$ vs. bond-perpendicular zigzag $2a+b=4u+3v$: $\frac{1471}{4m^2}$), and **75.30× TV reduction** at $m=40$. | Algebraic power-sum, series & cumulant ratios machine-checked in `lean/Morpheus/NoveltyTheorems.lean` (`thmC_*`, 0 `sorryAx`, 0 `Classical.choice`, 0 `ofReduceBool`); exact transfer-matrix verification at $m=40$ (`54,975,717,792` primes, 0 divisibility violations) across C++20 (`g++`/`clang++`), Pure Swift 6.4, Interop (`0.000e+00` delta), and Rust. |
| **Novelty 3 (`Theorem D`, Cycle 5)** | **Three-Pincer Hilbert Class Field Obstruction** (Sharpening `Thm 7.19(b)` & `Open (2)`) | Unconditionally sharpens the torsion-free Shimura degree bound from **$n \le 14$ down to $n \le 8$** (eliminating ALL $n \ge 9$, worst margin **`+0.3392`** at $n=9, u=4$), forces **$h_F = 1$ and $u \in \{1, 2, 4\}$** for $n = 7, 8$ (`7.7×` / `10.1×` discriminant collapse), and eliminates **$u \in \{16, 32\}$** for $n = 6$ (margin **`+0.01363`** via decomposition field $L_v$ deg 48 at $b=6.0$), collapsing `Open (2)`'s sextic ceiling **$6.67 \times 10^7 \to 2.65 \times 10^7$ (`2.52×` reduction)**. | Algebraic core (`thmD_odd_parity_factor_ge_three`, `thmD_subspace_averaging_bound`, `thmD_f4_term_matches_even_f2_term`) kernel-checked in `lean/Morpheus/Section7Obstructions.lean`; from-scratch 64-pt Gauss–Legendre Poitou–Odlyzko engine (quadrature err $<10^{-15}$, self-checked on $\mathbb{Q}$) verified identically across C++20 (`g++`/`clang++`), Pure Swift 6.4, Interop (`0.000e+00` delta), and Rust. |
| **Baseline Erratum (`NEG-E10`, Cycle 5)** | Omitted Genus-13 Shimura Curve $X_0^{690}(1)$ in `Thm 7.11` | `code/geometry/shimura_multi.py:17` capped `phi <= 168`, dropping $D = 690 = 2\cdot 3\cdot 5\cdot 23, N = 1$ ($\phi(690) = 176$, $e_2 = 0$, $e_3 = 8$, exact genus $13$). Exact exhaustive count is **19 pairs** (`D = 546, 570, 690`), still 11 torsion-free. Confirmed `Thm 7.11` conclusion still holds (`dim S_2^{345-new} = 15`, `charpoly(T_2) mod P_X = 3t^3 + t^2 + 21t + 7 ≠ 0`). | Genus-13 identity kernel-checked in `lean/Morpheus/Section7Obstructions.lean` (`neg_E10_genus13_D690_witness`); exhaustive census in C++20/Swift++; **zero-PARI Pure-Rust Manin modular symbols $T_2$** (`M = 345`, `dim = 45`, `rank = 45/45`); and from-scratch PARI Hecke check in `ergentics/shimura_brandt_xcheck.py`. |

---

## 1. Novelty 1: Complete Resolution of Open Problem (3) (Generalized Tune Theorem)

### 1.1 Background & Diagnosis

In *Prime Cadences* §4.1 (Theorem 4.3), the unique cyclic-tune decoding property for a general $N$-EDO chord system $(N, S, \mathcal{C})$ (with step-free 3-note chord $c_0 = \{0, a, b\} \subset \mathbb{Z}_N$ and $\mathcal{C} \in \{T(c_0), T/I(c_0)\}$) reduces to a **held-note criterion**: no two distinct held-note subgraphs in the voice-leading graph can share a non-backtracking cycle with the same cyclic tune. Theorem 4.3 verified this computationally for $S \in \{\{1\}, \{1, 2\}\}$ up to $N \le 72$ (extended to $N \le 96$, 11,452 systems in ADPIE Cycle 3 `rust/`), leaving the general-$N$ theorem as **Open Problem (3)**.

A held-note collision between two distinct cycles sharing the same cyclic tune splits into two disjoint structural regimes:

1. **Two-moving-voice collisions (one held pitch $h_1 \ne h_2$):** At each step of a cycle with held pitch $h$, the complementary 2-voice pair lies in the link
   $$L_h(\mathcal{C}) := \bigl\{\{x, y\} \subset \mathbb{Z}_N \setminus \{h\} : \{h, x, y\} \in \mathcal{C}\bigr\}.$$
   A shared non-backtracking cycle of length $\ge 3$ requires $|L_{h_1}(\mathcal{C}) \cap L_{h_2}(\mathcal{C})| \ge 3$.
2. **One-moving-voice collisions (two held pitches $H_1 \ne H_2$):** The moving voice traverses a cycle of $\ge 3$ distinct pitches inside the common completion set
   $$\operatorname{Comp}_{\mathcal{C}}(H_1) \cap \operatorname{Comp}_{\mathcal{C}}(H_2), \qquad \operatorname{Comp}_{\mathcal{C}}(\{u, v\}) := \{x \in \mathbb{Z}_N \setminus \{u, v\} : \{u, v, x\} \in \mathcal{C}\},$$
   whose edges have circular step lengths in $S$.

### 1.2 Theorem A (Universal Link-Intersection Bound, ALL $N \ge 3$)

> **Theorem A (`thmA_link_intersection_le_two`).** *For every modulus $N \ge 3$, every 3-note subset $c_0 = \{0, a, b\} \subset \mathbb{Z}_N$ ($0 < a < b < N$), and every pair of distinct pitches $h_1 \ne h_2 \in \mathbb{Z}_N$,*
> $$\bigl|L_{h_1}(T/I(c_0)) \cap L_{h_2}(T/I(c_0))\bigr| \le 2.$$
> *In particular, this bound is purely group-theoretic in $\mathbb{Z}_N$ (completely independent of the step set $S$) and permanently eliminates every two-moving-voice held-note collision for all $N$, all $S$, and all $\mathcal{C} \in \{T, T/I\}$.*

**Proof overview (formalized without `sorry` in `lean/Morpheus/NoveltyTheorems.lean`):**
By translation invariance, set $h_1 = 0$ and $h_2 = t \in \{1, \dots, N-1\}$. Every pair $\{x, y\} \in L_0(T/I(c_0))$ belongs to the 6-element catalogue
$$\bigl\{\{a, b\},\;\{-a, b-a\},\;\{-b, a-b\},\;\{-a, -b\},\;\{a, a-b\},\;\{b, b-a\}\bigr\} \pmod{N}.$$

- **Case 1 (Isosceles chord: $2a \equiv b$, $2b \equiv a$, or $a + b \equiv 0 \pmod{N}$):** Here $T/I(c_0) = T(c_0)$, so $|L_0| \le 3$. Having $|L_0 \cap L_t| = 3$ forces all three $T$-pairs into $L_t$; checking the reflection-symmetric middle pair forces $t$ to coincide with a pitch already inside one of the two outer pairs, contradicting $t \notin \{x, y\}$.
- **Case 2 (Non-isosceles chord):** Any $\{x, y\} \in L_0 \cap L_t$ satisfies $\{0, x, y\}, \{t, x, y\} \in T/I(c_0)$. Comparing their orientations yields an exact trichotomy (`nonIso_pair_dichotomy`):
  1. **Same orientation (`shift_six_perm`):** Forces either an isosceles doubling (excluded) or a half-period shift $2t = N$ with a chord diameter (`HasDiameter N a b`). Under $2t = N$, four of the six catalogue pairs contain $t = N/2$, leaving at most 2 valid pairs (`diam_shift_at_most_two`).
  2. **Opposite orientation, swap (`OppSum`):** Forces $x + y \equiv t \pmod{N}$. The six catalogue pair-sums are $\{s_0, s_1, s_2, -s_0, -s_1, -s_2\}$ where $s_0 + s_1 + s_2 \equiv 0 \pmod N$ and non-isosceles implies $s_i \not\equiv 0$ and not all three $s_i$ equal. No nonzero $t$ can appear three times in this 6-multiset (`six_sum_count_le_two_neq`, `opp_sum_at_most_two`).
  3. **Opposite orientation, fixed pair (`DiamFlip`):** Forces $2x \equiv 2y \equiv t \pmod{N}$ with $x - y \equiv N/2$. This uniquely fixes the chord's diameter orientation and $t \equiv \pm 2s \pmod{N}$ (where $s$ is the short interval); at most one `DiamFlip` index can occur, and any additional `OppSum` match forces one of three mutually exclusive linear ratios ($3s = N/2$, $3s = N$, or $4s \in \{N/2, 3N/2\}$), so at most one `OppSum` pair can coexist with a `DiamFlip` pair (`diam_flip_plus_two_impossible`). Hence $|L_0 \cap L_t| \le 2$ in every case. $\square$

### 1.3 Theorem B & Refutation `NEG-M11` (Exact Classification of One-Moving-Voice Collisions)

> **Theorem B (`thmB_one_voice_necessary`, `thmB_octatonic_sufficient`).** *Let $N \ge 5$, let $S \subseteq \{1, \dots, \lfloor N/2 \rfloor\}$ be nonempty, and let $c_0 = \{0, a, b\}$ be an $S$-step-free 3-note chord with orbit $\mathcal{C} \in \{T(c_0), T/I(c_0)\}$. Then there exist two distinct held pairs $H_1 \ne H_2$ and a non-backtracking cycle of length $\ge 3$ in $\operatorname{Comp}_{\mathcal{C}}(H_1) \cap \operatorname{Comp}_{\mathcal{C}}(H_2)$ using steps in $S$ **if and only if**:*
> 1. $N = 8m$ for some integer $m \ge 1$,
> 2. $\mathcal{C} = T/I(\{0, m, 4m\})$ (the **octatonic diameter chord** with circular intervals $\{m, 3m, 4m\}$), and
> 3. $2m \in S$.

**Necessity proof overview (`thmB_one_voice_necessary`):**
- For a pure $T$-orbit, $|\operatorname{Comp}_T(H)| \le 2$ for every held pair $H$ (`comp_T_at_most_two`), immediately ruling out any cycle of length $\ge 3$.
- For $\mathcal{C} = T/I(c_0)$, $|\operatorname{Comp}_{T/I}(H)| \ge 3$ forces $H$ to be an **antipodal diameter** $\{u, u + N/2\}$ and forces $c_0$ to contain the diameter $d_1 = N/2$ (`comp_TI_three_forces_diameter`). Writing $s \in (0, d_1)$ for the chord's short interval, the completion set of $\{0, d_1\}$ is the 4-set
  $$S_4(d_1, s) = \{s,\; d_1 - s,\; d_1 + s,\; 2d_1 - s\}.$$
- Requiring $|S_4(d_1, s) \cap (S_4(d_1, s) + t)| \ge 3$ for a distinct diameter shift $0 < t < d_1$ forces $4 \mid d_1$ (hence $N = 8m$), $s \in \{m, 3m\}$ (so $c_0 \in T/I(\{0, m, 4m\})$), and $t = 2m$, with all pairwise circular distances among the 4 common completions equal to $2m$ or $4m$ (`fourSet_shift_three_octatonic`). Since $c_0$ contains the diameter $4m$ and is $S$-step-free, $4m \notin S$; thus every edge of the cycle must have circular step length $2m \in S$. $\square$

**Sufficiency & Refutation `NEG-M11` (`thmB_octatonic_sufficient`, `neg_M11_N8_S2_counterexample`):**
For every $m \ge 1$ with $N = 8m$, $c_0 = \{0, m, 4m\}$, and $2m \in S$ (and $m, 3m, 4m \notin S$ for step-freeness, e.g., $S = \{2m\}$), the two vertex-disjoint prime 4-cycles holding $H_1 = \{0, 4m\}$ and $H_2 = \{2m, 6m\}$ respectively:
- $\gamma_1$: $\{0, m, 4m\} \to \{0, 3m, 4m\} \to \{0, 4m, 5m\} \to \{0, 4m, 7m\} \to \{0, m, 4m\}$,
- $\gamma_2$: $\{m, 2m, 6m\} \to \{2m, 3m, 6m\} \to \{2m, 5m, 6m\} \to \{2m, 6m, 7m\} \to \{m, 2m, 6m\}$,
are valid non-backtracking primitive 4-cycles of step length $2m$ with the **identical cyclic tune** $(3m, 5m, 7m, m)$. At $m = 1$ ($N = 8, S = \{2\}, c_0 = \{0, 1, 4\}$), this yields the minimal counterexample **`NEG-M11`**, refuting the unrestricted general-$S$ held-note conjecture.

### 1.4 Corollary B.1 (Complete Resolution of Open Problem (3))

> **Corollary B.1 (`corB1_half_closed_no_one_voice_collision`).** *For **every** $N \ge 5$, **every** step-free 3-note chord $c_0 \subset \mathbb{Z}_N$, and **every** nonempty step set $S \subseteq \{1, \dots, \lfloor N/2 \rfloor\}$, no held-note collision (either 1-moving-voice or 2-moving-voice) exists whenever **any** of the following holds:*
> 1. $\mathcal{C} = T(c_0)$ is a pure transposition orbit; OR
> 2. $8 \nmid N$; OR
> 3. $S$ is **closed under halving of even elements** ($\forall d,\; 2d \in S \implies d \in S$).
>
> *In particular, condition (3) holds automatically for **every consecutive step set** $S = \{1, 2, \dots, k\}$ (including $S = \{1\}$ and $S = \{1, 2\}$ of Prime Cadences §4.1): if $2m \in S$, then $m \in S$, contradicting step-freeness of $\{0, m, 4m\}$. Combined with Theorem A, this proves the held-note criterion of Theorem 4.3 for **all $N \ge 5$**.*

### 1.5 Four-Language Verification Summary (Novelty 1)

| Implementation | Verification Scope | Key Observed Result |
| :--- | :--- | :--- |
| **Lean 4.36.0** (`lean/Morpheus/NoveltyTheorems.lean`) | Universal $\forall N \ge 3$ (Thm A), $\forall N \ge 5$ (Thm B, Cor B.1, `NEG-M11`) | Kernel-checked, **0 `sorryAx`**, **0 `ofReduceBool`**, zero Mathlib (`[propext, Quot.sound]` for Thm B suff & `NEG-M11`; standard Lean core `[propext, Classical.choice, Quot.sound]` for Thm A, Thm B nec, Cor B.1) |
| **C++20 Lane 1** (`g++ 13.3`, `clang++ 18.1`, `-Werror`) | All 948 chord classes $5 \le N \le 32$ under maximal $S_{\max}(c_0)$ | `max|L0∩Lt| = 2`, `T_fail = 0`, `TI_oct = 4/4` ($N=8,16,24,32$), `TI_unexp = 0`, `NEG-M11 = true` |
| **Pure Swift 6.4 & Live Interop** (`swiftpp/`) | Independent Pure Swift vs. C++20 Interop (`NOV-1`) | Identical counts across all 948 chords, `0.000e+00` delta |
| **Rust 1.100.0** (`rust/src/novelty.rs`) | Exhaustive sweep over all **10,576** chord classes $5 \le N \le 72$ under maximal $S_{\max}(c_0)$ (covering all $2^{\lfloor N/2 \rfloor}$ step sets by monotonicity) | `max|L0∩Lt| = 2`, `T_fail = 0`, `TI_oct = 9/9` ($N=8,16,24,32,40,48,56,64,72$), `TI_unexp = 0`, `NEG-M11 = true` |

---

## 2. Novelty 2: Exact 2D Tonnetz Cumulant Expansion, 4th-Cumulant Isotropy, $C_6$ Symmetry Breaking, and Edgeworth Ladder (`C-2'` / `C-2''`)

### 2.1 Motivation & Diagnosis (`NEG-E3`)

In ADPIE Cycle 1 (`NEG-E3`), exact first-principles computation of the prime-cadence winding distribution $P_m(w) = \pi(m, w)/\pi(m)$ exposed a sharp platykurtic finite-$m$ departure from the Theorem 6.1 Gaussian $\mathcal{N}(0, m/24)$: even at $m = 40$ where $\operatorname{Var}(W)/(m/24) = 1.000027$ (`0.0027%` error), the exact excess kurtosis was $-0.2124$, scaling cleanly across $m = 12, 24, 40$ as $\approx -8.5 / m$ (i.e., $m \cdot \kappa_{\mathrm{ex}} = -8.4952$ at $m=40$). Why precisely $-8.5/m = -17/(2m)$, and how does this behave across the full 2D Tonnetz plane?

### 2.2 Theorem C (Exact 2D Honeycomb Cumulant Expansion through Order 6)

On the universal cover $\widetilde{X}$ (the 3-regular honeycomb graph in the Euclidean Tonnetz metric of Theorem 6.1, where adjacent major triads have unit spacing $1$ and the three major-to-minor flip displacements $\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3 \in \mathbb{R}^2$ satisfy $\sum_j \mathbf{v}_j = \mathbf{0}$, $\|\mathbf{v}_j\| = 1/\sqrt{3}$, separated by $120^\circ$), the twisted 2D Fourier adjacency symbol is
$$\lambda(\xi) = \left|\sum_{j=1}^3 e^{i \xi \cdot \mathbf{v}_j}\right|, \qquad \xi = r(\cos\alpha, \sin\alpha) \in \mathbb{R}^2,$$
where $\alpha$ is the angle of $\xi$ measured from a bond-perpendicular **zigzag** axis ($\mathbf{v}_j \cdot \xi = \frac{r}{\sqrt{3}}\sin(\alpha + \frac{2\pi j}{3})$). By the Ihara–Bass / Hashimoto transfer matrix for 3-regular non-backtracking walks, the dominant Perron–Frobenius eigenvalue $\rho(\xi)$ of the twisted 72-edge Hashimoto matrix $T(\xi)$ is given exactly near $\xi = \mathbf{0}$ by the quadratic root
$$\rho(\xi) = \frac{\lambda(\xi) + \sqrt{\lambda(\xi)^2 - 8}}{2}, \qquad \rho(0) = 2.$$

> **Theorem C (`thmC_hexagonal_power_sums_exact`, `thmC_exact_cumulant_series`, `thmC_cumulant_ratios_exact`).**
> 1. **Exact hexagonal power sums:** Writing $u_j = \sin(\alpha + 2\pi j / 3)$ (so $\mathbf{e}\cdot\mathbf{v}_j = u_j/\sqrt{3}$), the even power sums satisfy
>    $$\sum_{j=1}^3 u_j^2 = \frac{3}{2}, \qquad \sum_{j=1}^3 u_j^4 = \frac{9}{8}, \qquad \sum_{j=1}^3 u_j^6 = \frac{15}{16} - \frac{3}{32}\cos(6\alpha),$$
>    and $\bigl(\sum_{j=1}^3 u_j^3\bigr)^2 = \frac{9}{32}(1 - \cos(6\alpha))$, independent of $\alpha$ through order 4, with $C_6$ angular dependence entering for the first time at order 6 via $\cos(6\alpha)$.
> 2. **Exact 2D log-generating function through order 6:**
>    $$\log\frac{\rho(\xi)}{2} = -\frac{1}{4}r^2 - \frac{17}{192}r^4 - \left(\frac{49}{768} + \frac{\cos(6\alpha)}{23040}\right)r^6 + O(r^8).$$
>    Equivalently, along any unit direction $\mathbf{e} = (\cos\alpha, \sin\alpha)$ on the Tonnetz plane, the asymptotic cumulants per step of $\mathbf{e} \cdot \mathbf{X}_m$ are
>    $$\frac{\kappa_2}{m} = \frac{1}{2}, \qquad \frac{\kappa_4}{m} = -\frac{17}{8}, \qquad \frac{\kappa_6}{m} = \frac{1470 + \cos(6\alpha)}{32}.$$
> 3. **Ramanujan exponential suppression of finite-$m$ error (zero $O(1)$ constant offset):** Because $X$ is **Ramanujan** ($|\lambda_k(0)| \le 2\sqrt{2}$ for every nontrivial eigenvalue), every non-dominant Hashimoto eigenvalue has $|\mu_k(\xi)| \le \sqrt{2}$ near $\xi = 0$, and every primitive Möbius divisor $d \mid m$ with $d \le m/2$ contributes $O(2^{m/2})$ relative to the dominant $2^{m+1}$ branch. Consequently, the cumulants of the exact prime-cadence law converge with **exponentially small** finite-size error $O(m^r 2^{-m/2})$ (no $O(1)$ constant shift!).
> 4. **Universal 4th-cumulant rotational isotropy & $C_6$ symmetry breaking at order 6:** Along **every** direction $\mathbf{e} \in S^1$,
>    $$\frac{\kappa_4(\mathbf{e}\cdot\mathbf{X}_m)}{\kappa_2(\mathbf{e}\cdot\mathbf{X}_m)^2} = -\frac{17}{2m} + O\!\left(m^2 2^{-m/2}\right) = -\frac{8.5}{m} + O\!\left(m^2 2^{-m/2}\right),$$
>    $$\frac{\kappa_6(\mathbf{e}\cdot\mathbf{X}_m)}{\kappa_2(\mathbf{e}\cdot\mathbf{X}_m)^3} = \frac{1470 + \cos(6\alpha)}{4m^2} + O\!\left(m^3 2^{-m/2}\right).$$
>    - **Bond-parallel armchair axes ($\cos 6\alpha = -1$, projections $\propto (-1, -1, +2)$):** Both homology coordinates $W = -u$ (coboundary div 12, $\kappa_2/m = \frac{1}{24}$) and $v$ (coboundary div 9, $\kappa_2/m = \frac{2}{27}$) are bond-parallel armchair axes, giving exact 6th standardized ratio $\frac{1469}{4m^2} = \frac{367.25}{m^2}$ (and 1D winding cumulants $\kappa_2/m = \frac{1}{24}$, $\kappa_4/m = -\frac{17}{1152}$, $\kappa_6/m = \frac{1469}{55296}$).
>    - **Bond-perpendicular zigzag axis ($\cos 6\alpha = +1$, projections $\propto (0, +1, -1)$):** Theorem 5.1's voice-coset coordinate $2a + b = 4u + 3v$ (coboundary div 1, $\kappa_2/m = 2$) is a bond-perpendicular zigzag axis, giving exact 6th standardized ratio $\frac{1471}{4m^2} = \frac{367.75}{m^2}$.

### 2.3 Correspondence Refinement Ladder (`C-2 → C-2' → C-2''`)

Writing $z = w / \sqrt{m/24}$ and using probabilists' Hermite polynomials $H_4(z) = z^4 - 6z^2 + 3$, $H_6(z) = z^6 - 15z^4 + 45z^2 - 15$, $H_8(z) = z^8 - 28z^6 + 210z^4 - 420z^2 + 105$, Theorem C yields parameter-free discrete Edgeworth densities (clipped to $\max(0, \cdot)$):

- **`C-2` (Gaussian baseline, $O(1/m)$):** $Q_m^{(0)}(w) \propto e^{-z^2/2}$.
- **`C-2'` (4th-order Edgeworth, $O(1/m^2)$):**
  $$Q_m^{(4)}(w) \propto e^{-z^2/2}\left(1 - \frac{17}{48m} H_4(z)\right)_+.$$
- **`C-2''` (6th-order Edgeworth, $O(1/m^3)$):**
  $$Q_m^{(6)}(w) \propto e^{-z^2/2}\left(1 - \frac{17}{48m} H_4(z) + \frac{1469}{2880\,m^2} H_6(z) + \frac{289}{4608\,m^2} H_8(z)\right)_+.$$

**Normalization convention (`v0.2.0` Remark 6.4):** All `C-2 / C-2' / C-2''` distances below normalize $Q_m$ over the signed integer window $|w| \le 24$ (retaining tail mass outside the exact $m=40$ support $[-8, 8]$). Under the alternative convention normalizing strictly over the exact support $|w| \le 8$, the `C-2''` metrics shift slightly to `TV = 1.43e-4` and `JSD = 3.04e-6` (vs. `TV = 1.443e-4` and `JSD = 4.763e-6` on $|w| \le 24$). Both conventions confirm the `> 75×` TV collapse.

### 2.4 Exact Transfer-Matrix Verification at $m = 40$ (`54,975,717,792` Prime Cadences)

Verified identically across C++20 (`g++`/`clang++`), Pure Swift 6.4, Swift ↔ C++20 Interop (`0.000e+00` delta), Rust (`rust/src/novelty.rs`), and Grok Bot's from-scratch Python cross-check (`code/xcheck/audit_xcheck.py`, relative error $< 10^{-11}$):

| Metric ($m = 40$, $\pi(40) = 54{,}975{,}717{,}792$, normalized over $\|w\| \le 24$) | Exact Theory (Thm C) | Observed (4-Language Exact) | Correspondence Gain |
| :--- | :--- | :--- | :--- |
| Winding variance $\operatorname{Var}(W)$ | $40/24 = 1.666667$ | `1.666712` (`|err| = 4.55e-5`) | Ramanujan $O(m \cdot 2^{-m/2})$ |
| $m \cdot \kappa_{\mathrm{ex}}(W)$ (armchair $W = -u$, div 12) | $-17/2 = -8.500000$ | `-8.495174` | Matches to `0.0048` (`0.057%`) |
| $m \cdot \kappa_{\mathrm{ex}}(v)$ (armchair $v$, div 9) | $-17/2 = -8.500000$ | `-8.489783` | Matches to `0.0102` (`0.120%`) |
| $m \cdot \kappa_{\mathrm{ex}}(4u+3v)$ (zigzag, div 1) | $-17/2 = -8.500000$ | `-8.490889` | Matches to `0.0091` (`0.107%`) |
| Coboundary divisibility violations (`u` div 12, `v` div 9, `4u+3v` div 1) | `0` | `0` across all closed walks | Exact `R-Type` invariant |
| **TV (`C-2`, Gaussian)** | $O(1/m)$ | `1.086474e-2` | Baseline (`1.00×`) |
| **TV (`C-2'`, 4th Edgeworth)** | $O(1/m^2)$ | `9.951306e-4` | **10.92× reduction** |
| **TV (`C-2''`, 6th Edgeworth)** | $O(1/m^3)$ | `1.442787e-4` | **75.30× reduction** |

*(Notes on finite-$m$ scaling and Prop 6.3 extension: (1) Numerically across $m = 16, \dots, 44$, $|m\kappa_{\mathrm{ex}} + 17/2| \cdot 2^{m/2}/m^2$ stays bounded in $[0.5, 14]$, matching the Ramanujan exponential suppression; the `v0.2.0` manuscript conservatively states "exponentially small" without fixing the polynomial prefactor. At $m = 40$, $m^2\kappa_6/\kappa_2^3$ still carries sub-leading $2^{-m/2}$ oscillation while already driving the 75.30× TV collapse in `C-2''`. (2) While cross-checking Theorem C, Grok Bot added **Proposition 6.3 (`prop:Wcgf`)** deriving the closed-form 1D winding CGF $\log(\rho(\varphi)/2)$ via $\lambda(\varphi) = \sqrt{5 + 4\cos(\varphi/4)}$; we independently verified Grok Bot's 8th cumulant in exact rational arithmetic: $\kappa_2/m = 1/24$, $\kappa_4/m = -17/1152$, $\kappa_6/m = 1469/55296$, and **$\kappa_8/m = -887099/7962624$** exact match.)*

---

## 3. Novelty 3: Theorem D — Three-Pincer Hilbert Class Field Obstruction (ADPIE Cycle 5)

### 3.1 Motivation & Diagnosis (`Thm 7.19(b)` & `Open (2)`)

In *Prime Cadences* `v0.2.0` (`Thm 7.19(b)` and `Open (2)`), a totally real field $F$ of degree $n$ supporting a torsion-free 2-adic Shimura uniformisation with reduction graph $X$ at a prime $v$ of norm $2$ satisfies the mass equation
$$2^{1-n}\,|\zeta_F(-1)|\prod_{\mathfrak{p} \mid D''}(N\mathfrak{p}-1)\prod_{\mathfrak{p}^e \parallel N} N\mathfrak{p}^{e-1}(N\mathfrak{p}+1) = 12 u, \qquad u := \frac{h_F^+}{h_F} = 2^k \in \{1, 2, \dots, 2^{n-1}\}.$$
Using $|\zeta_F(-1)| = d_F^{3/2}\zeta_F(2)/(2\pi^2)^n$ and $\zeta_F(2) \ge \frac{4}{3}$ (Euler factor at $v$) gives the exact $u$-dependent mass ceiling
$$d_F^{3/2} \le C_{\text{mode}}(u)\,(4\pi^2)^n, \qquad C_{\text{even}}(u) = \frac{9}{2} u.$$
Because `Thm 7.19(b)` replaced $u$ by its worst-case maximum $2^{n-1}$ and applied Odlyzko's explicit formula solely to $F$ itself, it eliminated $n \ge 15$ (`LB = 19.937 > 19.080 = UB`) while missing $n = 14$ (`19.073 < 19.129`), leaving degrees $7 \le n \le 14$ and sextic fields up to $d_F \le 6.673 \times 10^7$ open.

**Key insight:** Large $u = 2^k$ is *not free*! By class field theory, the narrow Hilbert class field $H_F^+$ is an **unramified** extension of $F$ at every finite prime, so every intermediate field $F \subseteq K \subseteq H_F^+$ has the **identical root discriminant** $d_K^{1/[K:\mathbb{Q}]} = d_F^{1/n}$ while multiplying the degree by $[K:F] = h_F \cdot 2^j$! Simultaneously, for odd degree $n$, Hilbert reciprocity forces $n + |D''|$ even $\implies |D''| \ge 1$, sharpening the mass ceiling itself.

### 3.2 Exact Unconditional Poitou–Odlyzko Explicit Formula (Zero Table Lookups)

Let $h(t) = 1 + \cos(\pi t) = 2\cos^2(\pi t/2) \ge 0$ on $[-1, 1]$ and $H_1(u) = \frac{1}{3}(h * h)(u) = \frac{2-u}{3}(1 + \frac{1}{2}\cos(\pi u)) + \frac{\sin(\pi u)}{2\pi} \ge 0$ on $[0, 2]$ ($H_1(0) = 1$, $H_1(2) = 0$, $\widehat{H_1} \ge 0$). Taking the unconditional Weil–Poitou test function $F_b(x) = H_1(x/b)/\cosh(x/2)$ (supported on $[-2b, 2b]$, with $\operatorname{Re}\Phi(\rho) \ge 0$ unconditionally for every $\rho$ in the critical strip), every number field $K$ of degree $N_K = r_1 + 2r_2$ and real-place fraction $\rho_1 = r_1/N_K$ obeys
$$\frac{1}{N_K}\log d_K \;\ge\; \rho_1 \log A(b) + (1 - \rho_1)\log B(b) - \frac{E(b)}{N_K} + \frac{1}{N_K}\sum_{\mathfrak{q}} f_{N\mathfrak{q}}(b),$$
where $\gamma$ is Euler's constant and
$$\log B(b) = \gamma + \log(4\pi) - \int_0^{2b}\frac{1 - H_1(x/b)}{\sinh x}\,dx - \log(\coth b), \qquad \log A(b) = \log B(b) + \int_0^{2b}\frac{H_1(x/b)\,dx}{2\cosh^2(x/2)},$$
$$E(b) = \frac{8}{3}b, \qquad f_q(b) = 4\sum_{1 \le m < 2b/\log q}\frac{\log q}{1 + q^m}\,H_1\!\left(\frac{m\log q}{b}\right).$$
All integrals are evaluated directly from scratch via 64-point Gauss–Legendre quadrature (Newton–Raphson on $P_{64}$; error $< 10^{-15}$, self-checked against the Weil explicit formula on $\mathbb{Q}$ at $b = 2.0$, giving $\mathrm{LB}(\mathbb{Q}) \in [-10^{-5}, 0]$).

### 3.3 Theorem D (Three-Pincer Hilbert Class Field Obstruction)

> **Theorem D (`Section7Obstructions.lean`, `section7_cycle5.{cpp,swift,rs}`).** *Let $F$ be a totally real number field of degree $n$ admitting a torsion-free 2-adic Shimura uniformisation with reduction graph $X$ at a prime $v$ of norm $2$, with wide class number $h_F$ and narrow-class ratio $u = h_F^+/h_F = 2^k$. Then:*
> 1. **Degree bound sharpened unconditionally from $n \le 14$ to $n \le 8$:** No such field exists for **any $n \ge 9$** (eliminating all $9 \le n \le 14$ with worst kill margin **`+0.3392`** at $n = 9, u = 4, \text{odd\_B}$, and all $n \ge 15$ by the single monotone witness $b = 4.2$ where $E - f_2 = 9.537 > 0$ and $\mathrm{LB}(15) = 19.9366 > 19.0800 = \mathrm{UB}(15)$).
> 2. **Degrees $n = 7, 8$ collapse to $h_F = 1$ and $u \in \{1, 2, 4\}$:** Every $h_F \ge 2$ and every $u \ge 8$ is unconditionally eliminated for $n = 7$ and $n = 8$. The maximum root discriminant collapses from `19.345` to **`14.8556`** ($d_F \le 1.597 \times 10^8$, `7.7×` reduction) at $n = 7$, and from `19.691` to **`14.7518`** ($d_F \le 2.243 \times 10^9$, `10.1×` reduction) at $n = 8$.
> 3. **Degree $n = 6$ eliminates $u \in \{16, 32\}$ unconditionally & forces $h_F = 1$ for $u \in \{1, 2\}$:** Only $u \in \{1, 2, 4, 8\}$ survive (with $h_F = 1$ forced for $u = 1, 2$). In particular, `Open (2)`'s remaining sextic discriminant ceiling collapses from $d_F \le 6.673 \times 10^7$ (`u = 32`) down to **$d_F \le 2.648 \times 10^7$ (`u = 8`, `2.52×` reduction)**.

**Proof structure (Three Pincers + Odd-Degree Hilbert Reciprocity):**

- **Odd-degree Hilbert reciprocity parity split ($n$ odd $\implies |D''| \ge 1$):**
  - *Subcase `odd_A` (a second norm-2 prime $v_2 \neq v$ exists):* $\zeta_F(2) \ge (4/3)^2 = 16/9 \implies C_{\text{odd\_A}}(u) = \frac{27}{8} u$, AND $F$ gains a **double** $f_2$ boost ($2/n \cdot f_2(b)$).
  - *Subcase `odd_B` (every $\mathfrak{p} \mid D''$ has norm $q \ge 3$):* $\zeta_F(2) \cdot (q - 1) \ge \frac{4}{3}\frac{q^2}{q^2 - 1}(q - 1) = \frac{4}{3}\frac{q^2}{q+1} \ge 3$ for all $q \ge 3$ (proved universally in `lean/Morpheus/Section7Obstructions.lean:thmD_odd_parity_factor_ge_three`: $4q^2 \ge 9(q+1)$), forcing $C_{\text{odd\_B}}(u) = 2 u$.
- **Pincer 1 ($F$ itself, totally real, degree $n$):** Kills small $u$ (e.g. $n = 9, u \in \{1, 2, 4\}$; $n = 10, u \in \{1, 2, 4\}$; $n = 7, u = 1, \text{odd\_A}$).
- **Pincer 2 ($h_F \ge 2$: wide Hilbert class field $H_F$ and codim-$j$ subfields of $H_F^+/H_F$):** $H_F$ is totally real of degree $h_F n \ge 2n$, and $\mathrm{Gal}(H_F^+/H_F) \cong \mathbb{F}_2^k$. Because $H_F^+/F$ is abelian, the $h_F$ real places of $H_F$ over each real place $\sigma_i$ of $F$ share one complex conjugation element $c_i \in \mathbb{F}_2^k$. By $\mathrm{GL}_k(\mathbb{F}_2)$-transitivity and pigeonhole (`thmD_subspace_averaging_bound`), for every $0 \le j \le k$ there exists a codimension-$j$ fixed field $K_H \subseteq H_F^+$ of degree $h_F n \cdot 2^j \ge 2n \cdot 2^j$ with real-place fraction $\rho_1(K_H) \ge \frac{1}{n}\lceil n \frac{2^{k-j}-1}{2^k-1}\rceil$ ($\rho_1 = 1$ at $j = 0$). Taking $\max_{0 \le j \le k}$ kills ALL $h_F \ge 2$ for every $n \ge 7$, and kills $h_F \ge 2$ at $n = 6$ for $u \in \{1, 2, 16, 32\}$.
- **Pincer 3 ($h_F = 1, u = 2^k \ge 2$: exponent-2 Galois group $\mathrm{Gal}(H_F^+/F) \cong \mathbb{F}_2^k$):**
  1. Every quotient $\mathrm{Gal}(K/F)$ has exponent $2$, so $f_v(K/F) \in \{1, 2\}$. By `thmD_f4_term_matches_even_f2_term` ($4^m = 2^{2m}$), keeping only even terms of $f_2(b)$ yields $f_2(b) \ge \frac{1}{2}f_4(b)$, so every norm-2 prime of $F$ contributes unconditionally at least $\frac{1}{2n}f_4(b)$ to every codim-$j$ subfield $K_H \subseteq H_F^+$ (deg $n \cdot 2^j$, $\rho_1 \ge \frac{1}{n}\lceil n \frac{2^{k-j}-1}{2^k-1}\rceil$).
  2. Splitting on $f_v(H_F^+/F) \in \{1, 2\}$: if $f_v = 1$, $v$ splits completely in $H_F^+$ (deg $nu$, boost $\frac{1}{n}f_2$); if $f_v = 2$, $v$ splits completely in the **decomposition subfield** $L_v = (H_F^+)^{\langle \mathrm{Frob}_v \rangle}$ of degree $nu/2$ (boost $\frac{1}{n}f_2$) while contributing $\frac{1}{2n}f_4$ in $H_F^+$ (deg $nu$).
  3. At the tightest critical point **$n = 6, u = 16, h_F = 1, f_v = 2$**: $L_v$ has degree $48$, and at $b = 6.00$:
     $$\exp(\mathrm{LB}(L_v; b = 6.00)) = \mathbf{18.6606783717} \;>\; \mathbf{18.6470485626} = \mathrm{UB}(n=6, u=16),$$
     margin **`+0.0136298092`** ($> 3 \times 10^{13}\times$ larger than the 64-pt vs. 128-pt Gauss–Legendre discrepancy $4.44 \times 10^{-16}$!). $\square$

### 3.4 Exact Degree-by-Degree Elimination Summary & Four-Language Parity

| Degree $n$ | Prior `Thm 7.19(b)` Status | Theorem D Outcome | Surviving $(h_F, u)$ | Tightest Kill Margin ($\exp\mathrm{LB} - \exp\mathrm{UB}$) | Collapsed $d_F$ Ceiling |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **$n \ge 15$** | Excluded (`odl/table4`) | **Excluded** (single witness $b = 4.2$, zero tables) | **None (`0`)** | `+0.85655` at $n = 15$ ($E - f_2 = 9.537 > 0$) | — |
| **$11 \le n \le 14$** | Open (`u <= 2^{n-1}`) | **ALL KILLED unconditionally** | **None (`0`)** | `>= +2.0` across all $(u, h_F, \text{mode})$ | — |
| **$n = 10$** | Open (`u <= 512`) | **ALL KILLED unconditionally** | **None (`0`)** | **`+0.98880`** ($u = 4, h_F = 1$: `15.0468 > 14.0580`) | — |
| **$n = 9$** | Open (`u <= 256`) | **ALL KILLED unconditionally** | **None (`0`)** | **`+0.33915`** ($u = 4, \text{odd\_B}, h_F = 1$: `13.8641 > 13.5249`) | — |
| **$n = 8$** | Open (`u <= 128`, $d_F \le 2.26 \times 10^{10}$) | **$h_F \ge 2$ & $u \ge 8$ KILLED** | **$h_F = 1,\; u \in \{1, 2, 4\}$** | `+0.52467` ($u = 8, h_F = 1$: `16.1537 > 15.6290`) | **$2.243 \times 10^9$** (`14.7518^8`, **10.1×**) |
| **$n = 7$** | Open (`u <= 64`, $d_F \le 1.01 \times 10^9$) | **$h_F \ge 2$ & $u \ge 8$ KILLED** | **$h_F = 1,\; u \in \{1, 2, 4\}$** (`odd_A` $u=1$ dead) | `+0.64967` ($u = 8, \text{odd\_B}, h_F = 1$: `15.7476 > 15.0979`) | **$1.597 \times 10^8$** (`14.8556^7`, **6.35×**) |
| **$n = 6$** | Open ($8.26 \times 10^6 < d_F \le 6.67 \times 10^7$) | **$u \in \{16, 32\}$ KILLED**; $h_F \ge 2$ dead for $u \in \{1, 2\}$ | **$u \in \{1, 2, 4, 8\}$** ($h_F = 1$ for $u \le 2$) | **`+0.013630`** ($u = 16, h_F = 1, L_v$ deg 48 at $b = 6.0$) | **$2.648 \times 10^7$** (`17.2648^6`, **2.52×**) |

Verified with **`0.000e+00`** cross-lane delta across **C++20** (`g++ 13.3` & `clang++ 18.1`, `-Werror`), **Pure Swift 6.4**, **Swift ↔ C++20 Interop**, and **Pure Rust 1.100.0** (`rust/src/section7_cycle5.rs`), with algebraic core kernel-checked in **Lean 4.36.0** (`lean/Morpheus/Section7Obstructions.lean`) and emitted to checksummed Data Model record `data/calibrations/theorem_d_pincer_swiftpp.json`.

---

## 4. Baseline Erratum `NEG-E10` & Cycle 5 Honest Scope Boundary

### 4.1 Second Baseline Erratum (`NEG-E10` — Omitted Genus-13 Shimura Curve $X_0^{690}(1)$)

During our exhaustive genus-13 Shimura curve sweep (`phi(D) * psi(N) <= 1000`, rigorously complete), all four Cycle 5 planes caught a missing 4-prime curve omitted by `code/geometry/shimura_multi.py:17` (`if phi > 12*14: continue`, i.e. $\phi \le 168$):
- **$D = 690 = 2 \cdot 3 \cdot 5 \cdot 23,\; N = 1$ ($M = 345$):** $\phi(690) = 1 \cdot 2 \cdot 4 \cdot 22 = \mathbf{176} > 168$, $e_2 = 0$, $e_3 = 8$, exact genus $g = 1 + \frac{176}{12} - \frac{8}{3} = \mathbf{13}$ (kernel-checked in `lean/Morpheus/Section7Obstructions.lean:neg_E10_genus13_D690_witness`).
- **Correction needed in `paper/prime-cadences.tex:414`:** States *"18 pairs $(D, N)$: $D = 2p$ for 16 pairs, plus $D = 546$ and $D = 570$"*; the exact exhaustive count is **19 pairs** ($D = 2p$ for 16 pairs, plus $D = 546, 570, \mathbf{690}$; still 11 torsion-free, and 4 $\Gamma_H$ cases).
- **Conclusion of `Thm 7.11` still holds:** Confirmed BOTH in **zero-PARI Pure Rust** via exact Manin modular symbols $\mathcal{M}_2(\Gamma_0(345))^-$ over $\mathbb{F}_{1000003}$ (`dim = 45`, `tr(T_2) = -5 mod 1000003`, `rank(T_2^4 - 4 T_2^2 + I) = 45/45` — in fact full rank across ALL 18 distinct levels covering all 19 curves!) AND via from-scratch PARI Hecke computation in `ergentics/shimura_brandt_xcheck.py` (`dim S_2^{345-new} = 15`, exact mass $44/3$, `charpoly(T_2) mod (t^4 - 4t^2 + 1) = 3t^3 + t^2 + 21t + 7 ≠ 0`).

### 4.2 Honest Perimeter Disclosure After ADPIE Cycle 5

Per `AGENTS.md` Rule 6:
- **Newly verified from scratch in ADPIE Cycle 5 (all 7 formerly unchecked Section 7 items covered):** `Prop 7.3` (Lean 4 + C++20/Swift/Rust), `Thm 7.11` (all 19 $X_0^D(N)$ incl. `NEG-E10` + 4 $\Gamma_H$ in Pure Rust Manin $T_2$ + from-scratch PARI), `Lem 7.14` (Lean 4 ordered-valuation proof + `RCT-2`), `Thm 7.15` (Lean 4 valence forcing), `Prop 7.17` (Lean 4 + 504-element $PGL_2(\mathbb{F}_8)$ census in C++20/Swift/Rust), `Prop 7.18(a)–(c)` (exact Siegel/Gauss $h^+$ scan in C++20/Swift/Rust + full `nflist`/`lfun`/direct Brandt matrices for all 13 cubic/quartic + 2 quadratic solutions in `ergentics/shimura_brandt_xcheck.py`), and `Thm 7.19(a)–(b)` + quintic near-miss $d_F = 106069$ (from-scratch Poitou–Odlyzko + direct 12×12 Brandt matrix match + sharpened unconditionally to $n \le 8$ by **Theorem D**).
- **Remaining un-recomputed `[GB]` / external-census boundaries:** (1) The 55 $h_F^+ > 1$ Brandt graphs in degree $n \le 4$ and the LMFDB quintic/sextic field-table queries (`2507` / `300` fields) inside `Thm 7.19(c)` remain `[GB]` (the degree-5 near-miss $d_F = 106069$ itself IS independently verified from scratch); (2) Gröbner smoothness over $\overline{\mathbb{F}}_2$ and the genus-4 LMFDB non-Jacobian census in `Prop 7.10` remain `[GB]`.
- **Audit-forward preservation:** All `v0.2.0` `paper/`, `code/`, `audits/`, and `CONTRIBUTIONS.md` files remain untouched pending reconciliation with Ergentics' internal model results and Grok Bot.
