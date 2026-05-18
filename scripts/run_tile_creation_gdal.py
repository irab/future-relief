#!/usr/bin/env python3
"""
Tile Creation using GDAL Command Line (More Reliable)

Run from QGIS Python Console
"""

from qgis.core import QgsProject, QgsRasterLayer, QgsVectorLayer
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
print("Tile Creation using GDAL (Command Line)")
print("=" * 60)

# Verify raster
if not os.path.exists(RASTER_PATH):
    print(f"ERROR: Raster not found")
    exit()

print(f"✓ Raster: {RASTER_PATH}")

# Load raster to get extent
raster_layer = QgsRasterLayer(RASTER_PATH, "merged_dem")
if not raster_layer.isValid():
    print(f"ERROR: Invalid raster")
    exit()

extent = raster_layer.extent()
crs = raster_layer.crs()
width = extent.width()
height = extent.height()

print(f"  Extent: {width:.2f}m × {height:.2f}m")
print(f"  CRS: {crs.authid()}")

# Calculate spacing
h_spacing = width / COLS
v_spacing = height / ROWS

print(f"\nGrid: {COLS} × {ROWS} = {COLS * ROWS} tiles")
print(f"  H spacing: {h_spacing:.2f}m")
print(f"  V spacing: {v_spacing:.2f}m")

# Create output directory
output_path = Path(OUTPUT_DIR)
output_path.mkdir(parents=True, exist_ok=True)
print(f"\n✓ Output: {OUTPUT_DIR}")

# Create grid using QGIS (for reference)
print(f"\nCreating grid...")
grid_path = str(output_path / "print_grid.shp")

from qgis import processing

grid_params = {
    'TYPE': 0,
    'EXTENT': extent,
    'HSPACING': h_spacing,
    'VSPACING': v_spacing,
    'HOVERLAY': 0,
    'VOVERLAY': 0,
    'CRS': crs,
    'OUTPUT': grid_path
}

grid_result = processing.run('qgis:creategrid', grid_params)
grid_layer_path = grid_result['OUTPUT']
grid_layer = QgsVectorLayer(grid_layer_path, "grid", "ogr")
QgsProject.instance().addMapLayer(grid_layer)
print("✓ Grid created and loaded")

# Process each tile using GDAL command line
total_tiles = ROWS * COLS
print(f"\nClipping {total_tiles} tiles using GDAL...")
print("=" * 60)

tile_count = 0
success_count = 0

for feature in grid_layer.getFeatures():
    tile_count += 1
    row = (tile_count - 1) // COLS + 1
    col = (tile_count - 1) % COLS + 1
    
    print(f"\n[{tile_count}/{total_tiles}] Row {row}, Col {col}")
    
    geom = feature.geometry()
    if geom.isNull():
        print(f"  ✗ Invalid geometry")
        continue
    
    feature_extent = geom.boundingBox()
    
    # Get extent coordinates - ensure min < max
    xmin = min(feature_extent.xMinimum(), feature_extent.xMaximum())
    xmax = max(feature_extent.xMinimum(), feature_extent.xMaximum())
    ymin = min(feature_extent.yMinimum(), feature_extent.yMaximum())
    ymax = max(feature_extent.yMinimum(), feature_extent.yMaximum())
    
    # Check if extent is valid
    if xmin >= xmax or ymin >= ymax:
        print(f"  ✗ Invalid extent: {xmin:.0f} >= {xmax:.0f} or {ymin:.0f} >= {ymax:.0f}")
        print(f"     This grid cell has zero area - skipping")
        continue
    
    # Add small buffer to ensure we get the data
    buffer = 1.0  # 1 meter buffer
    xmin -= buffer
    xmax += buffer
    ymin -= buffer
    ymax += buffer
    
    clipped_path = str(output_path / f"tile_{row:02d}_{col:02d}.tif")
    
    # Use gdalwarp to clip
    cmd = [
        'gdalwarp',
        '-te', str(xmin), str(ymin), str(xmax), str(ymax),
        '-of', 'GTiff',
        '-co', 'COMPRESS=LZW',
        RASTER_PATH,
        clipped_path
    ]
    
    try:
        print(f"  Extent: {xmin:.0f}, {ymin:.0f} to {xmax:.0f}, {ymax:.0f}")
        print(f"  Size: {(xmax-xmin):.0f}m × {(ymax-ymin):.0f}m")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0 and os.path.exists(clipped_path):
            size_mb = os.path.getsize(clipped_path) / (1024 * 1024)
            print(f"  ✓ Created: tile_{row:02d}_{col:02d}.tif ({size_mb:.1f} MB)")
            success_count += 1
        else:
            print(f"  ✗ Failed (return code: {result.returncode})")
            if result.stderr:
                print(f"    Error: {result.stderr[:200]}")
    except subprocess.TimeoutExpired:
        print(f"  ✗ Timeout (>5 minutes)")
    except Exception as e:
        print(f"  ✗ Error: {e}")

print("\n" + "=" * 60)
print(f"Summary: {success_count}/{total_tiles} tiles created")
print("=" * 60)

if success_count > 0:
    print(f"\n✓ Successfully created {success_count} tiles!")
    print(f"  Location: {OUTPUT_DIR}")
    print(f"\nNext: Convert each tile to STL using DEMto3D")
else:
    print(f"\n✗ No tiles created. Check GDAL installation:")
    print(f"  Run: gdalwarp --version")

print("\nDone!")
