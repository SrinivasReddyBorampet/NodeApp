import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

// Mock the child components to isolate App component testing
jest.mock('./components/Header', () => () => <div data-testid="mock-header">Header</div>);
jest.mock('./components/Main', () => () => <div data-testid="mock-main">Main</div>);
jest.mock('./components/Footer', () => () => <div data-testid="mock-footer">Footer</div>);

describe('App Component', () => {
  test('renders without crashing', () => {
    render(<App />);
    expect(screen.getByTestId('mock-header')).toBeInTheDocument();
    expect(screen.getByTestId('mock-main')).toBeInTheDocument();
    expect(screen.getByTestId('mock-footer')).toBeInTheDocument();
  });

  test('renders with correct structure', () => {
    const { container } = render(<App />);
    const appDiv = container.querySelector('.App');
    expect(appDiv).toBeInTheDocument();
  });
});
