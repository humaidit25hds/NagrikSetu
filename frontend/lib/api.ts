const API_BASE_URL = (process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1").replace(/\/$/, "");

export type UserDemographics = {
  age?: number;
  gender?: string;
  state?: string;
  district?: string;
  annual_income?: number;
  occupation?: string;
  category?: string;
  is_differently_abled?: string;
  land_holding_acres?: number;
};

export type Scheme = {
  id: number;
  title: string;
  title_hi?: string | null;
  short_description: string;
  detailed_description?: string | null;
  department: string;
  category: string;
  level: string;
  state?: string | null;
  eligibility_criteria?: string | null;
  benefits?: string | null;
  required_documents?: string | null;
  application_process?: string | null;
  application_url?: string | null;
  helpline?: string | null;
  is_active: boolean;
  created_at?: string | null;
};

export type ChatResponse = {
  response: string;
  language: string;
  recommended_schemes: Array<{
    id?: number | null;
    title: string;
    title_hi?: string | null;
    department?: string | null;
    category?: string | null;
    benefits?: string | null;
    application_url?: string | null;
    helpline?: string | null;
    match_score?: number | null;
  }>;
  source_documents: Array<{
    title: string;
    url?: string | null;
    snippet: string;
  }>;
  suggested_followups: string[];
  metadata?: Record<string, unknown>;
};

export type Application = {
  id: number;
  tracking_number: string;
  service_id: number;
  service_title?: string | null;
  applicant_name?: string | null;
  applicant_phone?: string | null;
  status: string;
  remarks?: string | null;
  documents_submitted?: string | null;
  submitted_at: string;
  updated_at: string;
};

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers ?? {}),
    },
  });

  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`;
    try {
      const body = (await response.json()) as { detail?: string };
      detail = body.detail ?? detail;
    } catch {
      // Keep the HTTP status message when the server does not return JSON.
    }
    throw new Error(detail);
  }

  return response.json() as Promise<T>;
}

export function sendChatMessage(message: string, conversationHistory: Array<{ role: string; content: string }>) {
  return request<ChatResponse>("/chat", {
    method: "POST",
    body: JSON.stringify({
      message,
      conversation_history: conversationHistory,
      language: "en",
    }),
  });
}

export function getSchemes(search?: string) {
  const query = search ? `?search=${encodeURIComponent(search)}` : "";
  return request<Scheme[]>(`/services${query}`);
}

export function getApplications(phoneNumber: string) {
  return request<Application[]>(`/applications/user/${encodeURIComponent(phoneNumber)}`);
}

export function submitApplication(payload: {
  service_id: number;
  applicant_name: string;
  applicant_phone: string;
}) {
  return request<Application>("/applications", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function trackApplication(trackingNumber: string) {
  return request<Application>(`/applications/track/${encodeURIComponent(trackingNumber)}`);
}

export { API_BASE_URL };
