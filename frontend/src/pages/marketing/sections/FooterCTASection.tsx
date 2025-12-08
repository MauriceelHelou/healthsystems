'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

interface FooterCTASectionProps {
  className?: string;
}

const fadeInUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4, ease: [0.25, 0.1, 0.25, 1] } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.08, delayChildren: 0.1 } }
};

export function FooterCTASection({ className }: FooterCTASectionProps) {
  const shouldReduceMotion = useReducedMotion();

  const handleExplore = () => {
    window.location.href = '/systems';
  };

  const handleContact = () => {
    window.location.href = 'mailto:maurice_elhelou@gsd.harvard.edu';
  };

  return (
    <div className={cn("relative", className)}>
      {/* CTA Section */}
      <section className="py-24 md:py-32 bg-slate-900">
        <div className="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12">
          <motion.div
            initial={shouldReduceMotion ? "visible" : "hidden"}
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={staggerContainer}
            className="max-w-3xl"
          >
            <motion.p
              variants={fadeInUp}
              className="text-sm font-medium text-slate-400 uppercase tracking-wider mb-4"
            >
              Get Involved
            </motion.p>

            <motion.h2
              variants={fadeInUp}
              className="text-3xl md:text-4xl font-medium tracking-tight text-white leading-tight mb-6"
            >
              Partner With Us
            </motion.h2>

            <motion.p
              variants={fadeInUp}
              className="text-lg text-slate-400 leading-relaxed mb-10"
            >
              We're looking for pilot partners: state health departments, hospital systems,
              and foundations interested in testing the platform with their data and use cases.
              Early partners shape product direction.
            </motion.p>

            <motion.div
              variants={fadeInUp}
              className="flex flex-col sm:flex-row gap-4"
            >
              <button
                onClick={handleExplore}
                className={cn(
                  "px-6 py-3 bg-white text-slate-900 font-medium rounded-lg",
                  "hover:bg-slate-100 transition-colors duration-200",
                  "focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-slate-900"
                )}
              >
                Explore the Prototype
              </button>

              <button
                onClick={handleContact}
                className={cn(
                  "px-6 py-3 border border-slate-600 text-slate-300 font-medium rounded-lg",
                  "hover:border-slate-500 hover:text-white transition-colors duration-200",
                  "focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2 focus:ring-offset-slate-900"
                )}
              >
                Contact Us
              </button>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-950 py-8">
        <div className="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <p className="text-sm text-slate-500">
              Harvard Graduate School of Design + Harvard Chan School of Public Health
            </p>
            <p className="text-sm text-slate-600">
              2025
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
