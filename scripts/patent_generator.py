import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

DIRECTORY = "blogs/patent"
# Default tags
DEFAULT_TAGS = ["Patent", "快手"]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_patent_data(patent_id):
    url = f"https://patents.google.com/patent/{patent_id}/"
    en_url = f"https://patents.google.com/patent/{patent_id}/en"
    
    data = {
        "id": patent_id,
        "url": url,
        "en_url": en_url,
        "pdf_url": "",
        "title": "",
        "subtitle": "",
        "abstract": "",
        "date": "",
        "events": [],
        "type": "授权专利" if patent_id.endswith('B') else "待授权专利"
    }
    
    try:
        print(f"Fetching {url}...")
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print(f"Failed to fetch {url}: {resp.status_code}")
            return None
        
        # Set encoding properly
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # 1. Title
        title_tag = soup.find('meta', {'name': 'DC.title'})
        if title_tag:
            data["title"] = title_tag.get('content').strip()
        
        if not data["title"]:
            h1_title = soup.find('h1', itemprop='title')
            if h1_title:
                data["title"] = h1_title.text.strip()
        
        # 2. Abstract
        abstract_section = soup.find('section', itemprop='abstract')
        if abstract_section:
            data["abstract"] = " ".join(abstract_section.text.strip().split())
        else:
            abstract_div = soup.find('div', class_='abstract style-scope patent-result')
            if abstract_div:
                data["abstract"] = " ".join(abstract_div.text.strip().split())

        # 3. PDF Link
        pdf_meta = soup.find('meta', {'name': 'citation_pdf_url'})
        if pdf_meta:
            data["pdf_url"] = pdf_meta.get('content')

        # 4. Events
        # Strategy: find all elements with itemprop="date" and find their corresponding descriptions
        timeline_items = soup.find_all(itemprop='timeline')
        for item in timeline_items:
            d_tag = item.find(itemprop='date')
            desc_tag = item.find(itemprop='description')
            if d_tag and desc_tag:
                data["events"].append((d_tag.text.strip(), desc_tag.text.strip()))
        
        # If still empty, try table rows in sections that might contain events
        if not data["events"]:
            for section in soup.find_all(['section', 'div'], class_=lambda x: x and 'patent-result' in x):
                h2 = section.find('h2')
                if h2 and 'event' in h2.text.lower():
                    data["event_app_id"] = h2.text.strip()
                    rows = section.find_all('tr')
                    for row in rows:
                        tds = row.find_all('td')
                        if len(tds) >= 2:
                            d = tds[0].text.strip()
                            desc = tds[1].text.strip()
                            if d and desc:
                                data["events"].append((d, desc))
            
        # 5. Determine Date
        meta_date = soup.find('meta', {'name': 'DC.date'})
        meta_date_val = meta_date.get('content').strip() if meta_date else ""
        
        grant_date = ""
        pub_date = ""
        
        # Try to find dates in events
        for d, desc in data["events"]:
            if "granted" in desc.lower():
                grant_date = d
            if f"Publication of {patent_id}" in desc or (f"Publication of" in desc and patent_id[2:11] in desc):
                pub_date = d
            elif not pub_date and "Publication" in desc:
                pub_date = d
            
        if patent_id.endswith('B'):
            data["date"] = grant_date if grant_date else (pub_date if pub_date else meta_date_val)
        else:
            # For A version, filing date is often DC.date, but we want publication
            # If we didn't find "Publication" in events, check meta tags carefully
            if pub_date:
                data["date"] = pub_date
            else:
                # If meta_date exists and we are an 'A' patent, 
                # check if it's the publication date or filing date
                # Usually we'll just use meta_date as fallback
                data["date"] = meta_date_val

        if not data["date"] and data["events"]:
            # Last resort
            data["date"] = data["events"][-1][0]
        
        # Sanitize date (yyyy-mm-dd)
        if data["date"]:
            match = re.search(r'\d{4}-\d{2}-\d{2}', data["date"])
            if match:
                data["date"] = match.group(0)

    except Exception as e:
        print(f"Error processing {patent_id}: {e}")
        return None
        
    return data

def generate_md(data):
    if not data or not data["date"]:
        print(f"Incomplete data for {data['id'] if data else 'unknown'}")
        return
    
    filename = f"{data['date']}-{data['type']}-{data['id']}.md".replace("/", "-")
    filepath = os.path.join(DIRECTORY, filename)
    
    # Check for existing
    existing_files = os.listdir(DIRECTORY)
    for ef in existing_files:
        # Check if this exact patent ID is in the filename
        if f"-{data['id']}.md" in ef:
            if ef == filename:
                print(f"File {ef} already exists, skipping.")
                return
            # If A version exists but we are processing B, delete A
            if ef.endswith('A.md') and filename.endswith('B.md'):
                print(f"Found older version {ef}, deleting...")
                os.remove(os.path.join(DIRECTORY, ef))
            elif ef.endswith('B.md') and filename.endswith('A.md'):
                print(f"Found grant version {ef}, skipping application version {filename}.")
                return

    # Extract tags from title
    tags = list(DEFAULT_TAGS)
    # Simple keyword extraction (can be improved)
    keywords = ["IM", "游戏", "资源", "安全", "网络", "推送", "存储", "视频", "直播", "分发", "CDN", "域名", "解析", "消息", "服务器", "计算"]
    for kw in keywords:
        if kw in data["title"]:
            tags.append(kw)
    
    # Dedup tags
    tags = sorted(list(set(tags)))
    
    prefix = "Granted Patent" if data["id"].endswith('B') else "Patent Application"
    
    content = f"""---
layout:     post
permalink:  /blogs/{data['date']}-{data['type']}-{data['id']}/index.html
title:      "{data['type']}-{data['id']}-{data['title']}"
subtitle:   "{prefix}-{data['id']}-{data['title']}"
date:       {data['date']}
author:     StuartLau
header-style: text
catalog: true
tags:
"""
    for tag in tags:
        content += f"    - {tag}\n"
    content += "---\n"
    
    content += f"> 中文 [{data['url']}]({data['url']})\n"
    content += f">\n"
    content += f"> English [{data['en_url']}]({data['en_url']})\n\n"
    
    # Image placeholder/ref
    content += f"![patent](/images/in-post/patent/{data['id']}.jpg)\n"
    
    content += f"#### Title\n> {data['title']}\n\n"
    content += f"#### Abstract\n> {data['abstract']}\n\n"
    
    content += f"#### Application Event\n```\n"
    if "event_app_id" in data:
        content += f"{data['event_app_id']}\n"
    for d, desc in data["events"]:
        content += f"{d} {desc}\n"
    content += f"Status Active\n" # Default active for newly added
    content += "```\n\n"
    
    if data["pdf_url"]:
        label = "下载中文版本 (Download PDF)" if "CN" in data["id"] else "Download PDF"
        content += f"#### Downloads\n"
        content += f"> {label}: [{data['pdf_url']}]({data['pdf_url']})\n\n"
        
    content += f"> 本文首次发布于 [StuartLau's Blog](https://stuartlau.github.io), \n"
    content += f"转载请保留原文链接.\n"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created {filename}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 patent_generator.py ID1 ID2 ...")
        return
    
    patent_ids = sys.argv[1:]
    for pid in patent_ids:
        data = get_patent_data(pid)
        if data:
            generate_md(data)
        time.sleep(2) # Throttle

if __name__ == "__main__":
    main()
