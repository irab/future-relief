# Detecting and Excluding Flat Sea Areas

Large areas of flat sea don't need to be printed - they're just flat surfaces with no detail. This guide shows how to detect and exclude these areas to save printing time and material.

## Why Exclude Flat Sea?

- **Saves material**: No need to print flat areas
- **Saves time**: Fewer tiles to print
- **Better focus**: Only print areas with terrain detail
- **Easier assembly**: Fewer pieces to assemble

## Method: Detect Below Sea Level

Sea areas are identified by:
1. **Below sea level**: Elevation < 0m (actual sea/water)
2. This preserves beaches, coastlines, and low-lying areas (0m and above)

## Automated Detection Script

A script is available to automatically detect flat sea areas:

### Step 1: Run Detection Script

1. **Open QGIS Python Console**
   - **Plugins** → **Python Console** (or press `Ctrl+Alt+P`)

2. **Run the detection script:**
   ```python
   exec(open('/home/x/repos/future-relief/scripts/detect_flat_sea.py').read())
   ```

3. **The script will:**
   - Create a sea level mask (elevation < 0m - below sea level only)
   - Create a DEM with sea areas set to NoData
   - Preserves all land areas including beaches and low-lying areas

### Step 2: Review Results

1. **Load the flat sea mask in QGIS:**
   - **Layer** → **Add Layer** → **Add Raster Layer**
   - Navigate to `data/processed/flat_sea_mask.tif`
   - This shows areas that will be excluded (white = sea, black = land)

2. **Verify it looks correct:**
   - Check that sea areas are identified correctly
   - Ensure no land areas are incorrectly marked as sea
   - Adjust thresholds if needed (see below)

### Step 3: Use DEM Without Sea

1. **Use the new DEM for tile creation:**
   - Use `merged_full_area_no_sea.tif` instead of `merged_full_area.tif`
   - Update the tile creation script to use this file
   - Tiles will automatically skip flat sea areas

2. **Create tiles as normal:**
   - Run your tile creation script
   - Tiles will only cover areas with terrain detail
   - Sea areas will be NoData (not printed)

## Adjusting Detection Parameters

If the detection isn't accurate, adjust these parameters in the script:

### `SEA_LEVEL_MAX = 0.0`
- Maximum elevation to consider as sea (meters)
- Default: 0.0m (only excludes below sea level)
- This preserves beaches, coastlines, and all land areas
- Only actual sea/water areas (below 0m) are excluded

### `VARIATION_THRESHOLD = 0.5`
- Maximum elevation variation for "flat" (meters)
- Default: 0.5m (very flat areas)
- Increase to exclude slightly hilly low areas
- Decrease to only exclude perfectly flat areas

## Manual Method (Alternative)

If you prefer manual control:

### Step 1: Create Sea Level Mask

1. **Raster Calculator:**
   - **Raster** → **Raster Calculator**
   - Expression: `"merged_dem@1" <= 5`
   - Output: `sea_mask.tif`
   - Click **OK**

### Step 2: Calculate Elevation Variation

1. **Focal Statistics:**
   - **Raster** → **Analysis** → **Focal Statistics**
   - Input: `merged_dem`
   - Statistic: **Standard Deviation**
   - Kernel size: 3×3
   - Output: `elevation_variation.tif`
   - Click **Run**

### Step 3: Combine Masks

1. **Raster Calculator:**
   - Expression: `("sea_mask@1" == 1) AND ("elevation_variation@1" <= 0.5)`
   - Output: `flat_sea_mask.tif`
   - Click **OK**

### Step 4: Apply to DEM

1. **Raster Calculator:**
   - Expression: `"merged_dem@1" * (1 - "flat_sea_mask@1")`
   - Output: `merged_full_area_no_sea.tif`
   - Click **OK**

## What Happens to Tiles?

When you create tiles from the DEM without sea:

- **Sea tiles**: Will be mostly or entirely NoData
- **Coastal tiles**: Will have sea areas as NoData, land areas printed
- **Land tiles**: Unchanged, printed normally

**In DEMto3D:**
- NoData areas are automatically excluded
- Only areas with elevation data are converted to STL
- Result: STL files skip flat sea areas

## Example: Before and After

**Before (with sea):**
- 48 tiles covering entire area
- Many tiles are mostly flat sea
- ~20-30% of print area is flat sea

**After (without sea):**
- ~35-40 tiles (only areas with detail)
- No flat sea areas printed
- Focus on terrain features only

## Tips

1. **Start conservative**: Use default thresholds first
2. **Review visually**: Always check the mask in QGIS
3. **Adjust gradually**: Small changes to thresholds
4. **Keep coastal detail**: Don't exclude too much near coast
5. **Test one tile**: Create one test tile to verify it looks good

## Troubleshooting

### Too Much Sea Excluded
- **Problem**: Land areas marked as sea
- **Solution**: Increase `SEA_LEVEL_MAX` or `VARIATION_THRESHOLD`

### Not Enough Sea Excluded
- **Problem**: Flat sea areas still being printed
- **Solution**: Decrease `SEA_LEVEL_MAX` or `VARIATION_THRESHOLD`

### Coastal Areas Missing
- **Problem**: Important coastal features excluded
- **Solution**: Increase `VARIATION_THRESHOLD` to allow slight variation

## Integration with Tile Creation

Update your tile creation script to use the DEM without sea:

```python
# In create_square_tiles.py or similar
RASTER_PATH = "/home/x/repos/future-relief/data/processed/merged_full_area_no_sea.tif"
```

Then create tiles as normal - they'll automatically skip flat sea areas!
