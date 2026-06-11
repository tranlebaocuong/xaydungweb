#!/usr/bin/env python3
"""Complete image path fix - rewrite all image references in one pass"""
import os
from pathlib import Path

def fix_all():
    count = 0
    for txt_file in Path('data').rglob('*.txt'):
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Replace ALL image markdown paths
        # Pattern 1: ](ảnh_bài_ -> ](ảnh/ảnh_bài_
        content = content.replace('](ảnh_bài_', '](ảnh/ảnh_bài_')
        
        # Pattern 2: ](ảnh bài hát -> ](ảnh/ảnh bài hát  
        content = content.replace('](ảnh bài hát', '](ảnh/ảnh bài hát')
        
        if content != original:
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
            print(f"✓ Fixed: {txt_file}")
    
    print(f"\n✅ Total files fixed: {count}")

if __name__ == '__main__':
    fix_all()
