import { API_BASE } from "../config";

export type ApiEnvelope<T> = {
  result: T;
  message: string;
};

export type Note = {
  id: number;
  text: string;
  created_at: string;
};

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });

  const payload = (await response.json().catch(() => null)) as
    | { message?: string }
    | null;

  if (!response.ok) {
    throw new Error(payload?.message ?? `HTTP ${response.status}`);
  }

  return payload as T;
}

export async function fetchHealth(): Promise<{ status: string; version: string }> {
  const response = await fetch("/healthz");
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return (await response.json()) as { status: string; version: string };
}

export const api = {
  home: () => request<ApiEnvelope<string>>("/home/"),
  echo: (message: string, echoType: string) =>
    request<ApiEnvelope<string>>("/echo/string", {
      method: "POST",
      body: JSON.stringify({ message, echo_type: echoType }),
    }),
  [[#if database]]
  notes: {
    list: () => request<ApiEnvelope<Note[]>>("/notes/"),
    create: (text: string) =>
      request<ApiEnvelope<Note>>("/notes/", {
        method: "POST",
        body: JSON.stringify({ text }),
      }),
  },
  [[/endif]]
};
