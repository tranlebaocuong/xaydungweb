#!/usr/bin/env python3
"""Fix conservative spelling and punctuation issues in lesson text files."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path("data")
IMAGE_MARKDOWN = re.compile(r"^\s*!\[[^\]]*\]\([^)]+\)\s*$")

REPLACEMENTS = {
    "gốc rế": "gốc rễ",
    "Gốc rế": "Gốc rễ",
    "trãi": "trải",
    "Trãi": "Trải",
    "trổi dậy": "trỗi dậy",
    "Trổi dậy": "Trỗi dậy",
    "yên tỉnh": "yên tĩnh",
    "Yên tỉnh": "Yên tĩnh",
    "háp tay": "áp tay",
    "Háp tay": "Áp tay",
    "mà sác": "màu sắc",
    "Mà sác": "Màu sắc",
    "bàng cách": "bằng cách",
    "Bàng cách": "Bằng cách",
    "hòa kình": "hòa kính",
    "Hòa kình": "Hòa kính",
    "hòa kỉnh": "hòa kính",
    "Hòa kỉnh": "Hòa kính",
    "nầy": "này",
    "Nầy": "Này",
    "ngợigì": "ngợi gì",
    "Ngợigì": "Ngợi gì",
    "gúy bồ câu": "gút bồ câu",
    "Gúy bồ câu": "Gút bồ câu",
    "co pha muối": "có pha muối",
    "Co pha muối": "Có pha muối",
    "ôn ủi": "an ủi",
    "Ôn ủi": "An ủi",
    "dành làm hết": "giành làm hết",
    "Dành làm hết": "Giành làm hết",
    "bênh viện": "bệnh viện",
    "Bênh viện": "Bệnh viện",
    "dành iêng": "dành riêng",
    "Dành iêng": "Dành riêng",
    "jđiều": "j đều",
    "Jđiều": "J đều",
}


def fix_punctuation(line: str) -> str:
    if IMAGE_MARKDOWN.match(line):
        return line.rstrip()

    result = line.rstrip()

    for old, new in REPLACEMENTS.items():
        result = result.replace(old, new)

    result = re.sub(r"\s+([,.;:!?])", r"\1", result)
    result = re.sub(r"([,;:])(?=[^\s\d])", r"\1 ", result)
    result = re.sub(r"(?<!\.)\.(?=[A-ZÀ-ỸĐ])", ". ", result)
    result = re.sub(r"^-\s*(?=\S)", "- ", result)
    result = re.sub(r"\s{2,}", " ", result)
    result = result.replace(" .", ".")
    return result


def fix_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    fixed = "\n".join(fix_punctuation(line) for line in original.splitlines())
    if original.endswith("\n"):
        fixed += "\n"
    if fixed == original:
        return False
    path.write_text(fixed, encoding="utf-8")
    return True


def safe(path: Path) -> str:
    return str(path).encode("ascii", errors="backslashreplace").decode("ascii")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    changed: list[Path] = []
    for path in sorted(root.rglob("*.txt")):
        if fix_file(path):
            changed.append(path)
            print(f"UPDATED: {safe(path)}")

    print(f"Scanned: {sum(1 for _ in root.rglob('*.txt'))}")
    print(f"Updated: {len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
