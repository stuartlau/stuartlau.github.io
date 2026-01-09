import os
import re

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, 'images/in-post/patent/design')
BLOG_DIR = os.path.join(BASE_DIR, 'blogs/patent')

def find_md_file(patent_id):
    """
    Recursively search for a markdown file that contains the patent_id in its filename
    within the BLOG_DIR.
    """
    for root, dirs, files in os.walk(BLOG_DIR):
        for file in files:
            if file.endswith('.md') and patent_id in file:
                return os.path.join(root, file)
    return None

def insert_image_to_md(md_path, image_filename):
    """
    Inserts the image link into the markdown file after the front matter if it's not already present.
    """
    image_rel_path = f"/images/in-post/patent/design/{image_filename}"
    image_markdown = f"\n![Design Display]({image_rel_path})"
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if image is already linked
    if image_filename in content:
        print(f"Image {image_filename} already active in {os.path.basename(md_path)}")
        return

    # Split front matter
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"Warning: Could not parse front matter in {md_path}")
        return

    # Insert after front matter (parts[2] is the body)
    # parts[0] is empty (before first ---)
    # parts[1] is front matter
    # parts[2] is body
    
    new_content = '---' + parts[1] + '---' + image_markdown + parts[2]
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Inserted {image_filename} into {os.path.basename(md_path)}")

def process_images():
    if not os.path.exists(IMAGE_DIR):
        print(f"Image directory not found: {IMAGE_DIR}")
        return

    for image_file in os.listdir(IMAGE_DIR):
        if not image_file.lower().endswith('.png'):
            continue
            
        # Extract ID. Assuming format like "CN103746817B-Info.png" or "CN103746817B.png"
        # We take the part before the first hyphen or dot regex match of typical ID pattern
        # Simple heuristic: Split by '-' or '.' and take first part?
        # Alternatively, take the longest alphanumeric prefix?
        # ID is usually like CN12345678A/B
        
        # Strategy: matching the filename against known MD files is safer if we extract the whole prefix 
        # but let's try splitting by '-' first as seen in "CN103746817B-Info.png"
        
        name_part = image_file.split('-')[0].split('.')[0]
        
        # If the filename starts with the ID, searching for that ID in MD filenames should work.
        patent_id = name_part
        
        print(f"Processing image: {image_file}, extracted ID: {patent_id}")
        
        md_file = find_md_file(patent_id)
        
        if md_file:
            insert_image_to_md(md_file, image_file)
        else:
            print(f"No matching markdown file found for ID: {patent_id}")

if __name__ == "__main__":
    process_images()
