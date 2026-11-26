# Horizon WP030–WP035: Grok Bot (`[GB]`) Round-1 reconciliation (`main` @ `59780e6`)

Method: ADPIE, as in the Morpheus `v0.2.0` and round-2/3 reconciliations. Order: WP030, WP034, WP035, WP031, WP032, WP033. Date: 2026-11-26.

## What was checked
- **`[G4N]` planes re-run from scratch:** Python 34/34, Rust 31/31 (on rustc 1.85.1; the dossiers say 1.100.0), data manifests 6/6, all 78 PROVENANCE checksums OK.
- **Lean:** elan + Lean 4.36.0 installed (free). All six projects build: 15 + 9 + 9 + 7 + 9 + 9 = **58 theorems, 0 `sorry`, standard axioms only.** Scope finding: every theorem is stated over `Int`/`Nat`, so they certify integer shadows of the results, not the analytic theorems (NEG-W29).
- **Independent `[GB]` checks** (written without reading `[G4N]` code or data): `reconciliation/horizon_round1/code/` — Hopf-chart geometry and holonomy, Theorem G1, rounding order, tensions and Bennu scaling, 106-bit emulation, symbolic G5, Sen (2013) cross-check (arXiv:1205.0971v2 fetched), ζ′ spectra, J2 baseline, WP032 COM inertia and L4 Hessian, and an independent WP033 halo re-run (42-ODE STM, monodromy, Broucke indices, both W^u branches).
- **External sources:** NASA NTRS records 19910012850 / 19910029285 / 19910012826; the arXiv listing for 2611.34924.
- **Typst:** all six reconciled editions compile (8–10 pp), with no local paths in the PDFs.

## Verdict counts

| Paper | Items | CONFIRMED | CONFIRMED-IN-SUBSTANCE | PARTIAL | DISPUTED | UNVERIFIABLE | SPEC-NEEDED | NEW |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| WP030 | 17 | 8 | 1 | 0 | 1 | 3 | 1 | 3 |
| WP034 | 8 | 3 | 2 | 1 | 0 | 1 | 0 | 1 |
| WP035 | 11 | 6 | 0 | 2 | 0 | 2 | 0 | 1 |
| WP031 | 8 | 3 | 1 | 0 | 1 | 1 | 0 | 2 |
| WP032 | 8 | 5 | 0 | 0 | 0 | 2 | 1 | 0 |
| WP033 | 8 | 5 | 0 | 0 | 0 | 2 | 1 | 0 |
| **All** | **60** | **30** | **4** | **3** | **2** | **11** | **3** | **7** |

Of the 32 rows that check `[G4N]`'s NEG-W1–W24 sub-items: 24 CONFIRMED, 2 CONFIRMED-IN-SUBSTANCE, 3 PARTIAL, 2 DISPUTED (both NTRS IDs), 1 UNVERIFIABLE (C138). No `[G4N]` mathematical catch was overturned. Plus 3 series-level rows (Lean scope, registry numbering, NEGATIVES heading). GB-W27a and GB-W28 appear in two papers each, so there are 6 new proposed negatives: NEG-W25–W30.

## Patch series (apply in order with `git am`)
| Series | Commit | What it changes |
| :--- | :--- | :--- |
| 00-tools | `reconcile(horizon-r1)` | `reconciliation/horizon_round1/`: check scripts, logs, edition builder, README; root `.gitattributes` with `*.pdf binary` so the PDFs survive `git am` byte-exact |
| 01-wp030 … 06-wp033 | `reconcile(wp0xx)` | `papers/<slug>/paper/` (reconciled `paper.typ`, `paper.pdf`, figures), `reconciliation/GROKBOT_WP0xx_ROUND1.md`, README section. WP032 also gets a dated addendum under `[G4N]`'s stale "WP031 not yet archived" note |
| 07-registry | `docs(horizon-r1)` | `NEGATIVES.md` (R1 statuses on W1–W24, new W25–W30, §3 heading), `PROVENANCE.md`, `papers/README.md`, `CHANGELOG.md`, this changelog |

`cleanroom/` is untouched everywhere. The reconciled editions keep every `[E]` line verbatim and in order (the builder asserts this). Verdicts are boxed notes; corrections are proposed, not applied.

## Per-item verdicts

| Paper | ID | Item | Verdict |
| :--- | :--- | :--- | :--- |
| WP030 | `NEG-W1` | Table 1 Regimes A/B have underground perigees | **CONFIRMED** |
| WP030 | `NEG-W5` | Regime A tension 0.0012 N is about 100× too low | **CONFIRMED** |
| WP030 | `NEG-W6` | Regime C exponent, Bennu tension, SRP dominance | **CONFIRMED** |
| WP030 | `NEG-W6/7a` | C138 ≤ 1e-6 octupole bound | **UNVERIFIABLE** |
| WP030 | `NEG-W6/7b` | F35 loss is 84.8%, not 84.6% | **CONFIRMED** |
| WP030 | `NEG-W6/7c` | Ref [1] NTRS ID | **DISPUTED** |
| WP030 | `REF-12` | Ref [12] cites an internal Swift++ calibration ledger | **UNVERIFIABLE** |
| WP030 | `NEG-W2` | Θ = π/3 holonomy loop hits two binary collisions; Θ = 0 is collinear | **CONFIRMED** |
| WP030 | `GB-W25` | Holonomy sign: net physical rotation is +90°, not −90° | **NEW** |
| WP030 | `NEG-W4` | Theorem 2 sign: the printed Q is the mass quadrupole | **CONFIRMED** |
| WP030 | `NEG-W3` | Theorem G1: exact shape kinetic energy | **CONFIRMED** |
| WP030 | `NOTE-8` | Specify μ_tot and the energy convention for a_f, e_f | **CONFIRMED** |
| WP030 | `GB-W26` | The naive rounding error depends on evaluation order | **NEW** |
| WP030 | `GB-W27a` | Earth-radius convention differs across the series | **NEW** |
| WP030 | `X-MISSION` | Mission figure across WP030/WP031/G4N: 619.8 vs 220.2 vs 199.9 m/s/yr | **CONFIRMED-IN-SUBSTANCE** |
| WP030 | `SIM-030` | Coupled 4-body numbers (tumbles, ΔE, Eq. 5 residual, Arm A spin-up) | **SPEC-NEEDED** |
| WP030 | `INT-030` | Internal Swift++ corpus claims | **UNVERIFIABLE** |
| WP034 | `GB-W28` | arXiv:2611.34924 v1 date | **NEW** |
| WP034 | `NEG-W19` | The 106-bit closed form also fails; the fix is algebraic | **CONFIRMED-IN-SUBSTANCE** |
| WP034 | `NEG-W20` | Theorem G5 and the F39 witness mismatch | **CONFIRMED** |
| WP034 | `NEG-W21` | Certificate domains and β* dependence | **CONFIRMED** |
| WP034 | `NEG-W21/C154` | C154 proportional-cap scope | **PARTIAL** |
| WP034 | `SEN-2013` | Sen (2013) cross-check | **CONFIRMED** |
| WP034 | `X-106-167` | 106/45 (WP034) vs 167/90 (WP035): both right, different quantities | **CONFIRMED-IN-SUBSTANCE** |
| WP034 | `INT-034` | Swift++ v3.1 106-bit DD toolchain and Pinakes Epoch XL | **UNVERIFIABLE** |
| WP035 | `NEG-W22` | 'Dropping ζ'_R(0)' ratios are mis-stated | **CONFIRMED** |
| WP035 | `NEG-W24/1` | Lemma 8 volume ratio constant | **CONFIRMED** |
| WP035 | `NEG-W24/2` | a_e three-way cancellation | **PARTIAL** |
| WP035 | `NEG-W24/3` | k = 4 Beltrami chirality split | **PARTIAL** |
| WP035 | `NEG-W24/4` | Ref [12] points to a local, non-repository path | **CONFIRMED** |
| WP035 | `NIELSEN-SRC` | Statements about the Nielsen (2026) manuscript | **UNVERIFIABLE** |
| WP035 | `R1-R2` | Theorems R1 and R2 (standard functional analysis) | **CONFIRMED** |
| WP035 | `NEG-W23` | Remark 4 pole orders and the 'iff' in R3(1) | **CONFIRMED** |
| WP035 | `G6` | G4N Theorem G6 numbers | **CONFIRMED** |
| WP035 | `GB-W28` | Ref [2] arXiv date | **NEW** |
| WP035 | `INT-035` | Swift++ v3.1 toolchain upgrade #2 certificates | **UNVERIFIABLE** |
| WP031 | `NEG-W15` | Spin tension vs zero-spin holonomy (Theorem G4) | **CONFIRMED** |
| WP031 | `GB-W27b` | Triad inertia convention | **NEW** |
| WP031 | `NEG-W16` | Theorem 3 printed Δv formula | **CONFIRMED** |
| WP031 | `NEG-W17` | J2 drift is mostly point-mass precession | **CONFIRMED-IN-SUBSTANCE** |
| WP031 | `NEG-W18` | Euler axis, T_pk, strain and Hall mass | **CONFIRMED** |
| WP031 | `NEG-W18/NTRS` | Ref [3] NTRS ID | **DISPUTED** |
| WP031 | `GB-W27a` | Earth radius | **NEW** |
| WP031 | `INT-031` | Pass 9B ledger, Pinakes 144/144, 57,600 RCT, K9 certificate, F36 HIL, XCTests | **UNVERIFIABLE** |
| WP032 | `NEG-W7` | Theorem 1 potential: missing −J2/2 and a factor 3 | **CONFIRMED** |
| WP032 | `NEG-W8` | Theorem G2: post-jam retraction spins the triad up | **CONFIRMED** |
| WP032 | `NEG-W9` | L4 stiffness: passive term is positive, xx:yy = 1:11 | **CONFIRMED** |
| WP032 | `NEG-W10` | μ_R(0.02) and the Lyapunov error | **CONFIRMED** |
| WP032 | `SIM-032` | Kick growth (5,570× vs 11,618×), ladder values, FEM/FDIR counts | **SPEC-NEEDED** |
| WP032 | `HK-032` | Stale 'WP031 not yet archived' note | **CONFIRMED** |
| WP032 | `REF-12` | Ref [12] cites an internal Swift++ calibration ledger | **UNVERIFIABLE** |
| WP032 | `INT-032` | Pass 9B ledger and certificates C145–C148, K10, F37 | **UNVERIFIABLE** |
| WP033 | `HALO-RERUN` | Independent halo re-run from the paper's state | **CONFIRMED** |
| WP033 | `NEG-W11` | The W^u 'lunar tube' passes inside the Moon | **CONFIRMED** |
| WP033 | `NEG-W12` | Theorem G3 coupled stiffness and gap sensitivities | **CONFIRMED** |
| WP033 | `NEG-W13` | Regolith density and C_D | **CONFIRMED** |
| WP033 | `NEG-W14` | Certified intervals vs the operating regime | **CONFIRMED** |
| WP033 | `SIM-033` | Station-keeping (3,051× vs 3,442×), W^u kick, TAG Monte Carlo | **SPEC-NEEDED** |
| WP033 | `REF-12` | Ref [12] cites an internal Swift++ calibration ledger | **UNVERIFIABLE** |
| WP033 | `INT-033` | Pass 9B ledger and certificates C149–C152, K11, F38 | **UNVERIFIABLE** |
| series | `NEG-W29 (proposed)` | Lean scope across all six papers | **NEW** |
| series | `HK-NUM` | Registry numbering | **CONFIRMED** |
| series | `HK-NEG-TITLE` | NEGATIVES.md §3 heading | **CONFIRMED** |

## Not patched (your call)
1. **Annotate or correct in place.** The editions annotate. Applying the CONFIRMED corrections to the text (Table 1 orbits, tension typo, F35, Theorem 2 sign, WP031 axis and formula, WP032 factor 3 and μ_R, WP035 ratios) would make a canonical revision; say which.
2. **106/45 vs 167/90 (NEG-W30).** Which quantity is "Sen's entropy" in WP034 and WP035.
3. **Holonomy sign (NEG-W25).** Keep the paper's chart and say the physical turn is +90°, or adopt `[G4N]`'s equilateral-pole basis (−90° physical, collision-free).
4. **Conventions (NEG-W27).** One R⊕ for the series; restate WP031's power budget with I0 = ML² (61.78 W) or justify (2/3)ML².
5. **Flight baseline (NEG-W15).** Zero-spin Hopf triad or spin-tensioned triad.
6. **Mission headline.** WP031's safe-perigee 199.89 m/s/yr is the defensible figure; WP030's 619.8 is on an underground orbit.
7. **Run specs.** The simulation figures in WP030 §3, WP031 §2/§4, WP032 §§3–5 and WP033 §§2–3 need the specs listed in each dossier before a third party can re-run them.
8. **Lean wording (NEG-W29)** in the `[G4N]` dossiers and READMEs.
9. **NTRS IDs.** Do **not** apply `[G4N]`'s proposed changes to WP030 Ref [1] and WP031 Ref [3]; they are correct.
10. **Release.** Whether the reconciled editions get a tagged release, per the repo's release rule.
11. **Not checked this round:** WP033 L_y* = 40.44 m; C_D = 1.60 (contact area unstated); WP035 4th-order QED closure and Beltrami chirality split; C154 against Chandrasekaran Eq. 2.5; C138 octupole figure.
