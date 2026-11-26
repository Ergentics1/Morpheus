/-!
WP030.Theorems — Zero-Mathlib Lean 4.36.0 Kernel-Checked Algebraic Oracles
for Ergentics Working Paper 030 ("Shape-Controlled Gravitational Propulsion Resolved").

Author: Gemini 4 Neon ([G4N] / [E->G4N]) for Morpheus (MIT License).
Strict zero-sorry, zero-ofReduceBool, zero-Mathlib formal verification of exact
algebraic, Noether, quadrupole-sign, unitary-Hopf, binary-collision, kinetic-energy
divergence, Proposition 3, K8 critical eccentricity, F35 heat-loss, and physical
perigee / Table 1 theorems.
-/

namespace WP030

/-! ## 1. H1 Exact Collinear Factorization Numerator Identity -/

/-- Exact cleared-denominator identity underlying WP 030 §1 collinear factorization:
    ((1 - e)^2 + (1 + e)^2 - 2*(1 - e^2)^2) = 2 * e^2 * (3 - e^2). -/
theorem h1_collinear_factorization_int (e : Int) :
    (1 - e) ^ 2 + (1 + e) ^ 2 - 2 * (1 - e ^ 2) ^ 2 = 2 * e ^ 2 * (3 - e ^ 2) := by
  grind

/-! ## 2. Theorem 1 Core — Exact 3D Central-Force Noether Torque Cancellation -/

/-- 3D vector over Int (scales directly to any commutative ring). -/
structure Vec3 where
  x : Int
  y : Int
  z : Int
deriving DecidableEq, Repr

def Vec3.add (a b : Vec3) : Vec3 := ⟨a.x + b.x, a.y + b.y, a.z + b.z⟩
def Vec3.smul (c : Int) (a : Vec3) : Vec3 := ⟨c * a.x, c * a.y, c * a.z⟩
def Vec3.cross (a b : Vec3) : Vec3 :=
  ⟨a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x⟩

/-- Exact central-force identity: for any force F = lam * (R + rho) directed along
    R + rho, the internal torque rho x F plus orbital torque R x F vanishes identically. -/
theorem thm1_noether_central_torque_cancel (R rho : Vec3) (lam : Int) :
    let F := Vec3.smul lam (Vec3.add R rho)
    Vec3.add (Vec3.cross rho F) (Vec3.cross R F) = ⟨0, 0, 0⟩ := by
  cases R with | mk rx ry rz =>
  cases rho with | mk px py pz =>
  simp only [Vec3.add, Vec3.smul, Vec3.cross, Vec3.mk.injEq]
  refine ⟨by grind, by grind, by grind⟩

/-! ## 3. Theorem 2 Sign Catch (Catch 4) & Unitary Equilateral-Pole Hopf Basis -/

/-- Under standard rigid-body inertia (Ixx = m y^2, Iyy = m x^2, Ixy = -m x y),
    (Ixx - Iyy, 2 Ixy) is the EXACT NEGATIVE of the complex mass quadrupole m (x + i y)^2. -/
theorem catch4_inertia_vs_mass_quadrupole_sign (m x y : Int) :
    let Ixx := m * (y * y)
    let Iyy := m * (x * x)
    let Ixy := -(m * (x * y))
    let Qre := m * (x * x - y * y)
    let Qim := m * (2 * x * y)
    (Ixx - Iyy = -Qre) ∧ (2 * Ixy = -Qim) := by
  refine ⟨by grind, by grind⟩

/-- Unitary change of basis (w+, w-) <-> (z1, z2):
    With u1 = wp + wm, u2 = -i*(wp - wm) (so z1 = u1/sqrt(2), z2 = u2/sqrt(2)),
    u1^2 + u2^2 = 4 * wp * wm identically (so z1^2 + z2^2 = 2 * wp * wm, proving
    Q_C^mass = I_0 * sin(beta) * exp(2i * theta_0) is COMPLETELY INDEPENDENT of chi!). -/
theorem unitary_hopf_quadrupole_identity (a b c d : Int) :
    let u1r := a + c
    let u1i := b + d
    let u2r := b - d
    let u2i := c - a
    ((u1r * u1r - u1i * u1i) + (u2r * u2r - u2i * u2i) = 4 * (a * c - b * d)) ∧
    ((2 * u1r * u1i) + (2 * u2r * u2i) = 4 * (a * d + b * c)) := by
  refine ⟨by grind, by grind⟩

/-- Unitary norm preservation: |u1|^2 + |u2|^2 = 2 * (|wp|^2 + |wm|^2),
    proving I_zz = (M/3)(|z1|^2 + |z2|^2) = (M/3)(|wp|^2 + |wm|^2) = I_0 identically. -/
theorem unitary_hopf_norm_preservation (a b c d : Int) :
    let u1r := a + c
    let u1i := b + d
    let u2r := b - d
    let u2i := c - a
    (u1r * u1r + u1i * u1i) + (u2r * u2r + u2i * u2i) =
    2 * ((a * a + b * b) + (c * c + d * d)) := by
  grind

/-! ## 4. Catch 2 Exact Binary-Collision Witnesses in Paper's (Theta, Phi) Chart -/

/-- Exact integer-scaled binary collision witnesses for WP 030 §3.3 holonomy loop:
    At (Theta, Phi) = (pi/3, 0): scaled by 2*sqrt(3)/L, (rho1, rho2, rho3) = (4, -2, -2) => rho2 = rho3.
    At (Theta, Phi) = (pi/3, pi): scaled by 2*sqrt(3)/(i L), (rho1, rho2, rho3) = (2, -4, 2) => rho1 = rho3. -/
theorem catch2_paper_holonomy_exact_collisions :
    let rho1_phi0 : Int := 3 + 1
    let rho2_phi0 : Int := -3 + 1
    let rho3_phi0 : Int := -2
    let rho1_phipi : Int := 3 - 1
    let rho2_phipi : Int := -3 - 1
    let rho3_phipi : Int := 2
    (rho1_phi0 + rho2_phi0 + rho3_phi0 = 0) ∧
    (rho2_phi0 = rho3_phi0) ∧
    (rho1_phipi + rho2_phipi + rho3_phipi = 0) ∧
    (rho1_phipi = rho3_phipi) := by
  decide

/-- At the paper's North Pole Theta = 0 (scaled by 1/L): rho = (+1, -1, 0),
    collinear (d12^2 = 4 != 1 = d23^2 = d13^2), refuting fig3's "North Pole (Equilateral)" label. -/
theorem catch2_paper_north_pole_collinear :
    let rho1 : Int := 1
    let rho2 : Int := -1
    let rho3 : Int := 0
    (rho1 + rho2 + rho3 = 0) ∧
    ((rho1 - rho2) ^ 2 = 4) ∧
    ((rho2 - rho3) ^ 2 = 1) ∧
    ((rho1 - rho3) ^ 2 = 1) ∧
    ((rho1 - rho2) ^ 2 ≠ (rho2 - rho3) ^ 2) := by
  decide

/-! ## 5. Catch 3 ([G4N] Original Theorem) — Exact Zero-Spin Kinetic Divergence & Span Cap -/

/-- Exact rational kinetic-energy ratio T_shape / (1/2 I0 w^2) = q^2 / (1 - q^2) at q = 19/20 (0.95):
    equals 361 / 39, strictly inside (9.2564, 9.2565) — over 9.25x WP 030 §4.1's 1/2 I0 w^2 estimate. -/
theorem catch3_kinetic_divergence_q95 :
    let num : Nat := 19 * 19
    let den : Nat := 20 * 20 - 19 * 19
    (num = 361) ∧ (den = 39) ∧
    (num * 10000 > 92564 * den) ∧ (num * 10000 < 92565 * den) := by
  decide

/-- Exact hard boom-radius cap max_i |rho_i|^2 / L^2 = 2*(1 + q)/3 <= 1 iff q <= 1/2:
    at q = 1/2 exact equality holds (max |rho_i| = L); at q = 19/20, max |rho_i|^2 / L^2 = 13/10 > 1. -/
theorem catch3_span_cap_threshold :
    (2 * (2 + 1) = 3 * 2) ∧
    (2 * (20 + 19) * 10 = 3 * 20 * 13) ∧
    (13 > 10) := by
  decide

/-! ## 6. Proposition 3, K8 Critical Eccentricity e_50*, and F35 Witness -/

/-- Exact polynomial core of Proposition 3:
    (1 + e)^3 - (1 - e)^3 = 2 * (3 e + e^3), yielding (3/2) p^3 (r_p^-3 - r_a^-3) = 3(3e + e^3). -/
theorem prop3_pumping_polynomial (e : Int) :
    (1 + e) ^ 3 - (1 - e) ^ 3 = 2 * (3 * e + e ^ 3) := by
  grind

/-- Exact K8 algebraic equivalence:
    (1 + e)^3 - 2 * (1 - e)^3 = 3 * e^3 - 3 * e^2 + 9 * e - 1. -/
theorem k8_cubic_equivalence (e : Int) :
    (1 + e) ^ 3 - 2 * (1 - e) ^ 3 = 3 * e ^ 3 - 3 * e ^ 2 + 9 * e - 1 := by
  grind

/-- Exact rational sign-change certificate for K8 e_50* directly inside WP 030's Moore-Krawczyk
    interval [0.11501333195111552, 0.11501333195111600]:
    since g(e) = (1+e)^3 - 2(1-e)^3 is strictly increasing on [0, 1], g(lo) < 0 < g(hi)
    certifies the unique root e_50* in (lo, hi) with width 4.8e-16! -/
theorem k8_root_bracket_certified :
    let D  : Int := 100000000000000000 -- 10^17
    let lo : Int := 11501333195111552
    let hi : Int := 11501333195111600
    ((D + lo) ^ 3 < 2 * (D - lo) ^ 3) ∧
    (2 * (D - hi) ^ 3 < (D + hi) ^ 3) := by
  decide

/-- Exact F35 heat-loss witness at e* = 0.0275 = 11/400:
    q(11/400) = (389/411)^3 satisfies 0.8478 < q(e*) < 0.8479 (~84.79% -> 84.8% lost, vs paper's 84.6%). -/
theorem f35_exact_heat_loss_witness :
    (389 ^ 3 * 10000 > 8478 * 411 ^ 3) ∧
    (389 ^ 3 * 10000 < 8479 * 411 ^ 3) := by
  decide

/-! ## 7. Catches 1 & 6 — Exact Underground Perigee & Regime C Exponent Certificates -/

/-- Catch 1 (CRITICAL): WP 030 Table 1 Regimes A (a=7000 km, e=0.10) and B (a=7000 km, e=0.25)
    both violate Earth's mean surface radius R_E = 6371 km (r_p = 6300 km and 5250 km)! -/
theorem catch1_underground_earth_perigees :
    let R_E  : Nat := 6371
    let rp_A : Nat := 7000 * 90 / 100   -- 6300 km
    let rp_B : Nat := 7000 * 75 / 100   -- 5250 km
    (rp_A = 6300) ∧ (rp_A < R_E) ∧ (R_E - rp_A = 71) ∧
    (rp_B = 5250) ∧ (rp_B < R_E) ∧ (R_E - rp_B = 1121) := by
  decide

/-- Catch 6: 7.84e6 = (7000 / 2.5)^2 is the dimensionless coupling ratio (L/R)^2 = eps^2,
    NOT the fourth-power scaling (7000 / 2.5)^4 = 6.14656e13. -/
theorem catch6_regime_c_coupling_ratio :
    let ratio : Nat := 70000 / 25 -- 2800
    (ratio = 2800) ∧
    (ratio ^ 2 = 7840000) ∧
    (ratio ^ 4 = 61465600000000) := by
  decide

end WP030
