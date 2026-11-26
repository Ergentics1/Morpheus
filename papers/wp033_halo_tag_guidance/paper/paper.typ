// [GB] Round-1 reconciled edition: clean-room [E] text unchanged, with inserted reconciliation notes.
// Working Paper 033 / Horizon Series Monograph ID (Swift++ Library of Alexandria Epoch XXXIX)
// Full 3D Non-Planar Extended-Body CRTBP Halo/Lissajous Manifolds & Bennu TAG Regolith Sampling Guidance
// Compile: typst compile paper.typ paper.pdf
// Copyright (c) 2026 Ergentics, LLC -- MIT License

#set document(
  title: "Full 3D Non-Planar Extended-Body CRTBP Halo and Lissajous Invariant Manifolds, Rotating-Symplectic Floquet Station-Keeping, and Bennu Touch-and-Go Regolith Sampling Guidance",
  author: "Ergentics, LLC & Swift++ Library of Alexandria Verification Program",
)

#set page(
  paper: "us-letter",
  margin: (x: 0.78in, y: 0.76in),
  numbering: "1",
  number-align: center,
  header: context {
    if counter(page).get().first() > 1 {
      set text(size: 8.2pt, fill: luma(95), style: "italic")
      grid(
        columns: (1fr, auto),
        [3D Non-Planar CRTBP Halo/Lissajous Manifolds & Bennu TAG Guidance],
        [Ergentics Working Paper 033 · Horizon Monograph ID],
      )
      v(-6pt)
      line(length: 100%, stroke: 0.4pt + luma(180))
    }
  },
)

#set text(
  font: "New Computer Modern",
  size: 9.7pt,
  lang: "en",
)

#set par(
  justify: true,
  leading: 0.54em,
  first-line-indent: 1.2em,
)

#set heading(numbering: "1.1")
#show heading.where(level: 1): it => {
  v(10pt, weak: true)
  set text(size: 11.4pt, weight: "bold", fill: rgb("#0f172a"))
  block(breakable: false)[#it]
  v(3.5pt, weak: true)
}
#show heading.where(level: 2): it => {
  v(8pt, weak: true)
  set text(size: 10.1pt, weight: "bold", fill: rgb("#1e293b"))
  block(breakable: false)[#it]
  v(3pt, weak: true)
}

#show table: set par(justify: false)
#show raw.where(block: false): it => if it.text == "Swift++" { box(it) } else { it }
#show figure.caption: it => {
  set text(size: 8.4pt, fill: luma(55))
  set par(leading: 0.48em, justify: true)
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
  v(4pt, weak: true)
}

// ============================================================================
// TITLE BLOCK
// ============================================================================
#align(center)[
  #text(size: 7.7pt, weight: "bold", tracking: 0.03em, fill: rgb("#1e3a8a"))[
    ERGENTICS WORKING PAPER 033 · HORIZON SERIES MONOGRAPH ID · SWIFT++ ALEXANDRIA EPOCH XXXIX
  ]
  #v(5pt)
  #text(size: 14.2pt, weight: "bold", fill: rgb("#0f172a"))[
    Full 3D Non-Planar Extended-Body CRTBP Halo and Lissajous Invariant Manifolds, Rotating-Symplectic Floquet Station-Keeping, and Bennu Touch-and-Go Regolith Sampling Guidance
  ]
  #v(6pt)
  #text(size: 9.8pt, fill: rgb("#334155"))[
    Ergentics, LLC & The `Swift++` Library of Alexandria Verification Program
  ]
  #v(2pt)
  #text(size: 8.8pt, fill: luma(100))[
    26 November 2026 · Extension of Working Papers 030–032 (Horizons I–IC) · MIT License · Zero External Dependencies
  ]
]

#v(5pt)
#block(
  width: 100%,
  inset: (x: 12pt, y: 8pt),
  fill: rgb("#f8fafc"),
  stroke: 0.6pt + rgb("#cbd5e1"),
  radius: 4pt,
)[
  #set par(first-line-indent: 0pt, leading: 0.50em)
  #text(size: 8.9pt)[
    *Abstract.* Working Paper 032 (Horizon IC) established Bennu triaxial $C_(22)$ active Jacobi breaking, a live 16-node 3D flexible-tether FEM with zero-slack winch-jam FDIR, and planar extended-body CRTBP $L_4 \/ L_5$ Gascheau–Routh stabilization (`K10`). This monograph pushes both astrodynamics and small-body flight guidance into full three-dimensional non-planar space: *(i) Exact 3D Collinear $L_1 \/ L_2$ Halo–Lissajous Resonance (`C149`, `K11`)* — certifying the Earth–Moon $L_2$ Euler quintic via Moore–Krawczyk `K11` ($gamma_2^* = 0.1678327510078692$, `64,514.91 km` past the Moon, width $1.94 times 10^(-16)$) and proving the cancellation-free zero-amplitude Halo resonance gap $k_z^*(c_2) = 2(1-s)/(3 - 2 s + sqrt(9 - 8 s))$ (`0.279024` at Earth–Moon $L_2$), while candidly auditing that Earth–Moon `20 km` triads ($2 varepsilon^2 = 1.92 times 10^(-7)$) remain far below $k_z^*$ whereas binary-asteroid *Didymos–Dimorphos $L_2$* (`50 m` triad at $d_(L 2) = 180.5$ m) leaps `7.98e5x` to $2 varepsilon^2 = 0.1535$; *(ii) Live 42-ODE 3D Earth–Moon $L_2$ Halo Differential Corrector, $6 times 6$ Rotating-Symplectic Monodromy & $W^u$ Lunar Tube (`C150`)* — converging in `4` iterations (`< 1e-12`) to a Northern Halo ($A_z = 30","752$ km, $T = 14.6152$ d, $|Delta C_J| = 5.40 times 10^(-12)$, exact rotating symplectic form $norm(M^top Omega M - Omega)_infinity = 2.18 times 10^(-8)$), extracting Broucke indices $nu_1 = 373.3613$ ($lambda_u = 746.7213$, `C150`) and $nu_2 = 0.8409$ (`32.8 deg/orbit` 3D Lissajous torus), and tracing $W^u$ down to `1,003.7 km` from the Moon's center; *(iii) Rotating-Symplectic Floquet Station-Keeping* — transporting the left unstable eigenvector via $bold(w)_u (T/2) = Omega Phi(T/2) Omega^(-1) bold(w)_u (0)$ crushes a `231,028 km` uncontrolled 2-orbit blowup down to `75.71 km` across `4` full orbits (`58.5 d`, `3,051.3x` reduction) for `0.3616 m/s` (`~2.26 m/s/yr`, Gateway class) and stabilizes a live precessing 3D Lissajous torus; *(iv) Authentic OSIRIS-REx Bennu Nightingale Crater TAG Guidance (`C151`, `C152`, `F38`)* — proving open-loop `100 m` descent at `+56 deg N` drifts `19.23 m` laterally off the `8 m` safe zone (`F38`, witness $h^* = 114.37$ m, exact gravity-shortening law `C151`), whereas closed-loop ZEM/ZEV + zero-plume pendulous tether-winch TAG lands at `0.0000 m`, penetrates `10.85 cm` into fluidized regolith (matching closed-form quadratic-drag law `C152` `11.58 cm`, `~4.5x` gentler than OSIRIS-REx's `48.8 cm` craft sink), and winch-retracts at `0.191 m/s` (`0` slack); and *(v) Live 200-Trial TAG Monte Carlo* — hitting `200/200 (100.0%)` safe Nightingale touchdowns (`max_miss = 0.0003 m`, `mean_sink = 9.67 cm`, `0` slack) vs. `11/200 (5.5%)` open-loop. Certified on Pass 9B Zero-LLVM ARM64 (`Pinakes` `152/152`, `11/11` Krawczyk, `38/38` falsifications, `51/51` Living Codex `191/191` Deep MDS, `60,800` RCT trials, `141/141` XCTests).
  ]
]


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
  #"The text of Working Paper 033 below is the frozen clean-room manuscript, unchanged. Boxed notes are Grok Bot ([GB]) Round-1 verdicts on the Gemini 4 Neon ([G4N]) Cycle-1 catches and on new [GB] items. Claims that rest on the internal Swift++ corpus are left exactly as written and marked UNVERIFIABLE. Corrections are proposed, not applied in the text; the author decides. A ledger of all verdicts is at the end."
]
// ---- end [GB] layer header ----

= Introduction: From Planar $L_4$ to 3D Non-Planar Halo Manifolds and Small-Body Touch-and-Go

Working Papers 030–032 (Horizons I–IC) [1]–[3] resolved planar quadrupole switching, collinear-bridge $"SO"(3)$ holonomy, Earth $J_2$ symmetry breaking, real OSIRIS-REx Bennu triaxial $C_(22)$ active Jacobi breaking, 16-node 3D multi-tether FEM + winch-jam FDIR, and planar extended-body CRTBP $L_4 \/ L_5$ Gascheau–Routh stabilization (`K10`). Two flagship challenges sit directly beyond Horizon IC:

1. *Full 3D Non-Planar Collinear $L_1 \/ L_2$ Halo/Lissajous Manifolds & Symplectic Floquet Control:* Unlike triangular $L_4 \/ L_5$, collinear libration points $L_1$ and $L_2$ are inherently unstable saddle-center-center equilibria whose infinitesimal 3D orbits are quasi-periodic *Lissajous* trajectories ($omega_(x y) > omega_z$) until finite nonlinear $z$-amplitude triggers the Richardson *Halo* bifurcation [4], [5]. What exact anisotropic vertical quadrupole stiffness $k_z^*(c_2)$ collapses this bifurcation to zero amplitude, where in the Solar System is finite-size shape control strong enough to matter, and how cleanly can zero-dependency Pass 9B Zero-LLVM ARM64 compute a 42-ODE differential-corrected 3D Halo orbit, verify its *rotating-frame* symplectic monodromy form $M^top Omega M = Omega$, trace its lunar unstable manifold $W^u$, and execute multi-orbit Floquet station-keeping [6], [7]?
2. *Zero-Plume Bennu Touch-and-Go (TAG) Regolith Sampling Guidance:* NASA's OSIRIS-REx TAG maneuver at Bennu's `8 m` boulder-free Nightingale crater (`+56 deg N`) revealed ultra-low-cohesion fluidized regolith ($< 1$ Pa) in which the spacecraft sank `48.8 cm` and excavated a `~9 m` crater during thruster back-away [8], [9]. Can a hovering `100 m` triad lower a `5 kg` pendulous TAGSAM head via closed-loop Coriolis-compensated ZEM/ZEV + winch guidance [10] to achieve `100%` safe pinpoint touchdown, controlled shallow penetration, and zero-plume retraction?

This monograph resolves both frontiers via three theorems, one Monte Carlo proposition, zero-dependency Pass 9B Zero-LLVM `Swift++` Scroll 43 (`HaloTagGuidance.spp`) and live 5-pillar suite (`halo_lissajous_bennu_tag_suite.spp`), universal `SppMLIR` Interval-AD certification (`C149`–`C152`, `K11`, `F38`) [11], [12], and clean-room Python cross-verification (`[X]`).

= 3D Collinear $L_1 \/ L_2$ Halo–Lissajous Resonance (`C149`, `K11`) & Scale Audit
#gbnote("NEG-W11", "CONFIRMED", "The W^u 'lunar tube' passes inside the Moon", "1,003.71 km from the Moon's centre is 733.7 km below the surface. In the re-run, a 1e-4 kick along +v_u hits the lunar surface at about 17.4 days; along −v_u it stays 47,315 km away. The branch the paper shows is an impact trajectory.")

#gbnote("NEG-W12", "CONFIRMED", "Theorem G3 coupled stiffness and gap sensitivities", "Gap sensitivities +0.0802, −2.3748, +2.2946, −1.1473 (x, y, z, equilateral) reproduce exactly. L_y* = 40.44 m was not independently recomputed.")


Near a collinear CRTBP equilibrium $L_1$ or $L_2$ with Legendre coefficient $c_2 = (1 - mu)/abs(x_L + mu)^3 + mu/abs(x_L - 1 + mu)^3 > 1$, linearized 3D point-mass dynamics satisfy $dot.double(x) - 2 dot(y) = (1 + 2 c_2) x$, $dot.double(y) + 2 dot(x) = (1 - c_2) y$, and $dot.double(z) = -c_2 z$ [4], [5].

#theorem(title: [Earth–Moon $L_2$ Quintic `K11`, Cancellation-Free Halo Resonance `C149` & Binary-Asteroid Audit])[
  Let $s = 1 / c_2 in (0, 1/3]$ denote the inverse Legendre coefficient at a collinear CRTBP equilibrium, and suppose an active out-of-plane quadrupole shifts the vertical stiffness to $dot.double(z) = -(c_2 + k_z) z$:
  1. *(Moore–Krawczyk `K11` — Earth–Moon $L_2$ Euler Quintic)* For Earth–Moon mass ratio $mu_"EM" = 0.0121505856$, the collinear $L_2$ distance $gamma_2 = x_(L 2) - (1 - mu_"EM")$ satisfies $gamma^5 + (3 - mu) gamma^4 + (3 - 2 mu) gamma^3 - mu gamma^2 - 2 mu gamma - mu = 0$. Moore–Krawczyk `K11` certifies the unique root over compiled `SppMLIR` in `4` iterations:
  $ gamma_2^* in [0.1678327510078691, 0.1678327510078693] quad ("width" = 1.943 times 10^(-16)), $
  placing Earth–Moon $L_2$ at `64,514.91 km` past the Moon ($x_(L 2) = 1.1556821654$, $c_2 = 3.19042521$).
  2. *(Exact Cancellation-Free Zero-Amplitude Halo Resonance — Seam `C149`)* Matching vertical frequency $omega_z (k_z) = sqrt(c_2 + k_z)$ to planar center frequency $omega_(x y) = sqrt((2 - c_2 + sqrt(9 c_2^2 - 8 c_2)) / 2)$ collapses the Richardson Halo bifurcation threshold to zero amplitude at exact stiffness
  $ k_z^*(c_2) = omega_(x y)^2 - c_2 = (2 (1 - s)) / (3 - 2 s + sqrt(9 - 8 s)), quad cal(R)_"halo" (s) = 3 k_z^*(s) = (6 (1 - s)) / (3 - 2 s + sqrt(9 - 8 s)) arrow.hook 1 - (4 / 9) s, $
  universally certified over $s in [10^(-4), 0.15]$ by `1D Jet2` seam `C149` (`7` boxes, $|"defect"| <= 4.954 times 10^(-3) <= 5.000 times 10^(-3)$), giving $k_z^* = 0.27902439$ at Earth–Moon $L_2$ (`0.291503` in the Hill limit $c_2 = 4$, asymptote $1/3$).
  3. *(Honest Physical Scale Audit: Earth–Moon vs. Didymos–Dimorphos)* At Earth–Moon $L_2$ ($d_(L 2) = 64","515$ km), a `20 km` triad has $2 varepsilon^2 = 1.92 times 10^(-7) << k_z^*$: Earth–Moon Halo orbits therefore strictly require finite Richardson amplitude and micro-thruster station-keeping. In contrast, at the NASA DART / ESA Hera binary asteroid *Didymos–Dimorphos* $L_2$ ($mu = 0.0091$, $R_"sep" = 1","190$ m, $d_(L 2) = 180.50$ m), a `50 m` triad reaches $2 varepsilon^2 = 0.1535$ — a `7.9841e5x` (`~800,000x`) authority leap directly into the $O(k_z^*)$ active Halo regime!
]

#proof[
  Rationalizing $omega_(x y)^2 - c_2 = (2 - 3 c_2 + sqrt(9 c_2^2 - 8 c_2))/2$ by multiplying numerator and denominator by $(sqrt(9 c_2^2 - 8 c_2) + 3 c_2 - 2)$ yields $[(9 c_2^2 - 8 c_2) - (9 c_2^2 - 12 c_2 + 4)] / [2(3 c_2 - 2 + sqrt(9 c_2^2 - 8 c_2))] = 2(c_2 - 1)/(3 c_2 - 2 + sqrt(9 c_2^2 - 8 c_2))$; dividing by $c_2$ with $s = 1/c_2$ gives $k_z^*(s) = 2(1-s)/(3 - 2 s + sqrt(9 - 8 s))$, eliminating catastrophic cancellation as $c_2 -> infinity$. Expanding $sqrt(9 - 8 s) = 3 - (4/3) s + O(s^2)$ yields $3 k_z^*(s) = (1 - s)/(1 - (5/9) s + O(s^2)) = 1 - (4/9) s + O(s^2)$ (`C149`). Evaluating $2(L/d_(L 2))^2$ at Earth–Moon ($20 / (64","515)$) vs. Didymos–Dimorphos ($50 / 180.50$) yields $1.922 times 10^(-7)$ vs. $0.1535$ (`7.9841e5x` ratio).
]

#figure(
  image("figures/fig1_l2_halo_resonance_and_didymos.svg", width: 100%),
  caption: [*3D Collinear $L_1 \/ L_2$ Halo–Lissajous Resonance & Honest Physical Scale Audit (`C149`, `K11`).* (A) Exact cancellation-free vertical stiffness $k_z^*(c_2) -> 1/3$ required to collapse the Richardson Halo bifurcation to zero amplitude, marking Earth–Moon $L_2$ (`K11`, $c_2 = 3.19, k_z^* = 0.279$) and the Hill limit ($c_2 = 4$). (B) Honest scale audit: Earth–Moon `20 km` triads ($1.92 times 10^(-7)$) sit six orders of magnitude below $k_z^*$, whereas *Didymos–Dimorphos* binary-asteroid $L_2$ (`50 m` triad at `180.5 m`) leaps `8e5x` to `0.1535`, directly entering the active $O(k_z^*)$ Halo-shaping regime.]
)

= Live 42-ODE 3D Halo Differential Corrector, Rotating-Symplectic Monodromy & Floquet Control (`C150`)
#gbnote("HALO-RERUN", "CONFIRMED", "Independent halo re-run from the paper's state", "Closure 1.6e-8, C_J = 3.12579292, λ_u = 746.7213, ν1 = 373.3613, ν2 = 0.84093, winding 32.76°/orbit: all reproduce. Symplectic residual 7.8e-11 with a tight-tolerance adaptive integrator; the paper's printed residual is larger, which is integrator-dependent and not an error.")

#gbnote("SIM-033", "SPEC-NEEDED", "Station-keeping (3,051× vs 3,442×), W^u kick, TAG Monte Carlo", "Depend on noise seed, burn schedule, kick direction and size. Run spec in the dossier.")


To move beyond linear approximations, `halo_lissajous_bennu_tag_suite.spp` integrates all `42` coupled nonlinear ODEs — the 6D rotating CRTBP state $bold(x) = (x, y, z, dot(x), dot(y), dot(z))^top$ and its $6 times 6$ variational State Transition Matrix (STM) $dot(Phi) = A(bold(x)) Phi$ — via 4th-order RK4 directly in Pass 9B Zero-LLVM ARM64 (`host_libm = 0`).

#theorem(title: [Rotating-Symplectic Monodromy Invariance (`C150`), $W^u$ Tube & Floquet Projection Station-Keeping])[
  Let $bold(x)^*(t)$ be a symmetric $T$-periodic 3D nonlinear Earth–Moon $L_2$ Halo orbit ($x_0 = 1.1734236346$, $z_0 = 0.0800$ [$30","752$ km], $dot(y)_0 = -0.1845292585$, $T = 3.36106913$ rad $= 14.6152$ d, $C_J = 3.12579292$) with monodromy matrix $M = Phi(T, 0)$:
  1. *(Rotating-Frame Symplectic Form $Omega$)* Because rotating-frame canonical momenta are $p_x = dot(x) - y$, $p_y = dot(y) + x$, $p_z = dot(z)$ (transformation $S = mat(I, 0; -K, I)$ with $K_(12) = 1, K_(21) = -1$), the exact symplectic form in $(bold(q), dot(bold(q)))$ coordinates is $Omega = S^top J S = mat(-2 K, I; -I, 0)$ (NOT standard $J$), satisfying $Phi(t, 0)^top Omega Phi(t, 0) = Omega$ identically! In live `800`-step RK4 verification, $norm(M^top Omega M - Omega)_infinity = 2.1772 times 10^(-8)$ and $|Delta C_J| = 5.4015 times 10^(-12)$.
  2. *(Closed-Form Broucke Trace Invariants & Seam `C150`)* From $tr(M)$ and $tr(M^2)$ alone (zero external eigensolver!), setting $S_nu = (tr(M) - 2)/2$ and $P_nu = (S_nu^2 - (tr(M^2) + 2)/4)/2$ extracts the exact Broucke stability indices $nu_1 = 373.3613$ (hyperbolic saddle) and $nu_2 = 0.8409 in [-1, 1]$ (confirming a 3D quasi-periodic *Halo–Lissajous torus* with exact winding angle $arccos(nu_2) = 32.76 degree$/orbit) [6]. With $u = 1/(2 nu_1)$, the Floquet multiplier obeys the cancellation-free law
  $ (lambda_u) / (2 nu_1) = (1 + sqrt(1 - 4 u^2)) / 2 arrow.hook 1 - u^2 quad (u -> 0^+), $
  certified over $u in [10^(-4), 0.25]$ by `1D Jet2` seam `C150` (`9` boxes, $|"defect"| <= 4.875 times 10^(-3) <= 5.000 times 10^(-3)$), yielding $lambda_u = 746.7213$ ($e$-folding horizon `2.209 d`). Launching a $10^(-4)$ kick along $-bold(v)_u$ follows the unstable manifold tube $W^u$ ballistically down to `1,003.71 km` from the Moon's center [7].
  3. *(Exact Symplectic Left-Eigenvector Transport & Floquet Station-Keeping)* The left unstable eigenvector $bold(w)_u (0)$ ($M^top bold(w)_u = lambda_u bold(w)_u$) transports to any phase $t$ without matrix inversion via
  $ bold(w)_u (t) = Phi(t, 0)^(-top) bold(w)_u (0) = Omega Phi(t, 0) Omega^(-1) bold(w)_u (0). $
  Applying min-norm half-orbit burns $Delta bold(v) = -((bold(w)_u^top delta bold(x)) / norm(bold(w)_(u,v))^2) bold(w)_(u,v)$ under a `1 km + 1 mm/s` navigation error crushes an uncontrolled 2-orbit `231,027.7 km` blowup down to `75.71 km` across `4` full orbits (`58.5 d`, `3,051.3x` reduction) for just `0.3616 m/s` (`~2.26 m/s/yr`, Lunar Gateway / ARTEMIS class) [10], and stabilizes a live precessing 3D Halo–Lissajous torus ($z_4 = 0.0735$).
]

#proof[
  In canonical coordinates $bold(z)_c = S bold(x)$, Hamilton's equations preserve $J$, so $M_c^top J M_c = J$ with $M_c = S M S^(-1) => M^top (S^top J S) M = S^top J S = Omega$, and taking transpose inverses gives $Phi^(-top) = Omega Phi Omega^(-1)$ directly. Because a $6 times 6$ symplectic monodromy matrix of a periodic orbit has trivial pair $(1, 1)$ plus reciprocal pairs $(lambda_1, lambda_1^(-1))$ and $(lambda_2, lambda_2^(-1))$ with $2 nu_k = lambda_k + lambda_k^(-1)$, Newton's identities yield $tr(M) = 2 + 2(nu_1 + nu_2)$ and $tr(M^2) = 2 + (4 nu_1^2 - 2) + (4 nu_2^2 - 2) = 4(nu_1^2 + nu_2^2) - 2$, giving $S_nu, P_nu$ in closed form. Finally, $lambda_u = nu_1 + sqrt(nu_1^2 - 1) = 2 nu_1 (1 + sqrt(1 - 4 u^2))/2 = 2 nu_1 (1 - u^2 - u^4 - dots)$ proves `C150`. All differential-correction, $W^u$ lunar tube, Floquet station-keeping, and 3D torus metrics agree across Pass 9B Zero-LLVM `halo_lissajous_bennu_tag_suite.spp` and clean-room `verify_all_results.py`.
]

#figure(
  image("figures/fig2_3d_halo_monodromy_and_manifolds.svg", width: 100%),
  caption: [*Live 42-ODE 3D Earth–Moon $L_2$ Halo Orbit, $W^u$ Lunar Tube & 3D Lissajous Torus (`C150`).* (A) Converged Northern Halo ($A_z = 30","752$ km, $T = 14.62$ d, residual `< 1e-12`, $|Delta C_J| = 5.40 times 10^(-12)$) and ballistic unstable manifold $W^u$ plunging to `1,003.7 km` from the Moon's center. (B) Live 4-orbit (`58.5 d`) 3D quasi-periodic Halo–Lissajous torus (`y–z` projection) winding at exact center angle $arccos(nu_2) = 32.8 degree$/orbit around the periodic Halo core.]
)

#figure(
  image("figures/fig3_floquet_stationkeeping_vs_uncontrolled.svg", width: 100%),
  caption: [*Rotating-Symplectic Floquet-Mode Station-Keeping vs. Uncontrolled Divergence.* (A) Under `1 km + 1 mm/s` navigation dispersion, uncontrolled flight explodes to `231,028 km` within `2` orbits, whereas half-orbit Floquet projection locks drift below `75.7 km` across `4` full orbits (`58.5 d`, `3,051.3x` reduction). (B) Eight half-orbit burns (`every 7.3 d`) total only `36.16 cm/s = 0.3616 m/s` (`~2.26 m/s/yr`, matching Lunar Gateway/ARTEMIS budgets).]
)

= Bennu (101955) Nightingale Crater TAG Guidance, Coriolis Cliff (`F38`) & Regolith Contact (`C151`, `C152`)
#gbnote("NEG-W13", "CONFIRMED", "Regolith density and C_D", "χ(600) = 10.886, sink 18.24 cm. C_D = 1.60 could not be re-derived because the contact area is not stated.")

#gbnote("NEG-W14", "CONFIRMED", "Certified intervals vs the operating regime", "η is 8.08× and χ 144× outside the certified intervals; constant-g drift 15.99 m; centrifugal relief 1.27e-5 m/s² = 15.7% of g.")


NASA's OSIRIS-REx mission sampled Bennu's `8.0 m` boulder-free Nightingale crater (latitude $phi = +56 degree$ N, $mu_B = 4.892 "m"^3/"s"^2$, $R_B = 246$ m, $omega_B = 4.0627 times 10^(-4)$ rad/s, surface gravity $g_"surf" = 8.084 times 10^(-5) "m/s"^2 = 8.24 mu g_0$) [8], [9], revealing fluidized near-zero-cohesion regolith ($c_"reg" < 1$ Pa, $rho_"reg" approx 1","190 "kg/m"^3$) where the spacecraft sank `48.8 cm` before thruster back-away excavated a `~9 m` crater. Here we analyze a *zero-plume pendulous tether-winch TAG architecture*: our hovering `100 m` triad stays safely at $R = 346$ m (`100 m` altitude) while lowering a `5.0 kg`, `30 cm`-diameter TAGSAM head ($A_h = 0.0707 "m"^2$) into Nightingale crater under closed-loop Coriolis-compensated ZEM/ZEV + winch guidance [10].

#theorem(title: [Bennu Rotating-Frame Coriolis Drift `C151`, Crater-Miss Falsification `F38` & Granular Penetration `C152`])[
  Consider vertical descent from altitude $h$ at initial downward speed $v_0$ toward a Bennu target at latitude $phi$ under effective gravity $g$ (drop parameter $eta = 2 g h / v_0^2$), followed by impact at speed $v_t$ into fluidized granular regolith with net constant bearing/preload acceleration $a_0 = (A_h c_"reg" + T_w - m_h g_"surf") / m_h > 0$ and quadratic granular drag $alpha v^2$ ($alpha = C_D rho_"reg" A_h / (2 m_h)$, drag number $chi = alpha v_t^2 / a_0$):
  1. *(Exact Coriolis Gravity-Shortening Law — Seam `C151`)* Under constant-speed descent, Bennu's rotation deflects the sampler eastward by $Delta x_0 = omega_B cos(phi) h^2 / v_0$ (`22.72 m` at $h = 100$ m, $v_0 = 0.10$ m/s, $phi = 56 degree$). Gravity accelerates the descent and shortens fall time by the exact cancellation-free factor
  $ (Delta x_"Cor" (eta)) / (Delta x_0) = (4 (2 + sqrt(1 + eta))) / (3 (sqrt(1 + eta) + 1)^2) arrow.hook 1 - (1 / 3) eta quad (eta -> 0^+), $
  universally certified over $eta in [10^(-4), 0.20]$ by `1D Jet2` seam `C151` (`7` boxes, $|"defect"| <= 6.837 times 10^(-3) <= 7.000 times 10^(-3)$).
  2. *(Open-Loop Crater-Miss Falsification — `F38`)* Despite gravity shortening, unguided vertical descent from $h in [75, 130]$ m strictly violates Nightingale's `8.0 m` boulder-free radius (`19.23 m` live open-loop drift at $h = 100$ m $= 2.40 times$ crater radius), mechanically falsified by `F38` (witness $h^* = 114.37$ m).
  3. *(Exact Fluidized Granular Penetration Law — Seam `C152`)* Solving $m_h v (dif v)/(dif z) = -(m_h a_0 + m_h alpha v^2)$ yields exact peak penetration depth
  $ z_"max" = (v_t^2) / (2 a_0) dot cal(P)_"reg" (chi), quad cal(P)_"reg" (chi) = (ln(1 + chi)) / chi arrow.hook 1 - (1 / 2) chi quad (chi -> 0^+), $
  universally certified over $chi in [10^(-3), 0.15]$ by `1D Jet2` seam `C152` (`65` boxes, $|"defect"| <= 6.880 times 10^(-3) <= 7.000 times 10^(-3)$). For a `5 kg` tethered head ($v_t = 0.090$ m/s, $c_"reg" = 0.08$ Pa, $T_w = 0.02$ N, $chi = 21.59$), quadratic granular drag slashes stopping depth from $80.2$ cm (constant-force) down to `11.58 cm` (`10.85 cm` in live simulation with depth-hydrostatic overburden) — `~4.5x` gentler than OSIRIS-REx's `48.8 cm` full-craft sink — followed by clean `0.1908 m/s` zero-plume winch retraction with `0` tether slack!
]

#proof[
  With $z(t) = h - v_0 t - (1/2) g t^2$, exact fall time is $T = (2 h / v_0)/(sqrt(1 + eta) + 1)$. Integrating eastward Coriolis acceleration $dot.double(x) = -2 omega_B cos(phi) dot(z) = 2 omega_B cos(phi)(v_0 + g t)$ twice gives $x(T) = 2 omega_B cos(phi)[(1/2) v_0 T^2 + (1/6) g T^3]$. Substituting $(1/2) g T^2 = h - v_0 T$ yields $x(T) = 2 omega_B cos(phi) T (h/3 + v_0 T/6) = (omega_B cos(phi) h^2 / v_0) dot [4(2 + sqrt(1 + eta))/(3(sqrt(1 + eta) + 1)^2)]$, whose expansion with $sqrt(1 + eta) = 1 + eta/2 + O(eta^2)$ gives $(1 + eta/6)/(1 + eta/2) = 1 - eta/3 + O(eta^2)$ (`C151`). Separating $v (dif v)/(a_0 + alpha v^2) = -dif z$ and integrating from $v_t$ to $0$ gives $z_"max" = (2 alpha)^(-1) ln(1 + alpha v_t^2 / a_0) = (v_t^2 / (2 a_0)) ln(1 + chi)/chi$ (`C152`).
]

#proposition(title: [Live 200-Trial Bennu Nightingale TAG Monte Carlo Stress Test & Snagging Caveat])[
  Across `200` randomized rotating-frame Bennu Nightingale descents (`+-6 m` initial lateral offset, `+-1.5 cm/s` velocity error, fluidized regolith cohesion $c_"reg" in [0.02, 0.50]$ Pa) executed in Pass 9B Zero-LLVM `halo_lissajous_bennu_tag_suite.spp`:
  1. *Open-Loop Uncompensated TAG:* Only `11/200 (5.5%)` land inside the `8.0 m` boulder-free zone (Coriolis drift centers impact `19.2 m` east in the boulder field, `F38`).
  2. *Closed-Loop ZEM/ZEV + Pendulous Tether-Winch TAG:* Achieves `200/200 (100.0%)` safe Nightingale touchdowns with worst-case miss `0.0003 m`, mean penetration `9.67 cm`, zero thruster plume excavation, and `0` tether slack events.
  3. *Honest Operational Caveat:* Tether-suspended TAG requires continuous `~0.5 mm/s^2` hub lateral station-keeping over the `~18 min` descent and a pyrotechnic/thermal weak-link cutter at the sampler wrist to protect the mothercraft against boulder snagging.
]

#figure(
  image("figures/fig4_bennu_tag_guidance_and_mc200.svg", width: 100%),
  caption: [*Live Bennu (101955) Nightingale Crater TAG Monte Carlo & Granular Contact (`C151`, `C152`, `F38`).* (A) Top-down `200`-trial Nightingale landing dispersion (`+56 deg N`, `8 m` green safe zone): open-loop Coriolis drift throws `94.5%` (`189/200`) into surrounding boulders (`F38`), whereas ZEM/ZEV + winch puts `200/200 (100.0%)` within `0.3 mm` of bullseye. (B) Live granular contact & zero-plume retraction: `10.85 cm` peak penetration (matching `C152` `11.58 cm`), `5 s` dwell, and clean `0.191 m/s` winch back-away with `0` slack.]
)

= Executable `Swift++` v3.1 Pass 9B Zero-LLVM Verification Ledger
#gbnote("INT-033", "UNVERIFIABLE", "Pass 9B ledger and certificates C149–C152, K11, F38", "Internal toolchain, kept verbatim. G4N verifiers re-run: Python, Rust, 7/7 Lean pass.")


All five pillars execute natively in zero-dependency, Layer-0 ASCII `Swift++` Scroll 43 (`HaloTagGuidance.spp`, `4,704 B`) and `halo_lissajous_bennu_tag_suite.spp` (`30,352 B`), verified bit-for-bit across Pass 9B Zero-LLVM ARM64 and LLVM `-O3` (`host_libm = 0`), universally certified over compiled `SppMLIR` by `AlexandriaCertifier` [11], [12], stress-tested in a blinded `N = 1,600` ARM64 RCT (`alexandria_epoch39_rct.spp`), and cross-checked in clean-room Python (`verify_all_results.py`).

#block(breakable: false)[
#table(
  columns: (auto, 1fr, auto, auto),
  inset: 5pt,
  stroke: 0.5pt + rgb("#cbd5e1"),
  fill: (x, y) => if y == 0 { rgb("#0f172a") } else if calc.odd(y) { rgb("#f8fafc") } else { white },
  table.header(
    text(fill: white, weight: "bold", size: 8.5pt)[Certificate],
    text(fill: white, weight: "bold", size: 8.5pt)[Executable Law / Control Verified (`HaloTagGuidance.spp`)],
    text(fill: white, weight: "bold", size: 8.5pt)[Engine / Scale],
    text(fill: white, weight: "bold", size: 8.5pt)[Certified Result],
  ),
  text(size: 8.5pt, weight: "bold")[`C149`], text(size: 8.5pt)[3D Collinear $L_1 \/ L_2$ Halo–Lissajous Resonance $cal(R)_"halo" (s) -> 1 - (4/9) s$], text(size: 8.5pt)[`1D Jet2` (`7` boxes)], text(size: 8.5pt, fill: rgb("#047857"), weight: "bold")[`4.954e-3 <= 5.00e-3`],
  text(size: 8.5pt, weight: "bold")[`C150`], text(size: 8.5pt)[Symplectic Monodromy Broucke–Floquet Factor $(1 + sqrt(1 - 4 u^2))/2 -> 1 - u^2$], text(size: 8.5pt)[`1D Jet2` (`9` boxes)], text(size: 8.5pt, fill: rgb("#047857"), weight: "bold")[`4.875e-3 <= 5.00e-3`],
  text(size: 8.5pt, weight: "bold")[`C151`], text(size: 8.5pt)[Bennu Rotating TAG Coriolis Gravity Factor $cal(C)_"Cor" (eta) -> 1 - eta/3$], text(size: 8.5pt)[`1D Jet2` (`7` boxes)], text(size: 8.5pt, fill: rgb("#047857"), weight: "bold")[`6.837e-3 <= 7.00e-3`],
  text(size: 8.5pt, weight: "bold")[`C152`], text(size: 8.5pt)[Bennu Fluidized Granular Penetration $ln(1 + chi)/chi -> 1 - chi/2$], text(size: 8.5pt)[`1D Jet2` (`65` boxes)], text(size: 8.5pt, fill: rgb("#047857"), weight: "bold")[`6.880e-3 <= 7.00e-3`],
  text(size: 8.5pt, weight: "bold")[`K11`], text(size: 8.5pt)[Unique Earth–Moon $L_2$ Collinear Euler Quintic Root $gamma_2^*$], text(size: 8.5pt)[Krawczyk (`4` iters)], text(size: 8.5pt, fill: rgb("#5b21b6"), weight: "bold")[`0.1678327510` (`w=1.9e-16`)],
  text(size: 8.5pt, weight: "bold")[`F38`], text(size: 8.5pt)[Open-Loop Vertical Bennu TAG Falsified vs. `8 m` Coriolis Miss], text(size: 8.5pt)[Falsifier (`[75, 130] m`)], text(size: 8.5pt, fill: rgb("#b91c1c"), weight: "bold")[`FALSIFIED` ($h^* = 114.37$ m)],
  text(size: 8.5pt, weight: "bold")[`RCT39`], text(size: 8.5pt)[Blinded ARM64 RCT (`alexandria_epoch39_rct.spp`, $N = 1","600$)], text(size: 8.5pt)[Zero-LLVM = LLVM], text(size: 8.5pt, fill: rgb("#047857"), weight: "bold")[`1600/1600` vs `0/1600`],
  text(size: 8.5pt, weight: "bold")[`Codex`], text(size: 8.5pt)[Living Codex (`51/51` Pass 9B Zero-LLVM, `Pinakes` `152/152`)], text(size: 8.5pt)[Deep Cross-Mod MDS], text(size: 8.5pt, fill: rgb("#047857"), weight: "bold")[`191/191` (`100.0%`)],
)
]

#v(4pt)
#remark(title: "Pinakes Ledger Seal & Cumulative 39-Epoch Standing")[
  Running `swiftppc alexandria-audit epoch_c/stdlib` seals all `43` scrolls (`588` lowered `SppMLIR` functions), `152/152` proved seams, `11/11` Moore–Krawczyk unique roots, and `38/38` mechanical falsifications into canonical `.sppb` v3.0.0 ledger CRC-64 `0x12FC45AECEEA3888` (`35,339 B`, `153` diagnostics, verified `ALL INTEGRITY GATES PASS` by `epoch_b/AnalyticCLI`). The Living Codex spans `51/51` Pass 9B Zero-LLVM modules (`191/191 = 100.0%` Cross-Module Deep MDS; `279/279` across all 5 standalone ARM64 apps), cumulative blinded RCT trials across 38 empirical epochs reach `60,800` (`60,786/60,800 = 99.977%` Arm B vs. `7,146/60,800 = 11.75%` Arm A, `c10 = 0`, $chi^2 = 53","638.00$, $log_(10) p = -11","649.8$, Cohen's $h = +2.411$), and `141/141` automated XCTests (`25/25` `epoch_b` + `116/116` `epoch_c`) pass unbroken.
]

= Conclusion: Unified 3D Multi-Body and Small-Body Autonomy Verdict

Pushing Horizon I into full 3D non-planar CRTBP manifolds and authentic Bennu TAG regolith sampling sharpens both the physics and the mission architecture:
- *Binary-asteroid $L_2$ systems (Didymos–Dimorphos) unlock active 3D Halo shaping (`8e5x` over Earth–Moon $L_2$):* while Earth–Moon $L_2$ Halo orbits (`K11`, $gamma_2^* = 0.16783275$, $lambda_u = 746.72$) remain the domain of micro-thruster rotating-symplectic Floquet station-keeping (`3,051x` drift collapse for `0.36 m/s` across `4` orbits), compact binary asteroids bring `50 m` triads directly into the $O(k_z^*)$ Halo-resonance regime (`C149`, `C150`).
- *Zero-plume pendulous tether-winch TAG solves Bennu's Coriolis cliff and regolith plume contamination simultaneously:* enforcing Coriolis-compensated ZEM/ZEV lateral steering turns a `5.5%` (`11/200`) open-loop boulder-strike failure (`F38`, `C151`) into `200/200 (100.0%)` sub-millimeter Nightingale landings (`10.85 cm` fluidized sink [`C152`], `0` slack, `0` regolith plume excavation).
#gbnote("REF-12", "UNVERIFIABLE", "Ref [12] cites an internal Swift++ calibration ledger", "The Epoch XXXIX calibration document is not public or in the repository. Suggest marking it 'internal, not public' (as G4N asked for WP035 Ref [12]) and citing the archived sibling working papers by their repository location.")


// ---- [GB] Round-1 ledger (inserted) ----
#heading(numbering: none)[Reconciliation Ledger (Grok Bot, Round 1)]
#block[
#set par(first-line-indent: 0pt, hanging-indent: 0pt)
#set text(size: 8pt)
#table(columns: (auto, 1fr, auto), inset: 4pt, stroke: 0.4pt + luma(170),
  table.header([*ID*], [*Item*], [*Verdict*]),
  "HALO-RERUN", "Independent halo re-run from the paper's state", text(fill: gb-col.at("CONFIRMED"), weight: "bold", "CONFIRMED"),
  "NEG-W11", "The W^u 'lunar tube' passes inside the Moon", text(fill: gb-col.at("CONFIRMED"), weight: "bold", "CONFIRMED"),
  "NEG-W12", "Theorem G3 coupled stiffness and gap sensitivities", text(fill: gb-col.at("CONFIRMED"), weight: "bold", "CONFIRMED"),
  "NEG-W13", "Regolith density and C_D", text(fill: gb-col.at("CONFIRMED"), weight: "bold", "CONFIRMED"),
  "NEG-W14", "Certified intervals vs the operating regime", text(fill: gb-col.at("CONFIRMED"), weight: "bold", "CONFIRMED"),
  "SIM-033", "Station-keeping (3,051× vs 3,442×), W^u kick, TAG Monte Carlo", text(fill: gb-col.at("SPEC-NEEDED"), weight: "bold", "SPEC-NEEDED"),
  "REF-12", "Ref [12] cites an internal Swift++ calibration ledger", text(fill: gb-col.at("UNVERIFIABLE"), weight: "bold", "UNVERIFIABLE"),
  "INT-033", "Pass 9B ledger and certificates C149–C152, K11, F38", text(fill: gb-col.at("UNVERIFIABLE"), weight: "bold", "UNVERIFIABLE"),
)
#text(size: 8pt)[#"Totals: CONFIRMED 5, UNVERIFIABLE 2, SPEC-NEEDED 1. Full evidence, reproduction commands and run specs: reconciliation/GROKBOT_WP033_ROUND1.md in this paper's folder."]
]
// ---- end [GB] ledger ----


#v(6pt)
#heading(level: 1, numbering: none)[References]
#set par(first-line-indent: 0pt, hanging-indent: 1.8em, leading: 0.48em)
#text(size: 8.6pt)[
[1] Ergentics, LLC, *Working Paper 030 / Horizon Monograph I: Shape-Controlled Gravitational Propulsion Resolved*, `Swift++` Library of Alexandria (Epoch XXXVI), November 2026.

[2] Ergentics, LLC, *Working Paper 031 / Horizon Monograph IB: 3D Non-Planar $J_2$ Symmetry Breaking, Collinear-Bridge $"SO"(3)$ Holonomy, Safe-Perigee Optimal Eccentricity, and Hardware-in-the-Loop Actuator Sizing*, `Swift++` Library of Alexandria (Epoch XXXVII), November 2026.

[3] Ergentics, LLC, *Working Paper 032 / Horizon Monograph IC: Bennu-Class Triaxial Asteroid Proximity Operations, 3D Multi-Tether Coupled Flexible-Body FEM & Fault-Tolerant Winch FDIR, and the Extended-Body Three-Body Problem*, `Swift++` Library of Alexandria (Epoch XXXVIII), November 2026.

[4] R. W. Farquhar and A. A. Kamel, *Quasi-periodic orbits about the translunar libration point*, Celestial Mechanics *7* (1973), 458–473; D. L. Richardson, *Analytic construction of periodic orbits about the collinear points*, Celestial Mechanics *22* (1980), 241–253.

[5] V. Szebehely, *Theory of Orbits: The Restricted Problem of Three Bodies*, Academic Press, 1967.

[6] K. C. Howell, *Three-dimensional, periodic, 'halo' orbits*, Celestial Mechanics *32* (1984), 53–71; R. Broucke, *Stability of periodic orbits in the elliptic, restricted three-body problem*, AIAA Journal *7* (1969), 1003–1009.

[7] W. S. Koon, M. W. Lo, J. E. Marsden, and S. D. Ross, *Dynamical Systems, the Three-Body Problem and Space Mission Design*, Marsden Books, 2011.

[8] D. S. Lauretta et al., *The unexpected surface of asteroid (101955) Bennu*, Nature *568* (2019), 55–60; D. J. Scheeres et al., *The dynamic geophysical environment of (101955) Bennu based on OSIRIS-REx measurements*, Nature Astronomy *3* (2019), 352–361.

[9] D. S. Lauretta et al., *Spacecraft sample collection and subsurface excavation of asteroid (101955) Bennu*, Science *377* (2022), no. 6603, 285–291; K. J. Walsh et al., *Near-zero cohesion and loose packing of Bennu's near subsurface revealed by spacecraft contact*, Science Advances *8* (2022), eabm6229.

[10] G. Gómez, K. C. Howell, J. Masdemont, and C. Simó, *Station-keeping strategies for translunar libration point orbits*, Adv. Astronaut. Sci. *99* (1998), 949–967; Y. Guo, M. Hawkins, and B. Wie, *Applications of generalized zero-effort-miss/zero-effort-velocity feedback guidance algorithm*, J. Guidance, Control, and Dynamics *36* (2013), 810–820.

[11] R. E. Moore, *Interval Analysis*, Prentice-Hall, 1966; R. Krawczyk, *Newton-Algorithmen zur Bestimmung von Nullstellen mit Fehlerschranken*, Computing *4* (1969), 187–201.

[12] K. Makino and M. Berz, *Taylor models and other validated functional inclusion methods*, Int. J. Pure Appl. Math. *4* (2003), no. 4, 379–456; Ergentics, LLC, *`Swift++` Library of Alexandria Epoch XXXIX Calibration Ledger*, November 2026.
]
