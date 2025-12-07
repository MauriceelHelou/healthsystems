'use client';

import { motion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

interface RoadmapSectionProps {
  className?: string;
}

type PhaseStatus = 'complete' | 'in-progress' | 'planned';

interface Phase {
  status: PhaseStatus;
  title: string;
  phase: string;
  icon: React.FC<{ className?: string }>;
  features: string[];
}

// Inline SVG icon components
const CheckCircleIcon = ({ className }: { className?: string }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const ClockIcon = ({ className }: { className?: string }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const CalendarIcon = ({ className }: { className?: string }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
  </svg>
);

const fadeInUp = {
  hidden: { opacity: 0, y: 15 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.3, ease: "easeOut" } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.08, delayChildren: 0.1 } }
};

const lineAnimation = {
  hidden: { pathLength: 0, opacity: 0 },
  visible: { pathLength: 1, opacity: 1, transition: { duration: 0.8, ease: "easeInOut" } }
};

const badgeAnimation = {
  hidden: { scale: 0.8, opacity: 0 },
  visible: { scale: 1, opacity: 1, transition: { type: "spring", stiffness: 200, damping: 20 } }
};

const phases: Phase[] = [
  {
    status: 'complete',
    title: 'Topology & Direction Discovery',
    phase: 'Phase 1: MVP (Current)',
    icon: CheckCircleIcon,
    features: [
      '2000 mechanisms identified and catalogued',
      '400+ nodes defined with specifications',
      'Direction of each mechanism (positive/negative)',
      'Literature lineage for every pathway'
    ]
  },
  {
    status: 'in-progress',
    title: 'Quantification & Modeling',
    phase: 'Phase 2: Coming Soon',
    icon: ClockIcon,
    features: [
      'Effect size quantification with 95% confidence intervals',
      'Meta-analytic pooling from 300+ studies per mechanism',
      'Bayesian uncertainty propagation',
      'Intervention impact calculator'
    ]
  },
  {
    status: 'planned',
    title: 'Actor Network & Scale',
    phase: 'Phase 3: Future',
    icon: CalendarIcon,
    features: [
      'Multi-geography deployment (50+ states/counties)',
      'Organizational collaboration mapping',
      'Real-time data integration',
      'Policy change alerts'
    ]
  }
];

const statusConfig = {
  complete: {
    badge: 'Complete',
    color: 'bg-green-100 text-green-800 border-green-200',
    dotColor: 'bg-green-500',
    cardBorder: 'border-green-200',
    cardBg: 'bg-green-50/50'
  },
  'in-progress': {
    badge: 'In Progress',
    color: 'bg-orange-100 text-orange-800 border-orange-200',
    dotColor: 'bg-orange-500',
    cardBorder: 'border-orange-200',
    cardBg: 'bg-orange-50/50'
  },
  planned: {
    badge: 'Planned',
    color: 'bg-gray-100 text-gray-600 border-gray-200',
    dotColor: 'bg-gray-400',
    cardBorder: 'border-gray-200',
    cardBg: 'bg-gray-50/50'
  }
};

export function RoadmapSection({ className }: RoadmapSectionProps) {
  return (
    <section className={cn("py-24 md:py-32 bg-gray-50", className)}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={fadeInUp}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl lg:text-6xl font-semibold tracking-tight text-gray-900 mb-6">
            What We're Building
          </h2>
          <p className="text-xl md:text-2xl font-medium text-gray-600 max-w-3xl mx-auto">
            A phased approach to comprehensive health systems modeling
          </p>
        </motion.div>

        {/* Desktop Timeline */}
        <div className="hidden lg:block relative">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={staggerContainer}
            className="relative"
          >
            {/* Timeline Line */}
            <div className="absolute top-24 left-0 right-0 h-0.5 bg-gray-200">
              <motion.div
                variants={lineAnimation}
                className="h-full bg-gradient-to-r from-green-500 via-orange-500 to-gray-400"
              />
            </div>

            {/* Timeline Dots */}
            <div className="absolute top-24 left-0 right-0 flex justify-between items-center">
              {phases.map((phase, index) => (
                <motion.div
                  key={index}
                  variants={badgeAnimation}
                  className={cn(
                    "w-4 h-4 rounded-full border-4 border-white",
                    statusConfig[phase.status].dotColor
                  )}
                />
              ))}
            </div>

            {/* Phase Cards */}
            <div className="grid grid-cols-3 gap-8 pt-16">
              {phases.map((phase, index) => (
                <motion.div
                  key={index}
                  variants={fadeInUp}
                  className={cn(
                    "bg-white rounded-2xl border p-8 hover:shadow-lg transition-all duration-300",
                    statusConfig[phase.status].cardBorder,
                    statusConfig[phase.status].cardBg
                  )}
                >
                  <div className="flex items-center gap-3 mb-4">
                    <phase.icon className="w-6 h-6 text-gray-600" />
                    <motion.span
                      variants={badgeAnimation}
                      className={cn(
                        "px-3 py-1 rounded-full text-sm font-medium border",
                        statusConfig[phase.status].color
                      )}
                    >
                      {statusConfig[phase.status].badge}
                    </motion.span>
                  </div>
                  
                  <h3 className="text-sm font-medium text-gray-500 mb-2">
                    {phase.phase}
                  </h3>
                  
                  <h4 className="text-xl font-semibold text-gray-900 mb-6">
                    {phase.title}
                  </h4>
                  
                  <ul className="space-y-3">
                    {phase.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-start gap-3">
                        {phase.status === 'complete' ? (
                          <CheckCircleIcon className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                        ) : (
                          <div className="w-5 h-5 mt-0.5 flex-shrink-0 flex items-center justify-center">
                            <div className="w-2 h-2 bg-gray-300 rounded-full" />
                          </div>
                        )}
                        <span className="text-sm text-gray-600 leading-relaxed">
                          {feature}
                        </span>
                      </li>
                    ))}
                  </ul>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Mobile Timeline */}
        <div className="lg:hidden">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={staggerContainer}
            className="relative"
          >
            {/* Vertical Timeline Line */}
            <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-gray-200">
              <motion.div
                variants={lineAnimation}
                className="w-full bg-gradient-to-b from-green-500 via-orange-500 to-gray-400"
                style={{ height: '100%' }}
              />
            </div>

            <div className="space-y-8">
              {phases.map((phase, index) => (
                <motion.div
                  key={index}
                  variants={fadeInUp}
                  className="relative pl-20"
                >
                  {/* Timeline Dot */}
                  <motion.div
                    variants={badgeAnimation}
                    className={cn(
                      "absolute -left-2 top-4 w-4 h-4 rounded-full border-4 border-white",
                      statusConfig[phase.status].dotColor
                    )}
                  />

                  {/* Card */}
                  <div className={cn(
                    "bg-white rounded-2xl border p-6",
                    statusConfig[phase.status].cardBorder,
                    statusConfig[phase.status].cardBg
                  )}>
                    <div className="flex items-center gap-3 mb-4">
                      <phase.icon className="w-6 h-6 text-gray-600" />
                      <motion.span
                        variants={badgeAnimation}
                        className={cn(
                          "px-3 py-1 rounded-full text-sm font-medium border",
                          statusConfig[phase.status].color
                        )}
                      >
                        {statusConfig[phase.status].badge}
                      </motion.span>
                    </div>
                    
                    <h3 className="text-sm font-medium text-gray-500 mb-2">
                      {phase.phase}
                    </h3>
                    
                    <h4 className="text-xl font-semibold text-gray-900 mb-6">
                      {phase.title}
                    </h4>
                    
                    <ul className="space-y-3">
                      {phase.features.map((feature, featureIndex) => (
                        <li key={featureIndex} className="flex items-start gap-3">
                          {phase.status === 'complete' ? (
                            <CheckCircleIcon className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                          ) : (
                            <div className="w-5 h-5 mt-0.5 flex-shrink-0 flex items-center justify-center">
                              <div className="w-2 h-2 bg-gray-300 rounded-full" />
                            </div>
                          )}
                          <span className="text-sm text-gray-600 leading-relaxed">
                            {feature}
                          </span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}