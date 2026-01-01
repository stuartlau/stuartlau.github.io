#!/usr/bin/env python3
"""
Script to add header images to travel blog posts.
Processes markdown files in blogs/travelling/ directory:
1. Checks if header-img exists
2. If not, finds Douban album URL
3. Fetches first image from the album
4. Downloads image to images/in-post/
5. Adds header-img to front matter
"""

import os
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time

# Configuration
BLOG_DIR = "blogs/travelling"
IMAGE_DIR = "images/in-post"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_city_name(filename):
    """Extract city name from filename like '2017-07-31-Osaka.md'"""
    match = re.match(r'\d{4}-\d{2}-\d{2}-(.+)\.md', filename)
    if match:
        return match.group(1)
    return None

def has_header_img(content):
    """Check if markdown content already has header-img"""
    return re.search(r'^header-img:\s*.+', content, re.MULTILINE) is not None

def extract_douban_url(content):
    """Extract first Douban album URL from content"""
    match = re.search(r'https://www\.douban\.com/photos/album/(\d+)', content)
    if match:
        return match.group(0)
    return None

def fetch_douban_image_url(album_url):
    """Fetch cover/first image URL from Douban album page"""
    try:
        print(f"  Fetching album: {album_url}")
        response = requests.get(album_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. Try finding data-image (often used for cover sharing)
        share_el = soup.find(attrs={"data-image": True})
        if share_el:
            img_url = share_el['data-image']
            img_url = img_url.replace('/thumb/', '/l/').replace('/m/', '/l/')
            print(f"  Found data-image cover: {img_url}")
            return img_url

        # 2. Try to find cover image CSS selector
        cover_img = soup.select_one('.cover img')
        if cover_img and cover_img.get('src'):
            img_url = cover_img['src'].replace('/m/', '/l/').replace('/thumb/', '/l/')
            print(f"  Found cover image: {img_url}")
            return img_url
        
        # 3. Fallback to first photo in the album
        first_photo = soup.select_one('.photolst img')
        if first_photo and first_photo.get('src'):
            img_url = first_photo['src'].replace('/m/', '/l/').replace('/thumb/', '/l/')
            print(f"  Found first photo: {img_url}")
            return img_url
            
        print("  No image found in album")
        return None
        
    except Exception as e:
        print(f"  Error fetching album {album_url}: {e}")
        return None

def download_image(img_url, save_path):
    """Download image from URL to local path"""
    try:
        print(f"  Downloading image to: {save_path}")
        response = requests.get(img_url, headers=HEADERS, timeout=10, stream=True)
        response.raise_for_status()
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"  Image downloaded successfully")
        return True
        
    except Exception as e:
        print(f"  Error downloading image: {e}")
        return False

def add_header_img_to_frontmatter(content, header_img_value):
    """Add or update header-img in YAML front matter"""
    # Find the front matter boundaries
    lines = content.split('\n')
    
    if not lines or not lines[0].strip() == '---':
        print("  Warning: No front matter found")
        return content
    
    # Check if header-img already exists
    exists_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            break
        if lines[i].startswith('header-img:'):
            exists_idx = i
    
    if exists_idx != -1:
        # Update existing
        lines[exists_idx] = f'header-img: {header_img_value}'
        return '\n'.join(lines)
    
    # Insert new
    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end_idx = i
            break
    
    if end_idx == -1:
        return content
        
    insert_idx = end_idx
    for i in range(1, end_idx):
        if lines[i].startswith('author:'):
            insert_idx = i + 1
            break
    
    lines.insert(insert_idx, f'header-img: {header_img_value}')
    return '\n'.join(lines)

def process_markdown_file(filepath):
    """Process a single markdown file"""
    filename = os.path.basename(filepath)
    print(f"\nProcessing: {filename}")
    
    # Read file content
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract Douban URL
    douban_url = extract_douban_url(content)
    if not douban_url:
        print("  No Douban album URL found, skipping")
        return
    
    # Extract city name
    city_name = extract_city_name(filename)
    if not city_name:
        print("  Could not extract city name, skipping")
        return
    
    # Fetch image URL from Douban
    img_url = fetch_douban_image_url(douban_url)
    if not img_url:
        print("  Could not fetch image URL, skipping")
        return
    
    # Download image
    image_filename = f"{city_name}-0.jpg"
    image_path = os.path.join(IMAGE_DIR, image_filename)
    
    if not download_image(img_url, image_path):
        print("  Failed to download image, skipping")
        return
    
    # Add or update header-img in front matter
    header_img_value = f"img/in-post/{image_filename}"
    updated_content = add_header_img_to_frontmatter(content, header_img_value)
    
    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"  ✓ Successfully synced header-img: {header_img_value}")
    
    # Be nice to Douban servers
    time.sleep(2)

def main():
    """Main function to process all markdown files"""
    print("Starting header image processing...")
    print(f"Blog directory: {BLOG_DIR}")
    print(f"Image directory: {IMAGE_DIR}")
    print("-" * 60)
    
    # Get all markdown files
    md_files = sorted(Path(BLOG_DIR).glob("*.md"))
    
    print(f"Found {len(md_files)} markdown files")
    
    processed = 0
    skipped = 0
    errors = 0
    
    for md_file in md_files:
        try:
            process_markdown_file(str(md_file))
            processed += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            errors += 1
            skipped += 1
    
    print("\n" + "=" * 60)
    print(f"Processing complete!")
    print(f"  Processed: {processed}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors: {errors}")

if __name__ == "__main__":
    main()
