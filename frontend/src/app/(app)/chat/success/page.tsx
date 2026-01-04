/**
 * Payment success page
 * Polls for report generation completion
 */

'use client';

import { useEffect, useState, useCallback } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAuthenticatedApi } from '@/hooks/useAuthenticatedApi';
import type { Report, ReportStatus } from '@/types/report';

export default function PaymentSuccessPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const reportId = searchParams.get('reportId');
  const { get: authGet } = useAuthenticatedApi();

  const [status, setStatus] = useState<ReportStatus>('pending');
  const [error, setError] = useState<string | null>(null);

  const pollReport = useCallback(async () => {
    if (!reportId) return null;

    try {
      const response = await authGet<Report>(`/reports/${reportId}`);

      if (response.error || !response.data) {
        setError(response.error?.message || 'Failed to fetch report');
        return 'error';
      }

      const report = response.data;
      setStatus(report.status);

      if (report.status === 'completed') {
        router.push(`/report/${reportId}`);
        return 'completed';
      } else if (report.status === 'failed') {
        setError('Report generation failed');
        return 'failed';
      }

      return 'pending';
    } catch (err) {
      console.error('Polling error:', err);
      setError('Failed to check report status');
      return 'error';
    }
  }, [reportId, authGet, router]);

  useEffect(() => {
    if (!reportId) {
      router.push('/chat');
      return;
    }

    // Poll for report status every 2 seconds
    const pollInterval = setInterval(async () => {
      const result = await pollReport();
      if (result && result !== 'pending') {
        clearInterval(pollInterval);
      }
    }, 2000);

    // Initial poll
    pollReport();

    return () => clearInterval(pollInterval);
  }, [reportId, router, pollReport]);

  return (
    <div className="max-w-2xl mx-auto text-center py-12">
      <div className="mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
          <svg
            className="w-8 h-8 text-green-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Payment Successful!</h1>
        <p className="text-gray-600">Your report is being generated...</p>
      </div>

      {error ? (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">{error}</p>
          <button
            onClick={() => router.push('/chat')}
            className="mt-4 text-sm text-blue-600 hover:text-blue-700"
          >
            Return to chat
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="flex items-center justify-center gap-2">
            <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
            <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
            <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
          </div>
          <p className="text-sm text-gray-600">
            Status:
            {' '}
            <span className="font-medium capitalize">{status}</span>
          </p>
          <p className="text-xs text-gray-500">
            This usually takes about 60 seconds. Please don't close this page.
          </p>
        </div>
      )}
    </div>
  );
}
