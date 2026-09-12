# "Agents Are Leaving the Chatbox" — 12 Deep-Researched Winning Ideas
### Prepared 2026-09-12 · for a Tashkent-based team · every idea mapped to the 4 judging criteria

---

## 0. How to win this hackathon (read this first)

### 0.1 What the rubric actually rewards (decoded)

The rubric's wording leaks the judging strategy. Here is what separates a **4** from a **5** on each criterion:

| Criterion | A 4 looks like… | A 5 looks like… |
|---|---|---|
| **Core functionality** | Complete demo with minor bugs | Zero-bug core loop + graceful handling of the demo's failure case, live, on real infrastructure |
| **Innovation & theme** | "The environment adds meaningful value" | "A *surprising new agent pattern* whose central value could not be reproduced in a standalone chatbox" — the judges explicitly want a **pattern**, not a use case |
| **Technical execution** | Working integrations, some rough edges | "Robust orchestration, thoughtful failure handling, deeply integrated architecture" — failure handling is named **twice** in the rubric |
| **Usefulness & experience** | Solves a clear problem, feels native | "Uses context intelligently while remaining **clear and controllable**" — human-in-the-loop control is named explicitly |

**Three meta-conclusions:**
1. **The demo must run on real infrastructure, not a slide.** A real phone number, a real Telegram bot, a real browser tab, a real screen. "Working agent *inside* a place" (criterion 1) is literally impossible to prove with a mockup.
2. **Name a pattern, not a product.** Winning pitches frame as "we found that [environment] makes a new class of agent possible: the [operator / second-self / ambient-sentinel] pattern." The rubric's 5-score wording is your script.
3. **Design a visible failure.** Engineers lose points on hidden bugs and win points on *thoughtful failure handling*. Build one deliberate failure into the demo (network drop, ambiguous voice, missing data) and show the agent degrade gracefully, escalate to a human, and recover.

### 0.2 The four patterns that score 5 on Innovation

| Pattern | Meaning | Example idea below |
|---|---|---|
| **Operator** | The agent *drives the machine's UI itself* (computer-use inside the environment), not chatting about it | #8 Kiosk Operator, #4 Portal Agent |
| **Second-self** | The agent lives across *all* surfaces of a person/business (DMs + groups + channels + calls + payments) as a coherent actor with memory | #1 Telegram Bazaar Agent |
| **Ambient sentinel** | The agent has *context no chatbox can have* (a queue, a till, a wrist, a room) and acts proactively from it | #3 POS Sentinel, #5 Waiting-Room TV, #10 Wrist Agent |
| **Hands-free colleague** | The environment is a *body in motion* (ladder, road, kitchen line); the agent is the worker's teammate, not an app they open | #2 IVR Voice Agent, #7 Field Agent, #9 Kitchen Agent |

### 0.3 Your unfair advantage: you are in Tashkent

A global team building "agents for the places people already work" will default to Slack, Gmail, and US SaaS. You can build on the surfaces **2.9M Tashkent residents actually live in** — and the data says those surfaces are underserved by agent tooling:

- **Telegram is Uzbekistan's #1 messaging platform: ~88% adoption, ~25M users (≈85% of the population).** WhatsApp is "minimal" in UZ by comparison. Telegram is the chatbox your judges' users already live in — and it has the best agent surface of any messenger (details in §0.4). [kursiv.media](https://kz.kursiv.media/en/2025-04-10/engk-yeri-digital-habits-why-kazakhstan-loves-whatsapp-and-uzbekistan-prefers-telegram/) [101digital.uz](https://101digital.uz/en/blog/uzbekistan-digital-marketing-report-2026/)
- **Tashkent: 2.9M people, 97% internet penetration, "very high" e-commerce activity.** [101digital.uz](https://101digital.uz/en/blog/uzbekistan-digital-marketing-report-2026/)
- **Mobile connections = 95.5% of the population** — people here work and buy from a phone, not a desktop. [kursiv.media](https://kz.kursiv.media/en/2025-04-10/engk-yeri-digital-habits-why-kazakhstan-loves-whatsapp-and-uzbekistan-prefers-telegram/)
- **Delivery & mobility are app-native:** Yandex Go, Yango, Pedal.uz are the local surfaces; a local team can demo against them or their equivalents. [singular.net](https://www.singular.net/blog/food-delivery-apps/)
- **The language gap is a moat.** Almost no agent stack does fluent **Uzbek** (and Tashkent speakers *code-switch* UZ/RU/EN mid-sentence — an authentic, defensible design feature, and a robustness story the judges will remember).

### 0.4 The Telegram surface (your best "real environment")

Telegram is the only major messenger whose bot platform is **free, open, and agent-grade out of the box** — this makes it the single best hackathon environment (instant real deployment, zero platform approval friction):

- **Bot API is completely free** — no per-message fees, no template approval, no business verification. A bot is live in under 10 minutes via @BotFather. Contrast: WhatsApp Business API charges per conversation and requires Meta verification + template approvals. [blocksentient.com](https://blocksentient.com/review/telegram-bots/) [chatbotscape.com](https://chatbotscape.com/channels/telegram-chatbot-guide)
- **Telegram passed 1 billion MAU in March 2025.** [chatbotscape.com](https://chatbotscape.com/channels/telegram-chatbot-guide)
- **Agent-relevant surface:** inline keyboards, Mini Apps (a full web app *inside* the chat), **Telegram Stars payments + subscriptions** (Bot API 7.9/9.1), voice messages in/out, 50MB file uploads, **group/forum participation** (bots in multi-party group chats), business mode, checklists, paid messages. [core.telegram.org](https://core.telegram.org/bots/webapps) [BotNews](https://t.me/s/BotNews?before=110)
- Global context for why messaging is a first-class agent environment: the WhatsApp Business API market alone is **$8.2B (2025) → $38.6B (2034), 18.8% CAGR**; 175M+ messages reach business accounts daily with ~90% open rates; in mobile-first markets **80% of small businesses already use the dominant messenger to communicate with customers**. [dataintelo.com](https://dataintelo.com/report/whatsapp-business-api-platform-market) [electroiq.com](https://electroiq.com/stats/whatsapp-business-statistics/)

**Stack recommendation for Telegram ideas:** Python/Node bot (aiogram/grammY) → LangGraph/CrewAI agent loop → Postgres + pgvector (memory) → Stars/Payme for money → Mini App for the "app inside chat" moment.

---

## IDEA 1 — "Do'kon" (Shop): the vendor's second-self across its whole Telegram surface

> *A small Tashkent vendor (bazaar goods, home-baked naan, Instagram-style drops) gets an agent that runs its business across DMs, the customer group, the channel, voice notes, payments, and the delivery driver — as one consistent "second self."*

- **Pattern:** Second-self. **Theme environment:** messaging — where Tashkent commerce conversations actually happen.
- **Why this place (theme logic):** In Tashkent, buying is a *conversation*: customers negotiate in a vendor's Telegram group, send **voice notes** ("I'll take two kilos of this, can you bring it to Yunusobod?"), and pay via a wallet link. A standalone chatbot can't do that because the value isn't in answering one query — it's in *holding the whole commerce state* (inventory, price, route, who already ordered) across every surface at once and closing the loop with payment + delivery.
- **Evidence:** Telegram = 88% of UZ, 25M users [kursiv](https://kz.kursiv.media/en/2025-04-10/engk-yeri-digital-habits-why-kazakhstan-loves-whatsapp-and-uzbekistan-prefers-telegram/); 80% of SMBs in mobile-first markets use the dominant messenger with customers [electroiq](https://electroiq.com/stats/whatsapp-business-statistics/); Telegram Bot API free + Stars payments + Mini Apps = zero-friction real deployment [blocksentient](https://blocksentient.com/review/telegram-bots/).
- **End-to-end flow:**
  1. Customer DMs or posts in the group: voice note or text order, in UZ, with negotiation ("is 45k for two loaves possible?").
  2. Agent transcribes (Whisper `uz`), understands price negotiation bounds from a price sheet (Google Sheet = inventory/price system of record), counter-offers or confirms with an inline confirm button.
  3. On confirm: reserves stock (deducts in the Sheet), sends a **Stars/Payme payment link**, on payment webhook marks the order paid.
  4. Every 15 min the agent rolls orders into a **delivery batch**, messages the driver's bot with the route (group of 3–4 stops), and updates each customer ("your order is #2, arriving ~18:40").
  5. Proactively: vendor posts a drop in the channel → agent tracks the group's reactions/questions for 24h and answers with catalog context; Friday rush → agent pre-warns the vendor with predicted volume from historical orders.
  6. End of day: agent posts a daily digest to the vendor (revenue, top items, near-expiry stock) and suggests tomorrow's bake list.
- **Architecture:** aiogram bot (DM + group + channel, one process) → LangGraph agent with tools: `read_sheet`, `write_sheet`, `request_payment`, `send_driver_message`, `batch_orders`, `forecast` → Whisper STT for voice notes → TTS voice replies in UZ/RU → Postgres for order memory → Mini App = order tracker for customers ("where is my naan").
- **Why it's not a chatbox wrapper:** the agent's state is *outside* the chat (Sheet + Postgres + driver channel + payment webhook); the chat is only the interface. Remove the Telegram ecosystem (groups, channel, voice, Stars, driver bot) and it's just a FAQ bot — the value is in the multi-surface orchestration.
- **Failure handling (visible in demo):** payment webhook times out → order stays "awaiting payment," agent re-links after 10 min, never double-charge; voice note too noisy → agent asks one clarifying question, never guesses quantity; stock mismatch (two customers same item) → first-come reserved, second offered substitute + reason.
- **Demo (90s):** judge speaks a voice-note order in Uzbek inside a public bot → negotiates → pays via a test Stars/Payme link → driver bot in a second group receives the batch → customer Mini App shows live status → daily digest appears for the vendor. One deliberate failure: kill the payment webhook once; agent degrades gracefully.
- **Score map:**
  - Functionality: **4.5–5** — every integration is real and free-tier; end-to-end loop is short enough to be bug-free.
  - Innovation: **4** — messaging is an eligible environment and the multi-surface second-self is original, but the environment *is* a chatbox, so a strict judge caps at 4. Frame the pattern explicitly to push up.
  - Execution: **4.5** — clean tool graph, real webhooks, honest fallbacks.
  - Usefulness: **4.5–5** — a Tashkent vendor watching a stranger run their shop's back half in real time is the most visceral "clear value" moment possible for a local team.
- **Risks / build plan:** Uzbek STT quality (Whisper uz is decent; mitigate with UZ/RU code-switching and short clarifying questions). 48h plan: D1 = bot + sheet tools + payment; D2 = driver batch + Mini App + digest; D3 = failure paths + demo polish.
- **Prior art & differentiation:** Wati/Respond.io-style chatbots are *ticket bots for one business account*. Nobody is running a vendor's *entire commerce* (negotiation → reservation → payment → driver batching → forecasting) across the group+channel+DM ecosystem in Uzbek. The localization + voice-first negotiation is the moat.

---

## IDEA 2 — "Raqam": the phone number is the office (AI voice agent inside a real IVR tree)

> *A small Tashkent service business (dental clinic, car service, auto-wash) keeps the same phone number people already call — but the "press 1… press 2" tree is gone. A fluent voice agent answers, books, triages, confirms, and calls back. The phone is the last unmodernized surface, and the agent lives there.*

- **Pattern:** Hands-free colleague / legacy-surface takeover. **Theme environment:** voice / telephony — the place people *already call*.
- **Why this place (theme logic):** The phone tree is a 40-year-old UI: rigid menus, dead ends, "your call is important to us." An agent on the line can do things no chatbox can: **be reached by anyone with no app, no account, no onboarding** — including the 55-year-old who only knows how to dial. The environment's constraint (real-time, one-directional, no screen) is exactly what makes the agent pattern original: it must *speak, interrupt-handle, and act while talking*.
- **Evidence:** Gartner: by 2026, **1 in 10 customer-agent interactions will be automated** (~$80B labor cost impact) [nlpearl](https://nlpearl.ai/the-end-of-call-centers-as-we-know-them-how-ai-voice-agents-will-reshape-2025-2028); 80% of enterprises already run *some* voice agent but only **21% are very satisfied** — the IVR gap is the opportunity [Deepgram](https://deepgram.com/learn/state-of-voice-ai-2025); AI IVR adoption projected **78% (2025) → 85% (2026)** [AI IVR 2026 roundup](https://www.reddit.com/r/realestateainews/comments/1sxu3hg/ai_ivr_in_2026_top_companies_market_trends_and/); voice-AI market **$2.4B (2024) → $47.5B (2034)** [leadsnow](https://leadsnow.ai/ai-voice-agent-adoption-statistics-2026/); **60.7% of homeowners prefer booking via AI voice over a web form** [leadsnow](https://leadsnow.ai/ai-voice-agent-adoption-statistics-2026/).
- **End-to-end flow:**
  1. Call hits the business's real Twilio number (24/7, including nights).
  2. Agent answers in UZ (RU on request): "Assalomu alaykum, this is Dentis Clinic. How can I help?"
  3. **Book:** "I want a cleaning next week" → agent reads the calendar (Google Calendar), offers 3 real slots, confirms, sends SMS + Telegram confirmation.
  4. **Triage:** describes pain → agent classifies urgency; urgent → books same-day + flags the doctor's queue; non-urgent → normal slot.
  5. **Confirm/cancel:** morning-of, agent *calls back* to confirm appointments (new behavior: outbound campaign from the agent); no-show risk → offers reschedule by voice.
  6. **Handoff:** anything beyond policy ("is this covered by insurance?") → warm transfer to a human with a live transcript pinned to the staff screen.
- **Architecture:** Twilio Voice (real number) → Deepgram Nova streaming STT (UZ/RU) → LLM agent (LangGraph) with tools: `read_calendar`, `book_slot`, `cancel`, `sms_confirm`, `transfer_human`, `log_visit` → UZ TTS (ElevenLabs / edge-tts fallback) → live transcript UI for staff (the "human sees what the agent heard" trust layer).
- **Why it's not a chatbox wrapper:** the environment *is* the product — latency budget (<800ms turn), barge-in (customer interrupts), phone-state (mute, hold, callback scheduling) are all things a chatbot never has. A chatbox version is strictly worse (nobody installs an app for a toothache).
- **Failure handling (visible in demo):** STT confidence low → agent repeats/clarifies once, then offers "I'll call you back" (schedules an outbound call — the *phone-native* fallback, a lovely touch); calendar tool error → agent apologizes, books a callback, never invents slots; angry customer → sentiment drop triggers warm transfer.
- **Demo (90s):** a judge dials a real number from their phone mid-pitch, books a slot in Uzbek, asks an edge question, gets transferred to a staff screen with the transcript. Then the team shows the morning confirmation call hitting a teammate's phone.
- **Score map:**
  - Functionality: **4–4.5** — real telephony is the risk (latency, flaky TTS); plan a rehearsed happy path + one live failure.
  - Innovation: **4.5–5** — "the IVR tree is dead" is a genuinely fresh framing, and voice-real-time is a pattern impossible in a chatbox.
  - Execution: **4** — streaming voice pipelines are fiddly; the transcript+transfer trust layer is what lifts it to "thoughtful."
  - Usefulness: **5** — for a clinic that misses 30–40% of after-hours calls, this is obvious money; the local UZ-language voice makes it feel *made for here*.
- **Risks / build plan:** UZ TTS quality is the biggest unknown — mitigate by (a) RU-first agent with UZ greetings/confirmations (authentic Tashkent code-switching), (b) ElevenLabs voice cloning of a teammate. Twilio trial numbers work for demos. 48h: D1 = Twilio↔Deepgram↔LLM loop; D2 = calendar + SMS + transfer; D3 = confirmations + failure paths.
- **Prior art & differentiation:** Vapi/Retell/Bland exist as *platforms* (and are US/English-first). The submission is a **deployed, localized, calendar-owning agent for a real Tashkent business with an outbound confirmation behavior** — not a wrapper around a voice platform.

---

## IDEA 3 — "Kassa": the sentinel inside the cashier's screen (POS browser agent)

> *A browser-extension agent lives on the web-POS screen of a small shop. It watches the live till in real time, catches mistakes the human never sees (wrong change, un-scanned item, discount abuse), reconciles the shift, reorders low stock, and messages the owner a daily truth-report in Telegram. The POS is where business truth actually happens — and nobody is watching it.*

- **Pattern:** Ambient sentinel. **Theme environment:** web/browser — specifically *on top of the screen where the transaction physically happens*.
- **Why this place (theme logic):** Every other "business AI" listens to the *data after* the sale. This agent lives **in the register UI at the moment of the sale**: it sees what the cashier is about to do, in context, with the customer's face three feet away. That's the only place where catchable errors (change short by 2,000 som, loyalty discount applied twice) are still catchable. A chatbox fed a spreadsheet learns yesterday's mistakes; this one stops today's.
- **Evidence:** the industry is converging here: **Salesforce launched Agentforce for Retail + a cloud POS (Jan 2025)** with agent skills for order management and guided shopping [pymnts](https://www.pymnts.com/news/artificial-intelligence/2025/salesforce-launch-ai-agents-cloud-based-pos-retailers/); **Microsoft rebuilt Dynamics 365 Commerce POS explicitly as an "agentic" platform** with Copilot insights for associates [microsoft.com](https://www.microsoft.com/en-us/dynamics-365/blog/it-professional/2025/06/03/under-the-hood-building-an-ai-driven-storefront-with-dynamics-365-commerce-pos/). But both target big retail with enterprise stack — **nobody has done the sentinel for the 2-person Tashkent kirya/kiosk running a €30/month web POS**.
- **End-to-end flow:**
  1. Extension loads into the web-POS tab (Chrome MV3, content script). It reads the live register state via DOM + the POS's event bus/websocket (our demo POS emits these; a real POS like SmartPOS has webhooks [smartposai](https://smartposai.com/)).
  2. **Live sentinel:** each line-item change is checked by the agent: price vs price-list, discount vs policy (max 10%, manager code required above that), change-computation verification, item-not-scanned detection (weight mismatch at the scale, for produce).
  3. On anomaly: agent overlays a **non-blocking warning** on the register screen (red pulse + one-line reason) and, if cashier ignores it twice, silently flags it and notifies the owner's phone.
  4. **Shift close:** agent auto-reconciles (tender totals vs payment-channel webhooks: Payme/Click/cash), produces a discrepancy report, and sends it to the owner on Telegram with a 3-line UZ summary.
  5. **Reorder:** stock below threshold → agent drafts the supplier order (pre-agreed supplier price list), owner approves with one tap in Telegram.
  6. **Owner copilot:** owner can ask the extension (or Telegram) "what sold today vs last week" — agent answers from live till data, not stale exports.
- **Architecture:** Chrome extension (content script + sidepanel) → local agent (small model on-device for latency + cloud LLM for summaries) → rules + LLM hybrid anomaly engine → Telegram bot for owner (approvals, reports) → SQLite/Postgres for shift history → demo POS = open web-POS (we build a faithful 1-page register with websocket events, 1 day of work).
- **Why it's not a chatbox wrapper:** the agent's eyes are on the *live DOM of the register*. The value (catching the error at t=0) is destroyed the moment you move it out of the screen. The extension is the environment integration, not a skin.
- **Failure handling (visible in demo):** false-positive storm → agent auto-mutes its own alerts after 3 overrides and logs the pattern (self-governance, judges love this); POS tab crashes → extension reconnects and back-fills from the event log; ambiguous discount → escalates to owner Telegram instead of blocking the line (business never waits on AI).
- **Demo (90s):** live register in front of judges: cashier (teammate) makes 3 deliberate mistakes — agent catches 3/3 in real time with on-screen pulses; ignore-once behavior shown; end shift → reconciliation report lands in the owner's Telegram with the discrepancies marked; owner approves a reorder from Telegram.
- **Score map:**
  - Functionality: **4.5–5** — fully self-contained, no external flakiness beyond our own POS; the most controllable demo of the list.
  - Innovation: **4–4.5** — sentinel-on-the-register is an original pattern (Microsoft/Salesforce do copilot-for-staff, not real-time error sentinel + owner-reconciliation in one); extension-as-agent is fresh.
  - Execution: **4.5–5** — browser extension + event-driven agent + Telegram approval loop is a genuinely well-scoped engineering story.
  - Usefulness: **4.5** — cash leakage in small retail is real and measurable; "the owner sees what the till actually did" is instantly understood.
- **Risks / build plan:** DOM-reading fragility (we own the demo POS, so fine; be honest in pitch that real POSes vary — that's the roadmap). 48h: D1 = demo POS + extension skeleton + 3 detectors; D2 = shift reconciliation + Telegram reports; D3 = reorder loop + self-mute + polish.
- **Prior art & differentiation:** Knowlix/SmartPOS ship "AI assistant, ask in your language" [knowlix](https://knowlix.ai/ai-point-of-sale-software) [smartposai](https://smartposai.com/) — that's a *chat panel inside the POS*. The sentinel is the opposite: **no chat at all** — an agent that watches, flags, reconciles, and reports. That contrast is the pitch.

---

## IDEA 4 — "Davlat": the agent inside the government portal (browser computer-use for bureaucracy)

> *A browser agent that lives inside bureaucratic web portals (e-services, tax, permits, visa). You point it at the form; it sees the form, knows the rules, fills it from your documents, explains every field in Uzbek/Russian/English, flags what's missing, tracks status, and submits — with a human pressing the final button. Bureaucracy is where people already work, talk to the state, and live under rules — and the portals are APIs-free UIs that only a *seeing* agent can navigate.*

- **Pattern:** Operator (computer-use). **Theme environment:** web/browser — the state's digital front door.
- **Why this place (theme logic):** Government portals have **no public API** — they're just UIs. They were never designed for humans (dense, jargon, multi-step, stateful) and impossible for classic automation (RPA dies on any redesign). A *seeing* browser agent is the only agent class that can live there. And the environment contributes something a chatbox never has: **the ground truth of what the form actually requires right now** — field-by-field, in the moment, against your specific documents.
- **Evidence:** browser-use agents crossed from lab to operational in 2025: **OpenAI Operator ~87% on browser benchmarks, Mariner ~83.5%, Claude Computer Use 44% on OSWorld in 2026 vs 14% in 2024** [xelionlabs](https://xelionlabs.com/blog/ai-browser-agents-guide) [actgsys](https://actgsys.com/en/blog/ai-browser-agent-operator-business-2026); **62% of enterprises experimenting** with browser agents in 2026; 30-field form tasks run **~8x faster** (90s vs 12+ min) [xelionlabs](https://xelionlabs.com/blog/ai-browser-agents-guide); SME back-office automation saves **75–85% of repetitive hours**, with import/export + government portals the #1 benefit [actgsys](https://actgsys.com/en/blog/ai-browser-agent-operator-business-2026); citizen-services AI market heading to **$67B by 2030 at ~33% CAGR**; municipal chatbots already handle 30–50% of routine inquiries at **$0.50–2 per interaction vs $8–15** for live staff [mindstudio](https://www.mindstudio.ai/blog/government); BCG: GenAI's strongest government fit is *interactive form assistance and case processing* [bcg](https://www.bcg.com/publications/2025/benefits-of-ai-in-government).
- **End-to-end flow (demo service: e.g., a registration/permit/registration-style public form):**
  1. User (in UZ or RU): "I need to renew X. Here are my documents." → user drops photos/PDFs into the companion (browser sidepanel or Telegram).
  2. Agent **ingests documents** (OCR + vision): extracts name, ID numbers, dates — builds a *document graph* it can cite.
  3. Agent **navigates the real portal** (Playwright/computer-use loop): logs in (user's session), reaches the form, and **reads it live** — field by field, including dynamic conditional fields (the part RPA and chatbots can't see).
  4. For each field the agent decides: *fill from document X* (shows the source snippet), *ask the user* (in the sidepanel, plain language, UZ), or *not applicable* — with a reason.
  5. **Pre-submission review:** the agent produces a "before you submit" checklist: what it filled, what it couldn't, what the rules say will happen next (timeline, fees, office address). Human presses **Submit** — always.
  6. After submission: agent **watches the status page** on a schedule, summarizes changes ("your application moved to review, expected 5 working days"), and pings the user on Telegram.
- **Architecture:** browser extension or Playwright-driven tab (computer-use: screenshot + DOM accessibility tree → action model) → LLM planner (LangGraph) with tools: `ocr_doc`, `navigate`, `fill`, `read_field`, `check_rulebook` (RAG over the service's rules text), `notify` → rulebook = scraped public help pages of the portal → Postgres for case memory → Telegram for status pings and document drop-off.
- **Why it's not a chatbox wrapper:** the agent *is inside the portal*. The core value — seeing the form's actual current state and reconciling it with your documents — cannot be reproduced anywhere else; a chatbox version is just a document-filling app that breaks the moment the portal changes.
- **Failure handling (visible in demo):** captcha/2FA → pauses with a clear "your turn" handoff; unrecognized document field → never guesses, asks; portal page redesign mid-task → agent re-grounds from the accessibility tree and reports the diff; wrong-data risk → **no field auto-submits without either a document source or an explicit human confirm** (the control story the rubric asks for).
- **Demo (90s):** live browser, real public portal account: agent walks a real form end-to-end, fills 12/15 fields from documents (each with its source shown), asks 2 clarifying questions in UZ, produces the review checklist, and shows the scheduled status-watch. If live access is flaky that day (portal outages are a fact of life), fallback = a **faithful 1:1 clone of the portal** pre-captured, with the difference stated honestly — plus a video of a live run recorded that morning.
- **Score map:**
  - Functionality: **4** — highest external-dependency risk of the list; the clone-fallback protects the demo but a live run scores visibly higher.
  - Innovation: **4.5–5** — "an operator that lives inside a form" is exactly the *new pattern* wording; computer-use agents for civic forms in UZ are a blank space.
  - Execution: **4** — computer-use loops need care; the document-citation + rulebook-RAG design shows real architecture thinking.
  - Usefulness: **4.5–5** — everyone in the room has suffered this; "3 hours at the queue → 20 minutes on your couch, in your language" is the clearest value statement on this list.
- **Risks / build plan:** portal access/captcha/legal — pick a **public, non-sensitive, high-friction form** (avoid anything PII-heavy); record everything; be explicit about boundaries (the agent never submits without a human). 48h: D1 = document graph + portal navigation loop; D2 = field decisioning + rulebook RAG + checklist; D3 = status watch + clone fallback + demo.
- **Prior art & differentiation:** Operator/Mariner are *generic*; Supervity/Aigentiq sell *gov agencies* (top-down) [supervity](https://www.supervity.ai/ai-agents-for-government) [aigentiq](https://www.aigentiq.com/industries/public-sector). Nobody has built the **citizen-side, UZ-language, document-to-form operator** for Central Asian portals. That's the gap.

---

## IDEA 5 — "Navbat": the agent on the waiting-room screen (the TV is the front desk)

> *Every clinic, DMV-style office, and government service hall has a screen. Today it shows an ad or a channel number. Make the screen a live agent: it reads the real appointment queue, announces in Uzbek and English, preps patients before their room is ready, sends proactive delay notifications to phones, and escalates quietly to staff. A multimodal sentinel in a place nobody expects an agent.*

- **Pattern:** Ambient sentinel + "nobody expects it yet." **Theme environment:** the physical waiting room, via its screen (+ mic + speaker).
- **Why this place (theme logic):** The waiting room is where service *breaks silently*: patients don't know if they're forgotten, staff shout names that get missed, delays are discovered late and all at once. The screen in the room is a **pre-installed, ambient, shared surface** — no app, no device, no install, visible to everyone at once. An agent there has context no chatbox can: the *queue itself*, in real time, plus the room's attention.
- **Evidence:** the healthcare/waiting-room pain is the classic voice-AI motivation (queue times cut up to ~50%, CSAT +30% cited in deployments [mavenagi](https://www.mavenagi.com/blog/voice-ai-statistics-customer-service)); ambient/assisted-living tech is booming (**$67.7B market in 2025, ~2x by 2032**; smart AAL segment growing ~30.8% CAGR [marketgrowthreports](https://www.marketgrowthreports.com/blog/ambient-assisted-living-and-smart-home-companies-143) [grandview](https://www.grandviewresearch.com/industry-analysis/ambient-assisted-living-smart-home-market-report)) — proof that "the environment senses and acts" is a validated pattern; kiosks/signage are explicitly going conversational (Zamok's AI chat agent for kiosks announced for 2026; EU Accessibility Act June 2025 requires accessible self-service — an accessibility *obligation* with a deadline [kioskindustry](https://kioskindustry.org/payments-public-sector-advanced-kiosks/)).
- **End-to-end flow:**
  1. Agent receives the **live queue** (integration with the clinic's scheduling system; demo: a small PMS-like service that emits appointment events).
  2. Screen shows a calm, multilingual status: who's next (last name only — privacy by design), estimated wait, room number when ready.
  3. **Voice + vision in the room:** a patient can raise a hand / say "where am I?" → mic picks it up, agent answers (bilingual UZ/EN), shows them their place in line on screen.
  4. **Proactive delay handling:** if a slot slips >10 min, agent: (a) announces an *estimated* (never a promise), (b) sends an SMS/Telegram ping to affected patients with the new estimate, (c) pings the doctor's assistant privately. Nobody shouts, nobody discovers late.
  5. **Prep before the room is ready:** 2 minutes before, the screen tells *that patient* (by first name, on their QR-check-in device or the room board): "Document check complete — please prepare your insurance card."
  6. **Escalation:** 2 unacknowledged delays → agent drafts a note to the manager (never to the patients) with options.
- **Architecture:** kiosk browser on a TV/tablet → queue service (events) → agent (LangGraph) with tools: `read_queue`, `announce` (TTS UZ/EN), `sms_notify`, `notify_staff`, `check_in` → camera (optional, privacy-off by default; presence via QR check-in instead) → all announcements logged for the clinic's review.
- **Why it's not a chatbox wrapper:** the interface is a *shared, ambient, multimodal surface* — one agent, many simultaneous listeners, zero personal devices. The queue-context + proactive-SMS loop has no chatbox equivalent at all.
- **Failure handling (visible in demo):** queue feed drops → screen shows "updating…", never a wrong order, and re-syncs; TTS fails → falls back to on-screen text (the screen always shows what was said — accessibility); angry patient at the mic → sentiment triage → staff ping, agent stays neutral.
- **Demo (90s):** a real TV on stage, live queue ticking; judge checks in with a QR, asks a question by voice, watches the screen answer; team triggers a 15-min delay → judges see the SMS hit a phone + the screen update + the private staff ping. The moment the judge's phone buzzes while the TV explains itself is the whole pitch.
- **Score map:**
  - Functionality: **4.5–5** — self-contained (our own queue service + TV + Twilio SMS); low external risk; very rehearse-able.
  - Innovation: **4.5–5** — "the waiting-room TV is now an agent" is exactly the *somewhere nobody expects* line; the accessibility angle (EAA) adds global resonance.
  - Execution: **4** — multimodal kiosk pipelines have rough edges (mic echo, TTS); the "screen mirrors speech" design is a genuine a11y feature, not a crutch.
  - Usefulness: **4.5** — anyone who's ever sat in a queue in Tashkent (or a hospital anywhere) feels this instantly.
- **Risks / build plan:** mic/TTS quality in a loud room (demo is controlled); privacy optics (be explicit: last-name-only, QR-based identity, camera optional/off). 48h: D1 = queue service + screen UI + announce loop; D2 = SMS + staff escalation + check-in; D3 = voice Q&A + delay-scenario rehearsal.
- **Prior art & differentiation:** Way-finding screens (Google Nest-style) are *passive displays*; lobby chatbots are *one-to-one kiosks*. The **proactive queue-sentinel that talks, pings phones, and escalates to staff from a shared ambient surface** is a new pattern.

---

## IDEA 6 — "Uy" (Home): the household agent living on the family's screen

> *A 4-person Tashkent household: two parents, a student, an elderly parent on weekends. The agent lives on the family's TV/tablet (the one surface everyone already looks at) plus a family Telegram group. It's not a speaker that turns lights on — it's the household's **memory and logistics layer**: what's for dinner, who's driving, when the bill is due, whether grandma said good morning, and it *proposes* — the family approves in the chat where they already talk.*

- **Pattern:** Second-self (for a household) + ambient. **Theme environment:** the home — literally "where people live."
- **Why this place (theme logic):** Smart-home assistants stop at *device control*. The home's real workload is **logistics + memory + care**: meals, bills, school runs, medication, checking in on the elder. The home is the one environment where an agent can have *persistent, multi-person context* (calendars, smart locks, fridge list, family chat) and act **proactively on a schedule** — the opposite of a request-response chatbox. Google/Amazon's 2025–26 direction (Gemini "proactive suggestions," Health Guardian, Alexa+) confirms ambient proactive agents are the platform frontier [google blog](https://blog.google/products-and-platforms/devices/pixel/pixel-watch-5/), but no one has built the *household* version — the one that coordinates four people and one elder.
- **Evidence:** ambient intelligence is the named next era of the home (research consensus: context-aware, proactive, implicit-input homes [mdpi review](https://www.mdpi.com/2073-8994/18/5/718)); AAL market $67.7B 2025 [marketgrowthreports](https://www.marketgrowthreports.com/blog/ambient-assisted-living-and-smart-home-companies-143); on-device/ambient trends reducing cognitive load are the 2026 appliance narrative [lifetips](https://lifetips.alibaba.com/tech-efficiency/smart-appliance-trends-that-will-make-your-home-functional-in-2026).
- **End-to-end flow:**
  1. **Morning:** agent composes a household brief on the TV: weather, student's exam tomorrow, bill due in 3 days (Payme link pre-drafted), grandma's usual 9:00 video call — one tap to "do all."
  2. **Fridge list:** family taps items on the TV list as they run out (or the agent suggests from meal planning) → agent batches into a **delivery order draft** (local delivery service) → parent approves in the family Telegram group with one tap.
  3. **Dinner loop:** 18:00, agent asks the group "who's hungry for what?" — actually *reads* the group chat all day (who mentioned being tired, who has a game at 20:00) and proposes the meal + grocery top-ups from that context.
  4. **Elder check-in:** grandma's morning video call or a voice message by 10:00 → logged. **Silence rule:** if no signal by 11:00 → agent messages the daughter on Telegram: "No sign from grandma since 07:40 — want me to call?" (and can dial on confirm). This single loop is the emotional core of the demo.
  5. **Memory:** "what did we decide about the summer trip?" → agent answers from months of group-chat history (pgvector).
- **Architecture:** Home Assistant hub (locks, sensors, TV as dashboard) → LangGraph household agent with tools: `read_calendar` (shared CalDAV/Google), `read_group_chat` (family Telegram bot), `draft_order`, `draft_bill_payment`, `call_ellder` (Twilio), `search_memory` (pgvector over chat history) → family Telegram group as the **approval surface** (people approve where they already talk) → TV PWA as the ambient display.
- **Why it's not a chatbox wrapper:** the agent's power is *cross-surface memory* (TV + group + calendar + smart home + phone calls) and *schedule-driven proactivity*. The chat is the approval channel, not the brain's location; the home is the brain's location.
- **Failure handling (visible in demo):** grandma silence alert → never auto-dials without confirm (control story); delivery draft fails → falls back to the manual list, nothing is lost; wrong-calendar read (timezone!) → all times stored/validated in Asia/Tashkent, shown with the source.
- **Demo (90s):** TV on stage showing the household brief; family Telegram on two phones (parents, daughter) — judge approves a grocery draft with one tap; team triggers the "grandma silent" scenario → the daughter's phone gets the message, confirm → an outbound call is placed. The room goes quiet when the daughter's phone rings from the *agent*.
- **Score map:**
  - Functionality: **4.5** — all self-contained; Home Assistant is reliable; the demo loop is short.
  - Innovation: **4.5–5** — the *household second-self with an elder-care sentinel* is an original composite; "where people live" is the theme's own wording.
  - Execution: **4.5** — multi-system orchestration (TV, HA, Telegram, Twilio, vector memory) reads as a real architecture.
  - Usefulness: **4.5–5** — the elder-check-in loop creates the most emotionally legible value on this list; judges are human.
- **Risks / build plan:** scope creep (the household idea can bloat) — **hard-limit to 4 loops: morning brief, dinner/groceries, elder check-in, memory Q&A**. UZ voice for grandma (use a cloned family voice — this doubles as a moving demo moment). 48h: D1 = HA + TV dashboard + group bot; D2 = groceries/bills loop; D3 = elder loop + memory + rehearsal.
- **Prior art & differentiation:** Alexa+/Gemini Home = *device control with chat*; ElliQ/GrandPad = *senior-only hardware* [explainx](https://www.explainx.ai/blog/ai-for-elderly-care-aging-companion-robots-2026). The **multi-person household with care-escalation in the family chat** is the unclaimed middle.

---

## IDEA 7 — "Usta": the field technician's voice colleague (hands-free work orders in the field)

> *A gas/electrical/water technician climbs a roof in Tashkent with gloves on and one ladder. They don't open an app. They talk: "WO-231, the old wire at the meter was fried, I replaced the circuit, need a 40A breaker." The agent — living on the worker's phone and the office's screen — transcribes in Uzbek, writes the structured work order, checks parts stock, confirms with the customer by SMS in UZ, and schedules the follow-up. The environment is a body in motion; the agent is the worker's hands on paperwork.*

- **Pattern:** Hands-free colleague. **Theme environment:** mobile/voice, in the physical field — where people *work*.
- **Why this place (theme logic):** Field work is the anti-chatbox: hands occupied, signal patchy, 17 minutes lost per appointment just on scheduling [salesforce](https://www.salesforce.com/news/stories/agentforce-for-field-service-announcement/). The agent's value exists *because* of the environment's constraints — voice-first, offline-tolerant, SMS fallback — and its output (structured work orders, parts movement, customer confirmations) is something a chatbox can't produce at all: it requires *being where the work happens*.
- **Evidence:** Salesforce shipped **Agentforce for Field Service** (Apr 2025): voice work orders, pre-work briefs, post-work summaries; result cited: **30% fewer "where is my technician?" calls**, scheduling from 17 min to under 5 [salesforce](https://www.salesforce.com/news/stories/agentforce-for-field-service-announcement/); field techs lose **90–120 min/day to admin rework**; AI-assisted work-order generation cuts admin effort ~38% in 6 months [oxmaint](https://oxmaint.com/industries/facility-management/ai-voice-work-orders-for-facility-technicians); voice-agent tooling for exactly this exists now (streaming STT with part-number keyterms, FSM write-back) [assemblyai](https://www.assemblyai.com/solutions/voice-agents-field-service). **Nobody has done this in Uzbek, for the UZ utility/trade market** — where the workers, the parts, and the language are all local.
- **End-to-end flow:**
  1. Dispatcher's screen: new call → agent (voice, UZ) qualifies it, schedules with the tech's real availability, preps a **pre-work brief** (asset history, parts at site, route).
  2. Tech on site, hands on ladder: "Usta, start WO-231." Agent reads the brief; tech narrates the work as they go; agent captures **voice → structured fields** (asset, fault, parts used, status) using part-SKU keyterms.
  3. "Need a 40A breaker" → agent checks the office stock (Google Sheet/SQLite), confirms "in stock, 2 left — taking the last, reorder triggered" and logs the movement.
  4. Job done: agent drafts the **post-work summary** + customer SMS ("Replaced the circuit at your meter; 40A breaker fitted; next check in 6 months") — tech says "send it," customer's phone gets it in UZ.
  5. **Photo verify:** tech snaps the finished work; agent (vision) checks the photo against the task (breaker present, wiring neat) — fails the close if it doesn't match ("I see the old wiring still exposed — another photo?").
  6. Office: day-end rollup — jobs, parts used, reorders, revenue — on the dispatcher's screen and in the owner's Telegram.
- **Architecture:** phone app (or even just a phone call to a Twilio number — **zero app needed for the tech**, a huge adoption point) → streaming STT (Whisper/Deepgram, uz) → LangGraph agent with tools: `workorder_crud`, `check_stock`, `move_stock`, `sms_customer`, `vision_check`, `schedule_followup` → dispatcher web dashboard (live: what each tech is doing, narrated) → Postgres.
- **Why it's not a chatbox wrapper:** the agent *is the work-order system* — there is no separate system to chat *about*; its I/O is the field itself (voice in, structured records + customer SMS + photos out). The environment (ladder, glove, no-signal) defines every design decision.
- **Failure handling (visible in demo):** no signal on the roof → agent queues records locally, syncs when back (demo: airplane mode 30s, then watch the sync); ambiguous part name → one confirming question, never a wrong SKU; photo check fails twice → human review flag, not a blocked close.
- **Demo (90s):** dispatcher screen live; judge calls the tech's number (or the tech's phone is in the judge's hand): full narration of a job in UZ → structured work order appears on the dispatcher screen live → stock deduction → customer SMS lands on a phone → photo verify catches a deliberately bad photo → day rollup.
- **Score map:**
  - Functionality: **4.5–5** — fully self-contained; the "no app, just a phone call" design removes the hardest integration.
  - Innovation: **4–4.5** — the pattern is validated (Salesforce) but the *localization + phone-call-only + photo-verify* combination is original for this market; frame as "the first UZ field agent."
  - Execution: **4.5** — streaming pipeline + offline queue + vision verify is a strong, honest architecture.
  - Usefulness: **4.5** — 90–120 min/day per tech is a number any owner understands.
- **Risks / build plan:** UZ STT on noisy field audio (demo is controlled; ship keyterm lists — that's a real engineering feature, not a crutch). 48h: D1 = voice loop + work-order tools; D2 = stock + SMS + dispatcher screen; D3 = offline queue + photo verify + rehearsal.
- **Prior art & differentiation:** Salesforce Agentforce FS is enterprise SaaS in English for big HVAC/utilities [salesforce](https://www.salesforce.com/news/stories/agentforce-for-field-service-announcement/). The submission is the **SMB, UZ-language, call-based, photo-verified** version — the actual market in Central Asia.

---

## IDEA 8 — "Kiosk Operator": the agent that drives the machine (a computer-use agent inside a self-service kiosk/ATM)

> *A customer stands at a self-service kiosk — bank, utility, clinic, government. They don't know the buttons; they're elderly, or a foreign tourist, or just in a hurry. They say: "I need 1 million som in cash, and pay my electricity." The agent doesn't *explain* the buttons — **it presses them.** A computer-use agent lives inside the kiosk's own UI, operating the machine as the customer's hands, recovering from errors, translating, and never letting a transaction die at step 4. The kiosk is the place nobody expects an agent — and the agent-as-operator pattern cannot exist in a chatbox.*

- **Pattern:** Operator (the strongest instance — the agent drives the *physical machine's* UI). **Theme environment:** the self-service kiosk (ATM/utility/clinic check-in) — "somewhere nobody expects one yet."
- **Why this place (theme logic):** Kiosks are *deterministic UIs with no staff around* — the worst possible interface for anyone off the happy path, and the best possible environment for an agent: closed action space, full screen visibility, high stakes (money), zero ambient distraction. The environment's constraints create the pattern: **an agent whose job is to operate the machine, not converse about it.** Every "AI kiosk" today adds a chat box *next to* the buttons [kioskindustry](https://kioskindustry.org/category/ai-kiosk/); this one *becomes the hand on the screen*.
- **Evidence:** the kiosk industry itself flags the shift: conversational agents for kiosk software are shipping in 2026 (Zamok Chat Agent) — proof the direction is right, and proof that **chat-on-the-kiosk** is the current state of the art [kioskindustry](https://kioskindustry.org/payments-public-sector-advanced-kiosks/); voice-led kiosk experiences are already a retail novelty (Skechers' voice "Luna" kiosk, Singapore) [kioskindustry](https://kioskindustry.org/category/ai-kiosk/); **regulatory deadlines make accessible self-service an obligation**: EU Accessibility Act (kiosks, since June 2025) and ADA-style alternatives require *accessible operation* [kioskindustry](https://kioskindustry.org/regulatory-deadline-update/) — a voice-operated agent is the cleanest compliance story; computer-use agents are production-grade now (Operator ~87% on browser tasks [xelionlabs](https://xelionlabs.com/blog/ai-browser-agents-guide)).
- **End-to-end flow:**
  1. Customer approaches: agent greets (screen + speaker), asks language (UZ/RU/EN — the tourist case).
  2. Customer states intent in one sentence: "cash out 1,000,000 som and pay electricity for apartment 12."
  3. Agent **plans the transaction graph**: [login → withdraw → amount → confirm] + [services → utilities → electricity → account → pay → receipt].
  4. Agent **executes by actually operating the kiosk UI** (it has programmatic access to the kiosk's element tree + a computer-use fallback for anything unstructured): each press is **mirrored on screen with a one-line narration** ("logging you in — card ready?") → the customer watches the machine being driven for them.
  5. **Error recovery (the demo hero):** a card read fails / balance insufficient / service code typo → agent detects the machine's error state, explains in plain language, retries the right way (different denomination split, correct service code from the account), or escalates: "should I call a staff member?" (with one-tap call).
  6. Finish: receipt printed + Telegram copy; agent asks one feedback line; session log archived (audit trail — regulators love this).
- **Architecture:** kiosk = a faithful web kiosk app (banking/utility UI, built by us, with an **element tree API** — 1 day of work) → agent layer: LLM planner (LangGraph) + a `KioskDriver` that maps actions to the kiosk's element tree (computer-use loop: screenshot + tree → action → verify) → intent parser (voice or tap-to-talk) → TTS narration → audit log (every action + state hash) → staff escalation (push notification). The *same agent code* works on the kiosk UI it didn't build, via the screenshot/tree fallback — that's the generalization claim.
- **Why it's not a chatbox wrapper:** the chatbox version of this idea is a help-desk bot that *tells* you which button to press — and fails the moment the customer can't read or the UI changes. The value **is** the operation: intent → verified UI actions → money moved. That pattern is definitional to computer-use agents and has no chatbox equivalent.
- **Failure handling (visible in demo):** (a) card fail → retry → staff-escalation offer; (b) customer barks a new mid-transaction ("actually 2 million") → agent re-plans *from current machine state*, not from zero; (c) kiosk "freezes" (team injects a lock) → agent detects no state change after action, reports "the machine is stuck — calling staff," and the staff alert fires. This triple is the whole technical pitch.
- **Demo (90s):** judge steps up to a real kiosk-sized screen with mic, speaks UZ: cash + utility payment. Agent drives the machine, narrating; a deliberate card error hits; agent recovers; mid-flow the judge changes the amount; receipt prints; a second judge (in "tourist mode", English) repeats the flow. Team shows the audit log.
- **Score map:**
  - Functionality: **4.5–5** — the environment is 100% ours; the only external pieces are mic/TTS; extremely rehearse-able; error injection is *reliable by design*.
  - Innovation: **5** — this is the list's cleanest "surprising new agent pattern" claim: *the agent as the machine's operator*. Chat-on-kiosk is 2026 state of the art; operating-the-kiosk is the next thing. The central value (money moved by voice in a no-staff room) cannot exist in a chatbox, full stop.
  - Execution: **4.5** — element-tree + computer-use fallback + audit trail + re-planning-from-state is a genuinely well-engineered loop.
  - Usefulness: **4.5** — elderly + tourists + accessibility (EAA/ADA) makes the value legible to any judge; the compliance angle adds a "why now."
- **Risks / build plan:** make the kiosk app *look* like a real kiosk (the stage presence matters — a TV on a stand with a card reader prop); money is simulated (be transparent: "payment rails simulated, agent logic real"). 48h: D1 = kiosk app + element tree + driver loop; D2 = voice intent + narration + re-planning; D3 = error injection suite + audit + rehearsal.
- **Prior art & differentiation:** Zamok Chat Agent = chat on kiosk [kioskindustry](https://kioskindustry.org/payments-public-sector-advanced-kiosks/); Luna = voice *recommender* in a mall [kioskindustry](https://kioskindustry.org/category/ai-kiosk/); Operator/Mariner = generic web agents [xelionlabs](https://xelionlabs.com/blog/ai-browser-agents-guide). **An agent that owns a self-service machine's operation, with re-planning and audit, for a local market** = unclaimed.

---

## IDEA 9 — "Oshxona": the kitchen agent (sentinel on the KDS, from fire to door)

> *A restaurant's kitchen display is where the service actually happens — and it's a dumb board of tickets. Put an agent on it: it watches order flow in real time, predicts a ticket going late *before* the time is up, re-sequences by cook time, tells the floor before the customer complains, converts last-minute prep into specials to cut waste, and closes the day with a food-cost report. The kitchen is where people work; the agent is the head cook's second brain.*

- **Pattern:** Ambient sentinel. **Theme environment:** the kitchen display system (KDS) + the restaurant's operations — where the work physically happens.
- **Why this place (theme logic):** A restaurant's margin dies in three seconds: the fire is hit too late, the plate sits too long, the 8pm rush was never prepped. Those seconds are visible *only* on the KDS. An agent there has the one context no chatbox or dashboard-after-the-fact can: **live, per-ticket, per-station state while the kitchen is still hot**. Proactive (before the customer notices) is the entire game.
- **Evidence:** AI food-waste tracking is a proven, deployed category — Winnow runs **3,500+ sites in 94 countries**, cuts food cost **~2–8%**, trained on 500M+ images [winnow](https://www.winnowsolutions.com/); AI kitchen display systems are now an explicit product category (prep-time prediction, order sequencing, POS/delivery integration) [techryde](https://www.techryde.com/ai-kitchen-display-system/); restaurant POS is going agentic at the platform level (Salesforce Agentforce for Retail's order-management skills [pymnts](https://www.pymnts.com/news/artificial-intelligence/2025/salesforce-launch-ai-agents-cloud-based-pos-retailers/)). **The gap: the agent that spans fire → timing → floor → waste → cost in one loop, for a single small venue, in the local language** — no one serves the 12-staff Tashkent cafe, only the 400-site hotel chain.
- **End-to-end flow:**
  1. Orders arrive (POS + delivery-app feed; demo: a mock order stream with realistic inter-arrival patterns + a Friday rush burst).
  2. Agent **sequences the fire** by station load and cook time (grill vs sauté vs expo), re-sequencing live as tickets come in.
  3. **Late-prediction:** each ticket gets an ETA from its items' historical cook times; when ETA > promised time, the agent acts *now*: flags the ticket red on the KDS, tells the floor server ("table 6 will be 4 min late — offer bread basket, code LATE-6"), and — if the order was delivery — pings the delivery app's status so the *customer* hears it before they'd have complained.
  4. **Waste → special:** 18:30, agent sees 3.2kg of prep going unsold → drafts a "chef's special" (price, name in UZ/EN) → manager approves in Telegram → it appears on the QR menu and the KDS prep list.
  5. **Rush pre-plan:** 4 days of ticket data → agent forecasts Friday 19:00–21:00 volume by item, sends the prep list to the head cook Thursday ("prep 9kg lamb skewers, 2× usual").
  6. **Day close:** food-cost report (sold vs wasted vs prepped) → owner's Telegram, with one actionable line ("salad over-prepped 40% vs forecast — cut by half").
- **Architecture:** mock POS/order stream (event bus) → KDS web UI (the "screen in the kitchen") → LangGraph agent with tools: `sequence_tickets`, `eta_predict`, `notify_floor`, `ping_delivery`, `draft_special`, `forecast`, `cost_report` → Telegram (approvals) → Postgres for cook-time history (seeded with 2 weeks of synthetic data so predictions are real from minute one).
- **Why it's not a chatbox wrapper:** the agent's input is *live ticket state at second granularity*; its outputs are *actions on the kitchen* (re-sequence, floor message, delivery ping, menu change). None of it is request-response; all of it is ambient.
- **Failure handling (visible in demo):** ETA model unsure (new dish) → conservative default + flags itself "low confidence"; floor ignores the late alert → second escalation to the manager after 60s (never to the customer twice); delivery ping fails → falls back to a manual note for the runner.
- **Demo (90s):** KDS screen live; order stream runs; a spike hits at :45 → judges watch tickets re-sequence, a red ticket appear, the floor's phone get the "offer bread basket" ping, the delivery app show the proactive delay; then the 18:30 special lands on the QR menu; day-close report reads itself in the owner's Telegram.
- **Score map:**
  - Functionality: **4.5** — fully self-contained; the synthetic history makes predictions work from the first minute.
  - Innovation: **4** — KDS-AI exists [techryde](https://www.techryde.com/ai-kitchen-display-system/) and waste-AI exists [winnow](https://www.winnowsolutions.com/); the **unified fire→floor→waste→cost agent** is the original part — name it that way.
  - Execution: **4.5** — forecasting + real-time sequencing + multi-channel notifications is a solid systems story.
  - Usefulness: **4.5** — every judge has eaten at a restaurant; "the customer never finds out it was late" is the pitch in one line.
- **Risks / build plan:** keep the kitchen *small* (3 stations, 12 items — depth over breadth); if a real partner cafe is available, even one day of their real ticket data upgrades the whole story. 48h: D1 = order stream + KDS + sequencing; D2 = ETA + floor/delivery pings; D3 = special + forecast + cost report + rehearsal.
- **Prior art & differentiation:** Winnow/Leanpath = waste-only, hardware bin [winnow](https://www.winnowsolutions.com/) [pmc](https://pmc.ncbi.nlm.nih.gov/articles/PMC11799730/); KDSync = sequencing only [techryde](https://www.techryde.com/ai-kitchen-display-system/). **One agent, full loop, single venue, local language** = the unclaimed slot.

---

## IDEA 10 — "Qo'l" (Wrist): the agent that lives on the watch — and knows what your body is doing

> *A health agent on the smartwatch that doesn't wait to be asked. It has the one data source no chatbox on Earth can access: your live physiology. It paces a run against your heart-rate zones, notices the breathing pattern that means trouble, escalates to the family/doctor *before* the person is asking for help, and talks — on the wrist, out loud, hands-free. The theme says wearables; this is the only environment where "context" means your own organs.*

- **Pattern:** Ambient sentinel (biological). **Theme environment:** wearable — the wrist.
- **Why this place (theme logic):** A chatbot is *you telling it how you feel*. The watch agent is *measuring you while you don't think about it* and acting before symptoms become words. The environment (continuous biometrics, glanceable UI, haptics + voice, always-on) is not a delivery channel for chat — it's a **different sensing modality**, and the whole value (proactivity on your own physiology) is undefined without it.
- **Evidence:** this is the platform frontier *right now*: **Google's Pixel Watch 5 (Aug 2026) launched "proactive Gemini" + "Health Guardian" — including industry-first on-wrist breathing-emergency detection that can auto-call emergency services** [google blog](https://blog.google/products-and-platforms/devices/pixel/pixel-watch-5/); Samsung's Galaxy Watch 8 runs Gemini energy scores/adaptive coaching [onedayadvisor](https://www.onedayadvisor.com/2026/05/best-ai-wearables-2026-smart-rings.html); Apple Watch Series 11 adds on-device health analysis [onedayadvisor](https://www.onedayadvisor.com/2026/05/best-ai-wearables-2026-smart-rings.html). **But the big platforms ship closed, English-first, single-purpose (safety event) features.** The open, general, *conversational* layer that *reasons over your biometrics with tools* (calendar, family, weather, doctor) is the gap — and the hackathon-sized slice is that layer, demoed on any wrist.
- **End-to-end flow (demo user: a 45-year-old running for health, with a family connected):**
  1. **Run pacer:** run starts (watch) → agent reads live HR/pace and *talks*: "zone 2, easy — you're 10 bpm over target for 20s, soften." It adjusts the target per day (sleep score, RHR trend).
  2. **Anomaly escalation:** HR pattern crosses a sustained threshold (or the simulated "breathing event") → agent: haptic + voice on wrist ("stop, sit, I'm telling your sister") → **escalation chain**: sister's phone (Telegram + call), with a 30-second "cancel" window if the user is responsive; if unresponsive for 60s → full alert with location + recent vitals. (The cancel window *is* the control story the rubric wants.)
  3. **Day-level:** RHR trending up 4 days + poor sleep → morning watch brief: "your baseline is drifting — want me to book the check-up?" → one tap → the agent (phone-side) drafts the clinic booking (reuse of idea 2's calendar tools) — **the watch agent calling on the phone: cross-environment action**.
  4. **Family surface:** sister's phone shows a weekly digest (no raw data leak — summaries only), and can ask the agent: "how's been his week?"
- **Architecture:** watch = a WebXR-free **watch-face PWA** (round viewport, glance UI) running on a phone/tablet as the demo wrist + a **live biometrics feed** (real if a team member owns an Apple/Galaxy watch with an export/API — e.g., via the Health Connect bridge; otherwise a physiologically realistic simulated HR stream with seeded "events" — be transparent which) → agent (LangGraph) with tools: `read_bios` (streaming), `pace_advice`, `escalate` (Twilio/Telegram chain with cancel window), `book_checkup`, `family_digest` → Postgres for baselines (personal reference ranges, not population ones).
- **Why it's not a chatbox wrapper:** the input stream (continuous HR/SpO₂/accelerometry) and the output modality (haptics + voice at the wrist, glance UI) have **zero chatbox equivalent**. The agent's core act — *deciding, on your behalf, that your body needs help before you can ask* — is impossible for anything that requires a user to type first.
- **Failure handling (visible in demo):** cancel-window exercised live (judge "recovers," agent stands down, logs the false-positive, tunes threshold down — *the model visibly learns*); GPS/bio feed drops → agent says so and pauses escalation (never escalates on stale data); baseline not yet established (new user) → conservative thresholds + "learning" banner.
- **Demo (90s):** judge's phone-as-wrist shows the run: pacer talks through zones; team triggers the anomaly → haptics buzz, voice speaks, sister's phone buzzes → judge exercises the 60s cancel window both ways (recovers / doesn't); then the cross-environment beat: the agent books the check-up on the clinic calendar. The room sees *biology become a calendar entry*.
- **Score map:**
  - Functionality: **4.5** — self-contained; the simulated-bio option removes the biggest external dependency (and a real watch as B-plan).
  - Innovation: **4.5–5** — the pattern ("agent with your organs as context") is definitional to the wearable theme; the *escalation-with-cancel-window* design is original, and it's the safety story that makes a 5 on usefulness.
  - Execution: **4.5** — streaming bio + adaptive baselines + multi-step escalation chain = strong engineering surface.
  - Usefulness: **4.5–5** — one saved parent/athlete is the most legible value in the entire list; the cancel window keeps it *controllable*, exactly as the rubric phrases it.
- **Risks / build plan:** medical-adjacent optics → **strictly wellness-framed, explicitly non-diagnostic, escalation is always confirmable/cancellable** (say this in the pitch); UZ context: the family-escalation loop is culturally *perfect* for Tashkent (families coordinate via phone/Telegram). 48h: D1 = bio stream + pacer; D2 = escalation chain + cancel window; D3 = baselines + booking loop + rehearsal.
- **Prior art & differentiation:** Pixel Watch 5/Galaxy 8 = closed platform features (safety event or energy score) [google](https://blog.google/products-and-platforms/devices/pixel/pixel-watch-5/) [onedayadvisor](https://www.onedayadvisor.com/2026/05/best-ai-wearables-2026-smart-rings.html); Oura = sleep analytics, no action layer. **An open, conversational, tool-using agent that acts on live biometrics with a family escalation chain** = the gap.

---

## IDEA 11 — "Ko'cha" (Street): the agent you meet through the camera — the physical world as interface

> *Point your phone at a menu on a Chorsu bazaar stall, a pharmacy shelf, or a service sign. The agent — living in your **browser tab with the camera open** — reads the physical world, explains it in Uzbek, prices it against the market, translates the vendor's reply, and **closes the deal through the vendor's Telegram bot** — all without leaving the street. The environment is "the place nobody expects an agent yet": the street itself, seen through a browser.*

- **Pattern:** Second-self (the user's), but the *input* is the physical world. **Theme environment:** the browser + camera, standing on a street corner — the physical world as the interface.
- **Why this place (theme logic):** Every other agent lives in an app, a tab, or a room. This one's interface is **whatever the lens sees**. The environment contributes what no chatbox can: *the unstructured physical artifact in front of you* (handwritten price list, no English, no app) plus *the location and the vendor's real channel* (their Telegram). The agent is the bridge between the physical commerce layer — which in Tashkent is still 80% offline — and the digital one.
- **Evidence:** multimodal vision-in-browser is production-ready (vision LLMs as a commodity capability in 2025–26; browser agents already read screens like pixels [xelionlabs](https://xelionlabs.com/blog/ai-browser-agents-guide)); conversational commerce in messaging is the highest-growth segment (WhatsApp Business API market $8.2B→$38.6B, "conversational commerce" named a primary driver [dataintelo](https://dataintelo.com/report/whatsapp-business-api-platform-market)); Tashkent's e-commerce is "very high" but its physical commerce (bazaars, stalls) has no digital layer at all — the gap is the product [101digital](https://101digital.uz/en/blog/uzbekistan-digital-marketing-report-2026/).
- **End-to-end flow:**
  1. You're at a stall; the menu is handwritten, prices in UZ, no app exists. Camera on.
  2. Agent **reads the physical menu** (vision): builds a structured offer list (item, price, unit) and overlays it in the browser — with **market price checks** (local price index: "this is ~15% above Chorsu average for plov").
  3. You say: "two portions plov, can they deliver to my office?" → agent **opens the vendor's Telegram** (every stall with a bot, or a human vendor the agent can message on your behalf with your permission) and sends the order *as you*, UZ/EN adapted.
  4. Vendor replies (in UZ, by voice note) → agent transcribes, translates to your chosen language, shows it, and drafts the reply; you approve — **the agent is your delegate, not your replacement** (the control story).
  5. Payment: vendor sends a Payme/Stars link in chat → agent surfaces it one-tap.
  6. **Memory:** next time you're at the same stall (location), the agent remembers: "last time the plov was 55k — want to ask if the price held?"
- **Architecture:** browser tab (getUserMedia → vision LLM: menu OCR + structuring) → market-price RAG (curated UZ price index, 2 days of scraping) → Telegram bridge (bot DMs the vendor bot / or messages a vendor account the user has connected, with explicit per-message user approval) → STT/TTS for voice notes → Postgres for place memory (map of bazaars: what you've bought where, at what price).
- **Why it's not a chatbox wrapper:** the *source of truth is the physical world through the lens*; the chat is only the closing channel. The value — "read the unstructured offline world, price it, and negotiate through its own channel" — cannot exist without the camera + location + the vendor's real messenger.
- **Failure handling (visible in demo):** menu half-occluded / handwritten badly → agent marks low-confidence items ("can't read this price — worth a question?") instead of guessing; vendor doesn't answer → agent drafts a polite follow-up and offers a second stall from the place-memory ("the stall 10m down had it at 45k last week"); payment link looks off-domain → hard block + warning (the safety moment judges notice).
- **Demo (90s):** a real stall menu photo (or a printed prop menu at the booth) on camera → agent overlays the structured, price-checked menu live; order goes out through a vendor bot (a teammate plays the vendor, on a real Telegram phone the judges can see); vendor voice-note reply is translated; price memory fires on "return visit." Physical world in, deal out — no app installed.
- **Score map:**
  - Functionality: **4** — vision-on-handwriting is the flaky link; mitigate with the price-checked overlay as the hero (it's the most *verifiable* output) and a prop menu as plan C.
  - Innovation: **4.5–5** — "the agent you meet through your camera on the street, closing deals through the vendor's own channel" is the list's most *surprising* environment; it's the literal "somewhere nobody expects one yet."
  - Execution: **4** — vision structuring + market RAG + Telegram bridge + place memory is a credible, well-scoped pipeline.
  - Usefulness: **4** — high delight, moderate frequency; the price-check/memory loop is the real utility (a consumer's price radar in bazaars).
- **Risks / build plan:** handwriting OCR quality (choose the prop menu font to be "realistic but legible" if demoing a prop); keep the commerce loop *short* (menu → price check → one order → voice-note translation → memory). 48h: D1 = vision menu reader + overlay; D2 = Telegram order bridge + voice-note translation; D3 = price index + place memory + rehearsal.
- **Prior art & differentiation:** menu-translation apps exist (point-and-translate, dead end); chat-order bots exist (idea 1); **camera-reads-the-street → prices-against-market → negotiates-through-the-vendor's-own-channel, with place memory** = no one does the full loop, and no one does it in a bazaar.

---

## IDEA 12 — "Buvay / Buxona" (Grandma): the elder's companion on the home screen — a family on the other end

> *An elderly parent in Tashkent lives alone; their children are busy. The agent lives on the home screen (the TV/tablet that's already on) and speaks their language and *their family's voice*. It checks in the way a person would — and when the checking-in stops, **the family is the one who finds out**, with one tap to call. It's the ambient-care sentinel, but built as a relationship, not a sensor grid.*

- **Pattern:** Ambient sentinel (care) + second-self (for the family). **Theme environment:** the home, on the screen the elder already has — "where people live," in the theme's own words.
- **Why this place (theme logic):** Elder-care tech forces a choice: wear something (seniors resist) or add a camera (privacy revolt). The *screen the elder already stares at* needs neither: the agent's sensing is **conversational** (the morning chat itself is the vitals check — a missed or slowed morning chat *is* the signal), and the family's interface is **the Telegram they already live in**. The environment's value: zero new behavior required from the elder, zero devices to charge, context = the whole day's rhythm.
- **Evidence:** ambient assisted living is a **$67.7B (2025) market heading to ~2x by 2032**; **non-wearable monitoring is the explicitly preferred direction** (privacy-conscious, "technology works with natural limitations rather than demanding adaptation") [marketgrowthreports](https://www.marketgrowthreports.com/blog/ambient-assisted-living-and-smart-home-companies-143) [grtair](https://www.grtair.com/ambient-intelligence-the-era-of-invisible-technology-in-elderly-care/); the validated product shapes are exactly this: **GrandPad** (family admins see activity summaries + get alerts on unusual non-use), **ElliQ** (proactive conversational engagement, family connectivity) [explainx](https://www.explainx.ai/blog/ai-for-elderly-care-aging-companion-robots-2026); fall-detection hardware alone is a **$1.72B→$3.58B** market because the need is proven [openpr](https://www.openpr.com/news/4617249/smart-elderly-fall-detection-rug-market-research-reveals-path). **The gap: a conversation-first, family-escalated, UZ-language version that runs on hardware already in the house** — no new device, no Western hardware.
- **End-to-end flow:**
  1. **Morning check-in (the vitals):** ~08:30 the screen wakes: "Assalomu alaykum, Xurshida opa. How did you sleep? Tea's getting cold — I'll remind the doctor about your pills at 9." The agent *listens*: response latency, coherence, mood keywords become the daily signal (it never shows scores to the elder — scores go to the family).
  2. **Day:** medication reminders (with camera-optional verify: "show me the pill box"), a phone call with the daughter at the usual time (video, one tap — the agent dials), small talk about the things the family *told the agent* ("ask about the grandson's exam").
  3. **The silence rule (the hero loop):** no morning chat by 10:30, or chat quality drops sharply → agent tries once (re-asks warmly) → still nothing → **family Telegram**: "No sign from mom since 08:30; her last chat was slower than usual. Want me to call her now?" → family taps → outbound call (with the elder's voice profile, so it *sounds like family*, not a robot).
  4. **Weekly family digest:** "Mama's week: 6/7 mornings on time, BP reported 3×, asked about you twice, wants more time with Alisher." — the family surface, on their Telegram.
  5. **Medication logistics:** refill due → agent drafts the pharmacy order (or asks the family who will drop it off).
- **Architecture:** home screen PWA (TV/tablet, big text, one-tap mic, TTS voice = cloned family voice) → agent (LangGraph) with tools: `daily_signal` (chat quality scoring, stored per-day), `escalate` (→ family Telegram → Twilio call with confirm tap), `meds`, `schedule_call`, `family_digest` → family Telegram bot (multi-member: each child gets their view) → Postgres for the longitudinal baseline (the agent learns *her* normal).
- **Why it's not a chatbox wrapper:** the sensing is the *conversation's rhythm over weeks*; the acting spans **two households** (elder's screen → family's phones → an outbound call). A chatbox with a grandma is a toy; this is a distributed care loop where the environment (the home screen, the family's messenger, the phone line) is the architecture.
- **Failure handling (visible in demo):** false "silence" (she's at the market) → the family can silence the alert with one tap ("she's out") — the agent *learns her routines* (Fridays at the market, alert starts later); TTS fails → on-screen text with giant type (the screen is always the fallback channel); the agent **never diagnoses** — it reports *change* and defers to family/doctor (the ethics line, say it in the pitch).
- **Demo (90s):** the TV on stage with a warm UZ morning chat (cloned family voice — the room will hear it); team shows the family Telegram on two phones; the "silence" scenario fires → the daughter's phone gets the message → one tap → the outbound call lands on the TV (ringing in the room); then the weekly digest: "wants more time with Alisher." This demo wins or loses on the emotional beat — rehearse the voice cloning well.
- **Score map:**
  - Functionality: **4.5** — fully self-contained; the loops are short and deterministic.
  - Innovation: **4–4.5** — GrandPad/ElliQ prove the pattern [explainx](https://www.explainx.ai/blog/ai-for-elderly-care-aging-companion-robots-2026); the originality is the *conversation-as-sensor + cross-household escalation + UZ/family-voice* local build. Name the pattern: "the chat is the vital sign."
  - Execution: **4.5** — longitudinal baselines + multi-household messaging + voice cloning is a real system, and the "never diagnoses" guardrail is thoughtful failure handling in the rubric's own words.
  - Usefulness: **4.5–5** — the highest emotional-legibility score on the list; for a Tashkent family, this is a product they'd pay for *this month*.
- **Risks / build plan:** voice cloning of a real family member (get consent on camera before the hackathon — it's also a story); UZ TTS naturalness is make-or-break (practice the clone in the days before); keep the elder's UI to *two* interactions (tap-to-talk, one-tap video). 48h: D1 = screen PWA + voice loop + daily signal; D2 = family Telegram + silence rule + outbound call; D3 = digest + memory + rehearsal.
- **Prior art & differentiation:** GrandPad/ElliQ = Western hardware, English, US pricing [explainx](https://www.explainx.ai/blog/ai-for-elderly-care-aging-companion-robots-2026); fall-rug/wearable = device-first [openpr](https://www.openpr.com/news/4617249/smart-elderly-fall-detection-rug-market-research-reveals-path) [grtair](https://www.grtair.com/ambient-intelligence-the-era-of-invisible-technology-in-elderly-care/). **Conversation-first, no-new-device, UZ-language, family-voice, family-Telegram-escalated** = unclaimed, and culturally exact for the region.

---

## 13. BONUS — "Dispatch": the browser agent on the dispatcher's screen (if you want a 13th option)

> *A small Tashkent taxi/fleet dispatcher juggles 6 drivers, 40 orders/day, and a WhatsApp line. A browser agent lives **on the dispatch tool's screen** (web dispatch board or the driver app's admin): watches the live order stream and driver positions, suggests (and with approval, executes) re-assignments, drafts the reply for every passenger WhatsApp message in 30 seconds, re-quotes on surge, and files the day's exceptions. The environment is the dispatcher's actual screen — the tab everyone already stares at all day.*
>
> - **Pattern:** Ambient sentinel (ops). **Evidence:** browser agents are operational for exactly this class of work — "sees the screen, moves the cursor" across ERPs/portals/back-ends, 62% of enterprises experimenting [xelionlabs](https://xelionlabs.com/blog/ai-browser-agents-guide); scheduling/dispatch automation is a proven agent category (Salesforce FS: schedule-gap resolution, 30% fewer WISMO calls [salesforce](https://www.salesforce.com/news/stories/agentforce-for-field-service-announcement/)).
> - **Flow:** order spike detected → agent proposes re-assignment (driver, ETA, why) → dispatcher one-taps approve → agent clicks it in the dispatch board; passenger WhatsApp "where are you??" → agent drafts the localized reply with live ETA → dispatcher taps send; end of day: exception report (no-shows, cancellations, top corridors) to the owner's Telegram.
> - **Why it's not a chatbox:** the agent's eyes are on the *live dispatch board*; its hands are on the dispatch buttons; its ears are on the WhatsApp line. Same architecture as Idea 3's sentinel, different machine.
> - **Scores:** Functionality 4.5 / Innovation 4 / Execution 4.5 / Usefulness 4.5. **Build plan:** reuse Idea 3's extension+sentinel skeleton; swap detectors for dispatch rules. Strongest *second* demo if you can pull two ideas' worth of time — otherwise use it as the "scale" slide for Idea 3.

---

## Comparison matrix (honest self-scores)

| # | Idea | Environment | Pattern | Funct. | Innov. | Exec. | Use. | Sum/20 | Demo risk |
|---|------|-------------|---------|--------|--------|-------|------|--------|-----------|
| 8 | **Kiosk Operator** | self-service kiosk/ATM | Operator | 4.5 | **5** | 4.5 | 4.5 | **18.5** | Low (own env) |
| 2 | **Raqam (IVR voice)** | real phone line | Voice takeover | 4 | 4.5 | 4 | 5 | **17.5** | Medium (voice latency) |
| 1 | **Do'kon (Telegram 2nd-self)** | Telegram ecosystem | Second-self | 4.5 | 4 | 4.5 | 4.5 | **17.5** | Low (free API) |
| 12 | **Buvay (elder care)** | home screen + family phones | Ambient sentinel | 4.5 | 4 | 4.5 | 4.5 | **17.5** | Low |
| 5 | **Navbat (waiting-room TV)** | waiting room screen | Ambient sentinel | 4.5 | 4.5 | 4 | 4.5 | **17.5** | Low |
| 10 | **Qo'l (wrist agent)** | smartwatch/wrist | Biological sentinel | 4.5 | 4.5 | 4.5 | 4.5 | **18.0** | Low (sim bio) |
| 6 | **Uy (household)** | home TV + family chat | Household second-self | 4.5 | 4.5 | 4.5 | 4.5 | **18.0** | Low |
| 4 | **Davlat (gov portal)** | gov web portal | Operator | 4 | 4.5 | 4 | 4.5 | **17.0** | **High (external portal)** |
| 3 | **Kassa (POS sentinel)** | cashier screen (browser) | Ambient sentinel | 4.5 | 4 | 4.5 | 4.5 | **17.5** | Low |
| 9 | **Oshxona (kitchen)** | KDS/kitchen display | Ambient sentinel | 4.5 | 4 | 4.5 | 4.5 | **17.5** | Low |
| 7 | **Usta (field voice)** | field worker's phone/call | Hands-free colleague | 4.5 | 4 | 4.5 | 4.5 | **17.5** | Low |
| 11 | **Ko'cha (street camera)** | browser camera on a street | Physical-world 2nd-self | 4 | 4.5 | 4 | 4 | **16.5** | Medium (OCR) |
| 13 | **Dispatch** | dispatch screen (browser) | Ops sentinel | 4.5 | 4 | 4.5 | 4.5 | **17.5** | Low |

**Reading the matrix:**
- **Innovation is where most teams die.** Ideas that are *just* "agent + messenger" or "agent + one app" cap near 4. The five patterns from §0.2 are what push it to 5.
- **The safest high-scorers** (own environment, low demo risk, 4.5+ average): **8, 5, 6, 10, 12**.
- **The highest-ceiling shot** (pattern-5, "could not be reproduced in a chatbox", full stop): **8 (Kiosk Operator)**.
- **The most locally-authentic** (the story only *you* can tell): **1, 2, 7, 12** (UZ language + local surfaces + family culture).
- **The highest-risk/highest-reward**: **4 (gov portal)** — pick it only if you can secure a live public form by day 1; otherwise its clone-fallback costs you a point.

---

## Top 3 recommendations (if you can only build one)

### 🥇 1st choice: **Idea 8 — Kiosk Operator** (score ceiling, pattern-5, demo-controlled)
- **Why it wins:** it is the only idea whose *core value is definitional to computer-use* — an agent that **operates the machine** rather than chats about it. That is the rubric's 5-word-for-5-word ("a pattern whose central value could not be reproduced in a standalone chatbox"). The environment is 100% yours, so the demo is bulletproof; the three injected failures (card error, mid-flow change, frozen kiosk) are *reliable by design*, which is how you show "thoughtful failure handling" without gambling.
- **48-hour build plan:**
  - **Day 1 (build the machine + the hands):** kiosk web app (bank/utility UI: login, cash, services, utilities pay, receipt) with an element-tree API + a card-reader prop; `KioskDriver` computer-use loop (tree-first, screenshot-fallback); audit log. *Exit: agent can complete the happy path end-to-end, narrating.*
  - **Day 2 (the brain + the voice):** intent parser (UZ/RU/EN), planner with re-planning-from-state, TTS narration mirrored on screen, staff-escalation push. *Exit: 3-sentence intent → full transaction, incl. mid-flow change.*
  - **Day 3 (the failures + the stage):** error-injection suite (card fail, insufficient funds, frozen UI), audit-log screen, booth assembly (TV on a stand = kiosk), rehearsal ×5.
- **Demo day:** as scripted in Idea 8 (judge in UZ, then judge in "tourist" English, then show the audit log). One-liner: *"The kiosk stopped being a machine you operate. It became an agent that operates for you."*

### 🥈 2nd choice: **Idea 2 — Raqam (the phone number is the office)** (best real-world "environment integration" proof)
- **Why it wins:** a judge *dialing a real number from their own phone, in the middle of the pitch* is the single most undeniable "agent inside a place people already use" moment in this list. The IVR-is-dead framing is a fresh narrative, and the UZ/RU voice makes it feel made for the region.
- **Accept the trade-off:** streaming-voice latency is your #1 risk — rehearse the happy path to death, and let the *callback-scheduling* fallback be the visible failure (it's a feature, not a bug, and it's phone-native).
- **48-hour build plan:** D1 Twilio↔Deepgram↔LLM loop (real number); D2 calendar + SMS + warm transfer with staff transcript screen; D3 outbound confirmation call + UZ greeting/cloned voice + failure rehearsal.

### 🥉 3rd choice: **Idea 12 — Buvay (the elder's home screen)** (highest emotional legibility, lowest risk)
- **Why it wins:** the "the chat is the vital sign" pattern is original *as framed*, the loops are short and deterministic (near-zero demo risk), the family-Telegram escalation is culturally exact for Tashkent, and the clone-a-family-member voice is a demo moment no slide can match. Usefulness judges will score this a 5 on instinct.
- **48-hour build plan:** D1 screen PWA + voice loop + daily-signal scoring; D2 family Telegram + silence rule + Twilio outbound; D3 weekly digest + consent/ethics slide (never-diagnoses) + rehearsal.

### If your team is 2 engineers and you want maximum *technical* impression:
**Idea 3 (Kassa)** or **Idea 13 (Dispatch)** — the browser-extension sentinel is the most "engineered-looking" architecture for the least external risk, and it ports to a dozen verticals (the scaling slide writes itself).

---

## Technical playbook (applies to all ideas)

**Reference stack (proven, hackathon-speed):**
- **Agent loop:** LangGraph (or CrewAI) — explicit state, checkpoints, human-approval nodes. Use **checkpoints** so any demo failure can be recovered mid-run, and **human-approval tool nodes** for every irreversible action (that's your rubric's "clear and controllable").
- **LLM:** a strong general model (GPT-4.1/Claude/Gemini class) for planning + a small model for latency-critical paths (kiosk driver, register sentinel).
- **Voice:** Deepgram (streaming STT, multilingual) / Whisper `uz` for Uzbek; ElevenLabs for TTS (voice-cloned family voice for Idea 12; RU-voice-with-UZ-greetings hybrid for Ideas 2/7/12 — **code-switching is a feature and a robustness hedge**, say so in the pitch).
- **Telephony/SMS:** Twilio (trial numbers work for demos).
- **Messaging:** Telegram Bot API — free, no approval, Mini Apps + Stars + groups (see §0.4).
- **Computer-use:** Playwright (own-UI, deterministic) + accessibility-tree reading + screenshot-fallback for the "it also works on UIs we didn't build" claim.
- **Memory/state:** Postgres + pgvector (chat history, place memory, baselines). Google Sheets is a legitimate, *judge-legible* "system of record" for hackathon scale (inventory, prices, stock) — and it shows the agent working against a real external artifact.
- **Deployment:** one VPS/container; **everything the demo touches must be behind one `make demo`** that seeds state, starts services, and opens the right tabs. Demo-day infra failures are the most common self-inflicted wound.

**Failure-handling patterns to build into *every* idea (the rubric names this twice):**
1. **One designed failure per demo** — scripted, reliable, shown on purpose (card error; payment webhook down; grandma silent; frozen kiosk; no signal).
2. **Degrade, never block:** alerts that can be muted after repeated overrides; text fallback when TTS fails; local queue + sync when offline; callback-scheduling when voice fails.
3. **Human-approval gates on irreversible actions** (submit form, send money, dial a number) — and *show the gate in the demo*; that's the "controllable" score.
4. **Transparency layer:** every agent action logged + visible to a human (audit log / staff transcript / owner digest). Judges smell trust architecture.

**Pitch structure that maps to the rubric (5 min):**
1. **The place** (30s): "This is where people in Tashkent already [work/talk/live] — and today it's a [dumb board / dead menu / silent screen]."
2. **The pattern** (45s): name it — operator / second-self / ambient sentinel / hands-free colleague. "This pattern cannot exist in a chatbox, because…"
3. **The demo** (2.5 min): no slides during the demo. Let the environment do the talking.
4. **The evidence** (45s): 2–3 numbers from this document (market + gap).
5. **Control & failure** (45s): the designed failure + the human gate.
6. **Scale** (15s): "same architecture, different machine" — one slide.

**Do / don't for the local edge:**
- DO: build the UZ/RU/EN trilingual layer *as a feature* (locale switch mid-conversation, live in demo); name real Tashkent places (Chorsu, Yunusobod, the real queue times); get one real local user (a vendor, a clinic, a grandma) to appear on a video in the pitch.
- DON'T: pretend UZ TTS is flawless — demonstrate the fallback (that's the engineering point); don't pick the gov portal without day-1 live access.

---

## Source index (all accessed 2026-09-12)

**Messaging / local:**
- Kursiv — digital habits, UZ Telegram 88%: https://kz.kursiv.media/en/2025-04-10/engk-yeri-digital-habits-why-kazakhstan-loves-whatsapp-and-uzbekistan-prefers-telegram/
- 101digital — UZ digital marketing report 2026 (Tashkent 97%, Telegram 25M): https://101digital.uz/en/blog/uzbekistan-digital-marketing-report-2026/
- DataReportal — Digital in Uzbekistan: https://datareportal.com/reports/digital-2025-uzbekistan
- JASSS (inlibrary.uz) — UZ messaging ecosystem 2025: https://inlibrary.uz/index.php/jasss/article/download/133683/135320/195785
- WhatsApp Business API market ($8.2B→$38.6B): https://dataintelo.com/report/whatsapp-business-api-platform-market
- WhatsApp Business stats (175M msgs/day, 80% SMB use): https://electroiq.com/stats/whatsapp-business-statistics/
- Telegram Bot API free / 1B MAU / Mini Apps: https://chatbotscape.com/channels/telegram-chatbot-guide · https://blocksentient.com/review/telegram-bots/
- Telegram Bot API changelog (Stars, checklists, business mode): https://t.me/s/BotNews?before=110
- Telegram Mini Apps: https://core.telegram.org/bots/webapps

**Voice / telephony:**
- Gartner 1-in-10 by 2026, $80B: https://nlpearl.ai/the-end-of-call-centers-as-we-know-them-how-ai-voice-agents-will-reshape-2025-2028
- Deepgram State of Voice AI 2025 (80% use, 21% satisfied): https://deepgram.com/learn/state-of-voice-ai-2025
- AI IVR adoption 78%→85%: https://www.reddit.com/r/realestateainews/comments/1sxu3hg/ai_ivr_in_2026_top_companies_market_trends_and/
- Voice AI market $2.4B→$47.5B; 60.7% prefer voice booking: https://leadsnow.ai/ai-voice-agent-adoption-statistics-2026/
- Voice AI stats (queue −50%, CSAT +30%): https://www.mavenagi.com/blog/voice-ai-statistics-customer-service

**Browser / computer-use:**
- Operator 87% / Mariner 83.5% / 62% experimenting / $76.8B by 2034: https://xelionlabs.com/blog/ai-browser-agents-guide
- SME 75–85% back-office savings; gov portals = top use case: https://actgsys.com/en/blog/ai-browser-agent-operator-business-2026
- Enterprise browser agents 2026 guide (OSWorld 44% vs 14%): https://o-mega.ai/articles/ai-browser-agents-in-the-enterprise-the-ultimate-2026-guide
- Agentic browsers comparison: https://brightdata.com/blog/ai/best-agent-browsers

**POS / retail / field / kitchen:**
- Salesforce Agentforce for Retail + cloud POS: https://www.pymnts.com/news/artificial-intelligence/2025/salesforce-launch-ai-agents-cloud-based-pos-retailers/
- Microsoft agentic Dynamics 365 POS: https://www.microsoft.com/en-us/dynamics-365/blog/it-professional/2025/06/03/under-the-hood-building-an-ai-driven-storefront-with-dynamics-365-commerce-pos/
- Knowlix AI POS: https://knowlix.ai/ai-point-of-sale-software · SmartPOS AI: https://smartposai.com/
- Salesforce Agentforce for Field Service: https://www.salesforce.com/news/stories/agentforce-for-field-service-announcement/
- Field voice work orders (90–120 min/day admin): https://oxmaint.com/industries/facility-management/ai-voice-work-orders-for-facility-technicians · https://www.assemblyai.com/solutions/voice-agents-field-service
- Winnow (3,500 sites, 2–8% food cost): https://www.winnowsolutions.com/ · AI KDS: https://www.techryde.com/ai-kitchen-display-system/ · https://pmc.ncbi.nlm.nih.gov/articles/PMC11799730/

**Wearables / home / elder care:**
- Pixel Watch 5 (proactive Gemini, Health Guardian, breathing-emergency): https://blog.google/products-and-platforms/devices/pixel/pixel-watch-5/
- AI wearables 2026 (Galaxy Watch 8 Gemini, Apple S11): https://www.onedayadvisor.com/2026/05/best-ai-wearables-2026-smart-rings.html
- In-vehicle AI market $4.26B→$19.84B: https://www.fortunebusinessinsights.com/in-vehicle-ai-assistants-market-116192 · Mercedes×Google Automotive AI Agent: https://group.mercedes-benz.com/technology/innovation/collaboration/ai-powered-conversational-search.html
- AAL market $67.7B: https://www.marketgrowthreports.com/blog/ambient-assisted-living-and-smart-home-companies-143 · CAGR 30.8%: https://www.grandviewresearch.com/industry-analysis/ambient-assisted-living-smart-home-market-report
- Ambient intelligence in elder care: https://www.grtair.com/ambient-intelligence-the-era-of-invisible-technology-in-elderly-care/
- GrandPad/ElliQ/Alexa framing: https://www.explainx.ai/blog/ai-for-elderly-care-aging-companion-robots-2026
- Fall-detection market $1.72B→$3.58B: https://www.openpr.com/news/4617249/smart-elderly-fall-detection-rug-market-research-reveals-path
- Ambient intelligence (AmI) systematic review: https://www.mdpi.com/2073-8994/18/5/718
- 2026 appliance/ambient trends: https://lifetips.alibaba.com/tech-efficiency/smart-appliance-trends-that-will-make-your-home-functional-in-2026

**Government / kiosks / local delivery:**
- Citizen services AI $67.37B by 2030, cost per interaction: https://www.mindstudio.ai/blog/government · BCG: https://www.bcg.com/publications/2025/benefits-of-ai-in-government
- Gov AI vendors (Supervity, Aigentiq): https://www.supervity.ai/ai-agents-for-government · https://www.aigentiq.com/industries/public-sector
- Kiosk industry (Zamok Chat Agent 2026, EAA/ADA deadlines, Luna): https://kioskindustry.org/payments-public-sector-advanced-kiosks/ · https://kioskindustry.org/category/ai-kiosk/ · https://kioskindustry.org/regulatory-deadline-update/
- EMEA food delivery (Yandex Go et al.): https://www.singular.net/blog/food-delivery-apps/

---

*Document prepared for a Tashkent-based hackathon team, 2026-09-12. All market figures are as reported by the cited sources; treat vendor-published stats (Winnow, Salesforce, vendor blogs) as directional, and re-verify any number you put on a slide before demo day.*
