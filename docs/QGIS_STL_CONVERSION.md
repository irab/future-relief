# Converting LiDAR DEM to STL for 3D Printing (2m x 1.5m)

This guide explains how to convert the 1m resolution LiDAR GeoTIFF files to STL format for 3D printing using QGIS and the DEMto3D plugin.

## Overview

For a large format print (2m x 1.5m), you'll need to:
1. Import and merge the GeoTIFF tiles in QGIS
2. Clip to your area of interest
3. Use the DEMto3D plugin to convert to STL tiles
4. Export multiple tiles that can be printed and assembled

## Prerequisites

- **QGIS 3.x** (latest version recommended)
- **DEMto3D Plugin** - Available in QGIS Plugin Repository

## Step 1: Install DEMto3D Plugin

1. Open QGIS
2. Go to **Plugins** → **Manage and Install Plugins**
3. Search for "**DEMto3D**"
4. Click **Install Plugin**
5. The plugin will appear in the menu: **Raster** → **DEMto3D**

## Step 2: Import GeoTIFF Files

1. In QGIS, go to **Layer** → **Add Layer** → **Add Raster Layer**
2. Navigate to `lds-new-zealand-lidar-1m-dem-GTiff/`
3. Select all the `.tif` files you want to use (or select one to start)
4. Click **Open**

**Note:** If you have multiple tiles covering your area of interest, you may want to merge them first.

### Optional: Merge Multiple Tiles

If you need to combine multiple GeoTIFF tiles:

1. Go to **Raster** → **Miscellaneous** → **Merge**
2. Select all your input raster layers
3. Set output file location
4. Click **Run**

## Step 3: Clip to Area of Interest (Optional)

If you want to focus on a specific area:

1. Create a polygon layer for your area of interest, or
2. Use **Raster** → **Extraction** → **Clip Raster by Extent**
3. Set the extent to your desired area
4. Save the clipped raster

## Step 4: Prepare for Tiling

For a 2m x 1.5m print, you'll likely need to create tiles. The DEMto3D plugin can help with this, but you may want to:

1. **Calculate your tile size**: 
   - If your printer bed is smaller than 2m x 1.5m, divide the area into manageable tiles
   - For example, if printer bed is 300mm x 300mm, you'd need approximately 7 x 5 tiles

2. **Consider vertical exaggeration**:
   - Natural terrain may be too flat for 3D printing
   - Typical exaggeration: 2x to 5x for terrain visualization

## Step 5: Convert to STL Using DEMto3D

1. Make sure your DEM raster layer is selected in the Layers panel
2. Go to **Raster** → **DEMto3D** → **DEM 3D Printing**
3. Configure the settings:

   **General Settings:**
   - **Input DEM**: Select your raster layer
   - **Model size spacing**: 0.2 mm (standard for most 3D printers)
   - **Model height**: Set to the lowest elevation point (in meters)
     - You can find this in the layer properties → Statistics
   
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
   - **Format**: STL (ASCII or Binary - Binary is smaller)

4. Click **OK** to generate the STL file

## Step 6: Creating Tiles (If Needed)

If your print area is larger than your printer bed, you'll need to create tiles:

### Option A: Use DEMto3D with Extent Clipping

1. Before running DEMto3D, clip your raster to each tile extent
2. Run DEMto3D for each tile
3. Name files systematically (e.g., `tile_01_01.stl`, `tile_01_02.stl`)

### Option B: Use QGIS Raster Split Tool

1. Install **Raster Split** plugin (if available) or use GDAL tools
2. Split your raster into grid tiles
3. Process each tile with DEMto3D

### Option C: Manual Tiling Workflow

1. Create a grid layer covering your area:
   - **Vector** → **Research Tools** → **Create Grid**
   - Set grid size to match your printer bed dimensions (accounting for scale)
   
2. For each grid cell:
   - Clip raster to that extent
   - Run DEMto3D
   - Export STL with descriptive name

## Step 7: Post-Processing STL Files

After generating STL files, you may want to:

1. **Check in a 3D viewer** (e.g., MeshLab, Blender, or your slicer)
2. **Repair mesh** if needed (many slicers do this automatically)
3. **Scale verification**: Ensure dimensions are correct
4. **Add base/support**: Some models benefit from a flat base

## Tips for Large Format Printing

1. **Layer Height**: Use 0.2-0.3mm layer height for good detail
2. **Infill**: 10-20% is usually sufficient for terrain models
3. **Supports**: May need supports for overhangs
4. **Print Orientation**: Print with base flat on bed
5. **Material**: PLA is good for large prints, PETG for durability
6. **Assembly**: Plan for alignment marks or connection points between tiles

## Troubleshooting

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

### Tiles don't align
- Ensure consistent scale across all tiles
- Use same base height and vertical exaggeration
- Consider adding alignment markers in the model

## Additional Resources

- [DEMto3D Plugin Documentation](https://plugins.qgis.org/plugins/DEMto3D/)
- [QGIS Raster Processing](https://docs.qgis.org/latest/en/docs/user_manual/working_with_raster/index.html)
- [3D Printing Digital Elevation Models - OpenTopography](https://opentopography.org/learn/3D_printing)

## Coordinate System Notes

Your GeoTIFF files are in **NZGD2000 / New Zealand Transverse Mercator 2000 (EPSG:2193)**. QGIS should automatically detect this, but if you have issues:

1. Right-click layer → **Set Layer CRS**
2. Select EPSG:2193
3. Ensure project CRS matches (Project → Properties → CRS)
