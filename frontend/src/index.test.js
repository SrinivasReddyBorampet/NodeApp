import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Mock modules before requiring the index file
jest.mock('react-dom/client', () => {
  const mockRoot = {
    render: jest.fn()
  };
  return {
    createRoot: jest.fn(() => mockRoot)
  };
});

jest.mock('./App', () => () => 'App Component');

describe('Index', () => {
  test('renders without crashing', () => {
    // Setup
    const root = document.createElement('div');
    root.id = 'root';
    document.body.appendChild(root);
    
    // Mock getElementById
    const originalGetElementById = document.getElementById;
    document.getElementById = jest.fn(() => root);
    
    // Import the index.js file which will execute its code
    require('./index.js');
    
    // Assertions
    expect(document.getElementById).toHaveBeenCalledWith('root');
    expect(ReactDOM.createRoot).toHaveBeenCalledWith(root);
    
    // Cleanup
    document.body.removeChild(root);
    document.getElementById = originalGetElementById;
  });
});
