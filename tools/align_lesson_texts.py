#!/usr/bin/env python3
"""Normalize lesson text line breaks while preserving image markdown lines."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path("data")
IMAGE_MARKDOWN = re.compile(r"^\s*!\[[^\]]*\]\([^)]+\)\s*$")
HEADING = re.compile(
    r"^(?:[IVXLCDM]+\s*[-./]|[A-Z]\s*[-./)]|\d+\s*[-.)/])\s*",
    re.IGNORECASE,
)
UPPER_CHARS = re.compile(r"[A-ZÀ-ỸĐ]")
SENTENCE_END = re.compile(r'[.!?…。:”")\]]$')


def collapse_spaces(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())


def is_image_line(line: str) -> bool:
    return bool(IMAGE_MARKDOWN.match(line))


def is_heading(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if HEADING.match(stripped):
        return True
    return (
        stripped == stripped.upper()
        and len(stripped) > 2
        and bool(UPPER_CHARS.search(stripped))
    )


def starts_new_sentence(line: str) -> bool:
    return bool(re.match(r"^[A-ZÀ-ỸĐ0-9-]", line.strip()))


def starts_lowercase(line: str) -> bool:
    return bool(re.match(r"^[a-zà-ỹđ]", line.strip()))


def ends_sentence(line: str) -> bool:
    return bool(SENTENCE_END.search(line.strip()))


def split_inline_dialogue(line: str) -> list[str]:
    match = re.match(r"^(.{1,90}[:;])\s+(-\s+.+)$", line)
    if not match:
        return [line]
    return [match.group(1), match.group(2)]


def should_start_new_block(previous: str, current: str) -> bool:
    if not previous:
        return False
    if current.startswith("- ") and not previous.startswith("- "):
        return True
    if is_heading(current):
        return True
    if is_heading(previous) and not (":" in previous and starts_lowercase(current)):
        return True
    return ends_sentence(previous) and starts_new_sentence(current)


def normalize_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines()
    output: list[str] = []
    block: list[str] = []

    def flush_block() -> None:
        nonlocal block
        if not block:
            return
        output.append(collapse_spaces(" ".join(block)))
        block = []

    def append_blank() -> None:
        if output and output[-1] != "":
            output.append("")

    for raw_line in lines:
        if is_image_line(raw_line):
            flush_block()
            output.append(raw_line.rstrip("\r\n"))
            continue

        collapsed_line = collapse_spaces(raw_line)
        if not collapsed_line:
            flush_block()
            append_blank()
            continue

        for line in split_inline_dialogue(collapsed_line):
            previous = block[-1] if block else ""
            if should_start_new_block(previous, line):
                flush_block()
            block.append(line)

    flush_block()

    while output and output[-1] == "":
        output.pop()

    normalized = "\n".join(output)
    if normalized:
        normalized += "\n"

    if normalized == original:
        return False

    path.write_text(normalized, encoding="utf-8")
    return True


def safe_path(path: Path) -> str:
    return str(path).encode("ascii", errors="backslashreplace").decode("ascii")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    if not root.exists():
        print(f"{root}/ not found")
        return 2

    changed = []
    files = list(root.rglob("*.txt"))
    for path in sorted(files):
        if normalize_file(path):
            changed.append(path)
            print(f"UPDATED: {safe_path(path)}")

    print(f"Scanned: {len(files)}")
    print(f"Updated: {len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
