import React from 'react';
import { render, screen } from '@testing-library/react';
import Footer from './Footer';

describe('Footer Component', () => {
  test('renders without crashing', () => {
    render(<Footer />);
    const currentYear = new Date().getFullYear();
    expect(screen.getByText(`© ${currentYear} Wipro. All rights reserved.`)).toBeInTheDocument();
  });

  test('has the correct class name', () => {
    const { container } = render(<Footer />);
    const footerElement = container.querySelector('.footer');
    expect(footerElement).toBeInTheDocument();
  });

  test('displays the current year', () => {
    render(<Footer />);
    const currentYear = new Date().getFullYear();
    expect(screen.getByText(new RegExp(`${currentYear}`))).toBeInTheDocument();
  });
});
