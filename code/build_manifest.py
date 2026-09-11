#!/usr/bin/env python3
"""Regenerate the complete package MANIFEST.json deterministically."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import verify_manifest


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    files = []
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if (not path.is_file() or path.is_symlink()
                or verify_manifest.operationally_excluded(relative)):
            continue
        data = path.read_bytes()
        files.append({
            'path': relative.as_posix(),
            'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(),
        })
    manifest = {'schema_version': '1.0', 'algorithm': 'sha256', 'files': files}
    (root / 'MANIFEST.json').write_text(
        json.dumps(manifest, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    print(json.dumps({'status': 'WROTE', 'files': len(files)}, indent=2))


if __name__ == '__main__':
    main()
