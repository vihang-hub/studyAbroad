/**
 * Portable Stripe client initialization
 * Configurable via environment variables for different projects
 */

import { loadStripe, Stripe } from '@stripe/stripe-js';

export interface StripeConfig {
  publishableKey: string;
  priceAmount: number; // In pence (e.g., 299 for £2.99)
  currency: string;
}

let stripePromise: Promise<Stripe | null> | null = null;

/**
 * Get Stripe configuration from environment variables
 */
export function getStripeConfig(): StripeConfig {
  const publishableKey = process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
    || process.env.STRIPE_PUBLISHABLE_KEY
    || '';

  if (!publishableKey) {
    throw new Error('Stripe publishable key is required. Set NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY or STRIPE_PUBLISHABLE_KEY');
  }

  return {
    publishableKey,
    priceAmount: 299, // £2.99 per query
    currency: 'gbp',
  };
}

/**
 * Get Stripe client instance (singleton)
 */
export function getStripe(): Promise<Stripe | null> {
  if (!stripePromise) {
    const config = getStripeConfig();
    stripePromise = loadStripe(config.publishableKey);
  }
  return stripePromise;
}

/**
 * Format price for display
 * @param amountInPence - Amount in pence (e.g., 299)
 * @returns Formatted string (e.g., "£2.99")
 */
export function formatPrice(amountInPence: number): string {
  const pounds = amountInPence / 100;
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP',
  }).format(pounds);
}
