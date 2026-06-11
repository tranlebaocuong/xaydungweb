#!/usr/bin/env python3
"""
Walk data/ for common image extensions and check HTTP status via localhost:8000.
Print summary and non-200 responses.
"""
import sys
from pathlib import Path
from urllib import request, parse

root = Path('data')
if not root.exists():
    print('data/ not found')
    sys.exit(2)

exts = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp'}
files = [p for p in root.rglob('*') if p.suffix.lower() in exts]
print(f'Found {len(files)} images')

errors = []
for p in files:
    rel = str(p).replace('\\', '/')
    url = 'http://localhost:8000/' + parse.quote(rel, safe='/:')
    try:
        resp = request.urlopen(url, timeout=10)
        code = resp.getcode()
        if code != 200:
            errors.append((rel, code))
            print(f'BAD: {rel} -> HTTP {code}')
    except Exception as e:
        errors.append((rel, str(e)))
        print(f'ERR: {rel} -> {e}')

print('\nSummary:')
print(f'  total images: {len(files)}')
print(f'  errors: {len(errors)}')
if errors:
    print('\nExamples:')
    for e in errors[:30]:
        print(' ', e)

sys.exit(0 if not errors else 1)
