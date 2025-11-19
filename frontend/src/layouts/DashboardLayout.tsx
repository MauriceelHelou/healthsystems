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
      <Header />

      {/* Add padding-top to account for fixed header (h-14 = 56px) */}
      <div className="flex flex-1 overflow-hidden pt-14">
        {children}
      </div>
    </div>
  )
}
