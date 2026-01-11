#!/usr/bin/env python3
"""
Douban Album Sync Script - Enhanced Version
Features:
1. Recursively scan blogs/travelling directory and subdirectories
2. Support both filename formats: YYYY-MM-DD-CityName.md and 中文名_EnglishName.md
3. Sync missing images from Douban albums
4. Verify existing images for URL changes (--verify mode)
"""

import os
import re
import argparse
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import time
import random
import hashlib

BLOG_DIR = "blogs/travelling"
IMAGE_DIR = "images/in-post"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Referer': 'https://www.douban.com/',
    'Connection': 'keep-alive'
}

AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]


def extract_city_name(filename):
    """Extract city name from filename, supporting both formats."""
    # Format 1: YYYY-MM-DD-CityName.md
    match = re.match(r'\d{4}-\d{2}-\d{2}-(.+)\.md', filename)
    if match:
        return match.group(1)
    
    # Format 2: 中文名_EnglishName.md
    match = re.match(r'.+_(.+)\.md', filename)
    if match:
        return match.group(1)
    
    # Format 3: Just name.md
    match = re.match(r'(.+)\.md', filename)
    if match:
        return match.group(1)
    
    return None


def has_header_img(content):
    """Check if content has header-img in front matter."""
    return re.search(r'^header-img:\s*.+', content, re.MULTILINE) is not None


def get_header_img_path(content):
    """Extract header-img path from content."""
    match = re.search(r'^header-img:\s*(.+)', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None


def extract_albums(content):
    """Extract all Douban album URLs and their descriptions/dates."""
    pattern = r'(?:in\s+)?([A-Za-z0-9\s\-\u4e00-\u9fa5]+?)(?:\s+->\s+)?\[Douban Album\]\((https://www\.douban\.com/photos/album/\d+)/?'
    matches = re.findall(pattern, content)
    
    albums = []
    for desc, url in matches:
        date_match = re.search(r'\d{4}-\d{2}', desc)
        clean_desc = date_match.group(0) if date_match else desc.strip()
        albums.append({'url': url, 'desc': clean_desc})
        
    if not albums:
        urls = re.findall(r'https://www\.douban\.com/photos/album/\d+/?', content)
        for url in urls:
            albums.append({'url': url.strip('/'), 'desc': 'View Album'})
            
    return albums


def fetch_douban_image_url(album_url):
    """Fetch the cover image URL from a Douban album."""
    try:
        headers = HEADERS.copy()
        headers['User-Agent'] = random.choice(AGENTS)
        response = requests.get(album_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. Try span.rec with data-image
        rec_el = soup.select_one('span.rec[data-image]')
        if rec_el:
            img_url = rec_el['data-image']
            return img_url.replace('/thumb/', '/l/').replace('/m/', '/l/')

        # 2. Try any data-image attribute
        share_el = soup.find(attrs={"data-image": True})
        if share_el:
            img_url = share_el['data-image']
            return img_url.replace('/thumb/', '/l/').replace('/m/', '/l/')
            
        # 3. Try .cover img
        cover_img = soup.select_one('.cover img')
        if cover_img and cover_img.get('src'):
            return cover_img['src'].replace('/m/', '/l/').replace('/thumb/', '/l/')
        
        # 4. Try first photo in .photolst
        first_photo = soup.select_one('.photolst img')
        if first_photo and first_photo.get('src'):
            return first_photo['src'].replace('/m/', '/l/').replace('/thumb/', '/l/')
        
        return None
    except Exception as e:
        print(f"  Error fetching {album_url}: {e}")
        return None


def get_all_md_files(blog_dir):
    """Recursively get all markdown files."""
    return sorted(Path(blog_dir).rglob("*.md"))


def sync_missing(md_files):
    """Sync missing images."""
    print("=" * 60)
    print("Syncing MISSING albums...")
    print("=" * 60)
    
    all_sync_items = []
    
    for md_file in md_files:
        filename = md_file.name
        city_name = extract_city_name(filename)
        if not city_name:
            continue
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        albums = extract_albums(content)
        if not albums:
            continue
        
        for i, album in enumerate(albums):
            image_filename = f"{city_name}-{i}.jpg"
            image_path = Path(IMAGE_DIR) / image_filename
            
            if not image_path.exists():
                print(f"\n📁 {md_file.relative_to(BLOG_DIR)}")
                print(f"  Missing: {image_filename}")
                print(f"  Album: {album['url']}")
                
                img_url = None
                for attempt in range(3):
                    img_url = fetch_douban_image_url(album['url'])
                    if img_url:
                        break
                    print(f"    Attempt {attempt+1} failed, retrying...")
                    time.sleep(random.uniform(8, 15))
                
                if img_url:
                    all_sync_items.append({
                        'city': city_name,
                        'url': album['url'],
                        'img_url': img_url,
                        'image_filename': image_filename,
                        'md_file': str(md_file)
                    })
                    print(f"  ✓ Found: {img_url}")
                else:
                    print(f"  ✗ Could not find image URL")
                
                time.sleep(random.uniform(5, 10))
    
    if all_sync_items:
        generate_download_script(all_sync_items, "download_missing.sh")
        print(f"\n{'='*60}")
        print(f"✓ Found {len(all_sync_items)} missing images.")
        print(f"  Run: ./download_missing.sh")
    else:
        print(f"\n{'='*60}")
        print("✓ No missing images found.")


def verify_existing(md_files):
    """Verify existing images for URL changes."""
    print("=" * 60)
    print("Verifying EXISTING images for URL changes...")
    print("=" * 60)
    
    changed_items = []
    
    for md_file in md_files:
        filename = md_file.name
        city_name = extract_city_name(filename)
        if not city_name:
            continue
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Only check files that have header-img
        if not has_header_img(content):
            continue
            
        albums = extract_albums(content)
        if not albums:
            continue
        
        for i, album in enumerate(albums):
            image_filename = f"{city_name}-{i}.jpg"
            image_path = Path(IMAGE_DIR) / image_filename
            
            if image_path.exists():
                print(f"\n🔍 Checking: {image_filename}")
                
                # Fetch current URL from Douban
                current_url = fetch_douban_image_url(album['url'])
                
                if current_url:
                    # Compare with existing image (simplified - just check if URL structure changed)
                    changed_items.append({
                        'city': city_name,
                        'url': album['url'],
                        'img_url': current_url,
                        'image_filename': image_filename,
                        'md_file': str(md_file),
                        'status': 'needs_review'
                    })
                    print(f"  Current URL: {current_url}")
                    print(f"  (Manual review needed to confirm if changed)")
                
                time.sleep(random.uniform(3, 6))
    
    if changed_items:
        generate_download_script(changed_items, "download_updates.sh")
        print(f"\n{'='*60}")
        print(f"✓ Found {len(changed_items)} images to review.")
        print(f"  Review and run: ./download_updates.sh")
    else:
        print(f"\n{'='*60}")
        print("✓ No images to verify.")


def generate_download_script(items, script_name):
    """Generate a shell script to download images."""
    script_lines = ["#!/bin/bash", "mkdir -p images/in-post", ""]
    for item in items:
        script_lines.append(f"echo 'Downloading {item['image_filename']}...'")
        script_lines.append(f"curl -L -H 'Referer: https://www.douban.com/' \\")
        script_lines.append(f"     -H 'User-Agent: Mozilla/5.0' \\")
        script_lines.append(f"     '{item['img_url']}' \\")
        script_lines.append(f"     -o 'images/in-post/{item['image_filename']}'")
        script_lines.append("")
    
    with open(script_name, 'w', encoding='utf-8') as f:
        f.write('\n'.join(script_lines))
    os.chmod(script_name, 0o755)
    print(f"  Generated: {script_name}")


def list_no_album(md_files):
    """List files without Douban album links."""
    print("=" * 60)
    print("Files WITHOUT Douban album links:")
    print("=" * 60)
    
    count = 0
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        albums = extract_albums(content)
        if not albums:
            has_img = "✓ has header-img" if has_header_img(content) else "✗ no header-img"
            print(f"  {md_file.relative_to(BLOG_DIR)} - {has_img}")
            count += 1
    
    print(f"\n{'='*60}")
    print(f"Total: {count} files without Douban album links")


def main():
    parser = argparse.ArgumentParser(description='Douban Album Image Sync Tool')
    parser.add_argument('--verify', action='store_true', 
                        help='Verify existing images for URL changes')
    parser.add_argument('--list-no-album', action='store_true',
                        help='List files without Douban album links')
    args = parser.parse_args()
    
    md_files = get_all_md_files(BLOG_DIR)
    print(f"Found {len(md_files)} markdown files in {BLOG_DIR}")
    
    if args.list_no_album:
        list_no_album(md_files)
    elif args.verify:
        verify_existing(md_files)
    else:
        sync_missing(md_files)


if __name__ == "__main__":
    main()
