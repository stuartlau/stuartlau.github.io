import os

DATA_DIR = "douban_history"
DOUBAN_DIR = "douban"

def generate_pages():
    if not os.path.exists(DOUBAN_DIR):
        os.makedirs(DOUBAN_DIR)
        
    years = []
    for filename in os.listdir(DATA_DIR):
        if filename.startswith("douban_statuses_") and filename.endswith(".txt"):
            year = filename.replace("douban_statuses_", "").replace(".txt", "")
            years.append(year)
    
    # Also check for 2026 since it might be new
    if os.path.exists("douban_statuses_2025.txt") and "2025" not in years:
        years.append("2025")

    for year in years:
        content = f"---\nlayout: douban\ntitle: {year} Douban Broadcast\nyear: {year}\npermalink: /douban/{year}.html\n---\n"
        with open(os.path.join(DOUBAN_DIR, f"{year}.md"), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated douban/{year}.md")

if __name__ == "__main__":
    generate_pages()
