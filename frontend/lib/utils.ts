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
      return 'bg-moderator/10 border-moderator text-moderator-dark';
    case 'character1':
      return 'bg-character1/10 border-character1 text-character1-dark';
    case 'character2':
      return 'bg-character2/10 border-character2 text-character2-dark';
    case 'both':
      return 'bg-gradient-to-r from-character1/10 to-character2/10 border-character1';
    default:
      return 'bg-gray-100 border-gray-300';
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
 * Get status badge color
 */
export function getStatusColor(status: string): string {
  switch (status) {
    case 'pending':
      return 'bg-yellow-100 text-yellow-800 border-yellow-300';
    case 'running':
      return 'bg-blue-100 text-blue-800 border-blue-300';
    case 'completed':
      return 'bg-green-100 text-green-800 border-green-300';
    case 'failed':
      return 'bg-red-100 text-red-800 border-red-300';
    default:
      return 'bg-gray-100 text-gray-800 border-gray-300';
  }
}

/**
 * Get status text in Chinese
 */
export function getStatusText(status: string): string {
  switch (status) {
    case 'pending':
      return '等待中';
    case 'running':
      return '进行中';
    case 'completed':
      return '已完成';
    case 'failed':
      return '失败';
    default:
      return status;
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
