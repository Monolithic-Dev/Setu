# APISpec.md

**Phase 4 of 8 · Challenge 1: Intelligent Conversational AI for the KSP Crime Database**

*All endpoints implemented as Catalyst Functions (Advanced I/O), exposed as REST over HTTPS, authenticated via Catalyst Authentication (OAuth 2.0-based).*

---

## 1. Authentication

All endpoints below require a valid bearer token from Catalyst Authentication. The Auth/RBAC Service resolves the token to a `user_id` + `role_id`, which every downstream service uses to scope its Data Store queries (`Database.md` §4).

---

## 2. Endpoints

### `POST /api/query`
Main conversational endpoint.
```json
// Request
{
  "session_id": "sess_123",
  "text": "ಈ ಕೇಸ್‌ಗೆ ಸಂಬಂಧಿಸಿದ ಇತರ ಪ್ರಕರಣಗಳಿವೆಯೇ?",
  "language": "kn"
}

// Response
{
  "answer": "...",
  "sources": [{"case_id": "KA-2026-00231", "relevance": "structured+semantic"}],
  "language": "kn",
  "audit_id": "audit_9981"
}
```

### `POST /api/voice/transcribe`
Accepts an audio stream, returns transcribed text (routes to Bhashini/Sarvam per `Design.md` §3 Adapter pattern).

### `POST /api/voice/synthesize`
Accepts text + language, returns synthesized audio.

### `GET /api/network/{entityId}`
Returns a graph structure (nodes + edges) for the network visualization, scoped to the requesting user's role.

### `GET /api/alerts/hotspots`
Returns current aggregate hotspot/early-warning signals for the requester's scope (station/district), from the Prediction Service.

### `POST /api/export/pdf`
Given a `session_id`, generates a PDF of the conversation plus its audit trail (via Stratus for storage/delivery).

### `GET /api/audit/logs`
Role-gated (SCRB Analyst / District SP / Admin only) — returns audit entries within the requester's scope.

### `POST /api/feedback`
*(Added Phase 8 — implements FR-10.1/FR-10.2 from the Phase 7 review; missed in the original Phase 4 spec pass, caught while building the client.)*
```json
// Request
{ "audit_id": "audit_9981", "was_helpful": false }

// Response
{ "status": "recorded" }
```
Flags an answer as helpful/unhelpful in-conversation (FR-10.1). Flagged entries are logged separately from ordinary audit entries so quality issues are easy to surface (see `MonitoringStrategy.md`) rather than buried in routine audit volume.

### `POST /api/auth/login`, `POST /api/auth/refresh`
Standard Catalyst Authentication flows.

---

## 3. Error Handling Convention

All endpoints return a consistent error shape:
```json
{
  "status": "error",
  "error_code": "SCOPE_DENIED",
  "message": "Requested data is outside your role's access scope."
}
```
Errors distinguish `SCOPE_DENIED` (RBAC), `NOT_FOUND` (no grounding evidence — never silently fabricated, per FR-3.3), and `SERVICE_UNAVAILABLE` (upstream Bhashini/Sarvam/QuickML issue, triggers the fallback path in `Design.md` §3).

---

*Next: `Security.md`, `Deployment.md`, `UX.md`.*
