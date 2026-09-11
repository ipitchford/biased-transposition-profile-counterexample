"""Explicit spectrum of the two-class product-weight transposition walk, via commuting central elements.

P = q*e + (2/n^2) [ (al^2 - al*be) T_A + (be^2 - al*be) T_B + al*be T_n ]
where T_X = sum_{i<j in X} (ij), class A has weight al/n (|A| = m), class B weight be/n (|B| = n-m),
q = sum p_i^2 = (m al^2 + (n-m) be^2)/n^2.
Eigenvalue on the (lambda; mu, nu) block:  q + (2/n^2)[(al^2-al be) ct(mu) + (be^2 - al be) ct(nu) + al be ct(lambda)],
multiplicity f^lambda f^mu f^nu c^lambda_{mu nu}.
"""
from functools import lru_cache
from fractions import Fraction
import math, itertools
import numpy as np

def partitions(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0:
        yield ()
        return
    for k in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - k, k):
            yield (k,) + rest

def content_sum(lam):
    return sum(j - i for i, row in enumerate(lam) for j in range(row))

def hook_dim(lam):
    n = sum(lam)
    conj = [sum(1 for r in lam if r > j) for j in range(lam[0])] if lam else []
    h = 1
    for i, row in enumerate(lam):
        for j in range(row):
            h *= (row - j) + (conj[j] - i) - 1
    return math.factorial(n) // h

@lru_cache(maxsize=None)
def mn_char(lam, rho):
    """Murnaghan-Nakayama: character chi^lam at cycle type rho (both tuples, lam a partition)."""
    if not rho:
        return 1 if not lam else 0
    r = rho[0]; rest = rho[1:]
    # represent lam by beta-numbers (first-column hook lengths) to remove border strips of size r
    L = len(lam)
    beta = [lam[i] + (L - 1 - i) for i in range(L)]
    total = 0
    bset = set(beta)
    for b in beta:
        nb = b - r
        if nb >= 0 and nb not in bset:
            # sign = (-1)^{number of beta numbers strictly between nb and b}
            sgn = (-1) ** sum(1 for x in beta if nb < x < b)
            newbeta = sorted([x for x in beta if x != b] + [nb], reverse=True)
            L2 = len(newbeta)
            newlam = tuple(newbeta[i] - (L2 - 1 - i) for i in range(L2))
            newlam = tuple(x for x in newlam if x > 0)
            total += sgn * mn_char(newlam, rest)
    return total

def class_size(rho):
    n = sum(rho)
    denom = 1
    for k in set(rho):
        c = rho.count(k)
        denom *= (k ** c) * math.factorial(c)
    return math.factorial(n) // denom

def char_table(n):
    parts = list(partitions(n))
    X = np.array([[mn_char(lam, rho) for rho in parts] for lam in parts], dtype=np.float64)
    sizes = np.array([class_size(rho) for rho in parts], dtype=np.float64)
    return parts, X, sizes

def lr_table(n, m):
    """c^lambda_{mu nu} for lambda |- n, mu |- m, nu |- n-m via restriction inner products."""
    pn, Xn, sn = char_table(n)
    pm, Xm, sm = char_table(m)
    pk, Xk, sk = char_table(n - m)
    index_n = {rho: i for i, rho in enumerate(pn)}
    # M_lambda[rho, rho'] = |K_rho||K_rho'| chi^lambda(rho u rho') / (m! (n-m)!)
    C = {}
    norm = math.factorial(m) * math.factorial(n - m)
    for a, lam in enumerate(pn):
        M = np.zeros((len(pm), len(pk)))
        for i, rho in enumerate(pm):
            for j, rho2 in enumerate(pk):
                union = tuple(sorted(rho + rho2, reverse=True))
                M[i, j] = sm[i] * sk[j] * Xn[a, index_n[union]] / norm
        Cl = Xm @ M @ Xk.T   # (mu, nu) entries
        C[lam] = np.rint(Cl).astype(np.int64)
        assert np.allclose(Cl, C[lam], atol=1e-6), "non-integer LR coefficient?"
    return pn, pm, pk, C

def two_class_spectrum(n, m, al, be):
    """Return list of (eigenvalue, multiplicity)."""
    q = (m * al ** 2 + (n - m) * be ** 2) / n ** 2
    pn, pm, pk, C = lr_table(n, m)
    fn = {lam: hook_dim(lam) for lam in pn}
    fm = {mu: hook_dim(mu) for mu in pm}
    fk = {nu: hook_dim(nu) for nu in pk}
    ctn = {lam: content_sum(lam) for lam in pn}
    ctm = {mu: content_sum(mu) for mu in pm}
    ctk = {nu: content_sum(nu) for nu in pk}
    out = []
    for lam in pn:
        for i, mu in enumerate(pm):
            for j, nu in enumerate(pk):
                c = C[lam][i, j]
                if c == 0: continue
                ev = q + (2.0 / n ** 2) * ((al * al - al * be) * ctm[mu] + (be * be - al * be) * ctk[nu] + al * be * ctn[lam])
                out.append((ev, fn[lam] * fm[mu] * fk[nu] * c, lam, mu, nu))
    return out

def chi2_from_spectrum(spec, t):
    return sum(mult * ev ** (2 * t) for ev, mult, *_ in spec) - 1.0

if __name__ == "__main__":
    # basic checks
    assert hook_dim((3, 2)) == 5 and hook_dim((2, 1, 1)) == 3
    assert mn_char((2, 1), (1, 1, 1)) == 2 and mn_char((2, 1), (3,)) == -1 and mn_char((2, 1), (2, 1)) == 0
    for n in range(2, 8):
        parts, X, sizes = char_table(n)
        # orthogonality: sum_rho |K_rho| chi^a chi^b / n! = delta
        G = (X * sizes) @ X.T / math.factorial(n)
        assert np.allclose(G, np.eye(len(parts))), n
    print("character tables OK up to n=7")
    spec = two_class_spectrum(6, 3, 1.5, 0.5)
    print("total multiplicity", sum(m for _, m, *_ in spec), "=", math.factorial(6))
    print("top eigenvalues", sorted(set(round(e, 10) for e, *_ in spec), reverse=True)[:6])
