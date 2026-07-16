// Typed client for the endpoints defined in docs/APISpec.md.
// Base URL comes from Catalyst Web Client Hosting's same-origin function
// routing in production; VITE_API_BASE lets local dev point elsewhere.
// Optional chaining on `.env` itself, not just the property under it —
// import.meta.env is a Vite build-time injection and genuinely can be
// undefined outside a Vite runtime (found while trying to runtime-test
// this file directly under plain Node/tsx, which doesn't provide it).

const API_BASE = import.meta.env?.VITE_API_BASE ?? "/server/setu_api";

const DEV_AUTH_HEADERS: Record<string, string> = {};

export function setDevAuth(role: string, stationId: string, districtId: string) {
  DEV_AUTH_HEADERS["X-Dev-Role"] = role;
  DEV_AUTH_HEADERS["X-Dev-Station"] = stationId;
  DEV_AUTH_HEADERS["X-Dev-District"] = districtId;
  DEV_AUTH_HEADERS["X-Dev-User"] = `dev_user_${role.replace(/\s+/g, "_")}`;
}

export type Language = "en" | "kn";

export interface QueryRequest {
  session_id: string;
  text: string;
  language: Language;
}

export interface QueryResponseSource {
  case_id: string;
  relevance: string;
}

export interface QueryResponse {
  answer: string;
  sources: QueryResponseSource[];
  language: Language;
  audit_id: string;
}

export interface ApiError {
  status: "error";
  error_code: "SCOPE_DENIED" | "NOT_FOUND" | "SERVICE_UNAVAILABLE" | "BAD_REQUEST";
  message: string;
}

function isApiError(body: unknown): body is ApiError {
  return typeof body === "object" && body !== null && (body as ApiError).status === "error";
}

async function postJson<TResponse>(path: string, body: unknown): Promise<TResponse> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
      ...DEV_AUTH_HEADERS
    },
    body: JSON.stringify(body),
    credentials: "include", // Catalyst Authentication session
  });

  const data = (await res.json()) as TResponse | ApiError;

  if (isApiError(data)) {
    throw new Error(`${data.error_code}: ${data.message}`);
  }
  return data;
}

export function submitQuery(request: QueryRequest): Promise<QueryResponse> {
  return postJson<QueryResponse>("/api/query", request);
}

export interface HotspotAlert {
  cluster_id: number;
  district: string;
  explanation: string;
  case_count: number;
}

export async function fetchHotspotAlerts(): Promise<HotspotAlert[]> {
  const res = await fetch(`${API_BASE}/api/alerts/hotspots`, { 
    headers: DEV_AUTH_HEADERS,
    credentials: "include" 
  });
  const data = (await res.json()) as { alerts: HotspotAlert[] };
  return data.alerts;
}

export function flagAnswer(auditId: string, wasHelpful: boolean): Promise<void> {
  // FR-10.1 / FR-10.2, added in the Phase 7 review — feedback endpoint not
  // yet in APISpec.md's original list; add it there too when this is wired up.
  return postJson<void>("/api/feedback", { audit_id: auditId, was_helpful: wasHelpful });
}

export interface GraphNode {
  id: string;
  label: string;
}

export interface GraphEdge {
  source: string;
  target: string;
  relationship: string;
  confidence: number;
  suggested_link?: boolean;
  shared_associates?: string[];
  total_associates?: number;
}

export interface NetworkGraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export async function fetchNetworkGraph(entityId: string): Promise<NetworkGraphData> {
  const res = await fetch(`${API_BASE}/api/network/${encodeURIComponent(entityId)}`, {
    headers: DEV_AUTH_HEADERS,
    credentials: "include",
  });
  return (await res.json()) as NetworkGraphData;
}

export interface AuditEntry {
  audit_id: string;
  query_id: string;
  user_id: string;
  query_text: string;
  language: Language;
  sources_used: string[];
  answer_summary: string;
  timestamp: string;
}

export async function fetchAuditLogs(): Promise<AuditEntry[] | ApiError> {
  const res = await fetch(`${API_BASE}/api/audit/logs`, { 
    headers: DEV_AUTH_HEADERS,
    credentials: "include" 
  });
  const data = await res.json();
  if (isApiError(data)) return data;
  return (data as { entries: AuditEntry[] }).entries;
}

export async function exportConversationPdf(sessionId: string): Promise<{ path: string }> {
  return postJson<{ path: string }>("/api/export/pdf", { session_id: sessionId });
}

export async function transcribeAudio(audioBlob: Blob): Promise<{ text: string }> {
  const formData = new FormData();
  formData.append("audio", audioBlob);

  const res = await fetch(`${API_BASE}/api/voice/transcribe`, {
    method: "POST",
    headers: DEV_AUTH_HEADERS, // Do not set Content-Type, fetch handles multipart boundary automatically
    body: formData,
    credentials: "include",
  });
  
  if (!res.ok) {
    const errorBody = await res.json().catch(() => ({}));
    throw new Error(errorBody.message || "Failed to transcribe audio");
  }
  
  return res.json() as Promise<{ text: string }>;
}
