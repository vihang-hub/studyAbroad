/**
 * Report section component
 * Renders a single section with markdown support
 */

'use client';

import ReactMarkdown from 'react-markdown';
import type { ReportSection as ReportSectionType } from '@/types/report';
import { CitationList } from './CitationList';

export interface ReportSectionProps {
  section: ReportSectionType;
  index: number;
}

export function ReportSection({ section, index }: ReportSectionProps) {
  return (
    <section className="mb-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
        <span className="text-blue-600">
          {index}
          .
        </span>
        {section.heading}
      </h2>

      <div className="prose prose-blue max-w-none mb-6">
        <ReactMarkdown>{section.content}</ReactMarkdown>
      </div>

      {section.citations && section.citations.length > 0 && (
        <CitationList citations={section.citations} />
      )}
    </section>
  );
}
