/**
 * Authenticated app layout
 * Wraps all authenticated routes
 * T121: Integrated ReportSidebar for report history
 */

import { auth } from '@clerk/nextjs/server';
import { redirect } from 'next/navigation';
import { ReportSidebar } from '@/components/reports/ReportSidebar';

export default async function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { userId } = await auth();

  // Redirect to login if not authenticated
  if (!userId) {
    redirect('/login');
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="flex gap-6">
          {/* Main content area */}
          <main className="flex-1 min-w-0">
            {children}
          </main>

          {/* Sidebar with recent reports */}
          <aside className="hidden lg:block w-80 flex-shrink-0">
            <div className="sticky top-8">
              <ReportSidebar maxReports={10} />
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}
