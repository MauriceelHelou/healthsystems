import React from 'react'
import { cn } from '../../utils/classNames'
import { getEvidenceColor, evidenceLabels } from '../../utils/colors'

interface EvidenceBadgeProps {
  quality: 'A' | 'B' | 'C' | null
  size?: 'sm' | 'md' | 'lg'
  showLabel?: boolean
  className?: string
}

export const EvidenceBadge: React.FC<EvidenceBadgeProps> = ({
  quality,
  size = 'md',
  showLabel = false,
  className,
}) => {
  const color = getEvidenceColor(quality)
  const label = quality ? evidenceLabels[quality] : evidenceLabels.null

  const sizeClasses = {
    sm: 'w-4 h-4 text-[10px]',
    md: 'w-6 h-6 text-xs',
    lg: 'w-8 h-8 text-sm',
  }

  return (
    <div className={cn('inline-flex items-center gap-2', className)}>
      <div
        className={cn(
          'rounded-full bg-white flex items-center justify-center font-bold border-2',
          sizeClasses[size]
        )}
        style={{ borderColor: color, color }}
        title={`Evidence Quality: ${label}`}
      >
        {quality || '?'}
      </div>
      {showLabel && (
        <span className="text-sm font-medium" style={{ color }}>
          {label}
        </span>
      )}
    </div>
  )
}
