#!/usr/bin/env python3
"""
Auto-Match Douban Albums to Travel Blog Posts
1. Crawl all albums from user's Douban photo page
2. Parse album names with pattern: yyyy年yy月·在XXX (XXX = city name)
3. Match to existing markdown files
4. Update header-img and add album links
"""

import os
import re
import argparse
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import time
import random
import json

USER_ID = "shuoleo"
ALBUMS_URL = f"https://www.douban.com/people/{USER_ID}/photos"
BLOG_DIR = "blogs/travelling"
IMAGE_DIR = "images/in-post"

def load_cookie(cookie_arg=None):
    """Load cookie from argument or ~/.douban.cookie file."""
    if cookie_arg:
        return cookie_arg
    
    cookie_path = os.path.expanduser("~/.douban.cookie")
    if os.path.exists(cookie_path):
        try:
            with open(cookie_path, 'r', encoding='utf-8') as f:
                cookie = f.read().strip()
            print(f"Loaded cookie from {cookie_path}")
            return cookie
        except Exception as e:
            print(f"Error reading cookie file: {e}")
    else:
        print(f"Cookie file not found: {cookie_path}")
    
    return None

def get_headers(cookie=None):
    """Get request headers with optional cookie."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Referer': 'https://www.douban.com/',
        'Connection': 'keep-alive'
    }
    if cookie:
        headers['Cookie'] = cookie
    return headers

# City name mapping: Chinese -> English
CITY_NAME_MAP = {
    '北京': 'Beijing',
    '上海': 'Shanghai',
    '天津': 'Tianjin',
    '吉林': 'Jilin',
    '乐山': 'Leshan',
    '康定': 'Kangding',
    '伊犁': 'Yili',
    '秦皇岛': 'Qinhuangdao',
    '林芝': 'Nyingchi',
    '曼谷': 'Bangkok',
    '成都': 'Chengdu',
    '拉萨': 'Lasa',
    '昆明': 'Kunming',
    '丽江': 'Lijiang',
    '西安': 'Xian',
    '杭州': 'Hangzhou',
    '苏州': 'Suzhou',
    '青岛': 'Qingdao',
    '大同': 'Datong',
    '三亚': 'Sanya',
    '福州': 'Fuzhou',
    '长沙': 'Changsha',
    '沈阳': 'Shenyang',
    '澳门': 'Macau',
    '香港': 'HongKong',
    '台北': 'Taipei',
    '台南': 'Tainan',
    '高雄': 'Gaoxiong',
    '垦丁': 'Kenting',
    '嘉义': 'Jiayi',
    '遂宁': 'Suining',
    '张家口': 'Zhangjiakou',
    '湖州': 'Huzhou',
    '嘉兴': 'Jiaxing',
    '东阳': 'Dongyang',
    '乌兰察布': 'Wulanchabu',
    '博尔塔拉': 'Bortala',
    '东京': 'Tokyo',
    '京都': 'Kyoto',
    '大阪': 'Osaka',
    '首尔': 'Seoul',
    '象岛': 'KohChang',
    '罗马': 'Rome',
    '佛罗伦萨': 'Florence',
    '米兰': 'Milan',
    '威尼斯': 'Venice',
    '巴黎': 'Paris',
    '巴塞罗那': 'Barcelona',
    '马德里': 'Madrid',
    '莫斯科': 'Moscow',
    '卢加诺': 'Lugano',
    '梵蒂冈': 'Vatican',
}


def fetch_all_albums(cookie=None):
    """Fetch all albums from user's Douban photo page."""
    albums = []
    page = 0
    headers = get_headers(cookie)
    
    while True:
        url = f"{ALBUMS_URL}?start={page * 12}"
        print(f"Fetching: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find album items - correct selector based on actual page structure
            album_items = soup.select('div.albumlst')
            
            if not album_items:
                # Try alternative: look for album_photo links directly
                album_links = soup.select('a.album_photo')
                if not album_links:
                    print(f"  No more albums found on page {page}")
                    break
                
                # Process album links directly
                for link in album_links:
                    href = link.get('href', '')
                    match = re.search(r'/photos/album/(\d+)', href)
                    if match:
                        album_id = match.group(1)
                        # Find title in sibling elements
                        parent = link.parent
                        title_el = parent.find('a', href=True, class_=lambda x: x != 'album_photo') if parent else None
                        title = title_el.get_text(strip=True) if title_el else f"Album {album_id}"
                        
                        albums.append({
                            'id': album_id,
                            'url': f"https://www.douban.com/photos/album/{album_id}",
                            'title': title
                        })
                        print(f"  Found: {title}")
            else:
                for item in album_items:
                    # Find album_photo link
                    link = item.select_one('a.album_photo')
                    if not link:
                        continue
                    
                    href = link.get('href', '')
                    match = re.search(r'/photos/album/(\d+)', href)
                    if not match:
                        continue
                    
                    album_id = match.group(1)
                    
                    # Find title link (the other <a> tag that's not album_photo)
                    title_links = item.select('a')
                    title = None
                    for a in title_links:
                        if 'album_photo' not in (a.get('class') or []):
                            title = a.get_text(strip=True)
                            if title:
                                break
                    
                    if not title:
                        title = f"Album {album_id}"
                    
                    albums.append({
                        'id': album_id,
                        'url': f"https://www.douban.com/photos/album/{album_id}",
                        'title': title
                    })
                    print(f"  Found: {title}")
            
            page += 1
            time.sleep(random.uniform(2, 4))
            
            # Check if we found any new albums on this page
            if len(albums) == 0 or (page > 1 and len(albums) == len(set(a['id'] for a in albums))):
                # No new albums, we might have reached the end
                pass
                
        except Exception as e:
            print(f"  Error fetching page {page}: {e}")
            break
    
    return albums


def parse_album_title(title):
    """Parse album title to extract city name.
    Format: yyyy年yy月·在XXX or variations
    """
    # Pattern: yyyy年yy月·在XXX
    match = re.search(r'\d{4}年\d{1,2}月[·・]?在(.+)', title)
    if match:
        return match.group(1).strip()
    
    # Pattern: 在XXX
    match = re.search(r'在(.+)', title)
    if match:
        return match.group(1).strip()
    
    return None


def get_english_name(chinese_city):
    """Get English name for Chinese city."""
    return CITY_NAME_MAP.get(chinese_city)


def find_md_file(city_chinese, city_english):
    """Find corresponding markdown file for the city."""
    patterns = [
        f"*{city_english}*.md",
        f"*{city_chinese}*.md",
        f"*_{city_english}.md",
        f"*{city_chinese}_{city_english}.md"
    ]
    
    for pattern in patterns:
        files = list(Path(BLOG_DIR).rglob(pattern))
        if files:
            return files[0]
    
    return None


def fetch_album_cover(album_url, cookie=None):
    """Fetch cover image URL from album."""
    try:
        headers = get_headers(cookie)
        response = requests.get(album_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try span.rec with data-image
        rec_el = soup.select_one('span.rec[data-image]')
        if rec_el:
            img_url = rec_el['data-image']
            return img_url.replace('/thumb/', '/l/').replace('/m/', '/l/')

        # Try any data-image attribute
        share_el = soup.find(attrs={"data-image": True})
        if share_el:
            img_url = share_el['data-image']
            return img_url.replace('/thumb/', '/l/').replace('/m/', '/l/')
            
        # Try .cover img
        cover_img = soup.select_one('.cover img')
        if cover_img and cover_img.get('src'):
            return cover_img['src'].replace('/m/', '/l/').replace('/thumb/', '/l/')
        
        return None
    except Exception as e:
        print(f"  Error fetching cover: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='Auto-match Douban albums to travel posts')
    parser.add_argument('--dry-run', action='store_true', help='Show matches without making changes')
    parser.add_argument('--fetch-albums', action='store_true', help='Fetch and cache album list')
    parser.add_argument('--cookie', type=str, help='Douban cookie string (overrides ~/.douban.cookie)')
    args = parser.parse_args()
    
    # Load cookie
    cookie = load_cookie(args.cookie)
    if not cookie:
        print("Warning: No cookie provided. Requests may fail due to Douban anti-crawl.")
    
    cache_file = "douban_albums_cache.json"
    
    if args.fetch_albums or not Path(cache_file).exists():
        print("=" * 60)
        print("Fetching albums from Douban...")
        print("=" * 60)
        albums = fetch_all_albums(cookie)
        
        # Cache results
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(albums, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Cached {len(albums)} albums to {cache_file}")
    else:
        with open(cache_file, 'r', encoding='utf-8') as f:
            albums = json.load(f)
        print(f"Using cached albums from {cache_file}")
    
    print("\n" + "=" * 60)
    print("Matching albums to travel posts...")
    print("=" * 60)
    
    matches = []
    unmatched = []
    
    for album in albums:
        city_chinese = parse_album_title(album['title'])
        if not city_chinese:
            unmatched.append(album)
            continue
        
        city_english = get_english_name(city_chinese)
        if not city_english:
            print(f"⚠ Unknown city: {city_chinese} (add to CITY_NAME_MAP)")
            unmatched.append(album)
            continue
        
        md_file = find_md_file(city_chinese, city_english)
        if md_file:
            matches.append({
                'album': album,
                'city_chinese': city_chinese,
                'city_english': city_english,
                'md_file': md_file
            })
            print(f"✓ {album['title']} -> {md_file.name}")
        else:
            print(f"✗ No MD file for: {city_chinese} ({city_english})")
            unmatched.append(album)
    
    print("\n" + "=" * 60)
    print(f"Matched: {len(matches)} albums")
    print(f"Unmatched: {len(unmatched)} albums")
    print("=" * 60)
    
    if args.dry_run:
        print("\n[DRY RUN] No changes made.")
        return
    
    # Generate download script for matched albums without images
    download_items = []
    for match in matches:
        city = match['city_english']
        image_path = Path(IMAGE_DIR) / f"{city}-0.jpg"
        
        if not image_path.exists():
            print(f"\n📷 Fetching cover for {match['city_chinese']}...")
            cover_url = fetch_album_cover(match['album']['url'], cookie)
            
            if cover_url:
                download_items.append({
                    'city': city,
                    'img_url': cover_url,
                    'image_filename': f"{city}-0.jpg",
                    'album_url': match['album']['url']
                })
                print(f"  ✓ {cover_url}")
            
            time.sleep(random.uniform(2, 4))
    
    if download_items:
        script_lines = ["#!/bin/bash", "mkdir -p images/in-post", ""]
        for item in download_items:
            script_lines.append(f"echo 'Downloading {item['image_filename']}...'")
            script_lines.append(f"curl -L -H 'Referer: https://www.douban.com/' \\")
            script_lines.append(f"     -H 'User-Agent: Mozilla/5.0' \\")
            script_lines.append(f"     '{item['img_url']}' \\")
            script_lines.append(f"     -o 'images/in-post/{item['image_filename']}'")
            script_lines.append("")
        
        with open("download_matched.sh", 'w', encoding='utf-8') as f:
            f.write('\n'.join(script_lines))
        os.chmod("download_matched.sh", 0o755)
        
        print(f"\n✓ Created download_matched.sh for {len(download_items)} images")
        print("  Run: ./download_matched.sh")


if __name__ == "__main__":
    main()
