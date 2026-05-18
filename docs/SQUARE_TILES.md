# Creating Square Tiles for 3D Printing

Your merged DEM is **rectangular** (73.75km × 96.31km), which means when divided into a 6×5 grid, the tiles are also rectangular (12.29km × 19.26km). When converted to STL at 330mm × 330mm, DEMto3D maintains the aspect ratio, resulting in **rectangular STL files**, not square ones.

**For a 36cm × 36cm × 36cm printer bed**, you need **square tiles** (330mm × 330mm) to fit properly and be easier to assemble.

## The Problem

- **Current tiles**: 12.29km × 19.26km (rectangular)
- **STL output**: Will be rectangular (not square)
- **Desired**: Square tiles (330mm × 330mm) for easier printing and assembly

## Solution: Create Square Geographic Tiles

To get square STL files, we need to create **square tiles in geographic space**. This means using the same dimension for both width and height when dividing the DEM.

## Option 1: Use Square Tile Script (Recommended)

A script is available that automatically creates **perfectly square tiles**:

1. **Open QGIS Python Console**
   - **Plugins** → **Python Console** (or press `Ctrl+Alt+P`)

2. **Run the square tile script:**
   ```python
   exec(open('/home/x/repos/future-relief/scripts/create_square_tiles.py').read())
   ```

3. **The script will:**
   - Calculate square tile size based on your 2m × 1.5m print dimensions
   - Force all tiles to be perfectly square in geographic space
   - Create a grid of square tiles
   - Generate all tiles automatically

**Result:** You'll get square tiles that convert to square STL files (330mm × 330mm), perfect for your 36cm × 36cm × 36cm printer bed.

**Note:** This will create more tiles than the rectangular approach (approximately 48-56 tiles instead of 30), but all tiles will be square and easier to assemble.

## Option 2: Manual Calculation

If you prefer to calculate manually:

### Step 1: Determine Square Tile Size

Your DEM is 73.75km wide. For a 2m print width:
- Scale: 2000mm ÷ 73.75km = 0.0271 mm/m
- Square tile size: 330mm ÷ 0.0271 mm/m = **12,177 meters** (12.18km)

### Step 2: Calculate Grid

- **Columns**: 73.75km ÷ 12.18km = **6 columns**
- **Rows**: 96.31km ÷ 12.18km = **7.91** → **8 rows**
- **Total**: 6 × 8 = **48 tiles**

### Step 3: Create Grid in QGIS

1. **Vector** → **Research Tools** → **Create Grid**
2. **Grid type**: Rectangle (grid)
3. **Grid extent**: Calculate from `merged_full_area` layer
4. **Horizontal spacing**: `12180` meters
5. **Vertical spacing**: `12180` meters (same as horizontal!)
6. **Output**: `data/processed/square_grid.shp`
7. Click **Run**

### Step 4: Clip to Square Tiles

Use the same clipping process as before, but now tiles will be square.

## Trade-offs

**Square tiles (Option 1/2):**
- ✅ Square STL files (330mm × 330mm)
- ✅ Easier to assemble
- ✅ Consistent tile size
- ❌ More tiles (48 instead of 30)
- ❌ Slightly more printing time

**Rectangular tiles (current):**
- ✅ Fewer tiles (30)
- ✅ Faster to print
- ❌ Rectangular STL files
- ❌ Harder to align during assembly

## Recommendation

**Use square tiles** for better assembly and consistency. The extra 18 tiles are worth it for easier alignment and a more professional result.

## After Creating Square Tiles

1. **Verify tiles are square:**
   - Check one tile in QGIS
   - Right-click → **Properties** → **Information**
   - Width and height should be approximately equal

2. **Convert to STL:**
   - Use DEMto3D with 330mm × 330mm settings
   - STL files should now be square!

3. **Print and assemble:**
   - Square tiles are much easier to align
   - Use consistent spacing between tiles

## Quick Reference

**Square tile script:**
```bash
# From QGIS Python Console
exec(open('/home/x/repos/future-relief/scripts/create_square_tiles.py').read())
```

**Manual square grid:**
- Horizontal spacing: 12,180 meters
- Vertical spacing: 12,180 meters (same!)
- Result: 6 × 8 = 48 square tiles
