import { FC } from 'react'
import { scaleColors, scaleLabels, evidenceColors, evidenceLabels } from '../../utils/colors'

interface LegendProps {
  showEvidenceQuality?: boolean
  showScales?: boolean
  className?: string
}

export const Legend: FC<LegendProps> = ({
  showEvidenceQuality = true,
  showScales = true,
  className = '',
}) => {
  return (
    <div className={`legend bg-white rounded-lg shadow-md p-4 ${className}`} data-testid="systems-map-legend">
      <h3 className="text-sm font-semibold text-gray-900 mb-3">Legend</h3>

      {/* Scale System */}
      {showScales && (
        <div className="mb-4">
          <h4 className="text-xs font-medium text-gray-700 mb-2">7-Scale Hierarchy</h4>
          <div className="space-y-1.5">
            {[1, 2, 3, 4, 5, 6, 7].map((scale) => {
              const isReserved = scale === 2 || scale === 5
              return (
                <div key={scale} className="flex items-center gap-2">
                  <div
                    className="w-5 h-5 rounded-full flex items-center justify-center text-white text-xs font-bold"
                    style={{
                      backgroundColor: scaleColors[scale],
                      opacity: isReserved ? 0.4 : 1
                    }}
                  >
                    {scale}
                  </div>
                  <span className={`text-xs ${isReserved ? 'text-gray-500 italic' : 'text-gray-700'}`}>
                    {scaleLabels[scale]}
                    {isReserved && ' (Reserved)'}
                  </span>
                </div>
              )
            })}
          </div>
          <p className="text-xs text-gray-600 mt-2">
            Active scales: 1, 3, 4, 6, 7 | Reserved: 2, 5
          </p>
        </div>
      )}

      {/* Evidence Quality */}
      {showEvidenceQuality && (
        <div className="mb-4">
          <h4 className="text-xs font-medium text-gray-700 mb-2">Evidence Quality</h4>
          <div className="space-y-1.5">
            {(['A', 'B', 'C'] as const).map((quality) => (
              <div key={quality} className="flex items-center gap-2">
                <div
                  className="w-5 h-5 rounded-full flex items-center justify-center text-white text-xs font-bold border border-white"
                  style={{ backgroundColor: evidenceColors[quality] }}
                >
                  {quality}
                </div>
                <span className="text-xs text-gray-700">
                  {evidenceLabels[quality]} quality
                </span>
              </div>
            ))}
          </div>
          <p className="text-xs text-gray-600 mt-2">
            Badges on edges indicate strength of evidence
          </p>
        </div>
      )}

      {/* Additional Info */}
      <div className="pt-3 border-t border-gray-200">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-white border-2 border-gray-300 rounded"></div>
            <span className="text-xs text-gray-600">Node</span>
          </div>
          <div className="flex items-center gap-2">
            <svg width="20" height="8" className="flex-shrink-0">
              <line x1="0" y1="4" x2="20" y2="4" stroke="#D1D5DB" strokeWidth="2" markerEnd="url(#arrow-mini)"/>
              <defs>
                <marker id="arrow-mini" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
                  <polygon points="0 0, 6 3, 0 6" fill="#D1D5DB" />
                </marker>
              </defs>
            </svg>
            <span className="text-xs text-gray-600">Edge (mechanism)</span>
          </div>
        </div>
      </div>
    </div>
  )
}
