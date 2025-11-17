import React from 'react'
import { cn } from '../../utils/classNames'
import { getCategoryColor } from '../../utils/colors'
import type { Category } from '../../types'

interface CategoryBadgeProps {
  category: Category
  size?: 'sm' | 'md'
  clickable?: boolean
  onClick?: () => void
  className?: string
}

const categoryLabels: Record<Category, string> = {
  built_environment: 'Built Environment',
  social_environment: 'Social Environment',
  economic: 'Economic',
  political: 'Political',
  biological: 'Biological',
  default: 'Default',
}

export const CategoryBadge: React.FC<CategoryBadgeProps> = ({
  category,
  size = 'md',
  clickable = false,
  onClick,
  className,
}) => {
  const color = getCategoryColor(category)
  const label = categoryLabels[category]

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-3 py-1 text-xs',
  }

  const Component = clickable ? 'button' : 'span'

  return (
    <Component
      className={cn(
        'inline-flex items-center rounded-full font-medium transition-colors',
        sizeClasses[size],
        clickable && 'cursor-pointer hover:opacity-80',
        className
      )}
      style={{
        backgroundColor: `${color}20`,
        color: color,
      }}
      onClick={onClick}
    >
      {label}
    </Component>
  )
}
