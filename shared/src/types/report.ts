/**
 * Report-related TypeScript interfaces
 * For AI-generated research reports
 */

export type ReportStatus = 'pending' | 'generating' | 'completed' | 'failed' | 'expired';

export interface Citation {
  title: string;
  url: string;
  snippet?: string;
  accessedAt: Date;
}

export interface ReportSection {
  heading: string;
  content: string;
  citations: Citation[];
}

export interface ReportContent {
  query: string;
  summary: string;
  sections: ReportSection[];
  totalCitations: number;
  generatedAt: Date;
}

export interface Report {
  id: string;
  userId: string;
  query: string;
  status: ReportStatus;
  content?: ReportContent | null;
  error?: string | null;
  expiresAt: Date;
  createdAt: Date;
  updatedAt: Date;
  deletedAt?: Date | null;
}

export interface ReportListItem {
  id: string;
  query: string;
  status: ReportStatus;
  createdAt: Date;
  expiresAt: Date;
}

export interface CreateReportRequest {
  query: string;
}

export interface CreateReportResponse {
  reportId: string;
  status: ReportStatus;
  estimatedCompletionSeconds: number;
}
