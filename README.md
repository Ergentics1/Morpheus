# Morpheus

Open-sourced research repository by **Ergentics**.

## Paper: *Prime Cadences*

**[Prime cadences: Ihara zeta, graphene, and voice-leading homology on the Tonnetz](prime_cadences_paper.md)** *(Preprint, November 2026)*

- **Read on GitHub:** [`prime_cadences_paper.md`](prime_cadences_paper.md)
- **Compiled PDF:** [`paper/prime-cadences.pdf`](paper/prime-cadences.pdf)
- **LaTeX & BibTeX source:** [`paper/prime-cadences.tex`](paper/prime-cadences.tex), [`paper/references.bib`](paper/references.bib)
- **arXiv bundle:** [`arxiv/prime-cadences-arxiv.tar.gz`](arxiv/prime-cadences-arxiv.tar.gz)

Studies the 3-regular neo-Riemannian triad graph $X$ and its Ihara zeta primes (*prime cadences*), linking the Tonnetz to the honeycomb/graphene tight-binding spectrum, Weil polynomials over $\mathbb{F}_2$, the tune theorem and its generalisation, voice-leading homology, a genus-13 2-adic Mumford curve, minimal genus-5 binary curves, and 2-adic arithmetic obstructions.

> **Status:** Complete baseline package imported and reconciled across LaTeX, Markdown, figures, code, and upstream audit reports (176/176 checks recorded in [`audits/`](audits/README.md)). Independent cross-verification (`[X]`) and formal proofs (Lean 4 / Rust / C++ / Swift) have not yet been recorded; see [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md) and [`PROVENANCE.md`](PROVENANCE.md).

## Repository Layout

| Path | Description |
| :--- | :--- |
| [`paper/`](paper/) | Canonical LaTeX source (`prime-cadences.tex`), `.bbl`, compiled PDF, `references.bib`, and 8 vector PDF figures |
| [`prime_cadences_paper.md`](prime_cadences_paper.md) | GitHub Flavored Markdown mirror reconciled with `paper/prime-cadences.tex` |
| [`figures/`](figures/README.md) | PNG figures 1–5 for `prime_cadences_paper.md` |
| [`arxiv/`](arxiv/) | Ready-to-upload arXiv source tarball (`prime-cadences-arxiv.tar.gz`) |
| [`code/`](code/) | Python scripts and JSON artifacts for computations, audits, and figure generation |
| [`audits/`](audits/README.md) | Recorded reports from the five audit suites (31, 36, 23, 59, and 27 checks) |
| [`Makefile`](Makefile) & [`requirements.txt`](requirements.txt) | Build targets (`pdf`, `arxiv`, `audit`, `figures`) and pinned Python dependencies |
| [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md) | Author/AI contribution tags (`[GB]`, `[E]`, `[E→GB]`, `[lit.]`, `[X]`) and cross-verification ledger |
| [`PROVENANCE.md`](PROVENANCE.md) | Origin, AI-assistance disclosure, SHA-256 checksums, and reconciliation log |
| [`CITATION.cff`](CITATION.cff) | Machine-readable citation metadata (CFF 1.2.0) |
| [`POLICY.md`](POLICY.md) | Research integrity, AI provenance, licensing, and hygiene policy |
| [`SECURITY.md`](SECURITY.md) | Vulnerability reporting and secret/path-leak security policy |
| [`AGENTS.md`](AGENTS.md) | Rules for automated and AI agents working in this repository |
| [`LICENSE`](LICENSE), [`LICENSE-paper`](LICENSE-paper), [`LICENSES/`](LICENSES/) | Dual license: MIT (code) and CC BY 4.0 (paper, figures, docs) |

## Reproducing Audits and Figures

Install the pinned Python dependencies from [`requirements.txt`](requirements.txt), then use [`Makefile`](Makefile):

```bash
make audit    # run all 5 computational audit scripts in code/
make figures  # regenerate vector PDFs in paper/figures/
make pdf      # compile paper/prime-cadences.pdf (requires LaTeX + latexmk)
make arxiv    # build arxiv/prime-cadences-arxiv.tar.gz
```

## Citation

GitHub reads [`CITATION.cff`](CITATION.cff) for the **Cite this repository** menu. BibTeX:

```bibtex
@article{ergentics2026primecadences,
  author  = {Ergentics},
  title   = {Prime cadences: Ihara zeta, graphene, and voice-leading homology on the Tonnetz},
  year    = {2026},
  month   = nov,
  note    = {Preprint}
}
```

## Licensing & Governance

- **Code (`code/`, `Makefile`):** [MIT License](LICENSE) ([`LICENSES/MIT.txt`](LICENSES/MIT.txt))
- **Paper, figures, audits, and documentation:** [CC BY 4.0](LICENSE-paper) ([`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt))
- **Governance:** [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md) · [`PROVENANCE.md`](PROVENANCE.md) · [`POLICY.md`](POLICY.md) · [`SECURITY.md`](SECURITY.md)
