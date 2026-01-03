/**
 * Tests for login page
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';

// Mock Clerk's SignIn component
vi.mock('@clerk/nextjs', () => ({
  SignIn: ({ path, signUpUrl, afterSignInUrl, appearance }: {
    path: string;
    signUpUrl: string;
    afterSignInUrl: string;
    appearance: object;
  }) => (
    <div data-testid="clerk-sign-in">
      <span data-testid="sign-in-path">{path}</span>
      <span data-testid="sign-up-url">{signUpUrl}</span>
      <span data-testid="after-sign-in-url">{afterSignInUrl}</span>
    </div>
  ),
}));

describe('LoginPage', () => {
  beforeEach(() => {
    vi.resetModules();
  });

  describe('rendering', () => {
    it('should render SignIn component', async () => {
      const LoginPage = (await import('../../../../src/app/(auth)/login/[[...rest]]/page')).default;
      render(<LoginPage />);

      expect(screen.getByTestId('clerk-sign-in')).toBeInTheDocument();
    });

    it('should configure SignIn with correct path', async () => {
      const LoginPage = (await import('../../../../src/app/(auth)/login/[[...rest]]/page')).default;
      render(<LoginPage />);

      expect(screen.getByTestId('sign-in-path')).toHaveTextContent('/login');
    });

    it('should configure SignIn with signup URL', async () => {
      const LoginPage = (await import('../../../../src/app/(auth)/login/[[...rest]]/page')).default;
      render(<LoginPage />);

      expect(screen.getByTestId('sign-up-url')).toHaveTextContent('/signup');
    });

    it('should configure SignIn with redirect URL after sign in', async () => {
      const LoginPage = (await import('../../../../src/app/(auth)/login/[[...rest]]/page')).default;
      render(<LoginPage />);

      expect(screen.getByTestId('after-sign-in-url')).toHaveTextContent('/chat');
    });
  });

  describe('styling', () => {
    it('should have centered layout', async () => {
      const LoginPage = (await import('../../../../src/app/(auth)/login/[[...rest]]/page')).default;
      const { container } = render(<LoginPage />);

      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('flex', 'min-h-screen', 'items-center', 'justify-center');
    });

    it('should have gray background', async () => {
      const LoginPage = (await import('../../../../src/app/(auth)/login/[[...rest]]/page')).default;
      const { container } = render(<LoginPage />);

      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('bg-gray-50');
    });
  });
});
