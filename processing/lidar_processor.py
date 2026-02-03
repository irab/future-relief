"""
LiDAR Data Processor for Wellington 3D Map

Processes LiDAR point cloud data into formats suitable for projection mapping.
Converts LAS/LAZ files to mesh models, DEMs, and projection-ready textures.
"""

import os
import argparse
import numpy as np
from pathlib import Path
import laspy
import open3d as o3d
from scipy.spatial import cKDTree
import rasterio
from rasterio.transform import from_bounds
import json


class LiDARProcessor:
    """Process LiDAR data for projection mapping."""
    
    def __init__(self, input_dir, output_dir, resolution=1.0):
        """
        Initialize processor.
        
        Args:
            input_dir: Directory containing LAS/LAZ files
            output_dir: Directory for processed outputs
            resolution: Target resolution in meters
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.resolution = resolution
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_lidar_file(self, filepath):
        """Load a LAS/LAZ file."""
        print(f"Loading {filepath}...")
        las = laspy.read(str(filepath))
        
        # Extract points
        points = np.vstack((las.x, las.y, las.z)).transpose()
        
        # Extract colors if available
        colors = None
        if hasattr(las, 'red') and hasattr(las, 'green') and hasattr(las, 'blue'):
            colors = np.vstack((las.red, las.green, las.blue)).transpose() / 65535.0
        
        return points, colors, las.header
    
    def create_point_cloud(self, points, colors=None):
        """Create Open3D point cloud object."""
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        
        if colors is not None:
            pcd.colors = o3d.utility.Vector3dVector(colors)
        
        return pcd
    
    def create_mesh(self, pcd, method='poisson'):
        """
        Create mesh from point cloud.
        
        Args:
            pcd: Open3D point cloud
            method: 'poisson' or 'ball_pivoting'
        """
        print(f"Creating mesh using {method} method...")
        
        if method == 'poisson':
            # Estimate normals
            pcd.estimate_normals(
                search_param=o3d.geometry.KDTreeSearchParamHybrid(
                    radius=0.1, max_nn=30
                )
            )
            pcd.orient_normals_consistent_tangent_plane(100)
            
            # Poisson surface reconstruction
            mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
                pcd, depth=9
            )
            
            # Remove low density vertices
            vertices_to_remove = densities < np.quantile(densities, 0.01)
            mesh.remove_vertices_by_mask(vertices_to_remove)
            
        elif method == 'ball_pivoting':
            # Estimate normals
            pcd.estimate_normals()
            
            # Ball pivoting
            distances = pcd.compute_nearest_neighbor_distance()
            avg_dist = np.mean(distances)
            radius = 3 * avg_dist
            
            radii = [radius, radius * 2, radius * 4]
            mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
                pcd, o3d.utility.DoubleVector(radii)
            )
        
        return mesh
    
    def create_dem(self, points, bounds, output_path):
        """
        Create Digital Elevation Model (DEM) from points.
        
        Args:
            points: Nx3 array of points
            bounds: (min_x, min_y, max_x, max_y)
            output_path: Path to save GeoTIFF
        """
        print("Creating DEM...")
        min_x, min_y, max_x, max_y = bounds
        
        # Calculate grid dimensions
        width = int((max_x - min_x) / self.resolution)
        height = int((max_y - min_y) / self.resolution)
        
        # Create grid
        x = np.linspace(min_x, max_x, width)
        y = np.linspace(min_y, max_y, height)
        X, Y = np.meshgrid(x, y)
        
        # Interpolate Z values using nearest neighbor
        tree = cKDTree(points[:, :2])
        Z = np.zeros((height, width))
        
        grid_points = np.column_stack([X.ravel(), Y.ravel()])
        distances, indices = tree.query(grid_points, k=1)
        Z = points[indices, 2].reshape(height, width)
        
        # Create transform
        transform = from_bounds(min_x, min_y, max_x, max_y, width, height)
        
        # Write GeoTIFF
        with rasterio.open(
            output_path,
            'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=Z.dtype,
            crs='EPSG:2193',  # NZGD2000 / New Zealand Transverse Mercator 2000
            transform=transform,
            compress='lzw'
        ) as dst:
            dst.write(Z, 1)
        
        print(f"DEM saved to {output_path}")
    
    def process_file(self, filepath, output_name=None):
        """Process a single LiDAR file."""
        points, colors, header = self.load_lidar_file(filepath)
        
        # Calculate bounds
        bounds = (
            header.x_min, header.y_min,
            header.x_max, header.y_max
        )
        
        # Create point cloud
        pcd = self.create_point_cloud(points, colors)
        
        # Create mesh
        mesh = self.create_mesh(pcd, method='poisson')
        
        # Save mesh
        if output_name is None:
            output_name = Path(filepath).stem
        
        mesh_path = self.output_dir / f"{output_name}.ply"
        o3d.io.write_triangle_mesh(str(mesh_path), mesh)
        print(f"Mesh saved to {mesh_path}")
        
        # Create DEM
        dem_path = self.output_dir / f"{output_name}_dem.tif"
        self.create_dem(points, bounds, dem_path)
        
        # Save metadata
        metadata = {
            "bounds": bounds,
            "point_count": len(points),
            "resolution": self.resolution,
            "coordinate_system": "EPSG:2193"
        }
        
        metadata_path = self.output_dir / f"{output_name}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return mesh_path, dem_path, metadata_path
    
    def process_directory(self):
        """Process all LAS/LAZ files in input directory."""
        lidar_files = list(self.input_dir.glob("*.las")) + list(self.input_dir.glob("*.laz"))
        
        if not lidar_files:
            print(f"No LAS/LAZ files found in {self.input_dir}")
            return
        
        print(f"Found {len(lidar_files)} LiDAR files")
        
        for filepath in lidar_files:
            try:
                self.process_file(filepath)
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
                continue


def main():
    parser = argparse.ArgumentParser(description="Process LiDAR data for projection mapping")
    parser.add_argument("--input", "-i", required=True, help="Input directory with LAS/LAZ files")
    parser.add_argument("--output", "-o", required=True, help="Output directory for processed files")
    parser.add_argument("--resolution", "-r", type=float, default=1.0, help="Target resolution in meters")
    
    args = parser.parse_args()
    
    processor = LiDARProcessor(args.input, args.output, args.resolution)
    processor.process_directory()


if __name__ == "__main__":
    main()
