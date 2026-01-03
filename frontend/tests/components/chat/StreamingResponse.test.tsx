/**
 * Tests for StreamingResponse component
 * Coverage target: 100% (high-impact file: ~10-12% total frontend coverage)
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { StreamingResponse } from '../../../src/components/chat/StreamingResponse';

// Mock ReportSection component
vi.mock('../../../src/components/reports/ReportSection', () => ({
  ReportSection: ({ section, index }: any) => (
    <div data-testid={`report-section-${index}`}>
      <h3>{section.title}</h3>
      <p>{section.content}</p>
      {section.citations?.map((citation: any, idx: number) => (
        <a key={idx} href={citation.url}>
          {citation.title}
        </a>
      ))}
    </div>
  ),
}));

// Mock EventSource
class MockEventSource {
  url: string;
  onmessage: ((event: MessageEvent) => void) | null = null;
  onerror: ((event: Event) => void) | null = null;
  readyState: number = 0;

  static instances: MockEventSource[] = [];

  constructor(url: string, options?: any) {
    this.url = url;
    this.readyState = 1; // OPEN
    MockEventSource.instances.push(this);
  }

  close() {
    this.readyState = 2; // CLOSED
  }

  // Helper method to simulate receiving a message
  static sendMessage(data: any) {
    const instance = MockEventSource.instances[MockEventSource.instances.length - 1];
    if (instance?.onmessage) {
      instance.onmessage(new MessageEvent('message', { data: JSON.stringify(data) }));
    }
  }

  // Helper method to simulate an error
  static sendError() {
    const instance = MockEventSource.instances[MockEventSource.instances.length - 1];
    if (instance?.onerror) {
      instance.onerror(new Event('error'));
    }
  }

  static clearInstances() {
    MockEventSource.instances = [];
  }
}

// Set up global EventSource mock
global.EventSource = MockEventSource as any;

// Mock environment variable
const originalEnv = process.env.NEXT_PUBLIC_API_URL;

describe('StreamingResponse', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    MockEventSource.clearInstances();
    process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
  });

  afterEach(() => {
    process.env.NEXT_PUBLIC_API_URL = originalEnv;
    MockEventSource.clearInstances();
  });

  describe('Initial rendering', () => {
    it('should render progress indicator initially', () => {
      render(<StreamingResponse reportId="test-report-123" />);

      expect(screen.getByText('Generating Report')).toBeInTheDocument();
      expect(screen.getByText(/Section 0 of 10/)).toBeInTheDocument();
    });

    it('should initialize EventSource with correct URL', () => {
      render(<StreamingResponse reportId="report-456" />);

      const instance = MockEventSource.instances[0];
      expect(instance.url).toBe('http://localhost:8000/stream/reports/report-456');
    });

    it('should use default API URL if env var not set', () => {
      delete process.env.NEXT_PUBLIC_API_URL;

      render(<StreamingResponse reportId="report-789" />);

      const instance = MockEventSource.instances[0];
      expect(instance.url).toBe('http://localhost:8000/stream/reports/report-789');
    });

    it('should render with empty sections initially', () => {
      render(<StreamingResponse reportId="test-report" />);

      const sections = screen.queryAllByTestId(/^report-section-/);
      expect(sections).toHaveLength(0);
    });
  });

  describe('SSE event handling', () => {
    describe('start event', () => {
      it('should handle start event', async () => {
        const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {});

        render(<StreamingResponse reportId="test-report" />);

        MockEventSource.sendMessage({
          type: 'start',
          report_id: 'test-report',
        });

        await waitFor(() => {
          expect(consoleSpy).toHaveBeenCalledWith(
            'Streaming started for report:',
            'test-report'
          );
        });

        consoleSpy.mockRestore();
      });
    });

    describe('chunk event', () => {
      it('should accumulate text chunks', async () => {
        render(<StreamingResponse reportId="test-report" />);

        MockEventSource.sendMessage({
          type: 'chunk',
          content: 'First chunk ',
        });

        await waitFor(() => {
          expect(screen.getByText('First chunk ')).toBeInTheDocument();
        });

        MockEventSource.sendMessage({
          type: 'chunk',
          content: 'second chunk',
        });

        await waitFor(() => {
          expect(screen.getByText('First chunk second chunk')).toBeInTheDocument();
        });
      });

      it('should render chunks with pulsing animation', async () => {
        render(<StreamingResponse reportId="test-report" />);

        MockEventSource.sendMessage({
          type: 'chunk',
          content: 'Streaming content...',
        });

        await waitFor(() => {
          const chunkElement = screen.getByText('Streaming content...').closest('div');
          expect(chunkElement?.parentElement).toHaveClass('animate-pulse');
        });
      });

      it('should preserve whitespace in chunks', async () => {
        render(<StreamingResponse reportId="test-report" />);

        const contentWithWhitespace = 'Line 1\n\nLine 2\n  Indented';
        MockEventSource.sendMessage({
          type: 'chunk',
          content: contentWithWhitespace,
        });

        await waitFor(() => {
          const element = screen.getByText(contentWithWhitespace);
          expect(element).toHaveClass('whitespace-pre-wrap');
        });
      });
    });

    describe('section event', () => {
      it('should render completed section', async () => {
        render(<StreamingResponse reportId="test-report" />);

        MockEventSource.sendMessage({
          type: 'section',
          section_num: 1,
          heading: 'Introduction',
          content: 'This is the introduction section.',
          citations: [
            { title: 'Source 1', url: 'https://example.com/1' },
          ],
        });

        await waitFor(() => {
          expect(screen.getByText('Introduction')).toBeInTheDocument();
          expect(screen.getByText('This is the introduction section.')).toBeInTheDocument();
          expect(screen.getByText('Source 1')).toBeInTheDocument();
        });
      });

      it('should clear chunk buffer when section completes', async () => {
        render(<StreamingResponse reportId="test-report" />);

        MockEventSource.sendMessage({
          type: 'chunk',
          content: 'Partial content...',
        });

        await waitFor(() => {
          expect(screen.getByText('Partial content...')).toBeInTheDocument();
        });

        MockEventSource.sendMessage({
          type: 'section',
          section_num: 1,
          heading: 'Complete Section',
          content: 'Full section content',
          citations: [],
        });

        await waitFor(() => {
          expect(screen.queryByText('Partial content...')).not.toBeInTheDocument();
          expect(screen.getByText('Full section content')).toBeInTheDocument();
        });
      });

      it('should render multiple sections in order', async () => {
        render(<StreamingResponse reportId="test-report" />);

        MockEventSource.sendMessage({
          type: 'section',
          section_num: 1,
          heading: 'Section 1',
          content: 'First section',
          citations: [],
        });

        MockEventSource.sendMessage({
          type: 'section',
          section_num: 2,
          heading: 'Section 2',
          content: 'Second section',
          citations: [],
        });

        await waitFor(() => {
          const sections = screen.getAllByTestId(/^report-section-/);
          expect(sections).toHaveLength(2);
        });
      });

      it('should handle sections with multiple citations', async () => {
        render(<StreamingResponse reportId="test-report" />);

        MockEventSource.sendMessage({
          type: 'section',
          section_num: 1,
          heading: 'Research',
          content: 'Research content',
          citations: [
            { title: 'Paper 1', url: 'https://example.com/1', snippet: 'Snippet 1' },
            { title: 'Paper 2', url: 'https://example.com/2' },
            { title: 'Paper 3', url: 'https://example.com/3', snippet: 'Snippet 3' },
          ],
        });

        await waitFor(() => {
          expect(screen.getByText('Paper 1')).toBeInTheDocument();
          expect(screen.getByText('Paper 2')).toBeInTheDocument();
          expect(screen.getByText('Paper 3')).toBeInTheDocument();
        });
      });
    });

    describe('progress event', () => {
      it('should update progress indicator', async () => {
        render(<StreamingResponse reportId="test-report" />);

        MockEventSource.sendMessage({
          type: 'progress',
          current_section: 3,
          total_sections: 10,
        });

        await waitFor(() => {
          expect(screen.getByText(/Section 3 of 10/)).toBeInTheDocument();
        });
      });

      it('should update progress bar width', async () => {
        render(<StreamingResponse reportId="test-report" />);

        MockEventSource.sendMessage({
          type: 'progress',
          current_section: 5,
          total_sections: 10,
        });

        await waitFor(() => {
          const progressBar = document.querySelector('.bg-blue-600');
          expect(progressBar).toHaveStyle({ width: '50%' });
        });
      });

      it('should handle 100% progress', async () => {
        render(<StreamingResponse reportId="test-report" />);

        MockEventSource.sendMessage({
          type: 'progress',
          current_section: 10,
          total_sections: 10,
        });

        await waitFor(() => {
          const progressBar = document.querySelector('.bg-blue-600');
          expect(progressBar).toHaveStyle({ width: '100%' });
        });
      });
    });

    describe('complete event', () => {
      it('should show completion message', async () => {
        render(<StreamingResponse reportId="test-report" />);

        MockEventSource.sendMessage({
          type: 'complete',
        });

        await waitFor(() => {
          expect(screen.getByText('Report Generation Complete')).toBeInTheDocument();
          expect(screen.getByText('Your report is now available for 30 days')).toBeInTheDocument();
        });
      });

      it('should close EventSource on completion', async () => {
        render(<StreamingResponse reportId="test-report" />);

        const instance = MockEventSource.instances[0];
        const closeSpy = vi.spyOn(instance, 'close');

        MockEventSource.sendMessage({
          type: 'complete',
        });

        await waitFor(() => {
          expect(closeSpy).toHaveBeenCalled();
        });
      });

      it('should call onComplete callback', async () => {
        const onComplete = vi.fn();
        render(<StreamingResponse reportId="test-report" onComplete={onComplete} />);

        MockEventSource.sendMessage({
          type: 'complete',
        });

        await waitFor(() => {
          expect(onComplete).toHaveBeenCalled();
        });
      });

      it('should hide current chunk on completion', async () => {
        render(<StreamingResponse reportId="test-report" />);

        MockEventSource.sendMessage({
          type: 'chunk',
          content: 'In progress...',
        });

        await waitFor(() => {
          expect(screen.getByText('In progress...')).toBeInTheDocument();
        });

        MockEventSource.sendMessage({
          type: 'complete',
        });

        await waitFor(() => {
          expect(screen.queryByText('In progress...')).not.toBeInTheDocument();
        });
      });
    });

    describe('error event', () => {
      it('should display error message from SSE', async () => {
        render(<StreamingResponse reportId="test-report" />);

        MockEventSource.sendMessage({
          type: 'error',
          message: 'Failed to generate report',
        });

        await waitFor(() => {
          expect(screen.getByText('Error Generating Report')).toBeInTheDocument();
          expect(screen.getByText('Failed to generate report')).toBeInTheDocument();
        });
      });

      it('should display default error message if none provided', async () => {
        render(<StreamingResponse reportId="test-report" />);

        MockEventSource.sendMessage({
          type: 'error',
        });

        await waitFor(() => {
          expect(screen.getByText('Unknown error occurred')).toBeInTheDocument();
        });
      });

      it('should close EventSource on error', async () => {
        render(<StreamingResponse reportId="test-report" />);

        const instance = MockEventSource.instances[0];
        const closeSpy = vi.spyOn(instance, 'close');

        MockEventSource.sendMessage({
          type: 'error',
          message: 'Test error',
        });

        await waitFor(() => {
          expect(closeSpy).toHaveBeenCalled();
        });
      });

      it('should call onError callback', async () => {
        const onError = vi.fn();
        render(<StreamingResponse reportId="test-report" onError={onError} />);

        MockEventSource.sendMessage({
          type: 'error',
          message: 'Test error message',
        });

        await waitFor(() => {
          expect(onError).toHaveBeenCalledWith('Test error message');
        });
      });

      it('should show Try Again button on error', async () => {
        render(<StreamingResponse reportId="test-report" />);

        MockEventSource.sendMessage({
          type: 'error',
          message: 'API error',
        });

        await waitFor(() => {
          expect(screen.getByText('Try Again')).toBeInTheDocument();
        });
      });

      it('should reload page when Try Again is clicked', async () => {
        const user = userEvent.setup();
        const reloadMock = vi.fn();
        Object.defineProperty(window, 'location', {
          value: { reload: reloadMock },
          writable: true,
        });

        render(<StreamingResponse reportId="test-report" />);

        MockEventSource.sendMessage({
          type: 'error',
          message: 'Error',
        });

        await waitFor(() => {
          expect(screen.getByText('Try Again')).toBeInTheDocument();
        });

        await user.click(screen.getByText('Try Again'));
        expect(reloadMock).toHaveBeenCalled();
      });
    });

    describe('unknown event type', () => {
      it('should log warning for unknown event type', async () => {
        const consoleWarnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});

        render(<StreamingResponse reportId="test-report" />);

        MockEventSource.sendMessage({
          type: 'unknown_type',
          data: 'some data',
        });

        await waitFor(() => {
          expect(consoleWarnSpy).toHaveBeenCalledWith('Unknown event type:', 'unknown_type');
        });

        consoleWarnSpy.mockRestore();
      });

      it('should continue streaming after unknown event', async () => {
        render(<StreamingResponse reportId="test-report" />);

        MockEventSource.sendMessage({
          type: 'unknown_type',
        });

        MockEventSource.sendMessage({
          type: 'chunk',
          content: 'Valid content',
        });

        await waitFor(() => {
          expect(screen.getByText('Valid content')).toBeInTheDocument();
        });
      });
    });
  });

  describe('EventSource error handling', () => {
    it('should handle connection error', async () => {
      render(<StreamingResponse reportId="test-report" />);

      MockEventSource.sendError();

      await waitFor(() => {
        expect(screen.getByText('Error Generating Report')).toBeInTheDocument();
        expect(screen.getByText('Streaming connection lost. Please try again.')).toBeInTheDocument();
      });
    });

    it('should close EventSource on connection error', async () => {
      render(<StreamingResponse reportId="test-report" />);

      const instance = MockEventSource.instances[0];
      const closeSpy = vi.spyOn(instance, 'close');

      MockEventSource.sendError();

      await waitFor(() => {
        expect(closeSpy).toHaveBeenCalled();
      });
    });

    it('should call onError callback on connection error', async () => {
      const onError = vi.fn();
      render(<StreamingResponse reportId="test-report" onError={onError} />);

      MockEventSource.sendError();

      await waitFor(() => {
        expect(onError).toHaveBeenCalledWith('Streaming connection lost. Please try again.');
      });
    });

    it('should log connection error', async () => {
      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      render(<StreamingResponse reportId="test-report" />);

      MockEventSource.sendError();

      await waitFor(() => {
        expect(consoleErrorSpy).toHaveBeenCalledWith('SSE connection error:', expect.any(Event));
      });

      consoleErrorSpy.mockRestore();
    });
  });

  describe('JSON parsing errors', () => {
    it('should handle invalid JSON in message', async () => {
      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      render(<StreamingResponse reportId="test-report" />);

      const instance = MockEventSource.instances[0];
      if (instance.onmessage) {
        instance.onmessage(new MessageEvent('message', { data: 'invalid json' }));
      }

      await waitFor(() => {
        expect(consoleErrorSpy).toHaveBeenCalledWith(
          'Failed to parse SSE data:',
          expect.any(Error)
        );
      });

      consoleErrorSpy.mockRestore();
    });

    it('should continue streaming after JSON parse error', async () => {
      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      render(<StreamingResponse reportId="test-report" />);

      const instance = MockEventSource.instances[0];
      if (instance.onmessage) {
        // Send invalid JSON
        instance.onmessage(new MessageEvent('message', { data: 'invalid' }));

        // Send valid message
        MockEventSource.sendMessage({
          type: 'chunk',
          content: 'Valid after error',
        });
      }

      await waitFor(() => {
        expect(screen.getByText('Valid after error')).toBeInTheDocument();
      });

      consoleErrorSpy.mockRestore();
    });
  });

  describe('Component lifecycle', () => {
    it('should close EventSource on unmount', () => {
      const { unmount } = render(<StreamingResponse reportId="test-report" />);

      const instance = MockEventSource.instances[0];
      const closeSpy = vi.spyOn(instance, 'close');

      unmount();

      expect(closeSpy).toHaveBeenCalled();
    });

    it('should create new EventSource when reportId changes', async () => {
      const { rerender } = render(<StreamingResponse reportId="report-1" />);

      expect(MockEventSource.instances).toHaveLength(1);
      expect(MockEventSource.instances[0].url).toContain('report-1');

      rerender(<StreamingResponse reportId="report-2" />);

      await waitFor(() => {
        expect(MockEventSource.instances).toHaveLength(2);
        expect(MockEventSource.instances[1].url).toContain('report-2');
      });
    });

    it('should close old EventSource when reportId changes', () => {
      const { rerender } = render(<StreamingResponse reportId="report-1" />);

      const firstInstance = MockEventSource.instances[0];
      const closeSpy = vi.spyOn(firstInstance, 'close');

      rerender(<StreamingResponse reportId="report-2" />);

      expect(closeSpy).toHaveBeenCalled();
    });
  });

  describe('Callbacks', () => {
    it('should not crash if onComplete is undefined', async () => {
      render(<StreamingResponse reportId="test-report" />);

      expect(() => {
        MockEventSource.sendMessage({ type: 'complete' });
      }).not.toThrow();
    });

    it('should not crash if onError is undefined', async () => {
      render(<StreamingResponse reportId="test-report" />);

      expect(() => {
        MockEventSource.sendMessage({ type: 'error', message: 'Error' });
      }).not.toThrow();
    });

    it('should call callbacks with correct parameters', async () => {
      const onComplete = vi.fn();
      const onError = vi.fn();

      render(
        <StreamingResponse
          reportId="test-report"
          onComplete={onComplete}
          onError={onError}
        />
      );

      MockEventSource.sendMessage({ type: 'error', message: 'Test error' });

      await waitFor(() => {
        expect(onError).toHaveBeenCalledWith('Test error');
        expect(onComplete).not.toHaveBeenCalled();
      });
    });
  });

  describe('UI rendering', () => {
    it('should render sticky progress bar', () => {
      render(<StreamingResponse reportId="test-report" />);

      const progressContainer = screen.getByText('Generating Report').closest('div');
      expect(progressContainer?.parentElement).toHaveClass('sticky', 'top-0', 'z-10');
    });

    it('should animate sections when they appear', async () => {
      render(<StreamingResponse reportId="test-report" />);

      MockEventSource.sendMessage({
        type: 'section',
        section_num: 1,
        heading: 'Test Section',
        content: 'Content',
        citations: [],
      });

      await waitFor(() => {
        const sectionContainer = screen.getByTestId('report-section-1').parentElement;
        expect(sectionContainer).toHaveClass('animate-fade-in');
      });
    });

    it('should display completion checkmark icon', async () => {
      render(<StreamingResponse reportId="test-report" />);

      MockEventSource.sendMessage({ type: 'complete' });

      await waitFor(() => {
        const svg = document.querySelector('svg');
        expect(svg).toBeInTheDocument();
        expect(svg).toHaveClass('text-green-600');
      });
    });

    it('should not render chunk when complete', async () => {
      render(<StreamingResponse reportId="test-report" />);

      MockEventSource.sendMessage({ type: 'chunk', content: 'Chunk' });

      await waitFor(() => {
        expect(screen.getByText('Chunk')).toBeInTheDocument();
      });

      MockEventSource.sendMessage({ type: 'complete' });

      await waitFor(() => {
        expect(screen.queryByText('Chunk')).not.toBeInTheDocument();
      });
    });
  });

  describe('Edge cases', () => {
    it('should handle empty section content', async () => {
      render(<StreamingResponse reportId="test-report" />);

      MockEventSource.sendMessage({
        type: 'section',
        section_num: 1,
        heading: 'Empty Section',
        content: '',
        citations: [],
      });

      await waitFor(() => {
        expect(screen.getByText('Empty Section')).toBeInTheDocument();
      });
    });

    it('should handle section with no citations', async () => {
      render(<StreamingResponse reportId="test-report" />);

      MockEventSource.sendMessage({
        type: 'section',
        section_num: 1,
        heading: 'No Citations',
        content: 'Content without citations',
        citations: [],
      });

      await waitFor(() => {
        expect(screen.getByText('Content without citations')).toBeInTheDocument();
      });
    });

    it('should handle zero progress total', async () => {
      render(<StreamingResponse reportId="test-report" />);

      MockEventSource.sendMessage({
        type: 'progress',
        current_section: 0,
        total_sections: 0,
      });

      await waitFor(() => {
        const progressBar = document.querySelector('.bg-blue-600');
        // 0/0 = NaN, which should result in 0% width or be handled gracefully
        expect(progressBar).toBeInTheDocument();
      });
    });

    it('should handle very large section numbers', async () => {
      render(<StreamingResponse reportId="test-report" />);

      MockEventSource.sendMessage({
        type: 'section',
        section_num: 999999,
        heading: 'Large Number Section',
        content: 'Content',
        citations: [],
      });

      await waitFor(() => {
        expect(screen.getByTestId('report-section-999999')).toBeInTheDocument();
      });
    });

    it('should handle rapid successive events', async () => {
      render(<StreamingResponse reportId="test-report" />);

      // Send multiple events rapidly
      for (let i = 1; i <= 5; i++) {
        MockEventSource.sendMessage({
          type: 'section',
          section_num: i,
          heading: `Section ${i}`,
          content: `Content ${i}`,
          citations: [],
        });
      }

      await waitFor(() => {
        const sections = screen.getAllByTestId(/^report-section-/);
        expect(sections).toHaveLength(5);
      });
    });
  });
});
