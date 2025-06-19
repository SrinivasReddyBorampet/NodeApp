import React from 'react';
import { render, screen } from '@testing-library/react';
import Header from './Header';

describe('Header Component', () => {
  test('renders without crashing', () => {
    render(<Header />);
    expect(screen.getByText('Wipro')).toBeInTheDocument();
  });

  test('has the correct class name', () => {
    const { container } = render(<Header />);
    const headerElement = container.querySelector('.header');
    expect(headerElement).toBeInTheDocument();
  });

  test('contains logo element', () => {
    const { container } = render(<Header />);
    const logoElement = container.querySelector('.header-logo');
    expect(logoElement).toBeInTheDocument();
    expect(logoElement.textContent).toBe('Wipro');
  });
});
