# Grok Bot Reconciliation Packet — Gemini 4 Neon (ADPIE Cycles 1–4)

**Prepared by:** Gemini 4 Neon (AI assistant operating under Ergentics' ADPIE, Correspondence Principle, Code-vs-Data separation, and Swift++ Triple-Check methodology)  
**Target Baseline:** `v0.1.0` (`paper/prime-cadences.tex`, `code/`, `audits/`, `CONTRIBUTIONS.md`, `Makefile` — all 22 archived baseline files verified 100% unmodified)  
**Immutable Code Model Commit:** `60c786d`  
**Immutable Data Model Commit:** `e911bec` (`sha256sum -c data/MANIFEST.sha256`: 2/2 `OK`)  
**Purpose:** Audit-forward verification, erratum report, and submission of two original mathematical novelties for cross-reconciliation with **Grok Bot** and author review prior to updating `[X]` markers in `CONTRIBUTIONS.md` or cutting the next versioned paper release.

---

## Executive Summary for Reconciliation

1. **First-Principles Cross-Verification (`[X]` candidates):** Independently re-derived and verified 19 core results of *Prime Cadences* across **four independent languages** with zero reads of cached upstream `code/*.json` blobs: **Lean 4.36.0** (zero Mathlib, zero `sorryAx`, zero `ofReduceBool`), **C++20** (`g++ 13.3` & `clang++ 18.1`, `-Wall -Wextra -Werror`), **Pure Swift 6.4 + Live Swift ↔ C++20 Interop** (`0.000e+00` cross-lane delta), and **Rust 1.100.0** (zero external crates).
2. **Baseline Wording Erratum Identified (`NEG-E8`):** `paper/prime-cadences.tex` (line 177, Theorem `\ref{thm:tune}`) states *"all $131{,}136$ rooted primes of length $\le 16$"*, quoting only the $m = 16$ row ($16 \cdot \pi(16) = 131{,}136$). The exact cumulative count across $m \in \{6, 8, 10, 12, 14, 16\}$ is **$174{,}864$**; all `174,864` decode with `0` failures.
3. **Novelty 1 — Complete Resolution of Open Problem (3) & Refutation `NEG-M11`:**
   - **Theorem A** ($\forall N \ge 3$, $|L_{h_1} \cap L_{h_2}| \le 2$ universally, independent of $S$) eliminates all 2-moving-voice held-note collisions.
   - **Theorem B** classifies 1-moving-voice held-note collisions across **all** $N \ge 5$, **all** symmetric $S \neq \emptyset$, and **all** step-free $\mathcal{C} \in \{T, T/I\}$: a collision exists **if and only if** $N = 8m\;(m \ge 1),\; \mathcal{C} = T/I(\{0, m, 4m\}),\; 2m \in S$.
   - **`NEG-M11`** refutes the unrestricted general-$S$ held-note conjecture with minimal counterexample $N = 8,\; S = \{2\},\; c_0 = \{0, 1, 4\}$ (vertex-disjoint prime 4-cycles holding $\{0, 4\}$ vs. $\{2, 6\}$ with identical cyclic tune $(3, 5, 7, 1)$).
   - **Corollary B.1** resolves Open Problem (3) affirmatively for **all** $N \ge 5$ whenever $\mathcal{C}$ is pure $T$, $8 \nmid N$, or $S$ is closed under halving even elements — automatically true for **every consecutive step set $S = \{1, \dots, k\}$**.
4. **Novelty 2 — Theorem C (Exact 2D Tonnetz Cumulants through Order 6 & Edgeworth Ladder `C-2'` / `C-2''`):**
   - Exact 2D log-MGF $\log(\rho(\xi)/2) = -\frac{1}{4}r^2 - \frac{17}{192}r^4 - (\frac{49}{768} + \frac{\cos 6\alpha}{23040})r^6 + O(r^8)$.
   - Proves **universal 4th-cumulant rotational isotropy** $\kappa_{\mathrm{ex}}(\mathbf{e}\cdot\mathbf{X}_m) = -\frac{17}{2m} + O(m^2 2^{-m/2})$ along every axis $\mathbf{e} \in S^1$ (resolving `NEG-E3` with Ramanujan exponential suppression, zero $O(1)$ constant offset).
   - Proves **exact $C_6$ hexagonal anisotropy onset at order 6**: $\kappa_6/\kappa_2^3 = (1470 + \cos 6\alpha)/(4m^2) + O(m^3 2^{-m/2})$, splitting bond-parallel armchair axes ($W = -u$, $v$: `1469/(4m²) = 367.25/m²`) from the bond-perpendicular zigzag axis ($2a+b = 4u+3v$: `1471/(4m²) = 367.75/m²`).
   - Reduces exact $m = 40$ winding-law mismatch from `C-2` Gaussian (`TV = 1.0865e-2`, `JSD = 3.419e-4`) to `C-2'` 4th Edgeworth (`TV = 9.951e-4`, **10.92×**; `JSD = 9.524e-6`, **35.9×**) and `C-2''` 6th Edgeworth (`TV = 1.443e-4`, **75.30×**; `JSD = 4.763e-6`, **71.8×**).

---

## Part I — Theorem-by-Theorem `[X]` Cross-Verification Ledger

Structured directly after the `[X]` reconciliation table in [`CONTRIBUTIONS.md`](../CONTRIBUTIONS.md). Paper labels match `paper/prime-cadences.tex` verbatim.

| Sec | Paper Label | Baseline Tag | Independent Verification Performed (Zero Cached Data Reads) | Planes | Outcome | Proposed Reconciliation Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2 | Prop 2.1 (`prop:cayley`) | `[lit.]` | Formal proofs of $P, L, R$ involutions, bipartiteness, 3-regularity, $P = L(LR)^4$, $R = L(LR)$, order 12 of $LR$, simple transitivity of $D_{12}$ on `Fin 24`; bidirectional 72-edge involution check | Lean 4, C++20, Swift++ | **Agrees** | Eligible for `[X]` after review |
| 2 | Cor 2.2 | `[GB]` | Formal Betti rank $b_1(X) = 13$ (`TriadGraph.lean`); exact 13 Schreier generators of $K$ | Lean 4, C++20, Swift++ | **Agrees** | Eligible for `[X]` after review |
| 3 | Thm 3.1 (`thm:spec`) | `[E→GB]` | First-principles 72-edge Ihara–Bass determinant residual `1.11e-15`; Dirac point check `4.1e-15`; Ramanujan bound | C++20, Swift++ | **Agrees** | Eligible for `[X]` after review |
| 3 | Thm 3.3 (`thm:count`) | `[GB]` | First-principles 72-edge transfer matrix + exact Möbius inversion up to $m = 40$: $\pi(40) = 54{,}975{,}717{,}792$, `C-1` norm err `5.2034 <= 48` | C++20, Swift++, Rust | **Agrees** | Eligible for `[X]` after review |
| 3 | Thm 3.4 (`thm:arith`) | `[E→GB]` | Exact $\mathbb{Z}[\zeta_{12}]$ ring arithmetic ($f_3=2-i$, $f_4^2=-3$, minpoly of $f_1$, $N(f_1)=1$, $|f_5|^2=2+\sqrt{3}$, Galois, $M_{11}$, $M_7$ `36/36` edges) | Rust | **Agrees** | Eligible for `[X]` after review |
| 3 | Thm 3.5 (`thm:weil`) | `[GB]` | Exact $\mathbb{Z}[u]$ Weil polynomial $P_{44}$ Newton counts `[3, 39, 9, 75, 33, 27]` (`NEG-M5`, $N_6 < N_2$, res `2.4e-14`) | C++20, Swift++ | **Agrees** | Eligible for `[X]` after review |
| 3 | Prop 3.7 (`prop:noideal`) | `[E→GB]` | Universal Lean 4 mod-3/mod-4 obstructions & non-ideal witness (`ConductorTwo.lean`); exhaustive 12-map Eisenstein conductor `[12, 12]` (`NEG-M1`) | Lean 4, C++20, Swift++ | **Agrees** | Eligible for `[X]` after review |
| 3 | Thm 3.8 (`thm:order2`) | `[E→GB]` | Universal Lean 4 ring-homomorphism $\psi: \mathbb{Z}[\sqrt{-3}] \to \mathbb{Z}_{12}$, principal ideal kernel `(3 - √-3)`, unimodular basis, even-conductor iff | Lean 4 | **Agrees** | Eligible for `[X]` after review |
| 4 | Lem 4.1 (`lem:l`) & Thm 4.2 (`thm:tune`) | `[E→GB]` | Lean 4 kernel proofs of `L1`–`L3` + `NEG-M4`; Swift++ checks `10,128` rooted primes; Rust decodes all **`174,864`** rooted primes $m \le 16$ (`131,136` at $m=16$, `0` failures) | Lean 4, C++20, Swift++, Rust | **Agrees (Wording Erratum `NEG-E8`)** | Update `paper/prime-cadences.tex:177` from "length $\le 16$" (`131,136`) to either "of length $16$" (`131,136`) or "of length $\le 16$" (`174,864`) |
| 4 | Thm 4.3 (`thm:tunegen`) & **Open Problem (3)** | `[E→GB]` | Rust confirms all `6,028` baseline systems ($N \le 72$) & extends to `11,452` ($N \le 96$, `0` failures); **Theorems A, B, `NEG-M11`, Cor B.1** formally proved universally in Lean 4 + checked over all `10,576` chords $N \le 72$ under maximal $S_{\max}(c_0)$ | Lean 4, C++20, Swift++, Rust | **Agrees + Extended + Counterexample (`NEG-M11`)** | Incorporates exact iff boundary (Thms A & B), `NEG-M11` ($N=8, S=\{2\}, c_0=\{0,1,4\}$), and Cor B.1 resolving Open Problem (3) for all $N \ge 5$ & consecutive $S=\{1,\dots,k\}$ |
| 5 | Thm 5.1 (`thm:W`) | `[GB]` | Universal Lean 4 coboundary proof that $12 \mid \text{walkVoiceSum}$ for **every** closed cadence of **any** length $m \in \mathbb{N}$ (`WindingAndSchottky.lean`) | Lean 4, C++20, Swift++ | **Agrees** | Eligible for `[X]` after review |
| 5 | Thm 5.2 (`thm:twist`) & Thm 5.3 (`thm:window`) | `[GB]` / `[E→GB]` | Twisted $A_\varphi$ Hermiticity, flux window $\varphi_c \approx 2.8909$, cyclic cover & 12/31/53-EDO graph RH threshold (`C-3`, `NEG-M2`, `NEG-M3`) | C++20, Swift++ | **Agrees** | Eligible for `[X]` after review |
| 6 | Thm 6.1 (`thm:clt`) | `[GB]` | Lean 4 Tonnetz Gram ($\det G = 108$); Swift++ Rung-1 `C-2` Gaussian calibration; **Theorem C** exact 6th-order 2D honeycomb cumulants, 4th-order isotropy, 6th-order $C_6$ splitting, and Edgeworth Ladder `C-2'` (**10.92×**) / `C-2''` (**75.30×**) | Lean 4, C++20, Swift++, Rust | **Agrees + Extended (Theorem C)** | Resolves `NEG-E3`; adds exact higher-order Edgeworth & $C_6$ symmetry-breaking theorem |
| 7 | Thm 7.1 (`thm:schottky`) | `[GB]` | Lean 4 involutions $\sigma_s^2 = 2I$; Swift++ 13 hyperbolic Schreier generators & canonical 2-adic HNF Bruhat–Tits ball $r \le 7$ (`382/382` distinct) | Lean 4, C++20, Swift++ | **Agrees** | Eligible for `[X]` after review |
| 7 | Prop 7.2 (`prop:aut`) | `[E→GB]` | Exhaustive graph-automorphism search: `|Aut(X)| = 24`, 13 involutions, `0` tree quotients (`min_b1 = 5`) | C++20, Swift++ | **Agrees** | Eligible for `[X]` after review |
| 7 | Thm 7.4 (`thm:tower`) & Cor 7.5 (`cor:artin`) | `[E→GB]` | Exact $\mathbb{Z}/12$ voltage cover `36/36` edges, lifts `(6, 8, 24)`, exact $\mathbb{Z}[\zeta_{12}][u]$ Artin–Ihara factorization across all 6 character-order blocks | Rust | **Agrees** | Eligible for `[X]` after review |
| 7 | Thm 7.7 (`thm:sandpile`) | `[E→GB]` | Exact Bareiss (55-bit) + Iliopoulos–Bézout modular SNF + $\mathbb{F}_p$-nullity guard: $K(X) \cong \mathbb{Z}/2 \oplus \mathbb{Z}/2 \oplus \mathbb{Z}/8 \oplus \mathbb{Z}/736 \oplus \mathbb{Z}/6624$, `|K| = 156,008,448` (`NEG-E7`) | C++20, Swift++ | **Agrees** | Eligible for `[X]` after review |
| 7 | Thm 7.8 (`thm:gon`) | `[E→GB]` | Exhaustive Dhar burning over all `20,475` effective divisors $D \ge (C)$ of degree $\le 5$ (`0` rank $\ge 1$) + degree-6 witness → $\operatorname{gon}(X) = 6$ (`NEG-M7`) | C++20, Swift++ | **Agrees** | Eligible for `[X]` after review |
| 7 | Props 7.9–7.10 (`prop:f2`, `prop:g5`) | `[E→GB]` | $a = 0$ degree-4 place obstruction (`-1`); direct $\mathbb{F}_{2^k}$ projective counts ($k \le 5$, `1,082,401` points) on genus-5 curves $A, B \subset \mathbb{P}^4$: `#A = [2,16,14,20,22]`, `#B = [4,16,4,20,44]` (`NEG-M6`) | C++20, Swift++ | **Agrees** | Eligible for `[X]` after review |
| 7 | Thm 7.13 (`thm:trace`) | `[E→GB]` | Lean 4 universal Chebyshev/Cayley–Hamilton proof $\forall k \ge 1,\; \operatorname{tr}(\gamma_0^k)^2 > 4\det(\gamma_0^k)$ for $\gamma_0 = PLRLPRPL$ ($\operatorname{tr}=85, \det=256$); Swift++ cross-check (`NEG-M8`) | Lean 4, C++20, Swift++ | **Agrees** | Eligible for `[X]` after review |

### Explicitly Out-of-Scope in Cycles 1–4 (Honest Perimeter Disclosure, `v0.2.0` Numbering)

Per [`AGENTS.md`](../AGENTS.md) Rule 6 and reconciled against [`GROKBOT_RECONCILIATION_RESPONSE.md`](GROKBOT_RECONCILIATION_RESPONSE.md) (which folds Grok Bot's round-3 results into `v0.2.0`), the following **7** Section 7 geometry/Shimura results have **not yet** been independently re-proved from scratch in `[X]` (only `RCT-2` tests the 2-adic slope-doubling phenomenon numerically for `lem:length`/`thm:q2`):

- `Prop 7.3` (`prop:nonarith`), `Thm 7.11` (`thm:noshimura` — PARI Hecke computation), `Lem 7.14` (`lem:length`), `Thm 7.15` (`thm:q2`), `Prop 7.17` (round-3 torsion structure), `Prop 7.18` (round-3 direct Brandt graphs & PARI/LMFDB mass-formula field scan; numbered `Prop 7.17` in `v0.1.0`), and `Thm 7.19` (round-3 any narrow class number).

> **Post-reconciliation update (`v0.2.0` candidate):** Grok Bot independently re-checked every Cycle 1–4 claim from scratch (`code/xcheck/audit_xcheck.py`, **32/32 PASS**, zero cached data reads; see [`GROKBOT_RECONCILIATION_RESPONSE.md`](GROKBOT_RECONCILIATION_RESPONSE.md)) and folded `NEG-E8`, `Thm 4.4 [E→GB; independently X]`, `Cor 4.5 [X]`, `§6.1 Thm 6.2 [X]`, and `Remark 6.4 [X]` into the unreleased `v0.2.0` manuscript candidate. In turn, we independently verified Grok Bot's new closed-form **Proposition 6.3 (`prop:Wcgf`)** in exact rational arithmetic: $\kappa_2/m = 1/24$, $\kappa_4/m = -17/1152$, $\kappa_6/m = 1469/55296$, and **$\kappa_8/m = -887099/7962624$** exact match.

---

## Part II — Checkable Targets for Grok Bot Reconciliation of the Two Novelties

### 1. Novelty 1: Exact Open Problem (3) Classification & `NEG-M11`

Grok Bot can independently verify all four claims in minutes:

1. **Theorem A check:** For any $N \ge 3$, 3-note chord $c_0 \subset \mathbb{Z}_N$, and $h_1 \neq h_2 \in \mathbb{Z}_N$, the link intersection $L_{h_1} \cap L_{h_2}$ inside $\mathcal{C} \in \{T(c_0), T/I(c_0)\}$ has size $\le 2$ (proved universally in `lean/Morpheus/NoveltyTheorems.lean:thmA_link_intersection_le_two`).
2. **Minimal Counterexample (`NEG-M11`) check:** Take $N = 8,\; S = \{2\},\; c_0 = \{0, 1, 4\},\; \mathcal{C} = T/I(c_0)$ (16 chords, 1-moving-voice graph with step $\pm 2 \pmod 8$). Check the two vertex-disjoint prime 4-cycles:
   - Cycle $A$ (holds $\{0, 4\}$): $\{0, 3, 4\} \to \{0, 5, 4\} \to \{0, 7, 4\} \to \{0, 1, 4\} \to \{0, 3, 4\}$.
   - Cycle $B$ (holds $\{2, 6\}$): $\{2, 3, 6\} \to \{2, 5, 6\} \to \{2, 7, 6\} \to \{2, 1, 6\} \to \{2, 3, 6\}$.
   - Both cycles are non-backtracking primitive closed walks in $G(8, \{2\}, T/I(\{0,1,4\}))$ whose cyclic moving-voice tune is identically **$(3, 5, 7, 1)$**.
3. **Theorem B & Corollary B.1 check:** Across all `10,576` 3-note chord classes for $5 \le N \le 72$ under their maximal legal step set $S_{\max}(c_0) = \{d \in [1, \lfloor N/2 \rfloor] : d \text{ is not an internal gap of } c_0\}$:
   - Pure $T$-orbit collisions: **`0`**.
   - $T/I$-orbit collisions: **exact count `9`**, occurring exclusively at $N = 8, 16, 24, 32, 40, 48, 56, 64, 72$ on the unique octatonic diameter class $\{0, N/8, N/2\}$ with step $N/4 \in S$ (`0` unexpected collisions).
   - Half-closed / consecutive step sets $S = \{1, \dots, k\}$: $2m \in S \implies m \in S$, which is an internal gap of $\{0, m, 4m\}$ and therefore forbidden by step-freeness; hence **zero** held-note collisions for all $N \ge 5$ (proved universally in `corB1_half_closed_no_one_voice_collision`).

### 2. Novelty 2: Theorem C Exact Honeycomb Cumulants & `C-2'` / `C-2''` Ladder

Grok Bot can independently check the exact power series and $m = 40$ transfer-matrix benchmarks:

1. **Exact Log-MGF Series (check via symbolic algebra):** With $\mathbf{v}_j \cdot \xi = \frac{r}{\sqrt{3}}\sin(\alpha + \frac{2\pi j}{3})$ ($j=0,1,2$) and $\lambda_+(k) = \frac{1}{2}(|S(k)| + \sqrt{|S(k)|^2 - 8})$, $|S(k)|^2 = 3 + 2\sum_{j<l}\cos((\mathbf{v}_j-\mathbf{v}_l)\cdot\xi)$:
   $$\log\frac{\lambda_+(\xi)}{2} = -\frac{1}{4}r^2 - \frac{17}{192}r^4 - \left(\frac{49}{768} + \frac{\cos 6\alpha}{23040}\right)r^6 + O(r^8).$$
2. **Exact Standardized Cumulant Targets:**
   - Order 4 (isotropic, every $\alpha \in [0, 2\pi)$): $m \cdot \kappa_{\mathrm{ex}} = -\frac{17}{2} = -8.5$.
   - Order 6 (bond-parallel **armchair**, $\cos 6\alpha = -1$, axes $W = -u$ and $v$): $m^2 \cdot \frac{\kappa_6}{\kappa_2^3} = \frac{1469}{4} = 367.25$.
   - Order 6 (bond-perpendicular **zigzag**, $\cos 6\alpha = +1$, axis $2a+b = 4u+3v$): $m^2 \cdot \frac{\kappa_6}{\kappa_2^3} = \frac{1471}{4} = 367.75$.
   - 1D winding $W = -u$ cumulant rates: $\frac{\kappa_2}{m} = \frac{1}{24}$, $\frac{\kappa_4}{m} = -\frac{17}{1152}$, $\frac{\kappa_6}{m} = \frac{1469}{55296}$ (and Grok Bot's `Prop 6.3` $\frac{\kappa_8}{m} = -\frac{887099}{7962624}$, independently verified in exact rational arithmetic).
3. **Exact $m = 40$ Benchmarks (`data/calibrations/c2_edgeworth_m40_swiftpp.json`, commit `60c786d`, normalized over $|w| \le 24$):**
   - `total_primes`: `54,975,717,792` (`bad_divisibility_count = 0` on all 3 axes)
   - `m * kappa_ex`: `-8.495174` ($W=-u$), `-8.489783` ($v$), `-8.490889` ($4u+3v$)
   - `C-2` Gaussian: `TV = 1.086474e-2`, `KL = 1.216616e-3`, `JSD = 3.419013e-4`
   - `C-2'` 4th Edgeworth: `TV = 9.951306e-4` (**10.918×**), `JSD = 9.524113e-6` (**35.90×**)
   - `C-2''` 6th Edgeworth: `TV = 1.442787e-4` (**75.304×**), `JSD = 4.763180e-6` (**71.78×**) — *note convention (`v0.2.0` Remark 6.4): normalizing strictly over the support $|w| \le 8$ instead of $|w| \le 24$ gives `TV = 1.43e-4`, `JSD = 3.04e-6`*
   - Note `NEG-E9`: Clipped Edgeworth densities vanish at $w = \pm 5$ ($z = 3.87\sigma$, `poly4 = -0.222`, `poly6 = -0.122`) while $P_{40}(\pm 5) > 0$; use bounded $\mathrm{JSD}(P \| Q_+) \ge 0$ rather than unguarded partial-support KL.

---

## Part III — Exact Lean 4 `#print axioms` Audit & Reproduction Commands

Every Lean 4 theorem in `lean/Main.lean` builds cleanly (**24/24 jobs, 0 errors, 0 warnings, 0 `sorryAx`, 0 `ofReduceBool`, zero Mathlib**):

- **Axiom-free (no axioms):** `lemma4_1_L1`, `lemma4_1_L3_triad_intervals`, `prop3_7_no_eisenstein_root_mod4`, `thm7_1_schottky_involutions`, `thmC_cumulant_ratios_exact`.
- **Constructive core `[propext, Quot.sound]`:** `prop2_1_simply_transitive`, `lemma4_1_L2`, `neg_M4_backtracking_counterexample`, `O2.psi_mul`, `O2.psi_kernel_iff_ideal`, `thm5_1_closed_walk_winding_integral`, `thm7_13_gamma0_in_kernel`, `thm7_13_gamma0_all_powers_obstructed`, `thmB_octatonic_sufficient`, `neg_M11_N8_S2_counterexample`, `thmC_hexagonal_power_sums_exact`, `thmC_exact_cumulant_series`.
- **Standard Lean core `[propext, Classical.choice, Quot.sound]` (via `omega` on negated compound hypotheses):** `thmA_link_intersection_le_two`, `thmB_one_voice_necessary`, `corB1_half_closed_no_one_voice_collision`.

### One-Command Verification Across All Five Planes

```bash
# 1. Lean 4.36.0 universal proofs + #print axioms audit
lake --dir lean build && lake --dir lean exe morpheus-lean

# 2. Lane 1: Standalone Pure C++20 under both g++ and clang++ (-Wall -Wextra -Werror)
cmake -S swiftpp -B build/gcc -DCMAKE_CXX_COMPILER=g++ && cmake --build build/gcc -j && ctest --test-dir build/gcc --output-on-failure
cmake -S swiftpp -B build/clang -DCMAKE_CXX_COMPILER=clang++ && cmake --build build/clang -j && ctest --test-dir build/clang --output-on-failure

# 3. Lanes 2 & 3: Pure Swift 6.4 + Live Swift <-> C++20 Interop (0.000e+00 delta)
swift test --package-path swiftpp --build-system native -c release
swift run --package-path swiftpp --build-system native -c release ErgenticsCLI

# 4. Fourth-Language Independent Rust Verifier (10,576 chords N <= 72 + Theorem C)
cargo test --release --manifest-path rust/Cargo.toml
cargo run --release --manifest-path rust/Cargo.toml

# 5. Immutable Data Model SHA-256 integrity
sha256sum -c data/MANIFEST.sha256
```

---

## Part IV — Companion Explanatory Videos & Social Media Assets

See [`media/README.md`](../media/README.md) for the reproducible MIT generator scripts (`media/render_gemini4_neon_video.py`, `media/render_gemini4_neon_masterclass.py`), the 1:24 social reel (`media/gemini4_neon_prime_cadences.mp4`), the 4:18 **Spoken-in-Harmony Educator Masterclass** (`media/gemini4_neon_masterclass_chess_rh.mp4`), the clean poster frame (`media/gemini4_neon_poster.png`), and ready-to-post social media summaries.
