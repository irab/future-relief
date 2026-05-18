# Adding a Base to Your Terrain Model

Two approaches for adding a 20mm base to your 3D printed terrain model.

## Option 1: Add in QGIS/DEMto3D

### Settings:
- **Model height**: `-166.1` meters (instead of `-2.18`)
- This creates a 20mm base that follows the terrain shape

### Pros:
- ✅ Base follows terrain shape (more accurate)
- ✅ Accounts for sea level and below
- ✅ Base is part of the STL mesh
- ✅ One-step process

### Cons:
- ❌ Base surface follows terrain (not perfectly flat)
- ❌ Harder to adjust later
- ❌ Base might have slight variations

## Option 2: Add in PrusaSlicer (Recommended)

### Settings in DEMto3D:
- **Model height**: `-2.18` meters (keep original)
- Generate STL normally

### Then in PrusaSlicer:

1. **Load your STL**

2. **Add a Flat Base:**
   - **Right-click model** → **Add Pad** (if available)
   - OR use **Modifiers** → **Add Support Enforcer** → Set as base
   - OR manually add a flat box in a 3D editor

3. **Better Method - Use Slicer Settings:**
   - **Print Settings** → **Support material**
   - **Raft**: Enable and set to 20mm height
   - OR use **Bottom solid layers**: Set to create 20mm base
     - Calculate: 20mm ÷ 0.2mm layer height = 100 layers
     - Set bottom layers to 100

4. **Easiest Method - Use "Add Pad" Feature:**
   - Some slicers have "Add Pad" or "Add Base" feature
   - Adds a flat base automatically
   - Adjustable thickness

## Recommendation: Use PrusaSlicer (Option 2)

### Why PrusaSlicer is Better:

1. **Perfectly Flat Base**
   - Ensures stable printing
   - Better bed adhesion
   - Professional appearance

2. **Easy to Adjust**
   - Change base thickness without regenerating STL
   - Try different thicknesses (15mm, 20mm, 25mm)
   - No need to re-run DEMto3D

3. **Standard Practice**
   - Most 3D printed terrain models use flat bases
   - Easier to assemble tiles (flat bases align better)
   - Better for display/assembly

4. **Flexibility**
   - Can remove base if needed
   - Can adjust per tile if needed
   - Can use different base thicknesses for different tiles

## How to Add Base in PrusaSlicer

### Method 1: Bottom Layers (Easiest)

1. **Load STL in PrusaSlicer**

2. **Print Settings** → **Infill and perimeters**

3. **Bottom solid layers**: Calculate for 20mm
   - Layer height: 0.2mm
   - Layers needed: 20mm ÷ 0.2mm = **100 layers**
   - Set **Bottom solid layers**: `100`

4. **Infill**: Set to 100% for base area
   - Use **Modifier meshes** to set base area to 100% infill
   - OR just use high bottom layers (they're already solid)

**Note**: This makes the bottom 20mm solid, which is what you want!

### Method 2: Add Pad Feature (If Available)

1. **Right-click model** → **Add Pad**
2. Set thickness: `20mm`
3. Adjust position to sit under terrain

### Method 3: Manual Base in 3D Editor

1. Open STL in Blender/MeshLab
2. Add a flat box (330mm x 330mm x 20mm)
3. Position under terrain
4. Merge meshes
5. Export new STL

## Recommended Workflow

### Step 1: Generate STL in QGIS
- Use **Model height**: `-2.18` meters (original)
- Generate STL normally
- This creates terrain starting at sea level

### Step 2: Add Base in PrusaSlicer
- Load STL
- Set **Bottom solid layers**: `100` (for 20mm at 0.2mm layers)
- OR use **Raft** with 20mm height
- This creates a perfectly flat 20mm base

### Result:
- ✅ Flat, stable base (20mm)
- ✅ Terrain sits on top
- ✅ Easy to adjust
- ✅ Professional appearance

## Settings Summary

### DEMto3D:
- Model height: `-2.18` meters (keep original)
- Vertical exaggeration: `6.0x`
- Generate STL

### PrusaSlicer:
- Bottom solid layers: `100` (20mm ÷ 0.2mm)
- OR Raft height: `20mm`
- Infill: 10-15% (above base)
- Top solid layers: 3-5

## Alternative: Hybrid Approach

If you want the base to follow terrain shape:

1. **DEMto3D**: Use `-166.1` meters (creates shaped base)
2. **PrusaSlicer**: Add flat layer on bottom (1-2mm)
   - Ensures flat contact with bed
   - Base still follows terrain above that

This gives you both: flat bed contact + terrain-shaped base.

## Bottom Line

**Use PrusaSlicer to add the base** - it's easier, more flexible, and creates a perfectly flat base for better printing and assembly.
