#!/usr/bin/env python3
"""
Douban data sync script
Fetches broadcast data from Douban and saves to _data/douban/{year}.json

Usage:
    python sync_douban.py --year 2026
    python sync_douban.py --year all
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Data directory
DATA_DIR = Path("_data/douban")
OUTPUT_DIR = Path("_data")


def load_existing_data(year: str) -> dict:
    """Load existing data for a year"""
    file_path = DATA_DIR / f"{year}.json"
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_data(data: list, year: str):
    """Save data to JSON file"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DATA_DIR / f"{year}.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved {len(data)} records to {file_path}")


def merge_data(existing: list, new: list) -> list:
    """Merge existing and new data, avoiding duplicates"""
    existing_ids = set(item.get('time', '') for item in existing)
    merged = existing.copy()
    
    for item in new:
        if item.get('time', '') not in existing_ids:
            merged.append(item)
            existing_ids.add(item.get('time', ''))
    
    # Sort by time descending (newest first)
    merged.sort(key=lambda x: x.get('time', ''), reverse=True)
    return merged


def sync_year(year: str, cookie: str = None):
    """Sync data for a specific year"""
    print(f"\n📥 Syncing data for year {year}...")
    
    # Load existing data
    existing = load_existing_data(year)
    print(f"   Existing records: {len(existing)}")
    
    # Fetch new data
    # Note: This is a placeholder - actual implementation depends on data source
    # Options:
    # 1. Parse from Douban HTML pages (requires login)
    # 2. Import from a Google Sheet
    # 3. Use a shared Dropbox/Notion file
    
    new_data = fetch_douban_data(year, cookie)
    
    if not new_data:
        print(f"   ⚠️  No new data fetched (or data source not configured)")
        return
    
    # Merge data
    merged = merge_data(existing, new_data)
    print(f"   After merge: {len(merged)} records")
    
    # Save
    save_data(merged, year)
    
    # Update summary
    update_summary()


def fetch_douban_data(year: str, cookie: str = None) -> list:
    """
    Fetch Douban broadcast data
    
    This is a placeholder implementation. In practice, you might:
    1. Use Douban API (requires authentication)
    2. Scrape HTML pages (requires login cookie)
    3. Import from external source (Google Sheet, Notion, etc.)
    """
    
    # Placeholder: return empty list
    # In production, implement one of these methods:
    
    # Option 1: Scrape Douban mobile web
    # Requires DOUBAN_COOKIE environment variable
    # 
    # import requests
    # from bs4 import BeautifulSoup
    #
    # if cookie:
    #     headers = {'Cookie': cookie}
    #     url = f"https://m.douban.com/people/XXXXX/statuses?year={year}"
    #     response = requests.get(url, headers=headers)
    #     # Parse HTML and extract data...
    
    # Option 2: Import from Google Sheet
    # Requires google sheets API setup
    #
    # import gspread
    # from oauth2client.service_account import ServiceAccountCredentials
    #
    # scope = ['https://spreadsheets.google.com/feeds']
    # creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    # client = gspread.authorize(creds)
    # sheet = client.open("Douban Data").sheet1
    # records = sheet.get_all_records()
    
    print(f"   ℹ️  Fetch functionality not yet implemented")
    print(f"   To implement, configure one of:")
    print(f"   - Douban cookie for web scraping")
    print(f"   - Google Sheet for data import")
    print(f"   - Notion API for database sync")
    
    return []


def update_summary():
    """Update the douban_summaries.json file"""
    summary_file = OUTPUT_DIR / "douban_summaries.json"
    
    # Load existing or create new
    if summary_file.exists():
        with open(summary_file, 'r', encoding='utf-8') as f:
            summary = json.load(f)
    else:
        summary = {}
    
    # Calculate stats for each year
    for year_file in DATA_DIR.glob("*.json"):
        year = year_file.stem
        if year.isdigit() and len(year) == 4:
            with open(year_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Calculate stats
            with_images = sum(1 for item in data if item.get('images'))
            with_videos = sum(1 for item in data if item.get('video_url'))
            
            ratings = [item.get('my_rating', 0) for item in data if item.get('my_rating')]
            avg_rating = sum(ratings) / len(ratings) if ratings else 0
            
            summary[year] = {
                "count": len(data),
                "with_images": with_images,
                "with_videos": with_videos,
                "avg_rating": round(avg_rating, 1) if avg_rating else 0,
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }
    
    # Save
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Updated summary at {summary_file}")


def main():
    parser = argparse.ArgumentParser(description='Sync Douban broadcast data')
    parser.add_argument('--year', type=str, default='all',
                        help='Year to sync (e.g., 2026), or "all"')
    parser.add_argument('--cookie', type=str, default=None,
                        help='Douban cookie for authentication')
    
    args = parser.parse_args()
    
    # Get cookie from args or environment
    cookie = args.cookie or os.environ.get('DOUBAN_COOKIE')
    
    if args.year == 'all':
        # Sync all years
        for year in ['2021', '2022', '2023', '2024', '2025', '2026']:
            sync_year(year, cookie)
    else:
        sync_year(args.year, cookie)
    
    print("\n✨ Sync complete!")


if __name__ == '__main__':
    main()
