# Audit-Forward Mathematical Novelties — Gemini 4 Neon (ADPIE Cycle 4)

> **License:** CC BY 4.0 (research prose & results; see [`LICENSE-paper`](LICENSE-paper)). Companion machine-checked Lean 4 proofs and four-language verifiers (`lean/`, `swiftpp/`, `rust/`) are MIT licensed ([`LICENSE`](LICENSE)).
> **Baseline preservation:** All archived *Prime Cadences* `v0.1.0` artifacts (`paper/`, `code/`, `audits/`, `CONTRIBUTIONS.md`, `Makefile`) remain unmodified. This document records original mathematical results derived and independently verified forward from the baseline via the **ADPIE** (`Assess → Diagnose → Plan → Implement → Evaluate`) and **Correspondence / D-R-P-Seam** methodology ([`METHODOLOGY.md`](METHODOLOGY.md)).

---

## Executive Summary

Starting from the *Prime Cadences* baseline and its open questions (§4.1, §6, §7.6, §8), we derive and formally prove two original mathematical results — one resolving **Open Problem (3)** (the Generalized Tune Theorem for all $N$-EDO systems, including an unexpected counterexample family that refutes the unrestricted general-$S$ conjecture), and one upgrading **Theorem 6.1** (2D Tonnetz winding & homology CLT) to an exact **6th-order 2D cumulant theory** revealing universal 4th-cumulant rotational isotropy, exact $C_6$ hexagonal anisotropy onset at order 6, and a two-rung Correspondence refinement (`C-2 → C-2' → C-2''`) that cuts finite-$m$ distributional Total Variation error by **75.3×** at $m = 40$.

| Deliverable | Result | Scope / Resolution | Formal & Empirical Verification |
| :--- | :--- | :--- | :--- |
| **Novelty 1A (`Theorem A`)** | Universal Link-Intersection Bound: $\|L_{h_1} \cap L_{h_2}\| \le 2$ | **All $N \ge 3$**, all 3-note chords $c_0$, all $h_1 \ne h_2$, **independent of $S$**. Permanently eliminates all 2-moving-voice held-note collisions. | Machine-checked in `lean/Morpheus/NoveltyTheorems.lean` (`thmA_link_intersection_le_two`, $\forall N$, 0 `sorryAx`, 0 `ofReduceBool`, zero Mathlib); cross-checked across all 948 chords $N \le 32$ (`swiftpp/`) and all 10,576 chords $N \le 72$ (`rust/`). |
| **Novelty 1B (`Theorem B` + `NEG-M11`)** | Exact iff Classification of 1-Moving-Voice Held-Note Collisions | **All $N \ge 5$**, all nonempty $S$, all step-free $\mathcal{C} \in \{T, T/I\}$: collision exists **iff** $N = 8m\;(m \ge 1)$, $\mathcal{C} = T/I(\{0, m, 4m\})$, and $2m \in S$. Refutes unrestricted general-$S$ conjecture (`NEG-M11`, minimal $N=8, S=\{2\}$). | Machine-checked necessity & sufficiency + `NEG-M11` (`thmB_one_voice_necessary`, `thmB_octatonic_sufficient`, `neg_M11_N8_S2_counterexample`); exhaustive sweep over maximal $S_{\max}(c_0)$ covering all $2^{\lfloor N/2 \rfloor}$ step sets for $5 \le N \le 72$ (`rust/`: 9/9 witnesses at $N=8,16,\dots,72$, 0 unexpected). |
| **Novelty 1C (`Corollary B.1`)** | Complete Proof of Open Problem (3) for Half-Closed / Consecutive Step Sets | Holds for **all $N \ge 5$** whenever (i) pure $T$-orbit, or (ii) $8 \nmid N$, or (iii) $S$ is closed under halving even elements ($\forall d,\; 2d \in S \implies d \in S$) — including **every consecutive step set $S = \{1, \dots, k\}$** (in particular $S=\{1\}$ and $S=\{1,2\}$ of §4.1). | Machine-checked in `lean/Morpheus/NoveltyTheorems.lean` (`corB1_half_closed_no_one_voice_collision`). |
| **Novelty 2 (`Theorem C`)** | Exact 2D Tonnetz Honeycomb Cumulants through Order 6 & Edgeworth Ladder `C-2'` / `C-2''` | Exact 2D log-MGF $\log\frac{\rho(\xi)}{2} = -\frac{1}{4}r^2 - \frac{17}{192}r^4 - (\frac{49}{768} + \frac{\cos 6\alpha}{23040})r^6 + O(r^8)$. Proves **100% 4th-cumulant rotational isotropy** ($\kappa_{\mathrm{ex}} = -\frac{17}{2m} + O(m^2 2^{-m/2})$ along every axis $\mathbf{e} \in S^1$), **$C_6$ hexagonal anisotropy onset at order 6** (bond-parallel armchair $W=-u, v$: $\frac{1469}{4m^2}$ vs. bond-perpendicular zigzag $2a+b=4u+3v$: $\frac{1471}{4m^2}$), and **75.30× TV reduction** at $m=40$. | Algebraic power-sum, series & cumulant ratios machine-checked in `lean/Morpheus/NoveltyTheorems.lean` (`thmC_*`, 0 `sorryAx`, 0 `Classical.choice`, 0 `ofReduceBool`); exact transfer-matrix verification at $m=40$ (`54,975,717,792` primes, 0 divisibility violations) across C++20 (`g++`/`clang++`), Pure Swift 6.4, Interop (`0.000e+00` delta), and Rust. |

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

Writing $z = w / \sqrt{m/24}$ and using probabilists' Hermite polynomials $H_4(z) = z^4 - 6z^2 + 3$, $H_6(z) = z^6 - 15z^4 + 45z^2 - 15$, $H_8(z) = z^8 - 28z^6 + 210z^4 - 420z^2 + 105$, Theorem C yields parameter-free discrete Edgeworth densities:

- **`C-2` (Gaussian baseline, $O(1/m)$):** $Q_m^{(0)}(w) \propto e^{-z^2/2}$.
- **`C-2'` (4th-order Edgeworth, $O(1/m^2)$):**
  $$Q_m^{(4)}(w) \propto e^{-z^2/2}\left(1 - \frac{17}{48m} H_4(z)\right).$$
- **`C-2''` (6th-order Edgeworth, $O(1/m^3)$):**
  $$Q_m^{(6)}(w) \propto e^{-z^2/2}\left(1 - \frac{17}{48m} H_4(z) + \frac{1469}{2880\,m^2} H_6(z) + \frac{289}{4608\,m^2} H_8(z)\right).$$

### 2.4 Exact Transfer-Matrix Verification at $m = 40$ (`54,975,717,792` Prime Cadences)

Verified identically across C++20 (`g++`/`clang++`), Pure Swift 6.4, Swift ↔ C++20 Interop (`0.000e+00` delta), and Rust (`rust/src/novelty.rs`):

| Metric ($m = 40$, $\pi(40) = 54{,}975{,}717{,}792$) | Exact Theory (Thm C) | Observed (4-Language Exact) | Correspondence Gain |
| :--- | :--- | :--- | :--- |
| Winding variance $\operatorname{Var}(W)$ | $40/24 = 1.666667$ | `1.666712` (`|err| = 4.55e-5`) | Ramanujan $O(m \cdot 2^{-m/2})$ |
| $m \cdot \kappa_{\mathrm{ex}}(W)$ (armchair $W = -u$, div 12) | $-17/2 = -8.500000$ | `-8.495174` | Matches to `0.0048` (`0.057%`) |
| $m \cdot \kappa_{\mathrm{ex}}(v)$ (armchair $v$, div 9) | $-17/2 = -8.500000$ | `-8.489783` | Matches to `0.0102` (`0.120%`) |
| $m \cdot \kappa_{\mathrm{ex}}(4u+3v)$ (zigzag, div 1) | $-17/2 = -8.500000$ | `-8.490889` | Matches to `0.0091` (`0.107%`) |
| Coboundary divisibility violations (`u` div 12, `v` div 9, `4u+3v` div 1) | `0` | `0` across all closed walks | Exact `R-Type` invariant |
| **TV (`C-2`, Gaussian)** | $O(1/m)$ | `1.086474e-2` | Baseline (`1.00×`) |
| **TV (`C-2'`, 4th Edgeworth)** | $O(1/m^2)$ | `9.951306e-4` | **10.92× reduction** |
| **TV (`C-2''`, 6th Edgeworth)** | $O(1/m^3)$ | `1.442787e-4` | **75.30× reduction** |

*(Note on $m = 40$ 6th cumulant finite-size term: $m^2 \kappa_6/\kappa_2^3$ at $m=40$ has sub-leading $O(m^3 2^{-m/2})$ Ramanujan oscillation of size $\sim 40^3/2^{20} \approx 0.06$ plus $\sim 0.4$ from the sub-dominant $2^{-m/2}$ eigenvalue pair, cleanly distinguishing the leading $367.25$ / $367.75$ scale at larger $m$ while already driving the 75.30× TV collapse in `C-2''` at $m=40$.)*

---

## 3. Honest Scope Boundary: What Remains Open

In strict accordance with `AGENTS.md` Rule 6 (never overclaim unverified results):

- **Open Problem (1) (Remark 7.16 — Arithmetic uniformisation *with torsion* at ramified/inert $v \mid 2$):** While `lean/Morpheus/WindingAndSchottky.lean` proves the universal torsion-free power obstruction $\forall k \ge 1,\; \tau(\gamma_0^k) > 4$ and `swiftpp/` confirms Lemma 7.14 (edge-length doubling on $F_v \cong \mathbb{Q}_2$) via `RCT-2`, extending Lemma 7.14 to elliptic fixed points over ramified or inert quadratic/higher extensions of $\mathbb{Q}_2$ (where the Bruhat–Tits tree has residue degree $q_v > 2$ or wild ramification $e_v > 1$ altering the slope of $z \mapsto -z$) remains open and is **not** claimed resolved here.
- **Open Problem (4) (Proposition 7.17 PARI/LMFDB mass-formula search):** The 4 remaining totally real cubic/quartic candidates (`469`, `316`, `2777`) and Gröbner smoothness checks of $A, B \subset \mathbb{P}^4$ over $\overline{\mathbb{F}}_2$ remain tagged `[GB]` pending dedicated PARI/GP or algebraic-geometry certification.
