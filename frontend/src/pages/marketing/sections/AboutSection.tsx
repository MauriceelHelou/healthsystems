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
      duration: 0.3,
      ease: "easeOut",
      staggerChildren: 0.08,
      delayChildren: 0.1
    }
  }
};

const fadeInUp = {
  hidden: { opacity: 0, y: 15 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.3, ease: "easeOut" }
  }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.06,
      delayChildren: 0.1
    }
  }
};

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.3, ease: "easeOut" }
  }
};

const slideInRight = {
  hidden: { opacity: 0, x: 30 },
  visible: {
    opacity: 1,
    x: 0,
    transition: { duration: 0.35, ease: "easeOut" }
  }
};

export function AboutSection({ className }: AboutSectionProps) {
  const shouldReduceMotion = useReducedMotion();

  const values = [
    {
      icon: "🔍",
      title: "Transparency",
      description: "Every projection traces back to source studies. No black boxes."
    },
    {
      icon: "⚖️",
      title: "Equity", 
      description: "Outcomes stratified by population. See who benefits, who bears costs."
    },
    {
      icon: "📚",
      title: "Evidence",
      description: "2000+ mechanisms derived from peer-reviewed literature."
    }
  ];

  return (
    <section className={cn("py-24 md:py-32 bg-gray-50", className)}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={shouldReduceMotion ? "visible" : "hidden"}
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={sectionVariants}
          className="text-center"
        >
          {/* Mission Statement */}
          <motion.div variants={fadeInUp} className="max-w-4xl mx-auto mb-20">
            <h2 className="text-4xl md:text-5xl lg:text-6xl font-semibold tracking-tight text-gray-900 mb-8">
              Our Mission
            </h2>
            <p className="text-xl md:text-2xl font-medium text-gray-600 leading-relaxed">
              Enable evidence-based decision-making for structural health interventions by making complex causal pathways visible, quantifiable, and actionable.
            </p>
          </motion.div>

          {/* Core Values */}
          <motion.div
            variants={staggerContainer}
            className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20"
          >
            {values.map((value) => (
              <motion.div
                key={value.title}
                variants={cardVariants}
                whileHover={shouldReduceMotion ? {} : { scale: 1.02 }}
                className="bg-white rounded-2xl border border-gray-200 p-8 shadow-sm hover:shadow-lg transition-all duration-300"
              >
                <div className="text-4xl mb-6">{value.icon}</div>
                <h3 className="text-2xl font-semibold text-gray-900 mb-4">
                  {value.title}
                </h3>
                <p className="text-base md:text-lg text-gray-600 leading-relaxed">
                  {value.description}
                </p>
              </motion.div>
            ))}
          </motion.div>

          {/* What Makes Us Different */}
          <motion.div
            variants={slideInRight}
            className="max-w-4xl mx-auto"
          >
            <div className="bg-gradient-to-br from-primary-500 to-secondary-500 rounded-2xl p-8 md:p-12 text-white shadow-lg">
              <h3 className="text-2xl md:text-3xl font-semibold mb-6">
                What Makes Us Different
              </h3>
              <p className="text-lg md:text-xl leading-relaxed opacity-95">
                Unlike traditional health impact assessments that take months and produce qualitative reports, HealthSystems delivers quantified projections in seconds—all auditable to source research.
              </p>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}