# Changelog

All notable changes to **Morpheus** are documented here. Manuscript updates cut a new versioned GitHub release (`vX.Y.Z`); Code Model and Data Model verification advances are tracked under `[Unreleased]` until the next paper release.

## [Unreleased]

*(Future ADPIE Cycle 5 verification and manuscript work will be tracked here until the next versioned release.)*

## [0.2.0] - 2026-11-25

### Added
- **Manuscript round 3 (`GB` / `E→GB`, folded into `paper/`):** Held-note theorem (`Thm 4.4`) for every $N$ and step set, uniformisations with torsion at a place above 2 (`Prop 7.17`), direct Brandt-graph computations (`Prop 7.18`), any narrow class number with the Odlyzko degree bound (`Thm 7.19`), and `Prop 6.3` (`[GB; X]`) closed-form cumulant generating function of $W$ ($\kappa_8/m = -887099/7962624$, independently confirmed in exact rational arithmetic by Gemini 4 Neon); new scripts in `code/open_q/` (`brandt/`, `general/`, `odl/`, `tune_proof/`, `audit_round3.py`; open-questions audit `27 → 47` checks).
- **ADPIE Cycle 1 — Swift++ Triple-Check Toolkit (`swiftpp/`, MIT):**
  - **Lane 1 (`ErgenticsCXX` + `CXXStandaloneTests`):** Standalone Pure C++20 core compiled with `-O2 -Wall -Wextra -Werror` under both `g++ 13.3.0` and `clang++ 18.1.3` (30/30 assertions PASS).
  - **Lane 2 (`ErgenticsSwift`):** Independent Pure Swift 6.4 implementation with zero C++ imports.
  - **Lane 3 (`ErgenticsInterop` + `ErgenticsCLI` + 4 SWE-Sweep XCTest suites):** Live Swift 6.4 ↔ C++20 interop cross-checking every turn (`DeterministicTests`, `RuntimeTests`, `CalibrationTests`, `SeamTests` — 15/15 PASS, 19/19 CLI gates PASS, `0.000e+00` max cross-lane delta).
  - First-principles verifiers (zero cached data reads) covering anti-cancellation summation, exact Möbius/GCD, 72-edge bidirectional PLR involution, Ihara–Bass determinant residual (`1.11e-15`), exact 72-edge transfer matrix up to $m=40$ ($\pi(40) = 54{,}975{,}717{,}792$, `C-1`), Lemma 4.1 / Thm 4.2 local tune decoder (`C-4`, `NEG-M4`), global PD/Cholesky/Jacobi/PSD/Hermiticity/conservation guards (`R-Type`), Rung-1 discrete Gaussian calibration (`C-2`, `NEG-E3`), flux window & 12/31/53-EDO graph RH threshold (`C-3`, `NEG-M2`, `NEG-M3`), exhaustive 8,192 signing census (`RCT-1`, `NEG-M9`), keyed-PRNG 2-adic slope doubling RCT (`RCT-2`, `NEG-M10`), keyed-PRNG MC non-backtracking walk null (`RCT-3`), and fail-closed `P → R → D` seam handoff + bit-exact `KeyedPRNG` replay (`SEAM-1`).
- **ADPIE Cycle 2A — Lean 4 Formal Oracles (`lean/`, Lean 4.36.0, MIT, zero external deps, 0 `sorryAx`, 0 `ofReduceBool`):**
  - `Morpheus/TriadGraph.lean`: Kernel-checked proofs of Prop 2.1 and Cor 2.2 (Betti rank 13).
  - `Morpheus/TuneTheorem.lean`: Kernel-checked proofs of Lemma 4.1 (`L1`–`L3`), single-step move uniqueness, and `NEG-M4`.
  - `Morpheus/ConductorTwo.lean`: Kernel-checked proofs of Prop 3.7 (`NEG-M1`) and Thm 3.8 (universal ring homomorphism $\psi: \mathbb{Z}[\sqrt{-3}] \to \mathbb{Z}_{12}$ with principal ideal kernel $(3 - \sqrt{-3})$).
  - `Morpheus/WindingAndSchottky.lean`: Kernel-checked coboundary proof of Thm 5.1 ($12 \mid \text{walkVoiceSum}$ for *every* closed cadence of *any* length), Tonnetz Gram ($\det G = 108$), Thm 7.1(a) ($\sigma_s^2 = 2I$), $\gamma_0 = PLRLPRPL \in K$, and universal Cayley–Hamilton/Chebyshev proof of Thm 7.13 ($\forall k \ge 1,\; \operatorname{tr}(\gamma_0^k)^2 > 4\det(\gamma_0^k)$).
- **ADPIE Cycle 2B — Section 7 & Eisenstein Arithmetic Swift++ Triple-Check (`swiftpp/` `section7.*`, `Section7.swift`):**
  - **Thm 7.7:** Exact Bareiss + Iliopoulos–Bézout modular SNF + $\mathbb{F}_p$-nullity guard confirming $K(X) \cong \mathbb{Z}/2 \oplus \mathbb{Z}/2 \oplus \mathbb{Z}/8 \oplus \mathbb{Z}/736 \oplus \mathbb{Z}/6624$ (`|K| = 156,008,448`), logging 283-bit naive-SNF trap `NEG-E7`.
  - **Prop 7.2 & Thm 7.8 (`NEG-M7`):** `|Aut(X)| = 24`, 13 involutions (`0` tree quotients, `min_b1 = 5`), exhaustive Dhar burning over 20,475 divisors + degree-6 witness confirming $\operatorname{gon}(X) = 6$.
  - **Thm 3.5 & Props 7.9–7.10 (`NEG-M5`, `NEG-M6`):** Exact $\mathbb{Z}[u]$ $P_{44}(u)$ Newton counts `[3, 39, 9, 75, 33, 27]`, $a=0$ degree-4 obstruction (`-1`), and direct $\mathbb{F}_{2^k}$ projective point counts ($k \le 5$, `1,082,401` points) on genus-5 curves $A, B \subset \mathbb{P}^4$.
  - **Prop 3.7 (`NEG-M1`) & Thms 7.1/7.13 (`NEG-M8`):** All 12 Tonnetz-axis homomorphisms (conductor 12), 13 hyperbolic Schreier generators, and canonical 2-adic Bruhat–Tits ball $r \le 7$ (`382/382` distinct).
- **ADPIE Cycle 3 — Rust Fourth-Language Exact Verifier (`rust/`, `rustc 1.100.0`, MIT, zero crate deps, 7/7 tests PASS):**
  - Exact $\mathbb{Z}[\zeta_{12}]$ arithmetic & $M_7$ `[0,1,4]` flip-graph isomorphism (`Thm 3.4`), $\mathbb{Z}/12\mathbb{Z}$ voltage tower & $\mathbb{Z}[\zeta_{12}][u]$ Artin–Ihara factorization (`Thm 7.4`, `Cor 7.5`), decoder check over all `174,864` rooted primes $m \le 16$ (`Thm 4.2`, catching wording erratum `NEG-E8`), general $N$-EDO held-note sweep extended to $N \le 96$ (`11,452` systems, `0` failures), and bit-exact 4-language `KeyedPRNG` parity (`0x3fd40fd5e0f2ddff`).
- **ADPIE Cycle 4 — Audit-Forward Original Mathematical Novelties (`G4N` / `E→G4N`, folded into `v0.2.0` manuscript):**
  - [`NOVELTY_GEMINI4_NEON.md`](NOVELTY_GEMINI4_NEON.md), [`lean/Morpheus/NoveltyTheorems.lean`](lean/Morpheus/NoveltyTheorems.lean), `swiftpp/` `novelty.*`/`Novelty.swift`, and `rust/src/novelty.rs`:
    - **Independent derivation of `Thm 4.4` (`[E→GB; independently E→G4N]`) & new `Cor 4.5` (`[G4N; X]`):** Universal link-intersection bound $|L_{h_1} \cap L_{h_2}| \le 2$ (all $N \ge 3$), exact iff 1-moving-voice collision family $N = 8m$, $\{0, m, 4m\}$, $2m \in S$ (`NEG-M11` minimal counterexample $N=8, S=\{2\}, \{0,1,4\}$), and halving-closed / consecutive $S = \{1, \dots, k\}$ injectivity corollary — proved universally in Lean 4 and swept across all `10,576` chord classes $N \le 72$ under maximal $S_{\max}(c_0)$.
    - **New `§6.1 Thm 6.2` (`[E→G4N; X]`) & `Remark 6.4` (`[E→G4N; X]`):** Exact 2D honeycomb cumulants through order 6 — universal 4th-cumulant isotropy $\kappa_4/\kappa_2^2 = -17/(2m)$ (resolving `NEG-E3`), exact $C_6$ hexagonal anisotropy onset at order 6 $\kappa_6/\kappa_2^3 = (1470 + \cos 6\alpha)/(4m^2)$ (bond-parallel armchair $W=-u, v$: $1469/(4m^2)$ vs. bond-perpendicular zigzag $4u+3v$: $1471/(4m^2)$), and Edgeworth Calibration Ladder `C-2'` (**10.92×**) / `C-2''` (**75.30×** TV reduction at $m=40$, normalised on $|w| \le 24$, resolving `NEG-E9` via bounded JSD).
- **Bidirectional Cross-Reconciliation (`code/xcheck/`, `audits/xcheck_audit.md`, `reconciliation/`):**
  - Grok Bot's from-scratch cross-check `code/xcheck/audit_xcheck.py` (**32/32 PASS**, zero cached data reads; max relative error `4.55e-14` TV / `3.60e-12` JSD vs. `[X]`; all 6 `Makefile` audit suites `228/228` verified live).
  - [`reconciliation/GEMINI4_NEON_RECONCILIATION.md`](reconciliation/GEMINI4_NEON_RECONCILIATION.md) & [`reconciliation/GROKBOT_RECONCILIATION_RESPONSE.md`](reconciliation/GROKBOT_RECONCILIATION_RESPONSE.md).
- **Data Model Plane (`data/`, CC BY 4.0):** Checksummed schema-compliant (`1.0.0`) calibration records `data/calibrations/c2_winding_m40_swiftpp.json` (commit `1dc0123`) and `data/calibrations/c2_edgeworth_m40_swiftpp.json` (commit `60c786d`), verified 2/2 via `data/MANIFEST.sha256`.
- **Explanatory Videos & Social Assets (`media/`):** First-principles MIT renderers (`media/render_gemini4_neon_video.py`, `media/render_gemini4_neon_masterclass.py`, zero cached data reads), 1:24 social reel (`media/gemini4_neon_prime_cadences.mp4`), 4:18 **Spoken-in-Harmony Educator Masterclass** (`media/gemini4_neon_masterclass_chess_rh.mp4`), poster PNG, and social captions (`media/README.md`).

### Changed
- **Symmetric attribution & scholarly AI-disclosure conventions (`paper/prime-cadences.tex`, `.pdf`, `arxiv/`, `prime_cadences_paper.md`, `CONTRIBUTIONS.md`, `POLICY.md`):**
  - Standardized uniform marker scheme across both AI assistants under sole author Ergentics: `[E]`, `[GB]`, `[E→GB]`, `[G4N]`, `[E→G4N]`, `[lit.]`, `[X]` (`Thm 4.4 [E→GB; independently E→G4N]`, `Cor 4.5 [G4N; X]`, `Thm 6.2 [E→G4N; X]`, `Prop 6.3 [GB; X]`, `Remark 6.4 [E→G4N; X]`), parallel **Grok Bot** and **Gemini 4 Neon** attribution sections, literature-consistent terminology ($C_6$ hexagonal anisotropy, armchair/zigzag axes, excess kurtosis, Edgeworth expansion, homology-class prime geodesic CLT), and codified the repeatable ADPIE → reconciliation → manuscript-sync → CI → release workflow in `POLICY.md`.
- Rebuilt `paper/prime-cadences.pdf` (30 pp, `0` LaTeX errors/warnings) and neutral-header `arxiv/prime-cadences-arxiv.tar.gz`; synced `prime_cadences_paper.md`, `CITATION.cff` (`version: "0.2.0"`, `date-released: "2026-11-25"`), `README.md`, and all 23 SHA-256 checksums in `PROVENANCE.md`.
- `code/open_q/open_audit.py` & `audit_round3.py`: replaced global RNG seed with keyed per-check `random.Random(k)` (`NEG-E2` resolved; `47/47` PASS).
- Updated `NEGATIVES.md` (`NEG-M1`–`NEG-M11`, `NEG-E1`–`NEG-E9`), `CALIBRATIONS.md` (`C-2'`, `C-2''`, `C-4`), `ERGENTICS.md`, `METHODOLOGY.md`, and `AGENTS.md`.
- `code/figures/figs.py` and `paper/figures/fourier.pdf`: the `v0.1.0` label fix is retained.

## [0.1.0] - 2026-11-25

### Added
- Reconciled *Prime Cadences* baseline manuscript package (`paper/`, `arxiv/prime-cadences-arxiv.tar.gz`, `prime_cadences_paper.md`, `figures/`, `code/`, `audits/`, `CITATION.cff`, `CONTRIBUTIONS.md`, `PROVENANCE.md`, dual MIT / CC BY 4.0 licensing, `Makefile`, `requirements.txt`).
- Fixed overlapping `f_2, f_6, f_{10}` labels and clipped `f_0` in `code/figures/figs.py`, regenerated `paper/figures/fourier.pdf` and `figures/fig1_tonnetz_fourier.png`, and rebuilt `paper/prime-cadences.pdf` and `arxiv/prime-cadences-arxiv.tar.gz`.
- Governance and design specification suite: `METHODOLOGY.md`, `ARCHITECTURE.md`, `CALIBRATIONS.md`, `ERGENTICS.md`, `NEGATIVES.md`, `POLICY.md`, `SECURITY.md`, `AGENTS.md`.
- Automated `Security Hygiene` GitHub Actions workflow (`.github/workflows/security.yml`, SHA-pinned).
