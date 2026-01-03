/**
 * Payment flow hook (Portable)
 * Handles checkout creation and redirect logic
 */

import { useState, useCallback } from 'react';
import { api } from '../lib/api-client';
import type { CreateCheckoutRequest, CreateCheckoutResponse } from '../types/payment';

export interface UsePaymentOptions {
  apiEndpoint?: string;
  onSuccess?: (reportId: string) => void;
  onError?: (error: string) => void;
}

export interface UsePaymentResult {
  isLoading: boolean;
  error: string | null;
  createCheckout: (query: string) => Promise<void>;
  clearError: () => void;
}

export function usePayment({
  apiEndpoint = '/reports/initiate',
  onSuccess,
  onError,
}: UsePaymentOptions = {}): UsePaymentResult {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createCheckout = useCallback(
    async (query: string) => {
      setIsLoading(true);
      setError(null);

      try {
        const request: CreateCheckoutRequest = { query };

        const response = await api.post<CreateCheckoutResponse>(
          apiEndpoint,
          request,
        );

        if (!response.success || !response.data) {
          throw new Error(response.error?.message || 'Failed to create checkout');
        }

        const { report_id: reportId } = response.data as { report_id: string };

        // Trigger success callback with report ID
        if (reportId) {
          onSuccess?.(reportId);
        }
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Payment failed';
        setError(errorMessage);
        onError?.(errorMessage);
      } finally {
        setIsLoading(false);
      }
    },
    [apiEndpoint, onSuccess, onError],
  );

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    isLoading,
    error,
    createCheckout,
    clearError,
  };
}
