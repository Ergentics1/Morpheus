# Grok Bot (`[GB]`) Round-1 Reconciliation — Working Paper 032

*Bennu Proximity Ops, Multi-Tether FEM/FDIR and the Extended-Body 3-Body Problem* · Round 1 · 2026-11-26 · Method: ADPIE, as in the Morpheus v0.2.0 and round-2/3 reconciliations.

## Scope and rules

- Inputs: the frozen `cleanroom/` manuscript and the `[G4N]` Cycle-1 dossier in this folder. `[GB]` checks were written from scratch, without reading `[G4N]` code or data; `[G4N]`'s verifiers were then re-run separately.
- The reconciled edition is [`../paper/paper.typ`](../paper/paper.typ) → [`../paper/paper.pdf`](../paper/paper.pdf): every `[E]` line is kept verbatim and in order; verdicts are inserted as boxed notes. Corrections are proposed, not applied.
- Claims attributed to the Ergentics internal model / Swift++ corpus are never altered. Where they can't be checked from this repository they are marked **UNVERIFIABLE**.

**Verdict totals:** CONFIRMED 5 · UNVERIFIABLE 2 · SPEC-NEEDED 1

## Verdict table

| ID | Item | Verdict | Placed under |
| :--- | :--- | :--- | :--- |
| `NEG-W7` | Theorem 1 potential: missing −J2/2 and a factor 3 | **CONFIRMED** | § “Bennu (101955) Triaxial” |
| `NEG-W8` | Theorem G2: post-jam retraction spins the triad up | **CONFIRMED** | § “16-Node” |
| `NEG-W9` | L4 stiffness: passive term is positive, xx:yy = 1:11 | **CONFIRMED** | § “Fresh Three-Body Problem A” |
| `NEG-W10` | μ_R(0.02) and the Lyapunov error | **CONFIRMED** | § “Fresh Three-Body Problem A” |
| `SIM-032` | Kick growth (5,570× vs 11,618×), ladder values, FEM/FDIR counts | **SPEC-NEEDED** | § “Fresh Three-Body Problem B” |
| `HK-032` | Stale 'WP031 not yet archived' note | **CONFIRMED** | § “Conclusion” |
| `REF-12` | Ref [12] cites an internal Swift++ calibration ledger | **UNVERIFIABLE** | end of paper (before References) |
| `INT-032` | Pass 9B ledger and certificates C145–C148, K10, F37 | **UNVERIFIABLE** | § “Executable” |

## Evidence

### `NEG-W7` — Theorem 1 potential: missing −J2/2 and a factor 3 · **CONFIRMED**

The radial acceleration from the C22 term is 9 μ C22 R²/r⁴, not 3; with J2, the equatorial coefficient is 3C22 − J2/2 = 0.00865.

### `NEG-W8` — Theorem G2: post-jam retraction spins the triad up · **CONFIRMED**

A direct centre-of-mass inertia calculation gives I_COM/I0 = 0.8725 and T'/T0 = 1.1987, vs the paper's 0.8163. Retraction reduces inertia, so ω and tension rise.

### `NEG-W9` — L4 stiffness: passive term is positive, xx:yy = 1:11 · **CONFIRMED**

The passive isotropic-triad Hessian at L4 is proportional to [[3/4, 15√3/4], [15√3/4, 33/4]]: xx:yy = 1:11, both positive. The −k_s stabilisation needs active control.

### `NEG-W10` — μ_R(0.02) and the Lyapunov error · **CONFIRMED**

μ_R(0.02) = 0.0515459, not 0.0514772; the Lyapunov error is 0.43%, not 0.35% (Gascheau rate 3^(−1/4)/√2 derived analytically).

### `SIM-032` — Kick growth (5,570× vs 11,618×), ladder values, FEM/FDIR counts · **SPEC-NEEDED**

Depend on kick definition, step size and FEM/FDIR settings the paper doesn't give. Run spec in the dossier.

### `HK-032` — Stale 'WP031 not yet archived' note · **CONFIRMED**

WP031 is archived in the repository (papers/wp031_3d_j2_hil). The G4N dossier's note (line 3) is stale. A dated [GB] addendum is added under it; the original note and the frozen paper are not edited.

### `REF-12` — Ref [12] cites an internal Swift++ calibration ledger · **UNVERIFIABLE**

The Epoch XXXVIII calibration document is not public or in the repository. Suggest marking it 'internal, not public' (as G4N asked for WP035 Ref [12]) and citing the archived sibling working papers by their repository location.

### `INT-032` — Pass 9B ledger and certificates C145–C148, K10, F37 · **UNVERIFIABLE**

Internal toolchain, kept verbatim. G4N verifiers re-run: Python, Rust, 9/9 Lean pass.

## Run spec requested from the author

**SPEC-032 — Bennu ladder, 48-DOF FEM, FDIR and figure-8 / Lagrange kick runs**

| Field | Needed |
| :--- | :--- |
| Bennu model | μ_B, R_eq, C20/J2, C22 values and reference radius |
| FEM | node masses, EA, damping, reel slew rate, jam onset time, time step |
| FDIR | detection threshold, slack definition, count window |
| Kick test | kick size, direction (position/velocity, which body), integrator, step, horizon, growth metric (5,570× vs 11,618× depends on these) |
| Figure-8 | initial conditions source (Chenciner–Montgomery / Simó digits), Yoshida-4 step |

## Reproduce (from the repository root)

```bash
python3 reconciliation/horizon_round1/code/gb_r1_wp031_035.py
python3 papers/wp032_bennu_3body/code/*.py   # [G4N] plane 1
lake -d papers/wp032_bennu_3body/lean build   # [G4N] plane 2 (Lean 4.36.0)
cargo test --manifest-path papers/wp032_bennu_3body/rust/Cargo.toml   # [G4N] plane 3
typst compile papers/wp032_bennu_3body/paper/paper.typ
```
