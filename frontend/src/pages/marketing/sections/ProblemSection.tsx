'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

interface ProblemSectionProps {
  className?: string;
}

const fadeInUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4, ease: [0.25, 0.1, 0.25, 1] } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1, delayChildren: 0.1 } }
};

export function ProblemSection({ className }: ProblemSectionProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <section id="problem" className={cn("py-24 md:py-32", className)}>
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
              The Challenge
            </p>
            <h2 className="text-3xl md:text-4xl font-medium tracking-tight text-slate-900 leading-tight">
              The Quantification Gap
            </h2>
          </motion.div>

          {/* Body Content */}
          <motion.div variants={fadeInUp} className="max-w-4xl space-y-6">
            <p className="text-lg text-slate-700 leading-relaxed">
              State health departments allocate billions to housing interventions, community health workers, and food security programs. Hospitals invest in population health. Foundations fund structural change across dozens of organizations.
            </p>

            <p className="text-lg text-slate-700 leading-relaxed font-medium">
              None can answer the question that matters: what do these investments actually produce?
            </p>

            <p className="text-lg text-slate-600 leading-relaxed">
              The evidence exists. Thousands of studies document how housing instability affects health, how income support reduces emergency utilization, how built environment shapes chronic disease. But that evidence is scattered across journals, inaccessible to the decision-makers who need it.
            </p>

            <p className="text-lg text-slate-600 leading-relaxed">
              The result is advocacy without evidence. Programs survive or die based on anecdote. Departments optimize in isolation while cross-silo opportunities go unaddressed. Upstream investments lose to crisis response because crisis response has visible metrics.
            </p>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
