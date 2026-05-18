# 3D Printing Structure and Infill

Understanding how your terrain model will be printed and optimized.

## How Slicers Work (Automatic)

**You don't need to modify the STL!** The slicer (PrusaSlicer, Cura, etc.) automatically creates the optimal structure:

### Layer Structure (Bottom to Top):

1. **Bottom Layers (Solid)**
   - First few layers are 100% solid
   - Provides flat, stable base
   - Typically 3-5 layers (0.6-1.0mm thick)
   - Ensures good bed adhesion

2. **Infill (Hollow with Pattern)**
   - Interior uses your chosen infill percentage (10-20%)
   - Pattern: Gyroid, Cubic, or Grid
   - Strong but uses less material
   - Not solid - saves filament and time

3. **Top Layers (Solid)**
   - Last few layers are 100% solid
   - Creates smooth top surface
   - Typically 3-5 layers
   - Your terrain detail is here!

4. **Perimeters/Walls**
   - Outer walls are always solid
   - Typically 2-3 perimeters
   - Defines the shape and detail

## Recommended PrusaSlicer Settings

### For Your Terrain Model:

**Layer Settings:**
- **Layer height**: 0.2mm
- **First layer height**: 0.2mm (or 0.25mm for better adhesion)
- **Bottom solid layers**: 3-5 layers (0.6-1.0mm)
- **Top solid layers**: 3-5 layers (0.6-1.0mm)

**Infill:**
- **Infill density**: 10-15% (sufficient for terrain)
- **Infill pattern**: Gyroid or Cubic (strong, efficient)
- **Infill every N layers**: 1 (every layer)

**Perimeters:**
- **Perimeters**: 2-3 (defines detail)
- **External perimeters first**: Yes (better surface quality)

## What This Means for Your Model

### With 20mm Base:

**Structure:**
- **0-1mm**: Solid bottom layers (bed adhesion)
- **1-20mm**: Infill at 10-15% (hollow but strong)
- **20-206mm**: Terrain with infill (detailed surface, hollow interior)
- **Top**: Solid layers for smooth finish

**Benefits:**
- ✅ Strong structure (infill provides strength)
- ✅ Less material used (saves filament)
- ✅ Faster printing (less material to extrude)
- ✅ Detailed terrain surface (perimeters define shape)
- ✅ Stable base (solid bottom layers)

## Do You Need to Modify the STL?

### ❌ No Modification Needed

The STL from DEMto3D is perfect as-is. The slicer handles:
- Solid base layers
- Infill structure
- Top surface
- Detail preservation

### ✅ Optional: Add Supports (If Needed)

If your terrain has overhangs:
- Slicer can auto-generate supports
- Tree supports recommended (less material)
- Usually not needed for terrain (prints base-down)

## Material Savings

### Example Calculation:

**Solid Model (100% infill):**
- Volume: ~2,000 cm³
- Material: ~2,000g (2kg) of PLA
- Print time: ~40 hours

**With 15% Infill:**
- Volume: ~800 cm³ (60% reduction)
- Material: ~800g (0.8kg) of PLA
- Print time: ~20 hours (50% faster)

**Savings:**
- ✅ 1.2kg less filament
- ✅ 20 hours faster
- ✅ Still strong enough for display

## Strength Considerations

### Is 10-15% Infill Strong Enough?

**For Display/Art:**
- ✅ Yes, perfectly fine
- Terrain models are typically display pieces
- 10-15% provides adequate strength

**For Handling:**
- ✅ Yes, strong enough
- Perimeters provide most strength
- Infill prevents collapse

**For Heavy Use:**
- ⚠️ Consider 20-25% infill
- Or increase perimeters to 3-4

## Advanced: Variable Infill (Optional)

Some slicers support variable infill:
- **Base area**: 20-30% (more support)
- **Terrain area**: 10-15% (less material)
- **Peaks**: 15-20% (more strength)

This is optional - standard 10-15% works great.

## Bottom Line

**You don't need to modify the STL!**

The slicer automatically:
1. Creates solid base (bed adhesion)
2. Uses infill for interior (efficient, strong)
3. Preserves terrain detail (perimeters)
4. Creates solid top (smooth finish)

**Just use these settings:**
- Bottom layers: 3-5
- Infill: 10-15%
- Top layers: 3-5
- Perimeters: 2-3

Your model will be strong, detailed, and efficient!
