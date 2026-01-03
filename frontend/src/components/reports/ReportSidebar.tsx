/**
 * ReportSidebar component
 * T119: Display recent reports in sidebar with link to full history
 */

'use client';

import Link from 'next/link';
import { useReports } from '@/hooks/useReports';
import { ReportCard } from './ReportCard';

interface ReportSidebarProps {
  maxReports?: number;
}

export function ReportSidebar({ maxReports = 10 }: ReportSidebarProps) {
  const {
    reports, isLoading, error, refetch,
  } = useReports({
    limit: maxReports,
    autoFetch: true,
  });

  // Loading state
  if (isLoading) {
    return (
      <div className="w-full rounded-lg border border-gray-200 bg-white p-6">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">Recent Reports</h2>
        </div>
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="h-24 animate-pulse rounded-lg bg-gray-100"
            />
          ))}
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="w-full rounded-lg border border-red-200 bg-red-50 p-6">
        <div className="mb-2 flex items-center gap-2 text-red-800">
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <h3 className="font-medium">Failed to load reports</h3>
        </div>
        <p className="mb-3 text-sm text-red-700">{error}</p>
        <button
          onClick={refetch}
          className="text-sm text-red-800 underline hover:text-red-900"
        >
          Try again
        </button>
      </div>
    );
  }

  // Empty state
  if (reports.length === 0) {
    return (
      <div className="w-full rounded-lg border border-gray-200 bg-white p-6">
        <h2 className="mb-4 text-lg font-semibold text-gray-900">Recent Reports</h2>
        <div className="rounded-lg border border-dashed border-gray-300 bg-gray-50 p-8 text-center">
          <svg
            className="mx-auto mb-3 h-12 w-12 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <p className="mb-1 text-sm font-medium text-gray-900">No reports yet</p>
          <p className="mb-4 text-sm text-gray-500">
            Start a conversation to generate your first research report
          </p>
          <Link
            href="/chat"
            className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 4v16m8-8H4"
              />
            </svg>
            Start Chat
          </Link>
        </div>
      </div>
    );
  }

  // Reports list
  return (
    <div className="w-full rounded-lg border border-gray-200 bg-white p-6">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-900">Recent Reports</h2>
        <Link
          href="/reports"
          className="text-sm font-medium text-blue-600 hover:text-blue-700"
        >
          View all
        </Link>
      </div>

      <div className="space-y-3">
        {reports.map((report) => (
          <ReportCard key={report.id} report={report} compact />
        ))}
      </div>

      {reports.length >= maxReports && (
        <div className="mt-4 border-t border-gray-200 pt-4 text-center">
          <Link
            href="/reports"
            className="inline-flex items-center gap-2 text-sm font-medium text-blue-600 hover:text-blue-700"
          >
            <span>View all reports</span>
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
          </Link>
        </div>
      )}
    </div>
  );
}
