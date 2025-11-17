import React from 'react'
import { cn } from '../../utils/classNames'

interface BadgeProps {
  variant?: 'default' | 'pill' | 'dot'
  color?: 'primary' | 'success' | 'warning' | 'error' | 'gray'
  size?: 'sm' | 'md' | 'lg'
  children?: React.ReactNode
  icon?: React.ReactNode
  className?: string
}

export const Badge: React.FC<BadgeProps> = ({
  variant = 'default',
  color = 'primary',
  size = 'md',
  children,
  icon,
  className,
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-medium'

  const variantStyles = {
    default: 'rounded',
    pill: 'rounded-full',
    dot: 'rounded-full',
  }

  const colorStyles = {
    primary: 'bg-primary-100 text-primary-700 border-primary-200',
    success: 'bg-green-100 text-green-700 border-green-200',
    warning: 'bg-amber-100 text-amber-700 border-amber-200',
    error: 'bg-red-100 text-red-700 border-red-200',
    gray: 'bg-gray-100 text-gray-700 border-gray-200',
  }

  const sizeStyles = {
    sm: variant === 'dot' ? 'w-2 h-2' : 'px-2 py-0.5 text-xs',
    md: variant === 'dot' ? 'w-3 h-3' : 'px-2.5 py-1 text-xs',
    lg: variant === 'dot' ? 'w-4 h-4' : 'px-3 py-1.5 text-sm',
  }

  if (variant === 'dot') {
    return (
      <span
        className={cn(
          baseStyles,
          variantStyles[variant],
          colorStyles[color].split(' ')[0], // Just bg color for dots
          sizeStyles[size],
          className
        )}
      />
    )
  }

  return (
    <span
      className={cn(
        baseStyles,
        variantStyles[variant],
        colorStyles[color],
        sizeStyles[size],
        icon && 'gap-1',
        className
      )}
    >
      {icon}
      {children}
    </span>
  )
}
