/**
 * Tests for ChatInput component
 * Tests UK validation, character limits, and user interactions
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ChatInput } from '../../src/components/chat/ChatInput';

describe('ChatInput', () => {
  // AAA: Arrange, Act, Assert

  describe('Rendering', () => {
    it('should render the input form with label and textarea', () => {
      // Arrange
      const onSubmit = vi.fn();

      // Act
      render(<ChatInput onSubmit={onSubmit} />);

      // Assert
      expect(screen.getByLabelText(/what would you like to know/i)).toBeInTheDocument();
      expect(screen.getByRole('textbox')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /continue to payment/i })).toBeInTheDocument();
    });

    it('should show character count', () => {
      // Arrange
      const onSubmit = vi.fn();

      // Act
      render(<ChatInput onSubmit={onSubmit} />);

      // Assert
      expect(screen.getByText('0/200 characters')).toBeInTheDocument();
    });

    it('should disable submit button when query is empty', () => {
      // Arrange
      const onSubmit = vi.fn();

      // Act
      render(<ChatInput onSubmit={onSubmit} />);

      // Assert
      const button = screen.getByRole('button', { name: /continue to payment/i });
      expect(button).toBeDisabled();
    });
  });

  describe('User Input', () => {
    it('should update character count as user types', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');

      // Act
      fireEvent.change(textarea, { target: { value: 'Test query about UK universities' } });

      // Assert
      expect(screen.getByText('32/200 characters')).toBeInTheDocument();
    });

    it('should enable submit button when query has content', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const button = screen.getByRole('button', { name: /continue to payment/i });

      // Act
      fireEvent.change(textarea, { target: { value: 'UK universities' } });

      // Assert
      expect(button).not.toBeDisabled();
    });

    it('should respect 200 character maxLength', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox') as HTMLTextAreaElement;

      // Assert
      expect(textarea.maxLength).toBe(200);
    });
  });

  describe('UK Validation - Happy Path', () => {
    it('should accept query with "UK"', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act
      fireEvent.change(textarea, { target: { value: 'What are the best UK universities?' } });
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).toHaveBeenCalledWith('What are the best UK universities?');
      expect(onSubmit).toHaveBeenCalledTimes(1);
    });

    it('should accept query with "United Kingdom"', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act
      fireEvent.change(textarea, { target: { value: 'Studying in the United Kingdom' } });
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).toHaveBeenCalledWith('Studying in the United Kingdom');
    });

    it('should accept query with "Britain"', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act
      fireEvent.change(textarea, { target: { value: 'Universities in Britain' } });
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).toHaveBeenCalledWith('Universities in Britain');
    });

    it('should accept query with "British"', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act
      fireEvent.change(textarea, { target: { value: 'British universities for engineering' } });
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).toHaveBeenCalledWith('British universities for engineering');
    });

    it('should accept query with "England"', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act
      fireEvent.change(textarea, { target: { value: 'Universities in England' } });
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).toHaveBeenCalledWith('Universities in England');
    });

    it('should accept query with "Scotland"', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act
      fireEvent.change(textarea, { target: { value: 'Studying in Scotland' } });
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).toHaveBeenCalledWith('Studying in Scotland');
    });

    it('should accept query with "Wales"', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act
      fireEvent.change(textarea, { target: { value: 'Universities in Wales' } });
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).toHaveBeenCalledWith('Universities in Wales');
    });

    it('should accept query with "London"', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act
      fireEvent.change(textarea, { target: { value: 'Universities in London' } });
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).toHaveBeenCalledWith('Universities in London');
    });

    it('should accept query with "Oxford"', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act
      fireEvent.change(textarea, { target: { value: 'Studying at Oxford' } });
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).toHaveBeenCalledWith('Studying at Oxford');
    });

    it('should accept query with "Cambridge"', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act
      fireEvent.change(textarea, { target: { value: 'Cambridge University requirements' } });
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).toHaveBeenCalledWith('Cambridge University requirements');
    });

    it('should be case-insensitive for UK keywords', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act
      fireEvent.change(textarea, { target: { value: 'uNiVeRsItIeS iN tHe uk' } });
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).toHaveBeenCalledWith('uNiVeRsItIeS iN tHe uk');
    });
  });

  describe('UK Validation - Error Cases', () => {
    it('should reject query without UK keywords', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act
      fireEvent.change(textarea, { target: { value: 'What are the best universities in USA?' } });
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).not.toHaveBeenCalled();
      expect(screen.getByText(/your question must be related to studying in the uk/i)).toBeInTheDocument();
    });

    it('should reject query about US universities', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act
      fireEvent.change(textarea, { target: { value: 'MIT computer science programs' } });
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).not.toHaveBeenCalled();
      expect(screen.getByText(/your question must be related to studying in the uk/i)).toBeInTheDocument();
    });

    it('should reject query about Canadian universities', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act
      fireEvent.change(textarea, { target: { value: 'Universities in Toronto' } });
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).not.toHaveBeenCalled();
      expect(screen.getByText(/your question must be related to studying in the uk/i)).toBeInTheDocument();
    });

    it('should clear error when user starts typing UK keyword', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act - First submit invalid
      fireEvent.change(textarea, { target: { value: 'Universities in USA' } });
      fireEvent.submit(form);
      expect(screen.getByText(/your question must be related to studying in the uk/i)).toBeInTheDocument();

      // Act - Then fix the query
      fireEvent.change(textarea, { target: { value: 'Universities in UK' } });

      // Assert
      expect(screen.queryByText(/your question must be related to studying in the uk/i)).not.toBeInTheDocument();
    });
  });

  describe('Character Limit Validation', () => {
    it('should reject empty query', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const form = screen.getByRole('textbox').closest('form')!;

      // Act
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).not.toHaveBeenCalled();
      expect(screen.getByText('Please enter a question')).toBeInTheDocument();
    });

    it('should reject query with only whitespace', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act
      fireEvent.change(textarea, { target: { value: '   ' } });
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).not.toHaveBeenCalled();
      expect(screen.getByText('Please enter a question')).toBeInTheDocument();
    });

    it('should reject query over 200 characters', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;
      const longQuery = 'UK universities '.repeat(20); // Over 200 chars

      // Act
      fireEvent.change(textarea, { target: { value: longQuery } });
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).not.toHaveBeenCalled();
      expect(screen.getByText('Question must be less than 200 characters')).toBeInTheDocument();
    });

    it('should accept query exactly at 200 characters with UK keyword', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;
      const exactQuery = 'UK universities for Computer Science '.repeat(5).slice(0, 197) + ' UK'; // Exactly 200

      // Act
      fireEvent.change(textarea, { target: { value: exactQuery } });
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).toHaveBeenCalled();
    });

    it('should trim whitespace before validation', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act
      fireEvent.change(textarea, { target: { value: '  UK universities  ' } });
      fireEvent.submit(form);

      // Assert
      expect(onSubmit).toHaveBeenCalledWith('UK universities');
    });
  });

  describe('Disabled State', () => {
    it('should disable textarea when disabled prop is true', () => {
      // Arrange
      const onSubmit = vi.fn();

      // Act
      render(<ChatInput onSubmit={onSubmit} disabled={true} />);

      // Assert
      expect(screen.getByRole('textbox')).toBeDisabled();
      expect(screen.getByRole('button')).toBeDisabled();
    });

    it('should disable textarea when isLoading is true', () => {
      // Arrange
      const onSubmit = vi.fn();

      // Act
      render(<ChatInput onSubmit={onSubmit} isLoading={true} />);

      // Assert
      expect(screen.getByRole('textbox')).toBeDisabled();
      expect(screen.getByRole('button')).toBeDisabled();
    });

    it('should show "Processing..." when isLoading is true', () => {
      // Arrange
      const onSubmit = vi.fn();

      // Act
      render(<ChatInput onSubmit={onSubmit} isLoading={true} />);

      // Assert
      expect(screen.getByRole('button', { name: /processing/i })).toBeInTheDocument();
    });
  });

  describe('Integration Tests', () => {
    it('should handle complete user flow: type, validate, submit', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act - User types query
      fireEvent.change(textarea, { target: { value: 'What are the visa requirements for studying in the UK?' } });

      // Assert - Character count updated (string is 54 chars, not 61)
      expect(screen.getByText('54/200 characters')).toBeInTheDocument();

      // Act - User submits
      fireEvent.submit(form);

      // Assert - Form submitted
      expect(onSubmit).toHaveBeenCalledWith('What are the visa requirements for studying in the UK?');
      expect(onSubmit).toHaveBeenCalledTimes(1);
    });

    it('should handle error recovery: invalid -> valid -> submit', () => {
      // Arrange
      const onSubmit = vi.fn();
      render(<ChatInput onSubmit={onSubmit} />);
      const textarea = screen.getByRole('textbox');
      const form = textarea.closest('form')!;

      // Act - Submit invalid query
      fireEvent.change(textarea, { target: { value: 'Universities in France' } });
      fireEvent.submit(form);

      // Assert - Error shown
      expect(screen.getByText(/your question must be related to studying in the uk/i)).toBeInTheDocument();
      expect(onSubmit).not.toHaveBeenCalled();

      // Act - Fix query
      fireEvent.change(textarea, { target: { value: 'UK universities for medicine' } });
      fireEvent.submit(form);

      // Assert - Successfully submitted
      expect(screen.queryByText(/your question must be related to studying in the uk/i)).not.toBeInTheDocument();
      expect(onSubmit).toHaveBeenCalledWith('UK universities for medicine');
      expect(onSubmit).toHaveBeenCalledTimes(1);
    });
  });
});
