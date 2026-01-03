# Research: MVP UK Study & Migration App

**Generated**: 2025-12-29
**Purpose**: Resolve all NEEDS CLARIFICATION items from Technical Context and establish best practices for implementation.

## 1. Authentication Provider Selection

### Decision: Clerk (recommended over Auth.js)

**Rationale**:
- **Multi-provider support**: Clerk natively supports Google, Apple, Facebook, and Email (magic link & password) out of the box
- **Production-ready**: Less configuration required for OAuth providers
- **User management UI**: Built-in user dashboard reduces custom admin work
- **Session management**: Automatic token refresh and session handling
- **TypeScript-first**: Better DX for Next.js 15 App Router with Server Components
- **Compliance**: SOC 2 Type II certified, GDPR/CCPA compliant
- **Pricing**: Free tier supports up to 10,000 MAUs (sufficient for MVP)

**Alternatives Considered**:
- **Auth.js (NextAuth)**: More flexible but requires more boilerplate for multiple providers; manual session management; good for custom requirements but overkill for standard OAuth
- **Supabase Auth**: Already using Supabase for DB, but Clerk provides better multi-provider UX and user management features

**Implementation Notes**:
- Use `@clerk/nextjs` for frontend
- Verify Clerk JWT on FastAPI backend using `clerk-sdk-python`
- Store `clerk_user_id` as `user_id` in Supabase `users` table

---

## 2. Payment Provider Selection

### Decision: Stripe

**Rationale**:
- **Industry standard**: Most widely used, well-documented, proven reliability
- **GBP support**: Native support for £2.99 pricing
- **Payment Links**: Can use Stripe Checkout for quick MVP implementation
- **Webhooks**: Reliable webhook system for payment confirmation before report generation
- **PCI compliance**: Stripe handles all PCI-DSS compliance (no card data touches our servers)
- **Developer experience**: Excellent TypeScript SDK, test mode, webhook testing with Stripe CLI
- **Pricing**: 1.5% + 20p per transaction for UK cards (£2.99 → ~£0.24 fee = £2.75 net)

**Alternatives Considered**:
- **PayPal**: Higher fees (2.9% + £0.30), less developer-friendly webhooks
- **Paddle**: Good for SaaS but unnecessary complexity for single-price model
- **Razorpay**: Good for South Asian markets but less UK focus

**Implementation Pattern**:
```text
User flow:
1. User submits subject → Frontend calls backend POST /reports/initiate
2. Backend creates Stripe Checkout Session (£2.99, metadata: {userId, subject})
3. Frontend redirects to Stripe Checkout
4. User completes payment
5. Stripe webhook (checkout.session.completed) → Backend /webhooks/stripe
6. Backend verifies signature, initiates report generation, stores reportId
7. Frontend polls GET /reports/{id} until status=completed
```

**Security Requirements**:
- Stripe API keys in Google Secret Manager
- Webhook signature verification (prevents replay attacks)
- Idempotency keys for retry safety

---

## 3. Gemini API Integration with LangChain

### Decision: Use LangChain with Google Generative AI provider for streaming

**Rationale**:
- **Constitutional requirement**: LangChain is mandated in Section 1 of constitution
- **Streaming support**: `ChatGoogleGenerativeAI` supports streaming responses
- **Structured output**: Can enforce report section structure via prompt templates
- **Citation tracking**: LangChain supports retrieval chains with source tracking
- **Error handling**: Built-in retry logic and error handling

**Best Practices**:
1. **Prompt Engineering**:
   - Use `PromptTemplate` to enforce UK-specific context
   - Include mandatory sections in system prompt
   - Require citations for all factual claims

2. **Streaming Implementation**:
   ```python
   from langchain_google_genai import ChatGoogleGenerativeAI
   from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

   llm = ChatGoogleGenerativeAI(
       model="gemini-2.0-flash-exp",
       temperature=0.3,  # Lower temp for factual accuracy
       streaming=True,
       callbacks=[StreamingStdOutCallbackHandler()]
   )
   ```

3. **Citation Requirements**:
   - Use RAG pipeline with vector store (Supabase pgvector) for UK study data
   - Store curated UK immigration/education sources
   - Enforce citation format: `[Source: {title} - {url}]`

4. **Hallucination Prevention**:
   - Set `temperature=0.3` for factual queries
   - Use grounding with retrieval context
   - Validate report sections against mandatory checklist

**Gemini Model Selection**:
- **Model**: `gemini-2.0-flash-exp` (fast, cost-effective, good for structured output)
- **Fallback**: `gemini-1.5-pro` if flash model unavailable
- **Token limits**: Monitor context window (32k tokens for flash)

---

## 4. Supabase Row Level Security (RLS) Patterns

### Decision: User-scoped RLS policies with JWT claims

**Best Practices**:
1. **Authentication Integration**:
   - Clerk JWT contains `sub` (user ID)
   - Supabase RLS uses `auth.uid()` from JWT
   - Set JWT claims in Supabase: `clerk_user_id` → `auth.uid()`

2. **RLS Policies**:
   ```sql
   -- Users table: Users can only read their own record
   CREATE POLICY "Users can view own profile"
   ON users FOR SELECT
   USING (auth.uid() = user_id);

   -- Reports table: Users can only access their own reports
   CREATE POLICY "Users can view own reports"
   ON reports FOR SELECT
   USING (auth.uid() = user_id);

   CREATE POLICY "Users can create own reports"
   ON reports FOR INSERT
   WITH CHECK (auth.uid() = user_id);

   -- Payments table: Users can view own payments
   CREATE POLICY "Users can view own payments"
   ON payments FOR SELECT
   USING (auth.uid() = user_id);
   ```

3. **Retention Policy**:
   - Use PostgreSQL function to mark expired reports:
   ```sql
   CREATE OR REPLACE FUNCTION expire_old_reports()
   RETURNS void AS $$
   BEGIN
     UPDATE reports
     SET status = 'expired'
     WHERE expires_at < NOW() AND status = 'active';
   END;
   $$ LANGUAGE plpgsql;
   ```
   - Schedule with pg_cron or Cloud Scheduler

4. **Performance**:
   - Index on `user_id` for all tables
   - Index on `expires_at` for reports table
   - Partial index: `WHERE status = 'active'`

---

## 5. Next.js 15 App Router + Vercel AI SDK Streaming

### Decision: Use Vercel AI SDK with Route Handlers for streaming

**Best Practices**:
1. **Route Handler Pattern**:
   ```typescript
   // app/api/reports/stream/route.ts
   import { StreamingTextResponse } from 'ai';

   export async function POST(req: Request) {
     const { subject } = await req.json();

     // Call FastAPI backend stream endpoint
     const response = await fetch(`${BACKEND_URL}/reports/stream`, {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ subject }),
     });

     // Forward stream to client
     return new StreamingTextResponse(response.body);
   }
   ```

2. **Frontend Hook**:
   ```typescript
   import { useChat } from 'ai/react';

   const { messages, input, handleSubmit, isLoading } = useChat({
     api: '/api/reports/stream',
   });
   ```

3. **Server Components**:
   - Use React Server Components for static report rendering
   - Client Components only for interactive chat interface
   - Reduces client-side JavaScript bundle

4. **Error Boundaries**:
   - Wrap streaming components in error boundaries
   - Graceful degradation if stream fails
   - Fallback to polling for report status

---

## 6. Payment-Before-Generation Flow

### Decision: Synchronous payment verification with async report generation

**Flow**:
1. **Payment Initiation**:
   - User clicks "Generate Report" → Create Stripe Checkout Session
   - Redirect to Stripe hosted page (PCI-compliant)

2. **Payment Verification**:
   - Stripe webhook `checkout.session.completed` → Backend
   - Backend verifies webhook signature
   - Backend creates `Report` record with `status=pending`
   - Backend triggers async report generation (Cloud Tasks or Celery)

3. **Report Generation**:
   - Async worker calls Gemini API via LangChain
   - Streams result to Supabase (store incrementally or full report)
   - Updates `Report.status=completed` when done

4. **User Polling**:
   - Frontend polls `GET /reports/{id}` every 2 seconds
   - Display progress indicator
   - Show streaming UI when `status=generating`
   - Redirect to full report when `status=completed`

**Failure Handling**:
- Payment fails → No report created, user notified
- Report generation fails → Refund via Stripe API, mark `Report.status=failed`
- Partial generation → Store partial content, mark `status=failed`, offer retry

---

## 7. Data Retention Implementation

### Decision: Soft delete with scheduled cleanup

**30-Day Retention Strategy**:
1. **Expiry Tracking**:
   - `reports.expires_at = created_at + INTERVAL '30 days'`
   - `reports.status` enum: `pending`, `generating`, `completed`, `expired`, `failed`

2. **Access Control**:
   - RLS policy: `WHERE status IN ('pending', 'generating', 'completed') AND expires_at > NOW()`
   - Users cannot access expired reports (hard cutoff)

3. **Cleanup Options** (MVP must choose one):
   - **Option A (Soft Delete)**: Mark `status=expired`, keep data for audit/analytics
     - Pros: Data recovery possible, audit trail preserved
     - Cons: Storage costs accumulate
   - **Option B (Hard Delete)**: DELETE FROM reports WHERE expires_at < NOW()
     - Pros: Clean storage, GDPR-compliant
     - Cons: No recovery, need separate audit logs

**Recommendation**: **Option A (Soft Delete)** for MVP
- Preserve data for 90 days total (30 accessible + 60 archived)
- Hard delete after 90 days via scheduled job
- Allows debugging and analytics during MVP phase

**Scheduled Cleanup**:
```python
# Cloud Scheduler → Cloud Run endpoint
@app.post("/cron/expire-reports")
async def expire_reports():
    await supabase.rpc("expire_old_reports").execute()
    return {"status": "ok"}
```

---

## 8. Observability & Logging Strategy

### Decision: Structured logging with request correlation

**Stack**:
- **Frontend**: Vercel Analytics (built-in)
- **Backend**: Google Cloud Logging (native Cloud Run integration)
- **Correlation**: `requestId` + `userId` in all logs

**Implementation**:
```python
import structlog
from uuid import uuid4

logger = structlog.get_logger()

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    request.state.request_id = request_id

    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        user_id=request.state.user.id if hasattr(request.state, 'user') else None
    )

    response = await call_next(request)
    return response
```

**Logged Events** (per constitution Section 2):
- Authentication: Login success/failure, token refresh
- Payments: Checkout initiated, payment succeeded, payment failed
- Reports: Generation started, generation completed, generation failed
- Errors: All exceptions with stack traces

---

## Summary of Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| Auth Provider | Clerk | Multi-provider support, production-ready, TypeScript-first |
| Payment Provider | Stripe | Industry standard, GBP support, excellent webhooks |
| AI Model | Gemini 2.0 Flash | Fast, cost-effective, good for structured output |
| LangChain Integration | ChatGoogleGenerativeAI with streaming | Constitutional requirement, citation support |
| RLS Pattern | JWT claims + user-scoped policies | Secure, performant, standard Supabase pattern |
| Streaming | Vercel AI SDK + Route Handlers | Native Next.js 15 support, simple integration |
| Payment Flow | Stripe Checkout → Webhook → Async generation | PCI-compliant, reliable, good UX |
| Data Retention | Soft delete (30 days accessible + 60 archived) | Recovery possible, audit trail preserved |
| Observability | Structured logging with requestId + userId | Constitution Section 2 compliance |

**No remaining NEEDS CLARIFICATION items.**
