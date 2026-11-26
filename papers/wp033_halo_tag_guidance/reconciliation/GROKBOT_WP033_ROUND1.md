# Grok Bot (`[GB]`) Round-1 Reconciliation — Working Paper 033

*3D Halo/Lissajous Manifolds, Floquet Control and Bennu TAG Guidance* · Round 1 · 2026-11-26 · Method: ADPIE, as in the Morpheus v0.2.0 and round-2/3 reconciliations.

## Scope and rules

- Inputs: the frozen `cleanroom/` manuscript and the `[G4N]` Cycle-1 dossier in this folder. `[GB]` checks were written from scratch, without reading `[G4N]` code or data; `[G4N]`'s verifiers were then re-run separately.
- The reconciled edition is [`../paper/paper.typ`](../paper/paper.typ) → [`../paper/paper.pdf`](../paper/paper.pdf): every `[E]` line is kept verbatim and in order; verdicts are inserted as boxed notes. Corrections are proposed, not applied.
- Claims attributed to the Ergentics internal model / Swift++ corpus are never altered. Where they can't be checked from this repository they are marked **UNVERIFIABLE**.

**Verdict totals:** CONFIRMED 5 · UNVERIFIABLE 2 · SPEC-NEEDED 1

## Verdict table

| ID | Item | Verdict | Placed under |
| :--- | :--- | :--- | :--- |
| `HALO-RERUN` | Independent halo re-run from the paper's state | **CONFIRMED** | § “Live 42-ODE” |
| `NEG-W11` | The W^u 'lunar tube' passes inside the Moon | **CONFIRMED** | § “3D Collinear” |
| `NEG-W12` | Theorem G3 coupled stiffness and gap sensitivities | **CONFIRMED** | § “3D Collinear” |
| `NEG-W13` | Regolith density and C_D | **CONFIRMED** | § “Nightingale” |
| `NEG-W14` | Certified intervals vs the operating regime | **CONFIRMED** | § “Nightingale” |
| `SIM-033` | Station-keeping (3,051× vs 3,442×), W^u kick, TAG Monte Carlo | **SPEC-NEEDED** | § “Live 42-ODE” |
| `REF-12` | Ref [12] cites an internal Swift++ calibration ledger | **UNVERIFIABLE** | end of paper (before References) |
| `INT-033` | Pass 9B ledger and certificates C149–C152, K11, F38 | **UNVERIFIABLE** | § “Executable” |

## Evidence

### `HALO-RERUN` — Independent halo re-run from the paper's state · **CONFIRMED**

Closure 1.6e-8, C_J = 3.12579292, λ_u = 746.7213, ν1 = 373.3613, ν2 = 0.84093, winding 32.76°/orbit: all reproduce. Symplectic residual 7.8e-11 with a tight-tolerance adaptive integrator; the paper's printed residual is larger, which is integrator-dependent and not an error.

### `NEG-W11` — The W^u 'lunar tube' passes inside the Moon · **CONFIRMED**

1,003.71 km from the Moon's centre is 733.7 km below the surface. In the re-run, a 1e-4 kick along +v_u hits the lunar surface at about 17.4 days; along −v_u it stays 47,315 km away. The branch the paper shows is an impact trajectory.

### `NEG-W12` — Theorem G3 coupled stiffness and gap sensitivities · **CONFIRMED**

Gap sensitivities +0.0802, −2.3748, +2.2946, −1.1473 (x, y, z, equilateral) reproduce exactly. L_y* = 40.44 m was not independently recomputed.

### `NEG-W13` — Regolith density and C_D · **CONFIRMED**

χ(600) = 10.886, sink 18.24 cm. C_D = 1.60 could not be re-derived because the contact area is not stated.

### `NEG-W14` — Certified intervals vs the operating regime · **CONFIRMED**

η is 8.08× and χ 144× outside the certified intervals; constant-g drift 15.99 m; centrifugal relief 1.27e-5 m/s² = 15.7% of g.

### `SIM-033` — Station-keeping (3,051× vs 3,442×), W^u kick, TAG Monte Carlo · **SPEC-NEEDED**

Depend on noise seed, burn schedule, kick direction and size. Run spec in the dossier.

### `REF-12` — Ref [12] cites an internal Swift++ calibration ledger · **UNVERIFIABLE**

The Epoch XXXIX calibration document is not public or in the repository. Suggest marking it 'internal, not public' (as G4N asked for WP035 Ref [12]) and citing the archived sibling working papers by their repository location.

### `INT-033` — Pass 9B ledger and certificates C149–C152, K11, F38 · **UNVERIFIABLE**

Internal toolchain, kept verbatim. G4N verifiers re-run: Python, Rust, 7/7 Lean pass.

## Run spec requested from the author

**SPEC-033 — W^u branch, station-keeping and TAG Monte Carlo**

| Field | Needed |
| :--- | :--- |
| W^u | kick size (1e-4 assumed) and sign convention for the unstable eigenvector (the +v_u branch impacts the Moon at about 17.4 d; the −v_u branch does not) |
| Station-keeping | noise model and seed, burn cadence, deadband, control law, horizon (3,051× vs 3,442× depends on these) |
| TAG | contact area A_h (needed to check C_D = 1.60), regolith density used, Monte Carlo seed and N |
| Didymos L2 | μ, separation, triad L used for L_y* = 40.44 m |

## Reproduce (from the repository root)

```bash
python3 reconciliation/horizon_round1/code/gb_r1_wp031_035.py
python3 reconciliation/horizon_round1/code/gb_r1_wp033_halo.py
python3 papers/wp033_halo_tag_guidance/code/*.py   # [G4N] plane 1
lake -d papers/wp033_halo_tag_guidance/lean build   # [G4N] plane 2 (Lean 4.36.0)
cargo test --manifest-path papers/wp033_halo_tag_guidance/rust/Cargo.toml   # [G4N] plane 3
typst compile papers/wp033_halo_tag_guidance/paper/paper.typ
```
