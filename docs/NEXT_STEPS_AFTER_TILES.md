# Next Steps After Creating Tiles

You've successfully created 30 clipped tiles! Here's what to do next.

## Current Status

✅ **Completed:**
- Merged all GeoTIFF tiles into one DEM
- Created tiles (tile_01_01.tif through tile_XX_YY.tif)
- Tiles are ready in `data/processed/tiles/`

**Note:** If your tiles are **rectangular** (not square), see [Square Tiles Guide](SQUARE_TILES.md) to recreate them as square tiles for easier printing on a 36cm × 36cm × 36cm bed.

## Next: Convert Tiles to STL

### Step 1: Test with 1-2 Tiles First

**Before processing all 30 tiles, test your settings:**

1. **Load first tile in QGIS:**
   - Layer → Add Layer → Add Raster Layer
   - Navigate to `data/processed/tiles/`
   - Select `tile_01_01.tif`
   - Click Open

2. **Convert to STL using DEMto3D:**
   - See [FIRST_STL_GUIDE.md](FIRST_STL_GUIDE.md) for detailed steps
   - Use these settings:
     - Layer extent: Click leftmost magnifying glass
     - Width: 330mm, Height: 330mm
     - Spacing: 0.2mm
     - Height (m): -2.18
     - Base height (mm): 0
     - Exaggeration: 6.0x
     - Output: `output/tile_01_01.stl`

3. **Verify in PrusaSlicer:**
   - Open the STL file
   - Check dimensions (should be 330mm × 330mm)
   - Add 20mm base (see [Adding a Base](ADDING_BASE.md))
   - Verify it looks good

4. **If test looks good:** Proceed with all tiles
   - If not: Adjust settings and test again

### Step 2: Process All 30 Tiles

**Recommended workflow:**

1. **Process in batches:**
   - Batch 1: Tiles 01_01 through 01_06 (6 tiles)
   - Batch 2: Tiles 02_01 through 02_06 (6 tiles)
   - Continue until all 30 are done

2. **For each tile:**
   - Load tile in QGIS
   - Run DEMto3D with same settings
   - Wait 5-15 minutes
   - Move to next tile

3. **Time estimate:**
   - 30 tiles × 5-15 minutes = 2.5-7.5 hours total
   - Take breaks between batches!

### Step 3: Add Base in PrusaSlicer

After all STL files are created:

1. **Open each STL in PrusaSlicer**
2. **Add 20mm base:**
   - Print Settings → Infill and perimeters
   - Bottom solid layers: 100 (for 20mm at 0.2mm layers)
   - See [Adding a Base](ADDING_BASE.md) for details

3. **Configure print settings:**
   - Layer height: 0.2mm
   - Infill: 10-15%
   - See [Prusa XL Settings](PRUSA_XL_SETTINGS.md) for complete settings

### Step 4: Print and Assemble

1. **Print all 30 tiles**
   - Each tile: 10-20 hours print time
   - Total: 300-600 hours (12-25 days of continuous printing!)

2. **Label tiles** as you print them
   - Use systematic naming: tile_01_01, tile_01_02, etc.

3. **Assemble tiles:**
   - Dry fit first
   - Use strong adhesive (epoxy recommended)
   - Align carefully using tile edges

## Quick Reference: DEMto3D Settings

For **every tile**, use these exact settings:

```
Layer extent: Click leftmost magnifying glass (auto-set)
Model width: 330 mm
Model height (length): 330 mm  ⚠️ Should match width for square tiles!
Model size spacing: 0.2 mm
Height (m): -2.18 ⚠️ REQUIRED
Base height (mm): 0 ⚠️ REQUIRED
Vertical exaggeration: 6.0
Output format: STL Binary
Output file: output/tile_XX_YY.stl (match tile name)
```

**For 36cm × 36cm × 36cm printer bed:** Ensure tiles are square (330mm × 330mm). If your tiles are rectangular, see [Square Tiles Guide](SQUARE_TILES.md) to recreate them.

## Troubleshooting

### DEMto3D Shows "Fill the data correctly"
- Make sure **Height (m)** field is filled: `-2.18`
- Make sure **Base height (mm)** field is filled: `0`
- Set layer extent first (click magnifying glass)

### Processing Takes Too Long
- Increase model size spacing to 0.3mm
- Process smaller batches
- Close other applications

### STL File Too Large
- Increase spacing to 0.3mm or 0.5mm
- Use binary STL format

## Documentation Links

- **[FIRST_STL_GUIDE.md](FIRST_STL_GUIDE.md)** - Detailed STL conversion steps
- **[CREATING_TILES.md](CREATING_TILES.md)** - How tiles were created
- **[ADDING_BASE.md](ADDING_BASE.md)** - Adding 20mm base in PrusaSlicer
- **[PRUSA_XL_SETTINGS.md](PRUSA_XL_SETTINGS.md)** - Print settings
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues

## Progress Checklist

- [x] Merge GeoTIFF tiles
- [x] Create 30 clipped tiles
- [ ] Convert first test tile to STL
- [ ] Verify test tile in PrusaSlicer
- [ ] Convert remaining 29 tiles to STL
- [ ] Add 20mm base to all STLs
- [ ] Print test tile
- [ ] Print all 30 tiles
- [ ] Assemble terrain model

---

**You're making great progress!** Start with 1-2 test tiles, then process the rest in batches.
