/**
 * Tests for ReportCard component
 * T118: Display individual report in sidebar/list with status and metadata
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ReportCard } from '@/components/reports/ReportCard';
import type { Report } from '@/types/report';

// Mock next/navigation
const mockPush = vi.fn();
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}));

describe('ReportCard', () => {
  const baseReport: Report = {
    id: 'test-report-123',
    userId: 'user-123',
    query: 'Computer Science in UK',
    country: 'UK',
    subject: 'Computer Science',
    status: 'completed',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    expires_at: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(), // 30 days from now
    content: {
      total_citations: 5,
      sections: {},
    },
    citations: [],
  };

  beforeEach(() => {
    mockPush.mockClear();
  });

  it('renders report query text', () => {
    render(<ReportCard report={baseReport} />);
    expect(screen.getByText('Computer Science in UK')).toBeInTheDocument();
  });

  it('displays completed status badge', () => {
    render(<ReportCard report={baseReport} />);
    expect(screen.getByText('Completed')).toBeInTheDocument();
  });

  it('displays pending status badge', () => {
    const pendingReport = { ...baseReport, status: 'pending' as const };
    render(<ReportCard report={pendingReport} />);
    expect(screen.getByText('Processing')).toBeInTheDocument();
  });

  it('displays generating status badge', () => {
    const generatingReport = { ...baseReport, status: 'generating' as const };
    render(<ReportCard report={generatingReport} />);
    expect(screen.getByText('Generating')).toBeInTheDocument();
  });

  it('displays failed status badge', () => {
    const failedReport = { ...baseReport, status: 'failed' as const };
    render(<ReportCard report={failedReport} />);
    expect(screen.getByText('Failed')).toBeInTheDocument();
  });

  it('displays expired status badge', () => {
    const expiredReport = { ...baseReport, status: 'expired' as const };
    render(<ReportCard report={expiredReport} />);
    expect(screen.getByText('Expired')).toBeInTheDocument();
  });

  it('displays created date', () => {
    render(<ReportCard report={baseReport} />);
    // Should display some time-related text
    expect(screen.getByText(/ago|Yesterday|days ago/i)).toBeInTheDocument();
  });

  it('displays expiry date for non-expired reports', () => {
    render(<ReportCard report={baseReport} />);
    expect(screen.getByText(/Expires/i)).toBeInTheDocument();
  });

  it('does not display expiry date for expired reports', () => {
    const expiredReport = {
      ...baseReport,
      status: 'expired' as const,
      expires_at: new Date(Date.now() - 1000).toISOString(), // Past date
    };
    render(<ReportCard report={expiredReport} />);
    expect(screen.queryByText(/Expires/i)).not.toBeInTheDocument();
  });

  it('displays citation count when not compact', () => {
    render(<ReportCard report={baseReport} compact={false} />);
    expect(screen.getByText('5 sources cited')).toBeInTheDocument();
  });

  it('hides citation count when compact', () => {
    render(<ReportCard report={baseReport} compact={true} />);
    expect(screen.queryByText(/sources cited/i)).not.toBeInTheDocument();
  });

  it('truncates long query text', () => {
    const longReport = {
      ...baseReport,
      query: 'This is a very long query that should be truncated when displayed in the card to maintain a clean UI and prevent overflow issues',
    };
    render(<ReportCard report={longReport} />);
    const displayedText = screen.getByRole('heading', { level: 3 }).textContent;
    expect(displayedText).toContain('...');
    expect(displayedText!.length).toBeLessThan(longReport.query.length);
  });

  it('navigates to report detail on click', () => {
    render(<ReportCard report={baseReport} />);
    const card = screen.getByRole('button');
    fireEvent.click(card);
    expect(mockPush).toHaveBeenCalledWith(`/report/${baseReport.id}`);
  });

  it('navigates to report detail on Enter key press', () => {
    render(<ReportCard report={baseReport} />);
    const card = screen.getByRole('button');
    fireEvent.keyDown(card, { key: 'Enter' });
    expect(mockPush).toHaveBeenCalledWith(`/report/${baseReport.id}`);
  });

  it('navigates to report detail on Space key press', () => {
    render(<ReportCard report={baseReport} />);
    const card = screen.getByRole('button');
    fireEvent.keyDown(card, { key: ' ' });
    expect(mockPush).toHaveBeenCalledWith(`/report/${baseReport.id}`);
  });

  it('does not navigate on other key press', () => {
    render(<ReportCard report={baseReport} />);
    const card = screen.getByRole('button');
    fireEvent.keyDown(card, { key: 'a' });
    expect(mockPush).not.toHaveBeenCalled();
  });

  it('is keyboard accessible with tabindex', () => {
    render(<ReportCard report={baseReport} />);
    const card = screen.getByRole('button');
    expect(card).toHaveAttribute('tabIndex', '0');
  });

  it('applies compact styling when compact prop is true', () => {
    const { container } = render(<ReportCard report={baseReport} compact={true} />);
    const card = container.querySelector('.space-y-2');
    expect(card).toBeInTheDocument();
  });

  it('applies regular styling when compact prop is false', () => {
    const { container } = render(<ReportCard report={baseReport} compact={false} />);
    const card = container.querySelector('.space-y-3');
    expect(card).toBeInTheDocument();
  });

  it('shows correct date formatting for recent reports', () => {
    const recentReport = {
      ...baseReport,
      createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(), // 2 hours ago
    };
    render(<ReportCard report={recentReport} />);
    expect(screen.getByText(/hour/i)).toBeInTheDocument();
  });

  it('shows correct date formatting for yesterday', () => {
    const yesterdayReport = {
      ...baseReport,
      createdAt: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), // 1 day ago
    };
    render(<ReportCard report={yesterdayReport} />);
    expect(screen.getByText('Yesterday')).toBeInTheDocument();
  });
});
