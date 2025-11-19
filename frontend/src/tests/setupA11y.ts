// Setup for accessibility tests
import { toHaveNoViolations } from 'jest-axe';

// Extend Jest matchers
expect.extend(toHaveNoViolations);

// Configure axe for consistent testing
import { configureAxe } from 'jest-axe';

export const axe = configureAxe({
  // Rules to run
  rules: {
    // Enable all WCAG 2.1 Level A and AA rules
    'region': { enabled: true },
    'bypass': { enabled: true },
    'color-contrast': { enabled: true },
    'document-title': { enabled: false }, // Not applicable in component tests
    'html-has-lang': { enabled: false }, // Not applicable in component tests
    'landmark-one-main': { enabled: true },
    'page-has-heading-one': { enabled: false }, // Not applicable in all components
    'scrollable-region-focusable': { enabled: true },
  },

  // Tags to include
  runOnly: {
    type: 'tag',
    values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'],
  },
});

// Increase timeout for axe tests (they can be slow)
jest.setTimeout(10000);
