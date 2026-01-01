import os
import re
import requests
from bs4 import BeautifulSoup
import time
from pathlib import Path

DIRECTORY = "/Users/stuart/IdeaProjects/stuartlau.github.io/blogs/patent"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_patent_id(filename):
    # Pattern: 2018-01-09-授权专利-CN103746817B.md
    match = re.search(r'授权专利-(.+)\.md', filename)
    if match:
        return match.group(1)
    return None

def fetch_pdf_link(patent_id, suffix=""):
    url = f"https://patents.google.com/patent/{patent_id}/{suffix}"
    try:
        print(f"  Checking {url}...")
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            meta = soup.find('meta', {'name': 'citation_pdf_url'})
            if meta:
                return meta.get('content')
    except Exception as e:
        print(f"    Error: {e}")
    return None

def process_file(file_path):
    filename = os.path.basename(file_path)
    patent_id = get_patent_id(filename)
    if not patent_id:
        print(f"Could not extract patent ID from {filename}")
        return

    print(f"Processing {patent_id}...")
    
    links = []
    
    # Check default (usually native language)
    pdf_default = fetch_pdf_link(patent_id)
    if pdf_default:
        label = "Download PDF"
        if patent_id.startswith('CN'): label = "下载中文版本 (Download PDF)"
        elif patent_id.startswith('US'): label = "Download English Version (PDF)"
        elif patent_id.startswith('JP'): label = "ダウンロード PDF (Japanese Version)"
        elif patent_id.startswith('RU'): label = "Скачать PDF (Russian Version)"
        
        links.append((label, pdf_default))
        time.sleep(1) # Be nice

    # Check English translation if not already English
    if not patent_id.startswith('US') and not patent_id.startswith('EP'):
        pdf_en = fetch_pdf_link(patent_id, "en")
        if pdf_en and pdf_en != pdf_default:
            links.append(("Download English Version (PDF)", pdf_en))
            time.sleep(1)
        elif pdf_en and pdf_en == pdf_default:
            # Even if URL is same, having the label as requested by user
            if not any("English" in l[0] for l in links):
                links.append(("Download English Version (PDF)", pdf_en))

    # Check Chinese translation if not already Chinese
    if not patent_id.startswith('CN'):
        pdf_zh = fetch_pdf_link(patent_id, "zh")
        if pdf_zh and pdf_zh != pdf_default and pdf_zh not in [l[1] for l in links]:
            links.append(("下载中文版本 (Download PDF)", pdf_zh))
            time.sleep(1)

    if not links:
        print(f"  No links found for {patent_id}")
        return

    # Update the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if we already added PDF links
    if "#### Downloads" in content:
        print(f"  Links already exist in {filename}, skipping.")
        return

    # Append to the end, but before the "本文首次发布于" line if possible, 
    # or just at the very end.
    
    footer = "\n\n#### Downloads\n"
    for label, link in links:
        footer += f"> {label}: [{link}]({link})\n"
    
    # Find insertion point: usually before the signature or at the end
    signature_pos = content.find("> 本文首次发布于")
    if signature_pos != -1:
        new_content = content[:signature_pos] + footer + "\n" + content[signature_pos:]
    else:
        new_content = content + footer

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  Successfully updated {filename}")

def main():
    files = sorted([f for f in os.listdir(DIRECTORY) if f.endswith('.md')])
    print(f"Found {len(files)} files.")
    for f in files:
        process_file(os.path.join(DIRECTORY, f))
        time.sleep(1) # General delay between files

if __name__ == "__main__":
    main()
