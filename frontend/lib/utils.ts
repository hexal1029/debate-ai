/**
 * Utility functions for the frontend
 */

import { type ClassValue, clsx } from 'clsx';

/**
 * Merge class names with clsx
 */
export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}

/**
 * Format a date to a readable string
 */
export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
}

/**
 * Format a relative time (e.g., "2 minutes ago")
 */
export function formatRelativeTime(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  if (diffInSeconds < 60) {
    return '刚刚';
  }

  const diffInMinutes = Math.floor(diffInSeconds / 60);
  if (diffInMinutes < 60) {
    return `${diffInMinutes}分钟前`;
  }

  const diffInHours = Math.floor(diffInMinutes / 60);
  if (diffInHours < 24) {
    return `${diffInHours}小时前`;
  }

  const diffInDays = Math.floor(diffInHours / 24);
  if (diffInDays < 30) {
    return `${diffInDays}天前`;
  }

  return formatDate(dateString);
}

/**
 * Get color class for a message role
 */
export function getRoleColor(role: string): string {
  switch (role) {
    case 'moderator':
      return 'bg-blue-50 dark:bg-blue-900/20 border-blue-300 dark:border-blue-700 text-gray-900 dark:text-gray-100';
    case 'character1':
      return 'bg-green-50 dark:bg-green-900/20 border-green-300 dark:border-green-700 text-gray-900 dark:text-gray-100';
    case 'character2':
      return 'bg-amber-50 dark:bg-amber-900/20 border-amber-300 dark:border-amber-700 text-gray-900 dark:text-gray-100';
    case 'both':
      return 'bg-gradient-to-r from-green-50 to-amber-50 dark:from-green-900/20 dark:to-amber-900/20 border-green-300 dark:border-green-700 text-gray-900 dark:text-gray-100';
    default:
      return 'bg-gray-100 dark:bg-gray-800 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-gray-100';
  }
}

/**
 * Get emoji for a message role
 */
export function getRoleEmoji(role: string): string {
  switch (role) {
    case 'moderator':
      return '🎤';
    case 'character1':
      return '🔵';
    case 'character2':
      return '🟡';
    case 'both':
      return '🎭';
    default:
      return '💬';
  }
}

/**
 * Convert debate to Markdown format
 */
export function debateToMarkdown(debate: any): string {
  const { parameters, messages, created_at, completed_at } = debate;

  let markdown = `# ${parameters.p1} vs ${parameters.p2}：${parameters.topic}\n\n`;

  markdown += `## 辩论信息\n\n`;
  markdown += `- **辩论话题**: ${parameters.topic}\n`;
  markdown += `- **辩论双方**: ${parameters.p1} vs ${parameters.p2}\n`;
  markdown += `- **生成时间**: ${formatDate(created_at)}\n`;
  if (completed_at) {
    markdown += `- **完成时间**: ${formatDate(completed_at)}\n`;
  }
  markdown += `- **辩论轮数**: ${parameters.rounds}\n`;
  markdown += `- **辩论风格**: ${parameters.style}\n`;
  markdown += `- **输出语言**: ${parameters.language}\n\n`;

  markdown += `---\n\n## 辩论实录\n\n`;

  for (const msg of messages) {
    const emoji = getRoleEmoji(msg.role);
    markdown += `### ${emoji} ${msg.speaker}\n\n`;
    markdown += `${msg.content}\n\n`;
    markdown += `---\n\n`;
  }

  markdown += `*本辩论由 AI 历史人物辩论生成器自动生成*\n`;

  return markdown;
}

/**
 * Download text as a file
 */
export function downloadText(text: string, filename: string) {
  const blob = new Blob([text], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
