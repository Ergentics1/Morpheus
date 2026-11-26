# Gemini 4 Neon (`[G4N]`) ADPIE Cycle 1 Independent Audit — Working Paper 034 (Horizon Monograph IE)

- **Target Manuscript:** Ergentics Working Paper 034 / Horizon Series Monograph IE, *Independent Precision Audit and Structural Pressure Test of Algebraic Null-Cone Quantum Gravity (`arXiv:2611.34924v1`)* ([`cleanroom/paper.typ`](../cleanroom/paper.typ), frozen verbatim per Rule 5)
- **External Primary Preprint Audited by WP 034:** V. Chandrasekaran (Stanford University), *An algebraic quantization of gravity from the null cone*, `arXiv:2611.34924v1` [hep-th] (Nov. 23, 2026); cross-checked against A. Sen, JHEP 04 (2013) 156 (`arXiv:1205.0971v2`)
- **Auditor & Provenance:** Gemini 4 Neon (`[G4N]` / `[E→G4N]`), ADPIE Cycle 1 (2026-11-26)
- **Verification Planes:**
  1. **Plane 1 (Python 3.12 stdlib, zero external deps):** [`code/wp034_audit.py`](../code/wp034_audit.py) (`5/5` PASS, checksummed in [`data/MANIFEST.sha256`](../data/MANIFEST.sha256))
  2. **Plane 2 (Lean 4.36.0, zero Mathlib):** [`lean/WP034/Theorems.lean`](../lean/WP034/Theorems.lean) (`9/9` kernel-checked theorems, `0 sorryAx`, `0 ofReduceBool`, `0` warnings)
  3. **Plane 3 (Rust 1.100.0, zero crates):** [`rust/src/lib.rs`](../rust/src/lib.rs) + [`rust/tests/wp034_xcheck.rs`](../rust/tests/wp034_xcheck.rs) (`5/5` PASS, `0` warnings, bit-exact `SplitMix64` seam parity `0xb4005f8bfe2e1bca`)

---

## 1. Executive Meta-Audit Verdict

Working Paper 034 is an **exceptionally sharp, high-precision mathematical audit** of Chandrasekaran (`arXiv:2611.34924v1`). Every headline mathematical identity, operator counterexample, Schwarzschild/Sen (2013) rational coefficient, JT clock bound, ER=EPR Mellin integral, and Appendix D.3 Hölder/Weyl calculation in WP 034 holds up under independent three-plane reconstruction and primary-source cross-checking:

- **Pillar 1 (Dilogarithm / Clausen / `K12`):** Exact Bernoulli–Clausen split $\operatorname{Re}\operatorname{Li}_2(e^{-i\theta}) = \frac{\pi^2}{6} - \frac{\theta(2\pi-\theta)}{4} = \frac{(\theta-\pi)^2}{4} - \frac{\pi^2}{12}$, exact unreported real non-analytic cusp $\operatorname{Re} A(s) = \frac{\pi^2}{12 s^2} - \frac{\pi}{2 s^3} + \frac{1}{2 s^4}$ (`s > 1/π`), `K12` unique root $\theta^* = \pi(1 - 1/\sqrt{3}) = 1.327793289355575...$, $s^* = 1.506258553973164...$, direct partial sum failure at $s = 10^6, N = 10^5$ (`-5.0999`, `224.67%` err; `-12.0868` vs. `-14.1224`, `14.41%` err), `f64` subtraction wipeout (`-1.1102`, `29.32%` at $10^{16}$; `0.0000`, `100%` at $10^{17}$), Gieseking peak $\operatorname{Cl}_2(\pi/3) = 1.0149416$, and the Goroff–Sagnotti UV-convergence critique (`sum k^-2` already UV-convergent at $s = \infty$) are **all 100% verified**.
- **Pillar 2 (`F39` Refutation of Section 5.2):** Counterexample 2 on $\mathcal{H} = \ell^2(\mathbb{N}) \oplus \ell^2(\mathbb{N})$ ($s_* = \pi^2$, $c = e^{-\pi^2} = 5.1723\times 10^{-5}$, $\delta_\eta = 4 e^{-s_*/2}/(1+c) = 2.8766\times 10^{-2}$) is **mathematically airtight** — we further verified that it strictly satisfies Chandrasekaran's Eq. (5.24) boost variance bound with exact safety ratio $\mathrm{RHS}/\mathrm{LHS} = \pi/2 \approx 1.5708 > 1$. Paired exhaustion ($Z_{P^{\mathrm{pair}}}(10^4) = +143.8377 \to +\infty$) vs. cycle exhaustion ($r \ge 4$, $Z_{P^{\mathrm{cyc}}}(r=5, 10^4) = -287.6530 \to -\infty$), the non-Hilbert–Schmidt *petitio principii* diagnosis, and the Tonelli AdS boundary cascade (`-240.0` at $p = 0.4, M = 1000$) are **100% verified**.
- **Pillar 3 (Schwarzschild 1-Loop / Sen 2013 / `C155`):** Directly verified against Sen (2013, `arXiv:1205.0971v2` Eqs. `(1.2)`, `(1.4)`, `(1.5)`): pure 4D gravity $C_{\mathrm{local}} = 212/45$, fixed-mass angular-momentum-summed $+106/45 \ln A_H$, $J = 0$ singlet $+77/90 \ln A_H$. All exact rationals ($\alpha = 257/90$, $q = 257/302$, locked $x^* = \sqrt{257/347} = 0.860601$, RMS horizon-area dispersion $\sigma_A/\langle A\rangle = 90/\sqrt{112309} = 26.8556\%$, permanent Jensen gap $1 - \sqrt{89179}/302 = 1.1164\%$), `C155` defect (`6.013e-3 <= 7.146e-3`), and the Cauchy–Schlömilch integral (`3.66e-15` err at $s = 1000$) are **100% verified**.
- **Pillars 4 & 5 (`C154`, Supermetric, ER=EPR, Appendix D.3 `C156` & $\beta^*$):** Strict JT clock monotonicity (`C154` defect `6.943e-5 <= 4.996e-4`), $\mathrm{SL}(2,\mathbb{R})/\mathrm{SO}(2)$ conformal supermetric (`< 1e-13` rel err), Eq. (5.20) boost identity (`2.22e-16`), ER=EPR Mellin integral (`1.67e-16` err at `(0.3, 1.7)`), Appendix D.3 sharpness ratio $e^{-u}/(1-u)$ (`1.2131` at $R = e$, `1.0024` at $R = 10^6$, `C156` defect `2.289e-2 <= 2.332e-2`), optimal $\beta^*$ tightening (`2.801213` vs. `7.493939`, `2.6752x` at $C_\varepsilon = 1$), and all six primary references `[1]`–`[6]` are **verified authentic and accurate**.

At the same time, our independent audit caught **three concrete, substantive refinements** logged as `NEG-W19`–`NEG-W21` and proved **Original Theorem G5 (`[G4N]`)**, which closes the last remaining finite-limit loophole in WP 034's Section 5.2 refutation.

---

## 2. Original Result — Theorem G5 (`[G4N]`): Non-Hilbert–Schmidt Closed-Cut Riemann Rearrangement Universality

**Motivation:** WP 034's Counterexample 2 (`cleanroom/paper.typ`, lines 237–245) establishes $Z_{P_M^{\mathrm{pair}}}[X] \to +\infty$ while $Z_{P_M^{\mathrm{cyc}}}[X] \to -\infty$. A defender of `arXiv:2611.34924v1` might object that Chandrasekaran's sewing axiom only postulates a **finite, strictly positive** closed-cut amplitude $0 < Z[X] < \infty$, not $Z[X] = +\infty$. **Theorem G5** closes that loophole completely on WP 034's *exact same* Hilbert space $\mathcal{H} = \ell^2(\mathbb{N}) \oplus \ell^2(\mathbb{N})$ and operator triple $(\hat{s}, C_b, \hat{\mathcal{O}})$.

**Statement (Theorem G5 — `[G4N]`):** Let $(\mathcal{H}, \hat{s}, C_b, \hat{\mathcal{O}})$ be WP 034's infinite-dimensional counterexample with $c := e^{-s_*} \in (0, 1)$ and $\delta_\eta := 4 e^{-s_*/2}/(1+c) > 0$. For any triple of pairwise-disjoint finite index sets $(S_A, S_B, S_C) \subset \mathbb{N}$ of cardinalities $(A, B, C)$, let $P(S_A, S_B, S_C)$ be the finite-rank orthogonal projection onto $\operatorname{span}\{|0_n\rangle : n \in S_A \cup S_B\} \oplus \operatorname{span}\{|1_n\rangle : n \in S_A \cup S_C\}$. Then:

1. **Exact Closed-Cut Formula (Lean 4: [`p2_theorem_g5_closed_cut_and_nesting`](../lean/WP034/Theorems.lean#L68-L80)):**
   $$Z_{P(S_A, S_B, S_C)}[X] = \frac{\delta_\eta}{2}\bigl[(A - B) + (A - C)\,c\bigr].$$
   (Setting $(A, B, C) = (M, 0, 0)$ recovers WP 034's paired exhaustion $+\frac{1}{2}\delta_\eta M(1+c)$; setting $(A, B, C) = (M, (r-2)M, 0)$ recovers WP 034's cycle exhaustion $-\frac{1}{2}\delta_\eta M(r-3-c)$.)

2. **Constructive Strictly Nested Strong Exhaustion (Lean 4: [`p2_theorem_g5_closed_cut_and_nesting`](../lean/WP034/Theorems.lean#L68-L80)):** For **any** sequence of integer pairs $(u_M, v_M) \in \mathbb{Z}^2$, promoting all previously unmatched indices $S_{B,M} \cup S_{C,M}$ into $S_{A,M+1}$ together with $k_{\mathrm{new}} \ge 1$ fresh indices (always capturing the smallest unused natural number so $\{1,\dots,M\} \subseteq S_{A,M}$) and choosing
   $$A_{M+1} = \max\bigl(A_M + B_M + C_M + 1,\; u_{M+1},\; v_{M+1}\bigr), \quad B_{M+1} = A_{M+1} - u_{M+1}, \quad C_{M+1} = A_{M+1} - v_{M+1}$$
   yields a **strictly nested strong exhaustion** $P_1 < P_2 < \dots \uparrow \hat{1}$ with exact closed-cut trace $Z_{P_M}[X] = \frac{\delta_\eta}{2}(u_M + v_M c)$ at every step $M \ge 1$.

3. **Finite Positive Constant Exhaustion (All $c \in (0, 1)$) & Universal Kronecker Density (Irrational $c$):**
   - Setting $u_M \equiv K \ge 1, v_M \equiv K \ge 1$ yields a strictly increasing strong exhaustion $P_M \uparrow \hat{1}$ with **identically constant, finite, strictly positive** closed-cut amplitude $Z_{P_M}[X] \equiv \frac{K}{2}\delta_\eta(1+c) > 0$ for all $M \ge 1$ — yet Chandrasekaran's cycle exhaustion on the exact same space diverges to $-\infty$.
   - Whenever $c = e^{-s_*}$ is **irrational** — e.g., WP 034's $c = e^{-\pi^2}$, or the algebraic seed $s_* = \frac{1}{2}\ln 2 \implies c = 1/\sqrt{2}$ (irrationality proved from scratch in Lean 4 [`p2_theorem_g5_sqrt2_irrational_seed`](../lean/WP034/Theorems.lean#L101-L125)) — $\mathbb{Z} + \mathbb{Z} c$ is dense in $\mathbb{R}$ by Kronecker's theorem, so for **every** prescribed target $L \in \mathbb{R} \cup \{-\infty, +\infty\}$ there exists an explicit strictly nested strong exhaustion $P_M^{(L)} \uparrow \hat{1}$ with $\lim_{M \to \infty} Z_{P_M^{(L)}}[X] = L$.

**Live Python & Rust Verification (`c = e^{-pi^2}` and `c = 1/sqrt(2)`):**
- `L = +1.0` (`c = e^{-pi^2}`): `Z = 1.00000000000945` (`|err| = 9.45e-12`)
- `L = +42.0` (`c = e^{-pi^2}`): `Z = 42.00000000000301` (`|err| = 3.01e-12`)
- `L = 0.0` (`c = e^{-pi^2}`): `Z = 0.0` (`|err| = 0.0`, identically zero!)
- `L = +1.0` (`c = 1/sqrt(2)`): `Z = 0.99999508` (`|err| = 4.92e-6`, exact Dirichlet $O(1/U)$ rate)

---

## 3. Concrete Audit Catches (`NEG-W19`–`NEG-W21`)

### `NEG-W19` (Moderate/Major — Pillar 1 Numerical/Algorithmic Critique, `paper.typ` lines 220 & 224)
WP 034 attributes the `100%` wipeout of $\Delta_{\mathrm{re}}(s) = s^3(\operatorname{Re} A(s) - \frac{\pi^2}{12 s^2})$ at $s \ge 10^{17}$ (`"still 60 orders of magnitude below a solar-mass black hole s ≈ 10^77!"`) to IEEE-754 `binary64` and presents 106-bit Dekker–Knuth Double-Double EFT subtraction (`spp_p7s_dd_pair_re_anomaly`) as the cure (`< 10^-15` at `s = 10^17` and beyond / through `10^20`).
- **Catch 1 (106-bit DD EFT's own catastrophic wall):** Authentic 106-bit DD subtraction of $\pi^2/6$ loses $\approx \log_2(s)$ mantissa bits: at $s = 10^{20}$ its relative error is already $9.65 \times 10^{-14}$ (not $< 10^{-15}$, contradicting Fig. 1 caption line 224 if subtraction is actually performed in 106-bit DD), at $s = 10^{33}$ it degrades to **`96.17%` error** (`-3.0815` vs. `-1.5708`), and at a solar-mass black hole ($s = 10^{77}$) it collapses to exact **`0.0000` (`100%` wipeout)** — still 44 orders of magnitude short of $s \approx 10^{77}$.
- **Catch 2 (Algebraic formula-choice artifact):** The wipeout is not an IEEE-754 `binary64` limitation at all — it comes solely from numerically adding $\pi^2/6$ and subtracting $\pi^2/6$ back out. Evaluating the algebraically canceled form $\Delta_{\mathrm{re}}(s) = -\frac{\pi}{2} + \frac{1}{2 s}$ (proved exact in Lean 4 [`p1_bernoulli_re_dilog_and_cancel_free_identity`](../lean/WP034/Theorems.lean#L24-L27)) in **standard 53-bit `binary64`** achieves **`0.0` (`< 1 ULP`) relative error** at $s = 10^{16}, 10^{17}, 10^{20}, 10^{33}, 10^{77}$ (and up to $s = 10^{308}$).
- **Recommended fix:** Distinguish (a) algebraic cancellation-free evaluation of $\Delta_{\mathrm{re}}(s)$ in standard `f64` (exact through $s = 10^{308}$) from (b) where 106-bit DD genuinely adds value (e.g., high-precision intermediate argument reduction in `cr_clausen2` or sub-ULP transcendental libraries).

### `NEG-W20` (Moderate — Pillar 2 Strengthening via Theorem G5 & Internal Witness Mismatch, `paper.typ` lines 179, 255, 361)
1. **Finite-limit loophole closed by Theorem G5:** As proved in Section 2 above, Counterexample 2's $+\infty$ vs. $-\infty$ dichotomy can be strengthened on the exact same space to exhibit strictly nested strong exhaustions converging to **any finite target $L \in \mathbb{R}$** (including identically constant finite positive $0 < Z[X] < \infty$) while Chandrasekaran's cycle net diverges to $-\infty$.
2. **Internal witness mismatch across Table 1, Fig. 2, and Table 2:** Table 1 (line 179) reports `F39 witness = 1.50` (the value of $2 - 2/(r-1)$ at $r = 5$), whereas Fig. 2 caption (line 255) and Table 2 (line 361) report `Delta_rearr(12) = 1.818 > 0.50` (the value at $r = 12$), and $\Delta_{\mathrm{rearr}}(r)$ is never defined in prose (Lean 4 check: [`p2_f39_cycle_sign_inversion_and_witness`](../lean/WP034/Theorems.lean#L54-L62)).
- **Recommended fix:** Define $\Delta_{\mathrm{rearr}}(r)$ explicitly in Pillar 2 prose, harmonize `r = 5` (`1.50`) vs. `r = 12` (`1.818`) across Table 1, Fig. 2, and Table 2, and incorporate Theorem G5 to seal the finite-$Z[X]$ defense.

### `NEG-W21` (Minor — Certificate Domain-Scope Gaps, Parametric Specializations & Upstream Scope, `paper.typ` lines 274, 294–308, 338–375)
1. **`C156` domain excludes the highlighted $R = e$ endpoint:** Table 2 (line 352) certifies `C156` on $u \in [0.01, 0.35]$, which corresponds to $R \ge e^{(1-0.35)/0.35} = e^{13/7} \approx 6.4054 > e \approx 2.7183$ (proved in Lean 4 [`p5_c156_domain_catch_and_amgm_exact`](../lean/WP034/Theorems.lean#L180-L192)). At the highlighted $R = e$ point ($u = 0.50$), $|e^{-u}/(1-u) - (1 + u^2/2)| = 0.0881 > 0.025$ — outside the `C156` certified tolerance.
2. **`C153` domain covers only $s \in [5, 200]$:** Table 2 (line 340) certifies `cr_clausen2` on $\theta \in [0.01, 0.40]$, not the macroscopic $s \ge 10^{16}$ regime discussed in Pillar 1.
3. **JT clock `C154` proportional-cap scope:** WP 034's strict monotonicity proof (Eq. 2.5, line 295) verifies the proportional-cap specialization $\lambda_c = \varepsilon w / 2$; for a fixed constant cap $\lambda_c$ independent of $w$, monotonicity holds trivially in one line.
4. **Appendix D.3 $\beta^*$ gain dependence on $C_\varepsilon$:** The `2.6752x` tightening ratio (`7.4939 / 2.8012`) holds specifically at $C_\varepsilon = 1$. For general $C_\varepsilon > 0$, the exact ratio is $(1 + \frac{\pi^4}{15} C_\varepsilon) / (2.801213\, C_\varepsilon^{1/4}) \ge 1$, with equality at $C_\varepsilon = 5/\pi^4 \approx 0.05133$.
5. **Minor citation/upstream notes:** Line 274 cites an internal line number `L1970` of `arXiv:2611.34924v1` rather than a section/equation label; upstream `Swift++` v3.1 binary/scroll artifacts (`Scroll 44`, `156/156` Pinakes, `62,400` RCTs, CRC-64 `0xF26558090BB83BB2`, `142/142` XCTests) remain `[E]` upstream claims outside this repository.

---

## 4. Three-Plane Independent Verification Summary

| Plane | Artifact | Live Result | Highlights |
| :--- | :--- | :--- | :--- |
| **Plane 1 (Python 3.12)** | [`code/wp034_audit.py`](../code/wp034_audit.py) | `5/5` PASS | Authentic 106-bit DD EFT (`1e16`–`1e77`), Theorem G5 (`|err| ~ 1e-12`), Sen rationals, Cauchy–Schlömilch (`3.66e-15`), ER=EPR (`1.67e-16`), `SplitMix64` RCT (`1600/1600` vs `0/1600`, `0xb4005f8bfe2e1bca`) |
| **Data Model (CC BY 4.0)** | [`data/MANIFEST.sha256`](../data/MANIFEST.sha256) | `1/1` OK | SHA-256 verified against `wp034_g4n_cycle1_calibration.json` |
| **Plane 2 (Lean 4.36.0)** | [`lean/WP034/Theorems.lean`](../lean/WP034/Theorems.lean) | `9/9` PASS | `0` Mathlib, `0` warnings, `0 sorryAx`, `0 ofReduceBool`; includes Theorem G5 nesting & from-scratch irrationality of $\sqrt{2}$ |
| **Plane 3 (Rust 1.100.0)** | [`rust/tests/wp034_xcheck.rs`](../rust/tests/wp034_xcheck.rs) | `5/5` PASS | `0` crates, `0` warnings; FMA-backed 106-bit DD EFT + bit-exact `SplitMix64` parity (`0xb4005f8bfe2e1bca`, `1600/1600` vs `0/1600`) |

---

## 5. Grok Bot (`[GB]`) Cross-Check Protocol

To complete dual-agent independent sign-off (`[G4N]` + `[GB]`), Grok Bot should independently check:
1. **Pillar 1 (`NEG-W19`):** Verify in an independent high-precision implementation that 106-bit DD closed-form subtraction hits `~9.65e-14` at $s = 10^{20}$, `~96.2%` error at $s = 10^{33}$, and `0.0000` at $s = 10^{77}$, while cancellation-free `binary64` (`-pi/2 + 1/(2s)`) holds to `< 1 ULP` through $s = 10^{77}$.
2. **Pillar 2 (Theorem G5 & `NEG-W20`):** Independently check that WP 034's Counterexample 2 obeys Eq. (5.24) with ratio $\pi/2$, verify Theorem G5's $Z_{P(A,B,C)}[X] = \frac{\delta_\eta}{2}[(A-B)+(A-C)c]$ and constant-positive exhaustion $u_M = v_M = K$, and confirm the Table 1 (`1.50`) vs. Table 2 (`1.818`) witness mismatch.
3. **Pillar 3–5 (`NEG-W21`):** Independently cross-check Sen (2013) `arXiv:1205.0971v2` Eqs. `(1.2)`/`(1.4)`/`(1.5)` (`+106/45` mixed vs. `+77/90` singlet), `C156` domain boundary $R_{\min} = e^{13/7} \approx 6.4054 > e$, and general-$C_\varepsilon$ optimal $\beta^*$ equality at $C_\varepsilon = 5/\pi^4$.
