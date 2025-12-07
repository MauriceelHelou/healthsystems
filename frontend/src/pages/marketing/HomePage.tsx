'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { cn } from '../../utils/classNames';
import { HeroSection } from './sections/HeroSection';
import { AboutSection } from './sections/AboutSection';
import { FeaturesSection } from './sections/FeaturesSection';
import { HowToUseSection } from './sections/HowToUseSection';
import { RoadmapSection } from './sections/RoadmapSection';
import { TeamSection } from './sections/TeamSection';
import { TestimonialsSection } from './sections/TestimonialsSection';
import { FooterCTASection } from './sections/FooterCTASection';

// Animation variants
const scrollProgressVariants = {
  hidden: { scaleX: 0 },
  visible: { scaleX: 1, transition: { duration: 0.3, ease: "easeOut" } }
};

const backToTopVariants = {
  hidden: { opacity: 0, y: 20, scale: 0.8 },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { duration: 0.3, ease: "easeOut" }
  }
};

export function HomePage() {
  const shouldReduceMotion = useReducedMotion();
  const navigate = useNavigate();
  const [scrollProgress, setScrollProgress] = useState(0);
  const [showBackToTop, setShowBackToTop] = useState(false);

  // Calculate scroll progress
  useEffect(() => {
    const calculateScrollProgress = () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      setScrollProgress(progress);
      setShowBackToTop(scrollTop > window.innerHeight);
    };

    window.addEventListener('scroll', calculateScrollProgress, { passive: true });
    return () => window.removeEventListener('scroll', calculateScrollProgress);
  }, []);

  // Smooth scroll utility
  const scrollToSection = useCallback((sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({
        behavior: shouldReduceMotion ? 'auto' : 'smooth',
        block: 'start'
      });
    }
  }, [shouldReduceMotion]);

  // Event handlers
  const handlePrimaryCTA = useCallback(() => {
    navigate('/systems');
  }, [navigate]);

  const handleSecondaryCTA = useCallback(() => {
    scrollToSection('about');
  }, [scrollToSection]);

  const handleTryNow = useCallback(() => {
    navigate('/systems');
  }, [navigate]);

  const handleGetStarted = useCallback(() => {
    navigate('/systems');
  }, [navigate]);

  const handleContact = useCallback(() => {
    window.open('mailto:hello@healthsystems.platform', '_blank');
  }, []);

  const handleBackToTop = useCallback(() => {
    scrollToSection('hero');
  }, [scrollToSection]);

  return (
    <div className="min-h-screen bg-white" style={{ scrollBehavior: shouldReduceMotion ? 'auto' : 'smooth' }}>
      {/* Scroll Progress Indicator */}
      <motion.div
        className="fixed top-0 left-0 right-0 z-50 h-1 bg-primary-500 origin-left"
        style={{ scaleX: scrollProgress / 100 }}
        variants={!shouldReduceMotion ? scrollProgressVariants : undefined}
        initial="hidden"
        animate="visible"
      />

      {/* Main Content */}
      <main className="relative">
        {/* Hero Section */}
        <HeroSection
          onPrimaryCTA={handlePrimaryCTA}
          onSecondaryCTA={handleSecondaryCTA}
        />

        {/* About Section */}
        <AboutSection
          className="bg-gray-50"
        />

        {/* Features Section */}
        <FeaturesSection
          className="bg-white"
        />

        {/* How to Use Section */}
        <HowToUseSection
          className="bg-gray-50"
          onTryNow={handleTryNow}
        />

        {/* Roadmap Section */}
        <RoadmapSection
          className="bg-white"
        />

        {/* Team Section */}
        <TeamSection
          className="bg-gray-50"
        />

        {/* Testimonials Section */}
        <TestimonialsSection
          className="bg-white"
        />

        {/* Footer CTA Section */}
        <FooterCTASection
          className="bg-gradient-to-br from-primary-500 to-secondary-500"
          onGetStarted={handleGetStarted}
          onContact={handleContact}
        />
      </main>

      {/* Back to Top Button */}
      <motion.button
        onClick={handleBackToTop}
        className={cn(
          "fixed bottom-8 right-8 z-40 p-3 rounded-full",
          "bg-primary-500 text-white shadow-lg hover:shadow-xl",
          "hover:scale-110 transition-all duration-300",
          "focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2",
          "min-w-[44px] min-h-[44px]"
        )}
        variants={!shouldReduceMotion ? backToTopVariants : undefined}
        initial="hidden"
        animate={showBackToTop ? "visible" : "hidden"}
        whileHover={!shouldReduceMotion ? { scale: 1.1 } : undefined}
        whileTap={!shouldReduceMotion ? { scale: 0.95 } : undefined}
        aria-label="Back to top"
      >
        <svg
          className="w-6 h-6 mx-auto"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M5 10l7-7m0 0l7 7m-7-7v18"
          />
        </svg>
      </motion.button>
    </div>
  );
}

export default HomePage;
