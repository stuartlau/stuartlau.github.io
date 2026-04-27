import json
import os
import random
import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# Configuration
USER_ID = "shuoleo"
BASE_URL = f"https://www.douban.com/people/{USER_ID}/statuses"
DATA_DIR = "_data/douban"
IMAGE_DIR = "images/douban"
COOKIE_PATH = os.path.expanduser("~/.douban.cookie")


def get_cookie():
    if os.path.exists(COOKIE_PATH):
        with open(COOKIE_PATH, "r") as f:
            return f.read().strip()
    return ""


def download_image(url):
    if not url or url.startswith("/"):
        return url

    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    filename = url.split("/")[-1].split("?")[0]
    local_path = os.path.join(IMAGE_DIR, filename)
    local_url = f"/{IMAGE_DIR}/{filename}"

    if os.path.exists(local_path):
        return local_url

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.douban.com/",
        }
        # Try to get large version
        url = url.replace("/m/", "/l/").replace("/Xs/", "/l/").replace("/thumb/", "/l/")

        r = requests.get(url, headers=headers, stream=True, timeout=10)
        if r.status_code == 200:
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            print(f"  ✓ Downloaded: {filename}")
            return local_url
    except Exception as e:
        print(f"  ✗ Failed image {url}: {e}")
    return url


def extract_images(item):
    images = []

    # 1. Standard patterns
    selectors = [
        ".upload-pic img",
        ".status-saying .grid-view img",
        ".status-saying img",
        ".topic-img img",
    ]
    for selector in selectors:
        for img in item.select(selector):
            src = img.get("src") or img.get("data-src")
            if src:
                images.append(src)

    # 2. Regex-based fallback for the entire item HTML (very robust)
    # Douban sometimes puts URLs in data-attributes or hidden divs
    item_html = str(item)
    found_urls = re.findall(
        r'https?://img\d+\.doubanio\.com/view/status/[^"\'>\s]+', item_html
    )
    images.extend(found_urls)

    # 3. JS Script tags
    for script in item.select("script"):
        if "var photos =" in script.text:
            match = re.search(r"var photos = (\[.*?\])", script.text, re.DOTALL)
            if match:
                try:
                    photo_data = json.loads(match.group(1))
                    for p in photo_data:
                        u = p.get("image", {}).get("large", {}).get("url")
                        if u:
                            images.append(u)
                except:
                    pass

    # Clean URLs: convert to large format and remove duplicates
    cleaned_images = []
    seen = set()
    for url in images:
        # Standardize to large
        url = (
            url.replace("/m/", "/l/")
            .replace("/Xs/", "/l/")
            .replace("/thumb/", "/l/")
            .replace("/raw/", "/l/")
        )
        if url not in seen and "icon/u" not in url and "douban_avatar" not in url:
            cleaned_images.append(url)
            seen.add(url)

    # Download
    local_images = []
    for img_url in cleaned_images:
        local_url = download_image(img_url)
        if local_url:
            local_images.append(local_url)

    return local_images


def repair_year(year):
    print(f"=== Deep Repairing Images for {year} ===")
    json_path = os.path.join(DATA_DIR, f"{year}.json")
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Statistics before
    missing_before = sum(1 for i in data if not i.get("images"))
    print(f"Stats: {len(data)} total, {missing_before} missing images.")

    cookie = get_cookie()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cookie": cookie,
    }

    # Optimization: Start from a likely page if it's an old year
    # 2023 is quite old, so we might need to skip many pages
    # Let's start from page 50 if 2023
    start_page = 50 if year == "2023" else 0
    if year == "2022":
        start_page = 150
    if year == "2021":
        start_page = 250

    page = start_page
    max_pages = start_page + 200
    repaired_count = 0

    while page < max_pages:
        url = f"{BASE_URL}?p={page}"
        print(f"Scanning Douban Page {page}...", end="\r")

        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code != 200:
                print(f"\nStop: HTTP {res.status_code}")
                break

            soup = BeautifulSoup(res.text, "html.parser")
            items = soup.select(".status-item")
            if not items:
                print(f"\nNo items on page {page}. End of feed?")
                break

            for item in items:
                time_el = item.select_one(".created_at")
                if not time_el:
                    continue
                full_time_str = time_el.get("title", "")
                if not full_time_str:
                    continue

                dt = datetime.strptime(full_time_str, "%Y-%m-%d %H:%M:%S")
                item_year_str = str(dt.year)

                if item_year_str == str(year):
                    timestamp = dt.strftime("%Y-%m-%d %H:%M")
                    # Find matching record
                    for record in data:
                        if record["time"] == timestamp:
                            if not record.get("images"):
                                new_images = extract_images(item)
                                if new_images:
                                    record["images"] = new_images
                                    repaired_count += 1
                                    print(
                                        f"\n[+] Fixed {timestamp}: {len(new_images)} images"
                                    )
                            break
                elif dt.year < int(year):
                    print(f"\nReached earlier year {dt.year}. Finishing.")
                    page = max_pages  # break outer loop
                    break

            if page % 10 == 0:
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

            page += 1
            # Adjust sleep to be faster for repair but still safe
            time.sleep(random.uniform(0.5, 1.5))

        except Exception as e:
            print(f"\nError on page {page}: {e}")
            break

    # Final save
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nDeep Repair complete! Fixed {repaired_count} records.")


if __name__ == "__main__":
    import sys

    year = sys.argv[1] if len(sys.argv) > 1 else "2023"
    repair_year(year)
