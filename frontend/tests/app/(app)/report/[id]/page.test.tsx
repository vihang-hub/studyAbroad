/**
 * Tests for report detail page
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor, act } from '@testing-library/react';
import React from 'react';

// Mock next/navigation
const mockPush = vi.fn();
vi.mock('next/navigation', () => ({
  useParams: () => ({ id: 'test-report-id' }),
  useRouter: () => ({
    push: mockPush,
  }),
}));

// Mock API client
const mockApiGet = vi.fn();
vi.mock('../../../../../src/lib/api-client', () => ({
  api: {
    get: mockApiGet,
  },
}));

// Mock report components
vi.mock('../../../../../src/components/reports/ExecutiveSummary', () => ({
  ExecutiveSummary: ({ summary, query }: { summary: string; query: string }) => (
    <div data-testid="executive-summary">
      <span data-testid="summary">{summary}</span>
      <span data-testid="query">{query}</span>
    </div>
  ),
}));

vi.mock('../../../../../src/components/reports/ReportSection', () => ({
  ReportSection: ({ section, index }: { section: { title: string }; index: number }) => (
    <div data-testid={`section-${index}`}>{section.title}</div>
  ),
}));

describe('ReportDetailPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.resetModules();
  });

  describe('loading state', () => {
    it('should show loading spinner initially', async () => {
      mockApiGet.mockImplementation(() => new Promise(() => {})); // Never resolves

      const ReportDetailPage = (await import('../../../../../src/app/(app)/report/[id]/page')).default;
      render(<ReportDetailPage />);

      expect(screen.getByText('Loading report...')).toBeInTheDocument();
    });

    it('should show loading spinner element', async () => {
      mockApiGet.mockImplementation(() => new Promise(() => {}));

      const ReportDetailPage = (await import('../../../../../src/app/(app)/report/[id]/page')).default;
      const { container } = render(<ReportDetailPage />);

      const spinner = container.querySelector('.animate-spin');
      expect(spinner).toBeInTheDocument();
    });
  });

  describe('error state', () => {
    it('should show error when API returns error', async () => {
      mockApiGet.mockResolvedValue({ data: null, error: { message: 'Not found' } });

      const ReportDetailPage = (await import('../../../../../src/app/(app)/report/[id]/page')).default;
      render(<ReportDetailPage />);

      await waitFor(() => {
        expect(screen.getByText('Not found')).toBeInTheDocument();
      });
    });

    it('should show generic error when report is null', async () => {
      mockApiGet.mockResolvedValue({ data: null, error: null });

      const ReportDetailPage = (await import('../../../../../src/app/(app)/report/[id]/page')).default;
      render(<ReportDetailPage />);

      await waitFor(() => {
        // Component shows "Failed to load report" when data is null
        expect(screen.getByText(/Failed to load report|Report not found/)).toBeInTheDocument();
      });
    });

    it('should show Return to chat link on error', async () => {
      mockApiGet.mockResolvedValue({ data: null, error: { message: 'Error' } });

      const ReportDetailPage = (await import('../../../../../src/app/(app)/report/[id]/page')).default;
      render(<ReportDetailPage />);

      await waitFor(() => {
        expect(screen.getByText('Return to chat')).toBeInTheDocument();
      });
    });
  });

  describe('generating state', () => {
    it('should show generating message for pending status', async () => {
      mockApiGet.mockResolvedValue({
        data: { status: 'pending' },
        error: null,
      });

      const ReportDetailPage = (await import('../../../../../src/app/(app)/report/[id]/page')).default;
      render(<ReportDetailPage />);

      await waitFor(() => {
        expect(screen.getByText('Generating Your Report')).toBeInTheDocument();
      });
    });

    it('should show generating message for generating status', async () => {
      mockApiGet.mockResolvedValue({
        data: { status: 'generating' },
        error: null,
      });

      const ReportDetailPage = (await import('../../../../../src/app/(app)/report/[id]/page')).default;
      render(<ReportDetailPage />);

      await waitFor(() => {
        expect(screen.getByText('Generating Your Report')).toBeInTheDocument();
      });
    });

    it('should show status indicator', async () => {
      mockApiGet.mockResolvedValue({
        data: { status: 'generating' },
        error: null,
      });

      const ReportDetailPage = (await import('../../../../../src/app/(app)/report/[id]/page')).default;
      render(<ReportDetailPage />);

      await waitFor(() => {
        expect(screen.getByText('generating')).toBeInTheDocument();
      });
    });
  });

  describe('failed state', () => {
    it('should show failure message', async () => {
      mockApiGet.mockResolvedValue({
        data: { status: 'failed' },
        error: null,
      });

      const ReportDetailPage = (await import('../../../../../src/app/(app)/report/[id]/page')).default;
      render(<ReportDetailPage />);

      await waitFor(() => {
        expect(screen.getByText('Report Generation Failed')).toBeInTheDocument();
      });
    });

    it('should show Try Again button', async () => {
      mockApiGet.mockResolvedValue({
        data: { status: 'failed' },
        error: null,
      });

      const ReportDetailPage = (await import('../../../../../src/app/(app)/report/[id]/page')).default;
      render(<ReportDetailPage />);

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /try again/i })).toBeInTheDocument();
      });
    });
  });

  describe('expired state', () => {
    it('should show expired message', async () => {
      mockApiGet.mockResolvedValue({
        data: { status: 'expired' },
        error: null,
      });

      const ReportDetailPage = (await import('../../../../../src/app/(app)/report/[id]/page')).default;
      render(<ReportDetailPage />);

      await waitFor(() => {
        expect(screen.getByText('Report Expired')).toBeInTheDocument();
      });
    });

    it('should show Generate New Report button', async () => {
      mockApiGet.mockResolvedValue({
        data: { status: 'expired' },
        error: null,
      });

      const ReportDetailPage = (await import('../../../../../src/app/(app)/report/[id]/page')).default;
      render(<ReportDetailPage />);

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /generate new report/i })).toBeInTheDocument();
      });
    });
  });

  describe('completed state', () => {
    const mockCompletedReport = {
      status: 'completed',
      expires_at: '2025-02-01T00:00:00Z',
      content: {
        summary: 'This is the summary',
        query: 'What are the visa requirements?',
        total_citations: 15,
        generated_at: '2025-01-01T00:00:00Z',
        sections: [
          { title: 'Section 1', content: 'Content 1' },
          { title: 'Section 2', content: 'Content 2' },
        ],
      },
    };

    it('should render ExecutiveSummary', async () => {
      mockApiGet.mockResolvedValue({
        data: mockCompletedReport,
        error: null,
      });

      const ReportDetailPage = (await import('../../../../../src/app/(app)/report/[id]/page')).default;
      render(<ReportDetailPage />);

      await waitFor(() => {
        expect(screen.getByTestId('executive-summary')).toBeInTheDocument();
      });
    });

    it('should render report sections', async () => {
      mockApiGet.mockResolvedValue({
        data: mockCompletedReport,
        error: null,
      });

      const ReportDetailPage = (await import('../../../../../src/app/(app)/report/[id]/page')).default;
      render(<ReportDetailPage />);

      await waitFor(() => {
        expect(screen.getByTestId('section-1')).toBeInTheDocument();
        expect(screen.getByTestId('section-2')).toBeInTheDocument();
      });
    });

    it('should show Back to Chat link', async () => {
      mockApiGet.mockResolvedValue({
        data: mockCompletedReport,
        error: null,
      });

      const ReportDetailPage = (await import('../../../../../src/app/(app)/report/[id]/page')).default;
      render(<ReportDetailPage />);

      await waitFor(() => {
        expect(screen.getByText('Back to Chat')).toBeInTheDocument();
      });
    });

    it('should show expiration date', async () => {
      mockApiGet.mockResolvedValue({
        data: mockCompletedReport,
        error: null,
      });

      const ReportDetailPage = (await import('../../../../../src/app/(app)/report/[id]/page')).default;
      render(<ReportDetailPage />);

      await waitFor(() => {
        expect(screen.getByText(/expires/i)).toBeInTheDocument();
      });
    });

    it('should show citation count in footer', async () => {
      mockApiGet.mockResolvedValue({
        data: mockCompletedReport,
        error: null,
      });

      const ReportDetailPage = (await import('../../../../../src/app/(app)/report/[id]/page')).default;
      render(<ReportDetailPage />);

      await waitFor(() => {
        expect(screen.getByText(/15 sources cited/)).toBeInTheDocument();
      });
    });
  });

  describe('completed without content', () => {
    it('should show message when content is not available', async () => {
      mockApiGet.mockResolvedValue({
        data: { status: 'completed', content: null },
        error: null,
      });

      const ReportDetailPage = (await import('../../../../../src/app/(app)/report/[id]/page')).default;
      render(<ReportDetailPage />);

      await waitFor(() => {
        expect(screen.getByText('Report content is not available')).toBeInTheDocument();
      });
    });
  });
});
