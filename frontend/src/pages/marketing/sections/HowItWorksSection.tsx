'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

interface HowItWorksSectionProps {
  className?: string;
}

interface Step {
  id: string;
  title: string;
  description: string;
}

const steps: Step[] = [
  {
    id: '1',
    title: 'Specify Context',
    description: 'Define geography and population of interest.'
  },
  {
    id: '2',
    title: 'Configure System',
    description: 'Platform assembles relevant mechanisms from the validated bank.'
  },
  {
    id: '3',
    title: 'Explore Pathways',
    description: 'Click any node to see upstream causes and downstream effects. Understand what the literature says about why interventions work.'
  },
  {
    id: '4',
    title: 'Identify Leverage Points',
    description: 'Surface intervention points with connections to multiple outcomes.'
  },
  {
    id: '5',
    title: 'Export Evidence',
    description: 'Generate pathway documentation with literature backing for any connection you select.'
  },
  {
    id: '6',
    title: 'Track Progress',
    description: 'Monitor how interventions affect connected outcomes over time as new data becomes available.'
  }
];

const fadeInUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4, ease: [0.25, 0.1, 0.25, 1] } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1, delayChildren: 0.1 } }
};

export function HowItWorksSection({ className }: HowItWorksSectionProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <section id="how-it-works" className={cn("py-24 md:py-32", className)}>
      <div className="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12">
        <motion.div
          initial={shouldReduceMotion ? "visible" : "hidden"}
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={staggerContainer}
        >
          {/* Header */}
          <motion.div variants={fadeInUp} className="max-w-3xl mb-12">
            <p className="text-sm font-medium text-slate-500 uppercase tracking-wider mb-4">
              Process
            </p>
            <h2 className="text-3xl md:text-4xl font-medium tracking-tight text-slate-900 leading-tight">
              From Question to Evidence
            </h2>
          </motion.div>

          {/* Steps */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {steps.map((step, index) => (
              <motion.div
                key={step.id}
                variants={fadeInUp}
                className={cn(
                  "relative bg-white rounded-xl border border-slate-200 p-6 shadow-sm",
                  index === steps.length - 1 && steps.length % 3 !== 0 && "md:col-span-2 lg:col-span-1"
                )}
              >
                <div className="flex items-start gap-4">
                  <span className="flex-shrink-0 w-10 h-10 rounded-full bg-slate-900 text-white text-sm font-medium flex items-center justify-center">
                    {step.id}
                  </span>
                  <div>
                    <h3 className="text-lg font-medium text-slate-900 mb-2">
                      {step.title}
                    </h3>
                    <p className="text-base text-slate-600 leading-relaxed">
                      {step.description}
                    </p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
