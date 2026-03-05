/**
 * Debate viewer page
 */

import { getDebate } from '@/lib/api';
import { DebateViewer } from '@/components/DebateViewer';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';

export const revalidate = 0; // Disable caching

interface PageProps {
  params: { id: string };
}

export default async function DebatePage({ params }: PageProps) {
  const { id } = params;

  let debate = null;
  let error = null;

  try {
    debate = await getDebate(id);
  } catch (e) {
    error = e instanceof Error ? e.message : '加载失败';
  }

  if (error) {
    return (
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-800 dark:text-red-200 px-6 py-4 rounded-lg">
          <strong>错误:</strong> {error}
        </div>
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 mt-4"
        >
          <ArrowLeft className="h-4 w-4" />
          返回列表
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-6">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 mb-4"
        >
          <ArrowLeft className="h-4 w-4" />
          返回列表
        </Link>

        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">
          {debate?.parameters.p1} vs {debate?.parameters.p2}
        </h1>
        <p className="text-gray-600 dark:text-gray-400">{debate?.parameters.topic}</p>

        <div className="flex flex-wrap gap-2 mt-3 text-sm">
          <span className="bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 px-3 py-1 rounded-full">
            {debate?.parameters.style}
          </span>
          <span className="bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 px-3 py-1 rounded-full">
            {debate?.parameters.rounds} 轮
          </span>
          <span className="bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 px-3 py-1 rounded-full">
            {debate?.parameters.language_style}
          </span>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 min-h-[600px]">
        <DebateViewer debateId={id} initialData={debate} />
      </div>
    </div>
  );
}
