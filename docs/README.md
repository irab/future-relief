# Documentation

This directory contains the documentation for the Future Relief project.

## Building Locally

To build and preview the documentation locally:

```bash
# Install dependencies
pip install -r docs/requirements.txt

# Serve locally (with auto-reload)
mkdocs serve

# Build static site
mkdocs build
```

The documentation will be available at `http://localhost:8000` when using `mkdocs serve`.

## Documentation Structure

- `index.md` - Main landing page
- `INSTALL.md` - Installation instructions
- `QUICK_START.md` - Quick start guide
- `MERGING_TILES.md` - Guide for merging multiple tiles
- `QGIS_STL_CONVERSION.md` - Detailed STL conversion guide
- `TEST_TILES_GUIDE.md` - Creating test tiles
- `CHECK_DIMENSIONS.md` - Checking DEM dimensions
- `PRUSA_XL_SETTINGS.md` - Prusa XL specific settings
- `ADDING_BASE.md` - Adding a base to models
- `3D_PRINTING_STRUCTURE.md` - Understanding print structure
- `WHY_VERTICAL_EXAGGERATION.md` - Why exaggeration is used
- `TROUBLESHOOTING.md` - Common issues and solutions
- `ADJUSTING_DEM_DISPLAY.md` - Fixing display issues
- `INSTALL_QGIS.md` - QGIS installation details
- `DATA_SOURCES.md` - Data source information

## GitHub Pages

The documentation is automatically deployed to GitHub Pages when changes are pushed to the main branch. The workflow is defined in `.github/workflows/docs.yml`.

## Theme

The documentation uses [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), which provides:
- Responsive design
- Dark mode support
- Search functionality
- Navigation tabs and sections
