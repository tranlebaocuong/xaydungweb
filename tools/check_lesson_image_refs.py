#!/usr/bin/env python3
"""Check markdown image references in lesson text files."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote


ROOT = Path("data")
IMAGE_REF = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def resolve_refs(txt_path: Path, src: str) -> list[Path]:
    raw = unquote(src.strip().replace("\\", "/").lstrip("./"))
    if not raw or re.match(r"^(https?:|data:|/)", raw, flags=re.I):
        return []

    base_dir = txt_path.parent
    if raw.lower().startswith("ảnh_bài_"):
        return [base_dir / "ảnh" / raw, base_dir / raw]
    return [base_dir / raw]


def safe(text: object) -> str:
    return str(text).encode("ascii", errors="backslashreplace").decode("ascii")


def main() -> int:
    missing: list[tuple[Path, int, str, Path]] = []
    total = 0

    for txt_path in sorted(ROOT.rglob("*.txt")):
        try:
            lines = txt_path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue

        for line_no, line in enumerate(lines, 1):
            for match in IMAGE_REF.finditer(line):
                total += 1
                src = match.group(1)
                resolved = resolve_refs(txt_path, src)
                if resolved and not any(path.exists() for path in resolved):
                    missing.append((txt_path, line_no, src, resolved[0]))

    print(f"Image refs scanned: {total}")
    print(f"Missing refs: {len(missing)}")
    for txt_path, line_no, src, resolved in missing:
        print(f"{safe(txt_path)}:{line_no}")
        print(f"  src: {safe(src)}")
        print(f"  expected: {safe(resolved)}")

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
