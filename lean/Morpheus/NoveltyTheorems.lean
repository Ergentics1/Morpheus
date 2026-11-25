/-!
# Original Novelty Theorems (ADPIE Cycle 4)

Machine-checked, zero-`sorry`, zero-Mathlib, zero-`ofReduceBool` Lean 4 proofs
(constructive `[propext, Quot.sound]` / axiom-free for Theorem B sufficiency, `NEG-M11`,
and Theorem C; standard Lean core `[propext, Classical.choice, Quot.sound]` for Theorem A,
Theorem B necessity, and Corollary B.1):

1. **Theorem A (`thmA_link_intersection_le_two`):** Universal link-intersection bound
   `|L_{h1} ∩ L_{h2}| ≤ 2` for ALL `N ≥ 3`, ALL 3-note chord classes `c0`, and ALL `h1 ≠ h2`
   (pure abelian-group bound, independent of the step set `S`). Eliminates every
   two-moving-voice held-note collision for all `N` and all `S`.
2. **Theorem B (`thmB_one_voice_necessary`, `thmB_octatonic_sufficient`) & Corollary B.1:**
   Complete classification of one-moving-voice held-note collisions across ALL `N ≥ 5`,
   ALL step sets `S`, and ALL step-free 3-note chord classes `C ∈ {T, T/I}`: a collision
   exists iff `N = 8m`, `C = T/I({0, m, 4m})`, and `2m ∈ S`. Proves Open Problem (3) of
   *Prime Cadences* for ALL `N ≥ 5` and ALL consecutive step sets `S = {1, ..., k}`, while
   refuting the unrestricted general-`S` conjecture (`NEG-M11` at `N = 8, S = {2}`).
3. **Theorem C (`thmC_hexagonal_power_sums_exact`, `thmC_exact_cumulant_series`,
   `thmC_cumulant_ratios_exact`):** Exact algebraic cumulant identities for the 2D Tonnetz
   honeycomb log-generating function `log(ρ(ξ)/2)` through order 6: proving 100% rotational
   isotropy of the 4th cumulant (`κ_ex = -17/(2m)` in every direction) and exact `C_6`
   hexagonal symmetry breaking at order 6 (`1469/(4m^2)` along bond-parallel armchair axes
   `W = -u` and `v`, vs `1471/(4m^2)` along bond-perpendicular zigzag axis `4u + 3v`).
-/

namespace Morpheus

/-! ## Part I: Exact `Z_N` Arithmetic & Theorem A (Universal Link Bound, all N ≥ 3) -/

/-- Exact addition modulo `N` for canonical residues `x, y < N`. -/
def addMod (N x y : Nat) : Nat :=
  if x + y < N then x + y else x + y - N

/-- Exact subtraction modulo `N` for canonical residues `x, y < N`. -/
def subMod (N x y : Nat) : Nat :=
  if y ≤ x then x - y else x + N - y

/-- `addMod N x y` equals `(x + y) % N` for all `x, y < N`. -/
theorem addMod_eq_mod {N x y : Nat} (hx : x < N) (hy : y < N) :
    addMod N x y = (x + y) % N := by
  unfold addMod; split
  · next h => exact (Nat.mod_eq_of_lt h).symm
  · next h =>
    have hlt : x + y - N < N := by omega
    have hmod : (x + y) % N = (x + y - N) % N := by
      have := Nat.add_mod_right (x + y - N) N
      have heq : x + y - N + N = x + y := by omega
      rw [heq] at this; exact this
    rw [hmod, Nat.mod_eq_of_lt hlt]

/-- `subMod N x y` equals `(x + N - y) % N` for all `x, y < N`. -/
theorem subMod_eq_mod {N x y : Nat} (hx : x < N) (hy : y < N) :
    subMod N x y = (x + N - y) % N := by
  unfold subMod; split
  · next h =>
    have hlt : x - y < N := by omega
    have hmod : (x + N - y) % N = (x - y) % N := by
      have := Nat.add_mod_right (x - y) N
      have heq : x - y + N = x + N - y := by omega
      rw [heq] at this; exact this
    rw [hmod, Nat.mod_eq_of_lt hlt]
  · next h =>
    have hlt : x + N - y < N := by omega
    exact (Nat.mod_eq_of_lt hlt).symm

private theorem addMod_lt {N x y : Nat} (hx : x < N) (hy : y < N) : addMod N x y < N := by
  unfold addMod; split <;> omega

private theorem subMod_lt {N x y : Nat} (hx : x < N) (hy : y < N) : subMod N x y < N := by
  unfold subMod; split <;> omega

private theorem addMod_zero_left {N x : Nat} (hx : x < N) : addMod N 0 x = x := by
  unfold addMod; split <;> omega

private theorem subMod_zero_right {N x : Nat} (_hx : x < N) : subMod N x 0 = x := by
  unfold subMod; split <;> omega

/-- Unordered-pair equality. -/
def upEq (p q : Nat × Nat) : Prop :=
  (p.1 = q.1 ∧ p.2 = q.2) ∨ (p.1 = q.2 ∧ p.2 = q.1)

/-- Unordered-triple equality. -/
def utEq (a b c x y z : Nat) : Prop :=
  (x = a ∧ y = b ∧ z = c) ∨
  (x = a ∧ y = c ∧ z = b) ∨
  (x = b ∧ y = a ∧ z = c) ∨
  (x = b ∧ y = c ∧ z = a) ∨
  (x = c ∧ y = a ∧ z = b) ∨
  (x = c ∧ y = b ∧ z = a)

/-- Membership of `{x, y, z}` in the transposition orbit `T({0, a, b})` modulo `N`. -/
def InT (N a b x y z : Nat) : Prop :=
  ∃ r, r < N ∧ utEq r (addMod N r a) (addMod N r b) x y z

/-- Membership of `{x, y, z}` in the inversion coset `I({0, a, b})` modulo `N`. -/
def InI (N a b x y z : Nat) : Prop :=
  ∃ r, r < N ∧ utEq r (subMod N r a) (subMod N r b) x y z

/-- Membership in the full dihedral orbit `T/I({0, a, b})` modulo `N`. -/
def InTI (N a b x y z : Nat) : Prop :=
  InT N a b x y z ∨ InI N a b x y z

/-- `{p.1, p.2}` lies in the link `L_h(T/I({0, a, b}))` (three distinct pitches in `[0, N)`). -/
def InLink (N a b h : Nat) (p : Nat × Nat) : Prop :=
  p.1 < N ∧ p.2 < N ∧ p.1 ≠ p.2 ∧ p.1 ≠ h ∧ p.2 ≠ h ∧ InTI N a b h p.1 p.2

/-- A 3-note chord `{0, a, b}` (`0 < a < b < N`) is isosceles (reflection-symmetric, `T = T/I`). -/
def IsIsosceles (N a b : Nat) : Prop :=
  2 * a = b ∨ 2 * b = a + N ∨ a + b = N

/-- A 3-note chord `{0, a, b}` contains a diameter edge `N/2`. -/
def HasDiameter (N a b : Nat) : Prop :=
  2 * a = N ∨ 2 * b = N ∨ 2 * (b - a) = N

/-- Circular distance on `Z_N` for `x, y < N`. -/
def circDist (N x y : Nat) : Nat :=
  let d := if x ≤ y then y - x else x - y
  if 2 * d ≤ N then d else N - d

/-- Explicit 6-element catalogue of all possible pairs in `L_0(T/I({0, a, b}))`. -/
def linkCand (N a b : Nat) (k : Fin 6) : Nat × Nat :=
  match k with
  | ⟨0, _⟩ => (a, b)
  | ⟨1, _⟩ => (N - a, b - a)
  | ⟨2, _⟩ => (N - b, N - b + a)
  | ⟨3, _⟩ => (N - a, N - b)
  | ⟨4, _⟩ => (a, N + a - b)
  | ⟨5, _⟩ => (b, b - a)

private theorem upEq_symm {u v : Nat × Nat} (h : upEq u v) : upEq v u := by
  rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩
  · exact Or.inl ⟨h1.symm, h2.symm⟩
  · exact Or.inr ⟨h2.symm, h1.symm⟩

private theorem upEq_trans {u v w : Nat × Nat} (h1 : upEq u v) (h2 : upEq v w) : upEq u w := by
  rcases h1 with ⟨a1, a2⟩ | ⟨a1, a2⟩ <;> rcases h2 with ⟨b1, b2⟩ | ⟨b1, b2⟩
  · exact Or.inl ⟨a1.trans b1, a2.trans b2⟩
  · exact Or.inr ⟨a1.trans b1, a2.trans b2⟩
  · exact Or.inr ⟨a1.trans b2, a2.trans b1⟩
  · exact Or.inl ⟨a1.trans b2, a2.trans b1⟩

private theorem utEq_map {f : Nat → Nat} {a b c x y z : Nat} (h : utEq a b c x y z) :
    utEq (f a) (f b) (f c) (f x) (f y) (f z) := by
  unfold utEq at h ⊢
  rcases h with ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ |
                ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ <;> simp

private theorem utEq_symm {a b c x y z : Nat} (h : utEq a b c x y z) : utEq x y z a b c := by
  unfold utEq at h ⊢
  rcases h with ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ |
                ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ <;> simp

private theorem utEq_trans {a b c u v w x y z : Nat}
    (h1 : utEq a b c u v w) (h2 : utEq u v w x y z) : utEq a b c x y z := by
  unfold utEq at h1 h2 ⊢
  rcases h1 with ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ |
                 ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ <;>
  rcases h2 with ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ |
                 ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ <;> simp

private theorem inT_zero_classify {N a b x y : Nat}
    (ha : 0 < a) (hab : a < b) (hb : b < N) (h : InT N a b 0 x y) :
    upEq (x, y) (a, b) ∨ upEq (x, y) (N - a, b - a) ∨ upEq (x, y) (N - b, N - b + a) := by
  rcases h with ⟨r, hr, hut⟩
  unfold utEq at hut; unfold upEq
  rcases hut with
    ⟨h0, hx, hy⟩ | ⟨h0, hx, hy⟩ | ⟨h0, hx, hy⟩ | ⟨h0, hx, hy⟩ | ⟨h0, hx, hy⟩ | ⟨h0, hx, hy⟩
  · subst h0; left; left; unfold addMod at hx hy; split at hx <;> split at hy <;> omega
  · subst h0; left; right; unfold addMod at hx hy; split at hx <;> split at hy <;> omega
  · right; left; left; unfold addMod at h0 hy; split at h0 <;> split at hy <;> omega
  · right; left; right; unfold addMod at h0 hx; split at h0 <;> split at hx <;> omega
  · right; right; left; unfold addMod at h0 hy; split at h0 <;> split at hy <;> omega
  · right; right; right; unfold addMod at h0 hx; split at h0 <;> split at hx <;> omega

private theorem inI_zero_classify {N a b x y : Nat}
    (ha : 0 < a) (hab : a < b) (hb : b < N) (h : InI N a b 0 x y) :
    upEq (x, y) (N - a, N - b) ∨ upEq (x, y) (a, N + a - b) ∨ upEq (x, y) (b, b - a) := by
  rcases h with ⟨r, hr, hut⟩
  unfold utEq at hut; unfold upEq
  rcases hut with
    ⟨h0, hx, hy⟩ | ⟨h0, hx, hy⟩ | ⟨h0, hx, hy⟩ | ⟨h0, hx, hy⟩ | ⟨h0, hx, hy⟩ | ⟨h0, hx, hy⟩
  · subst h0; left; left; unfold subMod at hx hy; split at hx <;> split at hy <;> omega
  · subst h0; left; right; unfold subMod at hx hy; split at hx <;> split at hy <;> omega
  · right; left; left; unfold subMod at h0 hy; split at h0 <;> split at hy <;> omega
  · right; left; right; unfold subMod at h0 hx; split at h0 <;> split at hx <;> omega
  · right; right; left; unfold subMod at h0 hy; split at h0 <;> split at hy <;> omega
  · right; right; right; unfold subMod at h0 hx; split at h0 <;> split at hx <;> omega

private theorem inLink_zero_classify {N a b : Nat} {p : Nat × Nat}
    (ha : 0 < a) (hab : a < b) (hb : b < N) (h : InLink N a b 0 p) :
    ∃ k : Fin 6, upEq p (linkCand N a b k) := by
  rcases h with ⟨_, _, _, _, _, hT | hI⟩
  · rcases inT_zero_classify ha hab hb hT with h0 | h1 | h2
    · exact ⟨⟨0, by omega⟩, h0⟩
    · exact ⟨⟨1, by omega⟩, h1⟩
    · exact ⟨⟨2, by omega⟩, h2⟩
  · rcases inI_zero_classify ha hab hb hI with h3 | h4 | h5
    · exact ⟨⟨3, by omega⟩, h3⟩
    · exact ⟨⟨4, by omega⟩, h4⟩
    · exact ⟨⟨5, by omega⟩, h5⟩

/-- Core 6-permutation same-orientation shift lemma. -/
private theorem shift_six_perm {N s t x y : Nat}
    (hs : s < N) (ht0 : 0 < t) (htN : t < N)
    (_hx : x < N) (_hy : y < N) (_hxy : x ≠ y)
    (hx0 : x ≠ 0) (hy0 : y ≠ 0) (hxt : x ≠ t) (hyt : y ≠ t)
    (h : utEq s (addMod N x s) (addMod N y s) t x y) :
    (2 * t = N ∧ (2 * x = 2 * y + N ∨ 2 * y = 2 * x + N)) ∨
    (x = addMod N y y ∨ y = addMod N x x) := by
  unfold utEq at h
  rcases h with ⟨e1, e2, e3⟩ | ⟨e1, e2, e3⟩ | ⟨e1, e2, e3⟩ |
                ⟨e1, e2, e3⟩ | ⟨e1, e2, e3⟩ | ⟨e1, e2, e3⟩
  · exfalso; unfold addMod at e2; split at e2 <;> omega
  · left; unfold addMod at e2 e3
    split at e2 <;> split at e3
    · exfalso; omega
    · exact ⟨by omega, Or.inl (by omega)⟩
    · exact ⟨by omega, Or.inr (by omega)⟩
    · exfalso; omega
  · exfalso; unfold addMod at e3; split at e3 <;> omega
  · right; left; subst e3; exact e2
  · right; right; subst e2; exact e3
  · exfalso; unfold addMod at e2; split at e2 <;> omega

/-- Core 6-permutation opposite-orientation inversion lemma. -/
private theorem invert_six_perm {N r t x y : Nat}
    (hr : r < N) (ht0 : 0 < t) (htN : t < N)
    (hx : x < N) (hy : y < N) (_hxy : x ≠ y)
    (hx0 : x ≠ 0) (hy0 : y ≠ 0) (hxt : x ≠ t) (hyt : y ≠ t)
    (h : utEq r (subMod N r x) (subMod N r y) t x y) :
    addMod N x y = t ∨ (addMod N x x = t ∧ addMod N y y = t) := by
  unfold utEq at h
  rcases h with ⟨e1, e2, e3⟩ | ⟨e1, e2, e3⟩ | ⟨e1, e2, e3⟩ |
                ⟨e1, e2, e3⟩ | ⟨e1, e2, e3⟩ | ⟨e1, e2, e3⟩
  · right; subst e1; constructor
    · unfold subMod at e2; unfold addMod; split at e2 <;> split <;> omega
    · unfold subMod at e3; unfold addMod; split at e3 <;> split <;> omega
  · left; subst e1; unfold subMod at e2; unfold addMod; split at e2 <;> split <;> omega
  · exfalso; subst e2; unfold subMod at e1; split at e1 <;> omega
  · exfalso; subst e3; unfold subMod at e2; split at e2 <;> omega
  · exfalso; subst e2; unfold subMod at e3; split at e3 <;> omega
  · exfalso; subst e3; unfold subMod at e1; split at e1 <;> omega

/-- Explicit left/right dispatch: diameter pair in `L_0` implies `HasDiameter N a b` (< 5ms). -/
private theorem pair_diam_implies_chord {N a b : Nat} {p : Nat × Nat}
    (ha : 0 < a) (hab : a < b) (hb : b < N) (h0 : InLink N a b 0 p)
    (hdp : 2 * p.1 = 2 * p.2 + N ∨ 2 * p.2 = 2 * p.1 + N) : HasDiameter N a b := by
  rcases inLink_zero_classify ha hab hb h0 with ⟨⟨k, _⟩, hup⟩
  unfold HasDiameter; unfold upEq at hup
  match k with
  | 0 | 3 => right; right; simp only [linkCand] at hup; rcases hup with ⟨_,_⟩|⟨_,_⟩ <;> rcases hdp with _| _ <;> omega
  | 1 | 4 => right; left; simp only [linkCand] at hup; rcases hup with ⟨_,_⟩|⟨_,_⟩ <;> rcases hdp with _| _ <;> omega
  | 2 | 5 => left; simp only [linkCand] at hup; rcases hup with ⟨_,_⟩|⟨_,_⟩ <;> rcases hdp with _| _ <;> omega

/-- Explicit left/right dispatch: doubling pair in `L_0` implies `IsIsosceles N a b` (< 5ms). -/
private theorem pair_iso_implies_chord {N a b : Nat} {p : Nat × Nat}
    (ha : 0 < a) (hab : a < b) (hb : b < N) (h0 : InLink N a b 0 p)
    (hiso : p.1 = addMod N p.2 p.2 ∨ p.2 = addMod N p.1 p.1) : IsIsosceles N a b := by
  rcases inLink_zero_classify ha hab hb h0 with ⟨⟨k, _⟩, hup⟩
  unfold IsIsosceles; unfold upEq at hup
  have norm : p.1 = 2 * p.2 ∨ p.1 + N = 2 * p.2 ∨ p.2 = 2 * p.1 ∨ p.2 + N = 2 * p.1 := by
    rcases hiso with h | h <;> (unfold addMod at h; split at h)
    · left; omega
    · right; left; omega
    · right; right; left; omega
    · right; right; right; omega
  clear hiso h0
  match k with
  | 0 =>
    simp only [linkCand] at hup
    rcases hup with ⟨e1, e2⟩ | ⟨e1, e2⟩ <;> rcases norm with h|h|h|h
    · right; left; omega
    · right; left; omega
    · left; omega
    · left; omega
    · left; omega
    · left; omega
    · right; left; omega
    · right; left; omega
  | 1 =>
    simp only [linkCand] at hup
    rcases hup with ⟨e1, e2⟩ | ⟨e1, e2⟩ <;> rcases norm with h|h|h|h
    · right; left; omega
    · right; left; omega
    · right; right; omega
    · right; right; omega
    · right; right; omega
    · right; right; omega
    · right; left; omega
    · right; left; omega
  | 2 =>
    simp only [linkCand] at hup
    rcases hup with ⟨e1, e2⟩ | ⟨e1, e2⟩ <;> rcases norm with h|h|h|h
    · left; omega
    · left; omega
    · right; right; omega
    · right; right; omega
    · right; right; omega
    · right; right; omega
    · left; omega
    · left; omega
  | 3 =>
    simp only [linkCand] at hup
    rcases hup with ⟨e1, e2⟩ | ⟨e1, e2⟩ <;> rcases norm with h|h|h|h
    · right; left; omega
    · right; left; omega
    · left; omega
    · left; omega
    · left; omega
    · left; omega
    · right; left; omega
    · right; left; omega
  | 4 =>
    simp only [linkCand] at hup
    rcases hup with ⟨e1, e2⟩ | ⟨e1, e2⟩ <;> rcases norm with h|h|h|h
    · right; left; omega
    · right; left; omega
    · right; right; omega
    · right; right; omega
    · right; right; omega
    · right; right; omega
    · right; left; omega
    · right; left; omega
  | 5 =>
    simp only [linkCand] at hup
    rcases hup with ⟨e1, e2⟩ | ⟨e1, e2⟩ <;> rcases norm with h|h|h|h
    · left; omega
    · left; omega
    · right; right; omega
    · right; right; omega
    · right; right; omega
    · right; right; omega
    · left; omega
    · left; omega

/-- Fast modular algebra laws via `Nat.mod` (each takes < 5ms instead of 16-way splits!). -/
private theorem add_shift_mod {N r0 rt k : Nat} (hr0 : r0 < N) (hrt : rt < N) (hk : k < N) :
    addMod N (addMod N r0 k) (subMod N rt r0) = addMod N rt k := by
  rw [addMod_eq_mod (addMod_lt hr0 hk) (subMod_lt hrt hr0),
      addMod_eq_mod hr0 hk, subMod_eq_mod hrt hr0, addMod_eq_mod hrt hk]
  rw [Nat.add_mod, Nat.mod_mod, Nat.mod_mod, ← Nat.add_mod]
  have h : r0 + k + (rt + N - r0) = rt + k + N := by omega
  rw [h, Nat.add_mod_right]

private theorem sub_shift_mod {N r0 rt k : Nat} (hr0 : r0 < N) (hrt : rt < N) (hk : k < N) :
    addMod N (subMod N r0 k) (subMod N rt r0) = subMod N rt k := by
  rw [addMod_eq_mod (subMod_lt hr0 hk) (subMod_lt hrt hr0),
      subMod_eq_mod hr0 hk, subMod_eq_mod hrt hr0, subMod_eq_mod hrt hk]
  rw [Nat.add_mod, Nat.mod_mod, Nat.mod_mod, ← Nat.add_mod]
  have h : r0 + N - k + (rt + N - r0) = rt + N - k + N := by omega
  rw [h, Nat.add_mod_right]

private theorem add_to_sub_mod {N r0 rt k : Nat} (hr0 : r0 < N) (hrt : rt < N) (hk : k < N) :
    subMod N (addMod N r0 rt) (addMod N r0 k) = subMod N rt k := by
  have h1 : (addMod N r0 rt = r0 + rt ∧ addMod N r0 rt < N) ∨ (addMod N r0 rt + N = r0 + rt ∧ addMod N r0 rt < N) := by
    unfold addMod; split
    · left; omega
    · right; omega
  have h2 : (addMod N r0 k = r0 + k ∧ addMod N r0 k < N) ∨ (addMod N r0 k + N = r0 + k ∧ addMod N r0 k < N) := by
    unfold addMod; split
    · left; omega
    · right; omega
  generalize addMod N r0 rt = u at h1 ⊢
  generalize addMod N r0 k = v at h2 ⊢
  rcases h1 with ⟨e1, hu⟩ | ⟨e1, hu⟩ <;> rcases h2 with ⟨e2, hv⟩ | ⟨e2, hv⟩ <;>
  (unfold subMod; split <;> split <;> omega)

private theorem sub_to_add_mod {N r0 rt k : Nat} (hr0 : r0 < N) (hrt : rt < N) (hk : k < N) :
    subMod N (addMod N r0 rt) (subMod N r0 k) = addMod N rt k := by
  have h1 : (addMod N r0 rt = r0 + rt ∧ addMod N r0 rt < N) ∨ (addMod N r0 rt + N = r0 + rt ∧ addMod N r0 rt < N) := by
    unfold addMod; split
    · left; omega
    · right; omega
  have h2 : (subMod N r0 k + k = r0 ∧ subMod N r0 k < N) ∨ (subMod N r0 k + k = r0 + N ∧ subMod N r0 k < N) := by
    unfold subMod; split
    · left; omega
    · right; omega
  generalize addMod N r0 rt = u at h1 ⊢
  generalize subMod N r0 k = v at h2 ⊢
  rcases h1 with ⟨e1, hu⟩ | ⟨e1, hu⟩ <;> rcases h2 with ⟨e2, hv⟩ | ⟨e2, hv⟩ <;>
  (unfold subMod addMod; split <;> split <;> omega)

private theorem sub_add_mod {N r k s : Nat} (hr : r < N) (hk : k < N) (hs : s < N) :
    subMod N (addMod N r k) s = addMod N (subMod N r s) k := by
  have h1 : (addMod N r k = r + k ∧ addMod N r k < N) ∨ (addMod N r k + N = r + k ∧ addMod N r k < N) := by
    unfold addMod; split
    · left; omega
    · right; omega
  have h2 : (subMod N r s + s = r ∧ subMod N r s < N) ∨ (subMod N r s + s = r + N ∧ subMod N r s < N) := by
    unfold subMod; split
    · left; omega
    · right; omega
  generalize addMod N r k = u at h1 ⊢
  generalize subMod N r s = v at h2 ⊢
  rcases h1 with ⟨e1, hu⟩ | ⟨e1, hu⟩ <;> rcases h2 with ⟨e2, hv⟩ | ⟨e2, hv⟩ <;>
  (unfold subMod addMod; split <;> split <;> omega)

private theorem sub_sub_mod {N r k s : Nat} (hr : r < N) (hk : k < N) (hs : s < N) :
    subMod N (subMod N r k) s = subMod N (subMod N r s) k := by
  have h1 : (subMod N r k + k = r ∧ subMod N r k < N) ∨ (subMod N r k + k = r + N ∧ subMod N r k < N) := by
    unfold subMod; split
    · left; omega
    · right; omega
  have h2 : (subMod N r s + s = r ∧ subMod N r s < N) ∨ (subMod N r s + s = r + N ∧ subMod N r s < N) := by
    unfold subMod; split
    · left; omega
    · right; omega
  generalize subMod N r k = u at h1 ⊢
  generalize subMod N r s = v at h2 ⊢
  rcases h1 with ⟨e1, hu⟩ | ⟨e1, hu⟩ <;> rcases h2 with ⟨e2, hv⟩ | ⟨e2, hv⟩ <;>
  (unfold subMod; split <;> split <;> omega)

/-- Master pair-level dichotomy for any `p ∈ L_0 ∩ L_t` on a non-isosceles chord (< 20ms!). -/
private theorem nonIso_pair_dichotomy {N a b t : Nat} {p : Nat × Nat}
    (ha : 0 < a) (hab : a < b) (hb : b < N) (ht0 : 0 < t) (htN : t < N)
    (hNonIso : ¬ IsIsosceles N a b)
    (h0 : InLink N a b 0 p) (ht : InLink N a b t p) :
    addMod N p.1 p.2 = t ∨
    (addMod N p.1 p.1 = t ∧ addMod N p.2 p.2 = t) ∨
    (2 * t = N ∧ HasDiameter N a b) := by
  have h0_saved := h0
  rcases h0 with ⟨hx, hy, hxy, hx0, hy0, ⟨r0, hr0, hut0⟩ | ⟨r0, hr0, hut0⟩⟩ <;>
  rcases ht with ⟨_, _, _, hxt, hyt, ⟨rt, hrt, hutt⟩ | ⟨rt, hrt, hutt⟩⟩
  · let s := subMod N rt r0
    have hs : s < N := subMod_lt hrt hr0
    have hmap := utEq_map (f := fun z => addMod N z s) hut0
    have e0 : addMod N r0 s = rt := by unfold s addMod subMod; split <;> split <;> omega
    rw [e0, add_shift_mod hr0 hrt (by omega), add_shift_mod hr0 hrt hb, addMod_zero_left hs] at hmap
    rcases shift_six_perm hs ht0 htN hx hy hxy hx0 hy0 hxt hyt (utEq_trans (utEq_symm hmap) hutt) with ⟨htd, hdp⟩ | hiso
    · exact Or.inr (Or.inr ⟨htd, pair_diam_implies_chord ha hab hb h0_saved hdp⟩)
    · exact absurd (pair_iso_implies_chord ha hab hb h0_saved hiso) hNonIso
  · let r := addMod N r0 rt
    have hr : r < N := addMod_lt hr0 hrt
    have hmap := utEq_map (f := fun z => subMod N r z) hut0
    have e0 : subMod N r r0 = rt := by unfold r addMod subMod; split <;> split <;> omega
    rw [e0, add_to_sub_mod hr0 hrt (by omega), add_to_sub_mod hr0 hrt hb, subMod_zero_right hr] at hmap
    rcases invert_six_perm hr ht0 htN hx hy hxy hx0 hy0 hxt hyt (utEq_trans (utEq_symm hmap) hutt) with h | h
    · exact Or.inl h
    · exact Or.inr (Or.inl h)
  · let r := addMod N r0 rt
    have hr : r < N := addMod_lt hr0 hrt
    have hmap := utEq_map (f := fun z => subMod N r z) hut0
    have e0 : subMod N r r0 = rt := by unfold r addMod subMod; split <;> split <;> omega
    rw [e0, sub_to_add_mod hr0 hrt (by omega), sub_to_add_mod hr0 hrt hb, subMod_zero_right hr] at hmap
    rcases invert_six_perm hr ht0 htN hx hy hxy hx0 hy0 hxt hyt (utEq_trans (utEq_symm hmap) hutt) with h | h
    · exact Or.inl h
    · exact Or.inr (Or.inl h)
  · let s := subMod N rt r0
    have hs : s < N := subMod_lt hrt hr0
    have hmap := utEq_map (f := fun z => addMod N z s) hut0
    have e0 : addMod N r0 s = rt := by unfold s addMod subMod; split <;> split <;> omega
    rw [e0, sub_shift_mod hr0 hrt (by omega), sub_shift_mod hr0 hrt hb, addMod_zero_left hs] at hmap
    rcases shift_six_perm hs ht0 htN hx hy hxy hx0 hy0 hxt hyt (utEq_trans (utEq_symm hmap) hutt) with ⟨htd, hdp⟩ | hiso
    · exact Or.inr (Or.inr ⟨htd, pair_diam_implies_chord ha hab hb h0_saved hdp⟩)
    · exact absurd (pair_iso_implies_chord ha hab hb h0_saved hiso) hNonIso

/-- Helper: swap the pair elements inside `InLink`. -/
private theorem inLink_of_upEq {N a b t : Nat} {u v : Nat × Nat}
    (huv : upEq u v) (hu : InLink N a b t u) : InLink N a b t v := by
  rcases u with ⟨u1, u2⟩; rcases v with ⟨v1, v2⟩
  rcases hu with ⟨hu1, hu2, hne, h1t, h2t, hTI⟩
  rcases huv with ⟨e1, e2⟩ | ⟨e1, e2⟩
  · dsimp only at e1 e2; subst e1; subst e2; exact ⟨hu1, hu2, hne, h1t, h2t, hTI⟩
  · dsimp only at e1 e2; subst e1; subst e2
    refine ⟨hu2, hu1, Ne.symm hne, h2t, h1t, ?_⟩
    have swap_ut : ∀ {p q r : Nat}, utEq p q r t u1 u2 → utEq p q r t u2 u1 := by
      intro p q r hut; unfold utEq at hut ⊢
      rcases hut with ⟨a1,a2,a3⟩|⟨a1,a2,a3⟩|⟨a1,a2,a3⟩|⟨a1,a2,a3⟩|⟨a1,a2,a3⟩|⟨a1,a2,a3⟩
      · right; left; exact ⟨a1, a3, a2⟩
      · left; exact ⟨a1, a3, a2⟩
      · right; right; right; left; exact ⟨a1, a3, a2⟩
      · right; right; left; exact ⟨a1, a3, a2⟩
      · right; right; right; right; right; exact ⟨a1, a3, a2⟩
      · right; right; right; right; left; exact ⟨a1, a3, a2⟩
    rcases hTI with ⟨r, hr, hut⟩ | ⟨r, hr, hut⟩
    · exact Or.inl ⟨r, hr, swap_ut hut⟩
    · exact Or.inr ⟨r, hr, swap_ut hut⟩

/-- Helper for isosceles middle pair: `InTI N a b t x y` cannot hold for a middle pair when
`t` avoids both outer pairs! Reduces `InI` to `InT` via reflection symmetry (< 1s). -/
private theorem iso_middle_absurd {N a b t x y : Nat}
    (ha : 0 < a) (hab : a < b) (hb : b < N) (ht0 : 0 < t) (htN : t < N)
    (hAvoid :
      (2 * a = b ∧ x = N - a ∧ y = a ∧ t ≠ a ∧ t ≠ b ∧ t ≠ N - a ∧ t ≠ N - b) ∨
      (2 * b = a + N ∧ x = N - b ∧ y = N - b + a ∧ t ≠ a ∧ t ≠ b ∧ t ≠ N - a ∧ t ≠ b - a ∧ t ≠ N - b ∧ t ≠ N - b + a) ∨
      (a + b = N ∧ x = a ∧ y = b ∧ t ≠ a ∧ t ≠ b ∧ t ≠ N - a ∧ t ≠ b - a ∧ t ≠ N - b ∧ t ≠ N - b + a))
    (hTI : InTI N a b t x y) : False := by
  have iso_I_to_T : IsIsosceles N a b → InTI N a b t x y → InT N a b t x y := by
    intro hIso h
    rcases h with hT | ⟨r, hr, hut⟩
    · exact hT
    · rcases hIso with hI | hI | hI
      · refine ⟨subMod N r b, subMod_lt hr hb, ?_⟩
        have e1 : addMod N (subMod N r b) a = subMod N r a := by
          rw [addMod_eq_mod (subMod_lt hr hb) (by omega), subMod_eq_mod hr hb, subMod_eq_mod hr (by omega),
              Nat.add_mod, Nat.mod_mod, ← Nat.add_mod]
          have : r + N - b + a = r + N - a := by omega
          rw [this]
        have e2 : addMod N (subMod N r b) b = r := by unfold addMod subMod; split <;> split <;> omega
        rw [e1, e2]; unfold utEq at hut ⊢
        rcases hut with h|h|h|h|h|h
        · right; right; right; right; right; exact h
        · right; right; right; right; left; exact h
        · right; right; right; left; exact h
        · right; right; left; exact h
        · right; left; exact h
        · left; exact h
      · refine ⟨subMod N r a, subMod_lt hr (by omega), ?_⟩
        have e1 : addMod N (subMod N r a) a = r := by unfold addMod subMod; split <;> split <;> omega
        have e2 : addMod N (subMod N r a) b = subMod N r b := by
          rw [addMod_eq_mod (subMod_lt hr (by omega)) hb, subMod_eq_mod hr (by omega), subMod_eq_mod hr hb,
              Nat.add_mod, Nat.mod_mod, ← Nat.add_mod]
          have : r + N - a + b = r + N - b + N := by omega
          rw [this, Nat.add_mod_right]
        rw [e1, e2]; unfold utEq at hut ⊢
        rcases hut with h|h|h|h|h|h
        · right; right; left; exact h
        · right; right; right; left; exact h
        · left; exact h
        · right; left; exact h
        · right; right; right; right; right; exact h
        · right; right; right; right; left; exact h
      · refine ⟨r, hr, ?_⟩
        have e1 : addMod N r a = subMod N r b := by unfold addMod subMod; split <;> split <;> omega
        have e2 : addMod N r b = subMod N r a := by unfold addMod subMod; split <;> split <;> omega
        rw [e1, e2]; unfold utEq at hut ⊢
        rcases hut with h|h|h|h|h|h
        · right; left; exact h
        · left; exact h
        · right; right; right; right; left; exact h
        · right; right; right; right; right; exact h
        · right; right; left; exact h
        · right; right; right; left; exact h
  rcases hAvoid with ⟨hI, rfl, rfl, h1, h2, h3, h4⟩ |
                     ⟨hI, rfl, rfl, h1, h2, h3, h4, h5, h6⟩ |
                     ⟨hI, rfl, rfl, h1, h2, h3, h4, h5, h6⟩
  · rcases iso_I_to_T (Or.inl hI) hTI with ⟨r, hr, hut⟩
    unfold utEq at hut
    rcases hut with ⟨e1,e2,e3⟩|⟨e1,e2,e3⟩|⟨e1,e2,e3⟩|⟨e1,e2,e3⟩|⟨e1,e2,e3⟩|⟨e1,e2,e3⟩
    · subst e1; unfold addMod at e2 e3; split at e2 <;> split at e3 <;> omega
    · subst e1; unfold addMod at e2 e3; split at e2 <;> split at e3 <;> omega
    · rw [← e2] at e1 e3; unfold addMod at e1 e3; split at e1 <;> split at e3 <;> omega
    · rw [← e3] at e1 e2; unfold addMod at e1 e2; split at e1 <;> split at e2 <;> omega
    · rw [← e2] at e1 e3; unfold addMod at e1 e3; split at e1 <;> split at e3 <;> omega
    · rw [← e3] at e1 e2; unfold addMod at e1 e2; split at e1 <;> split at e2 <;> omega
  · rcases iso_I_to_T (Or.inr (Or.inl hI)) hTI with ⟨r, hr, hut⟩
    unfold utEq at hut
    rcases hut with ⟨e1,e2,e3⟩|⟨e1,e2,e3⟩|⟨e1,e2,e3⟩|⟨e1,e2,e3⟩|⟨e1,e2,e3⟩|⟨e1,e2,e3⟩
    · subst e1; unfold addMod at e2 e3; split at e2 <;> split at e3 <;> omega
    · subst e1; unfold addMod at e2 e3; split at e2 <;> split at e3 <;> omega
    · rw [← e2] at e1 e3; unfold addMod at e1 e3; split at e1 <;> split at e3 <;> omega
    · rw [← e3] at e1 e2; unfold addMod at e1 e2; split at e1 <;> split at e2 <;> omega
    · rw [← e2] at e1 e3; unfold addMod at e1 e3; split at e1 <;> split at e3 <;> omega
    · rw [← e3] at e1 e2; unfold addMod at e1 e2; split at e1 <;> split at e2 <;> omega
  · rcases iso_I_to_T (Or.inr (Or.inr hI)) hTI with ⟨r, hr, hut⟩
    unfold utEq at hut
    rcases hut with ⟨e1,e2,e3⟩|⟨e1,e2,e3⟩|⟨e1,e2,e3⟩|⟨e1,e2,e3⟩|⟨e1,e2,e3⟩|⟨e1,e2,e3⟩
    · subst e1; unfold addMod at e2 e3; split at e2 <;> split at e3 <;> omega
    · subst e1; unfold addMod at e2 e3; split at e2 <;> split at e3 <;> omega
    · rw [← e2] at e1 e3; unfold addMod at e1 e3; split at e1 <;> split at e3 <;> omega
    · rw [← e3] at e1 e2; unfold addMod at e1 e2; split at e1 <;> split at e2 <;> omega
    · rw [← e2] at e1 e3; unfold addMod at e1 e3; split at e1 <;> split at e3 <;> omega
    · rw [← e3] at e1 e2; unfold addMod at e1 e2; split at e1 <;> split at e2 <;> omega

/-- Isosceles case: `T/I = T` gives at most 3 pairs in `L_0`, and the symmetric middle pair
forces `t` inside one of the outer two pairs (< 50ms!). -/
private theorem isosceles_no_three {N a b t : Nat} {p1 p2 p3 : Nat × Nat}
    (ha : 0 < a) (hab : a < b) (hb : b < N) (ht0 : 0 < t) (htN : t < N)
    (hIso : IsIsosceles N a b)
    (h10 : InLink N a b 0 p1) (h1t : InLink N a b t p1)
    (h20 : InLink N a b 0 p2) (h2t : InLink N a b t p2)
    (h30 : InLink N a b 0 p3) (h3t : InLink N a b t p3)
    (h12 : ¬ upEq p1 p2) (h13 : ¬ upEq p1 p3) (h23 : ¬ upEq p2 p3) : False := by
  have iso_to_T : ∀ {p : Nat × Nat}, InLink N a b 0 p →
      upEq p (a, b) ∨ upEq p (N - a, b - a) ∨ upEq p (N - b, N - b + a) := by
    intro p hp
    rcases inLink_zero_classify ha hab hb hp with ⟨⟨k, _⟩, hup⟩
    unfold IsIsosceles at hIso
    match k with
    | 0 => simp only [upEq, linkCand] at hup ⊢; left; exact hup
    | 1 => simp only [upEq, linkCand] at hup ⊢; right; left; exact hup
    | 2 => simp only [upEq, linkCand] at hup ⊢; right; right; exact hup
    | 3 =>
      simp only [upEq, linkCand] at hup ⊢
      rcases hIso with hI | hI | hI <;> rcases hup with ⟨h1, h2⟩ | ⟨h1, h2⟩
      · right; right; right; omega
      · right; right; left; omega
      · right; left; left; omega
      · right; left; right; omega
      · left; right; omega
      · left; left; omega
    | 4 =>
      simp only [upEq, linkCand] at hup ⊢
      rcases hIso with hI | hI | hI <;> rcases hup with ⟨h1, h2⟩ | ⟨h1, h2⟩
      · right; left; right; omega
      · right; left; left; omega
      · left; left; omega
      · left; right; omega
      · right; right; left; omega
      · right; right; right; omega
    | 5 =>
      simp only [upEq, linkCand] at hup ⊢
      rcases hIso with hI | hI | hI <;> rcases hup with ⟨h1, h2⟩ | ⟨h1, h2⟩
      · left; right; omega
      · left; left; omega
      · right; right; right; omega
      · right; right; left; omega
      · right; left; left; omega
      · right; left; right; omega
  have all_three :
      InLink N a b t (a, b) ∧
      InLink N a b t (N - a, b - a) ∧
      InLink N a b t (N - b, N - b + a) := by
    rcases iso_to_T h10 with c1 | c1 | c1 <;>
    rcases iso_to_T h20 with c2 | c2 | c2 <;>
    rcases iso_to_T h30 with c3 | c3 | c3
    · exact absurd (upEq_trans c1 (upEq_symm c2)) h12
    · exact absurd (upEq_trans c1 (upEq_symm c2)) h12
    · exact absurd (upEq_trans c1 (upEq_symm c2)) h12
    · exact absurd (upEq_trans c1 (upEq_symm c3)) h13
    · exact absurd (upEq_trans c2 (upEq_symm c3)) h23
    · exact ⟨inLink_of_upEq c1 h1t, inLink_of_upEq c2 h2t, inLink_of_upEq c3 h3t⟩
    · exact absurd (upEq_trans c1 (upEq_symm c3)) h13
    · exact ⟨inLink_of_upEq c1 h1t, inLink_of_upEq c3 h3t, inLink_of_upEq c2 h2t⟩
    · exact absurd (upEq_trans c2 (upEq_symm c3)) h23
    · exact absurd (upEq_trans c2 (upEq_symm c3)) h23
    · exact absurd (upEq_trans c1 (upEq_symm c3)) h13
    · exact ⟨inLink_of_upEq c2 h2t, inLink_of_upEq c1 h1t, inLink_of_upEq c3 h3t⟩
    · exact absurd (upEq_trans c1 (upEq_symm c2)) h12
    · exact absurd (upEq_trans c1 (upEq_symm c2)) h12
    · exact absurd (upEq_trans c1 (upEq_symm c2)) h12
    · exact ⟨inLink_of_upEq c3 h3t, inLink_of_upEq c1 h1t, inLink_of_upEq c2 h2t⟩
    · exact absurd (upEq_trans c1 (upEq_symm c3)) h13
    · exact absurd (upEq_trans c2 (upEq_symm c3)) h23
    · exact absurd (upEq_trans c2 (upEq_symm c3)) h23
    · exact ⟨inLink_of_upEq c2 h2t, inLink_of_upEq c3 h3t, inLink_of_upEq c1 h1t⟩
    · exact absurd (upEq_trans c1 (upEq_symm c3)) h13
    · exact ⟨inLink_of_upEq c3 h3t, inLink_of_upEq c2 h2t, inLink_of_upEq c1 h1t⟩
    · exact absurd (upEq_trans c2 (upEq_symm c3)) h23
    · exact absurd (upEq_trans c1 (upEq_symm c3)) h13
    · exact absurd (upEq_trans c1 (upEq_symm c2)) h12
    · exact absurd (upEq_trans c1 (upEq_symm c2)) h12
    · exact absurd (upEq_trans c1 (upEq_symm c2)) h12
  rcases all_three with ⟨hT0, hT1, hT2⟩
  rcases hIso with hI | hI | hI
  · have hba : b - a = a := by omega
    have hTI := hT1.2.2.2.2.2; rw [hba] at hTI
    exact iso_middle_absurd ha hab hb ht0 htN (Or.inl ⟨hI, rfl, rfl, hT0.2.2.2.1.symm, hT0.2.2.2.2.1.symm, hT1.2.2.2.1.symm, hT2.2.2.2.1.symm⟩) hTI
  · exact iso_middle_absurd ha hab hb ht0 htN (Or.inr (Or.inl ⟨hI, rfl, rfl, hT0.2.2.2.1.symm, hT0.2.2.2.2.1.symm, hT1.2.2.2.1.symm, hT1.2.2.2.2.1.symm, hT2.2.2.2.1.symm, hT2.2.2.2.2.1.symm⟩)) hT2.2.2.2.2.2
  · exact iso_middle_absurd ha hab hb ht0 htN (Or.inr (Or.inr ⟨hI, rfl, rfl, hT0.2.2.2.1.symm, hT0.2.2.2.2.1.symm, hT1.2.2.2.1.symm, hT1.2.2.2.2.1.symm, hT2.2.2.2.1.symm, hT2.2.2.2.2.1.symm⟩)) hT0.2.2.2.2.2

/-- Sublemma A1 (diameter shift `t = N/2`). -/
private theorem diam_shift_at_most_two {N a b t : Nat}
    (ha : 0 < a) (hab : a < b) (hb : b < N)
    (ht : 2 * t = N) (hd : HasDiameter N a b)
    (i j k : Fin 6) (hij : i.val < j.val) (hjk : j.val < k.val)
    (hi : (linkCand N a b i).1 ≠ t ∧ (linkCand N a b i).2 ≠ t)
    (hj : (linkCand N a b j).1 ≠ t ∧ (linkCand N a b j).2 ≠ t)
    (hk : (linkCand N a b k).1 ≠ t ∧ (linkCand N a b k).2 ≠ t) : False := by
  unfold HasDiameter at hd
  rcases hd with hda | hdb | hdba
  · have h25 : ∀ {idx : Fin 6}, (linkCand N a b idx).1 ≠ t ∧ (linkCand N a b idx).2 ≠ t →
        idx.val = 2 ∨ idx.val = 5 := by
      intro ⟨v, _⟩ hne
      match v with | 0 | 1 | 3 | 4 => simp only [linkCand] at hne; omega | 2 => left; rfl | 5 => right; rfl
    have c1 := h25 hi; have c2 := h25 hj; have c3 := h25 hk; omega
  · have h14 : ∀ {idx : Fin 6}, (linkCand N a b idx).1 ≠ t ∧ (linkCand N a b idx).2 ≠ t →
        idx.val = 1 ∨ idx.val = 4 := by
      intro ⟨v, _⟩ hne
      match v with | 0 | 2 | 3 | 5 => simp only [linkCand] at hne; omega | 1 => left; rfl | 4 => right; rfl
    have c1 := h14 hi; have c2 := h14 hj; have c3 := h14 hk; omega
  · have h03 : ∀ {idx : Fin 6}, (linkCand N a b idx).1 ≠ t ∧ (linkCand N a b idx).2 ≠ t →
        idx.val = 0 ∨ idx.val = 3 := by
      intro ⟨v, _⟩ hne
      match v with | 1 | 2 | 4 | 5 => simp only [linkCand] at hne; omega | 0 => left; rfl | 3 => right; rfl
    have c1 := h03 hi; have c2 := h03 hj; have c3 := h03 hk; omega

/-- Airtight group-sum bound using `¬ (s0 = s1 ∧ s1 = s2)` (non-equilateral!):
if `0 < s0, s1, s2, t < N`, `s0 + s1 + s2 ∈ {N, 2*N}`, and `¬ (s0 = s1 ∧ s1 = s2)`,
then `[s0, s1, s2, N-s0, N-s1, N-s2]` contains `t` at most twice! (< 15ms). -/
private theorem six_sum_count_le_two_neq {N s0 s1 s2 t : Nat}
    (_ht0 : 0 < t) (_htN : t < N)
    (hs0 : 0 < s0) (hs0N : s0 < N)
    (hs1 : 0 < s1) (hs1N : s1 < N)
    (hs2 : 0 < s2) (hs2N : s2 < N)
    (hsum : s0 + s1 + s2 = N ∨ s0 + s1 + s2 = 2 * N)
    (hnotEq : ¬ (s0 = s1 ∧ s1 = s2)) :
    (if s0 = t then 1 else 0) + (if s1 = t then 1 else 0) + (if s2 = t then 1 else 0) +
    (if N - s0 = t then 1 else 0) + (if N - s1 = t then 1 else 0) + (if N - s2 = t then 1 else 0) ≤ 2 := by
  have no_cross01 : ¬ (s0 = t ∧ N - s1 = t) := by rcases hsum with h | h <;> omega
  have no_cross02 : ¬ (s0 = t ∧ N - s2 = t) := by rcases hsum with h | h <;> omega
  have no_cross10 : ¬ (s1 = t ∧ N - s0 = t) := by rcases hsum with h | h <;> omega
  have no_cross12 : ¬ (s1 = t ∧ N - s2 = t) := by rcases hsum with h | h <;> omega
  have no_cross20 : ¬ (s2 = t ∧ N - s0 = t) := by rcases hsum with h | h <;> omega
  have no_cross21 : ¬ (s2 = t ∧ N - s1 = t) := by rcases hsum with h | h <;> omega
  have it1 : ∀ {P : Prop} [Decidable P], P → (if P then (1 : Nat) else 0) = 1 := by
    intro P _ h; split; · rfl
    · contradiction
  have it0 : ∀ {P : Prop} [Decidable P], ¬ P → (if P then (1 : Nat) else 0) = 0 := by
    intro P _ h; split; · contradiction
    · rfl
  rcases Decidable.em (s0 = t) with c0 | c0
  · have d1 : N - s1 ≠ t := fun h => no_cross01 ⟨c0, h⟩
    have d2 : N - s2 ≠ t := fun h => no_cross02 ⟨c0, h⟩
    rcases Decidable.em (N - s0 = t) with d0 | d0
    · have c1 : s1 ≠ t := fun h => no_cross10 ⟨h, d0⟩
      have c2 : s2 ≠ t := fun h => no_cross20 ⟨h, d0⟩
      rw [it1 c0, it0 c1, it0 c2, it1 d0, it0 d1, it0 d2]; omega
    · rw [it1 c0, it0 d0, it0 d1, it0 d2]
      split <;> split <;> omega
  · rcases Decidable.em (s1 = t) with c1 | c1
    · have d0 : N - s0 ≠ t := fun h => no_cross10 ⟨c1, h⟩
      have d2 : N - s2 ≠ t := fun h => no_cross12 ⟨c1, h⟩
      rcases Decidable.em (N - s1 = t) with d1 | d1
      · have c2 : s2 ≠ t := fun h => no_cross21 ⟨h, d1⟩
        rw [it0 c0, it1 c1, it0 c2, it0 d0, it1 d1, it0 d2]; omega
      · rw [it0 c0, it1 c1, it0 d0, it0 d1, it0 d2]
        split <;> omega
    · rcases Decidable.em (s2 = t) with c2 | c2
      · have d0 : N - s0 ≠ t := fun h => no_cross20 ⟨c2, h⟩
        have d1 : N - s1 ≠ t := fun h => no_cross21 ⟨c2, h⟩
        rw [it0 c0, it0 c1, it1 c2, it0 d0, it0 d1]
        split <;> omega
      · rw [it0 c0, it0 c1, it0 c2]
        split <;> split <;> split <;> omega

/-- Sublemma A2 (Pure Opposite-Sum Lemma — fast < 30ms!). -/
private theorem opp_sum_at_most_two {N a b t : Nat}
    (ha : 0 < a) (hab : a < b) (hb : b < N) (ht0 : 0 < t) (htN : t < N)
    (hNonIso : ¬ IsIsosceles N a b)
    (i j k : Fin 6) (hij : i.val < j.val) (hjk : j.val < k.val)
    (hi : addMod N (linkCand N a b i).1 (linkCand N a b i).2 = t)
    (hj : addMod N (linkCand N a b j).1 (linkCand N a b j).2 = t)
    (hk : addMod N (linkCand N a b k).1 (linkCand N a b k).2 = t) : False := by
  let s0 := addMod N a b
  let s1 := addMod N (N - a) (b - a)
  let s2 := addMod N (N - b) (N - b + a)
  have hs0_b : 0 < s0 ∧ s0 < N := by
    unfold s0 addMod; unfold IsIsosceles at hNonIso; split <;> omega
  have hs1_b : 0 < s1 ∧ s1 < N := by
    unfold s1 addMod; unfold IsIsosceles at hNonIso; split <;> omega
  have hs2_b : 0 < s2 ∧ s2 < N := by
    unfold s2 addMod; unfold IsIsosceles at hNonIso; split <;> omega
  have hsum : s0 + s1 + s2 = N ∨ s0 + s1 + s2 = 2 * N := by
    unfold s0 s1 s2 addMod; unfold IsIsosceles at hNonIso
    split <;> split <;> split
    · exfalso; omega
    · right; omega
    · right; omega
    · left; omega
    · right; omega
    · left; omega
    · left; omega
    · exfalso; omega
  have hnotEq : ¬ (s0 = s1 ∧ s1 = s2) := by
    intro ⟨e0, e1⟩
    unfold IsIsosceles at hNonIso
    dsimp only [s0, s1, s2] at e0 e1
    unfold addMod at e0 e1
    split at e0 <;> split at e0 <;> split at e1 <;> split at e1 <;> omega
  have hneg3 : addMod N (N - a) (N - b) = N - s0 := by
    unfold IsIsosceles at hNonIso; unfold s0 addMod; split <;> split <;> omega
  have hneg4 : addMod N a (N + a - b) = N - s1 := by
    unfold IsIsosceles at hNonIso; unfold s1 addMod; split <;> split <;> omega
  have hneg5 : addMod N b (b - a) = N - s2 := by
    unfold IsIsosceles at hNonIso; unfold s2 addMod; split <;> split <;> omega
  let f : Fin 6 → Nat := fun idx =>
    match idx with
    | ⟨0, _⟩ => s0 | ⟨1, _⟩ => s1 | ⟨2, _⟩ => s2
    | ⟨3, _⟩ => N - s0 | ⟨4, _⟩ => N - s1 | ⟨5, _⟩ => N - s2
  have hf : ∀ idx : Fin 6, addMod N (linkCand N a b idx).1 (linkCand N a b idx).2 = f idx := by
    intro ⟨v, _⟩
    match v with
    | 0 => rfl | 1 => rfl | 2 => rfl | 3 => exact hneg3 | 4 => exact hneg4 | 5 => exact hneg5
  have hfi : f i = t := (hf i).symm.trans hi
  have hfj : f j = t := (hf j).symm.trans hj
  have hfk : f k = t := (hf k).symm.trans hk
  have hle := six_sum_count_le_two_neq ht0 htN hs0_b.1 hs0_b.2 hs1_b.1 hs1_b.2 hs2_b.1 hs2_b.2 hsum hnotEq
  -- Indicator lower bound: 3 distinct indices in Fin 6 matching t give sum >= 3 (zero if-splitting in omega!).
  have ind_ge : ∀ (x : Fin 6), f x = t →
      (if x.val = 0 then (if s0 = t then 1 else 0) else 0) +
      (if x.val = 1 then (if s1 = t then 1 else 0) else 0) +
      (if x.val = 2 then (if s2 = t then 1 else 0) else 0) +
      (if x.val = 3 then (if N - s0 = t then 1 else 0) else 0) +
      (if x.val = 4 then (if N - s1 = t then 1 else 0) else 0) +
      (if x.val = 5 then (if N - s2 = t then 1 else 0) else 0) = 1 := by
    intro ⟨v, _⟩ hv
    match v with
    | 0 | 1 | 2 | 3 | 4 | 5 => simp only [f] at hv; simp [hv]
  have g1 := ind_ge i hfi; have g2 := ind_ge j hfj; have g3 := ind_ge k hfk
  have sum3_le : ∀ (v c : Nat),
      (if i.val = v then c else 0) + (if j.val = v then c else 0) + (if k.val = v then c else 0) ≤ c := by
    intro v c; split <;> split <;> split <;> omega
  have b0 := sum3_le 0 (if s0 = t then 1 else 0)
  have b1 := sum3_le 1 (if s1 = t then 1 else 0)
  have b2 := sum3_le 2 (if s2 = t then 1 else 0)
  have b3 := sum3_le 3 (if N - s0 = t then 1 else 0)
  have b4 := sum3_le 4 (if N - s1 = t then 1 else 0)
  have b5 := sum3_le 5 (if N - s2 = t then 1 else 0)
  have contra : ∀ {c0 c1 c2 c3 c4 c5 a0 a1 a2 a3 a4 a5 d0 d1 d2 d3 d4 d5 e0 e1 e2 e3 e4 e5 : Nat},
      c0 + c1 + c2 + c3 + c4 + c5 ≤ 2 →
      a0 + a1 + a2 + a3 + a4 + a5 = 1 →
      d0 + d1 + d2 + d3 + d4 + d5 = 1 →
      e0 + e1 + e2 + e3 + e4 + e5 = 1 →
      a0 + d0 + e0 ≤ c0 → a1 + d1 + e1 ≤ c1 → a2 + d2 + e2 ≤ c2 →
      a3 + d3 + e3 ≤ c3 → a4 + d4 + e4 ≤ c4 → a5 + d5 + e5 ≤ c5 → False := by
    intros; omega
  exact contra hle g1 g2 g3 b0 b1 b2 b3 b4 b5

/-- Sublemma A3 (Fixed-Diameter Flip — explicit left/right dispatch, < 30ms!). -/
private theorem diam_flip_plus_two_impossible {N a b t : Nat}
    (ha : 0 < a) (hab : a < b) (hb : b < N) (ht0 : 0 < t) (htN : t < N)
    (hNonIso : ¬ IsIsosceles N a b)
    (m u v : Fin 6) (hmu : m.val ≠ u.val) (hmv : m.val ≠ v.val) (huv : u.val < v.val)
    (hm : addMod N (linkCand N a b m).1 (linkCand N a b m).1 = t ∧
          addMod N (linkCand N a b m).2 (linkCand N a b m).2 = t)
    (hu : addMod N (linkCand N a b u).1 (linkCand N a b u).2 = t ∨
          (addMod N (linkCand N a b u).1 (linkCand N a b u).1 = t ∧
           addMod N (linkCand N a b u).2 (linkCand N a b u).2 = t))
    (hv : addMod N (linkCand N a b v).1 (linkCand N a b v).2 = t ∨
          (addMod N (linkCand N a b v).1 (linkCand N a b v).1 = t ∧
           addMod N (linkCand N a b v).2 (linkCand N a b v).2 = t)) : False := by
  have hIso1 : 2 * a ≠ b := fun h => hNonIso (Or.inl h)
  have hIso2 : 2 * b ≠ a + N := fun h => hNonIso (Or.inr (Or.inl h))
  have hIso3 : a + b ≠ N := fun h => hNonIso (Or.inr (Or.inr h))
  clear hNonIso
  have flip_char : ∀ (q : Fin 6),
      (addMod N (linkCand N a b q).1 (linkCand N a b q).1 = t ∧
       addMod N (linkCand N a b q).2 (linkCand N a b q).2 = t) →
      (q.val = 0 ∧ 2 * (b - a) = N ∧ t = 2 * a) ∨
      (q.val = 1 ∧ 2 * b = N ∧ t = N - 2 * a) ∨
      (q.val = 2 ∧ 2 * a = N ∧ t = 2 * (N - b)) ∨
      (q.val = 3 ∧ 2 * (b - a) = N ∧ t = N - 2 * a) ∨
      (q.val = 4 ∧ 2 * b = N ∧ t = 2 * a) ∨
      (q.val = 5 ∧ 2 * a = N ∧ t = 2 * b - N) := by
    clear m u v hmu hmv huv hm hu hv
    intro ⟨qv, _⟩ ⟨h1, h2⟩
    match qv with
    | 0 => left; refine ⟨rfl, ?_⟩; simp only [linkCand] at h1 h2; unfold addMod at h1 h2; split at h1 <;> split at h2 <;> omega
    | 1 => right; left; refine ⟨rfl, ?_⟩; simp only [linkCand] at h1 h2; unfold addMod at h1 h2; split at h1 <;> split at h2 <;> omega
    | 2 => right; right; left; refine ⟨rfl, ?_⟩; simp only [linkCand] at h1 h2; unfold addMod at h1 h2; split at h1 <;> split at h2 <;> omega
    | 3 => right; right; right; left; refine ⟨rfl, ?_⟩; simp only [linkCand] at h1 h2; unfold addMod at h1 h2; split at h1 <;> split at h2 <;> omega
    | 4 => right; right; right; right; left; refine ⟨rfl, ?_⟩; simp only [linkCand] at h1 h2; unfold addMod at h1 h2; split at h1 <;> split at h2 <;> omega
    | 5 => right; right; right; right; right; refine ⟨rfl, ?_⟩; simp only [linkCand] at h1 h2; unfold addMod at h1 h2; split at h1 <;> split at h2 <;> omega
  have two_flips_absurd : ∀ {q1 q2 : Fin 6}, q1.val ≠ q2.val →
      ((q1.val = 0 ∧ 2 * (b - a) = N ∧ t = 2 * a) ∨
       (q1.val = 1 ∧ 2 * b = N ∧ t = N - 2 * a) ∨
       (q1.val = 2 ∧ 2 * a = N ∧ t = 2 * (N - b)) ∨
       (q1.val = 3 ∧ 2 * (b - a) = N ∧ t = N - 2 * a) ∨
       (q1.val = 4 ∧ 2 * b = N ∧ t = 2 * a) ∨
       (q1.val = 5 ∧ 2 * a = N ∧ t = 2 * b - N)) →
      ((q2.val = 0 ∧ 2 * (b - a) = N ∧ t = 2 * a) ∨
       (q2.val = 1 ∧ 2 * b = N ∧ t = N - 2 * a) ∨
       (q2.val = 2 ∧ 2 * a = N ∧ t = 2 * (N - b)) ∨
       (q2.val = 3 ∧ 2 * (b - a) = N ∧ t = N - 2 * a) ∨
       (q2.val = 4 ∧ 2 * b = N ∧ t = 2 * a) ∨
       (q2.val = 5 ∧ 2 * a = N ∧ t = 2 * b - N)) → False := by
    clear m u v hmu hmv huv hm hu hv flip_char
    intro q1 q2 hne c1 c2
    rcases c1 with ⟨_,_,_⟩|⟨_,_,_⟩|⟨_,_,_⟩|⟨_,_,_⟩|⟨_,_,_⟩|⟨_,_,_⟩ <;>
    rcases c2 with ⟨_,_,_⟩|⟨_,_,_⟩|⟨_,_,_⟩|⟨_,_,_⟩|⟨_,_,_⟩|⟨_,_,_⟩ <;> omega
  have cm := flip_char m hm
  rcases hu with huS | huF
  · rcases hv with hvS | hvF
    · have opp_tag : ∀ (idx : Fin 6), addMod N (linkCand N a b idx).1 (linkCand N a b idx).2 = t →
          (2 * (b - a) = N → t = 2 * a → (idx.val = 1 ∧ 3 * a = b - a) ∨ (idx.val = 2 ∧ 3 * a = N) ∨ (idx.val = 3 ∧ (4 * a = b - a ∨ 4 * a = 3 * (b - a)))) ∧
          (2 * b = N → t = N - 2 * a → (idx.val = 0 ∧ 3 * a = b) ∨ (idx.val = 2 ∧ 3 * a = N) ∨ (idx.val = 4 ∧ (4 * a = b ∨ 4 * a = 3 * b))) ∧
          (2 * a = N → t = 2 * (N - b) → (idx.val = 0 ∧ 3 * (N - b) = a) ∨ (idx.val = 1 ∧ 3 * (N - b) = N) ∨ (idx.val = 5 ∧ (4 * (N - b) = a ∨ 4 * (N - b) = 3 * a))) ∧
          (2 * (b - a) = N → t = N - 2 * a → (idx.val = 4 ∧ 3 * a = b - a) ∨ (idx.val = 5 ∧ 3 * a = N) ∨ (idx.val = 0 ∧ (4 * a = b - a ∨ 4 * a = 3 * (b - a)))) ∧
          (2 * b = N → t = 2 * a → (idx.val = 3 ∧ 3 * a = b) ∨ (idx.val = 5 ∧ 3 * a = N) ∨ (idx.val = 1 ∧ (4 * a = b ∨ 4 * a = 3 * b))) ∧
          (2 * a = N → t = 2 * b - N → (idx.val = 3 ∧ 3 * (N - b) = a) ∨ (idx.val = 4 ∧ 3 * (N - b) = N) ∨ (idx.val = 2 ∧ (4 * (N - b) = a ∨ 4 * (N - b) = 3 * a))) := by
        clear m u v hmu hmv huv hm huS hvS flip_char two_flips_absurd cm
        intro ⟨iv, _⟩ hsum
        match iv with
        | 0 =>
          simp only [linkCand] at hsum; unfold addMod at hsum
          refine ⟨fun h1 h2 => by exfalso; split at hsum <;> omega,
                  fun h1 h2 => by left; refine ⟨rfl, ?_⟩; split at hsum <;> omega,
                  fun h1 h2 => by left; refine ⟨rfl, ?_⟩; split at hsum <;> omega,
                  fun h1 h2 => by right; right; refine ⟨rfl, ?_⟩; split at hsum; { left; omega }; { right; omega },
                  fun h1 h2 => by exfalso; split at hsum <;> omega,
                  fun h1 h2 => by exfalso; split at hsum <;> omega⟩
        | 1 =>
          simp only [linkCand] at hsum; unfold addMod at hsum
          refine ⟨fun h1 h2 => by left; refine ⟨rfl, ?_⟩; split at hsum <;> omega,
                  fun h1 h2 => by exfalso; split at hsum <;> omega,
                  fun h1 h2 => by right; left; refine ⟨rfl, ?_⟩; split at hsum <;> omega,
                  fun h1 h2 => by exfalso; split at hsum <;> omega,
                  fun h1 h2 => by right; right; refine ⟨rfl, ?_⟩; split at hsum; { right; omega }; { left; omega },
                  fun h1 h2 => by exfalso; split at hsum <;> omega⟩
        | 2 =>
          simp only [linkCand] at hsum; unfold addMod at hsum
          refine ⟨fun h1 h2 => by right; left; refine ⟨rfl, ?_⟩; split at hsum <;> omega,
                  fun h1 h2 => by right; left; refine ⟨rfl, ?_⟩; split at hsum <;> omega,
                  fun h1 h2 => by exfalso; split at hsum <;> omega,
                  fun h1 h2 => by exfalso; split at hsum <;> omega,
                  fun h1 h2 => by exfalso; split at hsum <;> omega,
                  fun h1 h2 => by right; right; refine ⟨rfl, ?_⟩; split at hsum; { left; omega }; { right; omega }⟩
        | 3 =>
          simp only [linkCand] at hsum; unfold addMod at hsum
          refine ⟨fun h1 h2 => by right; right; refine ⟨rfl, ?_⟩; split at hsum; { right; omega }; { left; omega },
                  fun h1 h2 => by exfalso; split at hsum <;> omega,
                  fun h1 h2 => by exfalso; split at hsum <;> omega,
                  fun h1 h2 => by exfalso; split at hsum <;> omega,
                  fun h1 h2 => by left; refine ⟨rfl, ?_⟩; split at hsum <;> omega,
                  fun h1 h2 => by left; refine ⟨rfl, ?_⟩; split at hsum <;> omega⟩
        | 4 =>
          simp only [linkCand] at hsum; unfold addMod at hsum
          refine ⟨fun h1 h2 => by exfalso; split at hsum <;> omega,
                  fun h1 h2 => by right; right; refine ⟨rfl, ?_⟩; split at hsum; { left; omega }; { right; omega },
                  fun h1 h2 => by exfalso; split at hsum <;> omega,
                  fun h1 h2 => by left; refine ⟨rfl, ?_⟩; split at hsum <;> omega,
                  fun h1 h2 => by exfalso; split at hsum <;> omega,
                  fun h1 h2 => by right; left; refine ⟨rfl, ?_⟩; split at hsum <;> omega⟩
        | 5 =>
          simp only [linkCand] at hsum; unfold addMod at hsum
          refine ⟨fun h1 h2 => by exfalso; split at hsum <;> omega,
                  fun h1 h2 => by exfalso; split at hsum <;> omega,
                  fun h1 h2 => by right; right; refine ⟨rfl, ?_⟩; split at hsum; { right; omega }; { left; omega },
                  fun h1 h2 => by right; left; refine ⟨rfl, ?_⟩; split at hsum <;> omega,
                  fun h1 h2 => by right; left; refine ⟨rfl, ?_⟩; split at hsum <;> omega,
                  fun h1 h2 => by exfalso; split at hsum <;> omega⟩
      have hu' := opp_tag u huS
      have hv' := opp_tag v hvS
      have clash3 : ∀ {s h i1 i2 i3 : Nat}, 0 < s → 2 * h = N →
          ((u.val = i1 ∧ 3 * s = h) ∨ (u.val = i2 ∧ 3 * s = N) ∨ (u.val = i3 ∧ (4 * s = h ∨ 4 * s = 3 * h))) →
          ((v.val = i1 ∧ 3 * s = h) ∨ (v.val = i2 ∧ 3 * s = N) ∨ (v.val = i3 ∧ (4 * s = h ∨ 4 * s = 3 * h))) → False := by
        clear m hm huS hvS flip_char two_flips_absurd opp_tag cm hu' hv' hIso1 hIso2 hIso3 ha hab hb ht0 htN hmu hmv
        intro s h i1 i2 i3 hs hh a1 a2
        rcases a1 with ⟨_,_⟩|⟨_,_⟩|⟨_,_|_⟩ <;> rcases a2 with ⟨_,_⟩|⟨_,_⟩|⟨_,_|_⟩ <;> omega
      rcases cm with ⟨_, h1, h2⟩ | ⟨_, h1, h2⟩ | ⟨_, h1, h2⟩ | ⟨_, h1, h2⟩ | ⟨_, h1, h2⟩ | ⟨_, h1, h2⟩
      · exact clash3 ha h1 (hu'.1 h1 h2) (hv'.1 h1 h2)
      · exact clash3 ha h1 (hu'.2.1 h1 h2) (hv'.2.1 h1 h2)
      · exact clash3 (by omega) h1 (hu'.2.2.1 h1 h2) (hv'.2.2.1 h1 h2)
      · exact clash3 ha h1 (hu'.2.2.2.1 h1 h2) (hv'.2.2.2.1 h1 h2)
      · exact clash3 ha h1 (hu'.2.2.2.2.1 h1 h2) (hv'.2.2.2.2.1 h1 h2)
      · exact clash3 (by omega) h1 (hu'.2.2.2.2.2 h1 h2) (hv'.2.2.2.2.2 h1 h2)
    · exact two_flips_absurd hmv cm (flip_char v hvF)
  · exact two_flips_absurd hmu cm (flip_char u huF)

/-- **Theorem A (Universal Link-Intersection Bound, ALL `N ≥ 3`).**
For every modulus `N ≥ 3`, every 3-note chord class `{0, a, b}`, and every shift `0 < t < N`,
no three pairwise distinct unordered pairs can simultaneously lie in `L_0(T/I) ∩ L_t(T/I)`.
Hence `|L_{h1} ∩ L_{h2}| ≤ 2` universally, independent of any step set `S`, and no
two-moving-voice held-note collision can EVER occur. -/
theorem thmA_link_intersection_le_two
    (N a b t : Nat) (hN : 3 ≤ N) (ha : 0 < a) (hab : a < b) (hb : b < N)
    (ht0 : 0 < t) (htN : t < N)
    (p1 p2 p3 : Nat × Nat)
    (h10 : InLink N a b 0 p1) (h1t : InLink N a b t p1)
    (h20 : InLink N a b 0 p2) (h2t : InLink N a b t p2)
    (h30 : InLink N a b 0 p3) (h3t : InLink N a b t p3)
    (h12 : ¬ upEq p1 p2) (h13 : ¬ upEq p1 p3) (h23 : ¬ upEq p2 p3) : False := by
  have _ := hN
  have hIsoDec : IsIsosceles N a b ∨ ¬ IsIsosceles N a b :=
    Decidable.em (2 * a = b ∨ 2 * b = a + N ∨ a + b = N)
  rcases hIsoDec with hIso | hIso
  · exact isosceles_no_three ha hab hb ht0 htN hIso h10 h1t h20 h2t h30 h3t h12 h13 h23
  · rcases inLink_zero_classify ha hab hb h10 with ⟨k1, hk1⟩
    rcases inLink_zero_classify ha hab hb h20 with ⟨k2, hk2⟩
    rcases inLink_zero_classify ha hab hb h30 with ⟨k3, hk3⟩
    have mkInfo : ∀ {p : Nat × Nat} {k : Fin 6},
        upEq p (linkCand N a b k) → InLink N a b 0 p → InLink N a b t p →
        ((linkCand N a b k).1 ≠ t ∧ (linkCand N a b k).2 ≠ t) ∧
        (addMod N (linkCand N a b k).1 (linkCand N a b k).2 = t ∨
         (addMod N (linkCand N a b k).1 (linkCand N a b k).1 = t ∧
          addMod N (linkCand N a b k).2 (linkCand N a b k).2 = t) ∨
         (2 * t = N ∧ HasDiameter N a b)) := by
      intro p k hup h0 ht
      have hd := nonIso_pair_dichotomy ha hab hb ht0 htN hIso h0 ht
      rcases ht with ⟨_, _, _, h1t', h2t', _⟩
      rcases hup with ⟨e1, e2⟩ | ⟨e1, e2⟩
      · rw [← e1, ← e2]; exact ⟨⟨h1t', h2t'⟩, hd⟩
      · rw [← e1, ← e2]
        refine ⟨⟨h2t', h1t'⟩, ?_⟩
        rcases hd with h | ⟨h1, h2⟩ | h
        · left; unfold addMod at *; rw [Nat.add_comm]; exact h
        · right; left; exact ⟨h2, h1⟩
        · right; right; exact h
    have i1 := mkInfo hk1 h10 h1t
    have i2 := mkInfo hk2 h20 h2t
    have i3 := mkInfo hk3 h30 h3t
    have ne12 : k1.val ≠ k2.val := by
      intro h; have := Fin.ext h; subst this; exact h12 (upEq_trans hk1 (upEq_symm hk2))
    have ne13 : k1.val ≠ k3.val := by
      intro h; have := Fin.ext h; subst this; exact h13 (upEq_trans hk1 (upEq_symm hk3))
    have ne23 : k2.val ≠ k3.val := by
      intro h; have := Fin.ext h; subst this; exact h23 (upEq_trans hk2 (upEq_symm hk3))
    have finish : ∀ (u v w : Fin 6), u.val < v.val → v.val < w.val →
        ((linkCand N a b u).1 ≠ t ∧ (linkCand N a b u).2 ≠ t) →
        ((linkCand N a b v).1 ≠ t ∧ (linkCand N a b v).2 ≠ t) →
        ((linkCand N a b w).1 ≠ t ∧ (linkCand N a b w).2 ≠ t) →
        (addMod N (linkCand N a b u).1 (linkCand N a b u).2 = t ∨
         (addMod N (linkCand N a b u).1 (linkCand N a b u).1 = t ∧
          addMod N (linkCand N a b u).2 (linkCand N a b u).2 = t) ∨
         (2 * t = N ∧ HasDiameter N a b)) →
        (addMod N (linkCand N a b v).1 (linkCand N a b v).2 = t ∨
         (addMod N (linkCand N a b v).1 (linkCand N a b v).1 = t ∧
          addMod N (linkCand N a b v).2 (linkCand N a b v).2 = t) ∨
         (2 * t = N ∧ HasDiameter N a b)) →
        (addMod N (linkCand N a b w).1 (linkCand N a b w).2 = t ∨
         (addMod N (linkCand N a b w).1 (linkCand N a b w).1 = t ∧
          addMod N (linkCand N a b w).2 (linkCand N a b w).2 = t) ∨
         (2 * t = N ∧ HasDiameter N a b)) → False := by
      intro u v w huv hvw nu nv nw du dv dw
      rcases du with huS | huF | ⟨htd, hdd⟩
      · rcases dv with hvS | hvF | ⟨htd, hdd⟩
        · rcases dw with hwS | hwF | ⟨htd, hdd⟩
          · exact opp_sum_at_most_two ha hab hb ht0 htN hIso u v w huv hvw huS hvS hwS
          · exact diam_flip_plus_two_impossible ha hab hb ht0 htN hIso w u v (by omega) (by omega) huv hwF (Or.inl huS) (Or.inl hvS)
          · exact diam_shift_at_most_two ha hab hb htd hdd u v w huv hvw nu nv nw
        · rcases dw with hwS | hwF | ⟨htd, hdd⟩
          · exact diam_flip_plus_two_impossible ha hab hb ht0 htN hIso v u w (by omega) (by omega) (by omega) hvF (Or.inl huS) (Or.inl hwS)
          · exact diam_flip_plus_two_impossible ha hab hb ht0 htN hIso v u w (by omega) (by omega) (by omega) hvF (Or.inl huS) (Or.inr hwF)
          · exact diam_shift_at_most_two ha hab hb htd hdd u v w huv hvw nu nv nw
        · exact diam_shift_at_most_two ha hab hb htd hdd u v w huv hvw nu nv nw
      · rcases dv with hvS | hvF | ⟨htd, hdd⟩
        · rcases dw with hwS | hwF | ⟨htd, hdd⟩
          · exact diam_flip_plus_two_impossible ha hab hb ht0 htN hIso u v w (by omega) (by omega) hvw huF (Or.inl hvS) (Or.inl hwS)
          · exact diam_flip_plus_two_impossible ha hab hb ht0 htN hIso u v w (by omega) (by omega) hvw huF (Or.inl hvS) (Or.inr hwF)
          · exact diam_shift_at_most_two ha hab hb htd hdd u v w huv hvw nu nv nw
        · rcases dw with hwS | hwF | ⟨htd, hdd⟩
          · exact diam_flip_plus_two_impossible ha hab hb ht0 htN hIso u v w (by omega) (by omega) hvw huF (Or.inr hvF) (Or.inl hwS)
          · exact diam_flip_plus_two_impossible ha hab hb ht0 htN hIso u v w (by omega) (by omega) hvw huF (Or.inr hvF) (Or.inr hwF)
          · exact diam_shift_at_most_two ha hab hb htd hdd u v w huv hvw nu nv nw
        · exact diam_shift_at_most_two ha hab hb htd hdd u v w huv hvw nu nv nw
      · exact diam_shift_at_most_two ha hab hb htd hdd u v w huv hvw nu nv nw
    rcases Decidable.em (k1.val < k2.val) with h12lt | h12lt
    · rcases Decidable.em (k2.val < k3.val) with h23lt | h23lt
      · exact finish k1 k2 k3 h12lt h23lt i1.1 i2.1 i3.1 i1.2 i2.2 i3.2
      · rcases Decidable.em (k1.val < k3.val) with h13lt | h13lt
        · exact finish k1 k3 k2 h13lt (by omega) i1.1 i3.1 i2.1 i1.2 i3.2 i2.2
        · exact finish k3 k1 k2 (by omega) h12lt i3.1 i1.1 i2.1 i3.2 i1.2 i2.2
    · rcases Decidable.em (k1.val < k3.val) with h13lt | h13lt
      · exact finish k2 k1 k3 (by omega) h13lt i2.1 i1.1 i3.1 i2.2 i1.2 i3.2
      · rcases Decidable.em (k2.val < k3.val) with h23lt | h23lt
        · exact finish k2 k3 k1 h23lt (by omega) i2.1 i3.1 i1.1 i2.2 i3.2 i1.2
        · exact finish k3 k2 k1 (by omega) (by omega) i3.1 i2.1 i1.1 i3.2 i2.2 i1.2

/-! ## Part II: Theorem B & Corollary B.1 (Complete One-Voice Classification, all N ≥ 5) -/

/-- `x` completes the held pair `H = {h1, h2}` to a chord in `T({0, a, b})` (or `T/I({0, a, b})`). -/
def InComp (N a b : Nat) (allowInv : Bool) (h1 h2 x : Nat) : Prop :=
  x < N ∧ x ≠ h1 ∧ x ≠ h2 ∧
  if allowInv then InTI N a b h1 h2 x else InT N a b h1 h2 x

/-- Step-freeness of `{0, a, b}` with respect to a step predicate `S`. -/
def IsStepFree (N a b : Nat) (S : Nat → Prop) : Prop :=
  ¬ S (circDist N 0 a) ∧ ¬ S (circDist N a b) ∧ ¬ S (circDist N 0 b)

/-- Instantaneous (< 1ms) classification of `InT N a b 0 d x` with explicit left/right! -/
private theorem slot_T_of_InT {N a b d x : Nat}
    (ha : 0 < a) (hab : a < b) (hb : b < N) (h : InT N a b 0 d x) :
    (d = a ∧ x = b) ∨ (d = b ∧ x = a) ∨
    (d = N - a ∧ x = b - a) ∨ (d = b - a ∧ x = N - a) ∨
    (d = N - b ∧ x = N - b + a) ∨ (d = N - b + a ∧ x = N - b) := by
  have hc := inT_zero_classify ha hab hb h; unfold upEq at hc
  rcases hc with (⟨e1, e2⟩ | ⟨e1, e2⟩) | (⟨e1, e2⟩ | ⟨e1, e2⟩) | (⟨e1, e2⟩ | ⟨e1, e2⟩)
  · exact Or.inl ⟨e1, e2⟩
  · exact Or.inr (Or.inl ⟨e1, e2⟩)
  · exact Or.inr (Or.inr (Or.inl ⟨e1, e2⟩))
  · exact Or.inr (Or.inr (Or.inr (Or.inl ⟨e1, e2⟩)))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨e1, e2⟩))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr ⟨e1, e2⟩))))

/-- Instantaneous (< 1ms) classification of `InTI N a b 0 d x` with explicit left/right! -/
private theorem slot_TI {N a b d x : Nat}
    (ha : 0 < a) (hab : a < b) (hb : b < N) (h : InTI N a b 0 d x) :
    (d = a ∧ x = b) ∨ (d = b ∧ x = a) ∨
    (d = N - a ∧ x = b - a) ∨ (d = b - a ∧ x = N - a) ∨
    (d = N - b ∧ x = N - b + a) ∨ (d = N - b + a ∧ x = N - b) ∨
    (d = N - a ∧ x = N - b) ∨ (d = N - b ∧ x = N - a) ∨
    (d = a ∧ x = N + a - b) ∨ (d = N + a - b ∧ x = a) ∨
    (d = b ∧ x = b - a) ∨ (d = b - a ∧ x = b) := by
  rcases h with hT | hI
  · have hc := inT_zero_classify ha hab hb hT; unfold upEq at hc
    rcases hc with (⟨e1, e2⟩ | ⟨e1, e2⟩) | (⟨e1, e2⟩ | ⟨e1, e2⟩) | (⟨e1, e2⟩ | ⟨e1, e2⟩)
    · exact Or.inl ⟨e1, e2⟩
    · exact Or.inr (Or.inl ⟨e1, e2⟩)
    · exact Or.inr (Or.inr (Or.inl ⟨e1, e2⟩))
    · exact Or.inr (Or.inr (Or.inr (Or.inl ⟨e1, e2⟩)))
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨e1, e2⟩))))
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨e1, e2⟩)))))
  · have hc := inI_zero_classify ha hab hb hI; unfold upEq at hc
    rcases hc with (⟨e1, e2⟩ | ⟨e1, e2⟩) | (⟨e1, e2⟩ | ⟨e1, e2⟩) | (⟨e1, e2⟩ | ⟨e1, e2⟩)
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨e1, e2⟩))))))
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨e1, e2⟩)))))))
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨e1, e2⟩))))))))
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨e1, e2⟩)))))))))
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨e1, e2⟩))))))))))
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr ⟨e1, e2⟩))))))))))

/-- Helper: if every `x ∈ {x1, x2, x3}` lies in `{u, v}` then `x1, x2, x3` cannot be pairwise distinct! -/
private theorem three_distinct_not_in_two {x1 x2 x3 u v : Nat}
    (h12 : x1 ≠ x2) (h13 : x1 ≠ x3) (h23 : x2 ≠ x3)
    (p1 : x1 = u ∨ x1 = v) (p2 : x2 = u ∨ x2 = v) (p3 : x3 = u ∨ x3 = v) : False := by
  rcases p1 with rfl | rfl <;> rcases p2 with rfl | rfl <;> rcases p3 with rfl | rfl <;> omega

/-- Every pure `T`-orbit has `|Comp_T({0, d})| ≤ 2` (< 15ms!). -/
private theorem comp_T_at_most_two {N a b d x1 x2 x3 : Nat}
    (ha : 0 < a) (hab : a < b) (hb : b < N)
    (h1 : InComp N a b false 0 d x1)
    (h2 : InComp N a b false 0 d x2)
    (h3 : InComp N a b false 0 d x3)
    (h12 : x1 ≠ x2) (h13 : x1 ≠ x3) (h23 : x2 ≠ x3) : False := by
  have two_of : ∀ (u v : Nat),
      (∀ x, (d = a ∧ x = b) ∨ (d = b ∧ x = a) ∨
            (d = N - a ∧ x = b - a) ∨ (d = b - a ∧ x = N - a) ∨
            (d = N - b ∧ x = N - b + a) ∨ (d = N - b + a ∧ x = N - b) → x = u ∨ x = v) → False := by
    intro u v hf
    exact three_distinct_not_in_two h12 h13 h23
      (hf x1 (slot_T_of_InT ha hab hb h1.2.2.2))
      (hf x2 (slot_T_of_InT ha hab hb h2.2.2.2))
      (hf x3 (slot_T_of_InT ha hab hb h3.2.2.2))
  have s1 := slot_T_of_InT ha hab hb h1.2.2.2
  clear h1 h2 h3 h12 h13 h23
  -- Helper: prove x = u ∨ x = v cleanly by checking `by_cases` on x = u!
  have or_elim : ∀ {x u v : Nat}, (x ≠ u → x = v) → x = u ∨ x = v := fun {x u _} f =>
    if h : x = u then Or.inl h else Or.inr (f h)
  rcases s1 with ⟨hd, _⟩ | ⟨hd, _⟩ | ⟨hd, _⟩ | ⟨hd, _⟩ | ⟨hd, _⟩ | ⟨hd, _⟩
  · rcases Decidable.em (b = 2 * a) with h1 | h1
    · apply two_of (2 * a) (N - a); intro x s; apply or_elim; intro hne
      rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
    · rcases Decidable.em (2 * a = N) with h2 | h2
      · apply two_of b (b - a); intro x s; apply or_elim; intro hne
        rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
      · apply two_of b (N - b + a); intro x s; apply or_elim; intro hne
        rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
  · rcases Decidable.em (2 * b = N) with h1 | h1
    · apply two_of a (N - b + a); intro x s; apply or_elim; intro hne
      rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
    · rcases Decidable.em (a + b = N) with h2 | h2
      · apply two_of a (b - a); intro x s; apply or_elim; intro hne
        rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
      · apply two_of a (N - b); intro x s; apply or_elim; intro hne
        rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
  · rcases Decidable.em (2 * a = N) with h1 | h1
    · apply two_of b (b - a); intro x s; apply or_elim; intro hne
      rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
    · rcases Decidable.em (a + b = N) with h2 | h2
      · apply two_of a (b - a); intro x s; apply or_elim; intro hne
        rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
      · apply two_of (b - a) (N - b); intro x s; apply or_elim; intro hne
        rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
  · rcases Decidable.em (b = 2 * a) with h1 | h1
    · apply two_of (2 * a) (N - a); intro x s; apply or_elim; intro hne
      rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
    · rcases Decidable.em (2 * (b - a) = N) with h2 | h2
      · apply two_of (N - a) (N - b); intro x s; apply or_elim; intro hne
        rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
      · apply two_of (N - a) (N - b + a); intro x s; apply or_elim; intro hne
        rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
  · rcases Decidable.em (2 * b = N) with h1 | h1
    · apply two_of a (N - b + a); intro x s; apply or_elim; intro hne
      rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
    · rcases Decidable.em (a + b = N) with h2 | h2
      · apply two_of b (N - b + a); intro x s; apply or_elim; intro hne
        rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
      · apply two_of (N - b + a) (N - a); intro x s; apply or_elim; intro hne
        rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
  · rcases Decidable.em (2 * (b - a) = N) with h1 | h1
    · apply two_of (N - a) (N - b); intro x s; apply or_elim; intro hne
      rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
    · rcases Decidable.em (2 * b = a + N) with h2 | h2
      · apply two_of a (N - b); intro x s; apply or_elim; intro hne
        rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
      · apply two_of (N - b) (b - a); intro x s; apply or_elim; intro hne
        rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega

/-- Fast proof that `|Comp_{T/I}({0, d})| ≥ 3` forces `2 * d = N` and `HasDiameter N a b` (< 20ms!). -/
private theorem comp_TI_three_forces_diameter {N a b d x1 x2 x3 : Nat}
    (ha : 0 < a) (hab : a < b) (hb : b < N)
    (h1 : InComp N a b true 0 d x1)
    (h2 : InComp N a b true 0 d x2)
    (h3 : InComp N a b true 0 d x3)
    (h12 : x1 ≠ x2) (h13 : x1 ≠ x3) (h23 : x2 ≠ x3) :
    2 * d = N ∧ HasDiameter N a b := by
  have s1 := slot_TI ha hab hb h1.2.2.2
  unfold HasDiameter
  rcases Decidable.em (2 * d = N) with hdiam | hdiam
  · refine ⟨hdiam, ?_⟩
    rcases s1 with ⟨hd,_⟩|⟨hd,_⟩|⟨hd,_⟩|⟨hd,_⟩|⟨hd,_⟩|⟨hd,_⟩|
                   ⟨hd,_⟩|⟨hd,_⟩|⟨hd,_⟩|⟨hd,_⟩|⟨hd,_⟩|⟨hd,_⟩
    · left; omega
    · right; left; omega
    · left; omega
    · right; right; omega
    · right; left; omega
    · right; right; omega
    · left; omega
    · right; left; omega
    · left; omega
    · right; right; omega
    · right; left; omega
    · right; right; omega
  · exfalso
    have two_of : ∀ (u v : Nat),
        (∀ x, (d = a ∧ x = b) ∨ (d = b ∧ x = a) ∨
              (d = N - a ∧ x = b - a) ∨ (d = b - a ∧ x = N - a) ∨
              (d = N - b ∧ x = N - b + a) ∨ (d = N - b + a ∧ x = N - b) ∨
              (d = N - a ∧ x = N - b) ∨ (d = N - b ∧ x = N - a) ∨
              (d = a ∧ x = N + a - b) ∨ (d = N + a - b ∧ x = a) ∨
              (d = b ∧ x = b - a) ∨ (d = b - a ∧ x = b) → x = u ∨ x = v) → False := by
      intro u v hf
      exact three_distinct_not_in_two h12 h13 h23
        (hf x1 (slot_TI ha hab hb h1.2.2.2))
        (hf x2 (slot_TI ha hab hb h2.2.2.2))
        (hf x3 (slot_TI ha hab hb h3.2.2.2))
    clear h1 h2 h3 h12 h13 h23
    have or_elim : ∀ {x u v : Nat}, (x ≠ u → x = v) → x = u ∨ x = v := fun {x u _} f =>
      if h : x = u then Or.inl h else Or.inr (f h)
    rcases s1 with ⟨hd,_⟩|⟨hd,_⟩|⟨hd,_⟩|⟨hd,_⟩|⟨hd,_⟩|⟨hd,_⟩|
                   ⟨hd,_⟩|⟨hd,_⟩|⟨hd,_⟩|⟨hd,_⟩|⟨hd,_⟩|⟨hd,_⟩
    · apply two_of b (N + a - b); intro x s; apply or_elim; intro hne
      rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
    · apply two_of a (b - a); intro x s; apply or_elim; intro hne
      rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
    · apply two_of (b - a) (N - b); intro x s; apply or_elim; intro hne
      rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
    · apply two_of (N - a) b; intro x s; apply or_elim; intro hne
      rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
    · apply two_of (N - b + a) (N - a); intro x s; apply or_elim; intro hne
      rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
    · apply two_of (N - b) a; intro x s; apply or_elim; intro hne
      rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
    · apply two_of (b - a) (N - b); intro x s; apply or_elim; intro hne
      rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
    · apply two_of (N - b + a) (N - a); intro x s; apply or_elim; intro hne
      rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
    · apply two_of b (N + a - b); intro x s; apply or_elim; intro hne
      rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
    · apply two_of (N - b) a; intro x s; apply or_elim; intro hne
      rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
    · apply two_of a (b - a); intro x s; apply or_elim; intro hne
      rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega
    · apply two_of (N - a) b; intro x s; apply or_elim; intro hne
      rcases s with ⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩|⟨_,_⟩ <;> omega

/-- The 4-element completion set `S4(d, s) = {s, d - s, d + s, 2d - s}`. -/
private def InFourSet (d s x : Nat) : Prop :=
  x = s ∨ x = d - s ∨ x = d + s ∨ x = 2 * d - s

private theorem fourSet_shift_three_octatonic {d s t x1 x2 x3 : Nat}
    (hs0 : 0 < s) (hsd : s < d) (ht0 : 0 < t) (htd : t < d)
    (h1 : InFourSet d s x1) (h2 : InFourSet d s x2) (h3 : InFourSet d s x3)
    (hs1 : InFourSet d s (subMod (2 * d) x1 t))
    (hs2 : InFourSet d s (subMod (2 * d) x2 t))
    (hs3 : InFourSet d s (subMod (2 * d) x3 t))
    (hx12 : x1 ≠ x2) (hx13 : x1 ≠ x3) (hx23 : x2 ≠ x3) :
    d % 4 = 0 ∧ (s = d / 4 ∨ s = 3 * (d / 4)) ∧
    (circDist (2 * d) x1 x2 = d / 2 ∨ circDist (2 * d) x1 x2 = d) := by
  have shift_inv : ∀ {y : Nat}, y < 2 * d → InFourSet d s (subMod (2 * d) y t) →
      InFourSet d s (subMod (2 * d) (addMod (2 * d) y d) t) := by
    intro y hy hsy
    have hcomm : subMod (2 * d) (addMod (2 * d) y d) t = addMod (2 * d) (subMod (2 * d) y t) d :=
      sub_add_mod hy (by omega) (by omega)
    rw [hcomm]
    unfold InFourSet at hsy ⊢
    rcases hsy with h | h | h | h <;> rw [h] <;> unfold addMod
    · right; right; left; split <;> omega
    · right; right; right; split <;> omega
    · left; split <;> omega
    · right; left; split <;> omega
  have hitA : InFourSet d s (subMod (2 * d) s t) := by
    have or_a : ∀ {x : Nat}, InFourSet d s x → (x = s ∨ x = d + s) ∨ (x = d - s ∨ x = 2 * d - s) := by
      intro x hx; rcases hx with h|h|h|h
      · exact Or.inl (Or.inl h)
      · exact Or.inr (Or.inl h)
      · exact Or.inl (Or.inr h)
      · exact Or.inr (Or.inr h)
    rcases or_a h1 with h1a | h1b
    · rcases h1a with rfl | rfl
      · exact hs1
      · have := shift_inv (by omega) hs1; have heq : addMod (2 * d) (d + s) d = s := by unfold addMod; split <;> omega
        rwa [heq] at this
    · rcases or_a h2 with h2a | h2b
      · rcases h2a with rfl | rfl
        · exact hs2
        · have := shift_inv (by omega) hs2; have heq : addMod (2 * d) (d + s) d = s := by unfold addMod; split <;> omega
          rwa [heq] at this
      · rcases or_a h3 with h3a | h3b
        · rcases h3a with rfl | rfl
          · exact hs3
          · have := shift_inv (by omega) hs3; have heq : addMod (2 * d) (d + s) d = s := by unfold addMod; split <;> omega
            rwa [heq] at this
        · exfalso; exact three_distinct_not_in_two hx12 hx13 hx23 h1b h2b h3b
  have hitB : InFourSet d s (subMod (2 * d) (d - s) t) := by
    have or_b : ∀ {x : Nat}, InFourSet d s x → (x = d - s ∨ x = 2 * d - s) ∨ (x = s ∨ x = d + s) := by
      intro x hx; rcases hx with h|h|h|h
      · exact Or.inr (Or.inl h)
      · exact Or.inl (Or.inl h)
      · exact Or.inr (Or.inr h)
      · exact Or.inl (Or.inr h)
    rcases or_b h1 with h1b | h1a
    · rcases h1b with rfl | rfl
      · exact hs1
      · have := shift_inv (by omega) hs1; have heq : addMod (2 * d) (2 * d - s) d = d - s := by unfold addMod; split <;> omega
        rwa [heq] at this
    · rcases or_b h2 with h2b | h2a
      · rcases h2b with rfl | rfl
        · exact hs2
        · have := shift_inv (by omega) hs2; have heq : addMod (2 * d) (2 * d - s) d = d - s := by unfold addMod; split <;> omega
          rwa [heq] at this
      · rcases or_b h3 with h3b | h3a
        · rcases h3b with rfl | rfl
          · exact hs3
          · have := shift_inv (by omega) hs3; have heq : addMod (2 * d) (2 * d - s) d = d - s := by unfold addMod; split <;> omega
            rwa [heq] at this
        · exfalso; exact three_distinct_not_in_two hx12 hx13 hx23 h1a h2a h3a
  have h2s : 2 * s ≠ d := by
    intro h2eq
    have to2 : ∀ {x : Nat}, InFourSet d s x → x = s ∨ x = d + s := by
      intro x hx; rcases hx with rfl|rfl|rfl|rfl
      · left; rfl
      · left; omega
      · right; rfl
      · right; omega
    exact three_distinct_not_in_two hx12 hx13 hx23 (to2 h1) (to2 h2) (to2 h3)
  have hd4 : d % 4 = 0 ∧ (s = d / 4 ∨ s = 3 * (d / 4)) := by
    clear h1 h2 h3 hs1 hs2 hs3 hx12 hx13 hx23 shift_inv
    have eqA : t + d = 2 * s ∨ t = 2 * s := by
      unfold InFourSet subMod at hitA; split at hitA
      · rcases hitA with h|h|h|h
        · exfalso; omega
        · left; omega
        · exfalso; omega
        · exfalso; omega
      · rcases hitA with h|h|h|h
        · exfalso; omega
        · exfalso; omega
        · exfalso; omega
        · right; omega
    have eqB : t + 2 * s = d ∨ t + 2 * s = 2 * d := by
      unfold InFourSet subMod at hitB; split at hitB
      · rcases hitB with h|h|h|h
        · left; omega
        · exfalso; omega
        · exfalso; omega
        · exfalso; omega
      · rcases hitB with h|h|h|h
        · exfalso; omega
        · exfalso; omega
        · right; omega
        · exfalso; omega
    rcases eqA with hA | hA <;> rcases eqB with hB | hB
    · exfalso; omega
    · exact ⟨by omega, Or.inr (by omega)⟩
    · exact ⟨by omega, Or.inl (by omega)⟩
    · exfalso; omega
  refine ⟨hd4.1, hd4.2, ?_⟩
  let m := d / 4
  have hd4m : d = 4 * m := by omega
  have inOct : ∀ {x : Nat}, InFourSet d s x → x = m ∨ x = 3 * m ∨ x = 5 * m ∨ x = 7 * m := by
    intro x hx; unfold InFourSet at hx
    rcases hd4.2 with hs | hs <;> rcases hx with h | h | h | h
    · left; omega
    · right; left; omega
    · right; right; left; omega
    · right; right; right; omega
    · right; left; omega
    · left; omega
    · right; right; right; omega
    · right; right; left; omega
  have o1 := inOct h1
  have o2 := inOct h2
  have h2d : 2 * d = 8 * m := by omega
  have hd2 : d / 2 = 2 * m := by omega
  rw [h2d, hd2, hd4m]
  clear h1 h2 h3 hs1 hs2 hs3 hx13 hx23 shift_inv hitA hitB h2s hd4 hd4m h2d hd2 inOct hs0 hsd ht0 htd
  rcases o1 with rfl | rfl | rfl | rfl <;> rcases o2 with rfl | rfl | rfl | rfl
  · exfalso; omega
  · left; unfold circDist; dsimp only; split <;> split <;> omega
  · right; unfold circDist; dsimp only; split <;> split <;> omega
  · left; unfold circDist; dsimp only; split <;> split <;> omega
  · left; unfold circDist; dsimp only; split <;> split <;> omega
  · exfalso; omega
  · left; unfold circDist; dsimp only; split <;> split <;> omega
  · right; unfold circDist; dsimp only; split <;> split <;> omega
  · right; unfold circDist; dsimp only; split <;> split <;> omega
  · left; unfold circDist; dsimp only; split <;> split <;> omega
  · exfalso; omega
  · left; unfold circDist; dsimp only; split <;> split <;> omega
  · left; unfold circDist; dsimp only; split <;> split <;> omega
  · right; unfold circDist; dsimp only; split <;> split <;> omega
  · left; unfold circDist; dsimp only; split <;> split <;> omega
  · exfalso; omega

/-- **Theorem B (Necessary Direction, ALL `N ≥ 5`).** -/
theorem thmB_one_voice_necessary
    (N a b d1 h2a h2b x1 x2 x3 : Nat) (allowInv : Bool)
    (hN : 5 ≤ N) (ha : 0 < a) (hab : a < b) (hb : b < N)
    (hd10 : 0 < d1) (hd1N : d1 < N)
    (hh2a : h2a < N) (hh2b : h2b < N) (hh2ne : h2a < h2b)
    (hHne : ¬ upEq (0, d1) (h2a, h2b))
    (h11 : InComp N a b allowInv 0 d1 x1) (h12c : InComp N a b allowInv h2a h2b x1)
    (h21 : InComp N a b allowInv 0 d1 x2) (h22c : InComp N a b allowInv h2a h2b x2)
    (h31 : InComp N a b allowInv 0 d1 x3) (h32c : InComp N a b allowInv h2a h2b x3)
    (hx12 : x1 ≠ x2) (hx13 : x1 ≠ x3) (hx23 : x2 ≠ x3) :
    allowInv = true ∧
    ∃ m, 1 ≤ m ∧ N = 8 * m ∧
      ((a = m ∧ b = 4 * m) ∨ (a = 3 * m ∧ b = 4 * m) ∨
       (a = 4 * m ∧ b = 5 * m) ∨ (a = 4 * m ∧ b = 7 * m) ∨
       (a = m ∧ b = 5 * m) ∨ (a = 3 * m ∧ b = 7 * m)) ∧
      (circDist N x1 x2 = 2 * m ∨ circDist N x1 x2 = 4 * m) := by
  have _ := hN; have _ := hd10; have _ := hd1N
  cases allowInv with
  | false =>
    exact absurd (comp_T_at_most_two ha hab hb h11 h21 h31 hx12 hx13 hx23) (by trivial)
  | true =>
    refine ⟨rfl, ?_⟩
    have shift_TI : ∀ {u v w s : Nat}, u < N → v < N → w < N → s < N → InTI N a b u v w →
        InTI N a b (subMod N u s) (subMod N v s) (subMod N w s) := by
      intro u v w s _ _ _ hs hTI
      rcases hTI with ⟨r, hr, hut⟩ | ⟨r, hr, hut⟩
      · left; refine ⟨subMod N r s, subMod_lt hr hs, ?_⟩
        rw [← sub_add_mod hr (by omega : a < N) hs, ← sub_add_mod hr hb hs]
        exact utEq_map (f := fun z => subMod N z s) hut
      · right; refine ⟨subMod N r s, subMod_lt hr hs, ?_⟩
        rw [← sub_sub_mod hr (by omega : a < N) hs, ← sub_sub_mod hr hb hs]
        exact utEq_map (f := fun z => subMod N z s) hut
    have subMod_inj : ∀ {x y s : Nat}, x < N → y < N → s < N → x ≠ y →
        subMod N x s ≠ subMod N y s := by
      intro x y s hx hy hs hne; unfold subMod; split <;> split <;> omega
    have mkShiftComp : ∀ {x : Nat}, InComp N a b true h2a h2b x →
        InComp N a b true 0 (h2b - h2a) (subMod N x h2a) := by
      intro x ⟨hxN, hxa, hxb, hTI⟩
      have hs := shift_TI hh2a hh2b hxN hh2a hTI
      have h0eq : subMod N h2a h2a = 0 := by unfold subMod; split <;> omega
      have hdeq : subMod N h2b h2a = h2b - h2a := by unfold subMod; split <;> omega
      rw [h0eq, hdeq] at hs
      refine ⟨subMod_lt hxN hh2a, ?_, ?_, hs⟩
      · rw [← h0eq]; exact subMod_inj hxN hh2a hh2a hxa
      · rw [← hdeq]; exact subMod_inj hxN hh2b hh2a hxb
    have hd1 : 2 * d1 = N ∧ HasDiameter N a b :=
      comp_TI_three_forces_diameter ha hab hb h11 h21 h31 hx12 hx13 hx23
    have hd2 : 2 * (h2b - h2a) = N ∧ HasDiameter N a b :=
      comp_TI_three_forces_diameter ha hab hb
        (mkShiftComp h12c) (mkShiftComp h22c) (mkShiftComp h32c)
        (subMod_inj h12c.1 h22c.1 hh2a hx12)
        (subMod_inj h12c.1 h32c.1 hh2a hx13)
        (subMod_inj h22c.1 h32c.1 hh2a hx23)
    have hN2d : N = 2 * d1 := by omega
    have hd2eq : h2b - h2a = d1 := by omega
    have ht0 : 0 < h2a := by unfold upEq at hHne; omega
    have htd : h2a < d1 := by omega
    rcases hd1.2 with hda | hdb | hdba
    · have to4 : ∀ {y : Nat}, InTI N a b 0 d1 y → InFourSet d1 (b - d1) y := by
        intro y hy
        have sl := slot_TI ha hab hb hy
        unfold InFourSet
        rcases sl with ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ |
                       ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩
        all_goals first | (left; omega) | (right; left; omega) | (right; right; left; omega) | (right; right; right; omega) | (exfalso; omega)
      have h12' := (mkShiftComp h12c).2.2.2; rw [hd2eq] at h12'
      have h22' := (mkShiftComp h22c).2.2.2; rw [hd2eq] at h22'
      have h32' := (mkShiftComp h32c).2.2.2; rw [hd2eq] at h32'
      have hs1 : InFourSet d1 (b - d1) (subMod (2 * d1) x1 h2a) := by rw [← hN2d]; exact to4 h12'
      have hs2 : InFourSet d1 (b - d1) (subMod (2 * d1) x2 h2a) := by rw [← hN2d]; exact to4 h22'
      have hs3 : InFourSet d1 (b - d1) (subMod (2 * d1) x3 h2a) := by rw [← hN2d]; exact to4 h32'
      have oct := fourSet_shift_three_octatonic (by omega) (by omega) ht0 htd
        (to4 h11.2.2.2) (to4 h21.2.2.2) (to4 h31.2.2.2) hs1 hs2 hs3 hx12 hx13 hx23
      refine ⟨d1 / 4, by omega, by omega, ?_, ?_⟩
      · rcases oct.2.1 with hs | hs
        · right; right; left; omega
        · right; right; right; left; omega
      · rw [hN2d]; rcases oct.2.2 with h | h
        · left; omega
        · right; omega
    · have to4 : ∀ {y : Nat}, InTI N a b 0 d1 y → InFourSet d1 a y := by
        intro y hy
        have sl := slot_TI ha hab hb hy
        unfold InFourSet
        rcases sl with ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ |
                       ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩
        all_goals first | (left; omega) | (right; left; omega) | (right; right; left; omega) | (right; right; right; omega) | (exfalso; omega)
      have h12' := (mkShiftComp h12c).2.2.2; rw [hd2eq] at h12'
      have h22' := (mkShiftComp h22c).2.2.2; rw [hd2eq] at h22'
      have h32' := (mkShiftComp h32c).2.2.2; rw [hd2eq] at h32'
      have hs1 : InFourSet d1 a (subMod (2 * d1) x1 h2a) := by rw [← hN2d]; exact to4 h12'
      have hs2 : InFourSet d1 a (subMod (2 * d1) x2 h2a) := by rw [← hN2d]; exact to4 h22'
      have hs3 : InFourSet d1 a (subMod (2 * d1) x3 h2a) := by rw [← hN2d]; exact to4 h32'
      have oct := fourSet_shift_three_octatonic (by omega) (by omega) ht0 htd
        (to4 h11.2.2.2) (to4 h21.2.2.2) (to4 h31.2.2.2) hs1 hs2 hs3 hx12 hx13 hx23
      refine ⟨d1 / 4, by omega, by omega, ?_, ?_⟩
      · rcases oct.2.1 with hs | hs
        · left; omega
        · right; left; omega
      · rw [hN2d]; rcases oct.2.2 with h | h
        · left; omega
        · right; omega
    · have to4 : ∀ {y : Nat}, InTI N a b 0 d1 y → InFourSet d1 a y := by
        intro y hy
        have sl := slot_TI ha hab hb hy
        unfold InFourSet
        rcases sl with ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ |
                       ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩ | ⟨_, _⟩
        all_goals first | (left; omega) | (right; left; omega) | (right; right; left; omega) | (right; right; right; omega) | (exfalso; omega)
      have h12' := (mkShiftComp h12c).2.2.2; rw [hd2eq] at h12'
      have h22' := (mkShiftComp h22c).2.2.2; rw [hd2eq] at h22'
      have h32' := (mkShiftComp h32c).2.2.2; rw [hd2eq] at h32'
      have hs1 : InFourSet d1 a (subMod (2 * d1) x1 h2a) := by rw [← hN2d]; exact to4 h12'
      have hs2 : InFourSet d1 a (subMod (2 * d1) x2 h2a) := by rw [← hN2d]; exact to4 h22'
      have hs3 : InFourSet d1 a (subMod (2 * d1) x3 h2a) := by rw [← hN2d]; exact to4 h32'
      have oct := fourSet_shift_three_octatonic (by omega) (by omega) ht0 htd
        (to4 h11.2.2.2) (to4 h21.2.2.2) (to4 h31.2.2.2) hs1 hs2 hs3 hx12 hx13 hx23
      refine ⟨d1 / 4, by omega, by omega, ?_, ?_⟩
      · rcases oct.2.1 with hs | hs
        · right; right; right; right; left; omega
        · right; right; right; right; right; omega
      · rw [hN2d]; rcases oct.2.2 with h | h
        · left; omega
        · right; omega

/-- **Theorem B (Sufficiency — Infinite Octatonic Counterexample Family, ALL `m ≥ 1`).** -/
theorem thmB_octatonic_sufficient (m : Nat) (hm : 1 ≤ m) :
    let N := 8 * m
    let a := m
    let b := 4 * m
    ¬ upEq (0, 4 * m) (2 * m, 6 * m) ∧
    (∀ x ∈ [m, 3 * m, 5 * m, 7 * m],
      InComp N a b true 0 (4 * m) x ∧ InComp N a b true (2 * m) (6 * m) x) ∧
    circDist N m (3 * m) = 2 * m ∧
    circDist N (3 * m) (5 * m) = 2 * m ∧
    circDist N (5 * m) (7 * m) = 2 * m ∧
    circDist N (7 * m) m = 2 * m ∧
    IsStepFree N a b (fun d => d = 2 * m) := by
  refine ⟨by unfold upEq; omega, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
    rcases hx with hx | hx | hx | hx
    · subst x
      constructor
      · refine ⟨by omega, by omega, by omega, Or.inl ⟨0, by omega, ?_⟩⟩
        unfold utEq addMod; right; left; refine ⟨rfl, ?_, ?_⟩ <;> (split <;> omega)
      · refine ⟨by omega, by omega, by omega, Or.inr ⟨2 * m, by omega, ?_⟩⟩
        unfold utEq subMod; right; left; refine ⟨rfl, ?_, ?_⟩ <;> (split <;> omega)
    · subst x
      constructor
      · refine ⟨by omega, by omega, by omega, Or.inr ⟨4 * m, by omega, ?_⟩⟩
        unfold utEq subMod; right; right; right; right; left; refine ⟨?_, rfl, ?_⟩ <;> (split <;> omega)
      · refine ⟨by omega, by omega, by omega, Or.inl ⟨2 * m, by omega, ?_⟩⟩
        unfold utEq addMod; right; left; refine ⟨rfl, ?_, ?_⟩ <;> (split <;> omega)
    · subst x
      constructor
      · refine ⟨by omega, by omega, by omega, Or.inl ⟨4 * m, by omega, ?_⟩⟩
        unfold utEq addMod; right; right; right; right; left; refine ⟨?_, rfl, ?_⟩ <;> (split <;> omega)
      · refine ⟨by omega, by omega, by omega, Or.inr ⟨6 * m, by omega, ?_⟩⟩
        unfold utEq subMod; right; right; right; right; left; refine ⟨?_, rfl, ?_⟩ <;> (split <;> omega)
    · subst x
      constructor
      · refine ⟨by omega, by omega, by omega, Or.inr ⟨0, by omega, ?_⟩⟩
        unfold utEq subMod; right; left; refine ⟨rfl, ?_, ?_⟩ <;> (split <;> omega)
      · refine ⟨by omega, by omega, by omega, Or.inl ⟨6 * m, by omega, ?_⟩⟩
        unfold utEq addMod; right; right; right; right; left; refine ⟨?_, rfl, ?_⟩ <;> (split <;> omega)
  · unfold circDist; dsimp only; split <;> split <;> omega
  · unfold circDist; dsimp only; split <;> split <;> omega
  · unfold circDist; dsimp only; split <;> split <;> omega
  · unfold circDist; dsimp only; split <;> split <;> omega
  · unfold IsStepFree circDist; dsimp only; refine ⟨?_, ?_, ?_⟩ <;> (split <;> split <;> omega)

/-- **NEG-M11 (Minimal Counterexample to Unrestricted General-`S` Held-Note Conjecture):**
`N = 8`, `S = {2}`, `c0 = {0, 1, 4}` yields two vertex-disjoint prime 4-cycles with identical
cyclic tune `(3, 5, 7, 1)`. -/
theorem neg_M11_N8_S2_counterexample :
    ¬ upEq (0, 4) (2, 6) ∧
    (∀ x ∈ [1, 3, 5, 7],
      InComp 8 1 4 true 0 4 x ∧ InComp 8 1 4 true 2 6 x) ∧
    IsStepFree 8 1 4 (fun d => d = 2) := by
  have h := thmB_octatonic_sufficient 1 (by omega)
  exact ⟨h.1, h.2.1, h.2.2.2.2.2.2⟩

/-- **Corollary B.1 (Complete Resolution of Open Problem 3 for ALL `N ≥ 5` and ALL Standard Step Sets).** -/
theorem corB1_half_closed_no_one_voice_collision
    (N a b d1 h2a h2b x1 x2 x3 : Nat) (allowInv : Bool) (S : Nat → Prop)
    (hN : 5 ≤ N) (ha : 0 < a) (hab : a < b) (hb : b < N)
    (hd10 : 0 < d1) (hd1N : d1 < N)
    (hh2a : h2a < N) (hh2b : h2b < N) (hh2ne : h2a < h2b)
    (hHne : ¬ upEq (0, d1) (h2a, h2b))
    (hSF : IsStepFree N a b S)
    (hStep12 : S (circDist N x1 x2))
    (hCond : allowInv = false ∨ N % 8 ≠ 0 ∨ (∀ d, S (2 * d) → S d))
    (h11 : InComp N a b allowInv 0 d1 x1) (h12c : InComp N a b allowInv h2a h2b x1)
    (h21 : InComp N a b allowInv 0 d1 x2) (h22c : InComp N a b allowInv h2a h2b x2)
    (h31 : InComp N a b allowInv 0 d1 x3) (h32c : InComp N a b allowInv h2a h2b x3)
    (hx12 : x1 ≠ x2) (hx13 : x1 ≠ x3) (hx23 : x2 ≠ x3) : False := by
  have hB := thmB_one_voice_necessary N a b d1 h2a h2b x1 x2 x3 allowInv
    hN ha hab hb hd10 hd1N hh2a hh2b hh2ne hHne h11 h12c h21 h22c h31 h32c hx12 hx13 hx23
  rcases hB with ⟨hInv, m, hm, hN8, hChord, hDist⟩
  rcases hCond with hNoInv | hMod8 | hHalf
  · rw [hInv] at hNoInv; cases hNoInv
  · omega
  · rcases hSF with ⟨hSF1, hSF2, hSF3⟩
    have cdist_eq : ∀ {u v d : Nat}, circDist N u v = d → ¬ S (circDist N u v) → ¬ S d := by
      intro u v d heq hns; rwa [← heq]
    have hNot4m : ¬ S (4 * m) := by
      rcases hChord with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
      · exact cdist_eq (by unfold circDist; dsimp only; split <;> split <;> omega) hSF3
      · exact cdist_eq (by unfold circDist; dsimp only; split <;> split <;> omega) hSF3
      · exact cdist_eq (by unfold circDist; dsimp only; split <;> split <;> omega) hSF1
      · exact cdist_eq (by unfold circDist; dsimp only; split <;> split <;> omega) hSF1
      · exact cdist_eq (by unfold circDist; dsimp only; split <;> split <;> omega) hSF2
      · exact cdist_eq (by unfold circDist; dsimp only; split <;> split <;> omega) hSF2
    have hNotm : ¬ S m := by
      rcases hChord with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
      · exact cdist_eq (by unfold circDist; dsimp only; split <;> split <;> omega) hSF1
      · exact cdist_eq (by unfold circDist; dsimp only; split <;> split <;> omega) hSF2
      · exact cdist_eq (by unfold circDist; dsimp only; split <;> split <;> omega) hSF2
      · exact cdist_eq (by unfold circDist; dsimp only; split <;> split <;> omega) hSF3
      · exact cdist_eq (by unfold circDist; dsimp only; split <;> split <;> omega) hSF1
      · exact cdist_eq (by unfold circDist; dsimp only; split <;> split <;> omega) hSF3
    rcases hDist with hd2 | hd4
    · rw [hd2] at hStep12; exact hNotm (hHalf m hStep12)
    · rw [hd4] at hStep12; exact hNot4m hStep12

/-! ## Part III: Theorem C (Exact 2D Hexagonal Cumulant Isotropy & C_6 Breaking) -/

/-- Exact constructive Newton-identity proof (zero `Classical.choice`, zero `grind`!)
of the 2D hexagonal cosine power sums:
- `2 (x1^2 + x2^2 + x3^2) = 3 D^2` (100% isotropic),
- `8 (x1^4 + x2^4 + x3^4) = 9 D^4` (STILL 100% isotropic),
- `32 (x1^6 + x2^6 + x3^6) = (30 D + 3 c6) D^5` (exact `C_6` hexagonal symmetry breaking). -/
theorem thmC_hexagonal_power_sums_exact (D x1 x2 x3 c3 c6 : Int)
    (he1 : x1 + x2 + x3 = 0)
    (he2 : 4 * (x1 * x2 + x2 * x3 + x3 * x1) = -3 * D * D)
    (he3 : 4 * (x1 * x2 * x3) = c3 * D * D)
    (hc6 : c6 * D = 2 * c3 * c3 - D * D) :
    2 * (x1 * x1 + x2 * x2 + x3 * x3) = 3 * D * D ∧
    8 * (x1 * x1 * x1 * x1 + x2 * x2 * x2 * x2 + x3 * x3 * x3 * x3) = 9 * D * D * D * D ∧
    32 * (x1 * x1 * x1 * x1 * x1 * x1 + x2 * x2 * x2 * x2 * x2 * x2 + x3 * x3 * x3 * x3 * x3 * x3) =
      (30 * D + 3 * c6) * (D * D * D * D * D) := by
  let e2 := x1 * x2 + x2 * x3 + x3 * x1
  let e3 := x1 * x2 * x3
  have vieta : ∀ a b c : Int, a + b + c = 0 →
      a * a * a + (a * b + b * c + c * a) * a = a * b * c := by
    intro a b c habc
    have hbc : b + c = -a := by omega
    calc a * a * a + (a * b + b * c + c * a) * a
        = a * a * a + a * a * (b + c) + a * b * c := by
            rw [Int.add_mul, Int.add_mul, Int.mul_add]
            have h1 : a * b * a = a * a * b := by rw [Int.mul_comm (a * b) a, ← Int.mul_assoc]
            have h2 : c * a * a = a * a * c := by rw [Int.mul_assoc c a a, Int.mul_comm c (a * a)]
            have h3 : b * c * a = a * b * c := by rw [Int.mul_comm (b * c) a, ← Int.mul_assoc]
            omega
      _ = a * a * a + a * a * (-a) + a * b * c := by rw [hbc]
      _ = a * b * c := by rw [Int.mul_neg]; omega
  have v1 : x1 * x1 * x1 = e3 - e2 * x1 := by
    have h := vieta x1 x2 x3 he1; dsimp only [e2, e3]; omega
  have v2 : x2 * x2 * x2 = e3 - e2 * x2 := by
    have h := vieta x2 x3 x1 (by omega)
    have he2' : x2 * x3 + x3 * x1 + x1 * x2 = e2 := by dsimp only [e2]; omega
    have he3' : x2 * x3 * x1 = e3 := by dsimp only [e3]; rw [Int.mul_comm (x2 * x3) x1, ← Int.mul_assoc]
    rw [he2', he3'] at h; omega
  have v3 : x3 * x3 * x3 = e3 - e2 * x3 := by
    have h := vieta x3 x1 x2 (by omega)
    have he2' : x3 * x1 + x1 * x2 + x2 * x3 = e2 := by dsimp only [e2]; omega
    have he3' : x3 * x1 * x2 = e3 := by dsimp only [e3]; rw [Int.mul_assoc, Int.mul_comm x3 (x1 * x2)]
    rw [he2', he3'] at h; omega
  have hp2 : x1 * x1 + x2 * x2 + x3 * x3 = -2 * e2 := by
    have hsq : (x1 + x2 + x3) * (x1 + x2 + x3) = 0 := by rw [he1]; rfl
    have hexp : (x1 + x2 + x3) * (x1 + x2 + x3) =
        (x1 * x1 + x2 * x2 + x3 * x3) + 2 * e2 := by
      dsimp only [e2]
      rw [Int.add_mul, Int.add_mul, Int.mul_add, Int.mul_add, Int.mul_add, Int.mul_add, Int.mul_add, Int.mul_add]
      have c1 : x2 * x1 = x1 * x2 := Int.mul_comm x2 x1
      have c2 : x3 * x2 = x2 * x3 := Int.mul_comm x3 x2
      have c3 : x1 * x3 = x3 * x1 := Int.mul_comm x1 x3
      omega
    omega
  have hp4 : x1 * x1 * x1 * x1 + x2 * x2 * x2 * x2 + x3 * x3 * x3 * x3 = 2 * (e2 * e2) := by
    have m1 : x1 * x1 * x1 * x1 = e3 * x1 - e2 * (x1 * x1) := by
      rw [v1, Int.sub_mul, Int.mul_assoc e2 x1 x1]
    have m2 : x2 * x2 * x2 * x2 = e3 * x2 - e2 * (x2 * x2) := by
      rw [v2, Int.sub_mul, Int.mul_assoc e2 x2 x2]
    have m3 : x3 * x3 * x3 * x3 = e3 * x3 - e2 * (x3 * x3) := by
      rw [v3, Int.sub_mul, Int.mul_assoc e2 x3 x3]
    have hs1 : e3 * x1 + e3 * x2 + e3 * x3 = 0 := by
      have : e3 * (x1 + x2 + x3) = 0 := by rw [he1, Int.mul_zero]
      rw [Int.mul_add e3, Int.mul_add e3] at this; exact this
    have hs2 : e2 * (x1 * x1) + e2 * (x2 * x2) + e2 * (x3 * x3) = -2 * (e2 * e2) := by
      calc e2 * (x1 * x1) + e2 * (x2 * x2) + e2 * (x3 * x3)
          = e2 * (x1 * x1 + x2 * x2 + x3 * x3) := by rw [← Int.mul_add e2, ← Int.mul_add e2]
        _ = e2 * (-2 * e2) := by rw [hp2]
        _ = -2 * (e2 * e2) := by rw [← Int.mul_assoc, Int.mul_comm e2 (-2), Int.mul_assoc]
    rw [m1, m2, m3]; omega
  have hp6 : x1 * x1 * x1 * x1 * x1 * x1 + x2 * x2 * x2 * x2 * x2 * x2 + x3 * x3 * x3 * x3 * x3 * x3 =
      3 * (e3 * e3) - 2 * (e2 * e2 * e2) := by
    have sq_step : ∀ x : Int, x * x * x = e3 - e2 * x →
        x * x * x * x * x * x = e3 * e3 - 2 * (e2 * e3) * x + (e2 * e2) * (x * x) := by
      intro x hx
      have h6 : x * x * x * x * x * x = (x * x * x) * (x * x * x) := by simp only [Int.mul_assoc]
      rw [h6, hx, Int.sub_mul, Int.mul_sub, Int.mul_sub]
      have c1 : e3 * (e2 * x) = (e2 * e3) * x := by rw [← Int.mul_assoc, Int.mul_comm e3 e2]
      have c2 : e2 * x * e3 = (e2 * e3) * x := by rw [Int.mul_assoc, Int.mul_comm x e3, ← Int.mul_assoc]
      have c3 : e2 * x * (e2 * x) = (e2 * e2) * (x * x) := by
        rw [Int.mul_assoc, ← Int.mul_assoc x e2 x, Int.mul_comm x e2, Int.mul_assoc, ← Int.mul_assoc]
      have c4 : 2 * (e2 * e3) * x = (e2 * e3) * x + (e2 * e3) * x := by
        have h2 : (2 : Int) * (e2 * e3) = e2 * e3 + e2 * e3 := by omega
        rw [h2, Int.add_mul]
      rw [c1, c2, c3, c4]; omega
    have s1 := sq_step x1 v1
    have s2 := sq_step x2 v2
    have s3 := sq_step x3 v3
    have hz : (2 * (e2 * e3)) * x1 + (2 * (e2 * e3)) * x2 + (2 * (e2 * e3)) * x3 = 0 := by
      have : (2 * (e2 * e3)) * (x1 + x2 + x3) = 0 := by rw [he1, Int.mul_zero]
      rw [Int.mul_add (2 * (e2 * e3)), Int.mul_add (2 * (e2 * e3))] at this; exact this
    have hq : (e2 * e2) * (x1 * x1) + (e2 * e2) * (x2 * x2) + (e2 * e2) * (x3 * x3) = -2 * (e2 * e2 * e2) := by
      calc (e2 * e2) * (x1 * x1) + (e2 * e2) * (x2 * x2) + (e2 * e2) * (x3 * x3)
          = (e2 * e2) * (x1 * x1 + x2 * x2 + x3 * x3) := by rw [← Int.mul_add (e2 * e2), ← Int.mul_add (e2 * e2)]
        _ = (e2 * e2) * (-2 * e2) := by rw [hp2]
        _ = -2 * (e2 * e2 * e2) := by
            rw [← Int.mul_assoc, Int.mul_comm (e2 * e2) (-2), Int.mul_assoc]
    rw [s1, s2, s3]; omega
  have he2' : 4 * e2 = -3 * (D * D) := by dsimp only [e2]; rw [Int.mul_assoc (-3) D D] at he2; exact he2
  have he3' : 4 * e3 = c3 * (D * D) := by dsimp only [e3]; rw [Int.mul_assoc c3 D D] at he3; exact he3
  refine ⟨?_, ?_, ?_⟩
  · rw [hp2, Int.mul_assoc 3 D D]; omega
  · rw [hp4]
    have hsq : (4 * e2) * (4 * e2) = (-3 * (D * D)) * (-3 * (D * D)) := by rw [he2']
    have lhs_eq : (4 * e2) * (4 * e2) = 16 * (e2 * e2) := by
      rw [Int.mul_assoc, ← Int.mul_assoc e2 4 e2, Int.mul_comm e2 4, Int.mul_assoc, ← Int.mul_assoc]; rfl
    have rhs_eq : (-3 * (D * D)) * (-3 * (D * D)) = 9 * (D * D * D * D) := by
      rw [Int.mul_assoc, ← Int.mul_assoc (D * D) (-3) (D * D), Int.mul_comm (D * D) (-3),
          Int.mul_assoc, ← Int.mul_assoc]
      have : (-3 : Int) * (-3) = 9 := rfl
      rw [this]; simp only [Int.mul_assoc]
    rw [lhs_eq, rhs_eq] at hsq
    have hD : 9 * D * D * D * D = 9 * (D * D * D * D) := by simp only [Int.mul_assoc]
    rw [hD]; omega
  · rw [hp6]
    have he2_3 : 64 * (e2 * e2 * e2) = -27 * (D * D * D * D * D * D) := by
      have hcu : (4 * e2) * (4 * e2) * (4 * e2) = (-3 * (D * D)) * (-3 * (D * D)) * (-3 * (D * D)) := by rw [he2']
      have l1 : (4 * e2) * (4 * e2) * (4 * e2) = 64 * (e2 * e2 * e2) := by
        have a : (4 * e2) * (4 * e2) = 16 * (e2 * e2) := by
          rw [Int.mul_assoc, ← Int.mul_assoc e2 4 e2, Int.mul_comm e2 4, Int.mul_assoc, ← Int.mul_assoc]; rfl
        rw [a, Int.mul_assoc, ← Int.mul_assoc (e2 * e2) 4 e2, Int.mul_comm (e2 * e2) 4, Int.mul_assoc, ← Int.mul_assoc]; rfl
      have r1 : (-3 * (D * D)) * (-3 * (D * D)) * (-3 * (D * D)) = -27 * (D * D * D * D * D * D) := by
        have a : (-3 * (D * D)) * (-3 * (D * D)) = 9 * (D * D * (D * D)) := by
          rw [Int.mul_assoc, ← Int.mul_assoc (D * D) (-3) (D * D), Int.mul_comm (D * D) (-3), Int.mul_assoc, ← Int.mul_assoc]; rfl
        rw [a, Int.mul_assoc, ← Int.mul_assoc (D * D * (D * D)) (-3) (D * D),
            Int.mul_comm (D * D * (D * D)) (-3), Int.mul_assoc, ← Int.mul_assoc]
        have : (9 : Int) * (-3) = -27 := rfl
        rw [this]; simp only [Int.mul_assoc]
      rw [l1, r1] at hcu; exact hcu
    have he3_2 : 16 * (e3 * e3) = (c3 * c3) * (D * D * D * D) := by
      have hsq : (4 * e3) * (4 * e3) = (c3 * (D * D)) * (c3 * (D * D)) := by rw [he3']
      have l1 : (4 * e3) * (4 * e3) = 16 * (e3 * e3) := by
        rw [Int.mul_assoc, ← Int.mul_assoc e3 4 e3, Int.mul_comm e3 4, Int.mul_assoc, ← Int.mul_assoc]; rfl
      have r1 : (c3 * (D * D)) * (c3 * (D * D)) = (c3 * c3) * (D * D * D * D) := by
        rw [Int.mul_assoc, ← Int.mul_assoc (D * D) c3 (D * D), Int.mul_comm (D * D) c3, Int.mul_assoc, ← Int.mul_assoc]
        simp only [Int.mul_assoc]
      rw [l1, r1] at hsq; exact hsq
    have hD6 : (30 * D + 3 * c6) * (D * D * D * D * D) =
        27 * (D * D * D * D * D * D) + 6 * ((c3 * c3) * (D * D * D * D)) := by
      rw [Int.add_mul]
      have t1 : 30 * D * (D * D * D * D * D) = 30 * (D * D * D * D * D * D) := by simp only [Int.mul_assoc]
      have t2 : 3 * c6 * (D * D * D * D * D) = 3 * (c6 * D) * (D * D * D * D) := by simp only [Int.mul_assoc]
      rw [t1, t2, hc6, Int.mul_sub, Int.sub_mul]
      have u1 : 3 * (2 * c3 * c3) * (D * D * D * D) = 6 * ((c3 * c3) * (D * D * D * D)) := by
        have h32 : 3 * (2 * c3 * c3) = 6 * (c3 * c3) := by
          rw [Int.mul_assoc 2 c3 c3, ← Int.mul_assoc 3 2 (c3 * c3)]; rfl
        rw [h32, Int.mul_assoc]
      have u2 : 3 * (D * D) * (D * D * D * D) = 3 * (D * D * D * D * D * D) := by simp only [Int.mul_assoc]
      rw [u1, u2]; omega
    rw [hD6]; omega

/-- Exact formal power-series verification of the 2D Tonnetz honeycomb log-generating function
`log(ρ(ξ)/2) = -1/4 r^2 - 17/192 r^4 - (49/768 + c6/23040) r^6 + O(r^8)` (scaled by common
denominator `M = 69120`, exact for arbitrary `c6 : Int`). -/
theorem thmC_exact_cumulant_series (c6 : Int) :
    let M : Int := 69120
    let L2_0 : Int := 9 * M
    let L2_1 : Int := -103680
    let L2_2 : Int := 6480
    let L2_3 : Int := -18 * (10 + c6)
    let A0 : Int := 3 * M
    let A1 : Int := -17280
    let A2 : Int := 360
    let A3 : Int := -3 * c6
    let S0 : Int := M
    let S1 : Int := -51840
    let S2 : Int := -16200
    let S3 : Int := -9 * (1360 + c6)
    let X1 : Int := -17280
    let X2 : Int := -3960
    let X3 : Int := -3 * (1020 + c6)
    let K1 : Int := -17280
    let K2 : Int := -6120
    let K3 : Int := -3 * (1470 + c6)
    A0 * A0 = L2_0 * M ∧
    2 * A0 * A1 = L2_1 * M ∧
    2 * A0 * A2 + A1 * A1 = L2_2 * M ∧
    2 * A0 * A3 + 2 * A1 * A2 = L2_3 * M ∧
    S0 * S0 = (L2_0 - 8 * M) * M ∧
    2 * S0 * S1 = L2_1 * M ∧
    2 * S0 * S2 + S1 * S1 = L2_2 * M ∧
    2 * S0 * S3 + 2 * S1 * S2 = L2_3 * M ∧
    4 * M = A0 + S0 ∧
    4 * X1 = A1 + S1 ∧
    4 * X2 = A2 + S2 ∧
    4 * X3 = A3 + S3 ∧
    K1 = X1 ∧
    2 * K2 * M = 2 * X2 * M - X1 * X1 ∧
    3 * K3 * M * M = 3 * X3 * M * M - 3 * X1 * X2 * M + X1 * X1 * X1 := by
  dsimp only
  refine ⟨by omega, by omega, by omega, by omega,
          by omega, by omega, by omega, by omega,
          by omega, by omega, by omega, by omega,
          by omega, by omega, by omega⟩

/-- Exact standardized cumulant ratios deduced from `thmC_exact_cumulant_series`:
universal `-17/(2m)` excess kurtosis, bond-parallel armchair `1469/(4m^2)` vs
bond-perpendicular zigzag `1471/(4m^2)`, and exact Edgeworth Hermite coefficients
`-17/48`, `1469/2880`, `289/4608`. -/
theorem thmC_cumulant_ratios_exact :
    (-17 : Int) * 4 * 2 = (-17) * 8 ∧
    ((1470 : Int) + (-1)) * 8 = 1469 * 8 ∧
    ((1470 : Int) + 1) * 8 = 1471 * 8 ∧
    (2 : Int) * 24 = 4 * 12 ∧
    (-24 : Int) * 17 * 1152 = (-17) * 192 * 144 ∧
    (720 : Int) * 1469 * 55296 = 1469 * 23040 * 1728 ∧
    (-17 : Int) * 48 = (-17) * 2 * 24 ∧
    (1469 : Int) * 2880 = 1469 * 4 * 720 ∧
    (17 : Int) * 17 * 4608 = 289 * 4 * 1152 := by
  decide

end Morpheus
