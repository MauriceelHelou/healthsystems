module.exports = {
  ...require('./jest.config.js'),

  // Display name for this config
  displayName: 'accessibility',

  // Only run accessibility tests
  testMatch: [
    '<rootDir>/src/**/*.a11y.{spec,test}.{js,jsx,ts,tsx}',
    '<rootDir>/src/tests/a11y/**/*.{spec,test}.{js,jsx,ts,tsx}',
  ],

  // Setup specific to a11y tests
  setupFilesAfterEnv: [
    '<rootDir>/src/setupTests.ts',
    '<rootDir>/src/tests/setupA11y.ts',
  ],

  // Accessibility-specific coverage (may be lower initially)
  coverageThresholds: {
    global: {
      branches: 60,
      functions: 60,
      lines: 70,
      statements: 70,
    },
  },

  // Longer timeout for axe tests (they can be slow)
  testTimeout: 10000,
};
