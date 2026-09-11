import numpy as np, json, sys, time, math
from exact_tv import build_swap_index, run, t_star, U_of_t

def families(n):
    F = {}
    F['F1_uniform'] = np.ones(n)
    h = n // 2
    w = np.ones(n); w[:h] = 0.5; w[h:] = 1.5; F['F2_two_equal_b0.5'] = w
    w = np.ones(n); w[:2] = 0.5; F['F3_two_slow_labels'] = w
    w = np.ones(n) * 1.5; w[:3] = 0.5; w[3:6] = 0.6; F['F4_two_competing_slow_classes'] = w
    w = 0.5 + (1.5 - 0.5) * np.arange(n) / (n - 1); F['F5_continuum'] = w
    w = np.ones(n); w[0] = 3.0; F['F6_one_superfast'] = w
    w = np.ones(n); w[:h] = 0.25; w[h:] = 1.75; F['F7_two_equal_b0.25'] = w
    w = np.ones(n) * 1.5; w[:3] = 0.5; F['F8_three_slow_labels'] = w
    return {k: v / v.sum() for k, v in F.items()}

def tmix(rows, eps):
    # first integer t with d(t) <= eps, plus linear interpolation of the crossing
    ts = [r[0] for r in rows]; ds = [r[1] for r in rows]
    for k in range(1, len(ts)):
        if ds[k] <= eps:
            # interpolate between k-1 and k
            frac = (ds[k - 1] - eps) / (ds[k - 1] - ds[k])
            return ts[k], ts[k - 1] + frac
    return None, None

if __name__ == "__main__":
    n = int(sys.argv[1]); T = int(sys.argv[2])
    t0 = time.time(); cache = build_swap_index(n); print("built n=%d in %.1fs" % (n, time.time() - t0), flush=True)
    res = {}
    for name, p in families(n).items():
        t0 = time.time()
        rows = run(p, T, cache)
        ts = t_star(p)
        rec = {'p': p.tolist(), 't_star': ts, 'rows': [[float(x) for x in r] for r in rows]}
        for eps in (0.25, 0.1, 0.05):
            rec['tmix_%g' % eps] = tmix(rows, eps)
        res[name] = rec
        print("%-32s t*=%6.2f  tmix(.25)=%s tmix(.1)=%s tmix(.05)=%s  [%.0fs]" % (
            name, ts, rec['tmix_0.25'], rec['tmix_0.1'], rec['tmix_0.05'], time.time() - t0), flush=True)
    json.dump(res, open('exact_n%d.json' % n, 'w'))
