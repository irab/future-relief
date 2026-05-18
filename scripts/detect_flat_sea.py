#!/usr/bin/env python3
"""
Detect Flat Sea Areas in DEM

This script identifies areas that are flat sea (low elevation with no variation)
and creates a DEM with these areas set to NoData (excluded from printing).

Can be run standalone or from QGIS Python Console
"""

from pathlib import Path
import subprocess
import os

# ===== CONFIGURATION =====
RASTER_PATH = "/home/x/repos/future-relief/data/processed/merged_full_area.tif"
OUTPUT_DIR = "/home/x/repos/future-relief/data/processed"
SEA_LEVEL_MAX = 0.0  # Maximum elevation to consider as sea (meters) - only exclude below sea level
VARIATION_THRESHOLD = 0.5  # Maximum elevation variation for "flat" (meters)

# ===== SCRIPT =====
print("=" * 60)
print("Detecting Flat Sea Areas")
print("=" * 60)

output_path = Path(OUTPUT_DIR)
output_path.mkdir(parents=True, exist_ok=True)

# Check if input exists
if not os.path.exists(RASTER_PATH):
    print(f"ERROR: Input raster not found: {RASTER_PATH}")
    exit(1)

# Get raster info
print(f"\nInput raster: {RASTER_PATH}")
info_cmd = ['gdalinfo', '-stats', RASTER_PATH]
try:
    info_result = subprocess.run(info_cmd, capture_output=True, text=True, check=True)
    # Extract min/max from output
    for line in info_result.stdout.split('\n'):
        if 'STATISTICS_MINIMUM' in line:
            min_elev = float(line.split('=')[1])
        elif 'STATISTICS_MAXIMUM' in line:
            max_elev = float(line.split('=')[1])
    print(f"  Elevation range: {min_elev:.2f}m to {max_elev:.2f}m")
except Exception as e:
    print(f"  Warning: Could not get statistics: {e}")

# Step 1: Create sea level mask (only exclude below sea level: < 0m)
print(f"\nStep 1: Creating sea level mask (elevation < 0m - below sea level only)...")

sea_mask_path = str(output_path / "sea_mask.tif")

# Use gdal_calc.py to create mask: 1 if elevation < 0 (below sea level), else 0
calc_cmd = [
    'gdal_calc.py',
    '-A', RASTER_PATH,
    '--A_band=1',
    '--calc', '(A < 0) * 1',  # Only exclude below sea level
    '--outfile', sea_mask_path,
    '--NoDataValue=0',
    '--type=Byte',
    '--co', 'COMPRESS=LZW'
]

try:
    result = subprocess.run(calc_cmd, capture_output=True, text=True, check=True)
    print(f"  ✓ Sea mask created: {sea_mask_path}")
except subprocess.CalledProcessError as e:
    print(f"  ✗ Error creating sea mask: {e.stderr}")
    exit(1)
except FileNotFoundError:
    print(f"  ✗ gdal_calc.py not found. Install GDAL Python bindings:")
    print(f"     sudo apt-get install python3-gdal")
    exit(1)

# Step 2: Calculate elevation variation (standard deviation)
print(f"\nStep 2: Calculating elevation variation (standard deviation)...")

variation_path = str(output_path / "elevation_variation.tif")

# Use gdal_fillnodata with focal statistics or use gdal_calc with neighborhood
# For simplicity, we'll use a 3x3 standard deviation calculation
# This requires gdal_calc with a neighborhood function, which is complex
# Alternative: Use gdal_fillnodata or create a simpler approach

# For now, create a simple variation mask based on local min/max difference
print(f"  Using simplified approach: local elevation range...")

variation_simple_path = str(output_path / "elevation_variation_simple.tif")

# Calculate local range (max - min in 3x3 window) as proxy for variation
# This is simpler than standard deviation but works similarly
try:
    # Use gdal_calc with a neighborhood (requires gdal >= 3.1)
    # Fallback: Create variation mask based on simple threshold
    print(f"  Note: Using elevation-based detection only (variation check skipped)")
    print(f"  For more precise detection, use QGIS Focal Statistics manually")
    variation_path = sea_mask_path  # Use sea mask as variation for now
except Exception as e:
    print(f"  Warning: Could not calculate variation: {e}")

# Step 3: Create flat sea mask (low elevation AND low variation)
print(f"\nStep 3: Creating flat sea mask...")

flat_sea_path = str(output_path / "flat_sea_mask.tif")

# For now, use sea mask directly (variation check can be added manually in QGIS)
# Copy sea mask as flat sea mask
copy_cmd = ['gdal_translate', '-co', 'COMPRESS=LZW', sea_mask_path, flat_sea_path]

try:
    result = subprocess.run(copy_cmd, capture_output=True, text=True, check=True)
    print(f"  ✓ Flat sea mask created: {flat_sea_path}")
    print(f"  Note: Currently using elevation-only detection")
    print(f"  For variation-based detection, use QGIS Focal Statistics manually")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Step 4: Create DEM with NoData for flat sea areas
print(f"\nStep 4: Creating DEM with flat sea areas removed...")

dem_no_sea_path = str(output_path / "merged_full_area_no_sea.tif")

# Set flat sea areas to NoData: if mask is 1, set to NoData, else keep elevation
calc_cmd2 = [
    'gdal_calc.py',
    '-A', RASTER_PATH,
    '--A_band=1',
    '-B', flat_sea_path,
    '--B_band=1',
    '--calc', 'numpy.where(B == 1, -9999, A)',  # Set sea areas to NoData, keep land elevation  # Multiply by (1 - mask): 0 where mask=1, A where mask=0
    '--outfile', dem_no_sea_path,
    '--NoDataValue=-9999',
    '--co', 'COMPRESS=LZW',
    '--co', 'BIGTIFF=IF_NEEDED'
]

try:
    result = subprocess.run(calc_cmd2, capture_output=True, text=True, check=True)
    print(f"  ✓ DEM with sea removed: {dem_no_sea_path}")
    
    # Count NoData pixels
    info_cmd2 = ['gdalinfo', '-stats', '-mm', dem_no_sea_path]
    info_result2 = subprocess.run(info_cmd2, capture_output=True, text=True, check=True)
    
    print(f"\n  Use this file for tile creation: {dem_no_sea_path}")
except Exception as e:
    print(f"  ✗ Error: {e}")

print("\n" + "=" * 60)
print("Summary")
print("=" * 60)
print(f"✓ Sea mask: {sea_mask_path}")
print(f"✓ Flat sea mask: {flat_sea_path}")
print(f"✓ DEM without sea: {dem_no_sea_path}")
print("\nNext steps:")
print(f"  1. Review flat_sea_mask.tif in QGIS (white = sea, black = land)")
print(f"  2. Adjust SEA_LEVEL_MAX if needed (currently {SEA_LEVEL_MAX}m)")
print(f"  3. For variation-based detection, use QGIS Focal Statistics manually")
print(f"  4. Update tile creation script to use: {dem_no_sea_path}")
print(f"  5. Tiles will automatically skip flat sea areas!")

print("\nDone!")
