/**
 * Mock API responses for testing
 * Provides realistic mock data for API endpoints
 */

import { vi } from 'vitest';
import type { Report } from '@/types/report';

export const mockReports: Report[] = [
  {
    id: 'report-1',
    userId: 'user-123',
    query: 'Computer Science in UK',
    country: 'UK',
    subject: 'Computer Science',
    status: 'completed',
    createdAt: '2026-01-01T00:00:00Z',
    updatedAt: '2026-01-01T00:00:00Z',
    expires_at: '2026-01-31T00:00:00Z',
    content: {
      total_citations: 5,
      sections: {
        overview: 'Overview of Computer Science programs in the UK',
        universities: 'Top universities for Computer Science',
        requirements: 'Entry requirements and application process',
      },
    },
    citations: [
      {
        id: 'cite-1',
        url: 'https://example.com/source1',
        title: 'UK University Guide',
        accessed_at: '2026-01-01T00:00:00Z',
      },
    ],
  },
  {
    id: 'report-2',
    userId: 'user-123',
    query: 'Nursing in UK',
    country: 'UK',
    subject: 'Nursing',
    status: 'completed',
    createdAt: '2026-01-02T00:00:00Z',
    updatedAt: '2026-01-02T00:00:00Z',
    expires_at: '2026-02-01T00:00:00Z',
    content: {
      total_citations: 3,
      sections: {
        overview: 'Overview of Nursing programs in the UK',
      },
    },
    citations: [],
  },
  {
    id: 'report-3',
    userId: 'user-123',
    query: 'Business Management in UK',
    country: 'UK',
    subject: 'Business Management',
    status: 'generating',
    createdAt: '2026-01-03T00:00:00Z',
    updatedAt: '2026-01-03T00:00:00Z',
    expires_at: '2026-02-02T00:00:00Z',
    content: { sections: {} },
    citations: [],
  },
];

export const mockPayment = {
  session_id: 'cs_test_123456789',
  url: 'https://checkout.stripe.com/test/session',
  status: 'open',
};

export const mockUser = {
  id: 'test-user-123',
  email: 'test@example.com',
  firstName: 'Test',
  lastName: 'User',
  fullName: 'Test User',
  imageUrl: 'https://example.com/avatar.jpg',
};

// Mock fetch for API calls
export const createMockFetch = () => {
  return vi.fn((url: string, options?: RequestInit) => {
    const method = options?.method || 'GET';

    // Mock GET /api/reports
    if (url.includes('/api/reports') && method === 'GET') {
      return Promise.resolve({
        ok: true,
        status: 200,
        json: async () => mockReports,
        headers: new Headers({ 'Content-Type': 'application/json' }),
      } as Response);
    }

    // Mock GET /api/reports/:id
    if (url.match(/\/api\/reports\/[^/]+$/) && method === 'GET') {
      const reportId = url.split('/').pop();
      const report = mockReports.find(r => r.id === reportId);

      if (report) {
        return Promise.resolve({
          ok: true,
          status: 200,
          json: async () => report,
          headers: new Headers({ 'Content-Type': 'application/json' }),
        } as Response);
      }

      return Promise.resolve({
        ok: false,
        status: 404,
        json: async () => ({ error: 'Report not found' }),
        headers: new Headers({ 'Content-Type': 'application/json' }),
      } as Response);
    }

    // Mock POST /api/reports
    if (url.includes('/api/reports') && method === 'POST') {
      const newReport: Report = {
        ...mockReports[0],
        id: `report-${Date.now()}`,
        status: 'pending',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      return Promise.resolve({
        ok: true,
        status: 201,
        json: async () => newReport,
        headers: new Headers({ 'Content-Type': 'application/json' }),
      } as Response);
    }

    // Mock POST /api/payments/create-checkout-session
    if (url.includes('/api/payments/create-checkout-session') && method === 'POST') {
      return Promise.resolve({
        ok: true,
        status: 200,
        json: async () => mockPayment,
        headers: new Headers({ 'Content-Type': 'application/json' }),
      } as Response);
    }

    // Mock GET /api/user
    if (url.includes('/api/user') && method === 'GET') {
      return Promise.resolve({
        ok: true,
        status: 200,
        json: async () => mockUser,
        headers: new Headers({ 'Content-Type': 'application/json' }),
      } as Response);
    }

    // Default response for unknown endpoints
    return Promise.resolve({
      ok: true,
      status: 200,
      json: async () => ({}),
      headers: new Headers({ 'Content-Type': 'application/json' }),
    } as Response);
  });
};

// Setup global fetch mock
export function setupFetchMock(): void {
  global.fetch = createMockFetch();
}

// Reset fetch mock
export function resetFetchMock(): void {
  if (global.fetch && vi.isMockFunction(global.fetch)) {
    vi.mocked(global.fetch).mockClear();
  }
}
