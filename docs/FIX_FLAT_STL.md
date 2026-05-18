# Fix: STL Z-Dimension Too Small

If your STL shows Z-dimension of only 1-2mm (should be ~186mm), the DEMto3D settings were incorrect.

## The Problem

**What you're seeing:**
- X: 330mm ✓
- Y: 330mm ✓
- Z: 2mm ✗ (should be ~186mm!)

**What it should be:**
- X: 330mm ✓
- Y: 330mm ✓
- Z: ~186mm ✓ (with 6x exaggeration)

## Root Cause

The "Height (m)" field in DEMto3D was likely:
- ❌ Not filled (left empty)
- ❌ Set to wrong value
- ❌ Cleared after setting extent

## Solution: Re-generate STL with Correct Settings

### Step 1: Load Tile in QGIS

1. **Layer → Add Layer → Add Raster Layer**
2. Navigate to `data/processed/tiles/`
3. Select `tile_06_03.tif` (or your tile)
4. Click **Open**

### Step 2: Open DEMto3D

1. **Select the tile layer** in Layers panel
2. **Raster → DEMto3D → DEM 3D Printing**

### Step 3: Configure Settings (IN THIS ORDER!)

**⚠️ IMPORTANT: Fill fields in this exact order to avoid issues:**

1. **Layer extent:**
   - Click the **leftmost magnifying glass** button
   - This sets extent from layer
   - X and Y fields should fill automatically

2. **Model dimensions:**
   - Model width: `330` mm
   - Model height (length): `330` mm

3. **Model size spacing:**
   - `0.2` mm

4. **Height (m):** ⚠️ **CRITICAL - FILL THIS!**
   - Enter: `-2.18`
   - **This is your minimum elevation**
   - **If this is wrong or empty, Z will be tiny!**

5. **Base height (mm):** ⚠️ **REQUIRED**
   - Enter: `0`
   - **Must be filled or you'll get an error**

6. **Vertical exaggeration:**
   - Enter: `6.0`
   - **This creates the height!**

7. **Output:**
   - Output file: `output/tile_06_03_model.stl`
   - Format: STL Binary

### Step 4: Verify Before Exporting

**Check these values appear correctly:**
- Lowest point: Should show a value (around -2.18m)
- Highest point: Should show ~1523m
- Model height: Should calculate automatically (should be large, not tiny)

**If these are wrong, the Z dimension will be wrong!**

### Step 5: Export

1. Click **"Export to STL"**
2. Wait for processing (5-15 minutes)
3. Check the new STL file

### Step 6: Verify New STL

1. **Import new STL in PrusaSlicer**
2. **Check Z dimension:**
   - Should be ~186mm (not 2mm!)
   - With 6x exaggeration: (1523m - (-2.18m)) × 6 / scale ≈ 186mm

3. **Rotate to side view:**
   - Right-click + drag to rotate
   - You should see terrain height variation

## Expected Z-Dimension Calculation

**With correct settings:**
- Elevation range: -2.18m to 1523m = 1525.26m total
- Vertical exaggeration: 6x
- Scale: 2000mm / 73752m = 0.0271 mm/m
- Z dimension: 1525.26m × 6 × 0.0271 mm/m ≈ **186mm**

**If Z is only 2mm:**
- Settings were wrong (likely Height (m) field)
- Or exaggeration wasn't applied
- Or base height was wrong

## Common Mistakes

### Mistake 1: Height (m) Field Empty

**Symptom:** Z dimension is tiny (1-2mm)

**Fix:** Fill "Height (m)" with `-2.18`

### Mistake 2: Height (m) Set to 0

**Symptom:** Z dimension is wrong

**Fix:** Use `-2.18` (your minimum elevation)

### Mistake 3: Setting Extent After Height

**Symptom:** Height field gets cleared

**Fix:** Set extent FIRST, then fill Height (m)

### Mistake 4: Wrong Exaggeration

**Symptom:** Z dimension is too small or too large

**Fix:** Use `6.0` for Prusa XL

## Quick Checklist

Before exporting, verify:

- [ ] Layer extent: Set (clicked magnifying glass)
- [ ] Model width: 330mm
- [ ] Model height: 330mm
- [ ] Model size spacing: 0.2mm
- [ ] **Height (m): -2.18** ⚠️
- [ ] **Base height (mm): 0** ⚠️
- [ ] Vertical exaggeration: 6.0
- [ ] Output format: STL Binary
- [ ] Lowest/Highest points show correct values

## After Fixing

**You should see:**
- Z dimension: ~186mm (not 2mm!)
- Terrain visible from side view
- Layers show variation when sliced

**If still wrong:**
- Double-check all settings
- Verify original tile has elevation data
- Check DEMto3D for error messages

## Summary

**The issue:** Z dimension is 2mm (should be ~186mm)

**The cause:** "Height (m)" field in DEMto3D was wrong or empty

**The fix:** Re-generate STL with correct settings:
- Height (m): `-2.18` ⚠️ CRITICAL
- Base height (mm): `0` ⚠️ REQUIRED
- Vertical exaggeration: `6.0`

**Result:** Z dimension should be ~186mm with visible terrain!
