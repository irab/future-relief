# Troubleshooting Common Issues

This guide covers common errors and issues when working with GeoTIFF files and QGIS.

## Corrupted .aux File Errors

### Error: "Can't find RasterDMS field in Eimg_Layer with block list"

This error occurs when the `.aux` file (auxiliary metadata file) is corrupted or incompatible with your GDAL version.

**Solution 1: Delete and Regenerate .aux Files**

The `.aux` files are just cache files for statistics - they're not essential. You can safely delete them:

```bash
# Delete corrupted .aux files for a specific tile
rm lds-new-zealand-lidar-1m-dem-GTiff/BQ33.aux
rm lds-new-zealand-lidar-1m-dem-GTiff/BQ33.aux.aux.xml

# Or delete all .aux files at once (they'll be regenerated when needed)
find lds-new-zealand-lidar-1m-dem-GTiff/ -name "*.aux" -delete
find lds-new-zealand-lidar-1m-dem-GTiff/ -name "*.aux.aux.xml" -delete
```

**Solution 2: In QGIS**

1. Close QGIS if it's open
2. Delete the `.aux` files manually or using terminal
3. Reopen QGIS and load the layer again
4. QGIS/GDAL will regenerate the `.aux` files automatically

**Solution 3: Rebuild Statistics**

If you want to keep statistics but fix the corruption:

```bash
# Rebuild statistics using gdalinfo (this regenerates .aux files)
gdalinfo -stats lds-new-zealand-lidar-1m-dem-GTiff/BQ33.tif
```

### Other .aux File Issues

If multiple tiles have corrupted `.aux` files:

```bash
# Remove all .aux files (safe to do - they're just cache)
cd lds-new-zealand-lidar-1m-dem-GTiff/
rm -f *.aux *.aux.aux.xml
```

## QGIS Crashes or Freezes

### When Loading Multiple Large Tiles

**Symptoms:**
- QGIS becomes unresponsive
- System runs out of memory
- QGIS crashes

**Solutions:**

1. **Load Tiles in Batches**
   - Load 3-4 tiles at a time
   - Merge batches, then merge batch results

2. **Use Virtual Raster (VRT)**
   - **Raster** → **Miscellaneous** → **Build Virtual Raster**
   - Select all tiles
   - Creates a "virtual" merged file without combining data
   - Uses less memory

3. **Increase System Resources**
   - Close other applications
   - Increase swap space if needed
   - Use a machine with more RAM

4. **Process Outside QGIS**
   - Use GDAL command-line tools for merging
   - Then load the merged result in QGIS

## Out of Memory Errors

**When Merging Tiles:**

```bash
# Use GDAL command line with memory optimization
gdal_merge.py -o merged.tif -of GTiff \
  --config GDAL_CACHEMAX 2048 \
  lds-new-zealand-lidar-1m-dem-GTiff/*.tif
```

**In QGIS:**
- Process smaller batches
- Use VRT instead of full merge
- Close other applications

## File Won't Load in QGIS

### Check File Integrity

```bash
# Check if file is valid GeoTIFF
gdalinfo filename.tif

# If it fails, the file may be corrupted
```

### Rebuild Overviews

If file loads but is slow:

```bash
# Rebuild overviews (pyramids) for faster loading
gdaladdo -r average filename.tif 2 4 8 16
```

## STL Conversion Issues

### STL File Too Large

- Increase model size spacing (0.3mm or 0.5mm instead of 0.2mm)
- Use binary STL format (not ASCII)
- Clip to smaller area before conversion

### Terrain Too Flat

- Increase vertical exaggeration (try 3x, 5x, or higher)
- Check DEM statistics - ensure there's elevation variation

### Processing Takes Forever

- Increase model size spacing
- Process smaller areas
- Close other applications
- Check available RAM

## Coordinate System Issues

### Wrong CRS Detected

1. Right-click layer → **Set Layer CRS**
2. Select **EPSG:2193** (NZGD2000 / New Zealand Transverse Mercator 2000)
3. Ensure project CRS matches: **Project** → **Properties** → **CRS**

### Tiles Don't Align

- Ensure all tiles use the same CRS (EPSG:2193)
- Check that tiles are properly georeferenced
- Verify no coordinate transformation issues

## Disk Space Issues

### Running Out of Space During Merge

Merging 13GB+ of tiles requires:
- **At least 2x the input size** in free space (26GB+)
- More if creating overviews or processing

**Solutions:**
- Free up disk space
- Use external drive for output
- Process in smaller batches
- Use VRT (doesn't create large merged file)

## Performance Optimization

### QGIS is Slow

1. **Disable unnecessary plugins**
2. **Reduce layer rendering**
   - Right-click layer → **Properties** → **Rendering**
   - Reduce resolution or use overviews

3. **Use overviews (pyramids)**
   ```bash
   gdaladdo -r average filename.tif 2 4 8 16
   ```

4. **Process in smaller chunks**

### GDAL Command Line Tools

For better performance, use GDAL directly:

```bash
# Install GDAL tools (if not already installed)
sudo apt-get install gdal-bin python3-gdal

# Merge tiles
gdal_merge.py -o merged.tif *.tif

# Get file info
gdalinfo filename.tif

# Rebuild overviews
gdaladdo -r average filename.tif 2 4 8 16
```

## Getting Help

### Check File Integrity

```bash
# List all GeoTIFF files
ls -lh lds-new-zealand-lidar-1m-dem-GTiff/*.tif

# Check a specific file
gdalinfo lds-new-zealand-lidar-1m-dem-GTiff/BQ33.tif

# Check for corruption
file lds-new-zealand-lidar-1m-dem-GTiff/BQ33.tif
```

### QGIS Logs

Check QGIS logs for detailed error messages:
- **View** → **Panels** → **Log Messages**
- Look for GDAL/raster errors

### GDAL Version

Check your GDAL version (may affect compatibility):

```bash
gdalinfo --version
```

## Common File Extensions Explained

- **`.tif` / `.tiff`**: The actual GeoTIFF raster data
- **`.aux`**: Auxiliary file with statistics (can be deleted)
- **`.aux.xml`**: XML version of auxiliary data
- **`.tfw`**: World file with georeferencing info
- **`.xml`**: Metadata file
- **`.gfs`**: GDAL file system cache (can be deleted)

**Safe to delete:** `.aux`, `.aux.xml`, `.gfs` (they'll be regenerated)

**Don't delete:** `.tif`, `.tfw`, `.xml` (essential files)
