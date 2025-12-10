'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

interface ValidationSectionProps {
  className?: string;
}

interface ExpertQuote {
  id: string;
  quote: string;
  author: string;
  title: string;
  organization: string;
}

const expertQuotes: ExpertQuote[] = [
  {
    id: '1',
    quote: "What is it that we didn't know about investing in different kinds of social determinants? I think this has potential to reveal something that we didn't know.",
    author: "Ichiro Kawachi",
    title: "Professor of Social Epidemiology",
    organization: "Harvard School of Public Health"
  },
  {
    id: '2',
    quote: "There's excitement about mapping these systems. There's a need to do it that we're not doing right now in any comprehensive way.",
    author: "Brendan Smith",
    title: "Senior Epidemiologist",
    organization: "Public Health Ontario"
  },
  {
    id: '3',
    quote: "There is a huge opportunity here for hospital systems looking to identify what causes their at-risk patients to get sick and where to intervene.",
    author: "Rob McIsaac",
    title: "Former CEO",
    organization: "Hamilton Health Sciences"
  },
  {
    id: '4',
    quote: "I do think there could be really cool opportunities for this work because it is very relevant to the public health challenges we're trying to grapple with.",
    author: "Erin Hobin",
    title: "Senior Scientist",
    organization: "Public Health Ontario"
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

export function ValidationSection({ className }: ValidationSectionProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <section id="validation" className={cn("py-24 md:py-32", className)}>
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
              Validation
            </p>
            <h2 className="text-3xl md:text-4xl font-medium tracking-tight text-slate-900 leading-tight">
              What Experts Say
            </h2>
          </motion.div>

          {/* 2x2 Quote Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {expertQuotes.map((item) => (
              <motion.div
                key={item.id}
                variants={fadeInUp}
                className="bg-slate-50 rounded-xl p-8"
              >
                <blockquote>
                  <p className="text-lg text-slate-700 leading-relaxed mb-6">
                    "{item.quote}"
                  </p>
                  <footer className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-slate-200 rounded-full flex items-center justify-center text-slate-600 font-medium text-sm">
                      {item.author.split(' ').map(n => n[0]).join('')}
                    </div>
                    <div>
                      <cite className="block text-base font-medium text-slate-900 not-italic">
                        {item.author}
                      </cite>
                      <div className="text-sm text-slate-500">
                        {item.title}, {item.organization}
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
