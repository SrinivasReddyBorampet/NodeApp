// This configuration extends the default CRA Jest configuration
module.exports = {
  // Use the default CRA preset
  preset: 'react-scripts',
  
  // Test environment setup
  testEnvironment: 'jsdom',
  
  // Coverage configuration
  collectCoverage: true,
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/**/*.{js,jsx}',
    '!src/index.js',
    '!**/node_modules/**',
  ],
  
  // JUnit reporter for Jenkins integration
  reporters: [
    'default',
    ['jest-junit', {
      outputDirectory: '.',
      outputName: 'junit.xml',
      classNameTemplate: '{classname}',
      titleTemplate: '{title}',
      ancestorSeparator: ' › ',
      usePathForSuiteName: true
    }]
  ]
};
