# Website for Rock Haven Property LLC

Live at https://rockhaven.llc

This is based on https://github.com/gautamkrishnar/github-pages-gallery/blob/master/README.md

## Local Development

### Prerequisites

- Docker Desktop (required)
  - Download from https://www.docker.com/products/docker-desktop/
  - Or install via Homebrew: `brew install --cask docker`
  - Make sure Docker Desktop is running before building

### Build and Preview Locally

```bash
# Build the gallery from your local photos
docker run -v "$(pwd):/work" ghcr.io/thumbsup/thumbsup /bin/sh -c "cd /work/ && thumbsup --config config.json"

# Customize the HTML
bash customize_html.sh

# Serve locally
cd build_output && python3 -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Content

- `gallery/<Album>/` — photos, one folder per album. Files are sorted by filename.
- `desc_index.html` — the availability table and text on the home page.
- `desc_u2b.html` — the text on the Unit 2B page (`Unit-2B.html`).
- `custom.css` — the theme overrides, including the tagline under the site title.
- `logo.png`, `favicon*`, `apple-touch-icon.png` — branding.

Pushing to `master` builds and deploys to GitHub Pages via `.github/workflows/gallery.yml`.
