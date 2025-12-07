'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

interface HowToUseSectionProps {
  onTryNow?: () => void;
  className?: string;
}

const steps = [
  {
    number: 1,
    title: "Select Your Geography",
    description: "Choose a state, county, or city. The system automatically adapts to local policy context—Medicaid rules, housing protections, workforce programs."
  },
  {
    number: 2,
    title: "Identify Health Outcome",
    description: "Pick the crisis you're trying to prevent: cardiovascular events, alcohol-related mortality, housing instability, or 50+ other outcomes."
  },
  {
    number: 3,
    title: "Explore Pathways",
    description: "See which structural interventions matter most. Click nodes to understand mechanisms. Compare alternatives side-by-side."
  },
  {
    number: 4,
    title: "Model Scenarios",
    description: "Ask 'what if' questions. Shift resources between interventions. See projected outcomes with confidence intervals."
  }
];

const fadeInUp = {
  hidden: { opacity: 0, y: 15 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.3, ease: "easeOut" } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.1
    }
  }
};

const stepVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.3, ease: "easeOut" } }
};

const badgeVariants = {
  hidden: { opacity: 0, scale: 0.9 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: {
      duration: 0.25,
      ease: [0.175, 0.885, 0.32, 1.275]
    }
  }
};

const lineVariants = {
  hidden: { scaleX: 0 },
  visible: {
    scaleX: 1,
    transition: {
      duration: 0.6,
      ease: "easeInOut",
      delay: 0.15
    }
  }
};

const verticalLineVariants = {
  hidden: { scaleY: 0 },
  visible: {
    scaleY: 1,
    transition: {
      duration: 0.6,
      ease: "easeInOut",
      delay: 0.15
    }
  }
};

export function HowToUseSection({ onTryNow, className }: HowToUseSectionProps) {
  const shouldReduceMotion = useReducedMotion();

  const handleTryNow = () => {
    if (onTryNow) {
      onTryNow();
    } else {
      window.location.href = '/systems';
    }
  };

  return (
    <section className={cn("py-24 md:py-32 bg-gray-50", className)}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={fadeInUp}
          className="text-center mb-20"
        >
          <h2 className="text-4xl md:text-5xl lg:text-6xl font-semibold tracking-tight text-gray-900 mb-6">
            How It Works
          </h2>
          <p className="text-xl md:text-2xl font-medium text-gray-600 max-w-3xl mx-auto">
            From question to evidence-based insight in minutes
          </p>
        </motion.div>

        {/* Desktop: Horizontal Timeline */}
        <div className="hidden lg:block">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={staggerContainer}
            className="relative"
          >
            {/* Connecting Line */}
            <div className="absolute top-16 left-0 right-0 h-0.5 bg-gray-200">
              <motion.div
                variants={shouldReduceMotion ? {} : lineVariants}
                className="h-full bg-gradient-to-r from-primary-500 to-secondary-500 origin-left"
              />
            </div>

            <div className="grid grid-cols-4 gap-8">
              {steps.map((step) => (
                <motion.div
                  key={step.number}
                  variants={stepVariants}
                  className="text-center"
                >
                  {/* Number Badge */}
                  <motion.div
                    variants={badgeVariants}
                    className="relative z-10 w-16 h-16 bg-white border-4 border-primary-500 rounded-full flex items-center justify-center mx-auto mb-8 shadow-sm"
                  >
                    <span className="text-xl font-semibold text-primary-500">
                      {step.number}
                    </span>
                  </motion.div>

                  {/* Content */}
                  <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm hover:shadow-lg transition-all duration-300">
                    <h3 className="text-xl font-semibold text-gray-900 mb-4">
                      {step.title}
                    </h3>
                    <p className="text-base text-gray-600 leading-relaxed">
                      {step.description}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Mobile & Tablet: Vertical Timeline */}
        <div className="lg:hidden">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={staggerContainer}
            className="relative"
          >
            {/* Vertical Connecting Line */}
            <div className="absolute left-8 top-8 bottom-8 w-0.5 bg-gray-200">
              <motion.div
                variants={shouldReduceMotion ? {} : verticalLineVariants}
                className="w-full bg-gradient-to-b from-primary-500 to-secondary-500 origin-top"
              />
            </div>

            <div className="space-y-12">
              {steps.map((step) => (
                <motion.div
                  key={step.number}
                  variants={stepVariants}
                  className="flex items-start space-x-6"
                >
                  {/* Number Badge */}
                  <motion.div
                    variants={badgeVariants}
                    className="flex-shrink-0 relative z-10 w-16 h-16 bg-white border-4 border-primary-500 rounded-full flex items-center justify-center shadow-sm"
                  >
                    <span className="text-xl font-semibold text-primary-500">
                      {step.number}
                    </span>
                  </motion.div>

                  {/* Content */}
                  <div className="flex-1 bg-white p-6 rounded-2xl border border-gray-200 shadow-sm">
                    <h3 className="text-xl font-semibold text-gray-900 mb-3">
                      {step.title}
                    </h3>
                    <p className="text-base text-gray-600 leading-relaxed">
                      {step.description}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* CTA */}
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={fadeInUp}
          className="text-center mt-20"
        >
          <motion.button
            onClick={handleTryNow}
            whileHover={shouldReduceMotion ? {} : { scale: 1.02 }}
            whileTap={shouldReduceMotion ? {} : { scale: 0.98 }}
            className="inline-flex items-center justify-center px-8 py-4 bg-primary-500 hover:bg-primary-600 text-white font-medium text-lg rounded-xl shadow-sm hover:shadow-lg transition-all duration-300 min-h-[44px] min-w-[44px] focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
          >
            Try It Now
          </motion.button>
        </motion.div>
      </div>
    </section>
  );
}