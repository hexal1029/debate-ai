/**
 * Home page - Debate list
 */

import { listDebates } from '@/lib/api';
import { DebateList } from '@/components/DebateList';
import Link from 'next/link';
import { Plus } from 'lucide-react';

export const revalidate = 0; // Disable caching for real-time updates

export default async function HomePage() {
  let debates = [];
  let error = null;

  try {
    const response = await listDebates({ page: 1, page_size: 20 });
    debates = response.debates;
  } catch (e) {
    error = e instanceof Error ? e.message : '加载失败';
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">
            辩论列表
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            浏览所有历史人物辩论记录
          </p>
        </div>

        <Link
          href="/create"
          className="bg-indigo-600 dark:bg-indigo-500 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 dark:hover:bg-indigo-600 font-medium flex items-center gap-2 transition-colors"
        >
          <Plus className="h-5 w-5" />
          创建新辩论
        </Link>
      </div>

      {error && (
        <div className="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-800 dark:text-red-200 px-6 py-4 rounded-lg mb-6">
          <strong>错误:</strong> {error}
          <p className="text-sm mt-1">请确保后端服务正在运行</p>
        </div>
      )}

      <DebateList debates={debates} />
    </div>
  );
}
