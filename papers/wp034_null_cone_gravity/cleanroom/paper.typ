// Working Paper 034 / Horizon Series Monograph IE (Swift++ Library of Alexandria Epoch XL)
// Independent Precision Audit & Structural Pressure Test of V. Chandrasekaran (2026), arXiv:2611.34924v1
// Compile: typst compile paper.typ paper.pdf
// Copyright (c) 2026 Ergentics, LLC -- MIT License

#set document(
  title: "Independent Precision Audit and Structural Pressure Test of Algebraic Null-Cone Quantum Gravity (arXiv:2611.34924v1)",
  author: "Ergentics, LLC & Swift++ Library of Alexandria Verification Program",
)

#set page(
  paper: "us-letter",
  margin: (x: 0.74in, y: 0.68in),
  numbering: "1",
  number-align: center,
  header: context {
    if counter(page).get().first() > 1 {
      set text(size: 8.0pt, fill: luma(95), style: "italic")
      grid(
        columns: (1fr, auto),
        [Precision Audit of Null-Cone Quantum Gravity (arXiv:2611.34924v1)],
        [Ergentics Working Paper 034 · Horizon Monograph IE],
      )
      v(-6pt)
      line(length: 100%, stroke: 0.4pt + luma(180))
    }
  },
)

#set text(
  font: "New Computer Modern",
  size: 9.4pt,
  lang: "en",
)

#set par(
  justify: true,
  leading: 0.50em,
  first-line-indent: 1.2em,
)

#set heading(numbering: "1.1")
#show heading.where(level: 1): it => {
  v(9.5pt, weak: true)
  set text(size: 11.2pt, weight: "bold", fill: rgb("#0f172a"))
  block(breakable: false)[#it]
  v(3pt, weak: true)
}
#show heading.where(level: 2): it => {
  v(7.5pt, weak: true)
  set text(size: 10.0pt, weight: "bold", fill: rgb("#1e293b"))
  block(breakable: false)[#it]
  v(2.5pt, weak: true)
}

#show table: set par(justify: false)
#show raw.where(block: false): it => if it.text == "Swift++" { box(it) } else { it }
#show figure.caption: it => {
  set text(size: 8.3pt, fill: luma(55))
  set par(leading: 0.47em, justify: true)
  it
}

#let varepsilon = sym.epsilon.alt
#let thm-cnt = counter("thm")

#let env-box(kind, accent, title: none, body) = {
  thm-cnt.step()
  v(4pt, weak: true)
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
  v(4pt, weak: true)
}

#let theorem(title: none, body) = env-box("Theorem", rgb("#1e3a8a"), title: title, body)
#let proposition(title: none, body) = env-box("Proposition", rgb("#0f766e"), title: title, body)
#let counterexample(title: none, body) = env-box("Counterexample", rgb("#b91c1c"), title: title, body)
#let remark(title: none, body) = {
  thm-cnt.step()
  v(4pt, weak: true)
  block(
    width: 100%,
    inset: (left: 10pt, right: 8pt, top: 5pt, bottom: 5pt),
    stroke: (left: 1.8pt + luma(120)),
    fill: luma(251),
    radius: (right: 3pt),
    breakable: false,
  )[
    #set par(first-line-indent: 0pt)
    #text(weight: "bold", fill: luma(45))[Remark #context thm-cnt.display("1")#if title != none [ (#title)].] #body
  ]
  v(4pt, weak: true)
}

// ============================================================================
// TITLE BLOCK
// ============================================================================
#align(center)[
  #text(size: 8.5pt, weight: "bold", fill: rgb("#1e40af"), tracking: 0.08em)[
    ERGENTICS WORKING PAPER 034 · HORIZON MONOGRAPH IE · SWIFT++ LIBRARY OF ALEXANDRIA EPOCH XL
  ]
  #v(5pt)
  #text(size: 15.0pt, weight: "bold", fill: rgb("#0f172a"))[
    Independent Precision Audit and Structural Pressure Test of Algebraic Null-Cone Quantum Gravity (`arXiv:2611.34924v1`)
  ]
  #v(4pt)
  #text(size: 10.2pt, style: "italic", fill: luma(65))[
    Non-Analytic Dilogarithm Anomalies, Cycle-Rearrangement Counterexamples, Macroscopic Horizon-Area Dispersion, and `Swift++` v3.1 Special-Function & 106-Bit EFT Toolchain Certification
  ]
  #v(7pt)
  #text(size: 9.4pt, weight: "bold")[Ergentics, LLC · Swift++ Library of Alexandria Verification Program] \
  #text(size: 8.6pt, fill: luma(85))[Target Preprint: V. Chandrasekaran (Stanford University), *An algebraic quantization of gravity from the null cone*, `arXiv:2611.34924v1` (Nov. 23, 2026)] \
  #text(size: 8.5pt, fill: luma(95))[November 26, 2026 · Zero-Dependency Air-Gapped Three-Way `[X]` Audit · MIT License]
]

#v(6pt)
#block(
  width: 100%,
  inset: (x: 12pt, y: 8pt),
  fill: rgb("#f8fafc"),
  stroke: 0.6pt + rgb("#cbd5e1"),
  radius: 3pt,
)[
  #set par(first-line-indent: 0pt, leading: 0.49em)
  #text(size: 8.9pt)[
    *Abstract.* We perform a clean-room Three-Way `[X]` forensic pressure test and precision audit of Venkatesa Chandrasekaran's recent proposal for a background-independent algebraic quantization of four-dimensional Lorentzian general relativity from intersecting null cones (`arXiv:2611.34924v1`). Every closed-form analytical identity, asymptotic expansion, thermodynamic coefficient, and operator-theoretic proof step is verified independently across (i) 65-digit arbitrary-precision `Decimal`/exact-rational Python scripts, (ii) newly upgraded `Swift++` v3.1 Zero-LLVM Pass 9B ARM64 special-function (`SppStd.CRMathSpecial`: sub-1-ULP Clausen $op("Cl")_2(theta)$ and unit-circle dilogarithm $op("Li")_2(e^(-i theta))$) and 106-bit Double-Double EFT kernels, and (iii) outward-rounded `SppMLIR` 1D/2D Taylor-Model (`Jet2`/`Jet2D`), `ComplexIntervalF64`, Moore–Krawczyk (`K12`), and mechanical falsification (`F39`) proofs. Our audit cleanly separates exact, sharp analytical constructions from five substantive defects. *Verified:* Eq. (4.35)'s exact dilogarithm sum, the JT $op("AdS")_2$ clock's strict monotonicity (`C154`), the $op("SL")(2, RR) \/ op("SO")(2)$ supermetric, the kinematic boost correlator ratio $1 - tanh^2(eta\/2)$, the ER=EPR horizon integral, the exact Cauchy–Schlömilch resolution of identity, the exact algebraic match to Sen's (2013) fixed-mass angular-momentum-summed Schwarzschild coefficient $+106\/45$ ($q = 257\/302$), and Appendix D.3's localized-patch Raychaudhuri–Hölder bound (`C156`). *Caught:* (1) a fatal operator-theoretic *petitio principii* in Section 5.2's finite-dimensionality and AdS energy-spectrum proofs, refuted by an explicit infinite-dimensional counterexample $cal(H) = ell^2(NN) plus.o ell^2(NN)$ (`F39`) where paired exhaustion drives $Z_P [X] arrow +infinity$ while Chandrasekaran's cycle exhaustion drives $Z_P [X] arrow -infinity$; (2) an unreported non-analytic real $O(G_N^3)$ term $-pi \/ (2 s^3)$ in Eq. (4.35) that suffers 100% catastrophic cancellation in IEEE-754 `binary64` at $s >= 10^(17)$ (resolved to $< 10^(-15)$ by our 106-bit DD EFT upgrade) alongside a UV-finiteness critique vs. Goroff–Sagnotti; (3) an $O(1)$ macroscopic horizon-area dispersion $sigma_A \/ chevron.l A chevron.r = 26.86\%$ in Section 5.3's clock-projected ensemble that locks $x^* = sqrt(257\/347) = 0.8606$ and creates a permanent $1.1164\%$ Jensen gap (`C155`); (4) an unverified Euclidean heat-kernel / zero-mode import; and (5) a $s^(3\/4)$ vs. $s^1$ sub-Bekenstein microstate gap in Appendix D.3 (where we tighten the optimal $beta^*$ prefactor by $2.675 times$). All proofs and executables are sealed in Alexandria Scroll 44 (`NullConeQuantization.spp`, `156/156` Pinakes seams, `12/12` Krawczyk, `39/39` falsifications, `53/53` Living Codex `195/195 = 100.0%` Deep MDS, `62,400` blinded RCT trials, `142/142` XCTests).
  ]
]

= Introduction and Executive Audit Scorecard

Venkatesa Chandrasekaran's preprint *"An algebraic quantization of gravity from the null cone"* (`arXiv:2611.34924v1`, Nov. 23, 2026) [1] proposes a remarkably ambitious Lorentzian quantization of four-dimensional vacuum Einstein gravity ($G_(a b) + Lambda g_(a b) = 0$) formulated directly on the reduced phase space of intersecting past and future null cones bounding a causal diamond $cal(D)$. Starting from first-order Plebański–BF variables, the paper solves the constraints along null generators, defines a gravitational clock operator $hat(overline(u))_*$ from the Raychaudhuri focusing integral, builds a Type I GNS Hilbert space from Gaussian fixed-area states, and advances three headline claims: (i) nonperturbative UV finiteness of graviton pair amplitudes on a null cone, (ii) a proof that the clock-projected causal diamond Hilbert space $cal(H)_D = P_D cal(H)_omega$ is finite-dimensional (implying a discrete area spectrum and finite AdS thermal trace), and (iii) a Lorentzian recovery of Bekenstein–Hawking entropy and Ashoke Sen's (2013) one-loop logarithmic correction $+106\/45 ln s_b$ for large Schwarzschild black holes [2].

Because `arXiv:2611.34924v1` explicitly notes extensive AI-assisted derivation ($approx 400$M tokens) and sits at the frontier of mathematical quantum gravity, it is an ideal external stress test for the `Swift++` Library of Alexandria verification architecture. Crucially, testing Eq. (4.35)'s oscillatory complex polylogarithm at macroscopic horizon areas ($s = A \/ (4 G_N ℏ) >= 10^(16)$) revealed a genuine capability gap in IEEE-754 `binary64` and in our prior `SppStd.CRMath` v1.0 library. We therefore upgraded the `Swift++` toolchain to *v3.1* (Section 6), adding sub-1-ULP Zero-LLVM special functions (`cr_clausen2`, `cr_dilog_unit_re`, `cr_dilog_unit_im`), 106-bit Double-Double EFT scalar/anomaly kernels, and sound `ComplexIntervalF64` + analytical `Jet2`/`Jet2D` Clausen abstract interpretation inside `IntervalProofEngine.swift`.

Table 1 summarizes our complete referee verdict across every quantitative and structural pillar of Chandrasekaran (2026), distinguishing rigorously verified identities from five substantive mathematical, numerical, and physical catches.

#figure(
  table(
    columns: (0.9fr, 1.55fr, 0.8fr, 2.25fr),
    inset: 4.5pt,
    align: (left, left, center, left),
    stroke: 0.45pt + luma(180),
    fill: (_, row) => if row == 0 { rgb("#0f172a") } else if calc.odd(row) { rgb("#f8fafc") } else { white },
    table.header(
      text(fill: white, weight: "bold", size: 8.2pt)[Paper Section],
      text(fill: white, weight: "bold", size: 8.2pt)[Claim / Equation Audited],
      text(fill: white, weight: "bold", size: 8.2pt)[Verdict],
      text(fill: white, weight: "bold", size: 8.2pt)[Clean-Room `[X]` & `Swift++` v3.1 Finding],
    ),
    text(size: 8.1pt)[Sec. 2.1 Eq. (2.5)],
    text(size: 8.1pt)[JT $op("AdS")_2$ clock $u_* (w)$ strict monotonicity],
    text(size: 8.0pt, weight: "bold", fill: rgb("#047857"))[VERIFIED (`C154`)],
    text(size: 8.1pt)[Exact; $f'_varepsilon (z) > (1 - varepsilon) op("sech")^2 (varepsilon z) > 0$; 2D `Jet2D` proved to $4.996 times 10^(-4)$.],
    text(size: 8.1pt)[Sec. 4.3 Eq. (4.20)],
    text(size: 8.1pt)[Conformal supermetric $g_(alpha beta) = op("diag")(1, e^(2 z^1))$],
    text(size: 8.0pt, weight: "bold", fill: rgb("#047857"))[VERIFIED],
    text(size: 8.1pt)[Exact $op("SL")(2, RR)\/op("SO")(2)$ hyperbolic metric; $det overline(q) = 1$, error $< 10^(-15)$.],
    text(size: 8.1pt)[Sec. 4.4 Eqs. (4.35–36)],
    text(size: 8.1pt)[Graviton pair $op("Li")_2(e^(-2i\/s))\/(2s^2)$ & UV cure],
    text(size: 8.0pt, weight: "bold", fill: rgb("#b45309"))[PARTIAL / CATCH 2],
    text(size: 8.1pt)[Sum exact (`C153`, `K12` $theta^* = 1.3278$), but misses real $-pi\/(2s^3)$ cusp (`f64` wipes out at $s >= 10^(17)$) & $sum k^(-2)$ is already UV-convergent.],
    text(size: 8.1pt)[Sec. 5.2 Eq. (5.20)],
    text(size: 8.1pt)[Boost ratio $4 e^eta \/ (1 + e^eta)^2 = 1 - tanh^2(eta\/2)$],
    text(size: 8.0pt, weight: "bold", fill: rgb("#047857"))[VERIFIED],
    text(size: 8.1pt)[Exact kinematic ratio & bounded-observable variance bound (`Eq. (5.24)`).],
    text(size: 8.1pt)[Sec. 5.2 Eqs. (5.30, 5.37)],
    text(size: 8.1pt)[Cycle proof of $dim cal(H)_D < infinity$ & AdS $Z_beta < infinity$],
    text(size: 8.0pt, weight: "bold", fill: rgb("#b91c1c"))[REFUTED (`F39`)],
    text(size: 8.1pt)[*Fatal gap (petitio principii):* Explicit $cal(H) = ell^2(NN) plus.o ell^2(NN)$ gives $Z_(P^"pair")[X] arrow +infinity$ vs. $Z_(P^"cyc")[X] arrow -infinity$ (`F39` witness $= 1.50$).],
    text(size: 8.1pt)[Sec. 5.3 Eqs. (5.40–47)],
    text(size: 8.1pt)[Schwarzschild Sen $+106\/45$ & Cauchy–Schlömilch],
    text(size: 8.0pt, weight: "bold", fill: rgb("#b45309"))[PARTIAL / CATCH 3–4],
    text(size: 8.1pt)[Identities & Sen $+106\/45$ exact ($q = 257\/302$), *but* $x^* = 0.8606$ is locked, $sigma_A\/chevron.l A chevron.r = 26.86\%$ (`C155` Jensen gap $1.12\%$), Euclidean $a_4$ imported.],
    text(size: 8.1pt)[Sec. 5.4 Eq. (5.48)],
    text(size: 8.1pt)[ER=EPR horizon correlator Mellin integral],
    text(size: 8.0pt, weight: "bold", fill: rgb("#047857"))[VERIFIED],
    text(size: 8.1pt)[Exact $-c_perp \/ (u_L + u_R)^2$; 10,000-pt & Pass 9B quadrature error $1.8 times 10^(-15)$.],
    text(size: 8.1pt)[App. D.3 Eqs. (D.28–36)],
    text(size: 8.1pt)[Patch Hölder bound & $log d(s) lt.tilde (s Q_*)^(3\/4)$],
    text(size: 8.0pt, weight: "bold", fill: rgb("#b45309"))[VERIFIED / CATCH 5],
    text(size: 8.1pt)[Patch bound sharp (`C156`: $e^(-u)\/(1-u) arrow 1 + u^2\/2$); we tighten $s^(3\/4)$ prefactor $2.675 times$ ($2.8012$) & flag $s^(3\/4) << s^1$ microstate gap.],
  ),
  caption: [Executive clean-room `[X]` audit scorecard of Chandrasekaran (2026), `arXiv:2611.34924v1`, verified across 65-digit Python, Pass 9B ARM64 (`NullConeQuantization.spp`), and outward-rounded `SppMLIR` `Jet2`/`Jet2D`/Krawczyk/Falsification proofs.],
)

= Pillar 1: Graviton Pair Amplitude, Non-Analytic Real Anomaly, and Precision Failure

In Section 4.4 (`Eqs. (4.35)–(4.36)`), Chandrasekaran evaluates the connected two-point function of quadratic radial graviton insertions with Gaussian variance $(Delta q_k)^2 = 1 \/ (2 s k)$ (where $s = A \/ (4 G_N ℏ)$) and relative phase $e^(-2 i k \/ s)$:
$ A(s) = lim_(N arrow infinity) 2 sum_(k=1)^N (Delta q_k)^4 e^(-2 i k \/ s) = (op("Li")_2 (e^(-2 i \/ s))) / (2 s^2). $

== Exact Bernoulli–Clausen Decomposition and the Unreported Real $O(s^(-3))$ Anomaly

For any phase $theta = 2\/s in (0, 2 pi)$, the unit-circle dilogarithm splits exactly into a degree-2 Bernoulli polynomial real part and the Clausen function $op("Cl")_2 (theta) = sum_(k=1)^infinity sin(k theta) \/ k^2$:
$ op("Re") op("Li")_2 (e^(-i theta)) = pi^2 / 6 - (theta (2 pi - theta)) / 4 = ((theta - pi)^2) / 4 - pi^2 / 12, $
$ op("Im") op("Li")_2 (e^(-i theta)) = -op("Cl")_2 (theta) = theta ln theta - theta - sum_(m=1)^infinity (abs(B_(2 m))) / (2 m (2 m + 1)!) theta^(2 m + 1). $

#proposition(title: "Unreported Real Non-Analytic Anomaly and K12 Sign-Change Root")[
  For every $s > 1\/pi$ ($theta = 2\/s in (0, 2 pi)$), the real part of Eq. (4.35) is the exact rational-in-$s$ polynomial
  $ op("Re") A(s) = pi^2 / (12 s^2) - pi / (2 s^3) + 1 / (2 s^4), $
  whereas formal term-by-term expansion of $(2 s^2)^(-1) sum_(k=1)^N cos(2 k\/s)\/k^2$ in powers of $G_N prop 1\/s$ yields identically zero at every odd order $O(s^(-(2j+1)))$. Thus, resummation generates an unreported real non-analytic cusp term $-pi\/(2 s^3)$ (magnitude $pi\/2 approx 1.5708$, exceeding the constant imaginary offset $abs(ln 2 - 1) approx 0.3069$ by $5.12 times$) alongside the imaginary $-i ln(s)\/s^3$ term reported in Eq. (4.36). Moreover, $op("Re") A(s)$ changes sign at a unique critical threshold certified by Moore–Krawczyk certificate `K12`:
  $ theta^* = pi (1 - 1 / sqrt(3)) = 1.3277932893555754..., quad s^* = 2 / theta^* = 1.5062585539731641... $
]

*Referee Critique on Perturbative UV Finiteness vs. Goroff–Sagnotti.* Chandrasekaran [1] motivates Eq. (4.35) by citing the two-loop $R^3$ UV divergence of four-dimensional pure gravity (Goroff & Sagnotti 1986) [3]. However, at $G_N arrow 0^+$ ($s arrow infinity$), the pair amplitude $2 sum_(k=1)^infinity (Delta q_k)^4 = pi^2 \/ (12 s^2)$ is *already absolutely UV-convergent* before inserting any phase factor. The logarithmic divergence $-i s^(-3) sum_(k=1)^N k^(-1) = -i s^(-3) [ln N + O(1)]$ in Eq. (4.36) is produced solely by inserting a $1\/s$-scaled phase $e^(-2 i k\/s)$ into an already-convergent $sum k^(-2)$ series and differentiating three times at $G_N = 0$, where $op("Li")_2(e^(-2 i \/ s))$ has a branch-point cusp. This demonstrates non-commutativity of $lim_(N arrow infinity)$ and $partial_(G_N)^3|_(0^+)$ for a unitary-phase toy model, *not* a resolution of derivative-vertex loop divergences in 4D Einstein–Hilbert perturbation theory.

== Catastrophic IEEE-754 `binary64` Wipeout vs. `Swift++` v3.1 106-Bit DD EFT

Extracting the non-analytic real anomaly $Delta_"re" (s) := s^3 (op("Re") A(s) - pi^2 \/ (12 s^2)) = -pi\/2 + 1\/(2 s)$ numerically exposes two distinct precision failures (Figure 1):
1. *Direct partial summation failure:* Truncating $sum_(k=1)^N e^(-2 i k \/ s)\/(2 s^2 k^2)$ requires $N >> s$ terms; at $s = 10^6, N = 10^5$, the extracted real anomaly is $-5.0999$ vs. exact $-1.5708$ ($224.7\%$ relative error), while the scaled imaginary part gives $-12.0868$ vs. $-14.1224$ ($14.4\%$ error).
2. *IEEE-754 `binary64` catastrophic cancellation:* Even using the closed-form formula $pi^2\/6 - theta(2 pi - theta)\/4$, subtracting $pi^2\/6$ in 53-bit `f64` destroys half the mantissa bits by $s = 10^8$, produces a 1-ULP quantization artifact ($-1.1102$, $29.3\%$ error) at $s = 10^(16)$, and collapses to exact `0.0000` ($100\%$ total signal wipeout) for all $s >= 10^(17)$ (still 60 orders of magnitude below a solar-mass black hole $s approx 10^(77)$!). Our upgraded `Swift++` v3.1 kernel `spp_p7s_dd_pair_re_anomaly` performs the subtraction in 106-bit Dekker–Knuth Double-Double EFT, recovering $-1.5707963267948966$ to $< 10^(-15)$ at $s = 10^(17)$ and beyond.

#figure(
  image("figures/fig1_dilog_clausen_anomaly.svg", width: 96%),
  caption: [*Pillar 1 (`C153`, `K12`).* (A) Exact unit-circle dilogarithm real part $op("Re") op("Li")_2 (e^(-i theta))$ with unique Moore–Krawczyk sign-change root `K12` at $theta^* = 1.3278$ and Clausen imaginary part $op("Cl")_2 (theta)$ peaking at Gieseking's constant $1.01494$. (B) Relative error extracting the unreported real $O(s^(-3))$ anomaly $-pi\/2$: naive partial sums diverge past $s > 10^3$, IEEE-754 `binary64` suffers 100% wipeout at $s >= 10^(17)$, while `Swift++` v3.1 106-bit Double-Double EFT remains exact to $< 10^(-15)$ through $s = 10^(20)$.],
)

= Pillar 2: Refutation of the Section 5.2 Cycle-Rearrangement Proof (`F39`)

Section 5.2 of Chandrasekaran (2026) presents the paper's most consequential theorem: a claimed proof that the clock-projected causal diamond Hilbert space $cal(H)_D = P_D cal(H)_omega$ is finite-dimensional, from which a discrete area spectrum and a finite reflecting-AdS thermal partition function $Z_beta < infinity$ are deduced.

*Structure of the Paper's Argument.* Using Raychaudhuri focusing ($0 <= hat(s) <= s_*$) and a positive continuous Gaussian weight $f_b (hat(s))$ (`Eq. (5.22)`), the gluing operator $C_b = C_D f_b (hat(s))^(1\/2)$ satisfies the uniform two-sided bound
$ e^(-s_*) m_(b, D) hat(1) <= C_b^dagger C_b <= hat(1), quad m_(b, D) := min_(0 <= s <= s_*) f_b (s) > 0. $
For any finite-rank orthogonal projection $P = sum_(i in S_P) |i chevron.r chevron.l i|$, Eq. (5.23) defines the open-cut unnormalized expectation $Z_P [X] = chevron.l tilde(Psi)_P | X | tilde(Psi)_P chevron.r$, where $|tilde(Psi)_P chevron.r = sum_(i in S_P) C_b |i chevron.r times.o |i^* chevron.r$ has squared norm $op("Tr")(P C_b^dagger C_b)$, and $X = Delta_eta hat(cal(O)) - (delta_eta \/ 2) hat(1)$ measures the boost deformation of a bounded graviton observable ($norm(hat(cal(O))) <= 1$, $delta_eta > 0$). Eq. (5.24) rigorously bounds the boost change by the area variance:
$ abs(chevron.l hat(cal(O)) chevron.r_(eta, P) - chevron.l hat(cal(O)) chevron.r_(0, P)) <= (abs(eta)) / pi norm(hat(cal(O))) sqrt(op("Tr")[rho_P (hat(s) - s_0)^2]). $
Assuming for contradiction that $dim cal(H)_D = infinity$, Chandrasekaran partitions $[0, s_*]$ into intervals of width $<= Delta s$, picks one interval $I$ with $dim(bold(1)_I (hat(s)) cal(H)_D) = dim cal(H)_D$, and groups each basis vector outside $I$ with $r - 1$ basis vectors inside $I$ into cycles of length $r$. For every finite union of complete cycles $P$, choosing $Delta s$ small and $r$ large makes $abs(chevron.l Delta_eta hat(cal(O)) chevron.r_P) <= delta_eta \/ 2$, hence $Z_P [X] <= 0 < Z[X]$ (`Eq. (5.30)`). Because every basis vector belongs to some cycle ($P arrow.t hat(1)$ strongly), Eq. (5.30) is declared contradictory to sewing (`Eq. (1.1)`), concluding $dim cal(H)_D < infinity$.

#counterexample(title: "Explicit Infinite-Dimensional Refutation of Section 5.2 (F39)")[
  Let $cal(H) = cal(H)_0 plus.o cal(H)_1$ with $cal(H)_0 = cal(H)_1 = ell^2 (NN)$ (infinite-dimensional), equipped with orthonormal bases ${|0_n chevron.r}_(n >= 1)$ and ${|1_n chevron.r}_(n >= 1)$. Define the bounded self-adjoint area operator $hat(s) |0_n chevron.r = 0$ and $hat(s) |1_n chevron.r = s_* |1_n chevron.r$ with $s_* = pi^2$, and set $C_b = e^(-hat(s)\/2)$ so that $e^(-s_*) hat(1) <= C_b^dagger C_b <= hat(1)$ holds identically ($m_(b, D) = 1$). On $cal(H) times.o cal(H)^*$, define the bounded self-adjoint observable ($norm(hat(cal(O))) = 1$)
  $ hat(cal(O)) = - sum_(n=1)^infinity (|0_n, 0_n^* chevron.r chevron.l 1_n, 1_n^*| + |1_n, 1_n^* chevron.r chevron.l 0_n, 0_n^*|). $
  Under the relative boost $U_eta = hat(1) times.o e^(i eta hat(s)^* \/ (2 pi))$ at rapidity $eta = 2 pi^2 \/ s_* = 2$, $U_eta |0_n, 0_n^* chevron.r = |0_n, 0_n^* chevron.r$ and $U_eta |1_n, 1_n^* chevron.r = -|1_n, 1_n^* chevron.r$, so $Delta_eta hat(cal(O)) = U_eta^dagger hat(cal(O)) U_eta - hat(cal(O)) = -2 hat(cal(O))$. Let $c := e^(-pi^2) approx 5.1723 times 10^(-5)$ and $delta_eta := 4 e^(-s_* \/ 2) \/ (1 + c) approx 2.8766 times 10^(-2) > 0$. Then two exhaustions of the *same* infinite-dimensional space $cal(H)$ both converge strongly to $hat(1)$ yet drive $Z_P [X]$ to opposite infinities:
  1. *Natural paired exhaustion* $P_M^"pair" = sum_(n=1)^M (|0_n chevron.r chevron.l 0_n| + |1_n chevron.r chevron.l 1_n|) arrow.t hat(1)$:
     $ chevron.l Delta_eta hat(cal(O)) chevron.r_(P_M^"pair") = delta_eta, quad Z_(P_M^"pair") [X] = + 1 / 2 delta_eta M (1 + c) arrow +infinity quad (M = 10^4 => +143.8377). $
  2. *Chandrasekaran cycle exhaustion* $P_M^"cyc" arrow.t hat(1)$ (each cycle pairs one $|1_m chevron.r$ with $r - 1$ vectors from $I = {0}$, for any $r >= 4$):
     $ (chevron.l Delta_eta hat(cal(O)) chevron.r_(P_M^"cyc")) / delta_eta <= (1 + c) / (r - 1 + c) < 1 / 2, quad Z_(P_M^"cyc") [X] <= - 1 / 2 delta_eta M (r - 3 - c) arrow -infinity quad (r = 5, M = 10^4 => -287.6530). $
]

*Root Cause (Petitio Principii).* Why did Section 4.4's Cauchy–Schwarz sewing bound (`Eq. (4.33)`) fail to prevent this rearrangement paradox? Section 4.4 proved absolute convergence of an *open* transition amplitude $sum_alpha chevron.l phi | U_2 | e_alpha chevron.r chevron.l e_alpha | U_1 | psi chevron.r$ between two *normalizable* states ($norm(phi), norm(psi) < infinity$). By contrast, Section 5.2 closes a *trace loop* $op("Tr")(C_b^dagger C_b dots)$. Because $C_b^dagger C_b >= e^(-s_*) m_(b, D) hat(1)$, whenever $dim cal(H)_D = infinity$ we automatically have $op("Tr")(C_b^dagger C_b) = +infinity$: $C_b$ is *not Hilbert–Schmidt*, the uncut vector $|tilde(Psi) chevron.r = sum_i C_b |i chevron.r times.o |i^* chevron.r$ does not exist in $cal(H)_D times.o cal(H)_D^*$, and the bilinear net $P arrow.bar Z_P [X]$ is rearrangement-dependent. This traps the proof in a strict logical dichotomy:
- If one *assumes* unconditional (rearrangement-invariant) convergence of the closed-cut trace $Z_P [hat(1)] = op("Tr")(P C_b^dagger C_b) arrow Z[hat(1)] < infinity$, then $dim cal(H)_D <= e^(s_*) m_(b, D)^(-1) Z[hat(1)] < infinity$ follows in *one elementary line* without any boost correlator or cycle permutation.
- If one does *not* assume $Z[hat(1)] < infinity$, then $Z_P [X] <= 0$ along a cycle net $P_M^"cyc"$ does *not* contradict $Z[X] > 0$ along another exhaustion, as Counterexample 2 proves.

*Cascade to the AdS Boundary Energy-Spectrum Proof (`Eqs. (5.37)–(5.39)`).* Immediately following Eq. (5.30), Chandrasekaran applies the exact same rearrangement move to the joint-cut sum $sum_((i, a) in F) w_i v_a [bold(1)_I (A_a) - p]$ (`Eq. (5.37)`) to conclude $Z_beta = sum_i w_i < infinity$ on a reflecting AdS boundary. For any divergent positive sequence ($w_i equiv 1$, $p = 0.4$), summing over the finite diamond index $a$ first yields $sum_i w_i dot 0 = 0$, while appending $M$ unmatched $(i, a_0)$ terms shifts the partial sum by $-p (1 - p) M = -240.0$ (at $M = 1000$) $arrow -infinity$. By Tonelli's theorem, forbidding such partial-sum shifts assumes *unconditional* convergence of the double series, which is equivalent to $2 p (1 - p) sum_i w_i < infinity <=> sum_i w_i < infinity$ — again begging the exact conclusion to be proved.

#figure(
  image("figures/fig2_cycle_counterexample_f39.svg", width: 96%),
  caption: [*Pillar 2 (`F39`).* (A) Divergent closed-cut amplitudes $Z_P [X]$ on the infinite-dimensional Hilbert space $cal(H) = ell^2(NN) plus.o ell^2(NN)$ satisfying all operator bounds of Eq. (5.22): paired exhaustion $P_M^"pair" arrow.t hat(1)$ diverges to $+infinity$, while Chandrasekaran's cycle exhaustion $P_M^"cyc" arrow.t hat(1)$ diverges to $-infinity$. (B) Cycle dilution ratio $(1 + c)\/(r - 1 + c)$ crossing the $1\/2$ sign-inversion boundary for all $r >= 4$; `F39` mechanically falsifies rearrangement invariance with witness $Delta_"rearr" (12) = 1.818 > 0.50$.],
)

= Pillar 3: Schwarzschild 1-Loop Entropy, Locked Clock Ratio, and 26.86% Area Dispersion

Section 5.3 evaluates the von Neumann entropy of $rho_D = P_D e^(-hat(s)) \/ Z_(D, 1)$ for a marginally trapped surface in a Schwarzschild background. Our clean-room audit verifies every *algebraic* identity in Section 5.3 with remarkable exactness while uncovering two major physical/interpretive catches.

== Verified Exact Identities and Sen (2013) Cross-Check

1. *Integrated clock trace & Tauberian moment identity (`Eqs. (5.36)–(5.40)`):* For $Z(ell) = sum_(overline(u)_(*, i) <= ell) e^(-s_i)$, the identity $u = u^2 \/ ell + integral_u^ell (u\/t)^2 d t$ is exact, and under power-law scaling $Z(ell) tilde C ell^beta$ with $beta = q\/(1 - q)$, the second-moment ratio $x^2 = chevron.l (hat(overline(u))_* \/ ell)^2 chevron.r_ell = beta \/ (beta + 2)$ satisfies $q = 2 x^2 \/ (1 + x^2)$ and $q \/ (2 (1 - q)) = x^2 \/ (1 - x^2)$ identically.
2. *Exact Cauchy–Schlömilch identity (`Eq. (5.44)`):* Setting $sigma_s^2 = 2 s_b$ in $f_b (s) = exp(-(s - s_b)^2 \/ (2 sigma_s^2))$ and substituting $u = sqrt(s_b)$ yields
   $ integral_0^infinity exp(-((s - s_b)^2) / (4 s_b)) (d s_b) / sqrt(4 pi s_b) = 1 / sqrt(pi) integral_0^infinity exp(-1 / 4 (u - s / u)^2) d u = 1 $
   *identically for every $s > 0$* (verified numerically to $2.55 times 10^(-15)$ at $s = 1000$).
3. *Sen (2013) arithmetic check (`Eqs. (5.45)–(5.47)`):* From the pure-gravity Ricci-flat Seeley–DeWitt coefficient $a_4 = (53 \/ (45 (4 pi)^2)) R_(a b c d) R^(a b c d)$ (Christensen & Duff 1980; Bastianelli, Bonezzi & Melis 2022) [4] and $integral_S R[q] d A = 8 pi$, the opening-angle variation produces $log op("Tr")(C_b^dagger C_b) = (106\/45) log s_b + O(1)$. The measure $(4 pi s_b)^(-1\/2) d s_b$ shifts the scaling power of $Z(ell) prop s_*^alpha$ to $alpha = 106\/45 + 1\/2 = 257\/90$, yielding $q = 257\/302$ and fixed-mass coefficient $q\/(2(1-q)) - 1\/2 = 106\/45$. Cross-checking Ashoke Sen (2013, JHEP 04 (2013) 156, `arXiv:1205.0971`) [2] confirms $C_"local" = 212\/45$ for $ln r_h$, i.e., $+106\/45 ln s_b$ when *summing over angular momenta* at fixed mass — exactly as stated in Chandrasekaran's text [1].

== Catch 3: Locked Ratio $x^*$ and $O(1)$ Macroscopic Horizon-Area Dispersion (`C155`)

#theorem(title: "Locked Clock Ratio, 26.86% Area Variance, and Permanent Jensen Gap (C155)")[
  Under the limiting area distribution $op("Pr")_(rho_D) (s_i <= a s_*) arrow a^alpha$ (`Eq. (5.41)`) with $alpha = q \/ (2 (1 - q)) = 257\/90$:
  1. The geometric ratio $x = (1 - varepsilon) r_h \/ ell(cal(D))$ (with $4 pi r_h^2 = chevron.l hat(A) chevron.r_ell$) is *not* a free observer-chosen parameter as suggested in `L1970`; it is rigidly locked by the 1-loop exponent to
     $ x^* = sqrt(alpha / (alpha + 1)) = sqrt(257 / 347) = 0.8606009562..., quad (ell(cal(D))) / ((1 - varepsilon) r_h) = sqrt(347 / 257) = 1.1619787229... $
  2. The horizon area in $rho_D$ is *not* sharply peaked around $chevron.l hat(A) chevron.r$ even as $r_h \/ ell_P arrow infinity$. Its relative RMS fluctuation remains permanently order-one:
     $ (sigma_A) / (chevron.l A chevron.r) = 1 / sqrt(alpha (alpha + 2)) = 90 / sqrt(112309) = 0.26855623... quad (26.86% "RMS"). $
  3. Consequently, strict concavity of $sqrt(A)$ creates a permanent $O(1)$ Jensen gap between $chevron.l sqrt(hat(A)) chevron.r$ and $sqrt(chevron.l hat(A) chevron.r)$ governed by `C155` ($delta := 1\/alpha = 90\/257$):
     $ q / x^* = sqrt(1 + delta) / (1 + delta / 2) = sqrt(89179) / 302 = 0.98883620... quad (1.1164% "permanent Jensen gap"). $
]

*Catch 4 (Euclidean Heat-Kernel Import & Singlet $J = 0$ Zero-Mode Scope).* In `Eq. (5.45)`, the paper evaluates the Lorentzian trace $log op("Tr")(C_b^dagger C_b)$ by importing the Euclidean heat-kernel coefficient $53\/45$ [4] and Fursaev–Patrushev–Solodukhin (2013) conical variation [5] without proving that the nonlocal reduced-phase-space measure $mu_0$ restricted by $P_D$ shares the exact same one-loop determinant. Furthermore, while the angular-momentum-summed coefficient $+106\/45$ matches Sen (2013) [2], restricting to the rotationally invariant $J = 0$ singlet sector in Sen (2013) subtracts $N_R = 3$ $op("SO")(3)$ zero modes ($-3 ln r_h = -(3\/2) ln s_b$, giving $+77\/90 ln s_b$); verifying how Kerr inward null-cone focusing affects $overline(u)_* <= ell(cal(D))$ when summing over $J$ at fixed $M$ remains unperformed in Section 5.3.

#figure(
  image("figures/fig3_schwarzschild_dispersion_tauberian.svg", width: 96%),
  caption: [*Pillar 3 (`C155`).* (A) Limiting horizon-area probability density $p(a) = alpha a^(alpha - 1)$ ($alpha = 257\/90$) of the clock-projected ensemble $rho_D$: despite matching Sen's $+106\/45$ fixed-mass coefficient after differentiating out the area integral, $rho_D$ itself exhibits a macroscopic $26.86\%$ RMS horizon-area spread independent of $r_h \/ ell_P$. (B) Permanent Jensen gap $1 - q\/x^* = 1 - sqrt(1+delta)\/(1+delta\/2)$ vs. `C155` leading quadratic $delta^2\/8$, locking $x^* = 0.8606$ and $q = 257\/302$ ($1.1164\%$ gap) at $delta = 90\/257$.],
)

= Pillars 4 & 5: JT Clock, ER=EPR Integral, and Appendix D.3 Focusing Bounds

== Verified Analytical Constructions (`C154`, Supermetric, and ER=EPR)

We independently verified three additional analytical pillars of `arXiv:2611.34924v1` to machine precision:
- *JT $op("AdS")_2$ Gravitational Clock (`Sec. 2.1 Eq. (2.5)`, `C154`):* Letting $z = w \/ (2 L_"AdS") > 0$ and $varepsilon in (0, 1)$, the normalized clock reading $f_varepsilon (z) = (sinh z - sinh(varepsilon z)) \/ cosh(varepsilon z)$ satisfies
  $ f'_varepsilon (z) = (cosh z cosh(varepsilon z) - varepsilon sinh z sinh(varepsilon z) - varepsilon) / (cosh^2(varepsilon z)) > (cosh((1 - varepsilon) z) - varepsilon) / (cosh^2(varepsilon z)) >= (1 - varepsilon) / (cosh^2(varepsilon z)) > 0, $
  proving strict monotonicity globally on $z > 0$, while 2D `Jet2D` certifies the small-width curvature expansion $f_varepsilon (z) \/ ((1 - varepsilon) z) = 1 + (1 + varepsilon - 2 varepsilon^2) z^2 \/ 6 + O(z^4)$ to $4.996 times 10^(-4)$ across $(z, varepsilon) in [0.02, 0.30] times [0.05, 0.40]$ (`C154`).
- *Conformal Supermetric (`Sec. 4.3 Eq. (4.20)`):* Direct symbolic/numerical evaluation confirms $det overline(q) = 1$ and $1\/2 op("Tr")(overline(q)^(-1) delta overline(q) overline(q)^(-1) delta' overline(q)) = delta z^1 delta' z^1 + e^(2 z^1) delta z^2 delta' z^2$ to $< 10^(-15)$.
- *ER=EPR Horizon Correlator Integral (`Sec. 5.4 Eq. (5.48)`):* Live 10,000-point quadrature (and Pass 9B ARM64 quadrature) confirms $-(u_L u_R)^(-1) integral_0^infinity nu cos(nu ln(u_L\/u_R)) \/ sinh(pi nu) d nu = -(u_L + u_R)^(-2)$ to $1.80 times 10^(-15)$ at $(u_L, u_R) = (0.3, 1.7)$.

== Catch 5: Appendix D.3 Localized-Patch Sharpness (`C156`) and Sub-Bekenstein $s^(3\/4)$ Gap

1. *Localized-Patch Raychaudhuri–Hölder Bound (`Eq. (D.36)`, `C156`):* Starting from $D(y)^2 = 8 (integral_varepsilon^1 (partial_v Xi_y \/ v)^(1\/2) d v)^2$ and applying Cauchy–Schwarz + Hölder on $P times [varepsilon, 1]$ gives $integral_P D(y)^2 d A <= (8 (1 - varepsilon) A_P \/ varepsilon) (R^t \/ t)$ with $R = A_* \/ A_P >= 1$. Minimizing $R^t \/ t$ over $t in (0, 1]$ yields the sharp optimum $t_"opt" = min(1, 1 \/ ln R)$, giving $e ln R$ for $R >= e$. Chandrasekaran's nonsingular choice $t = u := (1 + ln R)^(-1)$ avoids the $R arrow 1^+$ singularity while remaining provably within a tight factor certified by `C156`:
   $ (B_"paper" (R)) / (B_"sharp" (R)) = (e^(-u)) / (1 - u) = 1 + u^2 / 2 + O(u^3) quad (1.2131 "at" R = e, "falling to" 1.0024 "at" R = 10^6). $
2. *Sub-Bekenstein 1-Loop Graviton Counting & Optimal $beta^*$ Tightening (`Eqs. (D.28)–(D.31)`):* Given the Weyl counting bound $N(nu) <= C_varepsilon (s nu)^3$, exact Stieltjes integration of the bosonic partition sum gives
   $ -sum_i ln(1 - e^(-beta nu_i)) <= C_varepsilon s^3 (6 zeta(4)) / beta^3 = A_varepsilon (s / beta)^3, quad A_varepsilon := (pi^4 / 15) C_varepsilon approx 6.493939 C_varepsilon. $
   Optimizing $Phi(beta) = beta Q_* + A_varepsilon (s \/ beta)^3$ over $beta > 0$ yields $beta^* = (3 A_varepsilon)^(1\/4) (s^3 \/ Q_*)^(1\/4)$ and sharp bound
   $ log d(s) <= (4 / 3^(3\/4)) A_varepsilon^(1\/4) (s Q_*)^(3\/4) approx 2.801213 C_varepsilon^(1\/4) (s Q_*)^(3\/4), $
   tightening the paper's unoptimized $beta = (s^3 \/ Q_*)^(1\/4)$ prefactor $(1 + pi^4\/15 = 7.4939)$ by $2.6752 times$ (for $C_varepsilon = 1$). Physically, however, this 1-loop linearized graviton bound scales as $s^(3\/4)$ (the 3+1D QFT-in-a-box entropy before collapse; Cohen–Kaplan–Nelson 1999) [6], which is *strictly sub-Bekenstein* ($s^(3\/4) << s^1$ as $s arrow infinity$, Figure 4B). Thus, while Appendix D.3 provides a genuinely non-circular 1-loop argument that perturbative graviton modes remain finite in number at fixed $Q_*$, it does *not* account for the $O(s)$ Bekenstein–Hawking microstate degeneracy $dim(bold(1)_([0, a s_*]) cal(H)_D) = exp(a s_* + o(s_*))$ claimed in `Eq. (5.42)`.

#figure(
  image("figures/fig4_jt_focusing_subbekenstein.svg", width: 96%),
  caption: [*Pillar 5 (`C156`).* (A) Exact sharpness ratio $e^(-u)\/(1 - u)$ comparing Chandrasekaran's localized-patch Hölder bound $t = (1 + ln R)^(-1)$ against the global Hölder optimum $e ln R$ across $R in [e, 10^6]$ (`C156`). (B) Perturbative 1-loop graviton entropy bound $log d(s) <= 2.801 (s Q_*)^(3\/4)$ (optimal $beta^*$, $2.675 times$ tighter than unoptimized $7.494 s^(3\/4)$) contrasted against full Bekenstein–Hawking scaling $S = s$, highlighting the unaccounted $O(s)$ microstate gap.],
)

= `Swift++` v3.1 Toolchain Upgrade and Pinakes Epoch XL Certification

Auditing `arXiv:2611.34924v1` motivated three durable, zero-dependency upgrades to the `Swift++` compiler, stdlib, and formal prover — all strictly air-gapped (`dependencies: []`), zero `Foundation` in `epoch_c/Sources/`, zero host `libm`, and 100% Zero-LLVM Pass 9B compatible:

1. *`SppStd.CRMathSpecial` (`6,584 B` Pass 9B ARM64) & 17-Function `SppStd.CRMath`:* Implements true 106-bit Double-Double `spp_p7s_dd_log`, sub-1-ULP Clausen `cr_clausen2` ($max$ error `0.936 ULP` across 1,998 test points on $(0, 2 pi)$ via 16-term origin and 26-term $pi$-shifted Bernoulli series with DD argument reduction), exact unit-circle dilogarithm `cr_dilog_unit_re` / `cr_dilog_unit_im`, and 106-bit DD real-anomaly extractor `spp_p7s_dd_pair_re_anomaly`.
2. *Public 106-Bit Double-Double Scalar Primitives in `SppStd.EFT`:* Exports `eft_two_sum_lo`, `eft_two_prod_lo`, `eft_dd_add_hi/lo`, and `eft_dd_mul_hi/lo` over hardware ARM64 `FMADD` (`f_fma`).
3. *`IntervalProofEngine.swift` v3.1 (`ComplexIntervalF64` + Analytical Clausen `Jet2`/`Jet2D`):* Adds sound outward-rounded rectangular complex intervals `ComplexIntervalF64` (`unitDilog(theta:)`) plus exact analytical derivatives $op("Cl")'_2 (theta) = -ln(2 sin(theta\/2))$, $op("Cl")''_2 (theta) = -1\/2 cot(theta\/2)$ and zero-dependency real dilogarithm $((theta - pi)^2\/4 - pi^2\/12)$ across all five `SppMLIR` abstract interpreters (`Interval`, `Dual`, `Dual2`, `Jet2`, `Jet2D`).

Table 2 records the complete, cryptographically sealed Epoch XL certification standing (`NullConeQuantization.spp`, Scroll 44) across all six formal certificates, the live 5-pillar Pass 9B suite, the blinded $N = 1,600$ ARM64 RCT, and the Living Codex.

#figure(
  table(
    columns: (0.85fr, 1.35fr, 1.45fr, 1.85fr),
    inset: 4.5pt,
    align: (left, left, left, left),
    stroke: 0.45pt + luma(180),
    fill: (_, row) => if row == 0 { rgb("#0f172a") } else if calc.odd(row) { rgb("#f8fafc") } else { white },
    table.header(
      text(fill: white, weight: "bold", size: 8.2pt)[Certificate / Gate],
      text(fill: white, weight: "bold", size: 8.2pt)[Prover / Target],
      text(fill: white, weight: "bold", size: 8.2pt)[Domain / Scope],
      text(fill: white, weight: "bold", size: 8.2pt)[Certified Result (`.sppb` CRC-64 `0xF26558090BB83BB2`)],
    ),
    text(size: 8.1pt, weight: "bold")[`C153`],
    text(size: 8.1pt)[1D `Jet2` (`cr_clausen2`)],
    text(size: 8.1pt)[$theta in [0.01, 0.40]$],
    text(size: 8.1pt)[`PROVED` (343 boxes, `max_hi` $= 9.764 times 10^(-7) <= 10^(-6)$)],
    text(size: 8.1pt, weight: "bold")[`C154`],
    text(size: 8.1pt)[2D `Jet2D` (JT Clock)],
    text(size: 8.1pt)[$[0.02, 0.30] times [0.05, 0.40]$],
    text(size: 8.1pt)[`PROVED` (1,567 boxes, `max_hi` $= 4.996 times 10^(-4) <= 5 times 10^(-4)$)],
    text(size: 8.1pt, weight: "bold")[`C155`],
    text(size: 8.1pt)[1D `Jet2` (Jensen Gap)],
    text(size: 8.1pt)[$delta in [10^(-3), 0.40]$],
    text(size: 8.1pt)[`PROVED` (5 boxes, `max_hi` $= 7.146 times 10^(-3) <= 8 times 10^(-3)$)],
    text(size: 8.1pt, weight: "bold")[`C156`],
    text(size: 8.1pt)[1D `Jet2` (App. D.3 Hölder)],
    text(size: 8.1pt)[$u in [0.01, 0.35]$],
    text(size: 8.1pt)[`PROVED` (9 boxes, `max_hi` $= 2.332 times 10^(-2) <= 2.5 times 10^(-2)$)],
    text(size: 8.1pt, weight: "bold")[`K12`],
    text(size: 8.1pt)[Moore–Krawczyk (`cr_dilog_unit_re`)],
    text(size: 8.1pt)[$theta in [0.90, 1.80]$],
    text(size: 8.1pt)[`UNIQUE_PROVED` in 3 iters: $theta^* = 1.327793289355...$ ($w = 4.33 times 10^(-12)$)],
    text(size: 8.1pt, weight: "bold")[`F39`],
    text(size: 8.1pt)[Falsifier (Sec. 5.2 Cycle)],
    text(size: 8.1pt)[$r in [4, 20]$],
    text(size: 8.1pt)[`FALSIFIED_OK` (witness $r = 12.0$, $Delta_"rearr" = 1.818 > 0.50$)],
    text(size: 8.1pt, weight: "bold")[5-Pillar Suite],
    text(size: 8.1pt)[`null_cone_gravity_audit_suite`],
    text(size: 8.1pt)[10/10 Pass 9B (`13,248 B`)],
    text(size: 8.1pt)[`EXACT PARITY` vs. LLVM `-O3`, `host_libm=0`, `nm -u = _putchar`],
    text(size: 8.1pt, weight: "bold")[Blinded RCT],
    text(size: 8.1pt)[`alexandria_epoch40_rct`],
    text(size: 8.1pt)[$N = 1,600$ (800 Disc + 800 Held)],
    text(size: 8.1pt)[`1,600/1,600` vs. `0/1,600` (`b01=1,600`, `c10=0`; `62,400` total)],
    text(size: 8.1pt, weight: "bold")[Living Codex],
    text(size: 8.1pt)[`alexandria_codex_app`],
    text(size: 8.1pt)[53/53 Pass 9B Zero-LLVM],
    text(size: 8.1pt)[`195/195 = 100.0%` Deep MDS (`283/283` across 5 apps); `142/142` XCTests],
  ),
  caption: [Complete Epoch XL / Horizon 1E certification ledger (`44` scrolls, `603` SppMLIR functions, `156/156` Pinakes seams, `12/12` Krawczyk unique roots, `39/39` falsifications, `AnalyticCLI` verified `36,258 B` `.sppb` v3.0.0 with `157` diagnostics).],
)

= Conclusion and Recommendations for Revising `arXiv:2611.34924v1`

Chandrasekaran's null-cone quantization program introduces genuinely sharp analytical tools — notably the $op("SL")(2, RR)\/op("SO")(2)$ conformal supermetric, the exact Cauchy–Schlömilch area resolution, the exact Tauberian clock-depth calculus, and the Appendix D.3 localized-patch Raychaudhuri–Hölder bound (`C156`). At the same time, our independent `[X]` audit shows that the paper's central nonperturbative claims require substantial revision before they can stand as rigorous theorems of 4D quantum gravity:

1. *Finite-dimensionality & discrete area spectrum (Sec. 5.2):* Replace the circular cycle-rearrangement argument (`F39`) with a direct, nonperturbative proof that $C_D = U e^(-hat(A)\/(8 G_N ℏ)) P_D$ is Hilbert–Schmidt (or compact) on $cal(H)_D$ — without assuming unconditional convergence of closed-cut trace sums.
2. *UV finiteness & pair amplitude (Sec. 4.4):* Report the exact real non-analytic $-pi\/(2 s^3)$ cusp term in Eq. (4.35), clarify that $sum k^(-2)$ is already UV-convergent at $s = infinity$, and distinguish phase-expansion non-commutativity from Goroff–Sagnotti derivative-vertex loop divergences.
3. *Schwarzschild ensemble & zero modes (Sec. 5.3):* Clarify that $x^* = sqrt(257\/347)$ is dynamically locked by $q = 257\/302$ rather than tunable, acknowledge the $26.86\%$ $O(1)$ area spread in $rho_D$ prior to fixing mass, verify the Lorentzian reduced-measure heat-kernel equivalence, and reconcile the perturbative $s^(3\/4)$ graviton bound of Appendix D.3 with the $O(s)$ Bekenstein–Hawking microstate count of Eq. (5.42).

#v(5pt)
#line(length: 100%, stroke: 0.45pt + luma(185))
#v(2pt)
#text(size: 8.4pt, weight: "bold")[References]
#set par(first-line-indent: 0pt, leading: 0.44em)
#text(size: 8.0pt)[
[1] V. Chandrasekaran, *An algebraic quantization of gravity from the null cone*, `arXiv:2611.34924v1` [hep-th] (Nov. 23, 2026). \
[2] A. Sen, *Logarithmic corrections to Schwarzschild and other non-extremal black hole entropy in different dimensions*, JHEP 04 (2013) 156, `arXiv:1205.0971`. \
[3] M. H. Goroff and A. Sagnotti, *The ultraviolet behavior of Einstein gravity*, Nucl. Phys. B 266 (1986) 709–736. \
[4] S. M. Christensen and M. J. Duff, *Quantizing gravity with a cosmological constant*, Nucl. Phys. B 170 (1980) 480–506; F. Bastianelli, R. Bonezzi, and M. Melis, *Gauge-invariant coefficients in perturbative quantum gravity*, Eur. Phys. J. C 82 (2022) 1139. \
[5] D. V. Fursaev, A. Patrushev, and S. N. Solodukhin, *Distributional geometry of squashed cones*, Phys. Rev. D 88 (2013) 044054. \
[6] A. G. Cohen, D. B. Kaplan, and A. E. Nelson, *Effective field theory, black holes, and the cosmological constant*, Phys. Rev. Lett. 82 (1999) 4971–4974.
]
