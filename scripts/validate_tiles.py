#!/usr/bin/env python3
"""
Validate Tiles Have Elevation Data

Checks all tiles to ensure they have proper elevation data (not all zeros or empty).

Usage:
    python3 scripts/validate_tiles.py [tiles_directory]
"""

import sys
import subprocess
from pathlib import Path
import argparse

# ===== CONFIGURATION =====
DEFAULT_TILES_DIR = "/home/x/repos/future-relief/data/processed/tiles"
MIN_ELEVATION_RANGE = 0.01  # Minimum elevation difference to consider valid (meters)

# ===== FUNCTIONS =====

def check_tile_elevation(tile_path, min_range=0.01):
    """
    Check if a tile has valid elevation data.
    
    Returns:
        (is_valid, min_elev, max_elev, message)
    """
    try:
        # Get tile info using gdalinfo
        info_cmd = ['gdalinfo', '-stats', str(tile_path)]
        result = subprocess.run(info_cmd, capture_output=True, text=True, check=True, timeout=30)
        
        min_elev = max_elev = None
        has_nodata = False
        nodata_value = None
        
        for line in result.stdout.split('\n'):
            if 'STATISTICS_MINIMUM=' in line:
                min_elev = float(line.split('=')[1])
            elif 'STATISTICS_MAXIMUM=' in line:
                max_elev = float(line.split('=')[1])
            elif 'NoData Value=' in line:
                has_nodata = True
                nodata_value = line.split('=')[1].strip()
        
        if min_elev is None or max_elev is None:
            return False, None, None, "Could not read statistics"
        
        # Check if tile has elevation variation
        elevation_range = abs(max_elev - min_elev)
        
        if elevation_range < min_range:
            return False, min_elev, max_elev, f"No elevation variation (range: {elevation_range:.3f}m)"
        
        if min_elev == 0 and max_elev == 0:
            return False, min_elev, max_elev, "All zeros (no elevation data)"
        
        return True, min_elev, max_elev, f"Elevation range: {min_elev:.2f}m to {max_elev:.2f}m"
        
    except subprocess.CalledProcessError as e:
        return False, None, None, f"Error reading tile: {e.stderr[:50] if hasattr(e, 'stderr') else str(e)[:50]}"
    except subprocess.TimeoutExpired:
        return False, None, None, "Timeout reading tile"
    except Exception as e:
        return False, None, None, f"Error: {str(e)[:50]}"

def main():
    parser = argparse.ArgumentParser(
        description='Validate tiles have elevation data',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('tiles_dir', nargs='?', default=DEFAULT_TILES_DIR,
                       help=f'Tiles directory (default: {DEFAULT_TILES_DIR})')
    parser.add_argument('--min-range', type=float, default=MIN_ELEVATION_RANGE,
                       help=f'Minimum elevation range to consider valid (default: {MIN_ELEVATION_RANGE}m)')
    
    args = parser.parse_args()
    
    tiles_dir = Path(args.tiles_dir)
    
    if not tiles_dir.exists():
        print(f"✗ Error: Tiles directory not found: {tiles_dir}")
        return 1
    
    # Find all tile files
    tile_files = sorted(tiles_dir.glob("tile_*.tif"))
    
    if not tile_files:
        print(f"✗ No tile files found in: {tiles_dir}")
        return 1
    
    print("=" * 60)
    print("Validating Tiles Have Elevation Data")
    print("=" * 60)
    print(f"\nTiles directory: {tiles_dir}")
    print(f"Minimum elevation range: {args.min_range}m")
    print(f"Total tiles found: {len(tile_files)}")
    print("\n" + "=" * 60)
    
    valid_tiles = []
    empty_tiles = []
    error_tiles = []
    
    for tile_file in tile_files:
        is_valid, min_elev, max_elev, message = check_tile_elevation(tile_file, args.min_range)
        
        tile_name = tile_file.name
        
        if is_valid:
            valid_tiles.append((tile_name, min_elev, max_elev))
            print(f"✓ VALID     {tile_name:20} - {message}")
        elif min_elev is not None:
            empty_tiles.append((tile_name, min_elev, max_elev))
            print(f"✗ EMPTY     {tile_name:20} - {message}")
        else:
            error_tiles.append((tile_name, message))
            print(f"✗ ERROR     {tile_name:20} - {message}")
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Valid tiles: {len(valid_tiles)}")
    print(f"Empty tiles: {len(empty_tiles)}")
    print(f"Error tiles: {len(error_tiles)}")
    
    if valid_tiles:
        print(f"\n✓ Valid tiles (have elevation data):")
        for tile_name, min_elev, max_elev in valid_tiles[:10]:
            print(f"  - {tile_name}: {min_elev:.2f}m to {max_elev:.2f}m")
        if len(valid_tiles) > 10:
            print(f"  ... and {len(valid_tiles) - 10} more")
    
    if empty_tiles:
        print(f"\n✗ Empty tiles (no elevation data):")
        for tile_name, min_elev, max_elev in empty_tiles[:10]:
            print(f"  - {tile_name}: Min={min_elev:.2f}, Max={max_elev:.2f}")
        if len(empty_tiles) > 10:
            print(f"  ... and {len(empty_tiles) - 10} more")
        print(f"\n  These tiles should be skipped for STL conversion!")
    
    if error_tiles:
        print(f"\n✗ Error tiles (could not read):")
        for tile_name, message in error_tiles:
            print(f"  - {tile_name}: {message}")
    
    # Save lists to file
    if valid_tiles:
        valid_list_path = tiles_dir / "tiles_valid.txt"
        with open(valid_list_path, 'w') as f:
            for tile_name, _, _ in valid_tiles:
                f.write(f"{tile_name}\n")
        print(f"\n✓ Valid tiles list saved: {valid_list_path}")
    
    if empty_tiles:
        empty_list_path = tiles_dir / "tiles_empty.txt"
        with open(empty_list_path, 'w') as f:
            for tile_name, _, _ in empty_tiles:
                f.write(f"{tile_name}\n")
        print(f"✓ Empty tiles list saved: {empty_list_path}")
    
    # Return error code if there are issues
    if empty_tiles or error_tiles:
        print(f"\n⚠️  WARNING: {len(empty_tiles) + len(error_tiles)} tiles have issues!")
        return 1
    
    print(f"\n✓ All tiles have valid elevation data!")
    return 0

if __name__ == '__main__':
    sys.exit(main())
