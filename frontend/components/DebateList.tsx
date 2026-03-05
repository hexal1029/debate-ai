/**
 * Debate list/gallery component
 */

'use client';

import Link from 'next/link';
import { DebateSummary } from '@/lib/types';
import { formatRelativeTime } from '@/lib/utils';

interface DebateListProps {
  debates: DebateSummary[];
}

export function DebateList({ debates }: DebateListProps) {
  if (debates.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500 dark:text-gray-400">
        <p className="text-lg mb-2">还没有辩论记录</p>
        <p className="text-sm">创建第一场辩论开始吧！</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {debates.map((debate) => (
        <Link
          key={debate.id}
          href={`/debate/${debate.id}`}
          className="block bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-lg hover:border-indigo-300 dark:hover:border-indigo-600 transition-all"
        >
          <h3 className="font-semibold text-lg mb-3 text-gray-900 dark:text-gray-100">
            {debate.parameters.p1} vs {debate.parameters.p2}
          </h3>

          <p className="text-gray-600 dark:text-gray-400 text-sm mb-3 line-clamp-2">
            {debate.parameters.topic}
          </p>

          <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-500">
            <span>{debate.parameters.style} · {debate.parameters.rounds}轮</span>
            <span>{formatRelativeTime(debate.created_at)}</span>
          </div>

          {debate.message_count > 0 && (
            <div className="mt-2 text-xs text-gray-600 dark:text-gray-400">
              {debate.message_count} 条消息
            </div>
          )}
        </Link>
      ))}
    </div>
  );
}
