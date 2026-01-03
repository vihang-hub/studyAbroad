/**
 * Tests for LoginForm component
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { LoginForm } from '../../src/components/auth/LoginForm';

// Mock child components
vi.mock('../../src/components/auth/OAuthButtons', () => ({
  OAuthButtons: ({ mode, onError }: any) => (
    <div data-testid="oauth-buttons" data-mode={mode}>
      OAuth Buttons Mock
    </div>
  ),
}));

vi.mock('../../src/components/auth/EmailAuthForm', () => ({
  EmailAuthForm: ({ mode, onSuccess, onError }: any) => (
    <div data-testid="email-auth-form" data-mode={mode}>
      Email Auth Form Mock
    </div>
  ),
}));

describe('LoginForm', () => {
  it('should render with default props', () => {
    render(<LoginForm />);

    expect(screen.getByText('Welcome back')).toBeInTheDocument();
    expect(screen.getByText('Sign in to your account to continue')).toBeInTheDocument();
    expect(screen.getByTestId('oauth-buttons')).toBeInTheDocument();
    expect(screen.getByTestId('email-auth-form')).toBeInTheDocument();
  });

  it('should render OAuth buttons with signin mode', () => {
    render(<LoginForm />);

    const oauthButtons = screen.getByTestId('oauth-buttons');
    expect(oauthButtons).toHaveAttribute('data-mode', 'signin');
  });

  it('should render email auth form with signin mode', () => {
    render(<LoginForm />);

    const emailForm = screen.getByTestId('email-auth-form');
    expect(emailForm).toHaveAttribute('data-mode', 'signin');
  });

  it('should show divider by default', () => {
    render(<LoginForm />);

    expect(screen.getByText('Or continue with email')).toBeInTheDocument();
  });

  it('should hide divider when showDivider is false', () => {
    render(<LoginForm showDivider={false} />);

    expect(screen.queryByText('Or continue with email')).not.toBeInTheDocument();
  });

  it('should render link to signup page', () => {
    render(<LoginForm />);

    const signupLink = screen.getByText("Don't have an account? Sign up");
    expect(signupLink).toBeInTheDocument();
    expect(signupLink.closest('a')).toHaveAttribute('href', '/signup');
  });

  it('should not display error initially', () => {
    render(<LoginForm />);

    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
  });

  it('should call onSuccess callback', () => {
    const mockOnSuccess = vi.fn();
    render(<LoginForm onSuccess={mockOnSuccess} />);

    // Callback is passed to child components
    const emailForm = screen.getByTestId('email-auth-form');
    expect(emailForm).toBeInTheDocument();
  });

  it('should call onError callback', () => {
    const mockOnError = vi.fn();
    render(<LoginForm onError={mockOnError} />);

    // Callback is passed to child components
    const oauthButtons = screen.getByTestId('oauth-buttons');
    expect(oauthButtons).toBeInTheDocument();
  });

  it('should render with custom providers', () => {
    render(<LoginForm providers={['google']} />);

    // Providers prop is passed to OAuth buttons
    expect(screen.getByTestId('oauth-buttons')).toBeInTheDocument();
  });
});
