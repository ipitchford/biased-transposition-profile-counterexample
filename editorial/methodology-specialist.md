# Methodology specialist review

Frozen artifact: original ZIP SHA-256
`03d8eae7e9e9cd263f5ba46d5443a0365eb13c59d917539a6a62a3361cbb50d2`.
The reviewer did not inspect other role reports.

**Recommendation:** Major Revision — HOLD_FOR_REPAIR. **Confidence:** 4/5.

The central counterexample and finite-moment alternative appeared logically
sound, and fresh normal/optimized replays passed. Two acceptance defects still
blocked the original package: the manifest checker accepted unlisted files,
and the numerical checker reported but did not reject corrupt saved time
coordinates.

Required successor tests must reject an unlisted file, duplicate manifest
path, removed or corrupted listed file, unsafe path, changed time coordinate,
truncated/reordered trajectory, perturbed saved numerical columns, changed
profile sign or threshold, and a manuscript table value inconsistent with the
certificate. A machine-readable claim contract was required because hard-coded
arithmetic alone does not establish claim-to-certificate correspondence.

The repair must regenerate normal and optimized receipts, construct a complete
manifest, freeze a new SHA-256 and receive confirmation review against those
exact bytes. Exact certificates remain finite evidence, not formal verification
of the asymptotic proof. Larger inherited runs remain unreplayed. The role's
provisional REF-informed score was 2-star for originality, significance and
rigour before repair, with rigour capable of 3-star after closure.
