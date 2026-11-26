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

- **Code Model (`code/`, `lean/`, `swiftpp/`, `rust/`, `media/*.py`, `Makefile`):** [MIT License](LICENSE) ([`LICENSES/MIT.txt`](LICENSES/MIT.txt)).
- **Paper & Data Model (`paper/`, `arxiv/`, `figures/`, `audits/`, `data/`, `reconciliation/`, and documentation):** [CC BY 4.0](LICENSE-paper) ([`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt)).
- Third-party code dependencies must use MIT-compatible permissive licenses (e.g., MIT, Apache-2.0, BSD) unless explicitly approved by the maintainer.

## 5. Repeatable Reconciliation & Release Workflow

Every research or paper-update cycle follows a single consistent pattern:

1. **ADPIE execution (`Assess → Diagnose → Plan → Implement → Evaluate`):** Develop and verify changes against first-principles tests and formal oracles without mutating prior tagged baselines in place.
2. **Bidirectional cross-reconciliation (`reconciliation/`):** Exchange structured verification packets (`GEMINI4_NEON_RECONCILIATION.md`, `GROKBOT_RECONCILIATION_RESPONSE.md`, etc.) and run from-scratch cross-checks (`code/xcheck/`, `lean/`, `swiftpp/`, `rust/`) before folding new results into `paper/`.
3. **Full manuscript & metadata sync:** Whenever `paper/prime-cadences.tex` is updated:
   - Rebuild `paper/prime-cadences.pdf` and `.bbl` cleanly via `latexmk` (`0` errors, `0` undefined references) and remove LaTeX auxiliaries.
   - Rebuild `arxiv/prime-cadences-arxiv.tar.gz` with neutral `0/0` ownership headers.
   - Sync `prime_cadences_paper.md`, `CONTRIBUTIONS.md`, `CITATION.cff` (`version` & `date-released`), `NEGATIVES.md`, `README.md`, and `CHANGELOG.md` (moving released items from `[Unreleased]` into `## [X.Y.Z] - YYYY-MM-DD`).
   - Recompute and verify every SHA-256 in `PROVENANCE.md` and `data/MANIFEST.sha256`.
4. **Pre-commit & CI gate:** Run all `Makefile` audits + security hygiene scan (text, PNG chunks, PDF/MP4/tarball path check), commit cleanly, push to `main`, and verify GitHub Actions `Security Hygiene` CI succeeds.
5. **Versioned GitHub release on paper update:** Tag `vX.Y.Z` and publish the GitHub release; [`.github/workflows/release-assets.yml`](.github/workflows/release-assets.yml) automatically checks out the exact tag, verifies PDF hygiene, generates `SHA256SUMS.txt`, and attaches `prime-cadences.pdf`, `prime-cadences-arxiv.tar.gz`, and `SHA256SUMS.txt` as release assets.
