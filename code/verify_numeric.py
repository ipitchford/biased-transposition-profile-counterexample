#!/usr/bin/env python3
"""Implementation-diverse in-package replay of inherited numerical claims.

Requires NumPy. Does not use the uploaded Lehmer-code state indexer. The replay
uses a tuple-to-index map and value-swaps (left multiplication); the inherited
code uses slot-swaps (right multiplication). Their one-time laws agree because
the independent transposition increments have identical distributions.

Run from the package root:
  python code/verify_numeric.py --input source_inputs/biased_transposition \
      --out results/numerical_verification.json
"""
from __future__ import annotations
import argparse
import importlib.util
import itertools
import json
import math
from pathlib import Path
import sys
import numpy as np


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def make_states(n: int):
    tuples = list(itertools.permutations(range(n)))
    index = {p: k for k, p in enumerate(tuples)}
    states = np.asarray(tuples, dtype=np.int16)
    swaps = {}
    for i in range(n):
        for j in range(i + 1, n):
            swaps[i, j] = np.fromiter(
                (index[tuple(j if x == i else i if x == j else x for x in p)] for p in tuples),
                dtype=np.int64, count=len(tuples))
    return states, swaps


def compact_key_tv(dist: np.ndarray, keys: np.ndarray) -> float:
    """Compact categories before bincount; memory depends on observed support."""
    if keys.ndim == 2:
        _, inverse = np.unique(keys, axis=0, return_inverse=True)
    else:
        _, inverse = np.unique(keys, return_inverse=True)
    observed = np.bincount(inverse, weights=dist)
    uniform = np.bincount(inverse) / len(dist)
    return float(np.abs(observed - uniform).sum() / 2)


def root_tstar(p: np.ndarray) -> float:
    rates = -np.log1p(-2 * p * (1 - p))
    lo, hi = 0.0, math.log(len(p)) / rates.min() + 1.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if np.exp(-rates * mid).sum() > 1:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def replay_n8(input_dir: Path) -> dict:
    inherited = json.loads((input_dir / 'exact_n8.json').read_text())
    states, swaps = make_states(8)
    N = len(states)
    fixed = states == np.arange(8)
    total_fixed = fixed.sum(axis=1)
    fixed_stationary = np.bincount(total_fixed, minlength=9) / N
    families = []
    for name, source in inherited.items():
        p = np.asarray(source['p'])
        require(np.all(p > 0) and abs(p.sum() - 1) < 1e-14, 'probability normalisation')
        rows = np.asarray(source['rows'], dtype=float)
        require(rows.ndim == 2 and rows.shape[1] == 5 and len(rows) == 61,
                f'invalid saved trajectory shape {name}')
        require(bool(np.all(np.isfinite(rows))), f'non-finite saved trajectory {name}')
        require(np.array_equal(rows[:, 0], np.arange(len(rows), dtype=float)),
                f'saved time column is not the expected integer sequence {name}')
        dist = np.zeros(N)
        dist[0] = 1
        errors = np.zeros(5)
        max_mass_error = 0.0
        last_tv = 1.0
        crossings = {str(eps): None for eps in (0.25, 0.1, 0.05)}
        tstar = root_tstar(p)
        projection = None
        # Exactly equal probabilities in inherited two-class arrays remain
        # equal here; continuum has eight distinct classes, handled compactly.
        _, classes = np.unique(p, return_inverse=True)
        counts = np.stack([fixed[:, classes == j].sum(axis=1)
                           for j in range(classes.max() + 1)], axis=1)
        fixedset = np.sum(fixed.astype(np.int64) * (2 ** np.arange(8)), axis=1)
        rates = -np.log1p(-2 * p * (1 - p))
        for t in range(len(rows)):
            tv = float(np.abs(dist - 1 / N).sum() / 2)
            chi2 = float(N * np.dot(dist, dist) - 1)
            fp = np.bincount(total_fixed, weights=dist, minlength=9)
            tvfp = float(np.abs(fp - fixed_stationary).sum() / 2)
            untouched = float(np.exp(-rates * t).sum())
            errors = np.maximum(errors, np.abs(np.array([t, tv, chi2, tvfp, untouched]) - rows[t]))
            max_mass_error = max(max_mass_error, abs(float(dist.sum()) - 1))
            require(tv <= last_tv + 1e-12, 'TV monotonicity')
            require(tvfp <= tv + 1e-12, 'projection cannot exceed full TV')
            last_tv = tv
            for eps in (0.25, 0.1, 0.05):
                if crossings[str(eps)] is None and tv <= eps:
                    crossings[str(eps)] = t
            if t == round(tstar):
                dset = compact_key_tv(dist, fixedset)
                dclasses = compact_key_tv(dist, counts)
                require(tvfp <= dclasses + 1e-12 and dclasses <= dset + 1e-12
                        and dset <= tv + 1e-12, 'data-processing hierarchy')
                projection = {'t': t, 'full_TV': tv, 'fixed_set_TV': dset,
                              'class_fixed_count_TV': dclasses, 'total_fixed_count_TV': tvfp,
                              'classes': int(classes.max() + 1)}
            new = float(np.dot(p, p)) * dist
            for (i, j), ind in swaps.items():
                new += 2 * p[i] * p[j] * dist[ind]
            dist = new
        require(errors[0] == 0 and errors[1] < 1e-11 and errors[2] < 1e-7 and errors[3] < 1e-11
                and errors[4] < 1e-11 and max_mass_error < 1e-11, f'replay discrepancy {name}')
        require(abs(tstar - source['t_star']) < 1e-10, 'tstar replay')
        for eps in (0.25, 0.1, 0.05):
            require(crossings[str(eps)] == source[f'tmix_{eps:g}'][0], 'integer crossing replay')
        families.append({'family': name, 'steps_checked': len(rows),
                         'max_absolute_errors_t_TV_chi2_fixedTV_U': errors.tolist(),
                         'max_probability_mass_error': max_mass_error,
                         't_star': tstar, 'integer_mixing_times': crossings,
                         'projection_at_nearest_t_star': projection})
    return {'name': 'all_inherited_n8_trajectories', 'state_count': N,
            'arithmetic': 'float64; deterministic enumeration, not exact rational',
            'families': families, 'pass': True}


def dense_spectrum(input_dir: Path) -> dict:
    n, m, alpha, beta = 6, 2, 2.0, 0.5
    p = np.array([alpha / n] * m + [beta / n] * (n - m))
    states, swaps = make_states(n)
    d = len(states)
    M = np.eye(d) * np.dot(p, p)
    for (i, j), inds in swaps.items():
        M[np.arange(d), inds] += 2 * p[i] * p[j]
    actual = np.linalg.eigvalsh(M)
    spec = importlib.util.spec_from_file_location('inherited_spectrum', input_dir / 'spectrum.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    blocks = module.two_class_spectrum(n, m, alpha, beta)
    predicted = np.sort(np.repeat([x[0] for x in blocks], [x[1] for x in blocks]))
    require(len(predicted) == math.factorial(n), 'spectrum multiplicity')
    error = float(np.max(np.abs(actual - predicted)))
    require(error < 1e-10, 'dense versus representation spectrum')
    return {'name': 'unequal_two_class_spectrum_dense_crosscheck', 'n': n, 'm': m,
            'alpha': alpha, 'beta': beta, 'dimension': d,
            'max_eigenvalue_absolute_error': error, 'pass': True}


def exact_small_walk() -> dict:
    n = 4
    states, swaps = make_states(n)
    weights = (1, 2, 3, 4)
    numerator = [0] * len(states)
    numerator[0] = 1
    denominator = 1
    checked = 0
    for t in range(9):
        require(sum(numerator) == denominator, 'rational walk conservation')
        total = math.factorial(n)
        tv_num = sum(abs(total * x - denominator) for x in numerator)
        require(tv_num <= 2 * total * denominator, 'rational TV range')
        updated = [30 * x for x in numerator]
        for (i, j), inds in swaps.items():
            for k in range(total):
                updated[k] += 2 * weights[i] * weights[j] * numerator[int(inds[k])]
        numerator = updated
        denominator *= 100
        checked += 1
    return {'name': 'integer_arithmetic_n4_walk', 'states': 24, 'times_checked': checked,
            'p': ['1/10', '2/10', '3/10', '4/10'], 'pass': True}


def asymptotic_diagnostics() -> dict:
    rows = []
    for n in (1000, 10000, 100000, 1000000):
        p = np.linspace(0.5, 1.5, n) / n
        ts = root_tstar(p)
        t = math.floor(ts)
        lower = float((n - 1) * np.exp(2 * t * np.log1p(-2 * p[1:])).sum())
        m = round(math.sqrt(n))
        pp = np.full(n, (n - 0.5 * m) / (n - m) / n)
        pp[:m] = 0.5 / n
        ts_critical = root_tstar(pp)
        slow_U = float(m * np.exp(ts_critical * np.log1p(-2 * pp[0] * (1 - pp[0]))))
        rows.append({'n': n, 'continuum_t_star': ts,
                     'continuum_interlacing_chi2_lower_at_floor_t_star': lower,
                     'continuum_lower_divided_by_log_n': lower / math.log(n),
                     'critical_sqrt_slow_U_at_t_star': slow_U})
    return {'name': 'asymptotic_diagnostics_not_proof',
            'continuum_expected_ratio_limit': 1.0,
            'critical_sqrt_expected_slow_U_limit': (math.sqrt(5) - 1) / 2,
            'rows': rows, 'status': 'observed_diagnostic'}


def metadata_audit(input_dir: Path) -> dict:
    nan_count = 0
    def reject_constant(value):
        raise ValueError(f'non-standard JSON constant {value}')
    inherited = input_dir / 'mc_n2000_all.json'
    try:
        json.loads(inherited.read_text(), parse_constant=reject_constant)
        strict = True
    except ValueError:
        strict = False
    nan_count = inherited.read_text().count('NaN')
    n9 = json.loads((input_dir / 'exact_n9.json').read_text())
    p = n9['F2_two_equal_b0.5']['p']
    return {'name': 'inherited_metadata_audit', 'mc_json_strictly_valid': strict,
            'mc_NaN_literals': nan_count, 'n9_nominal_equal_class_actual_weights_np': [9 * p[0], 9 * p[-1]],
            'n9_and_n10_full_trajectories_replayed': False,
            'n2000_monte_carlo_replayed': False,
            'original_class_projection_key_can_allocate_exponential_memory': True,
            'replacement_uses_compact_observed_keys': True,
            'status': 'observed_metadata_audit'}


def main(input_dir: Path) -> dict:
    require(input_dir.is_dir(), f'missing input directory {input_dir}')
    checks = [exact_small_walk(), replay_n8(input_dir), dense_spectrum(input_dir),
              asymptotic_diagnostics(), metadata_audit(input_dir)]
    return {'schema_version': '1.0', 'status': 'PASS', 'python': sys.version.split()[0],
            'numpy': np.__version__, 'independent_external_review': False, 'checks': checks}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    report = main(args.input)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
    print(json.dumps({'status': report['status'], 'checks': [x['name'] for x in report['checks']]}, indent=2))
