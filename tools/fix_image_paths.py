#!/usr/bin/env python3
import os
import re
from pathlib import Path

def fix_image_paths(root_dir='data'):
    """Fix all image paths in text files by adding 'ảnh/' prefix where needed."""
    
    count = 0
    files_fixed = []
    
    for txt_file in Path(root_dir).rglob('*.txt'):
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # Fix patterns like ](ảnh_bài_... -> ](ảnh/ảnh_bài_...
            content = re.sub(
                r'\]\(ảnh_bài_',
                r'](ảnh/ảnh_bài_',
                content
            )
            
            # Fix patterns like ](ảnh bài hát... -> ](ảnh/ảnh bài hát...
            content = re.sub(
                r'\]\(ảnh bài hát',
                r'](ảnh/ảnh bài hát',
                content
            )
            
            # Only save if there were changes
            if content != original:
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
                files_fixed.append(str(txt_file))
                print(f"✓ Fixed: {txt_file}")
        
        except Exception as e:
            print(f"✗ Error processing {txt_file}: {e}")
    
    print(f"\n✓ Total files fixed: {count}")
    return files_fixed

if __name__ == '__main__':
    fixed = fix_image_paths()
    if fixed:
        print("\nFixed files:")
        for f in fixed:
            print(f"  - {f}")
