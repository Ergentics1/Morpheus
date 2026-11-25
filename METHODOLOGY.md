# Methodology & Verification Standard

Core thesis, model separation rules, and SWE-sweep verification protocol for **Morpheus**.

## 1. Core Thesis: The Correspondence Principle

> **Every deeper theory must smoothly contain the older theory inside its proven dimensionless regime, with a quantifiable error bound on the mismatch.**

Every theorem, model refinement, asymptotic limit, or numerical implementation in this repository must specify:

1. The **older / limiting theory** being recovered.
2. The **dimensionless regime** where recovery holds (e.g. $2^{-m/2} \ll 1$, $w/\sqrt{m} = O(1)$, $\varphi \to 0$).
3. A **quantifiable error bound** on the mismatch, verified across regimes rather than at a single nominal point.

## 2. Non-Conflation Principle: Code Model vs. Data Model

**Do not conflate data with code — they are two different models.**

| Dimension | Code Model | Data Model |
| :--- | :--- | :--- |
| **Role** | Executable algorithms, mathematical operators, formal proofs, generators, and verifiers | Precomputed tables, empirical measurements, external snapshots (e.g. LMFDB), audit logs, RCT datasets |
| **License** | MIT ([`LICENSE`](LICENSE)) | CC BY 4.0 ([`LICENSE-paper`](LICENSE-paper)) |
| **Style** | Deep, thorough, inspectable open-source implementations with tight, to-the-point comments | Immutable, schema-typed, SHA-256-checksummed artifacts with explicit provenance |
| **Location (new `[X]` work)** | Dedicated language/code modules (`ergentics/`, `swiftpp/`, `lean/`, `rust/` — see [`ARCHITECTURE.md`](ARCHITECTURE.md) & [`ERGENTICS.md`](ERGENTICS.md)) | Dedicated artifact directories (`data/`, `data/calibrations/`, `audits/` — see [`CALIBRATIONS.md`](CALIBRATIONS.md)) |

### Anti-Conflation Rules

1. **No circular verification:** Assertions executed over cached JSON/log files validate a stored data snapshot, *not* the underlying mathematical computation. Independent `[X]` verification must recompute from first principles or machine-checked axioms.
2. **Explicit `Code ↔ Data` boundaries:** Code generates data into dedicated output paths with manifest checksums; data ingested by code must pass runtime schema and invariant guards (`R-Type`) before entering deterministic kernels (`D-Type`).
3. **Legacy baseline isolation:** The imported upstream `code/` directory co-locates Python scripts with precomputed `.json`/`.log` data files (and its 5 audit scripts read several of those cached JSON files). It is preserved as the upstream Grok Bot baseline; all new `[X]` code keeps Code and Data strictly separated.

## 3. SWE-Sweep Verification Matrix (`D` / `R` / `P` & Seams)

Every `[X]` cross-verification (tracked in [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md)) and new implementation runs across four classes targeting distinct failure modes:

### Deterministic (`D-Type`)
- **Blind spot:** Fixed-order floating-point assertions pass nominal inputs while masking catastrophic non-associative cancellation or basis-order dependence.
- **Required checks:**
  - Use exact arithmetic (integers, rationals, cyclotomic/algebraic rings, machine-checked Lean 4 proofs) as the ground-truth oracle.
  - Under floating-point evaluation, sweep adversarial summation orders, vertex/basis permutations, and conditioning regimes, asserting explicit error bounds against exact ground truth.

### Runtime (`R-Type`)
- **Blind spot:** Component-wise bounds (`diag(P) > 0`, `|u_i| <= c`) miss global invariants: an off-diagonal spike can render a symmetric covariance matrix indefinite ($\lambda_{\min}(P) < 0$) despite positive diagonals and crash downstream Cholesky solves; a single `NaN` poisons an entire state vector; per-cell clamps miss aggregate conservation caps.
- **Required checks:**
  - Enforce **global invariants**: positive definiteness ($\lambda_{\min} > 0$, Cholesky factorisation), PSD nullity (e.g. connected graph Laplacian), Hermiticity/symmetry, and exact aggregate conservation laws (e.g. $\sum_w \pi(m, w) = \pi(m)$, probability totals summing to $1$).
  - Inject adversarial runtime faults (`NaN`, `±Inf`, indefinite off-diagonal spikes, out-of-domain inputs) and assert clean rejection before state corruption.

### Probabilistic (`P-Type`)
- **Blind spot:** Point-estimate accuracy checks (mean or variance only) miss distributional calibration failures, such as assuming a naive Gaussian under Rung-1 distributional/observational considerations.
- **Required checks:**
  - Evaluate **full distributional calibration** (total variation distance, KL divergence, KS/$\chi^2$ goodness-of-fit, excess kurtosis, tail coverage, and finite-sample correspondence error decay) rather than single-point tolerances.
  - Pair claims with **RCT / controlled baselines** (randomized null ensembles, permutation controls, treatment vs. control comparisons) so effects and calibration bounds are tested against explicit controls.

### Cross-Type Boundary Seams (`D ↔ R ↔ P`)
- **Blind spot:** The most severe failures occur at type boundaries — an uncalibrated or out-of-distribution probabilistic estimator (`P`) feeding an unguarded deterministic kernel/actuator (`D`), or a deterministic simulation (`D`) calling an unkeyed global PRNG (`P`) and destroying bit-exact post-incident replay.
- **Required checks:**
  - **Bit-exact replay (`D ↔ P`):** Never call unkeyed global PRNG state in deterministic tests or simulations; pass explicit, scoped keyed PRNG streams so outcomes are invariant to execution order.
  - **Guarded handoffs (`P → R → D`):** Validate calibration, finiteness, and global structural invariants (`R`) at every boundary before probabilistic outputs drive deterministic logic (`D`).

## 4. Execution Loop (ADPIE) & Anti-Scaffolding Discipline

All engineering, verification, and paper-update work follows the **ADPIE** cycle:

1. **Assess:** Inspect current code, proofs, data models, baseline artifacts, and [`NEGATIVES.md`](NEGATIVES.md).
2. **Diagnose:** Pinpoint root causes, `D`/`R`/`P`/Seam blind spots, Code-vs-Data conflation, hardcoded shortcuts, or correspondence gaps.
3. **Plan:** Specify the real foundation, dimensionless regimes, error bounds, and pre-registered acceptance/RCT criteria before editing code.
4. **Implement:** Lay out deep, first-principles open-source code with tight comments across the target lanes (including Swift++ Triple-Check).
5. **Evaluate:** Execute full `D` / `R` / `P` / Seam SWE-sweeps, verify 3-way agreement and calibration bounds, update [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md) (`[X]`), [`PROVENANCE.md`](PROVENANCE.md), and [`NEGATIVES.md`](NEGATIVES.md), and publish a versioned GitHub release on every paper update.

### No Lingering Scaffolding or Hardcoded Fixtures

- Build the **real foundation** whenever possible instead of placeholder stubs or hardcoded lookup tables.
- Audit continuously for **superseded scaffolding, hardcoded constants, and temporary fixtures**; never allow temporary fixtures to outlive the step that needed them, and never let hardcoded outputs masquerade as live first-principles computation.

## 5. Baseline Audit Findings & `[X]` SWE-Sweep Targets

Concrete gaps identified in the imported baseline `code/` to address in independent `[X]` verification:

| Class | Baseline Gap Observed | Target `[X]` SWE-Sweep Check |
| :--- | :--- | :--- |
| **Data–Code Conflation** | All 5 upstream audit scripts in `code/` read co-located cached `.json`/`.log` files (`2`, `6`, `4`, `4`, `8` files respectively) | Strict Code/Data separation; first-principles recomputation with zero reliance on cached JSON blobs |
| **Correspondence** | Asymptotics checked at isolated $m$ (`m = 40`, single `u = 0.137`) | Sweep quantified error bounds across $m$ ($2^{-m/2}$ PNT bound, $O(1/m)$ winding CLT bound, $O(\varphi^4)$ flux expansion, 12/31/53-EDO Ramanujan threshold) |
| **D-Type** | Fixed-order `float64`/`np.allclose` and `h = 1e-6` finite-difference Hessian (`code/deep/graphene.py`) | Exact integer/rational/algebraic oracles + Lean 4 proofs + adversarial float summation/permutation sweeps |
| **R-Type** | Component-wise checks on `Cov` (`code/deep/audit.py:49`), no fault-injection tests | Global PD/Cholesky on $G$ and $\frac{m}{2}G^{-1}$, PSD nullity-1 on $3I - A$, Hermiticity of $A_\varphi$, exact aggregate conservation, `NaN`/indefinite fault injection |
| **P-Type + RCT** | Point-only checks (`Var(W)/m` and 3% tolerance at `w = 0`, `code/deep/audit.py:52-54`) | Full distribution calibration (TV, KL, kurtosis, tail bounds across all $w$) + RCT/null controls (random signings vs. voice-parity, non-backtracking null walks, non-fixed 2-adic discs) |
| **Seam (`D ↔ R ↔ P`)** | Shared global `random.seed(1)` reused across multiple checks (`code/open_q/open_audit.py`) | Independent keyed PRNG per check with order-invariance / bit-exact replay assertions and explicit boundary validators |
