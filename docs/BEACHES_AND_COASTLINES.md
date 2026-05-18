# Beaches and Coastlines in the Flat Sea Mask

Important considerations for ensuring beaches and coastlines are preserved when detecting flat sea areas.

## The Solution

The flat sea mask uses elevation < 0m to identify sea areas. This means:
- ✅ **Only actual sea/water** (below sea level) is excluded
- ✅ **All beaches and coastlines** (0m and above) are preserved
- ✅ **Low-lying areas** are preserved

## Good News: Beaches Should Be Preserved

### Why Beaches Are Different from Flat Sea

**Flat Sea:**
- Low elevation (≤ 5m)
- **Very flat** (no elevation variation)
- No terrain detail

**Beaches and Coastlines:**
- Low elevation (often 0-5m)
- **Have variation** (dunes, slopes, cliffs, etc.)
- **Have terrain detail** - this is what makes them interesting!

### Current Script Behavior

The script only excludes areas **below sea level** (< 0m):

- ✅ **All beaches** - Preserved (0m and above)
- ✅ **Coastal areas** - Preserved (0m and above)
- ✅ **Low-lying land** - Preserved (0m and above)
- ✅ **Dunes** - Preserved (above sea level)
- ✅ **Only actual sea** - Excluded (below 0m)

## How to Verify

### Step 1: Check the Mask Visually

1. **Load the flat sea mask in QGIS:**
   ```bash
   # After running the pipeline
   # In QGIS: Layer → Add Layer → Add Raster Layer
   # Load: data/processed/flat_sea_mask.tif
   ```

2. **Compare with original DEM:**
   - Load both `merged_full_area.tif` and `flat_sea_mask.tif`
   - Check coastal areas visually
   - White in mask = will be excluded
   - Black in mask = will be printed

3. **Look for:**
   - Are beaches marked as sea (white)? → Problem!
   - Are beaches marked as land (black)? → Good!
   - Are coastal features visible? → Good!

### Step 2: Adjust if Needed

The default setting (0m) should preserve all beaches. If you need to adjust:

**Option 1: Skip sea detection entirely**
```bash
# Print everything including sea
python3 scripts/complete_pipeline.py --skip-sea-detection
```

**Option 2: Manually edit the mask in QGIS**
- Load the mask
- Use raster calculator to manually adjust if needed
- Re-run tile creation

## Improving the Detection

### Ideal Approach: Check Both Elevation AND Variation

The ideal flat sea detection should check:
1. **Low elevation** (≤ 5m) **AND**
2. **Low variation** (standard deviation < 0.5m in a 3×3 window)

This would:
- ✅ Exclude flat sea (low elevation + flat)
- ✅ Preserve beaches (low elevation + variation)
- ✅ Preserve all terrain with detail

### Current Limitation

The current simplified script only checks elevation. For more precise detection:

1. **Use QGIS Focal Statistics manually:**
   - Calculate standard deviation
   - Combine with elevation mask
   - See [Detecting Flat Sea](DETECTING_FLAT_SEA.md) for manual method

2. **Or accept the trade-off:**
   - Some very flat beaches might be excluded
   - But most beaches with dunes/cliffs will be preserved

## Recommendations

### For Your New Zealand Coastline

New Zealand coastlines typically have:
- **Rocky shores** - Definitely preserved (higher elevation)
- **Sandy beaches with dunes** - Should be preserved (have variation)
- **Flat tidal areas** - Might be excluded (but these are often underwater anyway)

### Suggested Workflow

1. **Run pipeline with default settings** (5m threshold)
2. **Check the mask visually** in QGIS
3. **If beaches look good** → Proceed with tile creation
4. **If beaches are excluded** → Lower threshold to 3m and re-run
5. **If unsure** → Skip sea detection and print everything

## Example: Checking a Specific Area

```bash
# After running pipeline, check a coastal tile
gdalinfo data/processed/tiles/tile_01_01.tif

# Or load in QGIS and visually inspect
# Look for coastal features in the tile
```

## Summary

- **Most beaches will be preserved** because they have elevation variation
- **Very flat beaches might be excluded** - but these are less interesting anyway
- **Always check the mask visually** before proceeding
- **Adjust threshold if needed** - lower is more conservative
- **Coastal cliffs and dunes** - definitely preserved

The key is: **flat sea = boring, beaches = interesting**. The mask should exclude boring flat areas while preserving interesting coastal terrain.
