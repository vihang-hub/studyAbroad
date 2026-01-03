/**
 * Tests for database types and mappers
 */

import { describe, it, expect } from 'vitest';
import { mapToUser, mapToReport, mapToPayment } from '../src/types';

describe('Database Type Mappers', () => {
  describe('mapToUser', () => {
    it('should map database row to User entity', () => {
      const row = {
        user_id: 'user-123',
        clerk_user_id: 'clerk-123',
        email: 'test@example.com',
        created_at: new Date('2025-01-01T00:00:00Z'),
      };

      const user = mapToUser(row);

      expect(user).toEqual({
        userId: 'user-123',
        clerkUserId: 'clerk-123',
        email: 'test@example.com',
        createdAt: new Date('2025-01-01T00:00:00Z'),
      });
    });

    it('should convert snake_case to camelCase', () => {
      const row = {
        user_id: 'user-123',
        clerk_user_id: 'clerk-123',
        email: 'test@example.com',
        created_at: new Date('2025-01-01'),
      };

      const user = mapToUser(row);

      expect(user.userId).toBe('user-123');
      expect(user.clerkUserId).toBe('clerk-123');
      expect(user.createdAt).toBeInstanceOf(Date);
    });

    it('should convert string timestamps to Date objects', () => {
      const row = {
        user_id: 'user-123',
        clerk_user_id: 'clerk-123',
        email: 'test@example.com',
        created_at: '2025-01-01T12:00:00Z',
      };

      const user = mapToUser(row);

      expect(user.createdAt).toBeInstanceOf(Date);
      expect(user.createdAt.toISOString()).toBe('2025-01-01T12:00:00.000Z');
    });
  });

  describe('mapToReport', () => {
    it('should map database row to Report entity', () => {
      const row = {
        report_id: 'report-123',
        user_id: 'user-123',
        subject: 'Computer Science',
        country: 'UK',
        content: { section1: 'content' },
        citations: [{ title: 'Source 1', url: 'https://example.com' }],
        status: 'completed',
        created_at: new Date('2025-01-01'),
        expires_at: new Date('2025-01-31'),
        updated_at: new Date('2025-01-01'),
        deleted_at: null,
      };

      const report = mapToReport(row);

      expect(report).toEqual({
        reportId: 'report-123',
        userId: 'user-123',
        subject: 'Computer Science',
        country: 'UK',
        content: { section1: 'content' },
        citations: [{ title: 'Source 1', url: 'https://example.com' }],
        status: 'completed',
        createdAt: new Date('2025-01-01'),
        expiresAt: new Date('2025-01-31'),
        updatedAt: new Date('2025-01-01'),
        deletedAt: null,
      });
    });

    it('should handle soft-deleted report', () => {
      const row = {
        report_id: 'report-123',
        user_id: 'user-123',
        subject: 'Computer Science',
        country: 'UK',
        content: {},
        citations: [],
        status: 'completed',
        created_at: new Date('2025-01-01'),
        expires_at: new Date('2025-01-31'),
        updated_at: new Date('2025-01-01'),
        deleted_at: new Date('2025-01-15'),
      };

      const report = mapToReport(row);

      expect(report.deletedAt).toBeInstanceOf(Date);
      expect(report.deletedAt?.toISOString()).toBe('2025-01-15T00:00:00.000Z');
    });

    it('should handle null deleted_at', () => {
      const row = {
        report_id: 'report-123',
        user_id: 'user-123',
        subject: 'Computer Science',
        country: 'UK',
        content: {},
        citations: [],
        status: 'completed',
        created_at: new Date('2025-01-01'),
        expires_at: new Date('2025-01-31'),
        updated_at: new Date('2025-01-01'),
        deleted_at: null,
      };

      const report = mapToReport(row);

      expect(report.deletedAt).toBeNull();
    });

    it('should convert string timestamps to Date objects', () => {
      const row = {
        report_id: 'report-123',
        user_id: 'user-123',
        subject: 'Computer Science',
        country: 'UK',
        content: {},
        citations: [],
        status: 'generating',
        created_at: '2025-01-01T00:00:00Z',
        expires_at: '2025-01-31T00:00:00Z',
        updated_at: '2025-01-01T00:00:00Z',
        deleted_at: null,
      };

      const report = mapToReport(row);

      expect(report.createdAt).toBeInstanceOf(Date);
      expect(report.expiresAt).toBeInstanceOf(Date);
      expect(report.updatedAt).toBeInstanceOf(Date);
    });

    it('should preserve JSONB content structure', () => {
      const complexContent = {
        executive_summary: ['Point 1', 'Point 2'],
        study_options: 'Detailed options',
        estimated_costs: {
          tuition_ranges: '£10,000 - £20,000',
          living_costs: '£12,000 - £15,000',
        },
      };

      const row = {
        report_id: 'report-123',
        user_id: 'user-123',
        subject: 'Computer Science',
        country: 'UK',
        content: complexContent,
        citations: [],
        status: 'completed',
        created_at: new Date('2025-01-01'),
        expires_at: new Date('2025-01-31'),
        updated_at: new Date('2025-01-01'),
        deleted_at: null,
      };

      const report = mapToReport(row);

      expect(report.content).toEqual(complexContent);
    });

    it('should handle all valid report statuses', () => {
      const statuses = ['generating', 'completed', 'failed'] as const;

      statuses.forEach((status) => {
        const row = {
          report_id: 'report-123',
          user_id: 'user-123',
          subject: 'Computer Science',
          country: 'UK',
          content: {},
          citations: [],
          status,
          created_at: new Date('2025-01-01'),
          expires_at: new Date('2025-01-31'),
          updated_at: new Date('2025-01-01'),
          deleted_at: null,
        };

        const report = mapToReport(row);

        expect(report.status).toBe(status);
      });
    });
  });

  describe('mapToPayment', () => {
    it('should map database row to Payment entity', () => {
      const row = {
        payment_id: 'payment-123',
        user_id: 'user-123',
        report_id: 'report-123',
        amount: 299,
        currency: 'GBP',
        status: 'succeeded',
        stripe_payment_intent_id: 'pi_123',
        created_at: new Date('2025-01-01'),
      };

      const payment = mapToPayment(row);

      expect(payment).toEqual({
        paymentId: 'payment-123',
        userId: 'user-123',
        reportId: 'report-123',
        amount: 299,
        currency: 'GBP',
        status: 'succeeded',
        stripePaymentIntentId: 'pi_123',
        createdAt: new Date('2025-01-01'),
      });
    });

    it('should handle null report_id', () => {
      const row = {
        payment_id: 'payment-123',
        user_id: 'user-123',
        report_id: null,
        amount: 299,
        currency: 'GBP',
        status: 'pending',
        stripe_payment_intent_id: 'pi_123',
        created_at: new Date('2025-01-01'),
      };

      const payment = mapToPayment(row);

      expect(payment.reportId).toBeNull();
    });

    it('should convert string timestamp to Date object', () => {
      const row = {
        payment_id: 'payment-123',
        user_id: 'user-123',
        report_id: 'report-123',
        amount: 299,
        currency: 'GBP',
        status: 'succeeded',
        stripe_payment_intent_id: 'pi_123',
        created_at: '2025-01-01T12:00:00Z',
      };

      const payment = mapToPayment(row);

      expect(payment.createdAt).toBeInstanceOf(Date);
      expect(payment.createdAt.toISOString()).toBe('2025-01-01T12:00:00.000Z');
    });

    it('should handle all valid payment statuses', () => {
      const statuses = ['pending', 'succeeded', 'failed', 'canceled'] as const;

      statuses.forEach((status) => {
        const row = {
          payment_id: 'payment-123',
          user_id: 'user-123',
          report_id: 'report-123',
          amount: 299,
          currency: 'GBP',
          status,
          stripe_payment_intent_id: 'pi_123',
          created_at: new Date('2025-01-01'),
        };

        const payment = mapToPayment(row);

        expect(payment.status).toBe(status);
      });
    });

    it('should preserve amount as number', () => {
      const row = {
        payment_id: 'payment-123',
        user_id: 'user-123',
        report_id: 'report-123',
        amount: 299,
        currency: 'GBP',
        status: 'succeeded',
        stripe_payment_intent_id: 'pi_123',
        created_at: new Date('2025-01-01'),
      };

      const payment = mapToPayment(row);

      expect(typeof payment.amount).toBe('number');
      expect(payment.amount).toBe(299);
    });

    it('should preserve currency string', () => {
      const row = {
        payment_id: 'payment-123',
        user_id: 'user-123',
        report_id: 'report-123',
        amount: 299,
        currency: 'GBP',
        status: 'succeeded',
        stripe_payment_intent_id: 'pi_123',
        created_at: new Date('2025-01-01'),
      };

      const payment = mapToPayment(row);

      expect(payment.currency).toBe('GBP');
    });
  });
});
