# Small-Body Triaxial Proximity Operations, Three-Dimensional Extended-Body CRTBP Invariant Manifolds, and Bennu Touch-and-Go Guidance

**Author:** Ergentics  
**Series:** Horizon Synthesis — Piece II (synthesizing frozen clean-room `WP 032` + `WP 033`)  
**Canonical LaTeX / PDF:** [`paper/piece2_smallbody_crtbp.tex`](paper/piece2_smallbody_crtbp.tex) · [`paper/piece2_smallbody_crtbp.pdf`](paper/piece2_smallbody_crtbp.pdf) · [`arxiv/piece2-smallbody-crtbp-arxiv.tar.gz`](arxiv/piece2-smallbody-crtbp-arxiv.tar.gz)  
**Open Reference Code & Data:** [`code/piece2_sim.py`](code/piece2_sim.py) (`6/6 PASS`) · [`data/piece2_calibration.json`](data/piece2_calibration.json) · [`data/MANIFEST.sha256`](data/MANIFEST.sha256)

---

## Abstract

We synthesize and reconcile the small-body proximity, multi-body astrodynamics, and Touch-and-Go (TAG) guidance analyses of the Horizon clean-room manuscripts `WP 032` and `WP 033`, resolving all confirmed audit findings (`NEG-W7`–`NEG-W14`, `NEG-W29`) in place with an open, zero-dependency 42-ODE and symplectic reference suite (`code/piece2_sim.py`, `6/6 PASS`):

1. **Corrected Bennu equatorial potential (`NEG-W7`):** Including $-J_2/2 = -0.00875$ alongside $+3C_{22} = +0.0174$ halves the net equatorial coupling to `+0.00865`, giving $\Delta a = 7.913\times 10^{-7}\text{ m/s}^2$ (`7.86×` solar radiation pressure) at $R = 600\text{ m}$ ($L = 20\text{ m}$) and exact SRP crossover at $R_{\mathrm{eq}} = 997.02\text{ m}$.
2. **Theorem G2 post-jam FDIR tension inversion (`NEG-W8`):** Retracting healthy Arms 1 & 2 by `10%` ($d = +0.10$) spins the 3-arm+hub spacecraft up ($I_{\mathrm{cm}}/I_0 = 0.8725$) and **increases** jammed Arm 3 tension by **`+28.1%`** ($T_3/T_0 = 1.2808$), whereas **extending** healthy arms by `10%` ($d = -0.10$) lowers jammed-arm tension by **`-21.0%`** ($T_3/T_0 = 0.7899$).
3. **CRTBP $L_4$ scale audit & Yoshida-4 Figure-8 (`NEG-W9`, `NEG-W10`):** Exact isotropic critical mass ratio is $\mu_R(0.02) = 0.0515459$ (`+33.81%`, vs. `0.0514772`); Gascheau Lyapunov exponent at $\mu=0.5$ is `0.537285` (`0.425%` error). Passive finite-size $L_4$ curvature is `11:1` anisotropic ($\delta U_{yy}/\delta U_{xx} = 11.0$), so isotropic stabilization requires active modulation of span $\epsilon \ge 0.04195$. Open Yoshida-4 Figure-8 achieves 2-period closure `3.99e-8` and `max |ΔE| = 4.01e-11`.
4. **Theorem G3 coupled 3D $L_2$ multipole tensor & Didymos scale audit (`NEG-W12`):** Laplace's equation forbids decoupled vertical stiffness; evaluating the full 3D Hessian at Didymos–Dimorphos $L_2$ ($\mu = 0.0091$) shows a **$y$-aligned triad closes the Halo gap at $L_y^* = 40.44\text{ m}$** while maintaining **`107.0 m`** surface altitude (more than double a $50\text{ m}$ $x$-boom's `52.5 m`).
5. **Open 42-ODE Earth–Moon $L_2$ Halo, elevated safe $W^u$ branch, & Floquet SK (`NEG-W11`):** Confirms $\tau = 0$ departure impacts the Moon (`r_p = 993.8 km < 1,737.4 km` in `17.59 days`), discovers an **elevated non-impacting lunar-capture $W^u$ branch at $\tau = 0.750$** (`r_p = 2,064.6 km`, **`+327.2 km` altitude** in `18.10 days`), and achieves **`8,814×`** Floquet station-keeping error suppression (`169.9 km` peak error over 6 orbits for `2.95 m/s` $\Delta v$).
6. **Bennu TAG fluidized regolith & keyed 200-trial MC (`NEG-W13`, `NEG-W14`):** Under fluidized OSIRIS-REx subsurface density `500–700 kg/m^3` (`A_h = 28.274 m^2`, `C_D = 1.60`) and full $1/r^2$ + `15.71%` centrifugal relief ($\eta_{\mathrm{flight}} = 1.617$, $\chi(600) = 10.88$), Coriolis drift increases from `15.99 m` to **`18.81 m`** (`+17.6%`), nominal sinkage at `600 kg/m^3` is **`18.24 cm`**, and keyed `MC200` passes **`200/200 SAFE`** (median `18.21 cm`, p95 `21.86 cm`, digest `0xaa33ca849e87e22b`).

---

## 1. Corrected Bennu Triaxial Potential (`NEG-W7`)

Along Bennu's equatorial long axis,
$$U_{\mathrm{eq}}(r) = -\frac{\mu_B}{r} - \frac{\mu_B R_0^2}{r^3}\left(3 C_{22} - \frac{J_2}{2}\right), \qquad 3C_{22} - \frac{J_2}{2} = 0.0174 - 0.00875 = +0.00865.$$
At $R = 600\text{ m}$ ($L = 20\text{ m}$), $\beta_{\mathrm{eq}} = 0.004362$ and exact $\Delta a = 7.9130\times 10^{-7}\text{ m/s}^2 = 7.858\times$ SRP, with exact SRP crossover at $R_{\mathrm{eq}} = 997.02\text{ m}$.

---

## 2. Theorem G2: Post-Jam Winch FDIR Tension Inversion (`NEG-W8`)

**Theorem 2.1 (Theorem G2)** `[G4N]`: For a spin-stabilized equilateral 3-arm+hub tether spacecraft ($m_h = m_t$, $M_{\mathrm{tot}} = 4m_t$, $I_0 = 3 m_t L_0^2$) with Arm 3 jammed at $L_0$ and healthy Arms 1 & 2 retracted by $d = \Delta L/L_0$ ($L_{1,2} = (1-d)L_0$, barycenter shift $c_x = \frac14 d L_0$), exact parallel-axis algebra gives (verified to `2.22e-16`):
$$\frac{I_{\mathrm{cm}}(d)}{I_0} = 1 - \frac{4}{3}d + \frac{7}{12}d^2, \qquad \frac{T_3(d)}{T_0} = \left(1 - \frac{d}{4}\right)\!\left(\frac{I_0}{I_{\mathrm{cm}}(d)}\right)^2, \qquad \frac{T_{1,2}(d)}{T_0} = \left(1 - \frac{7d}{8}\right)\!\left(\frac{I_0}{I_{\mathrm{cm}}(d)}\right)^2.$$
- **Retracting ($d = +0.10$):** $I_{\mathrm{cm}}/I_0 = 0.8725$ (spin-up), $T_{1,2}/T_0 = 1.1987$ (`+19.9%`), **$T_3/T_0 = 1.2808$ (`+28.1%` overload!)**.
- **Extending ($d = -0.10$, safe FDIR law):** $I_{\mathrm{cm}}/I_0 = 1.1392$ (spin-down), $T_{1,2}/T_0 = 0.8380$ (`-16.2%`), **$T_3/T_0 = 0.7899$ (`-21.0%` relief!)**.

*(Figure 1: `paper/figures/fig1_fdir_g2_and_didymos_g3.pdf`.)*

---

## 3. Extended-Body CRTBP: $L_4$ Scale Audit, Figure-8, and Theorem G3

- **$L_4$ Routh Criticality (`NEG-W9`, `NEG-W10`):** Point-mass $\mu_R(0) = 0.0385209$; isotropic $k_s = 0.02$ gives exact $\mu_R(0.02) = 0.0515459$ (`+33.81%`). Exact Gascheau Lyapunov exponent at $\mu=0.5$ is `0.537285` (`0.425%` error vs. `WP 032`'s `0.535`). Passive finite-size $L_4$ quadrupole Hessian has `11:1` anisotropy ($\delta U_{yy}/\delta U_{xx} = 11.0$), so isotropic $k_s = 0.02$ requires active modulation at minimum span $\epsilon_{\min} = 0.04195$.
- **Open Yoshida-4 Figure-8 (`D3`):** 2-period closure `3.99e-8`, `max |ΔE| = 4.01e-11`, 2-period kick amplification `54.01×`.
- **Theorem G3 (Coupled 3D $L_2$ Multipole Tensor, `NEG-W12`)** `[G4N, X]`:

### Table 1: Exact Coupled 3D $L_2$ Multipole Sensitivities (Earth–Moon $L_2$, $\gamma_2 = 0.167833$, $c_2 = 3.190425$)

| Triad alignment | $\Delta\omega_{xy}^2/\epsilon^2$ | $\Delta\omega_z^2/\epsilon^2$ | $\Delta(\omega_{xy}^2 - \omega_z^2)/\epsilon^2$ | Effect on Halo gap |
|---|---:|---:|---:|---|
| $x$-aligned | `+4.0802` | `+4.0000` | `+0.0802` | slightly widens |
| **$y$-aligned (transverse)** | **`-3.3748`** | **`-1.0000`** | **`-2.3748`** | **optimal gap closure** |
| $z$-aligned | `-0.7054` | `-3.0000` | `+2.2946` | widens strongly |
| Equilateral ($xy$-plane) | `+0.3527` | `+1.5000` | `-1.1473` | moderate closure |

At **Didymos–Dimorphos $L_2$** ($\mu = 0.0091$, $\gamma_2 = 0.151684$, $L_2$ distance `180.50 m` from Dimorphos of radius `78 m`), the exact nonlinear 3-mass Hessian shows a $y$-aligned triad closes the Halo gap at **$L_y^* = 40.44\text{ m}$** with **`107.0 m`** surface altitude (vs. `52.5 m` for a `50 m` $x$-boom).

---

## 4. Open 42-ODE Earth–Moon $L_2$ Halo, Safe $W^u$ Branch, and Floquet SK (`R1`)

- **Halo Orbit (`R1`):** Periodic closure `1.63e-8`, symplectic residual `6.51e-10`, $\lambda_u = 746.7213$, Broucke indices $\nu_1 = 373.3613, \nu_2 = 0.840930$, winding `32.76°/orbit`.
- **Direct Impact vs. Elevated Safe $W^u$ Branch (`NEG-W11`):**
  - $\tau = 0$: direct lunar impact $r_p = 993.8\text{ km} < R_{\mathrm{Moon}} = 1{,}737.4\text{ km}$ in `17.59 days`.
  - **$\tau = 0.750$ (elevated safe branch):** non-impacting lunar capture **$r_p = 2{,}064.6\text{ km}$ (`+327.2 km` altitude)** in `18.10 days`.
- **Floquet Station-Keeping:** 6-orbit total $\Delta v = 2.95\text{ m/s}$, max position error `169.9 km` vs. `1,497,816 km` free 3-orbit divergence (**`8,814×`** suppression). *(Figure 2: `paper/figures/fig2_halo_wu_lunar_clearance.pdf`.)*

---

## 5. Bennu Touch-and-Go Fluidized Regolith & Keyed Monte Carlo (`P1`)

### Table 2: Reconciled Bennu TAG Parameters & Keyed `MC200` (`seed = 0x484f52495a5f5032`) `[G4N, X]`

| TAG Metric | Value | Regime | Audit Resolution |
|---|---:|---|---|
| Surface gravity $g_{\mathrm{surf}}$ [m/s²] | `8.084e-5` | Bennu equator | `15.71%` centrifugal relief ($a_{\mathrm{cent}}=1.270\times 10^{-5}$) |
| Coriolis drift (const-$g$ vs. full) [m] | `15.99` vs. **`18.81`** | $\eta_{\mathrm{flight}} = 1.617$ | `+17.6%` full-model drift (`NEG-W14`) |
| Sinkage at $\rho = 1{,}190\text{ kg/m}^3$ [cm] | `11.58` | $\chi = 21.59$ | Bulk-density baseline |
| **Sinkage at $\rho = 600\text{ kg/m}^3$** [cm] | **`18.24`** | $\chi = 10.88$ | Fluidized nominal ($A_h = 28.274\text{ m}^2$, $C_D = 1.60$) |
| Fluidized band (`500–700 kg/m^3`) [cm] | `20.42–16.53` | OSIRIS-REx subsurface | Lauretta/Walsh 2022 (`NEG-W13`) |
| Keyed `MC200` median / p95 sink [cm] | `18.21 / 21.86` | **`200/200 SAFE`** | p95 lateral `0.905 m`; digest `0xaa33ca849e87e22b` |

*(Figure 3: `paper/figures/fig3_bennu_tag_density_sensitivity.pdf`.)*

---

## Appendix A: Epsilon (`Swift++`) Provenance

`[E, X]` Internal `Swift++` Library of Alexandria Epochs XXXVIII–XXXIX ledgers (`INT-032`, `INT-033`) and Lean 4.36.0 integer/rational-bracket algebraic certificates (`NEG-W29`) are preserved transparently as author provenance while `code/piece2_sim.py` and `data/piece2_calibration.json` serve as the open canonical verification record resolving `NEG-W7`–`NEG-W14` and `NEG-W29` in place.
