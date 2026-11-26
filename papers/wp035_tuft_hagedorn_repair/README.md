# Paper #07 — Ergentics Working Paper 035 (Horizon Monograph IF — Series Finale)

**Title:** *Independent Precision Audit of Hopf-Fibration Unified Field Theory (Nielsen 2026) and Non-Circular Hagedorn Nuclearity Repair of Algebraic Null-Cone Gravity*  
**Author:** Ergentics (`[E]`) · **Series Position:** Closes the Horizon I–IF monograph series (`WP 030`–`WP 035`), pairing a forensic audit of Nielsen (2026) TUFT (Track A) with an original constructive functional-analytic repair of Chandrasekaran (`arXiv:2611.34924v1`, Sec. 5.2) directly extending [Paper #06 / WP 034](../wp034_null_cone_gravity/) (Track B).

## Directory Layout (Code vs. Data Strictly Separated)

- [`cleanroom/`](cleanroom/) — Frozen verbatim intake (`paper.typ` + `fig1`–`fig4.svg`, preserved byte-for-byte unmodified per Rule 5).
- [`reconciliation/GEMINI4_NEON_WP035_AUDIT.md`](reconciliation/GEMINI4_NEON_WP035_AUDIT.md) — **Gemini 4 Neon (`[G4N]`) ADPIE Cycle 1** independent three-plane audit dossier, original **Theorem G6** (Hagedorn Canonical Equivalence-Breaking, Universal $O(1)$ Gamma Dispersion & WP 034 Truncation Bridge), `NEG-W22`–`NEG-W24`, and Grok Bot (`[GB]`) series-closing checklist.
- [`code/wp035_audit.py`](code/wp035_audit.py) — **Plane 1:** Zero-dependency Python 3.12 independent verifier (`5/5` PASS, 65-digit $S^3$–$S^9$ spectral zetas, `L(3,1)`, $a_5$, Wyler/CODATA, `C157`–`C160`/`K13`/`F40`, Beltrami ODE, Theorems R1–R3, Theorem G6, and keyed `SplitMix64` 1,600-trial RCT).
- [`data/`](data/) — CC BY 4.0 checksummed calibration output (`wp035_g4n_cycle1_calibration.json` + `MANIFEST.sha256`).
- [`lean/`](lean/) — **Plane 2:** Zero-Mathlib Lean 4.36.0 kernel-checked algebraic oracle (`9/9` theorems, `0 sorryAx`, `0 ofReduceBool`).
- [`rust/`](rust/) — **Plane 3:** Zero-crate Rust 1.100.0 cross-verifier (`5/5` PASS, from-scratch Stirling–Bernoulli `lgamma`/`digamma`, bit-exact `SplitMix64` seam parity `0xcc617ec51b6fb1e0`, Arm B `1600/1600` vs. Arm A `0/1600`).

## Reproducibility Commands

```bash
python3 papers/wp035_tuft_hagedorn_repair/code/wp035_audit.py
sha256sum -c papers/wp035_tuft_hagedorn_repair/data/MANIFEST.sha256
cargo test --manifest-path papers/wp035_tuft_hagedorn_repair/rust/Cargo.toml
lake -d papers/wp035_tuft_hagedorn_repair/lean build && papers/wp035_tuft_hagedorn_repair/lean/.lake/build/bin/wp035-lean
```
