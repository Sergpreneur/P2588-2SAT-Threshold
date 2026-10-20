import Std

/-!
# Kernel-checked arithmetic for the P2588 coefficient certificate

This module checks finite integer-polynomial identities. It does not identify
their result with a cardinality of satisfiable clause sets. That bridge is an
explicit hypothesis in the separate model module.

All closed computations use `decide`, with proof terms checked by Lean's kernel.
There is no native_decide, external SAT oracle, or axiom for the enumeration.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace P2588.Certificate

abbrev Poly := List Int

def fact : Nat → Nat
  | 0 => 1
  | n+1 => (n+1) * fact n

def falling (n : Nat) : Nat → Nat
  | 0 => 1
  | k+1 => falling n k * (n-k)

/-- Descending factorial divided by k!, later related to Nat.choose. -/
def binom (n k : Nat) : Nat := falling n k / fact k

def add : Poly → Poly → Poly
  | [], q => q
  | p, [] => p
  | a::p, b::q => (a+b)::add p q

def scale (a : Int) (p : Poly) : Poly := p.map (a * ·)

def shift (k : Nat) (p : Poly) : Poly := List.replicate k 0 ++ p

def mul : Poly → Poly → Poly
  | [], _ => []
  | a::p, q => add (scale a q) (0::mul p q)

def normal (p : Poly) : Poly :=
  (p.reverse.dropWhile (· == 0)).reverse

def sumPolys (ps : List Poly) : Poly := ps.foldl add []

def coefficient (p : Poly) (m : Nat) : Int :=
  ((List.range p.length).map fun j => p[j]! * (binom j m : Int)).foldl (·+·) 0

end P2588.Certificate
