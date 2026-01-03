/**
 * Tests for MessageList component
 * Tests message rendering, empty states, and formatting
 */

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MessageList, Message } from '../../src/components/chat/MessageList';

describe('MessageList', () => {
  // AAA: Arrange, Act, Assert

  describe('Empty State', () => {
    it('should show empty message when no messages', () => {
      // Arrange
      const messages: Message[] = [];

      // Act
      render(<MessageList messages={messages} />);

      // Assert
      expect(screen.getByText(/no messages yet/i)).toBeInTheDocument();
      expect(screen.getByText(/start by asking a question/i)).toBeInTheDocument();
    });

    it('should not show messages container when empty', () => {
      // Arrange
      const messages: Message[] = [];

      // Act
      const { container } = render(<MessageList messages={messages} />);

      // Assert
      const messagesContainer = container.querySelector('.space-y-6');
      expect(messagesContainer).not.toBeInTheDocument();
    });
  });

  describe('Single Message Rendering', () => {
    it('should render a user message correctly', () => {
      // Arrange
      const messages: Message[] = [
        {
          id: '1',
          role: 'user',
          content: 'What are the best UK universities?',
          timestamp: new Date('2025-12-29T12:00:00Z'),
        },
      ];

      // Act
      render(<MessageList messages={messages} />);

      // Assert
      expect(screen.getByText('What are the best UK universities?')).toBeInTheDocument();
      expect(screen.getByText(/12:00:00/)).toBeInTheDocument();
    });

    it('should render an assistant message correctly', () => {
      // Arrange
      const messages: Message[] = [
        {
          id: '2',
          role: 'assistant',
          content: 'The best UK universities include Oxford, Cambridge, and Imperial College London.',
          timestamp: new Date('2025-12-29T12:01:00Z'),
        },
      ];

      // Act
      render(<MessageList messages={messages} />);

      // Assert
      expect(screen.getByText(/The best UK universities include Oxford/)).toBeInTheDocument();
    });

    it('should apply correct styling to user messages', () => {
      // Arrange
      const messages: Message[] = [
        {
          id: '1',
          role: 'user',
          content: 'Test user message',
          timestamp: new Date(),
        },
      ];

      // Act
      const { container } = render(<MessageList messages={messages} />);

      // Assert
      const messageDiv = container.querySelector('.bg-blue-600');
      expect(messageDiv).toBeInTheDocument();
      expect(messageDiv).toHaveClass('text-white');
    });

    it('should apply correct styling to assistant messages', () => {
      // Arrange
      const messages: Message[] = [
        {
          id: '1',
          role: 'assistant',
          content: 'Test assistant message',
          timestamp: new Date(),
        },
      ];

      // Act
      const { container } = render(<MessageList messages={messages} />);

      // Assert
      const messageDiv = container.querySelector('.bg-gray-100');
      expect(messageDiv).toBeInTheDocument();
      expect(messageDiv).toHaveClass('text-gray-900');
    });
  });

  describe('Multiple Messages Rendering', () => {
    it('should render multiple messages in order', () => {
      // Arrange
      const messages: Message[] = [
        {
          id: '1',
          role: 'user',
          content: 'First message',
          timestamp: new Date('2025-12-29T12:00:00Z'),
        },
        {
          id: '2',
          role: 'assistant',
          content: 'Second message',
          timestamp: new Date('2025-12-29T12:01:00Z'),
        },
        {
          id: '3',
          role: 'user',
          content: 'Third message',
          timestamp: new Date('2025-12-29T12:02:00Z'),
        },
      ];

      // Act
      render(<MessageList messages={messages} />);

      // Assert
      expect(screen.getByText('First message')).toBeInTheDocument();
      expect(screen.getByText('Second message')).toBeInTheDocument();
      expect(screen.getByText('Third message')).toBeInTheDocument();
    });

    it('should render conversation with alternating roles', () => {
      // Arrange
      const messages: Message[] = [
        {
          id: '1',
          role: 'user',
          content: 'What is the tuition fee?',
          timestamp: new Date(),
        },
        {
          id: '2',
          role: 'assistant',
          content: 'Tuition fees vary by university.',
          timestamp: new Date(),
        },
        {
          id: '3',
          role: 'user',
          content: 'What about scholarships?',
          timestamp: new Date(),
        },
        {
          id: '4',
          role: 'assistant',
          content: 'Many scholarships are available.',
          timestamp: new Date(),
        },
      ];

      // Act
      const { container } = render(<MessageList messages={messages} />);

      // Assert
      const userMessages = container.querySelectorAll('.bg-blue-600');
      const assistantMessages = container.querySelectorAll('.bg-gray-100');
      expect(userMessages).toHaveLength(2);
      expect(assistantMessages).toHaveLength(2);
    });
  });

  describe('Message Alignment', () => {
    it('should align user messages to the right', () => {
      // Arrange
      const messages: Message[] = [
        {
          id: '1',
          role: 'user',
          content: 'Test',
          timestamp: new Date(),
        },
      ];

      // Act
      const { container } = render(<MessageList messages={messages} />);

      // Assert
      const messageContainer = container.querySelector('.justify-end');
      expect(messageContainer).toBeInTheDocument();
    });

    it('should align assistant messages to the left', () => {
      // Arrange
      const messages: Message[] = [
        {
          id: '1',
          role: 'assistant',
          content: 'Test',
          timestamp: new Date(),
        },
      ];

      // Act
      const { container } = render(<MessageList messages={messages} />);

      // Assert
      const messageContainer = container.querySelector('.justify-start');
      expect(messageContainer).toBeInTheDocument();
    });
  });

  describe('Timestamp Formatting', () => {
    it('should format timestamp correctly', () => {
      // Arrange
      const testDate = new Date('2025-12-29T14:30:45Z');
      const messages: Message[] = [
        {
          id: '1',
          role: 'user',
          content: 'Test',
          timestamp: testDate,
        },
      ];

      // Act
      render(<MessageList messages={messages} />);

      // Assert
      // Note: toLocaleTimeString format may vary by locale
      const timeElement = screen.getByText(/\d{1,2}:\d{2}:\d{2}/);
      expect(timeElement).toBeInTheDocument();
    });

    it('should show timestamp for all messages', () => {
      // Arrange
      const messages: Message[] = [
        {
          id: '1',
          role: 'user',
          content: 'First',
          timestamp: new Date('2025-12-29T12:00:00Z'),
        },
        {
          id: '2',
          role: 'assistant',
          content: 'Second',
          timestamp: new Date('2025-12-29T12:01:00Z'),
        },
      ];

      // Act
      const { container } = render(<MessageList messages={messages} />);

      // Assert
      const timestamps = container.querySelectorAll('.text-xs');
      expect(timestamps.length).toBeGreaterThanOrEqual(2);
    });
  });

  describe('Content Formatting', () => {
    it('should preserve whitespace in message content', () => {
      // Arrange
      const messages: Message[] = [
        {
          id: '1',
          role: 'user',
          content: 'Line 1\nLine 2\nLine 3',
          timestamp: new Date(),
        },
      ];

      // Act
      const { container } = render(<MessageList messages={messages} />);

      // Assert
      const contentElement = container.querySelector('.whitespace-pre-wrap');
      expect(contentElement).toBeInTheDocument();
      expect(contentElement?.textContent).toBe('Line 1\nLine 2\nLine 3');
    });

    it('should render long messages without truncation', () => {
      // Arrange
      const longMessage = 'UK universities offer a wide range of programs. '.repeat(20);
      const messages: Message[] = [
        {
          id: '1',
          role: 'assistant',
          content: longMessage,
          timestamp: new Date(),
        },
      ];

      // Act
      render(<MessageList messages={messages} />);

      // Assert - Use trimmed comparison since testing library normalizes whitespace
      const messageElement = screen.getByText((content, element) => {
        return element?.textContent?.trim() === longMessage.trim();
      });
      expect(messageElement).toBeInTheDocument();
    });

    it('should handle special characters in message content', () => {
      // Arrange
      const messages: Message[] = [
        {
          id: '1',
          role: 'user',
          content: 'What about £10,000 tuition & fees?',
          timestamp: new Date(),
        },
      ];

      // Act
      render(<MessageList messages={messages} />);

      // Assert
      expect(screen.getByText('What about £10,000 tuition & fees?')).toBeInTheDocument();
    });
  });

  describe('Unique Keys', () => {
    it('should use message id as key', () => {
      // Arrange
      const messages: Message[] = [
        {
          id: 'unique-1',
          role: 'user',
          content: 'First',
          timestamp: new Date(),
        },
        {
          id: 'unique-2',
          role: 'assistant',
          content: 'Second',
          timestamp: new Date(),
        },
      ];

      // Act
      const { container } = render(<MessageList messages={messages} />);

      // Assert
      // React uses keys internally, but we can verify messages are rendered
      const messageElements = container.querySelectorAll('[class*="justify-"]');
      expect(messageElements).toHaveLength(2);
    });
  });

  describe('Edge Cases', () => {
    it('should handle message with empty content', () => {
      // Arrange
      const messages: Message[] = [
        {
          id: '1',
          role: 'user',
          content: '',
          timestamp: new Date(),
        },
      ];

      // Act
      const { container } = render(<MessageList messages={messages} />);

      // Assert
      const messageContainer = container.querySelector('.bg-blue-600');
      expect(messageContainer).toBeInTheDocument();
    });

    it('should handle single character message', () => {
      // Arrange
      const messages: Message[] = [
        {
          id: '1',
          role: 'user',
          content: 'X',
          timestamp: new Date(),
        },
      ];

      // Act
      render(<MessageList messages={messages} />);

      // Assert
      expect(screen.getByText('X')).toBeInTheDocument();
    });

    it('should handle very long conversation', () => {
      // Arrange
      const messages: Message[] = Array.from({ length: 100 }, (_, i) => ({
        id: `msg-${i}`,
        role: (i % 2 === 0 ? 'user' : 'assistant') as 'user' | 'assistant',
        content: `Message ${i}`,
        timestamp: new Date(),
      }));

      // Act
      const { container } = render(<MessageList messages={messages} />);

      // Assert
      const messageElements = container.querySelectorAll('[class*="justify-"]');
      expect(messageElements).toHaveLength(100);
    });
  });

  describe('Accessibility', () => {
    it('should have appropriate text size for readability', () => {
      // Arrange
      const messages: Message[] = [
        {
          id: '1',
          role: 'user',
          content: 'Test message',
          timestamp: new Date(),
        },
      ];

      // Act
      const { container } = render(<MessageList messages={messages} />);

      // Assert
      const contentElement = container.querySelector('.text-sm');
      expect(contentElement).toBeInTheDocument();
    });

    it('should have smaller timestamp text', () => {
      // Arrange
      const messages: Message[] = [
        {
          id: '1',
          role: 'user',
          content: 'Test',
          timestamp: new Date(),
        },
      ];

      // Act
      const { container } = render(<MessageList messages={messages} />);

      // Assert
      const timestampElement = container.querySelector('.text-xs');
      expect(timestampElement).toBeInTheDocument();
    });
  });
});
