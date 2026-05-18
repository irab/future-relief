# Creating Multiple Tiles for 3D Printing

DEMto3D creates **one STL file at a time**. To create multiple tiles for your Prusa XL, you need to clip your merged DEM into separate areas first, then convert each area to STL.

## Overview

For a 2m x 1.5m map on a Prusa XL (360mm x 360mm bed), you need tiles. 

**Important:** Your DEM is rectangular (73.75km × 96.31km), so dividing into a 6×5 grid creates **rectangular tiles** (12.29km × 19.26km). These will convert to **rectangular STL files**, not square ones.

**For square STL tiles (330mm × 330mm):**
- See **[Square Tiles Guide](SQUARE_TILES.md)** for creating square tiles
- Recommended: Use square tiles for easier assembly

**For rectangular tiles (current approach):**
- 6 columns × 5 rows = **30 tiles**
- Tiles will be rectangular in STL format
- Still printable, but harder to align

**Process:**
1. Create a grid covering your area
2. Clip merged DEM to each grid cell
3. Convert each clipped area to STL
4. Print each tile separately

## Step 1: Create a Grid

1. **In QGIS**, go to **Vector** → **Research Tools** → **Create Grid**

2. **Configure Grid:**
   - **Grid type**: Rectangle (grid)
   - **Grid extent**: 
     - Click the dropdown → **Calculate from Layer** → Select `merged_full_area`
     - This sets the extent to cover your entire DEM
   
   - **Horizontal spacing**: Calculate based on your scale
     - Your DEM is 73.75km wide
     - For 6 tiles: 73.75km ÷ 6 = **12.29km** per tile
     - Enter: `12290` meters
   
   - **Vertical spacing**: 
     - Your DEM is 96.31km tall
     - For 5 tiles: 96.31km ÷ 5 = **19.26km** per tile
     - Enter: `19260` meters
   
   - **Output**: `data/processed/print_grid.shp`
   
   - Click **Run**

3. **Result**: You'll get a grid layer with 30 cells (6 × 5)

## Step 2: Clip DEM to Each Grid Cell

You'll need to do this for each of the 30 grid cells. Here's the process:

### For Each Grid Cell:

1. **Select one grid cell:**
   - Use the **Select Features** tool (arrow icon)
   - Click on one grid cell to select it

2. **Clip Raster by Mask Layer:**
   - **Raster** → **Extraction** → **Clip Raster by Mask Layer**
   - **Input layer**: `merged_full_area`
   - **Mask layer**: Your grid layer
   - **Selected features only**: ✅ Check this (important!)
   - **Output file**: `data/processed/tile_01_01.tif` (use systematic naming)
   - Click **Run**

3. **Repeat for all 30 cells:**
   - Name them: `tile_01_01.tif`, `tile_01_02.tif`, ... `tile_06_05.tif`
   - Or: `tile_1_1.tif`, `tile_1_2.tif`, ... `tile_6_5.tif`

## Step 3: Convert Each Tile to STL

Now convert each clipped tile to STL using DEMto3D. You have 30 tiles to convert.

### Recommended: Start with Test Tiles

**Before processing all 30 tiles, test with 1-2 tiles first:**

1. Convert `tile_01_01.tif` and `tile_01_02.tif` to STL
2. Verify they look correct in PrusaSlicer
3. Check dimensions are 330mm × 330mm
4. If good, proceed with all tiles

### For Each Tile:

1. **Load the tile in QGIS:**
   - **Layer** → **Add Layer** → **Add Raster Layer**
   - Navigate to `data/processed/tiles/`
   - Select one tile (e.g., `tile_01_01.tif`)
   - Click **Open**

2. **Select the tile layer** in the Layers panel

3. **Open DEMto3D:**
   - **Raster** → **DEMto3D** → **DEM 3D Printing**

4. **Configure Settings:**
   - **Layer extent**: Click the **leftmost magnifying glass** button (sets extent from layer)
   - **Model width**: `330` mm
   - **Model height (length)**: `330` mm
   - **Model size spacing**: `0.2` mm (or `0.3` mm for faster processing)
   - **Height (m)**: `-2.18` ⚠️ **Important: Fill this field!**
   - **Base height (mm)**: `0` ⚠️ **Important: Fill this field!**
   - **Vertical exaggeration**: `6.0`
   - **Output file**: `output/tile_01_01.stl` (match your tile naming)
   - **Format**: STL Binary

5. **Click "Export to STL"**
   - Wait 5-15 minutes per tile
   - Progress shown in Processing Toolbox

6. **Repeat for all 30 tiles**
   - Process in batches of 5-10 tiles
   - Take breaks between batches

## Automated Tile Creation

### Using Standalone Script (Recommended)

You can create all tiles automatically using a Python script:

```bash
python3 scripts/create_tiles_standalone.py
```

This script:
- Uses GDAL command-line tools (no QGIS needed)
- Creates all 30 tiles automatically
- Takes 30-90 minutes total
- Saves tiles to `data/processed/tiles/`

See [AUTOMATING_TILES.md](AUTOMATING_TILES.md) for details.

### Using QGIS Python Console

Alternatively, run `scripts/create_tiles_simple.py` from QGIS Python Console.

## Manual Batch Processing

If you prefer to do it manually but more efficiently:

1. **Process in batches**: Do 5-10 tiles at a time
2. **Use consistent naming**: Makes it easier to track
3. **Verify each tile**: Check dimensions are correct

## Naming Convention

Use a systematic naming scheme:

**Option 1: Row_Column**
- `tile_01_01.stl` (row 1, column 1)
- `tile_01_02.stl` (row 1, column 2)
- ...
- `tile_06_05.stl` (row 6, column 5)

**Option 2: Sequential**
- `tile_001.stl`, `tile_002.stl`, ... `tile_030.stl`

**Option 3: Coordinates**
- `tile_NW.stl` (northwest)
- `tile_NE.stl` (northeast)
- etc.

## Verification

After creating all tiles:

1. **Check file sizes**: Should be similar (50-200MB each)
2. **Check dimensions**: All should be 330mm x 330mm
3. **Open a few in PrusaSlicer**: Verify they look correct
4. **Check alignment**: Tiles should fit together when assembled

## Time Estimate

- **Creating grid**: 1 minute
- **Clipping 30 tiles**: 30-60 minutes (1-2 min per tile)
- **Converting to STL**: 2.5-7.5 hours (5-15 min per tile)
- **Total**: 3-8 hours for all 30 tiles

## Tips

1. **Start with 1-2 test tiles** to verify settings
2. **Process in batches** - don't try to do all 30 at once
3. **Use consistent settings** for all tiles (same exaggeration, spacing, etc.)
4. **Save your work** - QGIS projects can be saved to resume later
5. **Take breaks** - this is a long process!

## Alternative: Process Full Map Then Split

If you want to try processing the full map first:

1. Convert full merged DEM to one large STL (2m x 1.5m)
2. Use a 3D editor (Blender, MeshLab) to split into tiles
3. Export each tile separately

**However**, this approach:
- ❌ Creates a very large STL file (may crash)
- ❌ Harder to split accurately
- ❌ More complex workflow

**Recommended**: Clip DEM first, then convert (the approach above).

## After Creating Tiles

✅ **Tiles Created!** Now convert each to STL:

1. **Test First**: Convert 1-2 tiles to verify settings
2. **Batch Process**: Convert remaining tiles (5-10 at a time)
3. **Add Base**: Add 20mm base in PrusaSlicer (see [Adding a Base](ADDING_BASE.md))
4. **Print**: Configure print settings (see [Prusa XL Settings](PRUSA_XL_SETTINGS.md))
5. **Assemble**: Print and assemble all 30 tiles

## Quick Reference: DEMto3D Settings

For each tile, use these **exact settings**:

- **Layer extent**: Click leftmost magnifying glass
- **Model width**: `330` mm
- **Model height (length)**: `330` mm
- **Model size spacing**: `0.2` mm
- **Height (m)**: `-2.18` ⚠️ **Required!**
- **Base height (mm)**: `0` ⚠️ **Required!**
- **Vertical exaggeration**: `6.0`
- **Output format**: STL Binary

## Time Estimate

- **Creating tiles**: 30-90 minutes (automated)
- **Converting to STL**: 2.5-7.5 hours (30 tiles × 5-15 min each)
- **Total**: ~3-9 hours

**Tip**: Process tiles in batches and take breaks!
