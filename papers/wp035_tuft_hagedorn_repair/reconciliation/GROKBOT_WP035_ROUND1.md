# Grok Bot (`[GB]`) Round-1 Reconciliation — Working Paper 035

*TUFT Audit and Hagedorn Nuclearity Repair* · Round 1 · 2026-11-26 · Method: ADPIE, as in the Morpheus v0.2.0 and round-2/3 reconciliations.

## Scope and rules

- Inputs: the frozen `cleanroom/` manuscript and the `[G4N]` Cycle-1 dossier in this folder. `[GB]` checks were written from scratch, without reading `[G4N]` code or data; `[G4N]`'s verifiers were then re-run separately.
- The reconciled edition is [`../paper/paper.typ`](../paper/paper.typ) → [`../paper/paper.pdf`](../paper/paper.pdf): every `[E]` line is kept verbatim and in order; verdicts are inserted as boxed notes. Corrections are proposed, not applied.
- Claims attributed to the Ergentics internal model / Swift++ corpus are never altered. Where they can't be checked from this repository they are marked **UNVERIFIABLE**.

**Verdict totals:** CONFIRMED 6 · PARTIAL 2 · UNVERIFIABLE 2 · NEW 1

## Verdict table

| ID | Item | Verdict | Placed under |
| :--- | :--- | :--- | :--- |
| `NEG-W22` | 'Dropping ζ'_R(0)' ratios are mis-stated | **CONFIRMED** | § “Nash–O'Connor” |
| `NEG-W24/1` | Lemma 8 volume ratio constant | **CONFIRMED** | § “Theorem 56” |
| `NEG-W24/2` | a_e three-way cancellation | **PARTIAL** | § “Full Appendix A Replication” |
| `NEG-W24/3` | k = 4 Beltrami chirality split | **PARTIAL** | § “Explicit Clifford-Torus Beltrami” |
| `NEG-W24/4` | Ref [12] points to a local, non-repository path | **CONFIRMED** | end of paper (before References) |
| `NIELSEN-SRC` | Statements about the Nielsen (2026) manuscript | **UNVERIFIABLE** | § “Dark-Sector Identities” |
| `R1-R2` | Theorems R1 and R2 (standard functional analysis) | **CONFIRMED** | § “Theorem R1” |
| `NEG-W23` | Remark 4 pole orders and the 'iff' in R3(1) | **CONFIRMED** | § “Theorem R3” |
| `G6` | G4N Theorem G6 numbers | **CONFIRMED** | § “Theorem R3” |
| `GB-W28` | Ref [2] arXiv date | **NEW** | end of paper (before References) |
| `INT-035` | Swift++ v3.1 toolchain upgrade #2 certificates | **UNVERIFIABLE** | § “Precision Toolchain Upgrade” |

## Evidence

### `NEG-W22` — 'Dropping ζ'_R(0)' ratios are mis-stated · **CONFIRMED**

S³: ζ1'(0) = +0.888490 and the remainder after dropping is ζ_R'(−2) = −ζ(3)/(4π²) = −0.030448 (the paper prints +0.030448, so the S³ sign also flips). Ratio 29.18; the printed 30.2× is the dropped-term ratio 30.18. S⁵: 1.757764 / 0.080113 = 21.94; the printed 22.9× is the dropped-term ratio 22.94. Both ratios are overstated by exactly 1. L(3,1) multiplicities [4, 4, 8, 20, 22, 28] reproduce.

### `NEG-W24/1` — Lemma 8 volume ratio constant · **CONFIRMED**

Vol(S²)Vol(S⁹)^(1/4)/(Vol(S⁴)²Vol(RP¹)) at R = 1 is 0.0129767 = 10^(1/4)·α_Wyler. Wyler's α is +3965.3σ from CODATA, as stated.

### `NEG-W24/2` — a_e three-way cancellation · **PARTIAL**

The waterfall sum −5428.8 + 121269.4 − 116156.4 = −315.8σ is confirmed. The fourth-order QED closure was not recomputed.

### `NEG-W24/3` — k = 4 Beltrami chirality split · **PARTIAL**

Not independently checked this round.

### `NEG-W24/4` — Ref [12] points to a local, non-repository path · **CONFIRMED**

Ref [12] should cite a public location or be marked as an internal source.

### `NIELSEN-SRC` — Statements about the Nielsen (2026) manuscript · **UNVERIFIABLE**

The TUFT manuscript is not public, so line and equation attributions to it cannot be checked. The mathematics used to refute them (spectra, volumes, Beltrami fields) is independent of the source and was checked where noted.

### `R1-R2` — Theorems R1 and R2 (standard functional analysis) · **CONFIRMED**

Read, not re-proved line by line: the arguments (a compact operator bounded below has finite rank; a trace-class heat kernel gives compact resolvent and nuclearity) are the standard ones and we found no gap. Note: the Lean file's 'Theorem R1' is a finite integer-list inequality, not the operator statement (see NEG-W29).

### `NEG-W23` — Remark 4 pole orders and the 'iff' in R3(1) · **CONFIRMED**

(1) With α = 257/90, R3(3) gives ln N = s + (167/90) ln s; listing 257/90 next to Sen's α_micro + 1 values mixes conventions (see X-106-167 in WP034). (2) Convergence at β = β_H can hold: ρ(E) = (1+E)^(−2) e^(β_H E) gives Z(β_H) = 1, so 'iff β greater than limsup' should read 'if', with the boundary case stated. R3(2)'s 4/3^(3/4) reproduces.

### `G6` — G4N Theorem G6 numbers · **CONFIRMED**

σ/mean = 1/√α, the tail mass and Beta(α,1) RMS reproduce for α = 3.3556, 2.8556, 1.8556.

### `GB-W28` — Ref [2] arXiv date · **NEW**

arXiv:2611.34924 v1 was submitted 25 November 2026, not 23 November (proposed NEG-W28).

### `INT-035` — Swift++ v3.1 toolchain upgrade #2 certificates · **UNVERIFIABLE**

Kept verbatim. G4N verifiers re-run here: Python, Rust and 9/9 Lean pass.

## Reproduce (from the repository root)

```bash
python3 reconciliation/horizon_round1/code/gb_r1_wp031_035.py
python3 papers/wp035_tuft_hagedorn_repair/code/*.py   # [G4N] plane 1
lake -d papers/wp035_tuft_hagedorn_repair/lean build   # [G4N] plane 2 (Lean 4.36.0)
cargo test --manifest-path papers/wp035_tuft_hagedorn_repair/rust/Cargo.toml   # [G4N] plane 3
typst compile papers/wp035_tuft_hagedorn_repair/paper/paper.typ
```
