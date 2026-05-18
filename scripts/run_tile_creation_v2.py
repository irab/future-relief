#!/usr/bin/env python3
"""
Tile Creation Script - Version 2 with Better Error Handling

Run from QGIS Python Console
"""

from qgis.core import QgsProject, QgsRasterLayer, QgsRectangle
from pathlib import Path
import processing
import os

# ===== CONFIGURATION =====
RASTER_PATH = "/home/x/repos/future-relief/data/processed/merged_full_area.tif"
OUTPUT_DIR = "/home/x/repos/future-relief/data/processed/tiles"
ROWS = 5
COLS = 6

# ===== SCRIPT =====
print("=" * 60)
print("Automated Tile Creation (Version 2)")
print("=" * 60)

# Verify raster
if not os.path.exists(RASTER_PATH):
    print(f"ERROR: Raster not found")
    exit()
else:
    print(f"✓ Raster found: {RASTER_PATH}")
    
    # Load raster
    raster_layer = QgsRasterLayer(RASTER_PATH, "merged_dem")
    if not raster_layer.isValid():
        print(f"ERROR: Invalid raster layer")
        exit()
    
    print(f"✓ Raster loaded")
    
    # Get extent
    extent = raster_layer.extent()
    crs = raster_layer.crs()
    width = extent.width()
    height = extent.height()
    
    print(f"  Extent: {width:.2f}m × {height:.2f}m")
    
    # Calculate spacing
    h_spacing = width / COLS
    v_spacing = height / ROWS
    
    print(f"\nGrid: {COLS} columns × {ROWS} rows")
    print(f"  H spacing: {h_spacing:.2f}m")
    print(f"  V spacing: {v_spacing:.2f}m")
    
    # Create output directory
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"\n✓ Output: {OUTPUT_DIR}")
    
    # Create grid
    print(f"\nCreating grid...")
    grid_path = str(output_path / "print_grid.shp")
    
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
    
    try:
        grid_result = processing.run('qgis:creategrid', grid_params)
        grid_layer_path = grid_result['OUTPUT']
        print(f"✓ Grid created")
    except Exception as e:
        print(f"✗ Grid error: {e}")
        exit()
    
    # Load grid
    grid_layer = QgsVectorLayer(grid_layer_path, "grid", "ogr")
    if not grid_layer.isValid():
        print("✗ Invalid grid")
        exit()
    
    QgsProject.instance().addMapLayer(grid_layer)
    print("✓ Grid loaded")
    
    # Process tiles
    total_tiles = ROWS * COLS
    print(f"\nProcessing {total_tiles} tiles...")
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
        
        # Try using 'native:cliprasterbyextent' instead
        clipped_path = str(output_path / f"tile_{row:02d}_{col:02d}.tif")
        
        # Method 1: Try native QGIS algorithm
        try:
            clip_params = {
                'INPUT': RASTER_PATH,
                'PROJWIN': f"{feature_extent.xMinimum()},{feature_extent.xMaximum()},{feature_extent.yMinimum()},{feature_extent.yMaximum()}",
                'OUTPUT': clipped_path
            }
            
            print(f"  Extent: {feature_extent.xMinimum():.0f}, {feature_extent.yMinimum():.0f} to {feature_extent.xMaximum():.0f}, {feature_extent.yMaximum():.0f}")
            
            result = processing.run('gdal:cliprasterbyextent', clip_params)
            
            # Check multiple possible output locations
            output_file = None
            if 'OUTPUT' in result:
                output_file = result['OUTPUT']
            elif 'OUTPUT_RASTER' in result:
                output_file = result['OUTPUT_RASTER']
            else:
                # Try the path we specified
                output_file = clipped_path
            
            # Wait a moment for file system
            import time
            time.sleep(0.5)
            
            if output_file and os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"  ✓ Created: {os.path.basename(output_file)} ({size_mb:.1f} MB)")
                success_count += 1
            else:
                # Try alternative: use 'native:cliprasterbyextent'
                print(f"  Trying alternative method...")
                alt_params = {
                    'INPUT': raster_layer,
                    'PROJWIN': feature_extent,
                    'OUTPUT': clipped_path
                }
                try:
                    alt_result = processing.run('native:cliprasterbyextent', alt_params)
                    if 'OUTPUT' in alt_result and os.path.exists(alt_result['OUTPUT']):
                        size_mb = os.path.getsize(alt_result['OUTPUT']) / (1024 * 1024)
                        print(f"  ✓ Created (alt): {os.path.basename(alt_result['OUTPUT'])} ({size_mb:.1f} MB)")
                        success_count += 1
                    else:
                        print(f"  ✗ Alternative method also failed")
                except Exception as e2:
                    print(f"  ✗ Alternative error: {e2}")
                    
        except Exception as e:
            print(f"  ✗ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"Summary: {success_count}/{total_tiles} tiles created")
    print("=" * 60)
    
    if success_count == 0:
        print("\nAll tiles failed. Trying manual method...")
        print("\nYou can manually clip tiles:")
        print("1. Select a grid cell")
        print("2. Raster → Extraction → Clip Raster by Mask Layer")
        print("3. Input: merged_full_area")
        print("4. Mask: print_grid (with 'Selected features only')")
        print("5. Output: tile_XX_YY.tif")

print("\nDone!")
