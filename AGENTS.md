# Agent & Security Guidelines

Instructions for AI coding/research agents and automated tools operating on **Morpheus**.

## Core Rules

1. **Keep it simple:** Write minimal, clear code and concise comments. Avoid unnecessary boilerplate or heavy dependencies.
2. **No credential exposures:** Never commit, print, or embed API keys, tokens, passwords, private keys, `.env` files, or personal contact details.
3. **No local path leaks:** Never write absolute local filesystem paths, workstation usernames, or host-specific paths into repository files, comments, configs, or generated image metadata. Use repository-relative paths or `$HOME` in shell examples.
4. **Preserve baselines:** Do not modify archived baseline papers or figures (listed in [`PROVENANCE.md`](PROVENANCE.md)) unless the maintainer explicitly asks for edits.
5. **Log provenance:** Record AI-assisted derivations, code, proofs, and verification status honestly in [`PROVENANCE.md`](PROVENANCE.md). Never present unverified statements as verified.
6. **Check licenses before adding dependencies:** All project dependencies must be compatible with the repository's [MIT License](LICENSE).

## Pre-Commit Security Checklist

Before committing or opening a pull request, verify:

- `git status` and `git diff` contain no secrets, tokens, personal info, or local filesystem paths.
- Build artifacts (`.lake/`, `target/`, `.build/`, `build/`, `__pycache__/`) are untracked and ignored via [`.gitignore`](.gitignore).
- Any newly added PNG/PDF assets contain no local path metadata.
- Automated hygiene checks in [`.github/workflows/security.yml`](.github/workflows/security.yml) pass.
