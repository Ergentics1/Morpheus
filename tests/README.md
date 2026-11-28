# Morpheus Continuous Testing & Content-Integrity Suite (`tests/`)

Permanent, zero-dependency continuous testing and content-integrity verification harness for **Morpheus** (MIT License; obeys [`AGENTS.md`](../AGENTS.md) and [`METHODOLOGY.md`](../METHODOLOGY.md)).

## Automated Gates (`content_integrity_audit.py`)

Run locally from the repository root:

```bash
python3 tests/content_integrity_audit.py
```

| Gate | Scope |
| :--- | :--- |
| **CI-1** | All `14/14` Data Model `MANIFEST.sha256` files verified from repo root (enforcing uniform repo-root-relative paths) |
| **CI-2** | Every `Current SHA-256` inventory row in [`PROVENANCE.md`](../PROVENANCE.md) verified against disk (`0` stale hashes) |
| **CI-3** | All `7/7` canonical arXiv tarballs checked for strictly neutral `0/0` ownership headers and byte-for-byte parity vs. `paper/` |
| **CI-4** | All tracked `.png` and `.pdf` assets scanned for PNG text metadata chunks and local filesystem path leaks |
| **CI-5** | All `7/7` canonical AMS `LaTeX`/BibTeX papers checked for `0` duplicate/unresolved `\ref`/`\eqref`, `0` undefined `\cite`, and `0` unused `.bib` entries (with Rule 5 waiver on frozen `v0.4.0` Horizon Piece II `farquhar1973`) |
| **CI-6** | Every relative link across all tracked Markdown files verified to resolve on disk (`0` broken links) |
| **CI-7** | All `10/10` Lean 4.36.0 projects (`lean-toolchain` pinned, static scan asserting `0` `sorry`/`admit`/`native_decide`/`unsafe`/`axiom` in code) |
| **CI-8** | Governance ledger consistency (`NEGATIVES.md` unique IDs, `CHANGELOG.md` strictly descending SemVer, `CITATION.cff` required fields) |
| **CI-9** | Code-vs-Data Model separation (Rule 2: zero `.json`/`.csv`/`.pkl`/`.npy` data blobs inside maintained `code/`, `cpp/`, `lean/`, `rust/`, `swiftpp/`, `ergentics/`, or `tests/`) |
| **CI-10** | Cryptographic SHA-256 immutability locks on frozen archived baselines (Rule 5: Paper #01 `v0.3.1`, Clean-Room Monograph I, `WP 030`–`WP 035` `cleanroom/`, and Horizon Synthesis `v0.4.0` PDFs) |
| **CI-11** | Cross-paper mathematical seam parity (`17` seams) across `Paper #01 ↔ PC-II ↔ PC-III ↔ PC-IV` (Poitou `(6,16,1,2)` margin & `FENV` bracket, $\pi_Y(6..24)$, `gon(Y)=6`, `gon(Z)=8`, `18` Cayley, `43` inv, `19/9 TF/0` Borel census, `<T,P,L,R>` `6/24`, `PC-III` `schema 1.1.0` `SplitMix64` digests, `PC-III ↔ PC-IV` degree-8 `UB_max_8_1 = 13.1423854579`, `peak_b = 3.039865`, `peak_exp_LB = 12.5955757277`, `f_bad = -0.6`, exact 9-curve torsion-free genus-25 Borel set, `PC-IV` `SplitMix64` digests & four-frontier counts), `WP 030`–`WP 035 ↔ Horizon Synthesis` (`Thm G1`, `Thm G3`, `NEG-W22`, `Thm G6`), and repo-wide Lean 4 `#print axioms` coverage (`>= 167`) |
| **CI-12** | Morpheus Standardized Universal Lexicon & Readability Gate ([`lexicon_audit.py`](lexicon_audit.py), `6/6` self-test gates `L1`–`L6` cross-checked bit-for-bit in zero-crate Rust [`lexicon_rust/`](lexicon_rust/)): `60` three-tier ISO 704 concepts (`120` deprecated-alias traps, `6` scoped symbol disambiguations) in [`data/lexicon/morpheus_universal_lexicon.json`](../data/lexicon/morpheus_universal_lexicon.json), byte-exact [`LEXICON.md`](../LEXICON.md) parity, `PC-IV` `0`-alias compliance, Negative Traps 1 & 2 (`4` injected aliases & Tier-3 `JWR = 40.0%`), positive JWR readability funnel (`40.0% -> 8.6% -> 0.0%`, `FK = 6.88`), and bit-exact `SplitMix64` seam parity (`xor=0x9f615b24f0dfd1d2`, `fnv=0x0345e6803850197e`) |

## Continuous Integration ([`.github/workflows/continuous-testing.yml`](../.github/workflows/continuous-testing.yml))

Runs automatically on every push to `main`, every pull request, weekly schedule, and manual dispatch across four parallel jobs:

1. **`content-integrity`**: Runs `python3 tests/content_integrity_audit.py` (`12/12` gates incl. `CI-11` `17`-seam cross-paper mathematical parity & `CI-12` Universal Lexicon gate) and `python3 tests/lexicon_audit.py --self-test`.
2. **`python-verifiers`**: Runs zero-dependency from-scratch Python verifiers (`triadic_nauru_verify.py --check-only` `15/15`, `triadic_3adic_verify.py --check-only --no-figs` `10/10`, `arithmetic_frontiers_verify.py --check-only --no-figs` `7/7`, `g4n_r1_xcheck.py` `4/4`, `wp030`–`wp035` `34/34`, and isolated Horizon Synthesis `piece{1,2,3}_sim.py` `18/18` with exact structural/digest + `1e-11` float JSON parity = `88/88` gates) and asserts zero unexpected working-tree drift (`git diff --exit-code`).
3. **`rust-and-cpp-verifiers`**: Builds and tests all `11/11` zero-crate Rust crates (`cargo test --release`, `72/72` tests + `PC-II`/`PC-III`/`PC-IV` & `tests/lexicon_rust` `cargo run --release`) plus **dual-compiler (`g++` & `clang++`)** Pure C++20 `ErgenticsCXX` (`cmake` + `ctest`, `-O2 -Wall -Wextra -Werror`) and freestanding zero-heap hardware-`FENV` C++20 `PC-III` (`8/8` gates) & `PC-IV` (`6/6` gates) oracles (`fenv_oracle.cpp`, `-O2 -std=c++20 -frounding-math -ffp-contract=off -Wall -Wextra -Werror`) with strict `diff -u` parity assertion between `g++` and `clang++` outputs.
4. **`lean-formal-oracles`**: Installs `elan` + `leanprover/lean4:v4.36.0` (cached), builds and executes all `10/10` zero-Mathlib Lean 4 projects (`167/167` kernel-checked theorems), and asserts `0` `sorryAx` and `0` `Lean.ofReduceBool` across live `#print axioms` output.
