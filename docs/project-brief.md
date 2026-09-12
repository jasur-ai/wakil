# Project brief — `wakil`

> **Status: CONFIRMED (2026-09-12).** The single source of truth for design is
> [`docs/wakil-v2-winning-edition.md`](docs/wakil-v2-winning-edition.md) (design + why-now/why-us)
> and [`docs/idea1-wakil-deep-dive.md`](docs/idea1-wakil-deep-dive.md) (architecture, schema, workflows).
> Per-role execution plan: [`docs/team-battle-plan.md`](docs/team-battle-plan.md).

## 1. One-line description
**wakil** — a personal Telegram delegate for Uzbekistan that, from a signed mandate, negotiates in-bounds with company support bots and human managers, escalates up the state consumer-protection ladder, and closes the case only after the money is verified.

## 2. Problem / goal
Uzbek e-commerce is growing ~40%/yr, but a consumer whose goods arrive defective rarely wins the refund: it dies in a support chat. The law exists (2023 Consumer Protection Law, Art. 18 = 10-day return) but awareness + friction kill it. A tired person won't file a complaint — so **wakil** does it for them, inside the messenger where the dispute already happens.

## 3. Scope
### In scope (v1 / hackathon)
- Mandate card + **11-rule BoundaryGuard** (mandate-bound agent)
- Negotiation loop vs official support bots + human managers (user-scoped)
- **State escalation ladder** (company bot → supervisor → `@consumergovuz_bot` / 1159) + auto-built **dossier** (.docx)
- **Verified close** (screenshot → local vision → confirmed)
- **Mini App** (onboarding, live timeline, prefs+provenance, search+price table, guardian, WIPE)
- **2FA-enforced** user session, **local-only** data (FastAPI + SQLite on one machine)

### Out of scope (now) → roadmap
- Live Uzum Bank statement auto-nav (needs a live account)
- More company packs (Beeline/Ucell/Kun), multilingual expansion, cloud deploy

## 4. Users
| User | Need |
|---|---|
| UZ consumer (phone-first, Uzbek) | "Chase my refund for me, within my limits, and prove it." |
| Family member | Read-only link to follow a case (guardian). |

## 5. Stack (confirmed)
| Layer | Choice | Notes |
|---|---|---|
| Agent / brain | Python (stdlib guard + corpus; LLM injected, vendor-agnostic) | `brain/` |
| Backend / hands | Python — Telethon + aiogram + FastAPI + SQLite (local) | `hands/` |
| Frontend / face | Single HTML file, vanilla JS, no build step | `face/` |
| DB | SQLite (WAL) — 9 tables | `hands/schema.sql` |
| Infra | One machine (booth laptop) is the only server; Cloudflare quick tunnel for the mini app | local-only by design |

## 6. Milestones
| # | Milestone | Owner | Status |
|---|---|---|---|
| 1 | Repo + consolidation (single public `wakil`) + coordination | Lead | ✅ DONE 2026-09-12 |
| 2 | Trust core green: guard (11 rules, 17 tests) + corpus + session/2FA | AI1/AI3 | 🟡 in progress |
| 3 | Demo: 6 beats, 90s, live | Lead + all | D2–D3 |

## 7. Open questions for the owner
1. `api_id`/`api_hash` for a real MTProto account (AI3).
2. Bot tokens: Mini App face (AI3) + counterparty bot (Lead).
3. 2 phones + 1 "family" phone for the booth (Lead).
4. Any live `@consumergovuz_bot` account for the read-only probe (AI3, D3)?
