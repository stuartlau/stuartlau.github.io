import os
import re

DIRECTORY = "/Users/stuart/IdeaProjects/stuartlau.github.io/blogs/patent"

def fix_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    i = 0
    modified = False
    
    while i < len(lines):
        line = lines[i]
        
        # Detect the Downloads section
        if line.strip() == "#### Downloads":
            new_lines.append(line)
            i += 1
            
            links_block = []
            while i < len(lines) and (lines[i].startswith("> ") or lines[i].strip() == ""):
                if lines[i].strip() != "":
                    links_block.append(lines[i])
                i += 1
            
            # Now we have a list of link lines like:
            # > 下载中文版本 (Download PDF): [URL](URL)
            # > Download English Version (PDF): [URL](URL)
            
            urls = []
            final_links = []
            for link_line in links_block:
                # Extract URL
                match = re.search(r'\[(https?://[^\]]+)\]', link_line)
                if match:
                    url = match.group(1)
                    if url not in urls:
                        urls.append(url)
                        final_links.append(link_line)
                    else:
                        # Duplicate URL detected!
                        print(f"  Duplicate URL found in {os.path.basename(file_path)}: {url}")
                        modified = True
                else:
                    final_links.append(link_line)
            
            for fl in final_links:
                new_lines.append(fl)
            
            # Continue from where the block ended
            continue
        
        new_lines.append(line)
        i += 1
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        print(f"Fixed {os.path.basename(file_path)}")
    return modified

def main():
    files = [f for f in os.listdir(DIRECTORY) if f.endswith('.md')]
    count = 0
    for f in files:
        if fix_links(os.path.join(DIRECTORY, f)):
            count += 1
    print(f"Successfully fixed {count} files.")

if __name__ == "__main__":
    main()
