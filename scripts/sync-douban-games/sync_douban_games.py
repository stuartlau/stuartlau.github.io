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
BASE_URL = f"https://www.douban.com/people/{USER_ID}/games"
DATA_DIR = "_data/games"
IMAGE_DIR = "images/games"

def download_image(url, game_id):
    """Download game cover image to local directory"""
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    
    ext = '.jpg'
    if '.' in url:
        ext_match = re.search(r'\.(jpg|jpeg|png|webp)', url, re.I)
        if ext_match:
            ext = '.' + ext_match.group(1).lower()
    
    filename = f"{game_id}{ext}"
    local_path = os.path.join(IMAGE_DIR, filename)
    
    if os.path.exists(local_path):
        return f"/{IMAGE_DIR}/{filename}"
        
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.douban.com/'
        }
        r = requests.get(url, headers=headers, stream=True, timeout=10)
        if r.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded cover: {filename}")
            return f"/{IMAGE_DIR}/{filename}"
    except Exception as e:
        print(f"Failed to download image {url}: {e}")
        
    return url

def extract_game_id_from_url(url):
    """Extract game ID from douban URL"""
    # URL format: https://www.douban.com/game/10734307/
    match = re.search(r'/game/(\d+)/', url)
    if match:
        return match.group(1)
    return None

def get_game_details(url, cookie):
    """Fetch additional metadata from the game detail page"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': cookie,
        'Referer': 'https://www.douban.com/'
    }
    try:
        time.sleep(random.uniform(1.5, 3))
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            print(f"  ! HTTP {r.status_code} for {url}")
            return {}
        
        soup = BeautifulSoup(r.text, 'html.parser')
        details = {}
        
        # Try multiple selectors for game info
        # Selector 1: .game-attr dl
        info_section = soup.select_one('.game-attr')
        if not info_section:
            info_section = soup.select_one('#content .aside')
        if not info_section:
            info_section = soup.select_one('.mod')
        
        if info_section:
            # Parse dt/dd pairs
            dt_elements = info_section.select('dt')
            for dt in dt_elements:
                label = dt.get_text(strip=True).replace(':', '').replace('：', '')
                dd = dt.find_next_sibling('dd')
                if dd:
                    value = dd.get_text(strip=True)
                    if label == '类型':
                        details['genres'] = [g.strip() for g in value.split('/') if g.strip()]
                    elif label == '平台':
                        details['platforms'] = [p.strip() for p in value.split('/') if p.strip()]
                    elif label in ['发行日期', '发行时间', '发布日期']:
                        date_match = re.search(r'(\d{4}[-年/]\d{1,2}[-月/]\d{1,2})', value)
                        if date_match:
                            date_str = date_match.group(1)
                            date_str = date_str.replace('年', '-').replace('月', '-').replace('日', '').replace('/', '-')
                            details['release_date'] = date_str
                        else:
                            year_match = re.search(r'(\d{4})', value)
                            if year_match:
                                details['release_date'] = year_match.group(1)
                    elif label == '开发商':
                        details['developer'] = value
                    elif label == '发行商':
                        details['publisher'] = value
                    elif label == '别名':
                        details['alias'] = value
        
        # Alternative: parse from text content
        if not details.get('genres') or not details.get('platforms'):
            page_text = soup.get_text()
            
            # Try to find platform in text
            platform_match = re.search(r'平台[：:]\s*([^\n]+)', page_text)
            if platform_match and not details.get('platforms'):
                platforms = platform_match.group(1).strip()
                details['platforms'] = [p.strip() for p in platforms.split('/') if p.strip()]
            
            # Try to find genres
            genre_match = re.search(r'类型[：:]\s*([^\n]+)', page_text)
            if genre_match and not details.get('genres'):
                genres = genre_match.group(1).strip()
                details['genres'] = [g.strip() for g in genres.split('/') if g.strip()]
            
            # Try to find release date
            release_match = re.search(r'发行日期[：:]\s*(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})', page_text)
            if release_match and not details.get('release_date'):
                date_str = release_match.group(1)
                date_str = date_str.replace('年', '-').replace('月', '-').replace('/', '-')
                details['release_date'] = date_str
            
            # Try to find developer
            dev_match = re.search(r'开发商[：:]\s*([^\n]+)', page_text)
            if dev_match and not details.get('developer'):
                details['developer'] = dev_match.group(1).strip()
            
            # Try to find publisher
            pub_match = re.search(r'发行商[：:]\s*([^\n]+)', page_text)
            if pub_match and not details.get('publisher'):
                details['publisher'] = pub_match.group(1).strip()
            
            # Try to find alias
            alias_match = re.search(r'别名[：:]\s*([^\n]+)', page_text)
            if alias_match and not details.get('alias'):
                details['alias'] = alias_match.group(1).strip()
        
        # Rating - try multiple selectors
        rating_elem = soup.select_one('.rating-star-small-score')
        if not rating_elem:
            rating_elem = soup.select_one('.rating_num')
        if not rating_elem:
            rating_elem = soup.select_one('.ll.rating_num')
        if rating_elem:
            rating_text = rating_elem.get_text(strip=True)
            if rating_text:
                details['douban_rating'] = rating_text
        
        # Rating count
        rating_count = soup.select_one('.rating-count')
        if not rating_count:
            rating_count = soup.select_one('.rating_sum span')
        if rating_count:
            count_text = rating_count.get_text(strip=True)
            count_match = re.search(r'(\d+)', count_text)
            if count_match:
                details['rating_count'] = count_match.group(1)
        
        # Description
        intro = soup.select_one('.mod.game-intro .bd')
        if not intro:
            intro = soup.select_one('#link-report')
        if intro:
            desc_text = intro.get_text(strip=True)[:500]
            if desc_text:
                details['description'] = desc_text

        return details
    except Exception as e:
        print(f"Error fetching details for {url}: {e}")
        import traceback
        traceback.print_exc()
        return {}


def parse_game_item(item, cookie):
    """Parse a single game item from the HTML"""
    try:
        game_data = {}
        
        # Extract game link
        title_link = item.select_one('.title a')
        if not title_link:
            return None
            
        game_url = title_link.get('href')
        game_data['douban_url'] = game_url
        
        game_id = extract_game_id_from_url(game_url)
        if not game_id:
            return None
        game_data['game_id'] = game_id
        
        # Extract title
        title = title_link.get_text(strip=True)
        game_data['title'] = title
        
        # Extract cover image
        cover_img = item.select_one('.pic img')
        if cover_img:
            cover_url = cover_img.get('src')
            if cover_url:
                cover_url = cover_url.replace('/s_', '/l_')
                game_data['cover'] = download_image(cover_url, game_id)

        # Fetch extra details from game page
        print(f"  > Fetching details for: {game_data['title']}...")
        details = get_game_details(game_url, cookie)
        game_data.update(details)
        
        # Extract my rating (stars)
        rating_el = item.select_one('.rating .date em')
        if rating_el:
            rating_class = rating_el.get('class', [])
            for cls in rating_class:
                if cls.startswith('rating'):
                    rating_match = re.search(r'rating(\d+)', cls)
                    if rating_match:
                        game_data['my_rating'] = int(rating_match.group(1))
                        break
        
        # Extract played date
        date_el = item.select_one('.date')
        if date_el:
            date_text = date_el.get_text(strip=True)
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', date_text)
            if date_match:
                game_data['played_date'] = date_match.group(1)
        
        # Extract my comment
        comment_el = item.select_one('.comment')
        if comment_el:
            comment_text = comment_el.get_text(strip=True)
            if comment_text:
                game_data['my_comment'] = comment_text
        
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
                game_data['tags'] = tags
        
        return game_data
        
    except Exception as e:
        print(f"Error parsing game item: {e}")
        return None

def load_existing_data():
    """Load existing game data from all.json"""
    filepath = os.path.join(DATA_DIR, "all.json")
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(data):
    """Save game data to JSON file"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    filepath = os.path.join(DATA_DIR, "all.json")
    
    # Sort by played date descending
    data.sort(key=lambda x: x.get('played_date', ''), reverse=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data)} games to {filepath}")

def scrape_games(cookie, max_pages=None):
    """Scrape all games from Douban"""
    print(f"Syncing all Douban games (collection)...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': cookie,
        'Upgrade-Insecure-Requests': '1',
    }
    
    existing_items = load_existing_data()
    existing_ids = {item.get('game_id') for item in existing_items if item.get('game_id')}
    
    new_items = []
    
    page = 0
    max_page_limit = max_pages if max_pages else 50
    
    while page < max_page_limit:
        print(f"Fetching page {page}...", flush=True)
        url = f"{BASE_URL}?action=collect" if page == 0 else f"{BASE_URL}?action=collect&start={page * 15}"
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"Error {response.status_code} fetching page {page}.")
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find game items
            items = soup.select('.game-list .common-item')
            
            if not items:
                print("No more items found, reached end of list.")
                break
            
            print(f"Found {len(items)} games on page {page}")
            
            for item in items:
                try:
                    game_data = parse_game_item(item, cookie)
                    if not game_data:
                        continue
                    
                    game_id = game_data.get('game_id')
                    
                    existing_item = next((i for i in existing_items if i.get('game_id') == game_id), None)
                    
                    if existing_item:
                        missing_fields = (
                            not existing_item.get('douban_rating') or
                            not existing_item.get('release_date') or
                            not existing_item.get('genres') or
                            not existing_item.get('platforms')
                        )
                        if missing_fields:
                            print(f"  * Updating metadata for: {game_data.get('title')}")
                            existing_item.update(game_data)
                    else:
                        new_items.append(game_data)
                        existing_ids.add(game_id)
                        played_date = game_data.get('played_date', 'N/A')
                        print(f"  + {game_data.get('title')} ({played_date})")
                except Exception as e:
                    print(f"Error processing item: {e}")
                    continue
                
            page += 1
            time.sleep(random.uniform(2, 4))
            
        except Exception as e:
            print(f"Error occurred: {e}")
            break
    
    if new_items:
        print(f"\nFound {len(new_items)} new games.")
        all_data = existing_items + new_items
    else:
        print("\nNo new games found.")
        all_data = existing_items
    
    save_data(all_data)
    
    return len(new_items)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sync Douban Games (Collection)')
    parser.add_argument('--max-pages', type=int, help='Maximum number of pages to fetch')
    parser.add_argument('--cookie', type=str, help='Douban cookie string')
    
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

    num_new = scrape_games(cookie, args.max_pages)
    
    json_file = os.path.join(DATA_DIR, "all.json")
    
    if os.path.exists(json_file):
        try:
            import subprocess
            print("\nChecking for changes to commit...")
            
            subprocess.run(["git", "add", json_file], check=True)
            
            if os.path.exists(IMAGE_DIR):
                subprocess.run(["git", "add", IMAGE_DIR], check=True)
            
            status = subprocess.run(["git", "diff", "--staged", "--name-only"], capture_output=True, text=True)
            
            if status.stdout.strip():
                commit_msg = f"chore: sync douban games (+{num_new} new)"
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
