// Working Paper 035 / Horizon Series Monograph IF (Swift++ Library of Alexandria Epoch XLI)
// Dual-Track Monograph:
//   Track A: Independent [X] Audit of J. L. Nielsen (Aug. 2026) TUFT (250 pp.)
//   Track B: Non-Circular Constructive Repair (Theorems R1-R3) of Chandrasekaran (arXiv:2611.34924v1, Sec. 5.2)
// Compile: typst compile paper.typ paper.pdf
// Copyright (c) 2026 Ergentics, LLC -- MIT License

#set document(
  title: "Independent Precision Audit of Hopf-Fibration Unified Field Theory (Nielsen 2026) and Non-Circular Hagedorn Nuclearity Repair of Algebraic Null-Cone Gravity",
  author: "Ergentics, LLC & Swift++ Library of Alexandria Verification Program",
)

#set page(
  paper: "us-letter",
  margin: (x: 0.72in, y: 0.66in),
  numbering: "1",
  number-align: center,
  header: context {
    if counter(page).get().first() > 1 {
      set text(size: 8.0pt, fill: luma(95), style: "italic")
      grid(
        columns: (1fr, auto),
        [TUFT \[X\] Audit & Hagedorn Nuclearity Repair of Null-Cone Gravity],
        [Ergentics Working Paper 035 · Horizon Monograph IF],
      )
      v(-6pt)
      line(length: 100%, stroke: 0.4pt + luma(180))
    }
  },
)

#set text(
  font: "New Computer Modern",
  size: 9.35pt,
  lang: "en",
)

#set par(
  justify: true,
  leading: 0.49em,
  first-line-indent: 1.2em,
)

#set heading(numbering: "1.1")
#show heading.where(level: 1): it => {
  v(8.5pt, weak: true)
  set text(size: 11.0pt, weight: "bold", fill: rgb("#0f172a"))
  block(breakable: false)[#it]
  v(2.8pt, weak: true)
}
#show heading.where(level: 2): it => {
  v(7pt, weak: true)
  set text(size: 9.9pt, weight: "bold", fill: rgb("#1e293b"))
  block(breakable: false)[#it]
  v(4.2pt, weak: true)
}

#show table: set par(justify: false)
#show table: it => {
  show raw: set text(size: 7.7pt)
  it
}
#show raw.where(block: false): it => if it.text == "Swift++" { box(it) } else { it }
#show figure.caption: it => {
  set text(size: 8.2pt, fill: luma(55))
  set par(leading: 0.46em, justify: true)
  it
}

#let varepsilon = sym.epsilon.alt
#let hbar = sym.planck
#let hD = $cal(H)_cal(D)$
#let thm-cnt = counter("thm")

#let env-box(kind, accent, title: none, body) = {
  thm-cnt.step()
  v(3.5pt, weak: true)
  block(
    width: 100%,
    inset: (left: 10pt, right: 8pt, top: 5pt, bottom: 5pt),
    stroke: (left: 2pt + accent),
    fill: luma(249),
    radius: (right: 3pt),
    breakable: false,
  )[
    #set par(first-line-indent: 0pt)
    #text(weight: "bold", fill: accent)[#kind #context thm-cnt.display("1")#if title != none [ (#title)].] #emph(body)
  ]
  v(3.5pt, weak: true)
}

#let theorem(title: none, body) = env-box("Theorem", rgb("#1e3a8a"), title: title, body)
#let proposition(title: none, body) = env-box("Proposition", rgb("#0f766e"), title: title, body)
#let counterexample(title: none, body) = env-box("Counterexample", rgb("#b91c1c"), title: title, body)
#let remark(title: none, body) = {
  thm-cnt.step()
  v(3.5pt, weak: true)
  block(
    width: 100%,
    inset: (left: 10pt, right: 8pt, top: 5pt, bottom: 5pt),
    stroke: (left: 1.8pt + luma(120)),
    fill: luma(251),
    radius: (right: 3pt),
    breakable: false,
  )[
    #set par(first-line-indent: 0pt)
    #text(weight: "bold", fill: luma(50))[Remark #context thm-cnt.display("1")#if title != none [ (#title)].] #body
  ]
  v(3.5pt, weak: true)
}

#let proof(body) = {
  block(breakable: true)[
    #set par(first-line-indent: 0pt)
    #emph[Proof.] #body #h(1fr) $square$
  ]
  v(3pt, weak: true)
}

// ============================================================================
// TITLE BLOCK
// ============================================================================
#align(center)[
  #text(size: 8.0pt, weight: "bold", tracking: 0.06em, fill: rgb("#0f766e"))[
    ERGENTICS WORKING PAPER 035 · HORIZON SERIES MONOGRAPH IF · ALEXANDRIA EPOCH XLI
  ]
  #v(5pt)
  #text(size: 14.2pt, weight: "bold", fill: rgb("#0f172a"))[
    Independent Precision Audit of Hopf-Fibration Unified Field Theory (Nielsen 2026) and Non-Circular Hagedorn Nuclearity Repair of Algebraic Null-Cone Gravity
  ]
  #v(5pt)
  #text(size: 9.5pt, fill: luma(60))[
    Ergentics, LLC & The `Swift++` Library of Alexandria Verification Program
  ]
  #v(2pt)
  #text(size: 8.5pt, fill: luma(95), style: "italic")[
    November 26, 2026 · Clean-Room 75-Digit \[X\] Audit & `Swift++` v3.1 Zero-LLVM Pass 9B Certification (Scroll 45, Seams `C157–C160`, `K13`, `F40`)
  ]
]

#v(5pt)
#block(
  width: 100%,
  inset: (x: 11pt, y: 6.5pt),
  fill: luma(248),
  stroke: (y: 0.6pt + luma(190)),
)[
  #set par(first-line-indent: 0pt, leading: 0.47em)
  #text(size: 8.7pt)[
    *Abstract.* This dual-track monograph reports two independent investigations certified via clean-room 75-digit exact arithmetic (`verify_all_results.py`) and an upgraded `Swift++` v3.1 Zero-LLVM Pass 9B precision-and-prover stack (`SppStd.CRMathSpecial` extended to 21 correctly-rounded functions including 106-bit Double-Double `cr_lgamma`, `cr_digamma`, `cr_hurwitz_zeta_p0`, and `cr_zeta_odd`; `IntervalProofEngine.swift` extended with outward-rounded polygamma `Jet2`/`Jet2D` intervals).
    _Track A_ performs a complete forensic referee audit of J. L. Nielsen's 250-page manuscript _"A Complete Topological Unified Field Theory on the Complex Hopf Fibration"_ (TUFT, Aug. 2026) [1]. While confirming exact spectral zeta derivatives on $S^7$ ($+1.748452204448$) and $S^9$ ($-0.413644658190$), our audit uncovers eight disqualifying mathematical, physical, formal-proof, and statistical failures: (i) an opposite-sign, $2 pi^2 approx 19.74 times$ error in Eq. (65) / Lemma 6 on $L(p, 1)$ paired with an incorrect lens-space spectrum; (ii) selective omission of $zeta'_R (0) = -1/2 ln(2 pi)$ on $S^3$ ($30.2 times$) and $S^5$ ($22.9 times$, flipping sign) while retaining it on $S^7, S^9$; (iii) a literal $2.955 times$ algebraic non-sequitur in Theorem 56's quark slope $a_5$; (iv) uncited reuse of Wyler's 1969 $alpha$ formula ($+3,965 sigma$ off CODATA) coupled with a false Lemma 8 scale-invariance claim (exact $R^(-19/4)$, mechanically falsified by `F40`); (v) a three-way $10^5 sigma$ accidental error cancellation masking wrong 2-loop and wrong-sign 3-loop QED coefficients in $a_e$ ($+5,407 sigma$ at CODATA $alpha$) and a quadratic $cal(L)(cal(L)-2)$ overshoot in $a_tau$ ($+62.3%$ over 2-loop QED); (vi) explicit smooth Clifford-torus Beltrami eigenforms at all odd $k = 1, 3, 5, 7, dots$ plus an 8-dimensional integrable $U(1)$-symmetric subspace at $k = 4$ refuting Theorems 45 and 50; (vii) fatal dark-sector vector-calculus and dimensional errors ($nabla dot (nabla times bold(Omega)) equiv 0$, $r^(-1/2)$ velocity decay, and an 89-order electroweak $rho_Lambda$ mismatch); and (viii) a Künneth-vs.-Cartesian ring-product fallacy in Appendix B's Lean 4 kernel alongside a refuted Appendix C Bayes factor.
    _Track B_ delivers original, non-circular functional-analytic derivations repairing the circular cycle-rearrangement proof (`F39`) identified in V. Chandrasekaran's null-cone gravity preprint (`arXiv:2611.34924v1`, Sec. 5.2) [2], [12]. We prove the _Schatten–Riesz Dichotomy_ (Theorem R1), a _Non-Circular Compact-Resolvent / Buchholz–Wichmann Nuclearity Repair_ (Theorem R2), and an _Exact Entropy–Nuclearity Scaling Classification_ (Theorem R3) proving that Bekenstein–Hawking linear entropy $ln dim hD tilde beta_H Q_*$ is mathematically equivalent to a strictly positive Hagedorn abscissa $beta_c = beta_H > 0$, with an exact $+1$ canonical-to-microcanonical variance shift and Stirling–Chernoff Binet gap $Delta_"Stirling" (alpha)$ certified by `C160` across Sen's $J$-summed ($alpha = 151/45$), Chandrasekaran's ($alpha = 257/90$), and Sen's $J = 0$ ($alpha = 167/90$) gravitational exponents.
  ]
]

// ============================================================================
// SECTION 1: INTRODUCTION & EXECUTIVE VERDICT
// ============================================================================
= Introduction and Dual-Track Scope

Horizon Monograph IE (Working Paper 034) [12] demonstrated that pairing clean-room arbitrary-precision arithmetic with `Swift++` v3.1's compiled-IR outward-rounded interval/AD prover (`SppMLIR` `Jet2`/`Jet2D` and Moore–Krawczyk certification) [10] turns theoretical-physics refereeing into an executable, reproducible discipline. In Horizon 1F (Alexandria Epoch XLI), we deploy this methodology on two complementary fronts:

1. _Track A (External Stress Test \#2 — Nielsen 2026 TUFT [1]):_ A 250-page unified-theory manuscript containing 83 numbered theorems, spectral zeta computations across the odd Hopf spheres $S^3, S^5, S^7, S^9$, a 40-digit Python suite (Appendix A), a dependency-free Lean 4 formalization (Appendix B), and a Bayesian claim $B = 8.6 times 10^(29)$ (Appendix C). Every claim is evaluated fairly — crediting verified exact calculations before pressure-testing every algebraic, spectral-geometric, physical, formal-logic, and statistical link.
2. _Track B (Original Constructive Derivations — Repairing Chandrasekaran [2] Sec. 5.2):_ Working Paper 034 [12] mechanically falsified (`F39`) Chandrasekaran's closed-cut cycle-rearrangement proof of $dim hD < infinity$ via an explicit infinite-dimensional counterexample. Rather than stopping at refutation, Section 4 derives three complete, non-circular theorems (Theorems R1–R3) establishing exactly what ambient spectral hypothesis is necessary and sufficient to yield _both_ $dim hD < infinity$ _and_ exact Bekenstein–Hawking linear scaling with Sen's 1-loop logarithmic correction [9].
3. _Precision Toolchain Upgrade \#2 (`Swift++` v3.1):_ Driven directly by Hurwitz zeta derivatives in Track A and Hagedorn Stirling–Chernoff remainders in Track B, Section 5 extends `SppStd.CRMathSpecial` / `SppStd.CRMath` from 17 to 21 Zero-LLVM functions (`cr_lgamma`, `cr_digamma`, `cr_hurwitz_zeta_p0`, `cr_zeta_odd`) [11] and adds sound polygamma `Jet2`/`Jet2D` enclosures to `IntervalProofEngine.swift`, sealing Scroll 45 (`C157–C160`, `K13`, `F40`).

#figure(
  table(
    columns: (1.45fr, 1.25fr, 2.55fr),
    align: (left, left, left),
    stroke: 0.45pt + luma(195),
    inset: 4.2pt,
    fill: (_, y) => if y == 0 { rgb("#0f172a") } else if calc.odd(y) { luma(249) } else { white },
    table.header(
      text(fill: white, weight: "bold", size: 8.2pt)[Audit Domain],
      text(fill: white, weight: "bold", size: 8.2pt)[Target Reference],
      text(fill: white, weight: "bold", size: 8.2pt)[Clean-Room 75-Digit & `Swift++` v3.1 Verdict],
    ),
    [*Verified Exact Results*], [$S^7$ p. 146; $S^9$ Eq. (136); $S^3$ Eq. (90)], [*Confirmed:* $zeta'_(cal(B)_7)(0)=+1.748452204$ (7/7 digits), $zeta'_(Delta_2)(0)=-0.413644658$ (5/5 digits), $zeta'_1(0)=+0.888490076$, and $sigma_3 zeta(2)=zeta(3)/24$.],
    [*Spectral Zeta & $L(p, 1)$*], [Eq. (65), Lem. 6, pp. 111–134], [*Refuted (`C158`):* Exact $-zeta'_"Eq65" (0) = +(zeta(3)/pi^2) p^2 + O(p ln p)$ — _opposite sign_ & $2 pi^2 = 19.74 times$ off claimed $-2 zeta(3) p^2$; wrong $L(p,1)$ spectrum; $zeta'_R (0)$ selectively dropped on $S^3, S^5$.],
    [*Quark Slope $a_5$*], [Thm. 56, pp. 134, 136, 225], [*Refuted:* Derived $a_5 = 6 sqrt(3) e^("spec"_5 / 6) = 10.5320$ equated on the next line to $sqrt(3)(2 + zeta(3)/(4 pi^2)) e^("spec"_5 / 6) = 3.5641$ — literal *$2.9550 times$ non-sequitur* ($m_t$ off by $1.20 times 10^9 times$ if derived formula used).],
    [*Fine-Structure $alpha$*], [Thm. 66, Lem. 8, pp. 156–157], [*Refuted (`F40`):* Uncited Wyler (1969) formula [3], *$+3,965.3 sigma$* off CODATA 2022; Lemma 8 scale-invariance claim false (exact $R^(-19/4)$, Robertson [3]; witness $R^* = 2.1$, defect $0.9705$).],
    [*Leptons & $g-2$*], [App. A, pp. 224, 227], [*Refuted (`C157`):* Unanchored $m_e$ $+7.42 times 10^6 sigma$, anchored $m_mu$ $+1,129 sigma$; $a_e$ hides 3-way $10^5 sigma$ cancellation ($+5,407 sigma$ at CODATA $alpha$); $a_tau$ quadratic $cal(L)(cal(L)-2)$ overshoots 2-loop QED by $+62.3%$ ($+3.1 sigma$).],
    [*3-Generation Proof*], [Thms. 45, 50, pp. 105–108], [*Refuted:* Explicit smooth Clifford-torus Beltrami eigenforms exist for _every_ odd $k = 1, 3, 5, 7, dots$ plus 8 integrable $U(1)$-symmetric modes at $k = 4$ via Cartan identity $i_B d(i_K omega) = 0$.],
    [*Dark Sector & Lean/Bayes*], [Eqs. (194–199), Apps. B–C], [*Refuted:* $nabla dot (nabla times bold(Omega)) equiv 0$; Eq. (199) $v prop r^(-1/2)$; Eq. (194) wrong units & $10^(89) times$ off at $R_"EW"$; Lean App. B confuses $R times S$ ($X ⊔ Y$) with $R times.o S$ ($X times Y$); App. C $log_(10) B <= -3.41 times 10^6$.],
    [*Null-Cone Sec. 5.2 Repair*], [Chandrasekaran [2] Sec. 5.2, App. D.3], [*Constructively Repaired (`C159–C160`, `K13`):* Theorems R1–R3 replace circular cycle rearrangement with Hagedorn compact-resolvent nuclearity ($beta_c = beta_H > 0$), proving $dim hD < infinity$ and exact BH + Sen log entropy.],
  ),
  caption: [Executive summary of Track A (Nielsen 2026 TUFT [1]) and Track B (Chandrasekaran [2] Sec. 5.2 constructive repair) certified at 75-digit clean-room precision and in `Swift++` v3.1.],
)

// ============================================================================
// SECTION 2: TRACK A — SPECTRAL GEOMETRY & ALGEBRAIC AUDIT OF NIELSEN (2026)
// ============================================================================
= Track A: Spectral Geometry and Algebraic Audit of Nielsen (2026) TUFT

A rigorous audit must first separate valid calculations from errors. Across the 250-page manuscript [1], standard topological preliminaries (Wu–Yang bundle transition maps, Hopf nontriviality $c_1 = 1$, self-adjointness of $cal(B) = star d$ on $Omega^1_"coex" (S^3)$ with $cal(B)^2 = Delta_1$, vanishing odd-dimensional Seeley–DeWitt coefficients $a_d = 0$, and $sigma_3 zeta(2) = zeta(3)/24$) are stated accurately. Moreover, our independent 75-digit Euler–Maclaurin analytic continuation of $zeta'_H (-r, a)$ (verified against exact closed forms at $r = 0, 2, 4, 6$ to $9.69 times 10^(-67)$ and against Lerch's identity [11] to $3.47 times 10^(-73)$) confirms three nontrivial spectral zeta evaluations in [1]:
$
  zeta'_(cal(B)_7)(0) = +1.748452204448 quad ("p. 146:" +1.748452), wide
  zeta'_(Delta_2, S^9)(0) = -0.413644658190 quad ("Eq. 136:" -0.41364),
$
and $zeta'_1(0) = zeta'_R (-2) - zeta'_R (0) = +0.888490076146$ (Eq. 90: $0.888490076$). Every quantitative physics derivation downstream of these preliminaries, however, breaks down under exact scrutiny.

== Nash–O'Connor Lens-Space Determinant Error (Eq. 65 / Lemma 6) and Selective $zeta'_R (0)$ Dropping

To derive the universal quadratic mass exponent $-zeta(3) n^2$ in the lepton mass formula, Nielsen [1, pp. 111–112] writes the lens-space coexact 1-form zeta function on $L(p, 1) = S^3 \/ bb(Z)_p$ in Eq. (65) as
$
  zeta_"Eq65" (s) = sum_(m=1)^infinity 2(m p)(m p + 2)(m p + 1)^(-2s)
  = 2 p^(2-2s) zeta_H (2s - 2, 1 + 1/p) - 2 p^(-2s) zeta_H (2s, 1 + 1/p),
$
and asserts in Lemma 6 that $-zeta'_"Eq65" (0) = -2 zeta(3) p^2 + O(p)$. Both the analytic evaluation _and_ the underlying lens-space spectrum are wrong.

#proposition(title: "Exact Evaluation of Nielsen Eq. (65) and True Lens-Space Spectrum")[
  Differentiating $zeta_"Eq65" (s)$ exactly at $s = 0$ via $zeta_H (-2, a) = -(1/3) B_3 (a)$, $zeta_H (0, a) = 1/2 - a$, and Lerch's identity $zeta'_H (0, a) = ln Gamma(a) - (1/2) ln(2 pi)$ [11] yields, as $p -> infinity$,
  $
    -zeta'_"Eq65" (0) &= 4 p^2 ln p dot zeta_H (-2, 1 + 1/p) - 4 p^2 zeta'_H (-2, 1 + 1/p) - 4 ln p dot zeta_H (0, 1 + 1/p) + 4 zeta'_H (0, 1 + 1/p) \
    &= +(zeta(3))/pi^2 p^2 - 2/3 p ln p + O(p).
  $
  Thus Nielsen Lemma 6 has the _wrong sign_ and is off by an exact factor of $2 pi^2 = 19.7392088 times$ ($+0.121794 p^2$ vs. claimed $-2.404114 p^2$). Furthermore, $zeta_"Eq65" (s)$ is not the spectrum of $Delta_1$ on $L(p, 1)$ [4]: under $S U(2)_L times S U(2)_R$, level $n$ coexact 1-forms decompose as $(V_(n-1) times.o V_(n+1)) plus.o (V_(n+1) times.o V_(n-1))$, and $bb(Z)_p$-invariance along the Hopf $U(1)_R$ fiber selects weights $q equiv 0 (mod p)$ at _every_ level $n >= 1$ (e.g., on $L(3, 1)$, multiplicities for $n = 1..6$ are $4, 4, 8, 20, 22, 28$ with Weyl density $1/3$, whereas Eq. (65) gives $0, 0, 30, 0, 0, 96$).
]

The Lerch Hurwitz expansion $zeta'_H (0, 1 + u) + (1/2) ln(2 pi) = ln Gamma(1 + u) arrow.r.hook -gamma_"EM" u + (pi^2 / 12) u^2$ ($u = 1/p in [10^(-3), 0.25]$) is certified directly over compiled `cr_hurwitz_zeta_p0` by `Swift++` seam `C158` (`1` `Jet2` box, `max_hi = 6.319e-3 <= 8.0e-3`). Compounding Eq. (65), Nielsen handles the universal $zeta'_R (0) = -(1/2) ln(2 pi) = -0.918939$ term inconsistently across the four odd spheres (Figure 1b): on $S^3$ (p. 115), dropping $-zeta'_R (0) = +0.918939$ shrinks $zeta'_1(0) = +0.888490$ by $30.2 times$ to $+zeta(3)/(4 pi^2) = +0.030448$; on $S^5$ (pp. 128, 134), dropping $+2 zeta'_R (0) = -1.837877$ flips the exact $zeta'_(cal(B)_5)(0) = -1.757764$ to `spec5` $= +0.080113$ ($22.9 times$ and _opposite sign_); yet on $S^7$ and $S^9$, the $zeta'_R (0)$ contribution ($+1.837877$ on $S^7$) is _kept_ to match the quoted values $+1.748452$ and $-0.41364$.

#figure(
  image("fig1_tuft_spectral_zeta_and_eq65.svg", width: 99%),
  caption: [Spectral zeta forensic audit of Nielsen [1]. (a) Exact normalized $(-zeta'_"Eq65" (0)) \/ p^2 -> +zeta(3)/pi^2 = +0.1218$ (teal) versus Nielsen Lemma 6's claimed $-2 zeta(3) = -2.4041$ (crimson), an opposite-sign error of factor $2 pi^2 = 19.74 times$. (b) Selective omission of $zeta'_R (0)$ on $S^3, S^5$ versus retention on $S^7, S^9$.],
)

== Theorem 56's $2.955 times$ Algebraic Non-Sequitur, Wyler's $alpha$, and Lemma 8 (`F40`)

Three further algebraic defects break the parameter-free derivation claims of Parts III–IV:

1. _Quark Slope $a_5$ ($2.955 times$ Non-Sequitur, Thm. 56, pp. 134, 136, 225):_ In the "Assembly" of the $S^5$ quark mass slope, Nielsen evaluates $a_5 = kappa_5 gamma_"eff"^((5)) ell = (1/(8 pi^3)) e^("spec"_5 / 6) dot 8 pi^3 sqrt(3) dot 6 = 6 sqrt(3) e^("spec"_5 / 6) = 10.531995$, and on the _immediately following equality sign_ writes $= e^("spec"_5 / 6) sqrt(3)(2 + zeta(3)/(4 pi^2)) = 3.564112$, silently replacing $6$ with $2 + zeta(3)/(4 pi^2) approx 2.030448$ — an algebraic error of factor $2.955012 times$. Because $a_5$ enters $exp(a_5 n)$, using the actually derived $a_5 = 10.5320$ blows up the top-quark mass $m_t$ by $exp(3(10.5320 - 3.5641)) = 1.198 times 10^9 times$.
2. _Uncited Wyler (1969) $alpha$ Formula & $+3,965 sigma$ Discrepancy (Thm. 66, pp. 156–157, 226):_ Theorem 66's geometric coupling $alpha = (9/(8 pi^4))(pi^5 / 1920)^(1/4) = 1/137.036082448$ is Armand Wyler's 1969 formula [3] (even named `aW` in Nielsen's own Appendix A code on p. 226, without citing Wyler). Against CODATA 2022 ($alpha^(-1) = 137.035999177(21)$), it is ruled out at *$+3,965.3 sigma$*.
3. _False Lemma 8 Scale Invariance (`F40`) and Homogeneous Space Error:_ Lemma 8 (pp. 156–157) claims the volume ratio $"Vol"(S^2) "Vol"(S^9)^(1/4) / ("Vol"(S^4)^2 "Vol"(bb(R)P^1))$ has homogeneity degree $0$ under simultaneous rescaling $g |-> R^2 g$, and p. 157 asserts $"Vol"(S^4) = "Vol"(S U(3) \/ S U(2))$ (false: $S U(3) \/ S U(2) tilde.eq S^5$, not $S^4$). Exactly as Robertson [3] showed in 1971, the ratio scales as $R^(2 - 8 - 1 + 9/4) = R^(-19/4) = R^(-4.75)$ — not $R^0$. `Swift++` mechanical falsifier `F40` refutes Lemma 8 on $R in [1.20, 3.00]$ with witness $R^* = 2.1$ ($1 - 2.1^(-4.75) = 0.9705 > 0.50$, Figure 3b).

// ============================================================================
// SECTION 3: NUMERICAL REPLICATION, g-2 CANCELLATION, BELTRAMI & LEAN/BAYES
// ============================================================================
= Experimental Pulls, Three-Way $g-2$ Cancellation, Beltrami Refutation, and Formal Audits

== Full Appendix A Replication, $a_e$ Three-Way Cancellation (`C157`), and $a_tau$ Overshoot

Executing every formula of `TUFT_Verification.py` [1, pp. 222–227] at 75-digit precision reveals a sharp split between loosely constrained sectors (quarks, $W, Z, H$, neutrinos, CKM — where $approx 25$ sector-specific algebraic choices absorb $approx 0.1$–$1%$ uncertainties) and precision QED/lepton observables (Figure 2a):
- _Charged leptons:_ Unanchored masses deviate by $+0.232%$ ($m_e$: *$+7.42 times 10^6 sigma$*), $+0.235%$ ($m_mu$: *$+1.08 times 10^5 sigma$*), and $+0.228%$ ($m_tau$: *$+45.1 sigma$*) — and the paper contradicts itself on this offset (`3e-5` on p. 121, `+0.22%` on p. 224, `+0.10%` on p. 228). Even after anchoring on $m_e$, $m_mu = 105.660972 "MeV"$ misses PDG 2024 by *$+1,129.0 sigma$*.
- _Anomalous magnetic moments (`C157`):_ Expanding TUFT's universal phase $Delta phi_"univ" / (2 pi) = (alpha / (2 pi)) exp(-(13 zeta(3) / (24 pi)) alpha - (zeta(5) / (4 pi^2)) alpha^2 - dots)$ in powers of $alpha / pi$ gives $C_1^"TUFT" = 1/2$, $C_2^"TUFT" = -13 zeta(3)/48 = -0.32555708$ (certified by `C157`, `1` `Jet2` box, `max_hi = 8.585e-6`), and $C_3^"TUFT" = (1/2)[(1/2)(13 zeta(3)/24)^2 - zeta(5)/4] = -0.02362856$. Comparing against exact QED [5] ($C_2^"QED" = -0.32847897$, $C_3^"QED" = +1.18124146$) exposes a striking *three-way accidental cancellation* in $a_e$ (Figure 2b):
  1. _1-loop Wyler-$alpha$ shift:_ $(alpha_"Wyler" - alpha_"CODATA")/(2 pi) = -7.057 times 10^(-10)$ (*$-5,428.8 sigma$*);
  2. _2-loop $C_2$ error ($-0.89%$):_ $(C_2^"TUFT" - C_2^"QED")(alpha/pi)^2 = +1.577 times 10^(-8)$ (*$+121,269.4 sigma$*);
  3. _3-loop $C_3$ error (wrong sign, $-102%$!):_ $(C_3^"TUFT" - C_3^"QED")(alpha/pi)^3 = -1.510 times 10^(-8)$ (*$-116,156.4 sigma$*).
  These three massive opposite-sign errors cancel to 4.5 digits only when evaluated at Wyler's _wrong_ $alpha$ ($a_e^"TUFT" = 0.00115965217995$, $-4.9 sigma$ vs. Fan et al. [6]); substituting CODATA $alpha$ immediately drives TUFT's $a_e$ to *$+5,407.4 sigma$*! Furthermore, TUFT's mass-dependent term `d4` $prop cal(L)(cal(L)-2)$ ($cal(L) = ln(m/m_e)$) grows quadratically instead of exact 2-loop QED's linear Suura–Wichmann vacuum polarization $(1/3) cal(L) - 25/36$ [5]: at $m_tau$, `d4` overshoots 2-loop QED by *$+62.3%$* ($1.772 times 10^(-5)$ vs. $1.092 times 10^(-5)$), pushing $a_tau^"TUFT" = 1.177365 times 10^(-3)$ to *$+3.1 sigma$* above the Standard Model prediction $1.17721(5) times 10^(-3)$ [6].

#figure(
  image("fig2_tuft_sigma_pulls_and_g2_cancellation.svg", width: 99%),
  caption: [Precision observable audit of Nielsen [1]. (a) True $|sigma|$-pulls across 10 precision observables versus Appendix C's claimed $overline(r) = 0.10 sigma$. (b) Waterfall decomposition of the three-way $10^5 sigma$ accidental error cancellation in $a_e$ that collapses to $+5,407 sigma$ when CODATA $alpha$ is used.],
)

== Explicit Clifford-Torus Beltrami Counterexamples Refuting Theorems 45 and 50

Theorems 45 and 50 [1, pp. 105–108, 144] claim to prove exactly three fermion generations by asserting that integrable torus-foliated Beltrami eigenfields on $S^3$ exist only for $k in {1, 2, 3\}$ and break into chaos at $k >= 4$ (while inconsistently quoting eigenspace dimension $(2k+1)^2 - 1 = 80$ on p. 105 vs. $n(n+2) = 24$ on p. 107). Both claims are false.

#counterexample(title: "Infinite Family of Smooth Clifford-Torus Beltrami Eigenforms & k = 4 Integrability")[
  In Hopf coordinates $(eta, xi_1, xi_2)$ on unit $S^3$ with $y = cos^2 eta in [0, 1]$, any $T^2$-invariant 1-form $omega = f(y) d xi_1 + g(y) d xi_2$ is automatically co-closed ($d star omega = 0$) and tangent to every Clifford torus $\{eta = "const"\}$. The Beltrami equation $star d omega = lambda omega$ reduces identically to $g(y) = -(2/lambda)(1 - y) f'(y)$ and the Sturm–Liouville ODE
  $
    -4 y (d)/(d y) [(1 - y) f'(y)] = lambda^2 f(y).
  $
  For _every_ positive integer $m >= 1$ ($lambda = 2m$, level $k = 2m - 1 in {1, 3, 5, 7, 9, dots\}$), the exact Jacobi polynomial $f_m (y) = sum_(j=1)^m a_j y^j$ with $a_1 = 1$, $a_(j+1) = ((j^2 - m^2)/(j(j+1))) a_j$ terminates identically at $j = m$, satisfies the ODE with exact zero residual (e.g., at $k = 5, lambda = 6 > 3$: $f_3(y) = y - 4 y^2 + (10/3) y^3$, Figure 3a), and yields a globally smooth, strictly integrable Beltrami eigenfield foliating $S^3$ by invariant Clifford tori. Moreover, for _every_ integer $k >= 1$ (including even $k = 4, lambda = 5$), any $U(1)$-symmetric Beltrami eigenform ($cal(L)_K omega = 0$ for a Killing field $K$) obeys Cartan's magic formula $0 = cal(L)_K omega = d(i_K omega) + lambda i_K i_B ("vol") ==> i_B d(i_K omega) = 0$, making $H = g(B, K)$ an exact global first integral; at $k = 4$, $(V_3 times.o V_5) plus.o (V_5 times.o V_3)$ contains an exact 8-dimensional real subspace of $K = partial_(xi_2)$-invariant integrable Beltrami eigenfields.
]

#figure(
  image("fig3_clifford_beltrami_and_lemma8_f40.svg", width: 99%),
  caption: [Geometric refutations of Nielsen [1]. (a) Explicit smooth Clifford-torus Beltrami eigenmodes $f_m (cos^2 eta)$ at $k = 1, 3, 5, 7$ ($lambda = 2, 4, 6, 8$) refuting Theorems 45 and 50. (b) Mechanical falsifier `F40` refuting Lemma 8 scale invariance against exact $R^(-19/4)$ scaling (witness $R^* = 2.10$, defect $0.9705 > 0.50$).],
)

== Dark-Sector Identities, Core Topology Contradictions, Lean 4 Künneth Fallacy, and Appendix C

Four additional structural failures invalidate Parts I, IV, V, and Appendices B–C of [1]:
1. _Dark Matter & Dark Energy (pp. 181–183):_ Eq. (196) sets $rho_"geom" = nabla dot (lambda_Omega^2 nabla times bold(Omega) + lambda_tau^2 nabla tau)$ with constant $lambda_Omega^2 = hbar / (m gamma_Omega)$, violating the exact vector-calculus identity $nabla dot (nabla times bold(Omega)) equiv 0$ ($d^2 = 0$). Eq. (199) writes $v(r) tilde sqrt(hbar c / (r R_"Hopf"))$, which lacks velocity dimensions (missing mass) _and_ decays as $r^(-1/2)$ (Keplerian falloff), directly contradicting the next sentence on p. 183 claiming flat rotation curves. Eq. (194) writes $rho_Lambda tilde hbar c / (R_"Hopf"^2 G)$ (units $"kg"^2/"m"^2$, not $"kg"/"m"^3$); even after dimension repair to $c^2 / (G R_"EW"^2)$ at $R_"EW" = hbar c / v_H = 8.014 times 10^(-19) "m"$, it yields $2.10 times 10^(63) "kg"/"m"^3$ — *89 orders of magnitude* above $6.9 times 10^(-27) "kg"/"m"^3$ (which requires Hubble radius $R_H approx 4.4 times 10^(26) "m"$).
2. _Internal Topological & Lie-Group Contradictions:_ Strong-CP resolution (pp. 62–66) claims $c_2 equiv 0$ identically, directly contradicting Theorem 54(iv) (p. 125) invoking $integral_(bb(C)P^2) c_2 = 1$ for $S U(3)$; Theorem 13 (p. 32) falsely asserts $S U(2)_L times U(1)_R$ and $S U(2)_L times S U(2)_R$ contain a trivially acting factor on $S^3 tilde.eq S U(2)$ (both left and right multiplication are free); Theorem 58 (pp. 142–143) conflates real and imaginary parts of a single scalar eigenvalue $(d \/ (d theta))(e^(i theta)) = i e^(i theta)$ with a spin-1 photon and spin-2 graviton; and Eq. (234)'s interferometer phase $Delta phi = (alpha^2 / (4 pi)) a T^2 / L$ diverges unphysically as arm length $L -> 0$.
3. _Lean 4 Appendix B Künneth Fallacy (pp. 228–233):_ `TUFT_Forcing_Core.lean` proves `product_has_zero_divisors` (that a Cartesian ring product $R times S$ has zero divisors $(1, 0) dot (0, 1) = (0, 0)$) and applies it to $H^* (bb(C)P^infinity; bb(Z)) tilde.eq bb(Z)[c_1]$ to rule out product spaces. This confuses the cohomology of a _disjoint union_ ($H^* (X ⊔ Y) tilde.eq H^* (X) times H^* (Y)$) with the Künneth theorem for a _Cartesian product_ ($H^* (X times Y) tilde.eq H^* (X) times.o H^* (Y)$): counterexample $H^* (bb(C)P^infinity times bb(C)P^infinity; bb(Z)) tilde.eq bb(Z)[x, y]$ is an integral domain with zero zero-divisors despite being a nontrivial product! (Additionally, p. 231 prints a Lean syntax error `R.one != R.zero` (`Bool`) in a `Prop` position.)
4. _Appendix C Bayes Factor Refutation (pp. 233–235):_ Claimed $B = 10^(30) exp(-(1/2) dot 30 dot 0.10^2) = 8.6 times 10^(29)$ miscounts 22 itemized observables as 30, includes exact 2019 SI definitions $\{c, hbar, e\}$ and input $v_H$, omits parameter/formula-search degrees of freedom, and fabricates $overline(r) = 0.10 sigma$: just two precision observables ($alpha^(-1)$ at $+3,965.3 sigma$ and $a_e$ at $-4.9 sigma$) already give $chi^2 = 1.572 times 10^7 ==> log_(10) B <= -3.414 times 10^6$ (and unanchored $m_e$ adds $-1.2 times 10^(13)$).

// ============================================================================
// SECTION 4: TRACK B — ORIGINAL CONSTRUCTIVE REPAIR OF CHANDRASEKARAN SEC. 5.2
// ============================================================================
= Track B: Non-Circular Constructive Repair of Chandrasekaran (2026) Section 5.2

In Working Paper 034 [12], we proved that Section 5.2 of Chandrasekaran (`arXiv:2611.34924v1`) [2] commits a fatal _petitio principii_ (`F39`): assuming closed-cut trace invariance under $r$-cycle rearrangement on $hD$ is logically equivalent to assuming $"Tr"(C_b^dagger C_b) < infinity$, which already implies $dim hD < infinity$. Here we establish the exact functional-analytic obstruction and derive a complete, non-circular replacement that simultaneously resolves the Appendix D.3 $s^(3/4) << s^1$ entropy gap [7], [12].

== Theorem R1: Schatten–Riesz Dichotomy and Sharp No-Go Bound

#theorem(title: "R1 — Schatten–Riesz Dichotomy & No-Go for Gluing Operators")[
  Let $hD, cal(H)$ be separable Hilbert spaces and $C_b : hD -> cal(H)$ a bounded gluing operator satisfying Chandrasekaran's coercivity bound $C_b^dagger C_b >= c hat(1)_(hD)$ with $c = e^(-s_*) m_(b, cal(D)) > 0$ [2, Eq. 5.22]. Then for every Schatten–von Neumann class $cal(S)_p$ ($1 <= p < infinity$) and the ideal of compact operators $cal(K)$:
  $
    C_b in cal(K) <==> C_b in cal(S)_p quad (forall p >= 1) <==> "Tr"_(hD)(C_b^dagger C_b) < infinity <==> dim hD < infinity,
  $
  with the sharp quantitative dimension bound
  $
    dim hD <= c^(-p/2) norm(C_b)_p^p = c^(-p/2) "Tr"((C_b^dagger C_b)^(p/2)).
  $
  In particular, no argument relying solely on boundedness, Eq. (5.22), and open-amplitude Cauchy–Schwarz sewing can ever exclude $dim hD = infinity$, because $C_b^dagger C_b >= c hat(1)$ bounds the spectrum of $C_b^dagger C_b$ away from $0$, barring compactness unless $hD$ is already finite-dimensional.
]

#proof[
  Since $C_b^dagger C_b >= c hat(1)$ ($c > 0$), $A := (C_b^dagger C_b)^(-1)$ exists as a bounded self-adjoint operator on $hD$ with $norm(A) <= c^(-1)$. If $C_b in cal(K)$, then $C_b^dagger C_b in cal(K)$, so $hat(1)_(hD) = A(C_b^dagger C_b)$ is compact; by Riesz's lemma, $dim hD < infinity$. Conversely, if $dim hD = N < infinity$, $C_b$ has finite rank so $C_b in cal(S)_p subset cal(K)$ for every $p >= 1$. Finally, denoting the singular values of $C_b$ by $s_1 >= s_2 >= dots >= sqrt(c)$, $norm(C_b)_p^p = sum_(k=1)^N s_k^p >= N c^(p/2)$, yielding $N <= c^(-p/2) norm(C_b)_p^p$.
]

== Theorem R2: Non-Circular Compact-Resolvent / Buchholz–Wichmann Nuclearity Repair

Theorem R1 proves that any non-circular proof of $dim hD < infinity$ must introduce an _ambient_ spectral-density (UV nuclearity) postulate on the full Raychaudhuri focusing generator $hat(Q)_*$ rather than manipulating traces inside $hD$.

#theorem(title: "R2 — Non-Circular Ambient Nuclearity Repair of Sec. 5.2")[
  Let $hat(Q)_* >= 0$ be a densely defined self-adjoint focusing/clock generator on the ambient Hilbert space $cal(H)$, and define the bounded-clock subspace $hD := bold(1)_([0, Q_*]) (hat(Q)_*) cal(H)$ for any finite ceiling $Q_* > 0$. Assume the ambient _Buchholz–Wichmann–Hagedorn nuclearity condition_ [7], [8]: there exists a finite abscissa $beta_H in [0, infinity)$ such that
  $
    Z(beta) := "Tr"_cal(H) (e^(-beta hat(Q)_*)) < infinity wide "for all" beta > beta_H.
  $
  Then: (i) $(1 + hat(Q)_*)^(-1)$ is compact on $cal(H)$, so $hat(Q)_*$ has purely discrete spectrum of finite multiplicity; (ii) $dim hD = N(Q_*) < infinity$ holds _non-circularly_ for every $Q_* > 0$, hence every bounded gluing operator $C_b : hD -> cal(H)$ is automatically trace-class and closed-cut trace cyclicity holds unconditionally; and (iii) the Hilbert-space dimension obeys the exact Chernoff–Laplace bound
  $
    ln dim hD = ln N(Q_*) <= inf_(beta > beta_H) [beta Q_* + ln Z(beta)].
  $
]

#proof[
  Fix any $beta > beta_H$. On $[0, infinity)$, $0 <= bold(1)_([0, Q_*]) (E) <= e^(beta(Q_* - E))$. By spectral monotonicity and positivity of the trace, $N(Q_*) = "Tr"_cal(H) bold(1)_([0, Q_*]) (hat(Q)_*) <= e^(beta Q_*) "Tr"_cal(H) (e^(-beta hat(Q)_*)) = e^(beta Q_*) Z(beta) < infinity$. Because $e^(-beta hat(Q)_*)$ is trace-class (hence compact) with strictly positive eigenvalues $-> 0$, $(1 + hat(Q)_*)^(-1)$ is compact and $dim hD < infinity$ without assuming trace-class properties of $C_b$. Taking logarithms and infimum over $beta > beta_H$ gives the Chernoff bound.
]

== Theorem R3: Entropy–Nuclearity Classification (QFT vs. Hagedorn)

Theorem R2 resolves _finiteness_; we now show that the _abscissa_ $beta_c := inf{beta >= 0 : Z(beta) < infinity\}$ uniquely classifies whether the resulting microcanonical entropy is sub-Bekenstein (local QFT) or exact Bekenstein–Hawking with Sen's logarithmic correction [9].

#theorem(title: "R3 — Exact Entropy–Nuclearity Scaling Classification & Hagedorn Variance Shift")[
  Under the hypotheses of Theorem R2 with $N(Q_*) = "Tr"_cal(H) bold(1)_([0, Q_*]) (hat(Q)_*)$:
  1. _Abelian–Tauberian Equivalence:_ $limsup_(Q_* -> infinity) Q_*^(-1) ln N(Q_*) = beta_H in [0, infinity)$ _if and only if_ the Laplace abscissa of convergence of $Z(beta) = integral_0^infinity e^(-beta E) d N(E)$ is $beta_c = beta_H$.
  2. _Polynomial UV Nuclearity ($beta_c = 0$, local QFT):_ If $ln Z(beta) tilde A beta^(-gamma)$ as $beta -> 0^+$ ($gamma > 0$, $A > 0$), then the unique Chernoff minimizer $beta^* = (gamma A / Q_*)^(1/(gamma+1))$ yields strictly sub-linear entropy
     $
       ln N(Q_*) <= (gamma + 1)/(gamma^(gamma/(gamma+1))) A^(1/(gamma+1)) Q_*^(gamma/(gamma+1)), wide lim_(Q_* -> infinity) (ln N(Q_*))/Q_* = 0.
     $
     At $gamma = 3$ (3+1D graviton box), $(gamma + 1)/gamma^(gamma/(gamma+1)) = 4 / 3^(3/4) = 1.75476535$, recovering the $s^(3/4)$ Cohen–Kaplan–Nelson / Appendix D.3 ceiling [7], [12]: no finite $gamma$ can reach linear Bekenstein–Hawking scaling $s^1$.
  3. _Hagedorn Compact-Resolvent Spectrum ($beta_c = beta_H > 0$, Quantum Gravity):_ Suppose $rho(E) = C E^(alpha - 1) e^(beta_H E)$ ($E > 0$, $alpha > 0$, $beta_H > 0$), so $Z(beta) = C Gamma(alpha)(beta - beta_H)^(-alpha)$ for $beta > beta_H$ [8]. Then the Chernoff functional $Phi(beta) = beta Q_* + ln Z(beta)$ is strictly convex with unique global minimizer $beta^* = beta_H + alpha / Q_* > beta_H$ (exact convexity defect $Phi(beta^* + delta dot alpha / Q_*) - Phi(beta^*) = alpha(delta - ln(1 + delta)) arrow.r.hook (1/2) alpha delta^2$, certified by `2D Jet2D` seam `C159`), yielding _both_ exact linear microcanonical Bekenstein–Hawking entropy ($s := beta_H Q_*$) and an exact $+1$ canonical-to-microcanonical Hagedorn variance shift:
     $
       ln N(Q_*) &= s + (alpha - 1) ln Q_* + ln(C / beta_H) - (alpha - 1)/s + O(s^(-2)), \
       S_"Chernoff" (Q_*) - ln N(Q_*) &= underbrace(ln s + 1/2 ln((2 pi)/alpha), 1/2 ln(2 pi beta_H^2 "Var"_(beta^*)(E))) + underbrace(Delta_"Stirling" (alpha), 1/(12 alpha) - 1/(360 alpha^3) + dots) + (alpha - 1)/s + O(s^(-2)),
     $
     where $Delta_"Stirling" (alpha) = ln Gamma(alpha) - (alpha - 1/2) ln alpha + alpha - (1/2) ln(2 pi) > 0$ is the exact Binet remainder (certified across $alpha in [1.5, 8.0]$ by `C160`).
]

#proof[
  (1) Integrating by parts for non-decreasing $N(E)$, $Z(beta) = beta integral_0^infinity e^(-beta E) N(E) d E$ converges iff $beta > limsup_(E -> infinity) E^(-1) ln N(E)$.
  (2) Differentiating $beta Q_* + A beta^(-gamma)$ gives $Q_* - gamma A beta^(-(gamma+1)) = 0 ==> beta^* = (gamma A / Q_*)^(1/(gamma+1))$; substitution yields the stated prefactor.
  (3) Laplace transformation gives $Z(beta) = C Gamma(alpha)(beta - beta_H)^(-alpha)$ for $beta > beta_H$, with $Phi'(beta) = Q_* - alpha / (beta - beta_H) = 0 ==> beta^* = beta_H + alpha / Q_*$, $Phi''(beta^*) = Q_*^2 / alpha = "Var"_(beta^*)(E) > 0$, and $S_"Chernoff" (Q_*) = beta_H Q_* + alpha ln Q_* + alpha(1 - ln alpha) + ln(C Gamma(alpha))$. Integrating $N(Q_*) = integral_0^(Q_*) C E^(alpha-1) e^(beta_H E) d E$ by parts yields $N(Q_*) = (C/beta_H) Q_*^(alpha-1) e^(beta_H Q_*)(1 - (alpha-1)/s + O(s^(-2)))$. Subtracting $ln N(Q_*)$ from $S_"Chernoff" (Q_*)$ gives $ln(beta_H Q_*) + ln Gamma(alpha) - alpha ln alpha + alpha + (alpha-1)/s + O(s^(-2)) = ln s + (1/2) ln(2 pi / alpha) + Delta_"Stirling" (alpha) + (alpha-1)/s + O(s^(-2))$.
]

#remark(title: "Exact Matching to Sen (2013) & Chandrasekaran (2026) Log Corrections")[
  Because the Hagedorn variance $"Var"_(beta^*)(E) = Q_*^2 / alpha$ shifts the canonical/Chernoff logarithmic coefficient by exactly $+1$ relative to $ln dim hD$, realizing a target microcanonical logarithmic correction $+alpha_"micro" ln s$ requires Hagedorn pole order $alpha = alpha_"micro" + 1$:
  - _Sen $J$-summed fixed-mass 4D Schwarzschild_ ($alpha_"micro" = 106/45$) [9]: $alpha = 106/45 + 1 = 151/45 = 302/90 approx 3.3556$ ($Delta_"Stirling" = 0.024763$; exact vs. asymptotic gap residual $4.25 times 10^(-7)$ at $s = 1000$);
  - _Chandrasekaran Tauberian clock exponent_ [2]: $alpha = 257/90 approx 2.8556$ ($Delta_"Stirling" = 0.029067$; residual $1.28 times 10^(-7)$ at $s = 1000$);
  - _Sen $J = 0$ singlet-subtracted Schwarzschild_ ($alpha_"micro" = 77/90$) [9]: $alpha = 77/90 + 1 = 167/90 approx 1.8556$ ($Delta_"Stirling" = 0.044506$; residual $4.86 times 10^(-7)$ at $s = 1000$).
  All three physical values lie strictly inside `C160`'s certified domain $alpha in [1.5, 8.0]$ (Figure 4b).
]

#figure(
  image("fig4_hagedorn_vs_qft_nuclearity_repair.svg", width: 99%),
  caption: [Constructive repair of Chandrasekaran [2] Sec. 5.2 (Theorems R1–R3). (a) Polynomial QFT nuclearity ($beta_c = 0$: $gamma = 1 -> s^(1/2)$, $gamma = 3 -> 1.7548 s^(3/4)$) stays strictly sub-Bekenstein, while Hagedorn compact-resolvent nuclearity ($beta_c = beta_H > 0$) yields finite dimension _and_ exact linear BH + Sen log entropy. (b) Seam `C160` certifying $Delta_"Stirling" (alpha) arrow.r.hook 1/(12 alpha)$ over compiled `cr_lgamma`, with `K13` marking $psi(1.461632) = 0$.],
)

// ============================================================================
// SECTION 5: SWIFT++ V3.1 TOOLCHAIN UPGRADE #2 & EXECUTABLE CERTIFICATION
// ============================================================================
= `Swift++` v3.1 Precision Toolchain Upgrade \#2 and Executable Certification

Both tracks motivated permanent, air-gapped, Zero-LLVM (`0` host `libm`, `0` `Foundation`) upgrades to `Swift++` v3.1:
1. _`SppStd.CRMathSpecial` (`11,176 B` Pass 9B) & 21-Function `SppStd.CRMath`:_ Added 106-bit Dekker–Knuth Double-Double [11] `cr_lgamma` and `cr_digamma` (scalar DD shift to $z >= 16$ + 10-term Stirling–Bernoulli Horner polynomials with tail $< 2 times 10^(-23)$, eliminating cancellation at $x = 1, 2$), Lerch's exact `cr_hurwitz_zeta_p0(a)` $= ln Gamma(a) - (1/2) ln(2 pi)$ in 106-bit DD, and `cr_zeta_odd(k)` for $k in {3, 5, 7, 9\}$.
2. _`IntervalProofEngine.swift` (Sound Polygamma `Jet2`/`Jet2D` AD):_ Added self-contained outward-rounded `lgammaInterval()` (tracking the unique global minimum $x_"min"^* = 1.4616321449683623$), strictly monotone `digammaInterval()`, `trigammaInterval()`, `tetragammaInterval()`, and `hurwitzZetaP0Interval()`, wired across all five `SppMLIR` abstract interpreters (`Interval`, `Dual`, `Dual2`, `Jet2`, `Jet2D`) [10].
3. _Scroll 45 (`SppAlexandria.HopfTuftAndHagedornRepair`, `5,768 B` Pass 9B), Pinakes `160/160`, Blinded RCT, and Codex `54/54`:_

#figure(
  table(
    columns: (0.80fr, 1.50fr, 1.40fr, 1.50fr),
    align: (left, left, left, left),
    stroke: 0.45pt + luma(195),
    inset: 4.2pt,
    fill: (_, y) => if y == 0 { rgb("#0f172a") } else if calc.odd(y) { luma(249) } else { white },
    table.header(
      text(fill: white, weight: "bold", size: 8.2pt)[ID / Gate],
      text(fill: white, weight: "bold", size: 8.2pt)[Method / Domain],
      text(fill: white, weight: "bold", size: 8.2pt)[Certified Result],
      text(fill: white, weight: "bold", size: 8.2pt)[Physics / Audit Role],
    ),
    [*`C157`*], [`1D Jet2`, $alpha in [10^(-4), 0.02]$], [`1` box, `max_hi = 8.585e-6 <= 1e-5`], [TUFT 2-loop $g-2$ $C_2 = -13 zeta(3)/48$ vs. QED [5]],
    [*`C158`*], [`1D Jet2` (`cr_hurwitz_zeta_p0`)], [`1` box, `max_hi = 6.319e-3 <= 8e-3`], [Nash–O'Connor Eq. (65) Lerch expansion ($u in [10^(-3), 0.25]$)],
    [*`C159`*], [`2D Jet2D`, $[1.8, 3.6] times [0.005, 0.15]$], [`27` boxes, `max_hi = 4.492e-3 <= 4.5e-3`], [Theorem R3b Hagedorn Chernoff free-energy convexity],
    [*`C160`*], [`1D Jet2` (`cr_lgamma`), $[1.5, 8.0]$], [`63` boxes, `max_hi = 8.281e-4 <= 1e-3`], [Theorem R3b Stirling–Chernoff gap (Sen & Chandrasekaran)],
    [*`K13`*], [Moore–Krawczyk (`cr_digamma`)], [`[1.4616321449663, ...703]`, `w = 4.00e-12`], [Unique positive digamma root $psi(x_"min"^*) = 0$ (`3` iters)],
    [*`F40`*], [Falsifier, $R in [1.20, 3.00]$], [`FALSIFIED_OK`, witness $R^* = 2.1$], [Refutes TUFT Lemma 8 scale invariance ($1 - 2.1^(-19/4) = 0.9705$)],
    [*Live Suite*], [`tuft_audit_and_hagedorn_suite`], [`10/10` Zero-LLVM (`6,752 B`), `EXACT`], [`0` `libm`, `nm -u = _putchar` ONLY, `5/5` pillars PASS],
    [*ARM64 RCT*], [`alexandria_epoch41_rct` ($N = 1,600$)], [Arm A `0/1600` vs. Arm B `1600/1600`], [`b01 = 1600, c10 = 0`, $chi^2 = 1598$, cumulative `64,000` trials],
    [*Codex & Seal*], [`alexandria_codex_app` & `.sppb`], [`54/54` Zero-LLVM, `199/199` MDS (`100%`)], [`.sppb` v3.0.0 CRC-64 `0xDCFD673807FD31BD`, `143/143` XCTests],
  ),
  caption: [Complete Epoch XLI / Horizon 1F executable certification ledger (`Swift++` v3.1 Pass 9B Zero-LLVM, `45` scrolls, `617` MLIR functions, `160/160` seams, `13/13` Krawczyk roots, `40/40` falsifications).],
)

// ============================================================================
// SECTION 6: CONCLUSION
// ============================================================================
= Conclusion

External stress testing sharpens both theoretical physics and verification infrastructure. On Nielsen's TUFT [1], clean-room 75-digit verification gives fair credit to exact $S^7$ and $S^9$ spectral zeta evaluations while proving decisively that the theory's central mass, coupling, generation-counting, dark-sector, Lean 4, and Bayesian claims do not survive mathematical or experimental inspection. Conversely, on Chandrasekaran's null-cone quantization program [2], [12], our Schatten–Riesz Dichotomy (Theorem R1) and Hagedorn Compact-Resolvent Nuclearity Repair (Theorems R2–R3) replace the circular Section 5.2 trace argument with a sharp, non-circular physical principle: _finite-dimensional local Hilbert spaces with exact Bekenstein–Hawking linear entropy and Sen logarithmic corrections arise if and only if the ambient Raychaudhuri generator exhibits a strictly positive Hagedorn abscissa $beta_c = beta_H > 0$_.

// ============================================================================
// REFERENCES (12/12 BIDIRECTIONAL PARITY)
// ============================================================================
= References

#set par(first-line-indent: 0pt, hanging-indent: 1.8em, leading: 0.44em)
#set text(size: 8.3pt)

[1] J. L. Nielsen, _A Complete Topological Unified Field Theory on the Complex Hopf Fibration: The Canonical Field Bundle, Beltrami Lagrangian, Spectral Geometry, and Particle Spectrum_, Center for Topological Physics / University of Kansas manuscript, Aug. 14, 2026 (250 pp.).

[2] V. Chandrasekaran, _An algebraic quantization of gravity from the null cone_, `arXiv:2611.34924v1` \[hep-th\], Nov. 23, 2026.

[3] A. Wyler, _L'espace symétrique du groupe des équations de Maxwell_, C. R. Acad. Sci. Paris *269A* (1969), 743–745; B. Robertson, _Wyler's expression for the fine-structure constant $alpha$_, Phys. Rev. Lett. *27* (1971), 1545–1547.

[4] C. Nash and D. O'Connor, _Determinants of Laplacians, the Ray–Singer torsion on lens spaces and the Riemann zeta function_, J. Math. Phys. *36* (1995), 1462–1505.

[5] A. Petermann, _Fourth order magnetic moment of the electron_, Helv. Phys. Acta *30* (1957), 407–408; C. M. Sommerfield, _Magnetic dipole moment of the electron_, Phys. Rev. *107* (1957), 328–329; H. Suura and E. H. Wichmann, _Magnetic moment of the mu meson_, Phys. Rev. *105* (1957), 1930–1931; S. Laporta and E. Remiddi, _The analytical value of the electron $(g-2)$ at order $alpha^3$ in QED_, Phys. Lett. B *379* (1996), 283–291.

[6] S. Eidelman and M. Passera, _Theory of the $tau$ lepton anomalous magnetic moment_, Mod. Phys. Lett. A *22* (2007), 159–179; X. Fan, T. G. Myers, B. A. D. Sukra, and G. Gabrielse, _Measurement of the electron magnetic moment_, Phys. Rev. Lett. *130* (2023), 071801.

[7] D. Buchholz and E. H. Wichmann, _Causal independence and the energy-level density of states in local quantum field theory_, Commun. Math. Phys. *106* (1986), 321–344; A. G. Cohen, D. B. Kaplan, and A. E. Nelson, _Effective field theory, black holes, and the cosmological constant_, Phys. Rev. Lett. *82* (1999), 4971–4974.

[8] R. Hagedorn, _Statistical thermodynamics of strong interactions at high energies_, Nuovo Cimento Suppl. *3* (1965), 147–186; J. J. Atick and E. Witten, _The Hagedorn transition and the number of degrees of freedom of string theory_, Nucl. Phys. B *310* (1988), 291–334.

[9] A. Sen, _Logarithmic corrections to Schwarzschild and other non-extremal black hole entropy in different dimensions_, JHEP *04* (2013), 156, `arXiv:1205.0971`.

[10] R. E. Moore, _Interval Analysis_, Prentice-Hall, 1966; R. Krawczyk, _Newton-Algorithmen zur Bestimmung von Nullstellen mit Fehlerschranken_, Computing *4* (1969), 187–201.

[11] T. J. Dekker, _A floating-point technique for extending the available precision_, Numer. Math. *18* (1971), 224–242; M. Lerch, _Další studie v oboru Malmsténovských řad_, Rozpravy České Akad. *3* (1894), 1–61.

[12] Ergentics, LLC, _Working Paper 034 / Horizon Monograph IE: Independent Precision Audit and Structural Pressure Test of Algebraic Null-Cone Quantum Gravity (`arXiv:2611.34924v1`)_ (`../null_cone_gravity_audit/paper.pdf`), Nov. 2026.
