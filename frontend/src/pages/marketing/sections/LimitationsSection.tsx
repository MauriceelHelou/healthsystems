'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

interface LimitationsSectionProps {
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

export function LimitationsSection({ className }: LimitationsSectionProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <section id="limitations" className={cn("py-24 md:py-32", className)}>
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
              Transparency
            </p>
            <h2 className="text-3xl md:text-4xl font-medium tracking-tight text-slate-900 leading-tight">
              Honest About Our Stage
            </h2>
          </motion.div>

          {/* Body Content */}
          <motion.div variants={fadeInUp} className="max-w-4xl space-y-6">
            <p className="text-lg text-slate-700 leading-relaxed">
              The platform maps pathways and surfaces evidence. It does not yet produce quantified projections.
            </p>

            <p className="text-lg text-slate-600 leading-relaxed">
              We can show that housing stability connects to reduced hospitalizations through specific mechanisms. We cannot yet calculate that a $10 million investment prevents 347 hospitalizations with a confidence interval.
            </p>

            <p className="text-lg text-slate-600 leading-relaxed">
              That capability requires methodological work we have scoped but not completed: extracting effect sizes across studies, propagating uncertainty through mechanism chains, and validating outputs against real-world data.
            </p>

            <p className="text-lg text-slate-700 leading-relaxed font-medium">
              We are building toward quantification. We are not there yet.
            </p>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
