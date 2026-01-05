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
BASE_URL = f"https://www.douban.com/people/{USER_ID}/statuses"
DATA_DIR = "_data/douban"

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
    existing_keys = {f"{item['time']}|{item['content']}" for item in existing_items}
    
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
                        text = extract_text(item)
                        if text:
                            key = f"{dt.strftime('%Y-%m-%d %H:%M')}|{text}"
                            if key not in existing_keys:
                                record = {
                                    "time": dt.strftime('%Y-%m-%d %H:%M'),
                                    "content": text
                                }
                                new_items.append(record)
                                existing_keys.add(key)
                    
                    elif int(item_year) < int(target_year):
                        # We reached older data
                        stop_scraping = True
                        break
                        
                except Exception as e:
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
        save_data(target_year, all_data)
    else:
        print("No new items found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sync Douban Feed')
    parser.add_argument('--year', type=int, required=True, help='Target year to sync')
    parser.add_argument('--cookie', type=str, required=True, help='Douban cookie')
    
    args = parser.parse_args()
    scrape(args.year, args.cookie)
