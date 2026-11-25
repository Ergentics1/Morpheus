# Security Policy

## Scope

This repository is an open-source research project. Security concerns in scope include:

- Accidental exposure of credentials, API keys, tokens, private keys, or personal data.
- Accidental leakage of local filesystem paths, hostnames, or embedded binary metadata.
- Vulnerabilities in repository scripts, build configurations, or CI workflows.

## Reporting a Vulnerability or Leak

Please **do not** open a public issue or pull request containing sensitive data, secrets, or exploit details.

Instead, report privately through **GitHub Security Advisories** on `Ergentics1/Morpheus` (under the **Security** tab → **Report a vulnerability**). Include the affected file or commit and a brief description so it can be rotated or remediated promptly.

## Preventive Controls

- No secrets, tokens, `.env` files, or local absolute paths may be committed (see [`POLICY.md`](POLICY.md) and [`AGENTS.md`](AGENTS.md)).
- Pull requests and pushes run an automated hygiene check ([`.github/workflows/security.yml`](.github/workflows/security.yml)) that scans for secret patterns, local path leaks, forbidden credential filenames, and embedded PNG text metadata.
- Workflow jobs run with minimal read-only token permissions (`contents: read`).
