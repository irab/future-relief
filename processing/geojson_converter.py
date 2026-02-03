"""
GeoJSON Converter for Wellington Map Layers

Converts various geospatial data sources to GeoJSON format
for use in the projection mapping system.
"""

import json
import argparse
from pathlib import Path
import geopandas as gpd
from shapely.geometry import mapping
import fiona


class GeoJSONConverter:
    """Convert geospatial data to GeoJSON format."""
    
    def __init__(self, output_dir):
        """Initialize converter."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def convert_shapefile(self, shapefile_path, output_name, crs='EPSG:2193'):
        """
        Convert shapefile to GeoJSON.
        
        Args:
            shapefile_path: Path to shapefile
            output_name: Name for output GeoJSON file
            crs: Target coordinate reference system
        """
        print(f"Converting {shapefile_path} to GeoJSON...")
        
        gdf = gpd.read_file(shapefile_path)
        
        # Reproject if needed
        if gdf.crs != crs:
            gdf = gdf.to_crs(crs)
        
        # Save as GeoJSON
        output_path = self.output_dir / f"{output_name}.geojson"
        gdf.to_file(output_path, driver='GeoJSON')
        
        print(f"Saved to {output_path}")
        return output_path
    
    def convert_geopackage(self, gpkg_path, layer_name, output_name, crs='EPSG:2193'):
        """Convert GeoPackage layer to GeoJSON."""
        print(f"Converting GeoPackage layer {layer_name}...")
        
        gdf = gpd.read_file(gpkg_path, layer=layer_name)
        
        if gdf.crs != crs:
            gdf = gdf.to_crs(crs)
        
        output_path = self.output_dir / f"{output_name}.geojson"
        gdf.to_file(output_path, driver='GeoJSON')
        
        print(f"Saved to {output_path}")
        return output_path
    
    def filter_by_bounds(self, geojson_path, bounds, output_name):
        """
        Filter GeoJSON features by bounding box.
        
        Args:
            geojson_path: Path to input GeoJSON
            bounds: (min_x, min_y, max_x, max_y)
            output_name: Name for output file
        """
        from shapely.geometry import box
        
        gdf = gpd.read_file(geojson_path)
        bbox = box(*bounds)
        
        # Filter features that intersect with bounding box
        filtered = gdf[gdf.intersects(bbox)]
        
        output_path = self.output_dir / f"{output_name}.geojson"
        filtered.to_file(output_path, driver='GeoJSON')
        
        print(f"Filtered GeoJSON saved to {output_path}")
        return output_path
    
    def add_metadata(self, geojson_path, metadata):
        """
        Add metadata to GeoJSON file.
        
        Args:
            geojson_path: Path to GeoJSON file
            metadata: Dictionary of metadata to add
        """
        with open(geojson_path, 'r') as f:
            geojson = json.load(f)
        
        geojson['metadata'] = metadata
        
        with open(geojson_path, 'w') as f:
            json.dump(geojson, f, indent=2)
        
        print(f"Metadata added to {geojson_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert geospatial data to GeoJSON")
    parser.add_argument("--input", "-i", required=True, help="Input file (shapefile, GeoPackage, etc.)")
    parser.add_argument("--output", "-o", required=True, help="Output directory")
    parser.add_argument("--name", "-n", required=True, help="Output filename (without extension)")
    parser.add_argument("--layer", "-l", help="Layer name (for GeoPackage)")
    parser.add_argument("--crs", default="EPSG:2193", help="Target CRS")
    
    args = parser.parse_args()
    
    converter = GeoJSONConverter(args.output)
    
    input_path = Path(args.input)
    
    if input_path.suffix == '.shp':
        converter.convert_shapefile(args.input, args.name, args.crs)
    elif input_path.suffix == '.gpkg':
        if not args.layer:
            print("Error: --layer required for GeoPackage files")
            return
        converter.convert_geopackage(args.input, args.layer, args.name, args.crs)
    else:
        print(f"Unsupported file format: {input_path.suffix}")


if __name__ == "__main__":
    main()
