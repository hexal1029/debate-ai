/**
 * Message bubble component for displaying individual debate messages
 *
 * Features:
 * - Color-coded by role (moderator, character1, character2)
 * - Markdown rendering
 * - Copy button
 * - Smooth animations
 */

'use client';

import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Copy, Check } from 'lucide-react';
import { DebateMessage } from '@/lib/types';
import { getRoleColor, getRoleEmoji } from '@/lib/utils';
import { cn } from '@/lib/utils';

interface MessageBubbleProps {
  message: DebateMessage;
  index: number;
}

export function MessageBubble({ message, index }: MessageBubbleProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const emoji = getRoleEmoji(message.role);
  const colorClass = getRoleColor(message.role);

  return (
    <div
      className={cn(
        'border rounded-lg p-6 animate-fade-in animate-slide-up',
        colorClass
      )}
      style={{
        animationDelay: `${index * 50}ms`,
      }}
    >
      <div className="flex items-start justify-between gap-4 mb-3">
        <div className="flex items-center gap-2">
          <span className="text-2xl">{emoji}</span>
          <h3 className="font-semibold text-lg">{message.speaker}</h3>
        </div>
        <button
          onClick={handleCopy}
          className="p-2 hover:bg-white/50 rounded-md transition-colors"
          title="复制内容"
        >
          {copied ? (
            <Check className="h-4 w-4 text-green-600" />
          ) : (
            <Copy className="h-4 w-4" />
          )}
        </button>
      </div>

      <div className="prose prose-sm max-w-none">
        <ReactMarkdown
          components={{
            p: ({ children }) => <p className="mb-3 leading-relaxed">{children}</p>,
            strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
            em: ({ children }) => <em className="italic">{children}</em>,
          }}
        >
          {message.content}
        </ReactMarkdown>
      </div>
    </div>
  );
}
