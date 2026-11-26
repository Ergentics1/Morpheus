# Morpheus Multi-Paper Research Registry (`papers/`)

**Morpheus** (*Open Sourced Living*, by **Ergentics**) houses multiple open-source research programs under a uniform **ADPIE**, **Code-vs-Data**, and **symmetric multi-model cross-verification** standard (`[E]`, `[GB]`, `[G4N]`, `[X]`). See [`../METHODOLOGY.md`](../METHODOLOGY.md), [`../POLICY.md`](../POLICY.md), and [`../AGENTS.md`](../AGENTS.md).

## Research Portfolio

| # | Paper / Program | Location | Stage | Verification Status |
| :---: | :--- | :--- | :--- | :--- |
| **01** | ***Prime Cadences:*** *Ihara zeta, graphene, and voice-leading homology on the Tonnetz* | Root layout ([`paper/`](../paper/), [`prime_cadences_paper.md`](../prime_cadences_paper.md), [`cleanroom/prime_cadences_resolution/`](../cleanroom/prime_cadences_resolution/)) | **`v0.3.1` Released** (Immutable GitHub Release) | **3-Way Reconciled & Verified (`[E]` · `[GB]` · `[G4N]`):** 35 pp PDF, 56 refs, `228/228` + `20/20` audits, `33/33` Lean 4 theorems, Swift++ (`0.000e+00` delta), Rust (zero-PARI Manin $T_2$), PARI/GP |
| **02** | ***Working Paper 030 (Horizon Monograph I):*** *Shape-Controlled Gravitational Propulsion Resolved* (continuation of Working Paper 028) | [`wp030_shape_propulsion/`](wp030_shape_propulsion/) | **Cycle 1 Audited (`[G4N]`) · Round 1 Reconciled (`[GB]`, 2026-11-26)** | **Frozen `[E]` baseline + 3-plane `[G4N]` audit:** Python `9/9`, Lean 4.36.0 `15/15` (`0 sorryAx`), Rust `7/7` (bit-exact `SplitMix64` parity), [`GEMINI4_NEON_WP030_AUDIT.md`](wp030_shape_propulsion/reconciliation/GEMINI4_NEON_WP030_AUDIT.md) (core `H1–H4` confirmed; 8 catches `NEG-W1`–`NEG-W6` + Theorem G1); awaiting independent **Grok Bot** (`[GB]`) pass |
| **03** | ***Working Paper 032 (Horizon Monograph IC):*** *Bennu-Class Triaxial Proximity Ops, 3D Multi-Tether FEM/FDIR & Extended-Body 3-Body Problem* | [`wp032_bennu_3body/`](wp032_bennu_3body/) | **Cycle 1 Audited (`[G4N]`) · Round 1 Reconciled (`[GB]`, 2026-11-26)** | **Frozen `[E]` baseline + 3-plane `[G4N]` audit:** Python `6/6`, Lean 4.36.0 `9/9` (`0 sorryAx`), Rust `5/5` (`SplitMix64` `0x55a32a121430eb49`), [`GEMINI4_NEON_WP032_AUDIT.md`](wp032_bennu_3body/reconciliation/GEMINI4_NEON_WP032_AUDIT.md) (4 catches `NEG-W7`–`NEG-W10` + Theorem G2); awaiting `[GB]` pass |
| **04** | ***Working Paper 033 (Horizon Monograph ID):*** *3D Non-Planar CRTBP Halo/Lissajous Manifolds, Rotating-Symplectic Floquet Control & Bennu TAG Guidance* | [`wp033_halo_tag_guidance/`](wp033_halo_tag_guidance/) | **Cycle 1 Audited (`[G4N]`) · Round 1 Reconciled (`[GB]`, 2026-11-26)** | **Frozen `[E]` baseline + 3-plane `[G4N]` audit:** Python `4/4`, Lean 4.36.0 `7/7` (`0 sorryAx`, $6\times 6$ $\Omega = S^T J S$), Rust `4/4` (bit-exact `SplitMix64` `0xda9392ed940a41ee`), [`GEMINI4_NEON_WP033_AUDIT.md`](wp033_halo_tag_guidance/reconciliation/GEMINI4_NEON_WP033_AUDIT.md) (4 catches `NEG-W11`–`NEG-W14` + Theorem G3); awaiting `[GB]` pass |
| **05** | ***Working Paper 031 (Horizon Monograph IB):*** *3D Non-Planar $J_2$ Symmetry Breaking, Collinear-Bridge $\mathrm{SO}(3)$ Holonomy, Safe-Perigee `K9` & HIL Sizing* | [`wp031_3d_j2_hil/`](wp031_3d_j2_hil/) | **Cycle 1 Audited (`[G4N]`) · Round 1 Reconciled (`[GB]`, 2026-11-26)** | **Frozen `[E]` baseline + 3-plane `[G4N]` audit:** Python `5/5`, Lean 4.36.0 `9/9` (`0 sorryAx`), Rust `5/5` (bit-exact `SplitMix64` `0xc844f9d684ec259c`), [`GEMINI4_NEON_WP031_AUDIT.md`](wp031_3d_j2_hil/reconciliation/GEMINI4_NEON_WP031_AUDIT.md) (4 catches `NEG-W15`–`NEG-W18` + Theorem G4); awaiting `[GB]` pass |
| **06** | ***Working Paper 034 (Horizon Monograph IE):*** *Independent Precision Audit & Structural Pressure Test of Algebraic Null-Cone Quantum Gravity (`arXiv:2611.34924v1`)* | [`wp034_null_cone_gravity/`](wp034_null_cone_gravity/) | **Cycle 1 Audited (`[G4N]`) · Round 1 Reconciled (`[GB]`, 2026-11-26)** | **Frozen `[E]` baseline + 3-plane `[G4N]` meta-audit:** Python `5/5`, Lean 4.36.0 `9/9` (`0 sorryAx`), Rust `5/5` (bit-exact `SplitMix64` `0xb4005f8bfe2e1bca`), [`GEMINI4_NEON_WP034_AUDIT.md`](wp034_null_cone_gravity/reconciliation/GEMINI4_NEON_WP034_AUDIT.md) (primary-source Sen 2013 cross-check + 3 catches `NEG-W19`–`NEG-W21` + Theorem G5); awaiting `[GB]` pass |
| **07** | ***Working Paper 035 (Horizon Monograph IF — Series Finale):*** *Independent Audit of Hopf-Fibration Unified Field Theory (Nielsen 2026) & Non-Circular Hagedorn Nuclearity Repair of Null-Cone Gravity* | [`wp035_tuft_hagedorn_repair/`](wp035_tuft_hagedorn_repair/) | **Cycle 1 Audited (`[G4N]`) · Round 1 Reconciled (`[GB]`, 2026-11-26)** | **Frozen `[E]` baseline + 3-plane `[G4N]` audit:** Python `5/5`, Lean 4.36.0 `9/9` (`0 sorryAx`), Rust `5/5` (bit-exact `SplitMix64` `0xcc617ec51b6fb1e0`), [`GEMINI4_NEON_WP035_AUDIT.md`](wp035_tuft_hagedorn_repair/reconciliation/GEMINI4_NEON_WP035_AUDIT.md) (Track A + Track B R1–R3 + 3 catches `NEG-W22`–`NEG-W24` + Theorem G6); **closes Horizon I–IF `[G4N]` pass, ready for `[GB]`** |

*Numbering (`#`) follows intake order, not working-paper number: WP 032 and WP 033 were archived before WP 031, so WP 031 is #05. Each Horizon paper now has a `[GB]` Round-1 reconciled edition under `paper/` and a dossier `reconciliation/GROKBOT_WP0xx_ROUND1.md`; the round summary is [`../reconciliation/horizon_round1/RECONCILIATION_CHANGELOG.md`](../reconciliation/horizon_round1/RECONCILIATION_CHANGELOG.md).*

## Standard Per-Paper Directory Layout (`papers/<slug>/`)

*Paper #01 (*Prime Cadences*) remains frozen at the repository root paths established in `v0.1.0`–`v0.3.1` so existing release checksums, citations, and links stay permanently intact.* All subsequent papers live self-contained under `papers/<slug>/` with strict separation between frozen clean-room intakes, reconciled manuscripts, executable verifiers, and checksummed data:

```text
papers/<slug>/
├── README.md          # Paper intake card, lifecycle status, and assessment checklist
├── cleanroom/         # Verbatim, unmodified clean-room intake (Rule 5 frozen once archived)
├── paper/             # Reconciled manuscript, bibliography, figures, and compiled PDF (post-assessment)
├── reconciliation/    # Independent [G4N], [GB], and 3-way cross-audit dossiers
├── lean/              # Optional zero-Mathlib Lean 4 formal proofs (Code Model, MIT)
├── swiftpp/           # Optional C++20 / Pure Swift / Interop verifiers (Code Model, MIT)
├── rust/              # Optional zero-crate Rust verifiers (Code Model, MIT)
├── code/              # Optional Python/SymPy/numerical audit suites (Code Model, MIT)
└── data/              # Immutable SHA-256-checksummed calibration outputs (Data Model, CC BY 4.0)
```
