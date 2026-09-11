---
title: "Audit and claim disposition"
subtitle: "Biased-transposition research bundle"
date: "11 September 2026 · Version 1.0.1"
lang: en-GB
fontsize: 11pt
geometry:
  - a4paper
  - margin=24mm
colorlinks: true
linkcolor: EPpurple
urlcolor: EPpurple
---

# 1. Corpus and result boundary

The inspected corpus is the complete uploaded ZIP, the earlier computational ZIP, both copies of the research brief, and the primary sources identified below. The complete ZIP contains 18 files: eight Python programs, five JSON results, three logs, one Markdown manuscript and one companion PDF. Its computational files match the earlier ZIP byte for byte. The two brief copies are also byte-identical. Exact hashes and archive-membership comparisons are recorded in `input_inventory.json`.

The final paper supplies an unconditional disproof of the profile conjecture in Nestoridi and Yan's arXiv:2409.16387v1, a general untouched-subset lower-bound theorem, and corrected supporting bounds. It does **not** supply the original requested general upper bound $t_{\rm mix}(\varepsilon)\le t_*+O(n)$. The proof gap is preserved explicitly in `claims.json`, rather than represented as a completed sharp-transition theorem.

The counterexample was prompted by the uploaded draft's class-sensitive objection. The present continuation replaces its unproved refined-Poisson premise with a single final-state event and an elementary untouched-count calculation. No claim is made that the original idea of examining slow-label fixed counts originated in this continuation. No exhaustive priority search or independent external mathematical review has been completed.

# 2. Mathematical audit of the supplied manuscript

Line numbers below refer to the unmodified manuscript `biased_transposition_transition.md`, archived in the `source_inputs/biased_transposition/` directory. These local source locations are included for reproducibility.

**A01 — General lower bound: retain with discrete-time scope.** Theorem 1, lines 29–38, correctly derives a variance bound from pairwise negative covariance and obtains $d(t)\ge1-6/U(t)$. Actual chain distances require integer times. The final paper makes that restriction explicit and checks the mixing-time rounding. The bound is Proposition 3 of the final paper.

**A02 — Additional Poisson assertion: remove.** Line 40 infers a $\operatorname{Pois}(1+U(t))$ fixed-count comparison from an untouched-count Poisson statement. A Poisson limit for untouched labels alone does not establish the contribution of labels that return home, or their joint dependence. Poissonising time also changes the covariance calculation. The final paper instead proves exactly the subset-count limit it uses and compares final-state events using $F_S\ge A_S$.

**A03 — Arbitrary two-class spectrum: correct, but reattribute.** Theorem 2, lines 46–54, is valid with $m\alpha+(n-m)\beta=n$. The group-algebra derivation is already present with arbitrary $|A|,|B|$ in Nestoridi and Yan's spectrum argument; their upper-bound analysis later specialises to equal halves. It is therefore misleading to present the algebraic formula as a new unequal-size extension. Section 3 below records the correctly normalised formula and its proof.

**A04 — More than two classes: narrow the conclusion.** Line 54 correctly observes that overlapping pairwise class sums need not commute. That invalidates this particular simultaneous scalar decomposition. It does not prove that no explicit spectrum, other diagonalisation or different spectral method exists.

**A05 — Interlacing after squaring: add a hypothesis.** Theorem 3, lines 58–62, overstates the domain of its second inequality. Ordering eigenvalues does not preserve the required order after squaring negative bases. The first, standard-representation bound is valid for every positive probability vector. The bound using $(1-2p_{(k)})^{2t}$ is justified when $p_{\max}\le1/2$. The exact counterexample $n=2$, $p=(9/10,1/10)$, $t=1$ gives $\chi^2=256/625<16/25$, the claimed unrestricted lower bound. Bounded arrays satisfy the repaired hypothesis for all sufficiently large $n$.

**A06 — Chi-square mixing location: replace equalities by lower bounds.** Lines 13, 64–74 and 183 repeatedly promote one spectral contribution into an actual chi-square cutoff location. The proof supplies no upper bound on the remaining representations. The final paper retains the resulting lower bounds on chi-square mixing time. It does not claim a chi-square cutoff theorem.

**A07 — Location lag and window width: distinguish.** Line 72 identifies an $n\log\log n$ lag relative to $t_*$ as a chi-square window of that order. A shift in the centre does not establish a window width. The final paper states the lag only as a one-sided location result.

**A08 — Spectral impossibility and sparse classes: qualify.** Lines 13, 74 and 183 rule out spectral approaches too broadly and do not impose all the asymptotic conditions needed for the obstruction. In particular, an $o(n)$ slow class need not dominate $t_*$. The final paper gives the explicit regime $m=n^\alpha$, $b<\alpha<1$, and identifies the failure of the direct, untruncated chi-square upper bound. Refined Fourier or spectral approximations remain possible.

**A09 — Central-mixture upper bound: retain, correct calibration.** Theorem 4, lines 78–85, contains a valid commuting-convolution argument. The final paper handles the endpoint $\theta=1$ separately. It uses the checked uniform mixing asymptotic rather than the draft's recalled constant and mismatched exponential parametrisation. Teyssier's convention at time $(n/2)\log n+Kn$ has Poisson excess $e^{-2K}$; at $(n/2)(\log n+K)$ the excess is $e^{-K}$. These time coordinates must not be interchanged.

**A10 — Comparison factor and priority: retract.** Lines 13 and 85 describe the extracted-uniform upper bound as at most a factor $1/c$ from $t_*$, and suggest the first explicit general constant. The bound proved there guarantees only the cruder worst comparison of order $1/c^2$. The earlier Bernstein–Bhatnagar–Pak paper already discusses an upper bound with a squared minimum-weight coefficient. The final paper makes no priority claim. That historical observation is separate from the flaw reported in their stopping-time construction.

**A11 — Profile counterexample: close the conditional gap.** Proposition 5(ii), lines 128–138, assumes the joint slow/fast fixed-count limit. Its status should therefore be conditional; a numerical fit cannot discharge that premise. The final paper's Theorem 1 proves a contradiction at $s=\log6$ without it. A stronger class-refined exact profile remains a conjecture. Even proving a joint fixed-count limit would initially establish a lower bound on full total variation, not automatically a matching upper bound.

**A12 — The brief's conjecture: preserve its actual meaning.** Lines 15 and 108 suggest the original conjecture identified total fixed points as a sufficient statistic. The supplied brief conjectures a mixing-time location through the expected untouched count. It does not make that stronger profile claim. The two research questions are separated throughout the final output.

**A13 — Critical square-root family: correct the asymptotic regime.** The Monte Carlo family with $\sqrt n$ labels of weight $1/(2n)$ has $\alpha=b=1/2$. At $t_*$, both classes contribute to $U$. The slow mean tends to $(\sqrt5-1)/2$, not one. The final paper derives this boundary case directly and uses it as a sanity check.

# 3. Correctly normalised two-class spectrum

Let $A$ have size $m$, $B$ have size $n-m$, and let the probabilities be $\alpha/n$ and $\beta/n$, respectively, with $m\alpha+(n-m)\beta=n$. Let $T_X=\sum_{i<j\in X}(ij)$. In the group algebra,

$$
\mu=q e+\frac{2}{n^2}\left[
(\alpha^2-\alpha\beta)T_A
+(\beta^2-\alpha\beta)T_B
+\alpha\beta T_{[n]}\right],
\qquad q=\frac{m\alpha^2+(n-m)\beta^2}{n^2}.
$$

Within-class and cross-class coefficients verify this identity term by term. The global class sum $T_{[n]}$ is central, and $T_A,T_B$ commute because they have disjoint supports. Let $f^\lambda$ denote the dimension of the irreducible representation indexed by a partition $\lambda$, let $\operatorname{ct}(\lambda)=\sum_{(i,j)\in\lambda}(j-i)$, and let $c^\lambda_{\rho,\tau}$ be the Littlewood–Richardson coefficient. Restricting the representation indexed by $\lambda\vdash n$ to $S_A\times S_B$ gives eigenvalues

$$
q+\frac{2}{n^2}\left[
(\alpha^2-\alpha\beta)\operatorname{ct}(\rho)
+(\beta^2-\alpha\beta)\operatorname{ct}(\tau)
+\alpha\beta\operatorname{ct}(\lambda)\right],
$$

with multiplicity $f^\lambda f^\rho f^\tau c^\lambda_{\rho,\tau}$ in the regular representation, for $\rho\vdash m$ and $\tau\vdash n-m$. This is the scalar action of the three commuting sums on each restriction component. The trivial block evaluates to one by the probability normalisation. It is a useful immediate check on the identity coefficient.

The inspected PDF of Nestoridi and Yan (2024), printed page 3, Theorem 1.2, displays the first term with denominator $2N$ rather than $N^2$. The same discrepancy appears in their general eigenvalue definition. This is a normalisation typo: the identity mass must be $(a^2|A|+b^2|B|)/N^2$. Their later equal-half working formula (PDF Section 4; HTML equation 42) uses the correctly normalised identity term. This local correction is separate from the profile counterexample and does not invalidate their cutoff proof.

The independent dense-matrix check used $n=6$, $m=2$, $\alpha=2$ and $\beta=1/2$. Its maximum eigenvalue discrepancy against the supplied spectrum implementation was $2.887\times10^{-15}$. The supplied Littlewood–Richardson routine uses floating-point inner products and rounding; this one bounded cross-check does not certify that implementation for arbitrarily large partitions.

# 4. Strict attenuation by added Poisson noise

One step in the draft's conditional argument can also be established without a numerical monotonicity check. Let $u>0$, $\gamma\ge0$ and $\delta>0$. Then

$$
\|\operatorname{Pois}(\gamma+\delta+u)-\operatorname{Pois}(\gamma+\delta)\|_{\rm TV}
<
\|\operatorname{Pois}(\gamma+u)-\operatorname{Pois}(\gamma)\|_{\rm TV}.
$$

To prove this, set $a_j=\mathbb P(\operatorname{Pois}(\gamma+u)=j)-\mathbb P(\operatorname{Pois}(\gamma)=j)$. The sequence has both negative and positive entries: $a_0<0$, its sum is zero, and it is not identically zero. Convolve with the mass function of $\operatorname{Pois}(\delta)$, which is strictly positive at every nonnegative integer. At some output index $k$, the convolution sum contains a strictly negative and a strictly positive contribution. The triangle inequality is strict at that index and non-strict at all others. Summing proves strict contraction in $\ell^1$, hence in total variation.

Taking $\gamma=\delta=1/2$ recovers the strict comparison needed by the draft's conditional proposition. It does not prove the unverified refined fixed-count limit or a replacement full profile. Theorem 1 in the final paper avoids those questions.

# 5. Computational audit and missingness

**Deterministic enumeration.** The programs named `exact_tv.py` and `run_families.py` enumerate all states but propagate probabilities in float64. “Exact” should describe the finite state space, not the arithmetic. Their integer first-crossing times are valid numerical estimates of the discrete mixing time. Their additional linear interpolations are descriptive interpolations, not new discrete-time values.

**Implementation-diverse in-package replay performed.** The new code replays all eight $n=8$ arrays at all 61 stored times using separate state indexing and the opposite multiplication convention. It checks normalisation, TV monotonicity, all stored numerical columns, first integer crossings and the hierarchy total-fixed TV $\le$ class-fixed TV $\le$ fixed-set TV $\le$ full TV. The complete errors are saved. The $n=4$ integer-arithmetic walk is a separate finite check. These implementations were produced within the same research process; they are not independent reproduction or external review.

**Acceptance-condition repair.** Review found that the first version reported, but did not reject, a mismatch in the saved time column; required only interval ordering for the finite Table 1 calculation; and checked listed manifest entries without rejecting extra package files. Version 1.0.1 now requires exactly 61 stored rows with times $0,1,\ldots,60$ in every $n=8$ family, binds each exact finite calculation to its stated $(N,t)$ tuple and published downward-rounded lower bound, and compares the manifest with the complete non-operational file inventory. `certificate_contract.json` also binds the published profile coefficients, rational gap thresholds and finite-moment margin. `code/test_negative_controls.py` verifies rejection of 23 mutations spanning finite bounds, time coordinates and row structure, all stored numerical columns, profile coefficients and thresholds, moment and table contracts, manifest completeness and safety, and manuscript-to-contract correspondence. These repairs strengthen what a checker `PASS` means; they do not change the mathematical values or Theorem 1.

**Larger results not replayed.** The $n=9$ and $n=10$ trajectories, the $n=20$ spectrum-derived chi-square table and the $n=2000$ Monte Carlo results were inspected as inherited artifacts. No full rerun of those outputs is claimed. The main theorem and exact certificates do not depend on them.

**Monte Carlo precision.** The code compares empirical laws of selected statistics against empirical uniform laws. Such empirical TV distances are biased upward; a single $1/\sqrt R$ quantity is not a general confidence interval and does not account for support size. The auxiliary two-uniform-sample program examines some noise effects, but its output is not a full uncertainty analysis. The script takes $R$ as an argument; its seed is visible in the implementation. The supplied JSON does not embed a complete invocation, software environment or raw draws. The package therefore does not claim exact reproduction of the Monte Carlo run.

**Projection limits.** Even an exact TV distance for a statistic is only a lower bound on full TV. Agreement among a finite collection of projected distributions cannot exclude a further distinguishing statistic. Neither the finite-state tables nor Monte Carlo identify the general upper bound by themselves.

**Memory correction.** The supplied `proj_fast.py` encodes class counts in base $n+1$ and passes the resulting sparse integers directly to `numpy.bincount`. With many classes, the maximum code is exponential in class count, despite only $n!$ realised states. The new implementation uses `numpy.unique(..., return_inverse=True)` to assign compact observed category indices before aggregation. The $n=8$ continuum case with eight distinct classes was exercised with this replacement.

**Metadata and strict JSON.** The inherited Monte Carlo JSON contains nine literal `NaN` values. Those entries represent unavailable model predictions when the fast untouched mean exceeds the code's chosen threshold. The original file is preserved unchanged for provenance; it is not treated as strict JSON. All newly generated JSON reports reject non-finite values. The $n=9$ “equal-halves” array has sizes four and five, with actual weights $np_{\rm slow}=9/19$ and $np_{\rm fast}=27/19$ in the raw 0.5/1.5 family.

# 6. Source inspection and novelty boundary

**Inspected conjecture and conference history.** Nestoridi and Yan, arXiv:2409.16387v1, PDF printed page 4, Conjecture 1.6, and matching HTML statement were inspected. Both the time convention and Poisson parameter were checked against the rendered preprint. The asymptotic contradiction is expressly pinned to that version. Two distinct 2025 FPSAC sources were also inspected. The published extended abstract's Theorem 1.2 uses the corrected $N^2$ denominator and retains the unequal-class setup; it says that the abstract does not discuss the limit profile and directs readers to the longer preprint. The official conference poster separately restates the limit-profile conjecture. The abstract's omission therefore does not establish withdrawal, while the poster is evidence that the conjecture remained part of the authors' conference presentation. On 11 September 2026, the official *Annals of Applied Probability* future-papers page listed the article as accepted; no public final journal text was located in the bounded search, so no claim is made about whether that version retains the conjecture.

**Uniform calibration.** Teyssier, arXiv:1905.08514v1, Section 1.1, explicitly uses identity mass $1/n$ and transposition mass $2/n^2$. Theorem 1.1 fixes the $Kn$ shift convention. This source supplies the external uniform-mixing input to the final comparison bound.

**Older comparison.** Bernstein, Bhatnagar and Pak, arXiv:1709.03477v1, printed page 2, discusses the minimum-weight-squared comparison. Nestoridi and Yan describe the separate stopping-time problem in that earlier work. The present direct convolution proof avoids reliance on the disputed stopping-time construction.

**Recent related work.** Jain–Sawhney was checked for its uniform hitting-time statement; Jain–Nestoridi for its star-shuffle statement and method summary; Francis–Nestoridi for its biased-perturbation separation result, including Proposition 8 and Section 4.5. These sources were not fully audited proof by proof. Their scopes do not discharge the general bounded-product upper bound.

**Search boundary.** This was a targeted check of the uploaded sources, their key cited precedents and closely related arXiv results accessible on 10 September 2026. Search-result absence is not evidence that no earlier counterexample or broader theorem exists. The package makes no first-in-literature claim and does not treat journal publication or external review as prerequisites for an accurately labelled candidate release.

# 7. Disposition

The original manuscript should be superseded by the final paper for any candidate release based on this continuation. Its broad claims of a resolved chi-square cutoff, a chi-square window, spectral impossibility, an exact corrected profile and a universal factor-$1/c$ comparison should not be carried forward. The supplied code and data remain useful archived provenance with the qualifications above.

The established release claim is an **unconditional counterexample to the inspected equal-half profile conjecture**, supported by the general subset argument and finite arithmetic certificates. The general $O(n)$ sharp-location upper bound remains the explicit unsolved obligation.

# Sources

## Main mathematical sources

Nestoridi, E., & Yan, A. (2024). *Cutoff for the biased random transposition shuffle* (arXiv:2409.16387v1). [arXiv v1](https://arxiv.org/abs/2409.16387v1).

Nestoridi, E., & Yan, A. (2025). Cutoff for the biased random transposition shuffle. *Séminaire Lotharingien de Combinatoire, 93B*, Article 6. [Official paper](https://www.mat.univie.ac.at/~slc/wpapers/FPSAC2025/6.pdf).

Nestoridi, E., & Yan, A. (2025). *Cutoff for the biased random transposition shuffle* [FPSAC 2025 poster]. [Official poster](https://www.math.sci.hokudai.ac.jp/sympo/fpsac2025/public/posters/107.pdf).

Teyssier, L. (2020). Limit profile for random transpositions. *The Annals of Probability, 48*(5), 2323–2343. [doi:10.1214/20-AOP1424](https://doi.org/10.1214/20-AOP1424).

Teyssier, L. (2019). *Limit profile for random transpositions* (arXiv:1905.08514v1) [Version used to check the time convention]. [arXiv v1](https://arxiv.org/abs/1905.08514v1).

Bernstein, M., Bhatnagar, N., & Pak, I. (2017). *Cutoff for biased transpositions*. [arXiv v1](https://arxiv.org/abs/1709.03477v1).

## Related results inspected for scope

Jain, V., & Sawhney, M. (2024). *Hitting time mixing for the random transposition walk* (arXiv:2410.23944v1). arXiv. https://arxiv.org/abs/2410.23944v1

Jain, V., & Nestoridi, E. (2026). *Hitting-time mixing for the star transposition shuffle* (arXiv:2608.13727v1). arXiv. https://arxiv.org/abs/2608.13727v1

Francis, P. E., & Nestoridi, E. (2026). *Limit profiles for separation distance* (arXiv:2605.19084v1). arXiv. https://arxiv.org/abs/2605.19084v1

## Project context

Evidence Press. (2026, September 8). *Biased shuffles still cut off* [Candidate research release, version 1.0.0-candidate]. https://evidencepress.org/releases/bounded-product-transposition-cutoff/
