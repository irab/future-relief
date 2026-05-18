# Complete Pipeline: Merged TIF to Print-Ready Tiles

This guide covers the automated pipeline that processes a merged TIF file into print-ready square tiles, including flat sea detection.

## Overview

The complete pipeline automates:
1. **Detecting flat sea areas** - Identifies and excludes flat sea from printing
2. **Creating square tiles** - Splits DEM into square tiles for 3D printing
3. **Preparing for STL conversion** - Tiles ready for DEMto3D

## Quick Start

### Option 1: Run Standalone (Recommended)

```bash
# Use default input file
python3 scripts/complete_pipeline.py

# Or specify custom input
python3 scripts/complete_pipeline.py /path/to/merged.tif

# Skip sea detection (if you don't want to exclude sea)
python3 scripts/complete_pipeline.py --skip-sea-detection

# Custom sea level threshold
python3 scripts/complete_pipeline.py --sea-level 3.0
```

### Option 2: Run from QGIS Python Console

1. **Open QGIS Python Console**
   - **Plugins** → **Python Console** (or press `Ctrl+Alt+P`)

2. **Run the pipeline:**
   ```python
   exec(open('/home/x/repos/future-relief/scripts/complete_pipeline.py').read())
   ```

## Pipeline Steps

### Step 1: Detect Flat Sea Areas (Optional)

**What it does:**
- Identifies areas with elevation < 0m (below sea level only)
- Creates a mask of sea areas
- Generates a DEM with sea areas set to NoData
- Preserves all land areas including beaches and low-lying areas

**Output:**
- `sea_mask.tif` - Mask showing sea areas
- `flat_sea_mask.tif` - Combined mask
- `merged_full_area_no_sea.tif` - DEM with sea removed

**Skip this step:**
- Use `--skip-sea-detection` flag
- Or if you want to print all areas including sea

### Step 2: Create Square Tiles

**What it does:**
- Calculates square tile size based on print dimensions
- Creates a grid of square tiles (330mm × 330mm)
- Clips DEM into individual tile files
- **Validates tiles have elevation data** (new!)

**Output:**
- `tiles/tile_01_01.tif` through `tile_XX_YY.tif`
- All tiles are square in geographic space
- **Validation report** showing which tiles have data
- Ready for STL conversion

**Validation:**
- Automatically checks each tile for elevation data
- Warns if tiles are empty (all zeros)
- Lists valid vs empty tiles
- Helps catch issues early

## Command Line Options

```bash
python3 scripts/complete_pipeline.py [input] [options]
```

**Arguments:**
- `input` - Path to merged TIF file (optional, uses default if not specified)

**Options:**
- `--output-dir DIR` - Output directory (default: `data/processed`)
- `--skip-sea-detection` - Skip flat sea detection step
- `--sea-level FLOAT` - Maximum elevation for sea detection in meters (default: 0.0 - only excludes below sea level)
- `--tile-size INT` - Tile size in mm (default: 330)
- `--print-width INT` - Full print width in mm (default: 2000)

**Examples:**

```bash
# Basic usage with defaults
python3 scripts/complete_pipeline.py

# Custom input file
python3 scripts/complete_pipeline.py /path/to/my_merged.tif

# Skip sea detection
python3 scripts/complete_pipeline.py --skip-sea-detection

# Lower sea level threshold (3m instead of 5m)
python3 scripts/complete_pipeline.py --sea-level 3.0

# Custom tile size and print width
python3 scripts/complete_pipeline.py --tile-size 300 --print-width 1800
```

## Output Structure

After running the pipeline:

```
data/processed/
├── sea_mask.tif              # Sea level mask
├── flat_sea_mask.tif         # Flat sea mask
├── merged_full_area_no_sea.tif  # DEM without sea (if sea detection enabled)
└── tiles/
    ├── tile_01_01.tif
    ├── tile_01_02.tif
    ├── ...
    └── tile_XX_YY.tif
```

## What Happens to Existing Files

- **Sea detection outputs**: Will be overwritten if they exist (you'll be prompted)
- **Tiles**: Will ask before overwriting existing tiles
- **Input file**: Never modified

## Time Estimates

- **Sea detection**: 5-15 minutes (depending on DEM size)
- **Tile creation**: 30-90 minutes (depending on number of tiles)
- **Total**: 35-105 minutes for complete pipeline

## Validation

After tile creation, the pipeline automatically validates tiles:

- **Checks elevation data:** Ensures tiles have actual elevation values (not all zeros)
- **Reports empty tiles:** Lists tiles with no data
- **Warns if issues found:** Stops if all tiles are empty

**Manual validation:**
```bash
python3 scripts/validate_tiles.py
```

This will:
- Check all tiles for elevation data
- Report which tiles are valid vs empty
- Save lists to `tiles_valid.txt` and `tiles_empty.txt`

## Troubleshooting

### All Tiles Are Empty (No Elevation Data)

**Error:** Validation shows all tiles have Min=0, Max=0

**Cause:** Tiles created from corrupted or empty source DEM

**Solution:**
```bash
# Delete old tiles
rm data/processed/tiles/tile_*.tif

# Re-run without sea detection (uses original DEM)
python3 scripts/complete_pipeline.py --skip-sea-detection

# Or check source DEM
gdalinfo -stats data/processed/merged_full_area.tif | grep STATISTICS
```

### GDAL Not Found

**Error:** `gdal_calc.py not found` or `gdalinfo: command not found`

**Solution:**
```bash
sudo apt-get install gdal-bin python3-gdal
```

### Permission Denied

**Error:** `Permission denied` when writing files

**Solution:**
- Check output directory permissions
- Ensure you have write access to `data/processed/`

### Out of Memory

**Error:** Process killed or system becomes unresponsive

**Solution:**
- Close other applications
- Process in smaller batches (modify script to process fewer tiles at once)
- Increase system swap space

### Tiles Not Square

**Issue:** Tiles appear rectangular in QGIS

**Solution:**
- Check that tile creation completed successfully
- Verify input DEM extent is correct
- Re-run tile creation step

## Integration with Other Workflows

### After Pipeline Completion

1. **Review tiles in QGIS:**
   - Load a few tiles to verify they look correct
   - Check that sea areas are excluded (if sea detection was used)

2. **Convert to STL:**
   - Use DEMto3D plugin for each tile
   - See [First STL Guide](FIRST_STL_GUIDE.md) for detailed steps

3. **Print settings:**
   - See [Prusa XL Settings](PRUSA_XL_SETTINGS.md) for print configuration

### Customizing the Pipeline

To modify the pipeline:

1. **Edit the script:**
   ```bash
   nano scripts/complete_pipeline.py
   ```

2. **Key parameters to adjust:**
   - `SEA_LEVEL_MAX` - Sea detection threshold
   - `TARGET_TILE_SIZE_MM` - Tile size
   - `TARGET_PRINT_WIDTH_MM` - Full map width

3. **Or use command-line options** (no script editing needed)

## Comparison: Manual vs Pipeline

### Manual Workflow
- Detect sea: ~15 minutes
- Create tiles: ~60 minutes
- **Total: ~75 minutes** + manual steps

### Automated Pipeline
- Run script: ~45-90 minutes
- **Total: ~45-90 minutes** (mostly automated)

**Benefits:**
- ✅ Consistent results
- ✅ Less error-prone
- ✅ Reproducible
- ✅ Can be re-run easily

## Next Steps

After running the pipeline:

1. **[Convert Tiles to STL](FIRST_STL_GUIDE.md)** - Convert each tile to STL format
2. **[Add Base in PrusaSlicer](ADDING_BASE.md)** - Add 20mm base to prints
3. **[Configure Print Settings](PRUSA_XL_SETTINGS.md)** - Optimize for Prusa XL
4. **Print and assemble** your terrain model!

## Advanced Usage

### Processing Specific Regions

To process only part of the DEM:

1. Clip the merged DEM to your region first:
   ```bash
   gdalwarp -te xmin ymin xmax ymax input.tif clipped.tif
   ```

2. Run pipeline on clipped file:
   ```bash
   python3 scripts/complete_pipeline.py clipped.tif
   ```

### Batch Processing Multiple Regions

Create a script to process multiple regions:

```bash
#!/bin/bash
for region in region1.tif region2.tif region3.tif; do
    python3 scripts/complete_pipeline.py "$region" --output-dir "output_$(basename $region .tif)"
done
```

## See Also

- **[Detecting Flat Sea](DETECTING_FLAT_SEA.md)** - Detailed sea detection guide
- **[Creating Tiles](CREATING_TILES.md)** - Manual tile creation guide
- **[Square Tiles](SQUARE_TILES.md)** - Square tile creation guide
- **[First STL Guide](FIRST_STL_GUIDE.md)** - Converting tiles to STL
