#!/usr/bin/env python3
"""Hostile regression tests for publication acceptance conditions."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile

import verify_exact
import verify_claim_surface
import verify_manifest
import verify_numeric


def require_rejection(action, label: str) -> None:
    try:
        action()
    except RuntimeError:
        return
    raise RuntimeError(f'negative control was incorrectly accepted: {label}')


def reject_trivial_finite_bounds() -> None:
    original = verify_exact.finite_tv_lower
    try:
        verify_exact.finite_tv_lower = lambda *args, **kwargs: (
            verify_exact.F(0), verify_exact.F(0))
        require_rejection(verify_exact.verify_published_finite_table,
                          'zero finite-table bounds')
    finally:
        verify_exact.finite_tv_lower = original


def reject_corrupted_saved_time(source: Path) -> None:
    with tempfile.TemporaryDirectory(prefix='biased-transposition-negative-') as tmp:
        copied = Path(tmp)
        inherited = json.loads((source / 'exact_n8.json').read_text(encoding='utf-8'))
        first = next(iter(inherited.values()))
        first['rows'][0][0] = 999
        (copied / 'exact_n8.json').write_text(
            json.dumps(inherited, allow_nan=False), encoding='utf-8')
        require_rejection(lambda: verify_numeric.replay_n8(copied),
                          'mutated saved time column')


def reject_truncated_saved_trajectory(source: Path) -> None:
    with tempfile.TemporaryDirectory(prefix='biased-transposition-negative-') as tmp:
        copied = Path(tmp)
        inherited = json.loads((source / 'exact_n8.json').read_text(encoding='utf-8'))
        first = next(iter(inherited.values()))
        first['rows'] = first['rows'][:-1]
        (copied / 'exact_n8.json').write_text(
            json.dumps(inherited, allow_nan=False), encoding='utf-8')
        require_rejection(lambda: verify_numeric.replay_n8(copied),
                          'truncated saved trajectory')


def reject_reordered_saved_trajectory(source: Path) -> None:
    with tempfile.TemporaryDirectory(prefix='biased-transposition-negative-') as tmp:
        copied = Path(tmp)
        inherited = json.loads((source / 'exact_n8.json').read_text(encoding='utf-8'))
        first = next(iter(inherited.values()))
        first['rows'][7], first['rows'][8] = first['rows'][8], first['rows'][7]
        (copied / 'exact_n8.json').write_text(
            json.dumps(inherited, allow_nan=False), encoding='utf-8')
        require_rejection(lambda: verify_numeric.replay_n8(copied),
                          'reordered saved trajectory')


def reject_perturbed_saved_columns(source: Path) -> None:
    labels = ('TV', 'chi-square', 'fixed-point TV', 'untouched mean')
    for column, label in enumerate(labels, start=1):
        with tempfile.TemporaryDirectory(prefix='biased-transposition-negative-') as tmp:
            copied = Path(tmp)
            inherited = json.loads((source / 'exact_n8.json').read_text(encoding='utf-8'))
            first = next(iter(inherited.values()))
            first['rows'][4][column] += 0.01
            (copied / 'exact_n8.json').write_text(
                json.dumps(inherited, allow_nan=False), encoding='utf-8')
            require_rejection(lambda: verify_numeric.replay_n8(copied),
                              f'perturbed saved {label} column')


def reject_contract_mutation(package: Path, label: str, mutate) -> None:
    contract = json.loads((package / 'certificate_contract.json').read_text(encoding='utf-8'))
    mutate(contract)
    with tempfile.TemporaryDirectory(prefix='biased-transposition-contract-') as tmp:
        path = Path(tmp) / 'mutated_contract.json'
        path.write_text(json.dumps(contract, allow_nan=False), encoding='utf-8')
        require_rejection(lambda: verify_exact.main(path), label)


def reject_unlisted_package_file(package: Path) -> None:
    with tempfile.TemporaryDirectory(prefix='biased-transposition-manifest-') as tmp:
        copied = Path(tmp) / 'package'
        shutil.copytree(package, copied, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'))
        (copied / 'UNLISTED.txt').write_text('hostile extra file\n', encoding='utf-8')
        report = verify_manifest.verify_package(copied)
        if report['status'] != 'FAIL' or not any(
                item == {'path': 'UNLISTED.txt', 'error': 'unlisted file'}
                for item in report['failures']):
            raise RuntimeError('negative control was incorrectly accepted: unlisted package file')


def reject_manifest_mutation(package: Path, label: str, mutate) -> None:
    with tempfile.TemporaryDirectory(prefix='biased-transposition-manifest-') as tmp:
        copied = Path(tmp) / 'package'
        shutil.copytree(package, copied, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'))
        manifest_path = copied / 'MANIFEST.json'
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        mutate(copied, manifest)
        manifest_path.write_text(json.dumps(manifest, allow_nan=False), encoding='utf-8')
        report = verify_manifest.verify_package(copied)
        if report['status'] != 'FAIL':
            raise RuntimeError(f'negative control was incorrectly accepted: {label}')


def reject_manuscript_table_mutation(package: Path) -> None:
    with tempfile.TemporaryDirectory(prefix='biased-transposition-surface-') as tmp:
        paper = Path(tmp) / 'paper.md'
        text = (package / 'paper.md').read_text(encoding='utf-8')
        text = text.replace('| 100 | 281 | 0.728373588448375223 |',
                            '| 100 | 281 | 0.700000000000000000 |', 1)
        paper.write_text(text, encoding='utf-8')
        require_rejection(
            lambda: verify_claim_surface.verify_claim_surface(package, paper),
            'manuscript finite-table mutation')


def main() -> None:
    package = Path(__file__).resolve().parents[1]
    source = package / 'source_inputs' / 'biased_transposition'
    reject_trivial_finite_bounds()
    reject_corrupted_saved_time(source)
    reject_truncated_saved_trajectory(source)
    reject_reordered_saved_trajectory(source)
    reject_perturbed_saved_columns(source)
    reject_contract_mutation(
        package, 'profile coefficient sign mutation',
        lambda c: c['profile_gap']['B_terms'].__setitem__(0, ['-3/2', '1/2']))
    reject_contract_mutation(
        package, 'profile gap threshold mutation',
        lambda c: c['profile_gap'].__setitem__('gap_lower_strict', '0'))
    reject_contract_mutation(
        package, 'finite-moment margin mutation',
        lambda c: c['finite_moment_witness'].__setitem__('exceeds_D_by_more_than', '0'))
    reject_contract_mutation(
        package, 'finite-table tuple mutation',
        lambda c: c['finite_table'][0].__setitem__('t', 280))
    reject_unlisted_package_file(package)
    reject_manifest_mutation(
        package, 'duplicate manifest path',
        lambda root, m: m['files'].append(dict(m['files'][0])))
    reject_manifest_mutation(
        package, 'missing listed file',
        lambda root, m: (root / m['files'][0]['path']).unlink())
    reject_manifest_mutation(
        package, 'byte-corrupted listed file',
        lambda root, m: (root / m['files'][0]['path']).write_bytes(
            (root / m['files'][0]['path']).read_bytes() + b'hostile'))
    reject_manifest_mutation(
        package, 'unsafe manifest path',
        lambda root, m: m['files'].__setitem__(0, {
            'path': '../outside.txt', 'bytes': 0, 'sha256': '0' * 64}))
    reject_manuscript_table_mutation(package)
    headline_mutations = [
        (r'B_0:=\frac32e^{-1/2}-4e^{-3}', r'B_0:=\frac32e^{-1/2}+4e^{-3}'),
        (r'=\frac{5}{2e}-13e^{-4}', r'=\frac{5}{2e}+13e^{-4}'),
        (r'\frac{29}{1000}&<B_0-D_0', r'\frac{0}{1000}&<B_0-D_0'),
        (r'&=\frac{5730077809}{8174960640}', r'&=\frac{5730077808}{8174960640}'),
        (r'> D_0+\frac{19}{1000}', r'> D_0+\frac{0}{1000}'),
    ]
    for old, new in headline_mutations:
        with tempfile.TemporaryDirectory(prefix='biased-headline-mutation-') as tmp:
            mutated = Path(tmp) / 'paper.md'
            text = (package / 'paper.md').read_text(encoding='utf-8')
            if old not in text:
                raise RuntimeError('mutation target absent: ' + old)
            mutated.write_text(text.replace(old, new, 1), encoding='utf-8')
            require_rejection(lambda: verify_claim_surface.verify_claim_surface(package, mutated),
                              'headline manuscript mutation: ' + old)
    print(json.dumps({
        'status': 'PASS',
        'rejected_mutations': [
            'zero finite-table bounds',
            'mutated saved time column',
            'truncated saved trajectory',
            'reordered saved trajectory',
            'perturbed saved TV column',
            'perturbed saved chi-square column',
            'perturbed saved fixed-point TV column',
            'perturbed saved untouched mean column',
            'profile coefficient sign mutation',
            'profile gap threshold mutation',
            'finite-moment margin mutation',
            'finite-table tuple mutation',
            'unlisted package file',
            'duplicate manifest path',
            'missing listed file',
            'byte-corrupted listed file',
            'unsafe manifest path',
            'manuscript finite-table mutation',
            'manuscript B coefficient sign',
            'manuscript D coefficient sign',
            'manuscript gap threshold',
            'manuscript finite-moment numerator',
            'manuscript finite-moment margin',
        ],
    }, indent=2))


if __name__ == '__main__':
    main()
