# Working Paper 032 — Bennu-Class Triaxial Proximity Ops, 3D Multi-Tether FEM/FDIR & Extended-Body Three-Body Problem

**Series:** Ergentics Working Paper 032 · Horizon Series Monograph IC · Extension of Working Papers 030 & 031 (Horizons I & IB)  
**Author:** Ergentics, LLC & Swift++ Library of Alexandria Verification Program (`[E]`)  
**Date:** 26 November 2026  
**Lifecycle Stage:** **`Cycle 1 Audited [G4N] — Awaiting [GB] Independent Pass`** — verbatim clean-room `[E]` archive frozen unmodified under `cleanroom/`; full **Gemini 4 Neon** (`[G4N]` / `[E→G4N]`) 3-plane independent audit & **Theorem G2** landed in [`reconciliation/GEMINI4_NEON_WP032_AUDIT.md`](reconciliation/GEMINI4_NEON_WP032_AUDIT.md). *(Note: Working Paper 031 / Horizon IB has not yet been uploaded into `papers/`.)*

---

## Verbatim Clean-Room Archive (`cleanroom/` — Frozen per Rule 5)

| File | Role | Size | SHA-256 | Hygiene Scan | License |
| :--- | :--- | ---: | :--- | :--- | :--- |
| [`cleanroom/paper.typ`](cleanroom/paper.typ) | Verbatim Typst source (*Working Paper 032 / Horizon Monograph IC*) | `39,331 B` (327 lines) | `c2fe46dbf0ee42c714926fae71ec9811d95389074e27c5e0c829809b6a9b89dd` | `0` paths · `0` URLs · `0` emails · `0` credentials | MIT |
| [`cleanroom/figures/fig1_bennu_triaxial_srp_jacobi.svg`](cleanroom/figures/fig1_bennu_triaxial_srp_jacobi.svg) | Figure 1: Bennu triaxial proximity, SRP crossover & Jacobi breaking | `8,831 B` | `4ac4a780b2d9a80a60ac932deedd7306fce35a8c9eb72910cd606d6bc6127f60` | `0` leaks | MIT |
| [`cleanroom/figures/fig2_3d_fem_and_fdir_jam.svg`](cleanroom/figures/fig2_3d_fem_and_fdir_jam.svg) | Figure 2: 16-node 3D multi-tether FEM & winch-jam FDIR | `15,701 B` | `f7fa08bb1a473ca21d8755cc3ba24313c85332a95ac025be35a01905e4aee81d` | `0` leaks | MIT |
| [`cleanroom/figures/fig3_crtbp_routh_k10_stabilization.svg`](cleanroom/figures/fig3_crtbp_routh_k10_stabilization.svg) | Figure 3: Extended-body CRTBP $L_4/L_5$ Routh stabilization (`K10`) | `12,864 B` | `6bc7df959282ae8b0933cf9f3ca7ef81d3b96c0791e8b854f5af67ef0b37cc32` | `0` leaks | MIT |
| [`cleanroom/figures/fig4_general_3body_choreo_vs_chaos.svg`](cleanroom/figures/fig4_general_3body_choreo_vs_chaos.svg) | Figure 4: Yoshida-4 Figure-8 choreography vs. Gascheau chaos | `13,513 B` | `d67aef2852ef874e4bf0a2794e87c75dfe725415bb82ab2d4dbbf3db5f91c249` | `0` leaks | MIT |

---

## Independent Verification Planes (`[G4N]` ADPIE Cycle 1)

| Plane | Path | Status | Verification Command (from repo root) |
| :--- | :--- | :--- | :--- |
| **1 — Zero-Dep Python 3.12** | [`code/wp032_audit.py`](code/wp032_audit.py) | **`6/6` PASS** (`C145`–`C148`, `K10`, `F37`, Bennu 4-level RK4, 16-node FEM/FDIR, Yoshida-4, `N=1,600` RCT) | `python3 papers/wp032_bennu_3body/code/wp032_audit.py` |
| **2 — Zero-Mathlib Lean 4.36.0** | [`lean/WP032/Theorems.lean`](lean/WP032/Theorems.lean) | **`9/9` PASS** (`0 sorryAx`, `0 ofReduceBool`, `0` warnings; 6 axiom-free) | `lake -d papers/wp032_bennu_3body/lean build && papers/wp032_bennu_3body/lean/.lake/build/bin/wp032-lean` |
| **3 — Zero-Crate Rust 1.100.0** | [`rust/src/lib.rs`](rust/src/lib.rs) · [`rust/tests/wp032_xcheck.rs`](rust/tests/wp032_xcheck.rs) | **`5/5` PASS** (`0.06 s`, bit-exact `SplitMix64` seam `0x55a32a121430eb49`) | `cargo test --manifest-path papers/wp032_bennu_3body/rust/Cargo.toml` |
| **Data Model (CC BY 4.0)** | [`data/wp032_g4n_cycle1_calibration.json`](data/wp032_g4n_cycle1_calibration.json) · [`data/MANIFEST.sha256`](data/MANIFEST.sha256) | **`1/1` SHA-256 OK** | `sha256sum -c papers/wp032_bennu_3body/data/MANIFEST.sha256` |
| **Audit & Novelty Dossier** | [`reconciliation/GEMINI4_NEON_WP032_AUDIT.md`](reconciliation/GEMINI4_NEON_WP032_AUDIT.md) | **Complete (`[G4N]`)** — 4 catches (`NEG-W7`–`NEG-W10`) + **Theorem G2** | — |
