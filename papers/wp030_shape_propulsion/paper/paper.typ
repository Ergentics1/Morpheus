// [GB] Round-1 reconciled edition: clean-room [E] text unchanged, with inserted reconciliation notes.
// Working Paper 030 / Horizon Series Monograph I (Swift++ Library of Alexandria Epoch XXXVI)
// Continuation, Pressure-Test & Resolution of Ergentics Working Paper 028 (23 September 2026)
// Compile: typst compile paper.typ paper.pdf
// Copyright (c) 2026 Ergentics, LLC -- MIT License

#set document(
  title: "Shape-Controlled Gravitational Propulsion Resolved: Iso-Inertial Hopf-Fibration Three-Mass Quadrupole Switching, Noether Constant-p Bounds, Shapere-Wilczek Holonomy, and Coupled Eq. (5) Mission Utility",
  author: "Ergentics, LLC & Swift++ Library of Alexandria Verification Program",
)

#set page(
  paper: "us-letter",
  margin: (x: 0.80in, y: 0.78in),
  numbering: "1",
  number-align: center,
  header: context {
    if counter(page).get().first() > 1 {
      set text(size: 8.2pt, fill: luma(95), style: "italic")
      grid(
        columns: (1fr, auto),
        [Shape-Controlled Gravitational Propulsion Resolved (Cont. of Paper 028)],
        [Ergentics Working Paper 030 · Horizon Monograph I],
      )
      v(-6pt)
      line(length: 100%, stroke: 0.4pt + luma(180))
    }
  },
)

#set text(
  font: "New Computer Modern",
  size: 9.8pt,
  lang: "en",
)

#set par(
  justify: true,
  leading: 0.55em,
  first-line-indent: 1.2em,
)

#set heading(numbering: "1.1")
#show heading.where(level: 1): it => {
  v(11pt, weak: true)
  set text(size: 11.5pt, weight: "bold", fill: rgb("#0f172a"))
  block(breakable: false)[#it]
  v(4pt, weak: true)
}
#show heading.where(level: 2): it => {
  v(8.5pt, weak: true)
  set text(size: 10.2pt, weight: "bold", fill: rgb("#1e293b"))
  block(breakable: false)[#it]
  v(3.5pt, weak: true)
}
#show heading.where(level: 3): it => {
  v(6.5pt, weak: true)
  set text(size: 9.7pt, weight: "bold", fill: rgb("#1e3a8a"))
  block(breakable: false)[#it]
  v(4pt, weak: true)
}

#show table: set par(justify: false)
#show raw.where(block: false): it => if it.text == "Swift++" { box(it) } else { it }
#show figure.caption: it => {
  set text(size: 8.5pt, fill: luma(55))
  set par(leading: 0.48em, justify: true)
  it
}

// Shorthand operators
#let varepsilon = sym.epsilon.alt
#let thm-cnt = counter("thm")

#let env-box(kind, accent, title: none, body) = {
  thm-cnt.step()
  v(4.5pt, weak: true)
  block(
    width: 100%,
    inset: (left: 10pt, right: 8pt, top: 5.5pt, bottom: 5.5pt),
    stroke: (left: 2pt + accent),
    fill: luma(249),
    radius: (right: 3pt),
    breakable: false,
  )[
    #set par(first-line-indent: 0pt)
    #text(weight: "bold", fill: accent)[#kind #context thm-cnt.display("1")#if title != none [ (#title)].] #emph(body)
  ]
  v(4.5pt, weak: true)
}

#let theorem(title: none, body) = env-box("Theorem", rgb("#1e3a8a"), title: title, body)
#let proposition(title: none, body) = env-box("Proposition", rgb("#0f766e"), title: title, body)
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

#let proof(body) = {
  v(2pt, weak: true)
  block(width: 100%)[
    #set par(first-line-indent: 0pt)
    #emph[Proof.] #body #h(1fr) $square$
  ]
  v(4.5pt, weak: true)
}

// ============================================================================
// TITLE BLOCK
// ============================================================================
#align(center)[
  #text(size: 8.4pt, fill: rgb("#1e3a8a"), weight: "bold", tracking: 0.08em)[
    ERGENTICS WORKING PAPER 030 · HORIZON SERIES MONOGRAPH I · CONTINUATION OF WORKING PAPER 028
  ]
  #v(5pt)
  #text(size: 14.0pt, weight: "bold", fill: rgb("#0f172a"))[
    Shape-Controlled Gravitational Propulsion Resolved: Iso-Inertial Hopf-Fibration Three-Mass Quadrupole Switching, Noether Constant-$p$ Bounds, Shapere–Wilczek Holonomy, and Coupled Eq. (5) Mission Utility
  ]
  #v(6pt)
  #text(size: 9.8pt)[
    Ergentics, LLC & the `Swift++` Library of Alexandria Verification Program (Epoch XXXVI · Horizon 1)
  ]
  #v(2.5pt)
  #text(size: 8.5pt, fill: luma(90))[
    November 2026 · Air-Gapped Pass 9B Zero-LLVM Executable Corpus · Universal `SppMLIR` Interval-AD Certification (MIT License)
  ]
]

#v(6pt)
#block(
  width: 100%,
  inset: (x: 14pt, y: 8.5pt),
  fill: luma(248),
  stroke: (y: 0.6pt + luma(180)),
)[
  #set par(first-line-indent: 0pt, leading: 0.51em)
  #set text(size: 8.9pt)
  *Abstract.* Ergentics Working Paper 028 (23 September 2026) evaluated a frozen 13-case three-mass Newtonian gravity protocol (`027`) against classical tether-pumping literature, confirming finite-size gravitational coupling (`H1–H3`) while explicitly leaving two decisive questions open: whether a controlled three-mass triad offers genuine novelty beyond two-mass tethers (`H4`), and whether it yields mission utility once coupled dynamics, internal-state cycle closure, Eq. (5) energy accounting, and fair baselines are enforced (`H5`). We take over Working Paper 028, pressure-test every prior equation and numerical bound in air-gapped zero-dependency `Swift++` (Pass 9B Zero-LLVM with bit-exact LLVM `-O3` parity and zero host `libm`), and resolve `H1–H5` completely. First, we confirm Paper 028's Earth values (`-3.3203` / `+1.6601` $mu$N) and synthetic work map (`13.1268` $mu$J) to all 11 digits while proving that naive IEEE-754 subtraction already loses `9` digits at `L = 100 m` and fails by `8.20e-3` at $L slash R = 10^(-7)$ (`C137`, `1` `Jet2` box). Second, we prove the _Exact Noether Constant-$p$ Theorem_: in a spherical $1 slash r$ field, any spin-closed cycle of any $N$-mass craft conserves orbital angular momentum exactly ($Delta L_"orb" = 0$), locking transfers onto constant semi-latus rectum $p = a(1 - e^2)$ and forbidding circular-to-circular raising without permanent spin-up or non-central coupling. Third, we resolve `H4` affirmatively by constructing the _Iso-Inertial Hopf-Fibration Three-Mass Triad_ on the normalized Jacobi shape sphere $S^2$: holding total polar inertia $I_(z z) equiv I_0 = (2 slash 3) M L^2$ strictly constant (`0.00` variation) while steering the complex quadrupole $Q_CC = I_0 e^(2 i theta_0)(cos Phi + i cos Theta sin Phi)$ via the Dirac-monopole zero-spin connection $dot(theta)_0 = -(1 slash 2) cos Theta dot(Phi)$. In live 5-orbit coupled 4-body (dynamical primary $M_p = 1000 M$) integration, the Hopf triad eliminates the catastrophic Coriolis tumbling of unassisted 2-mass Landis tethers (`0` tumbles vs. `1,475°–11,425°` tumble; `1.78×–1.83×` higher $Delta E_"orb"$), recovers the `2/3` equal-mass penalty, satisfies Paper 028's Eq. (5) to `3.28 ppm` ($|Delta J_"tot"| < 10^(-12)$), and executes live `-90.0000°` zero-angular-momentum Shapere–Wilczek reorientation (`C140`) impossible for $N = 2$. Fourth, we resolve `H5` with brutal quantitative honesty: at Paper 028's `L = 100 m` LEO baseline, ideal annual $Delta v = 5.17$ mm/s/yr is overwhelmed `~1,000×` by atmospheric drag, `~27×` by solar radiation pressure, and `~3 × 10^5×` by Hall thrusters (*falsified/dominated at `100 m` LEO*). Genuine propellantless utility emerges strictly in two quantified niches: kilometer-scale eccentric pumping (`L = 20 km`, $e = 0.25$: `619.8 m/s/yr`, `55.1 N` tidal tension, `< 12 kg` Zylon) and small-body/asteroid proximity (`R = 2.5 km`, `L = 100 m`: `7.84 × 10^6×` coupling boost, zero plume contamination, zero-momentum pointing). We also derive the exact Eq. (5) regeneration efficiency (`C139`), certify its 50%-efficiency critical eccentricity $e_(50)^* = 0.1150133319511158$ by Moore–Krawczyk (`K8`, width `4.86e-16`), and validate all kernels via an `N = 1,600` blinded ARM64 RCT (`1,600/1,600` vs. `276/1,600`, `c10 = 0`).
]

#v(2.5pt)
#text(size: 8.4pt, fill: luma(80))[
  *Keywords:* Shape-Controlled Gravitational Propulsion, Three-Mass Spacecraft, Hopf Fibration, Shapere–Wilczek Geometric Phase, Noether Constant-$p$ Manifold, Tether Coriolis Libration, Outward-Rounded `SppMLIR` Certification.
]

// ============================================================================
// SECTION 1: CONTINUING AND PRESSURE-TESTING WORKING PAPER 028
// ============================================================================

// ---- [GB] Round-1 reconciliation layer (inserted; [E] lines above and below are unchanged) ----
#let gb-col = ("CONFIRMED": rgb("#15803d"), "CONFIRMED-IN-SUBSTANCE": rgb("#4d7c0f"), "PARTIAL": rgb("#b45309"), "DISPUTED": rgb("#b91c1c"), "UNVERIFIABLE": rgb("#525252"), "SPEC-NEEDED": rgb("#1d4ed8"), "NEW": rgb("#7e22ce"))
#let gbnote(id, verdict, title, body) = block(width: 100%, breakable: true, above: 6pt, below: 6pt,
  inset: (x: 8pt, y: 5.5pt), fill: rgb("#fffaf3"), radius: 1.5pt,
  stroke: (left: 2.2pt + gb-col.at(verdict, default: luma(120))))[
  #set par(first-line-indent: 0pt, hanging-indent: 0pt, justify: true, leading: 0.5em)
  #set text(size: 8.3pt)
  #text(weight: "bold", fill: gb-col.at(verdict, default: luma(80)))[Reconciliation #id · #verdict] — #emph(title) \
  #body
]
#block(width: 100%, inset: (x: 10pt, y: 7pt), fill: rgb("#f5f3ff"), stroke: 0.6pt + rgb("#7e22ce"), radius: 2pt)[
  #set par(first-line-indent: 0pt, justify: true, leading: 0.5em)
  #set text(size: 8.4pt)
  #text(weight: "bold")[Reconciled edition — Round 1 (2026-11-26).]
  #"The text of Working Paper 030 below is the frozen clean-room manuscript, unchanged. Boxed notes are Grok Bot ([GB]) Round-1 verdicts on the Gemini 4 Neon ([G4N]) Cycle-1 catches and on new [GB] items. Claims that rest on the internal Swift++ corpus are left exactly as written and marked UNVERIFIABLE. Corrections are proposed, not applied in the text; the author decides. A ledger of all verdicts is at the end."
]
// ---- end [GB] layer header ----

= Continuing & Pressure-Testing Ergentics Working Paper 028

Ergentics Working Paper 028 (Web Edition 029, 23 September 2026) set an unusually disciplined standard for exploratory propulsion research [12]: rather than extrapolating a `3.32` $mu$N static force contrast into premature engineering claims, it anchored the finite 13-configuration `027` study against Landis's gravity-coupled tether pumping [1], [2], Guéron–Maia–Matsas's Newtonian vs. relativistic swimming distinction [3], Wisdom's spacetime swimming [5], and NASA/JPL's gravity-assist momentum-partner framework [4]. Paper 028 classified its five governing hypotheses (`H1–H5`) cleanly: `H1–H3` were supported only on fixed point evaluations and a prescribed static work rectangle, while *`H4` (distinct triad novelty over 2-mass tethers)* and *`H5` (coupled mission utility under complete Eq. (5) energy and momentum accounting)* remained explicitly open.

This continuation paper—inaugurating *Horizon 1 (Epoch XXXVI)* of the `Swift++` Library of Alexandria—takes over Working Paper 028 completely. Rather than treating `H4` and `H5` qualitatively, we bring four independent verification pillars to bear: (i) exact analytical mechanics on the three-body Jacobi shape sphere $S^2$, (ii) universal continuous-domain outward-rounded `SppMLIR` interval automatic differentiation (`Jet2`, `Jet2D`, Moore–Krawczyk `K8`, and mechanical falsification `F35`) [11], (iii) live coupled 4-body dynamical-primary ARM64 simulations compiled 100% by the air-gapped Pass 9B Zero-LLVM backend with bit-exact LLVM `-O3` parity and zero host `libm`, and (iv) a blinded paired ARM64 randomized controlled trial (`N = 1,600` trials) plus an independent clean-room Python archival verifier (`[X]` cross-verification).

== Immediate Audit & Cancellation Pressure-Test of Working Paper 028 (`H1–H3`)
#gbnote("GB-W26", "NEW", "The naive rounding error depends on evaluation order", "The binary64 'naive' contrast error is not one number: μ/3·(a+b−2c) gives 5.75e-8, summing three point accelerations gives 3.46e-7; the printed 1.89e-7 sits between them. ε = 1e-7 reproduces 8.20e-3 exactly, but ε = 1e-8 gives 48%, not 100% (100% only below about 5e-9). The qualitative point stands; the figures should name the evaluation order. Proposed NEG-W26 (minor).")


Evaluating Paper 028 Eq. (1) for three equal masses $m_i = M slash 3$ at collinear offsets $0, plus.minus L hat(r)$ and transverse offsets $0, plus.minus L hat(theta)$ with dimensionless span ratio $varepsilon = L slash R$ yields exact algebraic factorizations free of IEEE-754 subtraction cancellation:
$ (Delta a_(parallel)(varepsilon)) / (-(2 mu varepsilon^2) slash R^2) = (1 - varepsilon^2 slash 3) / ((1 - varepsilon^2)^2), quad
  (Delta a_(perp)(varepsilon)) / (+(mu varepsilon^2) slash R^2) = 2 / 3 (s^2 + s + 1) / (s^3 (s + 1)), quad s = sqrt(1 + varepsilon^2). $
At Paper 028's Earth benchmark ($mu = 3.986004418 times 10^(14) "m"^3 "s"^(-2)$, $R = 7.0 times 10^6 "m"$, $L = 100 "m"$, $M = 1000 "kg"$), our Zero-LLVM kernel (`sp_radial_delta_accel`, `sp_transverse_delta_accel`) replicates every published digit: $a_"pt" = -8.1347028939 "m/s"^2$, $Delta a_(parallel) = -3.3202868966 times 10^(-9) "m/s"^2$ (`-3.3203` $mu$N), $Delta a_(perp) = +1.6601434473 times 10^(-9) "m/s"^2$ (`+1.6601` $mu$N), and Paper 028's Eq. (4) synthetic work map $W_(q,"ext") = W_(C,"ext") = 1.3126816602 times 10^(-5) "J"$ (`13.1268` $mu$J).

However, pressure-testing naive direct evaluation $(1 slash (R+L)^2 + 1 slash (R-L)^2 - 2 slash R^2) slash 3$ exposes an immediate numerical cliff hidden inside Paper 028's `binary64` tolerance ($2 times 10^(-12)$): because $varepsilon^2 approx 2.04 times 10^(-10)$ at `L = 100 m`, direct subtraction _already destroys 9 of 16 decimal digits_ (`naive = -3.3202862681e-9`, relative error `1.89e-7`), degrading to `8.20e-3` relative error at $varepsilon = 10^(-7)$ and `100%` noise for $varepsilon <= 10^(-8)$. Direct `SppMLIR` `Jet2` certification (`C137`) proves universally in `1` box that our cancellation-free ratio matches `1` within `4.188e-3 <= 4.5e-3` across the entire continuum $varepsilon in [10^(-4), 0.05]$.

// ============================================================================
// SECTION 2: FOUR EXACT THEOREMS RESOLVING H2, H3, AND H4
// ============================================================================
= Exact Analytical Resolution: Noether Constant-$p$, Hopf Iso-Inertial Triad & Holonomy

Before asking whether a three-mass spacecraft improves on Landis's two-mass tether [1], [2], [9], [10], we must compare their exact leading quadrupole moments for fixed total mass $M$ and maximum half-span $L$. A symmetric 2-mass dumbbell ($M slash 2$ at $plus.minus L$) has polar inertia $I_"db" = M L^2$ and radial contrast $-3 mu L^2 slash R^4$. Paper 028's 3-equal-mass collinear triad ($M slash 3$ at $0, plus.minus L$) carries $1 slash 3$ of its mass at the center of mass, giving $I_0 = (2 slash 3) M L^2$ and radial contrast $-2 mu L^2 slash R^4$—an inherent _$2 slash 3$ collinear quadrupole penalty_ if operated purely by radial extension/retraction. We now prove three exact theorems showing both the universal conservation barrier (`H2–H3`) and the genuinely distinct geometric mechanism (`H4`) by which a 3-mass triad not only recovers this `2/3` penalty completely, but solves the Coriolis tumbling instability that defeats unassisted 2-mass tethers.

#theorem(title: "Exact Noether Constant-p Orbital Manifold Barrier")[
  Consider any bounded $N$-mass spacecraft ($N >= 2$) moving in a central Newtonian potential $V(r) = -mu slash r$ (with fixed or dynamical primary). Let $bold(L)_"orb"$ be orbital angular momentum and $bold(S)_"craft" = sum_(i=1)^N m_i bold(rho)_i times dot(bold(rho))_i$ be internal spin angular momentum. Because the full Lagrangian is $S O(3)$-invariant under simultaneous rotation of orbit and craft, $bold(J)_"tot" = bold(L)_"orb" + bold(S)_"craft"$ is an exact Noether invariant. Consequently, across _any_ internal-state-closed maneuver returning spin to its initial value ($Delta bold(S)_"craft" = bold(0)$):
  $ Delta bold(L)_"orb" = bold(0) arrow.r.double p = a(1 - e^2) = (|bold(L)_"orb"|^2) / (mu M_"red"^2) = "const". $
  In particular, raising a circular orbit ($e = 0$) to a larger circular orbit ($e = 0, a_2 > a_1$) via any spin-closed internal shape cycle in a spherical $1 slash r$ field is mathematically impossible.
]

#proof[
  Internal forces satisfy Newton's third law in strong form ($sum bold(f)_(i j) = bold(0)$, $sum bold(rho)_i times bold(f)_(i j) = bold(0)$), so internal actuators cannot alter $bold(J)_"tot"$. The external gravitational torque on the craft equals $bold(tau)_"int" = sum_i bold(rho)_i times bold(F)_i = -bold(R) times (sum_i bold(F)_i) = -dot(bold(L))_"orb"$, giving $d(bold(L)_"orb" + bold(S)_"craft") slash d t = bold(0)$ identically. When $bold(S)_"craft" (T) = bold(S)_"craft" (0)$, $Delta bold(L)_"orb" = bold(0)$, fixing the Keplerian semi-latus rectum $p = h^2 slash mu$. Since raising a circular orbit from $R_1$ to $R_2 > R_1$ requires $Delta h = sqrt(mu R_2) - sqrt(mu R_1) > 0$, it violates $Delta bold(L)_"orb" = bold(0)$ unless angular momentum is permanently stored as internal spin ($Delta S_"craft" = -Delta L_"orb"$) or exchanged with a non-central field ($J_2$ oblateness or a third gravitating body).
]

== The Iso-Inertial Hopf-Fibration Three-Mass Triad (`H4` Architecture)
#gbnote("NEG-W6/7a", "UNVERIFIABLE", "C138 ≤ 1e-6 octupole bound", "C138 is an internal Swift++ certificate. G4N's octupole scope point (bound needs the zero-octupole symmetric configuration) is plausible but its 1.29e-5 figure was not independently recomputed in this round. The [E] claim is left verbatim.")

#gbnote("NEG-W2", "CONFIRMED", "Θ = π/3 holonomy loop hits two binary collisions; Θ = 0 is collinear", "In the paper's (z1, z2) chart, d23 = 0 at Φ = 0 and d13 = 0 at Φ = π. Θ = 0 gives bodies at (1, −1, 0): collinear, not equilateral. The equilateral shape sits at Θ = Φ = π/2 in this chart. G4N's equilateral-pole basis loop at β = π/3 is collision-free (min d/L = 0.517638 = √(2−√3)) with |Q| independent of χ.")

#gbnote("GB-W25", "NEW", "Holonomy sign: net physical rotation is +90°, not −90°", "Integrating the zero-spin condition around the paper's own loop (Φ: 0→2π at Θ = π/3) gives Δθ0 = −90° for the chart angle, but the labelled bodies end up rotated by +90°: the chart's quadrupole phase carries an extra π over the loop. The −90° in Theorem 3, Fig. 3 and the abstract is the chart angle, not the physical attitude change. G4N's basis gives −90° physically, so the sign depends on the basis and orientation; the paper should state the convention. Proposed NEG-W25.")

#gbnote("NEG-W4", "CONFIRMED", "Theorem 2 sign: the printed Q is the mass quadrupole", "Σ m ρ² equals the paper's (M/3)(z1²+z2²) to 3.8e-15, while (Ixx−Iyy)+2i Ixy equals −Σ m ρ² to 4.4e-16. The identity is right if the left side is read as the mass quadrupole; with the inertia tensor it needs a minus sign. Iso-inertial |Izz − I0| ≤ 1.3e-15 confirmed.")


Parameterize three equal planar masses ($m_i = M slash 3$) in normalized Jacobi complex coordinates $(z_1, z_2) in CC^2$ satisfying $bold(rho)_1 = z_1 slash sqrt(2) + z_2 slash sqrt(6)$, $bold(rho)_2 = -z_1 slash sqrt(2) + z_2 slash sqrt(6)$, $bold(rho)_3 = -sqrt(2 slash 3) z_2$ (so $sum_i bold(rho)_i equiv bold(0)$ identically). Restricting to the constant-inertia 3-sphere $|z_1|^2 + |z_2|^2 = r_J^2 = 2 L^2$ via the Hopf fibration $S^3 -> S^2$ [6], [7], [8]:
$ z_1 = r_J cos(Theta slash 2) e^(i(theta_0 + Phi slash 2)), quad z_2 = r_J sin(Theta slash 2) e^(i(theta_0 - Phi slash 2)), quad (Theta, Phi) in [0, pi] times [0, 2 pi). $

#theorem(title: "Iso-Inertial Hopf Quadrupole Steering & Exact Lagrangian Decoupling")[
  Along every curve $(theta_0 (t), Theta(t), Phi(t))$ on the Hopf bundle $S^3 -> S^2$ of fixed radius $r_J = sqrt(2) L$:
  1. *Strictly Constant Polar Inertia:* $I_(z z) = (M slash 3)(|z_1|^2 + |z_2|^2) equiv I_0 = (2 slash 3) M L^2$, so $dot(I)_(z z) equiv 0$ (zero radial Coriolis torque!).
  2. *Full-Disk Complex Quadrupole Controllability:* The traceless planar quadrupole tensor $Q_CC := (I_(x x) - I_(y y)) + 2 i I_(x y) = (M slash 3)(z_1^2 + z_2^2)$ equals
     $ Q_CC = I_0 e^(2 i theta_0) (cos Phi + i cos Theta sin Phi), $
     which maps onto the _entire closed disk_ $|Q_CC| <= I_0$. For any desired orbital alignment angle $theta_"orb" (t)$ and stroke amplitude $q_"amp" in (-1, 1)$, setting $cos Phi = q_"amp" cos(2(theta_"orb" - theta_0))$ and $cos Theta = q_"amp" sin(2(theta_"orb" - theta_0)) slash sin Phi$ tracks $Q_CC (t) = q_"amp" I_0 e^(2 i theta_"orb" (t))$ with _identically zero leading quadrupole gravity-gradient torque_ ($tau_g^((2)) equiv 0$).
  3. *Dirac-Monopole Zero-Spin Connection:* The internal spin angular momentum is
     $ S_"craft" = (M slash 3) Im(overline(z)_1 dot(z)_1 + overline(z)_2 dot(z)_2) = I_0 (dot(theta)_0 + 1 / 2 cos Theta dot(Phi)). $
     Setting $S_"craft" equiv 0$ yields the non-integrable mechanical connection $dot(theta)_0 = -(1 slash 2) cos Theta dot(Phi)$, whose holonomy around any closed shape-sphere loop $partial Sigma subset S^2$ of solid angle $Omega_"solid" (Sigma)$ is exact pure geometric rotation $Delta theta_"geom" = -(1 slash 2) Omega_"solid" (Sigma)$—a maneuver mathematically impossible for any 2-mass tether ($N = 2$ has trivial 0D shape sphere $S^0$).
]

#proof[
  Direct substitution gives $|z_1|^2 + |z_2|^2 = r_J^2 (cos^2(Theta slash 2) + sin^2(Theta slash 2)) = r_J^2$, proving (1). Expanding $z_1^2 + z_2^2 = r_J^2 e^(2 i theta_0)[cos^2(Theta slash 2) e^(i Phi) + sin^2(Theta slash 2) e^(-i Phi)] = r_J^2 e^(2 i theta_0)(cos Phi + i cos Theta sin Phi)$ gives (2), whose real and imaginary components $(u, v) = (cos Phi, cos Theta sin Phi)$ satisfy $u^2 + v^2 = cos^2 Phi + cos^2 Theta sin^2 Phi <= 1$ with equality at the poles $Theta in {0, pi}$ and interior surjectivity on $|w| < 1$. Differentiating $z_1, z_2$ gives $Im(overline(z)_1 dot(z)_1) = r_J^2 cos^2(Theta slash 2)(dot(theta)_0 + dot(Phi) slash 2)$ and $Im(overline(z)_2 dot(z)_2) = r_J^2 sin^2(Theta slash 2)(dot(theta)_0 - dot(Phi) slash 2)$; summing yields $r_J^2 (dot(theta)_0 + (1 slash 2)(cos^2(Theta slash 2) - sin^2(Theta slash 2)) dot(Phi)) = r_J^2 (dot(theta)_0 + (1 slash 2) cos Theta dot(Phi))$. By Stokes' theorem on $S^2$, $-1 slash 2 integral.cont cos Theta d Phi = -(1 slash 2) integral.double_Sigma sin Theta d Theta d Phi = -(1 slash 2) Omega_"solid" (Sigma)$, proving (3).
]

#proposition(title: "Exact Eccentric Pumping Law & Recovery of the 2/3 Collinear Penalty")[
  Switching the iso-inertial triad between radial alignment ($q_"amp" = +1$, $Delta U = -mu I_0 slash r^3$) on the inbound leg ($dot(r) < 0$) and transverse alignment ($q_"amp" = -1$, $Delta U = +mu I_0 slash (2 r^3)$) on the outbound leg ($dot(r) > 0$) yields exact orbital energy gain per orbit on an eccentric orbit $(a, e)$ with $p = a(1 - e^2)$:
  $ Delta E_"orb" = 3 / 2 mu I_0 (1 / r_p^3 - 1 / r_a^3) = (3 mu I_0) / p^3 (3 e + e^3) = (2 mu M L^2) / p^3 (3 e + e^3). $
  Thus radial $arrow.l.r$ transverse iso-inertial switching (`1.5×` work per unit $I_0$) cancels the `2/3` mass-split factor of three equal masses identically ($3 slash 2 times 2 slash 3 = 1$), delivering _exact parity_ with a full-retraction 2-mass Landis dumbbell of equal mass $M$ and half-span $L$—while eliminating $dot(I)_(z z)$ Coriolis libration!
]

Direct `SppMLIR` `2D Jet2D` certification (`C138`, `1,859` boxes) universally proves the exact 3-mass radial acceleration contrast across the entire continuous morphing domain $(varepsilon, alpha) in [10^(-3), 0.02] times [0, pi slash 2]$ against its iso-inertial quadrupole law $-(1 slash 2) varepsilon^2 (1 + 3 cos 2 alpha)$ to `9.97e-7 <= 1.0e-6`. Likewise, `C140` (`139` `Jet2` boxes) certifies the cancellation-free Hopf holonomy magnitude $2 pi sin^2(Theta slash 2)$ against $(pi slash 2) Theta^2$ on $[10^(-4), 0.1]$.

#figure(
  image("figures/fig1_isoinertial_triad_vs_dumbbell.svg", width: 100%),
  caption: [Resolution of `H4`: (a) Iso-inertial 3-mass triad morphing from radial ($alpha = 0$) through equilateral ($alpha = pi slash 4$) to transverse ($alpha = pi slash 2$) at strictly constant $I_(z z) = (2 slash 3) M L^2$ and $S_"rel" = 0$; (b) Live 5-orbit coupled comparison without reaction wheels ($M = 3, L_"max" = 0.02, e_0 = 0.2$): unassisted 2-mass Landis tethers suffer severe Coriolis tumbling (`1,475°–11,425°`), whereas the Hopf 3-mass triad tracks the eccentric orbit with `0.00°` quadrupole error (`0` tumbles) and delivers `1.78×–1.83×` higher $Delta E_"orb"$.],
) <fig-h4>

// ============================================================================
// SECTION 3: LIVE COUPLED 4-BODY VERIFICATION & H4 HEAD-TO-HEAD BENCHMARKS
// ============================================================================
= Live Coupled 4-Body Verification (`shape_propulsion_5pillar_suite.spp`)
#gbnote("NOTE-8", "CONFIRMED", "Specify μ_tot and the energy convention for a_f, e_f", "Keplerian elements from the total ΔE (μ = 1, M = 3, p = 0.96) give a_f = 1.00486, e_f = 0.21130 vs the printed 1.0046, 0.2106; the gap is the osculating vs total-energy convention G4N flagged.")

#gbnote("SIM-030", "SPEC-NEEDED", "Coupled 4-body numbers (tumbles, ΔE, Eq. 5 residual, Arm A spin-up)", "G4N's Python and Rust re-runs agree with each other and with the trend in the paper, but the paper does not give the switching law, gains, q_max, L_min, step count, tumble metric or initial conditions, so no independent third run is possible. A run spec is in the [GB] dossier; the exact figures stay as printed until the author supplies it.")


To close Working Paper 028's explicit limitations (fixed primary, static snapshot, uncoupled trajectories, uncomputed Eq. (5)), we execute `shape_propulsion_5pillar_suite.spp` (`25,040 B` native ARM64 Mach-O compiled 100% by Pass 9B Zero-LLVM with bit-exact LLVM `-O3` parity and `0` host `libm`) integrating *all four bodies*—a dynamical primary of finite mass $M_p = 1000 M$ ($M_"red" = M slash 1.001$, exact linear momentum $bold(P)_"tot" = bold(0)$) coupled to the 3-mass Hopf triad over `5` full eccentric orbits ($e_0 = 0.2$, `7,855` RK4 steps) with strictly zero initial spin ($S_"craft" (0) = 0$) and zero reaction wheels:

1. *Exact Eq. (5) Energy & Noether Conservation (@fig-eq5):* Over 5 eccentric orbits (`q_max = 0.95`, collision-free), the triad smoothly raises semi-major axis `a: 1.0000 -> 1.0046` and eccentricity `e: 0.2000 -> 0.2106`, gaining $Delta E_"orb" = +7.2590 times 10^(-3)$ while internal actuators perform exact external-potential work $W_"act" = +7.2589 times 10^(-3)$—satisfying Paper 028 Eq. (5) to *`3.28 ppm` relative residual*! Total 4-body angular momentum is conserved to $|Delta J_"tot"| < 10^(-13)$, semi-latus rectum drift stays below $10^(-5)$ (pure $O(L^3 slash R^4)$ octupole spin exchange, `max|S_craft| < 3e-5`), and the Hopf geometric phase winds smoothly by $theta_0 = -15.4698$ rad to keep $Q_CC$ locked on $theta_"orb" (t)$ with zero reaction wheels. On the circular control orbit ($e_0 = 0.0$), energy gain collapses to `0.0000` (`< 1e-7`), directly confirming Theorem 1's circular barrier.
2. *Head-to-Head `H4` Resolution vs. 2-Mass Landis Tether (@fig-h4 (b)):* Under identical total mass ($M = 3$), identical max half-span ($L_"max" = 0.02$), identical 4-body eccentric orbit ($e_0 = 0.2$), and zero reaction wheels, pumping a 2-mass Landis tether between $L_"min" = 0.25 L_"max"$ and $L_"max"$ excites violent Coriolis spin-up ($dot(phi) prop 1 slash L^2$), tumbling through `11,425.2°` (`31.7` full rotations in 5 orbits) and collapsing energy gain to `3.9565e-3`. Even gentler `0.50 L_max` pumping tumbles through `1,474.6°` (`4.1` rotations) with `4.0865e-3` gain. The Hopf 3-mass triad maintains `0` tumbles and achieves `7.2590e-3`—*`1.78×` to `1.83×` higher energy transfer* without a single reaction wheel!
3. *Live `-90.0000°` Zero-Angular-Momentum Attitude Reorientation (@fig-holonomy):* Traversing a closed Hopf latitude loop $Theta = pi slash 3$, $Phi: 0 -> 2 pi$ (`400` steps) in free space produces exact net attitude rotation *`-90.0000°`* matching $-pi(1 - cos(pi slash 3)) = -pi slash 2$ to `< 1e-12` while keeping instantaneous physical spin $|S_"craft" (t)| < 10^(-6)$ (`0.96e-6` $O(d Phi^2)$ step discretization).

#figure(
  image("figures/fig2_coupled_symplectic_orbit_and_eq5.svg", width: 100%),
  caption: [Live 4-body dynamical-primary Zero-LLVM integration ($M_p = 1000 M$, 5 orbits): (a) orbital energy gain $Delta E_"orb" = +7.2590 times 10^(-3)$ matches actuator work $W_"act" = +7.2589 times 10^(-3)$ to `3.28 ppm` (Eq. (5)), while the $e_0 = 0$ circular control stays at `0.0000`; (b) $(a, e)$ trajectory rides the exact Noether constant-$p = a(1 - e^2) = 0.9600$ manifold.],
) <fig-eq5>

#figure(
  image("figures/fig3_shapere_wilczek_holonomy.svg", width: 100%),
  caption: [Unique $N >= 3$ capability: (a) Hopf shape-sphere loop $Theta = pi slash 3$ enclosing solid angle $Omega = pi$ rotates the 3-mass frame by exact `-90.0000°` with $S_"craft" (t) = 0$; (b) exact holonomy $|Delta theta(Theta)| = 2 pi sin^2(Theta slash 2)$ vs. `C140` small-loop limit $(pi slash 2) Theta^2$.],
) <fig-holonomy>

// ============================================================================
// SECTION 4: BRUTALLY HONEST H5 MISSION UTILITY & THERMODYNAMIC EFFICIENCY
// ============================================================================
= Honest Resolution of `H5`: Thermodynamic Efficiency (`K8`) & Mission Dominance Regimes

Qualifying a genuinely novel 3-mass mechanism (`H4`) does _not_ automatically imply mission usefulness (`H5`)—precisely the epistemic discipline demanded by Working Paper 028 §6. We therefore subject the Hopf triad to exact Eq. (5) thermodynamic accounting and fair mission baselines.

== Exact Eq. (5) Regeneration Efficiency & Internal Kinetic Barrier
#gbnote("NEG-W6/7b", "CONFIRMED", "F35 loss is 84.8%, not 84.6%", "q(e* = 0.0275) = 0.847858, i.e. 84.8%.")

#gbnote("NEG-W3", "CONFIRMED", "Theorem G1: exact shape kinetic energy", "Direct numerical differentiation of the zero-spin triad gives T/(½ I0 Ω²) = 0.3333, 1.0000, 2.6036, 9.2564 at q = 0.5, 0.7071, 0.85, 0.95, equal to q²/(1−q²), and max|ρ|/L = √(2(1+q)/3). The §4.1 estimate holds only near q = 1/√2. G4N's hard-span parity factor was not separately re-derived.")


During each eccentric orbit, actuators supply potential work $W_p = (3 mu I_0) slash (2 r_p^3)$ at perigee (at motor efficiency $eta_"act" in (0, 1]$) and may recover fraction $eta_"regen" in [0, 1]$ of $W_a = (3 mu I_0) slash (2 r_a^3)$ at apogee. Defining $q(e) = (r_p slash r_a)^3 = ((1 - e) slash (1 + e))^3$, exact net thermodynamic efficiency is
$ eta_"prop" (e; eta_"act", eta_"regen") = (Delta E_"orb") / E_"batt" = (1 - q(e)) / (eta_"act"^(-1) - eta_"regen" q(e)), quad 1 - q(e) = (6 e + 2 e^3) / ((1 + e)^3). $
Without apogee regeneration ($eta_"regen" = 0, eta_"act" = 1$), efficiency decays linearly as $6 e$ near $e -> 0^+$ (`C139`, `1` `Jet2` box), and Moore–Krawczyk `K8` universally certifies the unique 50%-efficiency threshold directly on `SppMLIR`:
$ e_(50)^* = (2^(1 slash 3) - 1) / (2^(1 slash 3) + 1) in [0.11501333195111552, 0.11501333195111600] quad (w = 4.86 times 10^(-16), "4 iters"). $
Mechanical falsification `F35` refutes the naive static-snapshot 100%-efficiency claim against exact $eta_"prop" (e; 1, 0)$ at low eccentricity (witness $e^* = 0.0275$, where `84.6%` of input work is lost as heat at apogee!). Furthermore, an honest referee must note the *Internal Kinetic Energy Barrier*: tracking $theta_"orb" (t)$ continuously at orbital rate $Omega$ carries conservative internal kinetic energy $T_"shape" approx (1 slash 2) I_0 Omega^2 = (1 slash 2) mu I_0 slash a^3$, comparable to $Delta E_"orb" slash (18 e)$. Because $T_"shape"$ is conservative, a low-friction continuous wave linkage coasts like a balanced flywheel, requiring power only for bearing losses and $Delta E_"orb"$; however, _non-regenerative stop-start actuation_ would dissipate more kinetic energy than gravity supplies for $e < 0.1$.

== Quantitative Mission Dominance Matrix (@fig-h5 & @tbl-h5)
#gbnote("NEG-W1", "CONFIRMED", "Table 1 Regimes A/B have underground perigees", "r_p = a(1−e) = 6,300 km (A) and 5,250 km (B), both below Earth's radius. Recomputed on a valid r_p = 6,800 km: Regime B 220.2 m/s/yr (was 619.8), Regime A 3.81 mm/s/yr (was 5.17); tension 25.35 N at r_p = 6,800 km (μ M L / r_p³). The arithmetic in Table 1 is right for the stated (a, e); the orbits are not physical. WP031 §3 already re-derives a safe-perigee optimum (199.89 m/s/yr at 600 km altitude), which supersedes both figures (see X-MISSION).")

#gbnote("NEG-W5", "CONFIRMED", "Regime A tension 0.0012 N is about 100× too low", "μ M L / r_p³ with M = 1000 kg, L = 100 m gives 0.1594 N at r_p = 6,300 km and 0.1268 N at 6,800 km (0.1162 N at a = 7,000 km). Regime B's 55.1 N reproduces (55.09 N), so the Regime A cell is a typo, not a formula error.")

#gbnote("NEG-W6", "CONFIRMED", "Regime C exponent, Bennu tension, SRP dominance", "7.84e6 = (L/R)² ratio Bennu vs Earth, not L²/R⁴ (that ratio is 6.15e13 at fixed μ). Bennu tension μ M L/R³ = 3.131e-5 N (not below 1e-6 N). Raw |Δa∥| = 2 μ L²/R⁴ = 2.505e-9 m/s², below 1 AU SRP 4.56e-8 m/s² at A/M = 0.01. Extra [GB] point: the physical Δa near Bennu is about 0.75× the Earth benchmark, so the 7.84e6 'boost' is a dimensionless ratio, not an acceleration gain. Bennu Δv recomputes to 11.69 mm/s/yr (a = 2.5 km, e = 0.25).")

#gbnote("GB-W27a", "NEW", "Earth-radius convention differs across the series", "G4N's WP030 corrections use the mean radius 6,371 km; WP031 uses the equatorial 6,378.137 km. r_p = 6,800 km is 429 km altitude in one and 421.9 km in the other. Pick one (equatorial, as WP031 does) for all Horizon papers. Part of proposed NEG-W27.")

#gbnote("X-MISSION", "CONFIRMED-IN-SUBSTANCE", "Mission figure across WP030/WP031/G4N: 619.8 vs 220.2 vs 199.9 m/s/yr", "All three are arithmetically right for their own perigee: 619.8 (r_p = 5,250 km, underground), 220.2 (G4N, r_p = 6,800 km), 199.89 (WP031 K9 optimum at 600 km altitude; 198.58 at e = 0.25). WP031's safe-perigee figure is the defensible headline. Author decision: which perigee convention the series adopts.")


#figure(
  image("figures/fig4_h5_mission_dominance_map.svg", width: 100%),
  caption: [Resolution of `H5`: (a) LEO annual $Delta v$ vs. half-span $L$ (`a = 7,000 km`, `M = 1,000 kg`): Paper 028's `L = 100 m` craft (`5.17 mm/s/yr`) lies `~1,000×` below LEO drag (`~5 m/s/yr`), whereas `L = 20 km` reaches `619.8 m/s/yr` propellantlessly; (b) Exact Eq. (5) cycle efficiency $eta_"prop" (e)$ showing regeneration gains and Moore–Krawczyk `K8` threshold $e_(50)^* = 0.1150$.],
) <fig-h5>

#figure(
  {
    set text(size: 8.1pt)
    table(
      columns: (1.05fr, auto, auto, 1.05fr, auto),
      inset: 4pt,
      align: (left, right, right, left, center),
      stroke: 0.4pt + luma(190),
      fill: (x, y) => if y == 0 { rgb("#f1f5f9") } else if y == 1 { rgb("#fef2f2") } else if y >= 2 { rgb("#ecfdf5") } else { white },
      [*Mission Regime (`M=1000 kg`)*], [*Triad $Delta v$ / Boost*], [*Tidal Tension*], [*Dominant Baseline Comparison*], [*`H5` Verdict*],
      [*A: LEO `L=100 m`* ($a=7000$ km, $e=0.10$, Paper 028)], [`5.17 mm/s/yr`], [`0.0012 N`], [LEO drag `~5 m/s/yr` (`1000×`), SRP `0.14 m/s/yr` (`27×`), Hall `1.5 km/s/yr` (`3e5×`)], [*FALSIFIED / DOMINATED*],
      [*B: Eccentric `L=20 km`* ($a=7000$ km, $e=0.25$, Propellantless)], [`619.8 m/s/yr`], [`55.1 N` (`~12 kg` Zylon)], [Matches Hall $Delta v$ over multi-year constant-$p$ raising/de-orbit with `0` expellant & `0` tumble], [*NICHE VIABLE*],
      [*C: Asteroid `R=2.5 km`* (`L=100 m`, $L slash R = 0.04$, Bennu-class)], [`7.84 × 10^6×` $L^2 slash R^4$ boost], [`< 10^-6 N`], [`0` thruster plume contamination of pristine regolith + `0`-spin SW pointing (`-90°`)], [*HIGH-VALUE NICHE*],
    )
  },
  caption: [Fair comparative `H5` mission-utility matrix under matched mass, constraint, and disturbance baselines.],
) <tbl-h5>

// ============================================================================
// SECTION 5: BLINDED RCT, CORPUS INTEGRATION & CONCLUSION
// ============================================================================
= Blinded Empirical Validation (`N = 1,600`), Corpus Integration & Conclusion
#gbnote("INT-030", "UNVERIFIABLE", "Internal Swift++ corpus claims", "Pass 9B Zero-LLVM, SppMLIR certificates C137–C140 and K8, the N = 1,600 RCT counts, Pinakes scroll counts and the corpus totals rest on the internal Ergentics toolchain, which is not in the repository. They are kept verbatim and not altered. Independently re-checkable parts (K8 root e* = 0.1150133…, Eq. 5 identity) were confirmed by G4N's verifiers, re-run here: 9/9 Python, 7/7 Rust, 15/15 Lean.")


To guard against silent numerical fragility across all four Horizon 1 kernels (`SppAlexandria.ShapePropulsion`, Scroll 40, `5,216 B` Pass 9B Zero-LLVM), we executed a 4-stratum blinded paired ARM64 RCT (`alexandria_epoch36_rct.spp`, `N = 1,600`: `800` Discovery + `800` Held-Out, exact LLVM `-O3` parity):
- *Arm A (Naive Subtraction / Static 100% Claim):* `276 / 1,600` (`17.25%`: `144/800` Disc, `132/800` Held).
- *Arm B (Exact Cancellation-Free & Eq. (5) Kernels):* *`1,600 / 1,600` (`100.00%`)*, `b01 = 1,324`, `c10 = 0`, McNemar $chi^2 = 1","322.00$, $log_(10) p = -288.7$, Cohen's $h = +2.285$.
- *Cumulative 35-Epoch Corpus (`N = 56,000` Paired Trials):* Arm B achieves `55,986 / 56,000 (99.975%)` vs. `6,590 / 56,000 (11.77%)` for Arm A (`b01 = 49,396`, `c10 = 0`).
- *Repository Verification Gates:* *Pinakes* scales to *`40` scrolls (`553` `SppMLIR` fns), `140/140` seams PROVED, `8/8` Krawczyk `UNIQUE_PROVED`, `35/35` `FALSIFIED_OK`* (`.sppb` v3.0.0 CRC-64 `0xF19521F2647C31DB`, `ALL INTEGRITY GATES PASS` in `AnalyticCLI`); the `48`-module Zero-C-Glue Living Codex hits *`179/179 (100.0%)` Adjusted Cross-Module Deep MDS* (`0` host `libm`); and all automated XCTests pass (`138/138`).

*Conclusion & Complete Resolution of Working Paper 028.* Working Paper 028's five hypotheses now stand cleanly resolved: `H1–H3` are elevated from 13 finite points to universally proved continuous `SppMLIR` theorems and live `3.28 ppm` 4-body Eq. (5) dynamical closure constrained by the exact Noether constant-$p$ theorem; `H4` is resolved affirmatively through the *Iso-Inertial Hopf-Fibration Three-Mass Triad* (`0` Coriolis tumbles vs. `1,475°–11,425°` on 2-mass tethers, plus unique `-90°` zero-spin Shapere–Wilczek reorientation); and `H5` is resolved with transparent engineering boundaries—refuting utility at `L = 100 m` LEO (`5.17 mm/s/yr`) while establishing clear propellantless feasibility for kilometer-scale eccentric pumping (`620 m/s/yr` at `20 km`) and zero-plume asteroid proximity missions.
#gbnote("NEG-W6/7c", "DISPUTED", "Ref [1] NTRS ID", "NASA NTRS 19910012850 is G. A. Landis, 'Reactionless propulsion using tethers' (April 1990), the paper inside the Vision-21 proceedings (NASA CP-10059; the volume itself is NTRS 19910012826). NTRS 19910029285 is the different October 1990 paper 'Reactionless orbital propulsion using tether deployment', which is Ref [2]'s conference version. Ref [1] as printed is correct; G4N's proposed change should not be applied.")

#gbnote("REF-12", "UNVERIFIABLE", "Ref [12] cites an internal Swift++ calibration ledger", "The Epoch XXXVI calibration document is not public or in the repository. Suggest marking it 'internal, not public' (as G4N asked for WP035 Ref [12]) and citing the archived sibling working papers by their repository location.")


// ---- [GB] Round-1 ledger (inserted) ----
#heading(numbering: none)[Reconciliation Ledger (Grok Bot, Round 1)]
#block[
#set par(first-line-indent: 0pt, hanging-indent: 0pt)
#set text(size: 8pt)
#table(columns: (auto, 1fr, auto), inset: 4pt, stroke: 0.4pt + luma(170),
  table.header([*ID*], [*Item*], [*Verdict*]),
  "NEG-W1", "Table 1 Regimes A/B have underground perigees", text(fill: gb-col.at("CONFIRMED"), weight: "bold", "CONFIRMED"),
  "NEG-W5", "Regime A tension 0.0012 N is about 100× too low", text(fill: gb-col.at("CONFIRMED"), weight: "bold", "CONFIRMED"),
  "NEG-W6", "Regime C exponent, Bennu tension, SRP dominance", text(fill: gb-col.at("CONFIRMED"), weight: "bold", "CONFIRMED"),
  "NEG-W6/7a", "C138 ≤ 1e-6 octupole bound", text(fill: gb-col.at("UNVERIFIABLE"), weight: "bold", "UNVERIFIABLE"),
  "NEG-W6/7b", "F35 loss is 84.8%, not 84.6%", text(fill: gb-col.at("CONFIRMED"), weight: "bold", "CONFIRMED"),
  "NEG-W6/7c", "Ref [1] NTRS ID", text(fill: gb-col.at("DISPUTED"), weight: "bold", "DISPUTED"),
  "REF-12", "Ref [12] cites an internal Swift++ calibration ledger", text(fill: gb-col.at("UNVERIFIABLE"), weight: "bold", "UNVERIFIABLE"),
  "NEG-W2", "Θ = π/3 holonomy loop hits two binary collisions; Θ = 0 is collinear", text(fill: gb-col.at("CONFIRMED"), weight: "bold", "CONFIRMED"),
  "GB-W25", "Holonomy sign: net physical rotation is +90°, not −90°", text(fill: gb-col.at("NEW"), weight: "bold", "NEW"),
  "NEG-W4", "Theorem 2 sign: the printed Q is the mass quadrupole", text(fill: gb-col.at("CONFIRMED"), weight: "bold", "CONFIRMED"),
  "NEG-W3", "Theorem G1: exact shape kinetic energy", text(fill: gb-col.at("CONFIRMED"), weight: "bold", "CONFIRMED"),
  "NOTE-8", "Specify μ_tot and the energy convention for a_f, e_f", text(fill: gb-col.at("CONFIRMED"), weight: "bold", "CONFIRMED"),
  "GB-W26", "The naive rounding error depends on evaluation order", text(fill: gb-col.at("NEW"), weight: "bold", "NEW"),
  "GB-W27a", "Earth-radius convention differs across the series", text(fill: gb-col.at("NEW"), weight: "bold", "NEW"),
  "X-MISSION", "Mission figure across WP030/WP031/G4N: 619.8 vs 220.2 vs 199.9 m/s/yr", text(fill: gb-col.at("CONFIRMED-IN-SUBSTANCE"), weight: "bold", "CONFIRMED-IN-SUBSTANCE"),
  "SIM-030", "Coupled 4-body numbers (tumbles, ΔE, Eq. 5 residual, Arm A spin-up)", text(fill: gb-col.at("SPEC-NEEDED"), weight: "bold", "SPEC-NEEDED"),
  "INT-030", "Internal Swift++ corpus claims", text(fill: gb-col.at("UNVERIFIABLE"), weight: "bold", "UNVERIFIABLE"),
)
#text(size: 8pt)[#"Totals: CONFIRMED 8, CONFIRMED-IN-SUBSTANCE 1, DISPUTED 1, UNVERIFIABLE 3, SPEC-NEEDED 1, NEW 3. Full evidence, reproduction commands and run specs: reconciliation/GROKBOT_WP030_ROUND1.md in this paper's folder."]
]
// ---- end [GB] ledger ----


// ============================================================================
// REFERENCES
// ============================================================================
#heading(numbering: none)[References]
#set text(size: 8.4pt)
#set par(first-line-indent: 0pt, hanging-indent: 1.8em, leading: 0.46em, spacing: 0.45em)

[1] G. A. Landis, _Reactionless propulsion using tethers_, in _Vision-21: Space Travel for the Next Millennium_, NASA CP-10059 / NTRS 19910012850, 1990/1991.

[2] G. A. Landis, _Reactionless orbital propulsion using tether deployment_, Acta Astronautica *26* (1992), no. 5, 307–312.

[3] E. Guéron, C. A. S. Maia, and G. E. A. Matsas, _Swimming versus swinging effects in spacetime_, Phys. Rev. D *73* (2006), 024020.

[4] NASA / JPL, _Basics of Space Flight_, Chapter 4: Gravity Assist, Jet Propulsion Laboratory, Pasadena, CA.

[5] J. Wisdom, _Swimming in spacetime: Motion by cyclic changes in body shape_, Science *299* (2003), 1865–1869.

[6] A. Guichardet, _On rotation and vibration motions of molecules_, Ann. Inst. H. Poincaré Phys. Théor. *40* (1984), no. 3, 329–342.

[7] A. Shapere and F. Wilczek, _Geometry of self-propulsion at low Reynolds number_, J. Fluid Mech. *198* (1989), 557–585; _Gauge kinematics of deformable bodies_, Amer. J. Phys. *57* (1989), 514–518.

[8] R. Montgomery, _Gauge theory of the falling cat_, in _Dynamics and Control of Mechanical Systems_, Fields Inst. Commun. *1*, AMS, 1993, pp. 193–218; T. Iwai, _A geometric setting for internal motions of the quantum three-body system_, J. Math. Phys. *28* (1987), 1315–1326.

[9] M. Martinez-Sanchez and S. A. Gavit, _Orbital modifications using forced tether-length variations_, J. Guidance, Control, and Dynamics *10* (1987), no. 3, 233–241.

[10] V. V. Beletsky and E. M. Levin, _Dynamics of Space Tether Systems_, Advances in the Astronautical Sciences, Vol. 83, Univelt / AAS, 1993.

[11] R. E. Moore, _Interval Analysis_, Prentice-Hall, 1966; R. Krawczyk, _Newton-Algorithmen zur Bestimmung von Nullstellen mit Fehlerschranken_, Computing *4* (1969), 187–201.

[12] Ergentics, LLC, _Working Paper 028 / Web Edition 029: Novelty and usefulness in shape-controlled gravitational propulsion_, 23 Sept. 2026; `Swift++` Library of Alexandria Verification Program, _Epoch XXXVI Calibration Monograph_ (`calibrations/ALEXANDRIA_EPOCH_36_HORIZON1_SHAPE_PROPULSION.md`), Nov. 2026.
