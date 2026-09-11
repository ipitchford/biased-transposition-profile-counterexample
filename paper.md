---
title: "Untouched subsets and a counterexample to the Nestoridi–Yan biased-transposition limit-profile conjecture"
subtitle: "An observable-event obstruction for a two-class shuffle"
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

**Status.** Unrefereed mathematical research note. The profile counterexample below has an unconditional proof and exact arithmetic certificates for its numerical inequalities. The general sharp-location conjecture remains unresolved. The certificates do not constitute formal verification of the asymptotic proofs.

## Abstract

Consider the discrete random walk on the symmetric group that independently samples two labels with probabilities $p_i$ and transposes them, retaining a self-sample as an identity step. A supplied research bundle investigates whether, for $c/n\le p_i\le C/n$, total-variation mixing occurs within $O(n)$ of the time at which the expected number of untouched labels is one. We obtain a different definitive result: the equal-half limit-profile conjecture in Nestoridi and Yan (2024, Conjecture 1.6, arXiv version 1) is false. For every fixed slow weight $0<b<1$, at time $\lfloor N(\log N-\log 6)/(2b)\rfloor$, the event that at least two slow labels are fixed gives an asymptotic total-variation lower bound $0.7106477160\ldots$. The conjectured value is $0.6815952973\ldots$. The argument uses only untouched slow labels and stationary fixed points; it requires no joint limit theorem for returned labels. We also prove a general subset-based Poisson lower bound, derive consequences for sparse and continuously distributed slow weights, and retain corrected lower, comparison and spectral bounds from the bundle. Exact certificates and an implementation-diverse finite-state replay within this package accompany the note. No matching upper bound at the untouched-label centre is asserted.

# 1. Model, research question and scope

All logarithms are natural. Time is measured in **discrete steps**, including identity steps. Write $[n]=\{1,\ldots,n\}$. The increment law on $S_n$ is

$$
\mu(e)=q:=\sum_i p_i^2,
\qquad \mu((ij))=2p_i p_j\quad(i<j),
\qquad \sum_i p_i=1.
$$

Start at the identity and let $\sigma_t$ be the product of $t$ independent increments. Let $\pi_n$ be the uniform law. Define

$$
d_n(t)=\|\mathcal L(\sigma_t)-\pi_n\|_{\rm TV},
\qquad
t_{\rm mix}(\varepsilon)=\min\{t\in\mathbb Z_{\ge0}:d_n(t)\le\varepsilon\}.
$$

Here and below, mixing times are stated for $0<\varepsilon<1$.

Translation invariance makes this the worst-start mixing time. Left and right multiplication give the same one-time law from the identity. The statements below therefore also apply to the convention in which the transpositions act on card labels rather than home-labelled coordinates.

A label is *untouched* if it has never participated in a nonidentity transposition. Set

$$
q_i=1-2p_i(1-p_i),\qquad
U_n(t)=\sum_i q_i^t,\qquad U_n(t_*)=1. \tag{1}
$$

Only $U_n$ is extended to real time. Under the standing bounded-weight hypothesis

$$
\frac cn\le p_i\le\frac Cn,\qquad 0<c\le C<\infty, \tag{2}
$$

$t_*$ exists uniquely for $n\ge2$. The supplied brief asks whether

$$
t_{\rm mix}(\varepsilon)=t_*+O_{c,C,\varepsilon}(n). \tag{3}
$$

The principal contribution is independent of any claimed solution of (3). An earlier candidate establishes a wider cutoff window but does not claim (3) (Evidence Press, 2026). A preliminary argument for the profile obstruction assumed an unproved joint limit for slow and fast fixed-point counts; Section 2 removes that assumption. Section 3 proves the general deterministic-subset theorem and its corollaries. The material after Section 3 is an explicitly supplementary dossier: it records inherited bounds, corrections and computations but is not presented as the article's new mathematical contribution.

| Item | Role in this article |
|:---|:---|
| Theorem 1 and finite-moment variant | New unconditional counterexample to the formula in arXiv:2409.16387v1 |
| Theorem 2 and Section 3 corollaries | New observable-subset lower-bound mechanism |
| Supplements A–C | Retained or corrected project results and bounded computations |
| Equation (31) | Unresolved general upper-bound obligation, not a claim |

**Interpretation and non-applications.** The results concern a time-homogeneous walk with fixed known weights, independent endpoint draws with replacement, identity self-samples, transpositions only and the uniform law on permutations as target. The main statements are asymptotic, with $p_i=\Theta(1/n)$ where specified. The lesson is that an aggregate fixed-point count can hide class-sensitive evidence about the full distribution; related stratified diagnostics may be worth investigating in MCMC, randomised algorithms or heterogeneous network processes, but no theorem here transfers the constants or convergence claims to those settings. In particular, the numerical lower bounds are not physical-shuffle prescriptions, empirical failure probabilities or guarantees for other Markov chains.

# 2. An unconditional counterexample to the proposed profile

## 2.1 Statement

Let $N=2m$, let $B$ contain $m$ slow labels, and give labels in $B$ probability $b/N$, where $0<b<1$ is fixed. The other $m$ labels have probability $(2-b)/N$. For $s\in\mathbb R$, put

$$
t_N(s)=\left\lfloor\frac{N}{2b}(\log N-s)\right\rfloor.
$$

Replacing the floor by any integer sequence at uniformly bounded distance changes each fixed-order avoidance probability by a factor $1+O(1/N)$ and hence leaves all limits below unchanged.

Nestoridi and Yan's Conjecture 1.6, in the inspected arXiv version 1, predicts

$$
d_N(t_N(s))\longrightarrow
\|\operatorname{Pois}(1+e^s/2)-\operatorname{Pois}(1)\|_{\rm TV}. \tag{4}
$$

The 2025 FPSAC poster restates this profile conjecture. The corresponding proceedings paper omits profile discussion and directs readers to the preprint. As of 11 September 2026, the official IMS page listed a journal article as forthcoming, but no public final journal text was located in the bounded check. The target here is therefore the displayed arXiv-v1 formula, not a claim about the contents of an unavailable final version.

**Theorem 1 (profile counterexample).** For every fixed $0<b<1$,

$$
\liminf_{N\to\infty,\,2\mid N}d_N(t_N(\log6))
\ge B_0:=\frac32e^{-1/2}-4e^{-3}.
\tag{5}
$$

At the same parameter, the right side of (4) equals

$$
D_0:=\|\operatorname{Pois}(4)-\operatorname{Pois}(1)\|_{\rm TV}
=\frac{5}{2e}-13e^{-4}.
\tag{6}
$$

Moreover,

$$
\begin{aligned}
B_0&=0.710647716097494363\ldots,\\
D_0&=0.681595297375061460\ldots,\\
\frac{29}{1000}&<B_0-D_0<\frac{291}{10000}.
\end{aligned} \tag{7}
$$

Consequently (4) is false. This conclusion concerns the proposed profile. It does not contradict the same paper's cutoff theorem or its theorem about the total number of fixed points, and it does not refute (3).

## 2.2 Proof by a single observable event

Let $A_B(t)$ count untouched labels in $B$, and let $F_B(t)$ count labels in $B$ that are fixed by $\sigma_t$. Pathwise,

$$F_B(t)\ge A_B(t). \tag{8}$$

For $r$ specified, distinct labels in $B$, avoiding a nonidentity transposition involving any of them in one step has probability

$$
Q_{N,r}=\left(1-\frac{rb}{N}\right)^2
+r\frac{b^2}{N^2}
=1-\frac{2rb}{N}+\frac{r(r+1)b^2}{N^2}. \tag{9}
$$

The first term describes two draws outside that set. The second describes drawing the same label in the set twice. In particular, a self-draw is correctly retained as an untouched event.

Write $(x)_r=x(x-1)\cdots(x-r+1)$. Independence of the increments gives the exact factorial moments

$$
\mathbb E[(A_B(t))_r]=(m)_r Q_{N,r}^{\,t}. \tag{10}
$$

For fixed $r$ and $s$, expansion of the logarithm yields

$$
t_N(s)\log Q_{N,r}
=-r(\log N-s)+O_{r,b}(\log N/N).
$$

Thus (10) converges to $(e^s/2)^r$. The factorial-moment criterion for a Poisson law gives

$$A_B(t_N(s))\ \Longrightarrow\ \operatorname{Pois}(e^s/2). \tag{11}$$

Under a uniform permutation, $r$ specified labels are all fixed with probability $1/(N)_r$. Hence

$$
\mathbb E_{\pi_N}[(F_B)_r]=\frac{(m)_r}{(N)_r}\longrightarrow(1/2)^r,
\qquad
F_B\text{ under }\pi_N\ \Longrightarrow\ \operatorname{Pois}(1/2). \tag{12}
$$

Take the event $E_N=\{F_B\ge2\}$, which is observable from the final permutation. Equations (8), (11) and (12), with $s=\log6$, imply

$$
d_N(t_N(\log6))
\ge \mathbb P_{t_N(\log6)}(E_N)-\pi_N(E_N)
\ge \mathbb P(A_B(t_N(\log6))\ge2)-\mathbb P_{\pi_N}(F_B\ge2).
$$

$$
\begin{aligned}
\liminf_N d_N(t_N(\log6))
&\ge \mathbb P(\operatorname{Pois}(3)\ge2)
 -\mathbb P(\operatorname{Pois}(1/2)\ge2)\\
&=\frac32e^{-1/2}-4e^{-3}.
\end{aligned}
$$

To compute (6), the likelihood ratio of the Poisson mass functions is $e^{-3}4^k$. It is below one at $k=2$ and above one at $k=3$. The upper tail starting at three therefore attains total variation:

$$
D_0=\mathbb P(\operatorname{Pois}(4)\ge3)
-\mathbb P(\operatorname{Pois}(1)\ge3)
=\frac{5}{2e}-13e^{-4}.
$$

The exact rational bounds in (7) follow from alternating Taylor bounds for the four exponentials. The verification program implements these bounds with integer and rational arithmetic. This completes the proof. $\square$

The use of (8) is deliberately one-sided. We have not assumed that slow labels which return to their original positions contribute an independent Poisson variable. Their contribution can only increase the probability of the event used in the proof.

## 2.3 A finite-moment certificate without a Poisson convergence theorem

The contradiction also follows from finitely many moments. For a nonnegative integer $z$, define

$$H_K(z)=\sum_{r=2}^{K}(-1)^r(r-1)\binom zr,$$

where terms with $r>z$ vanish. For odd $K$, $H_K(z)\le\mathbf1_{\{z\ge2\}}$; for even $K$, the inequality reverses. Indeed, when $z>K\ge2$,

$$
H_K(z)-1=(-1)^K
\left[z\binom{z-2}{K-1}-\binom{z-1}{K}\right],
$$

and the bracket is positive. When $2\le z\le K$, the sum equals one.

Use $K=11$ for $A_B$ and $K=10$ for stationary $F_B$. Equations (10) and (12), applied only to these finitely many moments, give

$$
\begin{aligned}
\liminf_Nd_N(t_N(\log6))
&\ge\sum_{r=2}^{11}\frac{(-1)^r(r-1)3^r}{r!}
-\sum_{r=2}^{10}\frac{(-1)^r(r-1)2^{-r}}{r!}\\
&=\frac{5730077809}{8174960640}
> D_0+\frac{19}{1000}.
\end{aligned} \tag{13}
$$

This is a second certificate of the disproof. Its strict comparison with $D_0$ is checked by exact rational arithmetic. Allowing the truncation order to increase recovers (5).

The same inequalities give finite-$N$ bounds. Table 1 uses $b=1/2$, an odd truncation of degree 21 for untouched slow labels and an even truncation of degree 20 for stationary fixed slow labels. Each displayed decimal is rounded **down** from a certified lower bound on full total variation. These are bounds, not computed full distances.

| $N$ | Integer time $t$ | Certified $d_N(t)$ lower bound |
|---:|---:|---:|
| 100 | 281 | 0.728373588448375223 |
| 1,000 | 5,115 | 0.713183969406310628 |
| 10,000 | 74,185 | 0.710943732347267839 |
| 1,000,000 | 12,023,751 | 0.710651383270999821 |

*Table 1. **Rigorous event-based lower bounds**, certified with exact arithmetic. The times are selected near $N(\log N-\log6)$; every certificate is valid at the explicitly reported integer, independently of how that integer was selected. The million-label row is an arithmetic certificate, not exhaustive enumeration of $S_N$.*

# 3. A general lower bound from deterministic subsets

For a deterministic subset $S_n\subseteq[n]$, let $A_{S_n}(t)$ and $F_{S_n}(t)$ denote its untouched and fixed counts. Define

$$U_{S_n}(t)=\sum_{i\in S_n}q_i^t.$$

**Theorem 2 (untouched-subset Poisson bound).** Assume (2), let $t_n=O(n\log n)$ be nonnegative integers, and suppose

$$
\max_{i\in S_n}q_i^{t_n}\longrightarrow0,\qquad
U_{S_n}(t_n)\longrightarrow u<\infty,\qquad
|S_n|/n\longrightarrow\gamma.
$$

The maximum over an empty set is interpreted as zero. Then

$$
A_{S_n}(t_n)\Longrightarrow\operatorname{Pois}(u),
\qquad F_{S_n}\text{ under }\pi_n\Longrightarrow\operatorname{Pois}(\gamma), \tag{14}
$$

and

$$
\liminf_n d_n(t_n)\ge
\Delta_+(u,\gamma):=
\sup_{\ell\ge1}\left\{
\mathbb P(\operatorname{Pois}(u)\ge\ell)
-\mathbb P(\operatorname{Pois}(\gamma)\ge\ell)\right\}. \tag{15}
$$

For $u\ge\gamma$, $\Delta_+$ equals the total-variation distance between those two Poisson laws. For $u<\gamma$, $\Delta_+=0$. In particular,

$$\gamma=0\quad\Longrightarrow\quad
\liminf_n d_n(t_n)\ge1-e^{-u}. \tag{16}$$

**Proof.** For a fixed set $R$ of $r$ distinct labels, put $p(R)=\sum_{i\in R}p_i$. The exact one-step avoidance probability is

$$Q_R=(1-p(R))^2+\sum_{i\in R}p_i^2. \tag{17}$$

Put $s_R=\sum_{i\in R}p_i$. Since $r$ is fixed and every $p_i\le C/n$, Taylor expansion with a uniform remainder gives

$$
\log Q_R=-2s_R-s_R^2+\sum_{i\in R}p_i^2+O_{r,C}(n^{-3}),
\qquad
\sum_{i\in R}\log q_i=-2s_R+O_{r,C}(n^{-3}).
$$

Thus $|\log Q_R-\sum_{i\in R}\log q_i|\le K_{r,C}/n^2$ for all sufficiently large $n$. Multiplication by $t_n\le Mn\log n$ and exponentiation therefore give the uniform comparison

$$
Q_R^{t_n}=
\left(1+O_{r,C,M}(\log n/n)\right)\prod_{i\in R}q_i^{t_n}, \tag{18}
$$

where $M$ is any fixed constant with $t_n\le Mn\log n$ for all sufficiently large $n$.

Write $a_i=q_i^{t_n}$. Summing (18) over ordered distinct $r$-tuples in $S_n$ gives the factorial moment of $A_{S_n}$. The difference between the unrestricted product sum $(\sum_{S_n}a_i)^r$ and the distinct-tuple sum is at most

$$\binom r2\left(\max_{S_n}a_i\right)\left(\sum_{S_n}a_i\right)^{r-1}.$$

For $r=1$ the sums agree. Thus every fixed factorial moment converges to $u^r$. Uniform fixed-count factorial moments are $(|S_n|)_r/(n)_r\to\gamma^r$. To make the distributional passage explicit, for each fixed threshold use the alternating inclusion–exclusion bounds for the corresponding point or tail probability, expressed through finitely many factorial moments. First pass $n\to\infty$ at fixed truncation order, then increase that order. The limiting remainders vanish because $\sum_{r\ge0}u^r/r!=e^u$ (and similarly for $\gamma$). This yields the two Poisson limits in (14) without an unstated uniform-integrability step.

For every fixed integer $\ell\ge1$, use $F_{S_n}(t_n)\ge A_{S_n}(t_n)$ in the event $\{F_{S_n}\ge\ell\}$. Pass to the limits in (14), then take the supremum over $\ell$. For $u>\gamma>0$, the Poisson likelihood ratio is increasing in the count, so an upper tail attains total variation. The zero-parameter cases follow directly. $\square$

The subset must be specified without inspecting the realised permutation. Selecting slow labels from the deterministic vector $p$ is allowed. Selecting whichever labels happen to be fixed would invalidate the stationary comparison used here.

## 3.1 Sparse, slow-dominated classes

Fix $0<b<\alpha<1$. Let $m=\lfloor n^\alpha\rfloor$, give the first $m$ labels probability $b/n$, and give the others probability $a_n/n$, where

$$a_n=\frac{n-mb}{n-m}\longrightarrow1.$$

For $t=O(n\log n)$, uniformly over both classes, $q_i^t=e^{-2p_it}(1+o(1))$. At $t=\alpha n\log n/(2b)+Kn$, the slow contribution tends to $e^{-2bK}$, while the fast contribution tends to zero, since $1-\alpha/b<0$. Monotonicity and the lower bound on the decay rates then give

$$t_*=\frac{\alpha n}{2b}\log n+o(n).$$

At $\lfloor t_*+Kn\rfloor$, take $S_n$ to be the slow class. Its stationary fixed-point mean is $m/n\to0$. Theorem 2 gives the unconditional lower envelope

$$
\liminf_n d_n(\lfloor t_*+Kn\rfloor)
\ge1-\exp\{-e^{-2bK}\}. \tag{19}
$$

Equation (19) is a lower bound. No matching upper bound for this family is proved here.

## 3.2 A critical sparse class: both populations matter

The simulated family with approximately $\sqrt n$ slow labels of weight $1/(2n)$ is at the boundary $\alpha=b=1/2$, rather than in the slow-dominated regime above. At $t=(n/2)\log n+Kn$, the two untouched contributions tend to $e^{-K}$ and $e^{-2K}$. Consequently,

$$
U_{S_n}(t_*)\longrightarrow y:=\frac{\sqrt5-1}{2},
\qquad y+y^2=1.
$$

Theorem 2 therefore gives

$$\liminf_n d_n(\lfloor t_*\rfloor)\ge1-e^{-y}=0.461\ldots.$$

The slow contribution at $t_*$ is not one. This checks which part of the population determines the lower bound and prevents an incorrect transfer of (19) to the critical case.

## 3.3 Continuously spaced weights

Let $0<b<1$, $B=2-b$ and $\Delta=B-b>0$. Set

$$p_i=\frac1n\left(b+\Delta\frac{i-1}{n-1}\right).$$

These probabilities sum exactly to one. For $x=2t/n$ of order $\log n$, the sum in (1) satisfies

$$
U_n(t)=(1+o(1))\,
\frac{n e^{-bx}(1-e^{-\Delta x})}{\Delta x}. \tag{20}
$$

To see this, $t p_i^2=O(\log n/n)$ uniformly, so replacing $q_i^t$ by $e^{-2p_it}$ incurs relative error $O(\log n/n)$. The resulting sum is geometric, with ratio $\exp[-\Delta x/(n-1)]$; the identity $1-e^{-y}=y(1+O(y))$ yields (20) uniformly for $x\asymp\log n$. At the root, (20) first implies $x_*\asymp\log n$. Taking logarithms then gives

$$b x_*=\log n-\log x_* -\log\Delta+O(\log\log n/\log n).$$

Since $\log x_*=\log\log n-\log b+O(\log\log n/\log n)$, one substitution gives

$$
t_*=\frac n{2b}\left[
\log n-\log\log n-\log(\Delta/b)
+O\!\left(\frac{\log\log n}{\log n}\right)\right]. \tag{21}
$$

Choose $S_n$ to be the first $\lfloor n/\sqrt{\log n}\rfloor$ labels. Its fraction tends to zero. The geometric progression shows that its complement contributes at most $O(e^{-k\sqrt{\log n}})$ times the full untouched sum, for some $k>0$. Within $S_n$, $np_i=b+o(1)$. Thus, at $\lfloor t_*+Kn\rfloor$, its untouched mean tends to $e^{-2bK}$. Equation (19) follows for this continuum family too. Neither (20) nor this lower envelope is a proof of its mixing-time upper bound.

# Supplementary dossier

Everything from this point is separated from the article's principal contribution. It records retained or corrected results, bounded computations and the unresolved project question. Its inclusion supports provenance and future work; it does not enlarge the release's headline theorem.

# Supplement A. General bounds retained from the project

## A.1 A one-sided sharp-location bound

**Proposition 3.** Under (2), for $n\ge4C$, integer $t\ge0$ and $0<\varepsilon<1$,

$$d_n(t)\ge1-\frac6{U_n(t)}. \tag{22}$$

Writing $\rho_{\min}=\min_i[-\log q_i]$, this implies

$$
\begin{aligned}
t_{\rm mix}(\varepsilon)
&\ge t_*-\rho_{\min}^{-1}\log\frac7{1-\varepsilon}\\
&\ge t_*-\frac{n}{2c(1-C/n)}\log\frac7{1-\varepsilon}.
\end{aligned} \tag{23}
$$

**Proof.** Let $Z$ be the total untouched count. For distinct $i,j$, subtracting $q_iq_j$ from the probability that both avoid a nonidentity swap in one step gives

$$2p_ip_j[1-2(1-p_i)(1-p_j)]\le0,$$

because $p_i,p_j\le1/4$. Raising the one-step probabilities to integer $t$ proves pairwise negative covariance of the untouched indicators. Hence $\operatorname{Var}(Z)\le U_n(t)$. Chebyshev's inequality gives $\mathbb P(Z\le U_n(t)/2)\le4/U_n(t)$. A uniform permutation has expected total fixed count one, so Markov's inequality bounds the probability that its fixed count exceeds $U_n(t)/2$ by $2/U_n(t)$. The walk's fixed count is at least $Z$, proving (22).

For $h\ge0$ with $t_*-h\ge0$, $U_n(t_*-h)\ge e^{\rho_{\min}h}$. Taking $h=\rho_{\min}^{-1}\log(7/(1-\varepsilon))$ makes (22) strictly larger than $\varepsilon$ at every nonnegative integer up to $t_*-h$. Finally, $\rho_{\min}\ge2c(1-C/n)/n$. If $t_*-h<0$, the claimed mixing-time bound is automatic. $\square$

This proof is for deterministic discrete times. It does not assert negative covariance after Poissonising time.

## A.2 A central-mixture upper bound

Let $\mu_0$ denote the uniform transposition increment law, including its identity mass $1/n$. Put $\theta=n^2p_{\min}^2\in[c^2,1]$. Pointwise $\mu\ge\theta\mu_0$, including at the identity. Unless $\theta=1$, write

$$\mu=\theta\mu_0+(1-\theta)\eta$$

for a probability law $\eta$. The uniform increment law is central in the group algebra, so it commutes with $\eta$. Conditional on $J\sim\operatorname{Bin}(t,\theta)$, convolution contraction gives

$$d_n(t)\le\mathbb E[d_n^{\rm unif}(J)]. \tag{24}$$

The uniform case is immediate when $\theta=1$. The classical uniform mixing estimate, in this discrete convention, is $t_{\rm mix}^{\rm unif}(\varepsilon)=(n/2)\log n+O_\varepsilon(n)$; Teyssier (2020) gives its full profile. For completeness, choose $k_0=(n/2)\log n+A_\varepsilon n$ so that $d_n^{\rm unif}(k_0)\le\varepsilon/2$, and take $t=\theta^{-1}(k_0+L_\varepsilon n)$. Then $\mathbb E J=k_0+L_\varepsilon n$ and $\operatorname{Var}J\le t=O_{c,\varepsilon}(n\log n)$. A Chernoff bound gives $\mathbb P(J<k_0)=o(1)$, uniformly for $\theta\ge c^2$; increasing $L_\varepsilon$ handles the finitely many smaller $n$. Hence (24) is at most $\varepsilon/2+\mathbb P(J<k_0)\le\varepsilon$ and

$$
t_{\rm mix}(\varepsilon)
\le\frac{n}{2\theta}\log n+O_{c,\varepsilon}(n)
\le\frac{n}{2c^2}\log n+O_{c,\varepsilon}(n). \tag{25}
$$

A bound with the same minimum-weight-squared coefficient already appears in the earlier biased-transposition literature (Bernstein et al., 2017, p. 2). No priority claim is made for (25). The direct proof above does not use that paper's disputed stopping-time construction.

**Normalisation check.** For uniform $p_i=1/n$,

$$t_*=\frac{\log n}{-\log(1-2/n+2/n^2)}\sim\frac n2\log n.$$

More generally, for $t\ge1$, the function $p\mapsto(1-2p+2p^2)^t$ is convex. Jensen's inequality shows $U_n(t)\ge n(1-2/n+2/n^2)^t$. Since $t_*\ge1$, the uniform value of $t_*$ is a lower bound for every probability vector. This also shows why (25) is not uniformly within a factor $1/c$ of $t_*$: its worst comparison is only of order $1/c^2$.

# Supplement B. What the spectral obstruction actually establishes

Let

$$L=2\operatorname{diag}(p)-2pp^{\mathsf T},\qquad
0=\lambda_1\le\lambda_2\le\cdots\le\lambda_n.$$

The permutation representation has transition matrix $I-L$. Its nonconstant part is the standard representation, which has dimension $n-1$ and therefore occurs $n-1$ times in the regular representation; this is the standard multiplicity formula for the regular representation (Diaconis, 1988, Chapter 3). Since $\mu$ is symmetric under inversion, the full transition matrix is self-adjoint. Decomposing the regular trace into irreducibles and retaining only the nonnegative even-power contribution of the standard representation yields

$$
\chi^2(\mathcal L(\sigma_t)\|\pi_n)
\ge(n-1)\sum_{k=2}^n(1-\lambda_k)^{2t}. \tag{26}
$$

Here $\chi^2(\nu\|\pi_n)=n!\sum_\sigma\nu(\sigma)^2-1$. Equivalently, symmetry gives $\chi^2=n!\mu^{*2t}(e)-1$, and the regular-representation trace separates into nonnegative even powers.

Order the probabilities increasingly as $p_{(1)},\ldots,p_{(n)}$. Applying the rank-one Hermitian interlacing theorem to $L=\operatorname{diag}(2p)-2pp^{\mathsf T}$ gives $\lambda_k\le2p_{(k)}$ (Horn & Johnson, 2013, Section 4.3). **When $p_{\max}\le1/2$**, both $1-\lambda_k$ and $1-2p_{(k)}$ are nonnegative, so

$$
\chi^2(\mathcal L(\sigma_t)\|\pi_n)
\ge(n-1)\sum_{k=2}^n(1-2p_{(k)})^{2t}. \tag{27}
$$

The restriction is essential to this inference. For $n=2$, $p=(9/10,1/10)$ and $t=1$, the true chi-square distance is $256/625$, whereas the unrestricted right side of (27) would be $16/25$. The latter is larger. The exact verifier includes this counterexample as a negative control. Under (2), $n\ge2C$ suffices for (27).

If the minimum probability occurs $m\ge2$ times, vectors supported on that class and summing to zero are exact eigenvectors of $L$ with eigenvalue $2p_{\min}$. Therefore

$$\chi^2\ge(n-1)(m-1)(1-2p_{\min})^{2t}. \tag{28}$$

In the sparse, slow-dominated family of Section 3.1, (28) shows that chi-square cannot become bounded by a fixed positive threshold before

$$\frac{(1+\alpha)n}{4b}\log n-O(n).$$

That lower bound lies $\frac{(1-\alpha)n}{4b}\log n-O(n)$ after $t_*$. It is a lower bound on chi-square mixing time, rather than an exact chi-square cutoff theorem.

For the continuum family of Section 3.3, applying the same geometric-sum estimate to (27) gives, for fixed $K$,

$$
\chi^2(\mathcal L(\sigma_{\lfloor t_*+Kn\rfloor})\|\pi_n)
\ge(1+o(1))\frac{\Delta}{2b}e^{-4bK}\log n. \tag{29}
$$

Deleting the smallest-probability term in (27) costs only a relative $O(\log n/n)$. To check the constant, (20) at $t_*$ gives $e^{-bx_*}\sim\Delta x_*/n$, where $x_*=2t_*/n$. Substitution into the sum with exponent $2t_*$ yields $\Delta x_*/2\sim\Delta\log n/(2b)$. Shifting time by $Kn$ contributes $e^{-4bK}$. More generally, for $t=t_*+L n\log\log n$ with fixed $L$, we still have $x=2t/n=O(\log n)$, so the replacement of $q_i^t$ by $e^{-2p_it}$ has relative error $O(\log n/n)$ and the geometric-sum remainder is uniform. The shift multiplies the lower bound by $(\log n)^{-4bL}$. It can therefore reach a fixed threshold only when $L\ge1/(4b)+o(1)$, so chi-square mixing at a fixed threshold is at least

$$t_*+\frac{n}{4b}\log\log n-O( n). \tag{30}$$

Equations (28)–(30) explain why a direct upper bound $d_n(t)\le\tfrac12\sqrt{\chi^2(t)}$ cannot establish (3) in these examples. They neither prove that total variation mixes at $t_*$ nor rule out a truncated or otherwise refined spectral proof. A lag between centres is also distinct from the width of a transition window.

# Supplement C. Computation, provenance and verification limits

The complete uploaded bundle contains a manuscript, a companion PDF, eight Python programs, five JSON result files and three logs. The earlier ZIP contains the same computational files without the manuscript and PDF. The package manifest records byte-level provenance. The research brief states (3); it does not assert that the total number of fixed points determines the whole profile.

Two verification programs accompany this note. `code/verify_exact.py` uses Python integers and rational arithmetic. It checks subset-avoidance identities against enumeration of draw pairs, the finite Bonferroni identity, the strict gap in (7), the degree-11 witness (13), the finite bounds in Table 1 and the failed out-of-domain spectral claim. Its finite-power bounds use directed rounding on a fixed-point integer grid. Its acceptance condition binds the exact parameter tuples and each published downward-rounded Table 1 bound. The verification gates remain active under `python -O`.

`code/verify_numeric.py` is a within-package second implementation: it enumerates permutations with a tuple-to-index map and applies value-swaps, whereas the inherited code uses Lehmer ranks and slot-swaps. All eight $n=8$ families, all 61 stored integer times, all probability-derived columns and all stored integer mixing thresholds were replayed. Full-TV discrepancies were below $4\times10^{-16}$; chi-square discrepancies were below $10^{-12}$. A $720\times720$ transition matrix for unequal class sizes $(2,4)$ reproduced the inherited representation-theoretic spectrum to $3\times10^{-15}$. An additional $n=4$ walk checked probability conservation using integer numerators. `code/test_negative_controls.py` confirms rejection of 23 specified hostile mutations. None of these producer-coordinated checks is independent external reproduction.

| $n=8$ family | Time | Full TV | Class-fixed TV | Total-fixed TV |
|:---|---:|---:|---:|---:|
| Equal halves, raw weights 0.5/1.5 | 12 | 0.333361 | 0.333146 | 0.252731 |
| Two slow labels | 9 | 0.319602 | 0.318587 | 0.251895 |
| Continuously spaced weights | 10 | 0.294253 | 0.292659 | 0.226561 |
| Three slow labels | 11 | 0.392844 | 0.392844 | 0.277187 |

*Table 2. Within-package second-implementation replay at the nearest integer to $t_*$. Raw family weights are normalised as in the inherited code. Distances use float64 arithmetic. Equality at six decimals does not certify exact equality.*

These finite calculations support the choice of a class-sensitive statistic. The proof of Theorem 1 does not depend on them. The $n=9$, $n=10$ and $n=2000$ Monte Carlo computations were inspected but not replayed. Their supplied outputs remain archived as inherited observations. Finite simulations of selected statistics cannot certify the full-distance upper bound in (3).

The audit also records several repairs. The original class-projection program can allocate a vector exponential in the number of weight classes; the replacement compacts observed keys before aggregation. The inherited Monte Carlo JSON contains nine `NaN` literals and therefore fails strict JSON parsing. Its empirical projection distances have sampling bias and are not exact distances. At $n=9$, families named “equal” actually have class sizes four and five, with normalised weights different from their raw labels.

# Supplement D. The unresolved upper bound

Combining (23) with (25) establishes the general order $n\log n$ and a lower bound within $O(n)$ of $t_*$. The remaining part of (3) is precisely

$$
\text{for every }\varepsilon>0,\ \exists K(c,C,\varepsilon)<\infty:
\quad d_n(\lfloor t_*+Kn\rfloor)\le\varepsilon
\quad\text{for all sufficiently large }n. \tag{31}
$$

No result in this package proves (31). The subset lower bounds also do not refute it. Conditional uniformity on the set of labels that have been touched would be a substantially stronger input; no such uniform approximation is established here.

For context, Jain and Sawhney (2024) prove hitting-time mixing for the **uniform** random-transposition walk. Jain and Nestoridi (2026) address the **star** transposition shuffle. Francis and Nestoridi (2026, Proposition 8) treat a very small biased perturbation in a **separation-distance** comparison. Those inspected results do not supply (31) for arbitrary bounded product weights. This was a targeted source check through 11 September 2026, rather than an exhaustive proof of absence from the literature.

The completed mathematical conclusion is the unconditional failure of (4), together with the subset theorem and the corrected supporting bounds. A replacement exact profile, general $O(n)$ location theorem, sharp upper window bound and priority claim remain outside the established results.

# References

## The profile conjecture and the uniform benchmark

Nestoridi, E., & Yan, A. (2024). *Cutoff for the biased random transposition shuffle* (arXiv:2409.16387v1). [arXiv v1](https://arxiv.org/abs/2409.16387v1).

Nestoridi, E., & Yan, A. (2025). Cutoff for the biased random transposition shuffle. *Séminaire Lotharingien de Combinatoire, 93B*, Article 6. [Official paper](https://www.mat.univie.ac.at/~slc/wpapers/FPSAC2025/6.pdf).

Nestoridi, E., & Yan, A. (2025). *Cutoff for the biased random transposition shuffle* [FPSAC 2025 poster]. [Official poster](https://www.math.sci.hokudai.ac.jp/sympo/fpsac2025/public/posters/107.pdf).

Teyssier, L. (2020). Limit profile for random transpositions. *The Annals of Probability, 48*(5), 2323–2343. [doi:10.1214/20-AOP1424](https://doi.org/10.1214/20-AOP1424).

Teyssier, L. (2019). *Limit profile for random transpositions* (arXiv:1905.08514v1) [Version used to check the time convention]. [arXiv v1](https://arxiv.org/abs/1905.08514v1).

Bernstein, M., Bhatnagar, N., & Pak, I. (2017). *Cutoff for biased transpositions*. [arXiv v1](https://arxiv.org/abs/1709.03477v1).

Diaconis, P. (1988). *Group representations in probability and statistics*. Institute of Mathematical Statistics.

Horn, R. A., & Johnson, C. R. (2013). *Matrix analysis* (2nd ed.). Cambridge University Press.

## Related hitting-time and separation results

Jain, V., & Sawhney, M. (2024). *Hitting time mixing for the random transposition walk* (arXiv:2410.23944v1). arXiv. <https://arxiv.org/abs/2410.23944v1>

Jain, V., & Nestoridi, E. (2026). *Hitting-time mixing for the star transposition shuffle* (arXiv:2608.13727v1). arXiv. <https://arxiv.org/abs/2608.13727v1>

Francis, P. E., & Nestoridi, E. (2026). *Limit profiles for separation distance* (arXiv:2605.19084v1). arXiv. <https://arxiv.org/abs/2605.19084v1>

## Project context

Evidence Press. (2026, September 8). *Biased shuffles still cut off* [Candidate research release, version 1.0.0-candidate]. https://evidencepress.org/releases/bounded-product-transposition-cutoff/
