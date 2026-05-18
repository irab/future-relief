#!/usr/bin/env python3
"""
Check Tiles for STL Conversion

Identifies which tiles have enough terrain data to be worth converting to STL.
Skips tiles that are mostly or entirely NoData (sea).

Usage:
    python3 scripts/check_tiles_for_stl.py [tiles_directory]
"""

import sys
import subprocess
from pathlib import Path
import argparse

# ===== CONFIGURATION =====
DEFAULT_TILES_DIR = "/home/x/repos/future-relief/data/processed/tiles"
MIN_DATA_PERCENTAGE = 10.0  # Minimum percentage of non-NoData pixels to convert

# ===== FUNCTIONS =====

def check_tile(tile_path, min_data_percent=10.0):
    """
    Check if a tile has enough data to be worth converting to STL.
    
    Returns:
        (has_data, data_percentage, message)
    """
    try:
        # Get tile info using gdalinfo
        info_cmd = ['gdalinfo', '-stats', '-mm', str(tile_path)]
        result = subprocess.run(info_cmd, capture_output=True, text=True, check=True)
        
        # Parse output
        has_nodata = False
        nodata_value = None
        width = height = None
        valid_pixels = None
        
        for line in result.stdout.split('\n'):
            if 'Size is' in line:
                # Size is 12169, 12169
                parts = line.split('Size is')[1].strip().split(',')
                width = int(parts[0].strip())
                height = int(parts[1].strip())
            elif 'NoData Value' in line:
                has_nodata = True
                nodata_value = line.split('=')[1].strip()
            elif 'STATISTICS_VALID_PERCENT' in line:
                valid_pixels = float(line.split('=')[1].strip())
        
        total_pixels = width * height if width and height else None
        
        if valid_pixels is not None:
            data_percentage = valid_pixels
            has_data = data_percentage >= min_data_percent
            message = f"{data_percentage:.1f}% valid data"
        elif has_nodata and total_pixels:
            # Estimate: if we have stats, assume most pixels are valid
            # This is a rough estimate - gdalinfo doesn't always give exact counts
            # For more accuracy, we'd need to read the actual raster
            message = "Data present (exact percentage unknown)"
            has_data = True  # Assume it has data if we can't determine
        else:
            message = "Unable to determine"
            has_data = True  # Default to converting if uncertain
        
        return has_data, data_percentage if valid_pixels else None, message
        
    except subprocess.CalledProcessError as e:
        return False, None, f"Error reading tile: {e.stderr[:50]}"
    except Exception as e:
        return False, None, f"Error: {str(e)[:50]}"

def main():
    parser = argparse.ArgumentParser(
        description='Check which tiles should be converted to STL',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('tiles_dir', nargs='?', default=DEFAULT_TILES_DIR,
                       help=f'Tiles directory (default: {DEFAULT_TILES_DIR})')
    parser.add_argument('--min-data', type=float, default=MIN_DATA_PERCENTAGE,
                       help=f'Minimum data percentage to convert (default: {MIN_DATA_PERCENTAGE}%%)')
    
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
    print("Checking Tiles for STL Conversion")
    print("=" * 60)
    print(f"\nTiles directory: {tiles_dir}")
    print(f"Minimum data percentage: {args.min_data}%")
    print(f"Total tiles found: {len(tile_files)}")
    print("\n" + "=" * 60)
    
    tiles_to_convert = []
    tiles_to_skip = []
    
    for tile_file in tile_files:
        has_data, data_percent, message = check_tile(tile_file, args.min_data)
        
        tile_name = tile_file.name
        
        if has_data:
            tiles_to_convert.append((tile_name, data_percent, message))
            status = "✓ CONVERT"
        else:
            tiles_to_skip.append((tile_name, data_percent, message))
            status = "✗ SKIP"
        
        # Show result
        if data_percent is not None:
            print(f"{status:12} {tile_name:20} - {message}")
        else:
            print(f"{status:12} {tile_name:20} - {message}")
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Tiles to convert: {len(tiles_to_convert)}")
    print(f"Tiles to skip: {len(tiles_to_skip)}")
    
    if tiles_to_convert:
        print(f"\n✓ Convert these tiles to STL:")
        for tile_name, data_percent, message in tiles_to_convert:
            print(f"  - {tile_name}")
    
    if tiles_to_skip:
        print(f"\n✗ Skip these tiles (mostly sea/NoData):")
        for tile_name, data_percent, message in tiles_to_skip:
            print(f"  - {tile_name}")
    
    # Save list to file
    convert_list_path = tiles_dir / "tiles_to_convert.txt"
    skip_list_path = tiles_dir / "tiles_to_skip.txt"
    
    with open(convert_list_path, 'w') as f:
        for tile_name, _, _ in tiles_to_convert:
            f.write(f"{tile_name}\n")
    
    with open(skip_list_path, 'w') as f:
        for tile_name, _, _ in tiles_to_skip:
            f.write(f"{tile_name}\n")
    
    print(f"\n✓ Lists saved:")
    print(f"  - {convert_list_path}")
    print(f"  - {skip_list_path}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
