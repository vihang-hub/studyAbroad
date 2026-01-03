/**
 * Report types for frontend
 * Based on API schema from shared-config
 */

export type ReportStatus = 'pending' | 'processing' | 'generating' | 'completed' | 'failed' | 'expired';

export interface Report {
  id: string;
  userId: string;
  query: string;
  status: ReportStatus;
  content?: ReportContent;
  createdAt: string;
  updatedAt: string;
  deletedAt?: string;
  expires_at?: string;
}

export interface ReportContent {
  executiveSummary: string;
  summary: string; // Executive summary text
  query: string; // Original user query
  total_citations: number; // Total number of citations
  generated_at: string; // ISO date string when generated
  sections: ReportSection[];
  citations: Citation[];
  actionPlan: ActionPlan;
}

export interface ReportSection {
  title: string;
  heading: string; // Section heading
  content: string;
  subsections?: ReportSection[];
  citations?: Citation[]; // Citations specific to this section
}

export interface Citation {
  id?: string;
  title: string;
  url: string;
  accessedAt?: string;
  snippet?: string;
}

export interface ActionPlan {
  steps: ActionStep[];
  timeline: string;
  resources: string[];
}

export interface ActionStep {
  id: string;
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  estimatedDuration: string;
}
