# Morpheus Standardized Universal Lexicon (`LEXICON.md`)

> **Auto-generated deterministically from** [`data/lexicon/morpheus_universal_lexicon.json`](data/lexicon/morpheus_universal_lexicon.json) via `python3 tests/lexicon_audit.py --emit-md`. Do not hand-edit; byte-exact parity is enforced by CI Gate `CI-12`.

- **Schema Version:** `1.0.0` (ISO 704:2022 Three-Tier Terminology Alignment)
- **Scope:** Morpheus 10-paper verified research corpus (Paper #01 Prime Cadences, Horizon WP 030-035 and Horizon Synthesis Pieces I-III, PC-II, PC-III, PC-IV); excludes external unarchived Swift++ WP 053 fluids/MHD and Atelier binary pipelines.
- **Coverage:** `60` canonical concepts × `3` tiers (`180` aligned expressions), `120` deprecated-alias traps, `6` scoped symbol disambiguations, and `50` Tier-3 specialist jargon markers.
- **Automated Enforcement:** Research strict ceiling `0` deprecated aliases; Atelier broadcast ceiling `JWR <= 2.5%` and Flesch–Kincaid Grade `[5.0, 12.5]`.

## Discipline Breakdown

| Discipline | Concept Count |
| :--- | :---: |
| **Arithmetic & Shimura Graphs** (`arithmetic_shimura_graphs`) | `22` |
| **Horizon Orbital & Quantum Gravity** (`horizon_orbital_gravity`) | `14` |
| **Verified Compilers, Oracles & Provers** (`verified_compilers_provers`) | `14` |
| **Empirical Methodology & Integrity Auditing** (`empirical_methodology_auditing`) | `10` |
| **Total** | **`60`** |

## Scoped Symbol Disambiguations

| Symbol ID | LaTeX | Discipline | Meaning | Disambiguated From |
| :--- | :---: | :--- | :--- | :---: |
| `Z_graph` | `$\mathcal{Z}_{\mathrm{graph}}$` | Arithmetic & Shimura Graphs | 4-regular 24-vertex Dicyclic Companion Cayley graph Cay(Dic_6, S) with 48 edges | `Z_part` |
| `Z_part` | `$Z_{\mathrm{part}}(\beta)$` | Horizon Orbital & Quantum Gravity | Canonical thermal partition function Tr(exp(-beta H)) in Hagedorn nuclearity analysis | `Z_graph` |
| `D_quat` | `$D_{\mathrm{quat}}$` | Arithmetic & Shimura Graphs | Reduced discriminant of a definite quaternion algebra over a totally real field | `d_F` |
| `d_F` | `$d_{F}$` | Arithmetic & Shimura Graphs | Absolute field discriminant of a totally real number field F | `D_quat` |
| `g_curve` | `$g_{\mathrm{curve}}$` | Arithmetic & Shimura Graphs | Arithmetic or tropical genus (first Betti number) of a Shimura or Mumford curve | `g_grav` |
| `g_grav` | `$g_{\mathrm{grav}}$` | Horizon Orbital & Quantum Gravity | Local gravitational acceleration magnitude on Earth, Moon, or small-body regolith | `g_curve` |

## Arithmetic & Shimura Graphs (`22` Concepts)

| ID | Tier 1 (Plain-English / Broadcast) | Tier 2 (Canonical Research) | Tier 3 (Specialist Literature Anchor) | Deprecated Aliases |
| :--- | :--- | :--- | :--- | :--- |
| `triad_tonnetz_graph` | 24-Chord Voice Network | **Neo-Riemannian Triad Graph** | 3-regular 24-vertex Cayley graph X = Cay(T/I, {P, L, R}) of genus 13 | `triad web`, `musical mesh` |
| `ihara_prime_cadence` | Indivisible Chord Loop | **Ihara Prime Cadence** | Primitive reduced tailless closed walk in the Ihara zeta function Z_X(u) | `prime chord loop`, `zeta cadence cycle` |
| `ramanujan_graph_corridor` | Optimal Mixing Bound | **Ramanujan Spectral Corridor** | Optimal nontrivial adjacency bound \|lambda_nt\| <= 2 sqrt(q) and Hashimoto trace corridor | `ramanujan magic bound`, `optimal graph hallway` |
| `voice_leading_homology` | Pitch-Drift Loop Count | **Voice-Leading Homology** | Lattice winding map H_1(X, Z) -> Z^2 on the hexagonal Tonnetz torus | `tone winding algebra`, `chord loop drift` |
| `uniform_triadic_wreath` | Two-Mode Chord Symmetry Group | **Uniform Triadic Wreath Product** | Hook group UTT = Z_12 wr Z_2 of order 288 and twin-diamond normalizer N_Sym(24)(UTT) | `hook chord wreath`, `triad wreath pack` |
| `nauru_lame_graph` | Symmetric 36-Bridge Star Graph | **Nauru Generalized Petersen Graph** | GP(12, 5) = {6,3}_{(2,2)} of order 24, \|Aut(Y)\| = 144, Lamé amalgam S_3 *_{Z_2} V_4 | `nauru star mesh`, `petersen 12-5 web` |
| `dicyclic_companion_graph` | 48-Bridge Companion Network | **Dicyclic Companion Graph** | 4-regular Cayley graph Z_graph = Cay(Dic_6, S), V = 24, E = 48, g = 25, \|Aut(Z)\| = 96 | `dic6 48-edge mesh`, `dicyclic buddy graph` |
| `bruhat_tits_uniformization` | Infinite Branching Prime Tree | **Bruhat-Tits Tree Uniformization** | p-adic Schottky quotient Gamma \ T_{q+1} for PGL_2(F_v) yielding a Mumford curve | `p-adic tree unwrapper`, `schottky branch tree` |
| `raynaud_sandpile_snf` | Chip-Firing Signature Table | **Raynaud Component Group SNF** | Smith normal form of reduced graph Laplacian K(G) = Phi(J(C_G)) | `sandpile signature list`, `laplacian torsion bag` |
| `metric_gonality_scramble` | Minimum Bottleneck Chip Count | **Equilateral Metric Gonality** | Scramble lower bound sn(G) <= dgon(G) <= gon(Gamma_eq(G)) <= gon(C_G) via Dhar burning | `chip bottleneck number`, `dhar gonality score` |
| `fricke_vogt_quaternion_surface` | Trace-Matched Parameter Map | **Fricke-Vogt Quaternion Surface** | Quaternion algebra family B(x) = (-3, x(x-3)) and B_Z(u,v) parametrized by character traces | `fricke trace sheet`, `quaternion parameter plane` |
| `universal_twin_duality` | Mirror Parameter Swap | **Universal Algebraic Twin Duality** | Involution tau((bt)a) = 3 - x exchanging surjections rho_6 <-> rho_12 across twin moduli | `parameter mirror flip`, `twin trace swap` |
| `level_congruence_shimura` | Clock-Remainder Arithmetic Curve | **Full Congruence Shimura Curve** | Arithmetic lattice containing principal congruence subgroup Gamma(M) in O[1/p]^1 / {+-1} | `clock-remainder curve`, `modular congruence loop` |
| `non_congruence_cover` | Hidden Non-Modular Cover | **Strictly Non-Congruence Arithmetic Cover** | Finite-index arithmetic subgroup Gamma not containing any principal congruence subgroup Gamma(M) | `non-modular sneaky cover`, `uncongruent quilt` |
| `split_prime_diagonal_sign_flip` | Split-Mirror Sign Flip | **Split-Prime Diagonal Sign-Flip** | Central element sigma = 1 - 2w equiv (+1, -1) mod (4) separating Ad_(4) from L_(4)/{+-1} | `split sign trick`, `diagonal mod-4 toggle` |
| `riehm_congruence_obstruction` | Coprime Normal-Subgroup Wall | **Riehm Congruence Obstruction** | Normal subgroup classification in SL_1(O_v) forcing trivial abelian kernels when gcd(e, q) = 1 | `riehm local wall`, `coprime kernel blocker` |
| `hecke_brandt_matrix` | Grid-Transition Table | **Hecke Brandt Matrix** | Definite quaternion ideal-class adjacency matrix B(p) representing the Hecke operator T_p | `brandt grid table`, `ideal hop matrix` |
| `manin_modular_symbols` | Exact Modular Frequency Sieve | **Manin Modular Symbols** | Finite-dimensional presentation of S_2(Gamma_0(M)) computing exact Hecke action T_p via Heilbronn matrices | `manin symbol sieve`, `modular form crusher` |
| `su2_wilson_holonomy` | Compact Rotation Loop Cost | **Compact SU(2) Wilson-Loop Action** | Definite quaternion trace bound tau(w) = 4 cos^2(theta) <= 4 and S_W(w) = 1 - sqrt(tau(w))/2 in (0,1) | `wilson loop penalty`, `su2 trace cost` |
| `poitou_odlyzko_explicit_formula` | Prime-Field Size Floor | **Poitou-Odlyzko Explicit Formula** | Positivity-constrained Fourier kernel lower bound on d_F^{1/n} including Sym^2 positive kernels | `odlyzko floor hack`, `discriminant squeeze formula` |
| `three_pincer_hilbert_obstruction` | Three-Wall Degree Squeeze | **Three-Pincer Hilbert Class Field Obstruction** | Joint Odlyzko, Hilbert class field, and decomposition-field bound collapsing n <= 14 to n <= 8 | `three-pincer crunch`, `hilbert degree trap` |
| `genus25_borel_census` | Nine-Curve Genus-25 Catalog | **Torsion-Free Genus-25 Borel Census** | Complete 19-curve (9 torsion-free) Eichler-Shimura list X_0^D(N) of genus 25 at p = 3 | `genus 25 curve roster`, `borel 9-curve list` |

## Horizon Orbital & Quantum Gravity (`14` Concepts)

| ID | Tier 1 (Plain-English / Broadcast) | Tier 2 (Canonical Research) | Tier 3 (Specialist Literature Anchor) | Deprecated Aliases |
| :--- | :--- | :--- | :--- | :--- |
| `isoinertial_hopf_switching` | Constant-Inertia Shape Wave | **Iso-Inertial Hopf-Fibration Quadrupole Switching** | Three-mass planar trajectory preserving total scalar moment of inertia I_0 = (2/3) M L^2 on the Hopf sphere | `hopf tether wiggle`, `iso-inertia swing` |
| `noether_constant_p_bound` | Axial Momentum Conservation Law | **Noether Constant-p Conservation Bound** | Exact invariance of axial angular momentum J_z under axisymmetric central and J_2 potentials | `noether p lock`, `axial spin ceiling` |
| `shapere_wilczek_holonomy` | Shape-Cycle Rotation Shift | **Shapere-Wilczek Geometric Holonomy** | Berry-Montgomery signed net orientation angle Delta theta = +-90 deg over a closed zero-angular-momentum loop | `shape loop twist`, `geometric reorientation trick` |
| `zero_spin_kinetic_divergence` | High-Stretch Energy Spike | **Zero-Spin Kinetic Divergence (Theorem G1)** | Exact shape kinetic energy T_shape = (1/8) I_0 beta_dot^2 + (q^2/(1-q^2))((1/2) I_0 omega_orb^2) on equilateral Hopf basis w_+- | `collinear energy blowup`, `theorem g1 spike` |
| `mechanical_spring_drum_hub` | Coupled Spring-Drum Hub | **Mechanical Differential Spring-Drum Hub (Theorem G4)** | Coupled elastic hub avoiding the >= 9.85x I_0-invariant electrical motor-winch waste-heat floor (13.92 W baseline) | `tether spring box`, `winch heat bypass` |
| `nonplanar_j2_symmetry_breaking` | Oblate-Planet Tilt Drift | **Non-Planar J_2 Symmetry Breaking** | Differential inclination/nodal torque measured against the subtracted L = 0 point-mass J_2 control baseline | `j2 tilt drift`, `bulge plane nudge` |
| `safe_perigee_k9_eccentricity` | Best Safe-Altitude Orbit Shape | **Safe-Perigee Optimal Eccentricity (K9)** | Unique optimal orbital eccentricity e_opt^* = 0.2817015579087740 maximizing safe-perigee quadrupole impulse | `k9 best ellipse`, `perigee sweet spot` |
| `com_shifted_fdir_inertia` | Jammed-Winch Rebalance Law | **COM-Shifted Three-Arm FDIR Inertia Law (Theorem G2)** | Exact center-of-mass-corrected inertia inversion yielding 21.0% peak tension relief under single-winch jam | `winch jam workaround`, `fdir inertia patch` |
| `transverse_y_halo_resonance` | Sideways Tether Halo Lock | **Transverse-y L_2 Halo Resonance Closure (Theorem G3)** | Laplace-constrained 3D CRTBP multipole coupling closing Didymos-Dimorphos L_2 to 1:1 resonance at L_y^* = 40.44 m | `didymos halo tweak`, `y-axis l2 resonance hack` |
| `elevated_wu_floquet_branch` | Safe Lunar-Capture Highway | **Elevated Safe Lunar-Capture W^u Branch** | 42-ODE CRTBP unstable manifold branch clearing lunar radius (+327.2 km altitude) with 8,814x Floquet station-keeping | `safe moon highway`, `floquet capture lane` |
| `fluidized_bennu_tag_guidance` | Loose-Rubble Touch-and-Go Control | **Fluidized Regolith Bennu TAG Guidance** | Closed-loop contact guidance validated across 500-700 kg/m^3 subsurface regolith density (MC200 200/200 SAFE) | `bennu rubble landing`, `tag dirt control` |
| `riemann_rearrangement_universality` | Order-Dependent Sum Breakdown | **Non-Hilbert-Schmidt Riemann Rearrangement Universality (Theorem G5)** | Nested strong exhaustions on H = l^2(N) + l^2(N) driving closed-cut Z_P[X] to any prescribed real limit L | `trace reordering paradox`, `cut sum ambiguity` |
| `odd_sphere_spectral_zeta` | Curved-Sphere Mode Sum | **Odd-Sphere Spectral Zeta Regularization** | Analytic continuation of Laplacian/Dirac mode sums on S^{2k+1} and lens spaces L(p,1) with 4-loop QED a_e check | `sphere zeta test`, `lens mode tally` |
| `hagedorn_equivalence_breaking` | Thermal-Temperature Spread Floor | **Hagedorn Canonical Equivalence-Breaking (Theorem G6)** | Exact Gamma(alpha, alpha) canonical energy dispersion 1/sqrt(alpha) and 1/sqrt(alpha+2) truncation bridge | `hagedorn heat jitter`, `canonical spread bug` |

## Verified Compilers, Oracles & Provers (`14` Concepts)

| ID | Tier 1 (Plain-English / Broadcast) | Tier 2 (Canonical Research) | Tier 3 (Specialist Literature Anchor) | Deprecated Aliases |
| :--- | :--- | :--- | :--- | :--- |
| `correspondence_seam` | Limit Check | **Correspondence Seam** | Dimensionless error bound \|f_exact - f_limit\| <= epsilon linking discrete algorithms to continuum limits (C_k) | `correspondence glue`, `limit error check` |
| `outward_rounded_interval` | Safe Number Box | **Outward-Rounded Interval** | IEEE-754 hardware directed-rounding bracket [x_down, x_up] via FE_DOWNWARD / FE_UPWARD with -ffp-contract=off | `FENV bracket`, `safe float range` |
| `zero_mathlib_lean_kernel` | Self-Contained Proof Kernel | **Zero-Mathlib Lean 4 Kernel Proof** | Machine-checked proof compiled directly by Lean 4.36.0 Init kernel with -DwarningAsError=true -DautoImplicit=false | `bare lean script`, `mathlib-free hack` |
| `axiom_trust_boundary` | Zero-Shortcut Proof Audit | **Lean Axiom Trust Boundary** | Live #print axioms verification enforcing 0 sorryAx and 0 Lean.ofReduceBool across every theorem | `sorry-free badge`, `axiom shortcut scan` |
| `unimodular_snf_certificate` | Direct Integer-Matrix Proof | **Pure-Kernel Unimodular SNF Certificate** | Explicit integer matrices U, V (det = +-1) proving U L V = diag(d_i) directly by kernel rfl | `snf witness blob`, `matrix rfl shortcut` |
| `dual_compiler_fenv_parity` | Two-Compiler Bitwise Match | **Dual-Compiler Hardware-FENV Parity** | Zero-byte diff -u equality between g++ and clang++ builds under -O2 -std=c++20 -frounding-math -ffp-contract=off | `gcc clang match`, `raw ARM64 emitter` |
| `freestanding_zero_heap_oracle` | Fixed-Memory Math Checker | **Freestanding Zero-Heap Oracle** | Static-memory C++20 verification binary with zero dynamic allocations and deterministic IEEE-754 state restoration | `no-malloc checker`, `stack-only math stub` |
| `three_prime_crt_determinant` | Exact Multi-Prime Determinant | **Three-Prime CRT Exact Determinant** | Overflow-free Gaussian elimination modulo three 31-bit primes reconstructed via Chinese Remainder Theorem | `crt det trick`, `modular det shortcut` |
| `keyed_splitmix64_replay` | Bit-Exact Random Replay | **Keyed SplitMix64 Cross-Language Replay** | Deterministic 64-bit SplitMix64 stream and FNV-1a64 / XOR order-invariant digests matched across Python, Rust, and C++ | `seeded rng hash`, `random replay checksum` |
| `code_data_separation` | Live Math vs. Saved Tables | **Code-vs-Data Model Separation** | Rule 2 boundary separating executable MIT verifiers from immutable SHA-256 CC BY 4.0 data records (CI-9) | `code data firewall`, `no cached JSON rule` |
| `frozen_baseline_lock` | Tamper-Proof Baseline Seal | **Frozen-Baseline SHA-256 Lock** | Rule 5 cryptographic SHA-256 immutability verification of archived baseline papers and clean-room intakes (CI-10) | `frozen hash guard`, `immutable file pin` |
| `neutral_arxiv_bundle` | Clean Reproducible Source Archive | **Neutral-Header arXiv Bundle** | Deterministic tar.gz archive with 0/0 numeric ownership, 1970-01-01 timestamps, and standalone pdflatex verification (CI-3) | `clean arxiv zip`, `0/0 tar packet` |
| `cancellation_free_reformulation` | Loss-Free Formula Rewrite | **Cancellation-Free Floating-Point Reformulation** | Algebraic rewriting eliminating catastrophic subtraction (0.0 error vs. 100% 106-bit double-double wipeout at s = 10^77) | `float cancel patch`, `double-double rescue` |
| `cross_paper_seam_gate` | Cross-Paper Consistency Lock | **Cross-Paper Mathematical Seam Gate (CI-11)** | Automated parity check enforcing exact numerical and structural agreement across Papers #01, PC-II, PC-III, PC-IV, and Horizon Synthesis | `cross-paper glue check`, `seam parity script` |

## Empirical Methodology & Integrity Auditing (`10` Concepts)

| ID | Tier 1 (Plain-English / Broadcast) | Tier 2 (Canonical Research) | Tier 3 (Specialist Literature Anchor) | Deprecated Aliases |
| :--- | :--- | :--- | :--- | :--- |
| `adpie_verification_cycle` | Five-Step Rigor Loop | **ADPIE Verification Cycle** | Structured Assess -> Diagnose -> Plan -> Implement -> Evaluate research engineering cycle (METHODOLOGY.md) | `adpie loop hack`, `five-stage sprint` |
| `mechanical_falsifier` | Trap Check | **Mechanical Falsifier** | Deterministic negative control or adversarial input engineered to trigger explicit rejection on invalid assumptions | `anti-facade gate`, `bad-input trap` |
| `permanent_negatives_ledger` | Open Dead-End Log | **Permanent Negatives Ledger** | Immutable catalog (NEGATIVES.md: NEG-M*, NEG-E*, NEG-W*) preserving every refuted claim, erratum, and scope cliff | `failure notebook`, `error graveyard` |
| `randomized_calibration_trial` | Keyed Random Null Test | **Randomized Controlled Calibration Trial (RCT)** | Reproducible keyed-PRNG baseline comparison (CALIBRATIONS.md: RCT-1..RCT-9) separating genuine signal from random ensembles | `monte carlo sanity check`, `random baseline ping` |
| `drp_seam_swe_sweep` | Four-Layer Stress Sweep | **D/R/P/Seam SWE-Sweep** | Joint verification across Deterministic (D), Runtime global-invariant (R), Probabilistic calibration (P), and cross-plane seams | `four-way stress test`, `swe quality sweep` |
| `symmetric_multimodel_attribution` | Balanced Credit Tagging | **Symmetric Multi-Model Attribution** | Uniform scholarly provenance tags ([E], [GB], [G4N], [lit.], [X]) recorded symmetrically in CONTRIBUTIONS.md and POLICY.md | `ai credit label`, `equal author tag` |
| `cleanroom_independent_xcheck` | From-Scratch Cross-Check | **Clean-Room Independent Cross-Verification** | Zero-shared-data reproduction across independent codebases and formalisms marked [X] only after live recomputation | `3-way check`, `blind recheck pass` |
| `content_integrity_harness` | Automated Repository Guardian | **Content-Integrity Audit Harness** | Zero-dependency CI suite (tests/content_integrity_audit.py, CI-1..CI-12) guarding hashes, links, LaTeX, Lean, and terminology | `repo health script`, `integrity bot check` |
| `three_tier_lexical_alignment` | Three-Level Shared Glossary | **Three-Tier Lexical Alignment** | ISO 704 single-source-of-truth registry synchronizing Plain-English Tier 1, Canonical Tier 2, and Literature Tier 3 terms | `glossary sync sheet`, `jargon mapper` |
| `jargon_readability_gate` | Plain-Language Score | **Jargon-to-Word Ratio Gate** | Automated JWR <= 2.5% and Flesch-Kincaid Grade [5.0, 12.5] readability check enforcing zero-alias research and plain broadcast prose (CI-12) | `jargon score cap`, `readability throttle` |

## Verification Commands

```bash
python3 tests/lexicon_audit.py --self-test
sha256sum -c data/lexicon/MANIFEST.sha256
cargo test --release --manifest-path tests/lexicon_rust/Cargo.toml
```
