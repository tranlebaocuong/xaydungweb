# Demo Tài liệu Tu Học

Đây là web demo cho bộ tài liệu tu học của gia đình Phật tử. Ứng dụng đang chạy theo mô hình: frontend HTML/CSS/JavaScript + backend Python phục vụ tĩnh và API đọc dữ liệu từ thư mục `data/`.

## Tính năng hiện có

- Menu trái dạng danh mục theo cây học liệu
- Tìm kiếm theo bậc học và danh mục lớn như: `SƠ THIỆN`, `HƯỚNG THIỆN`, `NGÀNH THIẾU`, `NGÀNH ĐỒNG`, `PHẬT PHÁP`, `HOẠT ĐỘNG THANH NIÊN`, ...
- Nút quay lại ở đầu danh sách để dễ điều hướng khi đã đi sâu vào từng mục
- Giao diện tối ưu cho desktop và mobile
- Nút menu mobile với overlay và animation tối giản
- Icon sách/biểu tượng tu học, theme tối hiện đại hơn

## Cấu trúc dữ liệu

Demo đang hỗ trợ các nhánh chính như:

- `NGÀNH THIẾU`
  - `HƯỚNG THIỆN`
  - `SƠ THIỆN`
- `NGÀNH ĐỒNG`
  - `MỞ MẮT`
  - `CÁNH MỀM`
  - `CHÂN CỨNG`
  - `TUNG BAY`

Mỗi nhánh chứa các phần như `PHẬT PHÁP`, `HOẠT ĐỘNG THANH NIÊN`, `HOẠT ĐỘNG XÃ HỘI`, `VĂN NGHỆ`, và các bài học được lưu dưới `data/`.

## Cách khởi động demo

Từ thư mục gốc của project:

```powershell
.\.venv\Scripts\python.exe main.py --port 8000 --no-browser
```

Nếu chưa kích hoạt venv nhưng đã cài Python hệ thống:

```powershell
python main.py --port 8000 --no-browser
```

Hoặc dùng:

```powershell
py main.py --port 8000 --no-browser
```

Sau đó mở trình duyệt và truy cập:

```text
http://127.0.0.1:8000/index.html
```

## Chạy nhanh trên Windows

Có sẵn 2 script:

- `start_demo.bat`
- `start_demo.ps1`

Hai file này đều ưu tiên dùng Python ảo `.venv` nếu có, nếu không thì fallback về `python` hoặc `py`.

## API backend

- `GET /api/health` — kiểm tra backend đang chạy
- `GET /api/structure` — trả về cây dữ liệu từ `data/`
- `GET /api/lesson?path=data/.../bài_1.txt` — trả về tiêu đề và nội dung bài học

## Lưu ý quan trọng

- Không nên mở trực tiếp `index.html` bằng `file://` vì frontend dùng `fetch()` để tải dữ liệu `.txt`.
- Hãy luôn chạy qua server HTTP để tránh lỗi tải nội dung.
- Nếu vừa sửa giao diện hoặc icon, nhấn `Ctrl+F5` hoặc mở tab mới để tránh cache cũ của browser.

## Các file chính

- `index.html` — shell giao diện demo
- `styles.css` — style chính của UI
- `script.js` — điều hướng, tìm kiếm, trình bày bài học
- `main.py` — backend server và API
- `data/` — dữ liệu bài học dạng `.txt`
- `start_demo.bat` — launcher cho Windows CMD
- `start_demo.ps1` — launcher cho PowerShell

## Ghi chú

- Nếu cần sửa nội dung học liệu, chỉnh trực tiếp trong thư mục `data/`.
- Nếu thay đổi giao diện, template và CSS đang được lưu theo phiên bản `?v=` để tránh cache trình duyệt giữ bản cũ.
