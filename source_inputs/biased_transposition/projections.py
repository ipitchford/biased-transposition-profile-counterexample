"""Projections of the exact law mu_t onto coarser statistics, to locate where TV mass lives."""
import numpy as np, json, sys, math
from exact_tv import build_swap_index, t_star
from run_families import families

def cycle_features(P, slow_mask):
    """For each permutation row (one-line, sigma(i)=P[r,i]) return several feature keys."""
    N, n = P.shape
    feats = {'cycle_type': [], 'fix_slow_fast': [], 'fix_2cyc': [], 'ctype_slowfix': [], 'coloured': []}
    for r in range(N):
        s = P[r]
        seen = [False] * n
        cycles = []
        for i in range(n):
            if not seen[i]:
                c = []
                j = i
                while not seen[j]:
                    seen[j] = True; c.append(j); j = int(s[j])
                cycles.append(c)
        ct = tuple(sorted(len(c) for c in cycles))
        fs = sum(1 for c in cycles if len(c) == 1 and slow_mask[c[0]])
        ff = sum(1 for c in cycles if len(c) == 1 and not slow_mask[c[0]])
        two = sum(1 for c in cycles if len(c) == 2)
        # coloured cycle type: multiset of canonical cyclic colour words
        words = []
        for c in cycles:
            w = [1 if slow_mask[k] else 0 for k in c]
            L = len(w)
            rots = [tuple(w[k:] + w[:k]) for k in range(L)]
            words.append(min(rots))
        col = tuple(sorted(words))
        feats['cycle_type'].append(ct)
        feats['fix_slow_fast'].append((fs, ff))
        feats['fix_2cyc'].append((fs + ff, two))
        feats['ctype_slowfix'].append((ct, fs))
        feats['coloured'].append(col)
    keys = {}
    for name, lst in feats.items():
        uniq = {v: k for k, v in enumerate(sorted(set(lst)))}
        keys[name] = np.array([uniq[v] for v in lst], dtype=np.int32)
    return keys

def proj_tv(dist, key):
    N = len(dist)
    a = np.bincount(key, weights=dist)
    b = np.bincount(key) / N
    return 0.5 * np.abs(a - b).sum()

if __name__ == "__main__":
    n = int(sys.argv[1]); fam = sys.argv[2]; T = int(sys.argv[3])
    cache = build_swap_index(n)
    P, idx, fixed = cache
    p = families(n)[fam]
    slow_mask = (p <= p.min() + 1e-12)
    keys = cycle_features(P, slow_mask)
    N = P.shape[0]; q = float(np.sum(p ** 2))
    dist = np.zeros(N); dist[0] = 1
    unif = 1 / N
    print("family", fam, "n", n, "t*=%.2f" % t_star(p), "slow labels:", np.where(slow_mask)[0].tolist())
    print("  t    d(t)   | cycle_type  fix(s,f)  (fix,2cyc)  (ctype,slowfix)  coloured")
    for t in range(T + 1):
        d = 0.5 * np.abs(dist - unif).sum()
        vals = [proj_tv(dist, keys[k]) for k in ['cycle_type', 'fix_slow_fast', 'fix_2cyc', 'ctype_slowfix', 'coloured']]
        if t % 2 == 0:
            print("%3d  %.4f  | %s" % (t, d, "  ".join("%.4f" % v for v in vals)))
        new = q * dist
        for (i, j), ind in idx.items():
            new += 2 * p[i] * p[j] * dist[ind]
        dist = new
