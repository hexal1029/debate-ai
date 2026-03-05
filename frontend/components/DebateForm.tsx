/**
 * Debate creation form component
 */

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Loader2, Sparkles } from 'lucide-react';
import { createDebate, getStyles } from '@/lib/api';
import { CreateDebateRequest, StyleInfo, DebateStyle, Language, LanguageStyle } from '@/lib/types';

const STYLE_EMOJIS: Record<DebateStyle, string> = {
  'academic': '🎓',
  'casual-chat': '💬',
  'heated-debate': '🔥',
  'comedy-duo': '🎭',
};

export function DebateForm() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [styles, setStyles] = useState<StyleInfo[]>([]);
  const [showAdvanced, setShowAdvanced] = useState(false);

  const [formData, setFormData] = useState<CreateDebateRequest>({
    p1: '',
    p2: '',
    topic: '',
    rounds: 5,
    style: 'academic',
    language: 'zh',
    language_style: '现代口语',
  });

  useEffect(() => {
    // Load available styles
    getStyles('zh').then((res) => setStyles(res.styles));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await createDebate(formData);
      // Redirect to debate viewer
      router.push(`/debate/${response.id}`);
    } catch (error) {
      alert(`创建辩论失败: ${error instanceof Error ? error.message : '未知错误'}`);
      setLoading(false);
    }
  };

  const selectedStyle = styles.find((s) => s.name === formData.style);

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Person 1 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          辩论者 1
        </label>
        <input
          type="text"
          required
          value={formData.p1}
          onChange={(e) => setFormData({ ...formData, p1: e.target.value })}
          placeholder="如：牛顿"
          className="w-full px-4 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-gray-900 dark:text-gray-100 rounded-lg focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400 focus:border-transparent placeholder-gray-400 dark:placeholder-gray-500"
        />
      </div>

      {/* Person 2 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          辩论者 2
        </label>
        <input
          type="text"
          required
          value={formData.p2}
          onChange={(e) => setFormData({ ...formData, p2: e.target.value })}
          placeholder="如：莱布尼茨"
          className="w-full px-4 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-gray-900 dark:text-gray-100 rounded-lg focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400 focus:border-transparent placeholder-gray-400 dark:placeholder-gray-500"
        />
      </div>

      {/* Topic */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          辩论话题
        </label>
        <input
          type="text"
          required
          value={formData.topic}
          onChange={(e) => setFormData({ ...formData, topic: e.target.value })}
          placeholder="如：微积分的发明权"
          className="w-full px-4 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-gray-900 dark:text-gray-100 rounded-lg focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400 focus:border-transparent placeholder-gray-400 dark:placeholder-gray-500"
        />
      </div>

      {/* Style */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          辩论风格
        </label>
        <div className="grid grid-cols-2 gap-3">
          {styles.map((style) => (
            <button
              key={style.name}
              type="button"
              onClick={() => setFormData({ ...formData, style: style.name as DebateStyle, rounds: style.default_rounds })}
              className={`p-4 border-2 rounded-lg text-left transition-all ${
                formData.style === style.name
                  ? 'border-indigo-500 dark:border-indigo-400 bg-indigo-50 dark:bg-indigo-900/30'
                  : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
              }`}
            >
              <div className="flex items-center gap-2 mb-1">
                <span className="text-2xl">{STYLE_EMOJIS[style.name as DebateStyle]}</span>
                <span className="font-medium text-sm text-gray-900 dark:text-gray-100">{style.description.split(' - ')[0]}</span>
              </div>
              <p className="text-xs text-gray-600 dark:text-gray-400">{style.word_limit}</p>
            </button>
          ))}
        </div>
        {selectedStyle && (
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            推荐轮数: {selectedStyle.default_rounds}轮 · {selectedStyle.word_limit}
          </p>
        )}
      </div>

      {/* Advanced Options */}
      <div>
        <button
          type="button"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="text-sm text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 font-medium"
        >
          {showAdvanced ? '隐藏' : '显示'}高级选项
        </button>

        {showAdvanced && (
          <div className="mt-4 space-y-4 p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                辩论轮数
              </label>
              <input
                type="number"
                min="1"
                max="20"
                value={formData.rounds}
                onChange={(e) => setFormData({ ...formData, rounds: parseInt(e.target.value) })}
                className="w-full px-4 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-gray-900 dark:text-gray-100 rounded-lg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                语言风格
              </label>
              <select
                value={formData.language_style}
                onChange={(e) => setFormData({ ...formData, language_style: e.target.value as LanguageStyle })}
                className="w-full px-4 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-gray-900 dark:text-gray-100 rounded-lg"
              >
                <option value="现代口语">现代口语</option>
                <option value="半文半白">半文半白</option>
                <option value="文言">文言</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                字数限制（可选）
              </label>
              <input
                type="number"
                min="20"
                max="500"
                value={formData.word_limit || ''}
                onChange={(e) => setFormData({ ...formData, word_limit: e.target.value ? parseInt(e.target.value) : undefined })}
                placeholder="留空使用默认值"
                className="w-full px-4 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-gray-900 dark:text-gray-100 rounded-lg placeholder-gray-400 dark:placeholder-gray-500"
              />
            </div>
          </div>
        )}
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading}
        className="w-full bg-indigo-600 dark:bg-indigo-500 text-white py-3 px-6 rounded-lg font-medium hover:bg-indigo-700 dark:hover:bg-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors"
      >
        {loading ? (
          <>
            <Loader2 className="h-5 w-5 animate-spin" />
            正在创建辩论...
          </>
        ) : (
          <>
            <Sparkles className="h-5 w-5" />
            开始辩论
          </>
        )}
      </button>
    </form>
  );
}
