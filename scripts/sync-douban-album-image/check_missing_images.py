import os
import re
from pathlib import Path

BLOG_DIR = "blogs/travelling"
IMAGE_DIR = "images/in-post"

def extract_albums(content):
    pattern = r'https://www\.douban\.com/photos/album/(\d+)'
    return re.findall(pattern, content)

def extract_city_name(filename):
    match = re.match(r'\d{4}-\d{2}-\d{2}-(.+)\.md', filename)
    return match.group(1) if match else None

def check_missing_images():
    md_files = sorted(Path(BLOG_DIR).glob("*.md"))
    missing = []
    
    for md_file in md_files:
        filename = md_file.name
        city_name = extract_city_name(filename)
        if not city_name: continue
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        album_urls = extract_albums(content)
        for i, album_id in enumerate(album_urls):
            image_filename = f"{city_name}-{i}.jpg"
            image_path = Path(IMAGE_DIR) / image_filename
            if not image_path.exists():
                missing.append({
                    'file': filename,
                    'city': city_name,
                    'index': i,
                    'album_id': album_id,
                    'url': f"https://www.douban.com/photos/album/{album_id}/"
                })
    return missing

if __name__ == "__main__":
    missing = check_missing_images()
    print(f"Total missing images: {len(missing)}")
    for m in missing:
        print(f"{m['url']} -> {m['city']}-{m['index']}.jpg")
