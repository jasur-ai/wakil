# Contract 03 — Mini App REST (P3 serves on :8000 · P2 consumes, same-origin)

Local-only (D0-5). Demo auth = none (single user); guardian view is token-scoped.

| Endpoint | Payload | Notes |
|---|---|---|
| `GET /health` | → `{ok, cases, events}` | Liveness for the UI status dot. |
| `POST /case` | `{mandate}` → `{case_id}` | Mandate validated against `contracts/00` (server-side; UI validation mirrors it). |
| `GET /case/{id}` | → `{id, status, mandate, timeline[≤50], pending_decision: bool}` | Pending = a `guard.escalation` with no later `user.decision`. |
| `GET /case/{id}/events?since=<id>` | → `[{id, type, payload, created_at}]` | **Polling endpoint (2s).** |
| `POST /case/{id}/decision` | `{option: "accept_exception"|"hold"|"stop"}` → 202 | Emits `user.decision`; unblocks the agent. |
| `GET /prefs` | → `[{key, value, provenance}]` | Typed learned prefs. |
| `POST /prefs` | `{key, value, provenance?}` | |
| `DELETE /prefs/{key}` | | User deletes a learned pref. |
| `GET /search?k=<query>` | → `{results: [{text, dialog, ts, url}], price_table: [{item, source, price, url}]}` | Via `search_global` (Contract 01). |
| `POST /watch` | `{keyword, scope}` → `{watcher_id}` | 2-min cadence watcher; new post → bot-DM ping + jump link. |
| `POST /wipe` | → `{wiped: true, tables: [...]}` | Deletes every row. Irreversible. |
| `GET /case/{id}/guardian?token=<t>` | → read-only `{id, status, mandate, timeline}` | No decision endpoints. Family member gets the link. |

**UI contract:** one HTML file (`face/index.html`), no build step (D0-4). Tunnel: Cloudflare quick tunnel to `localhost:8000`.
