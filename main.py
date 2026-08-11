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


def setup_utf8_console():
    if sys.platform != "win32":
        return
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if stream is not None and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (OSError, ValueError, AttributeError):
                pass


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
        if parsed.path == "/api/lesson":
            self.handle_lesson(parsed.query)
            return
        if parsed.path in ("", "/"):
            self.path = "/index.html"
        super().do_GET()

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
        if path.endswith(".txt"):
            return "text/plain; charset=utf-8"
        return super().guess_type(path)


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
