/**
 * Tests for auth layout
 */

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';
import AuthLayout from '../../../src/app/(auth)/layout';

describe('AuthLayout', () => {
  describe('rendering', () => {
    it('should render children', () => {
      render(
        <AuthLayout>
          <div data-testid="child">Child content</div>
        </AuthLayout>
      );

      expect(screen.getByTestId('child')).toBeInTheDocument();
      expect(screen.getByText('Child content')).toBeInTheDocument();
    });

    it('should wrap children in styled container', () => {
      render(
        <AuthLayout>
          <div data-testid="child">Test</div>
        </AuthLayout>
      );

      const child = screen.getByTestId('child');
      const container = child.parentElement;
      expect(container).toHaveClass('bg-white', 'rounded-2xl', 'shadow-xl');
    });
  });

  describe('styling', () => {
    it('should have gradient background', () => {
      const { container } = render(
        <AuthLayout>
          <div>Test</div>
        </AuthLayout>
      );

      const outerDiv = container.firstChild;
      expect(outerDiv).toHaveClass('bg-gradient-to-br', 'from-blue-50', 'to-indigo-100');
    });

    it('should center content vertically and horizontally', () => {
      const { container } = render(
        <AuthLayout>
          <div>Test</div>
        </AuthLayout>
      );

      const outerDiv = container.firstChild;
      expect(outerDiv).toHaveClass('flex', 'items-center', 'justify-center');
    });

    it('should have full screen height', () => {
      const { container } = render(
        <AuthLayout>
          <div>Test</div>
        </AuthLayout>
      );

      const outerDiv = container.firstChild;
      expect(outerDiv).toHaveClass('min-h-screen');
    });

    it('should have max-width constraint on card', () => {
      render(
        <AuthLayout>
          <div data-testid="child">Test</div>
        </AuthLayout>
      );

      const card = screen.getByTestId('child').parentElement;
      expect(card).toHaveClass('max-w-md', 'w-full');
    });

    it('should have padding on card', () => {
      render(
        <AuthLayout>
          <div data-testid="child">Test</div>
        </AuthLayout>
      );

      const card = screen.getByTestId('child').parentElement;
      expect(card).toHaveClass('p-8');
    });
  });

  describe('with different children', () => {
    it('should render form elements', () => {
      render(
        <AuthLayout>
          <form data-testid="auth-form">
            <input type="email" placeholder="Email" />
            <button type="submit">Submit</button>
          </form>
        </AuthLayout>
      );

      expect(screen.getByTestId('auth-form')).toBeInTheDocument();
      expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument();
    });

    it('should render complex nested content', () => {
      render(
        <AuthLayout>
          <div>
            <h1>Welcome</h1>
            <p>Please sign in</p>
            <div>
              <span>Nested content</span>
            </div>
          </div>
        </AuthLayout>
      );

      expect(screen.getByText('Welcome')).toBeInTheDocument();
      expect(screen.getByText('Please sign in')).toBeInTheDocument();
      expect(screen.getByText('Nested content')).toBeInTheDocument();
    });
  });
});
