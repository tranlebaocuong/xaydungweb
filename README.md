# Demo Tài liệu Tu Học

Đây là demo web tĩnh cho bộ tài liệu tu học. Nội dung được hiển thị bằng giao diện HTML/CSS/JavaScript và tải các bài học từ file `.txt` qua HTTP.

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
python music.py --demo --port 8000
```

3. Nếu cổng `8000` đã bị chiếm, script sẽ tự động thử các cổng tiếp theo từ `8000` đến `8009`.
4. Mở trình duyệt và truy cập URL được in ra, thường là:

```
http://127.0.0.1:8000/index.html
```

## Chạy nhanh trên Windows

- `start_demo.ps1`
- `start_demo.bat`

Các script này chỉ chạy `python music.py --demo --port 8000` từ thư mục chứa file.

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
- `music.py` — script khởi chạy server demo
- `start_demo.ps1`, `start_demo.bat` — script chạy nhanh trên Windows
- `data/` — thư mục chứa nội dung bài học `.txt`

## Ghi chú

- Nếu muốn sửa nội dung bài học, chỉnh các file `.txt` trong `data/`.
- `music.py` còn có chế độ `--playlist` để quản lý playlist, nhưng README này tập trung vào demo web.
