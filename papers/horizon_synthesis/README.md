# Horizon Synthesis: Three Canonical, Reconciled Working Pieces & Cross-Series Meta-Analysis

**Author:** Ergentics (`[E]`)  
**Cross-Verification & Synthesis:** Gemini 4 Neon (`[G4N]`), Grok Bot (`[GB]`), Cross-Checked (`[X]`)  
**Status:** Active maintained working editions synthesizing frozen clean-room Horizon parts `WP 030`–`WP 035` + `[G4N]` Cycle 1 + `[GB]` Round 1 + `[G4N]` Round-1 `[X]` reconciliation.

---

## 1. Six-to-Three Canonical Architecture

The six frozen clean-room Horizon working papers (`WP 030`–`WP 035`, preserved immutably under `papers/wp03*/cleanroom/` alongside their annotated Round-1 editions) are consolidated into **three standalone, publication-grade AMS `LaTeX` monographs**, each paired with a zero-dependency open Python~3.12 simulator, SHA-256-manifested calibration JSON, three vector PDF figures, a standalone-verified neutral `0/0` arXiv source tarball, and a 1-to-1 GitHub Flavored Markdown mirror:

| Piece | Synthesized Parts | Canonical Monograph | Open Verifier & Live Gates | arXiv Source Bundle | GFM Mirror |
|---|---|---|---|---|---|
| **Piece I** | `WP 030` + `WP 031` | [`piece1_propulsion_hardware.pdf`](piece1_propulsion_hardware/paper/piece1_propulsion_hardware.pdf) ([`.tex`](piece1_propulsion_hardware/paper/piece1_propulsion_hardware.tex)) | [`piece1_sim.py`](piece1_propulsion_hardware/code/piece1_sim.py) (`7/7 PASS`) | [`piece1-...-arxiv.tar.gz`](piece1_propulsion_hardware/arxiv/piece1-propulsion-hardware-arxiv.tar.gz) | [`piece1_propulsion_hardware.md`](piece1_propulsion_hardware/piece1_propulsion_hardware.md) |
| **Piece II** | `WP 032` + `WP 033` | [`piece2_smallbody_crtbp.pdf`](piece2_smallbody_crtbp/paper/piece2_smallbody_crtbp.pdf) ([`.tex`](piece2_smallbody_crtbp/paper/piece2_smallbody_crtbp.tex)) | [`piece2_sim.py`](piece2_smallbody_crtbp/code/piece2_sim.py) (`6/6 PASS`) | [`piece2-...-arxiv.tar.gz`](piece2_smallbody_crtbp/arxiv/piece2-smallbody-crtbp-arxiv.tar.gz) | [`piece2_smallbody_crtbp.md`](piece2_smallbody_crtbp/piece2_smallbody_crtbp.md) |
| **Piece III** | `WP 034` + `WP 035` | [`piece3_nullcone_tuft_hagedorn.pdf`](piece3_nullcone_tuft_hagedorn/paper/piece3_nullcone_tuft_hagedorn.pdf) ([`.tex`](piece3_nullcone_tuft_hagedorn/paper/piece3_nullcone_tuft_hagedorn.tex)) | [`piece3_sim.py`](piece3_nullcone_tuft_hagedorn/code/piece3_sim.py) (`5/5 PASS`) | [`piece3-...-arxiv.tar.gz`](piece3_nullcone_tuft_hagedorn/arxiv/piece3-nullcone-tuft-hagedorn-arxiv.tar.gz) | [`piece3_nullcone_tuft_hagedorn.md`](piece3_nullcone_tuft_hagedorn/piece3_nullcone_tuft_hagedorn.md) |

---

## 2. Unified Cross-Series Scientific Conventions

Every cross-paper inconsistency surfaced during Round-1 reconciliation is locked to a single canonical convention across all three maintained pieces:

| Domain | Unified Canonical Convention | Resolves |
|---|---|---|
| **Hopf Holonomy Basis** | Chiral equilateral-pole Jacobi basis $w_\pm = (z_1 \pm i z_2)/\sqrt{2}$; exact physical rotation `-90.0000°`, strictly collision-free $\min d_{ij} = \sqrt{2-\sqrt{3}}\,L \approx 0.517638\,L$ | `NEG-W2`, `NEG-W4`, `NEG-W25` |
| **Earth Radius & Safe Perigee** | WGS84 equatorial $R_\oplus = 6{,}378.137\text{ km}$, safe LEO perigee $r_p = 6{,}978.137\text{ km}$, `K9` optimal $e^* = 0.281702$ (`199.89 m/s/yr` at $L=20\text{ km}$) | `NEG-W1`, `NEG-W16`, `NEG-W27` |
| **Triad Polar Inertia $I_0$** | Canonical collinear $I_0 = \frac23 M L^2$ ($r_{\mathrm{eq}} = \sqrt{2/3}\,L = 16.330\text{ km}$, $P_{\mathrm{orb}} = 41.19\text{ W}$, $P_{\mathrm{heat}}^{\mathrm{elec}} = 312.2\text{ W}$ at $q=0.50$), with $I_0 = M L^2$ sensitivity (`61.78 W` / `468.3 W`) tabulated transparently alongside; Theorem G4 floor strictly $I_0$-invariant at **`9.85×`** (`15.16×` at $q=0.50$) | `NEG-W15`, `NEG-W18`, `NEG-W27` |
| **Piece I Flight Baseline** | Spin-tensioned Hopf triad with **coupled mechanical differential / spring-drum hub** (`1.5%` friction loss → `13.92 W` waste heat, `22.4×` reduction; `45.43 kg` hardware vs. `100.52 kg` wet 5-yr Hall) | `NEG-W15`, `NEG-W18` |
| **Sen (2013) Entropy Split** | `106/45` = fixed-$s_b$ trace $\operatorname{Tr}(C^\dagger C)$ (`WP 034`, `77/90` singlet); `167/90` = measure-weighted microcanonical density after $(4\pi s_b)^{-1/2}$ giving Hagedorn pole $\alpha = 257/90$ (`WP 035`); direct fixed-mass Sen requires $\alpha = 151/45$ | `NEG-W23`, `NEG-W30` |
| **Bibliographic & Proof Hygiene** | Chandrasekaran `arXiv:2611.34924v1` dated **25 Nov 2026**; Landis NASA NTRS `19910012850` retained; Lean 4.36.0 labeled honestly as integer/rational-bracket algebraic certificates; non-public Nielsen manuscript & `Swift++` *Epsilon* ledgers (`INT-030`–`INT-035`) isolated in Appendices | `NEG-W6`, `NEG-W24`, `NEG-W28`, `NEG-W29` |

---

## 3. Meta-Analysis of Novel Theorems (`Theorem G1`–`G6`) & Open Discoveries

| Theorem / Finding | Piece | Core Mathematical & Physical Result | Live Numerical Verification |
|---|---|---|---|
| **Theorem G1** `[G4N]` | Piece I | Exact iso-inertial Hopf kinetic-energy wall $K_{\mathrm{int}}^{\mathrm{peak}}/(\frac12 I_0\Omega^2) = q^2/(1-q^2)$, $r_{\max}(q) = L\sqrt{\frac23(1+q)}$ | `0.3333` ($q=0.50$), `2.6036` ($q=0.85$), `9.2564` ($q=0.95$, $r_{\max}=1.1402\,L$); err `9.38e-11` |
| **Theorem G2** `[G4N]` | Piece II | Exact 3-arm+hub barycentric post-jam FDIR inertia $I_{\mathrm{cm}}(d)/I_0 = 1 - \frac43 d + \frac7{12}d^2$ reverses tension sign | Retract $10\%$: jammed `+28.1%` overload; **extend $10\%$**: jammed **`-21.0%`** relief; poly err `2.22e-16` |
| **Theorem G3** `[G4N, X]` | Piece II | Laplace-coupled 3D $L_2$ multipole tensor; $y$-aligned triad is the unique optimal Halo gap-closing axis | EM $L_2$ $\Delta\text{gap} = -2.3748\,\epsilon^2$; Didymos $L_y^* = 40.44\text{ m}$ at **`107.0 m`** altitude (vs. `52.5 m` $x$-boom) |
| **Theorem G4** `[G4N, X]` | Piece I | $I_0$-invariant electrical heat wall $P_{\mathrm{heat}}^{\mathrm{elec}}/P_{\mathrm{orb}} = 9.8468(1-q^2)^{-3/2}$; coupled mechanical hub bypass | `9.85×` floor (`15.16×` at $q=0.50$, `118.90×` at $q=0.90$); mechanical hub cuts heat `22.4×` to **`13.92 W`** |
| **Theorem G5** `[G4N, X]` | Piece III | Kronecker density yields strictly nested strong exhaustions converging to *every* finite real target $L \in \mathbb{R}$ | $M=60$: `err(0)=0.0`, `err(+1)=3.50e-7`, `err(+42)=7.03e-8`, `err(1/sqrt(2), +1)=1.29e-5` |
| **Theorem G6** `[G4N, X]` | Piece III | Hagedorn nuclearity ($\beta_c = \beta_H > 0$) breaks canonical equivalence: $E/\langle E \rangle \to \mathrm{Gamma}(\alpha,\alpha)$ with $1/\sqrt{\alpha+2}$ bridge to `WP 034` $\mathrm{Beta}(\alpha,1)$ | $\alpha=257/90$: `59.18%` dispersion, `42.13%` tail vs. `26.86%` truncated (bridge `0.4538`); `1,600`-trial RCT `59.95%` / `41.69%` |
| **Open Discovery: Safe $W^u$** `[G4N]` | Piece II | Phase-scanning the open 42-ODE EM $L_2$ Halo orbit replaces `tau=0` lunar impact (`993.8 km`) with a non-impacting capture branch | `tau = 0.750` → **`r_p = 2,064.6 km` (`+327.2 km` lunar altitude)** in `18.10 d`; Floquet SK **`8,814×`** suppression (`2.95 m/s`) |
| **Open Discovery: 3D $J_2$ Control** `[G4N]` | Piece I | Subtracting an identical $L=0$ point-mass control with coupled $\dot S_z = \tau_z$ separates genuine shape signal from `96%+` $J_2$ precession | `max |Δ(L_z + S_z)| = 2.77e-13`; subtracted $\Delta i_{\mathrm{shape}} = -21.10\text{ mdeg}$, $\Delta p_{\mathrm{shape}} = -0.002815$ |

---

## 4. Complete 30-Item Audit Resolution Matrix (`NEG-W1`–`NEG-W30`)

Every single confirmed item from `NEGATIVES.md` is resolved in place across the three synthesized monographs:

| ID | Source WP | Synthesized Piece | Resolution Implemented in Canonical Synthesis |
|---|---|---|---|
| `NEG-W1` | `WP 030` | Piece I (§4) | Replaced subsurface $r_p = 5{,}250\text{ km}$ with WGS84 safe perigee $r_p = 6{,}978.137\text{ km}$ (`199.89 m/s/yr`) |
| `NEG-W2` | `WP 030` | Piece I (§3) | Replaced colliding $(z_1,z_2)$ loop with collision-free equilateral-pole $w_\pm$ chart ($\min d_{ij} = 0.5176\,L$) |
| `NEG-W3` | `WP 030` | Piece I (§3, Thm G1) | Replaced constant-energy assumption with exact wall $K_{\mathrm{int}}^{\mathrm{peak}}/(\frac12 I_0\Omega^2) = q^2/(1-q^2)$ |
| `NEG-W4` | `WP 030` | Piece I (§2) | Separated mass-quadrupole $Q_{ij}$ and inertia $I_{ij} = I_0\delta_{ij}-Q_{ij}$ sign explicitly (`0.0` trace residual) |
| `NEG-W5` | `WP 030` | Piece I (§4) | Corrected Regime A safe-perigee tidal tension to `0.1173 N`; separated osculating vs. total-energy elements |
| `NEG-W6` | `WP 030` | Piece I (§4, App. A) | Corrected Bennu $(L/R)^2 = 7.84\times 10^6$, tension `3.13e-5 N`, `F35` `84.79%`; **NTRS `19910012850` retained** |
| `NEG-W7` | `WP 032` | Piece II (§2.1) | Included $-J_2/2 = -0.00875$ with $+3C_{22} = +0.0174 \implies +0.00865$ (`7.86×` SRP at $R=600\text{ m}$, $R_{\mathrm{eq}}=997.0\text{ m}$) |
| `NEG-W8` | `WP 032` | Piece II (§2.2, Thm G2) | Reversed post-jam FDIR law: extend healthy arms (`-21.0%` jammed relief) instead of retracting (`+28.1%` overload) |
| `NEG-W9` | `WP 032` | Piece II (§3.1) | Distinguished passive `11:1` anisotropic $L_4$ curvature from active isotropic stabilization ($\epsilon \ge 0.04195$) |
| `NEG-W10` | `WP 032` | Piece II (§3.1) | Corrected $\mu_R(0.02) = 0.0515459$ (`+33.81%`) and exact Gascheau $\lambda = 0.537285$ (`0.425%` error) |
| `NEG-W11` | `WP 033` | Piece II (§4, Prop. 4.1) | Flagged `tau=0` (`993.8 km`) as lunar impact; discovered elevated safe $W^u$ branch (`tau=0.750`, `+327.2 km` alt) |
| `NEG-W12` | `WP 033` | Piece II (§3.2, Thm G3) | Replaced unphysical decoupled $k_z$ with coupled 3D multipole tensor; optimal Didymos $y$-span $L_y^* = 40.44\text{ m}$ |
| `NEG-W13` | `WP 033` | Piece II (§5) | Modeled OSIRIS-REx fluidized regolith `500–700 kg/m^3` (`18.24 cm` at `600 kg/m^3`, explicit $A_h = 28.27\text{ m}^2, C_D = 1.60$) |
| `NEG-W14` | `WP 033` | Piece II (§5) | Evaluated true flight regime ($\eta=1.617, \chi=10.88$) with full $1/r^2$ + `15.71%` centrifugal relief (`18.81 m` drift) |
| `NEG-W15` | `WP 031` | Piece I (§6, Thm G4) | Replaced electric-winch heat claim with $I_0$-invariant `9.85×` wall (`15.16×` at $q=0.50$) and mechanical-hub baseline (`13.92 W`) |
| `NEG-W16` | `WP 031` | Piece I (§4, Prop. 4.1) | Corrected printed safe-perigee $\Delta v_{\mathrm{yr}}$ formula and `K9` headline (`199.89 m/s/yr`) |
| `NEG-W17` | `WP 031` | Piece I (§5) | Disclosed `98.3×` $J_2$ amplification; added subtracted $L=0$ control & coupled $J_z = L_z + S_z$ (`-21.10 mdeg` shape signal) |
| `NEG-W18` | `WP 031` | Piece I (§5–6) | Corrected Rodrigues axis to $(+1,+1,-1)/\sqrt{3}$, exact $T_{\mathrm{pk}}$ (`44.70 N` / `54.74 N`), and 5-yr Hall wet (`100.52 kg`) / dry (`105.12 kg`) |
| `NEG-W19` | `WP 034` | Piece III (§2) | Proved authentic 106-bit DD fails (`96.17%` at $10^{33}$, `100%` at $10^{40}$); exact algebraic cancellation gives `0.0` `f64` error at $10^{77}$ |
| `NEG-W20` | `WP 034` | Piece III (§3, Thm G5) | Upgraded Counterexample 2 to universal Kronecker convergence to every finite real $L \in \mathbb{R}$ via strictly nested exhaustions |
| `NEG-W21` | `WP 034` | Piece III (§2) | Stated explicit domains: `C156` $R \ge e^{13/7} = 6.4054$, $\beta^*(C=1) = 2.67525$, $C_{\arg\min} = 5/\pi^4 = 0.05133$ |
| `NEG-W22` | `WP 035` | Piece III (§5) | Corrected spectral-zeta magnitude ratios to `29.18×` on $S^3$ (rem `-0.0304485`) and `21.94×` on $S^5$ (rem `+0.0801130`) |
| `NEG-W23` | `WP 035` | Piece III (§4, §6, Thm G6) | Reconciled $\alpha=257/90 \leftrightarrow 167/90$, tightened R3(1) boundary ($Z(\beta_H)=1$ witness), added Theorem G6 & `WP 034` bridge |
| `NEG-W24` | `WP 035` | Piece III (§5, App. A) | Added $10^{1/4}$ Lemma 8 factor, `+428.2σ` 4-loop QED $a_e$ closure, `4+4` Beltrami split, fixed Ref `[12]` path, marked Nielsen non-public |
| `NEG-W25` | `WP 030` | Piece I (§3) | Fixed `+90°` physical sign error via equilateral-pole $w_\pm$ basis (`-90.0000°` physical) |
| `NEG-W26` | `WP 030` | Piece I (§2) | Named summation orders (`5.75e-8` factored / `3.46e-7` mean-sub) and exact wipeout cliff (`48.0%` at $10^{-8}$, `100%` at $5\times 10^{-9}$) |
| `NEG-W27` | `WP 030/031` | Piece I (§4, §6) | Unified WGS84 $R_\oplus = 6{,}378.137\text{ km}$, canonical $I_0 = \frac23 ML^2$ (+ $ML^2$ sensitivity), and $I_0$-invariant `9.85×` G4 floor |
| `NEG-W28` | `WP 034/035` | Piece III (§1, Bib) | Corrected `arXiv:2611.34924v1` submission date to **25 November 2026** |
| `NEG-W29` | All WPs | Pieces I–III (App. A) | Relabeled Lean 4.36.0 proofs honestly as integer/rational-bracket algebraic certificates |
| `NEG-W30` | `WP 034/035` | Piece III (§4) | Explicitly separated `106/45` fixed-$s_b$ trace (`WP 034`) from `167/90` measure-weighted density / $\alpha = 257/90$ (`WP 035`) |

---

## 5. One-Command Full Reproduction Across All Three Pieces

```bash
python3 papers/horizon_synthesis/piece1_propulsion_hardware/code/piece1_sim.py
python3 papers/horizon_synthesis/piece2_smallbody_crtbp/code/piece2_sim.py
python3 papers/horizon_synthesis/piece3_nullcone_tuft_hagedorn/code/piece3_sim.py
sha256sum -c papers/horizon_synthesis/piece*/data/MANIFEST.sha256
```

All `18/18` open deterministic, runtime, and keyed stochastic gates (`7 + 6 + 5`) pass from standard Python 3.12 with zero third-party packages.
