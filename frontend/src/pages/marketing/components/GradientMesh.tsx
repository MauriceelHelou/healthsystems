'use client';

import { useEffect, useRef, useState } from 'react';
import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

/**
 * GradientMesh Component
 *
 * Creates an animated gradient mesh background similar to Stripe's homepage.
 * Uses CSS gradients with smooth color transitions for performance.
 *
 * Features:
 * - Animated gradient that shifts colors over time
 * - Optional mouse interaction for parallax effect
 * - Respects prefers-reduced-motion
 * - Fully customizable colors
 */

interface GradientMeshProps {
  /** Array of 4 colors for the mesh gradient */
  colors?: [string, string, string, string];
  /** Animation speed in seconds (default: 15) */
  speed?: number;
  /** Enable mouse parallax effect */
  interactive?: boolean;
  /** Additional CSS classes */
  className?: string;
  /** Opacity of the gradient (0-1) */
  opacity?: number;
}

// Default colors matching the design system
const DEFAULT_COLORS: [string, string, string, string] = [
  '#0ea5e9', // primary-500 (blue)
  '#a855f7', // secondary-500 (purple)
  '#f97316', // orange-500
  '#10b981', // emerald-500
];

export function GradientMesh({
  colors = DEFAULT_COLORS,
  speed = 15,
  interactive = true,
  className,
  opacity = 0.5,
}: GradientMeshProps) {
  const shouldReduceMotion = useReducedMotion();
  const containerRef = useRef<HTMLDivElement>(null);
  const [mousePosition, setMousePosition] = useState({ x: 0.5, y: 0.5 });

  // Handle mouse movement for parallax effect
  useEffect(() => {
    if (!interactive || shouldReduceMotion) return;

    const handleMouseMove = (e: MouseEvent) => {
      if (!containerRef.current) return;

      const rect = containerRef.current.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width;
      const y = (e.clientY - rect.top) / rect.height;

      setMousePosition({ x, y });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, [interactive, shouldReduceMotion]);

  // Calculate gradient positions based on mouse
  const getGradientStyle = () => {
    const baseX = interactive ? mousePosition.x * 20 : 0;
    const baseY = interactive ? mousePosition.y * 20 : 0;

    return {
      '--gradient-1-x': `${20 + baseX}%`,
      '--gradient-1-y': `${20 + baseY}%`,
      '--gradient-2-x': `${80 - baseX}%`,
      '--gradient-2-y': `${20 + baseY}%`,
      '--gradient-3-x': `${80 - baseX}%`,
      '--gradient-3-y': `${80 - baseY}%`,
      '--gradient-4-x': `${20 + baseX}%`,
      '--gradient-4-y': `${80 - baseY}%`,
    } as React.CSSProperties;
  };

  return (
    <div
      ref={containerRef}
      className={cn(
        'absolute inset-0 overflow-hidden -z-10',
        className
      )}
      aria-hidden="true"
    >
      {/* Base gradient layer */}
      <motion.div
        className="absolute inset-0"
        style={{
          ...getGradientStyle(),
          opacity,
          background: `
            radial-gradient(
              circle at var(--gradient-1-x, 20%) var(--gradient-1-y, 20%),
              ${colors[0]}40 0%,
              transparent 50%
            ),
            radial-gradient(
              circle at var(--gradient-2-x, 80%) var(--gradient-2-y, 20%),
              ${colors[1]}40 0%,
              transparent 50%
            ),
            radial-gradient(
              circle at var(--gradient-3-x, 80%) var(--gradient-3-y, 80%),
              ${colors[2]}40 0%,
              transparent 50%
            ),
            radial-gradient(
              circle at var(--gradient-4-x, 20%) var(--gradient-4-y, 80%),
              ${colors[3]}40 0%,
              transparent 50%
            )
          `,
        }}
        animate={
          shouldReduceMotion
            ? {}
            : {
                backgroundPosition: ['0% 0%', '100% 100%', '0% 0%'],
              }
        }
        transition={{
          duration: speed,
          repeat: Infinity,
          ease: 'linear',
        }}
      />

      {/* Animated floating orbs */}
      {!shouldReduceMotion && (
        <>
          <motion.div
            className="absolute w-96 h-96 rounded-full blur-3xl"
            style={{
              background: `radial-gradient(circle, ${colors[0]}30 0%, transparent 70%)`,
              left: '10%',
              top: '20%',
            }}
            animate={{
              x: [0, 30, 0],
              y: [0, -20, 0],
            }}
            transition={{
              duration: speed * 0.8,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
          />
          <motion.div
            className="absolute w-80 h-80 rounded-full blur-3xl"
            style={{
              background: `radial-gradient(circle, ${colors[1]}30 0%, transparent 70%)`,
              right: '15%',
              top: '10%',
            }}
            animate={{
              x: [0, -25, 0],
              y: [0, 25, 0],
            }}
            transition={{
              duration: speed * 0.9,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
          />
          <motion.div
            className="absolute w-72 h-72 rounded-full blur-3xl"
            style={{
              background: `radial-gradient(circle, ${colors[2]}25 0%, transparent 70%)`,
              left: '30%',
              bottom: '20%',
            }}
            animate={{
              x: [0, 20, 0],
              y: [0, 15, 0],
            }}
            transition={{
              duration: speed,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
          />
        </>
      )}

      {/* Noise texture overlay for depth */}
      <div
        className="absolute inset-0 opacity-[0.015]"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
        }}
      />
    </div>
  );
}

/**
 * Simplified gradient background without animation
 * Use when reduced motion is preferred or for static backgrounds
 */
export function StaticGradient({
  colors = DEFAULT_COLORS,
  className,
  opacity = 0.4,
}: Omit<GradientMeshProps, 'speed' | 'interactive'>) {
  return (
    <div
      className={cn('absolute inset-0 -z-10', className)}
      aria-hidden="true"
      style={{
        opacity,
        background: `
          linear-gradient(135deg, ${colors[0]}20 0%, transparent 50%),
          linear-gradient(225deg, ${colors[1]}20 0%, transparent 50%),
          linear-gradient(315deg, ${colors[2]}20 0%, transparent 50%),
          linear-gradient(45deg, ${colors[3]}20 0%, transparent 50%)
        `,
      }}
    />
  );
}

export default GradientMesh;
