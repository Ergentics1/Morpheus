# Morpheus

Open-sourced research repository by **Ergentics** (*Open Sourced Living*), structured to host multiple open-source research papers under a uniform ADPIE, Code-vs-Data, and multi-model verification standard.

## Research Portfolio ([`papers/`](papers/README.md))

| # | Paper | Location | Stage |
| :---: | :--- | :--- | :--- |
| **01** | **[Prime Cadences](prime_cadences_paper.md)** — *Ihara zeta, graphene, and voice-leading homology on the Tonnetz* | Root layout ([`paper/`](paper/), [`arxiv/`](arxiv/)) | **`v0.3.1` Released** (Immutable GitHub Release · 3-way verified) |
| **02** | **[Working Paper 030 (Horizon Monograph I)](papers/wp030_shape_propulsion/README.md)** — *Shape-Controlled Gravitational Propulsion Resolved* | [`papers/wp030_shape_propulsion/`](papers/wp030_shape_propulsion/) | **`Cycle 1 Audited [G4N]`** — frozen clean-room `[E]` archive + 3-plane `[G4N]` audit (`Python 9/9`, `Lean 4 15/15`, `Rust 7/7`, 8 catches + Theorem G1); awaiting `[GB]` pass |

## Paper #01: *Prime Cadences*

**[Prime cadences: Ihara zeta, graphene, and voice-leading homology on the Tonnetz](prime_cadences_paper.md)** *(Preprint, November 2026)*

- **Read on GitHub:** [`prime_cadences_paper.md`](prime_cadences_paper.md)
- **Compiled PDF:** [`paper/prime-cadences.pdf`](paper/prime-cadences.pdf)
- **LaTeX & BibTeX source:** [`paper/prime-cadences.tex`](paper/prime-cadences.tex), [`paper/references.bib`](paper/references.bib)
- **arXiv bundle:** [`arxiv/prime-cadences-arxiv.tar.gz`](arxiv/prime-cadences-arxiv.tar.gz)

Studies the 3-regular neo-Riemannian triad graph $X$ and its Ihara zeta primes (*prime cadences*), linking the Tonnetz to the honeycomb/graphene tight-binding spectrum, Weil polynomials over $\mathbb{F}_2$, the tune theorem and its generalisation, voice-leading homology, a genus-13 2-adic Mumford curve, minimal genus-5 binary curves, and 2-adic arithmetic obstructions.

> **Status:** **`v0.3.1` released (`2026-11-25`)** — round-2 referee-hardened canonical paper ([`paper/prime-cadences.tex`](paper/prime-cadences.tex), 35 pp PDF, 56 references incl. Poitou 1976/77, published with immutable release assets `prime-cadences.pdf`, `prime-cadences-arxiv.tar.gz`, and `SHA256SUMS.txt`), integrating Grok Bot's baseline (`code/`, `228/228` + `code/xcheck/round2/` `20/20`), Gemini 4 Neon's ADPIE Cycles 1–5 (`lean/` 33/33 theorems, `swiftpp/` `0.000e+00` delta, `rust/` zero-PARI Manin $T_2$, `ergentics/`, **Theorem 7.21 / Theorem D** $n \le 14 \to n \le 8$, erratum `NEG-E10` $18 \to 19$ pairs), and Ergentics' standalone clean-room Research Monograph I ([`cleanroom/prime_cadences_resolution/paper.typ`](cleanroom/prime_cadences_resolution/paper.typ), archived verbatim: 3-way 8/8 Brandt confirmation, wild involution $\sigma(z)=3/z$, combinatorially sharp $M(\mathcal{O}) \ge 36$, and **Proposition 7.18** unramified cyclotomic obstruction + non-arithmetic $\Gamma_5 \subset PGL_2(\mathbb{Q}_4)$ with $\tau(s_4 s_5) = 49/4 > 4$). See [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md) and [`reconciliation/`](reconciliation/README.md).

## Repository Layout

| Path | Description |
| :--- | :--- |
| [`papers/`](papers/README.md) | Multi-paper research registry and self-contained per-paper workspaces starting with Paper #02 ([`papers/wp030_shape_propulsion/`](papers/wp030_shape_propulsion/)) |
| [`paper/`](paper/) | Paper #01 (*Prime Cadences*) canonical LaTeX source (`prime-cadences.tex`), `.bbl`, compiled PDF (`v0.3.1`, 35 pp, 0 LaTeX warnings), `references.bib` (56 refs), and 8 vector PDF figures |
| [`prime_cadences_paper.md`](prime_cadences_paper.md) | GitHub Flavored Markdown mirror reconciled 1-to-1 with `paper/prime-cadences.tex` (`v0.3.1`, 56 refs) |
| [`figures/`](figures/README.md) | PNG figures 1–5 for `prime_cadences_paper.md` |
| [`arxiv/`](arxiv/) | Ready-to-upload arXiv source tarball (`prime-cadences-arxiv.tar.gz`, neutral `0/0` headers) |
| [`NOVELTY_GEMINI4_NEON.md`](NOVELTY_GEMINI4_NEON.md) | Audit-forward original mathematical novelties (ADPIE Cycles 4–5): Open Problem (3) resolution (Theorems A, B, Cor B.1, `NEG-M11`), 6th-order 2D cumulant/Edgeworth theory (Theorem C, `C-2'`/`C-2''`), & **Theorem D** (`Thm 7.21`: three-pincer Hilbert class field obstruction $n \le 8$ & sextic $u \in \{16, 32\}$ collapse) |
| [`cleanroom/`](cleanroom/README.md) | Standalone clean-room Research Monograph I ([`prime_cadences_resolution/paper.typ`](cleanroom/prime_cadences_resolution/paper.typ) & [`CONTRIBUTIONS_PATCH.md`](cleanroom/prime_cadences_resolution/CONTRIBUTIONS_PATCH.md)), archived verbatim on its own terms (`paper/prime-cadences.tex` is the single canonical reconciled manuscript) |
| [`reconciliation/`](reconciliation/README.md) | Multi-track reconciliation dossiers: [`GEMINI4_NEON_RECONCILIATION.md`](reconciliation/GEMINI4_NEON_RECONCILIATION.md) (Cycles 1–5), [`GROKBOT_RECONCILIATION_RESPONSE.md`](reconciliation/GROKBOT_RECONCILIATION_RESPONSE.md) (`v0.2.0`), & [`THREE_WAY_CLEANROOM_AUDIT.md`](reconciliation/THREE_WAY_CLEANROOM_AUDIT.md) (3-way audit) |
| [`media/`](media/README.md) | Gemini 4 Neon videos: 1:24 social reel (`gemini4_neon_prime_cadences.mp4`), 4:18 **Spoken-in-Harmony Educator Masterclass** with live Chess & Graph RH (`gemini4_neon_masterclass_chess_rh.mp4`), 4:08 **The Three-Pincer Symphony** (`gemini4_neon_cycle5_three_pincer_symphony.mp4`), zero-metadata posters, captions & MIT generators |
| [`lean/`](lean/) | Machine-checked Lean 4.36.0 formal proofs (**33/33 theorems**, zero Mathlib, 0 `sorryAx`, 0 `ofReduceBool`): `TriadGraph`, `TuneTheorem`, `ConductorTwo`, `WindingAndSchottky`, `NoveltyTheorems`, `Section7Obstructions` |
| [`swiftpp/`](swiftpp/) | **Swift++** Triple-Check verification suite (`ErgenticsCXX` C++20 `g++`/`clang++` 33/33 · `ErgenticsSwift` Pure Swift 6.4 16/16 · `ErgenticsInterop` live cross-check 22/22, `0.000e+00` delta) |
| [`rust/`](rust/) | Fourth-language exact verifier (Rust 1.100.0, zero external crates, 10/10 tests): $\mathbb{Z}[\zeta_{12}]$, Artin–Ihara tower, general $N$-EDO sweeps ($N \le 96$), Theorem C/D, & **zero-PARI Manin modular symbols $T_2$** across all 19 genus-13 curves |
| [`ergentics/`](ergentics/README.md) | Standalone from-scratch Python/PARI/SymPy verifiers (MIT, zero cached reads): `shimura_brandt_xcheck.py` (19 $X_0^D(N)$, 8/8 Brandt charpolys, quintic `106069`) & `open1_torsion_xcheck.py` ($\sigma(z)=3/z$, combinatorially sharp $M=36$ witness, $\Gamma_5 \subset PGL_2(\mathbb{Q}_4)$ & $\tau(s_4 s_5) = 49/4 > 4$) |
| [`data/`](data/README.md) | Immutable, SHA-256-checksummed Data Model calibration records (`data/MANIFEST.sha256` 3/3 OK, CC BY 4.0) |
| [`code/`](code/) | Archived Grok Bot Python scripts (`math_audit.py`, `deep/`, `eisenstein2/`, `geometry/`, `open_q/` round 3, from-scratch `xcheck/` 32/32, and `xcheck/round2/` 20/20) |
| [`audits/`](audits/README.md) | Recorded reports from the six `code/` audit suites (31, 36, 23, 59, 47, and 32 checks = 228/228) |
| [`Makefile`](Makefile) & [`requirements.txt`](requirements.txt) | Build targets (`pdf`, `arxiv` neutral `0/0` headers, `audit`, `figures`) and pinned Python dependencies |
| [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md) | Uniform symmetric contribution tags (`[E]`, `[GB]`, `[E→GB]`, `[G4N]`, `[E→G4N]`, `[lit.]`, `[X]`) and complete 3-way verification ledger |
| [`METHODOLOGY.md`](METHODOLOGY.md) | Core Thesis (Correspondence Principle), Code-vs-Data non-conflation, ADPIE, and D/R/P/Seam SWE-sweep standard |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Four-plane Code-vs-Data architecture, `D ↔ R ↔ P` seams, and multi-language layout blueprint |
| [`CALIBRATIONS.md`](CALIBRATIONS.md) | Correspondence error-bound ledger (`C-1`–`C-5`, `C-2'`, `C-2''`), Rung-1 calibration metrics, RCT protocol, and output schema |
| [`ERGENTICS.md`](ERGENTICS.md) | Ergentics core library (`ergentics/`) and **Swift++** Triple-Check spec (`swiftpp/`: Pure C++20 · Pure Swift · Swift↔C++ interop) |
| [`NEGATIVES.md`](NEGATIVES.md) | Permanent ledger of refuted claims (`NEG-M1`–`NEG-M14`, `NEG-E1`–`NEG-E11`, `NEG-W1`–`NEG-W6`), obstructions, negative controls, and engineering traps |
| [`PROVENANCE.md`](PROVENANCE.md) | Origin, AI-assistance disclosure, SHA-256 checksums, and revision log |
| [`CHANGELOG.md`](CHANGELOG.md) | Versioned release history (`v0.1.0`, `v0.2.0`, `v0.3.0`, `v0.3.1`) and `[Unreleased]` tracking |
| [`CITATION.cff`](CITATION.cff) | Machine-readable citation metadata (CFF 1.2.0, `v0.3.1`, `2026-11-25`) |
| [`POLICY.md`](POLICY.md) | Research integrity, symmetric AI attribution, licensing, and automated immutable release workflow |
| [`SECURITY.md`](SECURITY.md) | Vulnerability reporting and secret/path-leak security policy |
| [`AGENTS.md`](AGENTS.md) | Rules for automated and AI agents working in this repository |
| [`LICENSE`](LICENSE), [`LICENSE-paper`](LICENSE-paper), [`LICENSES/`](LICENSES/) | Dual license: MIT (Code Model) and CC BY 4.0 (Paper & Data Model) |

## Reproducing Audits and Figures

Install the pinned Python dependencies from [`requirements.txt`](requirements.txt), then use [`Makefile`](Makefile):

```bash
make audit    # run all 6 computational audit scripts in code/ (228/228 checks)
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
