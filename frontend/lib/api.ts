/**
 * API client for communicating with the FastAPI backend
 */

import {
  CreateDebateRequest,
  CreateDebateResponse,
  DebateListResponse,
  DebateDetail,
  StylesResponse,
  DebateStatus,
} from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Generic fetch wrapper with error handling
 */
async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Network error');
  }
}

/**
 * Create a new debate
 */
export async function createDebate(
  request: CreateDebateRequest
): Promise<CreateDebateResponse> {
  return fetchAPI<CreateDebateResponse>('/api/debates', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

/**
 * List all debates with optional filtering and pagination
 */
export async function listDebates(params?: {
  page?: number;
  page_size?: number;
  status?: DebateStatus;
}): Promise<DebateListResponse> {
  const queryParams = new URLSearchParams();

  if (params?.page) queryParams.set('page', params.page.toString());
  if (params?.page_size) queryParams.set('page_size', params.page_size.toString());
  if (params?.status) queryParams.set('status', params.status);

  const endpoint = `/api/debates${queryParams.toString() ? `?${queryParams}` : ''}`;

  return fetchAPI<DebateListResponse>(endpoint);
}

/**
 * Get details of a specific debate
 */
export async function getDebate(debateId: string): Promise<DebateDetail> {
  return fetchAPI<DebateDetail>(`/api/debates/${debateId}`);
}

/**
 * Delete a debate
 */
export async function deleteDebate(debateId: string): Promise<{ message: string }> {
  return fetchAPI<{ message: string }>(`/api/debates/${debateId}`, {
    method: 'DELETE',
  });
}

/**
 * Get available debate styles
 */
export async function getStyles(language: 'zh' | 'en' = 'zh'): Promise<StylesResponse> {
  return fetchAPI<StylesResponse>(`/api/styles?language=${language}`);
}

/**
 * Get SSE stream URL for a debate
 */
export function getStreamURL(debateId: string): string {
  return `${API_URL}/api/debates/${debateId}/stream`;
}

/**
 * Health check
 */
export async function healthCheck(): Promise<{
  status: string;
  api_key_configured: boolean;
  jobs: any;
}> {
  return fetchAPI<any>('/health');
}
