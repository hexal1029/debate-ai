/**
 * React hook for consuming Server-Sent Events (SSE) from debate stream
 *
 * This hook connects to the FastAPI SSE endpoint and provides real-time
 * updates as the debate is generated.
 */

import { useEffect, useState, useRef, useCallback } from 'react';
import { getStreamURL } from '@/lib/api';
import {
  DebateMessage,
  StreamStatus,
  ProgressEvent,
  MessageEvent,
  CompleteEvent,
  ErrorEvent,
} from '@/lib/types';

interface UseDebateStreamOptions {
  debateId: string;
  onProgress?: (data: ProgressEvent) => void;
  onMessage?: (data: MessageEvent) => void;
  onComplete?: (data: CompleteEvent) => void;
  onError?: (data: ErrorEvent) => void;
}

interface UseDebateStreamReturn {
  status: StreamStatus;
  messages: DebateMessage[];
  currentProgress: ProgressEvent | null;
  error: string | null;
}

export function useDebateStream({
  debateId,
  onProgress,
  onMessage,
  onComplete,
  onError,
}: UseDebateStreamOptions): UseDebateStreamReturn {
  const [status, setStatus] = useState<StreamStatus>('connecting');
  const [messages, setMessages] = useState<DebateMessage[]>([]);
  const [currentProgress, setCurrentProgress] = useState<ProgressEvent | null>(null);
  const [error, setError] = useState<string | null>(null);

  const eventSourceRef = useRef<EventSource | null>(null);

  // Cleanup function
  const cleanup = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
  }, []);

  useEffect(() => {
    // Create EventSource connection
    const streamURL = getStreamURL(debateId);
    const eventSource = new EventSource(streamURL);
    eventSourceRef.current = eventSource;

    setStatus('connecting');

    // Connected event
    eventSource.addEventListener('connected', (event) => {
      console.log('SSE connected:', event.data);
      setStatus('connected');
    });

    // Progress events
    eventSource.addEventListener('progress', (event) => {
      try {
        const data: ProgressEvent = JSON.parse(event.data);
        setCurrentProgress(data);
        onProgress?.(data);
      } catch (err) {
        console.error('Error parsing progress event:', err);
      }
    });

    // Message events
    eventSource.addEventListener('message', (event) => {
      try {
        const data: MessageEvent = JSON.parse(event.data);

        // Add message to list
        const newMessage: DebateMessage = {
          speaker: data.speaker,
          role: data.role as any,
          content: data.content,
        };

        setMessages((prev) => [...prev, newMessage]);
        onMessage?.(data);
      } catch (err) {
        console.error('Error parsing message event:', err);
      }
    });

    // Complete event
    eventSource.addEventListener('complete', (event) => {
      try {
        const data: CompleteEvent = JSON.parse(event.data);
        setStatus('completed');
        setCurrentProgress(null);
        onComplete?.(data);
        cleanup();
      } catch (err) {
        console.error('Error parsing complete event:', err);
      }
    });

    // Error event
    eventSource.addEventListener('error', (event: any) => {
      try {
        if (event.data) {
          const data: ErrorEvent = JSON.parse(event.data);
          setError(data.error);
          setStatus('error');
          onError?.(data);
        }
      } catch (err) {
        console.error('Error parsing error event:', err);
      }
      cleanup();
    });

    // EventSource error handler
    eventSource.onerror = (event) => {
      console.error('EventSource error:', event);
      setStatus('error');
      setError('Connection error');
      cleanup();
    };

    // Ping events (keepalive)
    eventSource.addEventListener('ping', () => {
      // Just keepalive, no action needed
    });

    // Cleanup on unmount
    return () => {
      cleanup();
    };
  }, [debateId, onProgress, onMessage, onComplete, onError, cleanup]);

  return {
    status,
    messages,
    currentProgress,
    error,
  };
}
