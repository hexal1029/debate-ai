/**
 * Real-time debate viewer component
 */

'use client';

import React from 'react';
import { Download } from 'lucide-react';
import { useDebateStream } from '@/hooks/useDebateStream';
import { MessageBubble } from './MessageBubble';
import { ProgressIndicator } from './ProgressIndicator';
import { debateToMarkdown, downloadText } from '@/lib/utils';

interface DebateViewerProps {
  debateId: string;
  initialData?: any;
}

export function DebateViewer({ debateId, initialData }: DebateViewerProps) {
  // Check if debate is already completed
  const isCompleted = initialData?.status === 'completed';

  // Only use SSE stream for non-completed debates
  const { status, messages: streamMessages, currentProgress, error } = useDebateStream({
    debateId,
  });

  // Use initial messages if debate is completed, otherwise use stream messages
  const messages = isCompleted ? (initialData?.messages || []) : streamMessages;
  const displayStatus = isCompleted ? 'completed' : status;

  const handleExport = () => {
    const markdown = debateToMarkdown({
      parameters: initialData?.parameters || {},
      messages,
      created_at: initialData?.created_at || new Date().toISOString(),
      completed_at: displayStatus === 'completed' ? (initialData?.completed_at || new Date().toISOString()) : undefined,
    });

    const filename = `debate_${debateId}_${Date.now()}.md`;
    downloadText(markdown, filename);
  };

  const isLoading = !isCompleted && (status === 'connecting' || status === 'connected');

  return (
    <div className="flex flex-col h-full">
      <ProgressIndicator progress={currentProgress} isActive={isLoading} />

      {error && (
        <div className="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-800 dark:text-red-200 px-6 py-4 rounded-lg mb-6">
          <strong>错误:</strong> {error}
        </div>
      )}

      <div className="flex-1 overflow-y-auto">
        <div className="space-y-4">
          {messages.map((message, index) => (
            <MessageBubble key={index} message={message} index={index} />
          ))}
        </div>
      </div>

      {displayStatus === 'completed' && messages.length > 0 && (
        <div className="sticky bottom-0 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 p-4 mt-6">
          <button
            onClick={handleExport}
            className="w-full md:w-auto bg-green-600 dark:bg-green-700 text-white px-6 py-2 rounded-lg font-medium hover:bg-green-700 dark:hover:bg-green-600 transition-colors flex items-center justify-center gap-2"
          >
            <Download className="h-4 w-4" />
            导出为 Markdown
          </button>
        </div>
      )}
    </div>
  );
}
