import Morpheus.TriadGraph

/-!
# Tune Theorem Local Lemmas & NEG-M4 Counterexample (Lemma 4.1, Theorem 4.2)

Machine-checked proofs of Lemma 4.1 (L1, L2, L3), single-step voice-leading uniqueness,
and the mandatory non-backtracking counterexample (`NEG-M4`).
-/

namespace Morpheus

/-- Circular pitch-class distance in `{0..6}`. -/
def circularDist12 (a b : Nat) : Nat :=
  let d := if a ≥ b then (a - b) % 12 else (b - a) % 12
  min d (12 - d)

/-- Lemma 4.1 (L1): At every triad, P, L, R depart three pairwise distinct pitch classes. -/
theorem lemma4_1_L1 :
    ∀ (v : Triad) (m₁ m₂ : Move), m₁ ≠ m₂ → departingPitch v m₁ ≠ departingPitch v m₂ := by
  intro v m₁ m₂
  cases m₁ <;> cases m₂ <;> revert v <;> decide

/-- Lemma 4.1 (L2): From `m(v)`, only the backtracking move `m` departs the just-arrived pitch. -/
theorem lemma4_1_L2 :
    ∀ (v : Triad) (m m' : Move),
      departingPitch (applyMove v m) m' = arrivingPitch v m ↔ m' = m := by
  intro v m m'
  cases m <;> cases m' <;> revert v <;> decide

/-- Lemma 4.1 (L3a): No major or minor triad contains two distinct notes 1 or 2 semitones apart. -/
theorem lemma4_1_L3_triad_intervals :
    ∀ (v : Triad),
      let ns := triadNotesList v
      ∀ a ∈ ns, ∀ b ∈ ns, a ≠ b → circularDist12 a b ≠ 1 ∧ circularDist12 a b ≠ 2 := by
  decide

/-- Lemma 4.1 (L3b): Every PLR move shifts a single voice by 1 or 2 semitones modulo 12. -/
theorem lemma4_1_L3_move_steps :
    ∀ (v : Triad) (m : Move),
      (voiceStep v m = -2 ∨ voiceStep v m = -1 ∨ voiceStep v m = 1 ∨ voiceStep v m = 2) ∧
      ((departingPitch v m : Int) + voiceStep v m) % 12 = (arrivingPitch v m : Int) := by
  intro v m
  cases m <;> revert v <;> decide

/-- Theorem 4.2 local propagation uniqueness: arriving pitch uniquely determines the PLR move from `v`. -/
theorem thm4_2_local_move_unique :
    ∀ (v : Triad) (m₁ m₂ : Move), arrivingPitch v m₁ = arrivingPitch v m₂ → m₁ = m₂ := by
  intro v m₁ m₂
  cases m₁ <;> cases m₂ <;> revert v <;> decide

/-- NEG-M4: Without non-backtracking, `C -> Cm -> C` and `E -> Abm -> E` share cyclic tune `(Eb, E)`. -/
theorem neg_M4_backtracking_counterexample :
    let cMaj : Triad := ⟨0, by decide⟩
    let cMin : Triad := ⟨12, by decide⟩
    let eMaj : Triad := ⟨4, by decide⟩
    let abMin : Triad := ⟨20, by decide⟩
    applyMove cMaj .P = cMin ∧ applyMove cMin .P = cMaj ∧
    applyMove eMaj .L = abMin ∧ applyMove abMin .L = eMaj ∧
    cMaj ≠ eMaj ∧
    arrivingPitch cMaj .P = 3 ∧ arrivingPitch cMin .P = 4 ∧
    arrivingPitch eMaj .L = 3 ∧ arrivingPitch abMin .L = 4 := by
  decide

end Morpheus
