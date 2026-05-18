# Installing PrusaSlicer on Linux

PrusaSlicer is the recommended slicer for viewing and preparing your terrain STL files for 3D printing.

## Quick Installation (AppImage - Recommended)

The easiest way is to download the AppImage, which doesn't require installation:

### Step 1: Download PrusaSlicer

1. **Visit the PrusaSlicer download page:**
   - https://www.prusa3d.com/page/prusaslicer_424/
   - Or direct link: https://github.com/prusa3d/PrusaSlicer/releases

2. **Download the AppImage:**
   - Look for: `PrusaSlicer-*-linux-x64-GTK3-*.AppImage`
   - Choose the latest stable version
   - Save to your Downloads folder or `~/bin/`

### Step 2: Make it Executable

```bash
# Navigate to where you downloaded it
cd ~/Downloads  # or wherever you saved it

# Make it executable
chmod +x PrusaSlicer-*.AppImage
```

### Step 3: Run PrusaSlicer

```bash
# Run directly
./PrusaSlicer-*.AppImage

# Or move to a permanent location first
mkdir -p ~/bin
mv PrusaSlicer-*.AppImage ~/bin/prusaslicer
~/bin/prusaslicer
```

### Step 4: Create Desktop Entry (Optional)

To add PrusaSlicer to your applications menu:

```bash
# Create desktop entry
cat > ~/.local/share/applications/prusaslicer.desktop << 'EOF'
[Desktop Entry]
Name=PrusaSlicer
Comment=3D printing slicer
Exec=/home/x/bin/prusaslicer
Icon=prusaslicer
Type=Application
Categories=Graphics;3DGraphics;
EOF

# Update icon (optional - download icon separately)
```

## Alternative: Install from Package Manager

### Debian/Ubuntu (via Snap)

```bash
# Install via snap
sudo snap install prusa-slicer
```

### Arch Linux

```bash
# Install from AUR
yay -S prusa-slicer
# or
pacman -S prusa-slicer
```

## System Requirements

- **OS:** Linux (x86_64)
- **RAM:** 2GB minimum, 4GB+ recommended
- **Disk:** ~200MB for installation
- **Graphics:** OpenGL 2.1+ support

## First Run

1. **Launch PrusaSlicer**
   - The first time, it will ask for configuration
   - Select your printer: **Prusa XL** (or closest match)

2. **Configure Printer:**
   - Printer Settings → Machine Limits
   - Set bed size: **360mm × 360mm × 360mm**
   - Set nozzle size: **0.4mm** (or your size)

3. **Import Your STL:**
   - File → Import → Select your STL file
   - Check dimensions (should be 330mm × 330mm for tiles)

## Troubleshooting

### AppImage Won't Run

**Error:** "Permission denied"

**Solution:**
```bash
chmod +x PrusaSlicer-*.AppImage
```

**Error:** "Cannot execute binary file"

**Solution:**
- Ensure you downloaded the Linux version (not Windows/Mac)
- Check architecture: `uname -m` (should be x86_64)

### Missing Dependencies

**Error:** "libfuse.so.2: cannot open shared object file"

**Solution:**
```bash
# Install FUSE (for AppImage support)
sudo apt-get install fuse libfuse2
```

**Error:** Missing OpenGL libraries

**Solution:**
```bash
# Install OpenGL libraries
sudo apt-get install libgl1-mesa-glx libglu1-mesa
```

### Can't See 3D Preview

**Problem:** Black screen or no 3D view

**Solution:**
- Check graphics drivers are installed
- Try software rendering: `LIBGL_ALWAYS_SOFTWARE=1 ./PrusaSlicer-*.AppImage`

## Using PrusaSlicer for Your Terrain Tiles

### Import STL File

1. **File → Import** (or drag and drop)
2. Select your STL file (e.g., `tile_01_01.stl`)
3. File should appear on the build plate

### Check Dimensions

1. **Look at bottom-right corner:**
   - Should show: **330mm × 330mm** (for your tiles)
   - Height will vary based on terrain

2. **Verify in Object List:**
   - Right panel shows object dimensions
   - Check X, Y, Z values

### Preview Terrain

1. **Rotate view:**
   - Right-click + drag to rotate
   - Middle-click + drag to pan
   - Scroll to zoom

2. **Check terrain detail:**
   - Rotate to see elevation changes
   - Verify terrain looks correct
   - Check for any flat/empty areas

### Prepare for Printing

1. **Add base (20mm):**
   - See [Adding a Base](ADDING_BASE.md) for details
   - Print Settings → Infill and perimeters
   - Bottom solid layers: 100 (for 20mm at 0.2mm layers)

2. **Configure print settings:**
   - See [Prusa XL Settings](PRUSA_XL_SETTINGS.md) for details
   - Layer height: 0.2mm
   - Infill: 10-15%

3. **Slice:**
   - Click "Slice now" button
   - Preview layers to verify

## Quick Start Command

```bash
# Download and run in one go (if you have wget and know the URL)
cd ~/bin
wget https://github.com/prusa3d/PrusaSlicer/releases/download/version_2.8.0/PrusaSlicer-2.8.0-linux-x64-GTK3-202409121307.AppImage
chmod +x PrusaSlicer-*.AppImage
./PrusaSlicer-*.AppImage
```

**Note:** Replace the version number with the latest available version.

## Updating PrusaSlicer

### AppImage Method

1. Download new AppImage
2. Replace old one (or keep both)
3. Run new version

### Snap Method

```bash
sudo snap refresh prusa-slicer
```

## Summary

**Recommended method:** AppImage
- ✅ No installation needed
- ✅ Easy to update
- ✅ Doesn't affect system packages
- ✅ Works on most Linux distributions

**Quick install:**
```bash
# Download from Prusa website
# Make executable: chmod +x PrusaSlicer-*.AppImage
# Run: ./PrusaSlicer-*.AppImage
```

Once installed, you can import your terrain STL files and check them before printing!
