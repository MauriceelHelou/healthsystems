'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

interface RoadmapSectionProps {
  className?: string;
}

interface RoadmapPhase {
  id: string;
  title: string;
  items: string[];
  isCurrent?: boolean;
}

const phases: RoadmapPhase[] = [
  {
    id: 'current',
    title: 'Current (MVP)',
    isCurrent: true,
    items: [
      'Complete network topology linking structural determinants to health outcomes',
      'Direction and quality rating for every pathway',
      'Literature lineage with clickable citations',
      'Interactive exploration interface'
    ]
  },
  {
    id: 'next',
    title: 'Next Phase: Quantification',
    items: [
      'Effect size extraction from literature',
      'Meta-analytic pooling where studies permit',
      'Uncertainty propagation through mechanism chains',
      'Scenario modeling with confidence intervals'
    ]
  },
  {
    id: 'future',
    title: 'Future',
    items: [
      'Equity-stratified outcome projections',
      'Actor network mapping (which organizations intervene where)',
      'Multi-geography deployment',
      'API access for integration'
    ]
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

export function RoadmapSection({ className }: RoadmapSectionProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <section id="roadmap" className={cn("py-24 md:py-32", className)}>
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
              Roadmap
            </p>
            <h2 className="text-3xl md:text-4xl font-medium tracking-tight text-slate-900 leading-tight">
              What We're Building
            </h2>
          </motion.div>

          {/* Phases Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {phases.map((phase) => (
              <motion.div
                key={phase.id}
                variants={fadeInUp}
                className={cn(
                  "rounded-xl p-6",
                  phase.isCurrent
                    ? "bg-slate-900 text-white"
                    : "bg-white border border-slate-200 shadow-sm"
                )}
              >
                <h3 className={cn(
                  "text-lg font-medium mb-4",
                  phase.isCurrent ? "text-white" : "text-slate-900"
                )}>
                  {phase.title}
                </h3>
                <ul className="space-y-3">
                  {phase.items.map((item, index) => (
                    <li key={index} className="flex items-start gap-3">
                      <span className={cn(
                        "flex-shrink-0 w-1.5 h-1.5 rounded-full mt-2",
                        phase.isCurrent ? "bg-slate-400" : "bg-slate-400"
                      )} />
                      <span className={cn(
                        "text-base leading-relaxed",
                        phase.isCurrent ? "text-slate-300" : "text-slate-600"
                      )}>
                        {item}
                      </span>
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
