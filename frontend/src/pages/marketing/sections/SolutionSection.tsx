'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

interface SolutionSectionProps {
  className?: string;
}

interface Capability {
  id: string;
  title: string;
  description: string;
}

const capabilities: Capability[] = [
  {
    id: 'pathway-mapping',
    title: 'Pathway Mapping',
    description: 'Trace forward from a policy you control, or backward from an outcome you care about. See the causal chain: housing stability \u2192 reduced eviction threat \u2192 reduced chronic stress \u2192 fewer asthma exacerbations \u2192 fewer ED visits. Each link cites peer-reviewed research.'
  },
  {
    id: 'leverage-points',
    title: 'Leverage Point Identification',
    description: 'Some variables affect many outcomes; others affect few. Our algorithms surface nodes where interventions generate disproportionate downstream effects across multiple health endpoints.'
  },
  {
    id: 'evidence-transparency',
    title: 'Evidence Transparency',
    description: 'Click any connection to see the supporting studies, quality ratings, and effect directions. No black boxes. Every pathway traces to literature you can inspect.'
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

export function SolutionSection({ className }: SolutionSectionProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <section id="solution" className={cn("py-24 md:py-32", className)}>
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
              What We Do
            </p>
            <h2 className="text-3xl md:text-4xl font-medium tracking-tight text-slate-900 leading-tight mb-6">
              Make the Evidence Navigable
            </h2>
            <p className="text-lg text-slate-600 leading-relaxed">
              We synthesize epidemiological literature into systems maps that show which structural conditions connect to which health outcomes, and what evidence supports each connection.
            </p>
          </motion.div>

          {/* Capability Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {capabilities.map((capability) => (
              <motion.div
                key={capability.id}
                variants={fadeInUp}
                className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm"
              >
                <h3 className="text-lg font-medium text-slate-900 mb-4">
                  {capability.title}
                </h3>
                <p className="text-base text-slate-600 leading-relaxed">
                  {capability.description}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
