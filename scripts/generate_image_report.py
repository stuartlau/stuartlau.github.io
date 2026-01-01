#!/usr/bin/env python3
"""
Alternative script: Extract Douban image URLs and generate a report.
Since Douban blocks automated downloads, this script will:
1. Extract image URLs from Douban albums
2. Generate a report with download commands
3. You can then manually download or use browser tools
"""

import os
import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import time

BLOG_DIR = "blogs/travelling"
IMAGE_DIR = "images/in-post"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Referer': 'https://www.douban.com/'
}

def extract_city_name(filename):
    match = re.match(r'\d{4}-\d{2}-\d{2}-(.+)\.md', filename)
    return match.group(1) if match else None

def has_header_img(content):
    return re.search(r'^header-img:\s*.+', content, re.MULTILINE) is not None

def extract_douban_url(content):
    match = re.search(r'https://www\.douban\.com/photos/album/(\d+)', content)
    return match.group(0) if match else None

def fetch_douban_image_url(album_url):
    try:
        response = requests.get(album_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. Try finding data-image (often used for cover sharing)
        share_el = soup.find(attrs={"data-image": True})
        if share_el:
            img_url = share_el['data-image']
            # Convert thumb/m to l for large size
            img_url = img_url.replace('/thumb/', '/l/').replace('/m/', '/l/')
            print(f"  Found data-image cover: {img_url}")
            return img_url
            
        # 2. Try cover image CSS selector
        cover_img = soup.select_one('.cover img')
        if cover_img and cover_img.get('src'):
            img_url = cover_img['src'].replace('/m/', '/l/').replace('/thumb/', '/l/')
            print(f"  Found .cover img: {img_url}")
            return img_url
        
        # 3. Try first photo in the grid
        first_photo = soup.select_one('.photolst img')
        if first_photo and first_photo.get('src'):
            img_url = first_photo['src'].replace('/m/', '/l/').replace('/thumb/', '/l/')
            print(f"  Found .photolst img: {img_url}")
            return img_url
        
        return None
    except Exception as e:
        print(f"  Error fetching {album_url}: {e}")
        return None

def main():
    print("Generating image download report (syncing all albums)...")
    
    md_files = sorted(Path(BLOG_DIR).glob("*.md"))
    report_lines = []
    report_lines.append("# Douban Image Sync Report")
    report_lines.append("# Generated: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    report_lines.append("# Note: This report includes all files with Douban albums to ensure images are updated.")
    report_lines.append("")
    
    needs_sync = []
    
    for md_file in md_files:
        filename = md_file.name
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        douban_url = extract_douban_url(content)
        if not douban_url:
            continue
        
        city_name = extract_city_name(filename)
        if not city_name:
            continue
        
        print(f"Processing: {filename}")
        img_url = fetch_douban_image_url(douban_url)
        
        if img_url:
            image_filename = f"{city_name}-0.jpg"
            needs_sync.append({
                'file': filename,
                'city': city_name,
                'douban_url': douban_url,
                'img_url': img_url,
                'image_filename': image_filename,
                'has_img': has_header_img(content)
            })
        
        time.sleep(1)
    
    # Generate report
    for item in needs_sync:
        status = "[Updating]" if item['has_img'] else "[New]"
        report_lines.append(f"## {item['file']} {status}")
        report_lines.append(f"City: {item['city']}")
        report_lines.append(f"Album: {item['douban_url']}")
        report_lines.append(f"Image URL: {item['img_url']}")
        report_lines.append(f"Save as: images/in-post/{item['image_filename']}")
        report_lines.append("")
    
    # Save report
    report_file = "douban_images_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"\n✓ Report saved to: {report_file}")
    print(f"  Found {len(needs_sync)} albums to sync")
    
    # Also generate a shell script for manual download
    script_lines = ["#!/bin/bash", "# Download images from Douban", "mkdir -p images/in-post", ""]
    for item in needs_sync:
        script_lines.append(f"# {item['file']}")
        script_lines.append(f"curl -L -H 'Referer: https://www.douban.com/' \\")
        script_lines.append(f"     -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36' \\")
        script_lines.append(f"     '{item['img_url']}' \\")
        script_lines.append(f"     -o 'images/in-post/{item['image_filename']}'")
        script_lines.append("")
    
    script_file = "download_images.sh"
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(script_lines))
    
    os.chmod(script_file, 0o755)
    print(f"✓ Sync script saved to: {script_file}")
    print("\nYou should run: ./download_images.sh")

if __name__ == "__main__":
    main()
