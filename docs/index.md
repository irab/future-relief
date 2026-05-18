# Future Relief - 3D Terrain Mapping

Welcome to the Future Relief documentation! This project provides tools and guides for converting high-resolution LiDAR Digital Elevation Model (DEM) data into 3D printable terrain models.

## Overview

This project enables you to:

- **Process LiDAR data** from GeoTIFF format
- **Merge multiple tiles** into continuous terrain maps
- **Convert to STL format** for 3D printing
- **Create large-format terrain models** (2m x 1.5m+)
- **Optimize for 3D printing** on printers like the Prusa XL

## Quick Links

### 🚀 Getting Started

- **[Installation Guide](INSTALL.md)** - Set up QGIS and required plugins
- **[Quick Start Guide](QUICK_START.md)** - Convert your first DEM to STL

### 📚 Main Guides

- **[Complete Pipeline](COMPLETE_PIPELINE.md)** - Automated workflow from merged TIF to print-ready tiles ⭐
- **[Merging Tiles](MERGING_TILES.md)** - Combine multiple GeoTIFF tiles
- **[Detecting Flat Sea](DETECTING_FLAT_SEA.md)** - Exclude flat sea areas from printing
- **[Creating Tiles](CREATING_TILES.md)** - Split merged DEM into print tiles
- **[Converting to STL](FIRST_STL_GUIDE.md)** - Convert tiles to STL format
- **[Next Steps After Tiles](NEXT_STEPS_AFTER_TILES.md)** - What to do after creating tiles
- **[Test Tiles Guide](TEST_TILES_GUIDE.md)** - Create test prints to verify settings

### 🖨️ 3D Printing

- **[Prusa XL Settings](PRUSA_XL_SETTINGS.md)** - Optimized settings for Prusa XL
- **[Adding a Base](ADDING_BASE.md)** - How to add a stable base to your model
- **[Print Structure](3D_PRINTING_STRUCTURE.md)** - Understanding infill and structure
- **[Why Vertical Exaggeration](WHY_VERTICAL_EXAGGERATION.md)** - Understanding this standard technique

### 🔧 Troubleshooting

- **[Common Issues](TROUBLESHOOTING.md)** - Solutions to frequent problems
- **[Adjusting DEM Display](ADJUSTING_DEM_DISPLAY.md)** - Fix dark or unclear terrain visualization

## Typical Workflow

### Quick Automated Workflow (Recommended)

1. **Install QGIS and DEMto3D plugin** ([Installation Guide](INSTALL.md))
2. **Load and merge GeoTIFF tiles** ([Merging Tiles](MERGING_TILES.md))
3. **Run complete pipeline** ([Complete Pipeline](COMPLETE_PIPELINE.md)) ⭐
   - Detects and excludes flat sea areas
   - Creates square tiles automatically
4. **Convert tiles to STL** ([First STL Guide](FIRST_STL_GUIDE.md))
5. **Add base and prepare for printing** ([Adding a Base](ADDING_BASE.md), [Prusa XL Settings](PRUSA_XL_SETTINGS.md))
6. **Print and assemble** your terrain model!

### Manual Workflow

1. **Install QGIS and DEMto3D plugin** ([Installation Guide](INSTALL.md))
2. **Load and merge GeoTIFF tiles** ([Merging Tiles](MERGING_TILES.md))
3. **Detect flat sea** ([Detecting Flat Sea](DETECTING_FLAT_SEA.md)) (optional)
4. **Create print tiles** ([Creating Tiles](CREATING_TILES.md) or [Square Tiles](SQUARE_TILES.md))
5. **Convert tiles to STL** ([First STL Guide](FIRST_STL_GUIDE.md))
6. **Add base and prepare for printing** ([Adding a Base](ADDING_BASE.md), [Prusa XL Settings](PRUSA_XL_SETTINGS.md))
7. **Print and assemble** your terrain model!

## Features

- ✅ **1m Resolution LiDAR Data** - High-detail terrain models
- ✅ **Large Format Printing** - Support for 2m x 1.5m+ models
- ✅ **Tile Management** - Handle multiple GeoTIFF tiles efficiently
- ✅ **Optimized for 3D Printing** - Settings for Prusa XL and other printers
- ✅ **Professional Quality** - Standard cartographic practices

## Requirements

- **QGIS 3.x** - Geographic Information System
- **DEMto3D Plugin** - Converts DEM to STL format
- **3D Printer** - Prusa XL or similar large-format printer
- **Python 3.9+** (optional, for processing scripts)

## Data Sources

This project works with LiDAR DEM data from:
- **LINZ (Land Information New Zealand)** - 1m resolution DEM
- **Other sources** - Any GeoTIFF DEM data

See [Data Sources](DATA_SOURCES.md) for more information.

## License

[Add your license information here]

## Contributing

Contributions welcome! Please see the repository for contribution guidelines.

## Support

For issues or questions:
- Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
- Review the relevant documentation sections
- Open an issue on GitHub

---

**Ready to start?** Begin with the [Installation Guide](INSTALL.md)!
