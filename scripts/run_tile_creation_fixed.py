#!/usr/bin/env python3
"""
Fixed Tile Creation Script with Better Error Handling

Run this from QGIS Python Console
"""

from qgis.core import QgsProject, QgsRasterLayer
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
print("Automated Tile Creation (Fixed Version)")
print("=" * 60)

# Verify raster exists
if not os.path.exists(RASTER_PATH):
    print(f"ERROR: Raster not found at {RASTER_PATH}")
    print("Please check the path and try again.")
else:
    print(f"✓ Found raster: {RASTER_PATH}")
    file_size_gb = os.path.getsize(RASTER_PATH) / (1024**3)
    print(f"  Size: {file_size_gb:.1f} GB")
    
    # Load raster
    raster_layer = QgsRasterLayer(RASTER_PATH, "merged_dem")
    if not raster_layer.isValid():
        print(f"ERROR: Could not load raster")
    else:
        print(f"✓ Raster loaded successfully")
        
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
            
            if os.path.exists(grid_layer_path):
                print(f"✓ Grid created: {grid_layer_path}")
            else:
                print(f"✗ Grid file not found at {grid_layer_path}")
                raise Exception("Grid creation failed")
        except Exception as e:
            print(f"✗ Error creating grid: {e}")
            import traceback
            traceback.print_exc()
            grid_layer_path = None
        
        if grid_layer_path:
            # Load grid layer
            grid_layer = QgsVectorLayer(grid_layer_path, "grid", "ogr")
            if not grid_layer.isValid():
                print("✗ ERROR: Failed to load grid")
            else:
                # Add grid to map
                QgsProject.instance().addMapLayer(grid_layer)
                print("✓ Grid added to map")
                
                # Process each grid cell
                total_tiles = ROWS * COLS
                print(f"\nProcessing {total_tiles} tiles...")
                print("=" * 60)
                
                tile_count = 0
                success_count = 0
                fail_count = 0
                
                for feature in grid_layer.getFeatures():
                    tile_count += 1
                    row = (tile_count - 1) // COLS + 1
                    col = (tile_count - 1) % COLS + 1
                    
                    print(f"\n[{tile_count}/{total_tiles}] Tile Row {row}, Col {col}")
                    
                    # Get feature extent
                    geom = feature.geometry()
                    if geom.isNull():
                        print(f"  ✗ Invalid geometry")
                        fail_count += 1
                        continue
                    
                    feature_extent = geom.boundingBox()
                    
                    # Clip raster
                    clipped_path = str(output_path / f"tile_{row:02d}_{col:02d}.tif")
                    
                    clip_params = {
                        'INPUT': RASTER_PATH,
                        'PROJWIN': feature_extent,
                        'OUTPUT': clipped_path
                    }
                    
                    try:
                        print(f"  Clipping to: {clipped_path}")
                        clip_result = processing.run('gdal:cliprasterbyextent', clip_params)
                        
                        # Check if file was actually created
                        if 'OUTPUT' in clip_result:
                            actual_path = clip_result['OUTPUT']
                            if os.path.exists(actual_path):
                                file_size_mb = os.path.getsize(actual_path) / (1024 * 1024)
                                print(f"  ✓ Created: {actual_path} ({file_size_mb:.1f} MB)")
                                success_count += 1
                            else:
                                print(f"  ✗ File not created at: {actual_path}")
                                fail_count += 1
                        else:
                            print(f"  ✗ No output path in result")
                            fail_count += 1
                            
                    except Exception as e:
                        print(f"  ✗ Error: {e}")
                        import traceback
                        traceback.print_exc()
                        fail_count += 1
                
                print("\n" + "=" * 60)
                print(f"Summary:")
                print(f"  Total tiles: {total_tiles}")
                print(f"  Successful: {success_count}")
                print(f"  Failed: {fail_count}")
                print("=" * 60)
                
                if success_count > 0:
                    print(f"\n✓ Created {success_count} tiles in: {OUTPUT_DIR}")
                    print(f"\nNext: Convert each tile to STL using DEMto3D")
                else:
                    print(f"\n✗ No tiles were created. Check errors above.")

print("\nScript complete!")
