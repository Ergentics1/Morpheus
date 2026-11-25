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
- **ADPIE Cycle 2B — Section 7 & Eisenstein Arithmetic Swift++ Triple-Check (`swiftpp/` `section7.*`, `Section7.swift`):**
  - **Thm 7.7 (Sandpile / Critical Group $K(X)$):** Exact Bareiss fraction-free determinant (max 55 bits) + Iliopoulos–Bézout modular SNF mod $\Delta$ + independent $\mathbb{F}_p$-nullity guard (`nullity_2 = 5`, `nullity_3 = 1`, `nullity_23 = 2`), verifying $K(X) \cong \mathbb{Z}/2 \oplus \mathbb{Z}/2 \oplus \mathbb{Z}/8 \oplus \mathbb{Z}/736 \oplus \mathbb{Z}/6624$ (`|K| = 156,008,448`). Caught and logged silent 283-bit `__int128` expression-swell trap in naive SNF as `NEG-E7`.
  - **Prop 7.2 & Thm 7.8 (`NEG-M7`):** Exhaustive graph-automorphism backtracking (`|Aut(X)| = 24`), 13 involutions with `0` tree quotients (`min_b1 = 5`, Chan's criterion), and exhaustive Dhar burning across all `20,475` effective divisors $D \ge (C)$ of degree $\le 5$ (`0` of rank $\ge 1$) + degree-6 witness $2\mathrm{C}+2\mathrm{Am}+\mathrm{D}\flat+\mathrm{A}\flat\mathrm{m}$ confirming $\operatorname{gon}(X) = 6$.
  - **Thm 3.5 & Props 7.9–7.10 (`NEG-M5`, `NEG-M6`):** Exact $\mathbb{Z}[u]$ Weil polynomial $P_{44}(u)$ Newton point counts `[3, 39, 9, 75, 33, 27]` ($N_6 < N_2$, residual `2.4e-14`), $a=0$ cofactor obstruction (`-1` degree-4 places), and direct $\mathbb{F}_{2^k}$ projective point counting ($k \le 5$, `1,082,401` points) on genus-5 complete intersections $A, B \subset \mathbb{P}^4$ matching $L_A, L_B$ identically (`#A = [2, 16, 14, 20, 22]`, `#B = [4, 16, 4, 20, 44]`).
  - **Prop 3.7 (`NEG-M1`):** Exhaustive check of all 12 Tonnetz-axis homomorphisms $\mathbb{Z}[\omega] \to \mathbb{Z}_{12}$ confirming multiplier conductor `12` (`0` ideals).
  - **Thms 7.1 & 7.13 (`NEG-M8`):** Exact 13 hyperbolic Schreier generators of $K$, canonical 2-adic Hermite normal form Bruhat–Tits ball $r \le 7$ (`382/382` distinct vertices), and $\gamma_0 = PLRLPRPL$ ($\operatorname{tr} = 85$, $\det = 256$, $\tau > 4$).
  - All 3 lanes passing: 27/27 C++20 (`g++` & `clang++`, `-Wall -Wextra -Werror`), 14/14 XCTests, 16/16 CLI gates, `0.000e+00` max cross-lane delta.
- **ADPIE Cycle 3 — Rust Fourth-Language Exact Verifier (`rust/`, `rustc 1.100.0`, MIT, zero crate deps):**
  - **Thm 3.4 (`src/cyclotomic.rs`):** Exact $\mathbb{Z}[\zeta_{12}]$ ring arithmetic ($f_3 = 2-i$, $f_4^2 = -3$, minimal polynomial of $f_1$, $N(f_1)=1$, $|f_5|^2 = 2+\sqrt{3}$, Galois action, $M_{11}$ automorphism, and $M_7$ bijection onto the 24 `[0,1,4]` chords & 36 flip edges).
  - **Thm 7.4 & Cor 7.5 (`src/tower.rs`):** Exact $\mathbb{Z}/12\mathbb{Z}$ voltage cover $X \to \Theta$ (36/36 edges, lifts `6, 8, 24`) and exact $\mathbb{Z}[\zeta_{12}][u]$ Artin–Ihara character factorization across all 6 character-order blocks.
  - **Thm 4.2 & Thm 4.3 / `C-4` (`src/tune_general.rs`):** Verified local tune decoder across all `174,864` rooted primes $m \le 16$ (`131,136` at $m = 16$, `0` failures — caught baseline wording erratum `NEG-E8`), verified all `6,028` general $(N, S, \mathcal{C})$ systems for $N \le 72$, and pushed the open boundary to **$N \le 96$ (`11,452` systems, `0` failures)**.
  - **Fourth-language SWE-sweep (`src/swe_sweep.rs`, `src/keyed_prng.rs`):** Independent confirmation of $\pi(40) = 54{,}975{,}717{,}792$, Rung-1 TV/excess-kurtosis, anti-cancellation, PD/Cholesky spike & `NaN` guards, and bit-exact 4-language `KeyedPRNG` parity (`0x3fd40fd5e0f2ddff` across C++20, Pure Swift 6.4, Swift ↔ C++20 Interop, and Rust).
  - 5/5 integration tests PASS in 3.22s (`--release`).
- **Data Model Plane (`data/`, CC BY 4.0):**
  - Initial schema-compliant (`1.0.0`) Rung-1 calibration record `data/calibrations/c2_winding_m40_swiftpp.json` generated from commit `1dc0123`, tracked via `data/MANIFEST.sha256` and documented in `data/README.md`.
- Governance & execution docs: codified ADPIE execution cycle, anti-scaffolding/anti-hardcoding rules, and release-on-paper-update policy in `METHODOLOGY.md`, `AGENTS.md`, `POLICY.md`.

### Changed
- Synced `ERGENTICS.md` directory tree with implemented `swiftpp/` target names.
- Updated `NEGATIVES.md`: promoted `NEG-M1` & `NEG-M6` (`Scoped / Resolved [Verified]`), `NEG-M2`, `NEG-M3`, `NEG-M4` (extended to $N \le 96$, 11,452 systems), `NEG-M5`, `NEG-M7`, `NEG-M8` (core), `NEG-M9`, `NEG-M10` (`Active [Verified]`); logged exact finite-$m$ kurtosis in `NEG-E3`, `NEG-E7` (283-bit SNF silent overflow trap), and `NEG-E8` (`131,136` vs `174,864` manuscript wording erratum).
- Logged ADPIE Cycle 1 provenance in `PROVENANCE.md`.

## [0.1.0] - 2026-11-25

### Added
- Reconciled *Prime Cadences* baseline manuscript package (`paper/`, `arxiv/prime-cadences-arxiv.tar.gz`, `prime_cadences_paper.md`, `figures/`, `code/`, `audits/`, `CITATION.cff`, `CONTRIBUTIONS.md`, `PROVENANCE.md`, dual MIT / CC BY 4.0 licensing, `Makefile`, `requirements.txt`).
- Fixed overlapping `f_2, f_6, f_{10}` labels and clipped `f_0` in `code/figures/figs.py`, regenerated `paper/figures/fourier.pdf` and `figures/fig1_tonnetz_fourier.png`, and rebuilt `paper/prime-cadences.pdf` and `arxiv/prime-cadences-arxiv.tar.gz`.
- Governance and design specification suite: `METHODOLOGY.md`, `ARCHITECTURE.md`, `CALIBRATIONS.md`, `ERGENTICS.md`, `NEGATIVES.md`, `POLICY.md`, `SECURITY.md`, `AGENTS.md`.
- Automated `Security Hygiene` GitHub Actions workflow (`.github/workflows/security.yml`, SHA-pinned).
