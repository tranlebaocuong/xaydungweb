#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

dirs = [
    'data/oanh_vũ/cánh_mềm',
    'data/oanh_vũ/chân_cứng'
]

# Common spelling mistakes
typos = {
    'gốc rế': 'gốc rễ',
    'chyện': 'chuyện',
    'mẫu chyện': 'mẫu chuyện',
}

all_files = []

for dir_path in dirs:
    if os.path.exists(dir_path):
        for root, folders, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.txt'):
                    full_path = os.path.join(root, file)
                    all_files.append(full_path)

print(f"Total files found: {len(all_files)}\n")

# Scan for issues
issues_found = {}

for file_path in all_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        issues = []
        
        # Check for specific typos
        for typo, correct in typos.items():
            if typo in content:
                issues.append(f"  - Typo: '{typo}' -> '{correct}'")
        
        # Check for formatting issues (missing space after Roman numerals)
        if re.search(r'I\.([A-Z])', content):
            issues.append(f"  - Missing space after 'I.' (should be 'I. ')")
        if re.search(r'II\.([A-Z])', content):
            issues.append(f"  - Missing space after 'II.' (should be 'II. ')")
        
        if issues:
            issues_found[file_path] = issues
            print(f"❌ {file_path}")
            for issue in issues:
                print(issue)
            print()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

print(f"\n\nTotal files with issues: {len(issues_found)}")
