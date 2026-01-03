/**
 * Complete signup form with all auth options (Portable)
 * Configurable providers and redirect URLs
 */

'use client';

import { useState } from 'react';
import { OAuthButtons } from './OAuthButtons';
import { EmailAuthForm } from './EmailAuthForm';

export interface SignupFormProps {
  providers?: ('google' | 'apple' | 'facebook')[];
  onSuccess?: () => void;
  onError?: (error: string) => void;
  showDivider?: boolean;
}

export function SignupForm({
  providers = ['google', 'apple', 'facebook'],
  onSuccess = () => {},
  onError = () => {},
  showDivider = true,
}: SignupFormProps) {
  const [error, setError] = useState<string | null>(null);

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
    onError?.(errorMessage);
  };

  return (
    <div className="w-full max-w-md">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Create your account</h1>
        <p className="text-gray-600">Get started with your research today</p>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      <OAuthButtons
        providers={providers}
        mode="signup"
        onError={handleError}
      />

      {showDivider && (
        <div className="relative my-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white text-gray-500">Or sign up with email</span>
          </div>
        </div>
      )}

      <EmailAuthForm
        mode="signup"
        onSuccess={onSuccess}
        onError={handleError}
      />

      <div className="mt-4 text-center text-sm text-gray-600">
        By signing up, you agree to our
        {' '}
        <a href="/terms" className="text-blue-600 hover:text-blue-700">
          Terms of Service
        </a>
        {' '}
        and
        {' '}
        <a href="/privacy" className="text-blue-600 hover:text-blue-700">
          Privacy Policy
        </a>
      </div>

      <div className="mt-4 text-center">
        <a href="/login" className="text-sm text-blue-600 hover:text-blue-700">
          Already have an account? Sign in
        </a>
      </div>
    </div>
  );
}
