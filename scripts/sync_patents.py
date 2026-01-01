import os
import csv
import re
import subprocess
import sys
import requests
import time

CSV_FILE = "patents.csv"
PATENT_DIR = "blogs/patent"
GENERATOR_SCRIPT = "scripts/patent_generator.py"
DOWNLOAD_URL = "https://patents.google.com/xhr/query?url=inventor%3D%E5%88%98%E7%A1%95%26assignee%3D%E5%8C%97%E4%BA%AC%E8%BE%BE%E4%BD%B3%E4%BA%92%E8%81%94%E4%BF%A1%E6%81%AF%E6%8A%80%E6%9C%AF%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%26num%3D100&exp=&download=true"

def download_csv():
    print(f"Downloading latest patents CSV from Google Patents...")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        resp = requests.get(DOWNLOAD_URL, headers=headers, timeout=30)
        resp.raise_for_status()
        with open(CSV_FILE, 'wb') as f:
            f.write(resp.content)
        print(f"Successfully downloaded {CSV_FILE}")
        return True
    except Exception as e:
        print(f"Error downloading CSV: {e}")
        return False

def get_existing_patents():
    existing = {}
    if not os.path.exists(PATENT_DIR):
        os.makedirs(PATENT_DIR)
    for filename in os.listdir(PATENT_DIR):
        if filename.endswith(".md"):
            # Extract ID like CN123456789A or CN123456789B
            match = re.search(r'-(CN[0-9]{9}[AB])\.md$', filename)
            if match:
                patent_id = match.group(1)
                existing[patent_id] = filename
    return existing

def sync_from_csv():
    if not os.path.exists(CSV_FILE):
        if not download_csv():
            return

    existing = get_existing_patents()
    ids_to_process = []

    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        # Skip the search URL line if it exists
        line = f.readline()
        if "search URL" not in line:
            f.seek(0)
            
        reader = csv.DictReader(f)
        for row in reader:
            raw_id = row.get('id', '')
            if not raw_id: continue
            
            # Convert CN-111399709-B to CN111399709B
            patent_id = raw_id.replace('-', '')
            
            if patent_id.startswith('CN'):
                is_granted = patent_id.endswith('B')
                base_id = patent_id[:-1]
                
                a_version = base_id + 'A'
                b_version = base_id + 'B'
                
                if is_granted:
                    if b_version not in existing:
                        ids_to_process.append(b_version)
                else:
                    if a_version not in existing and b_version not in existing:
                        ids_to_process.append(a_version)

    if not ids_to_process:
        print("No new patents to process.")
        return

    print(f"Found {len(ids_to_process)} new/updated patents to sync.")
    # Process in batches
    batch_size = 5
    for i in range(0, len(ids_to_process), batch_size):
        batch = ids_to_process[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}: {batch}")
        subprocess.run(["python3", GENERATOR_SCRIPT] + batch)
        time.sleep(1)

def main():
    if len(sys.argv) > 1:
        # Individual ID processing
        patent_ids = sys.argv[1:]
        print(f"Processing specific IDs: {patent_ids}")
        subprocess.run(["python3", GENERATOR_SCRIPT] + patent_ids)
    else:
        # Automated Smart Sync
        if download_csv():
            sync_from_csv()

if __name__ == "__main__":
    main()
