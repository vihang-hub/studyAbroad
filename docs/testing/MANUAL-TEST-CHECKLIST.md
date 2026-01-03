# Manual Testing Checklist - MVP UK Study & Migration Research App

**Date**: 2025-12-31
**Tester**: _________________
**Environment**: Local Development
**Branch**: `001-mvp-uk-study-migration`

---

## Prerequisites

### Environment Setup

- [ ] Backend running at `http://localhost:8000`
- [ ] Frontend running at `http://localhost:3000`
- [ ] PostgreSQL database running
- [ ] Environment variables configured (see SETUP-LOCAL-DEV.md)
- [ ] Test user account available

**Setup Instructions**: See `/docs/SETUP-LOCAL-DEV.md`

**Quick Start**:
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn src.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Verify backend: http://localhost:8000 (should see API status)
# Verify frontend: http://localhost:3000 (should see chat interface)
```

---

## Acceptance Criteria Testing

### AC-1: User can authenticate using all supported methods ✅❌

**Spec Requirement**: "User must authenticate using: Google OAuth, Apple, Facebook, Email."

**Test Cases**:

#### 1.1 Google OAuth Authentication
- [ ] Click "Sign in with Google" button
- [ ] Redirected to Google OAuth consent screen
- [ ] Select Google account
- [ ] Grant permissions
- [ ] Redirected back to app
- [ ] User is logged in (see user name/avatar in UI)
- [ ] User session persists on page refresh

**Expected Result**: ✅ Successful login, user session created
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 1.2 Apple Authentication
- [ ] Click "Sign in with Apple" button
- [ ] Redirected to Apple ID login
- [ ] Enter Apple ID credentials
- [ ] Complete 2FA if enabled
- [ ] Redirected back to app
- [ ] User is logged in

**Expected Result**: ✅ Successful login
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail / ⏭️ Skipped (if not implemented)
**Notes**: _________________

#### 1.3 Facebook Authentication
- [ ] Click "Sign in with Facebook" button
- [ ] Redirected to Facebook login
- [ ] Enter Facebook credentials
- [ ] Grant permissions
- [ ] Redirected back to app
- [ ] User is logged in

**Expected Result**: ✅ Successful login
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail / ⏭️ Skipped (if not implemented)
**Notes**: _________________

#### 1.4 Email Authentication
- [ ] Enter email address in login form
- [ ] Click submit
- [ ] Receive magic link or password prompt
- [ ] Complete authentication
- [ ] User is logged in

**Expected Result**: ✅ Successful login
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail / ⏭️ Skipped (if not implemented)
**Notes**: _________________

#### 1.5 Unauthenticated Access Handling
- [ ] Open app in incognito/private window
- [ ] Attempt to submit a query without logging in
- [ ] Verify prompted to authenticate before payment

**Expected Result**: ✅ Authentication required before paid query
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

---

### AC-2: User is charged £2.99 exactly once per query ✅❌

**Spec Requirement**: "Price per query: £2.99 (GBP). One successful payment → one report."

**Test Cases**:

#### 2.1 Correct Price Display
- [ ] Log in to the application
- [ ] View payment page/checkout
- [ ] Verify price displayed is **£2.99**
- [ ] Verify currency is **GBP** (not USD or other)

**Expected Result**: ✅ £2.99 displayed
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 2.2 Single Payment for Single Query
- [ ] Enter subject (e.g., "Computer Science")
- [ ] Proceed to payment
- [ ] Complete payment (use Stripe test card: `4242 4242 4242 4242`)
- [ ] Check database: `SELECT * FROM payments WHERE user_id = '<your-user-id>' ORDER BY created_at DESC LIMIT 1;`
- [ ] Verify exactly **ONE** payment record created
- [ ] Verify amount is **299** pence (£2.99)

**Expected Result**: ✅ One payment record, amount = 299 pence
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 2.3 No Duplicate Charges (Idempotency)
- [ ] Submit query with subject "Computer Science"
- [ ] Complete payment
- [ ] Immediately refresh page during report generation
- [ ] Check database payment records
- [ ] Verify only **ONE** payment exists (no duplicates)

**Expected Result**: ✅ Only one payment, no duplicates
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 2.4 Payment Receipt/Confirmation
- [ ] After successful payment, verify confirmation shown
- [ ] Check for payment ID or receipt number
- [ ] Verify user can access payment history

**Expected Result**: ✅ Payment confirmation displayed
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

---

### AC-3: Failed payment results in no report ✅❌

**Spec Requirement**: "If payment fails or is cancelled: No report is generated, No data is stored."

**Test Cases**:

#### 3.1 Declined Card - No Report Generated
- [ ] Enter subject "Computer Science"
- [ ] Proceed to payment
- [ ] Use Stripe test card for **declined payment**: `4000 0000 0000 0002`
- [ ] Payment should fail
- [ ] Verify **NO** report is generated
- [ ] Check database: `SELECT * FROM reports WHERE user_id = '<your-user-id>' ORDER BY created_at DESC LIMIT 1;`
- [ ] Verify no new report record exists

**Expected Result**: ✅ No report, no database record
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 3.2 User Cancels Payment
- [ ] Enter subject "Business Administration"
- [ ] Proceed to payment (Stripe checkout)
- [ ] Click "Cancel" or close payment window
- [ ] Verify returned to query input screen
- [ ] Verify NO report generated
- [ ] Check database for no new report record

**Expected Result**: ✅ No report, user can retry
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 3.3 Insufficient Funds Card
- [ ] Use Stripe test card: `4000 0000 0000 9995` (insufficient funds)
- [ ] Proceed to payment
- [ ] Verify payment fails
- [ ] Verify error message shown to user
- [ ] Verify NO report generated

**Expected Result**: ✅ Payment fails, no report
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

---

### AC-4: Successful payment produces a streamed report ✅❌

**Spec Requirement**: "Backend calls Gemini APIs. Responses are streamed to the frontend."

**Test Cases**:

#### 4.1 Report Generation Starts After Payment
- [ ] Complete successful payment (subject: "Nursing")
- [ ] Verify report generation starts immediately
- [ ] Observe streaming response (text appearing progressively)
- [ ] Verify NOT showing full report at once (streaming chunks)

**Expected Result**: ✅ Report streams progressively
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 4.2 Streaming Latency (SLA Compliance)
- [ ] Use browser DevTools Network tab
- [ ] Complete payment
- [ ] Measure time from payment success to **first chunk** of report
- [ ] Verify first chunk arrives within **≤5 seconds**

**Expected Result**: ✅ First chunk within 5s
**Actual Result**: _____ seconds
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 4.3 Complete Report Generation
- [ ] Allow report to fully generate
- [ ] Verify all sections appear (see AC-7 for section list)
- [ ] Verify citations appear at bottom
- [ ] Verify report is saved to database

**Expected Result**: ✅ Complete report with all sections
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 4.4 Network Interruption Handling
- [ ] Start report generation
- [ ] During streaming, **disconnect internet** (or use DevTools to simulate)
- [ ] Reconnect internet
- [ ] Verify error handling or retry mechanism

**Expected Result**: ✅ Graceful error handling
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

---

### AC-5: Reports are accessible for 30 days ✅❌

**Spec Requirement**: "Reports stored for 30 days. Reopening does not trigger AI regeneration. After 30 days: deleted or inaccessible."

**Test Cases**:

#### 5.1 Report Expiry Date Set Correctly
- [ ] Generate a new report (subject: "Engineering")
- [ ] Check database: `SELECT id, created_at, expires_at FROM reports WHERE id = <report-id>;`
- [ ] Verify `expires_at = created_at + 30 days`
- [ ] Calculate expected expiry date and compare

**Expected Result**: ✅ Expiry is created_at + 30 days
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 5.2 Reopen Report Within 30 Days (No AI Regeneration)
- [ ] Generate report for "Computer Science"
- [ ] Note the exact report content (copy first paragraph)
- [ ] Navigate away from report
- [ ] Reopen report from history/sidebar
- [ ] Verify **exact same content** displayed
- [ ] Check browser DevTools Network tab
- [ ] Verify **NO** Gemini API call made (should load from database)

**Expected Result**: ✅ Cached report, no API call
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 5.3 Report Accessible Within 30 Days
- [ ] Generate report
- [ ] Close browser completely
- [ ] Reopen browser and log in
- [ ] Navigate to report history
- [ ] Verify report appears in list
- [ ] Click to open report
- [ ] Verify full report loads

**Expected Result**: ✅ Report accessible
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 5.4 Expired Report Handling (After 30 Days)
**Note**: This test requires manual database manipulation since we can't wait 30 days.

- [ ] Generate a report
- [ ] Manually update database: `UPDATE reports SET expires_at = NOW() - INTERVAL '1 day' WHERE id = <report-id>;`
- [ ] Attempt to access the report
- [ ] Verify report is **inaccessible** or shows "Expired" message
- [ ] Verify 404 or appropriate error response

**Expected Result**: ✅ Expired report inaccessible
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

---

### AC-6: Reports cannot be accessed by other users ✅❌

**Spec Requirement**: "Users can only access their own reports."

**Test Cases**:

#### 6.1 User A Cannot Access User B's Report
**Setup**: Requires two user accounts

- [ ] Log in as **User A**
- [ ] Generate report (subject: "Medicine")
- [ ] Note the report ID from URL (e.g., `/reports/12345`)
- [ ] Log out
- [ ] Log in as **User B** (different Google account)
- [ ] Manually navigate to User A's report URL: `http://localhost:3000/reports/12345`
- [ ] Verify **403 Forbidden** or redirect to home
- [ ] Verify report content NOT displayed

**Expected Result**: ✅ Access denied (403 Forbidden)
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 6.2 User Can Only See Own Reports in List
- [ ] Log in as **User A**
- [ ] Generate 2 reports (subjects: "Law", "Architecture")
- [ ] Log out
- [ ] Log in as **User B**
- [ ] Generate 1 report (subject: "Business")
- [ ] View report history/list
- [ ] Verify **only User B's report** appears (Business)
- [ ] Verify User A's reports (Law, Architecture) do **NOT** appear

**Expected Result**: ✅ Only own reports visible
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 6.3 Unauthenticated Access Denied
- [ ] Generate report as authenticated user
- [ ] Note report URL
- [ ] Log out
- [ ] Open incognito/private window
- [ ] Navigate directly to report URL
- [ ] Verify redirect to login page or 401 Unauthorized

**Expected Result**: ✅ Authentication required
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

---

### AC-7: All mandatory report sections are present ✅❌

**Spec Requirement**: "Every report must contain all 10 sections."

**Mandatory Sections**:
1. Executive Summary (5-10 bullets)
2. Study Options in the UK
3. Estimated Cost of Studying
4. Visa & Immigration Overview
5. Post-Study Work Options
6. Job Prospects in the Chosen Subject
7. Fallback Job Prospects (Out-of-Field)
8. Risks & Reality Check
9. 30/60/90-Day Action Plan
10. Sources & Citations

**Test Cases**:

#### 7.1 All Sections Present in Report
- [ ] Generate report (subject: "Psychology")
- [ ] Scroll through entire report
- [ ] Verify each section heading appears:
  - [ ] Executive Summary
  - [ ] Study Options in the UK
  - [ ] Estimated Cost of Studying
  - [ ] Visa & Immigration Overview
  - [ ] Post-Study Work Options
  - [ ] Job Prospects in the Chosen Subject
  - [ ] Fallback Job Prospects
  - [ ] Risks & Reality Check
  - [ ] 30/60/90-Day Action Plan
  - [ ] Sources & Citations

**Expected Result**: ✅ All 10 sections present
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Missing Sections** (if any): _________________

#### 7.2 Executive Summary Format
- [ ] Verify Executive Summary has 5-10 bullet points
- [ ] Count bullets: _____ bullets
- [ ] Verify concise (not paragraphs)

**Expected Result**: ✅ 5-10 bullets
**Actual Result**: _____ bullets
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 7.3 Cost Section Contains Required Info
- [ ] Verify "Estimated Cost of Studying" section includes:
  - [ ] Tuition fee ranges
  - [ ] Living cost estimates
  - [ ] Currency (GBP)

**Expected Result**: ✅ Tuition + living costs in GBP
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 7.4 Action Plan Structure
- [ ] Verify "30/60/90-Day Action Plan" includes:
  - [ ] 30-day actions
  - [ ] 60-day actions
  - [ ] 90-day actions
- [ ] Verify actionable steps (not vague advice)

**Expected Result**: ✅ Structured timeline with actions
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

---

### AC-8: All factual claims include citations ✅❌

**Spec Requirement**: "Factual claims must include citations. If uncertain, state uncertainty. No uncited confident claims."

**Test Cases**:

#### 8.1 Citations Present in Report
- [ ] Generate report (subject: "Data Science")
- [ ] Scroll to "Sources & Citations" section
- [ ] Verify citations exist
- [ ] Count number of citations: _____ citations
- [ ] Verify citations have **titles** and **URLs**

**Expected Result**: ✅ Multiple citations with titles + URLs
**Actual Result**: _____ citations found
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 8.2 Citation Format Validation
- [ ] Inspect citation structure
- [ ] Verify each citation has:
  - [ ] Title (e.g., "UK Government - Study Visa")
  - [ ] URL (e.g., "https://www.gov.uk/study-visa")
  - [ ] Clickable link (opens in new tab)

**Example Citation**:
```
Title: UK Government - Study Visa
URL: https://www.gov.uk/study-visa
```

**Expected Result**: ✅ Proper format with title + URL
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 8.3 Factual Claims Have Citations
- [ ] Identify 3-5 factual claims in report (e.g., "Tuition fees range from £10,000-£38,000")
- [ ] For each claim, verify reference to source
- [ ] Check if citation number/link appears near claim

**Claims Checked**:
1. Claim: _________________ → Citation: ✅❌
2. Claim: _________________ → Citation: ✅❌
3. Claim: _________________ → Citation: ✅❌

**Expected Result**: ✅ Factual claims have citations
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 8.4 Uncertainty Language Validation
- [ ] Search report for uncertain data
- [ ] Verify phrases like:
  - "approximately"
  - "estimated"
  - "may vary"
  - "data is uncertain"
- [ ] Verify NO uncited confident claims (e.g., "Definitely £15,000" without source)

**Expected Result**: ✅ Uncertainty clearly stated
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

---

### AC-9: UK-only constraint is enforced ✅❌

**Spec Requirement**: "If user attempts non-UK destination: Show clear message 'This MVP currently supports the UK only.'"

**Test Cases**:

#### 9.1 UK Query Accepted
- [ ] Enter subject: "Computer Science"
- [ ] Mention UK explicitly in query (e.g., "I want to study Computer Science in the UK")
- [ ] Verify query accepted
- [ ] Verify payment page shown

**Expected Result**: ✅ UK query accepted
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 9.2 UK Synonyms Accepted
- [ ] Test with UK variations:
  - [ ] "United Kingdom"
  - [ ] "Britain"
  - [ ] "England"
  - [ ] "London" (UK city)
- [ ] Verify all accepted

**Expected Result**: ✅ All UK terms accepted
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 9.3 Non-UK Country Rejected (USA)
- [ ] Enter subject: "Computer Science"
- [ ] Mention USA (e.g., "I want to study in the USA")
- [ ] Verify error message shown
- [ ] Verify message text: **"This MVP currently supports the UK only."**
- [ ] Verify NO payment page shown

**Expected Result**: ✅ Rejected with clear message
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 9.4 Non-UK Country Rejected (Canada)
- [ ] Enter: "studying nursing in Canada"
- [ ] Verify rejected with UK-only message

**Expected Result**: ✅ Rejected
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 9.5 Non-UK Country Rejected (Australia)
- [ ] Enter: "I want to go to Australia for MBA"
- [ ] Verify rejected

**Expected Result**: ✅ Rejected
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### 9.6 No Country Mentioned (Default Behavior)
- [ ] Enter subject only: "Computer Science"
- [ ] No country mentioned
- [ ] Check if system assumes UK or prompts for country

**Expected Result**: System assumes UK or prompts
**Actual Result**: _________________
**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

---

## Additional Quality Checks

### Usability Testing

#### UI/UX Flow
- [ ] Gemini-style interface present (central input box)
- [ ] Conversational layout (chat-like)
- [ ] Sidebar with past conversations visible
- [ ] Can reopen past reports from sidebar
- [ ] Smooth animations and transitions

**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### Error Handling
- [ ] Clear error messages for all failure cases
- [ ] User can retry after errors
- [ ] No cryptic error codes shown to users

**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

---

### Performance Testing

#### Page Load Times
- [ ] Home page loads in < 2 seconds
- [ ] Report history loads in < 3 seconds
- [ ] Opening existing report loads in < 2 seconds

**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### Streaming Performance
- [ ] First chunk of report appears within 5 seconds
- [ ] Streaming is smooth (no long pauses between chunks)
- [ ] Full report generates within reasonable time (< 2 minutes)

**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

---

### Security Testing

#### Authentication Security
- [ ] Session cookies are HttpOnly and Secure
- [ ] CORS properly configured
- [ ] No secrets visible in frontend code or network requests
- [ ] JWT tokens properly validated

**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

#### Payment Security
- [ ] Payment processed through Stripe (PCI compliant)
- [ ] No card details stored in application database
- [ ] HTTPS enforced for all payment flows

**Status**: ✅ Pass / ❌ Fail
**Notes**: _________________

---

### Cross-Browser Testing

#### Chrome
- [ ] All features work
- [ ] UI renders correctly
- [ ] Streaming works

**Status**: ✅ Pass / ❌ Fail
**Version**: _________________

#### Firefox
- [ ] All features work
- [ ] UI renders correctly
- [ ] Streaming works

**Status**: ✅ Pass / ❌ Fail
**Version**: _________________

#### Safari
- [ ] All features work
- [ ] UI renders correctly
- [ ] Streaming works

**Status**: ✅ Pass / ❌ Fail
**Version**: _________________

---

## Summary

### Test Results

**Acceptance Criteria Status**:
- AC-1 (Authentication): ✅ ❌ ⏭️
- AC-2 (£2.99 charge): ✅ ❌ ⏭️
- AC-3 (Failed payment): ✅ ❌ ⏭️
- AC-4 (Streaming): ✅ ❌ ⏭️
- AC-5 (30-day retention): ✅ ❌ ⏭️
- AC-6 (User isolation): ✅ ❌ ⏭️
- AC-7 (10 sections): ✅ ❌ ⏭️
- AC-8 (Citations): ✅ ❌ ⏭️
- AC-9 (UK-only): ✅ ❌ ⏭️

**Overall Pass Rate**: _____ / 9 (____%)

**Critical Issues Found**:
1. _________________
2. _________________
3. _________________

**Recommendations**:
1. _________________
2. _________________
3. _________________

**Gate5-QA Status**: ✅ PASS / ❌ FAIL

**Tester Signature**: _________________
**Date Completed**: _________________

---

## Appendix: Test Data

### Test User Accounts
- User A: _________________
- User B: _________________

### Test Subjects Used
- _________________
- _________________
- _________________

### Stripe Test Cards
- Success: `4242 4242 4242 4242`
- Decline: `4000 0000 0000 0002`
- Insufficient funds: `4000 0000 0000 9995`

### Database Queries for Validation

**Check payment records**:
```sql
SELECT id, user_id, amount, status, created_at
FROM payments
WHERE user_id = '<user-id>'
ORDER BY created_at DESC;
```

**Check report records**:
```sql
SELECT id, user_id, subject, created_at, expires_at
FROM reports
WHERE user_id = '<user-id>'
ORDER BY created_at DESC;
```

**Check report sections**:
```sql
SELECT id, content
FROM reports
WHERE id = '<report-id>';
```

**Manually expire a report (for testing)**:
```sql
UPDATE reports
SET expires_at = NOW() - INTERVAL '1 day'
WHERE id = '<report-id>';
```
