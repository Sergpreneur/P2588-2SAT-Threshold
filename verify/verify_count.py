#!/usr/bin/env python3
"""Independent, standard-library-only integer certificate checker.

No import from src/ and no call to a SAT solver or a symbolic algebra package.
--rerun-dp additionally compiles and executes the independent 60-clause DP.
"""
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
from math import comb

ROOT=Path(__file__).resolve().parents[1]

def norm(a):
    a=list(a)
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def linear(terms):
    out=[0]*max(len(p)+shift for _,shift,p in terms)
    for multiplier,shift,p in terms:
        for i,v in enumerate(p):out[i+shift]+=multiplier*v
    return norm(out)

def product(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return norm(out)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rerun-dp',action='store_true');args=ap.parse_args()
    cert=json.loads((ROOT/'certificates/integer_polynomials.json').read_text())
    H,E,R,S=(cert[k] for k in ('H','E','R','S'))
    N=len(H)-1
    assert len(E)==len(R)==len(S)==N+1
    assert H[0]==E[0]==R[0]==[1]
    for n in range(1,N+1):
        # G*H=1, using EGF numerators.
        assert linear([(comb(n,j),comb(j,2),H[n-j]) for j in range(n+1)])==[0],('inverse',n)
        assert norm(E[n])==norm([0]*comb(n,2)+H[n]),('Hadamard',n)
        # R(z)=A(2z), hence R(z)^2=E(2z).
        square=linear([(comb(n,j),0,product(R[j],R[n-j])) for j in range(n+1)])
        assert square==norm([2**n*x for x in E[n]]),('square_root',n)
    rows=[]
    for n in range(N+1):
        sn=linear([(2**k*comb(n,k),2*(n-1)*k-comb(k,2),R[n-k]) for k in range(n+1)])
        assert sn==S[n],('Thm4.7',n)
        C=2*n*(n-1)
        row=[sum(v*comb(j,m) for j,v in enumerate(sn) if j>=m) for m in range(C+1)]
        assert row==cert['rows'][n]
        assert all(0<=v<=comb(C,m) for m,v in enumerate(row))
        assert row[0]==1
        for m in range(C):assert row[m]*comb(C,m+1)>=row[m+1]*comb(C,m)
        rows.append(row)
    primary=json.loads((ROOT/'data/exact_coefficients.json').read_text())
    assert rows==[primary['rows'][str(n)] for n in range(N+1)]
    brute=json.loads((ROOT/'data/brute_force_n4.json').read_text())
    assert brute['subsets_examined']==2**24
    assert brute['counts']==rows[4]
    independent=json.loads((ROOT/'data/mask_dp_n6.json').read_text())
    assert independent['n']==6 and independent['m_max']==13
    assert independent['counts']==rows[6][:14]
    summary=json.loads((ROOT/'certificates/count_certificate.json').read_text())
    for m in (12,13):
        a=rows[6][m];d=comb(60,m);v=summary['n6'][str(m)]
        assert v['count']==a and v['denominator']==d and v['twice_count_minus_denominator']==2*a-d
    assert 2*rows[6][12]>comb(60,12)
    assert 2*rows[6][13]<comb(60,13)
    upstream=json.loads((ROOT/'experiments/upstream_check.json').read_text())
    for item in upstream['results']:assert item['count']==rows[item['n']][item['m']]
    if args.rerun_dp:
        with tempfile.TemporaryDirectory() as td:
            binary=Path(td)/'mask_dp'
            subprocess.run(['g++','-O3','-std=c++17','-Wall','-Wextra','-pedantic',str(ROOT/'src/mask_dp.cpp'),'-o',str(binary)],check=True)
            result=subprocess.run([str(binary),'6','13','40000000'],check=True,text=True,stdout=subprocess.PIPE)
            fresh=json.loads(result.stdout)
            assert fresh==independent,'direct DP rerun mismatch'
        print('Independent direct mask DP rerun: PASS')
    manifest=ROOT/'SHA256SUMS'
    if manifest.exists():
        for line in manifest.read_text().splitlines():
            digest,name=line.split('  ',1)
            assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,('SHA256',name)
        print('SHA-256 manifest: PASS')
    print('Integer identities, all coefficient rows, published values, direct DP log, brute force: PASS')
    print('a_6,13 =',rows[6][13])
    print('First strict half-probability crossing: 13 (monotonicity proof in report)')
    print('This is an executable certificate check, not a Lean kernel proof.')

if __name__=='__main__':main()
