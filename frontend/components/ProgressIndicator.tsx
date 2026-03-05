/**
 * Progress indicator component for debate generation
 *
 * Shows current step and progress message during debate generation
 */

import { Loader2 } from 'lucide-react';
import { ProgressEvent } from '@/lib/types';

interface ProgressIndicatorProps {
  progress: ProgressEvent | null;
  isActive: boolean;
}

export function ProgressIndicator({ progress, isActive }: ProgressIndicatorProps) {
  if (!isActive || !progress) {
    return null;
  }

  return (
    <div className="sticky top-0 z-10 bg-blue-50 dark:bg-blue-900/30 border-b border-blue-200 dark:border-blue-800 px-6 py-4">
      <div className="flex items-center gap-3">
        <Loader2 className="h-5 w-5 animate-spin text-blue-600 dark:text-blue-400" />
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-blue-900 dark:text-blue-100">
              {progress.step}
            </span>
            <span className="text-sm text-blue-700 dark:text-blue-300">
              {progress.message}
            </span>
          </div>
          <div className="mt-2 h-1.5 w-full bg-blue-200 dark:bg-blue-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-blue-600 dark:bg-blue-500 transition-all duration-500 rounded-full"
              style={{
                width: `${calculateProgress(progress.step)}%`,
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

/**
 * Calculate progress percentage from step string (e.g., "3/7" -> 42.86%)
 */
function calculateProgress(step: string): number {
  const match = step.match(/(\d+)\/(\d+)/);
  if (!match) return 0;

  const [, current, total] = match;
  return (parseInt(current) / parseInt(total)) * 100;
}
