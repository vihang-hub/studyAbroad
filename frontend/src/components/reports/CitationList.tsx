/**
 * Citation list component
 * Displays sources with links
 */

'use client';

import type { Citation } from '@/types/report';

export interface CitationListProps {
  citations: Citation[];
}

export function CitationList({ citations }: CitationListProps) {
  if (!citations || citations.length === 0) {
    return null;
  }

  return (
    <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
      <h3 className="text-sm font-semibold text-gray-700 mb-3">Sources</h3>
      <ul className="space-y-2">
        {citations.map((citation, index) => (
          <li key={index} className="text-sm">
            <a
              href={citation.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-700 hover:underline flex items-start gap-2"
            >
              <span className="text-gray-500">
                [
                {index + 1}
                ]
              </span>
              <div>
                <div className="font-medium">{citation.title}</div>
                {citation.snippet && (
                  <div className="text-gray-600 italic mt-1">
                    &quot;
                    {citation.snippet}
                    &quot;
                  </div>
                )}
                <div className="text-gray-400 text-xs mt-1">{citation.url}</div>
              </div>
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
