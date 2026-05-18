#!/usr/bin/env python3
"""
Batch STL Conversion Helper Script

This script helps automate the conversion of clipped tiles to STL format.
Since DEMto3D doesn't have a direct Python API, this script:
1. Lists all tiles
2. Provides instructions for batch processing
3. Can be extended to use QGIS processing if available

Run this from QGIS Python Console after creating tiles.
"""

from pathlib import Path
import os

# Configuration
TILES_DIR = "/home/x/repos/future-relief/data/processed/tiles"
OUTPUT_DIR = "/home/x/repos/future-relief/output"
ROWS = 5
COLS = 6

def list_tiles():
    """List all created tiles."""
    tiles_path = Path(TILES_DIR)
    tiles = sorted(tiles_path.glob("tile_*.tif"))
    
    print("=" * 60)
    print("Created Tiles for STL Conversion")
    print("=" * 60)
    print(f"\nFound {len(tiles)} tiles:\n")
    
    for i, tile in enumerate(tiles, 1):
        size_mb = tile.stat().st_size / (1024 * 1024)
        print(f"{i:2d}. {tile.name:20s} ({size_mb:6.1f} MB)")
    
    return tiles

def generate_conversion_instructions():
    """Generate step-by-step instructions for converting tiles."""
    tiles = list_tiles()
    
    print("\n" + "=" * 60)
    print("STL Conversion Instructions")
    print("=" * 60)
    
    print("\nFor each tile, use DEMto3D with these settings:")
    print("\n  Model Dimensions:")
    print("    - Width: 330 mm")
    print("    - Height (Length): 330 mm")
    print("\n  Model Settings:")
    print("    - Spacing: 0.2 mm (or 0.3 mm)")
    print("    - Height (m): -2.18")
    print("    - Base height (mm): 0")
    print("\n  Vertical Exaggeration:")
    print("    - 6.0x")
    print("\n  Output:")
    print(f"    - Directory: {OUTPUT_DIR}")
    print("    - Format: STL Binary")
    print("    - Naming: tile_XX_YY.stl (match the .tif name)")
    
    print("\n" + "=" * 60)
    print("Recommended Workflow")
    print("=" * 60)
    print("\n1. Test with 1-2 tiles first:")
    print("   - Convert tile_01_01.tif and tile_01_02.tif")
    print("   - Verify STL files look correct")
    print("   - Check dimensions in PrusaSlicer")
    print("\n2. Process in batches of 5-10 tiles:")
    print("   - Convert 5-10 tiles at a time")
    print("   - Take breaks between batches")
    print("   - Each tile takes 5-15 minutes to convert")
    print("\n3. Use consistent settings for all tiles")
    
    print("\n" + "=" * 60)
    print("Estimated Time")
    print("=" * 60)
    print(f"\nTotal tiles: {len(tiles)}")
    print("Time per tile: 5-15 minutes")
    print(f"Total time: {len(tiles) * 5}-{len(tiles) * 15} minutes")
    print(f"           ({len(tiles) * 5 / 60:.1f}-{len(tiles) * 15 / 60:.1f} hours)")
    
    # Create output directory
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"\n✓ Output directory ready: {OUTPUT_DIR}")

def create_tile_list_file():
    """Create a text file listing all tiles for reference."""
    tiles = list(Path(TILES_DIR).glob("tile_*.tif"))
    tiles = sorted(tiles)
    
    list_file = Path(TILES_DIR) / "tile_list.txt"
    with open(list_file, 'w') as f:
        f.write("Tile List for STL Conversion\n")
        f.write("=" * 60 + "\n\n")
        for i, tile in enumerate(tiles, 1):
            row = (i - 1) // COLS + 1
            col = (i - 1) % COLS + 1
            f.write(f"{i:2d}. {tile.name:20s} (Row {row}, Col {col})\n")
    
    print(f"\n✓ Created tile list: {list_file}")
    return list_file

if __name__ == '__main__':
    # This can be run from QGIS Python Console
    print("\n" + "=" * 60)
    print("Batch STL Conversion Helper")
    print("=" * 60)
    
    tiles = list_tiles()
    generate_conversion_instructions()
    create_tile_list_file()
    
    print("\n" + "=" * 60)
    print("Ready to convert tiles to STL!")
    print("=" * 60)
    print("\nStart with 1-2 test tiles, then process the rest in batches.")
    print("Each tile conversion takes 5-15 minutes.")
