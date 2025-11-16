import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../App';

describe('App', () => {
  test('renders application title', () => {
    render(<App />);
    const titleElement = screen.getByText(/HealthSystems Platform/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders platform features', () => {
    render(<App />);
    expect(screen.getByText(/Self-configuring geographic analysis/i)).toBeInTheDocument();
    expect(screen.getByText(/Bayesian mechanism weighting/i)).toBeInTheDocument();
    expect(screen.getByText(/Interactive systems visualizations/i)).toBeInTheDocument();
  });

  test('has accessible main content landmark', () => {
    render(<App />);
    const main = screen.getByRole('main');
    expect(main).toBeInTheDocument();
    expect(main).toHaveAttribute('id', 'main-content');
  });
});
