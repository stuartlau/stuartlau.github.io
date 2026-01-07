import os
import re

DIRECTORY = "/Users/stuart/IdeaProjects/stuartlau.github.io/blogs/patent"

def fix_patent_formatting(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Split content around "#### Downloads" and the signature
    # Pattern to find the signature block
    sig_line = "> 本文首次发布于"
    sig_pos = content.find(sig_line)
    
    # Pattern to find Downloads block
    downloads_header = "#### Downloads"
    downloads_pos = content.find(downloads_header)
    
    if downloads_pos == -1:
        return False
        
    main_content = content[:downloads_pos].strip()
    
    # Extract links from the Downloads section
    downloads_section = content[downloads_pos:sig_pos] if sig_pos != -1 else content[downloads_pos:]
    
    # Find all download links in this section
    # Using regex to find lines starting with > and containing a URL
    link_lines = re.findall(r'^> .+: \[https?://[^\]]+\]\(https?://[^)]+\)$', downloads_section, re.MULTILINE)
    
    # Deduplicate by URL
    seen_urls = set()
    unique_links = []
    for line in link_lines:
        match = re.search(r'\[(https?://[^\]]+)\]', line)
        if match:
            url = match.group(1)
            if url not in seen_urls:
                seen_urls.add(url)
                unique_links.append(line)
    
    # 2. Reconstruct the file with proper spacing
    new_content = main_content + "\n\n" + downloads_header + "\n"
    for link in unique_links:
        new_content += link + "\n"
    
    new_content += "\n" # The requested extra space
    
    if sig_pos != -1:
        new_content += content[sig_pos:]
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    files = [f for f in os.listdir(DIRECTORY) if f.endswith('.md')]
    count = 0
    for f in files:
        if fix_patent_formatting(os.path.join(DIRECTORY, f)):
            count += 1
    print(f"Successfully reformatted {count} files.")

if __name__ == "__main__":
    main()
