/**
 * Login page
 * Uses Clerk's built-in SignIn component
 */

import { SignIn } from '@clerk/nextjs';

export default function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <SignIn
        appearance={{
          elements: {
            rootBox: 'mx-auto',
            card: 'shadow-lg',
          },
        }}
        routing="path"
        path="/login"
        signUpUrl="/signup"
        afterSignInUrl="/chat"
      />
    </div>
  );
}
