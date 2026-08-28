import argparse
import json
import re
import sys
import webbrowser
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HOST = "127.0.0.1"
PORT = 8000
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_ROOT = PROJECT_ROOT / "data"


def fallback_title(path: Path) -> str:
    name = path.stem.replace("_", " ").replace("-", " ")
    clean = " ".join(part for part in re.split(r"\s+", name) if part)
    return clean.strip() or path.parent.name


def is_image_markdown_line(line: str) -> bool:
    return bool(re.fullmatch(r"\s*!\[[^\]]*\]\([^)]+\)\s*", line))


def is_content_start_line(line: str) -> bool:
    trimmed = line.strip()
    if not trimmed:
        return False
    if is_image_markdown_line(trimmed):
        return True
    if re.fullmatch(r"\(.+\)", trimmed):
        return True
    if re.fullmatch(r"[IVXLCDM]+\s*[-./]\s*.*", trimmed, flags=re.IGNORECASE):
        return True
    if re.fullmatch(r"[A-Z]\s*[-./)]\s*.*", trimmed):
        return True
    if re.fullmatch(r"[0-9]+\s*[-.)]\s+.*", trimmed):
        return True
    if re.fullmatch(r"[-*+]\s+.*", trimmed):
        return True
    return False


def has_lowercase_letter(text: str) -> bool:
    return bool(re.search(r"[a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]", text))


def is_uppercase_title_line(text: str) -> bool:
    letters = re.sub(r"[^A-Za-zÀ-ỹĐđ]", "", text)
    return bool(letters) and letters == letters.upper()


def is_likely_title_continuation_line(text: str) -> bool:
    without_parentheses = re.sub(r"\([^)]*\)", "", text)
    letters = re.sub(r"[^A-Za-zÀ-ỹĐđ]", "", without_parentheses)
    has_lesson_part = bool(re.search(r"\(\s*(?:\d+\s*)?tiết\s*\d*\s*\)", text, flags=re.IGNORECASE))
    if not letters:
        return has_lesson_part
    return letters == letters.upper() and (has_lesson_part or len(text) <= 70)


def parse_lesson_text(text: str, fallback_title_value: str = "Giới thiệu") -> dict:
    lines = text.splitlines()
    first_content_line = next((i for i, line in enumerate(lines) if line.strip()), None)
    if first_content_line is None:
        return {"title": fallback_title_value, "content": ""}

    title_lines: list[str] = []
    content_start = first_content_line

    for i in range(first_content_line, len(lines)):
        trimmed = lines[i].strip()
        if not trimmed:
            content_start = i + 1
            break
        if title_lines and is_likely_title_continuation_line(trimmed):
            title_lines.append(trimmed)
            content_start = i + 1
            continue
        if title_lines and is_content_start_line(trimmed):
            content_start = i
            break
        if title_lines and is_uppercase_title_line(title_lines[-1]) and has_lowercase_letter(trimmed):
            content_start = i
            break
        if len(title_lines) >= 4:
            content_start = i
            break
        title_lines.append(trimmed)
        content_start = i + 1

    title = " ".join(title_lines) if title_lines else fallback_title_value
    title = re.sub(r"\s+", " ", title).strip() or fallback_title_value
    content = "\n".join(lines[content_start:]).strip()
    return {"title": title, "content": content}


def setup_utf8_console():
    if sys.platform != "win32":
        return
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if stream is None:
            continue
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError, AttributeError):
                pass


def build_data_structure(root: Path) -> list[dict]:
    if not root.exists():
        return []

    items: list[dict] = []
    for child in sorted(root.iterdir(), key=lambda p: p.name.casefold()):
        if child.name.startswith("."):
            continue
        item: dict = {"name": child.name, "path": child.relative_to(PROJECT_ROOT).as_posix()}
        if child.is_dir():
            item["type"] = "directory"
            item["children"] = build_data_structure(child)
        elif child.is_file() and child.suffix.lower() == ".txt":
            item["type"] = "file"
        else:
            continue
        items.append(item)
    return items


class DemoHandler(SimpleHTTPRequestHandler):
    server_version = "TuHocDemo/2.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PROJECT_ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            self.send_json({"ok": True, "name": "Tài liệu tu học"})
            return
        if parsed.path == "/api/structure":
            self.handle_structure()
            return
        if parsed.path == "/api/lesson":
            self.handle_lesson(parsed.query)
            return
        if parsed.path in ("", "/"):
            self.path = "/index.html"
        super().do_GET()

    def handle_structure(self):
        self.send_json({
            "ok": True,
            "root": DATA_ROOT.relative_to(PROJECT_ROOT).as_posix(),
            "structure": build_data_structure(DATA_ROOT),
        })

    def handle_lesson(self, query):
        params = parse_qs(query)
        raw_path = params.get("path", [""])[0]
        if not raw_path:
            self.send_error_json(HTTPStatus.BAD_REQUEST, "Thiếu tham số path")
            return

        try:
            decoded = raw_path.replace("\\", "/").lstrip("/")
            target = (PROJECT_ROOT / decoded).resolve()
            if not str(target).startswith(str(PROJECT_ROOT.resolve())):
                raise ValueError("Path không hợp lệ")
            if not target.exists() or not target.is_file():
                raise FileNotFoundError("Không tìm thấy file")
            if target.suffix.lower() != ".txt":
                raise ValueError("Chỉ hỗ trợ file .txt")

            content = target.read_text(encoding="utf-8")
            parsed = parse_lesson_text(content, fallback_title(target))
            self.send_json({
                "path": target.relative_to(PROJECT_ROOT).as_posix(),
                "basePath": target.parent.relative_to(PROJECT_ROOT).as_posix(),
                "title": parsed["title"],
                "content": parsed["content"],
            })
        except FileNotFoundError as error:
            self.send_error_json(HTTPStatus.NOT_FOUND, str(error))
        except (OSError, UnicodeDecodeError, ValueError) as error:
            self.send_error_json(HTTPStatus.BAD_REQUEST, str(error))

    def send_json(self, payload, status=HTTPStatus.OK):
        data = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_error_json(self, status, message):
        self.send_json({"ok": False, "error": message}, status=status)

    def guess_type(self, path):
        path_text = str(path)
        if path_text.endswith(".txt"):
            return "text/plain; charset=utf-8"
        return super().guess_type(path_text)


def serve(port=PORT, open_browser=True):
    setup_utf8_console()
    last_error = None
    for try_port in range(port, port + 10):
        try:
            with ThreadingHTTPServer((HOST, try_port), DemoHandler) as httpd:
                url = f"http://{HOST}:{try_port}/index.html"
                print(f"Server đang chạy tại: {url}")
                if open_browser:
                    webbrowser.open(url)
                httpd.serve_forever()
                return
        except OSError as error:
            last_error = error
            if getattr(error, "errno", None) in (98, 10048):
                continue
            raise
    print(f"Không thể mở server trên cổng {port}-{port + 9}: {last_error}")


def main():
    parser = argparse.ArgumentParser(description="Server cho demo tài liệu tu học")
    parser.add_argument("--host", default=HOST, help="Địa chỉ host")
    parser.add_argument("--port", type=int, default=PORT, help="Cổng chạy server")
    parser.add_argument("--no-browser", action="store_true", help="Không tự mở trình duyệt")
    args = parser.parse_args()
    serve(port=args.port, open_browser=not args.no_browser)


if __name__ == "__main__":
    main()
