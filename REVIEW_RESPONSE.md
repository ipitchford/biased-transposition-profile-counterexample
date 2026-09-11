# Response to the supplied review

The supplied review recommended Minor Revision. Its text is retained privately
and is identified here by SHA-256
`e591136a0e5784d5d4316f8d634d5b0d3986660732921aca05c0ebfec99090e5`.
Authorship, independence and redistribution rights were not established, so
the review is not relicensed or reproduced.

| Review item | Action | Closure |
|---|---|---|
| Saved time column was reported but not enforced | `verify_numeric.py` now requires 61 finite five-column rows with times exactly 0 through 60; corrupt-time and truncation mutations must fail. | Resolved by executable gate. |
| Table 1 success did not bind positive published values | Exact `(N,t,b)` tuples and downward-rounded bounds are in `certificate_contract.json`; the checker requires every rigorous lower endpoint to meet the printed value. | Resolved by exact arithmetic and hostile mutations. |
| 2025 conference source absent | Paper and audit now distinguish the FPSAC extended abstract from the official poster and keep the contradiction pinned to arXiv v1. | Resolved by primary-source inspection. |
| Epsilon range implicit | The paper states `0 < epsilon < 1` when defining mixing times. | Resolved. |
| Table 1 could resemble exhaustive permutation enumeration | Caption now says “rigorous event-based lower bounds” and explains the million-row arithmetic certificate. | Resolved. |
| Diagnostic reports used unconditional pass language | Load-bearing predicates are separated from observations; limitations are carried in `claims.json`, the paper and assurance record. | Resolved. |
| Original manuscript could appear current | `source_inputs/` is marked inherited/superseded provenance and `LICENSES.md` assigns `NOASSERTION`. | Resolved. |
| Table 2 layout and Theorem 2 weakening | Retained as optional exposition/future-proof improvements; neither is needed for correctness of the release claim. | Deliberate non-blocking choice. |

The independent methodology role additionally found that the old manifest
checker accepted unlisted files. Version 1.0.1 now compares the manifest with
the complete non-operational file inventory and includes an unlisted-file
negative control. The claim contract also rejects sign, constant, threshold
and table-tuple mutations. These are verification repairs, not changes to the
main theorem.
