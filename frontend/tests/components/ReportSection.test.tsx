/**
 * Tests for ReportSection component
 * Tests section rendering, markdown support, and citations
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ReportSection } from '../../src/components/reports/ReportSection';
import type { ReportSection as ReportSectionType } from '@study-abroad/shared';

// Mock ReactMarkdown
vi.mock('react-markdown', () => ({
  default: ({ children }: { children: string }) => <div data-testid="markdown-content">{children}</div>,
}));

// Mock CitationList
vi.mock('../../src/components/reports/CitationList', () => ({
  CitationList: ({ citations }: { citations: any[] }) => (
    <div data-testid="citation-list">Citations: {citations.length}</div>
  ),
}));

describe('ReportSection', () => {
  // AAA: Arrange, Act, Assert

  describe('Basic Rendering', () => {
    it('should render section heading with index', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'University Rankings',
        content: 'Top UK universities include...',
        citations: [],
      };

      // Act
      render(<ReportSection section={section} index={1} />);

      // Assert
      expect(screen.getByText('1.')).toBeInTheDocument();
      expect(screen.getByText('University Rankings')).toBeInTheDocument();
    });

    it('should render section content', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Admission Requirements',
        content: 'You need IELTS 6.5 and good grades.',
        citations: [],
      };

      // Act
      render(<ReportSection section={section} index={2} />);

      // Assert
      expect(screen.getByTestId('markdown-content')).toHaveTextContent('You need IELTS 6.5 and good grades.');
    });

    it('should render as section element', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Test Section',
        content: 'Test content',
        citations: [],
      };

      // Act
      const { container } = render(<ReportSection section={section} index={1} />);

      // Assert
      const sectionElement = container.querySelector('section');
      expect(sectionElement).toBeInTheDocument();
    });
  });

  describe('Index Numbering', () => {
    it('should display index 1 correctly', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Introduction',
        content: 'Content',
        citations: [],
      };

      // Act
      render(<ReportSection section={section} index={1} />);

      // Assert
      expect(screen.getByText('1.')).toBeInTheDocument();
    });

    it('should display index 5 correctly', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Section Five',
        content: 'Content',
        citations: [],
      };

      // Act
      render(<ReportSection section={section} index={5} />);

      // Assert
      expect(screen.getByText('5.')).toBeInTheDocument();
    });

    it('should apply blue color to index number', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Test',
        content: 'Content',
        citations: [],
      };

      // Act
      const { container } = render(<ReportSection section={section} index={1} />);

      // Assert
      const indexElement = container.querySelector('.text-blue-600');
      expect(indexElement).toHaveTextContent('1.');
    });
  });

  describe('Heading Rendering', () => {
    it('should render h2 heading', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Tuition Fees',
        content: 'Content',
        citations: [],
      };

      // Act
      const { container } = render(<ReportSection section={section} index={1} />);

      // Assert
      const heading = container.querySelector('h2');
      expect(heading).toBeInTheDocument();
      expect(heading).toHaveTextContent('Tuition Fees');
    });

    it('should handle long headings', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Complete Guide to Student Visa Application Process for International Students',
        content: 'Content',
        citations: [],
      };

      // Act
      render(<ReportSection section={section} index={1} />);

      // Assert
      expect(screen.getByText(/Complete Guide to Student Visa/)).toBeInTheDocument();
    });

    it('should handle special characters in heading', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Costs & Expenses (£)',
        content: 'Content',
        citations: [],
      };

      // Act
      render(<ReportSection section={section} index={1} />);

      // Assert
      expect(screen.getByText('Costs & Expenses (£)')).toBeInTheDocument();
    });
  });

  describe('Markdown Content', () => {
    it('should render markdown content', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Overview',
        content: '**Bold text** and *italic text*',
        citations: [],
      };

      // Act
      render(<ReportSection section={section} index={1} />);

      // Assert
      expect(screen.getByTestId('markdown-content')).toHaveTextContent('**Bold text** and *italic text*');
    });

    it('should handle multiline markdown', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Details',
        content: 'Line 1\n\nLine 2\n\nLine 3',
        citations: [],
      };

      // Act
      render(<ReportSection section={section} index={1} />);

      // Assert
      // The mock renders content as plain text, newlines become spaces in HTML
      expect(screen.getByTestId('markdown-content')).toHaveTextContent('Line 1 Line 2 Line 3');
    });

    it('should handle markdown lists', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Requirements',
        content: '- Item 1\n- Item 2\n- Item 3',
        citations: [],
      };

      // Act
      render(<ReportSection section={section} index={1} />);

      // Assert
      // The mock renders content as plain text, newlines become spaces in HTML
      expect(screen.getByTestId('markdown-content')).toHaveTextContent('- Item 1 - Item 2 - Item 3');
    });

    it('should handle empty content', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Empty Section',
        content: '',
        citations: [],
      };

      // Act
      render(<ReportSection section={section} index={1} />);

      // Assert
      expect(screen.getByTestId('markdown-content')).toBeInTheDocument();
    });
  });

  describe('Citations Rendering', () => {
    it('should render citations when present', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Universities',
        content: 'Content',
        citations: [
          {
            title: 'Source 1',
            url: 'https://example.com/1',
            accessedAt: new Date(),
          },
          {
            title: 'Source 2',
            url: 'https://example.com/2',
            accessedAt: new Date(),
          },
        ],
      };

      // Act
      render(<ReportSection section={section} index={1} />);

      // Assert
      expect(screen.getByTestId('citation-list')).toBeInTheDocument();
      expect(screen.getByText('Citations: 2')).toBeInTheDocument();
    });

    it('should not render citations when array is empty', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'No Sources',
        content: 'Content',
        citations: [],
      };

      // Act
      render(<ReportSection section={section} index={1} />);

      // Assert
      expect(screen.queryByTestId('citation-list')).not.toBeInTheDocument();
    });

    it('should handle undefined citations gracefully', () => {
      // Arrange
      const section: any = {
        heading: 'Test',
        content: 'Content',
        // citations is undefined
      };

      // Act
      render(<ReportSection section={section} index={1} />);

      // Assert
      expect(screen.queryByTestId('citation-list')).not.toBeInTheDocument();
    });

    it('should render single citation', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Research',
        content: 'Content',
        citations: [
          {
            title: 'Official Guide',
            url: 'https://gov.uk/study',
            accessedAt: new Date(),
          },
        ],
      };

      // Act
      render(<ReportSection section={section} index={1} />);

      // Assert
      expect(screen.getByTestId('citation-list')).toBeInTheDocument();
      expect(screen.getByText('Citations: 1')).toBeInTheDocument();
    });

    it('should render many citations', () => {
      // Arrange
      const citations = Array.from({ length: 10 }, (_, i) => ({
        title: `Source ${i + 1}`,
        url: `https://example.com/${i + 1}`,
        accessedAt: new Date(),
      }));
      const section: ReportSectionType = {
        heading: 'Comprehensive Study',
        content: 'Content',
        citations,
      };

      // Act
      render(<ReportSection section={section} index={1} />);

      // Assert
      expect(screen.getByText('Citations: 10')).toBeInTheDocument();
    });
  });

  describe('Styling', () => {
    it('should apply prose styling to content', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Styled Section',
        content: 'Content',
        citations: [],
      };

      // Act
      const { container } = render(<ReportSection section={section} index={1} />);

      // Assert
      const proseElement = container.querySelector('.prose');
      expect(proseElement).toBeInTheDocument();
      expect(proseElement).toHaveClass('prose-blue');
      expect(proseElement).toHaveClass('max-w-none');
    });

    it('should apply margin to section', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Test',
        content: 'Content',
        citations: [],
      };

      // Act
      const { container } = render(<ReportSection section={section} index={1} />);

      // Assert
      const sectionElement = container.querySelector('section');
      expect(sectionElement).toHaveClass('mb-8');
    });

    it('should apply margin to heading', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Test',
        content: 'Content',
        citations: [],
      };

      // Act
      const { container } = render(<ReportSection section={section} index={1} />);

      // Assert
      const heading = container.querySelector('h2');
      expect(heading).toHaveClass('mb-4');
    });
  });

  describe('Complete Section Structure', () => {
    it('should render complete section with all elements', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Top UK Universities for Computer Science',
        content: '## Rankings\n\n1. Oxford\n2. Cambridge\n3. Imperial College London',
        citations: [
          {
            title: 'QS World Rankings 2025',
            url: 'https://qs.com/rankings',
            snippet: 'Top universities ranked by subject',
            accessedAt: new Date(),
          },
        ],
      };

      // Act
      render(<ReportSection section={section} index={3} />);

      // Assert
      expect(screen.getByText('3.')).toBeInTheDocument();
      expect(screen.getByText('Top UK Universities for Computer Science')).toBeInTheDocument();
      expect(screen.getByTestId('markdown-content')).toBeInTheDocument();
      expect(screen.getByTestId('citation-list')).toBeInTheDocument();
    });

    it('should render multiple sections independently', () => {
      // Arrange
      const section1: ReportSectionType = {
        heading: 'Section 1',
        content: 'Content 1',
        citations: [],
      };
      const section2: ReportSectionType = {
        heading: 'Section 2',
        content: 'Content 2',
        citations: [],
      };

      // Act
      const { rerender } = render(<ReportSection section={section1} index={1} />);
      expect(screen.getByText('Section 1')).toBeInTheDocument();

      rerender(<ReportSection section={section2} index={2} />);
      expect(screen.getByText('Section 2')).toBeInTheDocument();
    });
  });

  describe('Edge Cases', () => {
    it('should handle very long content', () => {
      // Arrange
      const longContent = 'UK universities offer excellent programs. '.repeat(100);
      const section: ReportSectionType = {
        heading: 'Long Content',
        content: longContent,
        citations: [],
      };

      // Act
      render(<ReportSection section={section} index={1} />);

      // Assert
      // Trim to normalize whitespace since mock may render slightly differently
      expect(screen.getByTestId('markdown-content').textContent?.trim()).toBe(longContent.trim());
    });

    it('should handle zero as index', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Introduction',
        content: 'Content',
        citations: [],
      };

      // Act
      render(<ReportSection section={section} index={0} />);

      // Assert
      expect(screen.getByText('0.')).toBeInTheDocument();
    });

    it('should handle large index numbers', () => {
      // Arrange
      const section: ReportSectionType = {
        heading: 'Section 999',
        content: 'Content',
        citations: [],
      };

      // Act
      render(<ReportSection section={section} index={999} />);

      // Assert
      expect(screen.getByText('999.')).toBeInTheDocument();
    });
  });
});
