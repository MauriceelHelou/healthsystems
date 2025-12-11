'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

interface AboutSectionProps {
  className?: string;
}

const sectionVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      duration: 0.4,
      staggerChildren: 0.1,
      delayChildren: 0.1
    }
  }
};

const fadeInUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4, ease: [0.25, 0.1, 0.25, 1] } }
};

const valueProps = [
  {
    label: "Identification",
    title: "Find What Matters",
    description: "Not just mapping—discovery. Our platform surfaces high-leverage nodes where interventions generate outsized effects across multiple health outcomes. See which points in the system create disproportionate impact."
  },
  {
    label: "Justification",
    title: "Build the Evidence Case",
    description: "Every pathway traces to peer-reviewed literature. Quality ratings, citations, and effect directions are fully transparent. Defend upstream investments with evidence chains that hold up to scrutiny."
  },
  {
    label: "Equity",
    title: "See Who Benefits",
    description: "Outcomes stratified by population. Mechanisms include demographic, geographic, and policy moderators. Identify what reduces disparities—not just what improves averages."
  }
];

export function AboutSection({ className }: AboutSectionProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <section className={cn("py-24 md:py-32 bg-white", className)} id="about">
      <div className="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12">
        <motion.div
          initial={shouldReduceMotion ? "visible" : "hidden"}
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={sectionVariants}
        >
          {/* Mission Section */}
          <div className="max-w-3xl">
            <motion.p
              variants={fadeInUp}
              className="text-sm font-medium text-slate-500 uppercase tracking-wider mb-4"
            >
              The Problem We Solve
            </motion.p>

            <motion.h2
              variants={fadeInUp}
              className="text-3xl md:text-4xl font-medium tracking-tight text-slate-900 leading-tight"
            >
              Public health faces a $65 million question: how do you quantify the return on upstream prevention?
            </motion.h2>

            <motion.div variants={fadeInUp} className="mt-8 space-y-6 text-lg text-slate-600 leading-relaxed">
              <p>
                Agencies advocate for housing interventions, walkable communities, and income support—but
                cannot articulate what these investments actually buy in health outcomes. Budget silos
                prevent departments from seeing when their investments yield savings elsewhere. Prior
                attempts to build systems-level tools have failed.
              </p>
              <p>
                We make the invisible visible. We map the causal pathways connecting structural
                determinants to health crises, identify which intervention points generate disproportionate
                impact, and provide the evidence infrastructure to justify investments that have been
                impossible to defend.
              </p>
            </motion.div>
          </div>

          {/* Value Props */}
          <motion.div
            variants={fadeInUp}
            className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-12"
          >
            {valueProps.map((prop) => (
              <div key={prop.label}>
                <p className="text-sm font-medium text-slate-400 uppercase tracking-wider">
                  {prop.label}
                </p>
                <h3 className="mt-2 text-xl font-medium text-slate-900">
                  {prop.title}
                </h3>
                <p className="mt-4 text-base text-slate-600 leading-relaxed">
                  {prop.description}
                </p>
              </div>
            ))}
          </motion.div>

          {/* What Makes Us Different */}
          <motion.div
            variants={fadeInUp}
            className="mt-24 pt-16 border-t border-slate-200"
          >
            <div className="max-w-3xl">
              <p className="text-sm font-medium text-slate-500 uppercase tracking-wider mb-4">
                Why This Hasn't Been Done Before
              </p>

              <h3 className="text-2xl md:text-3xl font-medium tracking-tight text-slate-900 leading-tight">
                What Makes Us Different
              </h3>

              <div className="mt-8 space-y-6 text-lg text-slate-600 leading-relaxed">
                <p>
                  Traditional health impact assessments take 6-12 months and produce qualitative reports.
                  SROI platforms force everything into a single monetized ratio, hiding equity distributions
                  and causal complexity. Academic system dynamics models require PhD expertise and must be
                  rebuilt from scratch for each context.
                </p>
                <p>
                  We combine systems thinking with AI-powered literature synthesis at scale. Our mechanism
                  bank is reusable across geographies. Our evidence chains are auditable. Our platform
                  identifies intervention opportunities that siloed analysis systematically misses.
                </p>
              </div>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
