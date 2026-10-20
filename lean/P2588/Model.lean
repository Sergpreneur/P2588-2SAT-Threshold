import Mathlib.Combinatorics.SetFamily.LYM
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import P2588.Certificate

/-!
# The finite clause model and monotonicity

The two exact cardinalities are explicit hypotheses of the final threshold
theorem. No theorem in this file asserts the unformalized enumeration bridge.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace P2588

abbrev Var := Fin 6
abbrev Assignment := Var → Bool
abbrev Pair := {p : Var × Var // p.1 < p.2}
abbrev Clause := Pair × (Bool × Bool)
abbrev Formula := Finset Clause

def Holds (s : Assignment) (c : Clause) : Prop :=
  s c.1.1.1 = c.2.1 ∨ s c.1.1.2 = c.2.2

def Satisfiable (F : Formula) : Prop := ∃ s : Assignment, ∀ c ∈ F, Holds s c

instance (F : Formula) : Decidable (Satisfiable F) := by
  unfold Satisfiable Holds
  infer_instance

theorem pair_card : Fintype.card Pair = 15 := by decide

theorem clause_card : Fintype.card Clause = 60 := by
  simp [Clause, pair_card, Fintype.card_prod]

theorem assignment_card : Fintype.card Assignment = 64 := by decide

theorem satisfiable_of_subset {F G : Formula} (hFG : F ⊆ G)
    (hG : Satisfiable G) : Satisfiable F := by
  obtain ⟨s, hs⟩ := hG
  exact ⟨s, fun c hc => hs c (hFG hc)⟩

def satLayer (m : Nat) : Finset Formula :=
  (Finset.univ.powersetCard m).filter Satisfiable

def satCount (m : Nat) : Nat := (satLayer m).card

def probability (m : Nat) : ℚ := (satCount m : ℚ) / Nat.choose 60 m

theorem total_formulas (m : Nat) :
    ((Finset.univ : Finset Clause).powersetCard m).card = Nat.choose 60 m := by
  rw [Finset.card_powersetCard, Finset.card_univ, clause_card]

theorem mem_satLayer {m : Nat} {F : Formula} :
    F ∈ satLayer m ↔ F.card = m ∧ Satisfiable F := by
  simp [satLayer, Finset.mem_powersetCard]

theorem layer_sized (m : Nat) : (satLayer m : Set Formula).Sized m := by
  intro F hF
  exact (mem_satLayer.mp hF).1

theorem shadow_subset_layer (m : Nat) :
    Finset.shadow (satLayer (m+1)) ⊆ satLayer m := by
  intro F hF
  obtain ⟨G, hG, hFG, hcard⟩ :=
    Finset.mem_shadow_iff_exists_mem_card_add_one.mp hF
  have hg := mem_satLayer.mp hG
  apply mem_satLayer.mpr
  constructor
  · omega
  · exact satisfiable_of_subset hFG hg.2

theorem probability_succ_le (m : Nat) : probability (m+1) ≤ probability m := by
  have hlym := Finset.local_lubell_yamamoto_meshalkin_inequality_div
    (𝕜 := ℚ) (by omega : m+1 ≠ 0) (layer_sized (m+1))
  have hcard := Finset.card_le_card (shadow_subset_layer m)
  have hcast : ((Finset.shadow (satLayer (m+1))).card : ℚ) ≤ (satLayer m).card := by
    exact_mod_cast hcard
  have hdiv := div_le_div_of_nonneg_right hcast
    (show (0 : ℚ) ≤ (Nat.choose 60 m : ℚ) by positivity)
  change ((satLayer (m+1)).card : ℚ) / Nat.choose 60 (m+1) ≤
    ((satLayer m).card : ℚ) / Nat.choose 60 m
  calc
    _ ≤ ((Finset.shadow (satLayer (m+1))).card : ℚ) / Nat.choose 60 m := by
      simpa only [clause_card, Nat.add_sub_cancel] using hlym
    _ ≤ _ := hdiv

theorem probability_antitone : Antitone probability := by
  exact antitone_nat_of_succ_le probability_succ_le

theorem fact_eq_factorial (n : Nat) : Certificate.fact n = Nat.factorial n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [Certificate.fact, Nat.factorial_succ, ih]

theorem falling_eq_descFactorial (n k : Nat) :
    Certificate.falling n k = Nat.descFactorial n k := by
  induction k with
  | zero => rfl
  | succ k ih => simp [Certificate.falling, Nat.descFactorial_succ, ih, mul_comm]

theorem binom_eq_choose (n k : Nat) : Certificate.binom n k = Nat.choose n k := by
  rw [Certificate.binom, fact_eq_factorial, falling_eq_descFactorial,
    Nat.choose_eq_descFactorial_div_factorial]

theorem choose_60_12 : Nat.choose 60 12 = 1399358844975 := by
  rw [← binom_eq_choose]
  exact Certificate.denominator_12

theorem choose_60_13 : Nat.choose 60 13 = 5166863427600 := by
  rw [← binom_eq_choose]
  exact Certificate.denominator_13

/-- This is deliberately conditional: the finite-model count bridge is not proved. -/
theorem threshold13_of_counts
    (h12 : satCount 12 = 805717285720)
    (h13 : satCount 13 = 2381437338960) :
    probability 13 < (1/2 : ℚ) ∧
      ∀ m : Nat, m < 13 → (1/2 : ℚ) < probability m := by
  have p12 : (1/2 : ℚ) < probability 12 := by
    norm_num [probability, h12, choose_60_12]
  have p13 : probability 13 < (1/2 : ℚ) := by
    norm_num [probability, h13, choose_60_13]
  refine ⟨p13, ?_⟩
  intro m hm
  exact lt_of_lt_of_le p12 (probability_antitone (by omega))

/-- The exact missing bridge to the source theorem is visible as hypotheses. -/
theorem threshold13_of_enumeration_bridge
    (h12 : (satCount 12 : Int) = Certificate.coefficient Certificate.S6 12)
    (h13 : (satCount 13 : Int) = Certificate.coefficient Certificate.S6 13) :
    probability 13 < (1/2 : ℚ) ∧
      ∀ m : Nat, m < 13 → (1/2 : ℚ) < probability m := by
  rw [Certificate.coefficient_12] at h12
  rw [Certificate.coefficient_13] at h13
  apply threshold13_of_counts
  · exact_mod_cast h12
  · exact_mod_cast h13

#print axioms clause_card
#print axioms satisfiable_of_subset
#print axioms probability_antitone
#print axioms threshold13_of_enumeration_bridge

end P2588
