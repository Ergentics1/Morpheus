# Grok Bot (`[GB]`) Round-1 Reconciliation — Working Paper 031

*3D J2 Symmetry Breaking, SO(3) Holonomy and HIL Sizing* · Round 1 · 2026-11-26 · Method: ADPIE, as in the Morpheus v0.2.0 and round-2/3 reconciliations.

## Scope and rules

- Inputs: the frozen `cleanroom/` manuscript and the `[G4N]` Cycle-1 dossier in this folder. `[GB]` checks were written from scratch, without reading `[G4N]` code or data; `[G4N]`'s verifiers were then re-run separately.
- The reconciled edition is [`../paper/paper.typ`](../paper/paper.typ) → [`../paper/paper.pdf`](../paper/paper.pdf): every `[E]` line is kept verbatim and in order; verdicts are inserted as boxed notes. Corrections are proposed, not applied.
- Claims attributed to the Ergentics internal model / Swift++ corpus are never altered. Where they can't be checked from this repository they are marked **UNVERIFIABLE**.

**Verdict totals:** CONFIRMED 3 · CONFIRMED-IN-SUBSTANCE 1 · DISPUTED 1 · UNVERIFIABLE 1 · NEW 2

## Verdict table

| ID | Item | Verdict | Placed under |
| :--- | :--- | :--- | :--- |
| `NEG-W15` | Spin tension vs zero-spin holonomy (Theorem G4) | **CONFIRMED** | § “Closed-Loop HIL” |
| `GB-W27b` | Triad inertia convention | **NEW** | § “Closed-Loop HIL” |
| `NEG-W16` | Theorem 3 printed Δv formula | **CONFIRMED** | § “Fixed-Safe-Perigee” |
| `NEG-W17` | J2 drift is mostly point-mass precession | **CONFIRMED-IN-SUBSTANCE** | § “3D Oblate” |
| `NEG-W18` | Euler axis, T_pk, strain and Hall mass | **CONFIRMED** | § “3D Plane-Lock” |
| `NEG-W18/NTRS` | Ref [3] NTRS ID | **DISPUTED** | end of paper (before References) |
| `GB-W27a` | Earth radius | **NEW** | § “Fixed-Safe-Perigee” |
| `INT-031` | Pass 9B ledger, Pinakes 144/144, 57,600 RCT, K9 certificate, F36 HIL, XCTests | **UNVERIFIABLE** | § “Executable” |

## Evidence

### `NEG-W15` — Spin tension vs zero-spin holonomy (Theorem G4) · **CONFIRMED**

Holding a spin of 2Ω_max costs P_circ = 1392.5 W at q = 0.5 (numeric integration equals the closed form) with 468.4 W heat. A spinning rigid triad has non-zero angular momentum, so it cannot also execute §1's zero-momentum SO(3) holonomy; and a quadrupole spinning freely averages out to no net pumping (ρ̈ = −ω²ρ). The paper needs to say which mode is the flight baseline. Author decision.

### `GB-W27b` — Triad inertia convention · **NEW**

WP030's collinear triad has I0 = (2/3)ML²; WP031's three-arm hardware has I0 = ML². WP031's power budget uses WP030's (2/3) law (P_orb = 41.19 W); with its own geometry it is 61.78 W. Part of proposed NEG-W27.

### `NEG-W16` — Theorem 3 printed Δv formula · **CONFIRMED**

The printed formula gives 0.02645 m/s/yr against 199.8882 from the paper's own numbers; the printed expression drops factors that the paper's own numerical result includes.

### `NEG-W17` — J2 drift is mostly point-mass precession · **CONFIRMED-IN-SUBSTANCE**

A point-mass (L = 0) J2 baseline already gives |ΔJ⊥| = 3.51 with my initial conditions (circular r = 1), i_end = 42.76°, Δ|L| = −0.111, the same size as the paper's 3.087. G4N gets 3.0859 with theirs. The tether's own contribution is the small difference; exact numbers need the initial-condition spec.

### `NEG-W18` — Euler axis, T_pk, strain and Hall mass · **CONFIRMED**

Fig. 1 axis is [+1, +1, −1]/√3, not [−1, 1, −1]/√3. T_pk is 62.56 N as printed vs 54.74 N with the consistent formula; strain 0.5271% exceeds σ_allow/E = 0.4296%; Hall mass 100.52 kg (wet 1000) vs 105.12 kg (dry 1000 plus payload). The collinear-fold actuation scope point is accepted qualitatively.

### `NEG-W18/NTRS` — Ref [3] NTRS ID · **DISPUTED**

NTRS 19910012850 is Landis, 'Reactionless propulsion using tethers' (April 1990, NASA CP-10059). Ref [3] is correct as printed.

### `GB-W27a` — Earth radius · **NEW**

WP031 uses 6,378.137 km; G4N's WP030 corrections use 6,371 km. Adopt one across the series (NEG-W27).

### `INT-031` — Pass 9B ledger, Pinakes 144/144, 57,600 RCT, K9 certificate, F36 HIL, XCTests · **UNVERIFIABLE**

Internal toolchain, kept verbatim. G4N verifiers re-run: Python, Rust, 9/9 Lean pass. Rust 1.100.0 is claimed; the box's 1.85.1 also passes.

## Run spec requested from the author

**SPEC-031 — 5-orbit J2 diagnostic (§2, Fig. 2) and HIL slack test (§4)**

| Field | Needed |
| :--- | :--- |
| Units | μ, R_E (6,378.137 km assumed), J2, tether L (nondimensional) |
| Initial state | r0, v0 vector, inclination i0, RAAN, argument of perigee, initial triad attitude and spin |
| Baseline | whether a point-mass (L = 0) run under the same J2 field was subtracted |
| Integrator | method, step/tolerance, orbit count |
| HIL | controller gains, sensor noise, slack threshold, tick length, 2,000-tick seed |

## Reproduce (from the repository root)

```bash
python3 reconciliation/horizon_round1/code/gb_r1_wp031_035.py
python3 papers/wp031_3d_j2_hil/code/*.py   # [G4N] plane 1
lake -d papers/wp031_3d_j2_hil/lean build   # [G4N] plane 2 (Lean 4.36.0)
cargo test --manifest-path papers/wp031_3d_j2_hil/rust/Cargo.toml   # [G4N] plane 3
typst compile papers/wp031_3d_j2_hil/paper/paper.typ
```
