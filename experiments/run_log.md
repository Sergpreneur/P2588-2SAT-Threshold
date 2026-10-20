# Executed work

Session date: 2026-10-20. Tools and outputs are actual, not estimated.

1. Read the research brief and checked TheoremDB, arXiv v2, journal PDF, and
   current companion-repository API. Inspected the exact clause convention.
2. Ran `python src/coefficient_formula.py --n 7 --output data/exact_coefficients.json`.
   Elapsed 0.01035 seconds on this run. Full polynomial degrees retained.
   Reproduced all listed totals and a(6,12); extracted a(6,13)=2381437338960.
3. Benchmarked a two-buffer C++ mask DP. It hit its explicit state cap of
   12,000,000 during step 55 and exited with code 2. Its earlier completed
   stages agree in state counts/checksums with the completed implementation.
4. Replaced double buffering by increasing-popcount in-place transitions,
   after proving their equivalence. Compiled using the flags in environment.json.
   Executed all 60 steps, m<=13, cap 40,000,000 (not reached).
   Final states 24,444,343; last step at 117.657 seconds. Exit status 0.
5. Downloaded unmodified symbolic upstream modules at the pinned commit and
   executed both exact coefficient functions for m=12 and m=13, all agreeing.
6. Ran the four Python unittest cases; all passed in 0.611 seconds.
   Ran exhaustive n=4 C++ enumeration over 16,777,216 clause sets; full row agrees.
   Separately ran the in-place C++ DP at n=4 and compared all available degrees.
7. Generated the integer-polynomial certificate in q and executed its stand-alone
   checker. Checked all identities and all rows, not only the two target entries.
8. Wrote the Russian report, English draft and reproduction instructions.

State-table checksums are order-independent 64-bit checksums, not cryptographic
proofs. SHA256SUMS covers the actual distributed source, certificate and output
bytes. The compact verifier does not trust a saved output integer as the only
evidence: it checks finite polynomial identities and binomial transforms. Full
independent reenactment is available with `python verify/verify_count.py --rerun-dp`.

No statistical estimate was used in the proof. At the initial numerical run no
Lean toolchain was present in the standard command path. In a subsequent step,
the companion Lean 4.19.0 project was compiled: it checks certificate arithmetic,
the finite model and monotonicity. The enumerative bridge remains a hypothesis.
The updated preprint records this partial formalization.
