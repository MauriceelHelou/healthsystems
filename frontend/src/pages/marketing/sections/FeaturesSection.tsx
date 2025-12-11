'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

interface FeaturesSectionProps {
  className?: string;
}

interface Capability {
  title: string;
  description: string;
}

const capabilities: Capability[] = [
  {
    title: "Systems Mapping",
    description: "Visualize 1,000+ nodes and 1,200+ mechanisms showing how structural conditions connect to health outcomes. Our nested taxonomy moves from broad structural determinants to specific crisis endpoints—nodes become more granular as they approach individual health outcomes."
  },
  {
    title: "Literature-Backed Mechanisms",
    description: "Our AI pipeline extracts mechanisms from epidemiological literature across PubMed, Elsevier, and other databases. Quality filtering ensures journal standards, citation thresholds, and effect size validation. Click any connection to see the full evidence chain."
  },
  {
    title: "Leverage Point Identification",
    description: "Algorithms surface intervention points with disproportionate downstream effects. Expand from well-documented pathways to discover opportunities that siloed analysis misses."
  },
  {
    title: "Geographic and Population Modulation",
    description: "Mechanisms adjust based on local policy context, demographics, and implementation conditions. Effect sizes are not universal—the platform encodes moderators that strengthen or weaken pathways in specific contexts."
  },
  {
    title: "Budget Silo Transparency",
    description: "See which departments benefit from which investments. When housing improvements reduce asthma ED visits, the platform connects those dots—enabling cross-silo coordination that current budgeting structures prevent."
  },
  {
    title: "Dual ROI Architecture",
    description: "Financial ROI for hospital systems seeking cost savings. Outcome-based ROI (mortality avoided, quality of life, equity gains) for government contexts where pure financial framing is inappropriate. Both grounded in the same evidence infrastructure."
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

export function FeaturesSection({ className }: FeaturesSectionProps) {
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
          <motion.div variants={fadeInUp} className="max-w-3xl mb-16">
            <p className="text-sm font-medium text-slate-500 uppercase tracking-wider mb-4">
              Platform Capabilities
            </p>
            <h2 className="text-3xl md:text-4xl font-medium tracking-tight text-slate-900 leading-tight">
              What the Platform Does
            </h2>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-12">
            {capabilities.map((capability, index) => (
              <motion.div
                key={capability.title}
                variants={fadeInUp}
                className="group"
              >
                <div className="flex items-start gap-4">
                  <span className="flex-shrink-0 w-8 h-8 flex items-center justify-center text-sm font-medium text-slate-400 border border-slate-300 rounded-full">
                    {index + 1}
                  </span>
                  <div>
                    <h3 className="text-lg font-medium text-slate-900">
                      {capability.title}
                    </h3>
                    <p className="mt-3 text-base text-slate-600 leading-relaxed">
                      {capability.description}
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
