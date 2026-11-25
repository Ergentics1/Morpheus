# Morpheus

Open-sourced research repository by **Ergentics**.

## Paper: *Prime Cadences*

**[Prime cadences: Ihara zeta, graphene, and voice-leading homology on the Tonnetz](prime_cadences_paper.md)** *(Preprint, November 2026)*

- **Read on GitHub:** [`prime_cadences_paper.md`](prime_cadences_paper.md)
- **Compiled PDF:** [`paper/prime-cadences.pdf`](paper/prime-cadences.pdf)
- **LaTeX & BibTeX source:** [`paper/prime-cadences.tex`](paper/prime-cadences.tex), [`paper/references.bib`](paper/references.bib)
- **arXiv bundle:** [`arxiv/prime-cadences-arxiv.tar.gz`](arxiv/prime-cadences-arxiv.tar.gz)

Studies the 3-regular neo-Riemannian triad graph $X$ and its Ihara zeta primes (*prime cadences*), linking the Tonnetz to the honeycomb/graphene tight-binding spectrum, Weil polynomials over $\mathbb{F}_2$, the tune theorem and its generalisation, voice-leading homology, a genus-13 2-adic Mumford curve, minimal genus-5 binary curves, and 2-adic arithmetic obstructions.

> **Status:** Baseline `v0.1.0` package (`paper/`, `code/`, `audits/`, `CONTRIBUTIONS.md`, `Makefile`) is archived unmodified. First-principles `[X]` verification and formal proofs are live across four independent languages (`lean/` Lean 4.36.0, `swiftpp/` C++20 × Pure Swift 6.4 × Interop, `rust/` Rust 1.100.0) with strict Code-vs-Data separation (`data/`), alongside audit-forward original mathematical novelties in [`NOVELTY_GEMINI4_NEON.md`](NOVELTY_GEMINI4_NEON.md). Manuscript `[X]` tags in `CONTRIBUTIONS.md` and `paper/` remain unchanged until author review.

## Repository Layout

| Path | Description |
| :--- | :--- |
| [`paper/`](paper/) | Canonical LaTeX source (`prime-cadences.tex`), `.bbl`, compiled PDF, `references.bib`, and 8 vector PDF figures |
| [`prime_cadences_paper.md`](prime_cadences_paper.md) | GitHub Flavored Markdown mirror reconciled with `paper/prime-cadences.tex` |
| [`figures/`](figures/README.md) | PNG figures 1–5 for `prime_cadences_paper.md` |
| [`arxiv/`](arxiv/) | Ready-to-upload arXiv source tarball (`prime-cadences-arxiv.tar.gz`) |
| [`NOVELTY_GEMINI4_NEON.md`](NOVELTY_GEMINI4_NEON.md) | Audit-forward original mathematical novelties (ADPIE Cycle 4): complete resolution of Open Problem (3) (Theorems A, B, Cor B.1, `NEG-M11`) & exact 2D Tonnetz 6th-order cumulant/Edgeworth theory (Theorem C, `C-2'`/`C-2''`) |
| [`reconciliation/`](reconciliation/README.md) | Grok Bot reconciliation packet ([`GEMINI4_NEON_RECONCILIATION.md`](reconciliation/GEMINI4_NEON_RECONCILIATION.md)): theorem-by-theorem `[X]` ledger, `NEG-E8` erratum, checkable novelty targets, Lean 4 axiom audit & reproduction commands |
| [`media/`](media/README.md) | Gemini 4 Neon videos: 1:24 social reel (`gemini4_neon_prime_cadences.mp4`), 4:18 **Spoken-in-Harmony Educator Masterclass** with live Chess & Graph RH (`gemini4_neon_masterclass_chess_rh.mp4`), poster PNG, social captions & MIT generators |
| [`lean/`](lean/) | Machine-checked Lean 4.36.0 formal proofs (zero Mathlib, 0 `sorryAx`, 0 `ofReduceBool`; constructive `[propext, Quot.sound]` / axiom-free across Cycles 2A + Thm B suff/`NEG-M11`/Thm C, standard Lean core `[propext, Classical.choice, Quot.sound]` for Thm A/Thm B nec/Cor B.1): `TriadGraph`, `TuneTheorem`, `ConductorTwo`, `WindingAndSchottky`, `NoveltyTheorems` |
| [`swiftpp/`](swiftpp/) | **Swift++** Triple-Check verification suite (`ErgenticsCXX` C++20 `g++`/`clang++` · `ErgenticsSwift` Pure Swift 6.4 · `ErgenticsInterop` live cross-check, `0.000e+00` delta) |
| [`rust/`](rust/) | Fourth-language exact verifier (Rust 1.100.0, zero external crates): $\mathbb{Z}[\zeta_{12}]$, Artin–Ihara tower, general $N$-EDO sweeps ($N \le 96$ & maximal $S_{\max}$ to $N \le 72$), and Theorem C cross-check |
| [`data/`](data/README.md) | Immutable, SHA-256-checksummed Data Model calibration records (`data/MANIFEST.sha256`, CC BY 4.0) |
| [`code/`](code/) | Upstream baseline Python scripts and co-located JSON outputs (retained unmodified as baseline; new `[X]` work separates Code and Data models per [`METHODOLOGY.md`](METHODOLOGY.md)) |
| [`audits/`](audits/README.md) | Recorded reports from the five audit suites (31, 36, 23, 59, and 27 checks) |
| [`Makefile`](Makefile) & [`requirements.txt`](requirements.txt) | Build targets (`pdf`, `arxiv`, `audit`, `figures`) and pinned Python dependencies |
| [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md) | Author/AI contribution tags (`[GB]`, `[E]`, `[E→GB]`, `[lit.]`, `[X]`) and cross-verification ledger |
| [`METHODOLOGY.md`](METHODOLOGY.md) | Core Thesis (Correspondence Principle), Code-vs-Data non-conflation, ADPIE, and D/R/P/Seam SWE-sweep standard |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Four-plane Code-vs-Data architecture, `D ↔ R ↔ P` seams, and multi-language layout blueprint |
| [`CALIBRATIONS.md`](CALIBRATIONS.md) | Correspondence error-bound ledger (`C-1`–`C-4`, `C-2'`, `C-2''`), Rung-1 calibration metrics, RCT protocol, and output schema |
| [`ERGENTICS.md`](ERGENTICS.md) | Ergentics core library (`ergentics/`) and **Swift++** Triple-Check spec (`swiftpp/`: Pure C++20 · Pure Swift · Swift↔C++ interop) |
| [`NEGATIVES.md`](NEGATIVES.md) | Permanent ledger of refuted claims (`NEG-M1`–`NEG-M11`, `NEG-E1`–`NEG-E9`), obstructions, negative controls, and engineering traps |
| [`PROVENANCE.md`](PROVENANCE.md) | Origin, AI-assistance disclosure, SHA-256 checksums, and revision log |
| [`CHANGELOG.md`](CHANGELOG.md) | Versioned release and `[Unreleased]` verification/novelty changelog |
| [`CITATION.cff`](CITATION.cff) | Machine-readable citation metadata (CFF 1.2.0) |
| [`POLICY.md`](POLICY.md) | Research integrity, AI provenance, licensing, and hygiene policy |
| [`SECURITY.md`](SECURITY.md) | Vulnerability reporting and secret/path-leak security policy |
| [`AGENTS.md`](AGENTS.md) | Rules for automated and AI agents working in this repository |
| [`LICENSE`](LICENSE), [`LICENSE-paper`](LICENSE-paper), [`LICENSES/`](LICENSES/) | Dual license: MIT (Code Model) and CC BY 4.0 (Paper & Data Model) |

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

- **Code Model (`code/`, `Makefile`, future `ergentics/`, `swiftpp/`, `lean/`, `rust/`):** [MIT License](LICENSE) ([`LICENSES/MIT.txt`](LICENSES/MIT.txt))
- **Paper & Data Model (`paper/`, `figures/`, `audits/`, future `data/`, docs):** [CC BY 4.0](LICENSE-paper) ([`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt))
- **Governance & Specs:** [`METHODOLOGY.md`](METHODOLOGY.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`CALIBRATIONS.md`](CALIBRATIONS.md) · [`ERGENTICS.md`](ERGENTICS.md) · [`NEGATIVES.md`](NEGATIVES.md) · [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md) · [`PROVENANCE.md`](PROVENANCE.md) · [`POLICY.md`](POLICY.md) · [`SECURITY.md`](SECURITY.md)
