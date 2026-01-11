#!/usr/bin/env python3
"""
Sync Douban Books - Fetch books from Douban collection
Syncs: collect (已读), do (在读), wish (想读)
Usage: python3 sync_douban_books.py [--cookie COOKIE]
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import re
from datetime import datetime
import json
import argparse
import os
import sys

# Configuration
USER_ID = "shuoleo"
BASE_URLS = {
    'collect': f"https://book.douban.com/people/{USER_ID}/collect",  # 已读
    'do': f"https://book.douban.com/people/{USER_ID}/do",            # 在读
    'wish': f"https://book.douban.com/people/{USER_ID}/wish",        # 想读
}
DATA_DIR = "_data/books"
IMAGE_DIR = "images/books"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://book.douban.com/'
}


def download_image(url, book_id):
    """Download book cover image to local directory"""
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    
    ext = '.jpg'
    if '.' in url:
        ext_match = re.search(r'\.(jpg|jpeg|png|webp)', url, re.I)
        if ext_match:
            ext = '.' + ext_match.group(1).lower()
    
    filename = f"{book_id}{ext}"
    local_path = os.path.join(IMAGE_DIR, filename)
    
    if os.path.exists(local_path):
        return f"/{IMAGE_DIR}/{filename}"
        
    try:
        headers = HEADERS.copy()
        r = requests.get(url, headers=headers, stream=True, timeout=10)
        if r.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            print(f"  Downloaded cover: {filename}")
            return f"/{IMAGE_DIR}/{filename}"
    except Exception as e:
        print(f"  Failed to download image: {e}")
        
    return url


def extract_book_id_from_url(url):
    """Extract book ID from douban URL"""
    # URL format: https://book.douban.com/subject/35196328/
    match = re.search(r'/subject/(\d+)/', url)
    if match:
        return match.group(1)
    return None


def get_book_details(url, cookie):
    """Fetch additional metadata from the book detail page"""
    headers = HEADERS.copy()
    headers['Cookie'] = cookie
    
    try:
        time.sleep(random.uniform(1, 2))
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            print(f"  ! HTTP {r.status_code}")
            return {}
        
        soup = BeautifulSoup(r.text, 'html.parser')
        details = {}
        
        # Book info section
        info_section = soup.select_one('#info')
        if info_section:
            text = info_section.get_text()
            
            # Author
            author_match = re.search(r'作者[:\s：]+(.+?)(?:\n|出版社)', text)
            if author_match:
                details['author'] = author_match.group(1).strip()
            
            # Publisher
            pub_match = re.search(r'出版社[:\s：]+(.+?)(?:\n|出品方|译者|出版年)', text)
            if pub_match:
                details['publisher'] = pub_match.group(1).strip()
            
            # Translator
            translator_match = re.search(r'译者[:\s：]+(.+?)(?:\n|出版社|出版年)', text)
            if translator_match:
                details['translator'] = translator_match.group(1).strip()
            
            # Publish date
            date_match = re.search(r'出版年[:\s：]+(.+?)(?:\n|页数|定价)', text)
            if date_match:
                details['publish_date'] = date_match.group(1).strip()
            
            # Pages
            pages_match = re.search(r'页数[:\s：]+(\d+)', text)
            if pages_match:
                details['pages'] = pages_match.group(1)
            
            # ISBN
            isbn_match = re.search(r'ISBN[:\s：]+(\d+)', text)
            if isbn_match:
                details['isbn'] = isbn_match.group(1)
        
        # Rating
        rating_el = soup.select_one('.rating_num')
        if rating_el:
            details['douban_rating'] = rating_el.get_text(strip=True)
        
        rating_count_el = soup.select_one('.rating_people span')
        if rating_count_el:
            details['rating_count'] = rating_count_el.get_text(strip=True)
        
        return details
    except Exception as e:
        print(f"  Error fetching details: {e}")
        return {}


def parse_book_item(item, cookie):
    """Parse a single book item from the collection list"""
    try:
        book_data = {}
        
        # Extract book link
        title_link = item.select_one('.title a')
        if not title_link:
            return None
            
        book_url = title_link.get('href')
        book_data['douban_url'] = book_url
        
        book_id = extract_book_id_from_url(book_url)
        if not book_id:
            return None
        book_data['book_id'] = book_id
        
        # Title
        book_data['title'] = title_link.get_text(strip=True)
        
        # Cover image
        cover_el = item.select_one('.pic img')
        if cover_el:
            cover_url = cover_el.get('src', '')
            # Get larger image
            cover_url = cover_url.replace('/s/', '/l/')
            book_data['cover'] = download_image(cover_url, book_id)
        
        # Pub info (author / publisher / date)
        pub_el = item.select_one('.pub')
        if pub_el:
            pub_text = pub_el.get_text(strip=True)
            parts = pub_text.split('/')
            if len(parts) >= 1:
                book_data['author'] = parts[0].strip()
            if len(parts) >= 2:
                book_data['publisher'] = parts[-2].strip()
            if len(parts) >= 3:
                book_data['publish_date'] = parts[-1].strip()
        
        # My rating
        rating_el = item.select_one('.rating')
        if rating_el:
            stars = rating_el.select('.rating-star')
            if stars:
                class_name = stars[0].get('class', [])
                for cls in class_name:
                    if cls.startswith('rating'):
                        try:
                            rating = int(cls.replace('rating', '').replace('-t', ''))
                            book_data['my_rating'] = rating // 10
                        except:
                            pass
        
        # Read date
        date_el = item.select_one('.date')
        if date_el:
            date_text = date_el.get_text(strip=True)
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', date_text)
            if date_match:
                book_data['read_date'] = date_match.group(1)
        
        # My comment
        comment_el = item.select_one('.comment')
        if comment_el:
            book_data['my_comment'] = comment_el.get_text(strip=True)
        
        # Get more details from book page
        details = get_book_details(book_url, cookie)
        book_data.update(details)
        
        print(f"  ✓ {book_data['title']}")
        return book_data
        
    except Exception as e:
        print(f"  Error parsing book: {e}")
        return None


def load_existing_data():
    """Load existing book data from all.json"""
    filepath = os.path.join(DATA_DIR, "all.json")
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return []


def save_data(data):
    """Save book data to JSON file"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    filepath = os.path.join(DATA_DIR, "all.json")
    
    # Sort by publish_date descending (newest first)
    def get_publish_year(item):
        pd = item.get('publish_date', '')
        # Extract year from various formats like "2024-1-1", "2024年", "2024"
        match = re.search(r'(\d{4})', str(pd))
        return match.group(1) if match else '0000'
    
    data.sort(key=get_publish_year, reverse=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Saved {len(data)} books to {filepath}")


def scrape_list(list_type, base_url, cookie, existing_ids, max_pages=50):
    """Scrape books from a specific list (collect/do/wish)"""
    print(f"\n{'='*60}")
    print(f"Syncing: {list_type} ({base_url})")
    print(f"{'='*60}")
    
    headers = HEADERS.copy()
    headers['Cookie'] = cookie
    
    new_items = []
    page = 0
    
    while page < max_pages:
        start = page * 15
        url = f"{base_url}?start={start}&sort=time&rating=all&filter=all&mode=list"
        
        print(f"\nPage {page + 1}: {url}")
        
        try:
            time.sleep(random.uniform(2, 4))
            r = requests.get(url, headers=headers, timeout=15)
            
            if r.status_code != 200:
                print(f"  ! HTTP {r.status_code}")
                break
                
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Find book items
            items = soup.select('.list-view .item')
            
            if not items:
                items = soup.select('.subject-item')
            
            if not items:
                print("  No more books found")
                break
            
            print(f"  Found {len(items)} books")
            
            for item in items:
                book_data = parse_book_item(item, cookie)
                if book_data and book_data.get('book_id'):
                    if book_data['book_id'] not in existing_ids:
                        # Add status field
                        book_data['status'] = list_type
                        new_items.append(book_data)
                        existing_ids.add(book_data['book_id'])
            
            page += 1
            
        except Exception as e:
            print(f"  Error: {e}")
            break
    
    return new_items


def scrape_books(cookie, max_pages=None):
    """Scrape all books from Douban - collect, do, wish lists"""
    print(f"Syncing Douban books (collect + do + wish)...")
    
    existing_items = load_existing_data()
    existing_ids = {item.get('book_id') for item in existing_items if item.get('book_id')}
    print(f"Existing books: {len(existing_ids)}")
    
    all_new_items = []
    max_page_limit = max_pages if max_pages else 50
    
    # Sync all three lists
    for list_type, base_url in BASE_URLS.items():
        new_items = scrape_list(list_type, base_url, cookie, existing_ids, max_page_limit)
        all_new_items.extend(new_items)
        print(f"\n{list_type}: Added {len(new_items)} new books")
    
    # Merge with existing (update status if book exists)
    existing_by_id = {item.get('book_id'): item for item in existing_items}
    
    for new_item in all_new_items:
        book_id = new_item.get('book_id')
        if book_id in existing_by_id:
            # Update status if changed
            existing_by_id[book_id]['status'] = new_item.get('status', 'collect')
        else:
            existing_by_id[book_id] = new_item
    
    unique_items = list(existing_by_id.values())
    
    save_data(unique_items)
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  New books added: {len(all_new_items)}")
    print(f"  Total books: {len(unique_items)}")
    
    # Count by status
    status_counts = {}
    for item in unique_items:
        status = item.get('status', 'collect')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    for status, count in status_counts.items():
        label = {'collect': '已读', 'do': '在读', 'wish': '想读'}.get(status, status)
        print(f"  {label}: {count}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description='Sync Douban Books Collection')
    parser.add_argument('--cookie', type=str, help='Douban cookie string')
    parser.add_argument('--max-pages', type=int, default=None, help='Max pages to fetch')
    args = parser.parse_args()
    
    # Load cookie
    cookie = args.cookie
    if not cookie:
        cookie_path = os.path.expanduser("~/.douban.cookie")
        if os.path.exists(cookie_path):
            try:
                with open(cookie_path, 'r', encoding='utf-8') as f:
                    cookie = f.read().strip()
                print(f"Loaded cookie from {cookie_path}")
            except Exception as e:
                print(f"Error reading cookie: {e}")
        else:
            print(f"Cookie file not found: {cookie_path}")
    
    if not cookie:
        print("Error: No cookie provided.")
        print("Usage: python3 sync_douban_books.py --cookie 'your_cookie'")
        print("   or: echo 'your_cookie' > ~/.douban.cookie")
        sys.exit(1)
    
    scrape_books(cookie, args.max_pages)


if __name__ == "__main__":
    main()
