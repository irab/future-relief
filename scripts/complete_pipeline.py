#!/usr/bin/env python3
"""
Complete Pipeline: Merged TIF to Print-Ready Tiles

This script automates the entire workflow:
1. Detect and exclude flat sea areas
2. Create square tiles for 3D printing
3. Prepare tiles for STL conversion

Usage:
    python3 scripts/complete_pipeline.py [input_tif] [options]

Or run from QGIS Python Console:
    exec(open('/home/x/repos/future-relief/scripts/complete_pipeline.py').read())
"""

import sys
import subprocess
import os
from pathlib import Path
import argparse

# ===== CONFIGURATION =====
DEFAULT_INPUT = "/home/x/repos/future-relief/data/processed/merged_full_area.tif"
DEFAULT_OUTPUT_DIR = "/home/x/repos/future-relief/data/processed"
DEFAULT_TILES_DIR = "/home/x/repos/future-relief/data/processed/tiles"

# Sea detection parameters
SEA_LEVEL_MAX = 0.0  # Maximum elevation to consider as sea (meters) - only exclude below sea level
VARIATION_THRESHOLD = 0.5  # Maximum elevation variation for "flat" (meters)

# Tile creation parameters
TARGET_TILE_SIZE_MM = 330  # Square tiles: 330mm × 330mm
TARGET_PRINT_WIDTH_MM = 2000  # Full map width
TARGET_PRINT_HEIGHT_MM = 1500  # Full map height

# ===== FUNCTIONS =====

def check_gdal():
    """Check if GDAL is installed and available."""
    try:
        subprocess.run(['gdalinfo', '--version'], capture_output=True, check=True)
        subprocess.run(['gdal_calc.py', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def detect_flat_sea(input_raster, output_dir, sea_level_max=0.0):
    """
    Detect and exclude sea areas from DEM (only below sea level: < 0m).
    
    Returns path to DEM with sea areas removed.
    Preserves all land areas including beaches and low-lying areas.
    """
    print("\n" + "=" * 60)
    print("STEP 1: Detecting Flat Sea Areas")
    print("=" * 60)
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    sea_mask_path = str(output_path / "sea_mask.tif")
    flat_sea_path = str(output_path / "flat_sea_mask.tif")
    dem_no_sea_path = str(output_path / "merged_full_area_no_sea.tif")
    
    # Check if already exists
    if os.path.exists(dem_no_sea_path):
        print(f"  Found existing DEM without sea: {dem_no_sea_path}")
        response = input("  Use existing? (y/n): ").strip().lower()
        if response == 'y':
            return dem_no_sea_path
    
    # Get raster info
    print(f"\n  Input raster: {input_raster}")
    try:
        info_cmd = ['gdalinfo', '-stats', input_raster]
        info_result = subprocess.run(info_cmd, capture_output=True, text=True, check=True)
        for line in info_result.stdout.split('\n'):
            if 'STATISTICS_MINIMUM' in line:
                min_elev = float(line.split('=')[1])
            elif 'STATISTICS_MAXIMUM' in line:
                max_elev = float(line.split('=')[1])
        print(f"  Elevation range: {min_elev:.2f}m to {max_elev:.2f}m")
    except Exception as e:
        print(f"  Warning: Could not get statistics: {e}")
    
    # Step 1: Create sea level mask (only exclude below sea level: < 0m)
    print(f"\n  Creating sea level mask (elevation < 0m - below sea level only)...")
    calc_cmd = [
        'gdal_calc.py',
        '-A', input_raster,
        '--A_band=1',
        '--calc', '(A < 0) * 1',  # Only exclude below sea level
        '--outfile', sea_mask_path,
        '--NoDataValue=0',
        '--type=Byte',
        '--co', 'COMPRESS=LZW',
        '--quiet'
    ]
    
    try:
        subprocess.run(calc_cmd, check=True, capture_output=True)
        print(f"  ✓ Sea mask created")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error creating sea mask: {e}")
        return None
    except FileNotFoundError:
        print(f"  ✗ gdal_calc.py not found. Install GDAL Python bindings:")
        print(f"     sudo apt-get install python3-gdal")
        return None
    
    # Step 2: Create flat sea mask (for now, same as sea mask)
    # Copy sea mask as flat sea mask
    print(f"  Creating flat sea mask...")
    copy_cmd = ['gdal_translate', '-co', 'COMPRESS=LZW', '-q', sea_mask_path, flat_sea_path]
    try:
        subprocess.run(copy_cmd, check=True, capture_output=True)
        print(f"  ✓ Flat sea mask created")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None
    
    # Step 3: Create DEM with NoData for sea areas
    print(f"  Creating DEM with sea areas removed...")
    # Use conditional: if sea mask (B) is 1, set to NoData, else keep elevation (A)
    calc_cmd2 = [
        'gdal_calc.py',
        '-A', input_raster,
        '--A_band=1',
        '-B', flat_sea_path,
        '--B_band=1',
        '--calc', 'numpy.where(B == 1, -9999, A)',  # Set sea areas to NoData, keep land elevation
        '--outfile', dem_no_sea_path,
        '--NoDataValue=-9999',
        '--co', 'COMPRESS=LZW',
        '--co', 'BIGTIFF=IF_NEEDED',
        '--quiet'
    ]
    
    try:
        subprocess.run(calc_cmd2, check=True, capture_output=True)
        print(f"  ✓ DEM with sea removed: {dem_no_sea_path}")
        return dem_no_sea_path
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None

def create_square_tiles(input_raster, output_dir, target_tile_size_mm=330, 
                       target_print_width_mm=2000):
    """
    Create square tiles from DEM for 3D printing.
    
    Returns path to tiles directory.
    """
    print("\n" + "=" * 60)
    print("STEP 2: Creating Square Tiles")
    print("=" * 60)
    
    tiles_dir = Path(output_dir) / "tiles"
    tiles_dir.mkdir(parents=True, exist_ok=True)
    
    # Get raster extent using gdalinfo
    print(f"\n  Getting raster extent...")
    try:
        info_cmd = ['gdalinfo', input_raster]
        info_result = subprocess.run(info_cmd, capture_output=True, text=True, check=True)
        
        # Parse extent from gdalinfo output
        xmin = ymin = xmax = ymax = None
        for line in info_result.stdout.split('\n'):
            if 'Upper Left' in line:
                parts = line.split('(')[1].split(')')[0].split(',')
                xmin = float(parts[0].strip())
                ymax = float(parts[1].strip())
            elif 'Lower Right' in line:
                parts = line.split('(')[1].split(')')[0].split(',')
                xmax = float(parts[0].strip())
                ymin = float(parts[1].strip())
        
        if not all([xmin, ymin, xmax, ymax]):
            print("  ✗ Could not parse extent from gdalinfo")
            return None
        
        width_m = xmax - xmin
        height_m = ymax - ymin
        
        print(f"  Raster extent:")
        print(f"    X: {xmin:.2f} to {xmax:.2f} ({width_m:.2f}m = {width_m/1000:.2f}km)")
        print(f"    Y: {ymin:.2f} to {ymax:.2f} ({height_m:.2f}m = {height_m/1000:.2f}km)")
        print(f"    Aspect ratio: {width_m/height_m:.3f}:1")
        
    except Exception as e:
        print(f"  ✗ Error getting raster info: {e}")
        return None
    
    # Calculate square tile size
    scale = target_print_width_mm / width_m  # mm per meter
    tile_size_m = target_tile_size_mm / scale
    
    print(f"\n  Scale calculation:")
    print(f"    Scale: {scale*1000:.6f} mm/m")
    print(f"    Square tile size: {tile_size_m:.2f}m ({tile_size_m/1000:.2f}km)")
    
    # Calculate number of tiles
    cols = int(width_m / tile_size_m) + (1 if width_m % tile_size_m > 0 else 0)
    rows = int(height_m / tile_size_m) + (1 if height_m % tile_size_m > 0 else 0)
    
    print(f"\n  Tile grid:")
    print(f"    Columns: {cols}")
    print(f"    Rows: {rows}")
    print(f"    Total tiles: {cols * rows}")
    
    # Check if tiles already exist
    existing_tiles = list(tiles_dir.glob("tile_*.tif"))
    if existing_tiles:
        print(f"\n  Found {len(existing_tiles)} existing tiles")
        response = input("  Overwrite existing tiles? (y/n): ").strip().lower()
        if response != 'y':
            print("  Skipping tile creation")
            return str(tiles_dir)
    
    # Create tiles
    print(f"\n  Creating {cols * rows} tiles...")
    print("  " + "-" * 56)
    
    success_count = 0
    failed_tiles = []
    total_tiles = cols * rows
    
    for row in range(1, rows + 1):
        for col in range(1, cols + 1):
            tile_num = (row - 1) * cols + col
            
            # Calculate extent
            tile_xmin = xmin + (col - 1) * tile_size_m
            tile_xmax = min(xmin + col * tile_size_m, xmax)
            tile_ymin = ymin + (row - 1) * tile_size_m
            tile_ymax = min(ymin + row * tile_size_m, ymax)
            
            # Ensure square
            actual_width = tile_xmax - tile_xmin
            actual_height = tile_ymax - tile_ymin
            square_size = min(actual_width, actual_height)
            tile_xmax = tile_xmin + square_size
            tile_ymax = tile_ymin + square_size
            
            clipped_path = str(tiles_dir / f"tile_{row:02d}_{col:02d}.tif")
            
            # Use gdalwarp to clip
            cmd = [
                'gdalwarp',
                '-overwrite',
                '-te', str(tile_xmin), str(tile_ymin), str(tile_xmax), str(tile_ymax),
                '-of', 'GTiff',
                '-co', 'COMPRESS=LZW',
                '-co', 'BIGTIFF=IF_NEEDED',
                '-q',
                input_raster,
                clipped_path
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
                
                if result.returncode == 0 and os.path.exists(clipped_path):
                    size_mb = os.path.getsize(clipped_path) / (1024 * 1024)
                    print(f"  [{tile_num:3d}/{total_tiles}] Row {row:2d}, Col {col:2d} ✓ ({size_mb:.1f} MB)")
                    success_count += 1
                else:
                    print(f"  [{tile_num:3d}/{total_tiles}] Row {row:2d}, Col {col:2d} ✗")
                    failed_tiles.append(f"tile_{row:02d}_{col:02d}")
            except subprocess.TimeoutExpired:
                print(f"  [{tile_num:3d}/{total_tiles}] Row {row:2d}, Col {col:2d} ✗ (timeout)")
                failed_tiles.append(f"tile_{row:02d}_{col:02d}")
            except Exception as e:
                print(f"  [{tile_num:3d}/{total_tiles}] Row {row:2d}, Col {col:2d} ✗ ({e})")
                failed_tiles.append(f"tile_{row:02d}_{col:02d}")
    
    print("\n  " + "=" * 56)
    print(f"  Summary: {success_count}/{total_tiles} tiles created")
    
    if failed_tiles:
        print(f"  ✗ Failed tiles: {len(failed_tiles)}")
    else:
        print(f"  ✓ All tiles created successfully!")
    
    # Validate tiles have elevation data
    print(f"\n  Validating tiles have elevation data...")
    print("  " + "-" * 56)
    
    empty_tiles = []
    valid_tiles = []
    
    for row in range(1, rows + 1):
        for col in range(1, cols + 1):
            tile_path = tiles_dir / f"tile_{row:02d}_{col:02d}.tif"
            if not tile_path.exists():
                continue
            
            try:
                info_cmd = ['gdalinfo', '-stats', str(tile_path)]
                result = subprocess.run(info_cmd, capture_output=True, text=True, check=True, timeout=30)
                
                min_val = max_val = None
                for line in result.stdout.split('\n'):
                    if 'STATISTICS_MINIMUM=' in line:
                        min_val = float(line.split('=')[1])
                    elif 'STATISTICS_MAXIMUM=' in line:
                        max_val = float(line.split('=')[1])
                
                if min_val is not None and max_val is not None:
                    # Check if tile has actual elevation data (not all zeros or NoData)
                    if abs(max_val - min_val) < 0.01 or (min_val == 0 and max_val == 0):
                        empty_tiles.append(f"tile_{row:02d}_{col:02d}")
                        print(f"  ✗ {tile_path.name}: No elevation data (Min={min_val:.2f}, Max={max_val:.2f})")
                    else:
                        valid_tiles.append(f"tile_{row:02d}_{col:02d}")
                        print(f"  ✓ {tile_path.name}: Elevation range {min_val:.2f}m to {max_val:.2f}m")
            except Exception as e:
                empty_tiles.append(f"tile_{row:02d}_{col:02d}")
                print(f"  ✗ {tile_path.name}: Error checking ({str(e)[:50]})")
    
    print("  " + "=" * 56)
    print(f"  Validation: {len(valid_tiles)} valid, {len(empty_tiles)} empty")
    
    if empty_tiles:
        print(f"\n  ⚠️  WARNING: {len(empty_tiles)} tiles have no elevation data!")
        print(f"  Empty tiles: {', '.join(empty_tiles[:10])}")
        if len(empty_tiles) > 10:
            print(f"  ... and {len(empty_tiles) - 10} more")
        
        # If ALL tiles are empty, that's a problem
        if len(valid_tiles) == 0:
            print(f"\n  ✗ ERROR: ALL tiles are empty - no elevation data!")
            print(f"  This usually means:")
            print(f"  1. Source DEM has no data (check: gdalinfo -stats [source_file])")
            print(f"  2. Sea detection removed all data (check sea mask)")
            print(f"  3. Tiles were created from wrong/corrupted source file")
            print(f"\n  Recommendation:")
            print(f"  - Check source DEM: gdalinfo -stats {input_raster}")
            print(f"  - Re-run with --skip-sea-detection if sea detection is the issue")
            print(f"  - Delete old tiles and re-create from valid source")
            return None  # Return None to indicate failure
        else:
            print(f"\n  Note: Some empty tiles are normal (sea areas)")
            print(f"  Only convert tiles with elevation data to STL")
    
    return str(tiles_dir)

def main():
    """Main pipeline function."""
    parser = argparse.ArgumentParser(
        description='Complete pipeline: Merged TIF to Print-Ready Tiles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default input file
  python3 scripts/complete_pipeline.py
  
  # Specify custom input
  python3 scripts/complete_pipeline.py /path/to/merged.tif
  
  # Skip sea detection
  python3 scripts/complete_pipeline.py --skip-sea-detection
  
  # Custom sea level threshold
  python3 scripts/complete_pipeline.py --sea-level 3.0
        """
    )
    
    parser.add_argument('input', nargs='?', default=DEFAULT_INPUT,
                       help=f'Input merged TIF file (default: {DEFAULT_INPUT})')
    parser.add_argument('--output-dir', default=DEFAULT_OUTPUT_DIR,
                       help=f'Output directory (default: {DEFAULT_OUTPUT_DIR})')
    parser.add_argument('--skip-sea-detection', action='store_true',
                       help='Skip flat sea detection step')
    parser.add_argument('--sea-level', type=float, default=SEA_LEVEL_MAX,
                       help=f'Maximum elevation for sea detection in meters (default: {SEA_LEVEL_MAX} - only excludes below sea level)')
    parser.add_argument('--tile-size', type=int, default=TARGET_TILE_SIZE_MM,
                       help=f'Tile size in mm (default: {TARGET_TILE_SIZE_MM})')
    parser.add_argument('--print-width', type=int, default=TARGET_PRINT_WIDTH_MM,
                       help=f'Full print width in mm (default: {TARGET_PRINT_WIDTH_MM})')
    
    args = parser.parse_args()
    
    # Check if running in QGIS
    try:
        from qgis.core import QgsApplication
        in_qgis = True
    except ImportError:
        in_qgis = False
    
    print("=" * 60)
    print("Complete Pipeline: Merged TIF to Print-Ready Tiles")
    print("=" * 60)
    print(f"\nInput: {args.input}")
    print(f"Output directory: {args.output_dir}")
    
    # Check GDAL
    if not check_gdal():
        print("\n✗ ERROR: GDAL not found or incomplete installation")
        print("  Install GDAL: sudo apt-get install gdal-bin python3-gdal")
        return 1
    
    # Check input file
    if not os.path.exists(args.input):
        print(f"\n✗ ERROR: Input file not found: {args.input}")
        return 1
    
    # Step 1: Detect flat sea (optional)
    if args.skip_sea_detection:
        print("\n⏭️  Skipping sea detection (--skip-sea-detection)")
        dem_for_tiles = args.input
    else:
        dem_for_tiles = detect_flat_sea(args.input, args.output_dir, args.sea_level)
        if not dem_for_tiles:
            print("\n✗ Sea detection failed. Continuing with original DEM...")
            dem_for_tiles = args.input
    
    # Step 2: Create square tiles
    tiles_dir = create_square_tiles(
        dem_for_tiles, 
        args.output_dir,
        args.tile_size,
        args.print_width
    )
    
    if not tiles_dir:
        print("\n✗ Tile creation failed")
        return 1
    
    # Summary
    print("\n" + "=" * 60)
    print("Pipeline Complete!")
    print("=" * 60)
    print(f"\n✓ Tiles created in: {tiles_dir}")
    print(f"\nNext steps:")
    print(f"  1. Review tiles in QGIS to verify they look correct")
    print(f"  2. Convert each tile to STL using DEMto3D:")
    print(f"     - Model size: {args.tile_size}mm × {args.tile_size}mm")
    print(f"     - Spacing: 0.2mm")
    print(f"     - Height: -2.18m")
    print(f"     - Exaggeration: 6.0x")
    print(f"  3. Add 20mm base in PrusaSlicer")
    print(f"  4. Print and assemble!")
    
    return 0

if __name__ == '__main__':
    # Check if running from QGIS
    try:
        from qgis.core import QgsApplication
        # Running in QGIS - execute main
        if __name__ == '__main__':
            sys.exit(main())
    except ImportError:
        # Running standalone
        sys.exit(main())
