# Installation Guide

This guide will help you set up the environment to convert LiDAR DEM data to STL files for 3D printing.

## Overview

This project uses QGIS with the DEMto3D plugin to convert 1m resolution LiDAR GeoTIFF files into STL format for 3D printing large format terrain models (2m x 1.5m).

## System Requirements

- **OS**: Debian 11+ (Bullseye/Trixie) or Ubuntu 20.04+
- **RAM**: 4GB minimum, 8GB+ recommended
- **Disk Space**: ~2GB for QGIS installation
- **Graphics**: OpenGL support recommended for 3D features

## Quick Start

### Step 1: Install QGIS

Run the installation script:

```bash
./scripts/install_qgis.sh
```

This will install QGIS from Debian repositories (version 3.40.6+).

**Alternative Manual Installation:**

```bash
sudo apt-get update
sudo apt-get install -y qgis qgis-plugin-grass
```

Verify installation:

```bash
qgis --version
```

### Step 2: Install DEMto3D Plugin

1. **Launch QGIS**
   - From applications menu, or
   - Run `qgis` from terminal

2. **Open Plugin Manager**
   - Go to **Plugins** → **Manage and Install Plugins**
   - Or press `Ctrl+Shift+P`

3. **Install DEMto3D**
   - Click on **All** tab
   - Search for "**DEMto3D**"
   - Select **DEMto3D** from the list
   - Click **Install Plugin**
   - Wait for installation to complete

4. **Verify Installation**
   - Go to **Raster** menu
   - You should see **DEMto3D** option
   - If not visible, go to **Plugins** → **Manage and Install Plugins** → **Installed** tab
   - Make sure DEMto3D is checked/enabled

### Step 3: Prepare Your Data

The LiDAR data should be in GeoTIFF format in the `lds-new-zealand-lidar-1m-dem-GTiff/` directory.

If you need to download the data:
- Source: [LINZ Data Service - New Zealand LiDAR 1m DEM](https://data.linz.govt.nz/layer/121859-new-zealand-lidar-1m-dem/)
- Coordinate system: NZGD2000 / New Zealand Transverse Mercator 2000 (EPSG:2193)

## Converting DEM to STL

### Basic Workflow

1. **Open QGIS** and load your GeoTIFF files:
   - **Layer** → **Add Layer** → **Add Raster Layer**
   - Navigate to `lds-new-zealand-lidar-1m-dem-GTiff/`
   - Select your `.tif` files

2. **Merge tiles** (if needed):
   - **Raster** → **Miscellaneous** → **Merge**
   - Select all input raster layers
   - Set output file location
   - Click **Run**

3. **Convert to STL**:
   - Select your DEM raster layer
   - **Raster** → **DEMto3D** → **DEM 3D Printing**
   - Configure settings (see detailed guide below)
   - Click **OK** to generate STL

### Detailed Conversion Settings

For a **2m x 1.5m** print:

**General Settings:**
- **Input DEM**: Select your raster layer
- **Model size spacing**: 0.2 mm (standard for most 3D printers)
- **Model height**: Set to the lowest elevation point (check layer properties → Statistics)

**Model Dimensions:**
- **Model width**: 2000 mm (2 meters)
- **Model height**: 1500 mm (1.5 meters)
- The plugin will automatically calculate the scale

**Vertical Settings:**
- **Base height**: Usually 0 (or lowest point)
- **Vertical exaggeration**: Start with 2.0x, adjust as needed
  - Higher values = more dramatic terrain
  - Lower values = more accurate representation

**Output:**
- **Output file**: Choose location and filename (e.g., `wellington_map.stl`)
- **Format**: STL (Binary is smaller than ASCII)

### Creating Tiles for Large Prints

If your printer bed is smaller than 2m x 1.5m, you'll need to create tiles:

1. **Create a grid** covering your area:
   - **Vector** → **Research Tools** → **Create Grid**
   - Set grid size to match your printer bed dimensions

2. **For each grid cell**:
   - Clip raster to that extent: **Raster** → **Extraction** → **Clip Raster by Extent**
   - Run DEMto3D on the clipped raster
   - Export STL with descriptive name (e.g., `tile_01_01.stl`)

## Troubleshooting

### QGIS won't start
- Check dependencies: `sudo apt-get install -f`
- Run from terminal to see errors: `qgis`

### Plugin not appearing
- Make sure plugin is enabled in Plugin Manager → Installed tab
- Restart QGIS after installation
- Check QGIS version compatibility (DEMto3D works with QGIS 3.x)

### STL file is too large
- Reduce model size spacing (e.g., 0.3mm or 0.5mm)
- Use binary STL format instead of ASCII
- Clip to smaller area

### Terrain is too flat
- Increase vertical exaggeration (try 3x or 5x)
- Check that your DEM has sufficient elevation range

### File won't load in slicer
- Check file size (some slicers have limits)
- Try repairing mesh in MeshLab or Netfabb
- Ensure STL is not corrupted

## Next Steps

**Ready to convert your DEM to STL?** See the step-by-step guide:
- **[Quick Start Guide](docs/QUICK_START.md)** - Complete walkthrough for converting DEM to STL

After generating your STL files:

1. **Check in a 3D viewer** (e.g., MeshLab, Blender, or your slicer)
2. **Repair mesh** if needed (many slicers do this automatically)
3. **Scale verification**: Ensure dimensions are correct
4. **Prepare for printing**:
   - Layer height: 0.2-0.3mm for good detail
   - Infill: 10-20% is usually sufficient
   - Supports: May need supports for overhangs
   - Material: PLA is good for large prints, PETG for durability

## Additional Resources

- **Quick Start Guide**: See `docs/QUICK_START.md` for step-by-step conversion instructions
- **Merging Multiple Tiles**: See `docs/MERGING_TILES.md` if you have multiple GeoTIFF tiles to combine
- **Detailed STL Conversion Guide**: See `docs/QGIS_STL_CONVERSION.md` for advanced techniques
- **QGIS Installation Details**: See `docs/INSTALL_QGIS.md`
- **DEMto3D Plugin Documentation**: https://plugins.qgis.org/plugins/DEMto3D/
- **QGIS Raster Processing**: https://docs.qgis.org/latest/en/docs/user_manual/working_with_raster/index.html

## Python Environment (Optional)

If you want to use the Python processing scripts:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

See `README.md` for more information about the Python tools.

## Support

For issues or questions:
- Check the troubleshooting section above
- Review the detailed guides in `docs/`
- Consult QGIS and DEMto3D plugin documentation
