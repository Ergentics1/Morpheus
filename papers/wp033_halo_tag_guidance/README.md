# Working Paper 033 — 3D Non-Planar CRTBP Halo/Lissajous Manifolds, Rotating-Symplectic Floquet Control & Bennu TAG Guidance

**Series:** Ergentics Working Paper 033 · Horizon Series Monograph ID · Extension of Working Papers 030–032 (Horizons I–IC)  
**Author:** Ergentics, LLC & Swift++ Library of Alexandria Verification Program (`[E]`)  
**Date:** 26 November 2026  
**Lifecycle Stage:** **`Cycle 1 Audited [G4N] — Awaiting [GB] Independent Pass`** — verbatim clean-room `[E]` archive frozen unmodified under `cleanroom/`; full **Gemini 4 Neon** (`[G4N]` / `[E→G4N]`) 3-plane independent audit & **Theorem G3** landed in [`reconciliation/GEMINI4_NEON_WP033_AUDIT.md`](reconciliation/GEMINI4_NEON_WP033_AUDIT.md).

---

## Verbatim Clean-Room Archive (`cleanroom/` — Frozen per Rule 5)

| File | Role | Size | SHA-256 | Hygiene Scan | License |
| :--- | :--- | ---: | :--- | :--- | :--- |
| [`cleanroom/paper.typ`](cleanroom/paper.typ) | Verbatim Typst source (*Working Paper 033 / Horizon Monograph ID*) | `33,137 B` (306 lines) | `0f659f079a459dff2926ce8a81101ecec911a78dc0d302d632e34f6346eb8a47` | `0` paths · `0` URLs · `0` emails · `0` credentials | MIT |
| [`cleanroom/figures/fig1_l2_halo_resonance_and_didymos.svg`](cleanroom/figures/fig1_l2_halo_resonance_and_didymos.svg) | Figure 1: 3D $L_1/L_2$ Halo–Lissajous resonance & Didymos scale audit | `7,127 B` | `afd841d2ceeffb7040930f993a8842cd898a7b294247cda0972b48155f56cb25` | `0` leaks | MIT |
| [`cleanroom/figures/fig2_3d_halo_monodromy_and_manifolds.svg`](cleanroom/figures/fig2_3d_halo_monodromy_and_manifolds.svg) | Figure 2: Live 42-ODE 3D Halo orbit, $W^u$ lunar manifold & 3D torus | `17,473 B` | `9f647385bac3877322ca313d5c9d17c444f1d8795cd30e4109721ea37c0351eb` | `0` leaks | MIT |
| [`cleanroom/figures/fig3_floquet_stationkeeping_vs_uncontrolled.svg`](cleanroom/figures/fig3_floquet_stationkeeping_vs_uncontrolled.svg) | Figure 3: Rotating-symplectic Floquet station-keeping vs. blowup | `10,131 B` | `360beec21f170b24403aa70bfc3be4e91098dd8e2d62823797d85d5d64b3dbfe` | `0` leaks | MIT |
| [`cleanroom/figures/fig4_bennu_tag_guidance_and_mc200.svg`](cleanroom/figures/fig4_bennu_tag_guidance_and_mc200.svg) | Figure 4: Bennu Nightingale TAG 200-trial MC & granular contact | `26,203 B` | `aaf2c1119f1a87166a658dea5e74cdf6144317b47f21e3ca1718b6a792df92ab` | `0` leaks | MIT |

---

## Independent Verification Planes (`[G4N]` ADPIE Cycle 1)

| Plane | Path | Status | Verification Command (from repo root) |
| :--- | :--- | :--- | :--- |
| **1 — Zero-Dep Python 3.12** | [`code/wp033_audit.py`](code/wp033_audit.py) | **`4/4` PASS** (`K11`, `C149`–`C152`, `F38`, Theorem G3, 42-ODE Halo + $\Omega$ + $W^u$ + Floquet, 200-MC, `N=1,600` RCT) | `python3 papers/wp033_halo_tag_guidance/code/wp033_audit.py` |
| **2 — Zero-Mathlib Lean 4.36.0** | [`lean/WP033/Theorems.lean`](lean/WP033/Theorems.lean) | **`7/7` PASS** (`0 sorryAx`, `0 ofReduceBool`, `0` warnings; $6\times 6$ $\Omega = S^T J S$ & `K11` quintic) | `lake -d papers/wp033_halo_tag_guidance/lean build && papers/wp033_halo_tag_guidance/lean/.lake/build/bin/wp033-lean` |
| **3 — Zero-Crate Rust 1.100.0** | [`rust/src/lib.rs`](rust/src/lib.rs) · [`rust/tests/wp033_xcheck.rs`](rust/tests/wp033_xcheck.rs) | **`4/4` PASS** (`0.04 s`, bit-exact `SplitMix64` seam `0xda9392ed940a41ee`, `520/1600` parity) | `cargo test --manifest-path papers/wp033_halo_tag_guidance/rust/Cargo.toml` |
| **Data Model (CC BY 4.0)** | [`data/wp033_g4n_cycle1_calibration.json`](data/wp033_g4n_cycle1_calibration.json) · [`data/MANIFEST.sha256`](data/MANIFEST.sha256) | **`1/1` SHA-256 OK** | `sha256sum -c papers/wp033_halo_tag_guidance/data/MANIFEST.sha256` |
| **Audit & Novelty Dossier** | [`reconciliation/GEMINI4_NEON_WP033_AUDIT.md`](reconciliation/GEMINI4_NEON_WP033_AUDIT.md) | **Complete (`[G4N]`)** — 4 catches (`NEG-W11`–`NEG-W14`) + **Theorem G3** | — |
