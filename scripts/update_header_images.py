#!/usr/bin/env python3
"""
Update markdown files to add header-img to front matter
"""

import os
import re
from pathlib import Path

BLOG_DIR = "blogs/travelling"
IMAGE_DIR = "images/in-post"

def extract_city_name(filename):
    match = re.match(r'\d{4}-\d{2}-\d{2}-(.+)\.md', filename)
    return match.group(1) if match else None

def has_header_img(content):
    return re.search(r'^header-img:\s*.+', content, re.MULTILINE) is not None

def add_header_img_to_frontmatter(content, header_img_value):
    """Add header-img to YAML front matter"""
    lines = content.split('\n')
    
    if not lines[0].strip() == '---':
        print("  Warning: No front matter found")
        return content
    
    # Find the end of front matter
    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end_idx = i
            break
    
    if end_idx == -1:
        print("  Warning: Front matter not properly closed")
        return content
    
    # Insert header-img after author line if exists, otherwise before the closing ---
    insert_idx = end_idx
    for i in range(1, end_idx):
        if lines[i].startswith('author:'):
            insert_idx = i + 1
            break
    
    # Insert the header-img line
    lines.insert(insert_idx, f'header-img: {header_img_value}')
    
    return '\n'.join(lines)

def main():
    print("Updating markdown files with header-img...")
    
    md_files = sorted(Path(BLOG_DIR).glob("*.md"))
    updated = 0
    skipped = 0
    
    for md_file in md_files:
        filename = md_file.name
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has header-img
        if has_header_img(content):
            print(f"✓ {filename} - already has header-img")
            skipped += 1
            continue
        
        # Extract city name
        city_name = extract_city_name(filename)
        if not city_name:
            print(f"✗ {filename} - could not extract city name")
            skipped += 1
            continue
        
        # Check if image file exists
        image_filename = f"{city_name}-0.jpg"
        image_path = Path(IMAGE_DIR) / image_filename
        
        if not image_path.exists():
            print(f"✗ {filename} - image not found: {image_filename}")
            skipped += 1
            continue
        
        # Add header-img
        header_img_value = f"img/in-post/{image_filename}"
        updated_content = add_header_img_to_frontmatter(content, header_img_value)
        
        # Write back
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✓ {filename} - added header-img: {header_img_value}")
        updated += 1
    
    print("\n" + "=" * 60)
    print(f"Update complete!")
    print(f"  Updated: {updated}")
    print(f"  Skipped: {skipped}")

if __name__ == "__main__":
    main()
