import os
import re

DIRECTORY = "/Users/stuart/IdeaProjects/stuartlau.github.io/blogs/patent"

def cleanup_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove everything between multiple #### Downloads if they exist
    # Pattern: remove multiple #### Downloads and keep only the last one or merge
    # Actually, simplest is to find the first #### Downloads and remove everything after it until the signature
    
    first_download_pos = content.find("#### Downloads")
    if first_download_pos == -1:
        return
    
    signature_pos = content.find("> 本文首次发布于")
    
    # Keep content before first download, and content from signature onwards
    pre_content = content[:first_download_pos]
    if signature_pos != -1:
        post_content = content[signature_pos:]
    else:
        post_content = ""
    
    # We will let the main script re-add it correctly
    new_content = pre_content.strip() + "\n\n" + post_content
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Cleaned up {os.path.basename(file_path)}")

if __name__ == "__main__":
    files = [f for f in os.listdir(DIRECTORY) if f.endswith('.md')]
    for f in files:
        cleanup_file(os.path.join(DIRECTORY, f))
