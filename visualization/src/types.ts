export interface MapConfig {
  projection: {
    name: string
    region: string
    resolution: string
    coordinate_system: string
    bounds: {
      min_lon: number
      max_lon: number
      min_lat: number
      max_lat: number
    }
  }
  display: {
    width: number
    height: number
    fps: number
    sync_protocol: string
  }
  layers: {
    base?: {
      type: string
      visible: boolean
      opacity: number
    }
    overlays?: Layer[]
  }
  interaction?: {
    mode: string
    controllers: number
    split_regions: boolean
  }
}

export interface Layer {
  name: string
  type: string
  visible: boolean
  opacity: number
  source?: string
  style?: {
    fill_color?: string
    stroke_color?: string
    stroke_width?: number
  }
}

export interface GeoJSONFeature {
  type: string
  properties: Record<string, any>
  geometry: {
    type: string
    coordinates: any
  }
}

export interface GeoJSONData {
  type: string
  features: GeoJSONFeature[]
}
