'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';
import { NetworkGraph3D } from '../components/NetworkGraph3D';

interface HeroSectionProps {
  onPrimaryCTA?: () => void;
  onSecondaryCTA?: () => void;
  className?: string;
}

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1, delayChildren: 0.15 } }
};

const fadeInUp = {
  hidden: { opacity: 0, y: 24 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.25, 0.1, 0.25, 1] } }
};

export function HeroSection({ onPrimaryCTA, onSecondaryCTA, className }: HeroSectionProps) {
  const shouldReduceMotion = useReducedMotion();

  const handlePrimaryCTA = () => {
    if (onPrimaryCTA) {
      onPrimaryCTA();
    } else {
      window.location.href = '/systems';
    }
  };

  const handleSecondaryCTA = () => {
    if (onSecondaryCTA) {
      onSecondaryCTA();
    } else {
      window.location.href = 'mailto:contact@healthsystems.io';
    }
  };

  return (
    <section
      className={cn(
        "relative min-h-screen flex items-center overflow-hidden",
        "bg-slate-950",
        className
      )}
    >
      {/* Full-screen 3D Network Graph Background */}
      <div className="absolute inset-0 opacity-60">
        <NetworkGraph3D />
      </div>

      {/* Gradient overlay for text readability */}
      <div className="absolute inset-0 bg-gradient-to-r from-slate-950 via-slate-950/80 to-slate-950/40" />

      {/* Content */}
      <div className="relative z-10 max-w-6xl mx-auto px-6 sm:px-8 lg:px-12 w-full">
        <div className="max-w-3xl py-20 lg:py-32">
          <motion.div
            initial={shouldReduceMotion ? "visible" : "hidden"}
            animate="visible"
            variants={staggerContainer}
          >
            <motion.h1
              variants={fadeInUp}
              className="text-4xl md:text-5xl lg:text-6xl font-medium tracking-tight text-white leading-[1.1]"
            >
              Identify Where Health Interventions Matter Most
            </motion.h1>

            <motion.p
              variants={fadeInUp}
              className="mt-8 text-lg md:text-xl text-slate-400 leading-relaxed max-w-2xl"
            >
              A decision-support platform that maps how structural conditions cascade through
              causal pathways to health outcomes. Pinpoint high-leverage intervention points.
              Justify upstream investments with evidence.
            </motion.p>

            <motion.div
              variants={fadeInUp}
              className="mt-12 flex flex-col sm:flex-row gap-4"
            >
              <button
                onClick={handlePrimaryCTA}
                className={cn(
                  "inline-flex items-center justify-center px-6 py-3.5 text-base font-medium",
                  "bg-white text-slate-950 rounded-lg",
                  "transition-all duration-200 hover:bg-slate-100",
                  "focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-slate-950"
                )}
              >
                Explore the Platform
              </button>

              <button
                onClick={handleSecondaryCTA}
                className={cn(
                  "inline-flex items-center justify-center px-6 py-3.5 text-base font-medium",
                  "bg-transparent text-white border border-slate-700 rounded-lg",
                  "transition-all duration-200 hover:bg-slate-900 hover:border-slate-600",
                  "focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-slate-950"
                )}
              >
                Contact Us
              </button>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
