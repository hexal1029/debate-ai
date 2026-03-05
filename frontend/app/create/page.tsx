/**
 * Create debate page
 */

import { DebateForm } from '@/components/DebateForm';

export default function CreatePage() {
  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">
          创建新辩论
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          选择两位历史人物和一个话题，让AI生成精彩的思想交锋
        </p>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-8">
        <DebateForm />
      </div>

      <div className="mt-8 bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">💡 提示</h3>
        <ul className="text-sm text-blue-800 dark:text-blue-200 space-y-1">
          <li>• 选择有观点对立的人物会产生更有趣的辩论</li>
          <li>• 话题越具体，辩论越深入</li>
          <li>• 学术风格适合深度探讨，轻松对话适合快速交流</li>
          <li>• 辩论生成需要30-60秒，请耐心等待</li>
        </ul>
      </div>
    </div>
  );
}
