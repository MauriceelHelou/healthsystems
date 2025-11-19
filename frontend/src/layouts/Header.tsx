import { FC } from 'react'
import { NavLink } from 'react-router-dom'
import { Icon } from '../components/base/Icon'

/**
 * Minimalist fixed header with white background and orange accents
 */
export const Header: FC = () => {
  return (
    <header className="h-14 bg-white border-b border-gray-200 px-6 flex items-center justify-between fixed top-0 left-0 right-0 z-30 shadow-sm">
      <div className="flex items-center gap-8">
        {/* Logo - Compact */}
        <div className="text-lg font-semibold text-gray-900 tracking-tight">
          HealthSystems
        </div>

        {/* Tab Navigation - Minimal */}
        <nav className="flex gap-1" role="navigation" aria-label="Main navigation">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `px-3 py-2 text-xs font-medium transition-all relative ${
                isActive
                  ? 'text-orange-600'
                  : 'text-gray-500 hover:text-gray-900'
              }`
            }
          >
            {({ isActive }) => (
              <>
                Systems Map
                {isActive && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-orange-500" />
                )}
              </>
            )}
          </NavLink>
          <NavLink
            to="/pathways"
            className={({ isActive }) =>
              `px-3 py-2 text-xs font-medium transition-all relative ${
                isActive
                  ? 'text-orange-600'
                  : 'text-gray-500 hover:text-gray-900'
              }`
            }
          >
            {({ isActive }) => (
              <>
                Pathway Explorer
                {isActive && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-orange-500" />
                )}
              </>
            )}
          </NavLink>
          <NavLink
            to="/library"
            className={({ isActive }) =>
              `px-3 py-2 text-xs font-medium transition-all relative ${
                isActive
                  ? 'text-orange-600'
                  : 'text-gray-500 hover:text-gray-900'
              }`
            }
          >
            {({ isActive }) => (
              <>
                Library
                {isActive && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-orange-500" />
                )}
              </>
            )}
          </NavLink>
        </nav>
      </div>

      {/* Right Section - Minimal buttons only */}
      <div className="flex items-center gap-2">
        {/* Settings Button */}
        <button
          className="p-2 text-gray-400 hover:text-orange-600 transition-colors"
          aria-label="Settings"
        >
          <Icon name="settings" size="sm" />
        </button>

        {/* Help Button */}
        <button
          className="p-2 text-gray-400 hover:text-orange-600 transition-colors"
          aria-label="Help"
        >
          <Icon name="help" size="sm" />
        </button>
      </div>
    </header>
  )
}
