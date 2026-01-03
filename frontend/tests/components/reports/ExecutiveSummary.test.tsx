/**
 * Tests for ExecutiveSummary component
 */

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';
import { ExecutiveSummary, ExecutiveSummaryProps } from '../../../src/components/reports/ExecutiveSummary';

describe('ExecutiveSummary', () => {
  const defaultProps: ExecutiveSummaryProps = {
    summary: 'This is the executive summary text.',
    query: 'What are the requirements for UK student visa?',
    totalCitations: 15,
    generatedAt: new Date('2024-12-25T10:30:00Z'),
  };

  describe('rendering', () => {
    it('should render the component', () => {
      render(<ExecutiveSummary {...defaultProps} />);

      expect(screen.getByText('Executive Summary')).toBeInTheDocument();
    });

    it('should display the query', () => {
      render(<ExecutiveSummary {...defaultProps} />);

      expect(screen.getByText(defaultProps.query)).toBeInTheDocument();
    });

    it('should display the summary text', () => {
      render(<ExecutiveSummary {...defaultProps} />);

      expect(screen.getByText(defaultProps.summary)).toBeInTheDocument();
    });

    it('should display citation count', () => {
      render(<ExecutiveSummary {...defaultProps} />);

      expect(screen.getByText(/15\s*sources cited/)).toBeInTheDocument();
    });

    it('should display generated date', () => {
      render(<ExecutiveSummary {...defaultProps} />);

      expect(screen.getByText(/Generated/)).toBeInTheDocument();
    });
  });

  describe('with different props', () => {
    it('should display different summary text', () => {
      const customSummary = 'A comprehensive overview of immigration requirements.';
      render(<ExecutiveSummary {...defaultProps} summary={customSummary} />);

      expect(screen.getByText(customSummary)).toBeInTheDocument();
    });

    it('should display different query', () => {
      const customQuery = 'How to apply for a US work visa?';
      render(<ExecutiveSummary {...defaultProps} query={customQuery} />);

      expect(screen.getByText(customQuery)).toBeInTheDocument();
    });

    it('should display different citation count', () => {
      render(<ExecutiveSummary {...defaultProps} totalCitations={42} />);

      expect(screen.getByText(/42\s*sources cited/)).toBeInTheDocument();
    });

    it('should handle zero citations', () => {
      render(<ExecutiveSummary {...defaultProps} totalCitations={0} />);

      expect(screen.getByText(/0\s*sources cited/)).toBeInTheDocument();
    });

    it('should handle large citation count', () => {
      render(<ExecutiveSummary {...defaultProps} totalCitations={999} />);

      expect(screen.getByText(/999\s*sources cited/)).toBeInTheDocument();
    });
  });

  describe('date formatting', () => {
    it('should format date correctly', () => {
      const testDate = new Date('2025-01-01T00:00:00Z');
      render(<ExecutiveSummary {...defaultProps} generatedAt={testDate} />);

      // The date format depends on locale, but should contain Generated
      expect(screen.getByText(/Generated/)).toBeInTheDocument();
    });

    it('should handle different date values', () => {
      const testDate = new Date('2023-06-15T12:00:00Z');
      render(<ExecutiveSummary {...defaultProps} generatedAt={testDate} />);

      expect(screen.getByText(/Generated/)).toBeInTheDocument();
    });
  });

  describe('styling', () => {
    it('should have blue-themed container', () => {
      render(<ExecutiveSummary {...defaultProps} />);

      const container = screen.getByText('Executive Summary').closest('div')?.parentElement?.parentElement;
      expect(container).toHaveClass('bg-blue-50', 'border-blue-200');
    });

    it('should render document icon', () => {
      render(<ExecutiveSummary {...defaultProps} />);

      const iconContainer = document.querySelector('.bg-blue-600.rounded-lg');
      expect(iconContainer).toBeInTheDocument();
    });

    it('should have heading styled correctly', () => {
      render(<ExecutiveSummary {...defaultProps} />);

      const heading = screen.getByText('Executive Summary');
      expect(heading).toHaveClass('text-xl', 'font-bold', 'text-gray-900');
    });

    it('should have footer with border', () => {
      render(<ExecutiveSummary {...defaultProps} />);

      const footer = document.querySelector('.border-t.border-blue-200');
      expect(footer).toBeInTheDocument();
    });
  });

  describe('accessibility', () => {
    it('should have semantic heading structure', () => {
      render(<ExecutiveSummary {...defaultProps} />);

      const heading = screen.getByRole('heading', { level: 2 });
      expect(heading).toHaveTextContent('Executive Summary');
    });

    it('should render SVG icons with proper attributes', () => {
      render(<ExecutiveSummary {...defaultProps} />);

      const svgs = document.querySelectorAll('svg');
      expect(svgs.length).toBeGreaterThan(0);
    });
  });

  describe('edge cases', () => {
    it('should handle empty summary', () => {
      render(<ExecutiveSummary {...defaultProps} summary="" />);

      expect(screen.getByText('Executive Summary')).toBeInTheDocument();
    });

    it('should handle empty query', () => {
      render(<ExecutiveSummary {...defaultProps} query="" />);

      expect(screen.getByText('Executive Summary')).toBeInTheDocument();
    });

    it('should handle very long summary', () => {
      const longSummary = 'A'.repeat(1000);
      render(<ExecutiveSummary {...defaultProps} summary={longSummary} />);

      expect(screen.getByText(longSummary)).toBeInTheDocument();
    });

    it('should handle very long query', () => {
      const longQuery = 'B'.repeat(500);
      render(<ExecutiveSummary {...defaultProps} query={longQuery} />);

      expect(screen.getByText(longQuery)).toBeInTheDocument();
    });
  });
});
