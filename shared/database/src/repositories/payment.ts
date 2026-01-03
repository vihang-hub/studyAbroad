/**
 * Payment repository
 * Handles payment CRUD operations
 */

import { BaseRepository } from './base';
import { Payment, mapToPayment } from '../types';

/**
 * Payment repository implementation
 * Note: Payments do not have soft delete
 */
export class PaymentRepository extends BaseRepository {
  /**
   * Find payment by ID
   */
  async findById(paymentId: string, userId: string): Promise<Payment | null> {
    const { rows } = await this.db.query<any>(
      `SELECT * FROM payments
       WHERE payment_id = $1
         AND user_id = $2`,
      [paymentId, userId],
    );

    return rows[0] ? mapToPayment(rows[0]) : null;
  }

  /**
   * Find payment by Stripe payment intent ID
   */
  async findByStripePaymentIntentId(stripePaymentIntentId: string): Promise<Payment | null> {
    const { rows } = await this.db.query<any>(
      'SELECT * FROM payments WHERE stripe_payment_intent_id = $1',
      [stripePaymentIntentId],
    );

    return rows[0] ? mapToPayment(rows[0]) : null;
  }

  /**
   * List all payments for a user
   */
  async listByUser(
    userId: string,
    limit: number = 50,
    offset: number = 0,
  ): Promise<Payment[]> {
    const { rows } = await this.db.query<any>(
      `SELECT * FROM payments
       WHERE user_id = $1
       ORDER BY created_at DESC
       LIMIT $2 OFFSET $3`,
      [userId, limit, offset],
    );

    return rows.map(mapToPayment);
  }

  /**
   * Count total payments for a user
   */
  async countByUser(userId: string): Promise<number> {
    const { rows } = await this.db.query<{ count: string }>(
      'SELECT COUNT(*) as count FROM payments WHERE user_id = $1',
      [userId],
    );

    return parseInt(rows[0].count, 10);
  }

  /**
   * Create a new payment
   */
  async create(data: {
    userId: string;
    amount: number;
    currency: string;
    status: 'pending' | 'succeeded' | 'failed' | 'canceled';
    stripePaymentIntentId: string;
    reportId?: string;
  }): Promise<Payment> {
    const { rows } = await this.db.query<any>(
      `INSERT INTO payments (user_id, report_id, amount, currency, status, stripe_payment_intent_id)
       VALUES ($1, $2, $3, $4, $5, $6)
       RETURNING *`,
      [
        data.userId,
        data.reportId ?? null,
        data.amount,
        data.currency,
        data.status,
        data.stripePaymentIntentId,
      ],
    );

    return mapToPayment(rows[0]);
  }

  /**
   * Update payment status
   */
  async updateStatus(
    paymentId: string,
    status: 'pending' | 'succeeded' | 'failed' | 'canceled',
  ): Promise<void> {
    await this.db.query(
      'UPDATE payments SET status = $1 WHERE payment_id = $2',
      [status, paymentId],
    );
  }

  /**
   * Link payment to report
   */
  async linkToReport(paymentId: string, reportId: string): Promise<void> {
    await this.db.query(
      'UPDATE payments SET report_id = $1 WHERE payment_id = $2',
      [reportId, paymentId],
    );
  }

  /**
   * List successful payments for a user
   */
  async listSuccessfulByUser(userId: string): Promise<Payment[]> {
    const { rows } = await this.db.query<any>(
      `SELECT * FROM payments
       WHERE user_id = $1
         AND status = 'succeeded'
       ORDER BY created_at DESC`,
      [userId],
    );

    return rows.map(mapToPayment);
  }

  /**
   * Count successful payments for a user
   */
  async countSuccessfulByUser(userId: string): Promise<number> {
    const { rows } = await this.db.query<{ count: string }>(
      `SELECT COUNT(*) as count FROM payments
       WHERE user_id = $1
         AND status = 'succeeded'`,
      [userId],
    );

    return parseInt(rows[0].count, 10);
  }

  /**
   * Get total revenue (sum of all successful payments)
   */
  async getTotalRevenue(): Promise<number> {
    const { rows } = await this.db.query<{ total: string }>(
      `SELECT COALESCE(SUM(amount), 0) as total FROM payments
       WHERE status = 'succeeded'`,
    );

    return parseInt(rows[0].total, 10);
  }

  /**
   * Check if user has any successful payment
   */
  async hasSuccessfulPayment(userId: string): Promise<boolean> {
    const { rowCount } = await this.db.query(
      `SELECT 1 FROM payments
       WHERE user_id = $1
         AND status = 'succeeded'
       LIMIT 1`,
      [userId],
    );

    return rowCount > 0;
  }
}
