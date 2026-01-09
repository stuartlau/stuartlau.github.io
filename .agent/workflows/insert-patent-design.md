---
description: Automatically insert patent design images into corresponding markdown files
---

This workflow executes a Python script that scans for PNG images in `images/in-post/patent/design`, extracts the patent ID, and inserts the image at the top of the matching markdown file in `blogs/patent`.

1. Run the insertion script
// turbo
python3 /Users/stuart/IdeaProjects/stuartlau.github.io/scripts/insert_patent_design_images.py
