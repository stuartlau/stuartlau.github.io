#!/usr/bin/env python3
import json
import os
import math

def generate_api_json(base_name, data, per_page):
    """Generate paginated JSON files for API"""
    if not data or not isinstance(data, list) or len(data) == 0:
        return
    
    api_dir = os.path.join('_site', 'api', base_name)
    os.makedirs(api_dir, exist_ok=True)
    
    total_pages = math.ceil(len(data) / per_page)
    print(f"  Creating {total_pages} pages for {base_name} ({len(data)} items)")
    
    for page in range(1, total_pages + 1):
        start_index = (page - 1) * per_page
        end_index = min(start_index + per_page, len(data))
        page_items = data[start_index:end_index]
        
        json_data = {
            'page': page,
            'total_pages': total_pages,
            'total_count': len(data),
            'data': page_items
        }
        
        file_path = os.path.join(api_dir, f'page-{page}.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Created {file_path}")

print("=== Generating API JSON files ===")

# Generate Movies API
movies_file = '_data/movies/all.json'
if os.path.exists(movies_file):
    with open(movies_file, 'r', encoding='utf-8') as f:
        movies_data = json.load(f)
    generate_api_json('movies', movies_data, 24)

# Generate Books API
books_file = '_data/books/all.json'
if os.path.exists(books_file):
    with open(books_file, 'r', encoding='utf-8') as f:
        books_data = json.load(f)
    generate_api_json('books', books_data, 24)

# Generate Games API
games_file = '_data/games/all.json'
if os.path.exists(games_file):
    with open(games_file, 'r', encoding='utf-8') as f:
        games_data = json.load(f)
    generate_api_json('games', games_data, 24)

# Generate Douban API for each year
douban_dir = '_data/douban'
if os.path.exists(douban_dir):
    for filename in os.listdir(douban_dir):
        if filename.endswith('.json'):
            year = filename.replace('.json', '')
            file_path = os.path.join(douban_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                douban_data = json.load(f)
            generate_api_json(f'douban/{year}', douban_data, 30)

# Generate Blogs API (need to parse from Jekyll, skip for now)
print("  Note: Blogs API requires Jekyll processing, run after Jekyll build")

print("=== API JSON generation complete ===")
