/**
 * @study-abroad/shared-config
 *
 * Environment configuration management with type-safe validation.
 *
 * @module @study-abroad/shared-config
 */
// @ts-nocheck


// Export main configuration loader
export { ConfigLoader } from './loader';

// Export environment schemas and types
export {
  EnvironmentConfigSchema,
  EnvironmentMode,
  LogLevel,
  AuthProvider,
  PaymentStatus,
  ReportStatus,
  type EnvironmentConfig,
} from './schemas/environment.schema';

// Export API schemas and types
export {
  Country,
  ReportStatus as APIReportStatus,
  PaymentStatus as APIPaymentStatus,
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
  type CostRange,
  type ActionPlan,
  type ReportContent,
  type Citation,
  type CreateReportRequest,
  type CreateReportResponse,
  type ReportSummary,
  type ListReportsResponse,
  type ReportResponse,
  type CreatePaymentRequest,
  type CreatePaymentResponse,
  type HealthResponse,
  type HealthCheck,
  type DetailedHealthResponse,
  type ErrorResponse,
  type SSEEvent,
  type PaginationParams,
} from './schemas/api.schema';

// Export preset utilities
export {
  EnvironmentPresets,
  DEV_PRESET,
  TEST_PRESET,
  PRODUCTION_PRESET,
  getPreset,
  mergePreset,
} from './presets';
