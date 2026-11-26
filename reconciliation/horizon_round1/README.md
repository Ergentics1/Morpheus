# Horizon Series — Grok Bot (`[GB]`) Round-1 Reconciliation (WP030–WP035)

Round 1 of the `[GB]` pass on the six Horizon working papers, using the same ADPIE method as the Morpheus `v0.2.0` and round-2/3 reconciliations. Work order: WP030, WP034, WP035, WP031, WP032, WP033.

| Path | Model | What it is |
| :--- | :--- | :--- |
| [`code/gb_r1_wp030.py`](code/gb_r1_wp030.py) | Code (MIT) | WP030 checks: Hopf chart, collisions, holonomy sign, Theorem G1, rounding order, tensions, Bennu, F35 |
| [`code/gb_r1_wp031_035.py`](code/gb_r1_wp031_035.py) | Code (MIT) | WP031–WP035 checks, incl. 106-bit emulation, Sen (2013) cross-check, 106/45 vs 167/90, ζ′ ratios, J2 baseline |
| [`code/gb_r1_wp033_halo.py`](code/gb_r1_wp033_halo.py) | Code (MIT) | Independent WP033 halo re-run: 42-ODE STM, monodromy, Broucke indices, both W^u branches |
| [`logs/`](logs/) | Data (CC BY 4.0) | Output of the three scripts as committed |
| [`build_r1.py`](build_r1.py), [`r1_items.py`](r1_items.py), [`r1_specs.py`](r1_specs.py) | Code (MIT) | Builds `papers/<slug>/paper/paper.typ` (clean-room text unchanged plus boxed `[GB]` notes) and the per-paper `GROKBOT_WP0xx_ROUND1.md` dossiers from one verdict ledger |
| [`RECONCILIATION_CHANGELOG.md`](RECONCILIATION_CHANGELOG.md) | Docs | What was checked, per-item verdict table, open author decisions |

The checks were written from scratch and do not read `[G4N]` code or data. `[G4N]`'s planes were re-run separately (Python, Rust, and Lean 4.36.0 via elan: 58/58 theorems, 0 `sorry`).

```bash
pip install -r requirements.txt typst            # numpy, scipy, sympy, mpmath; typst for the PDFs
python3 reconciliation/horizon_round1/code/gb_r1_wp030.py
python3 reconciliation/horizon_round1/code/gb_r1_wp031_035.py
python3 reconciliation/horizon_round1/code/gb_r1_wp033_halo.py
python3 reconciliation/horizon_round1/build_r1.py .   # regenerate editions + dossiers
for d in papers/wp03*/paper; do (cd "$d" && python3 -c "import typst; typst.compile('paper.typ', output='paper.pdf', root='.')"); done
```

Rules followed: the frozen `cleanroom/` folders are untouched (Rule 5); claims attributed to the Ergentics internal model are never altered and are marked UNVERIFIABLE where they can't be checked from this repository; all corrections are proposals for the author.
