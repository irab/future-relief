# Fix: Tiles Have No Elevation Data (All Zeros)

If your tiles show all zeros (Min=0, Max=0) instead of elevation data, the tiles were likely created from the wrong source or the sea detection removed everything.

## The Problem

**What you're seeing:**
- Tiles show Min=0, Max=0
- No elevation variation
- Black/white binary appearance in QGIS

**What should be:**
- Min: -4.15m to -2.18m (varies by tile)
- Max: Up to 1523m (varies by tile)
- Elevation data visible

## Root Cause

The tiles were created from `merged_full_area_no_sea.tif` which may have:
1. All data removed by sea detection (unlikely with < 0m threshold)
2. Data corruption during sea detection process
3. Wrong input file used

## Solution: Re-create Tiles from Original DEM

### Option 1: Skip Sea Detection (Recommended First)

Re-run the pipeline but skip sea detection to use the original DEM:

```bash
cd /home/x/repos/future-relief
python3 scripts/complete_pipeline.py --skip-sea-detection
```

This will:
- Use `merged_full_area.tif` (original, has all data)
- Create tiles with full elevation data
- You can manually exclude sea areas later if needed

### Option 2: Re-run Sea Detection

If you want to keep sea detection, re-run it:

```bash
# Delete old sea detection outputs
rm data/processed/sea_mask.tif
rm data/processed/flat_sea_mask.tif
rm data/processed/merged_full_area_no_sea.tif

# Re-run pipeline (will use < 0m threshold now)
python3 scripts/complete_pipeline.py
```

### Option 3: Re-create Tiles from Original DEM

Manually re-create tiles from the original DEM:

```bash
# Update the script to use original DEM
# Edit scripts/complete_pipeline.py or create_tiles_simple.py
# Change: RASTER_PATH to use merged_full_area.tif instead

# Or use QGIS Python Console:
exec(open('/home/x/repos/future-relief/scripts/create_square_tiles.py').read())
# But first edit the script to use merged_full_area.tif
```

## Quick Fix: Use Original DEM

**Fastest solution:**

1. **Edit the tile creation script:**
   ```python
   # In scripts/create_square_tiles.py or complete_pipeline.py
   # Change:
   RASTER_PATH = "/home/x/repos/future-relief/data/processed/merged_full_area.tif"
   # Instead of:
   # RASTER_PATH = "/home/x/repos/future-relief/data/processed/merged_full_area_no_sea.tif"
   ```

2. **Re-run tile creation:**
   ```bash
   # Delete old tiles
   rm data/processed/tiles/tile_*.tif
   
   # Re-run (skip sea detection to use original)
   python3 scripts/complete_pipeline.py --skip-sea-detection
   ```

## Verify Tiles Have Data

After re-creating, check a tile:

```bash
gdalinfo -stats data/processed/tiles/tile_01_01.tif | grep STATISTICS
```

**Should show:**
- STATISTICS_MINIMUM: Negative or small positive value
- STATISTICS_MAXIMUM: Large positive value (hundreds of meters)

**Not:**
- STATISTICS_MINIMUM=0
- STATISTICS_MAXIMUM=0

## Why This Happened

The sea detection process (`merged_full_area_no_sea.tif`) may have:
1. **Removed too much:** Even with < 0m threshold, if the calculation was wrong
2. **Corrupted data:** The gdal_calc operation may have had issues
3. **Wrong input:** Tiles were created from wrong source file

## Prevention

**Always verify tiles have data after creation:**

```bash
# Quick check
python3 scripts/check_tiles_for_stl.py

# Or manually check one tile
gdalinfo -stats data/processed/tiles/tile_01_01.tif | grep STATISTICS
```

## Summary

**Problem:** Tiles show Min=0, Max=0 (no elevation data)

**Cause:** Tiles created from corrupted or empty `merged_full_area_no_sea.tif`

**Fix:** Re-create tiles from original `merged_full_area.tif`:
```bash
python3 scripts/complete_pipeline.py --skip-sea-detection
```

**Verify:** Check tile statistics show elevation range (not all zeros)
