# Morpheus Continuous Testing & Content-Integrity Suite (`tests/`)

Permanent, zero-dependency continuous testing and content-integrity verification harness for **Morpheus** (MIT License; obeys [`AGENTS.md`](../AGENTS.md) and [`METHODOLOGY.md`](../METHODOLOGY.md)).

## Automated Gates (`content_integrity_audit.py`)

Run locally from the repository root:

```bash
python3 tests/content_integrity_audit.py
```

| Gate | Scope |
| :--- | :--- |
| **CI-1** | All `11/11` Data Model `MANIFEST.sha256` files verified from repo root (enforcing uniform repo-root-relative paths) |
| **CI-2** | Every `Current SHA-256` inventory row in [`PROVENANCE.md`](../PROVENANCE.md) verified against disk (`0` stale hashes) |
| **CI-3** | All `5/5` canonical arXiv tarballs checked for strictly neutral `0/0` ownership headers and byte-for-byte parity vs. `paper/` |
| **CI-4** | All tracked `.png` and `.pdf` assets scanned for PNG text metadata chunks and local filesystem path leaks |
| **CI-5** | All `5/5` canonical AMS `LaTeX`/BibTeX papers checked for `0` duplicate/unresolved `\ref`/`\eqref`, `0` undefined `\cite`, and `0` unused `.bib` entries (with Rule 5 waiver on frozen `v0.4.0` Horizon Piece II `farquhar1973`) |
| **CI-6** | Every relative link across all tracked Markdown files verified to resolve on disk (`0` broken links) |
| **CI-7** | All `8/8` Lean 4.36.0 projects (`lean-toolchain` pinned, static scan asserting `0` `sorry`/`admit`/`native_decide`/`unsafe`/`axiom` in code) |
| **CI-8** | Governance ledger consistency (`NEGATIVES.md` unique IDs, `CHANGELOG.md` strictly descending SemVer, `CITATION.cff` required fields) |
| **CI-9** | Code-vs-Data Model separation (Rule 2: zero `.json`/`.csv`/`.pkl`/`.npy` data blobs inside maintained `code/`, `lean/`, `rust/`, `swiftpp/`, `ergentics/`, or `tests/`) |
| **CI-10** | Cryptographic SHA-256 immutability locks on frozen archived baselines (Rule 5: Paper #01 `v0.3.1`, Clean-Room Monograph I, `WP 030`–`WP 035` `cleanroom/`, and Horizon Synthesis `v0.4.0` PDFs) |

## Continuous Integration ([`.github/workflows/continuous-testing.yml`](../.github/workflows/continuous-testing.yml))

Runs automatically on every push to `main`, every pull request, weekly schedule, and manual dispatch across four parallel jobs:

1. **`content-integrity`**: Runs `python3 tests/content_integrity_audit.py` (`10/10` gates).
2. **`python-verifiers`**: Runs zero-dependency from-scratch Python verifiers (`triadic_nauru_verify.py --check-only` `15/15`, `g4n_r1_xcheck.py` `4/4`, `wp030`–`wp035` `34/34`, and isolated Horizon Synthesis `piece{1,2,3}_sim.py` `18/18` with exact structural/digest + `1e-11` float JSON parity = `71/71` gates) and asserts zero unexpected working-tree drift (`git diff --exit-code`).
3. **`rust-and-cpp-verifiers`**: Builds and tests all `8/8` zero-crate Rust crates (`cargo test --release`, `53/53` tests) plus Pure C++20 `ErgenticsCXX` (`cmake` + `ctest`, `-O2 -Wall -Wextra -Werror`).
4. **`lean-formal-oracles`**: Installs `elan` + `leanprover/lean4:v4.36.0` (cached), builds and executes all `8/8` zero-Mathlib Lean 4 projects (`129/129` kernel-checked theorems), and asserts `0` `sorryAx` and `0` `Lean.ofReduceBool` across live `#print axioms` output.
