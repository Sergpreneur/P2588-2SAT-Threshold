import sys,unittest,itertools,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from coefficient_formula import calculate
from mask_dp import count
from two_sat_check import clauses,satisfiable_assignments,satisfiable_scc

class SmallInstances(unittest.TestCase):
    def test_all_subsets_three_variables(self):
        universe=clauses(3);row=[0]*13
        for bits in range(1<<len(universe)):
            f=[c for i,c in enumerate(universe) if bits>>i&1]
            sat=satisfiable_assignments(3,f)
            self.assertEqual(sat,satisfiable_scc(3,f))
            row[bits.bit_count()]+=sat
        self.assertEqual(row,calculate(3)[0][3])

    def test_two_buffer_reference_all_degrees(self):
        rows,_=calculate(4)
        for n in range(1,5):self.assertEqual(count(n),rows[n])

    def test_scc_against_truth_table_six_variables(self):
        rng=random.Random(2588);universe=clauses(6)
        for m in range(61):
            for _ in range(20):
                f=rng.sample(universe,m)
                self.assertEqual(satisfiable_assignments(6,f),satisfiable_scc(6,f))

if __name__=='__main__':unittest.main()
