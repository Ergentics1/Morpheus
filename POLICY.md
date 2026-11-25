# Policy

Guidelines for research integrity, transparency, licensing, and repository hygiene in **Morpheus**.

## 1. AI Assistance & Provenance

- All AI-assisted drafting, derivations, code, or formal proofs must be disclosed in [`PROVENANCE.md`](PROVENANCE.md) and tracked under the marker scheme in [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md).
- Baseline manuscripts and artifacts are archived cleanly with SHA-256 checksums so revisions remain auditable.
- Unverified claims, references, or external computational results must be labeled honestly until independently reproduced in this repository.

## 2. Verification Standards

Keep verification tiers clearly separated:

1. **Baseline / Upstream AI-Assisted (`[GB]`, `[E→GB]`):** Results and audit logs imported from upstream working sessions.
2. **Cross-Verified (`[X]`):** Results independently reproduced, reconciled, or revised in Ergentics' verification workflow and recorded in [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md).
3. **Formal:** Machine-checked proofs (e.g., Lean 4) with no `sorry` or unreviewed axioms.

## 3. Code Simplicity & Hygiene

- Keep code, scripts, and comments concise and readable.
- Never commit credentials, API keys, tokens, `.env` files, private keys, or personal data.
- Never commit absolute local filesystem paths, workstation usernames, or embedded file-path metadata in assets. Use repository-relative paths only.

## 4. Dual Licensing & Dependencies

- **Code (`code/`, `Makefile`):** [MIT License](LICENSE) ([`LICENSES/MIT.txt`](LICENSES/MIT.txt)).
- **Paper, figures, audits, and documentation:** [CC BY 4.0](LICENSE-paper) ([`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt)).
- Third-party code dependencies must use MIT-compatible permissive licenses (e.g., MIT, Apache-2.0, BSD) unless explicitly approved by the maintainer.

## 5. Contributions

- Keep pull requests focused and minimal.
- Update [`PROVENANCE.md`](PROVENANCE.md) and [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md) whenever adding or revising research artifacts or verification results.
- Engage constructively and focus critiques on mathematical correctness, clarity, and reproducibility.
