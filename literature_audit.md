# Source audit

See `results/novelty_audit.md` for the assessment and `experiments/source_provenance.json`
for downloaded-file digests. Sources accessed directly:

1. https://theoremdb.org/statements/P2588/ : current displayed snapshot remains
   July 25, 2026; the exact m=13 coefficient is marked unextracted.
2. https://arxiv.org/abs/2108.08067v2 and its PDF: 29-page preprint.
3. https://escholarship.org/uc/item/1m48c7s8 : journal article, 38-page PDF,
   DOI https://doi.org/10.5070/C63261985. Article **7**, not 8.
4. https://gitlab.com/sergey-dovgal/enumeration-2sat-aux : tree, public commit API,
   README, Sequences notebook and exact symbolic counting modules.

The clause model in Definition 2.1 and the 60-clause model agree exactly.
Theorem 4.7 is the mathematical source of the primary evaluator. Theorem 4.6
was also executed via upstream code. No source supports a claim of major new
enumeration theory or independently established publication priority.

Raw upstream code is not redistributed here; its exact commit and downloaded
byte hashes are recorded. Upstream computation outputs are included in
`experiments/upstream_check.json`.
