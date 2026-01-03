/**
 * Tests for API schemas
 *
 * Verifies API request/response validation schemas.
 */

import { describe, it, expect } from 'vitest';
import {
  Country,
  ReportStatus,
  PaymentStatus,
  CostRangeSchema,
  ActionPlanSchema,
  ReportContentSchema,
  CitationSchema,
  CreateReportRequestSchema,
  CreateReportResponseSchema,
  ReportSummarySchema,
  ListReportsResponseSchema,
  ReportResponseSchema,
  CreatePaymentRequestSchema,
  CreatePaymentResponseSchema,
  HealthResponseSchema,
  HealthCheckSchema,
  DetailedHealthResponseSchema,
  ErrorResponseSchema,
  SSEEventType,
  SSEEventSchema,
  PaginationParamsSchema,
  ErrorCode,
} from '../src/schemas/api.schema';

describe('API Schemas', () => {
  describe('Enums', () => {
    it('should validate Country enum', () => {
      expect(Country.safeParse('UK').success).toBe(true);
      expect(Country.safeParse('US').success).toBe(false);
    });

    it('should validate ReportStatus enum', () => {
      expect(ReportStatus.safeParse('generating').success).toBe(true);
      expect(ReportStatus.safeParse('completed').success).toBe(true);
      expect(ReportStatus.safeParse('failed').success).toBe(true);
      expect(ReportStatus.safeParse('invalid').success).toBe(false);
    });

    it('should validate PaymentStatus enum', () => {
      expect(PaymentStatus.safeParse('succeeded').success).toBe(true);
      expect(PaymentStatus.safeParse('bypassed').success).toBe(true);
      expect(PaymentStatus.safeParse('invalid').success).toBe(false);
    });

    it('should validate SSEEventType enum', () => {
      expect(SSEEventType.safeParse('start').success).toBe(true);
      expect(SSEEventType.safeParse('chunk').success).toBe(true);
      expect(SSEEventType.safeParse('complete').success).toBe(true);
      expect(SSEEventType.safeParse('invalid').success).toBe(false);
    });

    it('should validate ErrorCode enum', () => {
      expect(ErrorCode.safeParse('VALIDATION_ERROR').success).toBe(true);
      expect(ErrorCode.safeParse('NOT_FOUND').success).toBe(true);
      expect(ErrorCode.safeParse('INTERNAL_SERVER_ERROR').success).toBe(true);
      expect(ErrorCode.safeParse('INVALID').success).toBe(false);
    });
  });

  describe('Object Schemas', () => {
    it('should validate CostRangeSchema', () => {
      const valid = { min: 1000, max: 2000, currency: 'GBP' };
      expect(CostRangeSchema.safeParse(valid).success).toBe(true);

      const invalid = { min: -1, max: 2000, currency: 'GBP' };
      expect(CostRangeSchema.safeParse(invalid).success).toBe(false);
    });

    it('should validate ActionPlanSchema', () => {
      const valid = {
        '30_day': ['Task 1', 'Task 2'],
        '60_day': ['Task 3'],
        '90_day': ['Task 4', 'Task 5'],
      };
      expect(ActionPlanSchema.safeParse(valid).success).toBe(true);

      const invalid = { '30_day': [], '60_day': ['Task'], '90_day': ['Task'] };
      expect(ActionPlanSchema.safeParse(invalid).success).toBe(false);
    });

    it('should validate CitationSchema', () => {
      const valid = {
        source: 'Gov.uk',
        url: 'https://gov.uk/visa',
        retrieved_at: '2025-01-01T00:00:00Z',
        confidence: 0.95,
      };
      expect(CitationSchema.safeParse(valid).success).toBe(true);

      const invalidUrl = { ...valid, url: 'not-a-url' };
      expect(CitationSchema.safeParse(invalidUrl).success).toBe(false);
    });

    it('should validate CreateReportRequestSchema', () => {
      const valid = { subject: 'Computer Science', country: 'UK' };
      expect(CreateReportRequestSchema.safeParse(valid).success).toBe(true);

      const invalid = { subject: '', country: 'UK' };
      expect(CreateReportRequestSchema.safeParse(invalid).success).toBe(false);
    });

    it('should validate CreatePaymentRequestSchema', () => {
      const valid = { amount: 2.99, currency: 'GBP', reportSubject: 'CS' };
      expect(CreatePaymentRequestSchema.safeParse(valid).success).toBe(true);

      const invalidAmount = { amount: 1.99, currency: 'GBP', reportSubject: 'CS' };
      expect(CreatePaymentRequestSchema.safeParse(invalidAmount).success).toBe(false);
    });

    it('should validate PaginationParamsSchema', () => {
      const valid = { limit: 50, offset: 0 };
      expect(PaginationParamsSchema.safeParse(valid).success).toBe(true);

      const withDefaults = {};
      const result = PaginationParamsSchema.safeParse(withDefaults);
      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.limit).toBe(50);
        expect(result.data.offset).toBe(0);
      }
    });

    it('should validate HealthResponseSchema', () => {
      const valid = {
        status: 'healthy',
        timestamp: '2025-01-01T00:00:00Z',
        environment: 'dev',
        version: '1.0.0',
      };
      expect(HealthResponseSchema.safeParse(valid).success).toBe(true);
    });

    it('should validate HealthCheckSchema', () => {
      const valid = { status: 'healthy', latency_ms: 50 };
      expect(HealthCheckSchema.safeParse(valid).success).toBe(true);

      const withError = { status: 'unhealthy', error: 'Connection failed' };
      expect(HealthCheckSchema.safeParse(withError).success).toBe(true);
    });

    it('should validate ErrorResponseSchema', () => {
      const valid = {
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid input',
          correlationId: '123e4567-e89b-12d3-a456-426614174000',
          timestamp: '2025-01-01T00:00:00Z',
        },
      };
      expect(ErrorResponseSchema.safeParse(valid).success).toBe(true);
    });
  });

  describe('Complex Schemas', () => {
    it('should validate ReportContentSchema', () => {
      const valid = {
        executive_summary: ['Point 1', 'Point 2', 'Point 3', 'Point 4', 'Point 5'],
        study_options: { universities: [] },
        estimated_costs: {
          tuition: { min: 10000, max: 20000, currency: 'GBP' },
          living: { min: 8000, max: 12000, currency: 'GBP' },
        },
        visa_overview: 'Student visa information',
        post_study_work: 'Graduate visa details',
        job_prospects: 'Employment prospects',
        fallback_jobs: 'Alternative careers',
        risks: 'Risk considerations',
        action_plan: {
          '30_day': ['Task 1'],
          '60_day': ['Task 2'],
          '90_day': ['Task 3'],
        },
      };
      expect(ReportContentSchema.safeParse(valid).success).toBe(true);
    });

    it('should require at least 5 executive summary points', () => {
      const invalid = {
        executive_summary: ['Point 1', 'Point 2'],
        study_options: {},
        estimated_costs: {
          tuition: { min: 10000, max: 20000, currency: 'GBP' },
          living: { min: 8000, max: 12000, currency: 'GBP' },
        },
        visa_overview: 'Visa info',
        post_study_work: 'Work info',
        job_prospects: 'Jobs',
        fallback_jobs: 'Fallback',
        risks: 'Risks',
        action_plan: {
          '30_day': ['T1'],
          '60_day': ['T2'],
          '90_day': ['T3'],
        },
      };
      expect(ReportContentSchema.safeParse(invalid).success).toBe(false);
    });

    it('should validate ReportResponseSchema', () => {
      const valid = {
        reportId: '123e4567-e89b-12d3-a456-426614174000',
        userId: '123e4567-e89b-12d3-a456-426614174001',
        subject: 'Computer Science',
        country: 'UK',
        status: 'completed',
        content: {
          executive_summary: ['P1', 'P2', 'P3', 'P4', 'P5'],
          study_options: {},
          estimated_costs: {
            tuition: { min: 10000, max: 20000, currency: 'GBP' },
            living: { min: 8000, max: 12000, currency: 'GBP' },
          },
          visa_overview: 'Visa',
          post_study_work: 'Work',
          job_prospects: 'Jobs',
          fallback_jobs: 'Fallback',
          risks: 'Risks',
          action_plan: { '30_day': ['T1'], '60_day': ['T2'], '90_day': ['T3'] },
        },
        citations: [
          {
            source: 'Gov.uk',
            url: 'https://gov.uk',
            retrieved_at: '2025-01-01T00:00:00Z',
            confidence: 0.95,
          },
        ],
        createdAt: '2025-01-01T00:00:00Z',
        expiresAt: '2025-01-31T00:00:00Z',
      };
      expect(ReportResponseSchema.safeParse(valid).success).toBe(true);
    });

    it('should require at least one citation', () => {
      const invalid = {
        reportId: '123e4567-e89b-12d3-a456-426614174000',
        userId: '123e4567-e89b-12d3-a456-426614174001',
        subject: 'Computer Science',
        country: 'UK',
        status: 'completed',
        content: {
          executive_summary: ['P1', 'P2', 'P3', 'P4', 'P5'],
          study_options: {},
          estimated_costs: {
            tuition: { min: 10000, max: 20000, currency: 'GBP' },
            living: { min: 8000, max: 12000, currency: 'GBP' },
          },
          visa_overview: 'Visa',
          post_study_work: 'Work',
          job_prospects: 'Jobs',
          fallback_jobs: 'Fallback',
          risks: 'Risks',
          action_plan: { '30_day': ['T1'], '60_day': ['T2'], '90_day': ['T3'] },
        },
        citations: [],
        createdAt: '2025-01-01T00:00:00Z',
        expiresAt: '2025-01-31T00:00:00Z',
      };
      expect(ReportResponseSchema.safeParse(invalid).success).toBe(false);
    });
  });
});
