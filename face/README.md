# P2 — FACE / Mini App (owner: ai2)

**Mission.** The control surface judges will trust: onboarding that *enforces security*, a live timeline where every guard decision is visible, prefs with provenance, search + price table, and a WIPE that ends the demo on trust.

## Already built by lead (extend, don't rewrite)
`face/index.html` — single-page mini app, dark poster palette, no build step:
- 8-step onboarding (device-only → phone → **2FA-enforce** → scope picker → voice note (Whisper demo) → mandate card → submit → `POST /case`)
- **Live timeline** polling `GET /case/{id}` every 2s (D0-9); guard chips PASS/REWRITE/⚠ESC; citation chips
- **Escalation modal**: violation text + `accept_exception / hold / stop` → `POST /case/{id}/decision`
- Prefs (provenance + delete) · Search + price table + watcher · Guardian link · **WIPE** (type O'CHIRISH)
- UZ/EN toggle (header button)

## Your tasks (docs/team-battle-plan.md §P2)
- **D1 EOD** — wire to the real endpoints (lead's `hands/app.py` serves it at `/`); Cloudflare **quick tunnel** public; wizard + mandate form clickable at the public URL.
- **D2 EOD** — live timeline against real Case Bus events (lead + ai1 will emit `turn.outbound` / `guard.escalation` during integration); timeline + modal on **two phones** (owner + guardian via token); lead approves UZ copy at the D2 standup (native check — gate-level).
- **D3** — polish pass on every demo screen; real-phone check (sizes, contrast, UZ glyph spacing); **you are the tablet operator in the demo** — write the tap-by-tap choreography into `voice/runbook.md`; freeze 14:00.

## Non-negotiables
- One HTML file, no build step (D0-4). If you add a dep, log it in chat.md.
- UI validation mirrors `contracts/00` (an incomplete mandate can never be submitted).
- Every guard decision visible; no silent rewrites. Polling (2s) is the design.
- Demo-critical screens only (runbook beats 1,2,3,4,6). Everything else = roadmap.

## Demo choreography hints (for the runbook)
- Beat 2: tap 🎙️ at step 6 → the Whisper line appears (900ms) → Continue → mandate card auto-filled.
- Beat 3: escalation modal appears red; tap **Kut (hold)** → the next outbound line carries the gold citation chip.
- Beat 6: after close, 👎 (demo shortcut) → pref row with provenance → WIPE → screen goes clean.
