"""Vectorised Monte Carlo of the product-weight transposition walk for large n.
Records fixed points by class, untouched labels, 2-cycles, cycle counts, slow-at-slow occupancy.
Compares with uniform permutations via empirical TV of discretised statistics."""
import numpy as np, sys, json, math, time
from exact_tv import t_star, U_of_t
from scipy.stats import poisson

def simulate(p, T, R, rng):
    n = len(p)
    sigma = np.tile(np.arange(n), (R, 1))          # sigma[r, i] = position of label i
    touched = np.zeros((R, n), dtype=bool)
    rows = np.arange(R)
    for _ in range(T):
        i = rng.choice(n, size=R, p=p); j = rng.choice(n, size=R, p=p)
        ne = i != j
        a = sigma[rows, i]; b = sigma[rows, j]
        sigma[rows[ne], i[ne]] = b[ne]; sigma[rows[ne], j[ne]] = a[ne]
        touched[rows[ne], i[ne]] = True; touched[rows[ne], j[ne]] = True
    return sigma, touched

def stats(sigma, slow, touched=None):
    R, n = sigma.shape
    idx = np.arange(n)
    fixed = sigma == idx[None, :]
    fix_s = fixed[:, slow].sum(1); fix_f = fixed[:, ~slow].sum(1)
    # 2-cycles: sigma[sigma[i]] == i and sigma[i] != i
    ss = np.take_along_axis(sigma, sigma, axis=1)
    two = ((ss == idx[None, :]) & ~fixed).sum(1) // 2
    two_slow = ((ss == idx[None, :]) & ~fixed & slow[None, :]).sum(1)  # slow labels in 2-cycles
    slow_at_slow = slow[sigma][:, slow].sum(1)  # slow labels whose position is a slow home
    # cycle count
    cyc = np.zeros(R, dtype=int)
    for r in range(R):
        seen = np.zeros(n, bool); c = 0
        s = sigma[r]
        for i in range(n):
            if not seen[i]:
                c += 1; j = i
                while not seen[j]:
                    seen[j] = True; j = s[j]
        cyc[r] = c
    out = dict(fix_s=fix_s, fix_f=fix_f, two=two, two_slow=two_slow, slow_at_slow=slow_at_slow - fix_s, cyc=cyc - fix_s - fix_f)
    if touched is not None:
        out['untouched_s'] = (~touched)[:, slow].sum(1); out['untouched_f'] = (~touched)[:, ~slow].sum(1)
    return out

def emp_tv(x, y, bins=None):
    """TV between empirical laws of integer statistics x, y."""
    lo = min(x.min(), y.min()); hi = max(x.max(), y.max())
    if bins is None:
        a = np.bincount(x - lo, minlength=hi - lo + 1) / len(x); b = np.bincount(y - lo, minlength=hi - lo + 1) / len(y)
    else:
        a, _ = np.histogram(x, bins); b, _ = np.histogram(y, bins); a = a / len(x); b = b / len(y)
    return 0.5 * np.abs(a - b).sum()

def emp_tv_joint(xs, ys):
    from collections import Counter
    cx = Counter(map(tuple, np.array(xs).T)); cy = Counter(map(tuple, np.array(ys).T))
    keys = set(cx) | set(cy); R1 = len(xs[0]); R2 = len(ys[0])
    return 0.5 * sum(abs(cx.get(k, 0) / R1 - cy.get(k, 0) / R2) for k in keys)

def run_setting(name, p, slow, Ks, R, seed=1):
    rng = np.random.default_rng(seed)
    n = len(p); ts = t_star(p)
    print("== %s: n=%d, #slow=%d, t*=%.1f, p_min*n=%.3f, p_max*n=%.3f" % (name, n, slow.sum(), ts, p.min() * n, p.max() * n), flush=True)
    # uniform reference sample
    U = np.array([rng.permutation(n) for _ in range(R)])
    su = stats(U, slow)
    res = {}
    for K in Ks:
        T = int(round(ts + K * n))
        t0 = time.time()
        sigma, touched = simulate(p, T, R, rng)
        sw = stats(sigma, slow, touched)
        Uslow = float(np.sum((1 - 2 * p[slow] * (1 - p[slow])) ** T)); Ufast = float(np.sum((1 - 2 * p[~slow] * (1 - p[~slow])) ** T))
        line = {}
        line['T'] = T; line['U_slow'] = Uslow; line['U_fast'] = Ufast
        line['mean_untouched_s'] = float(sw['untouched_s'].mean()); line['mean_untouched_f'] = float(sw['untouched_f'].mean())
        line['mean_fix_s'] = float(sw['fix_s'].mean()); line['mean_fix_f'] = float(sw['fix_f'].mean())
        ms = slow.sum() / n; mf = 1 - ms
        # predicted TV from class-refined Poisson profile
        k = np.arange(0, 60)
        pred_pair = 0.5 * np.abs(poisson.pmf(k, ms + Uslow) - poisson.pmf(k, ms)).sum() if Ufast < 1e-3 else float('nan')
        pred_total = 0.5 * np.abs(poisson.pmf(k, 1 + Uslow + Ufast) - poisson.pmf(k, 1)).sum()
        line['pred_TV_pair'] = pred_pair; line['pred_TV_total'] = pred_total
        for key in ['fix_s', 'fix_f', 'two', 'two_slow', 'slow_at_slow', 'cyc']:
            line['tv_' + key] = emp_tv(sw[key], su[key])
        line['tv_pair'] = emp_tv_joint([sw['fix_s'], sw['fix_f']], [su['fix_s'], su['fix_f']])
        line['tv_total_fix'] = emp_tv(sw['fix_s'] + sw['fix_f'], su['fix_s'] + su['fix_f'])
        # poisson fit check for fix_s: compare to Poisson(ms+Uslow)
        line['tv_fix_s_vs_Poisson'] = 0.5 * np.abs(np.bincount(sw['fix_s'], minlength=60)[:60] / R - poisson.pmf(k, ms + Uslow)).sum()
        line['mean_slow_at_slow'] = float(sw['slow_at_slow'].mean()); line['mean_slow_at_slow_unif'] = float(su['slow_at_slow'].mean())
        line['mean_cyc'] = float(sw['cyc'].mean()); line['mean_cyc_unif'] = float(su['cyc'].mean())
        line['mean_two'] = float(sw['two'].mean()); line['mean_two_unif'] = float(su['two'].mean())
        res[K] = line
        print("  K=%4.1f T=%6d U_s=%.3f U_f=%.4f | untouched_s mean=%.3f fix_s mean=%.3f (unif %.3f) | TV: fix_s %.3f pair %.3f total %.3f pred_pair %.3f pred_total %.3f | fix_s~Poi %.3f | two %.3f two_slow %.3f slow@slow %.3f cyc %.3f | MC noise ~%.3f [%.0fs]" % (
            K, T, Uslow, Ufast, line['mean_untouched_s'], line['mean_fix_s'], su['fix_s'].mean(), line['tv_fix_s'], line['tv_pair'], line['tv_total_fix'], pred_pair, pred_total, line['tv_fix_s_vs_Poisson'], line['tv_two'], line['tv_two_slow'], line['tv_slow_at_slow'], line['tv_cyc'], 1.0 / math.sqrt(R), time.time() - t0), flush=True)
    return res

if __name__ == "__main__":
    n = int(sys.argv[1]); R = int(sys.argv[2]); which = sys.argv[3]
    out = {}
    if which in ('S1', 'all'):
        m = int(round(math.sqrt(n))); b = 0.5
        w = np.ones(n); w[:m] = b; w[m:] = (n - m * b) / (n - m); p = w / w.sum(); slow = np.zeros(n, bool); slow[:m] = True
        out['S1_sqrt_slow_class'] = run_setting('S1 sqrt(n) slow labels b=0.5', p, slow, [-1, 0, 1, 2, 3], R)
    if which in ('S2', 'all'):
        h = n // 2; w = np.ones(n); w[:h] = 0.5; w[h:] = 1.5; p = w / w.sum(); slow = np.zeros(n, bool); slow[:h] = True
        out['S2_equal_classes'] = run_setting('S2 equal classes b=0.5 a=1.5', p, slow, [-1, 0, 1, 2, 3], R)
    if which in ('S3', 'all'):
        w = 0.5 + np.arange(n) / (n - 1); p = w / w.sum(); slow = w <= 0.6  # bottom decile as 'slow'
        out['S3_continuum'] = run_setting('S3 continuum 0.5..1.5 (slow := lowest 10%)', p, slow, [-1, 0, 1, 2, 3], R)
    if which in ('S4', 'all'):
        w = np.ones(n) * 1.5; k1 = n // 10; k2 = n // 5; w[:k1] = 0.5; w[k1:k1 + k2] = 0.6; p = w / w.sum(); slow = np.zeros(n, bool); slow[:k1 + k2] = True
        out['S4_two_competing'] = run_setting('S4 competing slow classes 0.5 (10%) and 0.6 (20%)', p, slow, [-1, 0, 1, 2, 3], R)
    json.dump({k: {str(kk): vv for kk, vv in v.items()} for k, v in out.items()}, open('mc_n%d_%s.json' % (n, which), 'w'), default=float)
