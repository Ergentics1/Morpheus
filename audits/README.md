# Audits

Recorded outputs of the five computational audit scripts in [`code/`](../code/) (176/176 checks passed in the upstream Grok Bot runs). See [`CONTRIBUTIONS.md`](../CONTRIBUTIONS.md) and [`PROVENANCE.md`](../PROVENANCE.md) for provenance and cross-verification status.

| Report | Script | Checks | Scope |
| :--- | :--- | ---: | :--- |
| [`core_audit.md`](core_audit.md) | `code/math_audit.py` | 31/31 | Chord graph, spectrum, Ihara–Bass, exact prime counts, 12/31/53-EDO |
| [`spectrum_audit.md`](spectrum_audit.md) | `code/deep/audit.py` | 36/36 | $D_{12}$ / Coxeter group, Artin–Ihara, tune theorem, winding CLT, flux window, graphene |
| [`arithmetic_audit.md`](arithmetic_audit.md) | `code/eisenstein2/audit.py` | 23/23 | Cyclotomic Fourier coefficients, Weil factors, LMFDB curves, conductor-2 order |
| [`geometry_audit.md`](geometry_audit.md) | `code/geometry/audit.py` | 59/59 | Schottky group, $\mathbb{Z}/12$ tower, sandpile group, gonality, $\mathbb{F}_2$ curves, $\mathbb{Q}$ Shimura exclusion |
| [`open_questions_audit.md`](open_questions_audit.md) | `code/open_q/open_audit.py` | 27/27 | Trace obstruction, edge lengths, mass scan, genus-5 curves over $\mathbb{F}_2$, general tune theorem, citations |

To re-run all five audit scripts locally after installing [`requirements.txt`](../requirements.txt):

```bash
make audit
```
