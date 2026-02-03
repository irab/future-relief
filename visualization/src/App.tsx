import { useState, useEffect } from 'react'
import MapView from './components/MapView'
import LayerControls from './components/LayerControls'
import { loadConfig } from './utils/config'
import type { MapConfig, Layer } from './types'

function App() {
  const [config, setConfig] = useState<MapConfig | null>(null)
  const [layers, setLayers] = useState<Layer[]>([])
  const [visibleLayers, setVisibleLayers] = useState<Set<string>>(new Set())

  useEffect(() => {
    loadConfig().then((loadedConfig) => {
      setConfig(loadedConfig)
      setLayers(loadedConfig.layers.overlays || [])
      // Set initial visible layers
      const initialVisible = new Set(
        loadedConfig.layers.overlays
          ?.filter((layer) => layer.visible)
          .map((layer) => layer.name) || []
      )
      if (loadedConfig.layers.base?.visible) {
        initialVisible.add('base')
      }
      setVisibleLayers(initialVisible)
    })
  }, [])

  const toggleLayer = (layerName: string) => {
    setVisibleLayers((prev) => {
      const next = new Set(prev)
      if (next.has(layerName)) {
        next.delete(layerName)
      } else {
        next.add(layerName)
      }
      return next
    })
  }

  if (!config) {
    return <div>Loading configuration...</div>
  }

  return (
    <div className="map-container">
      <MapView config={config} visibleLayers={visibleLayers} />
      <div className="map-overlay">
        <h2>Wellington 3D Map</h2>
        <LayerControls
          layers={layers}
          visibleLayers={visibleLayers}
          onToggleLayer={toggleLayer}
        />
      </div>
    </div>
  )
}

export default App
