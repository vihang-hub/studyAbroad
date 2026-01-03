# Clerk Authentication Setup Guide

**Date**: 2025-12-31
**Purpose**: Step-by-step instructions to configure Clerk authentication for the Study Abroad MVP

---

## ✅ What's Already Done

The code has been updated to use the **latest Clerk App Router approach**:

1. ✅ Clerk package upgraded to latest version (6.36.5)
2. ✅ `middleware.ts` updated with `clerkMiddleware()` (not deprecated `authMiddleware`)
3. ✅ `layout.tsx` updated with `<ClerkProvider>` and Clerk components
4. ✅ `.env.local` created with placeholder keys
5. ✅ `.gitignore` configured to exclude `.env.local`

**All code follows official Clerk documentation**: https://clerk.com/docs/nextjs/getting-started/quickstart

---

## 🎯 What You Need To Do Now

### Step 1: Create Free Clerk Account (5 minutes)

1. **Go to**: https://clerk.com
2. **Click**: "Start building for free"
3. **Sign up** with your email or GitHub
4. **Verify** your email address

**Note**: Free tier includes:
- ✅ 10,000 monthly active users
- ✅ All authentication methods
- ✅ Perfect for development & testing

---

### Step 2: Create Your Application (2 minutes)

1. **After logging in**, click **"Create Application"**
2. **Application name**: `Study Abroad Dev` (or any name you prefer)
3. **Select authentication methods**:
   - ✅ **Email** (enable)
   - ✅ **Google** (enable)
   - ⏭️ Apple (optional - skip for now)
   - ⏭️ Facebook (optional - skip for now)
4. **Click**: "Create Application"

**You'll be taken to the Dashboard**

---

### Step 3: Get Your API Keys (1 minute)

1. **In Clerk Dashboard**, navigate to: **"API Keys"** (left sidebar)
   - Direct link: https://dashboard.clerk.com/last-active?path=api-keys

2. **You'll see two keys**:
   - `Publishable key` (starts with `pk_test_`)
   - `Secret key` (starts with `sk_test_`)

3. **Copy both keys** (click the copy icon)

---

### Step 4: Add Keys to .env.local (2 minutes)

1. **Open** the file:
   ```bash
   nano /Users/vihang/projects/study-abroad/frontend/.env.local
   ```

2. **Replace the placeholder values**:

   **BEFORE** (current):
   ```bash
   NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=YOUR_PUBLISHABLE_KEY
   CLERK_SECRET_KEY=YOUR_SECRET_KEY
   ```

   **AFTER** (with your actual keys):
   ```bash
   NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_your_actual_publishable_key_here
   CLERK_SECRET_KEY=sk_test_your_actual_secret_key_here
   ```

3. **Save and close**: Press `Ctrl+O`, then `Enter`, then `Ctrl+X`

---

### Step 5: Restart Frontend Server (1 minute)

**Kill the current server:**
```bash
# Find the process ID
ps aux | grep "next dev" | grep -v grep

# Kill it (use the PID from above)
kill <PID>
```

**Or simpler - if you know the terminal where it's running:**
- Press `Ctrl+C` in that terminal

**Restart the server:**
```bash
cd /Users/vihang/projects/study-abroad/frontend
npm run dev
```

**Wait for**:
```
✓ Ready in 1-2s
- Local: http://localhost:3000
```

---

### Step 6: Test Authentication (5 minutes)

1. **Open browser**: http://localhost:3000

2. **You should now see**:
   - ✅ Header with "Sign In" and "Sign Up" buttons
   - ❌ NO "Demo Mode" warning banner

3. **Click "Sign Up"**:
   - Clerk modal should open
   - Enter your email
   - Create password
   - Verify email (check inbox)

4. **After sign up**:
   - ✅ You should be redirected to `/chat`
   - ✅ Header shows your profile (UserButton)
   - ✅ Can click profile to sign out

5. **Test "Sign In"**:
   - Sign out
   - Click "Sign In"
   - Enter credentials
   - Should be signed in

---

## 🔒 Security Verification

### ✅ Verify .env.local is NOT in Git

```bash
cd /Users/vihang/projects/study-abroad/frontend
git status

# Should NOT show .env.local in the list
# If it does, run:
git rm --cached .env.local
```

### ✅ Verify .gitignore is Correct

```bash
grep "\.env" .gitignore
```

Should show:
```
.env*.local
.env.local
.env
```

---

## 🧪 Testing Checklist

After setup, verify the following work:

- [ ] **Sign Up**: Create new account with email
- [ ] **Email Verification**: Receive and verify email
- [ ] **Sign In**: Log in with created account
- [ ] **Session Persistence**: Refresh page, still signed in
- [ ] **Sign Out**: Click profile → Sign Out → Redirected to home
- [ ] **Protected Routes**: Access `/chat` without auth → Redirected to sign in
- [ ] **Google OAuth** (if configured):
  - [ ] Click "Sign in with Google"
  - [ ] Authorize with Google account
  - [ ] Redirected back and signed in

---

## 🎨 UI Customization (Optional)

### Customize Sign-In/Sign-Up Appearance

1. **Go to**: Clerk Dashboard → **Customization** → **Theme**
2. **Choose**:
   - Light/Dark mode
   - Brand colors
   - Logo upload
3. **Instant preview** in dashboard

### Customize Redirect URLs

Already configured in `.env.local`:
```bash
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/chat
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/chat
```

**Change these** if you want different redirect destinations.

---

## 🚨 Troubleshooting

### Issue: "Invalid publishable key"

**Solution**:
1. Check `.env.local` has correct keys (no spaces)
2. Keys should start with `pk_test_` and `sk_test_`
3. Restart dev server after changing `.env.local`

### Issue: "Demo Mode" banner still showing

**Solution**:
1. Check `.env.local` exists in `frontend/` directory
2. Verify keys don't contain "dummy" or "YOUR_"
3. Restart frontend server

### Issue: "Clerk is not defined" error

**Solution**:
```bash
cd frontend
npm install @clerk/nextjs@latest
npm run dev
```

### Issue: Sign-in modal doesn't open

**Solution**:
1. Open browser console (F12)
2. Check for errors
3. Verify Clerk publishable key is set
4. Check browser blocks third-party cookies (disable if needed)

---

## 📊 Verify Setup is Correct

### ✅ Verification Checklist

Run these checks to ensure correct implementation:

1. **Middleware uses `clerkMiddleware()`**:
   ```bash
   grep "clerkMiddleware" frontend/src/middleware.ts
   ```
   Should show: `import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';`

2. **Layout uses `<ClerkProvider>`**:
   ```bash
   grep "ClerkProvider" frontend/src/app/layout.tsx
   ```
   Should show: `<ClerkProvider>` wrapper

3. **No deprecated patterns**:
   ```bash
   # Should return NOTHING:
   grep -r "authMiddleware" frontend/src/
   grep -r "_app.tsx" frontend/
   ```

4. **Environment keys set**:
   ```bash
   grep "CLERK" frontend/.env.local
   ```
   Should show your actual keys (not placeholders)

---

## 🎯 What's Next

After authentication is working:

1. **Manual Testing**: Update `TEST-STATUS-REPORT.md`
   - Mark AC-1 (Authentication) as ✅ VALIDATED

2. **Test User Isolation** (AC-6):
   - Create 2nd Google account
   - Test cross-user access denial

3. **Test Complete User Journey**:
   - Sign up → Pay → Generate report → Access report

4. **Configure Additional Providers** (Optional):
   - Apple OAuth
   - Facebook OAuth
   - Magic links (passwordless)

---

## 📚 Additional Resources

- **Clerk Docs**: https://clerk.com/docs
- **Next.js App Router**: https://clerk.com/docs/nextjs
- **Customization**: https://clerk.com/docs/customization/overview
- **Dashboard**: https://dashboard.clerk.com

---

## ✅ Success Criteria

You'll know it's working when:

1. ✅ No "Demo Mode" banner
2. ✅ "Sign In" / "Sign Up" buttons visible
3. ✅ Can create account and verify email
4. ✅ Can sign in and see user profile
5. ✅ Session persists on page refresh
6. ✅ Protected routes redirect to sign-in
7. ✅ Can sign out successfully

**Estimated Total Time**: 15-20 minutes

---

## 🔐 Security Reminders

1. ✅ **NEVER** commit `.env.local` to git
2. ✅ **NEVER** share secret keys publicly
3. ✅ Rotate keys if accidentally exposed
4. ✅ Use test keys for development (`pk_test_`, `sk_test_`)
5. ✅ Use production keys only in production (`pk_live_`, `sk_live_`)

---

**Ready to start?** Follow Step 1 and create your Clerk account! 🚀
