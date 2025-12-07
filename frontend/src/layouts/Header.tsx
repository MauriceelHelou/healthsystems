import { FC } from 'react'
import { NavLink } from 'react-router-dom'
// import { Icon } from '../components/base/Icon'

/**
 * Minimalist fixed header with white background and orange accents
 */
export const Header: FC = () => {
  return (
    <header className="h-14 bg-white border-b border-gray-200 px-6 flex items-center justify-between fixed top-0 left-0 right-0 z-30 shadow-sm">
      <div className="flex items-center gap-8">
        {/* Logo - Compact, clickable to go home */}
        <NavLink
          to="/"
          className="text-lg font-semibold text-gray-900 tracking-tight hover:text-primary-600 transition-colors"
        >
          HealthSystems
        </NavLink>

        {/* Tab Navigation - Minimal */}
        <nav className="flex gap-1" role="navigation" aria-label="Main navigation">
          <NavLink
            to="/systems"
            className={({ isActive }) =>
              `px-3 py-2 text-xs font-medium transition-all relative ${
                isActive
                  ? 'text-orange-700'
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
            to="/systems/alcoholism"
            className={({ isActive }) =>
              `px-3 py-2 text-xs font-medium transition-all relative ${
                isActive
                  ? 'text-orange-700'
                  : 'text-gray-500 hover:text-gray-900'
              }`
            }
          >
            {({ isActive }) => (
              <>
                Alcoholism System
                {isActive && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-orange-500" />
                )}
              </>
            )}
          </NavLink>
          <NavLink
            to="/important-nodes"
            className={({ isActive }) =>
              `px-3 py-2 text-xs font-medium transition-all relative ${
                isActive
                  ? 'text-orange-700'
                  : 'text-gray-500 hover:text-gray-900'
              }`
            }
          >
            {({ isActive }) => (
              <>
                Important Nodes
                {isActive && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-orange-500" />
                )}
              </>
            )}
          </NavLink>
          {/* Pathfinder - temporarily disabled
          <NavLink
            to="/pathfinder"
            className={({ isActive }) =>
              `px-3 py-2 text-xs font-medium transition-all relative ${
                isActive
                  ? 'text-orange-700'
                  : 'text-gray-500 hover:text-gray-900'
              }`
            }
          >
            {({ isActive }) => (
              <>
                Pathfinder
                {isActive && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-orange-500" />
                )}
              </>
            )}
          </NavLink>
          */}
          {/* Pathway Explorer - temporarily disabled
          <NavLink
            to="/pathways"
            className={({ isActive }) =>
              `px-3 py-2 text-xs font-medium transition-all relative ${
                isActive
                  ? 'text-orange-700'
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
          */}
          <NavLink
            to="/crisis-explorer"
            className={({ isActive }) =>
              `px-3 py-2 text-xs font-medium transition-all relative ${
                isActive
                  ? 'text-orange-700'
                  : 'text-gray-500 hover:text-gray-900'
              }`
            }
          >
            {({ isActive }) => (
              <>
                Crisis Explorer
                {isActive && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-orange-500" />
                )}
              </>
            )}
          </NavLink>
          {/* Library - temporarily disabled
          <NavLink
            to="/library"
            className={({ isActive }) =>
              `px-3 py-2 text-xs font-medium transition-all relative ${
                isActive
                  ? 'text-orange-700'
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
          */}
        </nav>
      </div>

      {/* Right Section - temporarily removed
      <div className="flex items-center gap-2">
        <button
          className="p-2 text-gray-400 hover:text-orange-700 transition-colors"
          aria-label="Settings"
        >
          <Icon name="settings" size="sm" />
        </button>
        <button
          className="p-2 text-gray-400 hover:text-orange-700 transition-colors"
          aria-label="Help"
        >
          <Icon name="help" size="sm" />
        </button>
      </div>
      */}
    </header>
  )
}
