/**
 * Debate list/gallery component
 */

'use client';

import Link from 'next/link';
import { DebateSummary } from '@/lib/types';
import { formatRelativeTime, getStatusColor, getStatusText } from '@/lib/utils';

interface DebateListProps {
  debates: DebateSummary[];
}

export function DebateList({ debates }: DebateListProps) {
  if (debates.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
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
          className="block border border-gray-200 rounded-lg p-4 hover:shadow-lg hover:border-indigo-300 transition-all"
        >
          <div className="flex items-start justify-between mb-3">
            <h3 className="font-semibold text-lg line-clamp-1">
              {debate.parameters.p1} vs {debate.parameters.p2}
            </h3>
            <span className={`text-xs px-2 py-1 rounded-full border ${getStatusColor(debate.status)}`}>
              {getStatusText(debate.status)}
            </span>
          </div>

          <p className="text-gray-600 text-sm mb-3 line-clamp-2">
            {debate.parameters.topic}
          </p>

          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>{debate.parameters.style} · {debate.parameters.rounds}轮</span>
            <span>{formatRelativeTime(debate.created_at)}</span>
          </div>

          {debate.message_count > 0 && (
            <div className="mt-2 text-xs text-gray-600">
              {debate.message_count} 条消息
            </div>
          )}
        </Link>
      ))}
    </div>
  );
}
