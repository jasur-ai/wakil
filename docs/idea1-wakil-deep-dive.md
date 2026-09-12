# IDEA 1 — DEEP DIVE: "wakil" (Вakil / وكيل — "your representative")
### Your personal Telegram delegate: it negotiates, resolves, and searches — under a signed mandate, with local-only memory, inside *your own account*

> *You come home tired from work. Your Uzum order arrived with a flaw. You don't want to fight with support — you open wakil (your Telegram bot) and give it the key points: "Shoes, heel defect, photo attached. I want exchange OR at least 450k som back. If they stall more than 48h, walk. Never accept damaged replacements." wakil opens the chat with the official Uzum support bot as **you**, negotiates within your exact bounds, presses the bot's own buttons, escalates to a human manager when the script says no, pings your Mini App the moment an offer falls outside your parameters — and only after you tap "hold firm" or "accept" does it continue. When it's done, you rate it 👍/👎. wakil files that rating into **your local memory** and next time it already negotiates the way you do. Everything stays on your device. And if you just want to find something — "who in my channels is selling an iPhone 15 this week?" — you give a keyword and it searches your own channels and groups for you.*

---

## 1. What changed from the original Idea 1 — and why this version is stronger

The original "Do'kon" was a **vendor-side** bot (the shop's agent). Your re-scope is a **consumer-side personal delegate** that operates *your own Telegram account*. That is a different product, and honestly, the better one for this hackathon:

| Dimension | Original (vendor shopbot) | Re-scoped (personal delegate) |
|---|---|---|
| Environment | One vendor's bot + group | **The user's entire account**: all DMs, groups, channels, official bots, search |
| Agent pattern | Assistant (answers + executes) | **Mandated delegate** (acts *as you*, under hard bounds, with learning) |
| Control story | Owner approves orders | **Mandate card** (min price, max conditions, walk-away) + per-action approval + one-tap takeover |
| Memory | Order history | **Preference memory**: learns *your* negotiation style from 👍/👎, local-only |
| Privacy story | Vendor data | **"Your data never leaves this device"** — a first-class pitch element |
| Theme fit | messaging = chatbox (judge may cap innovation at 4) | The value lives in **account-level action** (pressing other bots' buttons, searching your channels, multi-turn cross-chat deals) — a pattern a chatbox *cannot* host |
| Demo wow | Order → pay → delivery | A judge **watches the agent refuse an out-of-bounds offer and cite their own parameters out loud** |

**Strategic note:** the engine you build (user-session layer + mandate/boundary engine + local learning) is direction-agnostic. After the hackathon it flips: the same engine pointed at a *vendor's* account becomes the original Do'kon. One engine, two products. Invest accordingly.

---

## 2. Deep evaluation (honest, before the specs)

### 2.1 What makes this idea strong

1. **The counterparties you negotiate with literally live in Telegram bots in Tashkent.** This is the killer environmental fact, and it's verified:
   - **Uzum Bank** official support bot: `@UzumBank_Robot` (~78k monthly users) [t.me](https://t.me/UzumBank_Robot)
   - **Uzum Tezkor** support: `@tezkorhelp_bot`; **Uzum Market** business support: `@umarket_business_bot` [t.me](https://t.me/tezkorhelp_bot)
   - **Beeline UZ**: `@BeelineUz_HelpBot` (support), `@BeelineTakliflari_bot` (offers) [telegram.me](https://telegram.me/BeelineUzbekistan)
   - **Ucell**: `@Ucell_bot` ("My Ucell" — you can even *order a callback from a human support specialist* through it) [t.me](https://t.me/ucell)
   - **Yandex Go** (UZ partner support): `@Yapartnersupport`; **Yandex Market Go** launched in UZ in spring 2025 [yapartner.uz](https://yapartner.uz/) [sellerlab.uz](https://www.sellerlab.uz/en/yandexmarket-uzbekistan/)
   - **Government**: even the Ministry of Foreign Affairs runs citizen support through a Telegram bot (`@tiv_yordam_bot`) [uzdaily.uz](https://www.uzdaily.uz/en/uzbekistans-foreign-ministry-launches-telegram-bot-to-support-citizens-in-the-middle-east/)
   
   → In Tashkent, "customer service" is already a bot conversation. An agent that *joins that conversation as you* meets the work where it is — no app, no call center, no queue. That single fact is your "why this place" answer, and no Western team can replicate it by pointing at Slack or Gmail.

2. **The mandate pattern is the rubric's "clear and controllable" made architectural.** The user must supply complete, valid parameters (min price, acceptable outcomes, deadline, walk-away) *before* the agent acts. The agent is *structurally unable* to exceed them (BoundaryGuard, §5.4). That is not a prompt instruction — it's a code-level policy layer with unit tests. Judges scoring criterion 4 ("remaining clear and controllable") will see the design, not the promise.

3. **The feedback loop is genuine agentic memory, and it's demoable.** 👍/👎 + correction tags → typed preference updates → next mandate is *seeded from your own past decisions*, with the mini app showing **which past case** seeded each default ("starting with 48h persistence — from your Uzum case on 09.09"). Learnable, explainable, editable by the user. That's a full agentic story in 90 seconds.

4. **Local-only data is a differentiator, not a limitation.** "Your preferences, your negotiation history, your channel search index — on this device. One tap to wipe." For an agent with *full account access*, the privacy architecture is what makes the product believe-safe. We even **enforce 2FA during onboarding** — the agent makes your account *more* secure than it was before meeting it. (Technically verified: Telethon `client.edit_2fa()` enables/sets two-step programmatically [Telethon docs](https://arabic-telethon.readthedocs.io/en/stable/extra/basic/creating-a-client.html).)

5. **The channel/group search is a standalone killer utility** for a population that lives in Telegram channels (25M UZ users; 88% adoption). "Find me everything about X in my channels" + "watch for keyword Y, ping me" — real value even for users who never negotiate anything.

### 2.2 What is genuinely hard / risky (and the mitigation)

| Risk | Severity | Mitigation |
|---|---|---|
| **ToS gray zone** — acting via a user session (MTProto) is not the official Bot API. Personal-use userbots are widely operated with low ban risk (StackOverflow consensus: risk ≈ any third-party client; bans target *spam/bulk* behavior, not personal automation [SO](https://stackoverflow.com/questions/74479638/are-user-bots-made-with-telethon-allowed-on-telegram)). Ban risk rises with: fresh accounts, VOIP numbers, mass messaging. | Medium | (a) Personal use only, human-approved, per-counterparty allowlist; (b) rates ~100× under flood limits (we send a handful of messages per negotiation; limits are ~1 msg/s per chat [grammy](https://grammy.dev/advanced/flood)); (c) **disclosure in every first message** ("I'm acting on behalf of [name]"); (d) ship a "conservative mode" default; (e) in the pitch: name it honestly — "personal automation of your own account, the same category as any third-party Telegram client, at a fraction of rate limits." Honesty + numbers > pretending it's API-official. |
| **Live-login on stage** (phone code + 2FA in front of judges) | Medium | Pre-seed the session; the judge's act = typing the 2FA password once — which *is* the security demo. Fallback: pre-authenticated session, show the onboarding flow as a 20s recording. |
| **Negotiating with real official bots is scripted** — a real support bot won't "negotiate"; it follows menus | Medium (demo) | Demo split: **negotiation vs a scripted "Uzum support" bot run by a teammate** (designed to push back: policy-denial → below-minimum offer → supervisor escalation) + **real-bot navigation in read-only mode** (agent operates `@UzumBank_Robot`'s real menu flow, e.g. card-status check) to prove real-environment integration. State the split in the pitch — judges reward honesty. |
| **Pressing other bots' inline buttons from a user session** | Low | MTProto includes `messages.resendBotCallbackQuery` for exactly this (user side answers the callback). Run a **30-minute day-1 spike**; fallback if anything is off: the agent sends the equivalent text command most bots accept, or the user taps the single final confirm button themselves (which is *also* a control story). |
| **Search scale** — "find X in all my channels" across huge histories | Low-Medium | Scope it: user-selected dialogs + date window (default 90 days) + `messages.searchGlobal` for the rest [core.telegram.org](https://core.telegram.org/method/messages.search). Honest limits stated: channels you haven't joined are searchable by name/description only (`contacts.search`), not content. Watchers poll at 2–5 min cadence — well inside limits (GetHistory flood is ~30s/10 requests [Telethon docs](https://docs.telethon.dev/en/stable/modules/client.html)). |
| **Build complexity** — three subsystems (user session, bot+mini app, LLM engine) | High (this is the #1 risk) | The day-plan in §9 cuts scope hard: security story done by EOD D1, negotiation core D2, search+learning D3. Everything demo-critical is self-contained; nothing depends on a third party's API behavior at demo time. |
| **Impersonation optics** — the agent talks as you to humans | Low | Mandatory disclosure line in every first message; "takeover" is zero-friction (it's your account — the agent just stops, you keep typing in the same chat); tone guardrails (no aggression, no threats — escalation is factual only). |

### 2.3 Verdict

This is a **top-2 contending idea** for the team. It scores higher on Innovation and Usefulness than the original vendor bot, at the cost of higher execution complexity. The three things that decide whether it lands at 4 or 5:
1. The **boundary-guard demo beat** (agent refusing an out-of-bounds offer and citing the user's own parameters) — this must be flawless.
2. The **honest ToS framing** with the rate-limit numbers — turns the biggest risk into a credibility point.
3. The **learning loop visible in 30 seconds** — a pre-filled second mandate that says "from your last case" on screen.

---

## 3. The pattern (name it in the pitch)

> **"Mandated delegation inside the messenger."**
> Every chatbot is a *conversation*. wakil is a *delegation*: the user signs a mandate card (goal + hard bounds + evidence + walk-away), and the agent acts **as the user** across the account — official bots, human managers, personal chats — every outgoing message passing a policy guard, every irreversible action requiring a tap, every outcome feeding a local preference memory. The environment (your whole account, not one chat window) is what makes the pattern possible: a chatbox cannot press the counterparty's buttons, search your channels, or keep what it learns on your device.

The four rubric hooks in one line each:
- **Core functionality:** end-to-end on a *real* account: login → 2FA → mandate → live multi-turn negotiation → payment-status outcome → rating.
- **Innovation:** account-level delegated agency with hard-bound policy enforcement + local learning — a new pattern, not a new use case.
- **Execution:** dual-identity architecture (official Bot API face + MTProto hands), policy guard with unit tests, local-first data, 2FA enforced by the agent itself.
- **Usefulness:** refund/dispute pain is universal in a bazaar-and-marketplace economy; "find it in my channels" is a daily utility; the agent gets *better for you specifically* over time.

---

## 4. Research-verified technical foundations (what the platform actually allows)

Everything below was verified against current Telegram/Telethon documentation during research (2026-09-12):

| Capability | Verdict | Source |
|---|---|---|
| **User-session automation (the "hands")** | ✅ Telethon/Pyrogram act as your account: read any dialog, send messages, join group flows, receive pushes. Personal use is the accepted category; spam is the ban trigger. | [SO 74479638](https://stackoverflow.com/questions/74479638/are-user-bots-made-with-telethon-allowed-on-telegram) [Telethon docs](https://docs.telethon.dev/en/stable/modules/client.html) |
| **Login: phone → code → 2FA** | ✅ `send_code_request` → code (arrives in the user's own Telegram or SMS) → `sign_in`; if 2FA is on, `SessionPasswordNeededError` → enter 2FA password once. | [Telethon docs](https://arabic-telethon.readthedocs.io/en/stable/extra/basic/creating-a-client.html) |
| **Enabling 2FA programmatically (the "if not enabled — enable it" requirement)** | ✅ `client.edit_2fa(new_password=..., hint=..., email=...)` — set, change, or disable two-step from code. The onboarding wizard can *refuse to proceed* until it's set. | [Telethon docs](https://arabic-telethon.readthedocs.io/en/stable/extra/basic/creating-a-client.html) |
| **Global search across the user's chats/groups/channels** | ✅ `messages.search` (per-dialog, with `inputPeerEmpty` = all private chats + normal groups) and **`messages.searchGlobal`** (all chats, groups, supergroups, channels the user has access to); `contacts.search` for public channel name/description lookup. Channels you haven't joined: `CHANNEL_PRIVATE` — content is not readable (stated limitation). | [core.telegram.org/methods/search](https://core.telegram.org/method/messages.search) [SO 75888813](https://stackoverflow.com/questions/75888813/how-to-find-telegram-channel-by-word-in-its-message) |
| **History polling for watchers** | ✅ `iter_messages` / `GetHistory` — cheap call; flood behavior ≈ 30s per 10 requests; Telethon auto-sleeps on `FloodWaitError` below threshold. A 2–5 min watcher cadence is far inside limits. | [Telethon docs](https://docs.telethon.dev/en/stable/modules/client.html) |
| **Flood limits (our volume is trivial by comparison)** | ✅ Bot side: ~1 msg/s per chat, 20/min per group, ~30/s bulk. User side: same spirit, `retry_after` is law. Our usage (a handful of msgs per negotiation, periodic polls) is orders of magnitude under. | [grammy.dev](https://grammy.dev/advanced/flood) [betterclaw](https://betterclaw.io/blog/telegram-banned-ai-agent-what-to-do) |
| **Pressing inline buttons in bot chats from the user side** | ⚠️ Likely ✅ via `messages.resendBotCallbackQuery(query_id)` (MTProto RPC for the user to (re)send a callback) — **run a 30-min day-1 spike**; fallback: equivalent text command, or user taps the final confirm. | MTProto schema; spike required |
| **Official Bot API "face" + Mini App + Stars** | ✅ Separate BotFather bot = our UI (DM + inline buttons + Mini App webview). Free, no approval. Mini App calls our local backend over a tunnel (Cloudflare/ngrok at the booth). | [blocksentient](https://blocksentient.com/review/telegram-bots/) [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps) |
| **Real UZ official bots as counterparties** | ✅ Verified handles in §8 (Uzum ×3, Beeline ×2, Ucell, Yandex partner, MFA consular). Yandex Market Go is new in UZ (2025) — a growing dispute surface. | §8 sources |
| **LLM layer** | ✅ Cloud model API for negotiation quality (default) **or** local 7B class for the zero-egress tier ("literally nothing leaves the device"). | — |

**The dual-identity architecture (the core technical insight):**
- **The Face** — an official Bot API bot (`@wakilBot`): what the user talks to; owns the Mini App; sends status pushes; collects 👍/👎. 100% official API, zero risk.
- **The Hands** — an MTProto user session on the user's own account: what *acts* in the user's other chats (official bots, humans, groups). This is where the "agent in the place people already live" physically happens.
- **The Brain** — a local FastAPI + LangGraph agent connecting the two, with SQLite (or SQLite+sqlite-vec) as the local memory. The Face and the Hands never touch the user's data anywhere else.

---

## 5. Full workflows (your spec, made precise)

### 5.1 Onboarding — "login, MFA, consent" (your requirement: *login → enable MFA if missing → enter key*)

The wizard lives in the Mini App (big buttons, UZ/RU). Steps:

1. **Start** — user taps "Boshlash" in `@wakilBot` → bot explains the model in 3 lines: *"Men sizning nomingizdan gaplashaman. Ma'lumotlaringiz faqat shu qurilmada. Hech narsa o'rinlashtirmasdan oldin siz tasdiqlaysiz."* (I speak on your behalf. Your data stays on this device. Nothing happens without your confirmation.)
2. **Phone login** — Mini App step 1: phone number → backend triggers MTProto `send_code_request` → code arrives **in the user's own Telegram** (or SMS) → user enters it into the wizard. (We never see the code in transit to third parties — it's the user's normal Telegram auth.)
3. **2FA gate (the security money shot)** — backend checks `account.getPassword`:
   - *2FA already enabled* → step 4.
   - *Not enabled* → **the wizard refuses to continue**: "wakil ishlay olmaydi, chunki 2FA yo'q. Endi sozlaymizmi?" → guided enable: user types a password twice (+ optional recovery email) → `client.edit_2fa(new_password=...)` → confirmed. **Copy for the pitch: "The agent's first act on your account is to make it more secure than it was."**
4. **2FA key entry** — user enters the 2FA password once → session established. The password is **never stored** — the MTProto session file (encrypted, device-local, chmod 600) carries the auth. Re-login (new device) repeats steps 2–4.
5. **Data policy (explicit, in-app, not a wall of text)** — three lines + toggles:
   - *"Qaerda saqlanadi: shu qurilmada (SQLite, shifrlangan sessiya). Hech qayerga yuborilmaydi."* (Stored on this device only. Never sent anywhere.)
   - *"Qurilmadan chiquvchi yagona narsa: LLM so'rovlari (model: X). 'To'liq lokal' rejimi: 7B lokal model — hech narsa chiqmaydi."* (The only thing leaving the device: LLM prompts to [model]. "Full local" mode: 7B local model — nothing leaves.)
   - *"Tozalash: bitta tugma — barcha ma'lumot o'chadi."* (Wipe: one button — all data deleted.) + a visible **WIPE** button from day one.
6. **Scope selection (the counter to "full access")** — the agent's powers are **per-counterparty, allowlisted**, not global:
   - *Act in:* [official bots ▾] (pre-filled starter pack from §8: Uzum, Beeline, Ucell, Yandex…) — user checks which.
   - *Act with humans:* [allowlist ▾] — user adds specific contacts (e.g., the seller who owes them a refund). **Default: humans are OFF until explicitly allowed** (this is the safest default and a trust feature).
   - *Search in:* [all my channels & groups ▾ / selected ▾] + default date window (90 days).
7. **Preference init (60-second quiz)** — language (UZ/RU/mixed), risk style (conservative / balanced / assertive), default deadline (24h/48h/7d), escalation default (ask me / decide within bounds / silent stop).
8. **Ready** — bot DM + Mini App show: session active · 2FA ✓ · scope · learned-prefs (empty) · [New mandate] [Search] [Watch].

> **Why judges care:** this sequence is the "clear and controllable" criterion performed, not described. The agent *requires* 2FA, *limits* itself to an allowlist, and *offers* a wipe. "Full access" is reframed as **scoped, revocable, audited delegation** — which is the only defensible form of full access.

### 5.2 Negotiation — the core loop (your spec: *key points → strict user parameters → negotiate with bots or humans → out-of-bounds → escalation → completion*)

**A. Mandate creation (the "complete valid points" requirement).**
The user gives key points conversationally in the bot DM *or* via the Mini App form. The agent **must not start until the mandate card is complete and confirmed** — incompleteness is a feature: it asks exactly for what's missing, nothing else.

```jsonc
// mandate card (SQLite: mandates)
{
  "id": "M-0007",
  "counterpart": { "type": "official_bot", "handle": "@UzumSupport", "in_allowlist": true },
  "objective": "refund_or_exchange",
  "item": {
    "description": "Uzum'dan olingan pichoq, ayna qismi singan",  // shoes bought from Uzum, sole defect
    "order_ref": "UZ-88231",
    "evidence": [ "photo:heel_defect_1.jpg", "photo:box_label.jpg" ]
  },
  "bounds": {                                  // ← the user's STRICT parameters
    "min_value_uzs": 450000,                   // never below this (refund floor / credit floor)
    "acceptable_outcomes": ["exchange_same", "exchange_upgrade", "refund", "store_credit"],
    "max_wait_hours": 48,                      // deadline
    "non_negotiables": ["no_defective_replacement", "respond_in_uz_or_ru"],
    "disclosure_line": "Men foydalanuvchi o'nomidan murojaat qilaman (wakil orqali)."
  },
  "strategy": "assertive",                     // from preference quiz / learned profile
  "learned_seeds": [ { "pref": "persistence_hours", "value": 48, "from": "M-0003" } ],
  "status": "confirmed_by_user",
  "created_at": "2026-09-12T18:04:00+05:00"
}
```

The agent reads the card back in plain UZ: *"Tushundim: almashtirish YOKI 450k so'mdan past emas. 48 soat. Defektli mahsulot qabul qilinmaydi. Boshlayman?"* → user taps **Boshla**.

**B. The negotiation engine (LangGraph state machine).**

States: `open → argue → escalate → offer_check → {accept | counter | walk} → summarize → feedback`.
Per turn, the loop is:

1. **Observe** — read incoming message(s) in the counterpart chat (user session), classify: *policy-denial / counter-offer / question / silence / human-takeover-detected / resolved*.
2. **Plan** — LLM (system prompt = strategy + bound summary + tone rules + "you are the user's delegate, disclosure given") proposes the next message **and** the intended commitment (a structured JSON: `{text, committed_value?, outcome_type?}`).
3. **Guard** — `BoundaryGuard` checks the commitment against the mandate card (§5.4). Pass → 4. Fail → the agent **does not send**; instead it escalates to the user: Mini App push + bot DM inline buttons `[Qabul qil (exception)] [Bahsimni davom et] [To'xtat]` with the exact violation shown ("offer 300k < your min 450k").
4. **Act** — send via the user session (flood-aware queue; 1 msg/s cap per chat; auto-sleep on `FloodWaitError` — and the Mini App shows "waiting 8s (rate limit)" so the pause *looks* designed).
5. **Mirror** — every step is mirrored live to the bot DM + Mini App timeline (the judge watches the negotiation in the Mini App in real time, with each outgoing message tagged `guard: PASS` / `guard: ESCALATED`).
6. **Button actions** — when the official bot presents inline buttons (Uzum's refund flow: "Ishonch → qaytarish"), the agent operates them via the user session (day-1 spike item; fallback: text command or user tap — §4).
7. **Escalation ladder** (strategy-driven, always within bounds):
   - script says "no" → agent cites facts (photo evidence, order ref, consumer-rights point) and asks for the **supervisor / specialist** (in UZ: "ixtisoslashtirilgan mutaxassis bilan bog'lash imkoni bormi?") — the documented AI-negotiation play: factual claims, policy citation, methodical escalation, persistent follow-ups [19pine](https://www.19pine.ai/blog/ai-gets-subscription-refunds-no-refund-policy);
   - `@Ucell_bot`-style flows → agent can literally *order a callback from a human specialist* through the bot (a verified real capability of that bot [t.me/ucell](https://t.me/ucell)) — the human then joins, and the agent continues with them (if the human is allowlisted) or hands the chat to the user with a live summary ("takeover" — the agent stops, the user types in the same chat, zero friction, because it's *their* account);
   - silence > `max_wait_hours/2` → one polite follow-up; silence > `max_wait_hours` → timebox summary + user decision.
8. **Completion** — outcome classified (won / partial / lost / walked) → the agent posts a 3-line result to the bot DM + Mini App: what was achieved vs the mandate, what was spent (turns, time), and the **feedback request** (§5.3).

**C. The demo-critical beat (design it into the script):** the counterparty offers **below the minimum** → guard fires → Mini App push to the judge → judge taps **"Bahsimni davom et" (hold firm)** → the agent replies politely and firmly, quoting the user's own parameter: *"Afsuski, 300k men uchun yetarli emas — minimumim 450k. Katta mutaxassis qarorini kutaman."* → counterparty concedes (exchange + 100k credit) → within bounds → ✅. **The agent just cited the judge's own numbers back at a company. That is the whole pitch in one exchange.**

### 5.3 The learning loop (your spec: *👍/👎 at the end → concludes user's desires → data stays local*)

1. **Feedback** — on completion, bot DM + Mini App: *"Qanday o'tdi?"* → 👍 / 👎 + optional tags: `[juda yumshoq] [juda qattiq] [erta topshirdi] [yoq]` (+ free text, optional).
2. **Typed preference update** — the LLM maps (situation, policy used, outcome, rating, tags) → a **structured, human-readable** preference row — never a black-box embedding as the user-facing layer:
   ```
   persistence_min_hours: 48        (from M-0007: 👎 "erta topshirdi")
   price_flexibility: 0.05          (from M-0005: 👍 accepted 5% off walk-away)
   outcome_priority: [exchange > refund]  if value < 500k  (from M-0003, M-0005)
   escalation_style: "cite_consumer_rights"  (from M-0002: 👍)
   ```
3. **Seeding** — the next mandate card is **pre-filled from these rows**, and the Mini App shows the provenance next to each default: *"48 soat — M-0007 dan"* (from your Uzum case). The user can edit or delete any learned row — **learning is a settings page, not a black box**.
4. **Storage** — everything in local SQLite; the `(situation, policy, rating)` tuples also feed a simple k-NN "which of your past cases is most like this one" suggestion (explainable by construction: it *shows you* the past case it's imitating).
5. **Demo beat (30s):** after the Act-2 negotiation, the judge gives 👎 + "erta topshirdi" → the preferences screen visibly gains a row → the judge opens a **second** mandate (a small one, e.g. "Ucell: 30k'dan qimmatroq xizmat olingan, qaytaring") → the card is pre-filled with the learned 48h persistence and the escalation style, provenance badges visible. **"It learned you in one case."**

### 5.4 The BoundaryGuard (the "strict command, only user's preferences" requirement — as code)

Every outgoing message/commitment passes **all** of these checks before it leaves the device:

| # | Rule | On violation |
|---|---|---|
| 1 | **Value bounds** — any committed number (refund, credit, price, discount) must lie within `[min_value, max_value]` of the mandate | block + user escalation with the exact violation |
| 2 | **Outcome whitelist** — only `acceptable_outcomes`; no new obligations (no "I'll wait 3 weeks" beyond `max_wait_hours`) | block + escalate |
| 3 | **Data allowlist** — only user-provided fields may be shared (order ref, phone, address, photos); PII not in the mandate is never sent | block + log |
| 4 | **Tone** — no insults, threats, emotional escalation; escalation is factual + polite (classifier + pattern rules) | rewrite once, then block + log |
| 5 | **Irreversible actions** — confirming a refund/exchange in the official flow, pressing a "confirm" button, any money movement: **always a user tap** (Mini App push + inline button) | never auto |
| 6 | **Timebox** — max turns/hours per mandate; on expiry: summary + user decision (continue/stop) | pause + ask |
| 7 | **Identity** — first message in any new counterpart chat must contain the disclosure line | auto-prepend |
| 8 | **Language** — stay in the user's chosen language(s); never switch to a language the user didn't enable | rewrite |

Unit tests for all 8 rules are part of the submission (show the test run in the repo README) — this is the "thoughtful failure handling" the rubric names twice. The guard's log is visible in the Mini App timeline (`guard: PASS / REWRITE / ESCALATED`) — **the control system is the demo.**

### 5.5 Search & watch (your spec: *keyword → find item/topic in specific channels & groups*)

1. **Search** — Mini App (or bot DM): keyword (+ optional scope: all / selected dialogs; window: 30/90/365 days; filter: text/photo/price-mentioned).
   - Execution: `messages.searchGlobal(q)` first pass; scoped deep pass with `messages.search(peer, q, min_date, max_date)` over selected dialogs; ranking = recency × keyword density × dialog weight (user's pinned/frequent dialogs weighted higher); top-N results with **jump links** (deep links to the exact message), channel name, snippet, price extraction where present (the LLM pulls "450 000 so'm" out of the snippet into a structured field → a mini price table).
   - Honest limits (stated in-app and in the pitch): content is searchable only where you're a member; public channels you haven't joined → name/description match via `contacts.search` with a "join to search" hint.
2. **Watch** — "Meni xabardor qil" (notify me): the watcher polls selected dialogs every 2–5 min (`iter_messages` with offset tracking — comfortably inside flood limits), matches the keyword (+ optional regex/LLM check: "only if it's a *sale*, not just a mention"), and pings the bot DM with a jump link. This turns the agent **proactive** in the user's own information world — the theme's "agent where the life already happens," applied to feeds.
3. **Demo beat (15s):** "iPhone 15 Chorsu" → 4 results from pre-seeded test channels (one with a price extracted into the table) → arm a watcher for "PS5 Toshkent" → 20 seconds later a teammate posts in the test channel → the judge's phone pings with the jump link.

---

## 6. Architecture

```
                        ┌────────────────────────────────────────────────────┐
                        │                 DEVICE-LOCAL                       │
                        │                                                   │
  User's Telegram ────► │  HANDS: Telethon user session (MTProto)           │
  (all their chats:     │   • login: phone → code → 2FA (enforce if off)    │
   official bots,       │   • send/observe in allowlisted dialogs           │
   humans, channels)    │   • messages.searchGlobal / search / iter_messages│
                        │   • flood-aware queue (1/s per chat, auto-sleep)  │
                        │   • inline-button ops (resendBotCallbackQuery*)   │
                        │              │                                    │
                        │              ▼                                    │
                        │  BRAIN: FastAPI + LangGraph agent                 │
                        │   • mandate state machine (open→argue→escalate→   │
                        │     offer_check→accept/counter/walk→summarize)    │
                        │   • BoundaryGuard (8 rules, unit-tested)          │
                        │   • LLM: cloud API (default) or local 7B (zero-   │
                        │     egress tier)                                  │
                        │   • preference memory: typed prefs + k-NN over    │
                        │     past (situation, policy, rating) tuples       │
                        │              │                                    │
                        │              ▼                                    │
                        │  MEMORY: SQLite (encrypted dir) + session file    │
                        │   mandates · messages_log · preferences ·         │
                        │   search_jobs · watchers · audit · official_bots  │
                        │                                                   │
                        │  FACE: aiogram bot (official Bot API) ── Mini App │
                        │   onboarding wizard · mandate form · live         │
                        │   negotiation timeline (guard tags) · prefs page  │
                        │   with provenance · search UI · watchers · 👍/👎  │
                        │   · WIPE button                                   │
                        └────────────────────────────────────────────────────┘
   * day-1 spike; fallback = text command / user tap
```

**Component notes:**
- **One process, three roles.** Telethon (hands) + aiogram (face) + LangGraph (brain) in one FastAPI app. The face and hands are separate Telegram identities; only the brain bridges them.
- **Local-first, precisely defined.** What leaves the device: (a) LLM prompts (model: cloud API — named in the data policy) unless the user picks the **full-local tier** (7B-class local model via Ollama/llama.cpp — "literally zero egress"), (b) the MTProto connection to Telegram itself (the user's normal app traffic), (c) the Mini App's tunnel URL at demo time. What never leaves: preference rows, message logs, search index, the 2FA password (never stored), the session file.
- **Audit table** logs every action with `actor: agent|user`, the guard verdict, and a hash of the message — the mini app's "activity" page is the audit log, human-readable.
- **Kill switch** — a physical-feeling button in the Mini App: *pause all activity now* (the agent mid-negotiation sends one closing line "men hozircha to'xtadim" only if the user allows; otherwise it simply stops and logs `paused_by_user`).
- **Multi-device honesty:** v1 is single-device (your laptop / a Raspberry Pi at home). The pitch line: "your home server, not our cloud" — which is exactly the trust story, and the roadmap is a user-owned VPS.
```

---

## 7. Data model (SQLite) — the "local-only" made concrete

| Table | Key columns | Why it matters |
|---|---|---|
| `mandates` | id, counterpart_type, counterpart_handle, objective, bounds_json, evidence_json, strategy, status, outcome, rating, rating_tags_json, created_at, completed_at | The signed contract; `bounds_json` is what the guard enforces |
| `messages_log` | id, mandate_id, dialog_id, direction(in/out), text, ts, guard_verdict(PASS/REWRITE/ESCALATED/BLOCKED) | Full replayable transcript; the Mini App timeline reads this |
| `preferences` | key, value_json, provenance_mandate_ids_json, updated_at, user_edited(0/1) | **Editable learned memory** — provenance shown in UI |
| `decisions` | id, situation_json, policy_json, outcome, rating | k-NN "which past case" source; explainable seeding |
| `search_jobs` | id, keyword, scope_json, window_days, results_json, created_at | Search history (user can clear) |
| `watchers` | id, keyword, dialog_ids_json, last_msg_id, notify_chat, active | Proactive "notify me" |
| `official_bots` | handle, name, type, known_flows_json, button_map_json, in_allowlist(0/1) | The curated official-bot pack (§8) + user extensions |
| `audit` | ts, actor(agent/user), action, detail_hash | The trust layer; shown in the "activity" page |

---

## 8. The official-bot pack (researched, verified handles — your "we give a list" requirement)

Seed data for `official_bots`, each with a known-flow map the agent learns to navigate (the team spends a few hours per bot documenting its menu tree — that documentation is itself a demo artifact: "we mapped Uzum's refund flow button-by-button"):

| Company | Bot | Verified | What wakil can do there |
|---|---|---|---|
| Uzum (bank) | `@UzumBank_Robot` | ✅ ~78k monthly users [t.me](https://t.me/UzumBank_Robot) | card-status queries, card block/unblock requests, fee/charge disputes (read-only nav + dispute messages) |
| Uzum (marketplace) | `@tezkorhelp_bot` (Tezkor support) | ✅ [t.me](https://t.me/tezkorhelp_bot) | **the demo star**: refund/exchange flow, order status, "transfer to supervisor" path |
| Uzum (marketplace, B-side) | `@umarket_business_bot` | ✅ [t.me](https://t.me/umarket_business_bot) | seller-side disputes (the flipped product story) |
| Beeline UZ | `@BeelineUz_HelpBot` | ✅ support [telegram.me](https://telegram.me/BeelineUzbekistan) | billing disputes, plan-change requests, complaint tracking |
| Beeline UZ | `@BeelineTakliflari_bot` | ✅ offers [telegram.me](https://telegram.me/BeelineUzbekistan) | "find me a cheaper plan with same usage" (a *proactive* win case for wakil) |
| Ucell | `@Ucell_bot` (My Ucell) | ✅ [t.me](https://t.me/ucell) | **order a callback from a human specialist through the bot** (verified feature) — wakil books the callback, then the human negotiation begins |
| Yandex Go (UZ) | `@Yapartnersupport` | ✅ [yapartner.uz](https://yapartner.uz/) | partner/driver disputes, commission queries |
| Yandex Market Go | (new in UZ, 2025 — find/verify the support bot in build week) | ⚠️ [sellerlab.uz](https://www.sellerlab.uz/en/yandexmarket-uzbekistan/) | marketplace disputes — growing fast, "we're early" pitch point |
| Government (MFA) | `@tiv_yordam_bot` | ✅ [uzdaily.uz](https://www.uzdaily.uz/en/uzbekistans-foreign-ministry-launches-telegram-bot-to-support-citizens-in-the-middle-east/) | consular request drafting (demo-adjacent: shows wakil works with *state* bots too) |
| + user-extended | any official bot the user adds (Payme, Click, Hamlon, Poytaxt ADO, utilities…) | — | the pack is data, not code: each entry = handle + flow map |

**Demo counterparties, split honestly:**
- **Negotiation demo** → a teammate-operated **simulated** `@UzumSupport` bot (scripted: policy denial → below-min offer → supervisor path). State it in the pitch: *"the negotiation runs against a simulated support flow; everything else runs against your real account."*
- **Real-environment proof** → wakil navigates a **real** official bot in its scripted flow (e.g. `@UzumBank_Robot` card-status menu, or `@Ucell_bot` "order a callback") — the agent reading and pressing the *real* bot's menu is the "it's not a mockup" moment.

---

## 9. 48-hour build plan (scope-cut hard; this idea's #1 risk is complexity)

**Stack:** Python 3.12 · Telethon (hands) · aiogram (face) · LangGraph (brain) · FastAPI (local API) · SQLite + sqlite-vec (memory) · Mini App = single-page React (or plain HTML/htmx if time is short) · LLM = cloud API default + Ollama 7B as the "full-local" tier · Cloudflare tunnel (booth).

### Day 1 — Foundation + the security story (EOD gate: a stranger can log in and 2FA gets enforced)
- [ ] MTProto session manager: `send_code_request` → code entry → `SessionPasswordNeededError` → 2FA entry; **`account.getPassword` check + `edit_2fa` enable-wizard** (the EOD-1 gate).
- [ ] Bot face (`@wakilBot` via BotFather) + Mini App shell: onboarding wizard steps 1–8, live session-state page.
- [ ] FastAPI + SQLite schema (§7) + audit table + WIPE button wired.
- [ ] **Spike (30 min, first thing):** `resendBotCallbackQuery` — can the user session press a bot's inline button? Record the result; pick the fallback.
- [ ] Flood-aware send queue (1/s per chat, `FloodWaitError` auto-sleep, visible "waiting Xs" state).
- **EOD-1 exit criteria:** judge logs in on a test account; 2FA was off → the wizard forces it on; Mini App shows session active + scope picker + WIPE. *The security story is complete.*

### Day 2 — The negotiation engine (EOD gate: one full negotiation with a boundary trip and a user escalation)
- [ ] LangGraph mandate state machine (§5.2) + counterpart adapter (one interface: `official_bot_scripted`, `real_bot_nav`, `human_dm` — the scripted Uzum bot implements it; the real-bot nav reuses it read-only).
- [ ] **BoundaryGuard: all 8 rules + unit tests** (run the test suite on the repo README — it's a scoring artifact).
- [ ] Escalation push: Mini App modal + bot DM inline buttons `[accept-exception] [hold] [stop]`; the agent blocks until a tap (rule 5).
- [ ] Live timeline mirror (Mini App) with `guard: PASS/ESCALATED` tags per message.
- [ ] Teammate's scripted `@UzumSupport` bot (3 branches: instant-yes / policy-denial+below-min / supervisor-grant) — **write the script to hit the demo beats exactly**.
- [ ] Real-bot read-only module: navigate `@UzumBank_Robot` or `@Ucell_bot`'s real menu (document its flow in `official_bots.known_flows`).
- **EOD-2 exit criteria:** end-to-end: mandate → open → denial → below-min offer → guard fires → judge taps "hold" → firm reply citing the min → supervisor grants within bounds → completion summary. *Run it twice before sleeping.*

### Day 3 — Search, learning, rehearsal (EOD gate: 90-second demo, 5× without failure)
- [ ] Search: `searchGlobal` + scoped `messages.search` + ranking + jump links + price extraction; pre-seed 3–4 test channels/groups with realistic UZ posts (iPhone 15, PS5, naan batches, iPhone cases…).
- [ ] Watchers: 2-min poller + "only sales" LLM filter + bot-DM ping with jump link.
- [ ] Learning loop: feedback UI (👍/👎 + tags) → typed preference row with provenance → **next mandate pre-filled** with "from M-XXXX" badges → prefs page (edit/delete rows).
- [ ] Failure paths: flood-wait visible state; network drop mid-negotiation (pause + resume + "I re-read the thread" summary); counterparty silence → timebox summary; kill-switch demo.
- [ ] `make demo` script (seeds DB, starts services, opens Mini App + two test Telegram accounts on two phones: "user" and "Uzum support").
- [ ] **5 full rehearsals** with a teammate judging against the rubric; fix the top 3 wobbles; record a 3-min backup video of a perfect run (insurance, used only if the live demo breaks).

**Deliberate cuts (say "roadmap" in the pitch, don't hint they were missing):** multi-device sync, voice-note negotiation (text-first v1), payment execution (wakil never moves money — it negotiates outcomes; the refund itself is processed by the official flow), Star subscriptions, the vendor-side product.

---

## 10. The 90-second demo (scripted, rehearsed, one designed failure)

| t | Beat | What the judges see |
|---|---|---|
| 0:00 | **State** | Mini App on a tablet: "wakil active · 2FA ✓ · scope: 4 official bots · data: on-device". (The judge logged in at the start of the slot — they typed the 2FA password themselves. *That's the security demo.*) |
| 0:10 | **Mandate** | Judge opens the Mini App, fills the card (UZ, photo of the flawed heel already attached): *exchange or ≥450k, 48h, no defective replacement*. Taps "Boshla". Agent reads the card back + shows the disclosure line. |
| 0:25 | **Live negotiation** | Two phones on the table: the user's Telegram (real account) and the "Uzum support" bot. Agent opens the chat, states the defect, cites the photo. Support: "Siyosatga ko'ra qaytarish yo'q — almashtirish only." Agent argues factually, asks for the specialist. |
| 0:45 | **The guard fires** | Specialist offers **300k credit** (below the 450k min). Mini App modal on the tablet: "Siz chegarangizdan tashqari taklif: 300k < 450k. [Qabul] [Bahsim] [To'xtat]". **Judge taps "Bahsim".** Agent: "Afsuski, minimumim 450k so'm — katta mutaxassis qarorini kutaman." |
| 1:00 | **Resolution** | Supervisor grants: exchange + 100k credit. Agent verifies vs bounds (PASS, shown in timeline), confirms, closes. 3-line summary in the bot DM. |
| 1:10 | **Learning** | Judge taps 👎 + "erta topshirdi" (pretend-case tag for the demo). Prefs screen: row appears, provenance "M-0001 dan". New mini-mandate opens **pre-filled** with the learned persistence + escalation style, badges visible. |
| 1:25 | **Search + watch** | "iPhone 15 Chorsu" → 4 results from their channels, one with extracted price in a table. Arm watcher "PS5 Toshkent". 20s later a teammate posts in the test channel → the judge's phone pings with the jump link. |
| 1:30 | **Wipe** | Judge taps WIPE → the prefs/history/search pages empty live. "Your data was never here." (Final beat. Silence. Applause.) |

**Designed failure (injected during rehearsal, kept in the live run):** between 0:25–0:45, a `FloodWaitError`-style pause appears in the timeline: "kutmoqda: 8s (rate limit)" → resumes. Visible, graceful, *by design*.

---

## 11. Hard judge questions — prepared answers

**"Isn't automating a user account a ToS violation?"**
"Personal automation of your *own* account — the same category as any third-party Telegram client (Telethon has been mainstream for years). We send a handful of messages per negotiation; Telegram's own published limits are ~1 message/second per chat, and we cap at that with automatic backoff. No bulk, no cold contact, no spam vectors. And we disclose in every first message that a delegate is acting. We ship a conservative mode by default." *(Numbers > apology.)*

**"What stops it from agreeing to terms the user didn't want?"**
"Nothing can — it's structural, not prompt-based. The mandate card is a data contract; every outgoing commitment passes the BoundaryGuard, which unit-tests against the card's min/max, outcome whitelist, data allowlist, and tone rules. Out-of-bounds → the message is never sent; the user's phone gets the exact violation and three buttons. Irreversible actions always require a tap. Here is the guard's test suite." *(Show the tests.)*

**"Full access to my account is terrifying."**
"Which is why the agent's first act is to *force 2FA on your account if it's off* — we refuse to operate without it. And 'full' is actually 'scoped': an allowlist of counterparties you check off, a search scope you set, per-action approval, a kill switch, an audit log, and one-tap wipe. Your data is stored on your device in an encrypted directory — the only egress is the model API, and there's a full-local mode with zero egress."

**"Isn't this just a chatbot with more steps?"**
"No. A chatbot converses in one window. wakil acts *across your account*: it presses the official support bot's own buttons, orders a human callback through Ucell's bot, searches your channels' histories, watches them for a keyword, and remembers how you negotiate — on your device. The chat is the control room; the account is the workspace. Remove the account and there is no product."

**"How is this different from Pine / Operator / Sierra?"**
"Sierra/Fini are the *company's* agent (B2B, on their side). Pine negotiates refunds *by email* with a fixed strategy. Operator drives a cloud browser for a task. wakil is the *consumer's* agent, account-native in the messenger where Central Asian service actually happens, bound by a signed mandate you control, with memory that stays on your device and gets better with your ratings. Different side, different channel, different contract, different privacy."

---

## 12. Rubric score map (honest)

| Criterion | Score | Rationale |
|---|---|---|
| **Core functionality** | **4 – 4.5** | End-to-end on a *real* account (login → 2FA → mandate → live multi-turn negotiation → outcome → rating → wipe). The complexity is the risk: three subsystems. Mitigated by the scope cuts in §9 and the simulated counterparty for the negotiation. If the rehearsal plan is actually executed, 4.5; a live wobble costs 0.5. |
| **Innovation & theme** | **4.5 – 5** | "Mandated delegation inside the messenger" is a genuine new pattern: account-level agency + signed-bounds policy enforcement + local preference learning. The environment (your whole account, where UZ service bots actually live) enables it — a standalone chatbox cannot press the counterparty's buttons or search your channels. The only strict-judge cap risk: "messaging = chatbox" — answered by §11's last question and by the action-surface breadth. |
| **Technical execution** | **4.5** | Dual-identity architecture (official Bot API face + MTProto hands), 8-rule policy guard *with unit tests*, local-first data with a precise egress policy, 2FA enforced by the agent itself, flood-aware queue with visible state, audit log. This is the strongest "thoughtful failure handling" surface of any idea on the list — if the guard tests actually run in the repo. |
| **Usefulness & experience** | **4.5** | Refund/dispute pain is universal (and measurable: manual support fights take 20–60 min of a person's evening); "find it in my channels + watch for it" is a daily utility for a 25M-user Telegram-first market; the learning loop makes it *personal*, which is the "agentic experience" the rubric wants. Control is exemplary (mandate, guard, taps, takeover, kill switch, wipe). |
| **Total** | **17 – 18.5 / 20** | Top-2 contending. Higher ceiling on Innovation/Usefulness than the Kiosk Operator; higher execution risk. |

---

## 13. Strategic notes for the team

1. **The pitch title is the pattern, not the feature:** *"wakil — the mandated delegate inside your Telegram. It signs a contract with you, then fights your battles in the messenger."* (wakil = "your representative/attorney" in Uzbek — the word does half the pitch for a local room.)
2. **Open with the environmental fact, not the tech:** "In Tashkent, customer service is a Telegram bot: 78k people talk to Uzum Bank's bot every month. Nobody's agent lives where the fight actually happens. Ours does — as you."
3. **The three demo beats are the whole score:** (a) the guard citing the judge's own minimum back at the company; (b) the 👎 → pre-filled second mandate ("it learned you in one case"); (c) the WIPE at the end. Rehearse these three to perfection; everything else is garnish.
4. **Honesty is the moat:** the ToS answer, the simulated-vs-real counterparty split, the "never moves money" boundary — each stated *first*, in the pitch, turns a weakness into a credibility signal. Global teams will oversell; you don't have to.
5. **After the hackathon, the engine flips:** same session layer + guard + memory, pointed at a *vendor's* account with a different mandate schema = the original "Do'kon" product. Mention this one line in the roadmap slide — it shows the judges you're thinking past 48 hours.
6. **Naming the local voice:** the agent speaks in the user's language mix (UZ/RU) with the user's *tone preference* (conservative/balanced/assertive) — and never in a language the user didn't enable (guard rule 8). That's a small detail judges remember.

---

## 14. Source index (accessed 2026-09-12)

- Telethon docs — client, auth, 2FA (`edit_2fa`), flood behavior: https://docs.telethon.dev/en/stable/modules/client.html · https://arabic-telethon.readthedocs.io/en/stable/extra/basic/creating-a-client.html
- Userbot legitimacy/risk (community consensus): https://stackoverflow.com/questions/74479638/are-user-bots-made-with-telethon-allowed-on-telegram
- Flood limits (Bot API numbers; user-side practice): https://grammy.dev/advanced/flood · https://betterclaw.io/blog/telegram-banned-ai-agent-what-to-do · https://tgkit.io/telegram-error-codes/
- MTProto search methods (`messages.search`, `searchGlobal`, `CHANNEL_PRIVATE`): https://core.telegram.org/method/messages.search · https://stackoverflow.com/questions/75888813/how-to-find-telegram-channel-by-word-in-its-message
- Verified UZ official bots: Uzum Bank `@UzumBank_Robot` https://t.me/UzumBank_Robot · Uzum Tezkor `@tezkorhelp_bot` https://t.me/tezkorhelp_bot · Uzum Market `@umarket_business_bot` https://t.me/umarket_business_bot · Beeline UZ https://telegram.me/BeelineUzbekistan · Ucell https://t.me/ucell · Yandex Go UZ partner https://yapartner.uz/ · Yandex Market Go in UZ (2025) https://www.sellerlab.uz/en/yandexmarket-uzbekistan/ · MFA consular bot https://www.uzdaily.uz/en/uzbekistans-foreign-ministry-launches-telegram-bot-to-support-citizens-in-the-middle-east/
- AI refund-negotiation prior art (email-side, consumer; the pattern validated, the channel unclaimed): https://www.19pine.ai/blog/ai-gets-subscription-refunds-no-refund-policy
- B2B refund agents (company-side prior art): https://www.usefini.com/guides/ai-customer-support-refund-processing · https://irisagent.com/blog/ai-refund-automation-returns-billing-disputes/
- Telegram Bot API economics (free, no approval): https://blocksentient.com/review/telegram-bots/
- Mini Apps: https://core.telegram.org/bots/webapps
- UZ market context (Telegram 88%, 25M users; Tashkent 97% internet): https://kz.kursiv.media/en/2025-04-10/engk-yeri-digital-habits-why-kazakhstan-loves-whatsapp-and-uzbekistan-prefers-telegram/ · https://101digital.uz/en/blog/uzbekistan-digital-marketing-report-2026/
- Telegram 1B MAU: https://chatbotscape.com/channels/telegram-chatbot-guide

---

*Prepared 2026-09-12. All handles/stats verified on the access date; re-verify the Yandex Market Go support bot handle and any Uzum flow-button behavior during build week (they change).*
