# Quick Start Guide - Converting DEM to STL

This is a step-by-step guide for converting your LiDAR GeoTIFF files to STL format for 3D printing, assuming you've already installed QGIS and the DEMto3D plugin.

## Prerequisites

- ✅ QGIS installed (see `INSTALL.md`)
- ✅ DEMto3D plugin installed (see `INSTALL.md`)
- ✅ Tiles created (see [CREATING_TILES.md](CREATING_TILES.md) or [AUTOMATING_TILES.md](AUTOMATING_TILES.md))

**Workflow:**
1. Merge GeoTIFF tiles → [MERGING_TILES.md](MERGING_TILES.md)
2. Create print tiles → [CREATING_TILES.md](CREATING_TILES.md) or [AUTOMATING_TILES.md](AUTOMATING_TILES.md)
3. Convert tiles to STL → This guide
4. Print and assemble → [Prusa XL Settings](PRUSA_XL_SETTINGS.md)

**Tip:** If your DEM looks dark or lacks detail, switch to **Hillshade** visualization:
- Right-click layer → **Properties** → **Symbology** → Change **Render type** to **Hillshade**
- This creates a 3D-like shaded relief that makes terrain detail very visible, especially in low-lying areas!

## Step-by-Step Conversion (For Each Tile)

You have 30 tiles to convert. Start with 1-2 test tiles first!

### Step 1: Load a Tile

1. **Open QGIS**
   - Launch from applications menu or run `qgis` from terminal

2. **Add Raster Layer**
   - Go to **Layer** → **Add Layer** → **Add Raster Layer**
   - Navigate to `data/processed/tiles/`
   - Select one tile (start with `tile_01_01.tif` for testing)
   - Click **Open**

3. **Verify Tile Properties** (Optional)
   - Right-click the layer → **Properties** → **Information**
   - Check coordinate system (should be EPSG:2193)
   - Check dimensions

### Step 2: Set Layer Extent in DEMto3D

**Before configuring model dimensions:**

1. In the DEMto3D dialog, find the **Layer extent** section
2. Click the **leftmost magnifying glass** button (square with outward arrows)
   - This automatically sets the extent from your tile
   - The X and Y coordinate fields should fill automatically
3. **Important:** Do this before setting model dimensions, or the Height (m) field may get cleared

### Step 3: Convert Tile to STL Using DEMto3D

1. **Select Your Tile Layer**
   - Click on your tile layer in the Layers panel to select it

2. **Open DEMto3D Plugin**
   - Go to **Raster** → **DEMto3D** → **DEM 3D Printing**

3. **Configure Settings**

   **Layer Extent:**
   - Click the **leftmost magnifying glass** button (sets extent from layer)
   - X and Y fields should fill automatically
   
   **Model Dimensions:**
   - **Model width**: `330` mm
   - **Model height (length)**: `330` mm
   - This creates a tile that fits on Prusa XL bed
   
   **Model Settings:**
   - **Model size spacing**: `0.2` mm (or `0.3` mm for faster processing)
   - **Height (m)**: `-2.18` ⚠️ **REQUIRED - Fill this field!**
   - **Base height (mm)**: `0` ⚠️ **REQUIRED - Fill this field!**
   
   **Vertical Exaggeration:**
   - **Vertical exaggeration**: `6.0`
     - Creates ~186mm terrain height (fits in 360mm bed)
     - See [Why Vertical Exaggeration](WHY_VERTICAL_EXAGGERATION.md) for details
   
   **Output:**
   - **Output file**: `output/tile_01_01.stl` (match your tile name)
   - **Format**: STL Binary (recommended)

4. **Generate STL**
   - Click **"Export to STL"**
   - **Wait 5-15 minutes** per tile
   - Progress shown in Processing Toolbox panel
   - **Don't close QGIS** during processing

### Step 5: Verify Your STL File

1. **Check File Size**
   - Large files (>100MB) may need adjustment
   - If too large, increase model size spacing or reduce area

2. **Open in 3D Viewer**
   - Use MeshLab, Blender, or your 3D printer slicer
   - Verify dimensions are correct
   - Check that terrain looks good

3. **Repair if Needed**
   - Many slicers auto-repair meshes
   - If issues persist, use MeshLab or Netfabb to repair

## Processing All 30 Tiles

After testing 1-2 tiles successfully:

1. **Process in batches**: 5-10 tiles at a time
2. **Use consistent settings** for all tiles
3. **Name systematically**: `tile_01_01.stl`, `tile_01_02.stl`, etc.
4. **Take breaks** between batches (each tile takes 5-15 minutes)
5. **Total time**: 2.5-7.5 hours for all 30 tiles

See [NEXT_STEPS_AFTER_TILES.md](NEXT_STEPS_AFTER_TILES.md) for complete workflow.

## Tips for Success

### First Time Users
- **Start small**: Test with a small clipped area first
- **Check dimensions**: Verify your STL dimensions match expectations
- **Adjust exaggeration**: Try different vertical exaggeration values to see what looks best
- **File size**: Large STL files can be slow to process in slicers

### For Large Format Printing (2m x 1.5m)
- **Tiling is essential**: Most printers can't handle this size in one piece
- **Plan your grid**: Calculate how many tiles you need based on printer bed size
- **Consistent settings**: Use the same settings (exaggeration, base height) for all tiles
- **Alignment**: Consider adding alignment markers or connection points

### Performance Optimization
- **Model size spacing**: Increase to 0.3-0.5mm for faster processing and smaller files
- **Clip first**: Process smaller areas rather than full DEM
- **Binary STL**: Always use binary format for smaller files

## Troubleshooting

### STL file is too large
- Increase model size spacing (0.3mm or 0.5mm)
- Use binary STL format
- Clip to smaller area

### Terrain looks too flat
- Increase vertical exaggeration (try 3x or 5x)
- Check that your DEM has sufficient elevation range

### Processing takes too long
- Increase model size spacing
- Clip to smaller area
- Close other applications to free up RAM

### File won't load in slicer
- Check file size (some slicers have limits)
- Try repairing mesh in MeshLab or Netfabb
- Ensure STL is not corrupted
- Try opening in a different viewer first

### Tiles don't align
- Ensure consistent scale across all tiles
- Use same base height and vertical exaggeration for all tiles
- Consider adding alignment markers in the model

## Next Steps After STL Generation

1. **Import to Slicer**
   - Open STL in your 3D printer slicer (PrusaSlicer, Cura, etc.)
   - Verify dimensions

2. **Configure Print Settings**
   - **Layer height**: 0.2-0.3mm for good detail
   - **Infill**: 10-20% is usually sufficient for terrain models
   - **Supports**: May need supports for overhangs
   - **Print orientation**: Base flat on bed

3. **Print and Assemble**
   - Print each tile
   - Assemble tiles using alignment marks or connection points

## Additional Resources

- **[Next Steps After Tiles](NEXT_STEPS_AFTER_TILES.md)** - Complete workflow after creating tiles
- **[First STL Guide](FIRST_STL_GUIDE.md)** - Detailed STL conversion steps
- **[Creating Tiles](CREATING_TILES.md)** - How tiles were created
- **[Merging Tiles](MERGING_TILES.md)** - Merging multiple GeoTIFF tiles
- **[Adding a Base](ADDING_BASE.md)** - Adding 20mm base in PrusaSlicer
- **[Prusa XL Settings](PRUSA_XL_SETTINGS.md)** - Print settings
- **Installation**: See `INSTALL.md` if you need to install QGIS or plugins
- **DEMto3D Documentation**: https://plugins.qgis.org/plugins/DEMto3D/
