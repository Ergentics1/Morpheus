# Changelog

All notable changes to **Morpheus** are documented here. Manuscript updates cut a new versioned GitHub release (`vX.Y.Z`); Code Model and Data Model verification advances are tracked under `[Unreleased]` until the next paper release.

## [Unreleased]

### Added
- **ADPIE Cycle 1 — Swift++ Triple-Check Toolkit (`swiftpp/`, MIT):**
  - **Lane 1 (`ErgenticsCXX` + `CXXStandaloneTests`):** Standalone Pure C++20 core compiled with `-O2 -Wall -Wextra -Werror` under both `g++ 13.3.0` and `clang++ 18.1.3` (22/22 assertions PASS).
  - **Lane 2 (`ErgenticsSwift`):** Independent Pure Swift 6.4 implementation with zero C++ imports.
  - **Lane 3 (`ErgenticsInterop` + `ErgenticsCLI` + 4 SWE-Sweep XCTest suites):** Live Swift 6.4 ↔ C++20 interop cross-checking every turn (`DeterministicTests`, `RuntimeTests`, `CalibrationTests`, `SeamTests` — 13/13 PASS, `0.000e+00` max cross-lane delta).
  - First-principles verifiers (zero cached data reads) covering: anti-cancellation summation sweep, exact Möbius/GCD, 72-edge bidirectional PLR involution, Ihara–Bass determinant residual (`1.11e-15`), exact 72-edge transfer matrix up to $m=40$ ($\pi(40) = 54{,}975{,}717{,}792$, Correspondence `C-1`), Lemma 4.1 / Thm 4.2 local tune decoder across 10,128 rooted primes (`C-4`, `NEG-M4`), global PD/Cholesky/Jacobi & PSD nullity & Hermiticity & conservation guards (`R-Type`), Rung-1 discrete Gaussian calibration across $m = 12 \to 24 \to 40$ (`C-2`, `NEG-E3`), flux window & 12/31/53-EDO graph RH threshold (`C-3`, `NEG-M2`, `NEG-M3`), exhaustive 8,192 signing census (`RCT-1`, `NEG-M9`), keyed-PRNG 2-adic slope doubling RCT (`RCT-2`, `NEG-M10`), keyed-PRNG MC non-backtracking walk null (`RCT-3`), and fail-closed `P → R → D` seam handoff + bit-exact `KeyedPRNG` replay (`SEAM-1`).
- **ADPIE Cycle 2A — Lean 4 Formal Oracles (`lean/`, Lean 4.36.0, MIT, zero external deps, 0 `sorry`):**
  - `Morpheus/TriadGraph.lean`: Kernel-checked proofs of Prop 2.1 ($P,L,R$ involutions, bipartiteness, 3-regularity, $P=L(LR)^4$, $R=L(LR)$, exact order 12 of $LR$, simple transitivity of $D_{12}$ on `Fin 24`) and Cor 2.2 (Betti rank 13).
  - `Morpheus/TuneTheorem.lean`: Kernel-checked proofs of Lemma 4.1 (`L1`, `L2`, `L3`), local single-step move uniqueness, and `NEG-M4` backtracking counterexample.
  - `Morpheus/ConductorTwo.lean`: Kernel-checked proofs of Prop 3.7 (`NEG-M1` mod-3/mod-4 root obstructions & non-ideal witness) and Thm 3.8 (universal ring homomorphism $\psi: \mathbb{Z}[\sqrt{-3}] \to \mathbb{Z}_{12}$, universal principal ideal kernel `(3 - √-3)`, unimodularity, non-reduced $\mathcal{O}/(2)$, and even-conductor iff theorem).
  - `Morpheus/WindingAndSchottky.lean`: Kernel-checked coboundary proof of Thm 5.1 ($12 \mid \text{walkVoiceSum}$ for *every* closed cadence of *any* length), exact Tonnetz Gram ($\det G = 108$), Thm 7.1(a) ($\sigma_s^2 = 2I$), $\gamma_0 = PLRLPRPL \in K$, and universal Cayley–Hamilton/Chebyshev proof of Thm 7.13 ($\forall k \ge 1,\; \operatorname{tr}(\gamma_0^k)^2 > 4\det(\gamma_0^k)$).
  - Axiom audit in `Main.lean`: zero `sorryAx`, zero `Classical.choice`, zero `ofReduceBool` (only Lean core `[propext, Quot.sound]` or no axioms).
- **Data Model Plane (`data/`, CC BY 4.0):**
  - Initial schema-compliant (`1.0.0`) Rung-1 calibration record `data/calibrations/c2_winding_m40_swiftpp.json` generated from commit `1dc0123`, tracked via `data/MANIFEST.sha256` and documented in `data/README.md`.
- Governance & execution docs: codified ADPIE execution cycle, anti-scaffolding/anti-hardcoding rules, and release-on-paper-update policy in `METHODOLOGY.md`, `AGENTS.md`, `POLICY.md`.

### Changed
- Synced `ERGENTICS.md` directory tree with implemented `swiftpp/` target names.
- Updated `NEGATIVES.md`: promoted `NEG-M1` (`Scoped / Resolved [Verified]`), `NEG-M2`, `NEG-M3`, `NEG-M4`, `NEG-M9`, `NEG-M10` (`Active [Verified]`) and logged exact measured finite-$m$ platykurtic excess kurtosis (`-0.8182 → -0.3931 → -0.2124`) in `NEG-E3`.
- Logged ADPIE Cycle 1 provenance in `PROVENANCE.md`.

## [0.1.0] - 2026-11-25

### Added
- Reconciled *Prime Cadences* baseline manuscript package (`paper/`, `arxiv/prime-cadences-arxiv.tar.gz`, `prime_cadences_paper.md`, `figures/`, `code/`, `audits/`, `CITATION.cff`, `CONTRIBUTIONS.md`, `PROVENANCE.md`, dual MIT / CC BY 4.0 licensing, `Makefile`, `requirements.txt`).
- Fixed overlapping `f_2, f_6, f_{10}` labels and clipped `f_0` in `code/figures/figs.py`, regenerated `paper/figures/fourier.pdf` and `figures/fig1_tonnetz_fourier.png`, and rebuilt `paper/prime-cadences.pdf` and `arxiv/prime-cadences-arxiv.tar.gz`.
- Governance and design specification suite: `METHODOLOGY.md`, `ARCHITECTURE.md`, `CALIBRATIONS.md`, `ERGENTICS.md`, `NEGATIVES.md`, `POLICY.md`, `SECURITY.md`, `AGENTS.md`.
- Automated `Security Hygiene` GitHub Actions workflow (`.github/workflows/security.yml`, SHA-pinned).
