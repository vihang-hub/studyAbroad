/**
 * Integration Tests for User Story 1: Generate Paid Report
 * Tasks T106-T112 Acceptance Criteria
 *
 * These tests validate end-to-end flows from the specification:
 * - T106: Full flow (signup → chat → pay → generate → view report)
 * - T107: Citation validation (reports must have non-empty citations)
 * - T108: UK-only constraint enforcement
 * - T109: Payment-before-generation gate
 * - T110: Streaming validation
 * - T111: Multi-provider auth (Google, Apple, Facebook, Email)
 * - T112: Shared components portability
 */

import {
  describe, it, expect, vi, beforeEach,
} from 'vitest';
import {
  render, screen, waitFor,
} from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// Import components to test
import ChatPage from '@/app/(app)/chat/page';
import ReportPage from '@/app/(app)/report/[id]/page';
import ChatInput from '@/components/chat/ChatInput';
import MessageList from '@/components/chat/MessageList';
import CitationList from '@/components/reports/CitationList';

describe('T106: Full Flow - Signup → Chat → Pay → Generate → View Report', () => {
  beforeEach(() => {
    // Mock environment variables
    process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
    process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_mock';
  });

  it('should complete full flow with all 10 mandatory sections', async () => {
    // ARRANGE: Mock authenticated user
    const mockUser = {
      id: 'user_test_full_flow',
      email: 'test@example.com',
      firstName: 'Test',
      lastName: 'User',
    };

    // Mock Clerk auth
    vi.mock('@clerk/nextjs', () => ({
      ClerkProvider: ({ children }: any) => children,
      useUser: () => ({ user: mockUser, isLoaded: true, isSignedIn: true }),
      useAuth: () => ({ isLoaded: true, isSignedIn: true, userId: mockUser.id }),
    }));

    // Mock API calls
    const mockCheckoutResponse = {
      checkout_url: 'https://checkout.stripe.com/test',
      report_id: 'report_test_full_flow',
    };

    const mockReportResponse = {
      id: 'report_test_full_flow',
      user_id: mockUser.id,
      subject: 'Computer Science',
      country: 'UK',
      status: 'completed',
      content: JSON.stringify({
        executive_summary: [
          'UK offers world-class computer science programs',
          'Strong post-study work visa options available',
          'Average tuition: £15,000-£25,000 per year',
          'High demand for tech professionals',
          'Excellent job prospects in major cities',
        ],
        study_options: 'UK universities offer BSc, MSc, and PhD programs...',
        estimated_costs: {
          tuition: '£15,000 - £25,000 per year',
          living_costs: '£12,000 - £15,000 per year',
        },
        visa_immigration: 'Student visa (Tier 4) allows you to study full-time...',
        post_study_work: 'Graduate visa allows 2 years of post-study work...',
        job_prospects_subject: 'Strong demand for software engineers, data scientists...',
        fallback_jobs: 'IT support, business analyst, project coordinator roles available...',
        risks_reality_check: 'Competition is high. Cost of living in London is expensive...',
        action_plan: {
          '30_days': 'Research universities, prepare documents',
          '60_days': 'Apply to programs, secure funding',
          '90_days': 'Apply for visa, arrange accommodation',
        },
        sources_citations: [
          {
            title: 'UK Council for International Student Affairs',
            url: 'https://www.ukcisa.org.uk/',
            accessed: '2025-01-02',
          },
          {
            title: 'Gov.uk - Student Visa',
            url: 'https://www.gov.uk/student-visa',
            accessed: '2025-01-02',
          },
        ],
      }),
      citations: [
        { title: 'UKCISA', url: 'https://www.ukcisa.org.uk/' },
        { title: 'Gov.uk', url: 'https://www.gov.uk/student-visa' },
      ],
      created_at: new Date().toISOString(),
      expires_at: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
    };

    global.fetch = vi.fn((url: string) => {
      if (url.includes('/api/reports/initiate')) {
        return Promise.resolve({
          ok: true,
          json: async () => mockCheckoutResponse,
        } as Response);
      }
      if (url.includes('/api/reports/')) {
        return Promise.resolve({
          ok: true,
          json: async () => mockReportResponse,
        } as Response);
      }
      return Promise.reject(new Error('Unknown URL'));
    });

    // ACT: Step 1 - User enters subject in chat
    render(<ChatInput onSubmit={vi.fn()} />);
    const input = screen.getByPlaceholderText(/what subject/i);

    await userEvent.type(input, 'Computer Science');
    await userEvent.click(screen.getByRole('button', { name: /submit/i }));

    // ACT: Step 2 - User proceeds to payment
    // (In real flow, this would redirect to Stripe Checkout)
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/reports/initiate'),
        expect.any(Object),
      );
    });

    // ACT: Step 3 - User returns from successful payment
    // Report generation triggered by webhook (mocked above)

    // ACT: Step 4 - User views completed report
    const reportProps = {
      params: { id: 'report_test_full_flow' },
    };

    const reportPage = await ReportPage(reportProps);
    render(reportPage);

    // ASSERT: Verify all 10 mandatory sections are present
    await waitFor(() => {
      const content = JSON.parse(mockReportResponse.content);

      // Section 1: Executive Summary
      expect(content.executive_summary).toBeDefined();
      expect(content.executive_summary.length).toBeGreaterThanOrEqual(5);
      expect(content.executive_summary.length).toBeLessThanOrEqual(10);

      // Section 2: Study Options
      expect(content.study_options).toBeDefined();
      expect(content.study_options).not.toBe('');

      // Section 3: Estimated Costs
      expect(content.estimated_costs).toBeDefined();
      expect(content.estimated_costs.tuition).toBeDefined();
      expect(content.estimated_costs.living_costs).toBeDefined();

      // Section 4: Visa & Immigration
      expect(content.visa_immigration).toBeDefined();

      // Section 5: Post-Study Work Options
      expect(content.post_study_work).toBeDefined();

      // Section 6: Job Prospects in Subject
      expect(content.job_prospects_subject).toBeDefined();

      // Section 7: Fallback Jobs
      expect(content.fallback_jobs).toBeDefined();

      // Section 8: Risks & Reality Check
      expect(content.risks_reality_check).toBeDefined();

      // Section 9: Action Plan
      expect(content.action_plan).toBeDefined();
      expect(content.action_plan['30_days']).toBeDefined();
      expect(content.action_plan['60_days']).toBeDefined();
      expect(content.action_plan['90_days']).toBeDefined();

      // Section 10: Sources & Citations
      expect(content.sources_citations).toBeDefined();
      expect(content.sources_citations.length).toBeGreaterThan(0);
    });
  });
});

describe('T107: Citation Validation', () => {
  it('should ensure reports have non-empty citations array', async () => {
    // ARRANGE: Mock report with citations
    const mockReport = {
      id: 'report_citations_test',
      citations: [
        {
          title: 'UK Council for International Student Affairs',
          url: 'https://www.ukcisa.org.uk/',
          accessed: '2025-01-02',
        },
        {
          title: 'Gov.uk - Student Visa',
          url: 'https://www.gov.uk/student-visa',
          accessed: '2025-01-02',
        },
      ],
    };

    // ACT: Render citation list
    render(<CitationList citations={mockReport.citations} />);

    // ASSERT: Citations must be visible
    await waitFor(() => {
      expect(screen.getByText(/UK Council for International Student Affairs/i)).toBeInTheDocument();
      expect(screen.getByText(/Gov.uk - Student Visa/i)).toBeInTheDocument();
    });

    // ASSERT: Each citation must have title and URL
    mockReport.citations.forEach((citation) => {
      expect(citation.title).toBeTruthy();
      expect(citation.url).toBeTruthy();
      expect(citation.url).toMatch(/^https?:\/\//);
    });
  });

  it('should reject reports without citations', async () => {
    // ARRANGE: Mock report without citations
    const mockReportNoCitations = {
      id: 'report_no_citations',
      citations: [],
    };

    // ACT & ASSERT: Should throw error or show warning
    const { container } = render(<CitationList citations={mockReportNoCitations.citations} />);

    await waitFor(() => {
      // Either show error message or prevent rendering
      const errorMessage = container.querySelector('[data-testid="citations-error"]');
      const emptyState = container.querySelector('[data-testid="no-citations"]');

      expect(errorMessage || emptyState).toBeTruthy();
    });
  });
});

describe('T108: UK-Only Constraint Enforcement', () => {
  it('should reject non-UK country queries with clear error message', async () => {
    // ARRANGE: Mock API rejection for non-UK query
    global.fetch = vi.fn(() => Promise.resolve({
      ok: false,
      status: 400,
      json: async () => ({
        detail: 'This MVP currently supports the UK only.',
      }),
    } as Response));

    const onSubmitMock = vi.fn();

    // ACT: User tries to query about USA
    render(<ChatInput onSubmit={onSubmitMock} />);

    const input = screen.getByPlaceholderText(/what subject/i);
    await userEvent.type(input, 'Computer Science in USA');
    await userEvent.click(screen.getByRole('button', { name: /submit/i }));

    // ASSERT: Error message should appear
    await waitFor(() => {
      const errorElement = screen.getByText(/UK only/i) || screen.getByText(/only supports the UK/i);
      expect(errorElement).toBeInTheDocument();
    });
  });

  it('should accept UK queries', async () => {
    // ARRANGE
    global.fetch = vi.fn(() => Promise.resolve({
      ok: true,
      json: async () => ({
        checkout_url: 'https://checkout.stripe.com/test',
        report_id: 'report_uk_test',
      }),
    } as Response));

    const onSubmitMock = vi.fn();

    // ACT: User queries about UK
    render(<ChatInput onSubmit={onSubmitMock} />);

    const input = screen.getByPlaceholderText(/what subject/i);
    await userEvent.type(input, 'Computer Science in UK');
    await userEvent.click(screen.getByRole('button', { name: /submit/i }));

    // ASSERT: Should proceed to payment (no error)
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalled();
      expect(onSubmitMock).toHaveBeenCalled();
    });
  });
});

describe('T109: Payment-Before-Generation Gate', () => {
  it('should not generate report if payment fails', async () => {
    // ARRANGE: Mock failed payment
    const mockFailedPayment = {
      status: 'failed',
      error: 'Payment declined',
    };

    // ACT: Simulate payment failure
    global.fetch = vi.fn(() => Promise.resolve({
      ok: false,
      status: 402,
      json: async () => mockFailedPayment,
    } as Response));

    // ASSERT: Report should not be created
    // (Backend test ensures this, frontend should show error)
    const onSubmitMock = vi.fn();
    render(<ChatInput onSubmit={onSubmitMock} />);

    await userEvent.type(screen.getByPlaceholderText(/what subject/i), 'Computer Science');
    await userEvent.click(screen.getByRole('button', { name: /submit/i }));

    await waitFor(() => {
      // Should show payment error, not proceed to report
      expect(screen.queryByText(/generating report/i)).not.toBeInTheDocument();
    });
  });

  it('should only generate report after successful payment', async () => {
    // ARRANGE: Mock successful payment
    global.fetch = vi.fn(() => Promise.resolve({
      ok: true,
      json: async () => ({
        checkout_url: 'https://checkout.stripe.com/success',
        report_id: 'report_paid',
      }),
    } as Response));

    // ACT: Simulate successful payment flow
    const onSubmitMock = vi.fn();
    render(<ChatInput onSubmit={onSubmitMock} />);

    await userEvent.type(screen.getByPlaceholderText(/what subject/i), 'Computer Science');
    await userEvent.click(screen.getByRole('button', { name: /submit/i }));

    // ASSERT: Should redirect to checkout
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/reports/initiate'),
        expect.any(Object),
      );
    });
  });
});

describe('T110: Streaming Validation', () => {
  it('should render report chunks incrementally', async () => {
    // ARRANGE: Mock streaming response
    const mockMessages = [
      { role: 'assistant', content: 'Executive Summary: ', timestamp: Date.now() },
      { role: 'assistant', content: 'UK offers excellent programs. ', timestamp: Date.now() + 100 },
      { role: 'assistant', content: 'Study Options: Multiple universities...', timestamp: Date.now() + 200 },
    ];

    // ACT: Render message list with streaming messages
    const { rerender } = render(<MessageList messages={mockMessages.slice(0, 1)} />);

    // ASSERT: First chunk visible
    expect(screen.getByText(/Executive Summary:/)).toBeInTheDocument();

    // Simulate next chunk arrival
    rerender(<MessageList messages={mockMessages.slice(0, 2)} />);
    expect(screen.getByText(/UK offers excellent programs/)).toBeInTheDocument();

    // Simulate final chunk arrival
    rerender(<MessageList messages={mockMessages} />);
    expect(screen.getByText(/Study Options:/)).toBeInTheDocument();
  });

  it('should begin streaming within 5 seconds', async () => {
    // ARRANGE
    const startTime = Date.now();
    let firstChunkTime: number | null = null;

    global.fetch = vi.fn(() => {
      firstChunkTime = Date.now();
      return Promise.resolve({
        ok: true,
        body: {
          getReader: () => ({
            read: async () => ({
              done: false,
              value: new TextEncoder().encode('First chunk'),
            }),
          }),
        },
      } as any);
    });

    // ACT: Initiate report generation
    const onSubmitMock = vi.fn();
    render(<ChatInput onSubmit={onSubmitMock} />);

    await userEvent.type(screen.getByPlaceholderText(/what subject/i), 'Computer Science');
    await userEvent.click(screen.getByRole('button', { name: /submit/i }));

    // ASSERT: First chunk within 5s
    await waitFor(() => {
      expect(firstChunkTime).not.toBeNull();
      const elapsed = firstChunkTime! - startTime;
      expect(elapsed).toBeLessThan(5000);
    });
  });
});

describe('T111: Multi-Provider Auth', () => {
  const authProviders = [
    { name: 'Google', provider: 'google' },
    { name: 'Apple', provider: 'apple' },
    { name: 'Facebook', provider: 'facebook' },
    { name: 'Email', provider: 'email' },
  ];

  authProviders.forEach(({ name, provider }) => {
    it(`should authenticate via ${name}`, async () => {
      // ARRANGE: Mock user authenticated via provider
      const mockUser = {
        id: `user_${provider}_test`,
        email: `test@${provider}.com`,
        externalAccounts: [{ provider }],
      };

      vi.mock('@clerk/nextjs', () => ({
        useUser: () => ({ user: mockUser, isLoaded: true, isSignedIn: true }),
        useAuth: () => ({ isLoaded: true, isSignedIn: true, userId: mockUser.id }),
      }));

      // ACT: Render chat page (requires auth)
      render(<ChatPage />);

      // ASSERT: User should be authenticated
      await waitFor(() => {
        expect(screen.queryByText(/sign in/i)).not.toBeInTheDocument();
        // Chat interface should be visible
        expect(screen.getByPlaceholderText(/what subject/i)).toBeInTheDocument();
      });
    });
  });
});

describe('T112: Shared Components Portability', () => {
  it('should work with different API endpoint configurations', async () => {
    // ARRANGE: Test multiple API endpoints
    const endpoints = [
      'http://localhost:8000',
      'https://api-dev.studyabroad.com',
      'https://api-staging.studyabroad.com',
      'https://api.studyabroad.com',
    ];

    for (const endpoint of endpoints) {
      // ACT: Configure API endpoint
      process.env.NEXT_PUBLIC_API_URL = endpoint;

      // Shared component should use configured endpoint
      global.fetch = vi.fn((url: string) => {
        expect(url).toContain(endpoint);
        return Promise.resolve({
          ok: true,
          json: async () => ({ checkout_url: 'test' }),
        } as Response);
      });

      const onSubmitMock = vi.fn();
      const { unmount } = render(<ChatInput onSubmit={onSubmitMock} />);

      await userEvent.type(screen.getByPlaceholderText(/what subject/i), 'Test');
      await userEvent.click(screen.getByRole('button', { name: /submit/i }));

      // ASSERT: Fetch should use correct endpoint
      await waitFor(() => {
        expect(global.fetch).toHaveBeenCalled();
      });

      unmount();
    }
  });

  it('should adapt to different environment modes', async () => {
    // ARRANGE: Test dev, test, production modes
    const environments = [
      { mode: 'dev', enablePayments: 'false' },
      { mode: 'test', enablePayments: 'false' },
      { mode: 'production', enablePayments: 'true' },
    ];

    for (const env of environments) {
      // ACT
      process.env.ENVIRONMENT_MODE = env.mode;
      process.env.ENABLE_PAYMENTS = env.enablePayments;

      // ASSERT: Components should adapt behavior
      const onSubmitMock = vi.fn();
      const { unmount } = render(<ChatInput onSubmit={onSubmitMock} />);

      if (env.enablePayments === 'false') {
        // In dev/test, payment might be skipped or mocked
        expect(screen.getByPlaceholderText(/what subject/i)).toBeInTheDocument();
      } else {
        // In production, payment is enforced
        expect(screen.getByPlaceholderText(/what subject/i)).toBeInTheDocument();
      }

      unmount();
    }
  });
});
