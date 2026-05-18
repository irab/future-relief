# Creating Test Tiles for Prusa XL

Step-by-step guide to create two test tiles (0.2mm and 0.3mm spacing) to compare print quality.

## Step 1: Clip Two Test Areas from Merged DEM

You'll create two small test areas from your merged DEM.

### Option A: Clip by Drawing (Easiest)

1. **Zoom to an interesting area** in your merged DEM
   - Choose an area with varied terrain (hills, valleys)
   - Make sure it's visible on screen

2. **Clip Raster by Extent**:
   - Go to **Raster** → **Extraction** → **Clip Raster by Extent**
   - **Input layer**: Select your `merged_full_area` layer
   - **Clipped (extent)**: Click the dropdown → **Calculate from Layer** → Select `merged_full_area`
   - **OR** click the "..." button and **Draw on Canvas**
     - Draw a rectangle around your test area (about 1/6th of the map width)
   - **Output file**: `data/processed/test_tile_area.tif`
   - Click **Run**

3. **Repeat for Second Test Area**:
   - Zoom to a different interesting area
   - Repeat the clip process
   - **Output file**: `data/processed/test_tile_area_2.tif`

### Option B: Clip by Coordinates (More Precise)

1. **Get Extent of Your Merged DEM**:
   - Right-click `merged_full_area` → **Properties** → **Information**
   - Note the extent coordinates (e.g., X: 1600000 to 1650000, Y: 5400000 to 5450000)

2. **Calculate Test Tile Extent**:
   - For a 330mm tile at your scale, calculate the geographic extent
   - Example: If your DEM is 50km wide and you want 330mm = 1/6th of 2m = 1/6th of area
   - Calculate: (max_x - min_x) / 6 = tile width in meters
   - Calculate: (max_y - min_y) / 5 = tile height in meters

3. **Clip First Test Tile**:
   - **Raster** → **Extraction** → **Clip Raster by Extent**
   - **Input layer**: `merged_full_area`
   - **Clipped (extent)**: Enter coordinates manually
     - X min: [your calculated value]
     - X max: [your calculated value + tile width]
     - Y min: [your calculated value]
     - Y max: [your calculated value + tile height]
   - **Output file**: `data/processed/test_tile_01.tif`
   - Click **Run**

4. **Clip Second Test Tile**:
   - Use different coordinates (adjacent area or different region)
   - **Output file**: `data/processed/test_tile_02.tif`
   - Click **Run**

## Step 2: Convert First Test Tile to STL (0.2mm spacing)

1. **Select the first test tile layer** (e.g., `test_tile_01`)

2. **Open DEMto3D**:
   - **Raster** → **DEMto3D** → **DEM 3D Printing**

3. **Configure Settings for 0.2mm Test**:

   **Model Dimensions:**
   - **Model width**: `330` mm
   - **Model height**: `330` mm

   **Model Settings:**
   - **Model size spacing**: `0.2` mm ⭐ (this is the key difference)
   - **Model height**: `-2.18` (your minimum elevation)

   **Vertical Exaggeration:**
   - **6.0x** (recommended - provides good terrain visibility)
   - Creates ~186mm terrain height (fits in 360mm bed)

   **Output:**
   - **Output file**: `output/test_tile_0.2mm.stl`
   - **Format**: STL Binary

4. **Click OK** and wait for processing (5-15 minutes)

## Step 3: Convert Second Test Tile to STL (0.3mm spacing)

1. **Select the second test tile layer** (e.g., `test_tile_02`)

2. **Open DEMto3D**:
   - **Raster** → **DEMto3D** → **DEM 3D Printing**

3. **Configure Settings for 0.3mm Test**:

   **Model Dimensions:**
   - **Model width**: `330` mm
   - **Model height**: `330` mm

   **Model Settings:**
   - **Model size spacing**: `0.3` mm ⭐ (this is the key difference)
   - **Model height**: `-2.18` (your minimum elevation)
   - **Note**: Add 20mm base in PrusaSlicer (see [Adding a Base](ADDING_BASE.md))
   
   **Vertical Exaggeration:**
   - **6.0x** (same as first test)

   **Output:**
   - **Output file**: `output/test_tile_0.3mm.stl`
   - **Format**: STL Binary

4. **Click OK** and wait for processing (3-10 minutes, faster than 0.2mm)

## Step 4: Prepare for Printing in PrusaSlicer

1. **Open PrusaSlicer**

2. **Load First STL** (`test_tile_0.2mm.stl`):
   - **File** → **Import** → Select `test_tile_0.2mm.stl`
   - Verify it fits on the bed (should be 330mm x 330mm or smaller)

3. **Configure Print Settings for 0.2mm Test**:
   - **Layer height**: `0.2` mm
   - **Infill**: `10-15%`
   - **Pattern**: Gyroid or Cubic
   - **Supports**: Usually not needed (printing base-down)
   - **Brim**: `5-10mm` (helps with adhesion)
   - **First layer speed**: `20-30` mm/s
   - **Material**: PLA (recommended)

4. **Save as**: `test_tile_0.2mm.gcode`

5. **Repeat for Second STL** (`test_tile_0.3mm.stl`):
   - Load the 0.3mm STL
   - Use **same print settings** (layer height 0.2mm, etc.)
   - Save as: `test_tile_0.3mm.gcode`

## Step 5: Print and Compare

1. **Print First Tile** (0.2mm spacing):
   - Load `test_tile_0.2mm.gcode`
   - Start print
   - Note print time
   - After printing, examine detail quality

2. **Print Second Tile** (0.3mm spacing):
   - Load `test_tile_0.3mm.gcode`
   - Start print
   - Note print time
   - After printing, examine detail quality

3. **Compare Results**:
   - **Detail quality**: Which shows terrain features better?
   - **Print time**: How much faster is 0.3mm?
   - **File size**: Check STL file sizes (0.3mm should be smaller)
   - **Surface smoothness**: Which looks better?

## What to Look For

### 0.2mm Spacing (Higher Detail)
- ✅ More terrain detail visible
- ✅ Smoother surfaces
- ❌ Larger file size
- ❌ Longer processing time
- ❌ Longer print time

### 0.3mm Spacing (Faster)
- ✅ Smaller file size
- ✅ Faster processing
- ✅ Faster printing
- ❌ Slightly less detail
- ❌ May miss very fine terrain features

## Decision Guide

**Choose 0.2mm if:**
- Detail is most important
- You have time for longer processing/printing
- Terrain has many fine features

**Choose 0.3mm if:**
- Speed is important
- Detail difference is minimal
- You're printing 30 tiles (saves significant time)

**Compromise:**
- Use 0.2mm for important/interesting areas
- Use 0.3mm for flatter/less interesting areas

## Quick Reference: Settings Summary

### Test Tile 1 (0.2mm)
- Model size spacing: **0.2mm**
- Model dimensions: 330mm x 330mm
- Vertical exaggeration: **6.0x**
- Model height: -2.18 meters
- Output: `test_tile_0.2mm.stl`

### Test Tile 2 (0.3mm)
- Model size spacing: **0.3mm**
- Model dimensions: 330mm x 330mm
- Vertical exaggeration: **6.0x**
- Model height: -2.18 meters
- Output: `test_tile_0.3mm.stl`

### Print Settings (Both)
- Layer height: 0.2mm
- Infill: 10-15%
- Brim: 5-10mm
- Material: PLA

## Next Steps

After comparing the two test tiles:
1. Decide which spacing works best for your needs
2. Use that setting for all 30 production tiles
3. Follow the full tiling workflow in `docs/PRUSA_XL_SETTINGS.md`
