# Horizon Synthesis — Piece II: Small-Body Triaxial Proximity, Extended-Body CRTBP, and Bennu TAG Guidance

Synthesizes and reconciles frozen clean-room working papers [`WP 032`](../../wp032_bennu_3body/) and [`WP 033`](../../wp033_halo_tag_guidance/) with open 42-ODE Halo/manifold/Floquet integrators, symplectic Figure-8 choreography, and fluidized Bennu TAG Monte Carlo guidance.

## Files

| Path | Role |
|---|---|
| [`paper/piece2_smallbody_crtbp.tex`](paper/piece2_smallbody_crtbp.tex) | Canonical AMS `LaTeX` source (`0` warnings, `0` overfull hboxes) |
| [`paper/references.bib`](paper/references.bib) / [`paper/piece2_smallbody_crtbp.bbl`](paper/piece2_smallbody_crtbp.bbl) | Verified BibTeX bibliography |
| [`paper/piece2_smallbody_crtbp.pdf`](paper/piece2_smallbody_crtbp.pdf) | Compiled monograph PDF with 3 embedded vector figures (`0` local path leaks) |
| [`arxiv/piece2-smallbody-crtbp-arxiv.tar.gz`](arxiv/piece2-smallbody-crtbp-arxiv.tar.gz) | Neutral `0/0` arXiv source bundle (standalone `pdflatex`-verified) |
| [`piece2_smallbody_crtbp.md`](piece2_smallbody_crtbp.md) | 1-to-1 reconciled GitHub Flavored Markdown mirror |
| [`code/piece2_sim.py`](code/piece2_sim.py) | Open, zero-dependency Python 3.12 simulator (`6/6` D/R/P gates + vector figure generator) |
| [`data/piece2_calibration.json`](data/piece2_calibration.json) | Live-emitted calibration table (`MANIFEST.sha256` verified) |

## Reproducibility

```bash
python3 papers/horizon_synthesis/piece2_smallbody_crtbp/code/piece2_sim.py
sha256sum -c papers/horizon_synthesis/piece2_smallbody_crtbp/data/MANIFEST.sha256
```

## Resolved Audit Items

Resolves `NEG-W7`–`NEG-W14` and `NEG-W29` in place; proves **Theorem G2** (exact 3-arm+hub FDIR tension inversion) and **Theorem G3** (coupled 3D $L_2$ multipole tensor & Didymos $L_y^* = 40.44\text{ m}$), and discovers an elevated non-impacting lunar-capture $W^u$ branch ($\tau = 0.750 \to r_p = 2{,}064.6\text{ km}$, `+327.2 km` altitude) with `8,814×` Floquet station-keeping suppression. Internal `Swift++` (*Epsilon*) ledgers `INT-032` and `INT-033` are preserved in Appendix A.
