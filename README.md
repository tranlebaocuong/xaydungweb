# Demo Tài liệu Tu Học

Đây là demo web cho bộ tài liệu tu học. Giao diện dùng HTML/CSS/JavaScript, backend Python phục vụ web tĩnh và cung cấp API đọc dữ liệu bài học từ thư mục `data/`.

## Nội dung hiện có

Demo hiện hỗ trợ:

- `NGÀNH THIẾU`
  - `HƯỚNG THIỆN`
  - `SƠ THIỆN`
- `OANH VŨ`
  - `MỞ MẮT`
  - `CÁNH MỀM`
  - `CHÂN CỨNG`

Mỗi mục có các phần như `PHẬT PHÁP`, `HOẠT ĐỘNG THANH NIÊN`, `HOẠT ĐỘNG XÃ HỘI`, `VĂN NGHỆ`, và các bài học được lưu trong thư mục `data/`.

## Cách chạy demo

1. Mở PowerShell hoặc terminal ở thư mục gốc `a:\xaydungweb`.
2. Chạy lệnh:

```powershell
python main.py --port 8000
```

Hoặc dùng lệnh cũ, hiện đã được nối sang backend mới:

```powershell
python music.py --demo --port 8000
```

3. Nếu cổng `8000` đã bị chiếm, backend sẽ tự động thử các cổng tiếp theo từ `8000` đến `8009`.
4. Mở trình duyệt và truy cập URL được in ra, thường là:

```
http://127.0.0.1:8000/index.html
```

## Chạy nhanh trên Windows

- `start_demo.ps1`
- `start_demo.bat`

Các script này chạy backend từ thư mục chứa file.

## API backend

- `GET /api/health` — kiểm tra backend đang chạy
- `GET /api/structure` — trả về cây thư mục/bài học trong `data/`
- `GET /api/lesson?path=data/.../bài_1.txt` — trả về tiêu đề và nội dung bài học

## Tại sao phải dùng server HTTP

Trang demo sử dụng `fetch()` trong `script.js` để tải nội dung từ file `.txt`. Vì vậy, nếu mở `index.html` bằng `file://`, nội dung sẽ không tải được và có thể gặp lỗi.

Server HTTP giúp:

- phục vụ các file `index.html`, `styles.css`, `script.js` đúng cách
- tải nội dung bài học qua HTTP
- tránh lỗi `fetch` khi mở trực tiếp từ file local

## Các tệp quan trọng

- `index.html` — giao diện trang demo
- `styles.css` — phong cách hiển thị
- `script.js` — logic điều hướng và tải bài học
- `main.py` — backend Python phục vụ web và API
- `music.py` — script cũ, hiện vẫn chạy được demo và gọi backend mới
- `start_demo.ps1`, `start_demo.bat` — script chạy nhanh trên Windows
- `data/` — thư mục chứa nội dung bài học `.txt`

## Ghi chú

- Nếu muốn sửa nội dung bài học, chỉnh các file `.txt` trong `data/`.
- `music.py` còn có chế độ `--playlist` để quản lý playlist, nhưng README này tập trung vào demo web/backend.
