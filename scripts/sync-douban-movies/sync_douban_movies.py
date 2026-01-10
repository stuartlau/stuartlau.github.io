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
import hashlib

# Configuration
USER_ID = "shuoleo"
BASE_URL = f"https://movie.douban.com/people/{USER_ID}/collect"
DATA_DIR = "_data/movies"
IMAGE_DIR = "images/movies"

def download_image(url, movie_id):
    """Download movie poster image to local directory"""
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    
    # Generate filename from movie_id
    # Extract file extension from URL
    ext = '.jpg'
    if '.' in url:
        ext_match = re.search(r'\.(jpg|jpeg|png|webp)', url, re.I)
        if ext_match:
            ext = '.' + ext_match.group(1).lower()
    
    filename = f"{movie_id}{ext}"
    local_path = os.path.join(IMAGE_DIR, filename)
    
    # If already exists, return local path
    if os.path.exists(local_path):
        return f"/{IMAGE_DIR}/{filename}"
        
    try:
        # Douban images might need referer
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://movie.douban.com/'
        }
        r = requests.get(url, headers=headers, stream=True, timeout=10)
        if r.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded poster: {filename}")
            return f"/{IMAGE_DIR}/{filename}"
    except Exception as e:
        print(f"Failed to download image {url}: {e}")
        
    return url  # Return original URL if download fails

def extract_movie_id_from_url(url):
    """Extract movie ID from douban URL"""
    # URL format: https://movie.douban.com/subject/1292052/
    match = re.search(r'/subject/(\d+)/', url)
    if match:
        return match.group(1)
    return None

def get_subject_details(url, cookie):
    """Fetch additional metadata from the movie detail page"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': cookie,
        'Referer': 'https://movie.douban.com/'
    }
    try:
        time.sleep(random.uniform(1.5, 3)) # Polite delay
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            print(f"  ! HTTP {r.status_code} for {url}")
            return {}
        
        soup = BeautifulSoup(r.text, 'html.parser')
        info = soup.select_one('#info')
        if not info:
            print(f"  ! No #info found for {url}")
            return {}

        details = {}
        info_text = info.get_text()
        
        # Helper for labeled info (handles text after label)
        def get_data_by_label(label):
            spans = info.select('.pl')
            target = next((s for s in spans if label in s.get_text()), None)
            if not target: return None
            
            result = []
            curr = target.next_sibling
            while curr and curr.name != 'br':
                if hasattr(curr, 'get_text'):
                    result.append(curr.get_text())
                else:
                    text = str(curr).strip()
                    if text:
                        result.append(text)
                curr = curr.next_sibling
            
            res_str = "".join(result).strip()
            return re.sub(r'^[:\s]*', '', res_str).strip()

        # Helper for .attrs (linked cast/directors)
        def get_attrs_by_label(label):
            spans = info.select('.pl')
            target = next((s for s in spans if label in s.get_text()), None)
            if not target: return None
            attrs = target.find_next_sibling('span', class_='attrs')
            return attrs.get_text(strip=True) if attrs else None

        # Directors, writers, cast
        details['directors'] = [d.strip() for d in (get_attrs_by_label('导演') or "").split('/') if d.strip()]
        details['writers'] = [w.strip() for w in (get_attrs_by_label('编剧') or "").split('/') if w.strip()]
        details['cast'] = [c.strip() for c in (get_attrs_by_label('主演') or "").split('/') if c.strip()]
        
        # Genres from property tags
        details['genres'] = [g.get_text() for g in soup.select('span[property="v:genre"]')]
        
        # Other metadata
        details['countries'] = get_data_by_label('制片国家/地区')
        details['languages'] = get_data_by_label('语言')
        details['episodes'] = get_data_by_label('集数')
        details['duration'] = get_data_by_label('单集片长') or get_data_by_label('片长')
        
        # Release date - extract from 上映日期 or 首播
        release_date_raw = get_data_by_label('上映日期') or get_data_by_label('首播')
        if release_date_raw:
            # Parse: "2024-07-16(中国大陆) / 2024-07-13(大规模点映)" -> "2024-07-16"
            # Or from property tags
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', release_date_raw)
            if date_match:
                details['pub_date'] = date_match.group(1)
        
        # Also try from property tag if not found
        if 'pub_date' not in details:
            init_release = soup.select_one('span[property="v:initialReleaseDate"]')
            if init_release:
                date_text = init_release.get_text(strip=True)
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', date_text)
                if date_match:
                    details['pub_date'] = date_match.group(1)
                else:
                    # Try year only
                    year_match = re.search(r'(\d{4})', date_text)
                    if year_match:
                        details['pub_date'] = year_match.group(1)
        
        # Extract year from title area if still missing
        if 'pub_date' not in details:
            year_span = soup.select_one('.year')
            if year_span:
                year_match = re.search(r'(\d{4})', year_span.get_text())
                if year_match:
                    details['pub_date'] = year_match.group(1)
        
        # Rating
        rating_val = soup.select_one('strong[property="v:average"]')
        if rating_val:
            rating_text = rating_val.get_text(strip=True)
            if rating_text:
                details['douban_rating'] = rating_text
            
        rating_votes = soup.select_one('span[property="v:votes"]')
        if rating_votes:
            details['rating_count'] = rating_votes.get_text(strip=True)
        
        # IMDb ID
        imdb_match = re.search(r'IMDb[:\s]*(tt\d+)', info_text)
        if imdb_match:
            details['imdb_id'] = imdb_match.group(1)
        else:
            # Try from link
            imdb_link = info.select_one('a[href*="imdb.com"]')
            if imdb_link:
                imdb_href = imdb_link.get('href', '')
                imdb_id_match = re.search(r'(tt\d+)', imdb_href)
                if imdb_id_match:
                    details['imdb_id'] = imdb_id_match.group(1)

        return details
    except Exception as e:
        print(f"Error fetching details for {url}: {e}")
        import traceback
        traceback.print_exc()
        return {}

def parse_movie_item(item, cookie):
    """Parse a single movie item from the HTML"""
    try:
        movie_data = {}
        
        # Extract movie link and ID
        title_link = item.select_one('.info .title a')
        if not title_link:
            return None
            
        movie_url = title_link.get('href')
        movie_data['douban_url'] = movie_url
        
        movie_id = extract_movie_id_from_url(movie_url)
        if not movie_id:
            return None
        movie_data['movie_id'] = movie_id
        
        # Extract title
        title = title_link.get_text(strip=True)
        # Split Chinese and original title
        if ' / ' in title:
            parts = title.split(' / ', 1)
            movie_data['title'] = parts[0].strip()
            movie_data['original_title'] = parts[1].strip()
        else:
            movie_data['title'] = title
            movie_data['original_title'] = title
        
        # Extract poster image
        poster_img = item.select_one('.pic img')
        if poster_img:
            poster_url = poster_img.get('src')
            if poster_url:
                poster_url = poster_url.replace('s_ratio_poster', 'l_ratio_poster')
                movie_data['poster'] = download_image(poster_url, movie_id)

        # Fetch extra details from subject page
        print(f"  > Fetching details for: {movie_data['title']}...")
        details = get_subject_details(movie_url, cookie)
        movie_data.update(details)
        
        # Extract my rating
        rating_el = item.select_one('.date em')
        if rating_el:
            rating_class = rating_el.get('class', [])
            for cls in rating_class:
                if cls.startswith('rating'):
                    rating_match = re.search(r'rating(\d+)', cls)
                    if rating_match:
                        movie_data['my_rating'] = int(rating_match.group(1))
                        break
        
        # Extract watched date
        date_el = item.select_one('.date')
        if date_el:
            date_text = date_el.get_text(strip=True)
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', date_text)
            if date_match:
                movie_data['watched_date'] = date_match.group(1)
        
        # Extract my comment/review
        comment_el = item.select_one('.comment')
        if comment_el:
            comment_text = comment_el.get_text(strip=True)
            if comment_text:
                movie_data['my_comment'] = comment_text
        
        # Extract tags
        tags_el = item.select('.tags')
        if tags_el:
            tags = []
            for tag in tags_el:
                tag_text = tag.get_text(strip=True)
                tag_text = tag_text.replace('标签:', '').strip()
                if tag_text:
                    tags.extend([t.strip() for t in tag_text.split() if t.strip()])
            if tags:
                movie_data['tags'] = tags
        
        return movie_data
        
    except Exception as e:
        print(f"Error parsing movie item: {e}")
        return None

def load_existing_data():
    """Load existing movie data from all.json"""
    filepath = os.path.join(DATA_DIR, "all.json")
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(data):
    """Save movie data to JSON file"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    filepath = os.path.join(DATA_DIR, "all.json")
    
    # Sort by watched date descending
    data.sort(key=lambda x: x.get('watched_date', ''), reverse=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data)} movies to {filepath}")

def scrape_movies(cookie, max_pages=None):
    """Scrape all movies from Douban (full history)"""
    print(f"Syncing all Douban movies (full history)...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': cookie,
        'Upgrade-Insecure-Requests': '1',
    }
    
    existing_items = load_existing_data()
    # Create a set of existing movie IDs to avoid duplicates
    existing_ids = {item.get('movie_id') for item in existing_items if item.get('movie_id')}
    
    new_items = []
    
    page = 0
    # Douban usually limits to ~1000 items, set max_pages if specified
    max_page_limit = max_pages if max_pages else 100
    
    while page < max_page_limit:
        print(f"Fetching page {page}...", flush=True)
        url = BASE_URL if page == 0 else f"{BASE_URL}?start={page * 15}"
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"Error {response.status_code} fetching page {page}.")
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find movie items
            items = soup.select('.grid-view .item')
            
            if not items:
                print("No more items found, reached end of list.")
                break
            
            print(f"Found {len(items)} movies on page {page}")
            
            for item in items:
                try:
                    movie_data = parse_movie_item(item, cookie)
                    if not movie_data:
                        continue
                    
                    movie_id = movie_data.get('movie_id')
                    
                    # Check if we need to update existing item
                    existing_item = next((i for i in existing_items if i.get('movie_id') == movie_id), None)
                    
                    if existing_item:
                        # Update if missing key metadata
                        missing_fields = (
                            not existing_item.get('douban_rating') or
                            not existing_item.get('pub_date') or
                            not existing_item.get('genres') or
                            not existing_item.get('directors')
                        )
                        if missing_fields:
                            print(f"  * Updating metadata for: {movie_data.get('title')}")
                            existing_item.update(movie_data)
                    else:
                        # New movie
                        new_items.append(movie_data)
                        existing_ids.add(movie_id)
                        watched_date = movie_data.get('watched_date', 'N/A')
                        print(f"  + {movie_data.get('title')} ({watched_date})")
                except Exception as e:
                    print(f"Error processing item: {e}")
                    continue
                
            page += 1
            
            # Random delay to avoid being blocked
            time.sleep(random.uniform(2, 4))
            
        except Exception as e:
            print(f"Error occurred: {e}")
            break
    
    # Merge new items with existing ones and save
    if new_items:
        print(f"\nFound {len(new_items)} new movies.")
        all_data = existing_items + new_items
    else:
        print("\nNo new movies found.")
        all_data = existing_items
    
    save_data(all_data)
    
    return len(new_items)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sync Douban Movies (Full History)')
    
    # Optional max pages argument
    parser.add_argument('--max-pages', type=int, help='Maximum number of pages to fetch (default: 100)')
    
    # Optional cookie argument, defaults to reading from file
    parser.add_argument('--cookie', type=str, help='Douban cookie string (overrides ~/.douban.cookie)')
    
    args = parser.parse_args()
    
    cookie = args.cookie
    if not cookie:
        cookie_path = os.path.expanduser("~/.douban.cookie")
        if os.path.exists(cookie_path):
            try:
                with open(cookie_path, 'r', encoding='utf-8') as f:
                    cookie = f.read().strip()
                print(f"Loaded cookie from {cookie_path}")
            except Exception as e:
                print(f"Error reading cookie file: {e}")
        else:
            print(f"Cookie not provided and file {cookie_path} does not exist.")
            sys.exit(1)
            
    if not cookie:
        print("Error: No cookie provided.")
        sys.exit(1)

    # Scrape all movies
    num_new = scrape_movies(cookie, args.max_pages)
    
    # Git operations
    json_file = os.path.join(DATA_DIR, "all.json")
    
    if os.path.exists(json_file):
        try:
            import subprocess
            print("\nChecking for changes to commit...")
            
            # Add json file
            subprocess.run(["git", "add", json_file], check=True)
            
            # Add images directory
            if os.path.exists(IMAGE_DIR):
                subprocess.run(["git", "add", IMAGE_DIR], check=True)
            
            # Check status
            status = subprocess.run(["git", "diff", "--staged", "--name-only"], capture_output=True, text=True)
            
            if status.stdout.strip():
                commit_msg = f"chore: sync douban movies (full history, +{num_new} new)"
                subprocess.run(["git", "commit", "-m", commit_msg], check=True)
                print(f"Committed changes: {commit_msg}")
                
                print("Pushing to remote...")
                subprocess.run(["git", "push"], check=True)
            else:
                print("No changes detected by git.")
                
        except subprocess.CalledProcessError as e:
            print(f"Git operation failed: {e}")
        except Exception as e:
            print(f"Error during git operations: {e}")
