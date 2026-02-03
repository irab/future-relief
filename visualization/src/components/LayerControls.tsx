import type { Layer } from '../types'

interface LayerControlsProps {
  layers: Layer[]
  visibleLayers: Set<string>
  onToggleLayer: (layerName: string) => void
}

export default function LayerControls({
  layers,
  visibleLayers,
  onToggleLayer,
}: LayerControlsProps) {
  return (
    <div className="layer-controls">
      {layers.map((layer) => (
        <div key={layer.name} className="layer-control">
          <input
            type="checkbox"
            id={layer.name}
            checked={visibleLayers.has(layer.name)}
            onChange={() => onToggleLayer(layer.name)}
          />
          <label htmlFor={layer.name}>{layer.name}</label>
        </div>
      ))}
    </div>
  )
}
