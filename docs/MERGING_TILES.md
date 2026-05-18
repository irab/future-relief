# Merging Multiple DEM Tiles for Large Format Printing

This guide explains how to work with multiple GeoTIFF tiles to create one large 3D map for 2m x 1.5m printing.

## Overview

You have 13 GeoTIFF tiles covering a region. To create a single large 3D map:

1. **Merge all tiles** into one continuous DEM
2. **Clip to your desired area** (if needed)
3. **Convert to STL** at 2m x 1.5m scale
4. **Create print tiles** if your printer bed is smaller than 2m x 1.5m

## Understanding Your Tiles

Your tiles follow New Zealand map grid naming (e.g., BN32, BP33, BQ32):
- These are 1:50,000 map sheet tiles
- They cover a contiguous area
- Total data size: ~13GB+ (some individual tiles are 2-3GB)

**Important:** Processing all tiles at once requires significant RAM (8GB+ recommended).

## Step 1: Load All Tiles in QGIS

### Option A: Load All at Once (Recommended for Merging)

1. **Open QGIS**
2. **Add Multiple Raster Layers**
   - Go to **Layer** → **Add Layer** → **Add Raster Layer**
   - Navigate to `lds-new-zealand-lidar-1m-dem-GTiff/`
   - Select **ALL** `.tif` files (Ctrl+A or Cmd+A)
   - Click **Open**
   - QGIS will load all 13 tiles as separate layers

3. **Verify Coverage**
   - Zoom to full extent: **View** → **Zoom Full**
   - You should see all tiles forming a continuous map
   - Check that tiles align properly (no gaps)

### Option B: Load Tiles One by One (If Memory Issues)

If QGIS struggles with all tiles at once:
1. Load 3-4 tiles at a time
2. Merge in batches
3. Then merge the batch results

## Step 2: Merge All Tiles

1. **Open Merge Tool**
   - Go to **Raster** → **Miscellaneous** → **Merge**

2. **Select All Input Layers**
   - In the Merge dialog, click the dropdown for "Input layers"
   - Select **ALL** your DEM tile layers
   - Or use the "..." button to browse and select all files

3. **Configure Output**
   - **Output file**: Choose location (e.g., `data/processed/merged_full_area.tif`)
   - **Output data type**: Keep default (usually Float32)
   - **No data value**: Leave as default or set to -9999

4. **Advanced Options** (if needed)
   - **Place each input file into a separate band**: Unchecked (we want one continuous DEM)
   - **Create VRT**: Unchecked (we want actual merged file)

5. **Run Merge**
   - Click **Run**
   - **This will take time** - merging 13 tiles (13GB+) may take 10-30+ minutes
   - Progress will be shown in the Processing Toolbox panel
   - You may see a command window showing the GDAL command being executed:
     ```
     gdal_merge.py -ot Float32 -of GTiff -o [output_path] --optfile [temp_file]
     ```
     This is normal - QGIS uses GDAL command-line tools under the hood
   - **Don't close QGIS** while processing

6. **Result**
   - A new merged raster layer will appear in your Layers panel
   - The merged file will be saved to your specified output location
   - Remove individual tile layers to save memory (right-click each → Remove Layer)

## Step 3: Check Merged DEM

1. **Verify the Merged Layer**
   - Right-click merged layer → **Properties** → **Information**
   - Check dimensions (should be large - thousands of pixels)
   - Check coordinate system (EPSG:2193)
   - Check statistics (min/max elevation)

2. **Visual Check**
   - Zoom to full extent
   - Use **Identify Features** tool to check elevation values
   - Verify no obvious seams or artifacts

3. **Improve Visualization (Recommended)**
   - If the DEM looks dark or you want to see more detail:
     - Right-click layer → **Properties** → **Symbology**
     - Change **Render type** to **Hillshade**
     - Click **Apply** - this creates a 3D-like shaded relief that makes terrain detail very visible
   - Hillshade is especially good for seeing detail in low-lying areas
   - See `docs/ADJUSTING_DEM_DISPLAY.md` for more visualization options

## Step 4: Clip to Desired Area (Optional)

If you want to focus on a specific region within the merged area:

1. **Define Your Area**
   - Draw a polygon using **Vector** → **Create Layer** → **New Shapefile Layer**
   - Or use **View** → **New Print Layout** to define extent
   - Or note coordinates of your desired area

2. **Clip Raster**
   - **Raster** → **Extraction** → **Clip Raster by Mask Layer** (if using polygon)
   - Or **Raster** → **Extraction** → **Clip Raster by Extent** (if using coordinates)
   - Select your merged DEM
   - Set output location
   - Click **Run**

## Step 5: Convert Merged DEM to STL

Now convert your merged (and optionally clipped) DEM to STL:

1. **Select Merged Layer**
   - Click on your merged/clipped DEM layer

2. **Open DEMto3D**
   - **Raster** → **DEMto3D** → **DEM 3D Printing**

3. **Configure for 2m x 1.5m Print**

   **Model Dimensions:**
   - **Model width**: `2000` mm (2 meters)
   - **Model height**: `1500` mm (1.5 meters)
   - Plugin calculates scale automatically

   **Model Settings:**
   - **Model size spacing**: `0.2` mm (or `0.3` mm for faster processing)
   - **Model height**: `-2.18` (minimum elevation)
   - **Note**: Add 20mm base in PrusaSlicer (see [Adding a Base](ADDING_BASE.md))
   
   **Vertical Exaggeration:**
   - **6.0x** (recommended for Prusa XL)
     - Creates ~186mm terrain height (fits in 360mm bed)
     - Good terrain visibility
     - See [Why Vertical Exaggeration](WHY_VERTICAL_EXAGGERATION.md) for details

   **Output:**
   - **Output file**: `output/full_area_map.stl`
   - **Format**: STL Binary (recommended)

4. **Generate STL**
   - Click **OK**
   - **This will take significant time** - potentially 30-60+ minutes for a large area
   - The plugin processes the entire DEM into a mesh

## Step 6: Handle Large STL File

The resulting STL file may be very large (hundreds of MB to several GB). Options:

### Option A: Use as-is (If Your Slicer Can Handle It)

1. Open in your slicer
2. Check if it loads (some slicers have file size limits)
3. If it works, proceed to printing

### Option B: Create Print Tiles from STL

If the STL is too large or your printer bed is smaller than 2m x 1.5m:

1. **In QGIS - Create Grid Before STL Conversion**
   - Create a grid matching your printer bed size
   - Clip merged DEM to each grid cell
   - Convert each cell to STL separately
   - See "Creating Tiles" section in `docs/QUICK_START.md`

2. **In Mesh Editor (Alternative)**
   - Open large STL in MeshLab or Blender
   - Split into smaller tiles
   - Export each tile separately

## Performance Tips

### Memory Management
- **Close other applications** before merging
- **Process in batches** if you have <16GB RAM
- **Use virtual raster (VRT)** for viewing, then merge for processing

### Processing Time
- Merging 13 tiles: 10-30+ minutes
- STL conversion: 30-60+ minutes (depends on area size and spacing)
- **Be patient** - large datasets take time

### Monitoring Progress
- **Processing Toolbox panel**: Shows progress percentage and status
- **Command window**: May show GDAL commands (e.g., `gdal_merge.py`) - this is normal
- **Don't close QGIS** while processing is running
- The merged layer will appear automatically when complete

### File Sizes
- Merged GeoTIFF: May be 10-20GB+
- STL file: 500MB - 5GB+ depending on spacing
- Ensure you have enough disk space (need ~2x input size for merging)

## Alternative: Virtual Raster (VRT) Approach

If merging is too resource-intensive, use a Virtual Raster:

1. **Create VRT**
   - **Raster** → **Miscellaneous** → **Build Virtual Raster**
   - Select all tile files
   - Output: `merged.vrt`
   - This creates a "virtual" merged file without actually combining data

2. **Use VRT for STL Conversion**
   - DEMto3D can work with VRT files
   - Processing may be slower but uses less disk space

## Troubleshooting

### QGIS Crashes When Loading All Tiles
- Load tiles in smaller batches (3-4 at a time)
- Merge batches first, then merge batch results
- Increase system RAM if possible

### Merge Takes Too Long
- This is normal for 13GB+ of data
- Let it run - don't interrupt
- Check disk space (need 2x the size of input data)
- You may see GDAL commands in a command window - this is normal
- Monitor progress in the Processing Toolbox panel, not just the command window

### STL File Too Large
- Increase model size spacing (0.3mm or 0.5mm)
- Clip to smaller area
- Create tiles before STL conversion

### Out of Memory Errors
- Process in smaller batches
- Use VRT approach instead of full merge
- Close other applications
- Consider processing on a machine with more RAM

## Recommended Workflow Summary

1. ✅ Load all 13 tiles in QGIS
2. ✅ Merge all tiles → `merged_full_area.tif`
3. ✅ (Optional) Clip to specific region
4. ✅ Convert merged DEM to STL at 2m x 1.5m scale
5. ✅ If STL too large or printer bed smaller:
   - Create grid matching printer bed size
   - Clip merged DEM to each grid cell
   - Convert each cell to STL
6. ✅ Print and assemble tiles

## Next Steps

- See `docs/QUICK_START.md` for detailed STL conversion settings
- See `docs/QGIS_STL_CONVERSION.md` for advanced techniques
