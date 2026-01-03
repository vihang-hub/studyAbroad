/**
 * ReportCard component
 * T118: Display individual report in sidebar/list with status and metadata
 */

'use client';

import { useRouter } from 'next/navigation';
import type { Report, ReportStatus } from '@/types/report';

interface ReportCardProps {
  report: Report;
  compact?: boolean;
}

/**
 * Get status badge styling based on report status
 */
function getStatusBadge(status: ReportStatus): { label: string; className: string } {
  switch (status) {
    case 'completed':
      return {
        label: 'Completed',
        className: 'bg-green-100 text-green-800',
      };
    case 'pending':
    case 'processing':
      return {
        label: 'Processing',
        className: 'bg-blue-100 text-blue-800',
      };
    case 'generating':
      return {
        label: 'Generating',
        className: 'bg-yellow-100 text-yellow-800',
      };
    case 'failed':
      return {
        label: 'Failed',
        className: 'bg-red-100 text-red-800',
      };
    case 'expired':
      return {
        label: 'Expired',
        className: 'bg-gray-100 text-gray-800',
      };
    default:
      return {
        label: 'Unknown',
        className: 'bg-gray-100 text-gray-800',
      };
  }
}

/**
 * Format date for display
 */
function formatDate(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (diffDays === 0) {
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    if (diffHours === 0) {
      const diffMins = Math.floor(diffMs / (1000 * 60));
      return `${diffMins} min${diffMins !== 1 ? 's' : ''} ago`;
    }
    return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
  }

  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;

  return date.toLocaleDateString(undefined, {
    month: 'short',
    day: 'numeric',
    year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined,
  });
}

/**
 * Truncate query text for display
 */
function truncateQuery(query: string, maxLength: number = 60): string {
  if (query.length <= maxLength) return query;
  return `${query.substring(0, maxLength)}...`;
}

export function ReportCard({ report, compact = false }: ReportCardProps) {
  const router = useRouter();
  const statusBadge = getStatusBadge(report.status);

  const handleClick = () => {
    router.push(`/report/${report.id}`);
  };

  return (
    <div
      onClick={handleClick}
      className={`
        cursor-pointer rounded-lg border border-gray-200 bg-white p-4
        transition-all duration-200 hover:border-blue-400 hover:shadow-md
        ${compact ? 'space-y-2' : 'space-y-3'}
      `}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          handleClick();
        }
      }}
    >
      <div className="flex items-start justify-between gap-2">
        <h3
          className={`
            font-medium text-gray-900 line-clamp-2
            ${compact ? 'text-sm' : 'text-base'}
          `}
          title={report.query}
        >
          {truncateQuery(report.query, compact ? 50 : 80)}
        </h3>
        <span
          className={`
            flex-shrink-0 rounded-full px-2 py-1 text-xs font-medium
            ${statusBadge.className}
          `}
        >
          {statusBadge.label}
        </span>
      </div>

      <div className={`flex items-center gap-4 ${compact ? 'text-xs' : 'text-sm'} text-gray-500`}>
        <div className="flex items-center gap-1">
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
            />
          </svg>
          <span>{formatDate(report.createdAt)}</span>
        </div>

        {report.expires_at && report.status !== 'expired' && (
          <div className="flex items-center gap-1 text-orange-600">
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span>
              Expires
              {' '}
              {formatDate(report.expires_at)}
            </span>
          </div>
        )}
      </div>

      {!compact && report.content?.total_citations && (
        <div className="flex items-center gap-1 text-xs text-gray-500">
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <span>
            {report.content.total_citations}
            {' '}
            sources cited
          </span>
        </div>
      )}
    </div>
  );
}
