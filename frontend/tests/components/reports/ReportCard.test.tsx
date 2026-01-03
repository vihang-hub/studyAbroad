/**
 * Tests for ReportCard component
 * Tests status badges, date formatting, truncation, navigation, and accessibility
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import React from 'react';
import { ReportCard } from '../../../src/components/reports/ReportCard';
import type { Report } from '../../../src/types/report';

// Mock next/navigation
const mockPush = vi.fn();
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}));

const baseReport: Report = {
  id: 'test-123',
  user_id: 'user-1',
  query: 'UK visa requirements for students',
  status: 'completed',
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
};

describe('ReportCard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Fix the current time for date testing
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2025-01-03T12:00:00Z'));
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  describe('status badges', () => {
    it('should show "Completed" badge with green styling for completed status', () => {
      render(<ReportCard report={{ ...baseReport, status: 'completed' }} />);

      const badge = screen.getByText('Completed');
      expect(badge).toBeInTheDocument();
      expect(badge).toHaveClass('bg-green-100', 'text-green-800');
    });

    it('should show "Processing" badge with blue styling for pending status', () => {
      render(<ReportCard report={{ ...baseReport, status: 'pending' }} />);

      const badge = screen.getByText('Processing');
      expect(badge).toBeInTheDocument();
      expect(badge).toHaveClass('bg-blue-100', 'text-blue-800');
    });

    it('should show "Processing" badge with blue styling for processing status', () => {
      render(<ReportCard report={{ ...baseReport, status: 'processing' }} />);

      const badge = screen.getByText('Processing');
      expect(badge).toBeInTheDocument();
      expect(badge).toHaveClass('bg-blue-100', 'text-blue-800');
    });

    it('should show "Generating" badge with yellow styling for generating status', () => {
      render(<ReportCard report={{ ...baseReport, status: 'generating' }} />);

      const badge = screen.getByText('Generating');
      expect(badge).toBeInTheDocument();
      expect(badge).toHaveClass('bg-yellow-100', 'text-yellow-800');
    });

    it('should show "Failed" badge with red styling for failed status', () => {
      render(<ReportCard report={{ ...baseReport, status: 'failed' }} />);

      const badge = screen.getByText('Failed');
      expect(badge).toBeInTheDocument();
      expect(badge).toHaveClass('bg-red-100', 'text-red-800');
    });

    it('should show "Expired" badge with gray styling for expired status', () => {
      render(<ReportCard report={{ ...baseReport, status: 'expired' }} />);

      const badge = screen.getByText('Expired');
      expect(badge).toBeInTheDocument();
      expect(badge).toHaveClass('bg-gray-100', 'text-gray-800');
    });

    it('should show "Unknown" badge for unknown status', () => {
      render(<ReportCard report={{ ...baseReport, status: 'unknown' as any }} />);

      const badge = screen.getByText('Unknown');
      expect(badge).toBeInTheDocument();
      expect(badge).toHaveClass('bg-gray-100', 'text-gray-800');
    });
  });

  describe('date formatting', () => {
    it('should show "X mins ago" for recent dates', () => {
      const fifteenMinsAgo = new Date('2025-01-03T11:45:00Z').toISOString();
      render(<ReportCard report={{ ...baseReport, createdAt: fifteenMinsAgo }} />);

      expect(screen.getByText('15 mins ago')).toBeInTheDocument();
    });

    it('should show "1 min ago" for singular minute', () => {
      const oneMinsAgo = new Date('2025-01-03T11:59:00Z').toISOString();
      render(<ReportCard report={{ ...baseReport, createdAt: oneMinsAgo }} />);

      expect(screen.getByText('1 min ago')).toBeInTheDocument();
    });

    it('should show "X hours ago" for same-day dates', () => {
      const threeHoursAgo = new Date('2025-01-03T09:00:00Z').toISOString();
      render(<ReportCard report={{ ...baseReport, createdAt: threeHoursAgo }} />);

      expect(screen.getByText('3 hours ago')).toBeInTheDocument();
    });

    it('should show "1 hour ago" for singular hour', () => {
      const oneHourAgo = new Date('2025-01-03T11:00:00Z').toISOString();
      render(<ReportCard report={{ ...baseReport, createdAt: oneHourAgo }} />);

      expect(screen.getByText('1 hour ago')).toBeInTheDocument();
    });

    it('should show "Yesterday" for yesterday', () => {
      const yesterday = new Date('2025-01-02T12:00:00Z').toISOString();
      render(<ReportCard report={{ ...baseReport, createdAt: yesterday }} />);

      expect(screen.getByText('Yesterday')).toBeInTheDocument();
    });

    it('should show "X days ago" for dates within a week', () => {
      const threeDaysAgo = new Date('2024-12-31T12:00:00Z').toISOString();
      render(<ReportCard report={{ ...baseReport, createdAt: threeDaysAgo }} />);

      expect(screen.getByText('3 days ago')).toBeInTheDocument();
    });

    it('should show formatted date for older dates in same year', () => {
      const twoWeeksAgo = new Date('2024-12-20T12:00:00Z').toISOString();
      render(<ReportCard report={{ ...baseReport, createdAt: twoWeeksAgo }} />);

      // Should show date in short format, locale-dependent
      expect(screen.getByText(/Dec 20/i)).toBeInTheDocument();
    });

    it('should show formatted date with year for different year', () => {
      const lastYear = new Date('2023-06-15T12:00:00Z').toISOString();
      render(<ReportCard report={{ ...baseReport, createdAt: lastYear }} />);

      // Should include the year since it's different (locale-dependent format)
      expect(screen.getByText(/Jun.*2023|2023.*Jun/i)).toBeInTheDocument();
    });
  });

  describe('query truncation', () => {
    it('should not truncate short queries', () => {
      const shortQuery = 'Short query';
      render(<ReportCard report={{ ...baseReport, query: shortQuery }} />);

      expect(screen.getByText(shortQuery)).toBeInTheDocument();
    });

    it('should truncate long queries with ellipsis in normal mode', () => {
      const longQuery = 'This is a very long query that should definitely be truncated because it exceeds the maximum allowed length for display purposes';
      render(<ReportCard report={{ ...baseReport, query: longQuery }} />);

      // Should truncate at 80 chars in normal mode
      const heading = screen.getByRole('heading', { level: 3 });
      expect(heading.textContent).toContain('...');
      expect(heading.textContent?.length).toBeLessThan(longQuery.length);
    });

    it('should truncate at 50 chars in compact mode', () => {
      const longQuery = 'This is a medium length query that exceeds fifty characters';
      render(<ReportCard report={{ ...baseReport, query: longQuery }} compact />);

      const heading = screen.getByRole('heading', { level: 3 });
      // 50 chars + '...' = 53 max
      expect(heading.textContent?.length).toBeLessThanOrEqual(53);
      expect(heading.textContent).toContain('...');
    });

    it('should show full query in title attribute', () => {
      const longQuery = 'This is a very long query that should be truncated';
      render(<ReportCard report={{ ...baseReport, query: longQuery }} />);

      const heading = screen.getByRole('heading', { level: 3 });
      expect(heading).toHaveAttribute('title', longQuery);
    });
  });

  describe('navigation', () => {
    it('should navigate to report on click', () => {
      render(<ReportCard report={baseReport} />);

      const card = screen.getByRole('button');
      fireEvent.click(card);

      expect(mockPush).toHaveBeenCalledWith('/report/test-123');
    });

    it('should navigate to report on Enter key', () => {
      render(<ReportCard report={baseReport} />);

      const card = screen.getByRole('button');
      fireEvent.keyDown(card, { key: 'Enter' });

      expect(mockPush).toHaveBeenCalledWith('/report/test-123');
    });

    it('should navigate to report on Space key', () => {
      render(<ReportCard report={baseReport} />);

      const card = screen.getByRole('button');
      fireEvent.keyDown(card, { key: ' ' });

      expect(mockPush).toHaveBeenCalledWith('/report/test-123');
    });

    it('should not navigate on other key presses', () => {
      render(<ReportCard report={baseReport} />);

      const card = screen.getByRole('button');
      fireEvent.keyDown(card, { key: 'Tab' });

      expect(mockPush).not.toHaveBeenCalled();
    });
  });

  describe('compact mode', () => {
    it('should apply compact spacing in compact mode', () => {
      const { container } = render(<ReportCard report={baseReport} compact />);

      const card = container.firstChild;
      expect(card).toHaveClass('space-y-2');
    });

    it('should apply normal spacing in default mode', () => {
      const { container } = render(<ReportCard report={baseReport} />);

      const card = container.firstChild;
      expect(card).toHaveClass('space-y-3');
    });

    it('should apply smaller text in compact mode', () => {
      render(<ReportCard report={baseReport} compact />);

      const heading = screen.getByRole('heading', { level: 3 });
      expect(heading).toHaveClass('text-sm');
    });

    it('should apply normal text in default mode', () => {
      render(<ReportCard report={baseReport} />);

      const heading = screen.getByRole('heading', { level: 3 });
      expect(heading).toHaveClass('text-base');
    });
  });

  describe('expiration display', () => {
    it('should show expiration date when expires_at is set and not expired', () => {
      const expiresAt = new Date('2025-01-10T12:00:00Z').toISOString();
      render(<ReportCard report={{ ...baseReport, expires_at: expiresAt, status: 'completed' }} />);

      expect(screen.getByText(/Expires/)).toBeInTheDocument();
    });

    it('should not show expiration for expired reports', () => {
      const expiresAt = new Date('2025-01-10T12:00:00Z').toISOString();
      render(<ReportCard report={{ ...baseReport, expires_at: expiresAt, status: 'expired' }} />);

      expect(screen.queryByText(/Expires/)).not.toBeInTheDocument();
    });

    it('should not show expiration when expires_at is not set', () => {
      render(<ReportCard report={{ ...baseReport }} />);

      expect(screen.queryByText(/Expires/)).not.toBeInTheDocument();
    });

    it('should show expiration with orange text color', () => {
      const expiresAt = new Date('2025-01-10T12:00:00Z').toISOString();
      render(<ReportCard report={{ ...baseReport, expires_at: expiresAt, status: 'completed' }} />);

      const expiresText = screen.getByText(/Expires/).closest('div');
      expect(expiresText).toHaveClass('text-orange-600');
    });
  });

  describe('citations display', () => {
    it('should show citation count in normal mode when content has citations', () => {
      const reportWithCitations = {
        ...baseReport,
        content: {
          total_citations: 12,
          sections: [],
          executive_summary: '',
        },
      };
      render(<ReportCard report={reportWithCitations} />);

      // The text "12 sources cited" is in a single span
      expect(screen.getByText(/12\s+sources cited/)).toBeInTheDocument();
    });

    it('should not show citations in compact mode', () => {
      const reportWithCitations = {
        ...baseReport,
        content: {
          total_citations: 12,
          sections: [],
          executive_summary: '',
        },
      };
      render(<ReportCard report={reportWithCitations} compact />);

      expect(screen.queryByText('sources cited')).not.toBeInTheDocument();
    });

    it('should not show citations when content is missing', () => {
      render(<ReportCard report={baseReport} />);

      expect(screen.queryByText('sources cited')).not.toBeInTheDocument();
    });

    it('should not show citations when total_citations is 0', () => {
      const reportWithZeroCitations = {
        ...baseReport,
        content: {
          total_citations: 0,
          sections: [],
          executive_summary: '',
        },
      };
      render(<ReportCard report={reportWithZeroCitations} />);

      expect(screen.queryByText('sources cited')).not.toBeInTheDocument();
    });
  });

  describe('accessibility', () => {
    it('should have role="button"', () => {
      render(<ReportCard report={baseReport} />);

      expect(screen.getByRole('button')).toBeInTheDocument();
    });

    it('should have tabIndex=0 for keyboard navigation', () => {
      render(<ReportCard report={baseReport} />);

      const card = screen.getByRole('button');
      expect(card).toHaveAttribute('tabindex', '0');
    });

    it('should have cursor-pointer class', () => {
      const { container } = render(<ReportCard report={baseReport} />);

      const card = container.firstChild;
      expect(card).toHaveClass('cursor-pointer');
    });
  });

  describe('styling', () => {
    it('should have hover effect classes', () => {
      const { container } = render(<ReportCard report={baseReport} />);

      const card = container.firstChild;
      expect(card).toHaveClass('hover:border-blue-400', 'hover:shadow-md');
    });

    it('should have transition classes', () => {
      const { container } = render(<ReportCard report={baseReport} />);

      const card = container.firstChild;
      expect(card).toHaveClass('transition-all', 'duration-200');
    });

    it('should have base styling classes', () => {
      const { container } = render(<ReportCard report={baseReport} />);

      const card = container.firstChild;
      expect(card).toHaveClass('rounded-lg', 'border', 'border-gray-200', 'bg-white', 'p-4');
    });
  });
});
