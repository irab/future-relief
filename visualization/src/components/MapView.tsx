import { useEffect, useRef, useState } from 'react'
import mapboxgl from 'mapbox-gl'
import { GeoJsonLayer } from '@deck.gl/layers'
import DeckGL from '@deck.gl/react'
import { Map } from 'react-map-gl'
import type { MapConfig } from '../types'

interface MapViewProps {
  config: MapConfig
  visibleLayers: Set<string>
}

const INITIAL_VIEW_STATE = {
  longitude: 174.8,
  latitude: -41.25,
  zoom: 12,
  pitch: 60,
  bearing: 0,
}

export default function MapView({ config, visibleLayers }: MapViewProps) {
  const [layers, setLayers] = useState<any[]>([])
  const [viewState, setViewState] = useState(INITIAL_VIEW_STATE)

  useEffect(() => {
    // Update view state based on config bounds
    const centerLon = (config.projection.bounds.min_lon + config.projection.bounds.max_lon) / 2
    const centerLat = (config.projection.bounds.min_lat + config.projection.bounds.max_lat) / 2
    
    setViewState({
      ...viewState,
      longitude: centerLon,
      latitude: centerLat,
    })
  }, [config])

  useEffect(() => {
    // Load and update layers based on visibility
    const loadLayers = async () => {
      const newLayers: any[] = []

      for (const layerName of visibleLayers) {
        if (layerName === 'base') continue

        const layer = config.layers.overlays?.find((l) => l.name === layerName)
        if (!layer || !layer.source) continue

        try {
          const response = await fetch(layer.source)
          if (!response.ok) {
            console.warn(`Failed to load ${layer.source}`)
            continue
          }
          const geojson = await response.json()

          newLayers.push(
            new GeoJsonLayer({
              id: layerName,
              data: geojson,
              pickable: true,
              stroked: true,
              filled: true,
              extruded: false,
              lineWidthMinPixels: layer.style?.stroke_width || 1,
              getFillColor: layer.style?.fill_color
                ? hexToRgb(layer.style.fill_color, layer.opacity || 1.0)
                : [200, 200, 200, Math.round(180 * (layer.opacity || 1.0))],
              getLineColor: layer.style?.stroke_color
                ? hexToRgb(layer.style.stroke_color, 1.0)
                : [0, 0, 0, 255],
              getLineWidth: layer.style?.stroke_width || 1,
              opacity: layer.opacity || 1.0,
            })
          )
        } catch (error) {
          console.error(`Error loading layer ${layerName}:`, error)
        }
      }

      setLayers(newLayers)
    }

    loadLayers()
  }, [visibleLayers, config])

  return (
    <DeckGL
      viewState={viewState}
      onViewStateChange={({ viewState }) => setViewState(viewState)}
      controller={true}
      layers={layers}
    >
      <Map
        mapStyle="mapbox://styles/mapbox/satellite-v9"
        mapboxAccessToken={import.meta.env.VITE_MAPBOX_TOKEN || ''}
      />
    </DeckGL>
  )
}

function hexToRgb(hex: string, alpha: number = 1.0): [number, number, number, number] {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  if (result) {
    return [
      parseInt(result[1], 16),
      parseInt(result[2], 16),
      parseInt(result[3], 16),
      Math.round(255 * alpha),
    ]
  }
  return [0, 0, 0, 255]
}
