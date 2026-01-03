/**
 * Tests for CitationList component
 * Tests citation rendering, links, and formatting
 */

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { CitationList } from '../../src/components/reports/CitationList';
import type { Citation } from '@study-abroad/shared';

describe('CitationList', () => {
  // AAA: Arrange, Act, Assert

  describe('Empty State', () => {
    it('should return null when citations array is empty', () => {
      // Arrange
      const citations: Citation[] = [];

      // Act
      const { container } = render(<CitationList citations={citations} />);

      // Assert
      expect(container.firstChild).toBeNull();
    });

    it('should return null when citations is undefined', () => {
      // Arrange & Act
      const { container } = render(<CitationList citations={undefined as any} />);

      // Assert
      expect(container.firstChild).toBeNull();
    });

    it('should return null when citations is null', () => {
      // Arrange & Act
      const { container } = render(<CitationList citations={null as any} />);

      // Assert
      expect(container.firstChild).toBeNull();
    });
  });

  describe('Single Citation Rendering', () => {
    it('should render single citation with title and URL', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'UK Government Student Visa Guide',
          url: 'https://www.gov.uk/student-visa',
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      expect(screen.getByText('Sources')).toBeInTheDocument();
      expect(screen.getByText('UK Government Student Visa Guide')).toBeInTheDocument();
      expect(screen.getByText('https://www.gov.uk/student-visa')).toBeInTheDocument();
    });

    it('should render citation as a link', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'Test Source',
          url: 'https://example.com',
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      const link = screen.getByRole('link', { name: /Test Source/i });
      expect(link).toHaveAttribute('href', 'https://example.com');
      expect(link).toHaveAttribute('target', '_blank');
      expect(link).toHaveAttribute('rel', 'noopener noreferrer');
    });

    it('should display citation index', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'First Source',
          url: 'https://example.com',
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      expect(screen.getByText('[1]')).toBeInTheDocument();
    });

    it('should render snippet when provided', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'Research Paper',
          url: 'https://example.com',
          snippet: 'This is an important finding about UK universities.',
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      expect(screen.getByText('"This is an important finding about UK universities."')).toBeInTheDocument();
    });

    it('should not render snippet element when snippet is undefined', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'Source Without Snippet',
          url: 'https://example.com',
          accessedAt: new Date(),
        },
      ];

      // Act
      const { container } = render(<CitationList citations={citations} />);

      // Assert
      const snippetElement = container.querySelector('.italic');
      expect(snippetElement).not.toBeInTheDocument();
    });
  });

  describe('Multiple Citations Rendering', () => {
    it('should render multiple citations', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'First Source',
          url: 'https://example.com/1',
          accessedAt: new Date(),
        },
        {
          title: 'Second Source',
          url: 'https://example.com/2',
          accessedAt: new Date(),
        },
        {
          title: 'Third Source',
          url: 'https://example.com/3',
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      expect(screen.getByText('First Source')).toBeInTheDocument();
      expect(screen.getByText('Second Source')).toBeInTheDocument();
      expect(screen.getByText('Third Source')).toBeInTheDocument();
    });

    it('should number citations sequentially', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'Source A',
          url: 'https://example.com/a',
          accessedAt: new Date(),
        },
        {
          title: 'Source B',
          url: 'https://example.com/b',
          accessedAt: new Date(),
        },
        {
          title: 'Source C',
          url: 'https://example.com/c',
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      expect(screen.getByText('[1]')).toBeInTheDocument();
      expect(screen.getByText('[2]')).toBeInTheDocument();
      expect(screen.getByText('[3]')).toBeInTheDocument();
    });

    it('should render all links correctly', () => {
      // Arrange
      const citations: Citation[] = [
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
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      const links = screen.getAllByRole('link');
      expect(links).toHaveLength(2);
      expect(links[0]).toHaveAttribute('href', 'https://example.com/1');
      expect(links[1]).toHaveAttribute('href', 'https://example.com/2');
    });

    it('should handle mix of citations with and without snippets', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'Source With Snippet',
          url: 'https://example.com/1',
          snippet: 'This has a snippet',
          accessedAt: new Date(),
        },
        {
          title: 'Source Without Snippet',
          url: 'https://example.com/2',
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      expect(screen.getByText('"This has a snippet"')).toBeInTheDocument();
      expect(screen.getByText('Source Without Snippet')).toBeInTheDocument();
    });
  });

  describe('Large Citation Lists', () => {
    it('should handle 10+ citations', () => {
      // Arrange
      const citations: Citation[] = Array.from({ length: 15 }, (_, i) => ({
        title: `Source ${i + 1}`,
        url: `https://example.com/${i + 1}`,
        accessedAt: new Date(),
      }));

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      expect(screen.getByText('[1]')).toBeInTheDocument();
      expect(screen.getByText('[10]')).toBeInTheDocument();
      expect(screen.getByText('[15]')).toBeInTheDocument();
      const links = screen.getAllByRole('link');
      expect(links).toHaveLength(15);
    });
  });

  describe('Link Attributes', () => {
    it('should open links in new tab', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'External Link',
          url: 'https://example.com',
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      const link = screen.getByRole('link');
      expect(link).toHaveAttribute('target', '_blank');
    });

    it('should have noopener noreferrer for security', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'Secure Link',
          url: 'https://example.com',
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      const link = screen.getByRole('link');
      expect(link).toHaveAttribute('rel', 'noopener noreferrer');
    });
  });

  describe('URL Display', () => {
    it('should display full URL', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'Long URL Source',
          url: 'https://www.example.com/very/long/path/to/resource',
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      expect(screen.getByText('https://www.example.com/very/long/path/to/resource')).toBeInTheDocument();
    });

    it('should handle HTTPS URLs', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'HTTPS Source',
          url: 'https://secure.example.com',
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      expect(screen.getByRole('link')).toHaveAttribute('href', 'https://secure.example.com');
    });

    it('should handle HTTP URLs', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'HTTP Source',
          url: 'http://example.com',
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      expect(screen.getByRole('link')).toHaveAttribute('href', 'http://example.com');
    });
  });

  describe('Title Formatting', () => {
    it('should handle long titles', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'A Comprehensive Guide to Studying Computer Science at Top UK Universities in 2025',
          url: 'https://example.com',
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      expect(screen.getByText(/Comprehensive Guide to Studying Computer Science/)).toBeInTheDocument();
    });

    it('should handle special characters in title', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'UK Universities: Rankings & Fees (2025)',
          url: 'https://example.com',
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      expect(screen.getByText('UK Universities: Rankings & Fees (2025)')).toBeInTheDocument();
    });

    it('should handle unicode characters in title', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'UK Universities £10,000 Scholarships',
          url: 'https://example.com',
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      expect(screen.getByText('UK Universities £10,000 Scholarships')).toBeInTheDocument();
    });
  });

  describe('Snippet Formatting', () => {
    it('should wrap snippet in quotes', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'Source',
          url: 'https://example.com',
          snippet: 'Important information here',
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      expect(screen.getByText('"Important information here"')).toBeInTheDocument();
    });

    it('should handle long snippets', () => {
      // Arrange
      const longSnippet = 'This is a very long snippet that contains detailed information about UK universities and their admission requirements.';
      const citations: Citation[] = [
        {
          title: 'Source',
          url: 'https://example.com',
          snippet: longSnippet,
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      expect(screen.getByText(`"${longSnippet}"`)).toBeInTheDocument();
    });

    it('should handle snippets with quotes', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'Source',
          url: 'https://example.com',
          snippet: 'The report states "excellent programs" are available',
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      expect(screen.getByText('"The report states "excellent programs" are available"')).toBeInTheDocument();
    });
  });

  describe('Styling', () => {
    it('should apply background styling to container', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'Source',
          url: 'https://example.com',
          accessedAt: new Date(),
        },
      ];

      // Act
      const { container } = render(<CitationList citations={citations} />);

      // Assert
      const citationContainer = container.querySelector('.bg-gray-50');
      expect(citationContainer).toBeInTheDocument();
      expect(citationContainer).toHaveClass('border');
      expect(citationContainer).toHaveClass('border-gray-200');
      expect(citationContainer).toHaveClass('rounded-lg');
    });

    it('should have Sources heading', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'Source',
          url: 'https://example.com',
          accessedAt: new Date(),
        },
      ];

      // Act
      const { container } = render(<CitationList citations={citations} />);

      // Assert
      const heading = container.querySelector('h3');
      expect(heading).toBeInTheDocument();
      expect(heading).toHaveTextContent('Sources');
    });

    it('should apply link styling', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'Source',
          url: 'https://example.com',
          accessedAt: new Date(),
        },
      ];

      // Act
      const { container } = render(<CitationList citations={citations} />);

      // Assert
      const link = container.querySelector('a');
      expect(link).toHaveClass('text-blue-600');
    });
  });

  describe('Edge Cases', () => {
    it('should handle empty title', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: '',
          url: 'https://example.com',
          accessedAt: new Date(),
        },
      ];

      // Act
      const { container } = render(<CitationList citations={citations} />);

      // Assert
      const link = container.querySelector('a');
      expect(link).toBeInTheDocument();
      expect(link).toHaveAttribute('href', 'https://example.com');
    });

    it('should handle empty snippet', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'Source',
          url: 'https://example.com',
          snippet: '',
          accessedAt: new Date(),
        },
      ];

      // Act
      const { container } = render(<CitationList citations={citations} />);

      // Assert
      // Empty snippet should not render the snippet element
      const snippets = container.querySelectorAll('.italic');
      expect(snippets.length).toBe(0);
    });

    it('should handle very long URLs', () => {
      // Arrange
      const longUrl = 'https://example.com/' + 'path/'.repeat(50);
      const citations: Citation[] = [
        {
          title: 'Long URL Source',
          url: longUrl,
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      expect(screen.getByRole('link')).toHaveAttribute('href', longUrl);
    });
  });

  describe('Accessibility', () => {
    it('should have semantic list structure', () => {
      // Arrange
      const citations: Citation[] = [
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
      ];

      // Act
      const { container } = render(<CitationList citations={citations} />);

      // Assert
      const list = container.querySelector('ul');
      const listItems = container.querySelectorAll('li');
      expect(list).toBeInTheDocument();
      expect(listItems).toHaveLength(2);
    });

    it('should have descriptive link text', () => {
      // Arrange
      const citations: Citation[] = [
        {
          title: 'UK Government Official Guide',
          url: 'https://gov.uk',
          accessedAt: new Date(),
        },
      ];

      // Act
      render(<CitationList citations={citations} />);

      // Assert
      const link = screen.getByRole('link', { name: /UK Government Official Guide/i });
      expect(link).toBeInTheDocument();
    });
  });
});
