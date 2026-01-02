# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview
This is a Jekyll-based personal portfolio and blog website hosted on GitHub Pages (stuartlau.github.io). The site showcases a professional profile, career history, technical publications, and blog posts primarily focused on backend engineering, distributed systems, and Java technologies.

## Common Commands

### Development
```bash
# Install dependencies
bundle install

# Serve the site locally with auto-regeneration
bundle exec jekyll serve

# Serve with drafts and future posts
bundle exec jekyll serve --drafts --future

# Build the site (output to _site/)
bundle exec jekyll build

# Clean generated files
bundle exec jekyll clean
```

### Testing
```bash
# Verify Jekyll configuration
bundle exec jekyll doctor

# Check for broken links and deprecations
bundle exec jekyll doctor
```

## Architecture

### Site Structure
The site follows Jekyll's convention-based architecture with key directories:
- `_layouts/`: HTML templates that wrap content (page.html, post.html, post-index.html, home.html, default.html)
- `_includes/`: Reusable HTML fragments (head.html, scripts.html, navigation.html, author-bio.html, footer.html)
- `blogs/`: Markdown files for blog posts (200+ technical articles and patent descriptions)
- `_site/`: Generated static site (git-ignored)
- `assets/`: Static resources (CSS in assets/css/, JS in assets/js/, fonts, LESS source)
- `images/`: Image assets including profile pictures and post images

### Layout Hierarchy
- `default.html` - Base layout
- `home.html` - Homepage layout extending default
- `page.html` - Static pages (About, Career, Publications)
- `post.html` - Individual blog post layout with metadata, reading time, and related posts
- `post-index.html` - Blog listing page

### Content Types
1. **Blog Posts** (`blogs/*.md`): Technical articles and patent documentation
   - Front matter: layout, permalink, title, subtitle, date, author, header-img, catalog, tags
   - Organized by date in filenames: `YYYY-MM-DD-title.md`
   - Two main categories: technical articles and authorized patents (授权专利)

2. **Pages**: Top-level navigation pages
   - `index.md` - About/Home page
   - `career.md` - Career timeline
   - `publications.md` - Academic and patent publications
   - `blogs.md` - Blog post index
   - `life.md` - Personal content

### Configuration
- `_config.yml`: Jekyll site configuration with owner info, navigation links, timezone, markdown processor (kramdown), disqus settings
- `Gemfile`: Ruby dependencies (github-pages, webrick)
- Site URL: https://stuartlau.github.io

### Key Features
- **Dark Mode**: Implemented via theme toggle button with localStorage persistence and system preference detection
- **Search**: Fuzzy search using Fuse.js with search.json index
- **Image Zoom**: Medium-zoom integration for article images
- **Photo Grids**: Automatic grid layout for images in `/images/in-post/`
- **Reading Time**: Calculated based on word count (180 words/min)
- **Analytics**: Google Analytics and counter.dev integration
- **Comments**: Disqus integration (shortname: stuartlau)

### Styling
- LESS source files in `assets/less/` compiled to CSS
- CSS variables for theming with light/dark mode support
- Responsive design with mobile-first approach
- Custom fonts: Inter (UI), Source Serif Pro (content)

## Blog Post Creation
When creating new blog posts in the `blogs/` directory:
1. Use filename format: `YYYY-MM-DD-title.md`
2. Include required front matter:
   ```yaml
   ---
   layout: post
   permalink: /blogs/YYYY-MM-DD-title/index.html
   title: "Post Title"
   subtitle: "Optional Subtitle"
   date: YYYY-MM-DD
   author: StuartLau
   header-img: img/home-bg-o.jpg
   catalog: true
   tags:
       - Tag1
       - Tag2
   ---
   ```
3. Content uses kramdown markdown syntax
4. Code blocks support syntax highlighting via Rouge
5. Images should be placed in `images/` directory
6. In-post images in `/images/in-post/` automatically render in photo grids

## Content Updates
- When adding new blog posts, update `blogs.md` with a link to the post
- Patent publications should also be referenced in `publications.md`
- The site uses future: true in config, allowing posts with future dates

## Notes
- The site uses GitHub Pages' github-pages gem which includes Jekyll and dependencies
- No CI/CD pipeline configured - GitHub Pages builds automatically on push to main branch
- Site owner: Stuart Lau (stuart8@126.com)
- The codebase contains Chinese content (blog titles, patent descriptions) - maintain this bilingual approach
