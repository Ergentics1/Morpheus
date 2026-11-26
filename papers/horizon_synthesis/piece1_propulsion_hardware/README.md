# Horizon Synthesis — Piece I: Shape-Controlled Gravitational Propulsion & Mechanical-Hub Hardware Sizing

Synthesizes and reconciles frozen clean-room working papers [`WP 030`](../../wp030_shape_propulsion/) and [`WP 031`](../../wp031_3d_j2_hil/) under unified physical conventions (WGS84 $R_\oplus = 6{,}378.137\text{ km}$, equilateral-pole Hopf basis $w_\pm$, canonical collinear polar inertia $I_0 = \frac23 M L^2$, and mechanical spring-drum hub flight baseline).

## Files

| Path | Role |
|---|---|
| [`paper/piece1_propulsion_hardware.tex`](paper/piece1_propulsion_hardware.tex) | Canonical AMS `LaTeX` source (`0` warnings, `0` overfull hboxes) |
| [`paper/references.bib`](paper/references.bib) / [`paper/piece1_propulsion_hardware.bbl`](paper/piece1_propulsion_hardware.bbl) | Verified BibTeX bibliography (retaining NASA NTRS `19910012850`) |
| [`paper/piece1_propulsion_hardware.pdf`](paper/piece1_propulsion_hardware.pdf) | Compiled monograph PDF with 3 embedded vector figures (`0` local path leaks) |
| [`arxiv/piece1-propulsion-hardware-arxiv.tar.gz`](arxiv/piece1-propulsion-hardware-arxiv.tar.gz) | Neutral `0/0` arXiv source bundle (standalone `pdflatex`-verified) |
| [`piece1_propulsion_hardware.md`](piece1_propulsion_hardware.md) | 1-to-1 reconciled GitHub Flavored Markdown mirror |
| [`code/piece1_sim.py`](code/piece1_sim.py) | Open, zero-dependency Python 3.12 simulator (`7/7` D/R/P gates + vector figure generator) |
| [`data/piece1_calibration.json`](data/piece1_calibration.json) | Live-emitted calibration table (`MANIFEST.sha256` verified) |

## Reproducibility

```bash
python3 papers/horizon_synthesis/piece1_propulsion_hardware/code/piece1_sim.py
sha256sum -c papers/horizon_synthesis/piece1_propulsion_hardware/data/MANIFEST.sha256
```

## Resolved Audit Items

Resolves `NEG-W1`–`NEG-W6`, `NEG-W15`–`NEG-W18`, `NEG-W25`–`NEG-W27`, and `NEG-W29` in place; proves **Theorem G1** (Hopf kinetic-energy wall) and **Theorem G4** ($I_0$-invariant `9.85×` electrical heat floor & `22.4×` mechanical-hub bypass). Internal `Swift++` (*Epsilon*) ledgers `INT-030` and `INT-031` are preserved in Appendix A.
