/**
 * Polyfills for Jest test environment
 * This file runs BEFORE the test framework is installed
 */

const { TextEncoder, TextDecoder } = require('util');

// Polyfill TextEncoder/TextDecoder for MSW and other dependencies
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;
