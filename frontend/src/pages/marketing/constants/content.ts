/**
 * Marketing Page Content
 *
 * All text content for the marketing page is centralized here.
 * This makes it easy to update copy without touching component code.
 *
 * Items marked with PLACEHOLDER should be replaced with real content.
 */

// =============================================================================
// HERO SECTION
// =============================================================================

export const HERO_CONTENT = {
  headline: 'Quantify How Policy Shapes Health',
  subheadline:
    'A decision support platform that maps how structural interventions—housing policy, Medicaid design, workforce development—cascade through causal pathways to affect health outcomes.',
  primaryCTA: 'Explore the Map',
  secondaryCTA: 'Learn More',
  primaryCTALink: '/systems',
  secondaryCTALink: '#about',
} as const;

// =============================================================================
// ABOUT SECTION
// =============================================================================

export const ABOUT_CONTENT = {
  mission:
    'Enable evidence-based decision-making for structural health interventions by making complex causal pathways visible, quantifiable, and actionable.',
  differentiator:
    'Unlike traditional health impact assessments that take months and produce qualitative reports, HealthSystems delivers quantified projections in seconds—all auditable to source research.',
  values: [
    {
      id: 'transparency',
      icon: '🔍',
      title: 'Transparency',
      description: 'Every projection traces back to source studies. No black boxes.',
    },
    {
      id: 'equity',
      icon: '⚖️',
      title: 'Equity',
      description: 'Outcomes stratified by population. See who benefits, who bears costs.',
    },
    {
      id: 'evidence',
      icon: '📊',
      title: 'Evidence',
      description: '2000+ mechanisms derived from peer-reviewed literature.',
    },
  ],
} as const;

// =============================================================================
// FEATURES SECTION
// =============================================================================

export const FEATURES_CONTENT = {
  title: 'What We Can Do',
  subtitle: 'Built for policymakers, foundations, and community organizations',
  features: [
    {
      id: 'systems-mapping',
      icon: '🗺️',
      title: 'Interactive Systems Mapping',
      description:
        'Visualize 400+ nodes and 2000+ mechanisms showing how structural conditions connect to health outcomes.',
    },
    {
      id: 'llm-evidence',
      icon: '🤖',
      title: 'LLM-Synthesized Evidence',
      description:
        'Mechanisms extracted from literature using Claude AI, with full audit trail from studies to projections.',
    },
    {
      id: 'structural-competency',
      icon: '🏛️',
      title: 'Structural Competency Framework',
      description:
        'Focus on root causes—policy, housing, economics—not individual behavior. Explicit equity lens throughout.',
    },
    {
      id: 'scenario-modeling',
      icon: '⚡',
      title: 'Real-Time Scenario Modeling',
      description:
        "Seconds-to-answers analysis. 'What if we shift $50M to this intervention?' See results instantly.",
    },
    {
      id: 'equity-analysis',
      icon: '📈',
      title: 'Equity-Centered Analysis',
      description:
        'Every projection stratified by race, SES, insurance status. Identify what reduces disparities.',
    },
    {
      id: 'transparent-assumptions',
      icon: '🔎',
      title: 'Transparent Assumptions',
      description:
        'Click any number to see source studies. Challenge assumptions, propose improvements.',
    },
  ],
} as const;

// =============================================================================
// HOW TO USE SECTION
// =============================================================================

export const HOW_TO_USE_CONTENT = {
  title: 'How It Works',
  subtitle: 'From question to evidence-based insight in minutes',
  steps: [
    {
      id: 'step-1',
      number: 1,
      title: 'Select Your Geography',
      description:
        'Choose a state, county, or city. The system automatically adapts to local policy context—Medicaid rules, housing protections, workforce programs.',
    },
    {
      id: 'step-2',
      number: 2,
      title: 'Identify Health Outcome',
      description:
        "Pick the crisis you're trying to prevent: cardiovascular events, alcohol-related mortality, housing instability, or 50+ other outcomes.",
    },
    {
      id: 'step-3',
      number: 3,
      title: 'Explore Pathways',
      description:
        'See which structural interventions matter most. Click nodes to understand mechanisms. Compare alternatives side-by-side.',
    },
    {
      id: 'step-4',
      number: 4,
      title: 'Model Scenarios',
      description:
        "Ask 'what if' questions. Shift resources between interventions. See projected outcomes with confidence intervals.",
    },
  ],
  ctaText: 'Try It Now',
  ctaLink: '/systems',
} as const;

// =============================================================================
// ROADMAP SECTION
// =============================================================================

export const ROADMAP_CONTENT = {
  title: "What We're Building",
  subtitle: 'A phased approach to comprehensive health systems modeling',
  phases: [
    {
      id: 'phase-1',
      status: 'complete' as const,
      title: 'Topology & Direction Discovery',
      description: 'Foundation of the causal network',
      features: [
        '2000 mechanisms identified and catalogued',
        '400+ nodes defined with specifications',
        'Direction of each mechanism (positive/negative)',
        'Literature lineage for every pathway',
      ],
    },
    {
      id: 'phase-2',
      status: 'in-progress' as const,
      title: 'Quantification & Modeling',
      description: 'Adding numerical precision',
      features: [
        'Effect size quantification with 95% CIs',
        'Meta-analytic pooling from 300+ studies',
        'Bayesian uncertainty propagation',
        'Intervention impact calculator',
      ],
    },
    {
      id: 'phase-3',
      status: 'planned' as const,
      title: 'Actor Network & Scale',
      description: 'Expanding reach and capability',
      features: [
        'Multi-geography deployment (50+ states/counties)',
        'Organizational collaboration mapping',
        'Real-time data integration',
        'Policy change alerts',
      ],
    },
  ],
} as const;

// =============================================================================
// TESTIMONIALS SECTION
// =============================================================================

export const TESTIMONIALS_CONTENT = {
  title: 'What People Are Saying',
  testimonials: [
    {
      id: 'testimonial-1',
      quote:
        'For the first time, we can show our legislature exactly which interventions prevent the most health crises—and for whom. This changes how we justify our $800M budget.',
      name: 'Dr. Amanda Foster', // PLACEHOLDER
      title: 'Director of Population Health',
      organization: 'State Health Department',
    },
    {
      id: 'testimonial-2',
      quote:
        'We fund 50 programs across 5 states. Now we can finally compare apples to apples and understand which investments create the most equitable outcomes.',
      name: 'Michael Torres', // PLACEHOLDER
      title: 'VP of Health Initiatives',
      organization: 'Community Foundation',
    },
    {
      id: 'testimonial-3',
      quote:
        "Our housing advocacy work saves lives—we always knew it, but couldn't prove it in terms funders understand. Now we can compete with clinical interventions for resources.",
      name: 'Rev. Patricia Williams', // PLACEHOLDER
      title: 'Executive Director',
      organization: 'Community Health Alliance',
    },
  ],
} as const;

// =============================================================================
// FOOTER / CTA SECTION
// =============================================================================

export const FOOTER_CTA_CONTENT = {
  headline: 'Ready to transform how you approach health equity?',
  subheadline:
    'Join state health departments, foundations, and community organizations already using evidence-based systems thinking.',
  primaryCTA: 'Get Started',
  secondaryCTA: 'Contact Us',
  primaryCTALink: '/systems',
  contactEmail: 'contact@healthsystems.dev', // PLACEHOLDER

  footerLinks: {
    product: [
      { label: 'Systems Map', href: '/systems' },
      { label: 'Documentation', href: '/docs' },
      { label: 'API Access', href: '/api' },
      { label: 'Changelog', href: '/changelog' },
    ],
    research: [
      { label: 'Methodology', href: '/methodology' },
      { label: 'Publications', href: '/publications' },
      { label: 'Data Sources', href: '/data-sources' },
      { label: 'Mechanism Bank', href: '/mechanisms' },
    ],
    community: [
      { label: 'GitHub', href: 'https://github.com/healthsystems' },
      { label: 'Discussions', href: 'https://github.com/healthsystems/discussions' },
      { label: 'Contributing', href: '/contributing' },
      { label: 'Code of Conduct', href: '/code-of-conduct' },
    ],
    legal: [
      { label: 'Privacy Policy', href: '/privacy' },
      { label: 'Terms of Service', href: '/terms' },
      { label: 'Data License', href: '/license' },
      { label: 'Accessibility', href: '/accessibility' },
    ],
  },

  social: {
    github: 'https://github.com/healthsystems', // PLACEHOLDER
    twitter: 'https://twitter.com/healthsystems', // PLACEHOLDER
    linkedin: 'https://linkedin.com/company/healthsystems', // PLACEHOLDER
  },

  copyright: '© 2024 HealthSystems Platform. Built with evidence.',
} as const;

// =============================================================================
// NAVIGATION
// =============================================================================

export const NAV_CONTENT = {
  brand: 'HealthSystems',
  links: [
    { label: 'About', href: '#about' },
    { label: 'Features', href: '#features' },
    { label: 'How It Works', href: '#how-to-use' },
    { label: 'Roadmap', href: '#roadmap' },
    { label: 'Team', href: '#team' },
  ],
  cta: {
    label: 'Explore Map',
    href: '/systems',
  },
} as const;

// =============================================================================
// TYPE EXPORTS
// =============================================================================

export type Feature = (typeof FEATURES_CONTENT.features)[number];
export type Step = (typeof HOW_TO_USE_CONTENT.steps)[number];
export type Phase = (typeof ROADMAP_CONTENT.phases)[number];
export type Testimonial = (typeof TESTIMONIALS_CONTENT.testimonials)[number];
export type Value = (typeof ABOUT_CONTENT.values)[number];
