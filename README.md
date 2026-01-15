# Stuart Lau's Personal Website

> A digital garden documenting my journey as a full-stack engineer, patent inventor, and lifelong learner.

## Design Philosophy

This website is more than just a portfolio—it's a reflection of how I think about information, learning, and personal growth. Here are the key principles that guided its design:

### 1. Content-First Architecture

The web has become cluttered with distractions. This site prioritizes **readability** and **accessibility** above all else. Every design decision, from typography to color schemes, exists to serve the content—not the other way around.

- **Minimalist aesthetic**: Clean white/light backgrounds reduce eye strain and keep focus on the words
- **Thoughtful typography**: Careful attention to line height, character spacing, and font selection
- **Responsive by default**: The site adapts gracefully to any screen size, because content should be accessible everywhere

### 2. Multi-Dimensional Self-Presentation

I believe a person's identity cannot be captured in a single dimension. That's why this site presents who I am through multiple lenses:

- **Professional**: Work experience, patents, technical blog posts
- **Intellectual**: Books I've read, courses I've taken, ideas I've explored
- **Personal**: Travel journals, life reflections, the things that bring me joy

This multi-faceted approach allows visitors to understand the *why* behind my work, not just the *what*.

### 3. Learning in Public

I firmly believe in **learning in public**. Every blog post, every patent, every book notes is an opportunity to:
- Share knowledge with others who might be on a similar journey
- Document my own learning for future reference
- Invite feedback and collaboration

The technical blog section isn't just about showcasing expertise—it's about contributing to the collective knowledge of our industry.

### 4. Curated Collections

Rather than exhaustively listing every piece of media I've consumed, I've **curated** meaningful selections:

- **Movies**: Films that shaped my perspective or simply entertained me
- **Books**: Reads that fundamentally changed how I think
- **Games**: Experiences that taught me something about design or storytelling

These collections are intentionally **not** comprehensive—they're curated reflections of taste and judgment.

### 5. Spatial Navigation

The homepage uses a **terminal-inspired interface** for exploring different aspects of my professional life. This design choice reflects my background in systems engineering and distributed systems:

- The command-line metaphor suggests exploration and discovery
- Tab-based navigation allows quick access without page reloads
- Color-coded sections provide visual cues for different content types

### 6. Personal Database

The site doubles as a **personal knowledge management system**. My douban integrations (movies, books, games) automatically sync with my accounts, creating a living record of my media consumption and cultural engagement over time.

## Technology Stack

- **Jekyll**: Static site generator for simplicity and performance
- **GitHub Pages**: Hosting that aligns with my love for version control
- **Custom CSS**: No heavy frameworks—just purpose-built styling
- **Minimal JavaScript**: Progressive enhancement where needed

## Project Structure

```
stuartlau.github.io/
├── _layouts/           # Page templates
├── _includes/          # Reusable components
├── _data/              # Data files (books, movies, games)
├── blogs/              # Blog posts by category
│   ├── patent/         # Patent documentation
│   ├── tech/           # Technical articles
│   └── travelling/     # Travel journals
├── assets/             # CSS, JS, images
├── images/             # Static images
├── _config.yml         # Jekyll configuration
└── README.md           # This file
```

## Features

### Automatic Sync
The site integrates with Douban APIs to automatically sync:
- Movie watchlist and ratings
- Book reading history  
- Game play records

This automation ensures the site stays current without manual maintenance.

### Patent Portfolio
My 120+ patents are documented with full details, organized by:
- Technology domain (IM, distributed systems, video streaming)
- Geographic coverage (China, US, EU, Japan)
- Status (granted vs. pending)

### Travel Map
An interactive visualization of countries and cities I've visited, with detailed journal entries for each destination.

## Customization & Forking

This site is designed to be **forked and adapted**. Here's how you can make it your own:

### 1. Clone and Customize

```bash
git clone https://github.com/stuartlau/stuartlau.github.io.git
cd stuartlau.github.io
bundle install
bundle exec jekyll serve
```

### 2. Update Configuration

Edit `_config.yml` to change:
- Site title and description
- Social media links
- Navigation structure

### 3. Add Your Content

- Create posts in `blogs/tech/` for technical articles
- Add patents to `blogs/patent/` using the existing template
- Update data files in `_data/` for your media collections

### 4. Deploy

Push to GitHub and GitHub Pages will automatically build and deploy.

## Design Decisions Worth Noting

### Light Theme Default
The site uses a light theme because:
- Better readability for long-form content
- Reduced eye strain during extended reading
- Matches the clean, professional aesthetic I prefer

### No Dark Mode Toggle
I chose to omit a dark mode toggle to maintain design consistency and avoid the complexity of dual theme support. The light theme is carefully tuned for readability across environments.

### External Links Open in New Tabs
Links to external resources (books on Douban, patent databases) open in new tabs to preserve the user's navigation context.

### Limited Social Integration
Rather than embedding every possible social widget, I've chosen minimal integration—RSS for syndication, email for contact. This respects user privacy and page performance.

## Acknowledgments

This site was inspired by:
- [Minimalist Jekyll themes](https://github.com/pages-themes) for clean design
- [Digital gardens](https://maggie Appleton's digital garden) for the philosophy of learning in public
- The GitHub Pages community for excellent documentation

## License

Feel free to fork this project for your own personal website. The content (blog posts, patent descriptions, travel journals) is copyrighted. The code and design are available under the MIT license.

## Contact

- **Email**: stuart8@126.com
- **GitHub**: [@stuartlau](https://github.com/stuartlau)
- **LinkedIn**: [stuartlau](https://www.linkedin.com/in/stuartlau)

---

> "The best way to learn is to teach." — This site is my teaching.
