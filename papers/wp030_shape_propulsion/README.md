# Working Paper 030 — Shape-Controlled Gravitational Propulsion Resolved

**Series:** Ergentics Working Paper 030 · Horizon Series Monograph I · Continuation of Working Paper 028 (23 September 2026)  
**Author:** Ergentics, LLC & Swift++ Library of Alexandria Verification Program (`[E]`)  
**Date:** November 2026  
**Lifecycle Stage:** **`Cycle 1 Audited [G4N] — Awaiting [GB] Independent Pass`** — frozen clean-room `[E]` baseline preserved byte-for-byte unmodified under `cleanroom/`; full **Gemini 4 Neon** (`[G4N]` / `[E→G4N]`) 3-plane independent audit & mathematical sharpening landed in [`reconciliation/GEMINI4_NEON_WP030_AUDIT.md`](reconciliation/GEMINI4_NEON_WP030_AUDIT.md). Ready for **Grok Bot** (`[GB]`) independent cross-check prior to canonical `paper/` reconciliation.

---

## Verbatim Clean-Room Archive (`cleanroom/` — Frozen per Rule 5)

Per Rule 5 ([`../../AGENTS.md`](../../AGENTS.md)), the uploaded clean-room manuscript is archived byte-for-byte unmodified as the frozen `[E]` baseline for independent assessment:

| File | Role | Size | SHA-256 | Hygiene Scan | License |
| :--- | :--- | ---: | :--- | :--- | :--- |
| [`cleanroom/paper.typ`](cleanroom/paper.typ) | Verbatim Typst source (*Working Paper 030 / Horizon Monograph I*) | `34,006 B` (328 lines) | `f2202e9e69861143c44a233e4d403ab266d0c47e0a8dd09ea8afc449e9ea914e` | `0` local paths · `0` URLs · `0` emails · `0` credentials | MIT (per header) |
| [`cleanroom/figures/fig1_isoinertial_triad_vs_dumbbell.svg`](cleanroom/figures/fig1_isoinertial_triad_vs_dumbbell.svg) | Figure 1: Iso-inertial 3-mass triad vs. 2-mass Landis dumbbell (`H4`) | `14,447 B` | `e93e09a6895ed29398bc0c9bcfa0cd991fcd1b51969402520f51ee21853da201` | `0` local paths · `0` non-W3C URLs · `0` credentials | MIT |
| [`cleanroom/figures/fig2_coupled_symplectic_orbit_and_eq5.svg`](cleanroom/figures/fig2_coupled_symplectic_orbit_and_eq5.svg) | Figure 2: Coupled 4-body orbit & Eq. (5) / constant-$p$ closure | `14,999 B` | `f77d3813ee0914545fd2f159638f5b5e318d4a7a01a0beb9e85d55e9bbb779ae` | `0` local paths · `0` non-W3C URLs · `0` credentials | MIT |
| [`cleanroom/figures/fig3_shapere_wilczek_holonomy.svg`](cleanroom/figures/fig3_shapere_wilczek_holonomy.svg) | Figure 3: Shapere–Wilczek `-90°` zero-spin holonomy (`C140`) | `7,374 B` | `92bd1292a54b2b331e41a0f07a13a4495b7bef98efd12bdf3244a87138ab490a` | `0` local paths · `0` non-W3C URLs · `0` credentials | MIT |
| [`cleanroom/figures/fig4_h5_mission_dominance_map.svg`](cleanroom/figures/fig4_h5_mission_dominance_map.svg) | Figure 4: `H5` mission dominance map & Eq. (5) regeneration efficiency | `12,692 B` | `840ce4dbbb21b25bfd596bb1ff6efaf859d160d8ea7fad0657001875f73f4053` | `0` local paths · `0` non-W3C URLs · `0` credentials | MIT |

---

## Independent Verification Planes (`[G4N]` ADPIE Cycle 1)

All verifiers compute directly from first principles with zero cached data reads (`Code Model` = MIT; `Data Model` = CC BY 4.0):

| Plane | Path | Status | Verification Command (from repo root) |
| :--- | :--- | :--- | :--- |
| **1 — Zero-Dep Python 3.12** | [`code/wp030_audit.py`](code/wp030_audit.py) | **`9/9` PASS** (D1–D6, R1–R2 4-body & Landis RK4, P1 `N=1,600` SplitMix64 RCT) | `python3 papers/wp030_shape_propulsion/code/wp030_audit.py` |
| **2 — Zero-Mathlib Lean 4.36.0** | [`lean/WP030/Theorems.lean`](lean/WP030/Theorems.lean) | **`15/15` PASS** (`0 sorryAx`, `0 ofReduceBool`, `0` warnings; 8 axiom-free) | `lake -d papers/wp030_shape_propulsion/lean build && papers/wp030_shape_propulsion/lean/.lake/build/bin/wp030-lean` |
| **3 — Zero-Crate Rust 1.100.0** | [`rust/src/lib.rs`](rust/src/lib.rs) · [`rust/tests/wp030_xcheck.rs`](rust/tests/wp030_xcheck.rs) | **`7/7` PASS** (`0.16 s`, bit-exact SplitMix64 seam `0xe9de083b69c67979` & 4-body RK4 parity) | `cargo test --manifest-path papers/wp030_shape_propulsion/rust/Cargo.toml` |
| **Data Model (CC BY 4.0)** | [`data/wp030_g4n_cycle1_calibration.json`](data/wp030_g4n_cycle1_calibration.json) · [`data/MANIFEST.sha256`](data/MANIFEST.sha256) | **`1/1` SHA-256 OK** | `sha256sum -c papers/wp030_shape_propulsion/data/MANIFEST.sha256` |
| **Audit & Novelty Dossier** | [`reconciliation/GEMINI4_NEON_WP030_AUDIT.md`](reconciliation/GEMINI4_NEON_WP030_AUDIT.md) | **Complete (`[G4N]`)** — 8 catches (`NEG-W1`–`NEG-W6`), original **Theorem G1**, & `[GB]` handoff checklist | — |

---

## Audit Summary (`[G4N]` Cycle 1)

- **Confirmed rock-solid:** `H1–H3` exact factorizations & Earth benchmark (`C137`), **Theorem 1** exact Noether constant-$p$ barrier, **Proposition 3** pumping identity, **`K8`** $e_{50}^* = 0.1150133319511158$, coupled 4-body `Eq. (5)` closure (`0.0011 ppm`, `|ΔJ| <= 2.86e-12`, `0` tumbles vs. `2,382°–12,957°` on unassisted 2-mass Landis tethers, `e_0 = 0` circular barrier), and honest `H5` refutation of `100 m` LEO.
- **8 Concrete Catches Logged (`NEG-W1`–`NEG-W6` in [`../../NEGATIVES.md`](../../NEGATIVES.md)):**
  1. **Critical (`NEG-W1`):** Table 1 Regimes A & B have underground Earth perigees (`r_p = 6,300 km` and `5,250 km < 6,371 km`); valid above-atmosphere $r_p = 6{,}800\text{ km}$ reduces Regime B from `619.8` to **`220.2 m/s/yr`** (`25.4 N` / `27.5 N` tension — still propellantless & niche-viable).
  2. **Major (`NEG-W2`):** Paper's $\Theta = \pi/3$ holonomy loop hits **two exact binary collisions** ($\rho_2 = \rho_3$ at $\Phi = 0$, $\rho_1 = \rho_3$ at $\Phi = \pi$) and `fig3` mislabels collinear $\Theta = 0$ as `"North Pole (Equilateral)"`. Fixed by unitary equilateral-pole basis $w_\pm = (z_1 \pm i z_2)/\sqrt{2}$ (`-90.0000°` collision-free at $\beta = \pi/3$, $\min d_{ij} = 0.5176\,L$).
  3. **Major — Original `[G4N]` Theorem G1 (`NEG-W3`):** Exact zero-spin kinetic energy is $T_{\mathrm{shape}}(q) = \frac{1}{8}I_0\dot\beta^2 + \frac{q^2}{1-q^2}(\frac12 I_0 \dot\theta_{\mathrm{orb}}^2)$ — **`9.2564×` (`361/39`) larger at `q = 0.95`** than §4.1's $\frac12 I_0 \Omega^2$ estimate and diverging as $(1 - q^2)^{-1}$. Peak mass radius is $\sqrt{\frac{2(1+q)}{3}}\,L$ (`1.1402 L` at `q = 0.95`; $\le L$ iff $q \le 1/2$).
  4. **Moderate (`NEG-W4`):** Theorem 2 line 200 inertia-vs-mass-quadrupole sign convention (`Q_mass = -Q_inertia`).
  5. **Moderate (`NEG-W5`):** Table 1 Regime A tension `0.0012 N` is `~100×` too low (exact `0.159 N` at $r_p = 6{,}300\text{ km}$; `0.127 N` / `0.131 N` on valid $r_p = 6{,}800\text{ km}$).
  6. **Moderate (`NEG-W6`):** Regime C `7.84e6×` is $(L/R)^2$ (not $L^2/R^4$), Bennu tension is `3.13e-5 N` (not `< 10^-6 N`), and 1 AU SRP exceeds raw Bennu $|\Delta a_\parallel|$.
  7. **Minor (`NEG-W6`):** `C138 <= 1e-6` requires zero-octupole symmetry (`1.29e-5` over general $\chi$); `F35` loss at $e^* = 0.0275$ is `84.8%` (`0.8479`), not `84.6%`; Ref `[1]` NTRS ID should be `19910012826` (CP-10059) / `19910029285` (Landis tether paper).
  8. **Diagnostic note:** Specify $\mu_{\mathrm{tot}} = G(M_p + M)$ in Theorem 1 and osculating vs. total energy convention for §3.1 `a_f / e_f`.
