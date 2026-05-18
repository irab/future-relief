# 3D Printing Settings for Prusa XL

Optimized settings for printing your 2m x 1.5m terrain map on a Prusa XL.

## Prusa XL Specifications

- **Print bed**: 36cm x 36cm (360mm x 360mm) - standard model
- **Layer height**: Supports 0.05mm to 0.3mm
- **Nozzle**: 0.4mm standard (can use 0.6mm or 0.8mm for faster printing)
- **Material**: PLA, PETG, or other standard materials

## Tiling Strategy for 2m x 1.5m Map

Your map is **2000mm x 1500mm**, but the Prusa XL bed is **360mm x 360mm**.

**You'll need approximately:**
- **6 tiles wide** (2000mm ÷ 360mm = 5.56, round up to 6)
- **5 tiles tall** (1500mm ÷ 360mm = 4.17, round up to 5)
- **Total: ~30 tiles** to print and assemble

### Tile Size Calculation

For easier assembly, make tiles slightly smaller than the bed:
- **Tile size**: 330mm x 330mm (leaves 15mm margin on each side)
- This gives you: **6 x 5 = 30 tiles**

## DEMto3D Settings for Prusa XL

### For Each Tile:

**Model Dimensions:**
- **Model width**: `330` mm (per tile)
- **Model height**: `330` mm (per tile)
- Note: You'll need to clip your merged DEM into 30 separate tiles first

**Model Settings:**
- **Model size spacing**: `0.2` mm
  - Prusa XL can handle 0.2mm detail well
  - For faster processing: `0.3` mm (still good detail)
  - For maximum detail: `0.15` mm (slower processing, larger files)
- **Model height**: `-2.18` (your minimum elevation)
- **Note**: Add 20mm base in PrusaSlicer (see [Adding a Base](ADDING_BASE.md))

**Vertical Exaggeration:**
- **6.0x** (recommended - provides good terrain visibility and fits in 360mm bed)
- Creates ~186mm terrain height (fits comfortably in 360mm bed)
- See [Why Vertical Exaggeration](WHY_VERTICAL_EXAGGERATION.md) for details

**Output:**
- **Format**: STL Binary
- **Naming**: Use systematic names like `tile_01_01.stl`, `tile_01_02.stl`, etc.

## Creating Tiles in QGIS

Before converting to STL, you need to split your merged DEM into 30 tiles:

### Method 1: Create Grid and Clip

1. **Create Grid**:
   - **Vector** → **Research Tools** → **Create Grid**
   - **Grid type**: Rectangle (grid)
   - **Grid extent**: Cover your merged DEM area
   - **Horizontal spacing**: Calculate based on your scale
     - If your DEM covers X meters wide, and you want 6 tiles:
     - Spacing = (DEM width in meters) / 6
   - **Vertical spacing**: Same calculation for 5 tiles
   - Click **Run**

2. **For Each Grid Cell**:
   - **Raster** → **Extraction** → **Clip Raster by Mask Layer**
   - Select your merged DEM
   - Select one grid cell as mask
   - Output: `tile_01_01.tif`, `tile_01_02.tif`, etc.

3. **Convert Each Tile to STL**:
   - Run DEMto3D on each clipped tile
   - Use 330mm x 330mm dimensions
   - Name systematically: `tile_01_01.stl`, `tile_01_02.stl`, etc.

### Method 2: Clip by Extent (Manual)

1. Calculate extent for each tile based on your DEM bounds
2. **Raster** → **Extraction** → **Clip Raster by Extent**
3. Enter coordinates for each 330mm x 330mm tile
4. Convert each to STL

## Prusa XL Print Settings

### Recommended Print Settings

**Layer Height:**
- **0.2mm** - Good balance of detail and speed (recommended)
- **0.15mm** - Higher detail, slower printing
- **0.3mm** - Faster printing, slightly less detail

**Infill:**
- **10-15%** - Sufficient for terrain models
- **Pattern**: Gyroid or Cubic (good for large prints)

**Supports:**
- **Usually not needed** if printing base-down
- May need supports for overhangs if terrain has steep features
- Use **Tree supports** if needed (less material)

**Print Speed:**
- **First layer**: 20-30 mm/s (important for adhesion)
- **Perimeters**: 40-50 mm/s
- **Infill**: 60-80 mm/s
- **Travel**: 150-200 mm/s

**Material:**
- **PLA**: Recommended for large prints (easier to print, less warping)
- **PETG**: More durable, slightly more challenging
- **Temperature**: Follow material recommendations

**Bed Adhesion:**
- **Brim**: 5-10mm (helps with large prints)
- **Raft**: Usually not needed
- **First layer**: Ensure good bed leveling and adhesion

## Assembly Strategy

### Alignment Marks

Consider adding alignment features to your tiles:

1. **In QGIS**: Before clipping, you could add small alignment markers
2. **In Slicer**: Add small holes or pins to tiles for alignment
3. **Post-print**: Use registration marks or pins

### Assembly Process

1. **Print all tiles** with consistent settings
2. **Label each tile** (tile_01_01, tile_01_02, etc.)
3. **Dry fit** before gluing
4. **Use strong adhesive**: Epoxy or specialized 3D print adhesive
5. **Clamp or weight** during curing

## File Size Considerations

With 0.2mm spacing and 330mm x 330mm tiles:
- **Each STL**: ~50-200MB (depends on terrain complexity)
- **30 tiles total**: ~1.5-6GB
- Ensure you have enough disk space

## Time Estimates

**STL Generation** (per tile):
- 0.2mm spacing: 5-15 minutes per tile
- 30 tiles: 2.5-7.5 hours total

**Printing** (per tile on Prusa XL):
- 0.2mm layer height: 10-20 hours per tile
- 30 tiles: 300-600 hours total (12-25 days of continuous printing!)

**Recommendation**: Start with 1-2 test tiles to verify settings before printing all 30.

## Optimization Tips

1. **Test First**: Print 1-2 tiles to verify settings
2. **Batch Processing**: Generate all STL files in one session
3. **Consistent Settings**: Use same settings for all tiles
4. **Monitor First Layers**: Large prints need good first layer adhesion
5. **Material Management**: Ensure you have enough filament (estimate 500g-1kg per tile)

## Troubleshooting

### Tiles Don't Fit Bed
- Reduce tile size to 320mm x 320mm
- Check slicer bed size settings

### Poor Detail
- Reduce model size spacing to 0.15mm
- Increase vertical exaggeration
- Use smaller layer height (0.15mm)

### Print Fails
- Check first layer adhesion
- Use brim for better bed grip
- Slow down first layer speed
- Check bed leveling

### Tiles Don't Align
- Ensure consistent scale across all tiles
- Use same vertical exaggeration for all
- Add alignment marks before printing

## Next Steps

1. Create grid in QGIS for 30 tiles
2. Clip merged DEM to each grid cell
3. Convert first tile to STL as a test
4. Print test tile to verify settings
5. If test looks good, process all 30 tiles
6. Print and assemble!
