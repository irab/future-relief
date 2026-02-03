# Data Directory

This directory contains all data files for the Wellington 3D Map projection mapping project.

## Structure

- `lidar/` - Raw LiDAR point cloud files (`.las`, `.laz`)
- `geojson/` - GeoJSON map layers (buildings, roads, water, etc.)
- `json/` - JSON metadata files and narrative content
- `processed/` - Processed outputs (meshes, DEMs, textures)

## Data Sources

### LiDAR Data
- Wellington region 1m resolution LiDAR data
- Expected format: LAS/LAZ point cloud files
- Coordinate system: EPSG:2193 (NZGD2000 / New Zealand Transverse Mercator 2000)

### Map Layers
- LINZ (Land Information New Zealand) - Base maps, buildings, roads
- OpenStreetMap - Additional features
- Local government data - Regional boundaries, infrastructure

## Adding Data

1. Place LiDAR files in `lidar/` directory
2. Convert shapefiles/other formats to GeoJSON using `processing/geojson_converter.py`
3. Place GeoJSON files in `geojson/` directory
4. Update `config/map_layers.json` with new layer definitions

## File Naming Conventions

- LiDAR files: `wellington_*.las` or `wellington_*.laz`
- GeoJSON layers: `{layer_name}.geojson` (e.g., `buildings.geojson`, `roads.geojson`)
- Processed outputs: `{source_name}_{type}.{ext}` (e.g., `wellington_dem.tif`)
