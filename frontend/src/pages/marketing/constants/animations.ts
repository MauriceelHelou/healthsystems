/**
 * Shared Framer Motion animation variants for marketing page
 *
 * These variants ensure consistent animations across all sections.
 * Import and use with motion components:
 *
 * <motion.div variants={fadeInUp} initial="hidden" animate="visible">
 */

import { Variants } from 'framer-motion';

// =============================================================================
// ENTRANCE ANIMATIONS
// =============================================================================

/**
 * Fade in from bottom - standard entrance animation
 */
export const fadeInUp: Variants = {
  hidden: {
    opacity: 0,
    y: 20
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.6,
      ease: 'easeOut'
    }
  },
};

/**
 * Fade in from left
 */
export const fadeInLeft: Variants = {
  hidden: {
    opacity: 0,
    x: -30
  },
  visible: {
    opacity: 1,
    x: 0,
    transition: {
      duration: 0.6,
      ease: 'easeOut'
    }
  },
};

/**
 * Fade in from right
 */
export const fadeInRight: Variants = {
  hidden: {
    opacity: 0,
    x: 30
  },
  visible: {
    opacity: 1,
    x: 0,
    transition: {
      duration: 0.6,
      ease: 'easeOut'
    }
  },
};

/**
 * Simple fade without movement
 */
export const fadeIn: Variants = {
  hidden: {
    opacity: 0
  },
  visible: {
    opacity: 1,
    transition: {
      duration: 0.5
    }
  },
};

/**
 * Scale up from smaller size
 */
export const scaleIn: Variants = {
  hidden: {
    opacity: 0,
    scale: 0.9
  },
  visible: {
    opacity: 1,
    scale: 1,
    transition: {
      duration: 0.4,
      ease: 'easeOut'
    }
  },
};

// =============================================================================
// CONTAINER ANIMATIONS (for staggered children)
// =============================================================================

/**
 * Container that staggers children animations
 */
export const staggerContainer: Variants = {
  hidden: {
    opacity: 0
  },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

/**
 * Faster stagger for quick reveals
 */
export const staggerContainerFast: Variants = {
  hidden: {
    opacity: 0
  },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05,
      delayChildren: 0.1,
    },
  },
};

/**
 * Slower stagger for dramatic reveals
 */
export const staggerContainerSlow: Variants = {
  hidden: {
    opacity: 0
  },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.15,
      delayChildren: 0.3,
    },
  },
};

// =============================================================================
// CARD ANIMATIONS
// =============================================================================

/**
 * Card reveal with index-based delay
 * Usage: <motion.div custom={index} variants={cardReveal} />
 */
export const cardReveal: Variants = {
  hidden: {
    opacity: 0,
    y: 30
  },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: {
      delay: i * 0.1,
      duration: 0.5,
      ease: 'easeOut',
    },
  }),
};

// =============================================================================
// HOVER ANIMATIONS
// =============================================================================

/**
 * Subtle scale on hover - for cards and buttons
 */
export const hoverScale: Variants = {
  rest: {
    scale: 1
  },
  hover: {
    scale: 1.02,
    transition: {
      duration: 0.2
    }
  },
};

/**
 * Lift effect on hover - combines Y translation with shadow
 */
export const hoverLift: Variants = {
  rest: {
    y: 0,
    boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)',
  },
  hover: {
    y: -4,
    boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)',
    transition: {
      duration: 0.2
    }
  },
};

// =============================================================================
// SPECIAL EFFECTS
// =============================================================================

/**
 * Pulse animation for attention-grabbing elements
 */
export const pulse: Variants = {
  rest: {
    scale: 1
  },
  pulse: {
    scale: [1, 1.05, 1],
    transition: {
      duration: 2,
      repeat: Infinity,
      ease: 'easeInOut',
    },
  },
};

/**
 * Draw line animation (for SVG paths)
 */
export const drawLine: Variants = {
  hidden: {
    pathLength: 0,
    opacity: 0
  },
  visible: {
    pathLength: 1,
    opacity: 1,
    transition: {
      pathLength: {
        duration: 1.5,
        ease: 'easeInOut'
      },
      opacity: {
        duration: 0.3
      },
    },
  },
};

/**
 * Number counter animation props (use with useSpring)
 */
export const counterSpring = {
  stiffness: 100,
  damping: 30,
};

// =============================================================================
// VIEWPORT OPTIONS
// =============================================================================

/**
 * Standard viewport options for scroll-triggered animations
 */
export const viewportOnce = {
  once: true,
  margin: '-100px'
};

/**
 * More aggressive trigger (fires earlier)
 */
export const viewportEarly = {
  once: true,
  margin: '-50px'
};

/**
 * Repeating animation (fires every time element enters viewport)
 */
export const viewportRepeat = {
  once: false,
  margin: '-100px'
};
