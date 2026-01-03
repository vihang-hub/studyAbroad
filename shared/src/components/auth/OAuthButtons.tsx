/**
 * OAuth authentication buttons (Portable)
 * Supports Google, Apple, Facebook providers
 */

'use client';

import { useSignIn } from '@clerk/clerk-react';

export interface OAuthButtonsProps {
  providers?: ('google' | 'apple' | 'facebook')[];
  mode?: 'signin' | 'signup';
  onError?: (error: string) => void;
}

const providerLabels = {
  google: 'Continue with Google',
  apple: 'Continue with Apple',
  facebook: 'Continue with Facebook',
};

export function OAuthButtons({
  providers = ['google', 'apple', 'facebook'],
  mode: _mode = 'signin',
  onError = () => {},
}: OAuthButtonsProps) {
  const { signIn } = useSignIn();

  const handleOAuthSignIn = async (provider: 'google' | 'apple' | 'facebook') => {
    if (!signIn) {
      onError?.('Sign in not initialized');
      return;
    }

    try {
      await signIn.authenticateWithRedirect({
        strategy: `oauth_${provider}`,
        redirectUrl: '/sso-callback',
        redirectUrlComplete: '/chat',
      });
    } catch (error) {
      const message = error instanceof Error ? error.message : 'OAuth sign in failed';
      onError?.(message);
    }
  };

  return (
    <div className="flex flex-col gap-3">
      {providers.map((provider) => (
        <button
          key={provider}
          type="button"
          onClick={() => handleOAuthSignIn(provider)}
          className="w-full flex items-center justify-center gap-3 px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
        >
          {/* Provider icon would go here */}
          <span className="text-sm font-medium text-gray-700">
            {providerLabels[provider]}
          </span>
        </button>
      ))}
    </div>
  );
}
