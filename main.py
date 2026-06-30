import argparse
import json
import mimetypes
import re
import sys
import webbrowser
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

HOST = "127.0.0.1"
PORT = 8000
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_ROOT = PROJECT_ROOT / "data"

DISPLAY_NAMES = {
    "oanh_vũ": "NGÀNH ĐỒNG",
    "ngành_thiếu": "NGÀNH THIẾU",
}

FOLDER_ORDER = {
    "oanh_vũ": 10,
    "ngành_thiếu": 20,
    "mở_mắt": 10,
    "cánh_mềm": 20,
    "chân_cứng": 30,
    "tung_bay": 40,
    "hướng_thiện": 10,
    "sơ_thiện": 20,
    "trung_thiện": 30,
    "chánh_thiện": 40,
    "phật pháp": 10,
    "phật_pháp": 10,
    "hoạt_động_thanh_niên": 20,
    "hoạt_động_thanh_niên_và_xã_hội": 20,
    "hoạt_động_xã_hội": 30,
    "văn_nghệ": 40,
}


def setup_utf8_console():
    if sys.platform != "win32":
        return
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if stream is not None and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (OSError, ValueError, AttributeError):
                pass


def display_name(path):
    name = path.name
    if name in DISPLAY_NAMES:
        return DISPLAY_NAMES[name]
    return name.replace("_", " ").upper()


def natural_sort_key(path):
    name = path.name.lower()
    folder_rank = FOLDER_ORDER.get(name, 999)
    parts = [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", name)]
    return (folder_rank, parts)


def relative_posix(path):
    return path.relative_to(PROJECT_ROOT).as_posix()


def resolve_data_path(raw_path):
    if not raw_path:
        raise ValueError("Thiếu tham số path.")

    decoded = unquote(raw_path).replace("\\", "/").lstrip("/")
    target = (PROJECT_ROOT / decoded).resolve()
    data_root = DATA_ROOT.resolve()

    if not target.is_relative_to(data_root):
        raise ValueError("Path phải nằm trong thư mục data.")
    if not target.is_file():
        raise FileNotFoundError("Không tìm thấy bài học.")
    if target.suffix.lower() != ".txt":
        raise ValueError("Chỉ hỗ trợ file .txt.")
    return target


def fallback_title(path):
    stem = path.stem.replace("_", " ")
    return stem[:1].upper() + stem[1:]


def is_likely_title_continuation(text):
    without_parentheses = re.sub(r"\([^)]*\)", "", text)
    letters = re.sub(r"[^A-Za-zÀ-ỹĐđ]", "", without_parentheses)
    has_lesson_part = re.search(r"\(\s*(?:\d+\s*)?tiết\s*\d*\s*\)", text, re.IGNORECASE)
    if not letters:
        return bool(has_lesson_part)
    return letters == letters.upper() and (bool(has_lesson_part) or len(text) <= 70)


def is_content_start_line(text):
    stripped = text.strip()
    if not stripped:
        return False
    patterns = [
        r"^\s*!\[[^\]]*\]\([^)]+\)\s*$",
        r"^\(.+\)$",
        r"^[IVXLCDM]+\s*[-./]\s*",
        r"^[A-Z]\s*[-./)]\s*",
        r"^[0-9]+\s*[-.)]\s+",
        r"^[-*+]\s+",
    ]
    return any(re.search(pattern, stripped, re.IGNORECASE) for pattern in patterns)


def has_lowercase_letter(text):
    return bool(re.search(r"[a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]", text))


def is_uppercase_title_line(text):
    letters = re.sub(r"[^A-Za-zÀ-ỹĐđ]", "", text)
    return bool(letters) and letters == letters.upper()


def parse_lesson_text(text, default_title):
    lines = text.splitlines()
    first_content_line = next((i for i, line in enumerate(lines) if line.strip()), -1)
    if first_content_line < 0:
        return {"title": default_title, "content": ""}

    title_lines = []
    content_start = first_content_line

    for index in range(first_content_line, len(lines)):
        trimmed = lines[index].strip()
        if not trimmed:
            content_start = index + 1
            break
        if title_lines and is_likely_title_continuation(trimmed):
            title_lines.append(trimmed)
            content_start = index + 1
            continue
        if title_lines and is_content_start_line(trimmed):
            content_start = index
            break
        if title_lines and is_uppercase_title_line(title_lines[-1]) and has_lowercase_letter(trimmed):
            content_start = index
            break
        if len(title_lines) >= 4:
            content_start = index
            break
        title_lines.append(trimmed)
        content_start = index + 1

    title = " ".join(title_lines).strip() or default_title
    content = "\n".join(lines[content_start:]).strip()
    return {"title": re.sub(r"\s+", " ", title), "content": content}


def read_lesson(path):
    text = path.read_text(encoding="utf-8")
    parsed = parse_lesson_text(text, fallback_title(path))
    parsed.update(
        {
            "path": relative_posix(path),
            "basePath": path.parent.relative_to(PROJECT_ROOT).as_posix(),
        }
    )
    return parsed


def build_tree(path):
    folders = sorted((item for item in path.iterdir() if item.is_dir()), key=natural_sort_key)
    files = sorted((item for item in path.iterdir() if item.is_file() and item.suffix.lower() == ".txt"), key=natural_sort_key)

    children = [build_tree(folder) for folder in folders]
    for file_path in files:
        lesson = read_lesson(file_path)
        children.append(
            {
                "type": "lesson",
                "name": lesson["title"],
                "path": lesson["path"],
                "basePath": lesson["basePath"],
            }
        )

    return {
        "type": "folder",
        "name": display_name(path),
        "path": relative_posix(path) if path != DATA_ROOT else "data",
        "children": children,
    }


class BackendHandler(SimpleHTTPRequestHandler):
    server_version = "TuHocBackend/1.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PROJECT_ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            self.send_json({"ok": True, "name": "Tài liệu tu học backend"})
            return
        if parsed.path == "/api/structure":
            self.handle_structure()
            return
        if parsed.path == "/api/lesson":
            self.handle_lesson(parsed.query)
            return
        super().do_GET()

    def handle_structure(self):
        if not DATA_ROOT.is_dir():
            self.send_error_json(HTTPStatus.NOT_FOUND, "Không tìm thấy thư mục data.")
            return
        self.send_json(build_tree(DATA_ROOT))

    def handle_lesson(self, query):
        params = parse_qs(query)
        raw_path = params.get("path", [""])[0]
        try:
            lesson_path = resolve_data_path(raw_path)
            self.send_json(read_lesson(lesson_path))
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
        if path.endswith(".txt"):
            return "text/plain; charset=utf-8"
        return mimetypes.guess_type(path)[0] or "application/octet-stream"


def serve(port=PORT, open_browser=True):
    setup_utf8_console()
    last_error = None
    for try_port in range(port, port + 10):
        try:
            with ThreadingHTTPServer((HOST, try_port), BackendHandler) as httpd:
                url = f"http://{HOST}:{try_port}/index.html"
                print(f"Backend đang chạy tại: http://{HOST}:{try_port}")
                print(f"Trang demo: {url}")
                print(f"API cấu trúc: http://{HOST}:{try_port}/api/structure")
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
    parser = argparse.ArgumentParser(description="Backend cho demo tài liệu tu học")
    parser.add_argument("--port", type=int, default=PORT, help="Cổng chạy server")
    parser.add_argument("--no-browser", action="store_true", help="Không tự mở trình duyệt")
    args = parser.parse_args()
    serve(port=args.port, open_browser=not args.no_browser)


if __name__ == "__main__":
    main()
