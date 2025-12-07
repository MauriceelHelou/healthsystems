'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

interface HeroSectionProps {
  onPrimaryCTA?: () => void;
  onSecondaryCTA?: () => void;
  className?: string;
}

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.08, delayChildren: 0.1 } }
};

const fadeInUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4, ease: "easeOut" } }
};

const buttonVariants = {
  hover: { scale: 1.02, transition: { duration: 0.2 } },
  tap: { scale: 0.98 }
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
      const aboutSection = document.querySelector('#about');
      aboutSection?.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section 
      className={cn(
        "relative min-h-screen md:min-h-screen flex items-center overflow-hidden",
        "bg-gradient-to-br from-gray-50 via-white to-blue-50/30",
        className
      )}
    >
      {/* Floating background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="floating-dots">
          {[...Array(12)].map((_, i) => (
            <div
              key={i}
              className={cn(
                "absolute rounded-full opacity-20",
                i % 3 === 0 ? "bg-primary-500" : i % 3 === 1 ? "bg-secondary-500" : "bg-orange-400"
              )}
              style={{
                width: Math.random() * 6 + 4 + 'px',
                height: Math.random() * 6 + 4 + 'px',
                left: Math.random() * 100 + '%',
                top: Math.random() * 100 + '%',
                animationDelay: Math.random() * 10 + 's',
                animationDuration: (Math.random() * 20 + 15) + 's'
              }}
            />
          ))}
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-center min-h-[80vh] py-16">
          <motion.div
            initial={shouldReduceMotion ? "visible" : "hidden"}
            animate="visible"
            variants={staggerContainer}
            className="max-w-2xl"
          >
            <motion.h1 
              variants={fadeInUp}
              className="text-4xl md:text-5xl lg:text-6xl font-semibold tracking-tight text-gray-900 leading-tight"
            >
              Quantify How{' '}
              <span className="relative inline-block">
                <span className="gradient-text bg-gradient-to-r from-primary-500 via-secondary-500 to-orange-400 bg-clip-text text-transparent animate-gradient-x">
                  Policy
                </span>
              </span>
              {' '}Shapes Health
            </motion.h1>
            
            <motion.p 
              variants={fadeInUp}
              className="mt-6 text-xl md:text-2xl font-medium text-gray-600 leading-relaxed"
            >
              A decision support platform that maps how structural interventions—housing policy, 
              Medicaid design, workforce development—cascade through causal pathways to affect 
              health outcomes.
            </motion.p>

            <motion.div 
              variants={fadeInUp}
              className="mt-10 flex flex-col sm:flex-row gap-4"
            >
              <motion.button
                variants={buttonVariants}
                whileHover={shouldReduceMotion ? undefined : "hover"}
                whileTap={shouldReduceMotion ? undefined : "tap"}
                onClick={handlePrimaryCTA}
                className={cn(
                  "group inline-flex items-center justify-center px-8 py-4 text-lg font-medium",
                  "bg-primary-500 text-white rounded-2xl shadow-sm hover:shadow-lg",
                  "transition-all duration-300 hover:bg-primary-600",
                  "min-h-[56px] min-w-[160px]"
                )}
              >
                Explore the Map
                <svg className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </motion.button>

              <motion.button
                variants={buttonVariants}
                whileHover={shouldReduceMotion ? undefined : "hover"}
                whileTap={shouldReduceMotion ? undefined : "tap"}
                onClick={handleSecondaryCTA}
                className={cn(
                  "inline-flex items-center justify-center px-8 py-4 text-lg font-medium",
                  "bg-white text-gray-700 border border-gray-200 rounded-2xl shadow-sm hover:shadow-lg",
                  "transition-all duration-300 hover:border-gray-300 hover:bg-gray-50",
                  "min-h-[56px] min-w-[160px]"
                )}
              >
                Learn More
              </motion.button>
            </motion.div>
          </motion.div>

          {/* Right side space for future animated visual */}
          <div className="hidden lg:block relative">
            <div className="aspect-square max-w-lg mx-auto opacity-20">
              <div className="w-full h-full border-2 border-dashed border-gray-300 rounded-2xl flex items-center justify-center">
                <span className="text-gray-400 text-lg">Future Visual</span>
              </div>
            </div>
          </div>
        </div>
      </div>

    </section>
  );
}