# Policy

Guidelines for research integrity, transparency, model separation, licensing, and repository hygiene in **Morpheus**.

## 1. AI Assistance, Symmetric Attribution & Provenance

- **Sole human authorship & scholarly AI disclosure:** Ergentics is the sole author responsible for scientific direction, methodology, review, and content. Following standard scholarly practice on AI disclosure, AI assistants are never listed as authors and are credited transparently under uniform attribution bounds in [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md), [`PROVENANCE.md`](PROVENANCE.md), and the manuscript's *Contributions and provenance* section.
- **Uniform marker scheme (symmetric across AI assistants):**
  - `[E]` — by Ergentics.
  - `[GB]` / `[G4N]` — statement, proof, and computation by Grok Bot (`GB`) or Gemini 4 Neon (`G4N`), respectively (extensible to future assistants via a consistent short code).
  - `[E→GB]` / `[E→G4N]` — question, direction, or methodology set by Ergentics, with statement, proof, and computation by the named AI assistant.
  - `[lit.]` — result from the cited literature, re-checked computationally/formally.
  - `[X]` — cross-verified across at least two independent toolchains (zero shared cached outputs); `independently E→<AI>` marks an independent derivation reached in a second toolchain.
- **Lexical discipline:** Match terminology and citations consistently to established mathematical, physical, and music-theory literature.
- **Baseline auditability:** Archive versioned manuscripts and artifacts cleanly with SHA-256 checksums in [`PROVENANCE.md`](PROVENANCE.md) so revisions remain auditable.
- **Keep negatives:** Record refuted hypotheses, obstructions, negative controls, and engineering traps permanently in [`NEGATIVES.md`](NEGATIVES.md) with their exact scope boundaries so they are neither repeated nor lost when rechecking under relaxed hypotheses.
- Unverified claims, references, or external computational results must be labeled honestly until independently reproduced in this repository.

## 2. Verification Standards

All verification follows Ergentics' **Correspondence Principle**, **Code-vs-Data Non-Conflation**, and the **D / R / P / Seam SWE-sweep protocol** defined in [`METHODOLOGY.md`](METHODOLOGY.md). Keep verification tiers clearly separated:

1. **Single-Toolchain AI-Assisted (`[GB]`, `[E→GB]`, `[G4N]`, `[E→G4N]`):** Results derived and audited within one toolchain.
2. **Cross-Verified (`[X]`):** Results independently reproduced from first principles across separate toolchains (zero reads of cached upstream data), via D/R/P/Seam SWE-sweeps and RCT/calibration checks, recorded in [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md).
3. **Formal:** Machine-checked proofs (e.g., Lean 4 without Mathlib) with zero `sorryAx` and zero unreviewed axioms.

## 3. Code Depth, Comments & Non-Conflation

- Lay out open-source code deeply and thoroughly so mathematical steps and verification logic are directly inspectable; keep comments tight and to the point.
- **No lingering scaffolding or hardcoded shortcuts:** Prefer real foundations over temporary fixtures; actively monitor for and remove superseded scaffolding before committing.
- **Do not conflate data with code:** Code (executable logic, proofs, verifiers) and Data (cached tables, empirical measurements, external lookups, audit logs) are two distinct models and must stay structurally separated. Assertions over cached data files do not constitute independent code execution.
- Never commit credentials, API keys, tokens, `.env` files, private keys, or personal data.
- Never commit absolute local filesystem paths, workstation usernames, or embedded file-path metadata in assets. Use repository-relative paths only.

## 4. Dual Licensing & Dependencies

- **Code Model (`code/`, `ergentics/`, `lean/`, `swiftpp/`, `rust/`, `tests/`, `papers/<slug>/{code,cpp,lean,rust}/`, `reconciliation/*/code/`, `media/*.py`, `Makefile`):** [MIT License](LICENSE) ([`LICENSES/MIT.txt`](LICENSES/MIT.txt)).
- **Paper & Data Model (`paper/`, `arxiv/`, `figures/`, `audits/`, `cleanroom/`, `data/`, `papers/<slug>/{paper,arxiv,data,cleanroom}/`, `reconciliation/`, and documentation):** [CC BY 4.0](LICENSE-paper) ([`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt)).
- Third-party code dependencies must use MIT-compatible permissive licenses (e.g., MIT, Apache-2.0, BSD) unless explicitly approved by the maintainer.

## 5. Repeatable Reconciliation, Continuous Testing & Release Workflow

Every research or paper-update cycle follows a single consistent pattern:

1. **ADPIE execution (`Assess → Diagnose → Plan → Implement → Evaluate`):** Develop and verify changes against first-principles tests and formal oracles without mutating prior tagged or frozen baselines (`CI-10` locks) in place.
2. **Multi-plane zero-shared-data verification & reconciliation (`reconciliation/`):** Independently cross-check all claims across Pure Python (`--check-only`), Zero-Crate Rust, Dual-Compiler C++20 (`g++` & `clang++`), and Live Kernel-Compiled Zero-Mathlib Lean 4.36.0 (`0 sorryAx`, `0 Lean.ofReduceBool`), logging any bidirectional reconciliation packets or portfolio retrospectives in `reconciliation/`.
3. **Full manuscript & metadata sync:** Whenever any canonical AMS `LaTeX` manuscript (`paper/prime-cadences.tex` or `papers/<slug>/paper/*.tex`) is added or updated:
   - Rebuild the canonical `.pdf` and `.bbl` cleanly via `latexmk` (`0` errors, `0` warnings, `0` overfull hboxes, `0` local-path metadata) and remove LaTeX auxiliaries.
   - Rebuild the standalone-verified neutral `0/0` ownership arXiv bundle under `arxiv/` or `papers/<slug>/arxiv/`.
   - Sync the 1-to-1 GFM mirror, `CONTRIBUTIONS.md`, `NEGATIVES.md`, `CALIBRATIONS.md`, `README.md`, `papers/README.md`, and `CHANGELOG.md` (moving released items from `[Unreleased]` into `## [X.Y.Z] - YYYY-MM-DD`; update `CITATION.cff` when Paper #01 changes).
   - Recompute and verify every SHA-256 in `PROVENANCE.md` and all repo-root-relative `MANIFEST.sha256` files.
4. **Pre-commit & Continuous-Testing CI gate:** Run [`tests/content_integrity_audit.py`](tests/content_integrity_audit.py) (`11/11` gates incl. `CI-11` cross-paper mathematical seam parity) and verify all 5 GitHub Actions PR jobs pass green — [`.github/workflows/continuous-testing.yml`](.github/workflows/continuous-testing.yml) (`content-integrity`, `python-verifiers`, `rust-and-cpp-verifiers` under both `g++` & `clang++`, `lean-formal-oracles`) and [`.github/workflows/security.yml`](.github/workflows/security.yml) (`hygiene-check`).
5. **Versioned immutable GitHub release on paper update (Rule 11):** Because GitHub Immutable Releases lock tags and assets upon publication (`NEG-E11`), cut releases only when a paper manuscript is added or updated (keeping non-manuscript code/CI/governance improvements under `CHANGELOG.md` `## [Unreleased]`). Trigger [`.github/workflows/release-assets.yml`](.github/workflows/release-assets.yml) by pushing an annotated `vX.Y.Z` tag on `main` (or via `workflow_dispatch` targeting a `--draft` release); the workflow verifies PDF and neutral-tar (`0/0`) hygiene across all canonical manuscripts (currently `6` PDFs + `6` arXiv tarballs + `SHA256SUMS.txt` = `13` assets), uploads all assets before publication, and atomically seals the immutable release.
