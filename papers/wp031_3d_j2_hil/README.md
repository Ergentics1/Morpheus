# Paper #05 — Ergentics Working Paper 031 (Horizon Monograph IB)

**Title:** *3D Non-Planar $J_2$ Symmetry Breaking, Collinear-Bridge $\mathrm{SO}(3)$ Holonomy, Safe-Perigee Optimal Eccentricity, and Hardware-in-the-Loop Actuator Sizing for Shape-Controlled Gravitational Propulsion*  
**Author:** Ergentics (`[E]`) · **Series Position:** Bridges Paper #02 ([WP 030 / Horizon I](../wp030_shape_propulsion/)) to Papers #03–#04 ([WP 032 / Horizon IC](../wp032_bennu_3body/) & [WP 033 / Horizon ID](../wp033_halo_tag_guidance/))

## Directory Layout (Code vs. Data Strictly Separated)

- [`cleanroom/`](cleanroom/) — Frozen verbatim intake (`paper.typ` + `fig1`–`fig4.svg`, preserved byte-for-byte unmodified per Rule 5).
- [`reconciliation/GEMINI4_NEON_WP031_AUDIT.md`](reconciliation/GEMINI4_NEON_WP031_AUDIT.md) — **Gemini 4 Neon (`[G4N]`) ADPIE Cycle 1** independent three-plane audit dossier, original **Theorem G4** (Spin-Tensioned Hopf Harmonic-Tension & Thermodynamic Heat-Barrier Theorem), `NEG-W15`–`NEG-W18`, and Grok Bot (`[GB]`) cross-check checklist.
- [`code/wp031_audit.py`](code/wp031_audit.py) — **Plane 1:** Zero-dependency Python 3.12 independent verifier (`5/5` PASS, live 5-orbit 3D $J_2$ RK4 point-mass baseline, `K9`, `C141`–`C144`, `F36`, Theorem G4 quadrature, and keyed `SplitMix64` 1,600-trial RCT).
- [`data/`](data/) — CC BY 4.0 checksummed calibration output (`wp031_g4n_cycle1_calibration.json` + `MANIFEST.sha256`).
- [`lean/`](lean/) — **Plane 2:** Zero-Mathlib Lean 4.36.0 kernel-checked algebraic oracle (`9/9` theorems, `0 sorryAx`, `0 ofReduceBool`).
- [`rust/`](rust/) — **Plane 3:** Zero-crate Rust 1.100.0 cross-verifier (`5/5` PASS, bit-exact `SplitMix64` seam parity `0xc844f9d684ec259c`, Arm B `1600/1600` vs. Arm A `592/1600`).

## Reproducibility Commands

```bash
python3 papers/wp031_3d_j2_hil/code/wp031_audit.py
sha256sum -c papers/wp031_3d_j2_hil/data/MANIFEST.sha256
cargo test --manifest-path papers/wp031_3d_j2_hil/rust/Cargo.toml
lake -d papers/wp031_3d_j2_hil/lean build && papers/wp031_3d_j2_hil/lean/.lake/build/bin/wp031-lean
```
