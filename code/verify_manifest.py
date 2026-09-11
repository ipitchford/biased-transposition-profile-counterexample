#!/usr/bin/env python3
"""Check delivered package files against MANIFEST.json; no dependencies."""
from pathlib import Path
import hashlib
import json
import sys

def operationally_excluded(relative: Path) -> bool:
    return (relative == Path('MANIFEST.json') or '.git' in relative.parts
            or '__pycache__' in relative.parts or relative.suffix == '.pyc'
            or relative.name == '.DS_Store')


def verify_package(root: Path) -> dict:
    root = root.resolve()
    manifest = json.loads((root / 'MANIFEST.json').read_text(encoding='utf-8'))
    failures = []
    listed = set()
    for record in manifest['files']:
        relative = Path(record['path'])
        if relative.as_posix() in listed:
            failures.append({'path': record['path'], 'error': 'duplicate manifest entry'})
            continue
        listed.add(relative.as_posix())
        path = (root / relative).resolve()
        if not path.is_relative_to(root) or operationally_excluded(relative):
            failures.append({'path': record['path'], 'error': 'unsafe or excluded manifest path'})
            continue
        if not path.is_file() or path.is_symlink():
            failures.append({'path': record['path'], 'error': 'missing, non-file or symlink'})
            continue
        data = path.read_bytes()
        if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
            failures.append({'path': record['path'], 'error': 'size or SHA-256 mismatch'})

    actual = {
        path.relative_to(root).as_posix()
        for path in root.rglob('*')
        if path.is_file() and not operationally_excluded(path.relative_to(root))
    }
    for unexpected in sorted(actual - listed):
        failures.append({'path': unexpected, 'error': 'unlisted file'})
    for absent in sorted(listed - actual):
        if not any(item['path'] == absent for item in failures):
            failures.append({'path': absent, 'error': 'listed path absent from package inventory'})

    return {'status': 'FAIL' if failures else 'PASS',
            'listed_files_checked': len(listed),
            'actual_files_checked': len(actual), 'failures': failures}


if __name__ == '__main__':
    report = verify_package(Path(__file__).resolve().parents[1])
    print(json.dumps(report, indent=2, allow_nan=False))
    sys.exit(1 if report['failures'] else 0)
