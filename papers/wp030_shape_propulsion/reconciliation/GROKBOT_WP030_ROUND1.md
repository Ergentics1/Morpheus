# Grok Bot (`[GB]`) Round-1 Reconciliation — Working Paper 030

*Shape-Controlled Gravitational Propulsion Resolved* · Round 1 · 2026-11-26 · Method: ADPIE, as in the Morpheus v0.2.0 and round-2/3 reconciliations.

## Scope and rules

- Inputs: the frozen `cleanroom/` manuscript and the `[G4N]` Cycle-1 dossier in this folder. `[GB]` checks were written from scratch, without reading `[G4N]` code or data; `[G4N]`'s verifiers were then re-run separately.
- The reconciled edition is [`../paper/paper.typ`](../paper/paper.typ) → [`../paper/paper.pdf`](../paper/paper.pdf): every `[E]` line is kept verbatim and in order; verdicts are inserted as boxed notes. Corrections are proposed, not applied.
- Claims attributed to the Ergentics internal model / Swift++ corpus are never altered. Where they can't be checked from this repository they are marked **UNVERIFIABLE**.

**Verdict totals:** CONFIRMED 8 · CONFIRMED-IN-SUBSTANCE 1 · DISPUTED 1 · UNVERIFIABLE 3 · SPEC-NEEDED 1 · NEW 3

## Verdict table

| ID | Item | Verdict | Placed under |
| :--- | :--- | :--- | :--- |
| `NEG-W1` | Table 1 Regimes A/B have underground perigees | **CONFIRMED** | § “Quantitative Mission Dominance” |
| `NEG-W5` | Regime A tension 0.0012 N is about 100× too low | **CONFIRMED** | § “Quantitative Mission Dominance” |
| `NEG-W6` | Regime C exponent, Bennu tension, SRP dominance | **CONFIRMED** | § “Quantitative Mission Dominance” |
| `NEG-W6/7a` | C138 ≤ 1e-6 octupole bound | **UNVERIFIABLE** | § “The Iso-Inertial Hopf-Fibration” |
| `NEG-W6/7b` | F35 loss is 84.8%, not 84.6% | **CONFIRMED** | § “Exact Eq. (5) Regeneration” |
| `NEG-W6/7c` | Ref [1] NTRS ID | **DISPUTED** | end of paper (before References) |
| `REF-12` | Ref [12] cites an internal Swift++ calibration ledger | **UNVERIFIABLE** | end of paper (before References) |
| `NEG-W2` | Θ = π/3 holonomy loop hits two binary collisions; Θ = 0 is collinear | **CONFIRMED** | § “The Iso-Inertial Hopf-Fibration” |
| `GB-W25` | Holonomy sign: net physical rotation is +90°, not −90° | **NEW** | § “The Iso-Inertial Hopf-Fibration” |
| `NEG-W4` | Theorem 2 sign: the printed Q is the mass quadrupole | **CONFIRMED** | § “The Iso-Inertial Hopf-Fibration” |
| `NEG-W3` | Theorem G1: exact shape kinetic energy | **CONFIRMED** | § “Exact Eq. (5) Regeneration” |
| `NOTE-8` | Specify μ_tot and the energy convention for a_f, e_f | **CONFIRMED** | § “Live Coupled 4-Body” |
| `GB-W26` | The naive rounding error depends on evaluation order | **NEW** | § “Immediate Audit & Cancellation” |
| `GB-W27a` | Earth-radius convention differs across the series | **NEW** | § “Quantitative Mission Dominance” |
| `X-MISSION` | Mission figure across WP030/WP031/G4N: 619.8 vs 220.2 vs 199.9 m/s/yr | **CONFIRMED-IN-SUBSTANCE** | § “Quantitative Mission Dominance” |
| `SIM-030` | Coupled 4-body numbers (tumbles, ΔE, Eq. 5 residual, Arm A spin-up) | **SPEC-NEEDED** | § “Live Coupled 4-Body” |
| `INT-030` | Internal Swift++ corpus claims | **UNVERIFIABLE** | § “Blinded Empirical Validation” |

## Evidence

### `NEG-W1` — Table 1 Regimes A/B have underground perigees · **CONFIRMED**

r_p = a(1−e) = 6,300 km (A) and 5,250 km (B), both below Earth's radius. Recomputed on a valid r_p = 6,800 km: Regime B 220.2 m/s/yr (was 619.8), Regime A 3.81 mm/s/yr (was 5.17); tension 25.35 N at r_p = 6,800 km (μ M L / r_p³). The arithmetic in Table 1 is right for the stated (a, e); the orbits are not physical. WP031 §3 already re-derives a safe-perigee optimum (199.89 m/s/yr at 600 km altitude), which supersedes both figures (see X-MISSION).

### `NEG-W5` — Regime A tension 0.0012 N is about 100× too low · **CONFIRMED**

μ M L / r_p³ with M = 1000 kg, L = 100 m gives 0.1594 N at r_p = 6,300 km and 0.1268 N at 6,800 km (0.1162 N at a = 7,000 km). Regime B's 55.1 N reproduces (55.09 N), so the Regime A cell is a typo, not a formula error.

### `NEG-W6` — Regime C exponent, Bennu tension, SRP dominance · **CONFIRMED**

7.84e6 = (L/R)² ratio Bennu vs Earth, not L²/R⁴ (that ratio is 6.15e13 at fixed μ). Bennu tension μ M L/R³ = 3.131e-5 N (not below 1e-6 N). Raw |Δa∥| = 2 μ L²/R⁴ = 2.505e-9 m/s², below 1 AU SRP 4.56e-8 m/s² at A/M = 0.01. Extra [GB] point: the physical Δa near Bennu is about 0.75× the Earth benchmark, so the 7.84e6 'boost' is a dimensionless ratio, not an acceleration gain. Bennu Δv recomputes to 11.69 mm/s/yr (a = 2.5 km, e = 0.25).

### `NEG-W6/7a` — C138 ≤ 1e-6 octupole bound · **UNVERIFIABLE**

C138 is an internal Swift++ certificate. G4N's octupole scope point (bound needs the zero-octupole symmetric configuration) is plausible but its 1.29e-5 figure was not independently recomputed in this round. The [E] claim is left verbatim.

### `NEG-W6/7b` — F35 loss is 84.8%, not 84.6% · **CONFIRMED**

q(e* = 0.0275) = 0.847858, i.e. 84.8%.

### `NEG-W6/7c` — Ref [1] NTRS ID · **DISPUTED**

NASA NTRS 19910012850 is G. A. Landis, 'Reactionless propulsion using tethers' (April 1990), the paper inside the Vision-21 proceedings (NASA CP-10059; the volume itself is NTRS 19910012826). NTRS 19910029285 is the different October 1990 paper 'Reactionless orbital propulsion using tether deployment', which is Ref [2]'s conference version. Ref [1] as printed is correct; G4N's proposed change should not be applied.

### `REF-12` — Ref [12] cites an internal Swift++ calibration ledger · **UNVERIFIABLE**

The Epoch XXXVI calibration document is not public or in the repository. Suggest marking it 'internal, not public' (as G4N asked for WP035 Ref [12]) and citing the archived sibling working papers by their repository location.

### `NEG-W2` — Θ = π/3 holonomy loop hits two binary collisions; Θ = 0 is collinear · **CONFIRMED**

In the paper's (z1, z2) chart, d23 = 0 at Φ = 0 and d13 = 0 at Φ = π. Θ = 0 gives bodies at (1, −1, 0): collinear, not equilateral. The equilateral shape sits at Θ = Φ = π/2 in this chart. G4N's equilateral-pole basis loop at β = π/3 is collision-free (min d/L = 0.517638 = √(2−√3)) with |Q| independent of χ.

### `GB-W25` — Holonomy sign: net physical rotation is +90°, not −90° · **NEW**

Integrating the zero-spin condition around the paper's own loop (Φ: 0→2π at Θ = π/3) gives Δθ0 = −90° for the chart angle, but the labelled bodies end up rotated by +90°: the chart's quadrupole phase carries an extra π over the loop. The −90° in Theorem 3, Fig. 3 and the abstract is the chart angle, not the physical attitude change. G4N's basis gives −90° physically, so the sign depends on the basis and orientation; the paper should state the convention. Proposed NEG-W25.

### `NEG-W4` — Theorem 2 sign: the printed Q is the mass quadrupole · **CONFIRMED**

Σ m ρ² equals the paper's (M/3)(z1²+z2²) to 3.8e-15, while (Ixx−Iyy)+2i Ixy equals −Σ m ρ² to 4.4e-16. The identity is right if the left side is read as the mass quadrupole; with the inertia tensor it needs a minus sign. Iso-inertial |Izz − I0| ≤ 1.3e-15 confirmed.

### `NEG-W3` — Theorem G1: exact shape kinetic energy · **CONFIRMED**

Direct numerical differentiation of the zero-spin triad gives T/(½ I0 Ω²) = 0.3333, 1.0000, 2.6036, 9.2564 at q = 0.5, 0.7071, 0.85, 0.95, equal to q²/(1−q²), and max|ρ|/L = √(2(1+q)/3). The §4.1 estimate holds only near q = 1/√2. G4N's hard-span parity factor was not separately re-derived.

### `NOTE-8` — Specify μ_tot and the energy convention for a_f, e_f · **CONFIRMED**

Keplerian elements from the total ΔE (μ = 1, M = 3, p = 0.96) give a_f = 1.00486, e_f = 0.21130 vs the printed 1.0046, 0.2106; the gap is the osculating vs total-energy convention G4N flagged.

### `GB-W26` — The naive rounding error depends on evaluation order · **NEW**

The binary64 'naive' contrast error is not one number: μ/3·(a+b−2c) gives 5.75e-8, summing three point accelerations gives 3.46e-7; the printed 1.89e-7 sits between them. ε = 1e-7 reproduces 8.20e-3 exactly, but ε = 1e-8 gives 48%, not 100% (100% only below about 5e-9). The qualitative point stands; the figures should name the evaluation order. Proposed NEG-W26 (minor).

### `GB-W27a` — Earth-radius convention differs across the series · **NEW**

G4N's WP030 corrections use the mean radius 6,371 km; WP031 uses the equatorial 6,378.137 km. r_p = 6,800 km is 429 km altitude in one and 421.9 km in the other. Pick one (equatorial, as WP031 does) for all Horizon papers. Part of proposed NEG-W27.

### `X-MISSION` — Mission figure across WP030/WP031/G4N: 619.8 vs 220.2 vs 199.9 m/s/yr · **CONFIRMED-IN-SUBSTANCE**

All three are arithmetically right for their own perigee: 619.8 (r_p = 5,250 km, underground), 220.2 (G4N, r_p = 6,800 km), 199.89 (WP031 K9 optimum at 600 km altitude; 198.58 at e = 0.25). WP031's safe-perigee figure is the defensible headline. Author decision: which perigee convention the series adopts.

### `SIM-030` — Coupled 4-body numbers (tumbles, ΔE, Eq. 5 residual, Arm A spin-up) · **SPEC-NEEDED**

G4N's Python and Rust re-runs agree with each other and with the trend in the paper, but the paper does not give the switching law, gains, q_max, L_min, step count, tumble metric or initial conditions, so no independent third run is possible. A run spec is in the [GB] dossier; the exact figures stay as printed until the author supplies it.

### `INT-030` — Internal Swift++ corpus claims · **UNVERIFIABLE**

Pass 9B Zero-LLVM, SppMLIR certificates C137–C140 and K8, the N = 1,600 RCT counts, Pinakes scroll counts and the corpus totals rest on the internal Ergentics toolchain, which is not in the repository. They are kept verbatim and not altered. Independently re-checkable parts (K8 root e* = 0.1150133…, Eq. 5 identity) were confirmed by G4N's verifiers, re-run here: 9/9 Python, 7/7 Rust, 15/15 Lean.

## Run spec requested from the author

**SPEC-030 — coupled 4-body triad and Landis tether runs (§3, Fig. 2, Fig. 4)**

| Field | Needed |
| :--- | :--- |
| Units / constants | μ (or G, M_p), triad mass M and per-body m, L_max, L_min (Landis arm) |
| Initial state | a0, e0 = 0.2, true anomaly at t = 0, initial shape (α or (Θ, Φ, θ0)), initial spin |
| Control law | the switching function α(t) or q(t): trigger (true anomaly / radius / energy), gain k, q_max, slew-rate limit |
| Integrator | method, fixed step or tolerance, steps per orbit, number of orbits (5 stated) |
| Diagnostics | definition of a 'tumble' (angle threshold, frame), ΔE definition (osculating vs total), the Eq. 5 residual normalisation |
| Arm A (Landis) | retraction profile, whether arm inertia is included, spin-up metric |
| Seeds | RNG seed and stream for the N = 1,600 trials (G4N uses SplitMix64; state the [E] generator) |

## Reproduce (from the repository root)

```bash
python3 reconciliation/horizon_round1/code/gb_r1_wp030.py
python3 papers/wp030_shape_propulsion/code/*.py   # [G4N] plane 1
lake -d papers/wp030_shape_propulsion/lean build   # [G4N] plane 2 (Lean 4.36.0)
cargo test --manifest-path papers/wp030_shape_propulsion/rust/Cargo.toml   # [G4N] plane 3
typst compile papers/wp030_shape_propulsion/paper/paper.typ
```
