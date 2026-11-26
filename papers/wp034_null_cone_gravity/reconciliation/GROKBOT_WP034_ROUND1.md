# Grok Bot (`[GB]`) Round-1 Reconciliation — Working Paper 034

*Precision Audit of Algebraic Null-Cone Quantum Gravity* · Round 1 · 2026-11-26 · Method: ADPIE, as in the Morpheus v0.2.0 and round-2/3 reconciliations.

## Scope and rules

- Inputs: the frozen `cleanroom/` manuscript and the `[G4N]` Cycle-1 dossier in this folder. `[GB]` checks were written from scratch, without reading `[G4N]` code or data; `[G4N]`'s verifiers were then re-run separately.
- The reconciled edition is [`../paper/paper.typ`](../paper/paper.typ) → [`../paper/paper.pdf`](../paper/paper.pdf): every `[E]` line is kept verbatim and in order; verdicts are inserted as boxed notes. Corrections are proposed, not applied.
- Claims attributed to the Ergentics internal model / Swift++ corpus are never altered. Where they can't be checked from this repository they are marked **UNVERIFIABLE**.

**Verdict totals:** CONFIRMED 3 · CONFIRMED-IN-SUBSTANCE 2 · PARTIAL 1 · UNVERIFIABLE 1 · NEW 1

## Verdict table

| ID | Item | Verdict | Placed under |
| :--- | :--- | :--- | :--- |
| `GB-W28` | arXiv:2611.34924 v1 date | **NEW** | § “Introduction and Executive Audit Scorecard” |
| `NEG-W19` | The 106-bit closed form also fails; the fix is algebraic | **CONFIRMED-IN-SUBSTANCE** | § “Catastrophic IEEE-754” |
| `NEG-W20` | Theorem G5 and the F39 witness mismatch | **CONFIRMED** | § “Pillar 2: Refutation” |
| `NEG-W21` | Certificate domains and β* dependence | **CONFIRMED** | § “Catch 5: Appendix D.3” |
| `NEG-W21/C154` | C154 proportional-cap scope | **PARTIAL** | § “Verified Analytical Constructions” |
| `SEN-2013` | Sen (2013) cross-check | **CONFIRMED** | § “Verified Exact Identities and Sen” |
| `X-106-167` | 106/45 (WP034) vs 167/90 (WP035): both right, different quantities | **CONFIRMED-IN-SUBSTANCE** | § “Verified Exact Identities and Sen” |
| `INT-034` | Swift++ v3.1 106-bit DD toolchain and Pinakes Epoch XL | **UNVERIFIABLE** | § “Toolchain Upgrade and Pinakes” |

## Evidence

### `GB-W28` — arXiv:2611.34924 v1 date · **NEW**

arXiv lists v1 of 2611.34924 as submitted 25 November 2026; WP034 (title block, scorecard, references) and WP035 Ref [2] give 23 November. Proposed NEG-W28 (minor).

### `NEG-W19` — The 106-bit closed form also fails; the fix is algebraic · **CONFIRMED-IN-SUBSTANCE**

Emulated 106-bit double-double evaluation of the closed form: 1.2e-17 at s = 1e16, 4.7e-16 at 1e17, 6.4e-13 at 1e20, 831% at 1e33, 100% wipe-out at 1e77. So 'below 1e-15 through 1e20 and beyond' fails past about 1e17–1e20 (G4N's 9.65e-14 at 1e20 differs from mine by implementation; both exceed 1e-15). The cancellation-free rewriting is exact in plain binary64 at every s tested. Attribution of the wipe-out to binary64 alone should be rewritten as catastrophic cancellation.

### `NEG-W20` — Theorem G5 and the F39 witness mismatch · **CONFIRMED**

G5's closed form for Z under the pair and cycle rearrangements was re-derived symbolically from WP034's own definitions (difference 0). Counterexample values +143.8377 (pair, M = 1e4) and −287.6530 (cycle, r = 5) reproduce. Eq. 5.24 ratio is π/2. Witness 2 − 2/(r−1) gives 1.500 at r = 5 (Table 1) but 1.818 at r = 12 (Fig. 2, Table 2): the paper uses two different r.

### `NEG-W21` — Certificate domains and β* dependence · **CONFIRMED**

C156 covers u ≤ 0.35, i.e. R ≥ e^(13/7) = 6.4054, so it does not reach R = e (where the remainder is 0.0881). C153's θ ∈ [0.01, 0.40] means s ∈ [5, 200] only. The optimal β* ratio depends on C_ε (2.6752 at C = 1, equality only at C = 5/π⁴). 'L1970' appears as an internal reference.

### `NEG-W21/C154` — C154 proportional-cap scope · **PARTIAL**

Accepted as a scope note; not re-checked against Chandrasekaran's Eq. 2.5 in this round.

### `SEN-2013` — Sen (2013) cross-check · **CONFIRMED**

Fetched arXiv:1205.0971v2, Eqs. 1.4–1.5 and text: C_local = 212/45 per ln a (a a length), so the mixed ensemble is 106/45 ln A and the J = 0 singlet 77/90 ln A. WP034's per-shell 106/45 matches Sen's mixed coefficient.

### `X-106-167` — 106/45 (WP034) vs 167/90 (WP035): both right, different quantities · **CONFIRMED-IN-SUBSTANCE**

WP034's 106/45 is the log coefficient of Tr(C†C) at fixed s_b. The (4π s_b)^(−1/2) measure turns this into a state density with exponent 106/45 − 1/2, so ln N = s + (167/90) ln s, matching WP035 Theorem R3 with α = 257/90. The papers disagree only on which quantity is called 'Sen's entropy'. Author decision. Proposed NEG-W30.

### `INT-034` — Swift++ v3.1 106-bit DD toolchain and Pinakes Epoch XL · **UNVERIFIABLE**

Internal toolchain claims are kept verbatim. The emulation above suggests any 106-bit implementation of the closed form loses accuracy past about 1e20, whatever toolchain runs it. G4N verifiers re-run: Python, Rust and 9/9 Lean pass.

## Reproduce (from the repository root)

```bash
python3 reconciliation/horizon_round1/code/gb_r1_wp031_035.py
python3 papers/wp034_null_cone_gravity/code/*.py   # [G4N] plane 1
lake -d papers/wp034_null_cone_gravity/lean build   # [G4N] plane 2 (Lean 4.36.0)
cargo test --manifest-path papers/wp034_null_cone_gravity/rust/Cargo.toml   # [G4N] plane 3
typst compile papers/wp034_null_cone_gravity/paper/paper.typ
```
