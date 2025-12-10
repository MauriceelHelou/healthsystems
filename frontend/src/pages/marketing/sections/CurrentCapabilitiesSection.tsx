'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

interface CurrentCapabilitiesSectionProps {
  className?: string;
}

const capabilities = [
  'Validated mechanisms linking structural determinants to health outcomes, each with direction, quality rating, and citations',
  'Nodes organized from broad structural conditions through intermediate factors to specific crisis endpoints',
  'AI-powered literature extraction connecting to PubMed, Elsevier, and academic databases with quality filtering for journal standards and citation thresholds',
  'Interactive systems visualization allowing users to explore pathways, click into mechanisms, and trace evidence chains',
  'Geographic and population modulation flagging when effects vary by policy context, demographics, or implementation conditions'
];

const fadeInUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4, ease: [0.25, 0.1, 0.25, 1] } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1, delayChildren: 0.1 } }
};

export function CurrentCapabilitiesSection({ className }: CurrentCapabilitiesSectionProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <section id="capabilities" className={cn("py-24 md:py-32", className)}>
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
              Current Capabilities
            </p>
            <h2 className="text-3xl md:text-4xl font-medium tracking-tight text-slate-900 leading-tight">
              What the Platform Does Today
            </h2>
          </motion.div>

          {/* Numbered List */}
          <motion.div variants={fadeInUp} className="max-w-4xl">
            <ol className="space-y-6">
              {capabilities.map((capability, index) => (
                <li key={index} className="flex items-start gap-4">
                  <span className="flex-shrink-0 w-8 h-8 rounded-full bg-slate-900 text-white text-sm font-medium flex items-center justify-center mt-0.5">
                    {index + 1}
                  </span>
                  <span className="text-lg text-slate-700 leading-relaxed">{capability}</span>
                </li>
              ))}
            </ol>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
