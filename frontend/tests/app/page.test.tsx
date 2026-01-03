/**
 * Tests for landing page
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';
import Home from '../../src/app/page';

// Mock next/link
vi.mock('next/link', () => ({
  default: ({ children, href, ...props }: { children: React.ReactNode; href: string }) => (
    <a href={href} {...props}>{children}</a>
  ),
}));

describe('Home Page', () => {
  describe('rendering', () => {
    it('should render the main heading', () => {
      render(<Home />);

      expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('UK Study & Migration Research');
    });

    it('should render the description', () => {
      render(<Home />);

      expect(screen.getByText(/AI-powered research reports/)).toBeInTheDocument();
    });

    it('should render Login link', () => {
      render(<Home />);

      const loginLink = screen.getByRole('link', { name: /login/i });
      expect(loginLink).toBeInTheDocument();
      expect(loginLink).toHaveAttribute('href', '/login');
    });

    it('should render Sign Up link', () => {
      render(<Home />);

      const signupLink = screen.getByRole('link', { name: /sign up/i });
      expect(signupLink).toBeInTheDocument();
      expect(signupLink).toHaveAttribute('href', '/signup');
    });
  });

  describe('styling', () => {
    it('should have main element with centered layout', () => {
      render(<Home />);

      const main = screen.getByRole('main');
      expect(main).toHaveClass('flex', 'min-h-screen', 'items-center', 'justify-center');
    });

    it('should have heading with bold styling', () => {
      render(<Home />);

      const heading = screen.getByRole('heading', { level: 1 });
      expect(heading).toHaveClass('font-bold');
    });
  });

  describe('accessibility', () => {
    it('should have semantic main element', () => {
      render(<Home />);

      expect(screen.getByRole('main')).toBeInTheDocument();
    });

    it('should have accessible links', () => {
      render(<Home />);

      const links = screen.getAllByRole('link');
      expect(links).toHaveLength(2);
      links.forEach(link => {
        expect(link).toHaveAccessibleName();
      });
    });
  });
});
