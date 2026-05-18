# Troubleshooting: STL Appears Flat

If your STL file appears completely flat in PrusaSlicer or other viewers, here's how to diagnose and fix it.

## Quick Checks

### 1. Check the View Angle

**The terrain might be there, just hard to see from certain angles:**

1. **Rotate the view:**
   - Right-click and drag to rotate
   - Try viewing from the side (rotate 90°)
   - The terrain detail might be visible from different angles

2. **Zoom in:**
   - Scroll wheel to zoom in
   - Terrain detail might be subtle and hard to see when zoomed out

3. **Check layer preview:**
   - Click "Slice now" in PrusaSlicer
   - Look at the layer preview (bottom slider)
   - If layers show variation, the terrain is there!

### 2. Check STL File Size

**A flat STL would be very small:**

```bash
# Check file size
ls -lh your_tile.stl

# If it's very small (< 1MB), it might actually be flat
# If it's larger (10-100MB), it likely has terrain data
```

### 3. Check Dimensions in PrusaSlicer

**Look at the dimensions shown:**

1. **Bottom-right corner** shows dimensions
2. **Z-height (thickness):**
   - If Z is very small (< 1mm), it's actually flat
   - If Z is larger (10-200mm), terrain is there but might be hard to see

3. **Object List panel:**
   - Right panel shows object dimensions
   - Check the Z value

## Common Causes

### Cause 1: DEMto3D Settings Wrong

**Problem:** Height (m) field was incorrect or missing

**Check:**
- Did you fill "Height (m)" with `-2.18`?
- Did you set "Base height (mm)" to `0`?
- Did you set "Vertical exaggeration" to `6.0`?

**Fix:**
- Re-run DEMto3D with correct settings
- See [First STL Guide](FIRST_STL_GUIDE.md) for exact settings

### Cause 2: Tile is Actually Flat

**Problem:** The tile area is actually flat (no elevation variation)

**Check:**
- Load the original tile in QGIS
- Check if it has elevation variation
- Some tiles might be genuinely flat (e.g., very flat areas)

**Fix:**
- This is normal for some tiles
- Skip these tiles if they're mostly flat sea/land

### Cause 3: View Scale Issue

**Problem:** Terrain is there but too subtle to see

**Check:**
- Rotate to side view
- Zoom in very close
- Check layer preview after slicing

**Fix:**
- The terrain might be there but subtle
- Try slicing and checking layers

### Cause 4: STL File Corrupted

**Problem:** STL file didn't generate correctly

**Check:**
```bash
# Try opening in different viewer
meshlab your_tile.stl

# Or check file size (should be reasonable)
ls -lh your_tile.stl
```

**Fix:**
- Re-generate STL from DEMto3D
- Check for errors during generation

## Diagnostic Steps

### Step 1: Check Original Tile in QGIS

1. **Load the tile in QGIS:**
   ```bash
   # In QGIS: Layer → Add Layer → Add Raster Layer
   # Load: data/processed/tiles/tile_XX_YY.tif
   ```

2. **Check elevation range:**
   - Right-click layer → Properties → Information
   - Look for Min/Max elevation
   - If min ≈ max, tile is actually flat

3. **Visual check:**
   - Switch to Hillshade view
   - If you see terrain detail, the data is there
   - If it's completely flat, the tile has no variation

### Step 2: Check STL in PrusaSlicer

1. **Import STL:**
   - File → Import → Select STL

2. **Check dimensions:**
   - Bottom-right shows: X × Y × Z
   - Z should be > 1mm if terrain exists
   - If Z < 1mm, it's actually flat

3. **Rotate view:**
   - Right-click + drag to rotate
   - View from side (90° rotation)
   - Terrain should be visible from side

4. **Slice and check layers:**
   - Click "Slice now"
   - Use layer slider at bottom
   - If layers show variation, terrain is there!

### Step 3: Check STL in MeshLab

```bash
# Install if needed
sudo apt-get install meshlab

# Open STL
meshlab your_tile.stl

# Check mesh:
# - Filters → Measure → Measure distance
# - Measure from bottom to top
# - If distance is very small, it's flat
```

## Solutions

### Solution 1: Re-generate STL with Correct Settings

**If DEMto3D settings were wrong:**

1. **Load tile in QGIS**
2. **Run DEMto3D with exact settings:**
   - Layer extent: Click leftmost magnifying glass
   - Model width: 330mm
   - Model height: 330mm
   - Model size spacing: 0.2mm
   - **Height (m): -2.18** ⚠️ CRITICAL
   - **Base height (mm): 0** ⚠️ CRITICAL
   - Vertical exaggeration: 6.0
   - Output: STL Binary

3. **Verify settings before exporting**

### Solution 2: Check if Tile Has Data

**If tile is genuinely flat:**

```bash
# Check tile data content
python3 scripts/check_tiles_for_stl.py

# If tile shows very low data percentage, it might be flat
# Skip these tiles - they don't need STL files
```

### Solution 3: Adjust View in PrusaSlicer

**If terrain is there but hard to see:**

1. **Rotate to side view:**
   - Right-click + drag
   - Rotate 90° to see from side

2. **Zoom in:**
   - Scroll wheel
   - Zoom in close to see detail

3. **Slice and check layers:**
   - Click "Slice now"
   - Use layer slider
   - Layers should show terrain variation

4. **Change view mode:**
   - Try different view modes
   - Some show detail better

## Expected Results

### Good STL (with terrain):
- **File size:** 10-100MB (depending on detail)
- **Z dimension:** 10-200mm (with 6x exaggeration)
- **Layer preview:** Shows variation across layers
- **Side view:** Shows elevation changes

### Flat STL (no terrain):
- **File size:** < 1MB
- **Z dimension:** < 1mm
- **Layer preview:** All layers identical
- **Side view:** Completely flat

## Quick Test

**To quickly check if STL has terrain:**

```bash
# In PrusaSlicer:
1. Import STL
2. Check Z dimension (bottom-right)
3. Rotate to side view (right-click + drag 90°)
4. If you see height variation, terrain is there!
5. If completely flat, re-check DEMto3D settings
```

## Still Flat?

If after all checks it's still flat:

1. **Verify original tile has elevation data:**
   - Check in QGIS
   - Verify min/max elevation values

2. **Re-run DEMto3D:**
   - Double-check all settings
   - Ensure "Height (m)" is filled correctly
   - Watch for any error messages

3. **Try a different tile:**
   - Some tiles might be genuinely flat
   - Try a tile from a different area

4. **Check DEMto3D log:**
   - Look for any warnings or errors
   - Processing Toolbox shows progress

## Summary

**Most common causes:**
1. ❌ DEMto3D "Height (m)" field not filled correctly
2. ❌ View angle - terrain is there but hard to see
3. ✅ Tile is actually flat (normal for some areas)

**Quick fix:**
- Rotate view to side (90°)
- Check Z dimension
- Slice and check layers
- If still flat, re-check DEMto3D settings
