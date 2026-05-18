#!/usr/bin/env python3
"""
Simple Tile Creation - Manual Grid Calculation

Run from QGIS Python Console
"""

from qgis.core import QgsRasterLayer, QgsRectangle
from pathlib import Path
import subprocess
import os

# ===== CONFIGURATION =====
RASTER_PATH = "/home/x/repos/future-relief/data/processed/merged_full_area.tif"
OUTPUT_DIR = "/home/x/repos/future-relief/data/processed/tiles"
ROWS = 5
COLS = 6

# ===== SCRIPT =====
print("=" * 60)
print("Simple Tile Creation (Manual Grid Calculation)")
print("=" * 60)

# Load raster
raster_layer = QgsRasterLayer(RASTER_PATH, "merged_dem")
if not raster_layer.isValid():
    print("ERROR: Invalid raster")
    exit()

extent = raster_layer.extent()
crs = raster_layer.crs()

xmin = extent.xMinimum()
xmax = extent.xMaximum()
ymin = extent.yMinimum()
ymax = extent.yMaximum()

width = xmax - xmin
height = ymax - ymin

print(f"Raster extent:")
print(f"  X: {xmin:.2f} to {xmax:.2f} ({width:.2f}m)")
print(f"  Y: {ymin:.2f} to {ymax:.2f} ({height:.2f}m)")
print(f"  CRS: {crs.authid()}")

# Calculate tile size
tile_width = width / COLS
tile_height = height / ROWS

print(f"\nTile configuration:")
print(f"  Grid: {COLS} columns × {ROWS} rows = {COLS * ROWS} tiles")
print(f"  Tile size: {tile_width:.2f}m × {tile_height:.2f}m")

# Create output directory
output_path = Path(OUTPUT_DIR)
output_path.mkdir(parents=True, exist_ok=True)
print(f"\n✓ Output: {OUTPUT_DIR}")

# Create tiles by calculating extents directly
total_tiles = ROWS * COLS
print(f"\nCreating {total_tiles} tiles...")
print("=" * 60)

success_count = 0

for row in range(1, ROWS + 1):
    for col in range(1, COLS + 1):
        tile_num = (row - 1) * COLS + col
        
        # Calculate extent for this tile
        tile_xmin = xmin + (col - 1) * tile_width
        tile_xmax = xmin + col * tile_width
        tile_ymin = ymin + (row - 1) * tile_height
        tile_ymax = ymin + row * tile_height
        
        # Ensure we don't go outside bounds
        tile_xmax = min(tile_xmax, xmax)
        tile_ymax = min(tile_ymax, ymax)
        
        print(f"\n[{tile_num}/{total_tiles}] Row {row}, Col {col}")
        print(f"  Extent: X[{tile_xmin:.0f}, {tile_xmax:.0f}] Y[{tile_ymin:.0f}, {tile_ymax:.0f}]")
        print(f"  Size: {(tile_xmax-tile_xmin):.0f}m × {(tile_ymax-tile_ymin):.0f}m")
        
        clipped_path = str(output_path / f"tile_{row:02d}_{col:02d}.tif")
        
        # Use gdalwarp
        cmd = [
            'gdalwarp',
            '-te', str(tile_xmin), str(tile_ymin), str(tile_xmax), str(tile_ymax),
            '-of', 'GTiff',
            '-co', 'COMPRESS=LZW',
            RASTER_PATH,
            clipped_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0 and os.path.exists(clipped_path):
                size_mb = os.path.getsize(clipped_path) / (1024 * 1024)
                print(f"  ✓ Created: tile_{row:02d}_{col:02d}.tif ({size_mb:.1f} MB)")
                success_count += 1
            else:
                print(f"  ✗ Failed (code: {result.returncode})")
                if result.stderr:
                    error_msg = result.stderr.split('\n')[0]
                    print(f"    {error_msg}")
        except subprocess.TimeoutExpired:
            print(f"  ✗ Timeout (>10 minutes)")
        except Exception as e:
            print(f"  ✗ Error: {e}")

print("\n" + "=" * 60)
print(f"Summary: {success_count}/{total_tiles} tiles created")
print("=" * 60)

if success_count > 0:
    print(f"\n✓ Success! Created {success_count} tiles in {OUTPUT_DIR}")
    print(f"\nNext: Convert each tile to STL using DEMto3D")
else:
    print(f"\n✗ No tiles created. Check:")
    print(f"  1. GDAL is installed: gdalwarp --version")
    print(f"  2. Raster file exists and is readable")
    print(f"  3. Output directory is writable")

print("\nDone!")
