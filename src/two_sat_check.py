"""The clause (i,a,j,b) means (x_i == a) OR (x_j == b)."""

def clauses(n):
    return [(i,a,j,b) for j in range(1,n) for i in range(j) for a in range(2) for b in range(2)]

def masks(n):
    return [sum(1<<s for s in range(1<<n) if ((s>>i)&1)==a or ((s>>j)&1)==b)
            for i,a,j,b in clauses(n)]

def satisfiable_assignments(n,formula):
    return any(all(((s>>i)&1)==a or ((s>>j)&1)==b for i,a,j,b in formula) for s in range(1<<n))

def satisfiable_scc(n,formula):
    # Vertex 2*i+a denotes the literal x_i == a. Complement flips the last bit.
    reach=[1<<v for v in range(2*n)]
    for i,a,j,b in formula:
        u=2*i+a;v=2*j+b
        reach[u^1]|=1<<v;reach[v^1]|=1<<u
    for k in range(2*n):
        for i in range(2*n):
            if reach[i]>>k&1:reach[i]|=reach[k]
    return all(not ((reach[2*i]>>(2*i+1)&1) and (reach[2*i+1]>>(2*i)&1)) for i in range(n))
