#!/usr/bin/env python3
"""
Simplified script to run tile creation from QGIS Python Console

Copy and paste this into QGIS Python Console
"""

from qgis.core import QgsProject, QgsRasterLayer
from pathlib import Path
import processing

# ===== CONFIGURATION =====
# Update these paths to match your setup
RASTER_PATH = "/home/x/repos/future-relief/data/processed/merged_full_area.tif"
OUTPUT_DIR = "/home/x/repos/future-relief/data/processed/tiles"
ROWS = 5  # Number of rows (vertical tiles)
COLS = 6  # Number of columns (horizontal tiles)

# ===== SCRIPT =====
print("=" * 60)
print("Automated Tile Creation")
print("=" * 60)

# Load raster
raster_layer = QgsRasterLayer(RASTER_PATH, "merged_dem")
if not raster_layer.isValid():
    print(f"ERROR: Could not load raster from {RASTER_PATH}")
    print("Please check the path and try again.")
else:
    print(f"✓ Loaded raster: {RASTER_PATH}")
    
    # Get extent
    extent = raster_layer.extent()
    crs = raster_layer.crs()
    width = extent.width()
    height = extent.height()
    
    print(f"  Extent: {width:.2f}m × {height:.2f}m")
    print(f"  CRS: {crs.authid()}")
    
    # Calculate spacing
    h_spacing = width / COLS
    v_spacing = height / ROWS
    
    print(f"\nGrid configuration:")
    print(f"  Rows: {ROWS}, Columns: {COLS}")
    print(f"  Horizontal spacing: {h_spacing:.2f}m")
    print(f"  Vertical spacing: {v_spacing:.2f}m")
    
    # Create output directory
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"\n✓ Output directory: {OUTPUT_DIR}")
    
    # Create grid
    print(f"\nCreating grid...")
    grid_path = str(output_path / "print_grid.shp")
    
    grid_params = {
        'TYPE': 0,  # Rectangle (grid)
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
    print(f"✓ Grid created: {grid_layer_path}")
    
    # Load grid layer
    grid_layer = QgsVectorLayer(grid_layer_path, "grid", "ogr")
    if not grid_layer.isValid():
        print("ERROR: Failed to create grid")
    else:
        # Add grid to map (optional)
        QgsProject.instance().addMapLayer(grid_layer)
        print("✓ Grid added to map")
        
        # Process each grid cell
        total_tiles = ROWS * COLS
        print(f"\nProcessing {total_tiles} tiles...")
        print("=" * 60)
        
        tile_count = 0
        for feature in grid_layer.getFeatures():
            tile_count += 1
            row = (tile_count - 1) // COLS + 1
            col = (tile_count - 1) % COLS + 1
            
            print(f"\n[{tile_count}/{total_tiles}] Tile Row {row}, Col {col}")
            
            # Get feature extent
            geom = feature.geometry()
            feature_extent = geom.boundingBox()
            
            # Clip raster
            clipped_path = str(output_path / f"tile_{row:02d}_{col:02d}.tif")
            
            clip_params = {
                'INPUT': RASTER_PATH,
                'PROJWIN': feature_extent,
                'OUTPUT': clipped_path
            }
            
            try:
                clip_result = processing.run('gdal:cliprasterbyextent', clip_params)
                if clip_result and 'OUTPUT' in clip_result:
                    actual_path = clip_result['OUTPUT']
                    if os.path.exists(actual_path):
                        print(f"  ✓ Clipped: {actual_path}")
                    else:
                        print(f"  ⚠ Warning: File not found at {actual_path}")
                else:
                    print(f"  ✗ Error: No output from clipping")
            except Exception as e:
                print(f"  ✗ Error clipping tile {row}_{col}: {e}")
                import traceback
                traceback.print_exc()
        
        print("\n" + "=" * 60)
        print(f"✓ Completed! Created {total_tiles} clipped raster tiles")
        print(f"\nNext steps:")
        print(f"  1. Each tile is saved as: tile_XX_YY.tif")
        print(f"  2. Run the batch helper script:")
        print(f"     - Open Python Console")
        print(f"     - Run: scripts/batch_stl_conversion.py")
        print(f"  3. Convert each to STL using DEMto3D plugin:")
        print(f"     - Model size: 330mm × 330mm")
        print(f"     - Spacing: 0.2mm")
        print(f"     - Height: -2.18m")
        print(f"     - Exaggeration: 6.0x")
        print(f"  4. Start with 1-2 test tiles first!")

print("\nScript complete!")
