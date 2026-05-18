# Checking DEM Dimensions and Aspect Ratio

Guide to verify your DEM dimensions match your desired 2m x 1.5m print size.

## Step 1: Get DEM Dimensions in QGIS

1. **Right-click your merged DEM layer** → **Properties** → **Information** tab

2. **Find these values:**
   - **Width**: Number of pixels (e.g., 120000)
   - **Height**: Number of pixels (e.g., 90000)
   - **Extent**: Geographic coordinates
     - X min, X max (e.g., 1600000, 1650000)
     - Y min, Y max (e.g., 5400000, 5450000)

3. **Calculate Geographic Dimensions:**
   - **Width in meters** = X max - X min
   - **Height in meters** = Y max - Y min
   - Example: 1650000 - 1600000 = 50,000 meters (50 km)

## Step 2: Calculate Aspect Ratio

**Aspect Ratio = Width ÷ Height**

Example:
- Width: 50,000 meters
- Height: 37,500 meters
- Aspect Ratio: 50,000 ÷ 37,500 = **1.33:1** (or 4:3)

## Step 3: Compare to Print Size Ratio

**Your desired print size:**
- Width: 2000 mm (2 meters)
- Height: 1500 mm (1.5 meters)
- **Print Aspect Ratio**: 2000 ÷ 1500 = **1.33:1** (or 4:3)

**Note:** Your DEM is portrait (0.766:1), so 1.5m x 2m (portrait) would match better than 2m x 1.5m (landscape). You can use either orientation - just note that landscape will require cropping.

## Step 4: Verify Match

✅ **If aspect ratios match** (e.g., both 1.33:1):
- Your DEM will fit perfectly at 2m x 1.5m
- No cropping needed
- DEMto3D will scale it correctly

❌ **If aspect ratios don't match**:
- You'll need to either:
  - Crop the DEM to match 2m x 1.5m ratio
  - Adjust print dimensions to match DEM ratio
  - Accept some cropping/distortion

## Step 5: Calculate Scale Factor

To understand the scale of your print:

**Scale = Print Width ÷ Geographic Width**

Example:
- Geographic width: 50,000 meters (50 km)
- Print width: 2 meters (2000 mm)
- **Scale**: 2 ÷ 50,000 = **1:25,000** (1mm on print = 25 meters in reality)

Or:
- **1 meter on print = 25 kilometers in reality**

## Quick Method: Check in QGIS

### Method 1: Use Measure Tool

1. **Enable Measure Tool**: Click the ruler icon in toolbar
2. **Measure width**: Click two points across the DEM (east-west)
3. **Measure height**: Click two points across the DEM (north-south)
4. **Note the distances** shown in the measurement panel
5. **Calculate ratio**: Width ÷ Height

### Method 2: Check Layer Properties

1. **Properties** → **Information** tab
2. Look for **Extent** section:
   ```
   Extent
   X min: 1600000.0
   X max: 1650000.0
   Y min: 5400000.0
   Y max: 5450000.0
   ```
3. Calculate:
   - Width = X max - X min
   - Height = Y max - Y min
   - Ratio = Width ÷ Height

### Method 3: Use Python Console (Advanced)

1. Open **Python Console** in QGIS (Plugins → Python Console)
2. Run:
   ```python
   layer = iface.activeLayer()
   extent = layer.extent()
   width = extent.width()
   height = extent.height()
   ratio = width / height
   print(f"Width: {width:.0f} meters")
   print(f"Height: {height:.0f} meters")
   print(f"Aspect Ratio: {ratio:.3f}:1")
   print(f"Print ratio (2m x 1.5m): 1.333:1")
   ```

## Example Calculation

**If your DEM has:**
- Geographic width: 60,000 meters (60 km)
- Geographic height: 45,000 meters (45 km)
- Aspect ratio: 60,000 ÷ 45,000 = **1.33:1**

**Your print size:**
- Width: 2000 mm
- Height: 1500 mm
- Aspect ratio: 2000 ÷ 1500 = **1.33:1**

✅ **Perfect match!** The DEM will fit exactly at 2m x 1.5m.

## If Ratios Don't Match

### Option 1: Crop DEM to Match Print Ratio

1. Calculate target geographic dimensions:
   - If DEM width is 60,000m and ratio is 1.33:1
   - Target height = 60,000 ÷ 1.33 = 45,113m
   - Crop to: 60,000m x 45,113m

2. **Clip Raster by Extent**:
   - **Raster** → **Extraction** → **Clip Raster by Extent**
   - Set extent to match 1.33:1 ratio
   - Use the cropped layer for STL conversion

### Option 2: Adjust Print Dimensions

If DEM ratio is different (e.g., 1.5:1):
- Calculate new print dimensions:
  - If keeping width at 2000mm: Height = 2000 ÷ 1.5 = 1333mm
  - Or adjust both to maintain detail

### Option 3: Accept Cropping

- Use DEMto3D with 2m x 1.5m settings
- It will crop the DEM to fit the aspect ratio
- Some areas may be cut off

## For Tiling (Prusa XL)

When creating 330mm x 330mm tiles:

**Each tile should maintain the same aspect ratio:**
- If full map is 1.33:1 (2m x 1.5m)
- Each 330mm tile should also be square (1:1) OR
- Maintain 1.33:1 ratio per tile: 330mm x 248mm

**Recommendation**: Use square tiles (330mm x 330mm) for easier assembly, even if it means slight cropping.

## Quick Check Script

You can also check dimensions using GDAL from command line:

```bash
gdalinfo data/processed/merged_full_area.tif | grep -E "Size is|Upper Left|Lower Right"
```

This will show pixel dimensions and geographic extent.
