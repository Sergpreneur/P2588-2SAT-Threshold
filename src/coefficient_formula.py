#!/usr/bin/env python3
"""Exact EGF implementation of Dovgal--de Panafieu--Ravelomanana Thm 4.7.
Arrays are ordinary coefficients in w; outer arrays are EGF numerators in z.
Only the Python standard library is used.
"""
from fractions import Fraction
from math import comb
import json
from pathlib import Path

def add(a,b):
    c=[Fraction(0)]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=x
    while len(c)>1 and not c[-1]:c.pop()
    return c

def scale(a,s):return [x*s for x in a]
def mul(a,b):
    c=[Fraction(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:c[i+j]+=x*y
    while len(c)>1 and not c[-1]:c.pop()
    return c

def qpow(k):return [Fraction(comb(k,j)) for j in range(k+1)]
def calculate(N):
    G=[qpow(n*(n-1)//2) for n in range(N+1)]
    H=[[Fraction(1)]]
    E=[[Fraction(1)]]
    A=[[Fraction(1)]]
    rows=[]
    for n in range(1,N+1):
        hn=[Fraction(0)]
        for j in range(1,n+1):hn=add(hn,scale(mul(G[j],H[n-j]),-comb(n,j)))
        H.append(hn)
        en=mul(G[n],hn)
        E.append(en)
        an=en[:]
        for j in range(1,n):an=add(an,scale(mul(A[j],A[n-j]),-comb(n,j)))
        A.append(scale(an,Fraction(1,2)))
    for n in range(N+1):
        row=[Fraction(0)]
        for k in range(n+1):
            exponent=2*(n-1)*k-k*(k-1)//2
            row=add(row,scale(mul(qpow(exponent),A[n-k]),2**n*comb(n,k)))
        assert all(x.denominator==1 for x in row)
        row=list(map(int,row))
        total_clauses=2*n*(n-1)
        row += [0]*(total_clauses+1-len(row))
        assert len(row)==total_clauses+1
        assert all(0<=x<=comb(total_clauses,m) for m,x in enumerate(row))
        rows.append(row)
    return rows,{'G':G,'H':H,'E':E,'A':A}

def serialize(trace):
    return {name:[[str(x) for x in p] for p in polynomials] for name,polynomials in trace.items()}

if __name__=='__main__':
    import argparse,time
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=7);p.add_argument('--output',default='data/exact_coefficients.json');args=p.parse_args()
    t=time.perf_counter();rows,trace=calculate(args.n)
    out={'model':'distinct clauses on distinct pairs of labeled Boolean variables','method':'DPR Theorem 4.7; full degree, exact rational polynomials in w','rows':{str(n):r for n,r in enumerate(rows)},'intermediates':serialize(trace)}
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    for n,row in enumerate(rows):
        c=2*n*(n-1)
        crossing=next((m for m,a in enumerate(row) if 2*a<comb(c,m)),None)
        print('n',n,'total_sat',sum(row),'first_below_half',crossing)
    for m in (12,13):
        a=rows[6][m];d=comb(60,m)
        print('n=6 m=',m,'a=',a,'denom=',d,'difference=',2*a-d,'probability=',Fraction(a,d),float(Fraction(a,d)))
    print('elapsed_seconds',time.perf_counter()-t)
