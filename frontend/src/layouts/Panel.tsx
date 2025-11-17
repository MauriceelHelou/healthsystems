import React, { useRef, useState, useEffect } from 'react'
import { Button } from '../components/base/Button'
import { Icon } from '../components/base/Icon'
import { cn } from '../utils/classNames'

interface PanelProps {
  title: string
  icon?: React.ReactNode
  defaultWidth?: number
  minWidth?: number
  maxWidth?: number
  resizable?: boolean
  collapsible?: boolean
  onClose: () => void
  children: React.ReactNode
  footer?: React.ReactNode
}

export const Panel: React.FC<PanelProps> = ({
  title,
  icon,
  defaultWidth = 320,
  minWidth = 280,
  maxWidth = 480,
  resizable = true,
  collapsible = true,
  onClose,
  children,
  footer,
}) => {
  const [width, setWidth] = useState(defaultWidth)
  const [isResizing, setIsResizing] = useState(false)
  const [isExpanded, setIsExpanded] = useState(true)
  const panelRef = useRef<HTMLDivElement>(null)

  const handleMouseDown = (e: React.MouseEvent) => {
    e.preventDefault()
    setIsResizing(true)
  }

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isResizing) return
      const newWidth = window.innerWidth - e.clientX
      setWidth(Math.max(minWidth, Math.min(maxWidth, newWidth)))
    }

    const handleMouseUp = () => {
      setIsResizing(false)
    }

    if (isResizing) {
      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
    }
  }, [isResizing, minWidth, maxWidth])

  const toggleExpand = () => {
    if (isExpanded) {
      setWidth(400)
    } else {
      setWidth(320)
    }
    setIsExpanded(!isExpanded)
  }

  return (
    <aside
      ref={panelRef}
      className={cn(
        'bg-white border-l border-gray-200 flex flex-col overflow-hidden relative',
        'transition-all duration-300'
      )}
      style={{ width: `${width}px` }}
      role="complementary"
      aria-label={title}
    >
      {/* Resize Handle */}
      {resizable && (
        <div
          className={cn(
            'absolute left-0 top-0 bottom-0 w-1 cursor-col-resize hover:bg-primary-300 transition-colors z-10',
            isResizing && 'bg-primary-400'
          )}
          onMouseDown={handleMouseDown}
        />
      )}

      {/* Header */}
      <div className="h-12 flex items-center justify-between px-6 border-b border-gray-200 flex-shrink-0">
        <div className="flex items-center gap-2">
          {icon}
          <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
        </div>
        <div className="flex items-center gap-1">
          {collapsible && (
            <Button
              variant="icon"
              size="sm"
              onClick={toggleExpand}
              ariaLabel={isExpanded ? 'Collapse panel' : 'Expand panel'}
            >
              <Icon name={isExpanded ? 'chevron-left' : 'chevron-right'} size="sm" />
            </Button>
          )}
          <Button
            variant="icon"
            size="sm"
            onClick={onClose}
            ariaLabel="Close panel"
          >
            <Icon name="x" size="sm" />
          </Button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        {children}
      </div>

      {/* Footer */}
      {footer && (
        <div className="border-t border-gray-200 p-4 bg-gray-50 flex-shrink-0">
          {footer}
        </div>
      )}
    </aside>
  )
}
