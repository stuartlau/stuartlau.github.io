#!/usr/bin/env python3
import os
import re

def fix_headers_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False
    
    frontmatter = parts[1]
    body = parts[2]
    
    first_header_match = re.search(r'^(#{1,6})\s+', body, re.MULTILINE)
    if not first_header_match:
        return False
    
    first_level = len(first_header_match.group(1))
    
    if first_level >= 3:
        return False
    
    add_count = 3 - first_level
    
    def add_hashes(match):
        return '#' * (len(match.group(1)) + add_count) + match.group(2)
    
    new_body = re.sub(r'^(#{1,6})(\s+)', add_hashes, body, flags=re.MULTILINE)
    
    if new_body == body:
        return False
    
    new_content = '---' + frontmatter + '---' + new_body
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

if __name__ == '__main__':
    blogs_dir = '/Users/stuart/IdeaProjects/stuartlau.github.io/blogs/tech'
    fixed_count = 0
    total_count = 0

    for root, dirs, files in os.walk(blogs_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                total_count += 1
                if fix_headers_in_file(filepath):
                    print(f'Fixed: {os.path.basename(filepath)}')
                    fixed_count += 1

    print(f'\nTotal: {total_count} files, Fixed: {fixed_count} files')
