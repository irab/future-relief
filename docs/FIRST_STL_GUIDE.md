# Creating STL Files from Tiles

Step-by-step guide to convert your clipped tiles to STL format using DEMto3D.

## Prerequisites

- ✅ QGIS installed and running
- ✅ DEMto3D plugin installed
- ✅ Tiles created (in `data/processed/tiles/` directory)
- ✅ **Check which tiles to convert** (see Step 0 below)

## Step 0: Check Which Tiles to Convert (Important!)

**Not all tiles need to be converted!** Tiles that are mostly or entirely sea (NoData) don't need STL files.

### Quick Check

```bash
python3 scripts/check_tiles_for_stl.py
```

This will:
- Check all tiles for data content
- List which tiles to convert (have terrain data)
- List which tiles to skip (mostly sea/NoData)
- Save lists to `tiles_to_convert.txt` and `tiles_to_skip.txt`

**Only convert tiles that have terrain data!** This saves hours of processing time.

## Step-by-Step Instructions

### Step 1: Load a Tile

1. **Add Raster Layer:**
   - **Layer** → **Add Layer** → **Add Raster Layer**
   - Navigate to `data/processed/tiles/`
   - Select one tile (start with `tile_01_01.tif` for testing)
   - Click **Open**

2. **Select the tile layer** in the Layers panel
   - Click on the tile layer to make it active

### Step 2: Open DEMto3D Plugin

1. Go to the menu: **Raster** → **DEMto3D** → **DEM 3D Printing**
   - If you don't see this menu, make sure DEMto3D plugin is installed and enabled

2. The **DEM 3D Printing** dialog will open

### Step 3: Configure Input Settings

**Input DEM:**
- Should automatically show your selected layer (`merged_full_area`)
- If not, select it from the dropdown

### Step 4: Set Layer Extent

**Important:** Before setting model dimensions, set the layer extent:

1. In the **Layer extent** section
2. Click the **leftmost magnifying glass** button (square with outward arrows)
   - This automatically sets the extent from your tile layer
   - The X and Y fields should fill automatically

### Step 5: Set Model Dimensions

**For Each Tile:**
- **Model width**: `330` mm
- **Model height (length)**: `330` mm
  - This creates a tile that fits on Prusa XL bed (360mm × 360mm)

### Step 5: Fill Layer Extent (Important!)

**If X and Y fields are empty:**
1. Click the **zoom/action buttons** next to "Show width/length" (the three small square buttons)
2. Or click **"Show width/length"** checkbox - this may auto-fill the extent
3. The plugin should automatically detect the layer extent

**If it still doesn't fill:**
- The X and Y fields show the geographic extent
- You can leave them empty if the layer is already selected
- The plugin should use the full layer extent automatically

### Step 6: Configure Model Settings

**Model size spacing:**
- Should show: `0.2` mm (recommended for good detail)
  - Or change to `0.3` mm for faster processing and smaller file
  - Start with 0.2mm for your first test

**Model width:**
- Enter: `330` mm

**Model height (length):**
- Enter: `330` mm

**Vertical exaggeration:**
- Enter: `6.0` (in the spinbox)

### Step 7: Configure Model Height (Critical!)

**Height (m):**
- **This field MUST be filled!** Enter: `-2.18`
  - This is your minimum elevation from the layer statistics
  - Sets the base of your 3D model
  - **If this is empty, you'll get the "Fill the data correctly" error**

**After entering -2.18:**
- The plugin should update:
  - Lowest point: should show a value
  - Highest point: should show ~1523m
  - Model height: should calculate automatically

**Base height (mm):**
- Leave as `2.00` or set to `0` (we'll add base in PrusaSlicer)

### Step 8: Configure Output

**Output file:**
- Click the **"..."** button to browse
- Navigate to your desired output directory (e.g., `output/` or `data/processed/`)
- Enter a filename, for example:
  - `test_tile_0.2mm_6x.stl` (for test tile)
  - `full_map_6x.stl` (for full map)
- Click **Save**

**Format:**
- Select **STL Binary** (recommended - smaller file size)
- Or **STL ASCII** (larger but human-readable)

### Step 9: Generate STL

1. **Review all settings:**
   - Input DEM: `merged_full_area` ✓
   - Model width: `330` mm ✓
   - Model height: `330` mm ✓
   - Model size spacing: `0.2` mm ✓
   - Model height: `-2.18` ✓
   - Vertical exaggeration: `6.0` ✓
   - Output file: [your chosen path] ✓

2. **Click OK**

3. **Wait for processing:**
   - Progress will be shown in the **Processing Toolbox** panel
   - For a 330mm x 330mm tile: 5-15 minutes
   - For full 2m x 1.5m map: 30-60+ minutes
   - **Don't close QGIS** during processing!

### Step 10: Verify Your STL

1. **Check the output file:**
   - Navigate to your output directory
   - Verify the `.stl` file was created
   - Check file size (should be 50-200MB for a tile)

2. **Open in a 3D viewer (optional):**
   - Use MeshLab, Blender, or your 3D printer slicer
   - Verify the model looks correct
   - Check dimensions

## Complete Settings Summary

For each tile, use these exact settings:

```
Input DEM: tile_XX_YY.tif (your tile)
Layer extent: Click leftmost magnifying glass (auto-set)
Model width: 330 mm
Model height (length): 330 mm
Model size spacing: 0.2 mm
Height (m): -2.18 ⚠️ REQUIRED
Base height (mm): 0 ⚠️ REQUIRED
Vertical exaggeration: 6.0x
Output format: STL Binary
Output file: output/tile_XX_YY.stl (match tile name)
```

## Processing All 30 Tiles

After testing 1-2 tiles:

1. **Process in batches**: 5-10 tiles at a time
2. **Use consistent settings** for all tiles
3. **Name systematically**: `tile_01_01.stl`, `tile_01_02.stl`, etc.
4. **Take breaks** between batches (each tile takes 5-15 minutes)
5. **Total time**: 2.5-7.5 hours for all 30 tiles

## What Happens Next

After generating your STL files:

1. **Test First Tile:**
   - Open `tile_01_01.stl` in PrusaSlicer
   - Add 20mm base (see [Adding a Base](ADDING_BASE.md))
   - Configure print settings (see [Prusa XL Settings](PRUSA_XL_SETTINGS.md))
   - Print test tile to verify quality

2. **If Test Looks Good:**
   - Process remaining 29 tiles
   - Use same settings for all
   - Process in batches of 5-10 tiles

3. **After All STLs Created:**
   - Add 20mm base to each in PrusaSlicer
   - Print all 30 tiles
   - Assemble into your 2m × 1.5m terrain model

## Troubleshooting

### Plugin Not Appearing
- Check plugin is installed: **Plugins** → **Manage and Install Plugins** → **Installed**
- Make sure DEMto3D is checked/enabled
- Restart QGIS

### Processing Takes Too Long
- This is normal for large areas
- Reduce model size spacing to 0.3mm for faster processing
- Process smaller test areas first

### STL File Too Large
- Increase model size spacing (0.3mm or 0.5mm)
- Use binary STL format
- Process smaller area

### Error Messages
- Check that DEM layer is selected
- Verify DEM has valid data (check Statistics tab)
- Ensure output directory is writable

## Next Steps

- **[Adding a Base](ADDING_BASE.md)** - Add 20mm base in PrusaSlicer
- **[Prusa XL Settings](PRUSA_XL_SETTINGS.md)** - Configure print settings
- **[Test Tiles Guide](TEST_TILES_GUIDE.md)** - Create comparison test tiles

---

**Ready?** Follow the steps above to create your first STL file!
