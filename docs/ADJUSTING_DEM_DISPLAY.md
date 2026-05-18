# Adjusting DEM Display in QGIS

If your merged DEM looks very dark or hard to see, it's usually a rendering/symbology issue, not a data problem. Here's how to fix it.

## Quick Fix: Adjust Symbology

1. **Right-click your merged DEM layer** → **Properties** → **Symbology** tab

2. **Change Render Type** (if needed):
   - Should be "Singleband gray" or "Singleband pseudocolor"
   - If it's something else, change to "Singleband gray"

3. **Adjust Min/Max Values**:
   - Click **Min / Max Value Settings** (or the "..." button)
   - Set **Min** to the minimum elevation (check Statistics tab for this)
   - Set **Max** to the maximum elevation
   - Or use **Cumulative count cut** (2% to 98%) for better contrast
   - Click **OK**

4. **Invert Colors** (if needed):
   - Check **Invert** if you want high elevations to be light (typical)
   - Uncheck if you want high elevations to be dark

5. **Apply and Close**

## Better Visualization Options

### Option 1: Hillshade (Recommended for Seeing Detail)

**Hillshade** creates a 3D-like shaded relief that makes terrain detail very visible:

1. **Symbology** tab → Change **Render type** to **Hillshade**

2. **Hillshade Settings**:
   - **Azimuth**: 315° (default - light from northwest, typical for terrain)
   - **Altitude**: 45° (default - good balance)
   - **Z factor**: 1.0 (default, or increase to 2-3 for more dramatic shading)
   - **Multidirectional**: Unchecked (or check for softer lighting)

3. **Click Apply** - You should immediately see much more terrain detail!

**Why Hillshade Works**: It simulates sunlight hitting the terrain, making elevation changes visible as light and shadow. This is excellent for seeing the 1m resolution detail, especially in low-lying areas.

### Option 2: Use Color Ramp

For a more intuitive terrain view:

1. **Symbology** tab → Change to **Singleband pseudocolor**

2. **Color ramp**: Choose a terrain-style ramp:
   - "Spectral" (rainbow)
   - "Terrain" (if available)
   - Or create custom: Green → Yellow → Brown → White

3. **Classification**:
   - **Mode**: Continuous
   - **Classes**: 10-20 (more = smoother gradient)

4. **Min/Max**: Set to your elevation range

### Option 3: Combine Hillshade with Color

For the best of both worlds:

1. Create a **hillshade layer** (as above)
2. Create a **pseudocolor layer** (as above)
3. Stack them: Put pseudocolor on bottom, hillshade on top
4. Set hillshade layer **Blending mode** to "Multiply" or "Overlay"
5. Adjust **Opacity** of hillshade layer (try 40-60%)

## Check Data is Correct

To verify the data itself is fine:

1. **Properties** → **Information** tab
   - Check dimensions (should be large)
   - Check coordinate system (EPSG:2193)

2. **Properties** → **Statistics** tab
   - Check Min/Max elevation values
   - These should be reasonable (e.g., 0-500m for coastal areas)
   - If all zeros or very strange values, there might be a data issue

3. **Use Identify Tool**:
   - Click the **Identify Features** tool (i icon)
   - Click on different areas of the map
   - Check elevation values - they should vary across the terrain

## Common Issues

### All Black/Dark
- **Cause**: Min/Max values not set correctly
- **Fix**: Set proper min/max in symbology, or use "Cumulative count cut"

### All White
- **Cause**: Colors inverted or min/max reversed
- **Fix**: Check "Invert" checkbox, or swap min/max values

### No Variation
- **Cause**: Min and max are the same, or very close
- **Fix**: Check statistics - if elevation range is very small, that's the data
- **Note**: This is why vertical exaggeration is needed for 3D printing

### Looks Wrong After Merge
- **Cause**: Sometimes merged files need symbology reset
- **Fix**: Remove layer, reload, and set symbology again

## Recommended Settings for Terrain Visualization

**For viewing/checking your merged DEM:**

**Best Option: Hillshade**
- **Render type**: Hillshade
- **Azimuth**: 315° (default)
- **Altitude**: 45° (default)
- **Z factor**: 1.0-2.0 (increase for more dramatic shading)

**Alternative: Color Ramp**
- **Render type**: Singleband pseudocolor
- **Color ramp**: Terrain or Spectral
- **Min/Max**: Use "Cumulative count cut" 2% to 98%
- **Classes**: 15-20

**Why Hillshade is Great**: It makes the 1m resolution detail very visible, especially in low-lying areas where elevation differences are subtle. The simulated lighting reveals terrain features that might not be obvious with color ramps alone.

## For STL Conversion

**Important**: The dark appearance doesn't affect STL conversion. The DEMto3D plugin reads the actual elevation values, not the visual representation. As long as:
- The data loads (no errors)
- Statistics show reasonable elevation values
- The file has the correct dimensions

Then you're good to proceed with STL conversion, regardless of how dark it looks!
