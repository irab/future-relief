#!/usr/bin/env python3
"""
Setup script to create example GeoJSON files for testing.
Creates sample data for Wellington region if no data exists.
"""

import json
from pathlib import Path

# Wellington region bounds (approximate)
WELLINGTON_BOUNDS = {
    "min_lon": 174.6,
    "max_lon": 175.0,
    "min_lat": -41.4,
    "max_lat": -41.1
}

def create_example_municipalities():
    """Create example municipalities GeoJSON."""
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": "Wellington City",
                    "municipality": "wellington_city"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [174.75, -41.25],
                        [174.85, -41.25],
                        [174.85, -41.30],
                        [174.75, -41.30],
                        [174.75, -41.25]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Lower Hutt",
                    "municipality": "lower_hutt"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [174.85, -41.20],
                        [174.95, -41.20],
                        [174.95, -41.28],
                        [174.85, -41.28],
                        [174.85, -41.20]
                    ]]
                }
            }
        ]
    }
    
    output_path = Path("data/geojson/municipalities.geojson")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(geojson, f, indent=2)
    
    print(f"Created example municipalities GeoJSON at {output_path}")

def create_example_buildings():
    """Create example buildings GeoJSON."""
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": "Example Building 1",
                    "height": 20
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [174.77, -41.27],
                        [174.78, -41.27],
                        [174.78, -41.28],
                        [174.77, -41.28],
                        [174.77, -41.27]
                    ]]
                }
            }
        ]
    }
    
    output_path = Path("data/geojson/buildings.geojson")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(geojson, f, indent=2)
    
    print(f"Created example buildings GeoJSON at {output_path}")

def create_example_roads():
    """Create example roads GeoJSON."""
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": "Example Road",
                    "type": "highway"
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [174.75, -41.27],
                        [174.80, -41.27],
                        [174.85, -41.25]
                    ]
                }
            }
        ]
    }
    
    output_path = Path("data/geojson/roads.geojson")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(geojson, f, indent=2)
    
    print(f"Created example roads GeoJSON at {output_path}")

def main():
    """Create example data files."""
    print("Creating example GeoJSON files...")
    create_example_municipalities()
    create_example_buildings()
    create_example_roads()
    print("\nExample data created! You can now:")
    print("1. Replace these with real data from LINZ or OpenStreetMap")
    print("2. Process your LiDAR data using processing/lidar_processor.py")
    print("3. Start the visualization with: cd visualization && npm run dev")

if __name__ == "__main__":
    main()
