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
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Referer': 'https://www.douban.com/',
    'Connection': 'keep-alive'
}

import random

def extract_city_name(filename):
    match = re.match(r'\d{4}-\d{2}-\d{2}-(.+)\.md', filename)
    return match.group(1) if match else None

def has_header_img(content):
    return re.search(r'^header-img:\s*.+', content, re.MULTILINE) is not None

def extract_albums(content):
    """Extract all Douban album URLs and their descriptions/dates"""
    # Pattern to find date/description and the following Douban link
    # Matches something like: Chengdu 2011-12 -> [Douban Album](https://...)
    # Or just the URL
    pattern = r'(?:in\s+)?([A-Za-z0-9\s\-\u4e00-\u9fa5]+?)(?:\s+->\s+)?\[Douban Album\]\((https://www\.douban\.com/photos/album/\d+)/?\)'
    matches = re.findall(pattern, content)
    
    albums = []
    for desc, url in matches:
        # Clean up description to extract just the date if possible
        date_match = re.search(r'\d{4}-\d{2}', desc)
        clean_desc = date_match.group(0) if date_match else desc.strip()
        albums.append({'url': url, 'desc': clean_desc})
        
    if not albums:
        # Fallback to simple URL search if the structured pattern isn't found
        urls = re.findall(r'https://www\.douban\.com/photos/album/\d+/?', content)
        for url in urls:
            albums.append({'url': url.strip('/'), 'desc': 'View Album'})
            
    return albums

def fetch_douban_image_url(album_url):
    try:
        response = requests.get(album_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. Try specific span.rec with data-image (User suggested)
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

def main():
    print("Syncing MISSING albums...")
    
    md_files = sorted(Path(BLOG_DIR).glob("*.md"))
    all_sync_items = []
    
    # Random realistic User-Agents
    AGENTS = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    
    for md_file in md_files:
        filename = md_file.name
        city_name = extract_city_name(filename)
        if not city_name: continue
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        albums = extract_albums(content)
        if not albums: continue
        
        missing_in_file = False
        for i, album in enumerate(albums):
            image_filename = f"{city_name}-{i}.jpg"
            image_path = Path(IMAGE_DIR) / image_filename
            
            if not image_path.exists():
                missing_in_file = True
                print(f"  Missing: {image_filename} for {album['url']}")
                
                # Fetch with retries
                img_url = None
                for attempt in range(3):
                    headers = HEADERS.copy()
                    headers['User-Agent'] = random.choice(AGENTS)
                    img_url = fetch_douban_image_url(album['url'])
                    if img_url:
                        break
                    print(f"    Attempt {attempt+1} failed, sleeping...")
                    time.sleep(random.uniform(10, 20))
                
                if img_url:
                    item = {
                        'city': city_name,
                        'url': album['url'],
                        'img_url': img_url,
                        'image_filename': image_filename
                    }
                    all_sync_items.append(item)
                    print(f"    Found: {img_url}")
                
                # Always sleep between albums to avoid ban
                time.sleep(random.uniform(5, 12))
    
    # Generate download script only for the new ones
    if all_sync_items:
        script_lines = ["#!/bin/bash", "mkdir -p images/in-post", ""]
        for item in all_sync_items:
            script_lines.append(f"curl -L -H 'Referer: https://www.douban.com/' \\")
            script_lines.append(f"     -H 'User-Agent: Mozilla/5.0' \\")
            script_lines.append(f"     '{item['img_url']}' \\")
            script_lines.append(f"     -o 'images/in-post/{item['image_filename']}'")
        
        with open("download_missing.sh", 'w', encoding='utf-8') as f:
            f.write('\n'.join(script_lines))
        os.chmod("download_missing.sh", 0o755)
        print(f"\n✓ Found {len(all_sync_items)} missing images. Run ./download_missing.sh")
    else:
        print("\n✓ No missing images found to sync.")

if __name__ == "__main__":
    main()
