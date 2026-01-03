/**
 * API Request/Response Validation Schemas
 *
 * Zod schemas for validating API requests and responses.
 * Ensures type safety and runtime validation for all API interactions.
 *
 * @module shared/config/schemas/api
 */

import { z } from 'zod';

/**
 * Country enum (MVP: UK only)
 */
export const Country = z.enum(['UK']);
export type Country = z.infer<typeof Country>;

/**
 * Report Status enum
 */
export const ReportStatus = z.enum(['generating', 'completed', 'failed']);
export type ReportStatus = z.infer<typeof ReportStatus>;

/**
 * Payment Status enum
 */
export const PaymentStatus = z.enum([
  'requires_payment_method',
  'requires_confirmation',
  'processing',
  'succeeded',
  'failed',
  'canceled',
  'bypassed',
]);
export type PaymentStatus = z.infer<typeof PaymentStatus>;

/**
 * Cost Range Schema
 */
export const CostRangeSchema = z.object({
  min: z.number().min(0),
  max: z.number().min(0),
  currency: z.enum(['GBP']),
});
export type CostRange = z.infer<typeof CostRangeSchema>;

/**
 * Action Plan Schema (30/60/90 days)
 */
export const ActionPlanSchema = z.object({
  '30_day': z.array(z.string()).min(1),
  '60_day': z.array(z.string()).min(1),
  '90_day': z.array(z.string()).min(1),
});
export type ActionPlan = z.infer<typeof ActionPlanSchema>;

/**
 * Report Content Schema
 *
 * Validates the structure of AI-generated report content.
 * Matches the mandatory sections from spec.md Section 11.
 */
export const ReportContentSchema = z.object({
  executive_summary: z
    .array(z.string())
    .min(5)
    .max(10)
    .describe('5-10 bullet point summary'),
  study_options: z.object({}).passthrough().describe('Universities and programs'),
  estimated_costs: z
    .object({
      tuition: CostRangeSchema,
      living: CostRangeSchema,
    })
    .describe('Tuition and living cost ranges'),
  visa_overview: z.string().min(1).describe('High-level visa information'),
  post_study_work: z.string().min(1).describe('Post-study work visa options'),
  job_prospects: z.string().min(1).describe('Employment prospects in chosen field'),
  fallback_jobs: z.string().min(1).describe('Alternative career paths'),
  risks: z.string().min(1).describe('Realistic risks and challenges'),
  action_plan: ActionPlanSchema,
});
export type ReportContent = z.infer<typeof ReportContentSchema>;

/**
 * Citation Schema
 *
 * Validates citations for RAG integrity.
 */
export const CitationSchema = z.object({
  source: z.string().min(1).describe('Name of the source'),
  url: z.string().url().describe('Source URL'),
  retrieved_at: z.string().datetime().describe('Timestamp when data was retrieved'),
  confidence: z.number().min(0).max(1).describe('Confidence score (0-1)'),
});
export type Citation = z.infer<typeof CitationSchema>;

/**
 * Create Report Request Schema
 */
export const CreateReportRequestSchema = z.object({
  subject: z.string().min(1).max(255).describe('Field of study'),
  country: Country.default('UK'),
});
export type CreateReportRequest = z.infer<typeof CreateReportRequestSchema>;

/**
 * Create Report Response Schema
 */
export const CreateReportResponseSchema = z.object({
  reportId: z.string().uuid(),
  streamUrl: z.string().url(),
  status: ReportStatus,
  createdAt: z.string().datetime(),
  expiresAt: z.string().datetime(),
});
export type CreateReportResponse = z.infer<typeof CreateReportResponseSchema>;

/**
 * Report Summary Schema (for list endpoint)
 */
export const ReportSummarySchema = z.object({
  reportId: z.string().uuid(),
  subject: z.string(),
  country: Country,
  status: ReportStatus,
  createdAt: z.string().datetime(),
  expiresAt: z.string().datetime(),
});
export type ReportSummary = z.infer<typeof ReportSummarySchema>;

/**
 * List Reports Response Schema
 */
export const ListReportsResponseSchema = z.object({
  reports: z.array(ReportSummarySchema),
  total: z.number().int().min(0),
  limit: z.number().int().min(1),
  offset: z.number().int().min(0),
});
export type ListReportsResponse = z.infer<typeof ListReportsResponseSchema>;

/**
 * Report Response Schema (full report)
 */
export const ReportResponseSchema = z.object({
  reportId: z.string().uuid(),
  userId: z.string().uuid(),
  subject: z.string(),
  country: Country,
  status: ReportStatus,
  content: ReportContentSchema,
  citations: z.array(CitationSchema).min(1).describe('Must have at least one citation'),
  createdAt: z.string().datetime(),
  expiresAt: z.string().datetime(),
});
export type ReportResponse = z.infer<typeof ReportResponseSchema>;

/**
 * Create Payment Request Schema
 */
export const CreatePaymentRequestSchema = z.object({
  amount: z.number().min(2.99).max(2.99),
  currency: z.enum(['GBP']),
  reportSubject: z.string().min(1),
});
export type CreatePaymentRequest = z.infer<typeof CreatePaymentRequestSchema>;

/**
 * Create Payment Response Schema
 */
export const CreatePaymentResponseSchema = z.object({
  paymentId: z.string().uuid(),
  clientSecret: z.string(),
  amount: z.number(),
  currency: z.string(),
  status: PaymentStatus,
  bypassed: z.boolean().optional(),
});
export type CreatePaymentResponse = z.infer<typeof CreatePaymentResponseSchema>;

/**
 * Health Check Response Schema
 */
export const HealthResponseSchema = z.object({
  status: z.enum(['healthy', 'degraded', 'unhealthy']),
  timestamp: z.string().datetime(),
  environment: z.enum(['dev', 'test', 'production']),
  version: z.string(),
});
export type HealthResponse = z.infer<typeof HealthResponseSchema>;

/**
 * Individual Health Check Schema
 */
export const HealthCheckSchema = z.object({
  status: z.enum(['healthy', 'degraded', 'unhealthy']),
  latency_ms: z.number().int().min(0).optional(),
  error: z.string().optional(),
});
export type HealthCheck = z.infer<typeof HealthCheckSchema>;

/**
 * Detailed Health Check Response Schema
 */
export const DetailedHealthResponseSchema = HealthResponseSchema.extend({
  checks: z.object({
    database: HealthCheckSchema,
    gemini_api: HealthCheckSchema,
    stripe_api: HealthCheckSchema,
  }),
});
export type DetailedHealthResponse = z.infer<typeof DetailedHealthResponseSchema>;

/**
 * Error Response Schema
 */
export const ErrorResponseSchema = z.object({
  error: z.object({
    code: z.string().describe('Machine-readable error code'),
    message: z.string().describe('Human-readable error message'),
    correlationId: z.string().uuid().describe('Request correlation ID'),
    timestamp: z.string().datetime(),
    details: z.object({}).passthrough().optional(),
  }),
});
export type ErrorResponse = z.infer<typeof ErrorResponseSchema>;

/**
 * SSE Event Types
 */
export const SSEEventType = z.enum(['start', 'chunk', 'citation', 'complete', 'error']);
export type SSEEventType = z.infer<typeof SSEEventType>;

/**
 * SSE Event Schema
 */
export const SSEEventSchema = z.object({
  event: SSEEventType,
  data: z.union([
    z.object({ reportId: z.string().uuid(), status: ReportStatus }),
    z.object({ section: z.string(), content: z.string() }),
    CitationSchema,
    ErrorResponseSchema,
  ]),
});
export type SSEEvent = z.infer<typeof SSEEventSchema>;

/**
 * Pagination Parameters Schema
 */
export const PaginationParamsSchema = z.object({
  limit: z.coerce.number().int().min(1).max(100).default(50),
  offset: z.coerce.number().int().min(0).default(0),
});
export type PaginationParams = z.infer<typeof PaginationParamsSchema>;

/**
 * Error Codes Enum
 */
export const ErrorCode = z.enum([
  'VALIDATION_ERROR',
  'UNAUTHORIZED',
  'FORBIDDEN',
  'NOT_FOUND',
  'PAYMENT_REQUIRED',
  'PAYMENT_FAILED',
  'RATE_LIMIT_EXCEEDED',
  'INTERNAL_SERVER_ERROR',
  'SERVICE_UNAVAILABLE',
  'GEMINI_API_ERROR',
  'DATABASE_ERROR',
  'REPORT_GENERATION_FAILED',
  'REPORT_EXPIRED',
  'REPORT_DELETED',
  'INVALID_COUNTRY',
  'INVALID_SUBJECT',
]);
export type ErrorCode = z.infer<typeof ErrorCode>;
