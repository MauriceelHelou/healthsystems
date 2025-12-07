'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';
import { useState, useEffect } from 'react';

interface TestimonialsSectionProps {
  className?: string;
}

export interface Testimonial {
  id: string;
  quote: string;
  name: string;
  title: string;
  organization: string;
  image?: string;
}

const testimonials: Testimonial[] = [
  {
    id: '1',
    quote: "For the first time, we can show our legislature exactly which interventions prevent the most health crises—and for whom. This changes how we justify our $800M budget.",
    name: "Dr. Amanda Foster",
    title: "Director of Population Health",
    organization: "State Health Department"
  },
  {
    id: '2',
    quote: "We fund 50 programs across 5 states. Now we can finally compare apples to apples and understand which investments create the most equitable outcomes.",
    name: "Michael Torres",
    title: "VP of Health Initiatives",
    organization: "Community Foundation"
  },
  {
    id: '3',
    quote: "Our housing advocacy work saves lives—we always knew it, but couldn't prove it in terms funders understand. Now we can compete with clinical interventions for resources.",
    name: "Rev. Patricia Williams",
    title: "Executive Director",
    organization: "Community Health Alliance"
  }
];

const fadeInUp = {
  hidden: { opacity: 0, y: 15 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.3, ease: "easeOut" } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.08, delayChildren: 0.1 } }
};

const cardVariants = {
  hidden: { opacity: 0, y: 20, scale: 0.98 },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { duration: 0.35, ease: "easeOut" }
  }
};

export function TestimonialsSection({ className }: TestimonialsSectionProps) {
  const shouldReduceMotion = useReducedMotion();
  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    if (shouldReduceMotion) return;
    
    const interval = setInterval(() => {
      setActiveIndex((current) => (current + 1) % testimonials.length);
    }, 8000);

    return () => clearInterval(interval);
  }, [shouldReduceMotion]);

  return (
    <section className={cn("py-24 md:py-32 bg-gray-50", className)}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={staggerContainer}
          className="text-center mb-16"
        >
          <motion.h2 
            variants={fadeInUp}
            className="text-4xl md:text-5xl font-semibold tracking-tight text-gray-900 mb-4"
          >
            What People Are Saying
          </motion.h2>
          <motion.p 
            variants={fadeInUp}
            className="text-xl md:text-2xl font-medium text-gray-600 max-w-3xl mx-auto"
          >
            Leaders across the health sector are transforming how they make decisions
          </motion.p>
        </motion.div>

        {/* Desktop Grid */}
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={staggerContainer}
          className="hidden lg:grid grid-cols-3 gap-8"
        >
          {testimonials.map((testimonial) => (
            <motion.div
              key={testimonial.id}
              variants={cardVariants}
              className="bg-white rounded-2xl border border-gray-200 p-8 shadow-sm hover:shadow-lg transition-all duration-300 hover:scale-[1.02] relative"
            >
              <div className="absolute -top-2 -left-2 text-6xl text-gray-200 font-serif leading-none select-none">
                "
              </div>
              <blockquote className="relative z-10">
                <p className="text-lg md:text-xl text-gray-700 leading-relaxed italic mb-6 font-medium">
                  {testimonial.quote}
                </p>
                <footer className="not-italic">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center text-white font-semibold">
                      {testimonial.name.charAt(0)}
                    </div>
                    <div>
                      <cite className="block text-gray-900 font-semibold not-italic">
                        {testimonial.name}
                      </cite>
                      <div className="text-gray-600 text-sm">
                        {testimonial.title}
                      </div>
                      <div className="text-gray-500 text-sm font-medium">
                        {testimonial.organization}
                      </div>
                    </div>
                  </div>
                </footer>
              </blockquote>
            </motion.div>
          ))}
        </motion.div>

        {/* Mobile Carousel */}
        <div className="lg:hidden">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={fadeInUp}
            className="relative overflow-hidden"
          >
            <div 
              className="flex transition-transform duration-500 ease-in-out"
              style={{ transform: `translateX(-${activeIndex * 100}%)` }}
            >
              {testimonials.map((testimonial) => (
                <div
                  key={testimonial.id}
                  className="w-full flex-shrink-0 px-4"
                >
                  <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm relative max-w-lg mx-auto">
                    <div className="absolute -top-2 -left-2 text-6xl text-gray-200 font-serif leading-none select-none">
                      "
                    </div>
                    <blockquote className="relative z-10">
                      <p className="text-lg text-gray-700 leading-relaxed italic mb-6 font-medium">
                        {testimonial.quote}
                      </p>
                      <footer className="not-italic">
                        <div className="flex items-center space-x-3">
                          <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center text-white font-semibold text-sm">
                            {testimonial.name.charAt(0)}
                          </div>
                          <div>
                            <cite className="block text-gray-900 font-semibold not-italic text-sm">
                              {testimonial.name}
                            </cite>
                            <div className="text-gray-600 text-xs">
                              {testimonial.title}
                            </div>
                            <div className="text-gray-500 text-xs font-medium">
                              {testimonial.organization}
                            </div>
                          </div>
                        </div>
                      </footer>
                    </blockquote>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Dots Indicator */}
          <div className="flex justify-center mt-8 space-x-2">
            {testimonials.map((_, index) => (
              <button
                key={index}
                onClick={() => setActiveIndex(index)}
                className={cn(
                  "w-3 h-3 rounded-full transition-all duration-300",
                  activeIndex === index 
                    ? "bg-primary-500 w-8" 
                    : "bg-gray-300 hover:bg-gray-400"
                )}
                aria-label={`Go to testimonial ${index + 1}`}
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}