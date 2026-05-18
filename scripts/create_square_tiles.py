#!/usr/bin/env python3
"""
Create Square Tiles for 3D Printing

This script creates square tiles in geographic space, which will convert
to square STL files (330mm × 330mm) for easier printing and assembly.

Run from QGIS Python Console
"""

from qgis.core import QgsRasterLayer, QgsRectangle
from pathlib import Path
import subprocess
import os

# ===== CONFIGURATION =====
RASTER_PATH = "/home/x/repos/future-relief/data/processed/merged_full_area.tif"
OUTPUT_DIR = "/home/x/repos/future-relief/data/processed/tiles"
TARGET_TILE_SIZE_MM = 330  # Square tiles: 330mm × 330mm
TARGET_PRINT_WIDTH_MM = 2000  # Full map width
TARGET_PRINT_HEIGHT_MM = 1500  # Full map height

# ===== SCRIPT =====
print("=" * 60)
print("Creating Square Tiles for 3D Printing")
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

width_m = xmax - xmin
height_m = ymax - ymin

print(f"\nRaster extent:")
print(f"  X: {xmin:.2f} to {xmax:.2f} ({width_m:.2f}m = {width_m/1000:.2f}km)")
print(f"  Y: {ymin:.2f} to {ymax:.2f} ({height_m:.2f}m = {height_m/1000:.2f}km)")
print(f"  Aspect ratio: {width_m/height_m:.3f}:1")
print(f"  CRS: {crs.authid()}")

# Calculate square tiles for 36cm × 36cm × 36cm printer bed
# Strategy: Use the same square dimension for both width and height
# This ensures all tiles are perfectly square in geographic space

# Calculate scale factor for width (to get 2m print width)
scale = TARGET_PRINT_WIDTH_MM / width_m  # mm per meter

# Calculate square tile size in meters
# This ensures each tile converts to 330mm × 330mm STL
tile_size_m = TARGET_TILE_SIZE_MM / scale

print(f"\nScale calculation:")
print(f"  Scale: {scale*1000:.6f} mm/m")
print(f"  Square tile size: {tile_size_m:.2f}m ({tile_size_m/1000:.2f}km)")

# Calculate number of tiles needed using the same square size for both dimensions
cols = int(width_m / tile_size_m) + (1 if width_m % tile_size_m > 0 else 0)
rows = int(height_m / tile_size_m) + (1 if height_m % tile_size_m > 0 else 0)

print(f"\nSquare tile configuration:")
print(f"  Square tile size: {tile_size_m:.2f}m × {tile_size_m:.2f}m ({tile_size_m/1000:.2f}km)")
print(f"  Columns: {cols}")
print(f"  Rows: {rows}")
print(f"  Total tiles: {cols * rows}")

print(f"\n✓ All tiles will be perfectly square: {tile_size_m:.2f}m × {tile_size_m:.2f}m")
print(f"  This converts to: {TARGET_TILE_SIZE_MM}mm × {TARGET_TILE_SIZE_MM}mm STL files")
print(f"  Perfect for 36cm × 36cm × 36cm printer bed!")

# Create output directory
output_path = Path(OUTPUT_DIR)
output_path.mkdir(parents=True, exist_ok=True)
print(f"\n✓ Output: {OUTPUT_DIR}")

# Ask for confirmation
print(f"\n" + "=" * 60)
print(f"This will create {cols * rows} tiles.")
print(f"Existing tiles in {OUTPUT_DIR} will be overwritten.")
print("=" * 60)

# Create tiles by calculating extents directly
total_tiles = rows * cols
print(f"\nCreating {total_tiles} tiles...")
print("=" * 60)

success_count = 0
failed_tiles = []

for row in range(1, rows + 1):
    for col in range(1, cols + 1):
        tile_num = (row - 1) * cols + col
        
        # Calculate extent for this tile (using square dimensions)
        tile_xmin = xmin + (col - 1) * tile_size_m
        tile_xmax = min(xmin + col * tile_size_m, xmax)  # Don't exceed bounds
        tile_ymin = ymin + (row - 1) * tile_size_m
        tile_ymax = min(ymin + row * tile_size_m, ymax)  # Don't exceed bounds
        
        # Ensure square: use the smaller dimension to ensure perfect square
        # (Edge tiles may be slightly smaller but still square)
        actual_width = tile_xmax - tile_xmin
        actual_height = tile_ymax - tile_ymin
        square_size = min(actual_width, actual_height)
        
        # Adjust to ensure square (edge tiles may be slightly smaller)
        tile_xmax = tile_xmin + square_size
        tile_ymax = tile_ymin + square_size
        
        actual_width = tile_xmax - tile_xmin
        actual_height = tile_ymax - tile_ymin
        
        print(f"\n[{tile_num}/{total_tiles}] Row {row}, Col {col}")
        print(f"  Extent: X[{tile_xmin:.0f}, {tile_xmax:.0f}] Y[{tile_ymin:.0f}, {tile_ymax:.0f}]")
        print(f"  Size: {actual_width:.0f}m × {actual_height:.0f}m", end="")
        
        if abs(actual_width - actual_height) < 1.0:
            print(" ✓ SQUARE")
        else:
            print(f" ⚠️  (not square, diff: {abs(actual_width - actual_height):.1f}m)")
        
        clipped_path = str(output_path / f"tile_{row:02d}_{col:02d}.tif")
        
        # Use gdalwarp
        cmd = [
            'gdalwarp',
            '-overwrite',
            '-te', str(tile_xmin), str(tile_ymin), str(tile_xmax), str(tile_ymax),
            '-of', 'GTiff',
            '-co', 'COMPRESS=LZW',
            '-co', 'BIGTIFF=IF_NEEDED',
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

if failed_tiles:
    print(f"\n✗ Failed tiles: {', '.join(failed_tiles)}")
else:
    print(f"\n✓ All tiles created successfully!")

if success_count > 0:
    print(f"\nNext steps:")
    print(f"  1. Verify tiles are square in QGIS")
    print(f"  2. Convert each tile to STL using DEMto3D:")
    print(f"     - Model size: 330mm × 330mm")
    print(f"     - Spacing: 0.2mm")
    print(f"     - Height: -2.18m")
    print(f"     - Exaggeration: 6.0x")
    print(f"  3. Tiles should now be square in STL format!")

print("\nDone!")
