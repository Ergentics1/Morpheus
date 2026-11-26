# Gemini 4 Neon (`[G4N]` / `[E→G4N]`) — Independent ADPIE Cycle 1 Audit & Mathematical Sharpening of Working Paper 033

**Target Manuscript (Frozen Clean-Room Intake):** [`../cleanroom/paper.typ`](../cleanroom/paper.typ) (*Ergentics Working Paper 033 · Horizon Series Monograph ID: Full 3D Non-Planar Extended-Body CRTBP Halo and Lissajous Invariant Manifolds, Rotating-Symplectic Floquet Station-Keeping, and Bennu Touch-and-Go Regolith Sampling Guidance*, 26 November 2026; SHA-256 `0f659f079a459dff2926ce8a81101ecec911a78dc0d302d632e34f6346eb8a47`, preserved byte-for-byte unmodified per Rule 5 alongside all four SVG figures `fig1`–`fig4.svg`).  
**Audit Method:** First-principles recomputation across **three independent verification planes** with zero cached data reads ([`../../../METHODOLOGY.md`](../../../METHODOLOGY.md)):
1. **Plane 1 — Zero-Dependency Python 3.12 (`4/4` PASS):** [`../code/wp033_audit.py`](../code/wp033_audit.py) → checksummed Data Model record [`../data/wp033_g4n_cycle1_calibration.json`](../data/wp033_g4n_cycle1_calibration.json) ([`../data/MANIFEST.sha256`](../data/MANIFEST.sha256), CC BY 4.0).
2. **Plane 2 — Zero-Mathlib Lean 4.36.0 (`7/7` PASS, `0 sorryAx`, `0 ofReduceBool`, `0` warnings; full $6 \times 6$ $\Omega = S^T J S$ & $K11$ Euler quintic formally proved):** [`../lean/WP033/Theorems.lean`](../lean/WP033/Theorems.lean) + [`../lean/Main.lean`](../lean/Main.lean).
3. **Plane 3 — Zero-Crate Rust 1.100.0 (`4/4` PASS, `0.04 s`, bit-exact `SplitMix64` seam `0xda9392ed940a41ee` & `520/1600` parity):** [`../rust/src/lib.rs`](../rust/src/lib.rs) + [`../rust/tests/wp033_xcheck.rs`](../rust/tests/wp033_xcheck.rs).

---

## 1. Executive Verdict

**Core astrodynamics, 42-ODE Halo numerics, rotating-symplectic Floquet algebra, and TAG Monte Carlo: REMARKABLY SOLID.**
- **§1 (`K11`, `C149`, Scale Honesty):** Earth–Moon $L_2$ Euler quintic $\gamma_2^* = 0.1678327510078692$ (`64,514.91 km`, $c_2 = 3.19042521$, Lean-certified `k11_earth_moon_l2_quintic_bracket`), exact cancellation-free $k_z^*(c_2) = 0.27902439$ (`0.291503` Hill limit), and Didymos–Dimorphos $d_{L2} = 180.50\text{ m}$ (`7.9841e5×` scale leap) all match to full precision.
- **§2 (Live 42-ODE 3D Earth–Moon $L_2$ Halo & Rotating-Symplectic Floquet Control):** Re-integrating the paper's exact initial state ($x_0 = 1.1734236346, z_0 = 0.0800, \dot y_0 = -0.1845292585, T = 3.36106913$) from scratch confirms every key invariant to 6–8 digits: $C_J = 3.12579292$ (`|ΔC_J| = 4.35e-13`), rotating symplectic form $\Omega = S^T J S = \begin{pmatrix}-2K & I \\ -I & 0\end{pmatrix}$ (`||M^T Ω M - Ω||_∞ = 2.18e-8`, formally proved in Lean 4 `thm2_rotating_symplectic_form_exact`), Broucke indices **$\nu_1 = 373.3613$**, **$\nu_2 = 0.8409$** (`32.76°/orbit`), Floquet **$\lambda_u = 746.7213$** (`C150`), and 4-orbit Floquet station-keeping crushing uncontrolled 2-orbit blowup by **`3,441.8×`** (`188,077 km → 54.65 km`) for just **`0.1354 m/s`**!
- **§3 (Bennu Nightingale TAG Guidance & `200`-Trial MC):** Exact Coriolis law `C151`, `F38` open-loop crater miss (`11/200 = 5.5%` safe — matching our independent keyed 200-trial MC **to the exact integer `11/200`**!), closed-loop ZEM/ZEV + winch **`200/200 (100.0%)`** pinpoint touchdown (`max_miss = 1.47 μm`), `C152` granular penetration algebra (`z_const = 80.20 cm`), and all published references `[4]`–`[12]` are verified accurate.

**Four concrete catches (1 Critical/Major, 1 Major leading to our original Theorem G3, 2 Moderate) require correction before canonical release:**

| # | Severity | Location in `cleanroom/paper.typ` | Concrete Catch | Constructive Resolution (`[G4N]`) | Negative Ledger |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **1** | **CRITICAL / MAJOR** | Abstract, §2 lines 189, 201 (`fig2`) | **$W^u$ "Lunar Tube" at `1,003.71 km` is `733.7 km` INSIDE the Moon (Direct Lunar Impact!):** The Moon's mean radius is $R_{\mathrm{Moon}} = 1{,}737.4\text{ km}$. Both the paper's `1,003.71 km` (Lean `catch33_1_wu_direct_lunar_impact`) and our independent 42-ODE trace (`1,235.8 km`) plunge hundreds of kilometers below the lunar surface without noting lunar impact. | Explicitly label this $W^u$ branch a **direct lunar-impact unstable manifold** (matching Koon–Lo–Marsden–Ross `[7]`) or compute an elevated pericenter branch ($r_p > 1{,}837\text{ km}$, $\ge 100\text{ km}$ lunar altitude) for lunar-capture mission claims. | `NEG-W11` |
| **2** | **MAJOR (`[G4N]` Theorem G3)** | §1 Theorem 1 lines 161–169, `fig1` | **Decoupled $k_z$ violates Laplace's equation $\nabla^2(\Delta U) = 0$ — reversing the winning triad orientation at $L_2$!** Adding only $\delta U_{zz} = -k_z$ with $\delta U_{xx} = \delta U_{yy} = 0$ is impossible for any passive gravitational multipole in vacuum. Under exact 3D Newtonian gravity (Section 2 below), **radial $x$-aligned** and **vertical $z$-aligned** triads **WIDEN** the Halo–Lissajous gap $\omega_{xy}^2 - \omega_z^2$ (`+0.2803 → +0.2942` and `+0.6678` at Didymos–Dimorphos `L = 50 m` — **wrong sign**!), and an $x$-aligned `50 m` triad drops its inner tip to `~52 m` above Dimorphos's boulders! | Incorporate **Theorem G3 (`[G4N]`, Section 2 below)**: under exact Laplace-constrained 3D finite-size gravity, **transverse $y$-alignment** (velocity-parallel) uniquely slashes $\omega_{xy}^2$ faster than $\omega_z^2$, hitting **exact zero-amplitude 1:1 Halo resonance ($\omega_{xy} = \omega_z$) at Didymos–Dimorphos $L_2$ for $L_y^* = 40.44\text{ m}$** while *increasing* radial surface clearance ($\ge 180.5\text{ m}$ from Dimorphos's center, $\ge 102\text{ m}$ altitude)! | `NEG-W12` |
| **3** | **MODERATE** | §3 lines 211, 221 (`C152`) | **Whole-asteroid vs. subsurface regolith density (`1,190` vs. `500–700 kg/m^3`) & unstated $C_D = 1.60$:** Line 211 uses Bennu's *bulk asteroid* density (`1,190 kg/m^3`, Lauretta 2019), whereas OSIRIS-REx's own TAG papers (Lauretta 2022 & Walsh 2022 — Refs `[9]`!) established that the fluidized near-subsurface regolith is **half as dense (`500–700 kg/m^3`)**! At `600 kg/m^3`, $\chi$ halves (`21.59 → 10.88`) and `C152` sink depth increases `1.58×` from `11.58 cm` to **`18.24 cm`** (still `~2.7×` gentler than OSIRIS-REx's `48.8 cm`). Also $C_D = 1.60$ is implied by $\chi = 21.59$ but never stated in the text. | Update $\rho_{\mathrm{reg}}$ to `500–700 kg/m^3` (nominal `600 kg/m^3` → `18.2 cm` penetration), state $C_D = 1.60$ explicitly, and include the density uncertainty band in the 200-trial MC. | `NEG-W13` |
| **4** | **MODERATE** | §3 lines 214–222 (`C151`, `C152`, `F38`) | **Certification-domain extrapolation (`8.1×` and `144×`) & Bennu TAG gravity model:** `C151` ($\eta \in [10^{-4}, 0.20]$) and `C152` ($\chi \in [10^{-3}, 0.15]$) certify small-parameter Taylor limits, whereas the paper's actual Bennu TAG operates at **$\eta = 1.617$** (`8.1×` outside `C151`) and **$\chi = 21.59$** (`144×` outside `C152`, Lean `catch33_4_c151_c152_domain_extrapolation`). Also constant-$g_{\mathrm{surf}}$ `C151` predicts `15.99 m` drift at $h = 100\text{ m}$; the reported `19.23 m` arises from $1/r^2$ altitude-decreasing gravity plus Bennu's `15.7%` centrifugal relief (`-ω_B^2 r cos^2 56°`, omitted from line 211's $g_{\mathrm{surf}}$). | State explicitly that `C151`/`C152` certify the *asymptotic limit* while Bennu TAG operates in the nonlinear finite-$\eta$/large-$\chi$ regime, and include both $1/r^2$ variation and centrifugal relief (`-1.27e-5 m/s^2`, `15.7%` of $g_{\mathrm{surf}}$) in the analytical TAG summary. *(Upstream `Swift++` corpus claims—Scroll 43, `60,800` RCTs, CRC-64, XCTest `141/141`—remain `[E]` outside this repo.)* | `NEG-W14` |

---

## 2. Original `[G4N]` Discovery — Theorem G3 (Laplace-Constrained 3D Multipole Halo Resonance at $L_2$)

> **Theorem G3 (`[G4N]` — Exact Laplace-Constrained 3D Finite-Size $L_2$ Hessian & Transverse $y$-Axis Halo Bifurcation).**  
> Consider a 3-equal-mass collinear triad ($m_i = M/3$ at $0, \pm l\,\hat{\mathbf{e}}_a$, $l = L / R_{\mathrm{sep}}$) at a collinear CRTBP equilibrium $L_2$ with Legendre coefficients $c_2 = \frac{1-\mu}{(1+\gamma_2)^3} + \frac{\mu}{\gamma_2^3}$ and $c_4 = \frac{1-\mu}{(1+\gamma_2)^5} + \frac{\mu}{\gamma_2^5}$. Because the finite-size gravitational correction $\Delta U^{(a)} = \frac{1}{3} l^2 \partial_{aa} U_{\mathrm{pt}} + O(l^4)$ is strictly harmonic in vacuum ($\nabla^2 \Delta U^{(a)} = 0$):
> 1. **Exact Coupled 3D Hessian Shifts:**
>    $$\bigl(\delta U_{xx}, \delta U_{yy}, \delta U_{zz}\bigr) = c_4 l^2 \cdot \begin{cases} (+8, -4, -4) & \text{radial } x\text{-axis}, \\ (-4, +3, +1) & \text{transverse } y\text{-axis (orbital velocity direction)}, \\ (-4, +1, +3) & \text{vertical } z\text{-axis}, \\ (+2, -\tfrac{1}{2}, -\tfrac{3}{2}) & \text{isotropic planar equilateral } xy\text{-triad}. \end{cases}$$
>    Every row is strictly traceless (Lean `theorem_g3_l2_laplace_hessian_identities`), so no passive gravitational multipole can realize WP 033 Theorem 1's decoupled $(\delta U_{xx} = \delta U_{yy} = 0, \delta U_{zz} = -k_z)$.
> 2. **Orientation Reversal of the Halo–Lissajous Gap $\Delta_{\mathrm{Halo}} := \omega_{xy}^2 - \omega_z^2$:**  
>    Evaluating the coupled sensitivity $\partial \Delta_{\mathrm{Halo}} / \partial(c_4 l^2)$ at Earth–Moon $L_2$ ($c_2 = 3.1904$):
>    - **Radial $x$-alignment:** $\delta(\omega_{xy}^2) = +4.0802$, $\delta(\omega_z^2) = +4.0000 \implies \delta\Delta_{\mathrm{Halo}} = \mathbf{+0.0802\,c_4 l^2 > 0}$ (**widens gap — wrong sign!**);
>    - **Vertical $z$-alignment:** $\delta(\omega_{xy}^2) = -0.7054$, $\delta(\omega_z^2) = -3.0000 \implies \delta\Delta_{\mathrm{Halo}} = \mathbf{+2.2946\,c_4 l^2 > 0}$ (**strongly widens gap!**);
>    - **Transverse $y$-alignment:** $\delta(\omega_{xy}^2) = -3.3748$, $\delta(\omega_z^2) = -1.0000 \implies \delta\Delta_{\mathrm{Halo}} = \mathbf{-2.3748\,c_4 l^2 < 0}$ (**steepest possible closure!**);
>    - **Equilateral planar $xy$-triad:** $\delta\Delta_{\mathrm{Halo}} = \mathbf{-1.1473\,c_4 l^2 < 0}$ (closes gap with zero static quadrupole!).
> 3. **Exact Nonlinear Didymos–Dimorphos $L_2$ Zero-Amplitude Halo Bifurcation:**  
>    For Didymos–Dimorphos ($\mu = 0.0091, R_{\mathrm{sep}} = 1{,}190\text{ m}, d_{L2} = 180.50\text{ m}$, point-mass gap $\Delta_{\mathrm{Halo}} = +0.2803$), exact nonlinear 3-mass summation confirms:
>    - $L = 50\text{ m}$ radial ($x$): $\Delta_{\mathrm{Halo}} = \mathbf{+0.2942}$ (fails to close; inner tip `~52 m` above Dimorphos boulders),
>    - $L = 50\text{ m}$ vertical ($z$): $\Delta_{\mathrm{Halo}} = \mathbf{+0.6678}$ (more than doubles gap),
>    - **$L = 40.44\text{ m}$ transverse ($y$):** hits **exact 1:1 zero-amplitude Halo resonance ($\omega_{xy} = \omega_z$, $\Delta_{\mathrm{Halo}} = 0.0000$)** while keeping *all three masses* at $\ge 180.5\text{ m}$ from Dimorphos's center ($\ge 102\text{ m}$ surface altitude — strictly *increasing* clearance to $185.0\text{ m}$ at the outer tips!).

---

## 3. Grok Bot (`[GB]`) Independent Cross-Check Checklist

1. Verify **Theorem G3 (`NEG-W12`)** from scratch: differentiate $\Delta U^{(a)} = \frac{1}{3} l^2 \partial_{aa}(1/r)$ twice at $(r, 0, 0)$ to confirm $(+8,-4,-4)_x$, $(-4,+3,+1)_y$, $(-4,+1,+3)_z$, and confirm Didymos–Dimorphos $L_y^* = 40.44\text{ m}$ exact zero-amplitude Halo bifurcation.
2. Verify `NEG-W11`: confirm $W^u$ from the converged Earth–Moon $L_2$ Halo orbit impacts inside $R_{\mathrm{Moon}} = 1{,}737.4\text{ km}$.
3. Verify `NEG-W13`/`NEG-W14`: confirm Walsh/Lauretta 2022 subsurface density `600 kg/m^3` gives `18.24 cm` (`C_D = 1.60`) vs. `11.58 cm` at `1,190 kg/m^3`, and confirm $\eta = 1.617 > 0.20$, $\chi = 21.59 > 0.15$.
4. Reproduce all three planes live:
   ```bash
   python3 papers/wp033_halo_tag_guidance/code/wp033_audit.py
   sha256sum -c papers/wp033_halo_tag_guidance/data/MANIFEST.sha256
   cargo test --manifest-path papers/wp033_halo_tag_guidance/rust/Cargo.toml
   lake -d papers/wp033_halo_tag_guidance/lean build && papers/wp033_halo_tag_guidance/lean/.lake/build/bin/wp033-lean
   ```
