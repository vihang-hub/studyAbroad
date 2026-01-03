/**
 * Tests for signup page
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';

// Mock Clerk's SignUp component - capture all props for verification
let capturedSignUpProps: Record<string, unknown> = {};

vi.mock('@clerk/nextjs', () => ({
  SignUp: (props: {
    path: string;
    signInUrl: string;
    afterSignUpUrl: string;
    routing: string;
    appearance: { elements: { rootBox: string; card: string } };
  }) => {
    capturedSignUpProps = props;
    return (
      <div data-testid="clerk-sign-up">
        <span data-testid="sign-up-path">{props.path}</span>
        <span data-testid="sign-in-url">{props.signInUrl}</span>
        <span data-testid="after-sign-up-url">{props.afterSignUpUrl}</span>
        <span data-testid="routing">{props.routing}</span>
      </div>
    );
  },
}));

describe('SignupPage', () => {
  beforeEach(() => {
    vi.resetModules();
    capturedSignUpProps = {};
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
      expect(capturedSignUpProps.path).toBe('/signup');
    });

    it('should configure SignUp with signin URL', async () => {
      const SignupPage = (await import('../../../../src/app/(auth)/signup/[[...rest]]/page')).default;
      render(<SignupPage />);

      expect(screen.getByTestId('sign-in-url')).toHaveTextContent('/login');
      expect(capturedSignUpProps.signInUrl).toBe('/login');
    });

    it('should configure SignUp with redirect URL after sign up', async () => {
      const SignupPage = (await import('../../../../src/app/(auth)/signup/[[...rest]]/page')).default;
      render(<SignupPage />);

      expect(screen.getByTestId('after-sign-up-url')).toHaveTextContent('/chat');
      expect(capturedSignUpProps.afterSignUpUrl).toBe('/chat');
    });

    it('should configure SignUp with path routing', async () => {
      const SignupPage = (await import('../../../../src/app/(auth)/signup/[[...rest]]/page')).default;
      render(<SignupPage />);

      expect(screen.getByTestId('routing')).toHaveTextContent('path');
      expect(capturedSignUpProps.routing).toBe('path');
    });
  });

  describe('appearance configuration', () => {
    it('should configure appearance with rootBox class', async () => {
      const SignupPage = (await import('../../../../src/app/(auth)/signup/[[...rest]]/page')).default;
      render(<SignupPage />);

      expect(capturedSignUpProps.appearance).toBeDefined();
      const appearance = capturedSignUpProps.appearance as { elements: { rootBox: string } };
      expect(appearance.elements.rootBox).toBe('mx-auto');
    });

    it('should configure appearance with card class', async () => {
      const SignupPage = (await import('../../../../src/app/(auth)/signup/[[...rest]]/page')).default;
      render(<SignupPage />);

      const appearance = capturedSignUpProps.appearance as { elements: { card: string } };
      expect(appearance.elements.card).toBe('shadow-lg');
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

    it('should have correct full styling', async () => {
      const SignupPage = (await import('../../../../src/app/(auth)/signup/[[...rest]]/page')).default;
      const { container } = render(<SignupPage />);

      const wrapper = container.firstChild as HTMLElement;
      expect(wrapper.className).toContain('flex');
      expect(wrapper.className).toContain('min-h-screen');
      expect(wrapper.className).toContain('bg-gray-50');
    });
  });
});
