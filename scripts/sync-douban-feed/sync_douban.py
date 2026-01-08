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

# AI Comment Generation Logic
def generate_ai_comments(content):
    """
    Generates a single, high-quality AI comment.
    Prioritizes LLM API if available, otherwise uses advanced content analysis.
    """
    import os
    import requests
    import random
    
    # 1. Try LLM API
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    
    if api_key:
        try:
            system_prompt = (
                "你是一个温暖、真诚且充满智慧的好友。请对用户的这条朋友圈动态进行评论。"
                "要求：\n"
                "1. 只有一条评论。\n"
                "2. 语气真诚、有爱，言之有理。\n"
                "3. 可以适当给出建议，或者根据内容进行提问互动。\n"
                "4. 不要只做简单的陈述，要有深度的交流感。\n"
                "5. 字数控制在30-80字之间。"
            )
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-4o", # Or user defined model
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content}
                ],
                "temperature": 0.7
            }
            response = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                res_json = response.json()
                comment_text = res_json['choices'][0]['message']['content'].strip()
                if comment_text.startswith('"') and comment_text.endswith('"'):
                    comment_text = comment_text[1:-1]
                return [{
                    "author": "AI好友",
                    "content": comment_text,
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M')
                }]
        except Exception as e:
            print(f"LLM Generation Failed, switching to fallback: {e}")

    # 2. Fallback: Content Analysis (Deterministic & Context-Aware)
    # Similar to the backfill script to ensure consistency without API key
    content_lower = content.lower()
    base = ""
    
    if "书" in content_lower or "读" in content_lower:
        base = "阅读是与灵魂的对话。看你分享的这段，感觉这本书不仅是在讲故事，更是在照镜子。最近心静下来了吗？"
    elif "电影" in content_lower or "看片" in content_lower:
        base = "光影世界总能给人慰藉。这部片子的评价两极分化，但只要能打动你的，就是好电影。准备二刷吗？"
    elif "加班" in content_lower or "工作" in content_lower or "累" in content_lower:
        base = "看着文字都感觉到了你的疲惫。工作是做不完的，但身体是自己的。今晚什么都别想，好好睡一觉，明天又是新的一天！加油！"
    elif "娃" in content_lower or "女儿" in content_lower or "闺女" in content_lower:
        base = "孩子的成长就像一部快进的电影，每一帧都值得珍藏。看她现在的样子，不得不感叹基因的神奇，也为你这个老父亲/老母亲点赞，辛苦啦！"
    elif "吃" in content_lower or "饭" in content_lower or "美味" in content_lower:
        base = "这人间烟火气最抚凡人心。看描述感觉味道一定很棒，是那种吃一口就让人想家或者想起某个老朋友的味道吗？"
    elif "天气" in content_lower or "雨" in content_lower or "雪" in content_lower:
        base = "天气的变化总能影响心境。不管是晴是雨，都把它当成大自然的馈赠吧。记得照顾好自己，别着凉。"
    elif "玩" in content_lower or "旅行" in content_lower:
        base = "身体和灵魂，总有一个要在路上。羡慕你能在这个时刻享受当下的自由。这地方被你拍得真美，种草了！"
    else:
        # General profound comments, deterministic selection based on content
        opts = [
            "平淡的生活里藏着最真实的幸福。记录本身就是一种对抗遗忘的方式，多年后再看这条动态，一定会有不同的感触。",
            "说得真好，生活中的这些小细节往往最容易被忽视，却也最动人。感谢你的分享，让人觉得世界又温柔了一些。",
            "字里行间流露出的那份真挚很难得。在这个喧嚣的世界里，保持一份清醒和敏感度，是多么宝贵的能力。",
            "非常有同感。每个人都是一座孤岛，但通过这些文字，我们似乎又紧密相连了。加油，陌生人也是朋友。",
            "生活就是由这些琐碎拼凑而成的诗。看你的动态总能让人静下心来，仿佛时间都慢了半拍。"
        ]
        idx = hash(content) % len(opts)
        base = opts[idx]

    return [{
        "author": "AI好友",
        "content": base,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M')
    }]

# Configuration
USER_ID = "shuoleo"
BASE_URL = f"https://www.douban.com/people/{USER_ID}/statuses"
DATA_DIR = "_data/douban"
IMAGE_DIR = "images/douban"

def download_image(url):
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    
    # Extract filename from URL (or generate hash)
    filename = url.split('/')[-1]
    # Handle potential query params
    if '?' in filename:
        filename = filename.split('?')[0]
        
    local_path = os.path.join(IMAGE_DIR, filename)
    
    # If already exists, return local path
    if os.path.exists(local_path):
        return f"/{IMAGE_DIR}/{filename}"
        
    try:
        # Douban images might need referer
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.douban.com/'
        }
        r = requests.get(url, headers=headers, stream=True, timeout=10)
        if r.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded image: {filename}")
            return f"/{IMAGE_DIR}/{filename}"
    except Exception as e:
        print(f"Failed to download image {url}: {e}")
        
    return url # Return original URL if download fails

def process_content(item):
    # 1. Extract Text
    text = extract_text(item)
    
    # 2. Extract Images
    images = []
    
    # Debug: Print item HTML if "滴水湖" in text (as user mentioned this has images)
    if "滴水湖" in text or "Meta" in text:
        print(f"DEBUG: Found target post. HTML structure:\n{item.prettify()}\n--- End HTML ---")
    
    # Strategy A: Single image container (.upload-pic)
    # Often structure: <div class="upload-pic"><a href="..."><img src="..."></a></div>
    img_containers = item.select('.upload-pic')
    for container in img_containers:
        img_tag = container.select_one('img')
        if img_tag:
             src = img_tag.get('src')
             if src:
                # Try to get larger image
                # Common patterns: 
                # thumb: https://img9.doubanio.com/view/status/m/public/...
                # large: https://img9.doubanio.com/view/status/l/public/...
                # raw:   https://img9.doubanio.com/view/status/raw/public/...
                large_src = src.replace('/m/', '/l/').replace('/Xs/', '/l/') 
                local_url = download_image(large_src)
                if local_url and local_url not in images:
                    images.append(local_url)

    # Strategy B: Grid images (.upload-pics or similar) -- Douban sometimes changes this
    # Look for any img inside .status-item that isn't the avatar
    # Avatar usually in .mod-bd > .hd or .status-item > .hd or .user-face
    
    # Let's try a broader search if Strategy A found nothing
    if not images:
        all_imgs = item.select('img')
        for img in all_imgs:
            # Skip avatar (usually has class 'icon' or inside specific containers, or size is small)
            # Douban avatars often have 'icon/u' in src or 'doubanio.com/icon'
            src = img.get('src', '')
            if 'icon/u' in src or 'douban_avatar' in src or 'user_normal' in src:
                continue
                
            # Skip small icons/emojis
            if img.get('width') and int(img.get('width')) < 30:
                continue
                
            # It might be a content image
            large_src = src.replace('/m/', '/l/').replace('/Xs/', '/l/')
            local_url = download_image(large_src)
            if local_url and local_url not in images:
                print(f"DEBUG: Found image via fallback strategy: {large_src}")
                images.append(local_url)
    
    # Strategy C: Javascript injected photos (var photos = [...])
    # Douban uses this for multi-image posts in some views
    scripts = item.select('script')
    for script in scripts:
        if 'var photos =' in script.text:
            try:
                # Extract JSON list using regex
                match = re.search(r'var photos = (\[.*?\])', script.text, re.DOTALL)
                if match:
                    json_str = match.group(1)
                    try:
                        photo_data = json.loads(json_str)
                        for p in photo_data:
                            # Structure: {"image": {"large": {"url": "..."}}}
                            if 'image' in p and 'large' in p['image']:
                                img_url = p['image']['large'].get('url')
                                if img_url:
                                    local_url = download_image(img_url)
                                    if local_url and local_url not in images:
                                        print(f"DEBUG: Found image via JS photos: {img_url}")
                                        images.append(local_url)
                    except json.JSONDecodeError:
                         pass # JSON parsing failed
            except Exception as e:
                print(f"DEBUG: Error extracting JS photos: {e}")

    return text, images

def extract_text(item):
    text_selectors = [
        '.bd blockquote p',
        '.status-content .status-text',
        '.bd .content p',
        '.status-saying blockquote p',
        'p.text'
    ]
    for selector in text_selectors:
        el = item.select_one(selector)
        if el:
            txt = el.get_text(separator=" ", strip=True)
            txt = re.sub(r'\s+', ' ', txt).strip()
            txt = re.sub(r'^.*?说[:：]', '', txt).strip()
            if txt: return txt
    return ""

def load_existing_data(year):
    filepath = os.path.join(DATA_DIR, f"{year}.json")
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(year, data):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    filepath = os.path.join(DATA_DIR, f"{year}.json")
    
    # Sort by time descending
    data.sort(key=lambda x: x['time'], reverse=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data)} records to {filepath}")

def scrape(target_year, cookie):
    print(f"Syncing Douban feed for year {target_year}...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': cookie,
        'Upgrade-Insecure-Requests': '1',
    }
    
    existing_items = load_existing_data(target_year)
    # Create a set of existing identifiers to avoid duplicates (using time+content as key)
    existing_keys = {f"{item['time']}|{item.get('content', '')}" for item in existing_items}
    
    new_items = []
    
    page = 0
    max_pages = 200 # Safety limit
    stop_scraping = False
    
    while page < max_pages and not stop_scraping:
        print(f"Fetching page {page}...", flush=True)
        url = BASE_URL if page == 0 else f"{BASE_URL}?p={page}"
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"Error {response.status_code} fetching page {page}.")
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select('.status-item')
            
            if not items:
                print("No items found (login might be required or end of feed).")
                break
                
            for item in items:
                time_el = item.select_one('.created_at')
                if not time_el: continue
                
                full_time = time_el.get('title', '')
                if not full_time: continue
                
                try:
                    dt = datetime.strptime(full_time, '%Y-%m-%d %H:%M:%S')
                    item_year = str(dt.year)
                    
                    if item_year == str(target_year):
                        text, images = process_content(item)
                        # Use time+text for uniqueness.
                        # Normalize content for key generation to match `load_existing_data`
                        if text or images:
                            key = f"{dt.strftime('%Y-%m-%d %H:%M')}|{text}"
                            
                            if key not in existing_keys:
                                record = {
                                    "time": dt.strftime('%Y-%m-%d %H:%M'),
                                    "content": text,
                                    "images": images,
                                    "ai_comments": generate_ai_comments(text if text else "分享图片")
                                }
                                new_items.append(record)
                                existing_keys.add(key)
                            else:
                                # Check if we need to update images for existing item
                                # Find the item in existing_items (this is O(N) inside loop, but data size is small)
                                for ex_item in existing_items:
                                    ex_key = f"{ex_item['time']}|{ex_item.get('content', '')}"
                                    if ex_key == key:
                                        # If existing has no images but we found some, update it
                                        if not ex_item.get('images') and images:
                                            ex_item['images'] = images
                                            print(f"DEBUG: Updated existing item {key[:20]}... with {len(images)} images")
                                            # We need to ensure we save these changes. 
                                            # Since existing_items is passed to save_data, modifying it in place works.
                                            # But we need a flag to know save is needed if new_items is empty.
                                            pass 
                                        break

                    elif int(item_year) < int(target_year):
                        # We reached older data
                        stop_scraping = True
                        break
                        
                except Exception as e:
                    print(f"Error parsing item: {e}")
                    continue
            
            if stop_scraping:
                print("Reached older data, stopping.")
                break
                
            page += 1
            time.sleep(random.uniform(2, 4))
            
        except Exception as e:
            print(f"Error occurred: {e}")
            break
    
    # Merge new items with existing ones and save
    if new_items:
        print(f"Found {len(new_items)} new items.")
        all_data = existing_items + new_items
    else:
        print("No new items found.")
        all_data = existing_items

    # Ensure all items have comments (backfill)
    params_updated = False
    for item in all_data:
        if "ai_comments" not in item:
            content_val = item.get("content", "")
            if not content_val and item.get("images"):
                content_val = "分享图片"
            item["ai_comments"] = generate_ai_comments(content_val)
            params_updated = True
        
        # Check if we updated images in memory (from scrape loop)
        # Simple hack: any item with images but not in new_items implies update
        # But simplify logic: always save if we scraped to ensure latest state?
        # Better: compare `existing_items` (which we modified in place) 
        # But `all_data` refs the same objects. 
        # So we just need to know if ANY change happened.
        # Let's rely on params_updated or new_items, OR force save if we printed debug message.
    
    # Actually, since we modify existing_items in place, and all_data = existing + new
    # We should detect if any existing item has images now. 
    # To be safe and simple: ALways save if we found new items OR if we are running in sync mode (which usually implies updates)
    # Let's check if the file content would change.
    
    # For now, let's assume if we ran scrape, we might have updates.
    # To be precise, let's allow saving if existing items changed.
    # In scrape loop we printed "DEBUG: Updated existing item...". 
    # We can't easily pass a flag out from scrape to here without refactoring.
    
    # REFACTOR: Let's just always save if we have data, sorted. 
    # It's a small JSON file, writing it again is cheap.
    save_data(target_year, all_data)
    
    # if new_items or params_updated:
    #    save_data(target_year, all_data)
    # else:
    #    print("No changes to save.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sync Douban Feed')
    
    # Default year to current year
    current_year = datetime.now().year
    parser.add_argument('--year', type=int, default=current_year, help=f'Target year to sync (default: {current_year})')
    
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

    # Scrape
    target_year = args.year
    scrape(target_year, cookie)
    
    # Git operations
    # Check if there are changes in data directory and image directory
    json_file = os.path.join(DATA_DIR, f"{target_year}.json")
    
    # We should add images too
    
    if os.path.exists(json_file):
        try:
            import subprocess
            print("Checking for changes to commit...")
            
            # Add json file
            subprocess.run(["git", "add", json_file], check=True)
            
            # Add images directory
            if os.path.exists(IMAGE_DIR):
                 subprocess.run(["git", "add", IMAGE_DIR], check=True)
            
            # Check status
            status = subprocess.run(["git", "diff", "--staged", "--name-only"], capture_output=True, text=True)
            
            if status.stdout.strip():
                commit_msg = f"chore: sync douban feed & images for {target_year}"
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
