# Contributions and provenance

**Author:** Ergentics (sole author).  
**AI assistance:** Grok Bot, an AI assistant working with Ergentics. Following standard AI-disclosure practice, Grok Bot is credited here and in the paper's "Contributions and provenance" section, not as an author. Responsibility for the content rests with the author.

These records cover the work up to 25 November 2026, including the reconciliation with Ergentics' own program (Morpheus repository, code commit `60c786d`, data commit `e911bec`, packet commit `8aaecd3`). They were reconstructed from the working record and are subject to the author's review.

## Marker scheme (used on every numbered result in the paper)

| Tag | Meaning |
|---|---|
| `[GB]` | Statement, proof and computation by Grok Bot |
| `[E]` | By Ergentics |
| `[E→GB]` | Question or direction set by Ergentics; statement, proof and computation by Grok Bot |
| `[lit.]` | Result from the cited literature, re-checked by Grok Bot |
| `[X]` | Contributed, cross-verified or changed in Ergentics' own program, a separate forum and toolchain (Lean 4, C++20, Swift, Rust; AI assistant Gemini 4 Neon, under Ergentics' direction); see the table below |
| `[independently X]` | Found independently in Ergentics' own program as well |

## Ergentics

- Research direction and all prompts that steered the work.
- The starting point: the Tonnetz and the graph Riemann hypothesis.
- The phasor (Fourier) prompt behind the spectral and arithmetic readings (Thm 3.1, Thm 3.4).
- The melodic-primes question and the redirect "Where does the melody fit?" (Section 4: Lemma 4.1, Thm 4.2, Thm 4.3).
- The push towards Eisenstein integers (Prop 3.7, Thm 3.8).
- "The geometric object deserves its own focus" (Section 7).
- "Can't you attempt to derive them or find alternatives?" (direct computation of the Brandt graphs, Prop 7.18).
- "I'll wait for you to have a more fuller view" (round 3 of the open questions: held-note theorem, Thm 4.4; torsion structure, Prop 7.17; any narrow class number and the degree bound, Thm 7.19; the LMFDB cross-check folded into Prop 7.18).
- "Chase down those open questions" (Section 4.1 / Thm 4.3, Sections 7.6–7.7, Prop 7.10).
- Review of the drafts and of the videos.
- Ergentics' own verification program (`[X]`, below), which produced Thm 6.2, Cor 4.5, Remark 6.4, an independent derivation of Thm 4.4, and the decoder-count correction after Thm 4.2.

## Grok Bot, by section

Theorem numbers follow the repository (amsart) version of the paper.

| Section | Result | Tag | Grok Bot's part |
|---|---|---|---|
| 2 | Prop 2.1 (dihedral PLR group) | lit. | re-checked by enumeration |
| 2 | Cor 2.2 (Coxeter description, free group of rank 13) | GB | statement and proof |
| 3 | Thm 3.1 spectrum = honeycomb bands = Fourier moduli; Ramanujan | E→GB | proof and 50-digit check |
| 3 | Thm 3.3 exact prime-cadence counts (to m = 40) | GB | transfer matrix, Möbius inversion |
| 3 | Thm 3.4 arithmetic of the coefficients (Gaussian/Eisenstein primes, units) | E→GB | proof and exact algebra |
| 3 | Thm 3.5 ζ_X over Q as Weil polynomials over F₂; explicit curves | GB | factorisation, point counts, LMFDB look-ups |
| 3 | Prop 3.7 Tonnetz is not Z[ω]/I, Z[i]/I or Z[ζ]/I | E→GB | refutation |
| 3 | Thm 3.8 order of conductor 2 presentation | E→GB | proof |
| 4 | Lemma 4.1, Thm 4.2 tune theorem | E→GB | proof; decoder tested on all 174,864 rooted primes of length ≤ 16 (count corrected, see [X] #3) |
| 4 | Thm 4.3 general reduction; held-note criterion | E→GB | proof; 6,028 systems verified (N ≤ 72) |
| 4 | Thm 4.4 held-note theorem: proof for every N and step set; the exceptional family (8 ∣ N, class {0, N/8, N/2}, N/4 ∈ S), smallest N = 8, S = {2} | E→GB; independently X | proof (link graphs have no 4-cycles); brute-force checks for N ≤ 26 and all walks of length ≤ 8 for N ≤ 16 |
| 5 | Thm 5.1 W = −u; Thm 5.2 twisted spectrum; Thm 5.3 Riemann window | GB / GB / E→GB | proofs and checks |
| 6 | Thm 6.1 winding law (variance m/24, isotropic covariance) | GB | proof and numerics |
| 6 | Prop 6.3 all cumulants of W in closed form (κ₈/m = −887099/7962624) | GB | derivation from Thm 5.2; exact series check |
| 6 | Cross-check of every [X] claim (Thm 6.2, Cor 4.5, Remark 6.4, Thm 4.4 as found in [X], NEG-E8) | GB | `code/xcheck/`, 32/32 checks, recomputed from scratch |
| 7 | Thm 7.1 Schottky group from P, L, R; genus-13 curve C | GB | construction, proof, verification |
| 7 | Prop 7.2 Aut C = T/I; Prop 7.3 not arithmetic over Q | E→GB | proofs |
| 7 | Thm 7.4 Z/12 tower; Cor 7.5 Ihara factors as characters | E→GB | proofs, exact checks |
| 7 | Thm 7.7 sandpile group; Thm 7.8 gonality 6 | E→GB | Smith normal form; two independent searches |
| 7 | Prop 7.9 curves over F₂; Prop 7.10 octic in genus 5 (minimal) | E→GB | searches, census cross-check, Gröbner smoothness |
| 7 | Thm 7.11 no Shimura curve over Q | E→GB | Hecke computations (PARI) |
| 7 | Thm 7.13 trace obstruction; Lemma 7.14 edge lengths; Thm 7.15 F_v = Q₂ | E→GB | proofs and numerical controls |
| 7 | Prop 7.17 uniformisations with torsion at a place above 2: structure when e_v = 1, f_v = 2, f_v ≥ 3, e_v = 2 | E→GB | proof (Bass–Serre, valence count, edge lengths); the remaining gap stated |
| 7 | Prop 7.18 graph-level search: mass formula plus direct Brandt-graph computation for all 22 configurations | E→GB | field enumeration (PARI); quaternion ideal-class enumeration by v-neighbours; second method by theta counts; validated against LMFDB and PARI modular forms |
| 7 | Thm 7.19 any narrow class number: mass equation, Odlyzko degree bound (n ≤ 14), computations in degrees ≤ 5 and in part of degree 6 | E→GB | field scans (PARI, LMFDB lists), generalised Brandt computation with mass, theta and component checks for 55 + 4 configurations; Odlyzko Table 4 |
| all | Figures (8 vector PDFs) | GB | scripts in `code/figures/` |
| all | Independent audits: 31, 36, 23, 59, 47 checks, plus 32 for the [X] cross-check | GB | scripts in `code/` and `code/xcheck/`, reports in `audits/` |
| all | Citation verification (bibliographic data, DOIs via Crossref) | GB | `paper/references.bib` |
| all | Known / New / Refuted / Open separation | GB | Section 8 |
| — | Explanatory videos, music and narration (not part of the paper or this repository) | GB | full production pipeline |

(The table uses the theorem numbers of the compiled PDF; if numbering shifts, the labels in the LaTeX source are authoritative.)

## Cross-verification in Ergentics' own program `[X]`

Ergentics works in a separate program (a different forum and toolchain: Lean 4 without Mathlib, and independent verifiers in C++20, Swift and Rust, written with the AI assistant Gemini 4 Neon under Ergentics' direction). It worked from the baseline `v0.1.0` of the paper (the version before round 3). Its packet is `reconciliation/GEMINI4_NEON_RECONCILIATION.md` in the Morpheus repository, and its new results are in `NOVELTY_GEMINI4_NEON.md`. Grok Bot re-checked every new claim independently (`code/xcheck/`, 32/32 checks), and no conclusion of the paper changed.

Paper labels refer to this version (v0.2.0). Baseline numbers used in the packet differ for some Section 7 results: baseline Prop 7.17 (mass search) is Prop 7.18 here.

### New results and corrections from Ergentics' program

| # | Paper label | Contribution in Ergentics' program | Grok Bot's re-check | Outcome | Change to the paper | Date (PT) |
|---|---|---|---|---|---|---|
| 1 | Thm 6.2 (`thm:cumulants`) [X] | Exact higher cumulants of the homology class: κ₄/κ₂² = −17/(2m) along every axis (isotropy), κ₆/κ₂³ = (1470 + cos 6α)/(4m²) (hexagonal anisotropy first at order 6); W rates 1/24, −17/1152, 1469/55296. Lean 4 proofs of the power sums and series; C++/Swift/Rust checks at m = 40 ("Theorem C") | Exact rational perturbation series from an independently built twisted adjacency matrix, along 6 functionals; exact m = 40 distributions (54,975,717,792 primes) reproduce m·κ_ex = −8.495174, −8.489783, −8.490889 | agrees | New Section 6.1 with Thm 6.2, proof sketch and verification paragraph; abstract updated | 2026-11-25 |
| 2 | Cor 4.5 (`cor:halving`) [X] | Tune injectivity whenever the class is a transposition class, 8 ∤ N, or S is closed under halving; in particular for every S = {1, …, k} ("Corollary B.1") | Brute force over all step sets for N ≤ 24 and maximal step sets for N ≤ 72: no collision for halving-closed S | agrees; follows in one line from Thm 4.4(b) | New Cor 4.5 with proof | 2026-11-25 |
| 3 | after Thm 4.2 (`thm:tune`) [X] | Decoder count: the text said 131,136 rooted primes of length ≤ 16, which is only the length-16 row; the total for lengths 6–16 is 174,864 ("NEG-E8") | Recount from tr Bᵐ with Möbius inversion: 192 + 624 + 2,400 + 6,912 + 33,600 + 131,136 = 174,864; the decoder test (`code/deep/tune.py`) had in fact covered all of them | **corrected** (wording only; the test was complete) | Sentence corrected | 2026-11-25 |
| 4 | Remark 6.4 (`rem:edgeworth`) [X] | Edgeworth ladder at m = 40: TV 1.086·10⁻² (Gaussian) → 9.951·10⁻⁴ (4th order) → 1.443·10⁻⁴ (6th order); truncated densities go negative at w = ±5, so the comparison uses JSD, not KL ("C-2′/C-2″", "NEG-E9") | Reproduced TV and JSD to relative error < 10⁻¹¹ with the same convention (approximants normalised over \|w\| ≤ 24) | agrees; values depend on the normalisation convention, which the remark states | New Remark 6.4 | 2026-11-25 |
| 5 | Thm 4.4 (`thm:held`) [independently X] | Same classification found independently from the baseline: common-link-edge bound ≤ 2 ("Theorem A"); one-voice collisions iff N = 8m, class {0, m, 4m}, 2m ∈ S ("Theorem B"); minimal case N = 8, S = {2}, chord {0, 1, 4}, tune (3, 5, 7, 1) ("NEG-M11"). Lean 4 proofs; sweep over 10,576 chord classes, N ≤ 72 | Link bound (max 2, all classes N ≤ 30); 9 collisions at N = 8, 16, …, 72 and no others; N = 8 walks verified | agrees with Thm 4.4 (found here in round 3, and independently in Ergentics' program from the baseline, which did not contain it) | Tag and an "Independent confirmation" paragraph | 2026-11-25 |
| 6 | Prop 6.3 (`prop:Wcgf`) [GB] | — | Found while re-checking #1: the W-twisted top eigenvalue is \|2 + e^{iφ/4}\| in closed form, so log E e^{iφW} ≈ m log(ρ(φ)/2) gives every cumulant of W | new, Grok Bot | New Prop 6.3 | 2026-11-25 |

### Independent re-verification in Ergentics' program (no change to the paper)

All agree with the paper. "Lean" means a kernel-checked Lean 4 proof of the statement or its key step (0 `sorry`, no Mathlib).

| Paper label | What was re-verified | Planes |
|---|---|---|
| Prop 2.1 (`prop:cayley`) | involutions, bipartite, 3-regular, P = L(LR)⁴, R = L(LR), simply transitive D₁₂ | Lean, C++, Swift |
| Cor 2.2 (`cor:betti`) | b₁ = 13, 13 Schreier generators | Lean, C++, Swift |
| Thm 3.1 (`thm:spec`) | Ihara–Bass determinant, Dirac points, Ramanujan bound | C++, Swift |
| Thm 3.3 (`thm:count`) | π(40) = 54,975,717,792 by transfer matrix and Möbius inversion | C++, Swift, Rust |
| Thm 3.4 (`thm:arith`) | exact Z[ζ₁₂] arithmetic | Rust |
| Thm 3.5 (`thm:weil`) | P₄₄ point counts [3, 39, 9, 75, 33, 27] | C++, Swift |
| Prop 3.7 (`prop:noideal`) | mod-3/mod-4 obstructions, conductor 12 for all 12 maps | Lean, C++, Swift |
| Thm 3.8 (`thm:order2`) | ψ: Z[√−3] → Z₁₂ with kernel (3 − √−3) | Lean |
| Lemma 4.1, Thm 4.2 (`lem:l`, `thm:tune`) | L1–L3, the backtracking counterexample; all 174,864 rooted primes decode | Lean, C++, Swift, Rust |
| Thm 4.3 (`thm:tunegen`) | 6,028 systems (N ≤ 72), extended to 11,452 (N ≤ 96) | Rust |
| Thm 5.1 (`thm:W`) | 12 ∣ voice sum for every closed walk | Lean, C++, Swift |
| Thms 5.2, 5.3 (`thm:twist`, `thm:window`) | Hermiticity, window edge 2.8909, cyclic covers, 12/31/53-EDO thresholds | C++, Swift |
| Thm 6.1 (`thm:clt`) | Gram determinant 108; Gaussian calibration at m = 40 | Lean, C++, Swift, Rust |
| Thm 7.1 (`thm:schottky`) | σ² = 2I (Lean); 13 hyperbolic generators; Bruhat–Tits ball | Lean, C++, Swift |
| Prop 7.2 (`prop:aut`) | \|Aut X\| = 24, 13 involutions, no tree quotient | C++, Swift |
| Thm 7.4, Cor 7.5 (`thm:tower`, `cor:artin`) | voltage cover, lifts (6, 8, 24), Artin–Ihara factorisation | Rust |
| Thm 7.7 (`thm:sandpile`) | Z/2 ⊕ Z/2 ⊕ Z/8 ⊕ Z/736 ⊕ Z/6624 (exact Bareiss + modular SNF) | C++, Swift |
| Thm 7.8 (`thm:gon`) | gonality 6 (Dhar burning over 20,475 divisors) | C++, Swift |
| Props 7.9, 7.10 (`prop:f2`, `prop:g5`) | degree-4 obstruction; point counts of the genus-5 curves A, B over F₂ᵏ, k ≤ 5 | C++, Swift |
| Thm 7.13 (`thm:trace`) | tr(γ₀ᵏ)² > 4 det(γ₀ᵏ) for all k ≥ 1 | Lean, C++, Swift |

Not yet re-derived in Ergentics' program: Prop 7.3, Thm 7.11, Lemma 7.14, Thm 7.15, Prop 7.18, and the results added in round 3 after the baseline (Prop 7.17, Thm 7.19).

### Engineering notes from Ergentics' program, acted on here

- "NEG-E2" (a global random seed shared across checks in `code/open_q/open_audit.py`): fixed with a keyed random stream per check (`random.Random(k)`) there and in `audit_round3.py`; the audit still passes 47/47.
- "NEG-E1" (the baseline audit scripts partly assert over stored JSON outputs): noted. The new `code/xcheck/` audit recomputes everything and reads no stored data. The older audits are unchanged.
