/**
 * Tests for Payment repository
 */
// @ts-nocheck


import { describe, it, expect, beforeEach, vi } from 'vitest';
import { PaymentRepository } from '../../src/repositories/payment';
import { DatabaseAdapter } from '../../src/adapters/base';

describe('PaymentRepository', () => {
  let repository: PaymentRepository;
  let mockAdapter: DatabaseAdapter;

  beforeEach(() => {
    mockAdapter = {
      query: vi.fn(),
      beginTransaction: vi.fn(),
      close: vi.fn(),
      getType: vi.fn(() => 'postgres'),
    } as any;

    repository = new PaymentRepository(mockAdapter);
  });

  const mockPaymentRow = {
    payment_id: 'payment-123',
    user_id: 'user-123',
    report_id: 'report-123',
    amount: 299,
    currency: 'GBP',
    status: 'succeeded',
    stripe_payment_intent_id: 'pi_123',
    created_at: new Date('2025-01-01'),
  };

  describe('findById', () => {
    it('should find payment by ID for user', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [mockPaymentRow],
        rowCount: 1,
      });

      const result = await repository.findById('payment-123', 'user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('WHERE payment_id = $1'),
        ['payment-123', 'user-123'],
      );
      expect(result?.paymentId).toBe('payment-123');
    });

    it('should return null when payment not found', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      const result = await repository.findById('nonexistent', 'user-123');

      expect(result).toBeNull();
    });

    it('should not find payment from different user', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      const result = await repository.findById('payment-123', 'different-user');

      expect(result).toBeNull();
    });
  });

  describe('findByStripePaymentIntentId', () => {
    it('should find payment by Stripe payment intent ID', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [mockPaymentRow],
        rowCount: 1,
      });

      const result = await repository.findByStripePaymentIntentId('pi_123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        'SELECT * FROM payments WHERE stripe_payment_intent_id = $1',
        ['pi_123'],
      );
      expect(result?.stripePaymentIntentId).toBe('pi_123');
    });

    it('should return null when payment not found', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      const result = await repository.findByStripePaymentIntentId('pi_nonexistent');

      expect(result).toBeNull();
    });
  });

  describe('listByUser', () => {
    it('should list all payments for user', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [mockPaymentRow, { ...mockPaymentRow, payment_id: 'payment-456' }],
        rowCount: 2,
      });

      const result = await repository.listByUser('user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('WHERE user_id = $1'),
        ['user-123', 50, 0],
      );
      expect(result).toHaveLength(2);
    });

    it('should support pagination', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.listByUser('user-123', 10, 20);

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('LIMIT $2 OFFSET $3'),
        ['user-123', 10, 20],
      );
    });

    it('should order by created_at DESC', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.listByUser('user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('ORDER BY created_at DESC'),
        expect.any(Array),
      );
    });

    it('should use default limit and offset', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.listByUser('user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(expect.any(String), ['user-123', 50, 0]);
    });
  });

  describe('countByUser', () => {
    it('should count all payments for user', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ count: '5' }],
        rowCount: 1,
      });

      const result = await repository.countByUser('user-123');

      expect(result).toBe(5);
    });

    it('should return zero when no payments', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ count: '0' }],
        rowCount: 1,
      });

      const result = await repository.countByUser('user-123');

      expect(result).toBe(0);
    });
  });

  describe('create', () => {
    it('should create a new payment', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [mockPaymentRow],
        rowCount: 1,
      });

      const result = await repository.create({
        userId: 'user-123',
        amount: 299,
        currency: 'GBP',
        status: 'pending',
        stripePaymentIntentId: 'pi_123',
        reportId: 'report-123',
      });

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('INSERT INTO payments'),
        ['user-123', 'report-123', 299, 'GBP', 'pending', 'pi_123'],
      );
      expect(result.paymentId).toBe('payment-123');
    });

    it('should create payment without report ID', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ ...mockPaymentRow, report_id: null }],
        rowCount: 1,
      });

      const result = await repository.create({
        userId: 'user-123',
        amount: 299,
        currency: 'GBP',
        status: 'pending',
        stripePaymentIntentId: 'pi_123',
      });

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.any(String),
        ['user-123', null, 299, 'GBP', 'pending', 'pi_123'],
      );
      expect(result.reportId).toBeNull();
    });

    it('should handle duplicate stripe_payment_intent_id', async () => {
      (mockAdapter.query as any).mockRejectedValueOnce(new Error('duplicate key value'));

      await expect(
        repository.create({
          userId: 'user-123',
          amount: 299,
          currency: 'GBP',
          status: 'pending',
          stripePaymentIntentId: 'pi_existing',
        }),
      ).rejects.toThrow('duplicate key value');
    });
  });

  describe('updateStatus', () => {
    it('should update payment status', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 1,
      });

      await repository.updateStatus('payment-123', 'succeeded');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        'UPDATE payments SET status = $1 WHERE payment_id = $2',
        ['succeeded', 'payment-123'],
      );
    });

    it('should handle all valid statuses', async () => {
      const statuses: Array<'pending' | 'succeeded' | 'failed' | 'canceled'> = [
        'pending',
        'succeeded',
        'failed',
        'canceled',
      ];

      for (const status of statuses) {
        (mockAdapter.query as any).mockResolvedValueOnce({
          rows: [],
          rowCount: 1,
        });

        await repository.updateStatus('payment-123', status);

        expect(mockAdapter.query).toHaveBeenCalledWith(
          expect.any(String),
          [status, 'payment-123'],
        );
      }
    });
  });

  describe('linkToReport', () => {
    it('should link payment to report', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 1,
      });

      await repository.linkToReport('payment-123', 'report-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        'UPDATE payments SET report_id = $1 WHERE payment_id = $2',
        ['report-123', 'payment-123'],
      );
    });

    it('should handle nonexistent payment', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.linkToReport('nonexistent', 'report-123');

      // Should not throw
      expect(mockAdapter.query).toHaveBeenCalled();
    });
  });

  describe('listSuccessfulByUser', () => {
    it('should list only successful payments', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [mockPaymentRow],
        rowCount: 1,
      });

      const result = await repository.listSuccessfulByUser('user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining("status = 'succeeded'"),
        ['user-123'],
      );
      expect(result).toHaveLength(1);
    });

    it('should order by created_at DESC', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.listSuccessfulByUser('user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('ORDER BY created_at DESC'),
        expect.any(Array),
      );
    });
  });

  describe('countSuccessfulByUser', () => {
    it('should count successful payments', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ count: '3' }],
        rowCount: 1,
      });

      const result = await repository.countSuccessfulByUser('user-123');

      expect(result).toBe(3);
    });

    it('should only count succeeded status', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ count: '2' }],
        rowCount: 1,
      });

      await repository.countSuccessfulByUser('user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining("status = 'succeeded'"),
        ['user-123'],
      );
    });
  });

  describe('getTotalRevenue', () => {
    it('should calculate total revenue from successful payments', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ total: '1495' }], // 5 payments * 299
        rowCount: 1,
      });

      const result = await repository.getTotalRevenue();

      expect(result).toBe(1495);
    });

    it('should return zero when no successful payments', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ total: '0' }],
        rowCount: 1,
      });

      const result = await repository.getTotalRevenue();

      expect(result).toBe(0);
    });

    it('should only sum successful payments', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ total: '598' }],
        rowCount: 1,
      });

      await repository.getTotalRevenue();

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining("WHERE status = 'succeeded'"),
      );
    });

    it('should handle large revenue amounts', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ total: '1000000' }],
        rowCount: 1,
      });

      const result = await repository.getTotalRevenue();

      expect(result).toBe(1000000);
    });
  });

  describe('hasSuccessfulPayment', () => {
    it('should return true when user has successful payment', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ exists: true }],
        rowCount: 1,
      });

      const result = await repository.hasSuccessfulPayment('user-123');

      expect(result).toBe(true);
    });

    it('should return false when user has no successful payment', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      const result = await repository.hasSuccessfulPayment('user-123');

      expect(result).toBe(false);
    });

    it('should only check succeeded status', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.hasSuccessfulPayment('user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining("status = 'succeeded'"),
        ['user-123'],
      );
    });

    it('should use LIMIT 1 for efficiency', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.hasSuccessfulPayment('user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('LIMIT 1'),
        expect.any(Array),
      );
    });
  });
});
