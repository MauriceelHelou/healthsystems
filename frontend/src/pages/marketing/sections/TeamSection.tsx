'use client';

import { useState } from 'react';
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
  headshot: string;
  headshotLabel: string;
}

/**
 * Team headshots should be placed in: public/images/team/
 *
 * Required files:
 * - maurice-el-helou.jpg (400x400px recommended, square crop)
 * - noah-johnson.jpg (400x400px recommended, square crop)
 *
 * Image specifications:
 * - Format: JPG or PNG
 * - Size: 400x400px minimum (square aspect ratio)
 * - Style: Professional headshot, neutral background
 */
const coreTeam: TeamMember[] = [
  {
    id: '1',
    name: 'Maurice El Helou',
    role: 'Co-Founder',
    affiliation: 'Harvard GSD (Urban Planning + Design Studies) | McMaster Health Sciences',
    bio: 'Background in eco-social theory and built environment health impacts. Previously worked with Hamilton\'s public health department on data strategy.',
    initials: 'ME',
    headshot: '/images/team/maurice-el-helou.jpeg',
    headshotLabel: 'Maurice El Helou headshot'
  },
  {
    id: '2',
    name: 'Noah Johnson',
    role: 'Co-Founder',
    affiliation: 'Harvard GSD (Urban Planning) | Urban Institute (4 years)',
    bio: 'Quantitative policy analysis experience building government decision-support tools for housing and food access.',
    initials: 'NJ',
    headshot: '/images/team/noah-johnson.jpg',
    headshotLabel: 'Noah Johnson headshot'
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

function TeamMemberCard({ member }: { member: TeamMember }) {
  const [imageError, setImageError] = useState(false);

  return (
    <motion.div
      variants={fadeInUp}
      className="bg-slate-50 rounded-xl p-8"
    >
      <div className="flex flex-col items-center text-center">
        {/* Large Headshot with fallback to initials */}
        <figure className="mb-6">
          <div className="w-40 h-40 md:w-48 md:h-48 rounded-full overflow-hidden bg-slate-200">
            {!imageError ? (
              <img
                src={member.headshot}
                alt={member.headshotLabel}
                className="w-full h-full object-cover"
                onError={() => setImageError(true)}
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-slate-600 font-medium text-4xl">
                {member.initials}
              </div>
            )}
          </div>
          <figcaption className="mt-2 text-xs italic text-slate-400">
            {member.headshotLabel}
          </figcaption>
        </figure>

        {/* Info */}
        <div>
          <h3 className="text-xl font-medium text-slate-900">
            {member.name}
          </h3>
          <p className="text-base text-slate-600 mt-1">
            {member.role}
          </p>
          <p className="text-sm text-slate-500 mt-1">
            {member.affiliation}
          </p>
          <p className="text-sm text-slate-600 leading-relaxed mt-4 max-w-sm mx-auto">
            {member.bio}
          </p>
        </div>
      </div>
    </motion.div>
  );
}

export function TeamSection({ className }: TeamSectionProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <section id="team" className={cn("py-24 md:py-32 bg-white", className)}>
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
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {coreTeam.map((member) => (
              <TeamMemberCard key={member.id} member={member} />
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
