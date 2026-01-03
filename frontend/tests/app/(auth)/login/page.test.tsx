/**
 * Tests for login page
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';

// Mock Clerk's SignIn component - capture all props for verification
let capturedSignInProps: Record<string, unknown> = {};

vi.mock('@clerk/nextjs', () => ({
  SignIn: (props: {
    path: string;
    signUpUrl: string;
    afterSignInUrl: string;
    routing: string;
    appearance: { elements: { rootBox: string; card: string } };
  }) => {
    capturedSignInProps = props;
    return (
      <div data-testid="clerk-sign-in">
        <span data-testid="sign-in-path">{props.path}</span>
        <span data-testid="sign-up-url">{props.signUpUrl}</span>
        <span data-testid="after-sign-in-url">{props.afterSignInUrl}</span>
        <span data-testid="routing">{props.routing}</span>
      </div>
    );
  },
}));

describe('LoginPage', () => {
  beforeEach(() => {
    vi.resetModules();
    capturedSignInProps = {};
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
      expect(capturedSignInProps.path).toBe('/login');
    });

    it('should configure SignIn with signup URL', async () => {
      const LoginPage = (await import('../../../../src/app/(auth)/login/[[...rest]]/page')).default;
      render(<LoginPage />);

      expect(screen.getByTestId('sign-up-url')).toHaveTextContent('/signup');
      expect(capturedSignInProps.signUpUrl).toBe('/signup');
    });

    it('should configure SignIn with redirect URL after sign in', async () => {
      const LoginPage = (await import('../../../../src/app/(auth)/login/[[...rest]]/page')).default;
      render(<LoginPage />);

      expect(screen.getByTestId('after-sign-in-url')).toHaveTextContent('/chat');
      expect(capturedSignInProps.afterSignInUrl).toBe('/chat');
    });

    it('should configure SignIn with path routing', async () => {
      const LoginPage = (await import('../../../../src/app/(auth)/login/[[...rest]]/page')).default;
      render(<LoginPage />);

      expect(screen.getByTestId('routing')).toHaveTextContent('path');
      expect(capturedSignInProps.routing).toBe('path');
    });
  });

  describe('appearance configuration', () => {
    it('should configure appearance with rootBox class', async () => {
      const LoginPage = (await import('../../../../src/app/(auth)/login/[[...rest]]/page')).default;
      render(<LoginPage />);

      expect(capturedSignInProps.appearance).toBeDefined();
      const appearance = capturedSignInProps.appearance as { elements: { rootBox: string } };
      expect(appearance.elements.rootBox).toBe('mx-auto');
    });

    it('should configure appearance with card class', async () => {
      const LoginPage = (await import('../../../../src/app/(auth)/login/[[...rest]]/page')).default;
      render(<LoginPage />);

      const appearance = capturedSignInProps.appearance as { elements: { card: string } };
      expect(appearance.elements.card).toBe('shadow-lg');
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

    it('should have correct full styling', async () => {
      const LoginPage = (await import('../../../../src/app/(auth)/login/[[...rest]]/page')).default;
      const { container } = render(<LoginPage />);

      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.className).toContain('flex');
      expect(wrapper.className).toContain('min-h-screen');
      expect(wrapper.className).toContain('bg-gray-50');
    });
  });
});
