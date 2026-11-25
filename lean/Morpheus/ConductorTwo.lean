/-!
# Eisenstein Obstruction & Conductor-2 Order (Proposition 3.7, Theorem 3.8, NEG-M1)

Machine-checked proofs that `Z_12` is not a ring quotient of `Z[ω]`, `Z[i]`, or `Z[ζ_12]`
(`NEG-M1`), while the conductor-2 order `O = Z[√-3]` yields `Z_12 ≅ O / (√-3 (1 + √-3))`.
-/

namespace Morpheus

/-- NEG-M1 / Prop 3.7: `x^2 + x + 1` has no root mod 4 (2 is inert in `Z[ω]`). -/
theorem prop3_7_no_eisenstein_root_mod4 :
    ∀ (x : Fin 4), (x.val * x.val + x.val + 1) % 4 ≠ 0 := by
  decide

/-- NEG-M1 / Prop 3.7: `x^2 + 1` has no root mod 4 (`Z[i]` cannot map onto `Z_12`). -/
theorem prop3_7_no_gaussian_root_mod4 :
    ∀ (x : Fin 4), (x.val * x.val + 1) % 4 ≠ 0 := by
  decide

/-- NEG-M1 / Prop 3.7: `Φ_12(x) = x^4 - x^2 + 1` has no root mod 3 or mod 4. -/
theorem prop3_7_no_phi12_root_mod3_mod4 :
    (∀ (x : Fin 3), (x.val ^ 4 + 3 * x.val ^ 2 - x.val ^ 2 + 1) % 3 ≠ 0) ∧
    (∀ (x : Fin 4), (x.val ^ 4 + 4 * x.val ^ 2 - x.val ^ 2 + 1) % 4 ≠ 0) := by
  decide

/-- Explicit kernel-not-an-ideal witness in `Z[ω]` for `ψ(a + bω) = (7a + 9b) mod 12`. -/
theorem prop3_7_eisenstein_kernel_not_ideal :
    let psi := fun (a b : Int) => (7 * a + 9 * b) % 12
    -- ω * (a + bω) = -b + (a - b)ω
    psi (-12) (-8) = 0 ∧ psi 8 (-4) = 8 ∧ psi 8 (-4) ≠ 0 := by
  decide

/-- The conductor-2 quadratic order `O = Z[√-3]`, elements `a + b√-3`. -/
structure O2 where
  a : Int
  b : Int
  deriving DecidableEq, Repr

namespace O2

def add (x y : O2) : O2 := ⟨x.a + y.a, x.b + y.b⟩

def mul (x y : O2) : O2 := ⟨x.a * y.a - 3 * x.b * y.b, x.a * y.b + x.b * y.a⟩

def norm (x : O2) : Int := x.a * x.a + 3 * x.b * x.b

/-- Ring homomorphism `ψ : Z[√-3] -> Z/12Z` sending `a + b√-3 ↦ (a + 3b) mod 12`. -/
def psi (x : O2) : Int := (x.a + 3 * x.b) % 12

/-- Theorem 3.8: `ψ` preserves addition identically for all `x, y ∈ Z[√-3]`. -/
theorem psi_add (x y : O2) : psi (add x y) = (psi x + psi y) % 12 := by
  simp only [psi, add]
  omega

/-- Theorem 3.8: `ψ` preserves multiplication identically for all `x, y ∈ Z[√-3]`
since `(3)^2 = 9 ≡ -3 (mod 12)`. -/
theorem psi_mul (x y : O2) : psi (mul x y) = (psi x * psi y) % 12 := by
  simp only [psi, mul]
  have h :
      (x.a * y.a - 3 * x.b * y.b) + 3 * (x.a * y.b + x.b * y.a)
      = (x.a + 3 * x.b) * (y.a + 3 * y.b) - 12 * (x.b * y.b) := by
    have e1 : 3 * x.b * y.b = 3 * (x.b * y.b) := Int.mul_assoc 3 x.b y.b
    have e2 : x.a * (3 * y.b) = 3 * (x.a * y.b) := by
      rw [← Int.mul_assoc, Int.mul_comm x.a 3, Int.mul_assoc]
    have e3 : 3 * x.b * y.a = 3 * (x.b * y.a) := Int.mul_assoc 3 x.b y.a
    have e4 : 3 * x.b * (3 * y.b) = 9 * (x.b * y.b) := by
      calc 3 * x.b * (3 * y.b) = 3 * (x.b * (3 * y.b)) := Int.mul_assoc _ _ _
        _ = 3 * (3 * (x.b * y.b)) := by
            rw [← Int.mul_assoc x.b 3 y.b, Int.mul_comm x.b 3, Int.mul_assoc]
        _ = 9 * (x.b * y.b) := by rw [← Int.mul_assoc]; rfl
    have h1 : (x.a + 3 * x.b) * (y.a + 3 * y.b) =
              x.a * y.a + 3 * (x.a * y.b) + 3 * (x.b * y.a) + 9 * (x.b * y.b) := by
      rw [Int.add_mul, Int.mul_add, Int.mul_add, e2, e3, e4]
      omega
    have h2 : 3 * (x.a * y.b + x.b * y.a) = 3 * (x.a * y.b) + 3 * (x.b * y.a) := Int.mul_add _ _ _
    omega
  rw [h, Int.sub_emod, Int.mul_emod_right, Int.sub_zero, Int.emod_emod, Int.mul_emod]

/-- Theorem 3.8: `ψ` is surjective onto `Z/12Z`. -/
theorem psi_surjective (r : Fin 12) : psi ⟨r.val, 0⟩ = r.val := by
  simp only [psi]
  omega

/-- Principal ideal generator `g = 3 - √-3 = -√-3 (1 + √-3)` of norm 12. -/
def gen : O2 := ⟨3, -1⟩

theorem gen_factorization :
    mul ⟨0, -1⟩ ⟨1, 1⟩ = gen ∧ norm gen = 12 := by
  decide

/-- Theorem 3.8: Exact ideal kernel characterization for ALL `z ∈ Z[√-3]`:
`ψ(z) = 0 ↔ ∃ q ∈ Z[√-3], z = (3 - √-3) * q`. -/
theorem psi_kernel_iff_ideal (z : O2) :
    psi z = 0 ↔ ∃ q : O2, z = mul gen q := by
  cases z with | mk za zb =>
  constructor
  · intro h
    simp only [psi] at h
    let k : Int := (za + 3 * zb) / 12
    have hk : za + 3 * zb = 12 * k := by omega
    refine ⟨⟨3 * k - zb, k⟩, ?_⟩
    simp only [mul, gen]
    congr 1 <;> omega
  · rintro ⟨q, hq⟩
    rw [hq]
    simp only [psi, mul, gen]
    omega

/-- Unimodularity of the third-basis `{√-3, 1 + √-3}`: `det [[0, 1], [1, 1]] = -1`. -/
theorem basis_unimodular : (0 : Int) * 1 - 1 * 1 = -1 := by
  decide

/-- Non-reducedness of `O / (2)`: `ε = 1 + √-3` has `ε^2 ≡ 0 (mod 2)` while `ε ≢ 0 (mod 2)`. -/
theorem order2_mod2_nilpotent :
    let eps : O2 := ⟨1, 1⟩
    let eps2 := mul eps eps
    eps2 = ⟨-2, 2⟩ ∧ eps2.a % 2 = 0 ∧ eps2.b % 2 = 0 ∧ eps.a % 2 = 1 := by
  decide

/-- Theorem 3.8 conductor parity: `x^2 + f x + f^2 ≡ 0 (mod 4)` has a root iff `f` is even. -/
theorem conductor_mod4_root_iff_even (f : Fin 4) :
    (∃ x : Fin 4, (x.val * x.val + f.val * x.val + f.val * f.val) % 4 = 0) ↔ f.val % 2 = 0 := by
  revert f
  decide

end O2
end Morpheus
