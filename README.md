# xRegistry Codegen - GitHub Pages Branch

This branch contains the GitHub Pages site for the xRegistry Codegen project.

## Site Structure

```
gh-pages/
├── _config.yml          # Jekyll configuration
├── _layouts/            # Jekyll page templates
│   ├── default.html     # Base layout
│   └── gallery-viewer.html  # Gallery detail view
├── assets/
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript
│   └── images/          # Static images
├── gallery/             # Generated gallery pages
│   ├── index.md         # Gallery index
│   └── {example-id}/    # Individual examples
├── scripts/
│   └── build_gallery.py # Gallery generation script
├── index.md             # Home page
├── Gemfile              # Ruby dependencies
└── README.md            # This file
```

## Local Development

1. Install Ruby and Bundler
2. Install dependencies:
   ```bash
   bundle install
   ```
3. Serve locally:
   ```bash
   bundle exec jekyll serve
   ```
4. View at http://localhost:4000/xregistry-codegen/

## Rebuilding Gallery

The gallery is automatically rebuilt:
- On push to gh-pages branch
- Weekly (every Sunday)
- On new releases
- Manually via GitHub Actions

To rebuild locally:

```bash
# Install xrcg from main branch
pip install -e ../  # or pip install xrcg

# Ensure sample definitions are available
cp -r ../samples/message-definitions ./samples/

# Run the gallery build script
python scripts/build_gallery.py
```

## Deployment

This branch is deployed to GitHub Pages via GitHub Actions. The workflow:

1. Checks out this branch
2. Checks out main branch for xrcg and sample definitions
3. Generates gallery examples using xrcg
4. Builds Jekyll site
5. Deploys to GitHub Pages

## Visual Design

The site uses a light theme aligned with [xregistry.io](https://xregistry.io):
- Dark header/footer gradient
- White content backgrounds
- Blue accent color (#2879d0)
- Inter font family

## Related Links

- [Main Repository](https://github.com/xregistry/xregistry-codegen)
- [xRegistry Specification](https://xregistry.io)
- [CloudEvents](https://cloudevents.io)
