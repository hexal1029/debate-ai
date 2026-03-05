/**
 * Real-time debate viewer component
 */

'use client';

import { useRef, useEffect } from 'react';
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
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { status, messages, currentProgress, error } = useDebateStream({
    debateId,
  });

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleExport = () => {
    const markdown = debateToMarkdown({
      parameters: initialData?.parameters || {},
      messages,
      created_at: initialData?.created_at || new Date().toISOString(),
      completed_at: status === 'completed' ? new Date().toISOString() : undefined,
    });

    const filename = `debate_${debateId}_${Date.now()}.md`;
    downloadText(markdown, filename);
  };

  const isLoading = status === 'connecting' || status === 'connected';

  return (
    <div className="flex flex-col h-full">
      <ProgressIndicator progress={currentProgress} isActive={isLoading} />

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-800 px-6 py-4 rounded-lg mb-6">
          <strong>错误:</strong> {error}
        </div>
      )}

      <div className="flex-1 overflow-y-auto">
        <div className="space-y-4">
          {messages.map((message, index) => (
            <MessageBubble key={index} message={message} index={index} />
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {status === 'completed' && messages.length > 0 && (
        <div className="sticky bottom-0 bg-white border-t border-gray-200 p-4 mt-6">
          <button
            onClick={handleExport}
            className="w-full md:w-auto bg-green-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-green-700 transition-colors flex items-center justify-center gap-2"
          >
            <Download className="h-4 w-4" />
            导出为 Markdown
          </button>
        </div>
      )}
    </div>
  );
}
