# Policy

Guidelines for research integrity, transparency, model separation, licensing, and repository hygiene in **Morpheus**.

## 1. AI Assistance & Provenance

- All AI-assisted drafting, derivations, code, or formal proofs must be disclosed in [`PROVENANCE.md`](PROVENANCE.md) and tracked under the marker scheme in [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md).
- Baseline manuscripts and artifacts are archived cleanly with SHA-256 checksums so revisions remain auditable.
- **Keep negatives:** Record refuted hypotheses, obstructions, negative controls, and engineering traps permanently in [`NEGATIVES.md`](NEGATIVES.md) with their exact assumptions so they are neither repeated nor lost when rechecking under relaxed hypotheses.
- Unverified claims, references, or external computational results must be labeled honestly until independently reproduced in this repository.

## 2. Verification Standards

All verification follows Ergentics' **Correspondence Principle**, **Code-vs-Data Non-Conflation**, and the **D / R / P / Seam SWE-sweep protocol** defined in [`METHODOLOGY.md`](METHODOLOGY.md). Keep verification tiers clearly separated:

1. **Baseline / Upstream AI-Assisted (`[GB]`, `[E→GB]`):** Results and audit logs imported from upstream working sessions.
2. **Cross-Verified (`[X]`):** Results independently reproduced from first principles via D/R/P/Seam SWE-sweeps and RCT/calibration checks, recorded in [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md).
3. **Formal:** Machine-checked proofs (e.g., Lean 4) with no `sorry` or unreviewed axioms.

## 3. Code Depth, Comments & Non-Conflation

- Lay out open-source code deeply and thoroughly so mathematical steps and verification logic are directly inspectable; keep comments tight and to the point.
- **No lingering scaffolding or hardcoded shortcuts:** Prefer real foundations over temporary fixtures; actively monitor for and remove superseded scaffolding before committing.
- **Do not conflate data with code:** Code (executable logic, proofs, verifiers) and Data (cached tables, empirical measurements, external lookups, audit logs) are two distinct models and must stay structurally separated. Assertions over cached data files do not constitute independent code execution.
- Never commit credentials, API keys, tokens, `.env` files, private keys, or personal data.
- Never commit absolute local filesystem paths, workstation usernames, or embedded file-path metadata in assets. Use repository-relative paths only.

## 4. Dual Licensing & Dependencies

- **Code Model (`code/`, `Makefile`, and future executable/formal code modules):** [MIT License](LICENSE) ([`LICENSES/MIT.txt`](LICENSES/MIT.txt)).
- **Paper & Data Model (`paper/`, `figures/`, `audits/`, future `data/`, and documentation):** [CC BY 4.0](LICENSE-paper) ([`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt)).
- Third-party code dependencies must use MIT-compatible permissive licenses (e.g., MIT, Apache-2.0, BSD) unless explicitly approved by the maintainer.

## 5. Contributions & Releases

- Follow the **ADPIE** loop (**Assess → Diagnose → Plan → Implement → Evaluate**; see [`METHODOLOGY.md`](METHODOLOGY.md)) for every work unit.
- Keep pull requests focused, well-structured, and clean.
- Update [`PROVENANCE.md`](PROVENANCE.md), [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md), and [`NEGATIVES.md`](NEGATIVES.md) whenever adding or revising research artifacts or verification results.
- Cut a new versioned GitHub release whenever the paper manuscript is updated.
- Engage constructively and focus critiques on mathematical correctness, clarity, and reproducibility.
