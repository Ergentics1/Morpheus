# Morpheus Multi-Paper Research Registry (`papers/`)

**Morpheus** (*Open Sourced Living*, by **Ergentics**) houses multiple open-source research programs under a uniform **ADPIE**, **Code-vs-Data**, and **symmetric multi-model cross-verification** standard (`[E]`, `[GB]`, `[G4N]`, `[X]`). See [`../METHODOLOGY.md`](../METHODOLOGY.md), [`../POLICY.md`](../POLICY.md), and [`../AGENTS.md`](../AGENTS.md).

## Research Portfolio

| # | Paper / Program | Location | Stage | Verification Status |
| :---: | :--- | :--- | :--- | :--- |
| **01** | ***Prime Cadences:*** *Ihara zeta, graphene, and voice-leading homology on the Tonnetz* | Root layout ([`paper/`](../paper/), [`prime_cadences_paper.md`](../prime_cadences_paper.md), [`cleanroom/prime_cadences_resolution/`](../cleanroom/prime_cadences_resolution/)) | **`v0.3.1` Released** (Immutable GitHub Release) | **3-Way Reconciled & Verified (`[E]` · `[GB]` · `[G4N]`):** 35 pp PDF, 56 refs, `228/228` + `20/20` audits, `33/33` Lean 4 theorems, Swift++ (`0.000e+00` delta), Rust (zero-PARI Manin $T_2$), PARI/GP |
| **02** | ***Working Paper 030 (Horizon Monograph I):*** *Shape-Controlled Gravitational Propulsion Resolved* (continuation of Working Paper 028) | [`wp030_shape_propulsion/`](wp030_shape_propulsion/) | **Intake (`Pre-Assessment`)** | **Verbatim clean-room archive (`[E]`):** `cleanroom/paper.typ` + 4 SVG figures archived unmodified (`0` paths/URLs/credentials); awaiting independent assessment by **Gemini 4 Neon** (`[G4N]`) & **Grok Bot** (`[GB]`) |

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
