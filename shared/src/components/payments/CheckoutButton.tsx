/**
 * Stripe Checkout button (Portable)
 * Configurable price and product
 */

'use client';

import { useState } from 'react';
import { formatPrice } from '../../lib/stripe';

export interface CheckoutButtonProps {
  query: string;
  amount?: number; // In pence (default: 299 for £2.99)
  currency?: string;
  onCheckoutStart?: () => void;
  onCheckoutSuccess?: (reportId: string) => void;
  onCheckoutError?: (error: string) => void;
  disabled?: boolean;
  className?: string;
}

export function CheckoutButton({
  query,
  amount = 299,
  currency: _currency = 'gbp',
  onCheckoutStart = () => {},
  onCheckoutSuccess = () => {},
  onCheckoutError = () => {},
  disabled = false,
  className = '',
}: CheckoutButtonProps) {
  const [isLoading, setIsLoading] = useState(false);

  const handleCheckout = async () => {
    setIsLoading(true);
    onCheckoutStart?.();

    try {
      // This will be implemented by the consuming app
      // Call backend API to create checkout session
      const response = await fetch('/api/reports/initiate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error('Failed to create checkout session');
      }

      const data = await response.json();

      // Redirect to success page or handle in-app
      onCheckoutSuccess?.(data.reportId);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Checkout failed';
      onCheckoutError?.(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      type="button"
      onClick={handleCheckout}
      disabled={disabled || isLoading || !query.trim()}
      className={`px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium ${className}`}
    >
      {isLoading ? 'Processing...' : `Generate Report (${formatPrice(amount)})`}
    </button>
  );
}
