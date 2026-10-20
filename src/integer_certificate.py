#!/usr/bin/env python3
"""Build an integer-polynomial certificate, using q=1+w and R_n=2^n A_n.
This implementation shares no polynomial code with coefficient_formula.py.
"""
import json
from math import comb
from pathlib import Path

def plus(a,b):
    c=list(a)+[0]*max(0,len(b)-len(a))
    for i,x in enumerate(b):c[i]+=x
    while len(c)>1 and c[-1]==0:c.pop()
    return c

def times(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    while len(c)>1 and c[-1]==0:c.pop()
    return c

def scalar(a,s):return [x*s for x in a]
def shift(a,k):return [0]*k+list(a)

def build(N=7):
    H=[[1]];E=[[1]];R=[[1]];S=[]
    for n in range(1,N+1):
        hn=[0]
        for j in range(1,n+1):hn=plus(hn,scalar(shift(H[n-j],comb(j,2)),-comb(n,j)))
        H.append(hn);en=shift(hn,comb(n,2));E.append(en)
        r=scalar(en,2**n)
        for j in range(1,n):r=plus(r,scalar(times(R[j],R[n-j]),-comb(n,j)))
        assert all(x%2==0 for x in r)
        R.append([x//2 for x in r])
    for n in range(N+1):
        sn=[0]
        for k in range(n+1):
            sn=plus(sn,scalar(shift(R[n-k],2*(n-1)*k-comb(k,2)),2**k*comb(n,k)))
        S.append(sn)
    rows=[]
    for n,s in enumerate(S):
        rows.append([sum(x*comb(j,m) for j,x in enumerate(s) if j>=m) for m in range(2*n*(n-1)+1)])
    return {'basis':'ordinary powers of q = 1+w; ascending coefficient order',
            'normalization':'H_n = n![z^n]1/G; E_n=q^C(n,2)H_n; R_n=2^n n![z^n]sqrt(G hadamard 1/G)',
            'H':H,'E':E,'R':R,'S':S,'rows':rows}

if __name__=='__main__':
    cert=build()
    out=Path('certificates/integer_polynomials.json');out.parent.mkdir(exist_ok=True,parents=True)
    out.write_text(json.dumps(cert,indent=2)+'\n')
    print('S6(q) =',' + '.join(f'{x}q^{j}' for j,x in enumerate(cert['S'][6]) if x))
    print('a6,13 =',cert['rows'][6][13])
