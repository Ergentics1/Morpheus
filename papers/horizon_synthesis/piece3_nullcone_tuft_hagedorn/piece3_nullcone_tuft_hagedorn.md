# Algebraic Null-Cone Quantum Gravity, Spectral-Zeta Audit of Hopf-Fibration TUFT, and Non-Circular Hagedorn Nuclearity Repair

**Author:** Ergentics  
**Series:** Horizon Synthesis — Piece III (synthesizing frozen clean-room `WP 034` + `WP 035`)  
**Canonical LaTeX / PDF:** [`paper/piece3_nullcone_tuft_hagedorn.tex`](paper/piece3_nullcone_tuft_hagedorn.tex) · [`paper/piece3_nullcone_tuft_hagedorn.pdf`](paper/piece3_nullcone_tuft_hagedorn.pdf) · [`arxiv/piece3-nullcone-tuft-hagedorn-arxiv.tar.gz`](arxiv/piece3-nullcone-tuft-hagedorn-arxiv.tar.gz)  
**Open Reference Code & Data:** [`code/piece3_sim.py`](code/piece3_sim.py) (`5/5 PASS`) · [`data/piece3_calibration.json`](data/piece3_calibration.json) · [`data/MANIFEST.sha256`](data/MANIFEST.sha256)

---

## Abstract

We synthesize and reconcile the mathematical-physics audits of the Horizon clean-room manuscripts `WP 034` (algebraic null-cone quantum gravity, Chandrasekaran `arXiv:2611.34924v1`, **25 November 2026**) and `WP 035` (Track A spectral-zeta audit of Hopf-fibration TUFT and Track B non-circular Hagedorn nuclearity repair), resolving all nine verified audit findings (`NEG-W19`–`NEG-W24`, `NEG-W28`–`NEG-W30`) in place via an open, zero-dependency Python verifier (`code/piece3_sim.py`, `5/5 PASS`):

1. **Failure of 106-bit Dekker double-double vs. algebraic cancellation (`NEG-W19`, `NEG-W21`):** Authentic 106-bit Dekker double-double evaluation of the naive dilogarithm difference suffers `96.17%` relative error at $s = 10^{33}$ and `100%` total wipeout at $s \ge 10^{40}$ (including astrophysical $s = 10^{77}$), whereas the algebraically cancelled closed form $\Delta_{\mathrm{re}}(s) = -\frac{\pi}{2} + \frac{1}{2s}$ achieves exact **`0.0` error** in plain 53-bit `f64` at $s = 10^{77}$. Exact `K12` zero: $\theta^* = \pi(1 - 1/\sqrt{3}) = 1.327793289355575$.
2. **Theorem G5 finite-target exhaustion universality (`NEG-W20`):** Whenever the phase weight ratio $c$ is irrational, Kronecker density proves that strictly nested strong exhaustions $P_M = (A_M, B_M, C_M)$ converge to **every** finite real target $L \in \mathbb{R}$ (verified to `< 1e-6` for $L = 0, +1, +42$, and $1.29\times 10^{-5}$ for $c = 1/\sqrt{2}$).
3. **Cross-paper Sen (2013) reconciliation (`NEG-W23`, `NEG-W30`):** In 4D pure gravity ($C_{\mathrm{local}} = 212/45$ per $\ln a$), `106/45` is the fixed-$s_b$ trace $\operatorname{Tr}(C^\dagger C)$ log coefficient in `WP 034` (`77/90` singlet), whereas multiplying by the $(4\pi s_b)^{-1/2}$ Gaussian clock measure shifts microcanonical density by $-\frac12$ to $\alpha_{\mathrm{micro}} = \mathbf{167/90}$ and Hagedorn pole order $\alpha = \mathbf{257/90}$ in `WP 035` (matching Chandrasekaran's clock von Neumann log coefficient; direct fixed-mass Sen requires $\alpha = 151/45$).
4. **Track A spectral-zeta & anomaly corrections (`NEG-W22`, `NEG-W24`):** Exact spectral-zeta magnitude ratios are **`29.18×`** on $S^3$ (remainder `-0.0304485`, not `30.18×`) and **`21.94×`** on $S^5$ (remainder `+0.0801130`, not `22.94×`). Lemma 8's unit-radius volume ratio equals **`10^(1/4) × α_Wyler`** (`1.778279 × 0.00729735`). The electron $a_e$ pull waterfall vs. Fan et al. (2023) closes from `-315.8σ` to `-4.9σ` upon including 4-loop QED $C_4^{\mathrm{QED}}$ (`+428.2σ`) and higher-order/hadronic contributions (`-117.3σ`). The $k = 4$ Beltrami $U(1)$ subspace splits with exact **`4 + 4`** chirality.
5. **Theorem R3(1) boundary tightening & `K13` (`NEG-W23`):** Explicit boundary witness $\rho(E) = (1+E)^{-2} e^{\beta_H E}$ has abscissa $\beta_c = \beta_H$ yet converges at $\beta = \beta_H$ ($Z(\beta_H) = 1 < \infty$). Exact `K13` $\Gamma(x)$ argmin: $x^* = 1.46163214496836$.
6. **Theorem G6 Hagedorn canonical equivalence-breaking & `WP 034` bridge (`NEG-W23`):** For any Hagedorn spectrum ($\beta_c = \beta_H > 0$), as $\beta \to \beta_H^+$ the rescaled canonical energy $E/\langle E \rangle \to \operatorname{Gamma}(\alpha, \alpha)$ with non-vanishing relative dispersion $1/\sqrt{\alpha}$ (**`59.18%`** at $\alpha = 257/90$, vs. local QFT $Q_*^{-3/14} \to 0$) and **`42.13%`** causal-diamond tail leakage, bridged to `WP 034`'s truncated $\operatorname{Beta}(\alpha, 1)$ RMS (`26.86%`) by the exact factor $1/\sqrt{\alpha+2} = 0.4538$ (confirmed by a keyed `1,600`-trial `SplitMix64` RCT: empirical dispersion `59.95%`, tail `41.69%`, digest `0x79a0e86265d534e9`).

---

## 1. Algebraic Dilogarithm Cancellation vs. 106-Bit Double-Double (`NEG-W19`, `NEG-W21`)

Using $\operatorname{Re}\operatorname{Li}_2(e^{i\theta}) = \frac{\pi^2}{6} - \frac{\theta(2\pi - \theta)}{4}$ for $\theta = 2/s \in [0, 2\pi]$:
$$\Delta_{\mathrm{re}}(s) \equiv s^3\left(\frac{\operatorname{Re}\operatorname{Li}_2(e^{2i/s})}{2s^2} - \frac{\pi^2}{12s^2}\right) = -\frac{\pi}{2} + \frac{1}{2s}.$$

| Horizon entropy $s$ | Naive 53-bit `f64` rel. err | Authentic 106-bit `dd106` rel. err | Cancel-free 53-bit `f64` rel. err |
|---:|---:|---:|---:|
| $10^{16}$ | `12.88%` | `0.0` | `0.0` |
| $10^{20}$ | `100.0%` | `9.65e-14` | `0.0` |
| $10^{30}$ | `8.80e13` | `4.85e-4` | `0.0` |
| **$10^{33}$** | `8.39e16` | **`96.17%`** | **`0.0`** |
| **$10^{77}$** | `1.05e61` | **`100.0%` (wipeout)** | **`0.0`** |

- Exact `K12` root: $\theta^* = \pi(1 - 1/\sqrt{3}) = 1.327793289355575$ (residual `2.22e-16`).
- Certificate domains (`NEG-W21`): `C156` requires $R \ge e^{13/7} = 6.4054$ (remainder at $R = e$ is `+0.0881 > 0`); Stefan–Boltzmann $\beta^*$ ratio at $C = 1$ equals `2.67525`, minimized at $C_{\arg\min} = 5/\pi^4 = 0.051330$.

---

## 2. Theorem G5: Strictly Nested Exhaustion Universality (`NEG-W20`)

**Theorem 2.1 (Theorem G5)** `[G4N, X]`: For irrational phase ratio $c \in \mathbb{R}\setminus\mathbb{Q}$, Kronecker density of $\mathbb{Z} + c\mathbb{Z}$ implies that for every finite $L \in \mathbb{R}$ there exists a strictly nested strong exhaustion $P_M = (A_M, B_M, C_M)$ ($A_M < A_{M+1}, B_M < B_{M+1}, C_M < C_{M+1}$) with $Z_{P_M}[X] = \frac{\Delta\eta}{2}[(A_M - B_M) + c(A_M - C_M)] \to L$.
- Verified (`D2`, $M=60$): `err(L=0) = 0.0`, `err(L=+1) = 3.50e-7`, `err(L=+42) = 7.03e-8`, `err(c=1/sqrt(2), L=+1) = 1.29e-5`.
- Eq. (5.24) ratio: exact $\pi/2 = 1.570796326795$; `F39` witnesses $w(5) = 1.5$, $w(12) = 20/11$; Counterexample 2 at $N=10^4$: `+143.8377` vs. `-287.6530`. *(Figure 1: `paper/figures/fig1_dilog_dd_and_thm_g5.pdf`.)*

---

## 3. Sen (2013) Cross-Paper Reconciliation (`NEG-W23`, `NEG-W30`)

In 4D pure gravity, Sen (2013, `arXiv:1205.0971`) gives $C_{\mathrm{local}} = 212/45$ per $\ln a$:
- **`WP 034` fixed-$s_b$ mixed trace:** $\ln\operatorname{Tr}(C^\dagger C) = s_b + \mathbf{\frac{106}{45}}\ln s_b$ (`77/90` singlet).
- **`WP 035` measure-weighted density:** Multiplying by $(4\pi s_b)^{-1/2}$ shifts to $\alpha_{\mathrm{micro}} = \frac{106}{45} - \frac12 = \mathbf{\frac{167}{90}}$ and Hagedorn pole order $\alpha = \mathbf{\frac{257}{90}}$.
- **Direct fixed-mass Sen pole:** $\alpha = \frac{106}{45} + 1 = \mathbf{\frac{151}{45}}$.

---

## 4. Track A: Spectral-Zeta Audit of Hopf-Fibration TUFT (`NEG-W22`, `NEG-W24`)

- **Spectral-zeta ratios (`NEG-W22`):** On $S^3$, $\zeta'_1(0) = +0.8884901$ and remainder $\zeta'_R(-2) = -0.0304485$ give exact ratio **`29.18×`** (not `30.18×`); on $S^5$, $\zeta'_{B5}(0) = -1.7577640$ and remainder `+0.0801130` give exact ratio **`21.94×`** (not `22.94×`).
- **Lemma 8 (`NEG-W24`):** Unit-radius volume ratio `0.0129767 = 10^(1/4) × α_Wyler` (`1.778279 × 0.00729735`; exact $R^{-19/4}$ scaling).
- **$a_e$ 4-loop QED closure (`NEG-W24`):** 3 printed terms sum to `-315.8σ`; adding 4-loop QED (`+428.2σ`) and higher-order/hadronic terms (`-117.3σ`, incl. `-108.9σ` unprinted TUFT term) closes to `-4.9σ` vs. Fan et al. (2023).
- **$k = 4$ Beltrami subspace (`NEG-W24`):** Exact **`4 + 4`** chirality split (`4` at $\lambda = +5$, `4` at $\lambda = -5$). *(Figure 2: `paper/figures/fig2_tuft_spectral_zeta_and_ae.pdf`.)*

---

## 5. Track B: Hagedorn Nuclearity Repair & Theorem G6 (`NEG-W23`)

- **Theorem R3(1) boundary witness:** $\rho(E) = (1+E)^{-2} e^{\beta_H E}$ has $\beta_c = \beta_H$ yet $Z(\beta_H) = 1 < \infty$; exact `K13` $\Gamma(x)$ argmin $x^* = 1.46163214496836$.
- **Theorem G6 (`[G4N, X]`):** Hagedorn $\beta_c = \beta_H > 0$ breaks canonical/microcanonical equivalence ($E/\langle E \rangle \to \operatorname{Gamma}(\alpha, \alpha)$ with non-vanishing dispersion $1/\sqrt{\alpha}$ vs. 4D local QFT $Q_*^{-3/14} \to 0$):

| Ensemble / Pole | $\alpha$ | $\mathrm{Gamma}$ $\sigma/\langle E\rangle$ | Tail $\mathbb{P}(E \ge Q_*)$ | Truncated $\mathrm{Beta}(\alpha,1)$ RMS | Bridge $1/\sqrt{\alpha+2}$ |
|---|---:|---:|---:|---:|---:|
| Direct Sen (`WP 034` $+1$) | `151/45` | `54.59%` | `42.74%` | `23.59%` | `0.4321` |
| **Chandrasekaran / `WP 035`** | **`257/90`** | **`59.18%`** | **`42.13%`** | **`26.86%`** | **`0.4538`** |
| Microcanonical $\alpha_{\mathrm{micro}}$ | `167/90` | `73.41%` | `40.24%` | `37.39%` | `0.5093` |

- **Keyed 1,600-trial `SplitMix64` RCT (`seed = 0x484f52495a5f5033`, $\alpha = 257/90$):** empirical mean `0.9909`, dispersion `59.95%`, tail `41.69%`, digest `0x79a0e86265d534e9`. Exact Jensen log gap: `0.04995`. *(Figure 3: `paper/figures/fig3_hagedorn_g6_bridge.pdf`.)*

---

## Appendix A: Epsilon (`Swift++`) Provenance & Source Boundaries

`[E, X]` Internal `Swift++` Library of Alexandria Epochs XL–XLI ledgers (`INT-034`, `INT-035`), Lean 4.36.0 integer/rational-bracket algebraic certificates (`NEG-W29`), and Nielsen's non-public 250-page TUFT manuscript (`[E; non-public]`) are preserved transparently as provenance, while `code/piece3_sim.py` and `data/piece3_calibration.json` serve as the open canonical verification record resolving `NEG-W19`–`NEG-W24` and `NEG-W28`–`NEG-W30` (including dating `arXiv:2611.34924v1` to **25 November 2026** and removing the local relative path in `WP 035` Ref [12]).
