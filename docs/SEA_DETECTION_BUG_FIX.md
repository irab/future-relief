# Sea Detection Bug Fix

## The Problem

The sea detection had two bugs:

1. **Old sea mask:** Created with 5m threshold (before fix), marking almost everything as sea
2. **Wrong formula:** `A * (1 - B)` sets sea areas to 0 instead of NoData

## The Bugs

### Bug 1: Old Sea Mask

The sea mask was created with the old 5m threshold, which marked almost all areas as sea (all values = 1).

**Fix:** Delete old sea mask and re-create with < 0m threshold.

### Bug 2: Wrong Formula

**Old formula:** `A * (1 - B)`
- When B=1 (sea): `A * 0 = 0` (sets to 0, not NoData!)
- When B=0 (land): `A * 1 = A` (correct)

**Problem:** Sea areas become 0 (treated as valid elevation), not NoData.

**New formula:** `numpy.where(B == 1, -9999, A)`
- When B=1 (sea): Sets to -9999 (NoData)
- When B=0 (land): Keeps elevation A

## Solution

### Step 1: Delete Old Files

```bash
cd /home/x/repos/future-relief

# Delete old sea detection outputs
rm data/processed/sea_mask.tif
rm data/processed/flat_sea_mask.tif
rm data/processed/merged_full_area_no_sea.tif

# Delete old empty tiles
rm data/processed/tiles/tile_*.tif
```

### Step 2: Re-run Pipeline

```bash
# Re-run with fixed code
python3 scripts/complete_pipeline.py
```

This will:
- Create new sea mask with < 0m threshold (only actual sea)
- Use fixed formula (sets sea to NoData, not 0)
- Create tiles with proper elevation data

## Verification

After re-running, check:

```bash
# Check sea mask (should have mix of 0s and 1s, not all 1s)
gdalinfo -stats data/processed/sea_mask.tif | grep STATISTICS

# Check DEM without sea (should have elevation data, not all zeros)
gdalinfo -stats data/processed/merged_full_area_no_sea.tif | grep STATISTICS

# Check tiles (should have elevation data)
gdalinfo -stats data/processed/tiles/tile_01_01.tif | grep STATISTICS
```

**Should show:**
- Sea mask: Mix of 0s (land) and 1s (sea)
- DEM without sea: Min/Max elevation values (not all zeros)
- Tiles: Min/Max elevation values (not all zeros)

## What Changed

**Scripts updated:**
- `scripts/complete_pipeline.py` - Fixed formula
- `scripts/detect_flat_sea.py` - Fixed formula

**Formula change:**
- Old: `A * (1 - B)` → Sets sea to 0 (wrong)
- New: `numpy.where(B == 1, -9999, A)` → Sets sea to NoData (correct)

## Summary

**Problem:** Tiles have no elevation data (all zeros)

**Root cause:**
1. Old sea mask marked everything as sea (5m threshold)
2. Formula set sea to 0 instead of NoData

**Fix:**
1. Delete old sea detection outputs
2. Re-run pipeline with fixed code
3. New tiles will have proper elevation data
