# Automating Tile Creation

Guide to automatically create multiple tiles from your merged DEM.

## Overview

Instead of manually clipping and converting each tile, you can automate the process using Python scripts in QGIS.

## Method 1: Using QGIS Python Console (Easiest)

### Step 1: Open Python Console

1. In QGIS, go to **Plugins** → **Python Console**
   - Or press `Ctrl+Alt+P`

### Step 2: Run the Script

1. Open the script: `scripts/run_tile_creation.py`
2. **Copy the entire script**
3. **Paste it into the QGIS Python Console**
4. **Update the configuration** at the top:
   ```python
   RASTER_PATH = "/home/x/repos/future-relief/data/processed/merged_full_area.tif"
   OUTPUT_DIR = "/home/x/repos/future-relief/data/processed/tiles"
   ROWS = 5
   COLS = 6
   ```
5. **Press Enter** to run

### Step 3: Wait for Processing

The script will:
- Create a grid (6 columns × 5 rows = 30 cells)
- Clip your merged DEM to each grid cell
- Save each as `tile_01_01.tif`, `tile_01_02.tif`, etc.
- Show progress in the console

### Step 4: Convert to STL

After the script finishes, you'll have 30 clipped raster tiles. Then:

**Option A: Manual Conversion (Recommended for First Time)**
- Convert 1-2 tiles manually using DEMto3D to verify settings
- Then convert the rest

**Option B: Batch Conversion**
- Use the batch conversion script (see below)

## Method 2: Standalone Python Script

### Run from Terminal

```bash
cd /home/x/repos/future-relief
python3 scripts/create_tiles_automated.py
```

**Note:** This requires QGIS Python environment. Better to use Method 1 (Python Console).

## Method 3: QGIS Processing Model

Create a graphical model in QGIS:

1. **Processing** → **Graphical Modeler**
2. **Create new model**
3. **Add algorithms:**
   - Create Grid
   - Extract by Attribute (to iterate through cells)
   - Clip Raster by Mask Layer
   - (DEMto3D if available as processing algorithm)
4. **Save and run** the model

## Batch STL Conversion

After creating clipped tiles, you can batch convert them to STL:

### Using QGIS Processing Batch Mode

1. **Processing** → **Toolbox**
2. Search for "DEMto3D" or "DEM 3D Printing"
3. **Right-click** → **Execute as Batch Process**
4. **Add all your tile files** as inputs
5. **Configure settings** for each (or use same for all)
6. **Run batch**

### Manual Batch (If Batch Mode Not Available)

Since DEMto3D might not support batch processing directly, you'll need to:

1. **Process tiles in groups** (5-10 at a time)
2. **Use consistent settings** for all
3. **Name systematically**: `tile_01_01.stl`, `tile_01_02.stl`, etc.

## Script Configuration

### Adjust Grid Size

In the script, change:
```python
ROWS = 5   # Number of vertical tiles
COLS = 6   # Number of horizontal tiles
```

### Adjust Output Paths

```python
RASTER_PATH = "/path/to/your/merged_full_area.tif"
OUTPUT_DIR = "/path/to/output/tiles"
```

## Troubleshooting

### Script Fails to Load Raster

- Check the path is correct
- Ensure raster layer is valid
- Try loading the raster in QGIS first, then use the layer name instead of path

### Grid Not Created

- Check CRS matches your raster
- Verify extent is correct
- Check output directory is writable

### Clipping Fails

- Ensure you have enough disk space
- Check raster is not corrupted
- Verify grid cells are valid

## Time Savings

**Manual process:**
- Creating grid: 5 minutes
- Clipping 30 tiles: 60-90 minutes
- Converting to STL: 2.5-7.5 hours
- **Total: 4-9 hours**

**Automated process:**
- Running script: 2 minutes
- Script processing: 30-60 minutes (automated)
- Converting to STL: 2.5-7.5 hours (still manual or semi-automated)
- **Total: 3-8 hours** (saves 1 hour, but much less manual work!)

## Next Steps

After automated tile creation:
1. Verify a few tiles look correct
2. Convert to STL (manually or batch)
3. Print test tiles
4. Print all tiles and assemble

## Advanced: Full Automation

For complete automation including STL conversion, you would need to:
1. Use QGIS Processing API to call DEMto3D
2. Or use GDAL/other tools to convert DEM to STL
3. Or create a custom QGIS plugin

This is more complex and may not be worth it unless you're doing this frequently.
