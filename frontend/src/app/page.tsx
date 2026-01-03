/**
 * Landing page
 */

import Link from 'next/link';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-4">
          UK Study & Migration Research
        </h1>
        <p className="text-lg mb-8">
          AI-powered research reports for students studying in the UK
        </p>
        <div className="flex gap-4">
          <Link
            href="/login"
            className="px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90"
          >
            Login
          </Link>
          <Link
            href="/signup"
            className="px-6 py-3 bg-secondary text-secondary-foreground rounded-lg hover:bg-secondary/90"
          >
            Sign Up
          </Link>
        </div>
      </div>
    </main>
  );
}
