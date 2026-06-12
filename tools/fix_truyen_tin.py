filepath = r'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/truyền_tin/bài_1.txt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix: Move image markdown from end of line to separate line
content = content.replace(
    'Tập thổi còi  truyền tin, nhận tin các ký tự theo tháp Morse:       ![Hình](ảnh_bài_1/tháp.png)',
    'Tập thổi còi  truyền tin, nhận tin các ký tự theo tháp Morse:\n\n![Hình](ảnh_bài_1/tháp.png)'
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed truyền_tin/bài_1.txt")
