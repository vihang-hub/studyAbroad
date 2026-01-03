/**
 * Payment status display (Portable)
 * Shows current payment state with appropriate styling
 */

'use client';

import type { PaymentStatus as PaymentStatusType } from '../../types/payment';

export interface PaymentStatusProps {
  status: PaymentStatusType;
  amount?: number;
  currency?: string;
  errorMessage?: string;
  className?: string;
}

const statusConfig: Record<PaymentStatusType, {
  label: string;
  color: string;
  bg: string;
  border: string;
}> = {
  pending: {
    label: 'Payment Pending',
    color: 'text-yellow-700',
    bg: 'bg-yellow-50',
    border: 'border-yellow-200',
  },
  succeeded: {
    label: 'Payment Successful',
    color: 'text-green-700',
    bg: 'bg-green-50',
    border: 'border-green-200',
  },
  failed: {
    label: 'Payment Failed',
    color: 'text-red-700',
    bg: 'bg-red-50',
    border: 'border-red-200',
  },
  refunded: {
    label: 'Payment Refunded',
    color: 'text-gray-700',
    bg: 'bg-gray-50',
    border: 'border-gray-200',
  },
};

export function PaymentStatus({
  status,
  amount = undefined,
  currency = 'gbp',
  errorMessage = undefined,
  className = '',
}: PaymentStatusProps) {
  const config = statusConfig[status];

  return (
    <div className={`p-4 rounded-lg border ${config.bg} ${config.border} ${className}`}>
      <div className="flex items-center gap-2">
        <div className={`font-medium ${config.color}`}>{config.label}</div>
        {amount && status === 'succeeded' && (
          <div className="text-sm text-gray-600">
            (
            {new Intl.NumberFormat('en-GB', {
              style: 'currency',
              currency,
            }).format(amount / 100)}
            )
          </div>
        )}
      </div>
      {errorMessage && status === 'failed' && (
        <p className="mt-2 text-sm text-red-600">{errorMessage}</p>
      )}
    </div>
  );
}
