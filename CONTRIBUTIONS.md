# Contributions and provenance

**Author:** Ergentics (sole author).  
**AI assistance:** Two AI assistants worked independently under Ergentics' direction — **Grok Bot** (`GB`) and **Gemini 4 Neon** (`G4N`). Following standard scholarly practice on AI disclosure, neither AI assistant is listed as an author; both are credited transparently here and in the paper's *Contributions and provenance* section with identical attribution bounds. Full responsibility for the content rests with the author.

These records cover the `v0.3.1` release (25 November 2026), recording the round-2 referee-hardened three-way reconciliation into the single canonical paper (`paper/prime-cadences.tex`, 35 pp PDF, 56 references) across:
1. **Grok Bot** (`GB`, `code/`, Python/SymPy/PARI/LMFDB, `228/228` across 6 suites + `code/xcheck/round2/` `20/20`),
2. **Gemini 4 Neon** (`G4N`, ADPIE Cycles 1–5: `lean/` 33/33 Lean 4.36.0 theorems, `swiftpp/` C++20 × Pure Swift 6.4 × Interop `0.000e+00` delta, `rust/` Rust 1.100.0 incl. zero-PARI Manin $T_2$, `ergentics/` from-scratch PARI/Python verifiers, `data/` 3/3 checksummed calibrations), and
3. **Ergentics' Standalone Clean-Room Research Monograph I** (`E`, [`cleanroom/prime_cadences_resolution/paper.typ`](cleanroom/prime_cadences_resolution/paper.typ), archived verbatim alongside [`cleanroom/prime_cadences_resolution/CONTRIBUTIONS_PATCH.md`](cleanroom/prime_cadences_resolution/CONTRIBUTIONS_PATCH.md); three-way audit in [`reconciliation/THREE_WAY_CLEANROOM_AUDIT.md`](reconciliation/THREE_WAY_CLEANROOM_AUDIT.md)).

## Marker scheme (used uniformly on every numbered result in the paper)

| Tag | Meaning |
| :--- | :--- |
| `[E]` | By Ergentics (including Ergentics' standalone clean-room monograph) |
| `[GB]` | Statement, proof, and computation by Grok Bot |
| `[E→GB]` | Question, direction, or methodology set by Ergentics; statement, proof, and computation by Grok Bot |
| `[G4N]` | Statement, proof, and computation by Gemini 4 Neon |
| `[E→G4N]` | Question, direction, or methodology set by Ergentics; statement, proof, and computation by Gemini 4 Neon |
| `[lit.]` | Result from the cited literature, re-checked computationally/formally |
| `[X]` | Cross-verified across at least two independent toolchains (zero shared cached outputs); `[independently ...]` marks independent derivations reached across separate tracks |

## Ergentics (`E`), direction and clean-room breakthroughs

- Research direction, verification methodology, and all prompts steering both AI assistants.
- The starting point: the Tonnetz and the graph Riemann hypothesis.
- The phasor (Fourier) prompt behind the spectral and arithmetic readings (Thm 3.1, Thm 3.4).
- The melodic-primes question and the redirect "Where does the melody fit?" (Section 4: Lemma 4.1, Thm 4.2, Thm 4.3).
- The push towards Eisenstein integers (Prop 3.7, Thm 3.8).
- "The geometric object deserves its own focus" (Section 7).
- "Chase down those open questions" (Section 4.1 / Thm 4.3, Sections 7.6–7.7, Prop 7.10).
- "Can't you attempt to derive them or find alternatives?" (direct computation of the Brandt graphs, Prop 7.19).
- "I'll wait for you to have a more fuller view" (round 3 of the open questions: held-note theorem, Thm 4.4; torsion structure, Prop 7.17; any narrow class number and the degree bound, Thm 7.20; LMFDB cross-check folded into Prop 7.19).
- The Correspondence Principle, Code-vs-Data non-conflation standard, ADPIE execution loop, D/R/P/Seam SWE-sweep & Rung-1 distributional calibration methodology (`METHODOLOGY.md`, `CALIBRATIONS.md`, `NEGATIVES.md`), and the audit-forward prompt steering Gemini 4 Neon to Cycles 1–5 (independent Thm 4.4, Thm 6.2, Remark 6.4, Thm 7.21, `NEG-E8`, `NEG-E10`).
- **Standalone Clean-Room Research Monograph I (`cleanroom/prime_cadences_resolution/paper.typ`, archived verbatim, reconciled into `v0.3.0`–`v0.3.1` and independently cross-verified `[X]` in `ergentics/open1_torsion_xcheck.py` & `ergentics/shimura_brandt_xcheck.py`):**

| Paper label & tag | Ergentics' clean-room contribution (`[E]`) | Independent cross-verification (`[X]`) |
| :--- | :--- | :--- |
| Thm 4.4 (`thm:held`) `[E→GB; independently E→G4N & E; X]` | Third independent derivation of the exact $N=8m$, $\{0,m,4m\}$, $2m \in S$ held-note classification; exhaustive check over 13,382 systems ($N \le 18$: 17 predicted, 17 observed, 0 mismatches); Euclidean chord-length defect $D(a) = 2 - 2\cos(\pi a) = 4\sin^2(\pi a/2) > 0$ on $(0, \frac14)$ separating non-diameter reflection chords from diameter chords on $\mathbb{R}/\mathbb{Z}$ | Agrees identically with `GB` (`code/open_q/`, `code/xcheck/round2/`) and `G4N` (`lean/Morpheus/NoveltyTheorems.lean`, `rust/` 10,576 chords $N \le 72$) |
| Lemma 7.14 (`lem:length`) `[E→GB; sharpened E; X]` | Explicit char-2 wild-involution counterexample $\sigma(z) = 3/z \in PGL_2(\mathbb{Q}_2)$ (`NEG-M12`, fixed points $\pm\sqrt{3}$ strictly inside $A_e$) + cancellation-free invariant $u(1+x)-4 = x(x-2)/(1+x)$ proving $|u(1+x)-4|_2 = |x|_2^2$ despite interior branching | Independently verified algebraically & 2-adically in `ergentics/open1_torsion_xcheck.py` (Check 1) |
| Prop 7.17(c) (`prop:torsion`) `[E→GB; sharpened E; X]` | Exact length-conservation law $\sum_{i=1}^k |\Gamma_{e_i}| = e_v$; eliminates unsubdivided stabilised edges ($k=1$) for inversion-free $f_v=1, e_v \ge 2$; forces all 36 midpoints into one bipartition class with $|\Gamma_y| = 1$, proving combinatorially sharp floor **$M(\mathcal{O}) \ge 36$** at $e_v=2, f_v=1$ | Independently verified + combinatorial witness ($M = 36$ via 36 $C_3$-leaves, `NEG-M13`) in `ergentics/open1_torsion_xcheck.py` (Check 2) |
| Prop 7.18 (`prop:cyclotomic`) `[E; X]` | **Part (a):** Inversion-free unramified cyclotomic obstruction for arithmetic $\Gamma$ — even $f_v \ge 2$ forces $\mathbb{Q}(\zeta_{2^{f_v}+1})^+ \subset E$ (ruling out $E \not\supset \mathbb{Q}(\sqrt{5})$ at $f_v=2$); odd $f_v \ge 3$ forces $\mathbb{Q}(\zeta_{2^{f_v}+1})^+$ or $\mathbb{Q}(\zeta_{(2^{f_v}+1)/3})^+ \subset E$. **Part (b):** Explicit non-arithmetic Kleinian sharpness counterexample $\Gamma_5 \subset PGL_2(\mathbb{Q}_4)$ with 48 inverted capped edges (`NEG-M14`, $\tau(s_4 s_5) = 49/4 > 4$) | Orbit-stabiliser & $A_4/S_4/A_5$ proof checked; exact $\mathbb{Z}_2[\omega]$ matrices, $s_i^2 = 2I$, Klein ping-pong, $u=z+2/z$ & $\tau(s_4 s_5) = 49/4 > 4$ verified in `ergentics/open1_torsion_xcheck.py` (Check 3) and `code/xcheck/round2/` |
| Prop 7.19 (`prop:mass`) `[E→GB; independently E; X]` | Independent pure-Python monogenic Brandt engine (zero PARI/LMFDB) printing explicit $12 \times 12$ matrices for the six cases over $F_{469}, F_{316}, F_{2777}$ and verifying all eight $\mathbb{Q}[x]$-irreducible factorisations ($|\lambda|_{\mathrm{nt}} \le 2.7508 < 2\sqrt{2}$, $\Delta_X \ge 0.4371$) | **8/8 exact bit-for-bit characteristic polynomial match** against both `GB` and `ergentics/shimura_brandt_xcheck.py` (`reconciliation/THREE_WAY_CLEANROOM_AUDIT.md`) |

- Review of all drafts, three-way reconciliation, and accompanying videos.

## Grok Bot (`GB` / `E→GB`), by section

Theorem numbers follow the compiled `v0.3.1` PDF (amsart, 35 pp); LaTeX `\label{...}` anchors are authoritative.

| Section | Result | Tag | Grok Bot's part |
| :--- | :--- | :--- | :--- |
| 2 | Prop 2.1 (dihedral PLR group) | `lit.` | re-checked by enumeration |
| 2 | Cor 2.2 (Coxeter description, free group of rank 13) | `GB` | statement and proof |
| 3 | Thm 3.1 spectrum = honeycomb bands = Fourier moduli; Ramanujan | `E→GB` | proof and 50-digit check |
| 3 | Thm 3.3 exact prime-cadence counts (to $m = 40$) | `GB` | transfer matrix, Möbius inversion |
| 3 | Thm 3.4 arithmetic of the coefficients (Gaussian/Eisenstein primes, units) | `E→GB` | proof and exact algebra |
| 3 | Thm 3.5 $\zeta_X$ over $\mathbb{Q}$ as Weil polynomials over $\mathbb{F}_2$; explicit curves | `GB` | factorisation, point counts, LMFDB look-ups |
| 3 | Prop 3.7 Tonnetz is not $\mathbb{Z}[\omega]/I$, $\mathbb{Z}[i]/I$ or $\mathbb{Z}[\zeta]/I$ | `E→GB` | refutation |
| 3 | Thm 3.8 order of conductor 2 presentation | `E→GB` | proof |
| 4 | Lemma 4.1, Thm 4.2 tune theorem | `E→GB` | proof; decoder tested on all 174,864 rooted primes of length $\le 16$ (wording corrected via `[G4N]` catch `NEG-E8`) |
| 4 | Thm 4.3 general reduction; held-note criterion | `E→GB` | proof; 6,028 systems verified ($N \le 72$) |
| 4 | Thm 4.4 held-note theorem: proof for every $N$ and step set; exceptional family ($8 \mid N$, class $\{0, N/8, N/2\}$, $N/4 \in S$), smallest $N = 8, S = \{2\}$ | `E→GB; independently E→G4N & E; X` | proof (link graphs have no 4-cycles); brute-force checks for $N \le 26$ and all walks of length $\le 8$ for $N \le 16$ |
| 5 | Thm 5.1 $W = -u$; Thm 5.2 twisted spectrum; Thm 5.3 Riemann window | `GB` / `GB` / `E→GB` | proofs and checks |
| 6 | Thm 6.1 winding law (variance $m/24$, isotropic covariance) | `GB` | proof and numerics |
| 6 | Prop 6.3 all cumulants of $W$ in closed form ($\kappa_8/m = -887099/7962624$) | `GB; X` | derivation from Thm 5.2; exact series check (independently confirmed in exact rational arithmetic by Gemini 4 Neon) |
| 6 | From-scratch cross-check of every `[G4N]` / `[E→G4N]` Cycle 4 claim (Thm 6.2, Cor 4.5, Remark 6.4, Thm 4.4, `NEG-E8`) | `GB` (`X`) | `code/xcheck/`, 32/32 checks, recomputed from scratch with zero cached data reads |
| 7 | Thm 7.1 Schottky group from $P, L, R$; genus-13 curve $C$ | `GB` | construction, proof, verification |
| 7 | Prop 7.2 $\operatorname{Aut} C = T/I$; Prop 7.3 not arithmetic over $\mathbb{Q}$ | `E→GB` | proofs |
| 7 | Thm 7.4 $\mathbb{Z}/12$ tower; Cor 7.5 Ihara factors as characters | `E→GB` | proofs, exact checks |
| 7 | Thm 7.7 sandpile group; Thm 7.8 gonality 6 | `E→GB` | Smith normal form; two independent searches |
| 7 | Prop 7.9 curves over $\mathbb{F}_2$; Prop 7.10 octic in genus 5 (minimal) | `E→GB` | searches, census cross-check, Gröbner smoothness |
| 7 | Thm 7.11 no Shimura curve over $\mathbb{Q}$ | `E→GB; corrected G4N; X` | Hecke computations (PARI; cutoff `NEG-E10` adding $X_0^{690}(1)$ corrected in `v0.3.0`; re-derived from scratch in `code/xcheck/round2/`) |
| 7 | Thm 7.13 trace obstruction; Lemma 7.14 edge lengths; Thm 7.15 $F_v = \mathbb{Q}_2$ | `E→GB; X` (Lemma 7.14: `E→GB; sharpened E; X`) | proofs and numerical controls (wild-involution confirmation folded into Lemma 7.14 in `v0.3.0`) |
| 7 | Prop 7.17 uniformisations with torsion at a place above 2: structure when $e_v = 1$, $f_v = 2$, $f_v \ge 3$, $e_v = 2$ | `E→GB; sharpened E; X` | proof (Bass–Serre, valence count, edge lengths); part (c) sharpened by `[E]` to $M(\mathcal{O}) \ge 36$ |
| 7 | Prop 7.19 (`prop:mass`) graph-level search: mass formula plus direct Brandt-graph computation for all 22 configurations | `E→GB; independently E; X` | field enumeration (PARI); quaternion ideal-class enumeration by $v$-neighbours; second method by theta counts; validated against LMFDB & independently confirmed 8/8 by `[E]` and `[G4N]` |
| 7 | Thm 7.20 (`thm:anyh`) any narrow class number: mass equation, Odlyzko degree bound ($n \le 14$), computations in degrees $\le 5$ and part of degree 6 | `E→GB; X` | field scans (PARI, LMFDB lists), generalised Brandt computation with mass, theta and component checks for $55 + 4$ configurations; Odlyzko Table 4 (degree bound sharpened $n \le 14 \to n \le 8$ by `Thm 7.21`) |
| 7 | Round-2 from-scratch re-derivation of `Thm 7.21`, 19-pair census (`Thm 7.11`), and $\Gamma_5$ non-arithmeticity (`Prop 7.18(b)`, $\tau(s_4 s_5) = 49/4 > 4$) | `GB` (`X`) | `code/xcheck/round2/`, `20/20` checks |
| all | Figures (8 vector PDFs) | `GB` | scripts in `code/figures/` |
| all | Six audit scripts: 31, 36, 23, 59, 47 checks, plus 32 for `[X]` cross-check (228/228) | `GB` | scripts in `code/` and `code/xcheck/`, reports in `audits/` |
| all | Citation verification (bibliographic data, DOIs via Crossref) & round-2 recommendation of Poitou (1976/77) | `GB` | `paper/references.bib` (55 baseline refs + `poitou77` = 56 references total) |
| all | Known / New / Refuted / Open separation | `GB` | Section 8 (updated for `v0.3.0`–`v0.3.1`) |
| — | Explanatory videos, music, and narration (not part of the paper) | `GB` | full production pipeline |

## Gemini 4 Neon (`G4N` / `E→G4N`), new results and cross-verification `[X]`

Working independently from the archived baselines under Ergentics' direction (`lean/` Lean 4.36.0 **33/33 theorems** without Mathlib and zero `sorry`, `swiftpp/` C++20 `g++`/`clang++` + Pure Swift 6.4 + Live Interop with `0.000e+00` delta, `rust/` Rust 1.100.0 with zero external crates including zero-PARI Manin $T_2$, `ergentics/` standalone PARI/GP & Python/SymPy verifiers, and checksummed calibration records in `data/`). Dossiers: [`NOVELTY_GEMINI4_NEON.md`](NOVELTY_GEMINI4_NEON.md), [`reconciliation/GEMINI4_NEON_RECONCILIATION.md`](reconciliation/GEMINI4_NEON_RECONCILIATION.md), [`reconciliation/GROKBOT_RECONCILIATION_RESPONSE.md`](reconciliation/GROKBOT_RECONCILIATION_RESPONSE.md), and [`reconciliation/THREE_WAY_CLEANROOM_AUDIT.md`](reconciliation/THREE_WAY_CLEANROOM_AUDIT.md). Accompanying educational videos and audio in `media/` are not part of the paper.

### New results, independent derivations, and corrections

| # | Paper label & tag | Gemini 4 Neon's part (`G4N` / `E→G4N`) | Cross-verification (`[X]`) | Outcome | Release | Date (PT) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Thm 6.2 (`thm:cumulants`) `[E→G4N; X]` | Driven by Ergentics' Rung-1 kurtosis calibration (`NEG-E3`): exact higher cumulants of homology class — universal 4th-cumulant isotropy $\kappa_4/\kappa_2^2 = -17/(2m)$, exact $C_6$ hexagonal anisotropy onset at order 6 $\kappa_6/\kappa_2^3 = (1470 + \cos 6\alpha)/(4m^2)$, $W$ rates $1/24, -17/1152, 1469/55296$. Lean 4 proofs; C++20/Swift/Rust checks at $m = 40$ ("Theorem C") | `code/xcheck/` (32/32): exact rational perturbation series along 6 functionals & $m=40$ exact distributions reproduce $m\kappa_{\mathrm{ex}} = -8.495174, -8.489783, -8.490889$ | agrees | `v0.2.0` | 2026-11-25 |
| 2 | Cor 4.5 (`cor:halving`) `[G4N; X]` | Tune injectivity whenever $\mathcal{C}$ is a transposition class, $8 \nmid N$, or $S$ is closed under halving ($2d \in S \Rightarrow d \in S$); in particular every consecutive $S = \{1, \dots, k\}$. Proved in Lean 4 ("Corollary B.1") | `code/xcheck/` brute force over all step sets for $N \le 24$ and maximal step sets for $N \le 72$: 0 collisions | agrees | `v0.2.0` | 2026-11-25 |
| 3 | after Thm 4.2 (`thm:tune`) `[G4N]` | Decoder count catch (`NEG-E8`): `v0.1.0` text quoted 131,136 rooted primes of length $\le 16$ (length-16 row only); exact cumulative total for lengths 6–16 is 174,864 | `code/xcheck/` recount from $\operatorname{tr} B^m$ with Möbius inversion confirms 174,864 | **corrected** | `v0.2.0` | 2026-11-25 |
| 4 | Remark 6.4 (`rem:edgeworth`) `[E→G4N; X]` | Correspondence Ladder `C-2 → C-2' → C-2''` at $m = 40$: TV $1.086\cdot 10^{-2} \to 9.951\cdot 10^{-4}$ (10.92×) $\to 1.443\cdot 10^{-4}$ (75.30×) on $\|w\| \le 24$; caught `NEG-E9` clipped-tail KL trap, resolved with bounded JSD | `code/xcheck/` reproduced TV and JSD to relative error $< 10^{-11}$ (`4.55e-14` TV / `3.60e-12` JSD) | agrees | `v0.2.0` | 2026-11-25 |
| 5 | Thm 4.4 (`thm:held`) `[E→GB; independently E→G4N & E; X]` | Independently derived from `v0.1.0` baseline: universal link-intersection bound $\|L_{h_1} \cap L_{h_2}\| \le 2$ ("Theorem A"); exact iff 1-moving-voice classification $N = 8m$, $\{0, m, 4m\}$, $2m \in S$ ("Theorem B"); minimal counterexample $N = 8, S = \{2\}, \{0, 1, 4\}$ (`NEG-M11`). Lean 4 proofs; Rust sweep over 10,576 chords ($N \le 72$) | Agrees identically with `GB` (`code/xcheck/`, 9 collisions $N=8,\dots,72$) and `[E]` (`cleanroom/`, 13,382 systems $N \le 18$) | agrees (3-way) | `v0.2.0` / `v0.3.0` | 2026-11-25 |
| 6 | Prop 6.3 (`prop:Wcgf`) `[GB; X]` | Independently verified Grok Bot's closed-form $W$-CGF series in exact rational arithmetic (`Fraction`) through $\kappa_8/m = -887099/7962624$ | Derived by Grok Bot from Thm 5.2 while re-checking #1 | agrees | `v0.2.0` | 2026-11-25 |
| 7 | Thm 7.11 (`thm:noshimura`) `[E→GB; corrected G4N; X]` (`NEG-E10`) | Caught cutoff erratum in `code/geometry/shimura_multi.py:17` ($\phi \le 168$) omitting genus-13 Shimura curve $X_0^{690}(1)$ ($\phi=176, e_2=0, e_3=8$; exact 19 pairs, not 18); proved $X_0^{690}(1)$ fails via zero-PARI Rust Manin $T_2$ (`M=345`, `dim=45`, `rank=45/45`) and standalone PARI `mfheckemat` (`dim S_2^{345-new}=15`) | Verified across 5 planes: Lean 4 witness, Swift++ exhaustive census, Rust Manin $T_2$ (all 18 levels / 19 pairs), PARI `ergentics/shimura_brandt_xcheck.py`, and `code/xcheck/round2/` | **corrected** (`18 → 19`; Thm 7.11 holds) | `v0.3.0` / `v0.3.1` | 2026-11-25 |
| 8 | Thm 7.21 (`thm:threepincer`) `[E→G4N; X]` | **Three-Pincer Hilbert Class Field Obstruction ("Theorem D"):** Unconditionally sharpens `Thm 7.20(b)` from $n \le 14$ down to **$n \le 8$** (0 survivors in $9 \le n \le 14$, tightest margin `+0.3392` at $n=9$; universal monotone tail $n \ge 15$ at $b=4.2$); forces $h_F = 1, u \in \{1, 2, 4\}$ at $n = 7, 8$; eliminates sextic $u \in \{16, 32\}$ via $L_v$ deg 48 at $b=6.00$ (margin `+0.013630`, cutting sextic ceiling `2.52×` to $2.648 \times 10^7$) | Algebraic core kernel-checked in Lean 4 (`Section7Obstructions.lean`); full 64-pt & 128-pt Gauss–Legendre Poitou–Odlyzko sweep verified identically across C++20, Pure Swift 6.4, Live Interop (`0.000e+00` delta), Rust (`section7_cycle5.rs`), `code/xcheck/round2/`, and `data/calibrations/theorem_d_pincer_swiftpp.json` | agrees (5-plane) | `v0.3.0` / `v0.3.1` | 2026-11-25 |

### Complete independent first-principles cross-verification (`[X]`, zero cached data reads — every numbered result has at least one independent check)

Each baseline and reconciled result below has at least one independent check across our multi-language formal and computational planes (the scope of each check is given in its row; see the two limits stated after the table) (no conclusion of Sections 2–7 overturned; two wording/cutoff errata `NEG-E8` and `NEG-E10` corrected). "Lean" denotes a kernel-checked Lean 4.36.0 proof with **33/33 theorems**, 0 `sorryAx`, 0 `ofReduceBool`, and zero Mathlib.

| Paper label (`v0.3.1`) | What was independently verified (`[X]`) | Planes |
| :--- | :--- | :--- |
| Prop 2.1 (`prop:cayley`) | involutions, bipartite, 3-regular, $P = L(LR)^4$, $R = L(LR)$, simply transitive $D_{12}$ | Lean, C++, Swift |
| Cor 2.2 (`cor:betti`) | $b_1 = 13$, 13 Schreier generators | Lean, C++, Swift |
| Thm 3.1 (`thm:spec`) | Ihara–Bass determinant, Dirac points, Ramanujan bound | C++, Swift |
| Thm 3.3 (`thm:count`) | $\pi(40) = 54{,}975{,}717{,}792$ by transfer matrix and Möbius inversion | C++, Swift, Rust |
| Thm 3.4 (`thm:arith`) | exact $\mathbb{Z}[\zeta_{12}]$ arithmetic and $M_7$ $[0,1,4]$ flip-graph isomorphism | Rust |
| Thm 3.5 (`thm:weil`) | $P_{44}$ Newton point counts `[3, 39, 9, 75, 33, 27]` | C++, Swift |
| Prop 3.7 (`prop:noideal`) | mod-3/mod-4 obstructions, multiplier conductor 12 for all 12 maps | Lean, C++, Swift |
| Thm 3.8 (`thm:order2`) | $\psi: \mathbb{Z}[\sqrt{-3}] \to \mathbb{Z}_{12}$ with principal ideal kernel $(3 - \sqrt{-3})$ | Lean |
| Lemma 4.1, Thm 4.2 (`lem:l`, `thm:tune`) | L1–L3, backtracking counterexample (`NEG-M4`); all 174,864 rooted primes decode (`NEG-E8`) | Lean, C++, Swift, Rust |
| Thm 4.3 (`thm:tunegen`) | 6,028 systems ($N \le 72$), extended to 11,452 ($N \le 96$) | Rust |
| Thm 4.4, Cor 4.5 (`thm:held`, `cor:halving`) | 3-way derivation (`GB`, `G4N`, `E`); Lean 4 proofs; Rust 10,576 chords ($N \le 72$); Clean-Room 13,382 systems ($N \le 18$) | Lean, C++, Swift, Rust, Python (`GB` & `E`) |
| Thm 5.1 (`thm:W`) | $12 \mid \text{voice sum}$ for every closed walk of any length | Lean, C++, Swift |
| Thms 5.2, 5.3 (`thm:twist`, `thm:window`) | Hermiticity, window edge 2.8909, cyclic covers, 12/31/53-EDO thresholds | C++, Swift |
| Thms 6.1–6.2, Prop 6.3, Rem 6.4 | Gram det 108; exact 4th/6th cumulants; closed-form $W$-CGF through $\kappa_8$; Edgeworth TV/JSD at $m=40$ | Lean, C++, Swift, Rust, Python (`GB`) |
| Thm 7.1 (`thm:schottky`) | $\sigma_s^2 = 2I$ (Lean); 13 hyperbolic generators; Bruhat–Tits ball $r \le 7$ (`382/382`) | Lean, C++, Swift |
| Prop 7.2 (`prop:aut`) | $\|\operatorname{Aut} X\| = 24$, 13 involutions, no tree quotient | C++, Swift |
| Prop 7.3 (`prop:nonarith`) | Hamilton quaternion compact trace bound $0 \le \tau \le 4$ & universal $\gamma_0^k$ non-compactness | Lean (`Section7Obstructions.lean`) |
| Thm 7.4, Cor 7.5 (`thm:tower`, `cor:artin`) | $\mathbb{Z}/12$ voltage cover, lifts `(6, 8, 24)`, $\mathbb{Z}[\zeta_{12}][u]$ Artin–Ihara factorisation | Rust |
| Thm 7.7 (`thm:sandpile`) | $\mathbb{Z}/2 \oplus \mathbb{Z}/2 \oplus \mathbb{Z}/8 \oplus \mathbb{Z}/736 \oplus \mathbb{Z}/6624$ (exact Bareiss + modular SNF) | C++, Swift |
| Thm 7.8 (`thm:gon`) | gonality 6 (exhaustive Dhar burning over 20,475 divisors + degree-6 witness) | C++, Swift |
| Props 7.9, 7.10 (`prop:f2`, `prop:g5`) | degree-4 obstruction (`-1`); projective point counts of genus-5 curves $A, B$ over $\mathbb{F}_{2^k}$, $k \le 5$ | C++, Swift |
| Thm 7.11 (`thm:noshimura`) | Exhaustive 19 genus-13 pairs (catching `NEG-E10` $X_0^{690}(1)$) + 4 $\Gamma_H$; zero-PARI Manin $T_2$ full rank on all 18 levels + PARI `mfheckemat` | Lean, C++, Swift, Rust (Manin $T_2$), PARI (`ergentics/`), `code/xcheck/round2/` |
| Thm 7.13 (`thm:trace`) | $\operatorname{tr}(\gamma_0^k)^2 > 4\det(\gamma_0^k)$ for all $k \ge 1$ | Lean, C++, Swift |
| Lemma 7.14 (`lem:length`) | Abstract valuation slope-2 doubling, slope-1 control, odd-prime $\ell$ scaling; wild involution $\sigma(z)=3/z$ & $u(1+x)-4 = x(x-2)/(1+x)$ (`NEG-M12`) | Lean, C++, Swift (`RCT-2`), Python/SymPy (`ergentics/open1_torsion_xcheck.py`) |
| Thm 7.15 (`thm:q2`) | $e_v = 1, q = 2$ valence forcing $\Gamma_x = 1$ & reduction to Thm 7.13 | Lean (`Section7Obstructions.lean`) |
| Prop 7.17 (`prop:torsion`) | $q = 4, 8$ valence & 504-element $PGL_2(\mathbb{F}_8)$ census (`56/56` free order-3); ramified $e_v=2, f_v=1$ elimination of $(0,1)$ + combinatorially sharp $M(\mathcal{O}) = 36$ witness (`NEG-M13`) | Lean, C++, Swift, Rust, Python (`ergentics/open1_torsion_xcheck.py`) |
| Prop 7.18 (`prop:cyclotomic`) | Unramified cyclotomic obstruction $\mathbb{Q}(\zeta_{2^{f_v}+1})^+ \subset E$ (even $f_v \ge 2$) & exact $\mathbb{Z}_2[\omega]$ Klein ping-pong + $\tau(s_4 s_5) = 49/4 > 4$ non-arithmeticity of $\Gamma_5 \subset PGL_2(\mathbb{Q}_4)$ (`NEG-M14`) | Python (`ergentics/open1_torsion_xcheck.py`), `code/xcheck/round2/`, `[E]` clean-room monograph |
| Prop 7.19 (`prop:mass`) | Exact Siegel + $h^+(D)$ quadratic scan (118 fields); exhaustive `nflist` 177 cubics & 476 quartics; **3-way 8/8 exact Brandt characteristic polynomial match** (`GB` ↔ `E` pure-Python ↔ `G4N` PARI) | C++, Swift, Rust, PARI (`ergentics/shimura_brandt_xcheck.py`), Pure Python (`cleanroom/`) |
| Thm 7.20 (`thm:anyh`) | Mass equation, Poitou–Odlyzko $n \ge 15$ bound, and quintic near-miss $d_F = 106069$ exact 12×12 Brandt charpoly | C++, Swift, Rust, PARI (`ergentics/shimura_brandt_xcheck.py`) |
| Thm 7.21 (`thm:threepincer`) | Three-pincer Hilbert class field obstruction ($n \le 8$, $h_F = 1, u \le 4$ at $n=7,8$, sextic $u \in \{16,32\}$ killed via $L_v$ deg 48 at $b=6.00$) | Lean, C++, Swift (`0.000e+00` delta), Rust, `code/xcheck/round2/`, `data/` |

**Unchecked items remaining across Sections 2–7:** **0** in the sense that every numbered result has at least one independent computational check (all 7 formerly unchecked Section 7 items of `v0.2.0` are covered by Lean 4, Swift++, Rust, `ergentics/`, or `code/xcheck/round2/`). Two limits: the Lean files formalise the arithmetic or combinatorial cores, not the full statements; and for Thm 7.20(c) the 55 narrow-class configurations in degree $\le 4$ and the quintic and sextic scans were spot-checked through the near miss $d_F = 106069$, not re-run.

**Round-2 referee review (`v0.3.1`):** `code/xcheck/round2/round2_xcheck.py` (`20/20`, from scratch) re-derives the 19-pair census of Thm 7.11, the three-pincer sweep of Thm 7.21 (survivors exactly the open cases stated in the paper) and the non-arithmeticity of $\Gamma_5$ in Prop 7.18(b) ($\tau(s_4 s_5) = 49/4 > 4$, also confirmed in `ergentics/open1_torsion_xcheck.py`). Tag changes: Thm 7.11 `[E→GB; corrected G4N; X]` (the `NEG-E10` correction came from `G4N`); Lemma 7.14 `[E→GB; sharpened E; X]`. Poitou (1976/77) (`poitou77`, verified on Numdam) added as reference `[40]` (`55 → 56` references).

### Engineering notes acted on across `v0.2.0`–`v0.3.1`

- `NEG-E2` (global random seed shared across checks in `code/open_q/open_audit.py`): fixed in `v0.2.0` with a keyed random stream per check (`random.Random(k)`) in `code/open_q/open_audit.py` and `audit_round3.py`; audit passes `47/47`.
- `NEG-E1` (older `code/` audit scripts partly assert over stored JSON outputs): noted; `code/xcheck/` (`32/32`), `code/xcheck/round2/` (`20/20`), and all `lean/` / `swiftpp/` / `rust/` / `ergentics/` suites recompute everything from scratch with zero reads of cached data.
- `NEG-E10` (`code/geometry/shimura_multi.py:17` cutoff $\phi \le 168$ omitting $X_0^{690}(1)$): archived upstream `code/` preserved untouched per Rule 5; manuscript `Thm 7.11` corrected (`18 → 19` pairs) and verified in `v0.3.0`–`v0.3.1`.
- `NEG-E11` (GitHub Immutable Releases blocks post-publish asset uploads with `HTTP 422`): resolved via `.github/workflows/release-assets.yml` (`push: tags: ['v*']`), atomically creating + uploading `prime-cadences.pdf`, `prime-cadences-arxiv.tar.gz`, and `SHA256SUMS.txt` + publishing `v0.3.1` in a single `gh release create --verify-tag` call.
- `Makefile` `arxiv` target updated in `v0.3.0` with `--owner=0 --group=0 --numeric-owner` so every rebuilt arXiv bundle carries strictly neutral `0/0` ownership headers.

---

## Paper `PC-II`: *Uniform Triadic Wreath Products, the Nauru Graph, and Dual-Prime $D = 6$ Arithmeticity* (`papers/triadic_wreath_nauru/`)

- **Ergentics (`[E]`):** Initiated the Lewin $T/I$ vs. $PLR$ vs. Hook UTT wreath-product fusion question, directed the $2$-adic arithmetic extension into formal publication under the Morpheus ADPIE, Code-vs-Data, and multi-plane verification standard, and contributed Ergentics Monograph IV Act XXIV establishing the Eisenstein–Nauru $\{6,3\}_{(2,2)}$ recovery, intrinsic compact $\mathrm{SU}(2)$ Wilson-loop holonomy, and complete $3$-adic Hurwitz $B_2$ ($D = 6, p = 3$) resolution of $\mathrm{Dic}_6$.
- **Gemini 4 Neon (`[E→G4N; X]`):** Derived and proved the parity obstruction (`NEG-M16`) and non-isomorphism of $\langle T/I, PLR\rangle$ vs. $\mathrm{UTT}$ (`NEG-M15`), executed the exhaustive 24-subgroup simply transitive UTT census (8 classes, $PLR$ uniqueness, Nauru $Y=\mathrm{GP}(12,5)$ emergence), proved the $5/5$ $\mathbb{F}_2$ elliptic Weil splitting, exact $5$-smooth Raynaud SNF ($|K(Y)|=162{,}000{,}000$), prime-hexagon divisorial gonality $\operatorname{gon}(Y)=6$, universal Fricke–Vogt law $B(x)=(-3,x(x-3))_{\mathbb{Q}(x)}$, exact rational arithmetic classification $x\in\{\frac12,\frac32,\frac52\}$ (`NEG-M17`), explicit Shimura tower analysis alongside `0/19` Borel-level Manin $T_2$ exclusion (`NEG-M18`), and the order-`1,152` twin-diamond bifurcation (`NEG-M19`). In `v0.6.0`, independently verified and formally proved Monograph IV Pillars I–III across all three zero-shared-data planes (reconciling two minor editorial errata: correcting the printed Hurwitz relator factor `t_y b` → `b t_y` in Theorem 7.2, and assigning `NEG-M20`–`NEG-M21` to preserve `NEG-M19`). In `v0.6.1`, took lead on repo-wide continuous testing and content-integrity hardening (`NEG-M22`): caught and corrected `PC-II` Eq. (7.4)'s Hurwitz normalizer inclusion direction, proved constructive normality ($q_{x^4} \in H_8$ across `32/32`), mod-$16$ stabilization (`|H_16|=64`), and mod-$5$ $A_5$ surjection (`|H_5|=60`), upgraded Lean 4 to `33/33` theorems (`0 sorryAx`, `0 ofReduceBool`, direct `nauruAdj` traces in `thm9` + $\mathbb{F}_3$ quaternion & normalizer tower `thm33`), standardized all `11/11` `MANIFEST.sha256` files, reconciled `PROVENANCE.md`, and built the permanent zero-dependency `10`-gate audit harness (`tests/content_integrity_audit.py`) and 4-job GitHub Actions workflow (`.github/workflows/continuous-testing.yml`). In `v0.7.0`, closed every remaining open loose end of `PC-II`: discovered and proved across all primes that $x = \frac{5}{2}$ in $B_5$ ($D=10$) is a **genuine congruence Shimura curve** $\Gamma_Y(\frac{5}{2}) = \Gamma(3)\cap\Gamma(\mathfrak{P}_5) = \Gamma(3\mathfrak{P}_5)$ ($\mathfrak{P}_5\mid 5\mid 10$) while $x = \frac{1}{2}$ in $B_5$ is a strictly **non-congruence $V_4$-cover** of $K_{3,3}$ (`NEG-M23`), determined the exact tropical invariants of the $\mathrm{Dic}_6$ twin $Z$ (SNF $K(Z)\cong \mathbb{Z}/4\oplus(\mathbb{Z}/52)^2\oplus\mathbb{Z}/1820\oplus\mathbb{Z}/21840$, `43` involutions $\beta_1\in\{7^2,11^{24},13^{17}\}$, exhaustive `157,166`-divisor Dhar proof of $\operatorname{gon}(Z) = 8$ attained by `4` canonical two-coset witnesses), certified both `23×23` unimodular SNF decompositions directly in pure-kernel Lean 4 (`37/37` theorems, `SnfCertificates.lean` `thm34`–`thm35`, plus `thm36`–`thm37`, `0 sorryAx`, `0 ofReduceBool`), upgraded Pure Rust (`11/11` tests, `10/10` core suites) and Pure Python (`15/15` gates, `schema_version 1.2.0`), and expanded GitHub Actions Python CI coverage to `71/71` gates via isolated Horizon Synthesis `18/18` JSON parity checks.
- **Grok Bot (`[GB]` — Round-1 Independent Audit, 2026-11-27):** Independently verified `NEG-M15`, `NEG-M16`, the $I_0$ normalizer formula, $\mathrm{UTT}\rtimes\langle I_0\rangle$ (`576`), $N(T)$ (`1,152`), the 24-subgroup census, $PLR$ uniqueness, the Nauru graph $\mathrm{GP}(12,5)$, and spanning-tree counts; caught the `v0.5.0` Table 1 transcription typo on $\langle T, PLR\rangle$ (`6/24` vs. `12/12`), supplied the Crans–Fiore–Satyendra mutual-centralizer explanation for order `288` & refined Section 2 heading, identified the distinct order-`1,152` Hook quasi-uniform group $Q\mathrm{UTT}\cong D_{12}\wr\mathbb{Z}_2$ (`NEG-M19`), and refined the integral-Weil and Bruhat–Tits scope framing (Remark 4.2). (Gonality, Shimura covers, Manin $T_2$/$T_3$, Monograph IV pillars, `v0.6.1`–`v0.7.0` audit additions, and Lean/Rust builds have not been independently re-run by `[GB]`.)
