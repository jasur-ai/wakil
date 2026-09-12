# Contract 02 — Case Bus events (P1 emits · P3 persists · P2 renders)

Events are in-process calls into P3's `db.add_event(case_id, type, payload)`; P2 **polls** `GET /case/{id}/events?since=<id>` every 2s (D0-9). Every event gets an autoincrement `id` (the polling cursor).

| Event | Payload | Meaning |
|---|---|---|
| `case.created` | `{mandate}` | Mandate signed; case opened. |
| `turn.outbound` | `{text, guard_verdict, rule?, citation?}` | Every sent message, with its guard verdict (PASS/REWRITE/ESCALATED). |
| `turn.inbound` | `{text, from}` | Counterparty message. |
| `guard.escalation` | `{rule, violation, offer?, options: ["accept_exception","hold","stop"]}` | **User must decide.** P2 renders the modal; the case is blocked until `user.decision`. |
| `user.decision` | `{option}` | From `POST /case/{id}/decision`. |
| `case.resolved` | `{outcome, amount?, article?}` | Closed (verified) or stopped. |
| `verification.result` | `{expected, observed, verdict: "confirmed"|"mismatch"|"unreadable"}` | Screenshot → local vision → money check. Only `confirmed` may trigger "resolved". |
| `dossier.ready` | `{path, completeness}` | .docx built (R10 gate passed). |

**Rules.**
- No event carries PII beyond the evidence allowlist (R03 applies to events too).
- `guard.escalation` must never be auto-resolved by the agent.
- Order matters: P2 renders timeline in event id order; guard chips: green PASS / amber REWRITE / red ESCALATED.
