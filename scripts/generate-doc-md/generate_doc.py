import os
from datetime import datetime
import re

ASSETS_DIR = "assets/files"
BLOG_DIR = "blogs/tech" # Assuming these are tech docs, or adjust as needed

def generate_md_for_files():
    if not os.path.exists(ASSETS_DIR):
        print(f"Directory {ASSETS_DIR} does not exist.")
        return

    # Ensure target directory exists
    if not os.path.exists(BLOG_DIR):
        os.makedirs(BLOG_DIR)

    files = [f for f in os.listdir(ASSETS_DIR) if os.path.isfile(os.path.join(ASSETS_DIR, f))]
    
    generated_count = 0
    
    for filename in files:
        if filename.startswith('.'): continue # Skip hidden files
        
        # Determine title from filename (remove extension and replace underscores/hyphens)
        name_without_ext = os.path.splitext(filename)[0]
        title = name_without_ext.replace('_', ' ').replace('-', ' ').title()
        
        # Get file stats for date
        file_path = os.path.join(ASSETS_DIR, filename)
        creation_time = os.path.getctime(file_path)
        date_str = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d')
        year_str = datetime.fromtimestamp(creation_time).strftime('%Y')
        
        target_year_dir = os.path.join(BLOG_DIR, year_str)
        if not os.path.exists(target_year_dir):
            os.makedirs(target_year_dir)

        # Construct filename with correct naming convention
        md_filename = f"{date_str}-{name_without_ext.replace(' ', '-')}.md"
        md_file_path = os.path.join(target_year_dir, md_filename)
        
        # We overwrite existing files if they exist to update the format
        print(f"Generating markdown for {filename}...")
        
        # Determine layout/template based on extension
        ext = os.path.splitext(filename)[1].lower()
        
        # Create unique ID for pdf viewer
        safe_id = re.sub(r'[^a-zA-Z0-9]', '', name_without_ext)
        
        content = f"""---
layout: post
title: "{title}"
date: {date_str}
author: Stuart Lau
header-style: text
tags:
  - Document
  - {ext.replace('.', '').upper()}
---

{{% include pdf-viewer.html url="/assets/files/{filename}" id="{safe_id}" %}}

[Download {filename}](/assets/files/{filename})
"""
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Created/Updated {md_file_path}")
        generated_count += 1
        
    if generated_count == 0:
        print("No new documents to generate.")
    else:
        print(f"Successfully generated {generated_count} new markdown files.")
        
        # Git operations
        try:
            import subprocess
            print("Checking for changes to commit...")
            
            # Add blog directory
            if os.path.exists(BLOG_DIR):
                 subprocess.run(["git", "add", BLOG_DIR], check=True)
            
            # Check status
            status = subprocess.run(["git", "diff", "--staged", "--name-only"], capture_output=True, text=True)
            
            if status.stdout.strip():
                commit_msg = f"chore: auto-generate doc markdown files ({generated_count} files)"
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

if __name__ == "__main__":
    generate_md_for_files()
