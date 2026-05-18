# STL File Viewers

Recommended tools for viewing and inspecting STL files before printing.

## Quick Recommendations

### For 3D Printing Workflow
- **PrusaSlicer** - You're already using this! Great for checking printability
- **Cura** - Popular alternative slicer with good preview

### For Quick Viewing
- **MeshLab** - Powerful, free, open-source
- **Blender** - Full 3D suite, free
- **FreeCAD** - CAD software with STL support

### For Simple Viewing
- **3D Viewer (Windows)** - Built-in on Windows
- **Online viewers** - No installation needed

## Detailed Options

### PrusaSlicer (Recommended for Your Workflow)

**Why use it:**
- ✅ You're already using it for slicing
- ✅ Shows exactly what will be printed
- ✅ Can check dimensions, supports, infill
- ✅ Preview layer-by-layer
- ✅ Free and open-source

**Installation:**
```bash
# Download from: https://www.prusa3d.com/page/prusaslicer_424/
# Or use AppImage (no installation needed)
```

**Usage:**
- File → Import → Select STL file
- Use mouse to rotate/zoom/pan
- Check dimensions in bottom-right
- Preview layers to see print path

### MeshLab

**Why use it:**
- ✅ Excellent for inspecting mesh quality
- ✅ Can repair meshes
- ✅ Measure distances
- ✅ Free and open-source
- ✅ Works great on Linux

**Installation:**
```bash
sudo apt-get install meshlab
```

**Usage:**
- File → Import Mesh → Select STL
- Right-click for context menu
- Filters → Measure → Measure distance
- Filters → Cleaning and Repairing → Remove duplicate faces

**Good for:**
- Checking mesh quality
- Finding holes or errors
- Measuring dimensions
- Repairing meshes

### Blender

**Why use it:**
- ✅ Full-featured 3D software
- ✅ Excellent visualization
- ✅ Can edit meshes
- ✅ Free and open-source

**Installation:**
```bash
sudo apt-get install blender
```

**Usage:**
- File → Import → STL
- Use mouse to navigate (middle-click to rotate)
- Can add materials, lighting for better visualization

**Good for:**
- High-quality visualization
- Editing meshes
- Creating renders

### FreeCAD

**Why use it:**
- ✅ CAD software with STL support
- ✅ Can measure precisely
- ✅ Free and open-source

**Installation:**
```bash
sudo apt-get install freecad
```

**Usage:**
- File → Open → Select STL
- Use measurement tools
- Can convert to other formats

### Online Viewers (No Installation)

**Options:**
- **3D Viewer** (Windows Store) - If on Windows
- **ViewSTL.com** - Upload and view online
- **GitHub** - STL files render in browser on GitHub

**Good for:**
- Quick checks
- Sharing with others
- No installation needed

## For Your Specific Use Case

### Recommended Workflow

1. **Quick check:** PrusaSlicer (you already have it)
   - Import STL
   - Check dimensions (should be 330mm × 330mm)
   - Preview to see terrain detail

2. **Detailed inspection:** MeshLab
   - Check mesh quality
   - Verify no holes or errors
   - Measure specific features

3. **Visualization:** Blender (optional)
   - Create nice renders
   - Better lighting/materials

## Installation Commands

### On Debian/Ubuntu

```bash
# MeshLab
sudo apt-get update
sudo apt-get install meshlab

# Blender
sudo apt-get install blender

# FreeCAD
sudo apt-get install freecad
```

### PrusaSlicer

Download AppImage from Prusa website (no installation needed):
```bash
chmod +x PrusaSlicer-*.AppImage
./PrusaSlicer-*.AppImage
```

## Quick Comparison

| Viewer | Best For | Ease of Use | Linux Support |
|--------|----------|-------------|---------------|
| PrusaSlicer | Print preview | ⭐⭐⭐⭐⭐ | ✅ |
| MeshLab | Mesh inspection | ⭐⭐⭐⭐ | ✅ |
| Blender | Visualization | ⭐⭐⭐ | ✅ |
| FreeCAD | Measurements | ⭐⭐⭐ | ✅ |
| Online | Quick checks | ⭐⭐⭐⭐⭐ | ✅ |

## Tips

### Checking Your Terrain Tiles

1. **Dimensions:**
   - Should be 330mm × 330mm
   - Check in PrusaSlicer (bottom-right corner)

2. **Terrain detail:**
   - Rotate to see elevation changes
   - Check that terrain looks correct
   - Verify no flat/empty areas (unless sea)

3. **Mesh quality:**
   - Use MeshLab to check for errors
   - Look for holes or non-manifold edges
   - Most slicers auto-repair, but good to check

4. **Printability:**
   - PrusaSlicer will show if there are issues
   - Check for overhangs that need supports
   - Verify base is flat

## Troubleshooting

### STL Won't Load

- **File too large:** Some viewers have size limits
- **Corrupted file:** Try opening in different viewer
- **Wrong format:** Ensure it's binary STL (not ASCII)

### Can't See Detail

- **Zoom in:** Use mouse wheel or zoom tool
- **Change view:** Rotate to see from different angles
- **Adjust lighting:** Some viewers have lighting controls

### Dimensions Look Wrong

- **Check units:** Some viewers use different units
- **Verify in PrusaSlicer:** Most accurate for print dimensions
- **Check STL file:** Use `grep` or hex editor to verify

## Summary

**For your workflow, I recommend:**

1. **Primary:** PrusaSlicer (you already have it!)
   - Best for checking printability
   - Shows exact print dimensions

2. **Secondary:** MeshLab
   - Great for detailed mesh inspection
   - Can repair if needed

Both are free, work on Linux, and will handle your terrain STL files perfectly!
