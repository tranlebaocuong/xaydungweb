import argparse
import http.server
import json
import os
import socketserver
import sys
import webbrowser
from pathlib import Path

SERVER_PORT = 8000
PROJECT_ROOT = Path(__file__).resolve().parent


def setup_utf8_console():
    """Configure UTF-8 encoding for console on Windows."""
    if sys.platform != "win32":
        return
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if stream is not None and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (OSError, ValueError, AttributeError):
                pass


def load_json(file_path):
    """Load JSON file with error handling."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
        raise
    except json.JSONDecodeError as e:
        print(f"File JSON không hợp lệ ({file_path}): {e}")
        raise
    except OSError as e:
        print(f"Không đọc được file: {e}")
        raise


def save_json(path, data):
    """Save JSON file with error handling."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except OSError as e:
        print(f"Không ghi được file ({path}): {e}")
        raise


def find_song_title(song_id, songs):
    """Find song title by ID."""
    for song in songs:
        if song.get("id") == song_id:
            return song.get("title", "không rõ")
    return "không rõ"


def add_song_menu(playlist, songs):
    """Display songs and add to playlist."""
    print("==== DANH SÁCH BÀI HÁT ==== ")
    for i, song in enumerate(songs, 1):
        print(f"{i}. {song['title']}")

    try:
        choice = input("thêm bài số mấy? (hoặc q để thoát): ").strip().lower()
    except (EOFError, UnicodeDecodeError):
        print("Không đọc được dữ liệu nhập.")
        return

    if choice == "q":
        return

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(songs):
            song_id = songs[idx]["id"]
            playlist.setdefault("song_ids", [])
            if song_id not in playlist["song_ids"]:
                playlist["song_ids"].append(song_id)
            else:
                print("đã có trong playlist")
        else:
            print("STT không hợp lệ")
    else:
        print("không có")


def remove_song_menu(playlist):
    """Remove song from playlist."""
    playlist.setdefault("song_ids", [])
    try:
        choice = input("xóa bài số mấy? (stt): ").strip()
    except (EOFError, UnicodeDecodeError):
        print("Không đọc được dữ liệu nhập.")
        return

    if not choice.isdigit():
        print("Vui lòng nhập STT hợp lệ.")
        return

    try:
        playlist["song_ids"].pop(int(choice) - 1)
    except IndexError:
        print("STT không hợp lệ")


def reorder_songs_menu(playlist):
    """Reorder songs in playlist."""
    playlist.setdefault("song_ids", [])
    try:
        old_idx = int(input("bai muốn chuyển (stt): ").strip()) - 1
        new_idx = int(input("vị trí mới (stt): ").strip()) - 1
        song_id = playlist["song_ids"].pop(old_idx)
        playlist["song_ids"].insert(new_idx, song_id)
    except ValueError:
        print("Vui lòng nhập số hợp lệ.")
    except IndexError:
        print("STT không hợp lệ.")


def manage_single_playlist(playlist, songs, all_playlists, playlists_path):
    """Interactive management for a single playlist."""
    while True:
        print(f"=== {playlist['name']} ===")
        song_ids = playlist.get("song_ids", [])
        if not song_ids:
            print("trống")
        else:
            for i, song_id in enumerate(song_ids, 1):
                print(f"{i}. {find_song_title(song_id, songs)}")

        print("(1). Thêm | (2). xóa | (3). đổi | (p) đổi playlist | (q) thoát")
        try:
            cmd = input("---> : ").strip().lower()
        except (EOFError, UnicodeDecodeError):
            return "exit"

        if cmd == "q":
            return "exit"
        if cmd == "p":
            return "back"

        if cmd == "1":
            add_song_menu(playlist, songs)
        elif cmd == "2":
            remove_song_menu(playlist)
        elif cmd == "3":
            reorder_songs_menu(playlist)

        try:
            save_json(playlists_path, all_playlists)
        except OSError:
            pass


def next_playlist_id(playlists):
    """Generate next available playlist ID."""
    return max((pl.get("id", 0) for pl in playlists), default=0) + 1


def manage_playlists():
    """Main playlist management CLI."""
    setup_utf8_console()
    songs_path = PROJECT_ROOT / "data" / "music" / "songs.json"
    playlists_path = PROJECT_ROOT / "data" / "music" / "playlists.json"

    try:
        songs = load_json(songs_path)
        playlists = load_json(playlists_path)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return

    while True:
        print("=== DANH SÁCH BÀI PLAYLIST ===")
        for i, playlist in enumerate(playlists, 1):
            print(f"{i}. {playlist['name']}")
        print("(n). tạo mới | (q). thoát")

        try:
            choice = input("chọn: ").strip().lower()
        except (EOFError, UnicodeDecodeError):
            break

        if choice == "q":
            break

        if choice == "n":
            try:
                name = input("tên playlist mới: ").strip()
            except (EOFError, UnicodeDecodeError):
                break
            if name:
                new_id = next_playlist_id(playlists)
                playlists.append({"id": new_id, "name": name, "song_ids": []})
                try:
                    save_json(playlists_path, playlists)
                except OSError:
                    playlists.pop()
                    continue
                print(f" đã tạo playlist '{name}'")
            continue

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(playlists):
                result = manage_single_playlist(playlists[idx], songs, playlists, playlists_path)
                if result == "exit":
                    break
            else:
                print("playlist không tồn tại")


def serve_demo(port=SERVER_PORT, open_browser=True):
    """Serve the demo web application."""
    demo_dir = PROJECT_ROOT
    if not demo_dir.is_dir():
        print(f"Không tìm thấy thư mục demo: {demo_dir}")
        return

    os.chdir(str(demo_dir))
    handler = http.server.SimpleHTTPRequestHandler

    last_error = None
    for try_port in range(port, port + 10):
        try:
            with socketserver.ThreadingTCPServer(("127.0.0.1", try_port), handler) as httpd:
                url = f"http://127.0.0.1:{try_port}/index.html"
                print(f"Đang phục vụ demo tại: {url}")
                if open_browser:
                    webbrowser.open(url)
                httpd.serve_forever()
                return
        except OSError as e:
            last_error = e
            if getattr(e, "errno", None) in (98, 10048):
                continue
            print(f"Không thể mở server trên cổng {try_port}: {e}")
            return

    print(f"Không thể mở server trên cổng {port}-{port + 9}: {last_error}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Music utility and demo server launcher")
    parser.add_argument("--demo", action="store_true", help="Serve the hướng_thiện demo site")
    parser.add_argument("--port", type=int, default=SERVER_PORT, help="Port for the demo server")
    parser.add_argument("--playlist", action="store_true", help="Manage playlists")
    args = parser.parse_args()

    if args.demo:
        serve_demo(port=args.port)
    elif args.playlist:
        manage_playlists()
    else:
        print("Sử dụng --demo để mở trang demo hoặc --playlist để quản lý playlist.")


if __name__ == "__main__":
    main()

