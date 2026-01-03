/**
 * Tests for chat page
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import React from 'react';

// Mock next/navigation
const mockPush = vi.fn();
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}));

// Mock usePayment hook
const mockCreateCheckout = vi.fn();
vi.mock('../../../../src/hooks/usePayment', () => ({
  usePayment: vi.fn(() => ({
    isLoading: false,
    error: null,
    createCheckout: mockCreateCheckout,
  })),
}));

// Mock chat components
vi.mock('../../../../src/components/chat/ChatInput', () => ({
  ChatInput: ({ onSubmit, disabled, isLoading }: {
    onSubmit: (query: string) => void;
    disabled: boolean;
    isLoading: boolean;
  }) => (
    <div data-testid="chat-input">
      <input
        data-testid="chat-input-field"
        disabled={disabled}
        placeholder="Ask a question..."
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            onSubmit((e.target as HTMLInputElement).value);
          }
        }}
      />
      <button
        data-testid="chat-submit"
        disabled={disabled || isLoading}
        onClick={() => onSubmit('test query')}
      >
        {isLoading ? 'Loading...' : 'Submit'}
      </button>
    </div>
  ),
}));

vi.mock('../../../../src/components/chat/MessageList', () => ({
  MessageList: ({ messages }: { messages: Array<{ id: string; role: string; content: string }> }) => (
    <div data-testid="message-list">
      {messages.map((m) => (
        <div key={m.id} data-testid={`message-${m.role}`}>{m.content}</div>
      ))}
    </div>
  ),
}));

describe('ChatPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.resetModules();
  });

  describe('rendering', () => {
    it('should render the page heading', async () => {
      const ChatPage = (await import('../../../../src/app/(app)/chat/page')).default;
      render(<ChatPage />);

      expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('UK Study & Migration Research');
    });

    it('should render the pricing information', async () => {
      const ChatPage = (await import('../../../../src/app/(app)/chat/page')).default;
      render(<ChatPage />);

      expect(screen.getByText(/£2.99/)).toBeInTheDocument();
    });

    it('should render ChatInput component', async () => {
      const ChatPage = (await import('../../../../src/app/(app)/chat/page')).default;
      render(<ChatPage />);

      expect(screen.getByTestId('chat-input')).toBeInTheDocument();
    });

    it('should render MessageList component', async () => {
      const ChatPage = (await import('../../../../src/app/(app)/chat/page')).default;
      render(<ChatPage />);

      expect(screen.getByTestId('message-list')).toBeInTheDocument();
    });
  });

  describe('message handling', () => {
    it('should add user message when query is submitted', async () => {
      const ChatPage = (await import('../../../../src/app/(app)/chat/page')).default;
      render(<ChatPage />);

      const submitButton = screen.getByTestId('chat-submit');
      fireEvent.click(submitButton);

      await waitFor(() => {
        expect(screen.getByTestId('message-user')).toBeInTheDocument();
      });
    });

    it('should call createCheckout when submitting query', async () => {
      const ChatPage = (await import('../../../../src/app/(app)/chat/page')).default;
      render(<ChatPage />);

      const submitButton = screen.getByTestId('chat-submit');
      fireEvent.click(submitButton);

      await waitFor(() => {
        expect(mockCreateCheckout).toHaveBeenCalledWith('test query');
      });
    });
  });

  describe('loading state', () => {
    it('should show loading state on ChatInput when isLoading', async () => {
      const { usePayment } = await import('../../../../src/hooks/usePayment');
      (usePayment as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        isLoading: true,
        error: null,
        createCheckout: mockCreateCheckout,
      });

      const ChatPage = (await import('../../../../src/app/(app)/chat/page')).default;
      render(<ChatPage />);

      expect(screen.getByTestId('chat-submit')).toBeDisabled();
    });
  });

  describe('error handling', () => {
    it('should display error message when error exists', async () => {
      const { usePayment } = await import('../../../../src/hooks/usePayment');
      (usePayment as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        isLoading: false,
        error: 'Payment failed',
        createCheckout: mockCreateCheckout,
      });

      const ChatPage = (await import('../../../../src/app/(app)/chat/page')).default;
      render(<ChatPage />);

      expect(screen.getByText('Payment failed')).toBeInTheDocument();
    });

    it('should have error styling', async () => {
      const { usePayment } = await import('../../../../src/hooks/usePayment');
      (usePayment as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        isLoading: false,
        error: 'Error message',
        createCheckout: mockCreateCheckout,
      });

      const ChatPage = (await import('../../../../src/app/(app)/chat/page')).default;
      render(<ChatPage />);

      const errorDiv = screen.getByText('Error message').closest('div');
      expect(errorDiv).toHaveClass('bg-red-50', 'border-red-200');
    });
  });

  describe('styling', () => {
    it('should have max-width container', async () => {
      const ChatPage = (await import('../../../../src/app/(app)/chat/page')).default;
      const { container } = render(<ChatPage />);

      const mainDiv = container.firstChild;
      expect(mainDiv).toHaveClass('max-w-4xl', 'mx-auto');
    });

    it('should have sticky input area', async () => {
      const ChatPage = (await import('../../../../src/app/(app)/chat/page')).default;
      render(<ChatPage />);

      const chatInput = screen.getByTestId('chat-input');
      const stickyContainer = chatInput.closest('.sticky');
      expect(stickyContainer).toBeInTheDocument();
    });
  });
});
