# Validating Tiles Have Elevation Data

Guide to check that your tiles contain actual elevation data (not all zeros or empty).

## Why Validate?

After creating tiles, you should verify they have elevation data:
- **Empty tiles** (all zeros) won't create useful STL files
- **Early detection** saves time before STL conversion
- **Catches issues** with sea detection or source data

## Automatic Validation

The complete pipeline now **automatically validates tiles** after creation:

```bash
python3 scripts/complete_pipeline.py
```

**Output includes:**
```
  Validating tiles have elevation data...
  --------------------------------------------------------
  ✓ tile_01_01.tif: Elevation range -2.18m to 1523.08m
  ✓ tile_01_02.tif: Elevation range -1.95m to 1245.32m
  ✗ tile_01_03.tif: No elevation data (Min=0.00, Max=0.00)
  ...
  ========================================================
  Validation: 45 valid, 11 empty
```

## Manual Validation

### Standalone Script

```bash
python3 scripts/validate_tiles.py
```

**Output:**
- Lists all tiles
- Shows which have elevation data
- Reports empty tiles
- Saves lists to files

### What It Checks

1. **Elevation range:** Min and max elevation values
2. **Variation:** Ensures elevation changes (not all same value)
3. **Not all zeros:** Catches tiles with no data

### Example Output

```
============================================================
Validating Tiles Have Elevation Data
============================================================

Tiles directory: data/processed/tiles
Minimum elevation range: 0.01m
Total tiles found: 56

============================================================
✓ VALID     tile_01_01.tif       - Elevation range: -2.18m to 1523.08m
✓ VALID     tile_01_02.tif       - Elevation range: -1.95m to 1245.32m
✗ EMPTY     tile_01_03.tif       - All zeros (no elevation data)
✓ VALID     tile_01_04.tif       - Elevation range: 0.15m to 856.42m
...

============================================================
Summary
============================================================
Valid tiles: 45
Empty tiles: 11
Error tiles: 0

✓ Valid tiles (have elevation data):
  - tile_01_01.tif: -2.18m to 1523.08m
  - tile_01_02.tif: -1.95m to 1245.32m
  ...

✗ Empty tiles (no elevation data):
  - tile_01_03.tif: Min=0.00, Max=0.00
  ...
  
  These tiles should be skipped for STL conversion!
```

## What Gets Saved

The validation script creates:

- **`tiles_valid.txt`** - List of tiles with elevation data
- **`tiles_empty.txt`** - List of tiles to skip (no data)

Use these lists when converting to STL:
- Only convert tiles from `tiles_valid.txt`
- Skip tiles from `tiles_empty.txt`

## Integration with Pipeline

The pipeline now validates automatically:

1. **Creates tiles**
2. **Validates each tile** for elevation data
3. **Reports results** immediately
4. **Warns if issues** found

**If all tiles are empty:**
- Pipeline will warn you
- Suggests checking source DEM
- Recommends re-running with `--skip-sea-detection`

## Quick Check in QGIS

You can also check manually in QGIS:

1. **Load a tile:**
   - Layer → Add Layer → Add Raster Layer
   - Select a tile

2. **Check properties:**
   - Right-click → Properties → Information
   - Look for Min/Max elevation
   - If both are 0, tile is empty

3. **Visual check:**
   - Switch to Hillshade view
   - If completely flat/black, tile has no data

## Common Issues

### All Tiles Empty

**Symptom:** All tiles show Min=0, Max=0

**Causes:**
1. Source DEM is empty/corrupted
2. Sea detection removed all data
3. Tiles created from wrong file

**Fix:**
```bash
# Check source DEM
gdalinfo -stats data/processed/merged_full_area.tif | grep STATISTICS

# If source is good, re-run without sea detection
python3 scripts/complete_pipeline.py --skip-sea-detection
```

### Some Tiles Empty

**Symptom:** Some tiles empty, others have data

**Causes:**
1. Those areas are actually sea (below 0m)
2. Source DEM has no data in those areas
3. Normal - some tiles will be empty

**Fix:**
- This is normal if sea detection is working
- Just skip empty tiles for STL conversion
- Use `tiles_empty.txt` list

### Validation Errors

**Symptom:** "Error reading tile" or "Timeout"

**Causes:**
1. Corrupted tile file
2. File permissions issue
3. GDAL not installed

**Fix:**
```bash
# Check GDAL
gdalinfo --version

# Check file permissions
ls -l data/processed/tiles/tile_*.tif

# Try reading manually
gdalinfo data/processed/tiles/tile_01_01.tif
```

## Customizing Validation

### Change Minimum Range

```bash
# Only consider tiles valid if elevation range > 1m
python3 scripts/validate_tiles.py --min-range 1.0
```

### Check Specific Directory

```bash
python3 scripts/validate_tiles.py /path/to/tiles
```

## Summary

**Always validate tiles after creation!**

- ✅ Pipeline validates automatically
- ✅ Manual validation: `python3 scripts/validate_tiles.py`
- ✅ Check in QGIS for visual confirmation
- ✅ Use validation lists to skip empty tiles

**Empty tiles are normal** if:
- They're mostly sea (below 0m)
- Source DEM has no data there
- Just skip them for STL conversion!
