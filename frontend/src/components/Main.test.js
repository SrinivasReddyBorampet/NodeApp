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
    expect(headingElement.textContent).toBe('Developer Portal wipro');
  });

  test('heading and paragraph have correct text content', () => {
    render(<Main />);
    expect(screen.getByText('Developer Portal wipro')).toBeInTheDocument();
    expect(screen.getByText('Welcome to the Developer Portal')).toBeInTheDocument();
  });

  test('paragraph has correct styling', () => {
    render(<Main />);
    const paragraph = screen.getByText('Welcome to the Developer Portal');
    expect(paragraph).toHaveStyle('font-size: 19px');
  });
});
