import React from 'react'
import { NavLink } from 'react-router-dom'
import { Icon } from '../components/base/Icon'
import { Button } from '../components/base/Button'

export const Header: React.FC = () => {
  return (
    <header className="h-15 bg-white border-b border-gray-200 px-6 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center gap-6">
        {/* Logo */}
        <div className="text-xl font-bold text-gray-900">HealthSystems</div>

        {/* Tab Navigation */}
        <nav className="flex gap-1" role="navigation" aria-label="Main navigation">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `px-4 py-3 text-sm font-medium transition-colors relative ${
                isActive
                  ? 'text-primary-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`
            }
          >
            {({ isActive }) => (
              <>
                Systems Map
                {isActive && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary-600" />
                )}
              </>
            )}
          </NavLink>
          <NavLink
            to="/pathways"
            className={({ isActive }) =>
              `px-4 py-3 text-sm font-medium transition-colors relative ${
                isActive
                  ? 'text-primary-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`
            }
          >
            {({ isActive }) => (
              <>
                Pathway Explorer
                {isActive && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary-600" />
                )}
              </>
            )}
          </NavLink>
          <NavLink
            to="/library"
            className={({ isActive }) =>
              `px-4 py-3 text-sm font-medium transition-colors relative ${
                isActive
                  ? 'text-primary-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`
            }
          >
            {({ isActive }) => (
              <>
                Library
                {isActive && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary-600" />
                )}
              </>
            )}
          </NavLink>
        </nav>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-3">
        {/* Geography Selector */}
        <select className="px-3 py-1.5 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500">
          <option>Boston, MA</option>
          <option>Chicago, IL</option>
          <option>National</option>
        </select>

        {/* Settings Button */}
        <Button variant="icon" size="sm" ariaLabel="Settings">
          <Icon name="settings" size="md" />
        </Button>

        {/* Help Button */}
        <Button variant="icon" size="sm" ariaLabel="Help">
          <Icon name="help" size="md" />
        </Button>

        {/* User Menu */}
        <Button variant="icon" size="sm" ariaLabel="User menu">
          <Icon name="user" size="md" />
        </Button>
      </div>
    </header>
  )
}
