'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

interface TestimonialsSectionProps {
  className?: string;
}

interface Testimonial {
  id: string;
  quote: string;
  name: string;
  title: string;
  organization: string;
}

const testimonials: Testimonial[] = [
  {
    id: '1',
    quote: "Social epidemiology has known these pathways exist for decades. What's been missing is a tool that makes them visible and actionable for the people who can actually change them.",
    name: "Ichiro Kawachi",
    title: "Professor of Social Epidemiology",
    organization: "Harvard Chan School of Public Health"
  },
  {
    id: '2',
    quote: "We've needed this for years. A way to show policymakers exactly how housing connects to hospitalizations, with the evidence to back it up.",
    name: "Tamara Wallington",
    title: "Director of Community Health",
    organization: "Health System Partner"
  },
  {
    id: '3',
    quote: "The platform does something we've struggled with for a long time: it makes the case for upstream investment in terms that resonate with budget committees.",
    name: "Rob McIsaac",
    title: "Executive Director",
    organization: "Invest Health"
  }
];

const fadeInUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4, ease: [0.25, 0.1, 0.25, 1] } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1, delayChildren: 0.1 } }
};

export function TestimonialsSection({ className }: TestimonialsSectionProps) {
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
              Perspectives
            </p>
            <h2 className="text-3xl md:text-4xl font-medium tracking-tight text-slate-900 leading-tight">
              What Experts Say
            </h2>
          </motion.div>

          {/* Testimonials Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {testimonials.map((testimonial) => (
              <motion.div
                key={testimonial.id}
                variants={fadeInUp}
                className="bg-white rounded-xl border border-slate-200 p-6"
              >
                <blockquote>
                  <p className="text-base text-slate-700 leading-relaxed mb-6">
                    "{testimonial.quote}"
                  </p>
                  <footer>
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-slate-100 rounded-full flex items-center justify-center text-slate-500 font-medium text-sm">
                        {testimonial.name.split(' ').map(n => n[0]).join('')}
                      </div>
                      <div>
                        <cite className="block text-sm font-medium text-slate-900 not-italic">
                          {testimonial.name}
                        </cite>
                        <div className="text-xs text-slate-500">
                          {testimonial.title}
                        </div>
                        <div className="text-xs text-slate-400">
                          {testimonial.organization}
                        </div>
                      </div>
                    </div>
                  </footer>
                </blockquote>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
