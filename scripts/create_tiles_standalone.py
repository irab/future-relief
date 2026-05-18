#!/usr/bin/env python3
"""
Standalone Tile Creation Script

Run from terminal - no QGIS needed!
Uses GDAL command-line tools directly.

Usage:
    python3 scripts/create_tiles_standalone.py
"""

from pathlib import Path
import subprocess
import os
import sys

# ===== CONFIGURATION =====
RASTER_PATH = "/home/x/repos/future-relief/data/processed/merged_full_area.tif"
OUTPUT_DIR = "/home/x/repos/future-relief/data/processed/tiles"
ROWS = 5
COLS = 6

def get_raster_extent(raster_path):
    """Get raster extent using gdalinfo."""
    cmd = ['gdalinfo', raster_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"ERROR: Could not read raster: {raster_path}")
        sys.exit(1)
    
    # Parse extent from gdalinfo output
    xmin = xmax = ymin = ymax = None
    
    for line in result.stdout.split('\n'):
        if 'Upper Left' in line:
            parts = line.split('(')[1].split(')')[0].split(',')
            xmin = float(parts[0].strip())
            ymax = float(parts[1].strip())
        elif 'Lower Right' in line:
            parts = line.split('(')[1].split(')')[0].split(',')
            xmax = float(parts[0].strip())
            ymin = float(parts[1].strip())
    
    if None in [xmin, xmax, ymin, ymax]:
        print("ERROR: Could not parse raster extent")
        sys.exit(1)
    
    return xmin, xmax, ymin, ymax

# ===== MAIN SCRIPT =====
print("=" * 60)
print("Standalone Tile Creation (No QGIS Required)")
print("=" * 60)

# Check GDAL
result = subprocess.run(['gdalwarp', '--version'], capture_output=True)
if result.returncode != 0:
    print("ERROR: gdalwarp not found. Install GDAL:")
    print("  sudo apt-get install gdal-bin")
    sys.exit(1)

print("✓ GDAL found")

# Check raster exists
if not os.path.exists(RASTER_PATH):
    print(f"ERROR: Raster not found: {RASTER_PATH}")
    sys.exit(1)

file_size_gb = os.path.getsize(RASTER_PATH) / (1024**3)
print(f"✓ Raster found: {RASTER_PATH} ({file_size_gb:.1f} GB)")

# Get raster extent
print("\nReading raster extent...")
xmin, xmax, ymin, ymax = get_raster_extent(RASTER_PATH)

width = xmax - xmin
height = ymax - ymin

print(f"  Extent: {width:.2f}m × {height:.2f}m")
print(f"  X: {xmin:.2f} to {xmax:.2f}")
print(f"  Y: {ymin:.2f} to {ymax:.2f}")

# Calculate tile size
tile_width = width / COLS
tile_height = height / ROWS

print(f"\nTile configuration:")
print(f"  Grid: {COLS} columns × {ROWS} rows = {COLS * ROWS} tiles")
print(f"  Tile size: {tile_width:.2f}m × {tile_height:.2f}m")

# Create output directory
output_path = Path(OUTPUT_DIR)
output_path.mkdir(parents=True, exist_ok=True)
print(f"\n✓ Output directory: {OUTPUT_DIR}")

# Create tiles
total_tiles = ROWS * COLS
print(f"\nCreating {total_tiles} tiles...")
print("=" * 60)

success_count = 0
failed_tiles = []

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
                print(f"  ✗ Failed")
                if result.stderr:
                    error = result.stderr.split('\n')[0]
                    print(f"    {error}")
                failed_tiles.append(f"tile_{row:02d}_{col:02d}")
        except subprocess.TimeoutExpired:
            print(f"  ✗ Timeout (>10 minutes)")
            failed_tiles.append(f"tile_{row:02d}_{col:02d}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            failed_tiles.append(f"tile_{row:02d}_{col:02d}")

print("\n" + "=" * 60)
print(f"Summary: {success_count}/{total_tiles} tiles created")
print("=" * 60)

if success_count > 0:
    print(f"\n✓ Success! Created {success_count} tiles")
    print(f"  Location: {OUTPUT_DIR}")
    if failed_tiles:
        print(f"\n⚠ Failed tiles: {', '.join(failed_tiles)}")
    print(f"\nNext: Convert each tile to STL using DEMto3D in QGIS")
else:
    print(f"\n✗ No tiles created")
    print(f"  Check GDAL installation and raster file")

print("\nDone!")
