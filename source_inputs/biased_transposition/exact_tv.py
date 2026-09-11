"""Exact total-variation distance for the product-weight transposition walk on S_n.

Convention (as in the release / the problem statement): at each step draw two labels
i, j independently with probabilities p_i, p_j; if i != j replace sigma by sigma∘(i j)
(i.e. swap the entries in slots i and j of the one-line array), if i == j do nothing.
"""
import itertools, math, sys, json
import numpy as np

def all_perms(n):
    P = np.array(list(itertools.permutations(range(n))), dtype=np.int8)
    return P

def rank_perms(P):
    """Lexicographic rank (Lehmer code) of each row of P; rows are permutations of 0..n-1."""
    N, n = P.shape
    r = np.zeros(N, dtype=np.int64)
    fact = [math.factorial(k) for k in range(n)]
    for k in range(n - 1):
        cnt = np.zeros(N, dtype=np.int64)
        for l in range(k + 1, n):
            cnt += (P[:, l] < P[:, k])
        r += cnt * fact[n - 1 - k]
    return r

def build_swap_index(n):
    P = all_perms(n)
    # sanity: rank of row k must be k (itertools yields lexicographic order)
    idx = {}
    for i in range(n):
        for j in range(i + 1, n):
            Q = P.copy()
            Q[:, [i, j]] = Q[:, [j, i]]
            idx[(i, j)] = rank_perms(Q).astype(np.int32)
    fixed = (P == np.arange(n, dtype=np.int8)[None, :]).sum(axis=1).astype(np.int8)
    return P, idx, fixed

def U_of_t(p, t):
    p = np.asarray(p, float)
    return np.sum((1 - 2 * p * (1 - p)) ** t)

def t_star(p):
    """Real solution of U(t)=1 (U is decreasing)."""
    lo, hi = 0.0, 1.0
    while U_of_t(p, hi) > 1:
        hi *= 2
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if U_of_t(p, mid) > 1:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

def run(p, T, cache):
    P, idx, fixed = cache
    n = len(p)
    N = P.shape[0]
    p = np.asarray(p, float)
    q = float(np.sum(p ** 2))
    dist = np.zeros(N)
    dist[0] = 1.0  # identity is the first permutation lexicographically
    unif = 1.0 / N
    # fixed point law under uniform
    fp_unif = np.bincount(fixed, minlength=n + 1) / N
    out = []
    for t in range(T + 1):
        tv = 0.5 * np.abs(dist - unif).sum()
        chi2 = N * np.sum(dist ** 2) - 1.0
        fp = np.bincount(fixed, weights=dist, minlength=n + 1)
        tv_fp = 0.5 * np.abs(fp - fp_unif).sum()
        out.append((t, tv, chi2, tv_fp, float(U_of_t(p, t))))
        # step
        new = q * dist
        for (i, j), ind in idx.items():
            new += 2 * p[i] * p[j] * dist[ind]
        dist = new
    return out

if __name__ == "__main__":
    n = int(sys.argv[1])
    cache = build_swap_index(n)
    print("built", n, flush=True)
