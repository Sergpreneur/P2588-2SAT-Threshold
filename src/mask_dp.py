#!/usr/bin/env python3
"""Simple two-buffer reference DP for small n. No polynomial formula is used."""
from two_sat_check import masks

def count(n,mmax=None):
    clause_masks=masks(n)
    if mmax is None:mmax=len(clause_masks)
    dp={(1<<(1<<n))-1:[1]+[0]*mmax}
    for clause in clause_masks:
        new={mask:p[:] for mask,p in dp.items()}
        for mask,p in dp.items():
            dest=mask&clause
            if dest and any(p[:-1]):
                target=new.setdefault(dest,[0]*(mmax+1))
                for k in range(mmax):target[k+1]+=p[k]
        dp=new
    return [sum(p[k] for p in dp.values()) for k in range(mmax+1)]

if __name__=='__main__':
    import argparse,json
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=4);args=ap.parse_args()
    print(json.dumps({'n':args.n,'counts':count(args.n)}))
