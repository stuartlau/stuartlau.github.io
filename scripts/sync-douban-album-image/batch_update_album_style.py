#!/usr/bin/env python3
"""
Batch update travelling blog posts to use the modern album-grid card style.
This script replaces text-based Douban album links with visual HTML cards.
"""

import os
import re
from pathlib import Path

BLOG_DIR = "blogs/travelling"

def extract_city_name(filename):
    match = re.match(r'\d{4}-\d{2}-\d{2}-(.+)\.md', filename)
    return match.group(1) if match else None

def get_album_v2_html(city, albums):
    """Generate the modern HTML structure for albums"""
    html = ['<div class="album-grid">']
    for i, album in enumerate(albums):
        url = album['url']
        desc = album['desc']
        image_path = f"{{{{ site.url }}}}/images/in-post/{city}-{i}.jpg"
        
        html.append(f'  <a href="{url}" class="album-card" target="_blank">')
        html.append(f'    <div class="album-image">')
        html.append(f'      <img src="{image_path}" alt="{city} Album" class="no-zoom">')
        html.append(f'    </div>')
        html.append(f'    <div class="album-info">')
        html.append(f'      <span class="album-title">{city} Album</span>')
        html.append(f'      <span class="album-desc">{desc}</span>')
        html.append(f'    </div>')
        html.append(f'  </a>')
    html.append('</div>')
    return '\n'.join(html)

def process_file(file_path):
    city = extract_city_name(file_path.name)
    if not city:
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already using the grid
    if '<div class="album-grid">' in content:
        return False

    # Regex to find the pattern: > Text -> [Douban Album](URL)
    # Matches multiple occurrences or a single one
    pattern = r'>\s*([A-Za-z0-9\s\-\u4e00-\u9fa5]+?)\s*->\s*\[Douban Album\]\((https://www\.douban\.com/photos/album/\d+)/?\)'
    matches = re.findall(pattern, content)
    
    if not matches:
        # Try a simpler pattern if the above fails
        pattern_simple = r'\[Douban Album\]\((https://www\.douban\.com/photos/album/\d+)/?\)'
        simple_matches = re.findall(pattern_simple, content)
        if simple_matches:
            matches = [("View Album", url) for url in simple_matches]
        else:
            return False

    albums = []
    for desc, url in matches:
        # Extract date from description if possible
        date_match = re.search(r'\d{4}-\d{2}', desc)
        clean_desc = date_match.group(0) if date_match else desc.strip()
        # Remove "Photos taken in" prefix if present for cleaner cards
        clean_desc = clean_desc.replace("Photos taken in ", "").strip()
        albums.append({'url': url, 'desc': clean_desc})

    # Find the range of lines to replace
    # We want to replace the entire block of links
    lines = content.split('\n')
    start_replace = -1
    end_replace = -1
    
    # Simple logic: replace the first occurrence of the pattern and all subsequent links
    all_link_lines = []
    for i, line in enumerate(lines):
        if '[Douban Album]' in line:
            if start_replace == -1:
                start_replace = i
            end_replace = i

    if start_replace == -1:
        return False

    # Construct new content
    new_html = get_album_v2_html(city, albums)
    new_lines = lines[:start_replace] + [new_html] + lines[end_replace+1:]
    new_content = '\n'.join(new_lines)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    print("Updating blog posts to album card style...")
    md_files = sorted(Path(BLOG_DIR).glob("*.md"))
    updated = 0
    
    for md_file in md_files:
        if process_file(md_file):
            print(f"✓ {md_file.name}")
            updated += 1
            
    print(f"\nFinished! Updated {updated} files.")

if __name__ == "__main__":
    main()
