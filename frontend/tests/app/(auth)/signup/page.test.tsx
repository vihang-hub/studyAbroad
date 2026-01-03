/**
 * Tests for signup page
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';

// Mock Clerk's SignUp component
vi.mock('@clerk/nextjs', () => ({
  SignUp: ({ path, signInUrl, afterSignUpUrl, appearance }: {
    path: string;
    signInUrl: string;
    afterSignUpUrl: string;
    appearance: object;
  }) => (
    <div data-testid="clerk-sign-up">
      <span data-testid="sign-up-path">{path}</span>
      <span data-testid="sign-in-url">{signInUrl}</span>
      <span data-testid="after-sign-up-url">{afterSignUpUrl}</span>
    </div>
  ),
}));

describe('SignupPage', () => {
  beforeEach(() => {
    vi.resetModules();
  });

  describe('rendering', () => {
    it('should render SignUp component', async () => {
      const SignupPage = (await import('../../../../src/app/(auth)/signup/[[...rest]]/page')).default;
      render(<SignupPage />);

      expect(screen.getByTestId('clerk-sign-up')).toBeInTheDocument();
    });

    it('should configure SignUp with correct path', async () => {
      const SignupPage = (await import('../../../../src/app/(auth)/signup/[[...rest]]/page')).default;
      render(<SignupPage />);

      expect(screen.getByTestId('sign-up-path')).toHaveTextContent('/signup');
    });

    it('should configure SignUp with signin URL', async () => {
      const SignupPage = (await import('../../../../src/app/(auth)/signup/[[...rest]]/page')).default;
      render(<SignupPage />);

      expect(screen.getByTestId('sign-in-url')).toHaveTextContent('/login');
    });

    it('should configure SignUp with redirect URL after sign up', async () => {
      const SignupPage = (await import('../../../../src/app/(auth)/signup/[[...rest]]/page')).default;
      render(<SignupPage />);

      expect(screen.getByTestId('after-sign-up-url')).toHaveTextContent('/chat');
    });
  });

  describe('styling', () => {
    it('should have centered layout', async () => {
      const SignupPage = (await import('../../../../src/app/(auth)/signup/[[...rest]]/page')).default;
      const { container } = render(<SignupPage />);

      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('flex', 'min-h-screen', 'items-center', 'justify-center');
    });

    it('should have gray background', async () => {
      const SignupPage = (await import('../../../../src/app/(auth)/signup/[[...rest]]/page')).default;
      const { container } = render(<SignupPage />);

      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('bg-gray-50');
    });
  });
});
