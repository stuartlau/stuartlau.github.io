---
description: Auto-generate blog posts for documents
---

# Generate Doc MD

This workflow scans the `assets/file` directory for files (like PDFs) and automatically generates a corresponding Markdown blog post if one does not already exist.

### Usage

Run the generation script:

```bash
python3 scripts/generate-doc-md/generate_doc.py
```

The script will:
1. Check `assets/files` for files.
2. Check if a corresponding markdown file exists in `blogs/tech/YYYY/`.
3. If not, generate a new post embedding the file via iframe.