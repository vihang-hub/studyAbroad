/**
 * Chat page - Main interface for generating reports
 * User Story 1: Generate Paid Report
 */

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { ChatInput } from '@/components/chat/ChatInput';
import { MessageList, Message } from '@/components/chat/MessageList';
import { usePayment } from '@/hooks/usePayment';

export default function ChatPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [, setCurrentQuery] = useState('');

  const { isLoading, error, createCheckout } = usePayment({
    apiEndpoint: '/api/reports/initiate',
    onSuccess: (reportId) => {
      router.push(`/chat/success?reportId=${reportId}`);
    },
    onError: (errorMessage) => {
      console.error('Payment error:', errorMessage);
    },
  });

  const handleQuerySubmit = async (query: string) => {
    setCurrentQuery(query);

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: query,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);

    // Create checkout and initiate payment
    await createCheckout(query);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          UK Study & Migration Research
        </h1>
        <p className="text-gray-600">
          Ask a question and receive a comprehensive AI-generated research report (£2.99)
        </p>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      <div className="mb-8">
        <MessageList messages={messages} />
      </div>

      <div className="sticky bottom-0 bg-white border-t border-gray-200 pt-6 pb-4">
        <ChatInput
          onSubmit={handleQuerySubmit}
          disabled={isLoading}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
}
