/**
 * Signup page
 * Uses Clerk's built-in SignUp component
 */

import { SignUp } from '@clerk/nextjs';

export default function SignupPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <SignUp
        appearance={{
          elements: {
            rootBox: 'mx-auto',
            card: 'shadow-lg',
          },
        }}
        routing="path"
        path="/signup"
        signInUrl="/login"
        afterSignUpUrl="/chat"
      />
    </div>
  );
}
