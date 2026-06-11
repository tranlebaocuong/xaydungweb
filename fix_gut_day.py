filepath = r'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/gút_dây/bài_4.txt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix: Move image markdown from end of line to separate line
content = content.replace(
    '1. Tên gọi:  Gút quai chèo, gút cọc chèo, thuyền chài, gút chụp.        ![Hình](ảnh_bài_4/chèo.png)',
    '1. Tên gọi:  Gút quai chèo, gút cọc chèo, thuyền chài, gút chụp.\n\n![Hình](ảnh_bài_4/chèo.png)'
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed bài_4.txt")
