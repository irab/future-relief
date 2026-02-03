# Setup Guide

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- Git

## Initial Setup

### 1. Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Node.js Environment

```bash
cd visualization
npm install
```

### 3. Mapbox Token

Create a `.env` file in the `visualization` directory:

```bash
cd visualization
echo "VITE_MAPBOX_TOKEN=your_mapbox_token_here" > .env
```

Get your Mapbox token from [mapbox.com](https://account.mapbox.com/access-tokens/)

## Data Preparation

### LiDAR Data Processing

1. Place your LiDAR files (`.las` or `.laz`) in `data/lidar/`

2. Process the LiDAR data:

```bash
python processing/lidar_processor.py \
  --input data/lidar/ \
  --output data/processed/ \
  --resolution 1.0
```

This will generate:
- `.ply` mesh files
- `.tif` DEM (Digital Elevation Model) files
- `_metadata.json` files with bounds and coordinate information

### GeoJSON Layer Preparation

Convert shapefiles or other geospatial formats to GeoJSON:

```bash
python processing/geojson_converter.py \
  --input path/to/your/shapefile.shp \
  --output data/geojson/ \
  --name buildings \
  --crs EPSG:2193
```

Place converted GeoJSON files in `data/geojson/` and update `config/map_layers.json` with the correct paths.

## Running the Visualization

### Development Mode

```bash
cd visualization
npm run dev
```

The visualization will be available at `http://localhost:3000`

### Production Build

```bash
cd visualization
npm run build
```

The built files will be in `visualization/dist/`

## Projection Mapping Setup

### Using MadMapper

1. Open MadMapper
2. Create a new project
3. Add a browser source pointing to your visualization URL
4. Calibrate the projection to match your physical 3D model

### Browser-Based Projection

1. Open the visualization in a fullscreen browser window
2. Use browser developer tools to disable UI overlays if needed
3. Configure display settings in `config/projection_config.json`

## Configuration

### Projection Settings

Edit `config/projection_config.json` to adjust:
- Display resolution and dimensions
- Coordinate system and bounds
- Layer visibility and opacity

### Map Layers

Edit `config/map_layers.json` to:
- Add or remove map layers
- Configure layer styles (colors, stroke width)
- Define layer themes

## Troubleshooting

### LiDAR Processing Issues

- Ensure PDAL is properly installed if using PDAL-based processing
- Check that LAS/LAZ files are valid and not corrupted
- Verify coordinate system matches your data

### Visualization Issues

- Check browser console for errors
- Verify Mapbox token is set correctly
- Ensure GeoJSON files are valid and accessible
- Check CORS settings if loading data from external sources

### Projection Mapping Issues

- Verify display resolution matches projector output
- Check frame rate settings match your hardware capabilities
- Ensure network synchronization if using multiple projectors
