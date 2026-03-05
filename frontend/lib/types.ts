/**
 * TypeScript types for the AI Historical Debate Generator frontend.
 *
 * These types mirror the Pydantic models from the backend for type safety
 * across the frontend-backend boundary.
 */

export type DebateStatus = 'pending' | 'running' | 'completed' | 'failed';

export type DebateStyle = 'academic' | 'casual-chat' | 'heated-debate' | 'comedy-duo';

export type Language = 'zh' | 'en';

export type LanguageStyle = '文言' | '半文半白' | '现代口语';

export type MessageRole = 'moderator' | 'character1' | 'character2' | 'both';

export interface DebateMessage {
  speaker: string;
  role: MessageRole;
  content: string;
}

export interface CreateDebateRequest {
  p1: string;
  p2: string;
  topic: string;
  rounds: number;
  style: DebateStyle;
  language: Language;
  word_limit?: number;
  language_style: LanguageStyle;
}

export interface CreateDebateResponse {
  id: string;
  status: DebateStatus;
  created_at: string;
}

export interface DebateSummary {
  id: string;
  status: DebateStatus;
  parameters: CreateDebateRequest;
  message_count: number;
  created_at: string;
  completed_at?: string;
}

export interface DebateDetail {
  id: string;
  status: DebateStatus;
  parameters: CreateDebateRequest;
  messages: DebateMessage[];
  created_at: string;
  completed_at?: string;
  error?: string;
}

export interface DebateListResponse {
  debates: DebateSummary[];
  total: number;
  page: number;
  page_size: number;
}

export interface StyleInfo {
  name: string;
  description: string;
  max_tokens: number;
  temperature: number;
  default_rounds: number;
  word_limit: string;
  is_collaborative: boolean;
}

export interface StylesResponse {
  styles: StyleInfo[];
}

// SSE Event types
export interface ProgressEvent {
  step: string;
  message: string;
}

export interface MessageEvent {
  speaker: string;
  role: string;
  content: string;
}

export interface CompleteEvent {
  id: string;
}

export interface ErrorEvent {
  error: string;
}

// Stream status for useDebateStream hook
export type StreamStatus = 'connecting' | 'connected' | 'completed' | 'error' | 'disconnected';
