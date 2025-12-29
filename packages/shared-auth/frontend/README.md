# Shared Auth Frontend

Reusable authentication components and utilities for Next.js applications using Auth.js (NextAuth).

## Features

- 🔐 Google OAuth 2.0 integration
- 🎨 Ready-to-use auth components
- 🪝 React hooks for auth state
- 🔒 Session management
- 📝 TypeScript support

## Installation

This package is part of the monorepo and is automatically linked.

```json
{
  "dependencies": {
    "@studyabroad/shared-auth-frontend": "workspace:*"
  }
}
```

## Usage

### 1. Configure Auth.js

```typescript
// app/auth.ts
import { createAuthConfig } from '@studyabroad/shared-auth-frontend'

export const { handlers, signIn, signOut, auth } = createAuthConfig({
  googleClientId: process.env.GOOGLE_CLIENT_ID!,
  googleClientSecret: process.env.GOOGLE_CLIENT_SECRET!,
  // Optional: customize callbacks
  callbacks: {
    async jwt({ token, account, profile }) {
      // Custom JWT logic
      return token
    }
  }
})
```

### 2. Create API Route

```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/auth'

export const { GET, POST } = handlers
```

### 3. Use Auth Components

```typescript
import { LoginButton, LogoutButton, UserAvatar } from '@studyabroad/shared-auth-frontend'

export function Header() {
  return (
    <nav>
      <UserAvatar />
      <LoginButton />
      <LogoutButton />
    </nav>
  )
}
```

### 4. Use Auth Hooks

```typescript
import { useAuth } from '@studyabroad/shared-auth-frontend'

export function ProtectedPage() {
  const { user, isLoading, isAuthenticated } = useAuth()

  if (isLoading) return <div>Loading...</div>
  if (!isAuthenticated) return <div>Please log in</div>

  return <div>Welcome {user.name}!</div>
}
```

## Components

- `LoginButton` - Google sign-in button
- `LogoutButton` - Sign out button
- `UserAvatar` - User profile avatar with dropdown
- `AuthProvider` - Session provider wrapper
- `ProtectedRoute` - HOC for protected pages

## Hooks

- `useAuth()` - Get current auth state
- `useSession()` - Raw session hook (re-exported from next-auth)
- `useRequireAuth()` - Redirect if not authenticated

## Environment Variables

```env
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## TypeScript

Types are automatically included. Extend the session type:

```typescript
declare module 'next-auth' {
  interface Session {
    user: {
      id: string
      email: string
      name?: string
      image?: string
    }
  }
}
```
