#!/usr/bin/env python3
"""Exact, dependency-free certificates for the untouched-subset profile obstruction.

Run: python code/verify_exact.py --out results/exact_verification.json
No assertion is used as a verification gate; python -O runs the same checks.
The output certifies the listed finite identities/inequalities, not the entire
asymptotic paper in a formal proof assistant.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from itertools import combinations
from math import comb, factorial, floor, log
from pathlib import Path
import json
import sys


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CONTRACT = {
    'schema_version': '1.0',
    'profile_gap': {
        's': 'log(6)',
        'slow_weight_range': '0 < b < 1',
        'B_terms': [['3/2', '1/2'], ['-4', '3']],
        'D_terms': [['5/2', '1'], ['-13', '4']],
        'gap_lower_strict': '29/1000',
        'gap_upper_strict': '291/10000',
    },
    'finite_moment_witness': {
        'lower_degree': 11,
        'stationary_upper_degree': 10,
        'witness': '5730077809/8174960640',
        'exceeds_D_by_more_than': '19/1000',
    },
    'finite_table': [
        {'N': 100, 't': 281, 'b': '1/2', 'published_lower': '0.728373588448375223'},
        {'N': 1000, 't': 5115, 'b': '1/2', 'published_lower': '0.713183969406310628'},
        {'N': 10000, 't': 74185, 'b': '1/2', 'published_lower': '0.710943732347267839'},
        {'N': 1000000, 't': 12023751, 'b': '1/2', 'published_lower': '0.710651383270999821'},
    ],
    'saved_n8_trajectories': {'first_time': 0, 'last_time': 60, 'row_count': 61},
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_contract(path: Path | None = None) -> dict:
    contract_path = path or PACKAGE_ROOT / 'certificate_contract.json'
    contract = json.loads(contract_path.read_text(encoding='utf-8'))
    require(contract == EXPECTED_CONTRACT,
            'certificate contract differs from the exact publication claim contract')
    return contract


def exp_minus_bounds(x: F, even_degree: int = 80) -> tuple[F, F]:
    """Taylor's signed remainder gives odd lower/even upper bounds for exp(-x)."""
    require(x >= 0 and even_degree >= 0 and even_degree % 2 == 0, 'invalid Taylor input')
    term = F(1)
    total = term
    for k in range(1, even_degree + 1):
        term *= -x / k
        total += term
    upper = total
    lower = total + term * (-x / (even_degree + 1))
    require(lower <= upper, 'Taylor bound ordering')
    return lower, upper


def linear_exp_bounds(terms: list[tuple[F, F]]) -> tuple[F, F]:
    lo = hi = F(0)
    for coefficient, x in terms:
        a, b = exp_minus_bounds(x)
        if coefficient >= 0:
            lo += coefficient * a
            hi += coefficient * b
        else:
            lo += coefficient * b
            hi += coefficient * a
    return lo, hi


def decimal_bracket(bounds: tuple[F, F], digits: int = 18) -> dict:
    """Outward-rounded decimal strings, using integer arithmetic only."""
    lo, hi = bounds
    scale = 10 ** digits
    left = (lo.numerator * scale) // lo.denominator
    right = -((-hi.numerator * scale) // hi.denominator)
    def fmt(integer: int) -> str:
        sign = '-' if integer < 0 else ''
        integer = abs(integer)
        return f'{sign}{integer // scale}.{integer % scale:0{digits}d}'
    return {'lower': fmt(left), 'upper': fmt(right)}


def trunc_tail2(z: int, degree: int) -> int:
    return sum((-1) ** r * (r - 1) * comb(z, r)
               for r in range(2, min(z, degree) + 1))


def pow_fixed_interval(base: F, exponent: int, scale: int) -> tuple[int, int]:
    """Return integer lo,hi with lo/scale <= base**exponent <= hi/scale.

    Repeated squaring with outward integer rounding; all operations are exact.
    """
    require(0 <= base <= 1 and exponent >= 0, 'invalid power input')
    a = (base.numerator * scale) // base.denominator
    b = -((-base.numerator * scale) // base.denominator)
    lo = hi = scale
    while exponent:
        if exponent & 1:
            lo = lo * a // scale
            hi = (hi * b + scale - 1) // scale
        exponent >>= 1
        if exponent:
            a = a * a // scale
            b = (b * b + scale - 1) // scale
    return lo, hi


def untouched_binom_moment_interval(N: int, t: int, r: int, b: F,
                                    digits: int = 220) -> tuple[F, F]:
    m = N // 2
    if r > m:
        return F(0), F(0)
    scale = 10 ** digits
    qr = 1 - 2 * r * b / N + r * (r + 1) * b * b / (N * N)
    lo, hi = pow_fixed_interval(qr, t, scale)
    return F(comb(m, r) * lo, scale), F(comb(m, r) * hi, scale)


def stationary_binom_moment(N: int, r: int) -> F:
    if r > N // 2:
        return F(0)
    fall = 1
    for j in range(r):
        fall *= N - j
    return F(comb(N // 2, r), fall)


def finite_tv_lower(N: int, t: int, b: F = F(1, 2), degree: int = 21) -> tuple[F, F]:
    """Certified evaluation interval for a rigorous finite-N TV lower bound.

    Odd Bonferroni bound for P(untouched_slow >= 2), minus even bound for
    P(uniform_fixed_slow >= 2). The interval is for that bound, not TV itself.
    """
    require(N > 0 and N % 2 == 0 and degree % 2 == 1, 'invalid finite certificate input')
    lo = hi = F(0)
    for r in range(2, degree + 1):
        a, bb = untouched_binom_moment_interval(N, t, r, b)
        coefficient = (-1) ** r * (r - 1)
        if coefficient >= 0:
            lo += coefficient * a
            hi += coefficient * bb
        else:
            lo += coefficient * bb
            hi += coefficient * a
    stationary_upper = sum((F((-1) ** r * (r - 1)) * stationary_binom_moment(N, r)
                            for r in range(2, degree)), F(0))
    return lo - stationary_upper, hi - stationary_upper


# Exact parameter tuples and downward-rounded lower bounds printed in Table 1.
# PASS must certify these published values, not merely an ordered interval.
PUBLISHED_FINITE_ROWS = (
    (100, 281, '0.728373588448375223'),
    (1000, 5115, '0.713183969406310628'),
    (10000, 74185, '0.710943732347267839'),
    (1000000, 12023751, '0.710651383270999821'),
)


def verify_published_finite_table(contract: dict | None = None) -> list[dict]:
    contract = contract or load_contract()
    contract_rows = contract['finite_table']
    require(len(contract_rows) == len(PUBLISHED_FINITE_ROWS),
            'finite-table contract row count')
    finite = []
    for contract_row, expected_row in zip(contract_rows, PUBLISHED_FINITE_ROWS):
        N, t, published_text = expected_row
        require(contract_row == {'N': N, 't': t, 'b': '1/2',
                                 'published_lower': published_text},
                f'finite-table contract mismatch N={N}')
        published_lower = F(published_text)
        bound = finite_tv_lower(N, t)
        require(bound[0] <= bound[1], f'finite lower bound ordering N={N}')
        require(bound[0] >= published_lower,
                f'computed lower endpoint does not certify published Table 1 bound N={N}')
        finite.append({'N': N, 't': t, 'b': '1/2', 'bonferroni_degrees': [21, 20],
                       'published_downward_rounded_lower_bound': published_text,
                       'certified_lower_bound_interval': decimal_bracket(bound)})
    return finite


def main(contract_path: Path | None = None) -> dict:
    contract = load_contract(contract_path)
    checks = []
    # All draw pairs enumerated, independently of the closed avoidance formula.
    vectors = [(F(1, 4), F(1, 4), F(1, 4), F(1, 4)),
               (F(1, 10), F(1, 5), F(3, 10), F(2, 5))]
    avoidance_cases = 0
    for p in vectors:
        n = len(p)
        for k in range(n + 1):
            for subset_tuple in combinations(range(n), k):
                subset = set(subset_tuple)
                enumerated = sum((p[i] * p[j] for i in range(n) for j in range(n)
                                  if i == j or (i not in subset and j not in subset)), F(0))
                mass = sum((p[i] for i in subset), F(0))
                formula = (1 - mass) ** 2 + sum((p[i] ** 2 for i in subset), F(0))
                require(enumerated == formula, 'one-step subset avoidance identity')
                avoidance_cases += 1
    checks.append({'name': 'subset_avoidance_by_draw_enumeration', 'cases': avoidance_cases, 'pass': True})

    # Bonferroni identity has an explicit remainder for z>K:
    # S_K(z)-1 = (-1)^K [z C(z-2,K-1)-C(z-1,K)].
    for z in range(0, 101):
        target = int(z >= 2)
        for K in range(2, 24):
            value = trunc_tail2(z, K)
            require(value >= target if K % 2 == 0 else value <= target,
                    f'Bonferroni parity z={z}, K={K}')
            if z > K:
                residual = (-1) ** K * (z * comb(z - 2, K - 1) - comb(z - 1, K))
                require(value - 1 == residual, 'Bonferroni remainder identity')
    checks.append({'name': 'tail_at_least_two_Bonferroni_identity', 'cases': 101 * 22, 'pass': True})

    profile = contract['profile_gap']
    B = linear_exp_bounds([(F(c), F(x)) for c, x in profile['B_terms']])
    D = linear_exp_bounds([(F(c), F(x)) for c, x in profile['D_terms']])
    gap = (B[0] - D[1], B[1] - D[0])
    gap_lower = F(profile['gap_lower_strict'])
    gap_upper = F(profile['gap_upper_strict'])
    require(gap_lower < gap[0] and gap[1] < gap_upper, 'strict profile gap certificate')
    # Likelihood-ratio sign changes between k=2 and k=3: 16 < e^3 < 64.
    em3 = exp_minus_bounds(F(3))
    require(F(16) * em3[1] < 1 and F(64) * em3[0] > 1, 'Poisson likelihood threshold')
    checks.append({'name': 'exact_profile_gap', 'lower_bound_B': decimal_bracket(B),
                   'conjectured_value_D': decimal_bracket(D), 'gap': decimal_bracket(gap),
                   'rational_certificate': f'{gap_lower} < B-D < {gap_upper}', 'pass': True})

    # Finite truncation alone already refutes the conjecture, with no use of
    # a Poisson moment-convergence theorem: odd degree 11 / even degree 10.
    lower11 = sum((F((-1) ** r * (r - 1) * 3 ** r, factorial(r))
                   for r in range(2, 12)), F(0))
    upper10 = sum((F((-1) ** r * (r - 1), 2 ** r * factorial(r))
                   for r in range(2, 11)), F(0))
    witness = lower11 - upper10
    moment_contract = contract['finite_moment_witness']
    require(moment_contract['lower_degree'] == 11
            and moment_contract['stationary_upper_degree'] == 10,
            'finite-moment degree contract')
    require(witness == F(moment_contract['witness']), 'finite-moment witness contract')
    witness_margin = F(moment_contract['exceeds_D_by_more_than'])
    require(witness > D[1] + witness_margin, 'degree-11 asymptotic rational witness')
    checks.append({'name': 'finite_moment_disproof_without_Poisson_convergence',
                   'rational_witness': f'{witness.numerator}/{witness.denominator}',
                   'witness_interval': decimal_bracket((witness, witness)),
                   'exceeds_conjecture_by_more_than': str(witness_margin), 'pass': True})

    # A float logarithm selected these integers originally; the certificate is
    # exact for the four explicitly recorded times.
    finite = verify_published_finite_table(contract)
    checks.append({'name': 'finite_N_event_bounds', 'values': finite, 'pass': True})

    # The uploaded interlacing extension is false outside p_max<=1/2.
    actual = (F(1) - 4 * F(9, 10) * F(1, 10)) ** 2
    invalid_rhs = (F(1) - 2 * F(9, 10)) ** 2
    require(actual == F(256, 625) and invalid_rhs == F(16, 25) and actual < invalid_rhs,
            'out-of-domain negative control')
    checks.append({'name': 'negative_control_interlacing_square',
                   'p': ['9/10', '1/10'], 'n': 2, 't': 1,
                   'actual_chi_squared': str(actual), 'invalid_claim_rhs': str(invalid_rhs),
                   'expected_failure_detected': True, 'pass': True})

    return {'schema_version': '1.0', 'status': 'PASS', 'python': sys.version.split()[0],
            'arithmetic': 'integer and Fraction; fixed-point powers use directed integer rounding',
            'formal_proof_assistant': False,
            'claim_contract': 'certificate_contract.json', 'checks': checks}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--contract', type=Path)
    args = parser.parse_args()
    report = main(args.contract)
    text = json.dumps(report, indent=2, allow_nan=False) + '\n'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding='utf-8')
    print(text)
