import P2588.Arithmetic

set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace P2588.Certificate

/- Exact certificate data, independently checked below; ascending q powers. -/
def H0 : Poly := [1]
def H1 : Poly := [-1]
def H2 : Poly := [2, -1]
def H3 : Poly := [-6, 6, 0, -1]
def H4 : Poly := [24, -36, 6, 8, 0, 0, -1]
def H5 : Poly := [-120, 240, -90, -60, 20, 0, 10, 0, 0, 0, -1]
def H6 : Poly := [720, -1800, 1080, 390, -360, 0, -70, 30, 0, 0, 12, 0, 0, 0, 0, -1]
def H : List Poly := [H0, H1, H2, H3, H4, H5, H6]
def E0 : Poly := [1]
def E1 : Poly := [-1]
def E2 : Poly := [0, 2, -1]
def E3 : Poly := [0, 0, 0, -6, 6, 0, -1]
def E4 : Poly := [0, 0, 0, 0, 0, 0, 24, -36, 6, 8, 0, 0, -1]
def E5 : Poly := [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -120, 240, -90, -60, 20, 0, 10, 0, 0, 0, -1]
def E6 : Poly := [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 720, -1800, 1080, 390, -360, 0, -70, 30, 0, 0, 12, 0, 0, 0, 0, -1]
def E : List Poly := [E0, E1, E2, E3, E4, E5, E6]
def R0 : Poly := [1]
def R1 : Poly := [-1]
def R2 : Poly := [-1, 4, -2]
def R3 : Poly := [-3, 12, -6, -24, 24, 0, -4]
def R4 : Poly := [-15, 72, -84, -48, 84, 0, 176, -288, 48, 64, 0, 0, -8]
def R5 : Poly := [-105, 600, -1020, 0, 1500, -1440, 1320, -1280, 160, 320, -1920, 3840, -1480, -960, 320, 0, 160, 0, 0, 0, -16]
def R6 : Poly := [-945, 6300, -13950, 6480, 17460, -23760, 9960, -10080, 18000, -10560, -12000, 24960, -9160, -5280, 1680, 23040, -56640, 34560, 12480, -11520, -96, -2240, 960, 0, 0, 384, 0, 0, 0, 0, -32]
def R : List Poly := [R0, R1, R2, R3, R4, R5, R6]
def S6 : Poly := [-945, 6300, -13950, 6480, 17460, -23760, 9960, -10080, 18000, -10560, -13260, 32160, -21400, -5280, 19680, 5760, -40800, 19200, 14400, -8580, -18816, 38800, -19680, -6480, 3840, 10944, -15360, 2400, 5760, -960, -4064, 3360, 0, -640, -240, 960, -480, 0, 0, 0, -192, 0, 0, 0, 0, 64]

def inverseCheck (n : Nat) : Poly :=
  normal <| sumPolys <| (List.range (n+1)).map fun j =>
    shift (binom j 2) (scale (binom n j : Int) H[n-j]!)

def squareCheck (n : Nat) : Poly :=
  normal <| sumPolys <| (List.range (n+1)).map fun j =>
    scale (binom n j : Int) (mul R[j]! R[n-j]!)

def assembledS6 : Poly :=
  normal <| sumPolys <| (List.range 7).map fun k =>
    shift (10*k-binom k 2) (scale ((2^k * binom 6 k : Nat) : Int) R[6-k]!)

theorem inverse_1 : inverseCheck 1 = [] := by decide
theorem hadamard_1 : normal E1 = normal (shift (binom 1 2) H1) := by decide
theorem square_1 : squareCheck 1 = normal (scale (2^1) E1) := by decide
theorem inverse_2 : inverseCheck 2 = [] := by decide
theorem hadamard_2 : normal E2 = normal (shift (binom 2 2) H2) := by decide
theorem square_2 : squareCheck 2 = normal (scale (2^2) E2) := by decide
theorem inverse_3 : inverseCheck 3 = [] := by decide
theorem hadamard_3 : normal E3 = normal (shift (binom 3 2) H3) := by decide
theorem square_3 : squareCheck 3 = normal (scale (2^3) E3) := by decide
theorem inverse_4 : inverseCheck 4 = [] := by decide
theorem hadamard_4 : normal E4 = normal (shift (binom 4 2) H4) := by decide
theorem square_4 : squareCheck 4 = normal (scale (2^4) E4) := by decide
theorem inverse_5 : inverseCheck 5 = [] := by decide
theorem hadamard_5 : normal E5 = normal (shift (binom 5 2) H5) := by decide
theorem square_5 : squareCheck 5 = normal (scale (2^5) E5) := by decide
theorem inverse_6 : inverseCheck 6 = [] := by decide
theorem hadamard_6 : normal E6 = normal (shift (binom 6 2) H6) := by decide
theorem square_6 : squareCheck 6 = normal (scale (2^6) E6) := by decide

theorem assembled_polynomial : assembledS6 = S6 := by decide

theorem coefficient_12 : coefficient S6 12 = 805717285720 := by decide
theorem coefficient_13 : coefficient S6 13 = 2381437338960 := by decide

theorem denominator_12 : binom 60 12 = 1399358844975 := by decide
theorem denominator_13 : binom 60 13 = 5166863427600 := by decide

theorem gap_12 :
    2 * coefficient S6 12 - (binom 60 12 : Int) = 212075726465 := by decide
theorem gap_13 :
    2 * coefficient S6 13 - (binom 60 13 : Int) = -403988749680 := by decide

theorem above_half_12 : (binom 60 12 : Int) < 2 * coefficient S6 12 := by decide
theorem below_half_13 : 2 * coefficient S6 13 < (binom 60 13 : Int) := by decide

theorem reduced_probability_13 :
    coefficient S6 13 * 21528597615 = (binom 60 13 : Int) * 9922655579 := by decide

/-- A first-crossing assertion for the coefficient polynomial, not for satCount. -/
theorem first_crossing_for_coefficient :
    2 * coefficient S6 13 < (binom 60 13 : Int) ∧
      ∀ m : Fin 13, (binom 60 m.val : Int) < 2 * coefficient S6 m.val := by decide

#print axioms coefficient_13
#print axioms assembled_polynomial
#print axioms square_6
#print axioms below_half_13
#print axioms first_crossing_for_coefficient

end P2588.Certificate
