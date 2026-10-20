import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from coefficient_formula import calculate
from integer_certificate import build
from math import comb

class PublishedData(unittest.TestCase):
    def test_published_rows_and_totals(self):
        rows,_=calculate(7)
        self.assertEqual(rows[6][:13],[1,60,1770,34220,487500,5451072,49675760,377136960,2411974740,13063104000,60169952412,237115483560,805717285720])
        self.assertEqual([sum(r) for r in rows[1:]],[1,15,2397,3049713,28694311447,2034602766692687,1115068294703296663717])
        self.assertEqual(rows,build(7)['rows'])
        for n in range(2,8):
            self.assertEqual(rows[n][3*comb(n,2)],2**n)
            self.assertTrue(all(x==0 for x in rows[n][3*comb(n,2)+1:]))
            C=4*comb(n,2)
            for m in range(C):self.assertGreaterEqual(rows[n][m]*comb(C,m+1),rows[n][m+1]*comb(C,m))

if __name__=='__main__':unittest.main()
