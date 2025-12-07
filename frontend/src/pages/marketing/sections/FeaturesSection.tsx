'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';
import { useRef, useState, MouseEvent } from 'react';

interface FeaturesSectionProps {
  className?: string;
}

interface Feature {
  icon: string;
  title: string;
  description: string;
}

interface FeatureCardProps {
  feature: Feature;
}

const features: Feature[] = [
  {
    icon: '🗺️',
    title: 'Interactive Systems Mapping',
    description: 'Visualize 400+ nodes and 2000+ mechanisms showing how structural conditions connect to health outcomes.'
  },
  {
    icon: '🤖',
    title: 'LLM-Synthesized Evidence',
    description: 'Mechanisms extracted from literature using Claude AI, with full audit trail from studies to projections.'
  },
  {
    icon: '🏛️',
    title: 'Structural Competency Framework',
    description: 'Focus on root causes—policy, housing, economics—not individual behavior. Explicit equity lens throughout.'
  },
  {
    icon: '⚡',
    title: 'Real-Time Scenario Modeling',
    description: 'Seconds-to-answers analysis. "What if we shift $50M to this intervention?" See results instantly.'
  },
  {
    icon: '⚖️',
    title: 'Equity-Centered Analysis',
    description: 'Every projection stratified by race, SES, insurance status. Identify what reduces disparities.'
  },
  {
    icon: '🔍',
    title: 'Transparent Assumptions',
    description: 'Click any number to see source studies. Challenge assumptions, propose improvements.'
  }
];

const fadeInUp = {
  hidden: { opacity: 0, y: 15 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.3, ease: "easeOut" } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.05, delayChildren: 0.08 } }
};

const cardVariants = {
  hidden: { opacity: 0, y: 15 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.3, ease: "easeOut" } }
};

function FeatureCard({ feature }: FeatureCardProps) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [isHovered, setIsHovered] = useState(false);
  const shouldReduceMotion = useReducedMotion();

  const handleMouseMove = (e: MouseEvent<HTMLDivElement>) => {
    if (shouldReduceMotion || !cardRef.current) return;

    const rect = cardRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = (y - centerY) / 20;
    const rotateY = (centerX - x) / 20;

    cardRef.current.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
  };

  const handleMouseLeave = () => {
    if (shouldReduceMotion || !cardRef.current) return;
    setIsHovered(false);
    cardRef.current.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
  };

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  return (
    <motion.div
      variants={cardVariants}
      className="group"
    >
      <div
        ref={cardRef}
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        onMouseEnter={handleMouseEnter}
        className={cn(
          "relative p-8 bg-white border border-gray-200 rounded-2xl",
          "transition-all duration-300 cursor-pointer",
          "hover:shadow-lg",
          isHovered && !shouldReduceMotion && "shadow-lg",
          !shouldReduceMotion && "transform-gpu"
        )}
        style={shouldReduceMotion ? {} : { transition: 'box-shadow 0.3s ease, transform 0.1s ease' }}
      >
        <div className="flex flex-col items-start space-y-4">
          <div className="text-4xl md:text-5xl" role="img" aria-label={feature.title}>
            {feature.icon}
          </div>
          <h3 className="text-xl font-semibold text-gray-900 tracking-tight">
            {feature.title}
          </h3>
          <p className="text-base text-gray-600 leading-relaxed">
            {feature.description}
          </p>
        </div>
        
        {/* Hover glow effect */}
        <div 
          className={cn(
            "absolute inset-0 rounded-2xl transition-opacity duration-300",
            "bg-gradient-to-br from-primary-500/5 to-secondary-500/5",
            "opacity-0 group-hover:opacity-100"
          )}
        />
      </div>
    </motion.div>
  );
}

export function FeaturesSection({ className }: FeaturesSectionProps) {
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
            What We Can Do
          </h2>
          <p className="text-xl md:text-2xl font-medium text-gray-600 max-w-3xl mx-auto">
            Built for policymakers, foundations, and community organizations
          </p>
        </motion.div>

        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-50px" }}
          variants={staggerContainer}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
        >
          {features.map((feature, index) => (
            <FeatureCard
              key={index}
              feature={feature}
            />
          ))}
        </motion.div>
      </div>
    </section>
  );
}