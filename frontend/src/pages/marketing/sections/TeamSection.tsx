'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

interface TeamSectionProps {
  className?: string;
}

interface TeamMember {
  id: string;
  name: string;
  role: string;
  affiliation: string;
  bio: string;
  initials: string;
}

interface Advisor {
  id: string;
  name: string;
  affiliation: string;
}

const coreTeam: TeamMember[] = [
  {
    id: '1',
    name: 'Maurice el Helou',
    role: 'MDE Candidate',
    affiliation: 'Harvard Graduate School of Design',
    bio: 'Architecture and urban systems background. Building tools that make structural determinants legible to policymakers.',
    initials: 'ME'
  },
  {
    id: '2',
    name: 'Noah Johnson',
    role: 'PhD Candidate',
    affiliation: 'Harvard Chan School of Public Health',
    bio: 'Social epidemiology focus. Translating population health research into actionable system models.',
    initials: 'NJ'
  }
];

const advisors: Advisor[] = [
  {
    id: '1',
    name: 'Rob McIsaac',
    affiliation: 'Invest Health'
  },
  {
    id: '2',
    name: 'David Yarkin',
    affiliation: 'Invest Health'
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

export function TeamSection({ className }: TeamSectionProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <section className={cn("py-24 md:py-32 bg-white", className)}>
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
              Team
            </p>
            <h2 className="text-3xl md:text-4xl font-medium tracking-tight text-slate-900 leading-tight">
              Who We Are
            </h2>
          </motion.div>

          {/* Core Team */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
            {coreTeam.map((member) => (
              <motion.div
                key={member.id}
                variants={fadeInUp}
                className="bg-slate-50 rounded-xl p-6"
              >
                <div className="flex items-start gap-5">
                  {/* Avatar */}
                  <div className="flex-shrink-0 w-14 h-14 bg-slate-200 rounded-full flex items-center justify-center text-slate-600 font-medium text-lg">
                    {member.initials}
                  </div>

                  {/* Info */}
                  <div className="flex-1">
                    <h3 className="text-lg font-medium text-slate-900">
                      {member.name}
                    </h3>
                    <p className="text-sm text-slate-600 mt-0.5">
                      {member.role}
                    </p>
                    <p className="text-sm text-slate-500">
                      {member.affiliation}
                    </p>
                    <p className="text-sm text-slate-600 leading-relaxed mt-3">
                      {member.bio}
                    </p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Advisors */}
          <motion.div variants={fadeInUp}>
            <p className="text-sm font-medium text-slate-500 uppercase tracking-wider mb-6">
              Advisors
            </p>
            <div className="flex flex-wrap gap-6">
              {advisors.map((advisor) => (
                <div key={advisor.id} className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-slate-100 rounded-full flex items-center justify-center text-slate-500 font-medium text-sm">
                    {advisor.name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div>
                    <p className="text-sm font-medium text-slate-900">{advisor.name}</p>
                    <p className="text-xs text-slate-500">{advisor.affiliation}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
