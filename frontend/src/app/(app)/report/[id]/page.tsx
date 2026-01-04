/**
 * Report detail page
 * Displays full AI-generated report with all 10 sections
 */

'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { api } from '@/lib/api-client';
import type { Report } from '@/types/report';
import { ExecutiveSummary } from '@/components/reports/ExecutiveSummary';
import { ReportSection } from '@/components/reports/ReportSection';

export default function ReportDetailPage() {
  const params = useParams();
  const router = useRouter();
  const reportId = params.id as string;

  const [report, setReport] = useState<Report | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchReport = async () => {
      try {
        setIsLoading(true);
        const response = await api.get<Report>(`/reports/${reportId}`);

        if (response.error || !response.data) {
          setError(response.error?.message || 'Failed to load report');
          return;
        }

        setReport(response.data);
      } catch (err) {
        setError('Failed to load report');
      } finally {
        setIsLoading(false);
      }
    };

    fetchReport();
  }, [reportId]);

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto text-center py-12">
        <div className="animate-spin w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full mx-auto mb-4" />
        <p className="text-gray-600">Loading report...</p>
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="max-w-4xl mx-auto text-center py-12">
        <div className="p-6 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-600 mb-4">{error || 'Report not found'}</p>
          <button
            onClick={() => router.push('/chat')}
            className="text-blue-600 hover:text-blue-700"
          >
            Return to chat
          </button>
        </div>
      </div>
    );
  }

  // Show progress indicator for generating/pending states
  if (report.status === 'generating' || report.status === 'pending') {
    return (
      <div className="max-w-4xl mx-auto text-center py-12">
        <div className="p-8 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="animate-spin w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Generating Your Report
          </h2>
          <p className="text-gray-600 mb-4">
            Our AI is researching and compiling your comprehensive report. This usually takes about 60 seconds.
          </p>
          <p className="text-sm text-gray-500">
            Status:
            {' '}
            <span className="font-medium capitalize">{report.status}</span>
          </p>
        </div>
      </div>
    );
  }

  // Show error state
  if (report.status === 'failed') {
    return (
      <div className="max-w-4xl mx-auto text-center py-12">
        <div className="p-6 bg-red-50 border border-red-200 rounded-lg">
          <h2 className="text-xl font-semibold text-red-900 mb-2">
            Report Generation Failed
          </h2>
          <p className="text-red-600 mb-4">An error occurred during generation</p>
          <button
            onClick={() => router.push('/chat')}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  // Show expired state
  if (report.status === 'expired') {
    return (
      <div className="max-w-4xl mx-auto text-center py-12">
        <div className="p-6 bg-yellow-50 border border-yellow-200 rounded-lg">
          <h2 className="text-xl font-semibold text-yellow-900 mb-2">
            Report Expired
          </h2>
          <p className="text-yellow-700 mb-4">
            This report has expired after 30 days and is no longer available.
          </p>
          <button
            onClick={() => router.push('/chat')}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Generate New Report
          </button>
        </div>
      </div>
    );
  }

  // Show completed report
  if (!report.content) {
    return (
      <div className="max-w-4xl mx-auto text-center py-12">
        <p className="text-gray-600">Report content is not available</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6 flex items-center justify-between">
        <button
          onClick={() => router.push('/chat')}
          className="text-blue-600 hover:text-blue-700 flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Chat
        </button>

        <div className="text-sm text-gray-500">
          Expires:
          {' '}
          {report.expires_at ? new Date(report.expires_at).toLocaleDateString() : 'N/A'}
        </div>
      </div>

      <ExecutiveSummary
        summary={report.content.summary}
        query={report.content.query}
        totalCitations={report.content.total_citations}
        generatedAt={new Date(report.content.generated_at)}
      />

      <div className="space-y-8">
        {report.content.sections.map((section, index) => (
          <ReportSection key={index} section={section} index={index + 1} />
        ))}
      </div>

      <div className="mt-12 border-t border-gray-200 pt-6 text-center">
        <p className="text-sm text-gray-500">
          Report generated by AI •
          {' '}
          {report.content.total_citations}
          {' '}
          sources cited
        </p>
      </div>
    </div>
  );
}
