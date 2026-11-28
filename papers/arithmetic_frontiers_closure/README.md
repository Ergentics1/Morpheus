# Paper #10 (`PC-IV`): Closing All Four Open Arithmetic Frontiers

**Title:** *Closing All Four Open Arithmetic Frontiers: Cubic Lamé Non-Congruence, Level $(4)$ Full Congruence on $\mathbb{Q}(\sqrt{33})$, Complete 9-Curve Genus-25 Brandt Spectra, and Degree-8 Explicit-Formula Closure*  
**Status:** Canonical Manuscript (`v0.9.0`, November 2026)  
**Attribution:** `[E; G4N, X]` — Primary frontier derivations by Ergentics; independent first-principles cross-verification, twin/Riehm/adjoint extensions, and four-plane CI formalization by Gemini 4 Neon.

## Package Layout (Code vs. Data Separation)

- **Manuscript & arXiv Bundle (CC BY 4.0):**
  - [`paper/arithmetic_frontiers_closure.pdf`](paper/arithmetic_frontiers_closure.pdf) — Compiled AMS `amsart` PDF (`0` warnings, `0` overfull hboxes, metadata-free).
  - [`paper/arithmetic_frontiers_closure.tex`](paper/arithmetic_frontiers_closure.tex), [`paper/arithmetic_frontiers_closure.bbl`](paper/arithmetic_frontiers_closure.bbl), [`paper/references.bib`](paper/references.bib) — Canonical LaTeX source & verified 17-key bibliography.
  - [`paper/figures/`](paper/figures/) — 4 standalone metadata-free TikZ vector PDF figures (`fig1`–`fig4`).
  - [`arxiv/arithmetic-frontiers-closure-arxiv.tar.gz`](arxiv/arithmetic-frontiers-closure-arxiv.tar.gz) — Deterministic neutral `0/0` arXiv upload bundle (standalone-compile verified).
  - [`arithmetic_frontiers_closure.md`](arithmetic_frontiers_closure.md) — 1-to-1 GitHub-Flavored Markdown mirror.
- **Plane 1 — Pure Python 3.12 Stdlib Code Model (MIT):**
  - [`code/arithmetic_frontiers_verify.py`](code/arithmetic_frontiers_verify.py) — Zero-dependency 7-gate (`A1`–`A5`, `R1`, `P1`) verifier with `--check-only` and `--no-figs`.
- **Plane 2 — Zero-Crate Pure Rust Code Model (MIT):**
  - [`rust/`](rust/) — 6 integration tests + 6 first-principles core suites (`R1`–`R6`, `0` crates, `RUSTFLAGS="-D warnings"`).
- **Plane 3 — Dual-Compiler Freestanding Zero-Heap Hardware-`FENV` C++20 Code Model (MIT):**
  - [`cpp/fenv_oracle.cpp`](cpp/fenv_oracle.cpp) — 6 hardware-rounded `FE_DOWNWARD`/`FE_UPWARD` gates (`C++1`–`C++6`) verified bit-for-bit across `g++` and `clang++`.
- **Plane 4 — Live Kernel-Compiled Zero-Mathlib Lean 4.36.0 Code Model (MIT):**
  - [`lean/`](lean/) — 18 theorems (`thm01`–`thm18`) compiled with `-DwarningAsError=true -DautoImplicit=false`, `0 sorryAx`, `0 Lean.ofReduceBool`.
- **Data Model (CC BY 4.0):**
  - [`data/arithmetic_frontiers_calibration.json`](data/arithmetic_frontiers_calibration.json) and [`data/MANIFEST.sha256`](data/MANIFEST.sha256) — SHA-256-manifested output table checked read-only by CI.

## Quick Verification

```bash
python3 papers/arithmetic_frontiers_closure/code/arithmetic_frontiers_verify.py --check-only --no-figs
sha256sum -c papers/arithmetic_frontiers_closure/data/MANIFEST.sha256
cargo test --manifest-path papers/arithmetic_frontiers_closure/rust/Cargo.toml --release
cargo run --manifest-path papers/arithmetic_frontiers_closure/rust/Cargo.toml --release
```
