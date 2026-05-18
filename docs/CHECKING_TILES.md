# Checking Which Tiles to Convert to STL

Not all tiles need to be converted to STL! Tiles that are mostly or entirely sea (NoData) don't need STL files and would waste processing time.

## Why Check Tiles?

After running the pipeline with sea detection:
- Some tiles will be **mostly sea** (NoData) - don't convert these!
- Some tiles will be **mostly land** (terrain data) - convert these!
- Some tiles will be **coastal** (mix of sea and land) - convert these!

**Example:** If you have 56 tiles but 20 are mostly sea, you only need to convert 36 tiles - saving 3-5 hours of processing time!

## Quick Check

### Step 1: Run the Check Script

```bash
cd /home/x/repos/future-relief
python3 scripts/check_tiles_for_stl.py
```

### Step 2: Review Results

The script will show:
- ✓ **CONVERT** - Tiles with enough terrain data
- ✗ **SKIP** - Tiles that are mostly sea/NoData

Example output:
```
✓ CONVERT    tile_01_01.tif      - 85.3% valid data
✓ CONVERT    tile_01_02.tif      - 92.1% valid data
✗ SKIP       tile_01_03.tif      - 2.1% valid data
✓ CONVERT    tile_01_04.tif      - 78.5% valid data
...
```

### Step 3: Use the Lists

The script creates two files:
- `tiles_to_convert.txt` - List of tiles to convert
- `tiles_to_skip.txt` - List of tiles to skip

## Customizing the Threshold

By default, tiles with less than 10% valid data are skipped. To change this:

```bash
# Skip tiles with less than 5% data
python3 scripts/check_tiles_for_stl.py --min-data 5.0

# Only convert tiles with at least 20% data
python3 scripts/check_tiles_for_stl.py --min-data 20.0
```

## Manual Check in QGIS

If you prefer to check manually:

1. **Load a tile in QGIS:**
   - Layer → Add Layer → Add Raster Layer
   - Select a tile (e.g., `tile_01_03.tif`)

2. **Check for data:**
   - Right-click layer → Properties → Information
   - Look for "NoData Value" and statistics
   - If mostly NoData → Skip this tile
   - If has elevation data → Convert this tile

3. **Visual check:**
   - If the tile looks mostly black/empty → Skip
   - If the tile shows terrain → Convert

## What Happens to Skipped Tiles?

**Skipped tiles (mostly sea):**
- Don't create STL files for these
- They would just be flat/empty anyway
- Saves processing time and disk space

**Converted tiles (have terrain):**
- Create STL files using DEMto3D
- These are the interesting parts to print!

## Integration with STL Conversion

When converting tiles to STL:

1. **Check tiles first:**
   ```bash
   python3 scripts/check_tiles_for_stl.py
   ```

2. **Only convert tiles from the list:**
   - Use `tiles_to_convert.txt` as reference
   - Skip tiles in `tiles_to_skip.txt`

3. **Save time:**
   - Don't waste 5-15 minutes per tile on sea-only tiles
   - Focus on tiles with actual terrain!

## Example Workflow

```bash
# 1. Check which tiles to convert
python3 scripts/check_tiles_for_stl.py

# 2. Review the output
# Let's say it shows 36 tiles to convert, 20 to skip

# 3. Convert only the 36 tiles with terrain data
# (Use DEMto3D for each tile in tiles_to_convert.txt)

# 4. Result: Saved ~3-5 hours by skipping sea-only tiles!
```

## Troubleshooting

### Script Can't Read Tiles

**Error:** `Error reading tile` or `gdalinfo not found`

**Solution:**
```bash
# Install GDAL if missing
sudo apt-get install gdal-bin
```

### All Tiles Show as "Skip"

**Problem:** All tiles are being skipped even though they have data

**Solution:**
- Lower the threshold: `--min-data 1.0`
- Check if sea detection was too aggressive
- Verify tiles actually have data in QGIS

### Tiles Show as "Convert" But Are Empty

**Problem:** Script says to convert but tile looks empty

**Solution:**
- Check the tile visually in QGIS
- The threshold might be too low
- Manually skip tiles that look empty

## Summary

**Always check tiles before converting to STL!**
- Saves hours of processing time
- Focuses on interesting terrain
- Avoids creating empty STL files

The check script makes this easy - just run it and follow the lists!
