# Working Paper 030 — Shape-Controlled Gravitational Propulsion Resolved

**Series:** Ergentics Working Paper 030 · Horizon Series Monograph I · Continuation of Working Paper 028 (23 September 2026)  
**Author:** Ergentics, LLC & Swift++ Library of Alexandria Verification Program (`[E]`)  
**Date:** November 2026  
**Lifecycle Stage:** **`Intake (Pre-Assessment)`** — archived verbatim as-is prior to independent mathematical, physical, and computational assessment by **Gemini 4 Neon** (`[G4N]` / `[E→G4N]`) and **Grok Bot** (`[GB]` / `[E→GB]`).

---

## Verbatim Clean-Room Archive (`cleanroom/`)

Per Rule 5 ([`../../AGENTS.md`](../../AGENTS.md)), the uploaded clean-room manuscript is archived byte-for-byte unmodified as the frozen `[E]` baseline for independent assessment:

| File | Role | Size | SHA-256 | Hygiene Scan | License |
| :--- | :--- | ---: | :--- | :--- | :--- |
| [`cleanroom/paper.typ`](cleanroom/paper.typ) | Verbatim Typst source (*Working Paper 030 / Horizon Monograph I*) | `34,006 B` (328 lines) | `f2202e9e69861143c44a233e4d403ab266d0c47e0a8dd09ea8afc449e9ea914e` | `0` local paths · `0` URLs · `0` emails · `0` credentials | MIT (per header) |
| [`cleanroom/figures/fig1_isoinertial_triad_vs_dumbbell.svg`](cleanroom/figures/fig1_isoinertial_triad_vs_dumbbell.svg) | Figure 1: Iso-inertial 3-mass triad vs. 2-mass Landis dumbbell (`H4`) | `14,447 B` | `e93e09a6895ed29398bc0c9bcfa0cd991fcd1b51969402520f51ee21853da201` | `0` local paths · `0` non-W3C URLs · `0` credentials | MIT |
| [`cleanroom/figures/fig2_coupled_symplectic_orbit_and_eq5.svg`](cleanroom/figures/fig2_coupled_symplectic_orbit_and_eq5.svg) | Figure 2: Coupled 4-body orbit & Eq. (5) / constant-$p$ closure | `14,999 B` | `f77d3813ee0914545fd2f159638f5b5e318d4a7a01a0beb9e85d55e9bbb779ae` | `0` local paths · `0` non-W3C URLs · `0` credentials | MIT |
| [`cleanroom/figures/fig3_shapere_wilczek_holonomy.svg`](cleanroom/figures/fig3_shapere_wilczek_holonomy.svg) | Figure 3: Shapere–Wilczek `-90°` zero-spin holonomy (`C140`) | `7,374 B` | `92bd1292a54b2b331e41a0f07a13a4495b7bef98efd12bdf3244a87138ab490a` | `0` local paths · `0` non-W3C URLs · `0` credentials | MIT |
| [`cleanroom/figures/fig4_h5_mission_dominance_map.svg`](cleanroom/figures/fig4_h5_mission_dominance_map.svg) | Figure 4: `H5` mission dominance map & Eq. (5) regeneration efficiency | `12,692 B` | `840ce4dbbb21b25bfd596bb1ff6efaf859d160d8ea7fad0657001875f73f4053` | `0` local paths · `0` non-W3C URLs · `0` credentials | MIT |

All four relative SVG paths in `cleanroom/paper.typ` (`figures/fig1..fig4.svg`) resolve directly inside `cleanroom/` (`typst compile paper.typ paper.pdf`). *Ergentics Working Paper 028 / Web Edition 029* (23 September 2026) sits on the author's website and can be mirrored here later if desired.

---

## Pre-Assessment Scope for Independent Audit (`[G4N]` & `[GB]`)

Nothing below is marked `[X]` verified yet; all claims live in `cleanroom/paper.typ` as submitted `[E]` statements pending independent first-principles verification:

1. **`H1–H3` Exact Algebraic Factorizations & IEEE-754 Cancellation Audit (§1):**
   - Exact collinear ($\Delta a_\parallel$) and transverse ($\Delta a_\perp$) 3-mass Newtonian acceleration contrast factorizations; Paper 028 Earth benchmark (`-3.3203` / `+1.6601` μN, `13.1268` μJ); IEEE-754 subtraction loss (`9` digits at $L = 100\text{ m}$, `8.20e-3` at $L/R = 10^{-7}$).
2. **Theorem 1 — Exact Noether Constant-$p$ Orbital Manifold Barrier (§2):**
   - Exact $SO(3)$ conservation $\mathbf{J}_{\mathrm{tot}} = \mathbf{L}_{\mathrm{orb}} + \mathbf{S}_{\mathrm{craft}}$ forcing $\Delta \mathbf{L}_{\mathrm{orb}} = \mathbf{0}$ and $p = a(1 - e^2) = \text{const}$ for any spin-closed cycle of any $N$-mass craft in a spherical $1/r$ potential.
3. **Theorem 2 — Iso-Inertial Hopf-Fibration Three-Mass Triad & Dirac-Monopole Connection (§2):**
   - Normalized Jacobi complex coordinates $(z_1, z_2) \in \mathbb{C}^2$ on $|z_1|^2 + |z_2|^2 = 2L^2$: strictly constant $I_{zz} \equiv (2/3) M L^2$, full-disk complex quadrupole $Q_{\mathbb{C}} = I_0 e^{2i\theta_0}(\cos\Phi + i\cos\Theta\sin\Phi)$ controllability with zero leading quadrupole gravity-gradient torque, and zero-spin connection $\dot\theta_0 = -\tfrac12 \cos\Theta\,\dot\Phi$ yielding holonomy $\Delta\theta_{\mathrm{geom}} = -\tfrac12 \Omega_{\mathrm{solid}}(\Sigma)$.
4. **Proposition 3 — Exact Eccentric Pumping Law & `2/3` Penalty Recovery (§2):**
   - Per-orbit energy gain $\Delta E_{\mathrm{orb}} = \frac{3}{2}\mu I_0 (r_p^{-3} - r_a^{-3}) = \frac{2\mu M L^2}{p^3}(3e + e^3)$ matching a full-retraction 2-mass Landis dumbbell without radial $\dot I_{zz}$ Coriolis torque.
5. **Coupled 4-Body Dynamical-Primary Integration & `H4` Head-to-Head Benchmark (§3):**
   - Independent first-principles re-integration (dynamical primary $M_p = 1000 M$, 5 orbits, $e_0 = 0.2$ and $e_0 = 0.0$ control): Eq. (5) residual, $|\Delta J_{\mathrm{tot}}|$, octupole spin exchange, unassisted 2-mass Landis tether Coriolis tumble vs. Hopf triad (`0` tumbles, `1.78×–1.83×` $\Delta E_{\mathrm{orb}}$), and live `-90.0000°` Shapere–Wilczek reorientation at $\Theta = \pi/3$.
6. **Honest `H5` Thermodynamic Efficiency & Mission Dominance Regimes (§4):**
   - Regeneration efficiency $\eta_{\mathrm{prop}}(e; \eta_{\mathrm{act}}, \eta_{\mathrm{regen}})$, exact 50%-efficiency threshold $e_{50}^* = (2^{1/3} - 1)/(2^{1/3} + 1) \approx 0.1150133319511158$, internal kinetic energy barrier $T_{\mathrm{shape}}$, and quantitative mission budgets (Regime A: `100 m` LEO dominated; Regime B: `20 km` eccentric pumping `619.8 m/s/yr`, `55.1 N` tension; Regime C: `2.5 km` asteroid proximity `7.84e6×` coupling boost).
7. **Literature & Reference Verification (§References):**
   - Bibliographic verification of references `[1]`–`[12]` (Landis, Guéron–Maia–Matsas, Wisdom, Guichardet, Shapere–Wilczek, Montgomery/Iwai, Martinez-Sanchez–Gavit, Beletsky–Levin, Moore/Krawczyk).
