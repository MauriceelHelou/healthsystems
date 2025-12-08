'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

interface HowToUseSectionProps {
  className?: string;
}

const steps = [
  {
    number: 1,
    title: "Specify Context",
    description: "Define geography and population of interest."
  },
  {
    number: 2,
    title: "Configure System",
    description: "Platform assembles relevant mechanisms with local moderators applied."
  },
  {
    number: 3,
    title: "Explore Pathways",
    description: "Click any node to see upstream causes and downstream effects. Understand why interventions work."
  },
  {
    number: 4,
    title: "Identify Leverage Points",
    description: "Surface intervention points with disproportionate impact across multiple outcomes."
  },
  {
    number: 5,
    title: "Build Justification",
    description: "Export evidence chains with literature backing for any pathway you select."
  }
];

const fadeInUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4, ease: [0.25, 0.1, 0.25, 1] } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.08, delayChildren: 0.1 } }
};

const lineVariants = {
  hidden: { scaleX: 0 },
  visible: {
    scaleX: 1,
    transition: { duration: 0.6, ease: "easeInOut", delay: 0.15 }
  }
};

const verticalLineVariants = {
  hidden: { scaleY: 0 },
  visible: {
    scaleY: 1,
    transition: { duration: 0.6, ease: "easeInOut", delay: 0.15 }
  }
};

export function HowToUseSection({ className }: HowToUseSectionProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <section className={cn("py-24 md:py-32 bg-white", className)}>
      <div className="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12">
        <motion.div
          initial={shouldReduceMotion ? "visible" : "hidden"}
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={staggerContainer}
        >
          {/* Header */}
          <motion.div variants={fadeInUp} className="max-w-3xl mb-16">
            <p className="text-sm font-medium text-slate-500 uppercase tracking-wider mb-4">
              How It Works
            </p>
            <h2 className="text-3xl md:text-4xl font-medium tracking-tight text-slate-900 leading-tight">
              From Question to Evidence
            </h2>
          </motion.div>

          {/* Desktop: Horizontal Timeline */}
          <div className="hidden lg:block">
            <div className="relative">
              {/* Connecting Line */}
              <div className="absolute top-6 left-0 right-0 h-px bg-slate-200">
                <motion.div
                  variants={shouldReduceMotion ? {} : lineVariants}
                  className="h-full bg-slate-400 origin-left"
                />
              </div>

              <div className="grid grid-cols-5 gap-6">
                {steps.map((step) => (
                  <motion.div
                    key={step.number}
                    variants={fadeInUp}
                  >
                    {/* Number Badge */}
                    <div className="relative z-10 w-12 h-12 bg-white border border-slate-300 rounded-full flex items-center justify-center mb-6">
                      <span className="text-sm font-medium text-slate-600">
                        {step.number}
                      </span>
                    </div>

                    {/* Content */}
                    <div>
                      <h3 className="text-lg font-medium text-slate-900 mb-2">
                        {step.title}
                      </h3>
                      <p className="text-sm text-slate-600 leading-relaxed">
                        {step.description}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>

          {/* Mobile & Tablet: Vertical Timeline */}
          <div className="lg:hidden">
            <div className="relative">
              {/* Vertical Connecting Line */}
              <div className="absolute left-6 top-6 bottom-6 w-px bg-slate-200">
                <motion.div
                  variants={shouldReduceMotion ? {} : verticalLineVariants}
                  className="w-full h-full bg-slate-400 origin-top"
                />
              </div>

              <div className="space-y-10">
                {steps.map((step) => (
                  <motion.div
                    key={step.number}
                    variants={fadeInUp}
                    className="flex items-start gap-6"
                  >
                    {/* Number Badge */}
                    <div className="flex-shrink-0 relative z-10 w-12 h-12 bg-white border border-slate-300 rounded-full flex items-center justify-center">
                      <span className="text-sm font-medium text-slate-600">
                        {step.number}
                      </span>
                    </div>

                    {/* Content */}
                    <div className="flex-1 pt-2">
                      <h3 className="text-lg font-medium text-slate-900 mb-2">
                        {step.title}
                      </h3>
                      <p className="text-base text-slate-600 leading-relaxed">
                        {step.description}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>

          {/* Transparency Guarantee */}
          <motion.div
            variants={fadeInUp}
            className="mt-16 pt-12 border-t border-slate-200"
          >
            <div className="max-w-2xl">
              <p className="text-sm font-medium text-slate-500 uppercase tracking-wider mb-3">
                Transparency Guarantee
              </p>
              <p className="text-lg text-slate-700 leading-relaxed">
                Every projection traces to source studies. No black boxes.
              </p>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
