/**
 * Payment-related TypeScript interfaces
 * For Stripe integration (£2.99 per query)
 */
// @ts-nocheck


export type PaymentStatus = 'pending' | 'succeeded' | 'failed' | 'refunded';
export interface Payment {
  id: string;
  userId: string;
  reportId: string;
  stripePaymentIntentId: string;
  amount: number; // In pence (e.g., 299 for £2.99)
  currency: string; // 'gbp'
  status: PaymentStatus;
  errorMessage?: string | null;
  refundedAt?: Date | null;
  createdAt: Date;
  updatedAt: Date;
}
export interface CreateCheckoutRequest {
  reportId?: string; // Optional for pre-query payment
  query?: string; // Or pay at time of query
}
export interface CreateCheckoutResponse {
  clientSecret: string;
  paymentIntentId: string;
  amount: number;
  currency: string;
}
export interface PaymentIntentStatus {
  paymentIntentId: string;
  status: PaymentStatus;
  reportId?: string | null;
}
export interface StripeWebhookEvent {
  type: string;
  data: {
    object: {
      id: string;
      status: string;
      metadata?: Record<string, string>;
    };
  };
}