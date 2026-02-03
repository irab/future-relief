import type { MapConfig } from '../types'

export async function loadConfig(): Promise<MapConfig> {
  try {
    const response = await fetch('/config/projection_config.json')
    if (!response.ok) {
      throw new Error('Failed to load configuration')
    }
    return await response.json()
  } catch (error) {
    console.error('Error loading config:', error)
    console.log('Using default configuration')
    // Return default config
    return {
      projection: {
        name: 'Wellington 3D Map',
        region: 'Wellington',
        resolution: '1m',
        coordinate_system: 'EPSG:2193',
        bounds: {
          min_lon: 174.6,
          max_lon: 175.0,
          min_lat: -41.4,
          max_lat: -41.1,
        },
      },
      display: {
        width: 1920,
        height: 1080,
        fps: 60,
        sync_protocol: 'MQTT',
      },
      layers: {
        base: {
          type: 'lidar_terrain',
          visible: true,
          opacity: 1.0,
        },
        overlays: [],
      },
    }
  }
}
