/**
 * Tests for reports history page
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import React from 'react';

// Mock next/link
vi.mock('next/link', () => ({
  default: ({ children, href, ...props }: { children: React.ReactNode; href: string }) => (
    <a href={href} {...props}>{children}</a>
  ),
}));

// Mock useReports hook
const mockRefetch = vi.fn();
vi.mock('../../../../src/hooks/useReports', () => ({
  useReports: vi.fn(() => ({
    reports: [],
    isLoading: false,
    error: null,
    refetch: mockRefetch,
  })),
}));

// Mock ReportCard component
vi.mock('../../../../src/components/reports/ReportCard', () => ({
  ReportCard: ({ report }: { report: { id: string; query: string } }) => (
    <div data-testid={`report-card-${report.id}`}>{report.query}</div>
  ),
}));

describe('ReportsPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.resetModules();
  });

  describe('rendering', () => {
    it('should render page heading', async () => {
      const ReportsPage = (await import('../../../../src/app/(app)/reports/page')).default;
      render(<ReportsPage />);

      expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Report History');
    });

    it('should render New Report button', async () => {
      const ReportsPage = (await import('../../../../src/app/(app)/reports/page')).default;
      render(<ReportsPage />);

      const newReportLink = screen.getByRole('link', { name: /new report/i });
      expect(newReportLink).toHaveAttribute('href', '/chat');
    });

    it('should render search input', async () => {
      const ReportsPage = (await import('../../../../src/app/(app)/reports/page')).default;
      render(<ReportsPage />);

      expect(screen.getByPlaceholderText(/search reports/i)).toBeInTheDocument();
    });

    it('should render status filter dropdown', async () => {
      const ReportsPage = (await import('../../../../src/app/(app)/reports/page')).default;
      render(<ReportsPage />);

      expect(screen.getByLabelText(/status/i)).toBeInTheDocument();
    });
  });

  describe('loading state', () => {
    it('should show skeleton loaders when loading', async () => {
      const { useReports } = await import('../../../../src/hooks/useReports');
      (useReports as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        reports: [],
        isLoading: true,
        error: null,
        refetch: mockRefetch,
      });

      const ReportsPage = (await import('../../../../src/app/(app)/reports/page')).default;
      const { container } = render(<ReportsPage />);

      const skeletons = container.querySelectorAll('.animate-pulse');
      expect(skeletons.length).toBeGreaterThan(0);
    });
  });

  describe('empty state', () => {
    it('should show empty state when no reports', async () => {
      const { useReports } = await import('../../../../src/hooks/useReports');
      (useReports as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        reports: [],
        isLoading: false,
        error: null,
        refetch: mockRefetch,
      });

      const ReportsPage = (await import('../../../../src/app/(app)/reports/page')).default;
      render(<ReportsPage />);

      expect(screen.getByText('No reports yet')).toBeInTheDocument();
      expect(screen.getByText(/start a conversation/i)).toBeInTheDocument();
    });

    it('should show Start Chat link in empty state', async () => {
      const { useReports } = await import('../../../../src/hooks/useReports');
      (useReports as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        reports: [],
        isLoading: false,
        error: null,
        refetch: mockRefetch,
      });

      const ReportsPage = (await import('../../../../src/app/(app)/reports/page')).default;
      render(<ReportsPage />);

      expect(screen.getByRole('link', { name: /start chat/i })).toHaveAttribute('href', '/chat');
    });
  });

  describe('error state', () => {
    it('should show error message when error occurs', async () => {
      const { useReports } = await import('../../../../src/hooks/useReports');
      (useReports as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        reports: [],
        isLoading: false,
        error: 'Failed to load reports',
        refetch: mockRefetch,
      });

      const ReportsPage = (await import('../../../../src/app/(app)/reports/page')).default;
      render(<ReportsPage />);

      // There are multiple elements with this text (heading and paragraph)
      const errorElements = screen.getAllByText(/Failed to load reports/);
      expect(errorElements.length).toBeGreaterThan(0);
    });

    it('should show Try again button on error', async () => {
      const { useReports } = await import('../../../../src/hooks/useReports');
      (useReports as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        reports: [],
        isLoading: false,
        error: 'Error',
        refetch: mockRefetch,
      });

      const ReportsPage = (await import('../../../../src/app/(app)/reports/page')).default;
      render(<ReportsPage />);

      const retryButton = screen.getByRole('button', { name: /try again/i });
      fireEvent.click(retryButton);

      expect(mockRefetch).toHaveBeenCalled();
    });
  });

  describe('with reports', () => {
    const mockReports = [
      { id: '1', query: 'UK visa requirements', status: 'completed' },
      { id: '2', query: 'Student visa process', status: 'completed' },
      { id: '3', query: 'Work permit guide', status: 'generating' },
    ];

    it('should render report cards', async () => {
      const { useReports } = await import('../../../../src/hooks/useReports');
      (useReports as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        reports: mockReports,
        isLoading: false,
        error: null,
        refetch: mockRefetch,
      });

      const ReportsPage = (await import('../../../../src/app/(app)/reports/page')).default;
      render(<ReportsPage />);

      expect(screen.getByTestId('report-card-1')).toBeInTheDocument();
      expect(screen.getByTestId('report-card-2')).toBeInTheDocument();
      expect(screen.getByTestId('report-card-3')).toBeInTheDocument();
    });

    it('should show results count', async () => {
      const { useReports } = await import('../../../../src/hooks/useReports');
      (useReports as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        reports: mockReports,
        isLoading: false,
        error: null,
        refetch: mockRefetch,
      });

      const ReportsPage = (await import('../../../../src/app/(app)/reports/page')).default;
      render(<ReportsPage />);

      expect(screen.getByText(/showing 3 of 3 reports/i)).toBeInTheDocument();
    });
  });

  describe('filtering', () => {
    const mockReports = [
      { id: '1', query: 'UK visa requirements', status: 'completed' },
      { id: '2', query: 'Student visa process', status: 'completed' },
      { id: '3', query: 'Work permit guide', status: 'generating' },
    ];

    it('should filter by search query', async () => {
      const { useReports } = await import('../../../../src/hooks/useReports');
      (useReports as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        reports: mockReports,
        isLoading: false,
        error: null,
        refetch: mockRefetch,
      });

      const ReportsPage = (await import('../../../../src/app/(app)/reports/page')).default;
      render(<ReportsPage />);

      const searchInput = screen.getByPlaceholderText(/search reports/i);
      fireEvent.change(searchInput, { target: { value: 'visa' } });

      await waitFor(() => {
        expect(screen.getByText(/showing 2 of 3 reports/i)).toBeInTheDocument();
      });
    });

    it('should filter by status', async () => {
      const { useReports } = await import('../../../../src/hooks/useReports');
      (useReports as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        reports: mockReports,
        isLoading: false,
        error: null,
        refetch: mockRefetch,
      });

      const ReportsPage = (await import('../../../../src/app/(app)/reports/page')).default;
      render(<ReportsPage />);

      const statusSelect = screen.getByLabelText(/status/i);
      fireEvent.change(statusSelect, { target: { value: 'completed' } });

      await waitFor(() => {
        expect(screen.getByText(/showing 2 of 3 reports/i)).toBeInTheDocument();
      });
    });

    it('should show no results message when filter matches nothing', async () => {
      const { useReports } = await import('../../../../src/hooks/useReports');
      (useReports as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        reports: mockReports,
        isLoading: false,
        error: null,
        refetch: mockRefetch,
      });

      const ReportsPage = (await import('../../../../src/app/(app)/reports/page')).default;
      render(<ReportsPage />);

      const searchInput = screen.getByPlaceholderText(/search reports/i);
      fireEvent.change(searchInput, { target: { value: 'nonexistent' } });

      await waitFor(() => {
        expect(screen.getByText('No reports found')).toBeInTheDocument();
      });
    });

    it('should clear filters when Clear filters button clicked', async () => {
      const { useReports } = await import('../../../../src/hooks/useReports');
      (useReports as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        reports: mockReports,
        isLoading: false,
        error: null,
        refetch: mockRefetch,
      });

      const ReportsPage = (await import('../../../../src/app/(app)/reports/page')).default;
      render(<ReportsPage />);

      // Apply filter first
      const searchInput = screen.getByPlaceholderText(/search reports/i);
      fireEvent.change(searchInput, { target: { value: 'nonexistent' } });

      await waitFor(() => {
        expect(screen.getByText('No reports found')).toBeInTheDocument();
      });

      // Clear filters
      const clearButton = screen.getByRole('button', { name: /clear filters/i });
      fireEvent.click(clearButton);

      await waitFor(() => {
        expect(screen.getByText(/showing 3 of 3 reports/i)).toBeInTheDocument();
      });
    });
  });
});
