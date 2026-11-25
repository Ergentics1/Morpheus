import Morpheus.TriadGraph

/-!
# Voice Winding Integrality, Tonnetz Gram, and Schottky Trace Obstruction
(Theorems 5.1, 6.1 Gram, 7.1(a), and 7.13 / NEG-M8)

Machine-checked proofs of:
1. Voice-sum integrality `12 ∣ walkVoiceSum` on every closed cadence of any length `m ∈ ℕ`.
2. Exact Tonnetz Gram `det(G) = 108` and inverse covariance identity.
3. Schottky involutions `σ_P^2 = σ_L^2 = σ_R^2 = 2I`, kernel membership `γ_0 ∈ K`,
   exact matrix `γ_0 = [[5, -12], [-12, 80]]`, and universal power trace obstruction
   `∀ k ≥ 1, tr(γ_0^k)^2 > 4 det(γ_0^k)` (`τ(γ_0^k) > 4`).
-/

namespace Morpheus

/-- Lift potential `pot(v)` = sum of the three triad pitch classes in `Z`. -/
def voiceSumPotential (v : Triad) : Int :=
  let r : Int := v.val % 12
  if v.val < 12 then
    r + ((r + 4) % 12) + ((r + 7) % 12)
  else
    r + ((r + 3) % 12) + ((r + 7) % 12)

/-- Every single PLR edge satisfies `voiceStep ≡ pot(target) - pot(source) (mod 12)`. -/
theorem voiceStep_coboundary_mod12 :
    ∀ (v : Triad) (m : Move),
      (voiceStep v m - (voiceSumPotential (applyMove v m) - voiceSumPotential v)) % 12 = 0 := by
  intro v m
  cases m <;> revert v <;> decide

/-- Cumulative signed voice displacement along any move sequence `w` from `v`. -/
def walkVoiceSum : Triad → List Move → Int
  | _, [] => 0
  | v, m :: ms => voiceStep v m + walkVoiceSum (applyMove v m) ms

theorem walkVoiceSum_coboundary_mod12 (w : List Move) :
    ∀ (v : Triad),
      (walkVoiceSum v w - (voiceSumPotential (applyWord w v) - voiceSumPotential v)) % 12 = 0 := by
  induction w with
  | nil =>
    intro v
    simp [walkVoiceSum, applyWord]
  | cons m ms ih =>
    intro v
    have h1 := voiceStep_coboundary_mod12 v m
    have h2 := ih (applyMove v m)
    simp only [walkVoiceSum, applyWord, List.foldl_cons] at h2 ⊢
    omega

/-- Theorem 5.1 integrality: EVERY closed cadence of ANY length has total voice shift divisible by 12. -/
theorem thm5_1_closed_walk_winding_integral (v : Triad) (w : List Move)
    (hclosed : applyWord w v = v) :
    walkVoiceSum v w % 12 = 0 := by
  have h := walkVoiceSum_coboundary_mod12 w v
  rw [hclosed] at h
  omega

/-- Exact Tonnetz Gram `G = [[16, -6], [-6, 9]]`, `det(G) = 108`, and `2 G * (1/2 G^{-1}) = I`. -/
theorem thm6_1_tonnetz_gram_exact :
    let g00 : Int := 16
    let g01 : Int := -6
    let g11 : Int := 9
    let detG := g00 * g11 - g01 * g01
    detG = 108 ∧ g00 > 0 ∧ detG > 0 ∧
    -- Multiply G by 216 * Cov = [[9, 6], [6, 16]] = adj(G) -> 108 * I.
    g00 * 9 + g01 * 6 = 108 ∧ g00 * 6 + g01 * 16 = 0 ∧
    g01 * 9 + g11 * 6 = 0 ∧ g01 * 6 + g11 * 16 = 108 := by
  decide

/-- Exact 2×2 integer matrices for the `PGL_2(Q_2)` Schottky realization (Theorem 7.1). -/
structure Mat2Z where
  a : Int
  b : Int
  c : Int
  d : Int
  deriving DecidableEq, Repr

namespace Mat2Z

def id : Mat2Z := ⟨1, 0, 0, 1⟩

def scale (k : Int) (m : Mat2Z) : Mat2Z := ⟨k * m.a, k * m.b, k * m.c, k * m.d⟩

def mul (x y : Mat2Z) : Mat2Z :=
  ⟨x.a * y.a + x.b * y.c, x.a * y.b + x.b * y.d,
   x.c * y.a + x.d * y.c, x.c * y.b + x.d * y.d⟩

def tr (m : Mat2Z) : Int := m.a + m.d

def det (m : Mat2Z) : Int := m.a * m.d - m.b * m.c

def pow : Mat2Z → Nat → Mat2Z
  | _, 0 => id
  | m, k + 1 => mul (pow m k) m

theorem mul_assoc (x y z : Mat2Z) : mul (mul x y) z = mul x (mul y z) := by
  cases x; cases y; cases z
  simp only [mul]
  congr 1 <;>
    (simp only [Int.add_mul, Int.mul_add, Int.mul_assoc]; omega)

theorem mul_id (x : Mat2Z) : mul x id = x := by
  cases x; simp [mul, id]

theorem id_mul (x : Mat2Z) : mul id x = x := by
  cases x; simp [mul, id]

/-- Cayley-Hamilton for 2×2 integer matrices: `M^2 = tr(M)*M - det(M)*I`. -/
theorem cayley_hamilton (m : Mat2Z) :
    let m2 := mul m m
    m2.a = tr m * m.a - det m ∧
    m2.b = tr m * m.b ∧
    m2.c = tr m * m.c ∧
    m2.d = tr m * m.d - det m := by
  cases m with | mk a b c d =>
  simp only [mul, tr, det]
  refine ⟨?_, ?_, ?_, ?_⟩
  · have h : (a + d) * a = a * a + d * a := Int.add_mul a d a
    have h2 : a * d = d * a := Int.mul_comm a d
    omega
  · have h : (a + d) * b = a * b + d * b := Int.add_mul a d b
    have h2 : b * d = d * b := Int.mul_comm b d
    omega
  · have h : (a + d) * c = a * c + d * c := Int.add_mul a d c
    have h2 : c * a = a * c := Int.mul_comm c a
    omega
  · have h : (a + d) * d = a * d + d * d := Int.add_mul a d d
    have h2 : c * b = b * c := Int.mul_comm c b
    omega

theorem det_mul (x y : Mat2Z) : det (mul x y) = det x * det y := by
  cases x with | mk xa xb xc xd =>
  cases y with | mk ya yb yc yd =>
  simp only [mul, det]
  have h1 : (xa * ya + xb * yc) * (xc * yb + xd * yd) =
            xa * ya * (xc * yb) + xa * ya * (xd * yd) + xb * yc * (xc * yb) + xb * yc * (xd * yd) := by
    rw [Int.add_mul, Int.mul_add, Int.mul_add]; omega
  have h2 : (xa * yb + xb * yd) * (xc * ya + xd * yc) =
            xa * yb * (xc * ya) + xa * yb * (xd * yc) + xb * yd * (xc * ya) + xb * yd * (xd * yc) := by
    rw [Int.add_mul, Int.mul_add, Int.mul_add]; omega
  have h3 : (xa * xd - xb * xc) * (ya * yd - yb * yc) =
            xa * xd * (ya * yd) - xa * xd * (yb * yc) - xb * xc * (ya * yd) + xb * xc * (yb * yc) := by
    rw [Int.sub_mul, Int.mul_sub, Int.mul_sub]; omega
  have e1 : xa * ya * (xc * yb) = xa * yb * (xc * ya) := by
    calc xa * ya * (xc * yb) = xa * (ya * (xc * yb)) := Int.mul_assoc _ _ _
      _ = xa * (ya * (yb * xc)) := by rw [Int.mul_comm xc yb]
      _ = xa * ((ya * yb) * xc) := by rw [Int.mul_assoc]
      _ = xa * ((yb * ya) * xc) := by rw [Int.mul_comm ya yb]
      _ = xa * (yb * (ya * xc)) := by rw [Int.mul_assoc]
      _ = xa * (yb * (xc * ya)) := by rw [Int.mul_comm ya xc]
      _ = xa * yb * (xc * ya) := by rw [← Int.mul_assoc]
  have e2 : xa * ya * (xd * yd) = xa * xd * (ya * yd) := by
    calc xa * ya * (xd * yd) = xa * (ya * (xd * yd)) := Int.mul_assoc _ _ _
      _ = xa * ((ya * xd) * yd) := by rw [Int.mul_assoc]
      _ = xa * ((xd * ya) * yd) := by rw [Int.mul_comm ya xd]
      _ = xa * (xd * (ya * yd)) := by rw [Int.mul_assoc]
      _ = xa * xd * (ya * yd) := by rw [← Int.mul_assoc]
  have e3 : xb * yc * (xc * yb) = xb * xc * (yb * yc) := by
    calc xb * yc * (xc * yb) = xb * (yc * (xc * yb)) := Int.mul_assoc _ _ _
      _ = xb * ((yc * xc) * yb) := by rw [Int.mul_assoc]
      _ = xb * ((xc * yc) * yb) := by rw [Int.mul_comm yc xc]
      _ = xb * (xc * (yc * yb)) := by rw [Int.mul_assoc]
      _ = xb * (xc * (yb * yc)) := by rw [Int.mul_comm yc yb]
      _ = xb * xc * (yb * yc) := by rw [← Int.mul_assoc]
  have e4 : xb * yc * (xd * yd) = xb * yd * (xd * yc) := by
    calc xb * yc * (xd * yd) = xb * (yc * (xd * yd)) := Int.mul_assoc _ _ _
      _ = xb * (yc * (yd * xd)) := by rw [Int.mul_comm xd yd]
      _ = xb * ((yc * yd) * xd) := by rw [Int.mul_assoc]
      _ = xb * ((yd * yc) * xd) := by rw [Int.mul_comm yc yd]
      _ = xb * (yd * (yc * xd)) := by rw [Int.mul_assoc]
      _ = xb * (yd * (xd * yc)) := by rw [Int.mul_comm yc xd]
      _ = xb * yd * (xd * yc) := by rw [← Int.mul_assoc]
  have e5 : xa * yb * (xd * yc) = xa * xd * (yb * yc) := by
    calc xa * yb * (xd * yc) = xa * (yb * (xd * yc)) := Int.mul_assoc _ _ _
      _ = xa * ((yb * xd) * yc) := by rw [Int.mul_assoc]
      _ = xa * ((xd * yb) * yc) := by rw [Int.mul_comm yb xd]
      _ = xa * (xd * (yb * yc)) := by rw [Int.mul_assoc]
      _ = xa * xd * (yb * yc) := by rw [← Int.mul_assoc]
  have e6 : xb * yd * (xc * ya) = xb * xc * (ya * yd) := by
    calc xb * yd * (xc * ya) = xb * (yd * (xc * ya)) := Int.mul_assoc _ _ _
      _ = xb * ((yd * xc) * ya) := by rw [Int.mul_assoc]
      _ = xb * ((xc * yd) * ya) := by rw [Int.mul_comm yd xc]
      _ = xb * (xc * (yd * ya)) := by rw [Int.mul_assoc]
      _ = xb * (xc * (ya * yd)) := by rw [Int.mul_comm yd ya]
      _ = xb * xc * (ya * yd) := by rw [← Int.mul_assoc]
  omega

theorem det_pow (m : Mat2Z) : ∀ k : Nat, det (pow m k) = (det m) ^ k
  | 0 => by simp [pow, id, det]
  | k + 1 => by
    simp only [pow, det_mul, det_pow m k, Int.pow_succ]

/-- Trace linear recurrence `tr(M^(k+2)) = tr(M)*tr(M^(k+1)) - det(M)*tr(M^k)`. -/
theorem tr_pow_recurrence (m : Mat2Z) (k : Nat) :
    tr (pow m (k + 2)) = tr m * tr (pow m (k + 1)) - det m * tr (pow m k) := by
  have hmul : pow m (k + 2) = mul (pow m k) (mul m m) := by
    simp only [pow, mul_assoc]
  have h1 : pow m (k + 1) = mul (pow m k) m := rfl
  rw [hmul, h1]
  have hch := cayley_hamilton m
  generalize pow m k = p
  rcases p with ⟨pa, pb, pc, pd⟩
  rcases m with ⟨ma, mb, mc, md⟩
  rcases hch with ⟨ha, hb, hc, hd⟩
  simp only [mul, tr] at *
  rw [ha, hb, hc, hd]
  have r1 : pa * ((ma + md) * ma - det ⟨ma, mb, mc, md⟩) =
            (ma + md) * (pa * ma) - det ⟨ma, mb, mc, md⟩ * pa := by
    rw [Int.mul_sub]
    have e1 : pa * ((ma + md) * ma) = (ma + md) * (pa * ma) := by
      rw [← Int.mul_assoc, Int.mul_comm pa (ma + md), Int.mul_assoc]
    have e2 : pa * det ⟨ma, mb, mc, md⟩ = det ⟨ma, mb, mc, md⟩ * pa := Int.mul_comm _ _
    omega
  have r2 : pb * ((ma + md) * mc) = (ma + md) * (pb * mc) := by
    rw [← Int.mul_assoc, Int.mul_comm pb (ma + md), Int.mul_assoc]
  have r3 : pc * ((ma + md) * mb) = (ma + md) * (pc * mb) := by
    rw [← Int.mul_assoc, Int.mul_comm pc (ma + md), Int.mul_assoc]
  have r4 : pd * ((ma + md) * md - det ⟨ma, mb, mc, md⟩) =
            (ma + md) * (pd * md) - det ⟨ma, mb, mc, md⟩ * pd := by
    rw [Int.mul_sub]
    have e1 : pd * ((ma + md) * md) = (ma + md) * (pd * md) := by
      rw [← Int.mul_assoc, Int.mul_comm pd (ma + md), Int.mul_assoc]
    have e2 : pd * det ⟨ma, mb, mc, md⟩ = det ⟨ma, mb, mc, md⟩ * pd := Int.mul_comm _ _
    omega
  have r5 : (ma + md) * (pa * ma + pb * mc + (pc * mb + pd * md)) =
            (ma + md) * (pa * ma) + (ma + md) * (pb * mc) +
            (ma + md) * (pc * mb) + (ma + md) * (pd * md) := by
    rw [Int.mul_add, Int.mul_add, Int.mul_add]; omega
  have r6 : det ⟨ma, mb, mc, md⟩ * (pa + pd) =
            det ⟨ma, mb, mc, md⟩ * pa + det ⟨ma, mb, mc, md⟩ * pd := Int.mul_add _ _ _
  omega

/-- Auxiliary Chebyshev sequence `u_0 = 0, u_1 = 1, u_{k+2} = t*u_{k+1} - d*u_k`. -/
def chebU (t d : Int) : Nat → Int
  | 0 => 0
  | 1 => 1
  | k + 2 => t * chebU t d (k + 1) - d * chebU t d k

/-- Simultaneous exact trace/Chebyshev identity for all `k ≥ 0`. -/
theorem trace_cheb_invariant (m : Mat2Z) :
    ∀ k : Nat,
      let t := tr m
      let d := det m
      let D := t * t - 4 * d
      let ak := tr (pow m k)
      let uk := chebU t d k
      2 * tr (pow m (k + 1)) = t * ak + D * uk ∧
      2 * chebU t d (k + 1) = ak + t * uk ∧
      ak * ak - D * (uk * uk) = 4 * d ^ k := by
  intro k
  induction k with
  | zero =>
    dsimp only
    have hpow1 : pow m 1 = m := id_mul m
    have hpow0 : pow m 0 = id := rfl
    rw [hpow1, hpow0]
    simp only [id, tr, chebU, Int.pow_zero, Int.mul_zero, Int.add_zero]
    have hcomm : (m.a + m.d) * 2 = 2 * (m.a + m.d) := Int.mul_comm _ _
    refine ⟨?_, ?_, ?_⟩ <;> omega
  | succ k ih =>
    dsimp only at ih ⊢
    rcases ih with ⟨hA, hU, hQuad⟩
    have hrecA : tr (pow m (k + 2)) = tr m * tr (pow m (k + 1)) - det m * tr (pow m k) :=
      tr_pow_recurrence m k
    have hrecU : chebU (tr m) (det m) (k + 2) =
                 tr m * chebU (tr m) (det m) (k + 1) - det m * chebU (tr m) (det m) k := rfl
    generalize ht : tr m = t at *
    generalize hd : det m = d at *
    generalize hak : tr (pow m k) = ak at *
    generalize hak1 : tr (pow m (k + 1)) = ak1 at *
    generalize huk : chebU t d k = uk at *
    generalize huk1 : chebU t d (k + 1) = uk1 at *
    generalize hD : t * t - 4 * d = D at *
    have hA' : 2 * tr (pow m (k + 2)) = t * ak1 + D * uk1 := by
      have s1 : D * (2 * uk1) = D * (ak + t * uk) := by rw [hU]
      have s2 : D * (ak + t * uk) = D * ak + t * (D * uk) := by
        rw [Int.mul_add]
        have e : D * (t * uk) = t * (D * uk) := by
          rw [← Int.mul_assoc, Int.mul_comm D t, Int.mul_assoc]
        omega
      have s3 : D * uk = 2 * ak1 - t * ak := by omega
      have s4 : D * ak + t * (2 * ak1 - t * ak) = 2 * (t * ak1) - 4 * (d * ak) := by
        have e1 : D * ak = t * t * ak - 4 * d * ak := by
          rw [← hD, Int.sub_mul]
        have e2 : t * (2 * ak1 - t * ak) = t * (2 * ak1) - t * (t * ak) := Int.mul_sub _ _ _
        have e3 : t * (2 * ak1) = 2 * (t * ak1) := by
          rw [← Int.mul_assoc, Int.mul_comm t 2, Int.mul_assoc]
        have e4 : t * (t * ak) = t * t * ak := (Int.mul_assoc t t ak).symm
        have e5 : 4 * d * ak = 4 * (d * ak) := Int.mul_assoc 4 d ak
        omega
      have s5 : D * (2 * uk1) = 2 * (D * uk1) := by
        rw [← Int.mul_assoc, Int.mul_comm D 2, Int.mul_assoc]
      have s6 : 2 * (D * uk1) = 2 * (t * ak1) - 4 * (d * ak) := by
        rw [← s5, s1, s2, s3, s4]
      rw [hrecA]
      omega
    have hU' : 2 * chebU t d (k + 2) = ak1 + t * uk1 := by
      have s2 : t * (2 * uk1) = t * ak + t * t * uk := by
        rw [hU, Int.mul_add, ← Int.mul_assoc]
      have s3 : D * uk = t * t * uk - 4 * d * uk := by
        rw [← hD, Int.sub_mul]
      have e1 : 2 * (t * uk1) = t * (2 * uk1) := by
        rw [← Int.mul_assoc, Int.mul_comm 2 t, Int.mul_assoc]
      have e2 : 4 * d * uk = 4 * (d * uk) := Int.mul_assoc 4 d uk
      rw [hrecU]
      omega
    have hQuad' : ak1 * ak1 - D * (uk1 * uk1) = 4 * d ^ (k + 1) := by
      have lhs1 : (2 * ak1) * (2 * ak1) = 4 * (ak1 * ak1) := by
        calc (2 * ak1) * (2 * ak1) = 2 * (ak1 * (2 * ak1)) := Int.mul_assoc _ _ _
          _ = 2 * (2 * (ak1 * ak1)) := by
              rw [← Int.mul_assoc ak1 2 ak1, Int.mul_comm ak1 2, Int.mul_assoc]
          _ = 4 * (ak1 * ak1) := by rw [← Int.mul_assoc]; rfl
      have lhs2 : D * ((2 * uk1) * (2 * uk1)) = 4 * (D * (uk1 * uk1)) := by
        have e : (2 * uk1) * (2 * uk1) = 4 * (uk1 * uk1) := by
          calc (2 * uk1) * (2 * uk1) = 2 * (uk1 * (2 * uk1)) := Int.mul_assoc _ _ _
            _ = 2 * (2 * (uk1 * uk1)) := by
                rw [← Int.mul_assoc uk1 2 uk1, Int.mul_comm uk1 2, Int.mul_assoc]
            _ = 4 * (uk1 * uk1) := by rw [← Int.mul_assoc]; rfl
        rw [e, ← Int.mul_assoc, Int.mul_comm D 4, Int.mul_assoc]
      have sq1 : (t * ak + D * uk) * (t * ak + D * uk) =
                 t * t * (ak * ak) + 2 * (t * D * ak * uk) + D * D * (uk * uk) := by
        rw [Int.add_mul, Int.mul_add, Int.mul_add]
        have e1 : t * ak * (t * ak) = t * t * (ak * ak) := by
          calc t * ak * (t * ak) = t * (ak * (t * ak)) := Int.mul_assoc _ _ _
            _ = t * ((ak * t) * ak) := by rw [Int.mul_assoc]
            _ = t * ((t * ak) * ak) := by rw [Int.mul_comm ak t]
            _ = t * (t * (ak * ak)) := by rw [Int.mul_assoc]
            _ = t * t * (ak * ak) := by rw [← Int.mul_assoc]
        have e2 : D * uk * (D * uk) = D * D * (uk * uk) := by
          calc D * uk * (D * uk) = D * (uk * (D * uk)) := Int.mul_assoc _ _ _
            _ = D * ((uk * D) * uk) := by rw [Int.mul_assoc]
            _ = D * ((D * uk) * uk) := by rw [Int.mul_comm uk D]
            _ = D * (D * (uk * uk)) := by rw [Int.mul_assoc]
            _ = D * D * (uk * uk) := by rw [← Int.mul_assoc]
        have e3 : t * ak * (D * uk) = t * D * ak * uk := by
          calc t * ak * (D * uk) = t * (ak * (D * uk)) := Int.mul_assoc _ _ _
            _ = t * ((ak * D) * uk) := by rw [Int.mul_assoc]
            _ = t * ((D * ak) * uk) := by rw [Int.mul_comm ak D]
            _ = t * (D * (ak * uk)) := by rw [Int.mul_assoc]
            _ = (t * D) * (ak * uk) := by rw [← Int.mul_assoc]
            _ = t * D * ak * uk := by rw [← Int.mul_assoc]
        have e4 : D * uk * (t * ak) = t * D * ak * uk := by
          rw [Int.mul_comm (D * uk) (t * ak), e3]
        omega
      have sq2 : D * ((ak + t * uk) * (ak + t * uk)) =
                 D * (ak * ak) + 2 * (t * D * ak * uk) + D * (t * t) * (uk * uk) := by
        rw [Int.add_mul, Int.mul_add, Int.mul_add, Int.mul_add, Int.mul_add, Int.mul_add]
        have e1 : D * (ak * (t * uk)) = t * D * ak * uk := by
          calc D * (ak * (t * uk)) = D * ((ak * t) * uk) := by rw [Int.mul_assoc]
            _ = D * ((t * ak) * uk) := by rw [Int.mul_comm ak t]
            _ = (D * (t * ak)) * uk := by rw [← Int.mul_assoc]
            _ = ((D * t) * ak) * uk := by rw [← Int.mul_assoc D t ak]
            _ = ((t * D) * ak) * uk := by rw [Int.mul_comm D t]
        have e2 : D * (t * uk * ak) = t * D * ak * uk := by
          rw [Int.mul_comm (t * uk) ak, e1]
        have e3 : D * (t * uk * (t * uk)) = D * (t * t) * (uk * uk) := by
          have f : t * uk * (t * uk) = (t * t) * (uk * uk) := by
            calc t * uk * (t * uk) = t * (uk * (t * uk)) := Int.mul_assoc _ _ _
              _ = t * ((uk * t) * uk) := by rw [Int.mul_assoc]
              _ = t * ((t * uk) * uk) := by rw [Int.mul_comm uk t]
              _ = t * (t * (uk * uk)) := by rw [Int.mul_assoc]
              _ = (t * t) * (uk * uk) := by rw [← Int.mul_assoc]
          rw [f, ← Int.mul_assoc]
        omega
      have diff : (2 * ak1) * (2 * ak1) - D * ((2 * uk1) * (2 * uk1)) =
                  (4 * d) * (ak * ak - D * (uk * uk)) := by
        rw [hA, hU, sq1, sq2]
        have e1 : (t * t - D) * (ak * ak) = (4 * d) * (ak * ak) := by
          have : t * t - D = 4 * d := by omega
          rw [this]
        have e2 : (t * t - D) * (D * (uk * uk)) = (4 * d) * (D * (uk * uk)) := by
          have : t * t - D = 4 * d := by omega
          rw [this]
        have e3 : (t * t - D) * (ak * ak) = t * t * (ak * ak) - D * (ak * ak) := Int.sub_mul _ _ _
        have e4 : (t * t - D) * (D * (uk * uk)) = D * (t * t) * (uk * uk) - D * D * (uk * uk) := by
          rw [Int.sub_mul]
          have f1 : t * t * (D * (uk * uk)) = D * (t * t) * (uk * uk) := by
            rw [← Int.mul_assoc, Int.mul_comm (t * t) D, Int.mul_assoc]
          have f2 : D * (D * (uk * uk)) = D * D * (uk * uk) := (Int.mul_assoc D D _).symm
          omega
        have e5 : (4 * d) * (ak * ak - D * (uk * uk)) =
                  (4 * d) * (ak * ak) - (4 * d) * (D * (uk * uk)) := Int.mul_sub _ _ _
        omega
      have hpow : (4 * d) * (4 * d ^ k) = 4 * (4 * d ^ (k + 1)) := by
        rw [Int.pow_succ]
        calc (4 * d) * (4 * d ^ k) = 4 * (d * (4 * d ^ k)) := Int.mul_assoc _ _ _
          _ = 4 * (4 * (d * d ^ k)) := by
              rw [← Int.mul_assoc d 4 (d ^ k), Int.mul_comm d 4, Int.mul_assoc]
          _ = 4 * (4 * (d ^ k * d)) := by rw [Int.mul_comm d (d ^ k)]
      rw [hQuad, hpow, lhs1, lhs2] at diff
      omega
    exact ⟨hA', hU', hQuad'⟩

/-- Positivity of `tr(M^k)` and `chebU(k)` for all `k ≥ 1` whenever `tr(M) > 0` and `tr(M)^2 > 4 det(M)`. -/
theorem trace_cheb_pos (m : Mat2Z) (ht : tr m > 0) (hD : tr m * tr m > 4 * det m) :
    ∀ k : Nat, tr (pow m (k + 1)) > 0 ∧ chebU (tr m) (det m) (k + 1) > 0 := by
  intro k
  induction k with
  | zero =>
    constructor
    · simp only [pow, id_mul]; exact ht
    · simp only [chebU]; omega
  | succ k ih =>
    rcases ih with ⟨haPos, huPos⟩
    have hinv := trace_cheb_invariant m (k + 1)
    rcases hinv with ⟨hA, hU, _⟩
    have h1 : tr m * tr (pow m (k + 1)) > 0 := Int.mul_pos ht haPos
    have h2 : (tr m * tr m - 4 * det m) * chebU (tr m) (det m) (k + 1) > 0 :=
      Int.mul_pos (by omega) huPos
    have h3 : tr m * chebU (tr m) (det m) (k + 1) > 0 := Int.mul_pos ht huPos
    constructor <;> omega

/-- Universal power trace obstruction: if `tr(M) > 0` and `tr(M)^2 > 4 det(M)`, then
`tr(M^k)^2 > 4 det(M^k)` holds for EVERY positive integer power `k ≥ 1`. -/
theorem trace_obstruction_all_powers (m : Mat2Z) (ht : tr m > 0) (hD : tr m * tr m > 4 * det m) :
    ∀ k : Nat, k ≥ 1 → tr (pow m k) * tr (pow m k) > 4 * det (pow m k) := by
  intro k hk
  cases k with
  | zero => omega
  | succ n =>
    have hpos := (trace_cheb_pos m ht hD n).2
    have hquad := (trace_cheb_invariant m (n + 1)).2.2
    have hDpos : tr m * tr m - 4 * det m > 0 := by omega
    have hu2 : chebU (tr m) (det m) (n + 1) * chebU (tr m) (det m) (n + 1) > 0 :=
      Int.mul_pos hpos hpos
    have hterm : (tr m * tr m - 4 * det m) * (chebU (tr m) (det m) (n + 1) * chebU (tr m) (det m) (n + 1)) > 0 :=
      Int.mul_pos hDpos hu2
    rw [det_pow]
    omega

end Mat2Z

/-- Explicit `PGL_2(Q_2)` Schottky involution matrices (Section 7.1). -/
def sigmaP : Mat2Z := ⟨0, 1, 2, 0⟩
def sigmaL : Mat2Z := ⟨0, 2, 1, 0⟩
def sigmaR : Mat2Z := ⟨-1, 1, 1, 1⟩

def sigmaOfMove : Move → Mat2Z
  | .P => sigmaP
  | .L => sigmaL
  | .R => sigmaR

def matrixOfWord (w : List Move) : Mat2Z :=
  w.foldl (fun acc m => Mat2Z.mul acc (sigmaOfMove m)) Mat2Z.id

/-- Theorem 7.1(a): Each `σ_s` satisfies `σ_s^2 = 2I`. -/
theorem thm7_1_schottky_involutions :
    Mat2Z.mul sigmaP sigmaP = Mat2Z.scale 2 Mat2Z.id ∧
    Mat2Z.mul sigmaL sigmaL = Mat2Z.scale 2 Mat2Z.id ∧
    Mat2Z.mul sigmaR sigmaR = Mat2Z.scale 2 Mat2Z.id := by
  decide

/-- The explicit kernel word `γ_0 = P L R L P R P L`. -/
def gamma0Word : List Move := [.P, .L, .R, .L, .P, .R, .P, .L]
def gamma0Mat : Mat2Z := matrixOfWord gamma0Word

/-- `γ_0` lies in the Schottky kernel `K = ker(W → D_12)` (fixes all 24 triads). -/
theorem thm7_13_gamma0_in_kernel :
    ∀ (v : Triad), applyWord gamma0Word v = v := by
  decide

/-- Exact integer matrix, trace `85`, determinant `256 = 2^8`, and `τ(γ_0) = 7225/256 > 4`. -/
theorem thm7_13_gamma0_exact :
    gamma0Mat = ⟨5, -12, -12, 80⟩ ∧
    gamma0Mat.tr = 85 ∧
    gamma0Mat.det = 256 ∧
    gamma0Mat.tr * gamma0Mat.tr = 7225 ∧
    gamma0Mat.tr * gamma0Mat.tr > 4 * gamma0Mat.det := by
  decide

/-- Theorem 7.13 (NEG-M8): Every positive power `γ_0^k` (`k ≥ 1`) violates the compact quaternion
trace bound `0 ≤ τ ≤ 4`, ruling out all torsion-free arithmetic uniformisations over any field/place. -/
theorem thm7_13_gamma0_all_powers_obstructed :
    ∀ k : Nat, k ≥ 1 →
      (Mat2Z.pow gamma0Mat k).tr * (Mat2Z.pow gamma0Mat k).tr >
      4 * (Mat2Z.pow gamma0Mat k).det :=
  Mat2Z.trace_obstruction_all_powers gamma0Mat (by decide) (by decide)

end Morpheus
