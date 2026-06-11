import re
import os
from pathlib import Path

# Find all lines with images that aren't on their own line
issue_count = 0
files_with_issues = []

# Traverse all .txt files in data directory
for txt_file in Path('data').rglob('*.txt'):
    try:
        with open(txt_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            # Check if line has image markdown but isn't just the image
            if '![' in line and '](' in line and not re.match(r'^\s*!\[', line):
                issue_count += 1
                files_with_issues.append({
                    'file': str(txt_file),
                    'line': i,
                    'content': line.strip()[:80]
                })
                if issue_count <= 20:
                    print(f"{txt_file}:{i}")
                    print(f"  {line.strip()[:100]}")
    except:
        pass

print(f"\nTotal issues found: {issue_count}")
print(f"Files affected: {len(set(f['file'] for f in files_with_issues))}")
