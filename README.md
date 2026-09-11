# Untouched subsets and a biased-transposition profile counterexample

**Date:** 11 September 2026. **Version:** 1.0.1-candidate. **Status:** unrefereed; proofs supplied, bounded checks executed; no formal proof-assistant or independent external review.

## Result

The paper proves an unconditional counterexample to Conjecture 1.6 of Nestoridi and Yan, **arXiv:2409.16387v1**. At the specified early-window time, a slow-subset event yields full total variation at least 0.710647716… asymptotically, while the conjectured value is 0.681595297…. The gap is certified as greater than 29/1000. A second disproof needs only eleven untouched-count factorial moments.

The requested general sharp-location conjecture

    t_mix(epsilon) = t_star + O(n),   c/n <= p_i <= C/n,
    sum_i [1 - 2 p_i (1 - p_i)]^t_star = 1

**remains unresolved**. In particular, the package does not claim the general upper bound. The completed result is a profile counterexample, not a resolution of that original location conjecture or a replacement exact profile.

## Contents

- `paper.pdf`, `paper.md`, `paper.tex`: candidate article with an explicit supplementary-dossier boundary, editable Markdown and generated LaTeX.
- `audit.pdf`, `audit.md`: audit of the supplied claims, prior-art calibration, corrected two-class spectrum, code and missingness audit.
- `claims.json`: machine-readable claim statuses and remaining proof obligations.
- `certificate_contract.json`: exact constants, table rows and trajectory dimensions bound to checker success.
- `code/verify_exact.py`: dependency-free exact certificate checker.
- `code/verify_numeric.py`: NumPy within-package second-implementation replay and dense spectrum check.
- `editorial/`, `EDITORIAL_DECISION.md`, `REVIEW_RESPONSE.md`: frozen role reports, synthesis and repair disposition.
- `STATUS.md`, `ASSURANCE.md`, `PROVENANCE.md`, `LICENSES.md`: status, trust boundary, contribution history and file-level rights.
- `results/`: executed check reports, including optimised-Python repeat results.
- `source_inputs/`: original supplied manuscript, PDF, code, data and brief, preserved unchanged at the depositor's explicit direction and not relicensed.
- `input_inventory.json`: hashes of the original uploads and archive members; verifies the two ZIPs' common files match.
- `MANIFEST.json`, `code/verify_manifest.py`: complete non-operational file-inventory and byte-integrity check for this delivered package.

## Reproduce the exact certificates

From this directory:

```sh
python3 code/verify_manifest.py
python3 code/verify_exact.py --out results/exact_verification.json
python3 -O code/verify_exact.py --out results/exact_verification_optimized.json
python3 code/verify_claim_surface.py --out results/claim_surface_verification.json
python3 code/test_negative_controls.py
python3 -O code/test_negative_controls.py
```

NumPy is required for the trajectory mutation controls; the two exact-verification commands have no third-party dependency. Verification gates use explicit exceptions, not assertions that disappear under optimisation. The exponential inequalities use rational Taylor bounds. Finite-time power calculations use exact integer operations with outward fixed-point rounding. The four finite-N rows certify the published event-based lower bounds on total variation; they do not evaluate the full permutation distribution.

## Reproduce the numerical audit

The final producer replay used Python 3.14.7 and NumPy 2.4.2. NumPy is the only third-party dependency for the new numerical checker. It imports the archived `spectrum.py` for comparison with an independently built dense transition matrix; it does not use the inherited state indexer.

```sh
OPENBLAS_NUM_THREADS=1 python3 code/verify_numeric.py \
  --input source_inputs/biased_transposition \
  --out results/numerical_verification.json
```

The replay covers all 8! states, eight supplied n=8 arrays and all 61 saved times. It additionally checks a 720-state unequal-class spectrum and an integer-arithmetic 24-state walk. The n=9, n=10, n=20 and n=2000 inherited computations were not fully rerun. Their inclusion is archival, not a claim of independent numerical reproduction.

A fresh run may change last-bit floating-point values or the Python/NumPy version metadata. The original manifest checks the delivered bytes, rather than claiming every regenerated report will be byte-identical across environments. After intentionally regenerating a file, a manifest mismatch for that file is expected.

## Rebuild the PDFs

A working Pandoc and XeLaTeX installation is required. The executed commands were:

```sh
pandoc paper.md --standalone --pdf-engine=xelatex \
  --include-in-header=code/pdf_header.tex -o paper.pdf
pandoc audit.md --standalone --pdf-engine=xelatex \
  --include-in-header=code/pdf_header.tex -o audit.pdf
pandoc paper.md --standalone \
  --include-in-header=code/pdf_header.tex -o paper.tex
```

The producer build used Pandoc 3.9 and Tectonic 0.17.0 as its XeTeX-compatible engine. Substitute `--pdf-engine=tectonic` for the first two commands to reproduce that exact route.

## Interpretation and provenance

The main theorem needs neither the supplied Monte Carlo results nor the unproved refined fixed-count limit from the draft. It does not challenge Nestoridi and Yan's cutoff theorem or their total-fixed-count theorem. The paper pins its contradiction to arXiv:2409.16387v1. The 2025 FPSAC extended abstract was inspected: it uses the corrected spectral denominator, does not discuss the limit profile and points readers to the longer preprint. The official FPSAC poster separately restates the profile conjecture. Priority and later literature have not been exhaustively audited.

The new JSON reports are strict JSON. The original Monte Carlo JSON contains nine NaN literals and is preserved as received; `MANIFEST.json` hashes it as bytes without parsing it. The code replacement compacts observed projection categories to avoid the original potentially exponential allocation.

The original materials retain their original provenance. No licence or human authorship is inferred for them. No user name has been assigned as author of the new paper. New prose, structured claims and generated reports are CC0-1.0; original verification code is MIT licensed. See `LICENSES.md`. The reports distinguish computational checks from a full mathematical or formal verification.
