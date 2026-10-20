# P2588: exact median threshold for random 2-SAT on six variables

**Author:** Nefedov Sergey, Moscow State University, Mathematics Department.

**Repository:** https://github.com/Sergpreneur/P2588-2SAT-Threshold

This version is prepared for public upload to the URL above. Public availability
has not yet been verified. See `GITHUB_UPLOAD_RU.md` for upload instructions.

**Answer: 13.** In the model of uniformly chosen sets of distinct clauses,

```
a(6,12) =   805717285720
a(6,13) =  2381437338960
C(60,13)=  5166863427600
2*a(6,13) - C(60,13) = -403988749680
P(13) = 9922655579 / 21528597615 = 0.46090580336205517...
```

Deleting a clause preserves satisfiability and sends a uniformly chosen
(m+1)-clause set to a uniformly chosen m-clause set. Thus P(m) is nonincreasing.
The exact comparisons at 12 and 13 prove that 13 is the first strict crossing.

## Independent executed checks

1. New exact rational-polynomial implementation of Theorem 4.7 of Dovgal,
   de Panafieu and Ravelomanana, with all degrees retained, n <= 7.
2. A separate integer-polynomial certificate and stand-alone checker.
3. Direct assignment-mask subset DP, written in C++17, processing all 60
   clauses. All coefficients m <= 13 agree. Final nonempty states: 24,444,343.
   Measured DP time in this environment: 117.657 seconds, excluding teardown.
4. Exhaustive examination of every one of 2^24 clause subsets for n=4,
   agreeing in every degree, and exhaustive SCC/truth-table comparison for n=3.
5. Both unmodified upstream coefficient functions at commit
   `346079fa8606ebd48f4557bcef7bc1f73a2aed4d` were run at (6,12) and (6,13).

## Reproduce

Run commands from this directory. The main implementation and checker require
Python 3.8+ and its standard library. The direct verifier needs a C++17 compiler.
The recorded environment is Python 3.12.14, g++ 13.3.0. Only the separate
upstream comparison uses SymPy 1.14.0.

```bash
python3 verify/verify_count.py
python3 -m unittest discover -s tests -v
python3 verify/verify_count.py --rerun-dp
```

The first command checks exact polynomial identities, binomial transforms,
saved independent outputs, and SHA-256 digests. It does not rerun the large DP.
The third command additionally recompiles and executes the direct DP and compares
its complete output, including its order-independent state checksum. Allow
several minutes and approximately 5 GiB of available process memory. Actual memory
and runtime depend on the compiler and standard-library implementation.

To regenerate coefficient files and the exhaustive n=4 output:

```bash
python3 src/coefficient_formula.py --n 7 --output data/exact_coefficients.json
python3 src/integer_certificate.py
g++ -O3 -std=c++17 -Wall -Wextra -pedantic src/brute_force.cpp -o /tmp/p2588-brute
/tmp/p2588-brute 4
```

Output files are hashed for the recorded run. Reformatting/regenerating them may
change byte hashes even when their mathematical contents agree. Preserve the
original files when checking the recorded manifest.

## Contents and status

- `results/final_report_ru.md`: Russian report and full proof of monotonicity.
- `paper/main.tex`, `paper/P2588_exact_threshold.pdf`: English research-note draft.
- `src/`: two exact coefficient implementations, independent direct DP,
  a small two-buffer reference DP, exhaustive enumeration, and SCC checks.
- `certificates/`: exact integer identities and final numerical certificate.
- `data/`: full coefficient rows, assignment-mask order, independent outputs.
- `verify/verify_count.py`: no imports from `src/`, no SAT solver dependency.
- `experiments/`: executed logs, versions, upstream provenance and comparison.
- `lean/`: Lean 4.19.0 project, pinned mathlib revision, sources and executed build logs.
- `CITATION.cff`: citation metadata for these computational materials.
- `SHA256SUMS`: SHA-256 digests of the distributed payload. The Lean project
  also retains its original, separately checked manifest.

This is a computationally certified evaluation of a consequence of a published
enumeration theorem. A separate publication of the explicit coefficient was not
found in the bounded audit, but first-publication priority is **not established**.
The authors' existing notebook already evaluated it internally when summing all
degrees. No new general enumeration theorem is claimed. A companion Lean 4.19.0
project now checks the certificate arithmetic, finite clause model and
monotonicity. The connection between certificate coefficients and satisfiable
formula counts remains an explicit hypothesis: **the Lean formalization is
partial**. Its sources and build logs are supplied in `P2588_Lean_checked.zip`.
The same project is unpacked in `lean/`; run `lake build` from that directory.
The GitHub archive contains `lean/` directly and omits the redundant companion ZIP.
For the arithmetic-only check without mathlib, run:

```bash
cd lean
lean P2588Arithmetic.lean
```

The updated preprint describes the coverage. Nothing has been submitted to a journal.

Primary source: S. Dovgal, E. de Panafieu, V. Ravelomanana,
*Exact enumeration of satisfiable 2-SAT formulae*, Combinatorial Theory 3(2)
(2023), article **7**, DOI: https://doi.org/10.5070/C63261985;
https://arxiv.org/abs/2108.08067v2, Theorems 4.6 and 4.7.
