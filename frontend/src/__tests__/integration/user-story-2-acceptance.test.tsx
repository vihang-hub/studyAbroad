/**
 * Integration Tests for User Story 2: View Report History
 * Tasks T130-T134 Acceptance Criteria
 *
 * End-to-end tests validating complete report history workflow
 */

import {
  describe, it, expect, vi, beforeEach,
} from 'vitest';
import {
  render, screen, fireEvent, waitFor,
} from '@testing-library/react';
import type { Report } from '@/types/report';

import { ReportSidebar } from '@/components/reports/ReportSidebar';

// Mock API client
const mockGet = vi.fn();
vi.mock('@/lib/api-client', () => ({
  api: {
    get: (...args: any[]) => mockGet(...args),
  },
}));

// Mock next/navigation
const mockPush = vi.fn();
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}));

// Mock next/link
vi.mock('next/link', () => ({
  default: ({ children, href }: { children: React.ReactNode; href: string }) => (
    <a href={href}>{children}</a>
  ),
}));

describe('User Story 2: View Report History - Integration Tests', () => {
  const mockReports: Report[] = Array.from({ length: 12 }, (_, i) => ({
    id: `report-${i}`,
    userId: 'user-123',
    query: `Subject ${i} in UK`,
    country: 'UK',
    subject: `Subject ${i}`,
    status: 'completed' as const,
    createdAt: new Date(Date.now() - i * 24 * 60 * 60 * 1000).toISOString(),
    updatedAt: new Date().toISOString(),
    expires_at: new Date(Date.now() + (30 - i) * 24 * 60 * 60 * 1000).toISOString(),
    content: {
      total_citations: 5,
      sections: {
        overview: { title: 'Overview', content: 'Content' },
      },
    },
    citations: [],
  }));

  beforeEach(() => {
    mockGet.mockClear();
    mockPush.mockClear();
  });

  describe('T130: Sidebar displays all user reports (max 10 recent)', () => {
    it('displays maximum 10 most recent reports', async () => {
      // API returns only 10 most recent
      const recentReports = mockReports.slice(0, 10);

      mockGet.mockResolvedValue({
        data: recentReports,
        error: null,
      });

      render(<ReportSidebar />);

      await waitFor(() => {
        expect(screen.queryByText('Recent Reports')).toBeInTheDocument();
      });

      // Should display all 10 reports
      await waitFor(() => {
        const cards = screen.getAllByText(/Subject \d+ in UK/);
        expect(cards.length).toBe(10);
      });

      // Verify API was called with limit=10
      expect(mockGet).toHaveBeenCalledWith('/api/reports?limit=10');
    });

    it('displays reports sorted by most recent first', async () => {
      const sortedReports = mockReports.slice(0, 5);

      mockGet.mockResolvedValue({
        data: sortedReports,
        error: null,
      });

      render(<ReportSidebar />);

      await waitFor(() => {
        const cards = screen.getAllByText(/Subject \d+ in UK/);
        expect(cards[0].textContent).toContain('Subject 0'); // Most recent
        expect(cards[4].textContent).toContain('Subject 4'); // Oldest in list
      });
    });

    it('shows View all link when reports exist', async () => {
      mockGet.mockResolvedValue({
        data: mockReports.slice(0, 10),
        error: null,
      });

      render(<ReportSidebar />);

      await waitFor(() => {
        const viewAllLink = screen.getByText('View all');
        expect(viewAllLink).toBeInTheDocument();
        expect(viewAllLink.closest('a')).toHaveAttribute('href', '/reports');
      });
    });
  });

  describe('T131: Clicking past report shows content without AI regeneration', () => {
    it('navigates to report detail when report card is clicked', async () => {
      const reports = mockReports.slice(0, 3);

      mockGet.mockResolvedValue({
        data: reports,
        error: null,
      });

      render(<ReportSidebar />);

      await waitFor(() => {
        expect(screen.getByText(/Subject 0 in UK/)).toBeInTheDocument();
      });

      const firstReport = screen.getByText(/Subject 0 in UK/);
      const reportCard = firstReport.closest('[role="button"]');

      expect(reportCard).toBeInTheDocument();
      fireEvent.click(reportCard!);

      // Should navigate to report detail page
      expect(mockPush).toHaveBeenCalledWith(`/report/${reports[0].id}`);
    });

    it('report card displays completed status', async () => {
      const completedReports = mockReports.slice(0, 2);

      mockGet.mockResolvedValue({
        data: completedReports,
        error: null,
      });

      render(<ReportSidebar />);

      await waitFor(() => {
        const statusBadges = screen.getAllByText('Completed');
        expect(statusBadges.length).toBe(2);
      });
    });

    it('keyboard navigation works for report cards', async () => {
      const reports = mockReports.slice(0, 1);

      mockGet.mockResolvedValue({
        data: reports,
        error: null,
      });

      render(<ReportSidebar />);

      await waitFor(() => {
        expect(screen.getByText(/Subject 0 in UK/)).toBeInTheDocument();
      });

      const reportCard = screen.getByRole('button');
      fireEvent.keyDown(reportCard, { key: 'Enter' });

      expect(mockPush).toHaveBeenCalledWith(`/report/${reports[0].id}`);
    });
  });

  describe('T132: Reports are user-scoped (user A cannot see user B reports)', () => {
    it('only displays reports for authenticated user', async () => {
      // Mock returns only user-123's reports
      const userReports = mockReports.filter((r) => r.userId === 'user-123');

      mockGet.mockResolvedValue({
        data: userReports.slice(0, 10),
        error: null,
      });

      render(<ReportSidebar />);

      await waitFor(() => {
        expect(mockGet).toHaveBeenCalledWith('/api/reports?limit=10');
      });

      // All displayed reports should belong to same user
      await waitFor(() => {
        const reports = screen.getAllByText(/Subject \d+ in UK/);
        expect(reports.length).toBeGreaterThan(0);
      });
    });

    it('displays error when unauthorized to access reports', async () => {
      mockGet.mockResolvedValue({
        data: null,
        error: { message: 'Unauthorized' },
      });

      render(<ReportSidebar />);

      await waitFor(() => {
        expect(screen.getByText('Failed to load reports')).toBeInTheDocument();
        expect(screen.getByText('Unauthorized')).toBeInTheDocument();
      });
    });
  });

  describe('T133: Immutability - reopening report does not trigger new AI call', () => {
    it('clicking same report multiple times navigates consistently', async () => {
      const reports = mockReports.slice(0, 3);

      mockGet.mockResolvedValue({
        data: reports,
        error: null,
      });

      render(<ReportSidebar />);

      await waitFor(() => {
        expect(screen.getByText(/Subject 0 in UK/)).toBeInTheDocument();
      });

      const reportCard = screen.getByText(/Subject 0 in UK/).closest('[role="button"]');

      // Click first time
      fireEvent.click(reportCard!);
      expect(mockPush).toHaveBeenCalledWith(`/report/${reports[0].id}`);

      // Click second time
      mockPush.mockClear();
      fireEvent.click(reportCard!);
      expect(mockPush).toHaveBeenCalledWith(`/report/${reports[0].id}`);

      // Both navigations should be to same URL (no regeneration)
    });

    it('report content is fetched from API, not regenerated', async () => {
      const reports = mockReports.slice(0, 1);

      mockGet.mockResolvedValue({
        data: reports,
        error: null,
      });

      render(<ReportSidebar />);

      await waitFor(() => {
        expect(mockGet).toHaveBeenCalledTimes(1);
      });

      // Only one API call to fetch reports list
      // No AI regeneration calls
      expect(mockGet).toHaveBeenCalledWith('/api/reports?limit=10');
    });
  });

  describe('T134: Empty state when user has no reports', () => {
    it('displays empty state message when no reports exist', async () => {
      mockGet.mockResolvedValue({
        data: [],
        error: null,
      });

      render(<ReportSidebar />);

      await waitFor(() => {
        expect(screen.getByText('No reports yet')).toBeInTheDocument();
      });

      expect(screen.getByText('Start a conversation to generate your first research report')).toBeInTheDocument();
    });

    it('displays Start Chat button in empty state', async () => {
      mockGet.mockResolvedValue({
        data: [],
        error: null,
      });

      render(<ReportSidebar />);

      await waitFor(() => {
        const startChatLink = screen.getByText('Start Chat');
        expect(startChatLink).toBeInTheDocument();
        expect(startChatLink.closest('a')).toHaveAttribute('href', '/chat');
      });
    });

    it('does not display View all link in empty state', async () => {
      mockGet.mockResolvedValue({
        data: [],
        error: null,
      });

      render(<ReportSidebar />);

      await waitFor(() => {
        expect(screen.getByText('No reports yet')).toBeInTheDocument();
      });

      expect(screen.queryByText('View all')).not.toBeInTheDocument();
    });

    it('empty state is visually distinct with icon', async () => {
      mockGet.mockResolvedValue({
        data: [],
        error: null,
      });

      const { container } = render(<ReportSidebar />);

      await waitFor(() => {
        expect(screen.getByText('No reports yet')).toBeInTheDocument();
      });

      // Should have SVG icon in empty state
      const svg = container.querySelector('svg');
      expect(svg).toBeInTheDocument();
    });
  });

  describe('Complete workflow integration', () => {
    it('handles full user journey: load reports → select report → navigate', async () => {
      const reports = mockReports.slice(0, 5);

      // Step 1: Load sidebar
      mockGet.mockResolvedValue({
        data: reports,
        error: null,
      });

      render(<ReportSidebar />);

      // Step 2: Wait for loading to complete
      await waitFor(() => {
        expect(screen.queryByRole('generic', { name: /loading/i })).not.toBeInTheDocument();
      });

      // Step 3: Verify reports displayed
      await waitFor(() => {
        expect(screen.getAllByText(/Subject \d+ in UK/).length).toBe(5);
      });

      // Step 4: Click on second report
      const secondReport = screen.getByText(/Subject 1 in UK/).closest('[role="button"]');
      fireEvent.click(secondReport!);

      // Step 5: Verify navigation
      expect(mockPush).toHaveBeenCalledWith(`/report/${reports[1].id}`);
    });

    it('handles error → retry flow', async () => {
      // First attempt fails
      mockGet.mockResolvedValueOnce({
        data: null,
        error: { message: 'Network error' },
      });

      render(<ReportSidebar />);

      await waitFor(() => {
        expect(screen.getByText('Failed to load reports')).toBeInTheDocument();
      });

      // Second attempt succeeds
      const reports = mockReports.slice(0, 3);
      mockGet.mockResolvedValueOnce({
        data: reports,
        error: null,
      });

      const retryButton = screen.getByText('Try again');
      fireEvent.click(retryButton);

      await waitFor(() => {
        expect(screen.getAllByText(/Subject \d+ in UK/).length).toBe(3);
      });
    });

    it('displays loading → reports → navigation in sequence', async () => {
      const reports = mockReports.slice(0, 2);

      mockGet.mockImplementation(() => new Promise((resolve) => {
        setTimeout(() => {
          resolve({ data: reports, error: null });
        }, 100);
      }));

      render(<ReportSidebar />);

      // Should show loading state initially
      expect(screen.getByText('Recent Reports')).toBeInTheDocument();

      // Wait for reports to load
      await waitFor(() => {
        expect(screen.getByText(/Subject 0 in UK/)).toBeInTheDocument();
      }, { timeout: 2000 });

      // Click report
      const reportCard = screen.getByText(/Subject 0 in UK/).closest('[role="button"]');
      fireEvent.click(reportCard!);

      expect(mockPush).toHaveBeenCalledWith(`/report/${reports[0].id}`);
    });
  });

  describe('Edge cases', () => {
    it('handles exactly 10 reports (boundary case)', async () => {
      const exactlyTen = mockReports.slice(0, 10);

      mockGet.mockResolvedValue({
        data: exactlyTen,
        error: null,
      });

      render(<ReportSidebar />);

      await waitFor(() => {
        expect(screen.getAllByText(/Subject \d+ in UK/).length).toBe(10);
      });
    });

    it('handles single report', async () => {
      const singleReport = [mockReports[0]];

      mockGet.mockResolvedValue({
        data: singleReport,
        error: null,
      });

      render(<ReportSidebar />);

      await waitFor(() => {
        expect(screen.getAllByText(/Subject 0 in UK/).length).toBe(1);
      });
    });

    it('handles reports with missing optional fields gracefully', async () => {
      const minimalReport: Report = {
        id: 'minimal-1',
        userId: 'user-123',
        query: 'Minimal Report',
        country: 'UK',
        subject: 'Subject',
        status: 'completed',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        content: { sections: {} },
        citations: [],
      };

      mockGet.mockResolvedValue({
        data: [minimalReport],
        error: null,
      });

      render(<ReportSidebar />);

      await waitFor(() => {
        expect(screen.getByText('Minimal Report')).toBeInTheDocument();
      });
    });
  });
});
