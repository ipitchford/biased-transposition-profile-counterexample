# Find the sharp transition for biased shuffles

**This would be my first choice for a direct mathematical collaboration.**

Your latest transposition release claims cutoff for arbitrary bounded product weights, with an \(O(n\log\log n)\) window, but leaves the transition location and optimal window unresolved. Nestoridi and Yan obtain a sharper result for two equally sized weight classes. There is therefore a concrete gap to investigate between generality and precision. ([Evidence Press][1])

The question I would attack is:

> Does the disappearance of untouched labels essentially determine when an arbitrarily biased deck becomes mixed?

There is an explicit conjecture we could begin testing. Keep the release’s discrete-time convention: choose two labels independently with probabilities \(p_i\), and count choosing the same label twice as an identity step. Label \(i\) participates in a nonidentity swap with probability \(2p_i(1-p_i)\). Consequently,

$$
U_n(t)=\sum_{i=1}^{n}\bigl[1-2p_i(1-p_i)\bigr]^t
$$

is the expected number of labels that have never participated in such a swap after \(t\) steps. Define \(t_*\) by the real interpolation \(U_n(t_*)=1\).

**A conjecture to investigate—not a result I am asserting—is**

$$
t_{\mathrm{mix}}(\varepsilon)
=
t_*+O_{c,C,\varepsilon}(n),
\qquad
\frac cn\le p_i\le\frac Cn.
$$

That would locate the transition to within an order-\(n\) error and improve the current window bound.

The interesting cases would include a shrinking proportion of unusually slow labels, several competing slow classes, and arrays whose weight distributions never converge. I would use exact small-state calculations to expose overlooked mechanisms, then investigate growing families that could genuinely disprove the asymptotic claim. The substantial proof obligation is an upper bound showing that other sources of non-randomness disappear sufficiently close to \(t_*\).

**Sanity check:** when \(p_i=1/n\),

$$
t_*=
\frac{\log n}{-\log(1-2/n+2/n^2)}
\sim \frac n2\log n,
$$

which recovers the classical leading-order location. That checks the normalisation; it does not establish the conjecture. ([arXiv][2])

This project would exercise mathematical discovery, computation and proof criticism together. Even a counterexample could be valuable if it identified a second mechanism that a sharp theorem must capture.


[1]: https://evidencepress.org/releases/bounded-product-transposition-cutoff/ "Biased shuffles still cut off · Evidence Press"
