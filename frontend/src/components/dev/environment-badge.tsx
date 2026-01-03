/**
 * Environment Badge Component
 * Shows current environment mode and active feature flags
 * Only visible in non-production environments
 */

'use client';

import React, { useState } from 'react';
import { useFeatureFlags } from '@/providers/feature-flag-provider';

export function EnvironmentBadge() {
  const { flags, environmentMode, isLoading } = useFeatureFlags();
  const [isExpanded, setIsExpanded] = useState(false);

  // Only show in non-production environments
  if (environmentMode === 'production' || isLoading) {
    return null;
  }

  const envColors = {
    development: 'bg-green-600',
    test: 'bg-yellow-600',
    production: 'bg-red-600',
  };

  const badgeColor = envColors[environmentMode];

  return (
    <div className="fixed bottom-4 right-4 z-50">
      {/* Collapsed Badge */}
      {!isExpanded && (
        <button
          onClick={() => setIsExpanded(true)}
          className={`${badgeColor} rounded-lg px-4 py-2 text-xs font-semibold text-white shadow-lg transition-all hover:scale-105`}
          aria-label="Expand environment info"
        >
          {environmentMode.toUpperCase()}
        </button>
      )}

      {/* Expanded Panel */}
      {isExpanded && (
        <div className="rounded-lg bg-white p-4 shadow-xl ring-1 ring-black ring-opacity-5">
          <div className="flex items-center justify-between gap-3 mb-3">
            <div className={`${badgeColor} rounded px-3 py-1 text-xs font-semibold text-white`}>
              {environmentMode.toUpperCase()}
            </div>
            <button
              onClick={() => setIsExpanded(false)}
              className="text-gray-400 hover:text-gray-600"
              aria-label="Collapse environment info"
            >
              <svg
                className="h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>

          <div className="space-y-2">
            <h3 className="text-xs font-semibold text-gray-900">Feature Flags</h3>
            <div className="space-y-1">
              {Object.entries(flags).map(([key, value]) => (
                <div key={key} className="flex items-center justify-between text-xs">
                  <span className="text-gray-600">{key}</span>
                  <span
                    className={`rounded px-2 py-0.5 font-medium ${
                      value
                        ? 'bg-green-100 text-green-700'
                        : 'bg-gray-100 text-gray-600'
                    }`}
                  >
                    {value ? 'ON' : 'OFF'}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-3 border-t border-gray-200 pt-3">
            <div className="text-xs text-gray-500">
              <div className="flex justify-between">
                <span>Database:</span>
                <span className="font-medium">
                  {flags.ENABLE_SUPABASE ? 'Supabase' : 'Mock'}
                </span>
              </div>
              <div className="flex justify-between mt-1">
                <span>Payments:</span>
                <span className="font-medium">
                  {flags.ENABLE_PAYMENTS ? 'Stripe' : 'Bypassed'}
                </span>
              </div>
            </div>
          </div>

          {environmentMode === 'development' && (
            <div className="mt-3 rounded bg-blue-50 p-2 text-xs text-blue-800">
              <strong>Dev Mode:</strong>
              {' '}
              All features are mocked for easy testing
            </div>
          )}

          {environmentMode === 'test' && (
            <div className="mt-3 rounded bg-yellow-50 p-2 text-xs text-yellow-800">
              <strong>Test Mode:</strong>
              {' '}
              Using test database and payment bypass
            </div>
          )}
        </div>
      )}
    </div>
  );
}
