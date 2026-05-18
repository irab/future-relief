# Running the Complete Pipeline from Terminal

Quick guide to run the pipeline on your merged TIF file.

## Quick Start

### Basic Usage (Uses Default File)

```bash
cd /home/x/repos/future-relief
python3 scripts/complete_pipeline.py
```

This will use the default merged TIF file: `data/processed/merged_full_area.tif`

### Specify Custom Input File

```bash
python3 scripts/complete_pipeline.py /path/to/your/merged.tif
```

## Common Options

### Skip Sea Detection

If you want to print all areas including flat sea:

```bash
python3 scripts/complete_pipeline.py --skip-sea-detection
```

### Adjust Sea Level Threshold

Change the maximum elevation considered as sea (default is 5m):

```bash
# Lower threshold (3m instead of 5m)
python3 scripts/complete_pipeline.py --sea-level 3.0

# Higher threshold (10m)
python3 scripts/complete_pipeline.py --sea-level 10.0
```

### Custom Output Directory

```bash
python3 scripts/complete_pipeline.py --output-dir /path/to/output
```

## Full Example

```bash
# Navigate to project directory
cd /home/x/repos/future-relief

# Run pipeline with custom sea level
python3 scripts/complete_pipeline.py data/processed/merged_full_area.tif --sea-level 3.0
```

## What to Expect

The script will:

1. **Check GDAL installation** - Verifies GDAL tools are available
2. **Detect flat sea** (if not skipped):
   - Creates sea mask
   - Creates DEM without sea areas
   - Takes 5-15 minutes
3. **Create square tiles**:
   - Calculates tile grid
   - Clips DEM into tiles
   - Takes 30-90 minutes
   - Shows progress for each tile

**Total time: 35-105 minutes** (mostly automated)

## Output

After completion, you'll find:

```
data/processed/
├── sea_mask.tif
├── flat_sea_mask.tif
├── merged_full_area_no_sea.tif
└── tiles/
    ├── tile_01_01.tif
    ├── tile_01_02.tif
    └── ... (all tiles)
```

## Troubleshooting

### GDAL Not Found

**Error:** `gdal_calc.py: command not found`

**Solution:**
```bash
sudo apt-get install gdal-bin python3-gdal
```

### Permission Denied

**Error:** `Permission denied` when writing files

**Solution:**
```bash
# Check directory permissions
ls -ld data/processed/

# Fix if needed
chmod 755 data/processed/
```

### Script Not Found

**Error:** `python3: can't open file 'scripts/complete_pipeline.py'`

**Solution:**
```bash
# Make sure you're in the project directory
cd /home/x/repos/future-relief

# Verify script exists
ls -l scripts/complete_pipeline.py
```

## Running in Background

For long-running processes, you can run in background:

```bash
# Run in background and save output to log
nohup python3 scripts/complete_pipeline.py > pipeline.log 2>&1 &

# Check progress
tail -f pipeline.log

# Check if still running
ps aux | grep complete_pipeline
```

## Next Steps

After the pipeline completes:

1. **Review tiles in QGIS** to verify they look correct
2. **Convert to STL** using DEMto3D (see [First STL Guide](FIRST_STL_GUIDE.md))
3. **Print and assemble** your terrain model!
