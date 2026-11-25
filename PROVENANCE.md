# Provenance

This document tracks the origin, baseline integrity, AI-assistance disclosures, and verification status of research artifacts in **Morpheus**. See [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md) for the result-by-result contribution marker ledger (`[GB]`, `[E]`, `[E→GB]`, `[lit.]`, `[X]`).

## Paper Package: *Prime Cadences*

- **Title:** Prime cadences: Ihara zeta, graphene, and voice-leading homology on the Tonnetz
- **Author:** Ergentics (sole author)
- **Baseline archived:** 2026-11-25 (manuscript dated November 2026)
- **Status:** Reconciled pre-commit baseline (LaTeX source, Markdown mirror, figures, code, dual licenses, and upstream audit reports aligned; independent cross-verification `[X]` and formal proofs pending)

### Origin & AI-Assistance Disclosure

- Initial exploration, proofs, computations, figures, and literature checks originated through Ergentics' work with **Grok Bot** (detailed per theorem in [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md)).
- Two upstream exports were reconciled before the initial commit:
  1. An earlier PDF-to-Markdown conversion (`prime_cadences_paper.md`, `CITATION.cff`, and PNG `figures/fig1..fig5.png`).
  2. The updated arXiv/LaTeX package (`paper/`, `arxiv/prime-cadences-arxiv.tar.gz`, `code/`, `audits/`, `CONTRIBUTIONS.md`, `Makefile`, `requirements.txt`, `LICENSE-paper`, and `LICENSES/`), adding §4.1 (general tune reduction), Proposition 7.10 (minimal genus-5 binary curves), §7.6–7.7 (trace obstruction, 2-adic edge lengths, mass-formula search), contribution tags, and 50 DOI-verified references.

### Key File Inventory (SHA-256)

| File | Role | Current SHA-256 | Original Upload SHA-256 |
| :--- | :--- | :--- | :--- |
| `paper/prime-cadences.tex` | Canonical LaTeX manuscript | `49ac679f2d376ac5b2f4e0ee37709f00e7483dd69f8683144de9bdc6111e87d7` | *(unchanged)* |
| `paper/prime-cadences.bbl` | Pre-built bibliography for arXiv | `2ea46ebf7e4e1fc8920565a9f271de1cb4aa1e9fc47770e2c311c8f0d9e0c6cf` | *(unchanged)* |
| `paper/prime-cadences.pdf` | Compiled PDF (rebuilt via `make pdf` with fixed `fourier.pdf`) | `e18fbdc42e09b6ce7bc758a80d9098a930eacb09e257d730e5e34fb00a1eebee` | `0518682840e6026cdb4d6f6840a78c17c2ba8c3a8cca27823f1645ee6a98cb1b` |
| `paper/references.bib` | BibTeX database (50 DOI-checked refs) | `2a9b9cc7ab48c0c39b41518aba6075e5f00447314ab394c8e73db5234ca5b906` | *(unchanged)* |
| `paper/figures/fourier.pdf` | Vector Figure 1 (right panel, fixed) | `115b60e6d3caf341826c12011d9961a9129cd32b21182a764afdacbecf67d164` | `8b5749ef5431ddf0dd07519c924433bf5da35f0e043122ba598fb8425e9586a9` |
| `arxiv/prime-cadences-arxiv.tar.gz` | arXiv bundle (rebuilt with fixed `fourier.pdf`) | `af20cc2aaf9db5eff38ea47aef52843450407da0e68948de42b42a5d66ec55a8` | `749ff2a62c5453277270d82f6d84e4d8d415d1d98adfea0f9063da592be2a4bf` |
| `prime_cadences_paper.md` | Reconciled GFM mirror of `prime-cadences.tex` | `3f7817c34790cc7d89e242fa5df455f0858d20878da8c1e3ca098401be7ae09b` | `3049266c44fc6e77a6e4e255bd8c1536ea368c535cfdb5169fbf9b991b8a75b2` |
| `CITATION.cff` | Reconciled CFF 1.2.0 metadata | `11b3ea663f708fa51d953fe5b009671a676c90d99247bb2ec3bd40c311c69c94` | `0765b64b3f4f57334552c94776c0331c7774e88e4cb7278484beb48e1e9916e0` |
| `CONTRIBUTIONS.md` | Contribution tags & `[X]` ledger | `5c220ff5adc7c95d280584d1d42c2e1127df84a5c15346cc701a20d5ebaad240` | *(unchanged)* |
| `LICENSE-paper` | CC BY 4.0 summary for paper & docs | `9f98b93e50200f10f04087b6001a882b08ce98fa641bfafe89f19fc272b1e8b6` | *(unchanged)* |
| `Makefile` | Paper, arXiv, figure, and audit build rules | `1d2f9ce5d5882c5c84bd9f6f8e82f1e3bba9e80722ca0ae012bfe07f966bb8cd` | *(unchanged)* |
| `requirements.txt` | Pinned Python dependencies | `65cefed607187da37d350bf55b67f185ea2d51476b9b4c7ad4858b9dd0719bc4` | *(unchanged)* |
| `figures/fig1_tonnetz_fourier.png` | Figure 1 PNG (right panel fixed) | `fcd8db26b2da7b99bff55920be04854b60212ac0b840e3fbc4536269775f0cc5` | `5cc428ff14b5a9df6f2d78ef1527ac5489915cd678a2a39859847d5ec45e0227` |
| `figures/fig2_prime_cadences_poles.png` | Figure 2 PNG | `8c4cc98168f9dbb7b374ecb2b600075ef5c3deeae0ff24580c23c5461a11d24d` | *(unchanged)* |
| `figures/fig3_flux_winding.png` | Figure 3 PNG | `5d4099fb1a058150cf591afbeac95526d07a85f688a6a669222b5194018fac15` | *(unchanged)* |
| `figures/fig4_reduction_graph_cover.png` | Figure 4 PNG | `b9da044f3d6b8bd3475cbcf84578ebe9bfa0aab5a7915a4d6bed5eda8e82119e` | *(unchanged)* |
| `figures/fig5_genus2_curve_theta.png` | Figure 5 PNG | `5a2a347b8d236ad8354b594b667c89c0828042062e80811058915202fc91aa96` | *(unchanged)* |
| `audits/core_audit.md` | Upstream audit log (31/31) | `aa3cc266422ea2a1fe7c49719d0bd7b14b94ba20b209c5dcd9cdd509dc0a4267` | *(unchanged)* |
| `audits/spectrum_audit.md` | Upstream audit log (36/36) | `d7dc10c132d5985e2e4bb1b47b280cd1a3ca1c9330737fadea89b0d33e060dbe` | *(unchanged)* |
| `audits/arithmetic_audit.md` | Upstream audit log (23/23) | `9ade965c6ef7fa9a21bb4ea25de565b04eb268d0f512a6b1dbe511f4469a19ce` | *(unchanged)* |
| `audits/geometry_audit.md` | Upstream audit log (59/59) | `8f82e3b13dfe2ecd10a76b178e9fae36ff43b97dad0ddc4e1ddb3a97bc6f12f9` | *(unchanged)* |
| `audits/open_questions_audit.md` | Upstream audit log (27/27) | `2f67a9c542b6382878a7a7087ed2add3e4c48586784360be8876978ec535bcb8` | *(unchanged)* |

### Audit & Verification Status

- **Hygiene & leak scan:** All text, Python, JSON, LaTeX, PNG, and PDF files scanned cleanly — zero credentials, emails, local filesystem paths, or PNG text metadata chunks.
- **Fourier figure fixed in source and assets:** Updated `code/figures/figs.py` to merge the coinciding labels `f_2, f_6, f_{10}` at `(1, 0)` and keep `f_0` inside the right border; regenerated `paper/figures/fourier.pdf`, rebuilt `paper/prime-cadences.pdf` cleanly via `make pdf`, rebuilt `arxiv/prime-cadences-arxiv.tar.gz` with neutral `root/root` tar headers, and fixed `figures/fig1_tonnetz_fourier.png`.
- **Markdown reconciliation:** `prime_cadences_paper.md` and `CITATION.cff` have been reconciled with `paper/prime-cadences.tex` and `paper/prime-cadences.bbl` (matching section/theorem numbers, contribution markers, 50 verified references with DOIs, and linking `paper/prime-cadences.pdf`).
- **Execution & non-conflation status:** The 176/176 checks in `audits/` are the upstream Grok Bot reports. Inspection of the imported `code/` baseline shows all five upstream audit scripts read co-located cached `.json`/`.log` data files rather than recomputing every artifact from scratch. Per [`METHODOLOGY.md`](METHODOLOGY.md), `code/` is retained unmodified as the upstream baseline, while independent `[X]` cross-verification will strictly separate Code and Data models and recompute from first principles. No `[X]` entries have been logged yet.

## Revision Log

| Date | Artifact | Change & Verification Summary |
| :--- | :--- | :--- |
| 2026-11-25 | Initial baseline (`prime_cadences_paper.md`, `CITATION.cff`, `figures/`) | Imported initial PDF-to-MD conversion originating from Grok Bot collaboration. |
| 2026-11-25 | Full baseline package (`paper/`, `arxiv/`, `code/`, `audits/`, `LICENSES/`, `LICENSE-paper`, `CONTRIBUTIONS.md`, `Makefile`, `requirements.txt`) | Reconciled Markdown & `CITATION.cff` with `paper/prime-cadences.tex`, fixed Fourier label overlap in `code/figures/figs.py`, `paper/figures/fourier.pdf`, rebuilt `paper/prime-cadences.pdf` and `arxiv/prime-cadences-arxiv.tar.gz`, fixed `figures/fig1_tonnetz_fourier.png`, and aligned dual licensing and security checks. |
| 2026-11-25 | Governance, architecture, calibration & negatives docs (`METHODOLOGY.md`, `ARCHITECTURE.md`, `CALIBRATIONS.md`, `ERGENTICS.md`, `NEGATIVES.md`, `POLICY.md`, `AGENTS.md`, `README.md`, `PROVENANCE.md`) | Codified Ergentics' Correspondence Principle, Code-vs-Data non-conflation standard, D/R/P/Seam SWE-sweep protocol, Rung-1/RCT calibration specs, `ergentics/` + `swiftpp/` (Swift++ Triple-Check) organization, and permanent negatives ledger prior to `[X]` code implementation. |
