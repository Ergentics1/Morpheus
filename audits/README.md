# Audits

Recorded outputs of the six computational audit scripts in [`code/`](../code/) (228/228 checks passed in the Grok Bot runs for v0.2.0). See [`CONTRIBUTIONS.md`](../CONTRIBUTIONS.md) and [`PROVENANCE.md`](../PROVENANCE.md) for provenance and cross-verification status.

| Report | Script | Checks | Scope |
| :--- | :--- | ---: | :--- |
| [`core_audit.md`](core_audit.md) | `code/math_audit.py` | 31/31 | Chord graph, spectrum, Ihara–Bass, exact prime counts, 12/31/53-EDO |
| [`spectrum_audit.md`](spectrum_audit.md) | `code/deep/audit.py` | 36/36 | $D_{12}$ / Coxeter group, Artin–Ihara, tune theorem, winding CLT, flux window, graphene |
| [`arithmetic_audit.md`](arithmetic_audit.md) | `code/eisenstein2/audit.py` | 23/23 | Cyclotomic Fourier coefficients, Weil factors, LMFDB curves, conductor-2 order |
| [`geometry_audit.md`](geometry_audit.md) | `code/geometry/audit.py` | 59/59 | Schottky group, $\mathbb{Z}/12$ tower, sandpile group, gonality, $\mathbb{F}_2$ curves, $\mathbb{Q}$ Shimura exclusion |
| [`open_questions_audit.md`](open_questions_audit.md) | `code/open_q/open_audit.py` | 47/47 | Trace obstruction, edge lengths, mass scan, Brandt graphs, any narrow class number, torsion structure, genus-5 curves over $\mathbb{F}_2$, general tune and held-note theorems, citations |
| [`xcheck_audit.md`](xcheck_audit.md) | `code/xcheck/audit_xcheck.py` | 32/32 | Grok Bot's from-scratch cross-check of the `[X]` results: held notes (Thm 4.4, Cor 4.5), higher cumulants (Thm 6.2, Prop 6.3), exact $m=40$ benchmarks, decoder count, Edgeworth calibration |

To re-run all six audit scripts locally after installing [`requirements.txt`](../requirements.txt):

```bash
make audit
```
