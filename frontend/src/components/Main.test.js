import React from 'react';
import { render, screen } from '@testing-library/react';
import Main from './Main';

describe('Main Component', () => {
  test('renders without crashing', () => {
    render(<Main />);
    expect(screen.getByText('Welcome to the Developer Portal')).toBeInTheDocument();
  });

  test('has the correct class name', () => {
    const { container } = render(<Main />);
    const mainElement = container.querySelector('.main');
    expect(mainElement).toBeInTheDocument();
  });

  test('contains heading element', () => {
    render(<Main />);
    const headingElement = screen.getByRole('heading', { level: 1 });
    expect(headingElement).toBeInTheDocument();
    expect(headingElement.textContent).toBe('Developer Portal');
  });
});
