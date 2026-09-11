---
title: "Where the biased transposition shuffle mixes: the untouched-label conjecture examined"
author: "Prepared for Ian Pitchford, Evidence Press"
date: "10 September 2026"
geometry: margin=2.4cm
fontsize: 11pt
---

# Summary

The question posed was whether the disappearance of untouched labels determines when an arbitrarily biased deck becomes mixed; concretely, whether the total-variation mixing time of the product-weight transposition walk satisfies $t_{\mathrm{mix}}(\varepsilon)=t_*+O_{c,C,\varepsilon}(n)$, where $t_*$ solves $U_n(t_*)=1$ and $U_n(t)=\sum_i[1-2p_i(1-p_i)]^t$ is the expected number of untouched labels.

The outcome is a split verdict, with one half settled and the other half sharpened rather than closed. The lower half of the conjecture, $t_{\mathrm{mix}}(\varepsilon)\ge t_*-O(n)$, is proved below for every bounded array, with an explicit constant (Theorem 1); it needs nothing beyond a second-moment bound on the untouched count, and it is the easy half. The upper half, $t_{\mathrm{mix}}(\varepsilon)\le t_*+O(n)$, is proved in the literature only for two equally sized weight classes (Nestoridi and Yan, 2024), and I have not proved it in general. What I can add is a structural result that explains why it is hard and constrains any future proof: the $L^2$ (chi-square) distance, which is the engine behind every sharp transposition result from Diaconis and Shahshahani onwards, provably does not reach its cutoff at $t_*+O(n)$ unless the slowest labels form a macroscopic fraction of the deck (Theorem 3). In the natural example of a slow class of size $n^{\alpha}$ the chi-square cutoff lags $t_*$ by order $n\log n$, and for an array whose weights spread continuously over $[c/n,C/n]$ the lag is of order $n\log\log n$, the same order as the window in the Evidence Press release. So the conjecture, if true, asserts a genuine separation between total-variation and $L^2$ mixing, and it cannot be proved by spectral or chi-square methods alone. A complete general bound of the right order, $t_{\mathrm{mix}}(\varepsilon)\le \frac{n}{2c^2}(\log n+O_\varepsilon(1))$, follows from a one-line convolution argument (Theorem 4); it is off from $t_*$ by a factor of at most $1/c$ and is, as far as I can tell, the first explicit constant for general bounded arrays.

Exact computation of the walk on $S_n$ for $n\le 10$ and Monte Carlo at $n=2000$ found no mechanism other than untouched labels, but they did find that the conjecture as phrased misidentifies the statistic. What governs the transition is not the number of fixed points but the number of fixed points *within each weight class*; from $t_*$ onward the exact total-variation distance is reproduced to three or four decimal places by the joint law of the class-refined fixed-point counts, whereas the total count alone misses between a third and a half of it. This has a consequence for the two-class model: the limiting profile conjectured by Nestoridi and Yan (their Conjecture 1.6), $d_{\mathrm{TV}}(\mathrm{Poi}(1+e^{c}/2),\mathrm{Poi}(1))$, is strictly smaller than the class-refined lower bound $d_{\mathrm{TV}}(\mathrm{Poi}(\tfrac12+e^{c}/2),\mathrm{Poi}(\tfrac12))$ for every $c$, and so cannot be the limit profile provided the class-refined fixed-point counts have the joint Poisson limit that their own Theorem 1.3 gives for the total (Proposition 5). The corrected general conjecture is stated as Conjecture 6.

All statements labelled theorem or proposition below are proved in full; the two places where I rely on something I have not verified line by line (the Diaconis–Shahshahani constant in Theorem 4, and the joint Poisson limit in Proposition 5) are flagged where they occur. Every numerical claim was produced by code written for this note and cross-checked against an independent computation, as recorded in Section 9.

# 1. Setting and notation

Fix $n$ and a probability vector $p=(p_1,\dots,p_n)$ with $c/n\le p_i\le C/n$ for constants $0<c\le C<\infty$. One step of the walk draws two labels $i,j$ independently from $p$ and replaces the current permutation $\sigma$ by $\sigma\circ(i\,j)$ when $i\ne j$, leaving it unchanged when $i=j$. This is the discrete-time convention of the release: the step measure $\mu$ on $S_n$ gives mass $2p_ip_j$ to each transposition $(i\,j)$ and mass $q:=\sum_ip_i^2$ to the identity. Since $\mu$ is symmetric, the law of $\sigma_t$ started from the identity is the convolution power $\mu_t:=\mu^{*t}$, and because the walk lives on a group the distance $d(t):=\|\mu_t-U\|_{\mathrm{TV}}$ from the uniform measure $U$ does not depend on the starting point. Write $t_{\mathrm{mix}}(\varepsilon)=\min\{t:d(t)\le\varepsilon\}$.

Label $i$ takes part in a non-identity swap at a given step with probability $2p_i(1-p_i)$, so $q_i:=1-2p_i(1-p_i)$ is the probability that it survives a step untouched, $U(t)=\sum_iq_i^t$ is the expected number of untouched labels after $t$ steps, and $t_*$ is the real root of $U(t_*)=1$. Two further quantities recur. The *label chain* is the Markov chain on $[n]$ followed by the position of a single label; its kernel is $Q_{jk}=2p_jp_k$ for $k\ne j$ and $Q_{jj}=1-2p_j+2p_j^2$, which can be written $Q=I-L$ with $L=\mathrm{diag}(2p_i)-2pp^{\mathsf T}$. Because $\sigma_t(i)=\tau_1\circ\cdots\circ\tau_t(i)$ for independent identically distributed transpositions $\tau_s$, the position of label $i$ at time $t$ has exactly the law $Q^t(i,\cdot)$; in particular $\mathbb P(\sigma_t(i)=i)=(Q^t)_{ii}$. The chi-square distance is $\chi^2(t):=n!\sum_\sigma\mu_t(\sigma)^2-1$, and $d(t)\le\frac12\sqrt{\chi^2(t)}$.

The release proves that for every such triangular array the walk has total-variation cutoff at a time of order $n\log n$ with window $O_{c,C,\varepsilon}(n\log\log n)$, and states as its first open problem the determination of the cutoff location. Nestoridi and Yan (2024) treat the case of $N=2n$ cards split into two classes of size $n$ with weights $a/N$ and $b/N$, $0<b\le a$, $a+b=2$, and prove cutoff at $t_N=\frac{1}{2b}N\log N$ with window $N$. In the present notation their slow class has $q_i=1-2b/N+2b^2/N^2$, so $U(t)=\tfrac N2(1-2b/N+\dots)^t+\tfrac N2(1-2a/N+\dots)^t$ and one checks that $t_*=\frac{N}{2b}(\log N-\log2)+o(N)$; their theorem is therefore exactly the statement $t_{\mathrm{mix}}(\varepsilon)=t_*+O(N)$ for that family.

# 2. The lower bound (proved in general)

**Theorem 1.** Suppose $n\ge4C$, so that $p_i+p_j\le\tfrac12$ for all $i,j$. Then for every $t\ge0$,
$$d(t)\;\ge\;1-\frac{6}{U(t)}.$$
Consequently, writing $\rho_{\min}:=\min_i(-\log q_i)$, for every $\varepsilon\in(0,1)$
$$t_{\mathrm{mix}}(\varepsilon)\;\ge\;t_*-\frac{\log\big(7/(1-\varepsilon)\big)}{\rho_{\min}}\;\ge\;t_*-\frac{n}{2c(1-C/n)}\log\frac{7}{1-\varepsilon}.$$

*Proof.* Let $\mathbf 1_i$ be the indicator that label $i$ is untouched after $t$ steps and $A_t=\sum_i\mathbf 1_i$, so $\mathbb E A_t=U(t)$. For $i\ne j$, at a single step the probability that neither label is swapped is $1-2p_i(1-p_i)-2p_j(1-p_j)+2p_ip_j$, because the events "$i$ swapped" and "$j$ swapped" intersect exactly in the draws $(i,j)$ and $(j,i)$. Comparing with the product $q_iq_j$ gives
$$\mathbb P(\text{neither swapped})-q_iq_j=2p_ip_j\big[1-2(1-p_i)(1-p_j)\big]\le0$$
whenever $(1-p_i)(1-p_j)\ge\tfrac12$, which holds under $p_i+p_j\le\tfrac12$. Steps are independent, so $\mathbb E[\mathbf 1_i\mathbf 1_j]\le q_i^tq_j^t=\mathbb E\mathbf 1_i\,\mathbb E\mathbf 1_j$: the untouched indicators are pairwise negatively correlated and $\operatorname{Var}A_t\le\mathbb EA_t=U(t)$. An untouched label is a fixed point of $\sigma_t$, so $\mathrm{Fix}(\sigma_t)\ge A_t$. By Chebyshev, $\mathbb P(A_t\le U/2)\le\operatorname{Var}A_t/(U/2)^2\le4/U$, whereas under the uniform measure the expected number of fixed points is $1$ and Markov gives $U\{\mathrm{Fix}>U/2\}\le2/U$. Hence $d(t)\ge\mathbb P(\mathrm{Fix}(\sigma_t)>U/2)-U\{\mathrm{Fix}>U/2\}\ge1-4/U-2/U$.

For the second statement, $U$ is decreasing and $U(t_*-s)=\sum_iq_i^{t_*}q_i^{-s}\ge(\max_iq_i)^{-s}\,U(t_*)=e^{\rho_{\min}s}$. With $s=\log(7/(1-\varepsilon))/\rho_{\min}$ every integer $t\le t_*-s$ has $U(t)\ge7/(1-\varepsilon)$ and therefore $d(t)\ge1-\tfrac67(1-\varepsilon)>\varepsilon$, so $t_{\mathrm{mix}}(\varepsilon)>t$. Finally $\rho_{\min}\ge2p_{\min}(1-p_{\min})\ge\frac{2c}{n}(1-\frac Cn)$. $\square$

The constant can be improved by Poissonising ($A_t$ is asymptotically Poisson with mean $U(t)$, so $d(t)\ge d_{\mathrm{TV}}(\mathrm{Poi}(1+U(t)),\mathrm{Poi}(1))-o(1)$), but the point of the theorem is that the lower half of the conjecture holds uniformly over all bounded arrays, including arrays whose weight distribution never converges, with no structure assumed beyond $c/n\le p_i\le C/n$. Nothing in the proof used the two-sided bound except to control $\rho_{\min}$.

# 3. The two-class spectrum for arbitrary class sizes

Nestoridi and Yan diagonalise their transition operator for two classes of equal size. The diagonalisation is in fact available for any class sizes, and the mechanism is worth stating because it is exactly what fails with three or more distinct weights.

**Theorem 2.** Let $[n]=A\sqcup B$ with $|A|=m$, $|B|=n-m$, $p_i=\alpha/n$ on $A$ and $p_i=\beta/n$ on $B$ (so $m\alpha+(n-m)\beta=n$), and let $T_X=\sum_{i<j,\;i,j\in X}(i\,j)$ in the group algebra $\mathbb C[S_n]$. Then the step measure is
$$\mu\;=\;q\,e+\frac{2}{n^2}\Big[(\alpha^2-\alpha\beta)\,T_A+(\beta^2-\alpha\beta)\,T_B+\alpha\beta\,T_{[n]}\Big],\qquad q=\frac{m\alpha^2+(n-m)\beta^2}{n^2},$$
and the three elements $T_A,T_B,T_{[n]}$ commute pairwise. Consequently the transition operator of the walk on $L^2(S_n)$ has eigenvalues
$$\theta(\lambda;\mu,\nu)\;=\;q+\frac{2}{n^2}\Big[(\alpha^2-\alpha\beta)\,\mathrm{ct}(\mu)+(\beta^2-\alpha\beta)\,\mathrm{ct}(\nu)+\alpha\beta\,\mathrm{ct}(\lambda)\Big]$$
indexed by partitions $\lambda\vdash n$, $\mu\vdash m$, $\nu\vdash n-m$, with multiplicity $f^\lambda f^\mu f^\nu c^\lambda_{\mu\nu}$, where $\mathrm{ct}$ is the sum of contents, $f$ the number of standard Young tableaux and $c^\lambda_{\mu\nu}$ the Littlewood–Richardson coefficient. In particular $\chi^2(t)=\sum_{(\lambda;\mu,\nu)}f^\lambda f^\mu f^\nu c^\lambda_{\mu\nu}\,\theta(\lambda;\mu,\nu)^{2t}-1$.

*Proof.* The coefficient of a transposition inside $A$ in the bracket is $(\alpha^2-\alpha\beta)+\alpha\beta=\alpha^2$, inside $B$ it is $\beta^2$, and across it is $\alpha\beta$; multiplied by $2/n^2$ these are the required masses $2p_ip_j$. $T_{[n]}$ is central in $\mathbb C[S_n]$, so it commutes with everything; $T_A$ and $T_B$ have disjoint supports and commute with each other. Under the restriction to $S_A\times S_B$ the irreducible $V_\lambda$ decomposes as $\bigoplus_{\mu,\nu}c^\lambda_{\mu\nu}\,V_\mu\otimes V_\nu$, and on each summand $T_A$ acts as the scalar $\mathrm{ct}(\mu)$ and $T_B$ as $\mathrm{ct}(\nu)$ (the classical evaluation of the class sum of transpositions), while $T_{[n]}$ acts on all of $V_\lambda$ as $\mathrm{ct}(\lambda)$. The three commuting operators are therefore simultaneously diagonal on this decomposition, and the multiplicity follows from $L^2(S_n)\cong\bigoplus_\lambda V_\lambda^{\oplus f^\lambda}$. $\square$

For equal sizes this is Theorem 1.2 of Nestoridi and Yan; the derivation above is the same and makes no use of $m=n/2$. I verified the formula against a brute-force eigendecomposition of the $720\times720$ transition matrix for $n=6$, $m=2$ (agreement to $4\times10^{-15}$), and against the exact chi-square distance computed by iterating the walk on all $9!$ permutations for $n=9$ with $m=4$ and $m=3$ (agreement to all printed digits at $t=5,10,20$). Two remarks. First, the block $\lambda=(n-1,1)$, $\mu=(m)$, $\nu=(n-m-1,1)$ has eigenvalue exactly $1-2\beta/n$ and multiplicity $(n-1)(n-m-1)$, which is the slow eigenspace discussed next. Second, the construction breaks with three classes $A_1,A_2,A_3$: the cross terms $T_{A_k\cup A_l}$ are central only in $\mathbb C[S_{A_k\cup A_l}]$ and $T_{A_1\cup A_2}$ does not commute with $T_{A_2\cup A_3}$ (already for singleton classes, $(1\,2)$ and $(2\,3)$ do not commute), so there is no simultaneous diagonalisation and no explicit spectrum. This is the precise sense in which general bounded arrays are harder than two classes.

# 4. The $L^2$ obstruction

**Theorem 3.** Let $0=\lambda_1\le\lambda_2\le\dots\le\lambda_n$ be the eigenvalues of $L=\mathrm{diag}(2p_i)-2pp^{\mathsf T}$ and $p_{(1)}\le\dots\le p_{(n)}$ the ordered weights. For every array (no boundedness needed) and every $t$,
$$\chi^2(t)\;\ge\;(n-1)\sum_{k=2}^{n}(1-\lambda_k)^{2t}\;\ge\;(n-1)\sum_{k=2}^{n}\big(1-2p_{(k)}\big)^{2t}.$$
If the minimal weight $p_{\min}$ is carried by $m\ge2$ labels then also $\chi^2(t)\ge(n-1)(m-1)(1-2p_{\min})^{2t}$.

*Proof.* By Plancherel on $S_n$, $n!\sum_\sigma\mu_t(\sigma)^2=\sum_\rho d_\rho\operatorname{Tr}\big(\hat\mu(\rho)^{2t}\big)$, the sum running over irreducible unitary representations, and $\hat\mu(\rho)$ is Hermitian because $\mu$ is symmetric. All terms are non-negative, so dropping every representation except the standard one $\rho=(n-1,1)$ gives $\chi^2(t)\ge(n-1)\operatorname{Tr}(\hat\mu(\mathrm{std})^{2t})$. The permutation representation of $S_n$ on $\mathbb C^n$ is $\mathrm{triv}\oplus\mathrm{std}$, and $\hat\mu$ evaluated on it is the matrix with $(j,k)$ entry $\mu\{\tau:\tau(k)=j\}=Q_{kj}$, i.e. the symmetric label-chain kernel $Q=I-L$; so the eigenvalues of $\hat\mu(\mathrm{std})$ are $1-\lambda_k$, $k\ge2$. For the second inequality, $L$ is the diagonal matrix $\mathrm{diag}(2p_i)$ minus the positive semidefinite rank-one matrix $2pp^{\mathsf T}$, and Weyl interlacing for a rank-one perturbation gives $\lambda_k\le2p_{(k)}$ for every $k$. For the last statement, any vector supported on the minimal class with zero sum is an eigenvector of $L$ with eigenvalue $2p_{\min}$, giving an $(m-1)$-dimensional eigenspace. $\square$

The standard-representation contribution is the chi-square mass carried by the *linear statistics* $F(\sigma)=\sum_ia_i\varphi(\sigma(i))$, and its dominant part comes from $a$ supported on the slowest labels. What the theorem says is that the walk cannot be $L^2$-close to uniform until $(n-1)(m-1)(1-2p_{\min})^{2t}$ is small, i.e. until
$$t\;\ge\;t_\chi:=\frac{\log\big((n-1)(m-1)\big)}{-2\log(1-2p_{\min})}\;=\;\frac{n}{4c_{\min}}\big(\log n+\log m\big)\,(1+O(1/n)),\qquad c_{\min}:=np_{\min}.$$
Compare this with $t_*$, which never exceeds $\frac{n}{2c_{\min}}\log n\,(1+O(1/n))$ and, when the slowest class dominates $U$, equals $\frac{n}{2c_{\min}}\log m+O(n)$. The two agree to within $O(n)$ precisely when $\log(n/m)=O(1)$, that is, when the slowest labels are a positive fraction of the deck. Two examples make the gap concrete; both were checked numerically for $n$ from $10^3$ to $10^6$ using the interlacing form of the bound, and the increments per decade of $n$ matched the predicted $\frac{1}{4c}\log(n/m)$ and $\frac1{4c}\log\log n$ growth to two digits.

*A small slow class.* Take $m=n^{\alpha}$ labels of weight $c/n$ and the rest of weight about $1/n$, with $\alpha>c$ so that the slow class dominates $U$ at $t_*$. Then $t_*=\frac{\alpha n}{2c}\log n+O(n)$ while $t_\chi\ge\frac{(1+\alpha)n}{4c}\log n-O(n)$, a gap of $\frac{(1-\alpha)n}{4c}\log n$. With two slow labels only ($m=2$) and $c<\tfrac12$ the same computation gives $t_\chi\ge\frac{n}{4c}\log n$ against $t_*=\frac n2\log n+O(n)$: even two slow labels push the chi-square cutoff later than $t_*$ by order $n\log n$, although they cannot delay total-variation mixing by more than the vanishing amount $n^{-c}$ their untouched probability contributes.

*A continuum of weights.* Take $p_i=\big(c+(C-c)\tfrac{i-1}{n-1}\big)/n$, which sums to one when $c+C=2$ (for instance $c=\tfrac12$, $C=\tfrac32$). Then the geometric sum in $U$ gives $U(t)\approx e^{-2ct/n}\,\frac{n^2}{2(C-c)t}$, whence
$$t_*=\frac{n}{2c}\Big(\log n-\log\log n-\log\tfrac{C-c}{c}+O\big(\tfrac{\log\log n}{\log n}\big)\Big),$$
an effective slow class of size $n/\log n$ (the correction term is what makes the constant converge slowly: at $n=10^6$ it is still $0.25$ away from its limit, exactly as the expansion predicts); and the theorem gives $\chi^2(t_*+Kn)\ge e^{-4cK}\,\frac{C-c}{2c}\log n\,(1+o(1))$, so that $t_\chi=t_*+\frac{n}{4c}\log\log n+O(n)$. The chi-square window in this example is of order $n\log\log n$, the same order as the total-variation window bound in the release. I note this as suggestive only: the release's argument is entropic rather than spectral, and I have not analysed whether its window is tight for total variation.

Three consequences follow. Any proof of $t_{\mathrm{mix}}(\varepsilon)\le t_*+O(n)$ for general bounded arrays must be a genuinely total-variation argument; the Diaconis–Shahshahani route, and the Nestoridi–Yan route which is its two-class descendant, cannot work when the slowest class is $o(n)$, because the quantity they bound is not small at the conjectured time. Conversely, in two-class families with both classes of size proportional to $n$ the chi-square distance *is* small at $t_*+O(n)$ (numerically and, for equal classes, by Nestoridi–Yan), so extending their spectral estimate from $m=n/2$ to $m=\gamma n$ using Theorem 2 is a well-posed finite task and is the natural next rigorous step. And the conjecture, if true, is a statement about a walk whose total-variation cutoff strictly precedes its $L^2$ cutoff, which is an unusual and interesting phenomenon for random walks on groups.

# 5. A general upper bound of the right order

**Theorem 4.** Let $\theta:=n^2p_{\min}^2\ge c^2$ and let $d_u(k)$ be the total-variation distance after $k$ steps of the uniform walk ($p_i\equiv1/n$). Then for every $t$,
$$d(t)\;\le\;\mathbb E\big[d_u(B_t)\big],\qquad B_t\sim\mathrm{Bin}(t,\theta).$$
Consequently $t_{\mathrm{mix}}(\varepsilon)\le\frac{1}{\theta}\,t^{u}_{\mathrm{mix}}(\varepsilon/2)+O\big(\sqrt{n\log n\cdot\log(1/\varepsilon)}\big)$, and with the Diaconis–Shahshahani bound $d_u\big(\tfrac n2(\log n+K)\big)\le a e^{-2K}$ for a universal constant $a$ this reads
$$t_{\mathrm{mix}}(\varepsilon)\;\le\;\frac{n}{2c^2}\Big(\log n+\tfrac12\log\frac{2a}{\varepsilon}\Big)+o(n).$$

*Proof.* The uniform step measure $\mu_u$ has mass $2/n^2$ on each transposition and $1/n$ on the identity, so $\mu\ge\theta\mu_u$ pointwise and $\mu=\theta\mu_u+(1-\theta)\mu'$ for a probability measure $\mu'$. Realise each step by an independent coin of bias $\theta$ choosing between a $\mu_u$-step and a $\mu'$-step. Conditional on the coin sequence with $k$ heads, $\sigma_t$ is a product of alternating blocks $A_1\tau_1A_2\tau_2\cdots$ where the $A_r$ are independent products of $\mu'$-steps and the $\tau_r$ are independent $\mu_u$-steps. Because $\mu_u$ is a class function it is central in the convolution algebra, $\mu_u*\nu=\nu*\mu_u$ for every $\nu$, so the conditional law of $\sigma_t$ is $\nu*\mu_u^{*k}$ with $\nu=\mathcal L(A_1)*\mathcal L(A_2)*\cdots$. Convolution contracts total variation and fixes $U$, so $\|\nu*\mu_u^{*k}-U\|_{\mathrm{TV}}=\|\nu*(\mu_u^{*k}-U)\|_{\mathrm{TV}}\le d_u(k)$. Averaging over the coins gives the first claim. For the second, $B_t$ has mean $\theta t$ and standard deviation at most $\sqrt{t}$, so choosing $t$ with $\theta t\ge t^u_{\mathrm{mix}}(\varepsilon/2)+\sqrt{2t\log(2/\varepsilon)}$ makes $\mathbb P(B_t<t^u_{\mathrm{mix}}(\varepsilon/2))\le\varepsilon/2$ by Hoeffding. $\square$

The Diaconis–Shahshahani constant $a$ and exponent $e^{-2K}$ are quoted from the statement of their 1981 Theorem 1 as I recall it and have not been re-derived or re-checked against the paper here; the structure of the argument does not depend on them, only the final constant does. The bound is crude in one specific way: it extracts from each step only the uniform-transposition mass $c^2$ that every pair $(i,j)$ is guaranteed to carry. When all weights equal $c/n$ (so $c=1$) it is sharp, and in general it locates the transition within a factor $1/c$ of $t_*$. I could not find a way to extract more: the only central measures available are conjugacy-class sums, and the mass of two-step or three-step class functions inside $\mu^{*2}$ or $\mu^{*3}$ is smaller still. The commutation trick is also why the argument cannot be localised to a subset of labels: uniform transpositions on a subset $B$ are central in $\mathbb C[S_B]$ but not in $\mathbb C[S_n]$.

# 6. What the exact computations show: fixed points must be counted by class

The walk was iterated exactly on all of $S_n$ for $n=8,9,10$ (up to $3\,628\,800$ states), for eight weight families chosen to cover the cases named in the brief: the uniform control; two equal classes at $b=0.5$ and at $b=0.25$; two slow labels among fast ones; three slow labels; two competing slow classes ($0.5$ and $0.6$ against $1.5$); a continuum of weights from $0.5$ to $1.5$; and one very fast label (weight $3$ against $1$). For each, $d(t)$, $\chi^2(t)$ and the total-variation distance of several projections of $\mu_t$ were computed for all $t$ up to $110$.

The first table records the transition location. The column $(t_{\mathrm{mix}}(0.1)-t_*)/n$ is the quantity the conjecture asserts is bounded; at these sizes it is stable in $n$ within each family and grows as $1/c$ shrinks, as the untouched-label picture predicts (with $U_{\mathrm{slow}}(t_*+Kn)\approx e^{-2cK}$, the class-refined Poisson profile of Section 6.2 predicts $K\approx1.7$ for the family at $b=0.5$ and $K\approx3.4$ at $b=0.25$; the observed values are $1.3$–$1.5$ and $2.9$–$3.3$). Nothing at $n\le10$ can confirm an asymptotic statement, and these numbers are reported as consistency checks, not evidence.

| family | $n$ | $t_*$ | $t_{\mathrm{mix}}(0.25)$ | $t_{\mathrm{mix}}(0.1)$ | $t_{\mathrm{mix}}(0.05)$ | $(t_{\mathrm{mix}}(0.1)-t_*)/n$ |
|---|---|---|---|---|---|---|
| uniform | 8 / 9 / 10 | 8.42 / 9.98 / 11.60 | 8.2 / 9.8 / 11.6 | 11.5 / 13.6 / 15.8 | 13.9 / 16.4 / 19.0 | 0.38 / 0.40 / 0.42 |
| two equal classes, $b=0.5$ | 8 / 9 / 10 | 11.61 / 13.87 / 16.52 | 14.6 / 18.2 / 20.8 | 22.1 / 27.1 / 30.4 | 27.4 / 33.5 / 37.2 | 1.31 / 1.47 / 1.39 |
| two equal classes, $b=0.25$ | 8 / 9 / 10 | 22.20 / 27.05 / 32.20 | 29.9 / 38.0 / 42.2 | 45.4 / 56.9 / 62.1 | 56.4 / 70.4 / 76.2 | 2.90 / 3.31 / 2.99 |
| two slow labels ($0.5$) | 8 / 9 / 10 | 9.16 / 10.84 / 12.57 | 10.6 / 12.6 / 14.6 | 16.5 / 19.4 / 22.3 | 20.8 / 24.4 / 28.0 | 0.92 / 0.95 / 0.97 |
| three slow labels ($0.5$ vs $1.5$) | 8 / 9 / 10 | 11.18 / 13.22 / 15.30 | 15.5 / 18.8 / 22.2 | 23.6 / 28.3 / 33.1 | 29.4 / 35.2 / 41.1 | 1.55 / 1.68 / 1.78 |
| two competing slow classes | 8 / 9 / 10 | 10.50 / 13.02 / 15.56 | 11.3 / 14.7 / 18.3 | 16.8 / 21.7 / 26.7 | 20.8 / 26.7 / 32.7 | 0.79 / 0.96 / 1.11 |
| continuum $0.5\to1.5$ | 8 / 9 / 10 | 9.55 / 11.36 / 13.25 | 11.1 / 13.3 / 15.7 | 17.0 / 20.1 / 23.3 | 21.6 / 25.2 / 29.0 | 0.94 / 0.97 / 1.01 |
| one very fast label | 8 / 9 / 10 | 9.83 / 11.53 / 13.26 | 9.9 / 11.8 / 13.6 | 14.2 / 16.5 / 18.8 | 17.5 / 20.1 / 22.8 | 0.55 / 0.55 / 0.55 |

Mixing times are the linear interpolations of the first crossing of $\varepsilon$.

## 6.1 Where the total-variation mass sits

The more informative computation projects $\mu_t$ onto coarser statistics and asks how much of $d(t)$ each projection retains. The next table, for $n=9$ and two equal classes at $b=0.5$, is representative of every biased family. From roughly $t_*$ onward the pair (number of fixed points among slow labels, number among fast labels) reproduces $d(t)$ to four decimal places; the total number of fixed points, which is the statistic in the conjecture and in Nestoridi–Yan's Theorem 1.3, retains only between $55$ and $75$ per cent of it, the fraction falling as $t$ grows; the full cycle type, which contains the total fixed-point count but not the class information, does no better than the total. For the uniform walk, by contrast, the total count and the full distance differ by less than $0.01$ from $t=6$ onward, as one expects from Teyssier's limit profile.

| $t$ | $d(t)$ | pair $(\mathrm{Fix}_{\mathrm{slow}},\mathrm{Fix}_{\mathrm{fast}})$ | total $\mathrm{Fix}$ | cycle type | $\chi^2(t)$ | $U(t)$ |
|---|---|---|---|---|---|---|
| 10 | 0.5001 | 0.4938 | 0.4373 | 0.4373 | 5.65 | 1.63 |
| 12 | 0.4304 | 0.4301 | 0.3452 | 0.3452 | 2.77 | 1.26 |
| 14 | 0.3669 | 0.3669 | 0.2720 | 0.2720 | 1.49 | 0.98 |
| 16 | 0.3081 | 0.3081 | 0.2145 | 0.2145 | 0.86 | 0.78 |
| 20 | 0.2101 | 0.2101 | 0.1339 | 0.1339 | 0.31 | 0.50 |
| 30 | 0.0731 | 0.0731 | 0.0421 | 0.0421 | 0.03 | 0.17 |
| 40 | 0.0242 | 0.0242 | 0.0135 | 0.0135 | 0.003 | 0.06 |

($n=9$, $t_*=13.87$; the projections are exact total-variation distances between the push-forwards of $\mu_t$ and of $U$.)

For the three-class and continuum families the analogous statement holds with the counts refined by weight class (for the continuum, every class is a singleton, so the statistic is the set of fixed points itself): the projection retains $98.5$–$99.5\%$ of $d(t)$ from $t_*$ onward, the residual of about one per cent being attributable at these sizes to short cycles among slow labels, an effect whose expected size scales like $(\log m)/n$ and is invisible at $n=2000$ (Section 7). I found no other statistic carrying total-variation mass.

Why the refinement matters is easy to see in the limit. Under the uniform measure the fixed-point counts of the slow and fast classes are asymptotically independent Poisson variables with means $m/n$ and $(n-m)/n$. Under the walk, the untouched slow labels add an independent Poisson$(U_{\mathrm{slow}}(t))$ to the slow count only. The class-refined test is therefore a Poisson$(\tfrac mn+U_{\mathrm{slow}})$ against Poisson$(\tfrac mn)$ comparison, whereas the total count dilutes the same signal in Poisson$(1)$ noise; and $d_{\mathrm{TV}}(\mathrm{Poi}(\lambda+x),\mathrm{Poi}(\lambda))$ is decreasing in $\lambda$ for every $x>0$ (I verified this numerically on a fine grid; it is the statement that added independent noise cannot help a test). When the slow class is small the difference is dramatic: at $n=2000$ with $45$ slow labels the pair statistic gives $0.46$ at $t_*$ where the total gives $0.33$.

## 6.2 Consequence for the two-class limit profile

**Proposition 5.** In the Nestoridi–Yan model ($N=2n$ cards, equal classes, $b<1$), at $t=\frac{N}{2b}(\log N-c)$:

(i) $\mathbb E[\mathrm{Fix}_{\mathrm{slow}}]=\sum_{i\in\mathrm{slow}}(Q^t)_{ii}$ exactly, and the untouched slow count $A^{\mathrm{slow}}_t$ has mean $\tfrac N2 q_{\mathrm{slow}}^t\to e^{c}/2$ and variance at most its mean, while the untouched fast count has mean $\tfrac N2q_{\mathrm{fast}}^t\to0$.

(ii) If $(\mathrm{Fix}_{\mathrm{slow}},\mathrm{Fix}_{\mathrm{fast}})$ converges in law to $\mathrm{Poi}(\tfrac12+e^c/2)\otimes\mathrm{Poi}(\tfrac12)$, then
$$\liminf_{N\to\infty}d(t)\;\ge\;d_{\mathrm{TV}}\big(\mathrm{Poi}(\tfrac12+e^c/2),\mathrm{Poi}(\tfrac12)\big)\;>\;d_{\mathrm{TV}}\big(\mathrm{Poi}(1+e^c/2),\mathrm{Poi}(1)\big)$$
for every real $c$, so that Conjecture 1.6 of Nestoridi and Yan cannot hold.

*Proof.* (i) is the one-particle identity of Section 1 together with the variance bound of Theorem 1. For (ii), the pair is a function of $\sigma_t$, and under $U$ it converges to $\mathrm{Poi}(\tfrac12)\otimes\mathrm{Poi}(\tfrac12)$ (a classical consequence of inclusion–exclusion for fixed points of a uniform permutation restricted to a set of $n$ labels out of $2n$). Total variation can only decrease under push-forward, and the fast coordinate has the same law on both sides and is independent of the slow one in the limit, so it contributes nothing; the first inequality follows. The second is the monotonicity in $\lambda$ noted above, numerically confirmed for the relevant range and strict throughout it (for $c=0$: $0.239$ against $0.178$; for $c=1$: $0.464$ against $0.418$; for $c=-1$: $0.102$ against $0.067$). $\square$

The hypothesis in (ii) is the class-refined form of Nestoridi–Yan's Theorem 1.3, which proves the Poisson limit $\mathrm{Poi}(1+e^c/2)$ for the total. I have not carried out the refined moment computation and flag this as the one unverified step; it is however exactly the same phenomenon, the exact finite-$n$ law of the pair captures the entire distance for $n\le10$, and at $N=2000$ the empirical law of $\mathrm{Fix}_{\mathrm{slow}}$ is within Monte Carlo error of $\mathrm{Poi}(\tfrac12+U_{\mathrm{slow}}(t))$ at every time tested (Section 7). If the profile exists, the corrected two-class statement is $d\big(\tfrac{N}{2b}(\log N-c)\big)\to d_{\mathrm{TV}}(\mathrm{Poi}(\tfrac12+e^c/2),\mathrm{Poi}(\tfrac12))$.

## 6.3 The corrected general conjecture

The natural general form replaces the fixed-point count by the fixed-point *set*. Under the walk, label $i$ is untouched with probability $q_i^t$, nearly independently across $i$, and a touched label returns home with probability close to $1/n$; under $U$ each label is fixed with probability $1/n$, again nearly independently. This suggests:

**Conjecture 6 (untouched-set profile).** For any triangular array with $c/n\le p_i\le C/n$,
$$\sup_{t\ge0}\Big|\,d(t)-d_{\mathrm{TV}}\Big(\bigotimes_{i=1}^n\mathrm{Ber}\big(q_i^t+(1-q_i^t)/n\big),\ \bigotimes_{i=1}^n\mathrm{Ber}(1/n)\Big)\Big|\;\longrightarrow\;0 .$$

The right-hand distance is at most $\sum_iq_i^t(1-1/n)\le U(t)$, so the conjecture implies $t_{\mathrm{mix}}(\varepsilon)\le t_*+O(n)$; it reduces to Teyssier's profile when all $q_i$ coincide, to the corrected two-class profile above, and it is stated in terms of the array itself, so it makes sense for arrays whose weight distributions never converge. It is the precise form of the statement that the disappearance of untouched labels determines the transition, and it is the statement the exact computations support.

# 7. Search for a second mechanism at $n=2000$

Twenty thousand independent runs of the walk were simulated at $n=2000$ for four arrays, each to the times $t_*+Kn$, $K\in\{-1,0,1,2,3\}$, and compared with twenty thousand uniform permutations. For every run I recorded, by class, the numbers of fixed points and of untouched labels, together with statistics chosen to expose mechanisms other than untouched labels: the number of $2$-cycles, the number of slow labels in $2$-cycles, the number of slow labels sitting at the home position of a *different* slow label, and the number of cycles of length at least two. For each statistic the empirical total-variation distance between walk and uniform was computed; with $R=20\,000$ the noise floor of such an estimate is about $0.01$.

The array with $\sqrt n$ slow labels (weight $0.5/n$ against about $1/n$) is the one where a chi-square proof is impossible (Theorem 3) and where any second mechanism would be least masked by fast-class noise. Its results:

| $K$ | $T$ | $U_{\mathrm{slow}}$ | mean untouched slow | mean $\mathrm{Fix}_{\mathrm{slow}}$ | TV: pair | TV: total Fix | TV: $\mathrm{Fix}_{\mathrm{slow}}$ vs $\mathrm{Poi}(\tfrac mn+U_{\mathrm{slow}})$ | TV: $2$-cycles | slow in $2$-cycles | slow at other slow homes | cycles $\ge2$ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $-1$ | 6504 | 1.741 | 1.731 | 1.749 | 0.876 | 0.830 | 0.013 | 0.007 | 0.009 | 0.040 | 0.014 |
| $0$ | 8504 | 0.641 | 0.627 | 0.647 | 0.460 | 0.333 | 0.009 | 0.002 | 0.002 | 0.019 | 0.015 |
| $1$ | 10504 | 0.236 | 0.233 | 0.255 | 0.202 | 0.104 | 0.004 | 0.007 | 0.001 | 0.008 | 0.012 |
| $2$ | 12504 | 0.087 | 0.087 | 0.106 | 0.078 | 0.035 | 0.003 | 0.003 | 0.001 | 0.011 | 0.010 |

(Uniform reference: mean $\mathrm{Fix}_{\mathrm{slow}}=0.0225=m/n$. Noise floors, measured by comparing two independent uniform samples of the same size, are $0.007$ for the pair and the counts, $0.012$ for "slow at other slow homes" and $0.011$ for the cycle count; wider-support statistics have higher floors.)

The untouched slow count tracks $U_{\mathrm{slow}}(t)$ to within $0.015$, the slow fixed-point count exceeds it by $m/n=0.0225$ as predicted, and its empirical law is indistinguishable from $\mathrm{Poi}(m/n+U_{\mathrm{slow}})$. Of the remaining statistics only one ever rises above its floor, and only before $t_*$: the number of slow labels sitting at other slow labels' homes, at $K=-1$.

For two equal classes at $b=0.5$ ($N=2000$, $t_*=13\,816$) the same run gives a direct test of Section 6.2: the empirical distance of the pair against the class-refined prediction $d_{\mathrm{TV}}(\mathrm{Poi}(\tfrac12+U_{\mathrm{slow}}),\mathrm{Poi}(\tfrac12))$, and of the total count against the Nestoridi–Yan form $d_{\mathrm{TV}}(\mathrm{Poi}(1+U_{\mathrm{slow}}),\mathrm{Poi}(1))$.

| $K$ | $U_{\mathrm{slow}}$ | mean untouched | TV: pair | predicted (refined) | TV: total Fix | predicted (total) | slow at other slow homes | floor |
|---|---|---|---|---|---|---|---|---|
| $-1$ | 2.718 | 2.721 | 0.740 | 0.741 | 0.637 | 0.637 | 0.094 | 0.032 |
| $0$ | 1.000 | 0.977 | 0.368 | 0.383 | 0.321 | 0.330 | 0.044 | 0.032 |
| $1$ | 0.368 | 0.367 | 0.186 | 0.187 | 0.134 | 0.133 | 0.033 | 0.032 |
| $2$ | 0.135 | 0.131 | 0.075 | 0.077 | 0.050 | 0.050 | 0.033 | 0.032 |

Both predictions are met to within Monte Carlo error at every time, and the pair exceeds the total by the margin Proposition 5 requires. The continuum array (with "slow" taken to be the lowest decile) and the array with two competing slow classes behaved in the same way, with the class-refined pair matching the fixed-point mechanism and every other statistic at its floor from $t_*$ onward; their outputs are in the accompanying log.

The one statistic with a real but transient signal deserves a mechanism, because it is precisely the kind of second effect the brief asked to look for. A touched slow label sits where its last partner was, and that partner was drawn from $p$; if the partner was itself a slow label that had not yet moved, the label lands on a slow home. Summing over slow labels and over the law of the last-touch time gives an expected excess of about $\tfrac b4\,e^{-2bK}\log N$ slow labels at other slow homes (partly offset by the untouched labels themselves, which sit at their own homes and are excluded from the count), against a uniform standard deviation of about $\sqrt N/4$; the signal-to-noise ratio is of order $(\log N)/\sqrt N$ up to constants, about $0.1$–$0.2$ at $N=2000$, which is the size of the effect in the table, and it vanishes as $N$ grows. It is the total-variation shadow of the linear statistics that make the chi-square distance large (Section 4): visible in $L^2$, where all $mn$ of them add coherently, but not in total variation, where they are drowned by the fluctuations of the uniform measure. I found no statistic whose signal at $t_*+O(n)$ grows with $n$.

# 8. What remains open, and a route

The upper half of the conjecture remains open for every array other than two equally sized classes. Three approaches are visible, and the results above say something about each.

The spectral approach is closed off in general by Theorem 3, but open and finite for two classes of proportional sizes: Theorem 2 gives the spectrum, the dominant terms are the blocks with $\lambda$, $\mu$, $\nu$ each within one box of a row, and what is required is the analogue of Nestoridi–Yan's bound on the full triple sum with $m=\gamma n$ in place of $m=n/2$. I have not attempted that estimate here; the exact spectral chi-square at $n=20$ (Section 9) behaves as it should.

The strong-stationary-time approach, in the Matthews marking form used by Bernstein, Bhatnagar and Pak for the same two-class model, bounds separation distance, which dominates total variation. Nestoridi and Yan report a gap in that argument. With a small slow class it is not clear that separation cuts off at $t_*+O(n)$ at all, since separation is sensitive to under-represented permutations in the way chi-square is sensitive to over-represented ones; I have not resolved this.

The approach that fits the structure is a burn-in argument: $d(t)\le\|\mu_s-\nu\|_{\mathrm{TV}}+\tfrac12\sqrt{\chi^2(\nu P^{\,t-s})}$ for any auxiliary law $\nu$, with $s=t_*+Kn/2$. The chi-square from $\nu$ of the slow linear statistics is $(1-2p_{\min})^{2(t-s)}$ times $n\sum_{i\,\mathrm{slow}}\|\nu(\sigma(i)\in\cdot)-\tfrac1n\|_2^2$, so what is needed is a $\nu$ within $o(1)$ of $\mu_s$ in total variation under which each slow label's position is uniform to $\ell^2$ precision $o(1/(n\sqrt m))$. The obvious candidate, $\mu_s$ conditioned on every label having been touched, removes the atoms at $\sigma(i)=i$ but I could not show that it meets the precision requirement; the position of a touched slow label is the position its last partner occupied, and that partner is drawn from $p$, not uniformly. Establishing the precision, or a different $\nu$, would prove the conjecture in the two-class case for all class sizes and plausibly in general, since after burn-in only eigenvalues within $O(1/n)$ of one matter and those are governed by the label chain, whose spectrum is explicit for any array.

Independently of the upper bound, the moment computation behind Proposition 5(ii), the joint Poisson limit of the class-refined fixed-point counts, is a concrete and bounded task: the $k$-th factorial moment of $\mathrm{Fix}_{\mathrm{slow}}$ is the return probability of the $k$-particle interchange process started from $k$ slow labels, and for two classes that process lumps, by the $S_A\times S_B$ symmetry, to a finite chain whose state records for each particle whether it is at home, at another particle's home, or elsewhere in class $A$ or $B$.

# 9. What was verified

The rank function used to index permutations was checked to be a bijection onto lexicographic order for $n=5$; the exact one-step distance for $n=7$ agreed with the closed form $\tfrac12\big(|\tfrac1n-\tfrac1{n!}|+\binom n2|\tfrac2{n^2}-\tfrac1{n!}|+(n!-1-\binom n2)/n!\big)$. Murnaghan–Nakayama character tables were checked against orthogonality for $n\le7$, and the Littlewood–Richardson multiplicities from Theorem 2 sum to $n!$; the spectrum from Theorem 2 matched brute-force eigenvalues of the $720\times720$ transition matrix for $n=6$, $m=2$, $\alpha=2$, $\beta=0.5$ to $4\times10^{-15}$, and the spectral $\chi^2(t)$ matched the exact walk for $n=9$ at $m=3$ and $m=4$ to seven digits. The standard-representation bound of Theorem 3 was checked to lie below the exact $\chi^2$ at every time for $n=9$ and, via Theorem 2, for $n=20$ with slow-class sizes $2$ to $18$, where it accounts for between a half and three quarters of $\chi^2(t_*)$. The trivial block of Theorem 2 was checked to have eigenvalue $1$. The pairwise negative correlation in Theorem 1 was checked symbolically and the sign condition $(1-p_i)(1-p_j)\ge\tfrac12$ is the only place $n\ge4C$ is used. The Monte Carlo untouched counts agree with $U(t)$ computed independently from the array. Everything not listed here (the Diaconis–Shahshahani constant; the refined Poisson limit) is quoted, not verified, and is marked as such where it is used.

# Sources

*Primary sources for the model and the conjecture*

Evidence Press. (2026, 8 September). *Biased shuffles still cut off: bounded product-weight random transpositions* (Version 1.0.0-candidate). https://doi.org/10.5281/zenodo.22662125 ; https://evidencepress.org/releases/bounded-product-transposition-cutoff/

Nestoridi, E., & Yan, A. (2024). Cutoff for the biased random transposition shuffle. *arXiv*. https://arxiv.org/abs/2409.16387

Bernstein, M., Bhatnagar, N., & Pak, I. (2017). Cutoff for biased transpositions. *arXiv*. https://arxiv.org/abs/1709.03477

*Classical random transpositions*

Diaconis, P., & Shahshahani, M. (1981). Generating a random permutation with random transpositions. *Zeitschrift für Wahrscheinlichkeitstheorie und verwandte Gebiete, 57*(2), 159–179. https://doi.org/10.1007/BF00535487

Matthews, P. (1988). A strong uniform time for random transpositions. *Journal of Theoretical Probability, 1*(4), 411–423. https://doi.org/10.1007/BF01048728

Teyssier, L. (2020). Limit profile for random transpositions. *The Annals of Probability, 48*(5), 2323–2343. https://doi.org/10.1214/20-AOP1424

*Cutoff methodology cited by the release*

Hermon, J., & Peres, Y. (2018). The power of averaging at two consecutive time steps: Proof of a mixing conjecture by Aldous and Fill. *Annales de l'Institut Henri Poincaré, Probabilités et Statistiques, 54*(4), 2030–2042. https://doi.org/10.1214/16-AIHP782

Pedrotti, F., & Salez, J. (2025). A new cutoff criterion for non-negatively curved chains. *arXiv*. https://arxiv.org/abs/2501.13079

*Computation*

All code (exact iteration on $S_n$, Murnaghan–Nakayama and Littlewood–Richardson tables, spectral chi-square, Monte Carlo) accompanies this note as `biased_transposition_code.zip`; the machine outputs quoted above are in `n8/n9/n10` JSON files, `chi2_n20_be0.5.json` and `mc2000.log`.
