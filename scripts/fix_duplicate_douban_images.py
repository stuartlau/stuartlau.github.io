import glob
import json
import os


def fix_duplicates():
    # 1. Deduplicate the JSON arrays
    changed_files = 0
    for filepath in glob.glob("_data/douban/*.json"):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        modified = False
        for item in data:
            images = item.get("images", [])
            if not images:
                continue

            # Deduplicate preserving order
            unique_images = list(dict.fromkeys(images))
            if len(unique_images) != len(images):
                item["images"] = unique_images
                modified = True

        if modified:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Fixed duplicate array entries in {filepath}")
            changed_files += 1

    print(f"Total JSON files fixed: {changed_files}")

    # 2. Find and delete completely unreferenced/orphaned physical images
    referenced = set()
    for filepath in glob.glob("_data/douban/*.json"):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            for img in item.get("images", []):
                referenced.add(os.path.basename(img))

    img_dir = "images/douban"
    deleted = 0
    for f in os.listdir(img_dir):
        p = os.path.join(img_dir, f)
        if (
            os.path.isfile(p)
            and f.endswith(".jpg")
            and f not in referenced
            and f != "douban_avatar.jpg"
        ):
            os.remove(p)
            print(f"Deleted unreferenced image: {f}")
            deleted += 1

    print(f"Total unreferenced physical images deleted: {deleted}")


if __name__ == "__main__":
    fix_duplicates()
