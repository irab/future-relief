# Wellington 3D Map Projection Mapping

A projection mapping system for visualizing maps and data on a 1m resolution LiDAR map of the Wellington region, inspired by the Gaia System approach.

## Overview

This project enables projection mapping of various map layers and data visualizations onto a physical 3D model of the Wellington region using high-resolution LiDAR data. The system supports:

- LiDAR data processing and 3D model generation
- Multi-layer map visualization
- Real-time data integration
- Interactive touchscreen controls
- Projection mapping output for MadMapper or similar software

## Project Structure

```
3d-map/
├── data/                  # Raw and processed data
│   ├── lidar/            # LiDAR point cloud data
│   ├── geojson/          # GeoJSON map layers
│   ├── json/             # JSON metadata and narratives
│   └── processed/        # Processed 3D models and textures
├── processing/            # Data processing scripts
│   ├── lidar_processor.py
│   ├── geojson_converter.py
│   └── model_generator.py
├── visualization/        # Web-based visualization
│   ├── src/              # React/TypeScript source
│   ├── public/           # Static assets
│   └── package.json
├── config/               # Configuration files
│   ├── projection_config.json
│   └── map_layers.json
└── docs/                 # Documentation
```

## Requirements

- Python 3.9+
- Node.js 18+
- LiDAR processing libraries (PDAL, laspy, etc.)
- WebGL-capable browser
- Projection mapping software (MadMapper recommended)

## Setup

### Python Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Node.js Environment

```bash
cd visualization
npm install
```

## Usage

### Quick Start with Example Data

Create example GeoJSON files for testing:

```bash
python scripts/setup_example_data.py
```

### Processing LiDAR Data

Place your LiDAR files (`.las` or `.laz`) in `data/lidar/`, then:

```bash
python processing/lidar_processor.py --input data/lidar/ --output data/processed/
```

### Starting Visualization Server

1. Set up your Mapbox token in `visualization/.env`:
   ```
   VITE_MAPBOX_TOKEN=your_token_here
   ```

2. Start the development server:
   ```bash
   cd visualization
   npm install
   npm run dev
   ```

3. Open `http://localhost:3000` in your browser

### Projection Mapping

1. Open the web interface in a browser
2. Configure projection settings in `config/projection_config.json`
3. Export to MadMapper or use browser-based projection

## Data Sources

- Wellington LiDAR data (1m resolution)
- LINZ (Land Information New Zealand) for base maps
- OpenStreetMap for additional layers
- Real-time APIs as needed

## References

- [The Gaia System Paper](https://www.mdpi.com/2813-2084/4/4/49)
- [Gaia System Video](https://www.youtube.com/watch?v=11_Q1gfUPxw)

## License

[Add your license here]
