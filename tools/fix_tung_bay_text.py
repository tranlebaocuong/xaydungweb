#!/usr/bin/env python3
"""Apply conservative spelling and spacing fixes for Oanh Vu Tung Bay texts."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("data/oanh_vũ/tung_bay")
IMAGE_MARKDOWN = re.compile(r"^\s*!\[[^\]]*\]\([^)]+\)\s*$")

REPLACEMENTS = {
    "ca dao,tục ngữ": "ca dao, tục ngữ",
    "Thiên nhiên,quê hương": "Thiên nhiên, quê hương",
    "Khái niệm:Tường thuật": "Khái niệm: Tường thuật",
    "Bố cục:Mở bài": "Bố cục: Mở bài",
    "Bản tên,GĐ": "Bản tên, GĐ",
    "Tài thí:Tài": "Tài thí: Tài",
    "Pháp Danh:Tâm": "Pháp Danh: Tâm",
    "Pháp Danh: Tâm Chánh..": "Pháp Danh: Tâm Chánh.",
    "MỤC ĐÍCH:Giúp": "MỤC ĐÍCH: Giúp",
    "cha mẹ,cha": "cha mẹ, cha",
    "lớn,sức": "lớn, sức",
    "phương tiện chính là xe đạp": "phương tiện chính là xe đạp",
    "gia thông": "giao thông",
    "sỡ hữu": "sở hữu",
    "thể hịên": "thể hiện",
    "cóthể": "có thể",
    "Trò chơi lớn,Trò chơi": "Trò chơi lớn, Trò chơi",
    "củathiếunhi": "của thiếu nhi",
    "Đácầu": "Đá cầu",
    "Đoàn,cách": "Đoàn, cách",
    "địa phương,v.v": "địa phương, v.v",
    "nhiếp tâm,Tam": "nhiếp tâm, Tam",
    "Cát Tường,Ấn": "Cát Tường, Ấn",
    "đồng phục.Trong": "đồng phục. Trong",
    "Quán Thế Âm.Từ": "Quán Thế Âm. Từ",
    "tinh thần.Chung": "tinh thần. Chung",
    "bảo vệ.Hiện": "bảo vệ. Hiện",
    "vắng mặt.Cướp": "vắng mặt. Cướp",
    "người khác.Tà": "người khác. Tà",
    "lợi ích.Thực": "lợi ích. Thực",
    "gia đình.Ngoài": "gia đình. Ngoài",
    "xì ke.Những": "xì ke. Những",
    "khó khăn.Công": "khó khăn. Công",
    "yếu tố.Tính": "yếu tố. Tính",
    "giản.Phần": "giản. Phần",
    "tốt.Tính": "tốt. Tính",
    "chơi.Hoặc": "chơi. Hoặc",
    "lều trại.Ngoài": "lều trại. Ngoài",
    "mặt đất.Dựng": "mặt đất. Dựng",
    "cây thấp.Cũng": "cây thấp. Cũng",
    "đi trại.Vì": "đi trại. Vì",
    "tiêu chảy.Phosphalugel": "tiêu chảy. Phosphalugel",
    "ợ nóng.Motilium": "ợ nóng. Motilium",
    "hằng tuần": "hằng tuần",
}


def fix_line(line: str) -> str:
    if IMAGE_MARKDOWN.match(line):
        return line.rstrip()

    text = line.rstrip()
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)

    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"([,;:!?])(?=[^\s])", r"\1 ", text)
    text = re.sub(r"(?<=[A-Za-zÀ-ỹĐđ0-9])\.(?=[A-ZÀ-ỸĐ0-9])", ". ", text)
    text = re.sub(r"^([A-ZÀ-ỸĐ])\.([A-ZÀ-ỸĐ])", r"\1. \2", text)
    text = re.sub(r"^([IVXLCDM]+)\.([A-ZÀ-ỸĐ])", r"\1. \2", text, flags=re.I)
    text = text.replace("v. v.", "v.v.")
    text = text.replace("...", "...")
    return text


def main() -> int:
    changed: list[Path] = []
    for path in sorted(ROOT.rglob("*.txt")):
        original = path.read_text(encoding="utf-8")
        fixed = "\n".join(fix_line(line) for line in original.splitlines())
        if original.endswith("\n"):
            fixed += "\n"
        if fixed != original:
            path.write_text(fixed, encoding="utf-8")
            changed.append(path)
            safe = str(path).encode("ascii", errors="backslashreplace").decode("ascii")
            print(f"UPDATED: {safe}")

    print(f"Scanned: {len(list(ROOT.rglob('*.txt')))}")
    print(f"Updated: {len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
