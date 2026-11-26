# Morpheus Multi-Paper Research Registry (`papers/`)

**Morpheus** (*Open Sourced Living*, by **Ergentics**) houses multiple open-source research programs under a uniform **ADPIE**, **Code-vs-Data**, and **symmetric multi-model cross-verification** standard (`[E]`, `[GB]`, `[G4N]`, `[X]`). See [`../METHODOLOGY.md`](../METHODOLOGY.md), [`../POLICY.md`](../POLICY.md), and [`../AGENTS.md`](../AGENTS.md).

## Research Portfolio

| # | Paper / Program | Location | Stage | Verification Status |
| :---: | :--- | :--- | :--- | :--- |
| **01** | ***Prime Cadences:*** *Ihara zeta, graphene, and voice-leading homology on the Tonnetz* | Root layout ([`paper/`](../paper/), [`prime_cadences_paper.md`](../prime_cadences_paper.md), [`cleanroom/prime_cadences_resolution/`](../cleanroom/prime_cadences_resolution/)) | **`v0.3.1` Released** (Immutable GitHub Release) | **3-Way Reconciled & Verified (`[E]` · `[GB]` · `[G4N]`):** 35 pp PDF, 56 refs, `228/228` + `20/20` audits, `33/33` Lean 4 theorems, Swift++ (`0.000e+00` delta), Rust (zero-PARI Manin $T_2$), PARI/GP |
| **02** | ***Working Paper 030 (Horizon Monograph I):*** *Shape-Controlled Gravitational Propulsion Resolved* (continuation of Working Paper 028) | [`wp030_shape_propulsion/`](wp030_shape_propulsion/) | **Cycle 1 Audited (`[G4N]`, Awaiting `[GB]`)** | **Frozen `[E]` baseline + 3-plane `[G4N]` audit:** Python `9/9`, Lean 4.36.0 `15/15` (`0 sorryAx`), Rust `7/7` (bit-exact `SplitMix64` parity), [`GEMINI4_NEON_WP030_AUDIT.md`](wp030_shape_propulsion/reconciliation/GEMINI4_NEON_WP030_AUDIT.md) (core `H1–H4` confirmed; 8 catches `NEG-W1`–`NEG-W6` + Theorem G1); awaiting independent **Grok Bot** (`[GB]`) pass |
| **03** | ***Working Paper 032 (Horizon Monograph IC):*** *Bennu-Class Triaxial Proximity Ops, 3D Multi-Tether FEM/FDIR & Extended-Body 3-Body Problem* *(WP 031 / Horizon IB not yet archived)* | [`wp032_bennu_3body/`](wp032_bennu_3body/) | **Cycle 1 Audited (`[G4N]`, Awaiting `[GB]`)** | **Frozen `[E]` baseline + 3-plane `[G4N]` audit:** Python `6/6`, Lean 4.36.0 `9/9` (`0 sorryAx`), Rust `5/5` (`SplitMix64` `0x55a32a121430eb49`), [`GEMINI4_NEON_WP032_AUDIT.md`](wp032_bennu_3body/reconciliation/GEMINI4_NEON_WP032_AUDIT.md) (4 catches `NEG-W7`–`NEG-W10` + Theorem G2); awaiting `[GB]` pass |
| **04** | ***Working Paper 033 (Horizon Monograph ID):*** *3D Non-Planar CRTBP Halo/Lissajous Manifolds, Rotating-Symplectic Floquet Control & Bennu TAG Guidance* | [`wp033_halo_tag_guidance/`](wp033_halo_tag_guidance/) | **Cycle 1 Audited (`[G4N]`, Awaiting `[GB]`)** | **Frozen `[E]` baseline + 3-plane `[G4N]` audit:** Python `4/4`, Lean 4.36.0 `7/7` (`0 sorryAx`, $6\times 6$ $\Omega = S^T J S$), Rust `4/4` (bit-exact `SplitMix64` `0xda9392ed940a41ee`), [`GEMINI4_NEON_WP033_AUDIT.md`](wp033_halo_tag_guidance/reconciliation/GEMINI4_NEON_WP033_AUDIT.md) (4 catches `NEG-W11`–`NEG-W14` + Theorem G3); awaiting `[GB]` pass |

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
