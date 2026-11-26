# Shape-Controlled Gravitational Propulsion: Iso-Inertial Hopf Holonomy, Three-Dimensional $J_2$ Symmetry Breaking, and Mechanical-Hub Hardware Sizing

**Author:** Ergentics  
**Series:** Horizon Synthesis — Piece I (synthesizing frozen clean-room `WP 030` + `WP 031`)  
**Canonical LaTeX / PDF:** [`paper/piece1_propulsion_hardware.tex`](paper/piece1_propulsion_hardware.tex) · [`paper/piece1_propulsion_hardware.pdf`](paper/piece1_propulsion_hardware.pdf) · [`arxiv/piece1-propulsion-hardware-arxiv.tar.gz`](arxiv/piece1-propulsion-hardware-arxiv.tar.gz)  
**Open Reference Code & Data:** [`code/piece1_sim.py`](code/piece1_sim.py) (`7/7 PASS`) · [`data/piece1_calibration.json`](data/piece1_calibration.json) · [`data/MANIFEST.sha256`](data/MANIFEST.sha256)

---

## Abstract

We present a reconciled, self-contained synthesis of planar and three-dimensional shape-controlled gravitational propulsion for an iso-inertial three-mass spacecraft triad, unifying and repairing the Horizon clean-room manuscripts `WP 030` and `WP 031` under a single set of physical constants and open, reproducible simulations. Five structural issues uncovered during cross-agent verification are resolved in place:

1. **Cancellation-free finite-size tidal evaluation (`NEG-W4`, `NEG-W26`):** Factored evaluation eliminates catastrophic IEEE-754 double-precision cancellation below $\epsilon = L/R \lesssim 10^{-7}$.
2. **Collision-free equilateral-pole Hopf holonomy (`NEG-W2`, `NEG-W25`):** Switching to the chiral equilateral-pole Jacobi basis $w_\pm = (z_1 \pm i z_2)/\sqrt{2}$ yields an exact physical rotation $\Delta\theta_{\mathrm{phys}} = -90.0000^\circ$ while keeping all inter-mass separations strictly positive ($\min d_{ij} = \sqrt{2-\sqrt{3}}\,L \approx 0.517638\,L$).
3. **Theorem G1 iso-inertial kinetic-energy wall (`NEG-W3`):** Exact closed form $K_{\mathrm{int}}^{\mathrm{peak}}(q)/(\tfrac12 I_0 \Omega^2) = q^2/(1-q^2)$ bounds high-amplitude pumping ($0.3333$ at $q=0.50$, $2.6036$ at $q=0.85$, $9.2564$ at $q=0.95$; peak arm radius $r_{\max}(0.95)=1.1402\,L$).
4. **Unified WGS84 safe-perigee mission sizing and subtracted 3D $J_2$ control (`NEG-W1`, `NEG-W5`, `NEG-W6`, `NEG-W16`, `NEG-W17`, `NEG-W18`, `NEG-W27`):** Standardizing Earth's equatorial radius to WGS84 $R_\oplus = 6{,}378.137\text{ km}$ yields safe LEO perigee $r_p = 6{,}978.137\text{ km}$, optimal eccentricity $e^* = 0.281702$, and headline $\Delta v/\mathrm{yr} = 199.89\text{ m/s/yr}$ at $L = 20\text{ km}$ under canonical $I_0 = \frac23 M L^2$. Subtracting an identical $L = 0$ point-mass control in 3D oblate $J_2$ while tracking coupled axial spin $J_z = L_z + S_z$ to $< 10^{-12}$ isolates the genuine shape effect ($\Delta i_{\mathrm{shape}} = -21.10\text{ mdeg}$, $\Delta p_{\mathrm{shape}} = -0.002815$).
5. **Theorem G4 $I_0$-invariant electrical heat wall and mechanical-hub flight baseline (`NEG-W15`, `NEG-W18`, `NEG-W27`):** Consistent polar inertia $I_0 = \frac23 M L^2$ proves an $I_0$-invariant $9.85\times$ minimum electrical waste-heat-to-orbital-power floor ($15.16\times$ at $q=0.50$, $118.90\times$ at $q=0.90$), motivating a spin-tensioned Hopf triad with a coupled mechanical differential / spring-drum hub (`1.5%` friction loss) that cuts waste heat by $22.4\times$ (from $312.2\text{ W}$ to $13.92\text{ W}$) at a hardware mass of $45.43\text{ kg}$ versus $100.52\text{ kg}$ wet for a 5-year Hall thruster.

---

## 1. Introduction and Attribution Convention

Propellantless orbital modification by cyclic redistribution of a spacecraft's mass distribution in a non-uniform gravitational field (*gravitational swinging*) builds on Martinez-Sanchez & Gavit (1987), Landis (1990/1991, NASA NTRS `19910012850`; 1992), Beletsky & Levin (1993), Wisdom (2003), Guéron–Maia–Matsas (2006), and the gauge-theoretic shape-space framework of Guichardet (1984), Iwai (1987), Shapere & Wilczek (1989), and Montgomery (1993).

Attribution tags match Morpheus house convention: `[lit.]` classical literature, `[E]` original author derivations and internal `Swift++` (*Epsilon*) provenance, `[G4N]` independent proofs, repairs, and open simulations by Gemini 4 Neon, `[GB]` Round-1 verification checks by Grok Bot, and `[X]` cross-checked syntheses.

---

## 2. Exact Finite-Size Acceleration and Cancellation-Free Evaluation

**Proposition 2.1 (Cancellation-free finite-size tidal acceleration)** `[E→G4N]`: For three equal masses $m = M/3$ at $\mathbf{r}_a = \mathbf{R} + \boldsymbol{\rho}_a$ ($\sum_a \boldsymbol{\rho}_a = \mathbf{0}$), setting $s_a = 2(\boldsymbol{\rho}_a\cdot\hat{\mathbf{R}})/R + \|\boldsymbol{\rho}_a\|^2/R^2$ and $\alpha_a = (1+s_a)^{-1/2}$ gives the algebraically exact, cancellation-free differential acceleration
$$\Delta \mathbf{a} = -\frac{\mu}{3 R^3} \sum_{a=1}^{3} \left[-\frac{s_a(1 + \alpha_a + \alpha_a^2)}{(1+s_a)^{3/2}(1+\alpha_a)}\mathbf{R} + (1+s_a)^{-3/2}\boldsymbol{\rho}_a\right].$$

**Remark 2.2 (`NEG-W4`, `NEG-W26`)** `[GB, G4N, X]`:
- At LEO ($R = 7{,}000\text{ km}$, $L = 100\text{ m}$), exact $\Delta a = -3.3202868966\times 10^{-9}\text{ m/s}^2$; factored summation has relative error $5.75\times 10^{-8}$ vs. $3.46\times 10^{-7}$ for mean-subtracted summation.
- Unit-sphere IEEE-754 `f64` naive relative errors: `8.26e-8` ($\epsilon=10^{-5}$), `1.49e-5` ($\epsilon=10^{-6}$), `8.20e-3` ($\epsilon=10^{-7}$), `48.03%` ($\epsilon=10^{-8}$), `100.0%` ($\epsilon=5\times 10^{-9}$).
- The planar mass-quadrupole $Q_{ij}$ and inertia tensor $I_{ij} = I_0\delta_{ij} - Q_{ij}$ satisfy $Q_{xx}+Q_{yy} = I_{xx}+I_{yy} = I_0$ identically (`0.0` residual) with opposite traceless sign $(I_{xx}-I_{yy}) + 2iI_{xy} = -[(Q_{xx}-Q_{yy}) + 2iQ_{xy}]$.

---

## 3. Equilateral-Pole Hopf Holonomy and Theorem G1

**Proposition 3.1 (Collision-free equilateral-pole Hopf chart)** `[G4N, X]`: In complex Jacobi coordinates $(z_1, z_2)$ with fixed polar moment $I_0 = \frac23 M L^2$, the unitary chiral basis
$$w_+ = \frac{z_1 + i z_2}{\sqrt{2}}, \qquad w_- = \frac{z_1 - i z_2}{\sqrt{2}}, \qquad |w_+|^2 + |w_-|^2 = 2L^2$$
places the two equilateral triangles at the north/south poles of $S^2$ and collinear collisions on the equator. Around the latitude circle $\vartheta = \pi/3$ ($q = \sqrt{3}/2$, $\Omega_{\mathrm{solid}} = \pi$), the zero-angular-momentum connection produces exact physical rotation $\Delta\theta_{\mathrm{phys}} = -\frac12 \Omega_{\mathrm{solid}} = -90.0000^\circ$ with strictly positive minimum separation
$$\min_{t,\, i\neq j} d_{ij}(t) = \sqrt{2-\sqrt{3}}\,L \approx 0.517638\,L.$$
This resolves both the pairwise collision at $t=\pi/2$ (`NEG-W2`) and the $+90^\circ$ physical sign mismatch (`NEG-W25`) of the unrotated $(z_1, z_2)$ chart in `WP 030`.

**Theorem 3.3 (Theorem G1: Iso-inertial Hopf kinetic-energy wall, `NEG-W3`)** `[G4N]`: Along a meridian quadrupole stroke $q = \sin\vartheta \in (0,1)$,
$$\frac{K_{\mathrm{int}}^{\mathrm{peak}}(q)}{\tfrac12 I_0 \Omega^2} = \frac{q^2}{1 - q^2}, \qquad r_{\max}(q) = L\sqrt{\frac23(1+q)}.$$
Exact dimensionless values (verified to `9.38e-11`): `0.3333` ($q=0.50$), `1.0000` ($q=1/\sqrt{2}$), `2.6036` ($q=0.85$), and `9.2564` ($q=0.95$, with $r_{\max} = 1.1402\,L$). *(Figure 1: `paper/figures/fig1_hopf_holonomy_g1.pdf`.)*

---

## 4. Safe-Perigee Optimal Eccentricity and Open 4-Body Verification (`R1`)

**Proposition 4.1 (`K9`, `K8`, `F35`, Bennu scaling)** `[E→G4N]`:
- Under WGS84 $R_\oplus = 6{,}378.137\text{ km}$ (`NEG-W27`), safe LEO perigee is $r_p = 6{,}978.137\text{ km}$ (`NEG-W1`).
- Optimal safe-perigee eccentricity (`K9`): $e^*_{\mathrm{opt}} = 0.281701557908774$ (`K8` 50% retention root: $e^*_{50} = 0.11501333$).
- Headline safe-perigee rate at $L = 20\text{ km}$ (`I_0 = (2/3)ML^2`, `NEG-W16`): **`199.89 m/s/yr`** (`198.58` at $e=0.25$, `186.68` at $e=0.40$; `4.997 mm/s/yr` at $L=100\text{ m}$).
- Safe-perigee tidal tensions ($M = 1{,}000\text{ kg}$): `0.1173 N` at $L=100\text{ m}$ (`NEG-W5`) and `23.46 N` at $L=20\text{ km}$.
- Bennu ($R=500\text{ m}, L=20\text{ m}$, `NEG-W6`): $(L/R)^2 = 7.84\times 10^6\times$ LEO scaling, $a_{\mathrm{quad}} = 2.505\times 10^{-9}\text{ m/s}^2$ (`5.49%` of 1 AU SRP `4.56e-8 m/s^2`), $\Delta v/\mathrm{yr} = 11.69\text{ mm/s/yr}$, tension `3.13e-5 N`. At $\epsilon = 0.0275$ (`F35`), the $O(\epsilon^2)$ quadrupole loses `84.79%`.

### Table 1: Open Planar 4-Body RK4 Benchmark (`R1`, `piece1_sim.py`) `[G4N]`

Run parameters: $\mu=1, M=3, L=0.04, a_0=1, q_{\max}=0.85, k_{\mathrm{sw}}=8$, 5 orbits at 2,000 steps/orbit, radial-reflection-symmetric switching ($\chi = \pi$ inbound, $\chi = 0$ outbound).

| Run | $\Delta E_{\mathrm{osc}}$ | $\Delta E_{\mathrm{tot}}$ | $a_{\mathrm{osc}} / a_{\mathrm{tot}}$ | $\max|\Delta J_{\mathrm{tot}}|$ | Outcome |
|---|---:|---:|---:|---:|---|
| Hopf triad ($e_0=0.20$) | `+0.027083` | `+0.023907` | `1.01839 / 1.01501` | `8.21e-13` | `96.6%` of ideal `0.028038` ($e_{\mathrm{osc}}=0.23944$, $e_{\mathrm{tot}}=0.23280$) |
| Circular null ($e_0=0$) | `+1.15e-5` | `+5.42e-6` | `1.00090 / 1.00031` | `4.02e-13` | `>4,400×` suppressed |
| Unassisted 2-mass Landis | tumble | tumble | $\max|\Delta\theta|=16{,}215.0^\circ$ | — | final spin $\omega_f = 2.199$ |

---

## 5. Three-Dimensional Oblate $J_2$ Symmetry Breaking and Control Subtraction (`R2`)

- **Rodrigues axis (`NEG-W18`):** The $2\pi/3$ cyclic permutation $(1,0,0) \mapsto (0,-1,0) \mapsto (0,0,1) \mapsto (1,0,0)$ rotates about true invariant axis $\hat{\mathbf{n}} = (+1, +1, -1)/\sqrt{3}$.
- **Subtracted $L=0$ control (`NEG-W17`):** At simulation oblateness $J_2 R^2 = 0.05$ (`98.3×` real Earth's `5.088e-4` at $r = 9{,}304\text{ km}$), $i_0 = 45^\circ$, 5 orbits:
  - Spherical $J_2 = 0$: $|\Delta J_z| = 2.84\times 10^{-13}$, $|\Delta J_\perp| = 2.83\times 10^{-13}$, $i_{\mathrm{end}} = 45.0000^\circ$.
  - Oblate $L = 0$ control: $i_{\mathrm{end}} = 44.3968^\circ$, $p_{\mathrm{end}} = 1.05283$, $|\Delta J_z| = 2.50\times 10^{-13}$.
  - Oblate $L = 0.04$ triad: $i_{\mathrm{end}} = 44.3757^\circ$, $p_{\mathrm{end}} = 1.05002$, $S_z = +0.002150$, coupled Noether $\max|\Delta(L_z + S_z)| = 2.77\times 10^{-13}$.
  - **Subtracted finite-size signal:** $\Delta i_{\mathrm{shape}} = -21.10\text{ mdeg}$, $\Delta p_{\mathrm{shape}} = -0.002815$. *(Figure 2: `paper/figures/fig2_safe_perigee_j2_control.pdf`.)*

---

## 6. Theorem G4: $I_0$-Invariant Electrical Heat Wall and Mechanical-Hub Baseline (`D4`)

**Theorem 6.1 (Theorem G4, `NEG-W15`, `NEG-W27`)** `[G4N, X]`: For an iso-inertial spin-tensioned triad ($\omega_{\mathrm{spin}} = 2\Omega_{\max}$, $e = 0.25$, $r_p = 6{,}978.137\text{ km}$, independent electric winches with $\eta_{\mathrm{act}} = 0.88$, $\eta_{\mathrm{reg}} = 0.80$, $f_{\mathrm{elec}} = \eta_{\mathrm{act}}^{-1} - \eta_{\mathrm{reg}} = 37/110$), $I_0$ cancels identically between $P_{\mathrm{circ}}(q)$ and $P_{\mathrm{orb}}(q)$:
$$\frac{P_{\mathrm{heat}}^{\mathrm{elec}}(q)}{P_{\mathrm{orb}}(q)} = 9.8468\,(1 - q^2)^{-3/2} = \begin{cases} 9.85\times & (q \to 0^+), \\ 15.16\times & (q = 0.50), \\ 45.59\times & (q = 0.80), \\ 118.90\times & (q = 0.90). \end{cases}$$
A coupled mechanical differential / spring-drum hub ($f_{\mathrm{mech}} = 1.5\%$) exchanges centrifugal work elastically across the three arms, reducing waste heat by **`22.4×`** (from `312.2 W` to **`13.92 W`** at $q = 0.50$, i.e., `0.338 × P_orb`).

### Table 2: Reconciled Hardware Sizing ($q = 0.50$, $L = 20\text{ km}$, $M = 1{,}000\text{ kg}$, $e = 0.25$) `[G4N, X]`

| Metric | Canonical $I_0 = \frac23 M L^2$ | Sensitivity $I_0 = M L^2$ | Notes / Resolution |
|---|---:|---:|---|
| Equilateral circumradius $r_{\mathrm{eq}}$ [km] | `16.330` | `20.000` | Consistent collinear $I_0$ (`NEG-W27`) |
| Full orbital power $P_{\mathrm{orb}}(1)$ [W] | `41.19` | `61.78` | Safe-perigee $e = 0.25$ |
| Circulating winch power $P_{\mathrm{circ}}$ [W] | `928.2` | `1,392.3` | $\omega_{\mathrm{spin}} = 2\Omega_{\max}$ |
| Uncoupled electrical heat $P_{\mathrm{heat}}^{\mathrm{elec}}$ [W] | `312.2` | `468.3` | `15.16×` ($I_0$-invariant) |
| **Mechanical spring-drum hub heat** [W] | **`13.92`** | `20.88` | `22.4×` cut (`1.5%` friction loss) |
| Exact peak inertial tension $T_{\mathrm{pk}}$ [N] | `44.70` | `54.74` | `WP 031` printed `62.56 N` (`NEG-W18`) |
| Tapered Zylon tether mass [kg] | `3.93` | `4.81` | Working strain `0.430%` |
| **Flight baseline hardware mass** [kg] | **`45.43`** | `46.31` | vs. 5-yr Hall `100.52 kg` wet / `105.12 kg` dry |

*(Figure 3: `paper/figures/fig3_g4_mechanical_hub_sizing.pdf`.)*

---

## 7. Keyed Stochastic Replay (`P1`) and Epsilon Provenance (`Appendix A`)

- **Keyed RCT (`P1`):** `SplitMix64` (`seed = 0x484f52495a5f5031`), `1,600/1,600 PASS`, bit-exact digest `0x1156b7558c78243a`.
- **Epsilon (`Swift++`) Provenance (`[E, X]`):** Internal `Swift++` Library of Alexandria Epochs XXXVI–XXXVII ledgers (`INT-030`, `INT-031`) and Lean 4.36.0 integer/rational-bracket certificates (`NEG-W29`) are preserved transparently as author provenance while `code/piece1_sim.py` and `data/piece1_calibration.json` serve as the open canonical verification record. NASA NTRS `19910012850` for Landis (1990/1991) is retained per Round-1 verification.
