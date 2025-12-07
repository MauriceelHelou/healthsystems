'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { cn } from '../../../utils/classNames';

// Types
interface TeamSectionProps {
  className?: string;
}

export interface TeamMember {
  id: string;
  name: string;
  role: string;
  bio: string;
  image?: string;
  linkedin?: string;
  twitter?: string;
  gradientFrom?: string;
  gradientTo?: string;
  initials?: string;
}

// Team data
const teamMembers: TeamMember[] = [
  {
    id: '1',
    name: 'Dr. Sarah Chen',
    role: 'Principal Investigator',
    bio: 'Professor of Population Health Sciences with 15 years of experience in health equity research and systems modeling.',
    gradientFrom: 'from-blue-500',
    gradientTo: 'to-purple-600',
    initials: 'SC',
    linkedin: '#',
    twitter: '#'
  },
  {
    id: '2',
    name: 'Dr. Marcus Johnson',
    role: 'Director of Data Science',
    bio: 'Former CDC epidemiologist specializing in causal inference and machine learning applications in public health.',
    gradientFrom: 'from-purple-500',
    gradientTo: 'to-pink-600',
    initials: 'MJ',
    linkedin: '#',
    twitter: '#'
  },
  {
    id: '3',
    name: 'Dr. Elena Rodriguez',
    role: 'Community Engagement Lead',
    bio: 'Community health advocate with deep expertise in translating research into actionable policy recommendations.',
    gradientFrom: 'from-orange-500',
    gradientTo: 'to-red-600',
    initials: 'ER',
    linkedin: '#',
    twitter: '#'
  },
  {
    id: '4',
    name: 'Dr. James Park',
    role: 'Technical Architect',
    bio: 'Full-stack engineer with background in health informatics and decision support systems.',
    gradientFrom: 'from-green-500',
    gradientTo: 'to-blue-600',
    initials: 'JP',
    linkedin: '#',
    twitter: '#'
  }
];

// Animation variants
const fadeInUp = {
  hidden: { opacity: 0, y: 15 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.3, ease: "easeOut" } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.05, delayChildren: 0.08 } }
};

const cardHover = {
  y: -6,
  transition: { duration: 0.2, ease: "easeOut" }
};

const avatarHover = {
  scale: 1.05,
  transition: { duration: 0.2, ease: "easeOut" }
};

// Social icon components
const LinkedInIcon = () => (
  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
    <path fillRule="evenodd" d="M16.338 16.338H13.67V12.16c0-.995-.017-2.277-1.387-2.277-1.39 0-1.601 1.086-1.601 2.207v4.248H8.014v-8.59h2.559v1.174h.037c.356-.675 1.227-1.387 2.526-1.387 2.703 0 3.203 1.778 3.203 4.092v4.711zM5.005 6.575a1.548 1.548 0 11-.003-3.096 1.548 1.548 0 01.003 3.096zm-1.337 9.763H6.34v-8.59H3.667v8.59zM17.668 1H2.328C1.595 1 1 1.581 1 2.298v15.403C1 18.418 1.595 19 2.328 19h15.34c.734 0 1.332-.582 1.332-1.299V2.298C19 1.581 18.402 1 17.668 1z" clipRule="evenodd" />
  </svg>
);

const TwitterIcon = () => (
  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
    <path d="M6.29 18.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0020 3.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.073 4.073 0 01.8 7.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 010 16.407a11.616 11.616 0 006.29 1.84" />
  </svg>
);

export function TeamSection({ className }: TeamSectionProps) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <section className={cn("py-24 md:py-32 bg-white", className)}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={shouldReduceMotion ? undefined : "hidden"}
          whileInView={shouldReduceMotion ? undefined : "visible"}
          viewport={{ once: true, margin: "-100px" }}
          variants={fadeInUp}
          className="text-center mb-16 md:mb-20"
        >
          <h2 className="text-4xl md:text-5xl lg:text-6xl font-semibold tracking-tight text-gray-900 mb-6">
            Our Team
          </h2>
          <p className="text-xl md:text-2xl font-medium text-gray-600 max-w-3xl mx-auto">
            Researchers, engineers, and advocates working to transform health policy
          </p>
        </motion.div>

        <motion.div
          initial={shouldReduceMotion ? undefined : "hidden"}
          whileInView={shouldReduceMotion ? undefined : "visible"}
          viewport={{ once: true, margin: "-100px" }}
          variants={staggerContainer}
          className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-8"
        >
          {teamMembers.map((member) => (
            <motion.div
              key={member.id}
              variants={fadeInUp}
              whileHover={shouldReduceMotion ? undefined : cardHover}
              className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm hover:shadow-lg transition-all duration-300 text-center"
            >
              {/* Avatar */}
              <motion.div
                whileHover={shouldReduceMotion ? undefined : avatarHover}
                className="relative mx-auto mb-6"
              >
                <div className={cn(
                  "w-20 h-20 md:w-28 md:h-28 lg:w-32 lg:h-32 rounded-full bg-gradient-to-br flex items-center justify-center text-white font-semibold text-lg md:text-xl lg:text-2xl shadow-lg",
                  member.gradientFrom,
                  member.gradientTo
                )}>
                  {member.image ? (
                    <img
                      src={member.image}
                      alt={member.name}
                      className="w-full h-full rounded-full object-cover"
                    />
                  ) : (
                    <span>{member.initials}</span>
                  )}
                </div>
              </motion.div>

              {/* Name */}
              <h3 className="text-xl md:text-2xl font-semibold text-gray-900 mb-2">
                {member.name}
              </h3>

              {/* Role */}
              <p className="text-sm font-medium text-primary-500 uppercase tracking-wide mb-4">
                {member.role}
              </p>

              {/* Bio */}
              <p className="text-sm md:text-base text-gray-600 leading-relaxed mb-6">
                {member.bio}
              </p>

              {/* Social Links */}
              <div className="flex justify-center space-x-4">
                {member.linkedin && (
                  <a
                    href={member.linkedin}
                    className="text-gray-400 hover:text-primary-500 transition-colors duration-200"
                    aria-label={`${member.name} LinkedIn profile`}
                  >
                    <LinkedInIcon />
                  </a>
                )}
                {member.twitter && (
                  <a
                    href={member.twitter}
                    className="text-gray-400 hover:text-primary-500 transition-colors duration-200"
                    aria-label={`${member.name} Twitter profile`}
                  >
                    <TwitterIcon />
                  </a>
                )}
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}