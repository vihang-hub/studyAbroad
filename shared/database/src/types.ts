/**
 * Database entity types
 * Defines the structure of database entities used across the application
 */

/**
 * Soft-deletable entity interface
 * Entities implementing this interface support soft delete pattern
 */
export interface SoftDeletable {
  deletedAt: Date | null;
}

/**
 * User entity
 */
export interface User {
  userId: string;
  clerkUserId: string;
  email: string;
  createdAt: Date;
}

/**
 * Report entity with soft delete support
 */
export interface Report extends SoftDeletable {
  reportId: string;
  userId: string;
  subject: string;
  country: string;
  content: any;
  citations: any[];
  status: 'generating' | 'completed' | 'failed';
  createdAt: Date;
  expiresAt: Date;
  updatedAt: Date;
  deletedAt: Date | null;
}

/**
 * Payment entity
 */
export interface Payment {
  paymentId: string;
  userId: string;
  reportId: string | null;
  amount: number;
  currency: string;
  status: 'pending' | 'succeeded' | 'failed' | 'canceled';
  stripePaymentIntentId: string;
  createdAt: Date;
}

/**
 * Database row to entity mappers
 * Converts database row objects to typed entities
 */

/**
 * Map database row to User entity
 */
export function mapToUser(row: any): User {
  return {
    userId: row.user_id,
    clerkUserId: row.clerk_user_id,
    email: row.email,
    createdAt: new Date(row.created_at),
  };
}

/**
 * Map database row to Report entity
 */
export function mapToReport(row: any): Report {
  return {
    reportId: row.report_id,
    userId: row.user_id,
    subject: row.subject,
    country: row.country,
    content: row.content,
    citations: row.citations,
    status: row.status,
    createdAt: new Date(row.created_at),
    expiresAt: new Date(row.expires_at),
    updatedAt: new Date(row.updated_at),
    deletedAt: row.deleted_at ? new Date(row.deleted_at) : null,
  };
}

/**
 * Map database row to Payment entity
 */
export function mapToPayment(row: any): Payment {
  return {
    paymentId: row.payment_id,
    userId: row.user_id,
    reportId: row.report_id,
    amount: row.amount,
    currency: row.currency,
    status: row.status,
    stripePaymentIntentId: row.stripe_payment_intent_id,
    createdAt: new Date(row.created_at),
  };
}
