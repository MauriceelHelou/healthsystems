'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { cn } from '../../utils/classNames';
import { NetworkGraph3D } from './components/NetworkGraph3D';

const fadeInUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.25, 0.1, 0.25, 1] } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1, delayChildren: 0.2 } }
};

interface TeamContact {
  name: string;
  email: string;
  role: string;
}

const contacts: TeamContact[] = [
  {
    name: 'Maurice El Helou',
    email: 'maurice_elhelou@gsd.harvard.edu',
    role: 'Co-Founder'
  },
  {
    name: 'Noah Johnson',
    email: 'noah_johnson@gsd.harvard.edu',
    role: 'Co-Founder'
  }
];

export function ContactPage() {
  const shouldReduceMotion = useReducedMotion();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-950 relative overflow-hidden">
      {/* Full-screen 3D Network Graph Background */}
      <div className="absolute inset-0 opacity-50">
        <NetworkGraph3D nodeCount={200} />
      </div>

      {/* Gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-slate-950/80 via-slate-950/60 to-slate-950/80" />

      {/* Content */}
      <div className="relative z-10 min-h-screen flex flex-col">
        {/* Back button */}
        <div className="p-6 sm:p-8">
          <button
            onClick={() => navigate('/')}
            className={cn(
              "inline-flex items-center gap-2 text-slate-400 hover:text-white",
              "transition-colors duration-200"
            )}
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            <span>Back to Home</span>
          </button>
        </div>

        {/* Main content centered */}
        <div className="flex-1 flex items-center justify-center px-6 sm:px-8 pb-16">
          <motion.div
            initial={shouldReduceMotion ? "visible" : "hidden"}
            animate="visible"
            variants={staggerContainer}
            className="max-w-2xl w-full text-center"
          >
            {/* Heading */}
            <motion.h1
              variants={fadeInUp}
              className="text-4xl md:text-5xl font-medium tracking-tight text-white mb-6"
            >
              Get in Touch
            </motion.h1>

            <motion.p
              variants={fadeInUp}
              className="text-lg text-slate-400 mb-12 max-w-lg mx-auto"
            >
              Interested in piloting the platform or learning more? Reach out to either of us.
            </motion.p>

            {/* Contact Cards */}
            <motion.div
              variants={fadeInUp}
              className="grid grid-cols-1 sm:grid-cols-2 gap-6"
            >
              {contacts.map((contact) => (
                <a
                  key={contact.email}
                  href={`mailto:${contact.email}`}
                  className={cn(
                    "group block p-6 rounded-xl",
                    "bg-slate-900/50 backdrop-blur-sm border border-slate-800",
                    "hover:bg-slate-900/70 hover:border-slate-700",
                    "transition-all duration-300"
                  )}
                >
                  <div className="text-left">
                    <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">
                      {contact.role}
                    </p>
                    <h2 className="text-xl font-medium text-white mb-3">
                      {contact.name}
                    </h2>
                    <p className={cn(
                      "text-base text-slate-400 group-hover:text-sky-400",
                      "transition-colors duration-200 break-all"
                    )}>
                      {contact.email}
                    </p>
                  </div>
                </a>
              ))}
            </motion.div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}

export default ContactPage;
