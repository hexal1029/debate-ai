import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Link from 'next/link';
import './globals.css';

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
        <div className="min-h-screen bg-gray-50">
          <nav className="bg-white border-b border-gray-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between items-center h-16">
                <Link href="/" className="flex items-center gap-2">
                  <span className="text-2xl">🎭</span>
                  <span className="text-xl font-bold text-gray-900">
                    AI 历史人物辩论
                  </span>
                </Link>

                <div className="flex items-center gap-4">
                  <Link
                    href="/"
                    className="text-gray-600 hover:text-gray-900 font-medium"
                  >
                    辩论列表
                  </Link>
                  <Link
                    href="/create"
                    className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 font-medium"
                  >
                    创建辩论
                  </Link>
                </div>
              </div>
            </div>
          </nav>

          <main>{children}</main>

          <footer className="bg-white border-t border-gray-200 mt-12">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-sm text-gray-600">
              <p>
                Powered by{' '}
                <a
                  href="https://www.anthropic.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-indigo-600 hover:text-indigo-700"
                >
                  Claude AI
                </a>{' '}
                · Built with Next.js & FastAPI
              </p>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
