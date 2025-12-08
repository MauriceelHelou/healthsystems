'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

interface RoadmapSectionProps {
  className?: string;
}

type PhaseStatus = 'current' | 'upcoming' | 'future';

interface Phase {
  status: PhaseStatus;
  title: string;
  timeline: string;
  features: string[];
}

const fadeInUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4, ease: [0.25, 0.1, 0.25, 1] } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.08, delayChildren: 0.1 } }
};

const lineAnimation = {
  hidden: { scaleX: 0 },
  visible: { scaleX: 1, transition: { duration: 0.6, ease: "easeInOut", delay: 0.15 } }
};

const verticalLineAnimation = {
  hidden: { scaleY: 0 },
  visible: { scaleY: 1, transition: { duration: 0.6, ease: "easeInOut", delay: 0.15 } }
};

const phases: Phase[] = [
  {
    status: 'current',
    title: 'Current Prototype',
    timeline: 'Now',
    features: [
      '1,000+ nodes mapped across structural domains',
      '1,200+ literature-backed mechanisms',
      'Direction and category for every pathway',
      'Interactive exploration interface'
    ]
  },
  {
    status: 'upcoming',
    title: 'Quantification',
    timeline: 'Q1-Q2 2025',
    features: [
      'Effect size extraction with confidence intervals',
      'Meta-analytic pooling where studies permit',
      'Scenario modeling with uncertainty propagation',
      'Equity-stratified projections'
    ]
  },
  {
    status: 'future',
    title: 'Scale',
    timeline: '2025+',
    features: [
      'Multi-geography deployment',
      'API access for integration',
      'Custom mechanism bank curation',
      'Collaborative analysis workspaces'
    ]
  }
];

const statusConfig = {
  current: {
    badge: 'Current',
    badgeClass: 'bg-slate-900 text-white',
    dotClass: 'bg-slate-900',
    borderClass: 'border-slate-300'
  },
  upcoming: {
    badge: 'Q1-Q2 2025',
    badgeClass: 'bg-slate-100 text-slate-700',
    dotClass: 'bg-slate-400',
    borderClass: 'border-slate-200'
  },
  future: {
    badge: '2025+',
    badgeClass: 'bg-slate-100 text-slate-500',
    dotClass: 'bg-slate-300',
    borderClass: 'border-slate-200'
  }
};

export function RoadmapSection({ className }: RoadmapSectionProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <section className={cn("py-24 md:py-32 bg-slate-50", className)}>
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
              Roadmap
            </p>
            <h2 className="text-3xl md:text-4xl font-medium tracking-tight text-slate-900 leading-tight">
              What We're Building
            </h2>
          </motion.div>

          {/* Desktop Timeline */}
          <div className="hidden lg:block relative">
            {/* Timeline Line */}
            <div className="absolute top-6 left-0 right-0 h-px bg-slate-200">
              <motion.div
                variants={shouldReduceMotion ? {} : lineAnimation}
                className="h-full bg-slate-400 origin-left"
              />
            </div>

            {/* Phase Cards */}
            <div className="grid grid-cols-3 gap-8">
              {phases.map((phase) => (
                <motion.div
                  key={phase.title}
                  variants={fadeInUp}
                >
                  {/* Timeline Dot */}
                  <div className={cn(
                    "relative z-10 w-12 h-12 rounded-full flex items-center justify-center mb-6 border-4 border-white",
                    statusConfig[phase.status].dotClass
                  )} />

                  {/* Card */}
                  <div className={cn(
                    "bg-white rounded-xl border p-6",
                    statusConfig[phase.status].borderClass
                  )}>
                    <div className="flex items-center gap-3 mb-4">
                      <span className={cn(
                        "px-3 py-1 rounded-full text-xs font-medium",
                        statusConfig[phase.status].badgeClass
                      )}>
                        {statusConfig[phase.status].badge}
                      </span>
                    </div>

                    <h3 className="text-xl font-medium text-slate-900 mb-4">
                      {phase.title}
                    </h3>

                    <ul className="space-y-3">
                      {phase.features.map((feature, featureIndex) => (
                        <li key={featureIndex} className="flex items-start gap-3">
                          <div className="w-1.5 h-1.5 bg-slate-400 rounded-full mt-2 flex-shrink-0" />
                          <span className="text-sm text-slate-600 leading-relaxed">
                            {feature}
                          </span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Mobile Timeline */}
          <div className="lg:hidden">
            <div className="relative">
              {/* Vertical Timeline Line */}
              <div className="absolute left-6 top-6 bottom-6 w-px bg-slate-200">
                <motion.div
                  variants={shouldReduceMotion ? {} : verticalLineAnimation}
                  className="w-full h-full bg-slate-400 origin-top"
                />
              </div>

              <div className="space-y-8">
                {phases.map((phase) => (
                  <motion.div
                    key={phase.title}
                    variants={fadeInUp}
                    className="relative pl-16"
                  >
                    {/* Timeline Dot */}
                    <div className={cn(
                      "absolute left-0 top-0 w-12 h-12 rounded-full flex items-center justify-center border-4 border-white",
                      statusConfig[phase.status].dotClass
                    )} />

                    {/* Card */}
                    <div className={cn(
                      "bg-white rounded-xl border p-5",
                      statusConfig[phase.status].borderClass
                    )}>
                      <div className="flex items-center gap-3 mb-3">
                        <span className={cn(
                          "px-3 py-1 rounded-full text-xs font-medium",
                          statusConfig[phase.status].badgeClass
                        )}>
                          {statusConfig[phase.status].badge}
                        </span>
                      </div>

                      <h3 className="text-lg font-medium text-slate-900 mb-4">
                        {phase.title}
                      </h3>

                      <ul className="space-y-2">
                        {phase.features.map((feature, featureIndex) => (
                          <li key={featureIndex} className="flex items-start gap-3">
                            <div className="w-1.5 h-1.5 bg-slate-400 rounded-full mt-2 flex-shrink-0" />
                            <span className="text-sm text-slate-600 leading-relaxed">
                              {feature}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
