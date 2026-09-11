#!/usr/bin/env python3
"""Bind the human-readable finite table and claim register to the exact contract."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile
from verify_exact import load_contract


ROW = re.compile(r'^\|\s*([0-9,]+)\s*\|\s*([0-9,]+)\s*\|\s*([0-9]+\.[0-9]+)\s*\|$')


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def verify_claim_surface(root: Path, paper_path: Path | None = None) -> dict:
    root = root.resolve()
    contract = load_contract(root / 'certificate_contract.json')
    claims = json.loads((root / 'claims.json').read_text(encoding='utf-8'))
    paper = (paper_path or root / 'paper.md').read_text(encoding='utf-8')
    headline = [
        r'B_0:=\frac32e^{-1/2}-4e^{-3}',
        r'=\frac{5}{2e}-13e^{-4}',
        r'\frac{29}{1000}&<B_0-D_0<\frac{291}{10000}',
        r'&=\frac{5730077809}{8174960640}',
        r'> D_0+\frac{19}{1000}',
    ]
    for formula in headline:
        expected_count = 2 if formula == r'=\frac{5}{2e}-13e^{-4}' else 1
        require(paper.count(formula) == expected_count,
                'headline formula differs from exact contract: ' + formula)
    indexed = {item['id']: item for item in claims['claims']}
    require(indexed['T1_FINITE']['certificate'] ==
            contract['finite_moment_witness']['witness'] +
            ' > conjectured Poisson TV + ' +
            contract['finite_moment_witness']['exceeds_D_by_more_than'],
            'finite-moment claim register differs from exact contract')

    rows = []
    for line in paper.splitlines():
        match = ROW.match(line)
        if match:
            rows.append({
                'N': int(match.group(1).replace(',', '')),
                't': int(match.group(2).replace(',', '')),
                'b': '1/2',
                'published_lower': match.group(3),
            })
    require(rows == contract['finite_table'],
            'paper Table 1 differs from certificate_contract.json')
    require(claims.get('certificate_contract') == 'certificate_contract.json',
            'claim register does not identify the certificate contract')
    finite_claims = [item for item in claims['claims'] if item.get('id') == 'FINITE_TABLE']
    require(len(finite_claims) == 1, 'FINITE_TABLE claim missing or duplicated')
    require(finite_claims[0].get('location') ==
            'paper.md Table 1 and results/exact_verification.json',
            'FINITE_TABLE claim location mismatch')
    return {
        'status': 'PASS',
        'paper_table_rows_bound': len(rows),
        'headline_formulas_bound': len(headline),
        'contract': 'certificate_contract.json',
        'claim': 'FINITE_TABLE',
        'limitations': 'Binds enumerated publication fields; does not parse or verify the full prose proof.',
    }


def verify_documents(root: Path) -> dict:
    """Rebuild publication surfaces and compare TeX and extracted PDF text."""
    root = root.resolve()
    with tempfile.TemporaryDirectory(prefix='biased-doc-parity-') as tmp:
        out = Path(tmp)
        subprocess.run(['pandoc', 'paper.md', '--standalone',
                        '--include-in-header=code/pdf_header.tex',
                        '-o', str(out / 'paper.tex')], cwd=root, check=True)
        require((out / 'paper.tex').read_bytes() == (root / 'paper.tex').read_bytes(),
                'paper.tex differs from Markdown regeneration')
        subprocess.run(['pandoc', 'paper.md', '--standalone', '--pdf-engine=tectonic',
                        '--include-in-header=code/pdf_header.tex',
                        '-o', str(out / 'paper.pdf')], cwd=root, check=True)
        texts = [subprocess.check_output(['pdftotext', '-layout', str(p), '-'])
                 for p in [root / 'paper.pdf', out / 'paper.pdf']]
        require(texts[0] == texts[1], 'paper.pdf text differs from Markdown regeneration')
    return {'tex_regeneration': 'PASS', 'pdf_text_regeneration': 'PASS',
            'limitations': 'Text parity plus separate visual QA; not formal proof verification.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--paper', type=Path)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--documents', action='store_true')
    args = parser.parse_args()
    report = verify_claim_surface(args.root, args.paper)
    if args.documents:
        report['documents'] = verify_documents(args.root)
    text = json.dumps(report, indent=2, allow_nan=False) + '\n'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding='utf-8')
    print(text)
