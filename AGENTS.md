# Agent & Security Guidelines

Instructions for AI coding/research agents and automated tools operating on **Morpheus**.

## Core Rules

1. **Deep code, tight comments:** Lay out open-source code deeply, clearly, and thoroughly for auditability and mathematical rigor; keep comments tight and to the point. Avoid unnecessary boilerplate or heavy dependencies.
2. **Do not conflate data with code:** Code (algorithms, proofs, verifiers) and Data (cached tables, empirical outputs, external snapshots, audit logs) are two different models. Keep them strictly separated and never treat assertions over cached data files as independent code verification (see [`METHODOLOGY.md`](METHODOLOGY.md)).
3. **No credential exposures:** Never commit, print, or embed API keys, tokens, passwords, private keys, `.env` files, or personal contact details.
4. **No local path leaks:** Never write absolute local filesystem paths, workstation usernames, or host-specific paths into repository files, comments, configs, or generated image/PDF metadata. Use repository-relative paths or `$HOME` in shell examples.
5. **Preserve baselines:** Do not modify archived baseline papers, figures, or upstream `code/` artifacts (listed in [`PROVENANCE.md`](PROVENANCE.md)) unless the maintainer explicitly asks for edits.
6. **Log provenance:** Record AI-assisted derivations, code, proofs, and verification status honestly in [`PROVENANCE.md`](PROVENANCE.md) and [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md). Never present unverified statements as verified.
7. **Check licenses before adding dependencies:** All code dependencies must be compatible with the repository's [MIT License](LICENSE).
8. **Verify by Correspondence & D/R/P/Seam SWE-sweeps:** Follow [`METHODOLOGY.md`](METHODOLOGY.md) — quantify error bounds in dimensionless regimes, test Deterministic (`D`), Runtime global-invariant (`R`), Probabilistic calibration/RCT (`P`), and `D ↔ R ↔ P` boundary seams (including keyed PRNGs for bit-exact replay).
9. **Keep negatives:** Never discard refuted hypotheses, negative controls, or failed assumptions; log and recheck them in [`NEGATIVES.md`](NEGATIVES.md) with their exact scope boundaries.
10. **Follow ADPIE & eliminate superseded scaffolding:** Execute every work unit via **Assess → Diagnose → Plan → Implement → Evaluate** ([`METHODOLOGY.md`](METHODOLOGY.md)). Build real foundations directly; audit for and remove hardcoded shortcuts, superseded scaffolding, or temporary fixtures rather than letting them linger.
11. **Release on paper updates:** Cut a new versioned GitHub release whenever the paper manuscript is updated.

## Pre-Commit Security Checklist

Before committing or opening a pull request, verify:

- `git status` and `git diff` contain no secrets, tokens, personal info, or local filesystem paths.
- Code and Data models remain cleanly separated (no stray data blobs dropped into new source directories).
- No superseded scaffolding, hardcoded placeholder fixtures, or dead stubs are left behind.
- Build artifacts (`.lake/`, `target/`, `.build/`, `build/`, `__pycache__/`) are untracked and ignored via [`.gitignore`](.gitignore).
- Any newly added PNG/PDF assets contain no local path metadata.
- Automated hygiene checks in [`.github/workflows/security.yml`](.github/workflows/security.yml) pass.
