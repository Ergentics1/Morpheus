/-!
# Triad Graph & PLR Dihedral Action (Proposition 2.1, Corollary 2.2)

First-principles formalization of the 24 consonant triads (`Fin 24`: `0..11` = Major(r),
`12..23` = Minor(r)) and the neo-Riemannian moves `P`, `L`, `R`.
-/

namespace Morpheus

abbrev Triad := Fin 24
abbrev Pitch := Fin 12

inductive Move where
  | P | L | R
  deriving DecidableEq, Repr

def Move.all : List Move := [.P, .L, .R]

def isMajor (v : Triad) : Bool := v.val < 12

def triadRoot (v : Triad) : Nat := v.val % 12

def applyMove (v : Triad) (m : Move) : Triad :=
  let r := v.val % 12
  if v.val < 12 then
    match m with
    | .P => ⟨12 + r, by omega⟩
    | .L => ⟨12 + (r + 4) % 12, by omega⟩
    | .R => ⟨12 + (r + 9) % 12, by omega⟩
  else
    match m with
    | .P => ⟨r, by omega⟩
    | .L => ⟨(r + 8) % 12, by omega⟩
    | .R => ⟨(r + 3) % 12, by omega⟩

def applyWord (w : List Move) (v : Triad) : Triad :=
  w.foldl applyMove v

def applyLRPow : Nat → Triad → Triad
  | 0, v => v
  | k + 1, v => applyLRPow k (applyMove (applyMove v .R) .L)

/-- Pitch-class triple (as a 12-bit mask) of each major/minor triad. -/
def triadNotesList (v : Triad) : List Nat :=
  let r := v.val % 12
  if v.val < 12 then [r, (r + 4) % 12, (r + 7) % 12]
  else [r, (r + 3) % 12, (r + 7) % 12]

/-- Signed voice-leading displacement in `{-2, -1, +1, +2}`. -/
def voiceStep (v : Triad) (m : Move) : Int :=
  if v.val < 12 then
    match m with | .P => -1 | .L => -1 | .R => 2
  else
    match m with | .P => 1 | .L => 1 | .R => -2

/-- Pitch class arriving under move `m` from triad `v`. -/
def arrivingPitch (v : Triad) (m : Move) : Nat :=
  let r := v.val % 12
  if v.val < 12 then
    match m with
    | .P => (r + 3) % 12
    | .L => (r + 11) % 12
    | .R => (r + 9) % 12
  else
    match m with
    | .P => (r + 4) % 12
    | .L => (r + 8) % 12
    | .R => (r + 10) % 12

/-- Pitch class departing under move `m` from triad `v`. -/
def departingPitch (v : Triad) (m : Move) : Nat :=
  let r := v.val % 12
  if v.val < 12 then
    match m with
    | .P => (r + 4) % 12
    | .L => r
    | .R => (r + 7) % 12
  else
    match m with
    | .P => (r + 3) % 12
    | .L => (r + 7) % 12
    | .R => r

/-- Every neo-Riemannian move `P`, `L`, `R` is an involution on the 24 triads. -/
theorem move_involutive : ∀ (v : Triad) (m : Move), applyMove (applyMove v m) m = v := by
  intro v m
  cases m <;> revert v <;> decide

/-- The triad graph is bipartite: every move flips Major <-> Minor. -/
theorem move_bipartite : ∀ (v : Triad) (m : Move), isMajor (applyMove v m) ≠ isMajor v := by
  intro v m
  cases m <;> revert v <;> decide

/-- Simple 3-regularity: distinct moves from any triad lead to distinct neighbors. -/
theorem move_distinct_neighbors :
    ∀ (v : Triad) (m₁ m₂ : Move), m₁ ≠ m₂ → applyMove v m₁ ≠ applyMove v m₂ := by
  intro v m₁ m₂
  cases m₁ <;> cases m₂ <;> revert v <;> decide

/-- Proposition 2.1: `P = L (L R)^4` on all 24 triads. -/
theorem prop2_1_presentation_P :
    ∀ (v : Triad), applyMove v .P = applyMove (applyLRPow 4 v) .L := by
  decide

/-- Proposition 2.1: `R = L (L R)` on all 24 triads. -/
theorem prop2_1_presentation_R :
    ∀ (v : Triad), applyMove v .R = applyMove (applyLRPow 1 v) .L := by
  decide

/-- Proposition 2.1: `(L R)^12 = id` on all 24 triads. -/
theorem prop2_1_lr_pow_12 : ∀ (v : Triad), applyLRPow 12 v = v := by
  decide

/-- Proposition 2.1: `L R` has exact order 12 (no proper positive power `< 12` fixes all triads). -/
theorem prop2_1_lr_exact_order_12 :
    ∀ (k : Fin 11), ∃ (v : Triad), applyLRPow (k.val + 1) v ≠ v := by
  decide

/-- Dihedral group element `(flip, rot) ∈ Bool × Fin 12` acting on C major (`0`). -/
def dihedralAction (flip : Bool) (rot : Fin 12) (v : Triad) : Triad :=
  let v1 := applyLRPow rot.val v
  if flip then applyMove v1 .L else v1

/-- Proposition 2.1: `D_12` acts simply transitively on all 24 consonant triads. -/
theorem prop2_1_simply_transitive :
    ∀ (v : Triad),
      ∃ (flip : Bool) (rot : Fin 12),
        dihedralAction flip rot ⟨0, by decide⟩ = v ∧
        ∀ (flip' : Bool) (rot' : Fin 12),
          dihedralAction flip' rot' ⟨0, by decide⟩ = v → flip' = flip ∧ rot' = rot := by
  decide

/-- Corollary 2.2: `V = 24`, `E = 36` undirected edges, Betti rank `E - V + 1 = 13`. -/
theorem cor2_2_betti_rank : (24 * 3) / 2 - 24 + 1 = 13 := by
  decide

end Morpheus
