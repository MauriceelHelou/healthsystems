import React from 'react'
import { Header } from './Header'

interface DashboardLayoutProps {
  children: React.ReactNode
}

/**
 * Main dashboard layout with fixed header and minimalist styling
 */
export const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  return (
    <div className="flex flex-col h-screen bg-white">
      {/* Skip to main content link for accessibility */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-orange-600 focus:text-white focus:rounded"
      >
        Skip to main content
      </a>

      <Header />

      {/* Main landmark for accessibility - Add padding-top to account for fixed header (h-14 = 56px) */}
      <main
        id="main-content"
        className="flex flex-1 overflow-auto pt-14"
        role="main"
      >
        {children}
      </main>
    </div>
  )
}
