# Priority and novelty audit

Audit date: 2026-10-20. This is a bounded search, not proof of absence.

- Primary article: Dovgal, de Panafieu and Ravelomanana, *Exact enumeration of
  satisfiable 2-SAT formulae*, Combinatorial Theory 3(2) (2023), **article 7**,
  DOI 10.5070/C63261985. Theorem 4.7 already gives every a(n,m) in this model.
- arXiv landing page lists v2, last revised 2022-10-24. Its table stops at m=12.
- GitLab repository tree and commit history were fetched using the public API.
  Master head was still 346079fa8606ebd48f4557bcef7bc1f73a2aed4d (2022-10-07).
- At that commit, `Sequences.ipynb`, cell 23, prints a(n,m) for m in range(13),
  i.e. m=0,...,12. It does not separately print a(6,13).
- Crucially, cell 19 computes the total over **all** m=0,...,2n(n-1), for n=1,...,7.
  Thus its recorded total for n=6 already involved evaluating a(6,13) internally.
- The two original functions `generating_function_count_sat` and
  `second_generating_function_count_sat` were executed, unchanged, with (6,13).
  Both return 2381437338960. Both also reproduce the published (6,12) value.
- Queries included the exact coefficient with and without separators, the exact
  paper title, P2588, and six-variable median-threshold terminology. Engines
  returned the source paper, TheoremDB packet, and related asymptotic research.
  No separately displayed prior value a(6,13) was found in the inspected material.
  Some search results were irrelevant; such results are not evidence of priority.

**Assessment:** an explicit verified computation closing the finite TheoremDB
request, with an independent direct enumeration algorithm. It is a computational
corollary of existing work, not a new general theorem. Even the numerical evaluation
is already implicit in an executed upstream notebook. Do not claim a new solution
to the general random 2-SAT threshold problem or first-publication priority.

The new deliverable adds exact comparisons, an integer-polynomial certificate,
direct 60-clause assignment-mask counting, and reproducibility material. Whether
this warrants a standalone journal note is an editorial question; strong novelty
claims would not be justified by this audit.

Update after the numerical audit: the companion Lean 4.19.0 project has been
compiled. It checks exact certificate arithmetic, the finite model and
monotonicity. Its threshold theorem still assumes the enumerative bridge.
This partial formalization does not establish a new general enumeration theorem
or priority. No external journal submission has been performed.
