#!/usr/bin/env python3
"""
Normalize text files under data/:
- ensure UTF-8 encoding
- remove trailing whitespace
- collapse multiple spaces into single (except leading indentation)
- remove trailing blank lines
- create a backup with .bak extension before modifying
"""
import sys
from pathlib import Path

def normalize_text(path: Path) -> bool:
    try:
        raw = path.read_text(encoding='utf-8')
    except Exception:
        try:
            raw = path.read_text(encoding='latin-1')
        except Exception:
            print(f"SKIP (encoding): {path}")
            return False

    orig = raw
    lines = raw.splitlines()
    out_lines = []
    for ln in lines:
        # preserve leading tabs/spaces; collapse interior multi-spaces
        if ln.strip() == '':
            out_lines.append('')
            continue
        leading = ''
        i = 0
        while i < len(ln) and ln[i] in (' ', '\t'):
            leading += ln[i]
            i += 1
        body = ln[i:]
        # collapse multiple spaces inside body
        import re
        body = re.sub(r' {2,}', ' ', body)
        # strip trailing whitespace
        body = body.rstrip()
        out_lines.append(leading + body)

    # remove trailing blank lines
    while len(out_lines) > 0 and out_lines[-1] == '':
        out_lines.pop()

    new = '\n'.join(out_lines) + ('\n' if out_lines else '')
    if new != orig:
        bak = path.with_suffix(path.suffix + '.bak')
        try:
            path.rename(path.with_suffix(path.suffix + '.orig'))
            bak.write_text(orig, encoding='utf-8')
            path.write_text(new, encoding='utf-8')
            # restore original name for .orig to .txt for compatibility
            path.with_suffix(path.suffix + '.orig').rename(path.with_suffix(path.suffix))
        except Exception:
            # fallback: write backup and overwrite
            bak.write_text(orig, encoding='utf-8')
            path.write_text(new, encoding='utf-8')
        print(f"MODIFIED: {path}")
        return True
    return False


def main():
    root = Path('data')
    if not root.exists():
        print('data/ not found')
        return 2
    files = list(root.rglob('*.txt'))
    modified = 0
    for f in files:
        if normalize_text(f):
            modified += 1
    print(f"Total files scanned: {len(files)}, modified: {modified}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
