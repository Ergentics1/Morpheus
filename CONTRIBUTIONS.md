# Contributions and provenance

**Author:** Ergentics (sole author).  
**AI assistance:** Grok Bot, an AI assistant working with Ergentics. Following standard AI-disclosure practice, Grok Bot is credited here and in the paper's "Contributions and provenance" section, not as an author. Responsibility for the content rests with the author.

These records cover the work up to 25 November 2026. They were reconstructed from the working conversation and are subject to the author's review.

## Marker scheme (used on every numbered result in the paper)

| Tag | Meaning |
|---|---|
| `[GB]` | Statement, proof and computation by Grok Bot |
| `[E]` | By Ergentics |
| `[E→GB]` | Question or direction set by Ergentics; statement, proof and computation by Grok Bot |
| `[lit.]` | Result from the cited literature, re-checked by Grok Bot |
| `[X]` | Cross-verified, or changed, in Ergentics' own program, a separate forum and tool (none yet; see the table below) |

## Ergentics

- Research direction and all prompts that steered the work.
- The starting point: the Tonnetz and the graph Riemann hypothesis.
- The phasor (Fourier) prompt behind the spectral and arithmetic readings (Thm 3.1, Thm 3.4).
- The melodic-primes question and the redirect "Where does the melody fit?" (Section 4: Lemma 4.1, Thm 4.2, Thm 4.3).
- The push towards Eisenstein integers (Prop 3.7, Thm 3.8).
- "The geometric object deserves its own focus" (Section 7).
- "Chase down those open questions" (Section 4.1 / Thm 4.3, Sections 7.6–7.7, Prop 7.10).
- Review of the drafts and of the videos.

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
| 4 | Lemma 4.1, Thm 4.2 tune theorem | E→GB | proof; decoder tested on 131,136 rooted primes |
| 4 | Thm 4.3 general reduction; held-note criterion | E→GB | proof; 6,028 systems verified (N ≤ 72) |
| 5 | Thm 5.1 W = −u; Thm 5.2 twisted spectrum; Thm 5.3 Riemann window | GB / GB / E→GB | proofs and checks |
| 6 | Thm 6.1 winding law (variance m/24, isotropic covariance) | GB | proof and numerics |
| 7 | Thm 7.1 Schottky group from P, L, R; genus-13 curve C | GB | construction, proof, verification |
| 7 | Prop 7.2 Aut C = T/I; Prop 7.3 not arithmetic over Q | E→GB | proofs |
| 7 | Thm 7.4 Z/12 tower; Cor 7.5 Ihara factors as characters | E→GB | proofs, exact checks |
| 7 | Thm 7.7 sandpile group; Thm 7.8 gonality 6 | E→GB | Smith normal form; two independent searches |
| 7 | Prop 7.9 curves over F₂; Prop 7.10 octic in genus 5 (minimal) | E→GB | searches, census cross-check, Gröbner smoothness |
| 7 | Thm 7.11 no Shimura curve over Q | E→GB | Hecke computations (PARI) |
| 7 | Thm 7.13 trace obstruction; Lemma 7.14 edge lengths; Thm 7.15 F_v = Q₂ | E→GB | proofs and numerical controls |
| 7 | Prop 7.17 graph-level mass-formula search | E→GB | field enumeration (PARI), LMFDB spectral tests |
| all | Figures (8 vector PDFs) | GB | scripts in `code/figures/` |
| all | Independent audits: 31, 36, 23, 59, 27 checks | GB | scripts in `code/`, reports in `audits/` |
| all | Citation verification (bibliographic data, DOIs via Crossref) | GB | `paper/references.bib` |
| all | Known / New / Refuted / Open separation | GB | Section 8 |
| — | Explanatory videos, music and narration (not part of the paper or this repository) | GB | full production pipeline |

(The table uses the theorem numbers of the compiled PDF; if numbering shifts, the labels in the LaTeX source are authoritative.)

## Cross-verification in Ergentics' own program `[X]`

Ergentics works in a separate program (a different forum and tool). Results that it reproduces, reconciles or changes are recorded here, and the matching results in the paper get the `[X]` tag.

| # | Result (paper label) | What was checked or changed in Ergentics' program | Outcome (agrees / differs / changed) | Reconciliation and resulting change to the paper | Date |
|---|---|---|---|---|---|
| 1 | — | — | — | — | — |

No entries yet.
