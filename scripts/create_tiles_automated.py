#!/usr/bin/env python3
"""
Automated Tile Creation Script for QGIS

This script automates the process of:
1. Creating a grid over your merged DEM
2. Clipping the DEM to each grid cell
3. Converting each tile to STL using DEMto3D

Usage:
    Run this script from QGIS Python Console or as a standalone script
"""

import os
from pathlib import Path
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsProcessingParameterFolderDestination,
    QgsProcessingOutputRasterLayer,
    QgsProcessingOutputVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsRectangle,
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProcessingException,
    QgsApplication,
    QgsProcessingRegistry,
    QgsProcessingAlgorithmProvider
)
from qgis import processing

def create_grid(extent, rows, cols, output_path, crs):
    """
    Create a grid covering the extent.
    
    Args:
        extent: QgsRectangle with the extent
        rows: Number of rows (vertical tiles)
        cols: Number of columns (horizontal tiles)
        output_path: Path to save grid shapefile
        crs: Coordinate reference system
    """
    width = extent.width()
    height = extent.height()
    
    h_spacing = width / cols
    v_spacing = height / rows
    
    print(f"Creating grid: {cols} columns × {rows} rows")
    print(f"Horizontal spacing: {h_spacing:.2f} meters")
    print(f"Vertical spacing: {v_spacing:.2f} meters")
    
    # Use QGIS processing algorithm
    params = {
        'TYPE': 0,  # Rectangle (grid)
        'EXTENT': extent,
        'HSPACING': h_spacing,
        'VSPACING': v_spacing,
        'HOVERLAY': 0,
        'VOVERLAY': 0,
        'CRS': crs,
        'OUTPUT': output_path
    }
    
    result = processing.run('qgis:creategrid', params)
    return result['OUTPUT']

def clip_raster_to_feature(raster_path, feature, output_path, feedback=None):
    """
    Clip raster to a single feature (grid cell).
    
    Args:
        raster_path: Path to input raster
        feature: QgsFeature (grid cell)
        output_path: Path to save clipped raster
        feedback: Processing feedback object
    """
    # Get feature geometry extent
    geom = feature.geometry()
    extent = geom.boundingBox()
    
    params = {
        'INPUT': raster_path,
        'PROJWIN': extent,
        'OUTPUT': output_path
    }
    
    result = processing.run('gdal:cliprasterbyextent', params, feedback=feedback)
    return result['OUTPUT']

def process_tiles_automated(
    raster_layer_path,
    output_dir,
    rows=5,
    cols=6,
    tile_width_mm=330,
    tile_height_mm=330,
    spacing_mm=0.2,
    height_m=-2.18,
    base_height_mm=0,
    exaggeration=6.0
):
    """
    Automate the entire tile creation process.
    
    Args:
        raster_layer_path: Path to merged DEM raster
        output_dir: Directory to save all outputs
        rows: Number of rows (default: 5)
        cols: Number of columns (default: 6)
        tile_width_mm: Width of each tile in mm (default: 330)
        tile_height_mm: Height of each tile in mm (default: 330)
        spacing_mm: Model size spacing in mm (default: 0.2)
        height_m: Base elevation in meters (default: -2.18)
        base_height_mm: Base height offset in mm (default: 0)
        exaggeration: Vertical exaggeration (default: 6.0)
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load raster layer
    raster_layer = QgsRasterLayer(raster_layer_path, "merged_dem")
    if not raster_layer.isValid():
        raise ValueError(f"Invalid raster layer: {raster_layer_path}")
    
    extent = raster_layer.extent()
    crs = raster_layer.crs()
    
    print(f"Raster extent: {extent.width():.2f}m × {extent.height():.2f}m")
    print(f"CRS: {crs.authid()}")
    
    # Create grid
    grid_path = str(output_path / "print_grid.shp")
    grid_layer_path = create_grid(extent, rows, cols, grid_path, crs)
    
    # Load grid layer
    grid_layer = QgsVectorLayer(grid_layer_path, "grid", "ogr")
    if not grid_layer.isValid():
        raise ValueError("Failed to create grid")
    
    # Process each grid cell
    total_tiles = rows * cols
    print(f"\nProcessing {total_tiles} tiles...")
    
    tile_count = 0
    for feature in grid_layer.getFeatures():
        tile_count += 1
        row = (tile_count - 1) // cols + 1
        col = (tile_count - 1) % cols + 1
        
        print(f"\nProcessing tile {tile_count}/{total_tiles} (Row {row}, Col {col})...")
        
        # Clip raster
        clipped_raster_path = str(output_path / f"tile_{row:02d}_{col:02d}.tif")
        print(f"  Clipping raster...")
        clip_raster_to_feature(raster_layer_path, feature, clipped_raster_path)
        
        # Note: DEMto3D conversion would need to be done manually or via plugin API
        # For now, we'll create the clipped rasters and provide instructions
        print(f"  Saved: {clipped_raster_path}")
    
    print(f"\n✓ Completed! Created {total_tiles} clipped raster tiles")
    print(f"\nNext step: Convert each tile to STL using DEMto3D plugin")
    print(f"  - Use settings: {tile_width_mm}mm × {tile_height_mm}mm")
    print(f"  - Spacing: {spacing_mm}mm")
    print(f"  - Height: {height_m}m")
    print(f"  - Exaggeration: {exaggeration}x")
    
    return grid_layer_path

# QGIS Processing Algorithm version (for use in QGIS)
class CreateTilesAlgorithm(QgsProcessingAlgorithm):
    """QGIS Processing Algorithm for automated tile creation."""
    
    INPUT_RASTER = 'INPUT_RASTER'
    OUTPUT_DIR = 'OUTPUT_DIR'
    ROWS = 'ROWS'
    COLS = 'COLS'
    TILE_WIDTH = 'TILE_WIDTH'
    TILE_HEIGHT = 'TILE_HEIGHT'
    
    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                'Input Raster Layer'
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT_DIR,
                'Output Directory'
            )
        )
        
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ROWS,
                'Number of Rows',
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=5
            )
        )
        
        self.addParameter(
            QgsProcessingParameterNumber(
                self.COLS,
                'Number of Columns',
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=6
            )
        )
    
    def processAlgorithm(self, parameters, context, feedback):
        raster_layer = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        output_dir = self.parameterAsString(parameters, self.OUTPUT_DIR, context)
        rows = self.parameterAsInt(parameters, self.ROWS, context)
        cols = self.parameterAsInt(parameters, self.COLS, context)
        
        process_tiles_automated(
            raster_layer.source(),
            output_dir,
            rows=rows,
            cols=cols
        )
        
        return {}
    
    def name(self):
        return 'createtiles'
    
    def displayName(self):
        return 'Create Print Tiles'
    
    def group(self):
        return 'Future Relief'
    
    def groupId(self):
        return 'futurerelief'
    
    def createInstance(self):
        return CreateTilesAlgorithm()

if __name__ == '__main__':
    # Example usage (when run from QGIS Python Console)
    # Adjust paths and parameters as needed
    
    raster_path = "/home/x/repos/future-relief/data/processed/merged_full_area.tif"
    output_dir = "/home/x/repos/future-relief/data/processed/tiles"
    
    process_tiles_automated(
        raster_path,
        output_dir,
        rows=5,
        cols=6
    )
