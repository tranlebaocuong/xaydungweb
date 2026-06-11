# Demo Tài liệu Tu Học

Đây là demo web tĩnh cho bộ tài liệu tu học, hiện tại tập trung vào hai nhánh chính:

- `HƯỚNG THIỆN`
- `SƠ THIỆN`

Mỗi nhánh có các mục `PHẬT PHÁP` và `HOẠT ĐỘNG THANH NIÊN` với nội dung bài học được lưu dưới dạng `.txt`.

## Cách chạy demo

Mở PowerShell hoặc terminal ở thư mục gốc `a:\xaydungweb`.

Chạy lệnh:

```powershell
python music.py --demo --port 8000
```

Nếu cổng `8000` đã bị chiếm, chương trình sẽ tự động thử các cổng tiếp theo từ `8000` đến `8009` và in ra URL phù hợp.

Sau đó mở trình duyệt và truy cập:

```
http://127.0.0.1:8000/index.html
```

Hoặc URL do script in ra.

## Vì sao phải dùng server HTTP

Demo tải nội dung bài học từ các file `.txt` bằng `fetch()`. Vì vậy bạn không nên mở trực tiếp bằng `file://`.

Sử dụng server HTTP để:

- tải `index.html`, `styles.css`, `script.js` đúng cách
- đọc nội dung bài học qua HTTP
- tránh lỗi `CORS` hoặc lỗi `fetch` khi mở file local

## Cấu trúc hiển thị hiện tại

Trang demo hiện nay hiển thị:

1. Trang root với hai nút: `HƯỚNG THIỆN` và `SƠ THIỆN`
2. Mỗi nhánh có:
   - `PHẬT PHÁP`
   - `HOẠT ĐỘNG THANH NIÊN`
   - `HOẠT ĐỘNG XÃ HỘI`
   - `VĂN NGHỆ`
3. Các bài học được tải từ các file `.txt` trong thư mục `data/ngành_thiếu/`

## Tệp quan trọng

- `index.html`: trang chủ demo
- `styles.css`: giao diện cơ bản
- `script.js`: logic điều hướng bài học và tải nội dung
- `music.py`: script khởi chạy server demo

## Ghi chú

- Nếu cần sửa nội dung bài học, chỉnh các file `.txt` trong `data/ngành_thiếu/`
- Demo hiện không dựa trên `bài_1.html` cũ nữa, nội dung được load động qua `script.js`

Nếu bạn muốn, mình có thể thêm mục “Cách đóng góp” hoặc mô tả nhanh hơn cấu trúc file trong README.
