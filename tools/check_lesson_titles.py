#!/usr/bin/env python3
"""Check parsed lesson titles for lines that likely include lesson body text."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("data")


def is_image_markdown_line(line: str) -> bool:
    return bool(re.match(r"^\s*!\[[^\]]*\]\([^)]+\)\s*$", line))


def is_content_start_line(line: str) -> bool:
    trimmed = line.strip()
    if not trimmed:
        return False
    if is_image_markdown_line(trimmed):
        return True
    if re.match(r"^\(.+\)$", trimmed):
        return True
    if re.match(r"^[IVXLCDM]+\s*[-./]\s*", trimmed, flags=re.I):
        return True
    if re.match(r"^[A-Z]\s*[-./)]\s*", trimmed):
        return True
    if re.match(r"^[0-9]+\s*[-.)]\s+", trimmed):
        return True
    if re.match(r"^[-*+]\s+", trimmed):
        return True
    return False


def has_lowercase_letter(text: str) -> bool:
    return bool(
        re.search(
            r"[a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]",
            text,
        )
    )


def is_uppercase_title_line(text: str) -> bool:
    letters = re.sub(r"[^A-Za-zÀ-ỹĐđ]", "", text)
    return bool(letters) and letters == letters.upper()


def is_likely_title_continuation_line(text: str) -> bool:
    without_parentheses = re.sub(r"\([^)]*\)", "", text)
    letters = re.sub(r"[^A-Za-zÀ-ỹĐđ]", "", without_parentheses)
    has_lesson_part = bool(re.search(r"\(\s*(?:\d+\s*)?tiết\s*\d*\s*\)", text, flags=re.I))
    if not letters:
        return has_lesson_part
    return letters == letters.upper() and (has_lesson_part or len(text) <= 70)


def parse_title(text: str, fallback: str) -> str:
    lines = text.splitlines()
    first_content_line = next((i for i, line in enumerate(lines) if line.strip()), -1)
    if first_content_line < 0:
        return fallback

    title_lines: list[str] = []
    for i in range(first_content_line, len(lines)):
        trimmed = lines[i].strip()
        if not trimmed:
            break
        if title_lines and is_likely_title_continuation_line(trimmed):
            title_lines.append(trimmed)
            continue
        if title_lines and is_content_start_line(trimmed):
            break
        if title_lines and is_uppercase_title_line(title_lines[-1]) and has_lowercase_letter(trimmed):
            break
        if len(title_lines) >= 4:
            break
        title_lines.append(trimmed)

    return re.sub(r"\s+", " ", " ".join(title_lines)).strip() or fallback


def safe(text: object) -> str:
    return str(text).encode("ascii", errors="backslashreplace").decode("ascii")


def main() -> int:
    suspicious: list[tuple[Path, str]] = []

    for path in sorted(ROOT.rglob("*.txt")):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        title = parse_title(text, path.stem)
        if (
            len(title) > 180
            or re.search(r"\b(?:I|II|III|IV|V)\s*[/.-]\s+(?:MỤC|NỘI|CÂU|CHUẨN)", title, flags=re.I)
            or re.search(r"\b(?:Mục đích|Nội dung|Chuẩn bị|Câu hỏi)\s*:", title, flags=re.I)
        ):
            suspicious.append((path, title))

    print(f"Files checked: {sum(1 for _ in ROOT.rglob('*.txt'))}")
    print(f"Suspicious titles: {len(suspicious)}")
    for path, title in suspicious:
        print(f"{safe(path)}")
        print(f"  {safe(title)}")

    return 1 if suspicious else 0


if __name__ == "__main__":
    raise SystemExit(main())
