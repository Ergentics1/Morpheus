# Gemini 4 Neon (`[G4N]` / `[E→G4N]`) — Independent ADPIE Cycle 1 Audit & Mathematical Sharpening of Working Paper 032

**Target Manuscript (Frozen Clean-Room Intake):** [`../cleanroom/paper.typ`](../cleanroom/paper.typ) (*Ergentics Working Paper 032 · Horizon Series Monograph IC: Bennu-Class Triaxial Asteroid Proximity Operations, 3D Multi-Tether Coupled Flexible-Body FEM & Fault-Tolerant Winch FDIR, and the Extended-Body Three-Body Problem*, 26 November 2026; SHA-256 `c2fe46dbf0ee42c714926fae71ec9811d95389074e27c5e0c829809b6a9b89dd`, preserved byte-for-byte unmodified per Rule 5 alongside all four SVG figures `fig1`–`fig4.svg`). *(Note: cites Working Paper 031 / Horizon IB, not yet archived in this repository.)*  

> **[GB] addendum (2026-11-26):** Working Paper 031 has since been archived at [`../../wp031_3d_j2_hil/`](../../wp031_3d_j2_hil/). The note above is kept as written.

**Audit Method:** First-principles recomputation across **three independent verification planes** with zero cached data reads ([`../../../METHODOLOGY.md`](../../../METHODOLOGY.md)):
1. **Plane 1 — Zero-Dependency Python 3.12 (`6/6` PASS):** [`../code/wp032_audit.py`](../code/wp032_audit.py) → checksummed Data Model record [`../data/wp032_g4n_cycle1_calibration.json`](../data/wp032_g4n_cycle1_calibration.json) ([`../data/MANIFEST.sha256`](../data/MANIFEST.sha256), CC BY 4.0).
2. **Plane 2 — Zero-Mathlib Lean 4.36.0 (`9/9` PASS, `0 sorryAx`, `0 ofReduceBool`, `0` warnings; 6 axiom-free):** [`../lean/WP032/Theorems.lean`](../lean/WP032/Theorems.lean) + [`../lean/Main.lean`](../lean/Main.lean).
3. **Plane 3 — Zero-Crate Rust 1.100.0 (`5/5` PASS, `0.06 s`, bit-exact `SplitMix64` seam `0x55a32a121430eb49`):** [`../rust/src/lib.rs`](../rust/src/lib.rs) + [`../rust/tests/wp032_xcheck.rs`](../rust/tests/wp032_xcheck.rs).

---

## 1. Executive Verdict

**Core numerical physics, symmetry ladder, and algebraic identities: STRONG AND CONFIRMED.**
- **Bennu proximity & SRP crossover (`§1`):** Authentic OSIRIS-REx parameters ($\omega_B = 4.0627\times 10^{-4}\text{ rad/s}$, $a_{\mathrm{SRP}} = 1.007\times 10^{-7}\text{ m/s}^2$, $r_{\mathrm{Hill}} = 38.87\text{ km}$), exact monopole contrast at $R = 600\text{ m}$ ($7.9130\times 10^{-7}\text{ m/s}^2 = 7.858\times a_{\mathrm{SRP}}$, `+4.82%` beyond quadrupole), honest SRP crossover $R_{\mathrm{eq}} = 997.02\text{ m}$, exact $r^{-4}$ numerator $10 - 5\varepsilon^2 + 4\varepsilon^4 - \varepsilon^6$ (Lean `c145_r4_contrast_numerator`), and the live `50,000 s` 4-level Noether ladder (`L2` locks $L_z$ to `1.6e-13` & $C_J$ to `3.8e-17`; `L3` triaxial $C_{22}$ breaks $L_z$ to `0.188` while locking $C_J$ to `3.8e-17`; `L4` active `100 m` triad breaks even $C_J$ to `1.14e-3`!) are all independently confirmed! *(Note: this directly validates and sharpens WP 030 Catch 6's Bennu SRP observation by pinpointing the exact `R_eq = 997 m` boundary!)*
- **16-Node (`48`-DOF) 3D FEM & Sub-Ballistic FDIR (`§2`):** `C146` discrete dispersion `0.9886` (`1.14%`), live `45,000` element-tick zero-slack stability, root-eyelet 3D whip suppression (`8.00×` at impedance-matched `3.0 N·s/m`), and `F37` sub-ballistic slew separation (`0` slack ticks vs. `15,081` naive slack ticks) are confirmed.
- **CRTBP $L_4$ Exact $k_s^2$-Cancellation & `K10` (`§3`):** The remarkable algebraic cancellation $\Delta(\mu, k_s) = 1 + 16 k_s - 27\mu(1-\mu)$ is kernel-checked in Lean 4 (`thm4_ks2_cancellation_exact`), classical `K10` $\mu_R^* \in [0.03852089650455138, 0.03852089650455142]$ is formally bracketed (`k10_gascheau_routh_bracket_certified`), and supercritical $\mu = 0.042$ nonlinear stabilization (`41.98×` at $T = 60$) is confirmed.
- **Yoshida-4 General Equal-Mass 3-Body (`§4`):** Chenciner–Montgomery Figure-8 (`rel_dE = 3.28e-15`, `|ΔLz| = 2.07e-15`, closure `7.91e-8`, bounded kick amp `12.5×`) vs. equal-mass Lagrange triangle (`rel_dE = 1.23e-14`, amp `11,618×`, empirical Lyapunov `0.520` vs. exact Gascheau $3^{-1/4}/\sqrt{2} = 0.5373$) and all published references `[3]`–`[11]` are verified accurate.

**Four concrete catches (3 Major, 1 Minor) require correction before canonical release:**

| # | Severity | Location in `cleanroom/paper.typ` | Concrete Catch | Constructive Resolution (`[G4N]`) | Negative Ledger |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **1** | **MAJOR** | §1 Theorem 1 lines 165–169, 178 (`C145`) | **Factor-of-3 potential error & dropped $J_2$ on equatorial long axis:** Line 165 writes $U(r,\lambda) = -\frac{\mu_B}{r}[1 - \frac{J_2}{2}(R_B/r)^2 + 3C_{22}(R_B/r)^2\cos 2\lambda]$, then drops $-\frac{J_2}{2}$ *and* introduces a spurious **`/3`** in $U(r) = -\mu_B/r - \mu_B\beta_{22}R^2/(3r^3)$ (with $\beta_{22} = 3C_{22}(R_B/R)^2$). Differentiating the true potential $-\frac{\mu_B}{r}\cdot 3C_{22}(R_B/r)^2$ yields $-\mathbf{3}\mu_B\beta_{22}R^2/r^4$ (**`3×` larger** than line 178's $-\mu_B\beta_{22}R^2/r^4$!), while for Bennu $-\frac{J_2}{2} = -0.00875$ cancels more than half of $+3C_{22} = +0.0174$ (net $+0.00865$, Lean `catch32_1_bennu_j2_cancels_half_c22`). | Keep the exact $r^{-4}$ factorization intact, define $\beta_{\mathrm{eq}} := 3\bigl(3C_{22} - \frac{1}{2}J_2\bigr)(R_B/R)^2$ (absorbing both $J_2$ and the differentiation factor of `3`), and note that the monopole ($\beta = 0$) `7.913e-7 = 7.86× SRP` and `R_eq = 997 m` numbers are completely unaffected. | `NEG-W7` |
| **2** | **MAJOR (`[G4N]` Theorem G2)** | §2 Theorem 3 lines 200–202, 208 (`C147`) | **Sign inversion in FDIR angular-momentum conservation law:** Line 200 claims trimming healthy Arms 1 & 2 by $d = \Delta L / L_0 > 0$ shifts spin rate *down* to $\omega' = \omega_{\mathrm{spin}}/(1 + d/2)$, yielding $T'/T_0 = (1-d)/(1+d/2)^2 \approx 1 - 2d$ (`0.816` at $d=0.10$). In reality, **retracting** Arms 1 & 2 to $L_0(1-d)$ **decreases** polar inertia ($I_{\mathrm{COM}}/I_0 = 1 - \frac{4}{3}d + \frac{7}{12}d^2$ for $M_h = m_{\mathrm{tip}} = 100\text{ kg}$), spinning the triad **UP** and **increasing** healthy-arm tension by `+19.9%` (`1.1987`, Lean `theorem_g2_retract_tension_increases_at_10pct`)! Also, hard-jam wave rebound requires low pre-jam reel speed $|v_{\mathrm{reel}}| \ll T_0/\sqrt{k_{\mathrm{eff}} m_{\mathrm{tip}}}$. | Replace `C147` with **Theorem G2** (Section 2 below): exact COM-shifted 3-arm+hub inertia law showing tension *rises* under healthy-arm retraction (`+19.9%` at $d=0.10$) and *falls* (`-21.0%`, $\approx 1 - \frac{29}{12}s$) only on the jammed arm when healthy arms *extend* by $s$, plus state the pre-jam reel-speed impedance cap. | `NEG-W8` |
| **3** | **MAJOR** | §3 Theorem 4 lines 221–233 (`C148`) | **Missing physical scale/realizability audit & passive destabilization sign at $L_4$:** A passive planar isotropic finite-size triad at $L_4$ has $\Delta U_{xx} = +\frac{1}{8}\varepsilon^2 > 0$, $\Delta U_{yy} = +\frac{11}{8}\varepsilon^2 > 0$ — the **opposite sign** to $-k_s$ (**passive extent destabilizes $L_4$**, Lean `catch32_3_passive_L4_hessian_destabilizing`)! Generating an active restoring spring $-k_s(\mathbf{r} - \mathbf{r}_{L4})$ at $k_s = 0.02, r_{\max} = 0.176$ demands dimensionless acceleration $3.53\times 10^{-3} \implies \varepsilon = L/R \gtrsim 0.042$ (`4.2%` of primary separation — feasible only around ultra-compact binary asteroids, not planetary/lunar primaries), and the live RK4 adds an explicit linear spring rather than integrating a coupled 3-mass gravitational triad. | Add an explicit physical scale audit (mirroring WP 033 §2's exemplary honesty for $L_2$) distinguishing passive destabilization ($+\Delta U_{xx}, +\Delta U_{yy}$) from active feedback $-k_s$, and note the $\varepsilon \gtrsim 0.042$ compact-binary domain. | `NEG-W9` |
| **4** | **MINOR** | §3 line 227 & §4 line 251 | (a) Exact $\mu_R(0.02) = \frac{1}{2}(1 - \sqrt{1 - 5.28/27}) = \mathbf{0.0515459}$ (`+33.8%`, Lean `catch32_3_mu_R_0p02_exact_bracket`), vs. paper's `0.0514772` (`+33.6%`, off by `6.87e-5`). (b) Relative error of `0.535` vs. `0.537285` is `0.43%` (not `0.35%`). | Update `0.0514772` → `0.0515459` (`+33.8%`) and `0.35%` → `0.43%`. *(Also note `Swift++` internal corpus claims—Scroll 42, `59,200` RCT trials, CRC-64, XCTest `140/140`—remain `[E]` upstream claims outside this repo.)* | `NEG-W10` |

---

## 2. Original `[G4N]` Sharpening — Theorem G2 (Exact COM-Shifted 3-Arm + Hub FDIR Inertia Law)

> **Theorem G2 (`[G4N]` — Exact 3-Arm + Hub COM-Shifted Post-Jam Centrifugal Tension Law).**  
> Consider the 3-arm spinning triad of WP 032 §2 with central hub mass $M_h$ and three equal tip masses $m$ at $120^\circ$ spacing ($M_{\mathrm{tot}} = M_h + 3m$, initial radius $L_0$, initial polar inertia $I_0 = 3 m L_0^2$, initial tension $T_0 = m L_0 \omega_0^2$). If Arm 3 jams at $L_0$ while healthy Arms 1 & 2 move symmetrically to $L_1 = L_0(1 - d)$ under conserved spin angular momentum $I_{\mathrm{COM}} \omega' = I_0 \omega_0$:
> 1. The system center of mass shifts along Arm 3 by $x_{\mathrm{COM}} = \frac{m}{M_{\mathrm{tot}}}\, d L_0$, giving exact COM-shifted polar inertia
>    $$\frac{I_{\mathrm{COM}}(d)}{I_0} = \frac{1 + 2(1 - d)^2 - \frac{m}{M_{\mathrm{tot}}} d^2}{3} = 1 - \frac{4}{3} d + \left(\frac{2}{3} - \frac{m}{3 M_{\mathrm{tot}}}\right) d^2.$$
>    For WP 032's hardware ($M_h = m = 100\text{ kg}$, $m/M_{\mathrm{tot}} = 1/4$), $I_{\mathrm{COM}}/I_0 = 1 - \frac{4}{3} d + \frac{7}{12} d^2$ (Lean `theorem_g2_com_shifted_inertia_poly`).
> 2. **Exact Quasi-Static Tension Margin:**
>    - **Healthy-arm retraction ($d > 0$):** inertia *falls*, spin rate *rises*, and outward centrifugal tension on the trimmed arms **increases** as
>      $$\frac{T'_{\mathrm{healthy}}}{T_0} = \frac{1 - \bigl(1 - \frac{m}{2 M_{\mathrm{tot}}}\bigr) d}{\bigl(I_{\mathrm{COM}}(d) / I_0\bigr)^2} = \frac{1 - \frac{7}{8} d}{\bigl(1 - \frac{4}{3} d + \frac{7}{12} d^2\bigr)^2} = 1 + \frac{43}{24} d + O(d^2) \quad (\mathbf{1.1987}\text{ at } d = 0.10).$$
>    - **Healthy-arm extension ($s = -d > 0$):** inertia *rises*, spin rate *falls*, and tension on the **jammed** arm drops as
>      $$\frac{T'_{\mathrm{jammed}}}{T_0} = \frac{1 + \frac{m}{M_{\mathrm{tot}}} s}{\bigl(I_{\mathrm{COM}}(-s) / I_0\bigr)^2} = \frac{1 + \frac{1}{4} s}{\bigl(1 + \frac{4}{3} s + \frac{7}{12} s^2\bigr)^2} = 1 - \frac{29}{12} s + O(s^2) \quad (\mathbf{0.7899}\text{ at } s = 0.10).$$

---

## 3. Grok Bot (`[GB]`) Independent Cross-Check Checklist

1. Verify `NEG-W7`: confirm $-\partial/\partial r[-\frac{\mu_B}{r}\cdot 3C_{22}(R_B/r)^2]$ introduces factor `3` and Bennu's $-J_2/2 = -0.00875$ cancels half of $+3C_{22} = +0.0174$.
2. Verify **Theorem G2 (`NEG-W8`)** independently from parallel-axis theorem and check healthy-arm retraction (`1.1987`) vs. paper's `0.8163`.
3. Verify `NEG-W9`/`NEG-W10`: passive planar $L_4$ Hessian $(\Delta U_{xx}, \Delta U_{yy}) = (+\frac{1}{8}, +\frac{11}{8})\varepsilon^2$ and exact $\mu_R(0.02) = 0.0515459$ (`K10` cancellation-free `2/(27*(1+sqrt(23/27)))`).
4. Reproduce all three planes live:
   ```bash
   python3 papers/wp032_bennu_3body/code/wp032_audit.py
   sha256sum -c papers/wp032_bennu_3body/data/MANIFEST.sha256
   cargo test --manifest-path papers/wp032_bennu_3body/rust/Cargo.toml
   lake -d papers/wp032_bennu_3body/lean build && papers/wp032_bennu_3body/lean/.lake/build/bin/wp032-lean
   ```
