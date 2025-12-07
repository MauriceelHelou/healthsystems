/**
 * Team Member Data
 *
 * PLACEHOLDER DATA - Replace with actual team information.
 *
 * To update:
 * 1. Replace name, role, bio with real information
 * 2. Add actual image URLs or keep gradient placeholders
 * 3. Update social links
 */

export interface TeamMember {
  id: string;
  name: string;
  role: string;
  bio: string;
  image?: string;
  // Gradient colors for placeholder avatar (used when no image)
  gradientFrom: string;
  gradientTo: string;
  linkedin?: string;
  twitter?: string;
  email?: string;
}

export const TEAM_MEMBERS: TeamMember[] = [
  {
    id: 'member-1',
    name: 'Dr. Sarah Chen', // PLACEHOLDER
    role: 'Principal Investigator',
    bio: 'Professor of Population Health Sciences with 15 years of experience in health equity research and systems modeling.',
    gradientFrom: '#0ea5e9', // primary-500
    gradientTo: '#0369a1', // primary-700
    linkedin: 'https://linkedin.com/in/placeholder', // PLACEHOLDER
    twitter: 'https://twitter.com/placeholder', // PLACEHOLDER
  },
  {
    id: 'member-2',
    name: 'Dr. Marcus Johnson', // PLACEHOLDER
    role: 'Director of Data Science',
    bio: 'Former CDC epidemiologist specializing in causal inference and machine learning applications in public health.',
    gradientFrom: '#a855f7', // secondary-500
    gradientTo: '#7e22ce', // secondary-700
    linkedin: 'https://linkedin.com/in/placeholder', // PLACEHOLDER
  },
  {
    id: 'member-3',
    name: 'Dr. Elena Rodriguez', // PLACEHOLDER
    role: 'Community Engagement Lead',
    bio: 'Community health advocate with deep expertise in translating research into actionable policy recommendations.',
    gradientFrom: '#f97316', // orange-500
    gradientTo: '#c2410c', // orange-700
    linkedin: 'https://linkedin.com/in/placeholder', // PLACEHOLDER
    twitter: 'https://twitter.com/placeholder', // PLACEHOLDER
  },
  {
    id: 'member-4',
    name: 'Dr. James Park', // PLACEHOLDER
    role: 'Technical Architect',
    bio: 'Full-stack engineer with background in health informatics and decision support systems.',
    gradientFrom: '#10b981', // emerald-500
    gradientTo: '#047857', // emerald-700
    linkedin: 'https://linkedin.com/in/placeholder', // PLACEHOLDER
  },
];

export const TEAM_SECTION_CONTENT = {
  title: 'Our Team',
  subtitle: 'Researchers, engineers, and advocates working to transform health policy',
} as const;

/**
 * Helper to get initials from name
 */
export function getInitials(name: string): string {
  return name
    .split(' ')
    .map((part) => part[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
}

/**
 * Helper to generate a consistent avatar placeholder
 */
export function getAvatarStyle(member: TeamMember): React.CSSProperties {
  return {
    background: `linear-gradient(135deg, ${member.gradientFrom}, ${member.gradientTo})`,
  };
}
