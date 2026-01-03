'use client';

import { useState, useEffect } from 'react';
import { ReportSection } from '@/components/reports/ReportSection';
import type { Citation } from '@/types/report';

interface Section {
  section_num: number;
  heading: string;
  content: string;
  citations: Citation[];
}

interface StreamingResponseProps {
  reportId: string;
  onComplete?: () => void;
  onError?: (error: string) => void;
}

/**
 * StreamingResponse Component
 *
 * Implements Server-Sent Events (SSE) streaming per specification Section 5 & 9
 * Provides Gemini-style progressive rendering of AI-generated report sections
 *
 * @param reportId - The report ID to stream
 * @param onComplete - Callback when streaming completes
 * @param onError - Callback when an error occurs
 */
export function StreamingResponse({ reportId, onComplete, onError }: StreamingResponseProps) {
  const [sections, setSections] = useState<Section[]>([]);
  const [currentChunk, setCurrentChunk] = useState<string>('');
  const [progress, setProgress] = useState<{ current: number; total: number }>({ current: 0, total: 10 });
  const [isComplete, setIsComplete] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const eventSource = new EventSource(
      `${apiUrl}/stream/reports/${reportId}`,
      { withCredentials: true },
    );

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        switch (data.type) {
          case 'start':
            console.log('Streaming started for report:', data.report_id);
            break;

          case 'chunk':
            // Accumulate raw text chunks for progressive rendering
            setCurrentChunk((prev) => prev + data.content);
            break;

          case 'section':
            // Complete section received
            setSections((prev) => [...prev, {
              section_num: data.section_num,
              heading: data.heading,
              content: data.content,
              citations: data.citations,
            }]);
            setCurrentChunk(''); // Clear chunk buffer
            break;

          case 'progress':
            setProgress({
              current: data.current_section,
              total: data.total_sections,
            });
            break;

          case 'complete':
            setIsComplete(true);
            eventSource.close();
            onComplete?.();
            break;

          case 'error':
            const errorMsg = data.message || 'Unknown error occurred';
            setError(errorMsg);
            onError?.(errorMsg);
            eventSource.close();
            break;

          default:
            console.warn('Unknown event type:', data.type);
        }
      } catch (err) {
        console.error('Failed to parse SSE data:', err);
      }
    };

    eventSource.onerror = (err) => {
      console.error('SSE connection error:', err);
      const errorMsg = 'Streaming connection lost. Please try again.';
      setError(errorMsg);
      onError?.(errorMsg);
      eventSource.close();
    };

    // Cleanup on unmount
    return () => {
      eventSource.close();
    };
  }, [reportId, onComplete, onError]);

  // Show error state
  if (error) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-6">
        <h3 className="text-lg font-semibold text-red-900 mb-2">
          Error Generating Report
        </h3>
        <p className="text-red-700">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Progress indicator */}
      <div className="sticky top-0 z-10 bg-white border-b border-gray-200 p-4 -mx-4">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">
              Generating Report
            </span>
            <span className="text-sm text-gray-600">
              Section
              {' '}
              {progress.current}
              {' '}
              of
              {' '}
              {progress.total}
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${(progress.current / progress.total) * 100}%` }}
            />
          </div>
        </div>
      </div>

      {/* Rendered sections */}
      <div className="space-y-6">
        {sections.map((section) => (
          <div
            key={section.section_num}
            className="animate-fade-in"
          >
            <ReportSection
              section={{ ...section, title: section.heading }}
              index={section.section_num || 0}
            />
          </div>
        ))}

        {/* Current chunk being streamed (progressive rendering) */}
        {currentChunk && !isComplete && (
          <div className="animate-pulse">
            <div className="rounded-lg border border-gray-200 bg-gray-50 p-6">
              <p className="text-gray-600 whitespace-pre-wrap">{currentChunk}</p>
            </div>
          </div>
        )}
      </div>

      {/* Completion message */}
      {isComplete && (
        <div className="rounded-lg border border-green-200 bg-green-50 p-6 text-center animate-fade-in">
          <div className="flex items-center justify-center mb-2">
            <svg
              className="w-6 h-6 text-green-600 mr-2"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M5 13l4 4L19 7" />
            </svg>
            <span className="text-lg font-semibold text-green-900">
              Report Generation Complete
            </span>
          </div>
          <p className="text-green-700 text-sm">
            Your report is now available for 30 days
          </p>
        </div>
      )}
    </div>
  );
}
