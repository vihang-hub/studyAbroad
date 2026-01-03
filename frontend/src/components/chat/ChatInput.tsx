/**
 * Chat input component
 * Subject input with UK-only validation
 */

'use client';

import { useState } from 'react';

export interface ChatInputProps {
  onSubmit: (query: string) => void;
  disabled?: boolean;
  isLoading?: boolean;
}

const UK_KEYWORDS = [
  'uk', 'united kingdom', 'britain', 'british', 'england', 'scotland',
  'wales', 'northern ireland', 'london', 'oxford', 'cambridge',
  'russell group', 'ucas',
];

export function ChatInput({ onSubmit, disabled = false, isLoading = false }: ChatInputProps) {
  const [query, setQuery] = useState('');
  const [error, setError] = useState<string | null>(null);

  const validateUKQuery = (text: string): boolean => {
    const lowerText = text.toLowerCase();
    return UK_KEYWORDS.some((keyword) => lowerText.includes(keyword));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const trimmedQuery = query.trim();

    // Validation
    if (!trimmedQuery) {
      setError('Please enter a question');
      return;
    }

    if (trimmedQuery.length > 200) {
      setError('Question must be less than 200 characters');
      return;
    }

    if (!validateUKQuery(trimmedQuery)) {
      setError(
        'Your question must be related to studying in the UK. '
        + 'Please include UK-specific keywords (e.g., "UK universities", "studying in Britain").',
      );
      return;
    }

    onSubmit(trimmedQuery);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
          What would you like to know about studying in the UK?
        </label>
        <textarea
          id="query"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setError(null);
          }}
          placeholder="E.g., What are the best universities for Computer Science in the UK?"
          rows={4}
          maxLength={200}
          disabled={disabled || isLoading}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none disabled:opacity-50 disabled:cursor-not-allowed"
        />
        <div className="flex justify-between items-center mt-1">
          <span className="text-xs text-gray-500">
            {query.length}
            /200 characters
          </span>
          {error && <span className="text-xs text-red-600">{error}</span>}
        </div>
      </div>

      <button
        type="submit"
        disabled={disabled || isLoading || !query.trim()}
        className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
      >
        {isLoading ? 'Processing...' : 'Continue to Payment'}
      </button>
    </form>
  );
}
