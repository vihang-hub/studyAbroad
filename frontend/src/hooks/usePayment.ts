/**
 * Payment hook for frontend
 * Handles Stripe checkout integration with feature flag support
 */

'use client';

import { useState } from 'react';
import { useFeature } from '@/providers/feature-flag-provider';
import { Feature } from '@study-abroad/shared-feature-flags';
import { useAuthenticatedApi } from './useAuthenticatedApi';
import { logInfo, logError } from '@/lib/logger';

interface UsePaymentOptions {
  apiEndpoint: string;
  onSuccess?: (reportId: string) => void;
  onError?: (error: string) => void;
}

interface UsePaymentReturn {
  isLoading: boolean;
  error: string | null;
  createCheckout: (query: string) => Promise<void>;
}

/**
 * Hook for handling payment flow
 * Automatically bypasses payment in dev/test mode based on feature flags
 */
export function usePayment(options: UsePaymentOptions): UsePaymentReturn {
  const { apiEndpoint, onSuccess, onError } = options;
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const paymentsEnabled = useFeature(Feature.PAYMENTS);
  const { post: authPost } = useAuthenticatedApi();

  const createCheckout = async (query: string) => {
    setIsLoading(true);
    setError(null);

    try {
      if (!paymentsEnabled) {
        // In dev/test mode, bypass payment and create report directly
        logInfo('Payment bypassed in dev/test mode', { query });

        interface CreateReportResponse {
          reportId?: string;
          id?: string;
        }

        const response = await authPost<CreateReportResponse>(apiEndpoint, { query });

        if (response.error) {
          throw new Error(response.error.message);
        }

        const reportId = response.data?.reportId || response.data?.id;
        if (reportId) {
          onSuccess?.(reportId);
        } else {
          throw new Error('No report ID returned');
        }
      } else {
        // Production mode: create Stripe checkout
        logInfo('Creating Stripe checkout', { query });

        interface CheckoutResponse {
          checkoutUrl?: string;
        }

        const response = await authPost<CheckoutResponse>(apiEndpoint, { query });

        if (response.error) {
          throw new Error(response.error.message);
        }

        const checkoutUrl = response.data?.checkoutUrl;
        if (checkoutUrl) {
          // Redirect to Stripe checkout
          window.location.href = checkoutUrl;
        } else {
          throw new Error('No checkout URL returned');
        }
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Payment failed';
      setError(errorMessage);
      logError('Payment error', err);
      onError?.(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    isLoading,
    error,
    createCheckout,
  };
}
