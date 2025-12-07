'use client';

import { motion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

interface FooterCTASectionProps {
  onGetStarted?: () => void;
  onContact?: () => void;
  className?: string;
}

const fadeInUp = {
  hidden: { opacity: 0, y: 15 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.3, ease: "easeOut" } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.05, delayChildren: 0.08 } }
};

export function FooterCTASection({ onGetStarted, onContact, className }: FooterCTASectionProps) {
  const handleGetStarted = () => {
    if (onGetStarted) {
      onGetStarted();
    } else {
      window.location.href = '/systems';
    }
  };

  const handleContact = () => {
    if (onContact) {
      onContact();
    } else {
      window.location.href = 'mailto:hello@healthsystems.platform';
    }
  };

  return (
    <div className={cn("relative", className)}>
      {/* CTA Section */}
      <section className="relative py-24 md:py-32 bg-gradient-to-br from-primary-50 via-white to-secondary-50 overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-20">
          <svg className="w-full h-full" viewBox="0 0 100 100" fill="none">
            <defs>
              <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
                <path d="M 10 0 L 0 0 0 10" fill="none" stroke="currentColor" strokeWidth="0.5" className="text-primary-200"/>
              </pattern>
            </defs>
            <rect width="100" height="100" fill="url(#grid)" />
          </svg>
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={staggerContainer}
            className="text-center max-w-4xl mx-auto"
          >
            <motion.h2
              variants={fadeInUp}
              className="text-4xl md:text-5xl lg:text-6xl font-semibold tracking-tight text-gray-900 mb-6"
            >
              Ready to transform how you approach health equity?
            </motion.h2>

            <motion.p
              variants={fadeInUp}
              className="text-xl md:text-2xl font-medium text-gray-600 mb-12 leading-relaxed"
            >
              Join state health departments, foundations, and community organizations already using evidence-based systems thinking.
            </motion.p>

            <motion.div
              variants={fadeInUp}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center"
            >
              <button
                onClick={handleGetStarted}
                className={cn(
                  "group relative px-8 py-4 bg-primary-500 text-white font-semibold rounded-xl",
                  "shadow-lg shadow-primary-500/25 hover:shadow-xl hover:shadow-primary-500/40",
                  "transition-all duration-300 hover:scale-[1.02] active:scale-[0.98]",
                  "focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2",
                  "min-w-[160px] min-h-[56px] text-lg"
                )}
              >
                <span className="relative z-10">Get Started</span>
                <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-primary-600 to-primary-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
              </button>

              <button
                onClick={handleContact}
                className={cn(
                  "group px-8 py-4 border-2 border-gray-300 text-gray-700 font-semibold rounded-xl",
                  "hover:border-gray-400 hover:text-gray-800 hover:bg-gray-50",
                  "transition-all duration-300 hover:scale-[1.02] active:scale-[0.98]",
                  "focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2",
                  "min-w-[160px] min-h-[56px] text-lg"
                )}
              >
                Contact Us
              </button>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <p className="text-gray-400 text-center sm:text-left">
              © 2025 HealthSystems Platform. Built with evidence.
            </p>

            <div className="flex items-center gap-6">
              <a
                href="/methodology"
                className="text-gray-400 hover:text-white transition-colors duration-200"
              >
                Methodology
              </a>
              <a
                href="/mechanisms"
                className="text-gray-400 hover:text-white transition-colors duration-200"
              >
                Mechanism Bank
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}