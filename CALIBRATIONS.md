# Calibrations & RCT Verification Standard

Specification for **Correspondence Principle error bounds**, **Rung-1 distributional calibration (`P-Type`)**, and **Randomized Controlled Trial (RCT)** testing in **Morpheus**.

> **Non-conflation rule:** This file defines calibration *specifications and acceptance contracts*. Executable calibration code lives in the Code Model (`ergentics/`, `swiftpp/`, `rust/`); recorded calibration run outputs live strictly in the Data Model (`data/calibrations/`).

## 1. Correspondence Error-Bound Ledger (*Prime Cadences*)

Every deeper result must smoothly recover the older limiting model inside its dimensionless regime with a quantifiable error bound:

| ID | Deeper Model | Older / Limiting Model | Dimensionless Regime | Quantifiable Error Bound / Threshold |
| :--- | :--- | :--- | :--- | :--- |
| **C-1** | Exact prime cadence count $\pi(m)$ via Ihara trace (Thm 3.3) | Graph PNT asymptotic $\hat{\pi}(m) = 2^{m+1}/m$ | $\varepsilon = 2^{-m/2} \ll 1$, even $m \ge 6$ | Normalized error $|m\pi(m) - 2^{m+1}| / 2^{m/2} \le 48$ (12-EDO Ramanujan bound); contrast 53-EDO blow-up ($\lambda_{\max} = 2.8565 > 2\sqrt{2}$) |
| **C-2** | Exact discrete winding law $P_m(w) = \pi(m, w)/\pi(m)$ & 2D homology $(u, v)$ (Thm 6.1) | Local CLT $\mathcal{N}(0, m/24)$ and isotropic 2D Gaussian $\mathcal{N}(0, \frac{m}{2}G^{-1})$ | $z = w/\sqrt{m} = O(1)$, $1/m \ll 1$ | Full-distribution mismatch (TV, KL, excess kurtosis) decays at $O(1/m)$ as $m$ sweeps $6 \to 40$ (`TV = 1.086e-2` at $m=40$); covariance $\frac{m}{2}G^{-1}$ globally PD ($\lambda_{\min} > 0$) |
| **C-2'** | Exact discrete winding law $P_m(w)$ & 2D honeycomb axes $W=-u, v, 4u+3v$ (Thm C) | 4th-order Edgeworth density $Q_m^{(4)}(w) \propto e^{-z^2/2}(1 - \frac{17}{48m}H_4(z))$ & universal 2D isotropic 4th cumulant | $z = w/\sqrt{m/24} = O(1)$, $1/m \ll 1$ | Universal excess kurtosis $\kappa_{\mathrm{ex}} = -\frac{17}{2m} + O(m^2 2^{-m/2})$ along every axis $\mathbf{e} \in S^1$ (at $m=40$: `m·κ_ex = (-8.4952, -8.4898, -8.4909)`, max spread from `-8.5` = `0.0102`); TV drops to $O(1/m^2)$ (`9.951e-4` at $m=40$, **10.92×** over `C-2`) |
| **C-2''** | Exact discrete winding law $P_m(w)$ & 6th-order $C_6$ honeycomb expansion (Thm C) | 6th-order Edgeworth density $Q_m^{(6)}(w) \propto e^{-z^2/2}(1 - \frac{17}{48m}H_4 + \frac{1469}{2880m^2}H_6 + \frac{289}{4608m^2}H_8)$ | $z = w/\sqrt{m/24} = O(1)$, $1/m \ll 1$ | Exact $C_6$ anisotropy onset at order 6: bond-parallel armchair ($W=-u, v$) $\frac{1469}{4m^2}$ vs. bond-perpendicular zigzag ($4u+3v$) $\frac{1471}{4m^2}$; TV drops to $O(1/m^3)$ (`1.443e-4` at $m=40$, **75.30×** over `C-2`) |
| **C-3** | Flux-twisted adjacency spectrum $A_\varphi$ (Thms 5.2–5.3) | Untwisted triad graph spectrum $A_0$ (Thm 3.1) | $\varphi \to 0$ and $\varphi \in [0, 2\pi)$ | Dominant branch $|\lambda(\varphi) - (3 - \varphi^2/48)| = O(\varphi^4)$; exact Ramanujan boundary $\varphi_c = 4\arccos(3/4)$ separating $n \le 2$ from $n \ge 3$ cyclic covers |
| **C-4** | General $N$-EDO step-system tune reduction (Thm 4.3; Thms A, B & Cor B.1) | 12-EDO consonant-triad tune theorem (Thm 4.2) | $N = 12,\; S = \{1, 2\}$ inside general $(N, S, \mathcal{C})$ | Universal proof for all $N \ge 5$ whenever $\mathcal{C} = T$, $8 \nmid N$, or $S$ is closed under halving even elements (all consecutive $S = \{1, \dots, k\}$); exact sharp counterexample boundary `NEG-M11` ($N = 8m,\; \mathcal{C} = T/I(\{0, m, 4m\}),\; 2m \in S$) + non-backtracking failure (`NEG-M4`); verified across all 10,576 chords $N \le 72$ under maximal $S_{\max}(c_0)$ and 11,452 systems $N \le 96$ in `rust/` |

## 2. Rung-1 Distributional Calibration (`P-Type`)

Point-estimate checks (such as checking only `Var(W)/m` or `w = 0` within 3%) are insufficient because they mask skewness, heavy/light tails, finite-sample discreteness, and naive-Gaussian miscalibration under Rung-1 distributional considerations.

Every distributional calibration sweep must report the full metric vector:

| Metric | Formula / Definition | Purpose |
| :--- | :--- | :--- |
| **Total Variation (TV)** | $\frac{1}{2}\sum_w |P_m(w) - Q_m(w)|$ | Worst-case event probability mismatch across all measurable sets |
| **KL Divergence** | $\sum_{w:\,P_m(w) > 0} P_m(w)\log\frac{P_m(w)}{Q_m(w)}$ | Information loss; sensitive to tail miscalibration |
| **KS & Wasserstein-1** | $\sup_t |F_{P_m}(t) - F_{Q_m}(t)|$, $\int |F_{P_m} - F_{Q_m}|$ | Cumulative & transport-distance calibration |
| **Shape / Non-Gaussianity** | Skewness $\gamma_1$, excess kurtosis $\kappa_{\mathrm{ex}} = \mu_4/\sigma^4 - 3$ | Directly measures departure from naive Gaussianity and checks $O(1/m)$ Edgeworth decay |
| **Tail Coverage** | Empirical mass inside $[-k\sigma, +k\sigma]$ for $k \in \{1, 2, 3\}$ vs. nominal | Catches under-/over-dispersion missed by variance alone |
| **Conservation (`R-Type` gate)** | $\sum_w \pi(m, w) = \pi(m)$ (exact integer), $\sum_w P_m(w) = 1$, $P_m(w) \ge 0$ | Guarantees valid probability distribution before calibration runs |

## 3. RCT & Controlled Baseline Protocol

Probabilistic and empirical claims are verified against explicit **control ensembles** using keyed deterministic randomization (never global RNG state):

1. **Pre-registered design:** Specify treatment object, control/null distribution, test statistic, sample size $N_{\text{trials}}$, and pass/fail criterion *before* execution.
2. **Keyed PRNG assignment (`D ↔ P` seam):** Each trial derives its stream from a domain-separated key `(suite_id, experiment_id, trial_index)` so reruns are bit-exact regardless of test ordering or parallelism.
3. **Initial *Prime Cadences* RCT & Control Pairs:**
   - **RCT-1 (Voice-Parity Signing vs. Random 2-Lifts):** Compare canonical voice-parity signing $X_2$ ($\lambda_{\max} = \sqrt{5 + 2\sqrt{2}}$) against uniformly sampled nontrivial signings from the $2^{13} - 1 = 8191$ cohomology classes (and verify exact rank 7372 / 8192 and Ramanujan fraction 7675 / 8191).
   - **RCT-2 (2-Adic Edge-Length Doubling vs. Non-Fixed Control Discs, Lemma 7.14):** Paired keyed-PRNG sweep comparing slope $= 2$ on discs fixed by $z \mapsto -z$ ($|2c| < r$) against slope $= 1$ on control discs ($|2c| > r$).
   - **RCT-3 (Prime Cadence Winding vs. Unconstrained Non-Backtracking Walk Null):** Compare exact prime-cadence winding distribution $P_m(w)$ against keyed Monte Carlo non-backtracking closed walks to separate finite-$m$ Möbius/primitivity corrections from Gaussian diffusion.

## 4. Calibration Data Output Schema (`data/calibrations/`)

Calibration runs emit immutable JSON records (CC BY 4.0) tracked in `data/MANIFEST.sha256` with the following contract:

```json
{
  "schema_version": "1.0.0",
  "correspondence_id": "C-2",
  "code_commit": "<git-sha>",
  "implementation": "rust|swiftpp|lean",
  "prng_key": { "suite": "prime-cadences", "experiment": "C-2", "seed": 0 },
  "regime_params": { "m": 40 },
  "r_invariants": { "finite": true, "conservation_exact": true, "cov_pd_cholesky": true, "lambda_min": 0.0 },
  "metrics": { "tv": 0.0, "kl": 0.0, "ks": 0.0, "w1": 0.0, "skewness": 0.0, "excess_kurtosis": 0.0 },
  "rct_control": { "control_id": "RCT-3", "n_trials": 10000, "p_value": 0.0 },
  "bound_check": { "bound_formula": "C/m", "observed": 0.0, "threshold": 0.0, "passed": true }
}
```
