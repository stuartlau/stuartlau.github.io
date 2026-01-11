#!/usr/bin/env python3
"""
Download book covers from Douban - fast parallel version
Usage: python3 download_book_covers.py
"""

import json
import requests
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Referer': 'https://book.douban.com/'
}

IMAGE_DIR = 'images/books'
DATA_FILE = '_data/books/all.json'

def load_cookie():
    """Load Douban cookie from file"""
    cookie_path = os.path.expanduser('~/.douban.cookie')
    if os.path.exists(cookie_path):
        with open(cookie_path, 'r') as f:
            return f.read().strip()
    return None

def get_cover_url(book_id, cookie=None):
    """Fetch book page and extract cover URL"""
    url = f'https://book.douban.com/subject/{book_id}/'
    headers = HEADERS.copy()
    if cookie:
        headers['Cookie'] = cookie
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        
        # Find cover image URL
        match = re.search(r'href="(https://img[^"]+/view/subject/l/[^"]+)"', r.text)
        if not match:
            match = re.search(r'src="(https://img[^"]+/view/subject/[ls]/[^"]+)"', r.text)
        
        if match:
            return match.group(1).replace('/m/', '/l/').replace('/s/', '/l/')
        return None
    except Exception as e:
        print(f"  Error getting cover URL for {book_id}: {e}")
        return None

def download_cover(book_id, cover_url):
    """Download cover image"""
    filepath = f'{IMAGE_DIR}/{book_id}.jpg'
    if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
        return True
    
    try:
        r = requests.get(cover_url, headers=HEADERS, timeout=10)
        if r.status_code == 200 and len(r.content) > 1000:
            with open(filepath, 'wb') as f:
                f.write(r.content)
            return True
    except Exception as e:
        print(f"  Error downloading {book_id}: {e}")
    return False

def process_book(book, cookie):
    """Process a single book: get URL and download"""
    book_id = book.get('book_id')
    title = book.get('title', '')[:25]
    
    filepath = f'{IMAGE_DIR}/{book_id}.jpg'
    if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
        return (book_id, 'exists', title)
    
    cover_url = get_cover_url(book_id, cookie)
    if not cover_url:
        return (book_id, 'no_url', title)
    
    if download_cover(book_id, cover_url):
        return (book_id, 'downloaded', title)
    return (book_id, 'failed', title)

def main():
    os.makedirs(IMAGE_DIR, exist_ok=True)
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        books = json.load(f)
    
    cookie = load_cookie()
    if cookie:
        print("✓ Using cookie for authentication")
    else:
        print("! No cookie found, some requests may fail")
    
    print(f"Processing {len(books)} books...\n")
    
    downloaded = 0
    failed = 0
    existed = 0
    
    # Use thread pool for parallel downloads
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_book, book, cookie): book for book in books}
        
        for future in as_completed(futures):
            book_id, status, title = future.result()
            if status == 'downloaded':
                downloaded += 1
                print(f"✓ {book_id}: {title}")
            elif status == 'exists':
                existed += 1
            else:
                failed += 1
                print(f"✗ {book_id}: {title}")
            
            # Rate limiting
            time.sleep(0.5)
    
    print(f"\n{'='*40}")
    print(f"Downloaded: {downloaded}")
    print(f"Already existed: {existed}")
    print(f"Failed: {failed}")
    print(f"Total: {len(books)}")

if __name__ == '__main__':
    main()
