# Paper #06 — Ergentics Working Paper 034 (Horizon Monograph IE)

**Title:** *Independent Precision Audit and Structural Pressure Test of Algebraic Null-Cone Quantum Gravity (`arXiv:2611.34924v1`)*  
**Author:** Ergentics (`[E]`) · **External Target:** V. Chandrasekaran (Stanford University), *An algebraic quantization of gravity from the null cone*, `arXiv:2611.34924v1` (Nov. 23, 2026)

## Directory Layout (Code vs. Data Strictly Separated)

- [`cleanroom/`](cleanroom/) — Frozen verbatim intake (`paper.typ` + `fig1`–`fig4.svg`, preserved byte-for-byte unmodified per Rule 5).
- [`reconciliation/GEMINI4_NEON_WP034_AUDIT.md`](reconciliation/GEMINI4_NEON_WP034_AUDIT.md) — **Gemini 4 Neon (`[G4N]`) ADPIE Cycle 1** independent three-plane meta-audit dossier, original **Theorem G5** (Non-Hilbert–Schmidt Closed-Cut Riemann Rearrangement Universality), `NEG-W19`–`NEG-W21`, primary-source Sen (2013) cross-check, and Grok Bot (`[GB]`) checklist.
- [`code/wp034_audit.py`](code/wp034_audit.py) — **Plane 1:** Zero-dependency Python 3.12 independent verifier (`5/5` PASS, authentic 106-bit Dekker–Knuth DD EFT vs. cancellation-free `f64`, Theorem G5 constructive exhaustions, Sen 2013 rationals, Cauchy–Schlömilch & ER=EPR quadratures, `C153`–`C156`/`K12`/`F39`, and keyed `SplitMix64` 1,600-trial RCT).
- [`data/`](data/) — CC BY 4.0 checksummed calibration output (`wp034_g4n_cycle1_calibration.json` + `MANIFEST.sha256`).
- [`lean/`](lean/) — **Plane 2:** Zero-Mathlib Lean 4.36.0 kernel-checked algebraic oracle (`9/9` theorems, `0 sorryAx`, `0 ofReduceBool`, including Theorem G5 nesting and from-scratch irrationality of $\sqrt{2}$).
- [`rust/`](rust/) — **Plane 3:** Zero-crate Rust 1.100.0 cross-verifier (`5/5` PASS, FMA-backed 106-bit DD EFT, bit-exact `SplitMix64` seam parity `0xb4005f8bfe2e1bca`, Arm B `1600/1600` vs. Arm A `0/1600`).

## Reproducibility Commands

```bash
python3 papers/wp034_null_cone_gravity/code/wp034_audit.py
sha256sum -c papers/wp034_null_cone_gravity/data/MANIFEST.sha256
cargo test --manifest-path papers/wp034_null_cone_gravity/rust/Cargo.toml
lake -d papers/wp034_null_cone_gravity/lean build && papers/wp034_null_cone_gravity/lean/.lake/build/bin/wp034-lean
```
