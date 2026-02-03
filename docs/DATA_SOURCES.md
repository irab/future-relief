# Data Sources for Wellington 3D Map

This document lists recommended data sources for the Wellington region projection mapping project.

## LiDAR Data

### New Zealand LiDAR Data

- **LINZ Data Service**: [data.linz.govt.nz](https://data.linz.govt.nz/)
  - Search for "LiDAR" or "Wellington"
  - Available formats: LAS, LAZ
  - Coordinate system: NZGD2000 (EPSG:2193)

- **OpenTopography**: [opentopography.org](https://opentopography.org/)
  - Global LiDAR data repository
  - May have Wellington region datasets

## Base Map Data

### LINZ (Land Information New Zealand)

- **Topo50 Maps**: High-resolution topographic maps
- **NZ Building Outlines**: Building footprints
- **NZ Roads**: Road centerlines and attributes
- **NZ Coastlines**: Coastline data
- **NZ Place Names**: Geographic place names

Access via: [data.linz.govt.nz](https://data.linz.govt.nz/)

### OpenStreetMap

- **OSM Data**: [download.geofabrik.de](https://download.geofabrik.de/australia-oceania/new-zealand.html)
  - Complete OSM data for New Zealand
  - Includes buildings, roads, water, etc.
  - Can be converted to GeoJSON using tools like `osmium` or `ogr2ogr`

## Administrative Boundaries

- **Territorial Authorities**: Wellington City, Lower Hutt, Upper Hutt, Porirua, Kapiti Coast
- **Regional Boundaries**: Greater Wellington Region
- Available from LINZ Data Service

## Elevation Data

- **NZ DEM**: Digital Elevation Models from LINZ
- **SRTM**: Global 30m resolution (backup option)
- **Aster GDEM**: Global 30m resolution

## Real-Time Data Sources

### Weather

- **MetService API**: Weather data for Wellington
- **OpenWeatherMap**: Weather API

### Transport

- **Greater Wellington Regional Council**: Public transport data
- **Waka Kotahi (NZTA)**: Road conditions and traffic

### Marine

- **LINZ Hydrographic Service**: Marine charts and data
- **NIWA**: Oceanographic data

## Data Processing Workflow

1. **Download LiDAR data** → Place in `data/lidar/`
2. **Process LiDAR** → Run `processing/lidar_processor.py`
3. **Download base map data** → Convert to GeoJSON using `processing/geojson_converter.py`
4. **Place GeoJSON files** → In `data/geojson/`
5. **Update configuration** → Edit `config/map_layers.json` with file paths

## Coordinate Systems

- **Input**: NZGD2000 / New Zealand Transverse Mercator 2000 (EPSG:2193)
- **Web Display**: WGS84 Web Mercator (EPSG:3857) or WGS84 (EPSG:4326)
- **Projection Mapping**: Match your physical model coordinate system

## Data Formats

- **LiDAR**: LAS/LAZ (point clouds)
- **Vector**: GeoJSON, Shapefile, GeoPackage
- **Raster**: GeoTIFF (for DEMs and imagery)
- **Metadata**: JSON

## Useful Tools

- **QGIS**: For viewing and converting geospatial data
- **GDAL/OGR**: Command-line tools for data conversion
- **PDAL**: Point cloud processing
- **CloudCompare**: Point cloud visualization and processing
