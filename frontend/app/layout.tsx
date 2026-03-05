import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Link from 'next/link';
import './globals.css';
import { ThemeProvider } from '@/components/ThemeProvider';
import { ThemeToggle } from '@/components/ThemeToggle';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'AI Historical Debate Arena',
  description: '让历史人物跨越时空，在AI的世界里继续思想的交锋',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body className={inter.className}>
        <ThemeProvider>
          <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <nav className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                  <div className="flex-1" />
                  <Link href="/" className="flex items-center gap-2">
                    <span className="text-2xl">🎭</span>
                    <span className="text-xl font-bold text-gray-900 dark:text-gray-100">
                      AI 历史人物辩论
                    </span>
                  </Link>
                  <div className="flex-1 flex justify-end">
                    <ThemeToggle />
                  </div>
                </div>
              </div>
            </nav>

            <main>{children}</main>

            <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-12">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-sm text-gray-600 dark:text-gray-400">
                <p>
                  Powered by{' '}
                  <a
                    href="https://www.anthropic.com"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300"
                  >
                    Claude AI
                  </a>{' '}
                  · Built with Next.js & FastAPI
                </p>
              </div>
            </footer>
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
