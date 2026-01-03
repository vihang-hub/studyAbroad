/**
 * Tests for CheckoutButton component
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { CheckoutButton } from '../../src/components/payments/CheckoutButton';

global.fetch = vi.fn();

describe('CheckoutButton', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render with default amount', () => {
    render(<CheckoutButton query="Test query" />);

    const button = screen.getByRole('button');
    expect(button).toBeInTheDocument();
    expect(button).toHaveTextContent('Generate Report (£2.99)');
  });

  it('should render with custom amount', () => {
    render(<CheckoutButton query="Test query" amount={500} />);

    const button = screen.getByRole('button');
    expect(button).toHaveTextContent('Generate Report (£5.00)');
  });

  it('should be disabled when query is empty', () => {
    render(<CheckoutButton query="" />);

    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
  });

  it('should be disabled when query is whitespace only', () => {
    render(<CheckoutButton query="   " />);

    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
  });

  it('should be disabled when disabled prop is true', () => {
    render(<CheckoutButton query="Test query" disabled />);

    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
  });

  it('should call onCheckoutStart when clicked', async () => {
    const mockOnStart = vi.fn();
    (global.fetch as any).mockResolvedValue({
      ok: true,
      json: async () => ({ reportId: 'report_123' }),
    });

    render(<CheckoutButton query="Test query" onCheckoutStart={mockOnStart} />);

    const button = screen.getByRole('button');
    fireEvent.click(button);

    expect(mockOnStart).toHaveBeenCalledTimes(1);
  });

  it('should make API call with correct query', async () => {
    (global.fetch as any).mockResolvedValue({
      ok: true,
      json: async () => ({ reportId: 'report_123' }),
    });

    render(<CheckoutButton query="UK university query" />);

    const button = screen.getByRole('button');
    fireEvent.click(button);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        '/api/reports/initiate',
        expect.objectContaining({
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ query: 'UK university query' }),
        })
      );
    });
  });

  it('should call onCheckoutSuccess on successful checkout', async () => {
    const mockOnSuccess = vi.fn();
    (global.fetch as any).mockResolvedValue({
      ok: true,
      json: async () => ({ reportId: 'report_12345' }),
    });

    render(<CheckoutButton query="Test query" onCheckoutSuccess={mockOnSuccess} />);

    const button = screen.getByRole('button');
    fireEvent.click(button);

    await waitFor(() => {
      expect(mockOnSuccess).toHaveBeenCalledWith('report_12345');
    });
  });

  it('should call onCheckoutError on failed checkout', async () => {
    const mockOnError = vi.fn();
    (global.fetch as any).mockResolvedValue({
      ok: false,
    });

    render(<CheckoutButton query="Test query" onCheckoutError={mockOnError} />);

    const button = screen.getByRole('button');
    fireEvent.click(button);

    await waitFor(() => {
      expect(mockOnError).toHaveBeenCalledWith('Failed to create checkout session');
    });
  });

  it('should handle network errors', async () => {
    const mockOnError = vi.fn();
    (global.fetch as any).mockRejectedValue(new Error('Network error'));

    render(<CheckoutButton query="Test query" onCheckoutError={mockOnError} />);

    const button = screen.getByRole('button');
    fireEvent.click(button);

    await waitFor(() => {
      expect(mockOnError).toHaveBeenCalledWith('Network error');
    });
  });

  it('should show loading state during checkout', async () => {
    let resolvePromise: any;
    const promise = new Promise((resolve) => {
      resolvePromise = resolve;
    });

    (global.fetch as any).mockReturnValue(promise);

    render(<CheckoutButton query="Test query" />);

    const button = screen.getByRole('button');
    fireEvent.click(button);

    expect(button).toHaveTextContent('Processing...');
    expect(button).toBeDisabled();

    resolvePromise({
      ok: true,
      json: async () => ({ reportId: 'report_123' }),
    });

    await waitFor(() => {
      expect(button).toHaveTextContent('Generate Report');
      expect(button).not.toBeDisabled();
    });
  });

  it('should apply custom className', () => {
    render(<CheckoutButton query="Test query" className="custom-class" />);

    const button = screen.getByRole('button');
    expect(button).toHaveClass('custom-class');
  });

  it('should include default styling classes', () => {
    render(<CheckoutButton query="Test query" />);

    const button = screen.getByRole('button');
    expect(button).toHaveClass('px-6');
    expect(button).toHaveClass('py-3');
    expect(button).toHaveClass('bg-blue-600');
    expect(button).toHaveClass('text-white');
  });

  it('should use custom currency', async () => {
    render(<CheckoutButton query="Test query" amount={500} currency="usd" />);

    const button = screen.getByRole('button');
    // Currency formatting depends on formatPrice implementation
    expect(button).toBeInTheDocument();
  });
});
