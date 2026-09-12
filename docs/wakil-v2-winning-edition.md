# wakil v2 — WINNING EDITION
### Research-driven re-design · 2026-09-12 · "Nega biz · Nega aynan hozir · Nega aynan shu"

> **One-line v2:** wakil is a mandated, local-memory agent that fights your consumer cases **inside your own Telegram** — from the company's support bot, through a human supervisor, all the way to the **state Consumer Protection Agency's own Telegram bot** — citing real Uzbek law, verifying the money actually landed, and learning how *you* negotiate, with everything stored on your device.

This document builds on `idea1-wakil-deep-dive.md` (v1: architecture, mandate card, BoundaryGuard, 2FA enforcement, search/watch, dual-identity design). **Nothing in v1 is thrown away** — v2 adds the differentiation layer that turns a strong idea into a winning one. Everything new here is research-backed; sources are in §9.

---

## 0. What changed in v2 (the six upgrades)

| # | Upgrade | Why it wins |
|---|---|---|
| 1 | **State escalation ladder** — company bot → supervisor → **state Consumer Protection Agency** (`@consumergovuz_bot`, hotline 1159), with an auto-built **official complaint dossier** citing real law | No competitor touches the state level. The whole dispute ladder in Uzbekistan *already exists in Telegram* — wakil is the first thing that walks it. This is the "surprising new pattern" the rubric asks for, with a government stamp on it. |
| 2 | **Refund verification loop** — "the case isn't closed until the money lands" (screenshot-vision check in demo; Uzum Bank bot statement nav on roadmap) | Turns "agent negotiated" into "agent **delivered**." Delivery, not conversation, is the value. |
| 3 | **Voice-first mandate** — dictate the dispute as a voice note (self-hosted Whisper `uz` = zero egress) | The natural interface for a tired UZ user; doubles the "your data never leaves the device" story (STT runs locally). |
| 4 | **Legal citation engine** — local corpus of the 2023 Consumer Protection Law + real company return policies; the agent cites articles **with source and article number**, and a guard rule blocks any citation not in the corpus | "It quotes the law, and it can't hallucinate one." Factual escalation is the documented winning negotiation play; in UZ the facts are law articles. |
| 5 | **Code-switching + price radar** — UZ-Latin/Cyrillic/RU/EN auto-detection in replies; search results extract prices into a table + cross-channel market check | 84% of UZ retail is still bazaar; Telegram channels *are* the marketplace. A price radar in your own channels is daily utility nobody offers. |
| 6 | **Family guardian** — one-tap read-only share of a live case to a relative (no control, no data beyond the case timeline) | UZ families co-manage problems. It's a cultural feature, a trust feature, and a safety feature in one. |

---

## 1. Nega aynan HOZIР (why exactly now) — four clocks, all verified

### Clock 1 — The market clock: commerce is exploding, disputes grow with it
- **Uzum alone: 20M+ monthly users — over half of Uzbekistan's population** — 2025 net income **$176M**, e-commerce GMV **>$500M (up 1.5× y/y)**, total payment volume **$11.1B (2× y/y)**, **4M+ bank cards issued**, 17,000+ sellers, 100M+ SKUs, 1,500 pickup points. [bne IntelliNews, Feb 2026](https://new.intellinews.com/articles/uzbekistan-s-uzum-reports-2025-bottom-line-of-176mn-fintech-fastest-growing-vertical-425973) [Wikipedia/Uzum](https://en.wikipedia.org/wiki/Uzum)
- **Uzbek e-commerce: ~$1.2–2.6B and growing 15–40% y/y** depending on methodology; KPMG sees **up to 7× growth to $2.2B by 2027 (40%+ CAGR)**. [ecdb](https://ecdb.com/resources/sample-data/market/uz/all) [Forbes Council (KPMG data)](https://www.forbes.com/councils/forbesbusinessdevelopmentcouncil/2026/03/02/unlocking-opportunity-how-e-commerce-is-empowering-every-uzbek/) [101digital](https://101digital.uz/en/blog/uzbekistan-digital-marketing-report-2026/)
- **The gap that makes this urgent: online is still only ~3% of UZ retail; 84% of transactions happen in bazaars** (vs 20% in Kazakhstan, 14% in Belarus). [Kursiv/INFOLine, Apr 2025](https://uz.kursiv.media/en/2025-04-29/e-commerce-accounts-for-just-3-of-uzbekistans-retail-market/)
- **Pitch line:** *"Every single incremental dollar of Uzbek e-commerce creates new customers, new orders — and new disputes. The market is on a 40% CAGR and still at 3% of retail. We are not late to this market; we are early, and the fight is just beginning."*

### Clock 2 — The channel clock: the arena is already in Telegram
- In Tashkent, customer service **is** a Telegram bot — verified list in v1 §8: Uzum Bank (24/7, ~78k monthly users), Uzum Tezkor, Beeline, Ucell (with human-callback ordering), Yandex Go, **and the state Consumer Protection Agency's own bot `@consumergovuz_bot`** (verified live [t.me](https://t.me/consumergovuz_bot); hotline **1159** confirmed on the official government portal [davlat.uz](https://davlat.uz/en/raqobat/news/prezident-matbuot-xizmati-yangiliklari?activity_id=503)).
- Telegram in UZ: **~85–88% of the population, ~25M users** [101digital](https://101digital.uz/en/blog/uzbekistan-digital-marketing-report-2026/) [Kursiv](https://kz.kursiv.media/en/2025-04-10/engk-yeri-digital-habits-why-kazakhstan-loves-whatsapp-and-uzbekistan-prefers-telegram/); globally **1B+ MAU since March 2025** [chatbotscape](https://chatbotscape.com/channels/telegram-chatbot-guide).
- **The decisive fact (v2's spine):** the *entire* consumer-dispute ladder in Uzbekistan — company support bot → company human → **state agency bot/1159** — **already lives in one app: Telegram.** The battlefield was digitized *before* agents arrived. Nobody has to build the arena; wakil just steps onto it.
- **Pitch line:** *"In the West, the fight for your rights happens on email and phone calls. In Tashkent it already happens inside Telegram — company bots, and even the state agency's bot. The arena is built. The player is missing. That's us."*

### Clock 3 — The technology clock: agents became mandate-grade in 2025–26
- Gartner: **<1% → 33%** of enterprise software will include agentic AI (2024 → 2028); **0% → 15%** of day-to-day work decisions made autonomously by agentic AI. [Gartner via BigDATAwire, Jun 2025](https://www.hpcwire.com/bigdatawire/this-just-in/gartner-predicts-over-40-of-agentic-ai-projects-will-be-canceled-by-end-of-2027/)
- **And the counter-argument, weaponized:** Gartner also says **>40% of agentic AI projects will be canceled by end-2027** — for *unclear business value* and *inadequate risk controls*. [same](https://www.hpcwire.com/bigdatawire/this-just-in/gartner-predicts-over-40-of-agentic-ai-projects-will-be-canceled-by-end-of-2027/)
  → **Pitch line:** *"Gartner predicts 40% of agent projects will die from unclear value and weak risk controls. wakil was designed to be the opposite: the value loop is closed (the money lands, verified), the risk is contractually bounded (the mandate card + 10-rule guard), and the data risk is eliminated (local-only). We're the 60%."*
- The three enablements that only existed recently: (a) LLM tool-use reliable enough for multi-turn negotiation with structured commitments; (b) **Whisper with native `uz` support, self-hostable** (voice-first + zero-egress) [Deepgram Whisper docs / Whisper 99-language list incl. Uzbek](https://developers.deepgram.com/docs/deepgram-whisper-cloud); (c) mature MTProto user-client libraries (Telethon) with programmatic 2FA enforcement. In 2024 this project was a thesis; in 2026 it's a weekend.

### Clock 4 — The legal clock: the law was modernized, the enforcement gap is the product
- The **2023 re-issuance of the Law "On Protection of Consumer Rights"** explicitly strengthened protection for **digital trade and online services** — the law caught up with e-commerce. [CyberLeninka analysis of the 2023 law](https://cyberleninka.ru/article/n/o-zbekistonda-iste-molchilar-huquqlarini-himoya-qilish-to-g-risida-gi-qonunning-ahamiyati)
- **Article 18 (real, citable): the right to return/exchange good-quality non-food goods within 10 days** of purchase. [Kun.uz](https://kun.uz/news/2021/08/14/sotilgan-tovar-qaytarib-olinmaydi-bu-qonuniymi)
- **33% of all analyzed complaints to the Consumer Protection Agency are about defective-product returns/exchanges** — the single most common consumer battle in the country is *exactly* wakil's core loop. [Kun.uz, citing the Agency](https://kun.uz/news/2021/08/14/sotilgan-tovar-qaytarib-olinmaydi-bu-qonuniymi)
- The state machinery exists (Agency under the Antitrust Committee, hotline 1159, territorial hotlines) but **enforcement is slow and offline** — the academic analysis itself says implementation mechanisms "work weakly" and legal awareness is the bottleneck. [CyberLeninka](https://cyberleninka.ru/article/n/o-zbekistonda-iste-molchilar-huquqlarini-himoya-qilish-to-g-risida-gi-qonunning-ahamiyati)
  → **The gap, precisely stated:** the law is new and consumer-friendly; the state bot exists; companies' bots exist; but **no one connects the three** — the citizen still has to know the article, gather the evidence, format the complaint, and switch channels. wakil *is* that connection.
- **Pitch line:** *"The government wrote a modern consumer law in 2023 and gave the agency a Telegram bot. But 33% of all complaints in the country are still the same fight: 'I bought a defective item, I want it back or exchanged' — and the citizen has to do the legal homework alone. wakil does the homework, carries the evidence, and files the case. The law is ready. The arena is ready. Now the agent is here."*

### Why not earlier / why not later (one line each)
- **2024:** the negotiation loop wasn't reliable enough; UZ marketplaces were half their size; the state bot was unknown to builders.
- **2027+:** enterprise agent platforms (Sierra-class) will localize *downmarket* — the consumer side of a 3%-penetration, bazaar-trusting, Telegram-native market won't be their first stop. **The window for the local team is now.**

---

## 2. Nega aynan BIZ (why exactly us)

This is the section most hackathon teams skip. It's also the one judges remember, because every global team in the room will be asking themselves the same question. Four points, each verifiable in the room:

### 2.1 We are the product's first users (and our demo uses a real dispute)
We are daily users of Uzum, Beeline, and Ucell with real accounts and **real past disputes** (a refund that took 3 weeks, a bill error we fixed by phone at 9pm, a lost-parcel case). During build week, one of those *actual* disputes becomes the seed case in the demo — the photo evidence is a real photo, the order number is real.
**Pitch line:** *"The dispute you're about to watch a version of — our team member already lost it by hand last month. The agent fights the same fight we lost."*
*(A global team's demo case will be synthetic. Ours has a scar.)*

### 2.2 Native trilingual negotiation — tone is a technology
UZ service culture has its own grammar: respectful persistence beats Western aggression; the right word at the right step ("mazkur buyurtma bo'yicha", "majburiy", escalation phrasing) changes outcomes. We design the negotiation strategy **in** the language, not **into** it — UZ-Latin, UZ-Cyrillic, Russian, English, code-switching mid-conversation, auto-detected.
**What a translated product gets wrong:** it sounds like a foreigner demanding rights. Ours sounds like a sharp neighbor's son who read the law.
**Pitch line:** *"Any team can translate a prompt into Uzbek. Only a team from Tashkent can write a negotiation that a Tashkent support bot — and a Tashkent supervisor — actually responds to."*

### 2.3 The service-flow maps are local knowledge, and they are the product's brain
v1's `official_bots` table (per-bot flow maps, button trees, escalation paths) looks like a data file; it's actually **field research**: who answers, what the script says, where the supervisor path hides, which phrasing triggers a human callback (e.g., Ucell's bot literally sells a "callback from a specialist" — a verified feature [t.me/ucell](https://t.me/ucell)). That map is built by *being in the queues*, not by scraping.
**Pitch line:** *"Our moat isn't the model — it's the map. We walked every flow we demoed, with a real account, and wrote down where the real person hides behind the bot."*

### 2.4 "wakil" is a local concept — the product is culturally native, and local data trust is a feature
"wakil" (вакил / representative, attorney, the one you authorize) is how UZ speakers already describe a person you give authority to. The product name *is* the pitch. And "your data stays on your device" lands differently here than in the EU: in a market where 84% of commerce is still face-to-face bazaar trust [Kursiv](https://uz.kursiv.media/en/2025-04-29/e-commerce-accounts-for-just-3-of-uzbekistans-retail-market/), a homegrown agent with **no cloud, no third party, one-tap wipe, and 2FA enforced by the agent itself** is the only credible trust story for giving an AI your account.
**Pitch line:** *"A cloud SaaS can't sell 'your data stays on your device' to a bazaar culture and mean it. We're not a cloud. We're your home server, your language, and your name on the product."*

### What a competitor team cannot copy (honest table)

| If the competitor is… | They can copy | They **can't** copy in 48h (or ever, cheaply) |
|---|---|---|
| A global LLM team | The agent loop, the guard | UZ-native negotiation tone; the service-flow maps; real local accounts & real disputes; "wakil" cultural fit |
| A local UZ team (typical: "AI assistant for business") | A chatbot | The **consumer-side mandate** (they build for companies, not citizens); the state-ladder integration; local-only architecture |
| An enterprise agent vendor (Sierra/Fini-class) | The refund flow | The consumer side of a 3%-penetration Telegram-native market isn't their ICP; per-resolution pricing vs a local agent; local trust |
| A fast-cloning hackathon team | The UI, the mini app | The 2FA-enforced session layer + boundary guard tests (weeks of careful work compressed); the legal corpus (law + policies, local); the state bot flow map |

**The one-sentence difference:** *Everyone else is building a support bot for a company. We are building a wakil for a citizen — in the messenger where the fight already happens, down to the state agency's own bot.*

---

## 3. The six UZ-realism upgrades — spec, evidence, feasibility, demo beat

### U1 ⭐ The state escalation ladder + complaint dossier (THE differentiator)

**What.** wakil's negotiation state machine gains a **level-3 escalation** (v1 had company-bot → human; v2 adds the state):
```
L1: company support bot (scripted flow, mapped)
L2: human supervisor / specialist (via the bot's own escalation paths,
    e.g. Ucell's "order a callback" feature [t.me/ucell](https://t.me/ucell))
L3: STATE — Consumer Protection Agency (Antitrust Committee):
    • auto-built official complaint dossier (shikoyat)
    • pre-filled submission draft for @consumergovuz_bot (verified live bot
      [t.me](https://t.me/consumergovuz_bot)) and hotline 1159
      (official [davlat.uz](https://davlat.uz/en/raqobat/news/prezident-matbuot-xizmati-yangiliklari?activity_id=503))
```

**The dossier** (a real `.docx`/PDF, built from the case record):
1. Citizen data (from the mandate — user-confirmed fields only)
2. Counterparty, order ref, dates
3. Factual narrative (auto-summarized from the logged negotiation, in formal UZ)
4. **Law citations with article numbers** (from the local legal corpus — U4)
5. Company's own policy citations (their return policy, from the corpus)
6. Evidence: photos (the defect), chat-log export (wakil's own transcript, timestamped)
7. Demand (from the mandate's outcome preference) + the exact relief requested
8. Signature line (the user signs on paper or confirms digitally)

**Why UZ specifically.** The 2023 Consumer Protection Law modernized digital-trade protection [CyberLeninka](https://cyberleninka.ru/article/n/o-zbekistonda-iste-molchilar-huquqlarini-himoya-qilish-to-g-risida-gi-qonunning-ahamiyati); **33% of all agency complaints are defective-goods returns/exchanges** — the exact case type wakil automates [Kun.uz](https://kun.uz/news/2021/08/14/sotilgan-tovar-qaytarib-olinmaydi-bu-qonuniymi); enforcement is the bottleneck (slow, offline, low legal awareness) [CyberLeninka](https://cyberleninka.ru/article/n/o-zbekistonda-iste-molchilar-huquqlarini-himoya-qilish-to-g-risida-gi-qonunning-ahamiyati). wakil removes the bottleneck: the citizen taps, the dossier exists.
**Also — the threat is the leverage:** even *mentioning* "ishonch bo'lmasa, 1159 va Agentlikka shikoyat tayyorlayman" (if we can't agree, I'll prepare a complaint to 1159/the Agency) — as a **last-resort, user-authorized line only** — changes company behavior. (Guard rule: the state-escalation threat may only be sent if the user pre-checked "allow mentioning state escalation" in the mandate card. Never auto.)

**Feasibility (48h):** MEDIUM-HIGH value / MEDIUM cost (~6h). The dossier builder = a template engine over the existing case record + `python-docx`. The L3 "submission" in the demo = the agent **opens the real `@consumergovuz_bot`, starts its flow as the user, and prepares the first steps, stopping before final submit for a user tap** (read-mostly, honest). If the state bot's flow turns out opaque in build week: fallback = dossier + a formatted copy ready to paste into the bot/1159 channel, clearly labeled. **The dossier itself is the hero artifact — it wins even if the live submission is a paste-ready draft.**

**Demo beat (15s):** after the company concedes (or in the "if they refuse" branch): *"Va agar rad etsa?"* → the Mini App shows the dossier: formal complaint, 2 photos attached, chat export, **"18-moddaga asosan… 10 kun ichida"** citation → export .docx → "shikoyat tayyor: @consumergovuz_bot / 1159". One tap later the judges have a *real legal document* in their hands (projected on screen).

### U2 The refund verification loop — "the case isn't closed until the money lands"

**What.** On resolution, wakil doesn't trust the promise. It waits for the money:
- **Demo-safe version (MUST):** the agent messages: "Qaytarish ko'rsatildi: 450k → Uzum karta. Mablag' tushdi-mi? Skrinshot yuboring." The user sends a **wallet/bank statement screenshot** (Payme / Click / Uzum Bank app) → **vision check**: agent extracts amount + date, matches against the mandate's expected value, confirms: *"Tasdiqlandi: 450 000 so'm, 14-sentabr 09:12, Uzum karta. Ish yopildi. ✅"* — or flags a mismatch (*"Miqdor to'g'ri emas: 400k tushgan, 450k kutilgan — davom etaymi?"*).
- **Roadmap version (name it, don't build it):** read-only statement navigation inside `@UzumBank_Robot` (the bank's own 24/7 bot [t.me](https://t.me/UzumBank_Robot)) to confirm the credit without any screenshot — if a team member has a live Uzum Bank account, map the statement menu in build week.

**Why UZ.** Refund disputes in a 3%-penetration market are often *about the money that never arrives* (5–14 working days per local refund policies [bazari.app policy text](https://www.bazari.app/refund)). "Negotiated" is not "received" — the verification loop is the difference between a demo toy and a trusted agent. It also makes the agent's success metric **measurable in the demo**: the case ends with a green check and a timestamp, not a chat emoji.

**Feasibility:** LOW cost (~3h). Vision on a screenshot = one LLM call with a strict JSON schema (`{amount_uzs, date, channel}`) + unit tests on 5 fixture screenshots. Robust enough for the demo; honest about real-world messiness.

**Demo beat (10s):** screenshot in → 2s → *"Tasdiqlandi: 450k, 14-sentabr. Ish yopildi ✅"* with the amount and date on screen. *(Prep two screenshots: a match and a mismatch — use the mismatch if the judges ask "what if it's wrong?".)*

### U3 Voice-first mandate — "I'm tired, I'll just say it"

**What.** The user's demo opens with **a voice note**, not a form: the judge (or teammate) records ~10–15 seconds in Uzbek: *"Uzum'dan pichoq oldim, tagi singan, qaytarishim kerak… kamida 450k, 2 kun vaqt bor."* wakil: **self-hosted Whisper (`uz`)** transcribes (zero egress — it runs on the booth machine) → parses into the mandate card (objective, amount floor, deadline) → **reads the card back for confirmation** → the judge taps "Boshla".
**Why UZ.** Voice is the dominant mode of personal communication in UZ (voice notes everywhere); a tired user dictating a dispute is the *most natural* entry point imaginable — and it's the moment the room hears the agent understand colloquial Uzbek with real numbers. It also upgrades the privacy story: **STT is on-device** — even the voice never leaves.
**Feasibility:** LOW (~2h). Whisper small/base self-hosted is fine for 15-second clean audio; the LLM does slot extraction with a JSON schema; unknown slots → the agent asks (v1 behavior). Keep the Mini App form as the parallel path (form is faster for the demo if voice stumbles — the fallback is visible, which is honest design).
**Demo beat (10s):** voice note in → transcript appears word-by-word → mandate card populates itself → confirmation tap.

### U4 Legal citation engine — "it quotes the law, and it can't make one up"

**What.** A **local legal corpus** (SQLite + sqlite-vec embeddings, built D1):
- **The Law "On Protection of Consumer Rights" (2023 edition)** — key articles: **Art. 18** (10-day return/exchange right for good-quality non-food goods [Kun.uz](https://kun.uz/news/2021/08/14/sotilgan-tovar-qaytarib-olinmaydi-bu-qonuniymi)), return windows, defective-goods provisions (Art. 11-class: seller obligations re: expired/mislabeled goods [daryo.uz](https://daryo.uz/2021/05/20/ozbekistonda-muddati-otgan-mahsulotlarni-sotganlik-uchun-sanksiyalarni-kuchaytirish-rejalashtirilmoqda)), compensation for damages.
- **Counterparty policies**: Uzum's 14-day return window (marketplace level) [101digital guide](https://101digital.uz/en/blog/how-to-sell-on-uzum-market-2026/), FBS/FBO return responsibilities [chaika.uz](https://chaika.uz/en/marketplace/uzum), Beeline/Ucell public terms — scraped once in build week, versioned with fetch-date.
- **Guard rule 9 (new):** *any* citation in an outgoing message must resolve to a corpus entry (article number + source); unresolvable → rewrite or drop. **No hallucinated law, ever.** The Mini App timeline shows the citation with its source chip: *[18-modda · Qonun, 2023]*.
**Why it wins:** the documented winning plays of AI refund negotiation are **factual claims, policy citation, methodical escalation** [19pine](https://www.19pine.ai/blog/ai-gets-subscription-refunds-no-refund-policy). In a court-and-law culture, a well-cited agent is intimidating *in the right way* — and the guard rule turns the scariest LLM risk (confident legal hallucination) into a testable engineering guarantee.
**Feasibility:** MEDIUM (~4h incl. scraping/structuring). Build it D1 evening so D2's negotiation engine has ammo from hour one. (If lex.uz full-text access is flaky during the hackathon, the corpus still works from the verified article summaries + official agency pages — cite the source URL per entry either way.)
**Demo beat (inside Act 2):** the agent's second message: *"18-modda asosan, sifatli nooziq-ovqat tovarini 10 kun ichida almashtirish/qaytarish huquqi menga berilgan. Mazkur holat — ishlab chiqarish eibi."* The source chip glows in the Mini App timeline.

### U5 Code-switching + price radar

**What.** (a) **Code-switching**: the agent detects the counterpart's language (UZ-Latin / UZ-Cyrillic / RU / EN) per message and replies in kind — within the user's enabled languages (guard rule 8 extended). This is trivial with modern LLMs and *huge* for realism: UZ support bots reply in RU; the agent handles it without the user noticing. (b) **Price radar** (extends v1 search): for each search hit, the LLM extracts price mentions (`"450 000 so'm"` patterns + context) into a mini table, and for a repeated item across the user's channels it computes "cheapest seen / median / 30-day trend".
**Why UZ:** 84% of commerce is bazaar [Kursiv](https://uz.kursiv.media/en/2025-04-29/e-commerce-accounts-for-just-3-of-uzbekistans-retail-market/); Telegram channels *are* the marketplace; "who has the best price this week" is a weekly ritual. A personal price radar inside the user's own channels is **private market intelligence** — no platform has it because it would require reading your chats (only an account-native agent can).
**Feasibility:** LOW (~2h). Price extraction = regex + one LLM verify pass; the table is a Mini App component.
**Demo beat (10s):** the v1 search beat, upgraded: results arrive **with prices in a table** and a one-line verdict ("eng arzon: @tashkent_deals, 30 kunning eng past narxi").

### U6 Family guardian — "apam ham ko'radi"

**What.** One tap in the case view: **"Oilaga ko'rsatish"** → generates a **read-only** link to the Mini App case timeline (the negotiation transcript, guard tags, status) for one or two family members — no control actions, no account access, no data beyond that case, revocable with the same tap.
**Why UZ:** UZ families co-manage problems; an elderly parent's dispute watched by the adult child is the culturally exact shape of "someone is handling it for you." It also **solves the demo-audience problem**: the judges *become* the family — their phones show the live case timeline while the negotiation runs. The room is inside the product.
**Feasibility:** VERY LOW (~1–2h): the Mini App case page already exists (v1 timeline); the guardian link = the same page with a read-only session token.
**Demo beat:** two judge phones (or one judge phone) show the live case timeline with guard tags during Act 2. *(This is what makes the demo feel like a system, not a bot.)*

---

## 4. Architecture deltas over v1 (what's new, precisely)

```
v1 state machine: open → argue → escalate → offer_check → accept/counter/walk → summarize → feedback
v2 state machine: open → argue → escalate → [L2 human] → offer_check → accept/counter/walk
                                        ↘ L3 state: dossier_build → dossier_handoff (user tap)
   + intake paths:      voice_note → (local Whisper uz) → slot_extraction → mandate_confirm
   + post-resolution:   promise → wait_window → screenshot_vision_check → verified_close | mismatch_escalation
   + guard rules:       #9 citation-must-resolve-to-corpus   #10 dossier-completeness-before-export
                        #11 state-escalation-mention only if pre-authorized in mandate
   + new tables:        legal_corpus(entry_id, type=law|policy, article, text, source_url, fetched_at)
                        dossiers(id, mandate_id, docx_path, submitted_state, created_at)
                        verifications(id, mandate_id, expected_uzs, observed_uzs, date, channel, verdict)
                        guardians(id, mandate_id, token_hash, role=readonly, revoked_at)
```

Everything else (dual identity, flood-aware queue, 2FA enforcement, local SQLite, kill switch, WIPE, audit) stands as v1.

---

## 5. The 90-second demo, v2 (final script)

| t | Beat | Stage |
|---|---|---|
| 0:00 | **State** | Tablet: "wakil active · 2FA ✓ · data: on-device". (The judge typed the 2FA password at slot start.) A second phone (a "family member's") already shows the live case timeline — read-only. |
| 0:10 | **Voice mandate** | Judge records a 12-second voice note in UZ (flawed shoes, min 450k, 48h). Whisper (local) transcribes live → mandate card populates → guard pre-check → tap **Boshla**. |
| 0:28 | **L1: company bot** | Real user account → `@UzumSupport` (simulated, teammate-operated). Agent opens with disclosure + defect photo + factual claim. Bot: *"Siyosatga ko'ra qaytarish yo'q."* |
| 0:45 | **L2 + law** | Agent escalates politely, asks for specialist. Specialist offers **300k** → **guard fires** → Mini App modal (violation shown: 300k < 450k) → judge taps **Bahsim** → agent: *"Minimumim 450k. **18-modda** asosan sifatli tovarda 10 kun ichida almashtirish huquqi bor."* (source chip in the timeline on the family phone — same moment.) |
| 1:05 | **Resolution + money lands** | Supervisor: exchange + 100k credit (within bounds, PASS). Agent closes the negotiation… then: *"Mablag' tushdi-mi?"* → wallet screenshot in → **2s** → *"Tasdiqlandi: 450 000, 14-sentabr 09:12. Ish yopildi ✅"* |
| 1:20 | **The state ladder (15s)** | *"Va agar rad etsa?"* → dossier materializes: formal complaint, photos, chat export, **[18-modda]** citation → .docx exported → *"Tayyor: @consumergovuz_bot / 1159."* |
| 1:35 | **Learning + search (20s, fast cuts)** | Judge 👎 + "erta topshirdi" → prefs row appears with provenance → second mini-mandate **pre-filled** from it. Then "iPhone 15 Chorsu" → results **with price table** → watcher armed → teammate posts → judge's phone pings. |
| 1:55 | **WIPE** | Tap WIPE → history, prefs, search empty on screen. *"Ma'lumotlar shu qurilmada edi. Endi yo'q."* (End.) |

**Injected failure (kept):** a visible `FloodWaitError`-style pause mid-Act 2 ("kutmoqda: 8s — rate limit") → resumes. Designed, graceful.
**Backup insurance:** 3-min recorded perfect run, played only if the live demo breaks.

---

## 6. The 5-minute pitch, v2 (ready to speak — UZ/EN mix, with stage directions)

**[0:00 – The scene, in UZ]**
"O'zbekistonlik odam uchun 'murojaat qilish' deb bir so'z bor. Ushbu so'z orqasida uchta navbat bor: birinchi — kompaniya boti. Ikkinchi — 'operator hozir band' telefoni. Uchinchisi — tuman bo'limiga borib, qog'oz to'ldirish. Va aksariyat odam ikkinchi navqatda topshiradi. Chunki u qonunning 18-moddasini bilmasligi mumkin, lekin bot bilmaydi — va bot hech qachon topshirmaydi."
*(For an Uzbek, "making a claim" means three queues: the company bot, the busy phone line, the district office with its forms. Most people quit at queue two. They might not know Article 18 — but the bot doesn't know either, and the bot never quits.)*

**[0:40 – What we built]**
"wakil — shu uch navqatning barchasini **bitta Telegram ichida** o'tkazadigan wakilangiz. Bu chatbot emas: u *sizning* hisobingizdan, *sizning* so'zlaringiz bilan, siz imzolagan **mandat** doirasi ichida gaplashadi. Minimum narx, maksimal shart, muddat, topshirish nuqtasi — hammasi oldindan siz tomonidan belgilanadi. Chegara ortiga bir harf ham chiqolmaydi — har xabar **policy guard** dan o'tadi, har tartibsiz amal **sizning barmoq zarbingizni** kutadi."

**[1:30 – Why now, in one breath (the four clocks, 30s)]**
"Chun ki hozir: **birinchi** — Uzum oyiga 20 million odamni ishlatadi, e-commerce 40% tezlikda o'syapti, lekin hali ham savdoning 3 foizi — ya'ni kurash hali boshlanmoqda. **Ikkinchi** — kurash maydoni allaqachon Telegramda: Uzum boti, Beeline boti, hatto **davlat Agentlik boti** ham. Arena tayyor — o'yinchi yo'q edi. **Uchinchisi** — 2023-yilda istismolchi huquqlari qonuni raqamli savdo uchun yangilandi; 33% davlat shikoyatlari aynan 'defektli tovar qaytarish' haqida. Qonun tayyor, agentlik boti bor, kompaniya boti bor — ularni bog'lagan hech narsa yo'q edi. **To'rtinchi** — agent texnologiya 2025-26 da ilk bor mandat-sifatiga yetdi: Gartner aytishicha, 40% agent loyihalari aniq qiymat va xavf nazorati yo'qligida o'ladi. Bizning loyihaning butun me'morchiligi aynan shu ikki so'zga — **aniq qiymat, cheklangan xavf** — asoslangan."

**[3:00 – Why us (20s)]**
"Va nega biz: chunki biz bu mahsulotning ilk foydalanuvchilariyuk. Demo'da ko'rsatadigan kurashning asl nusxasini biz o'tgan oy qo'lda yuttuq. Butun jamoa Toshkentda: o'zbekcha, ruscha, latinka va kirill — biz nega bu tilning tarjimasi emas, **o'zi** ekanini bilamiz. Va 'wakil' so'zini biz bobolardan bilamiz — vakolat bergan shaxs. Bu mahsulot bu yerda tabiiy."

**[3:30 – The demo (90s)]** *(run the §5 script live; no slides during demo)*

**[5:00 – Close, in one line]**
"Chatbot savolga javob beradi. wakil — ishni yig'adi. Va ish shu joyda yig'iladi, bu erda biz har kuni kurashayotgan joyda — Telegramda, sizning hisobingizda, sizning qonuningiz bilan, va ma'lumotlaringiz hech qachon shu qurilmadan chiqmaydi."
*(A chatbot answers. A wakil closes the case. And the case closes where we already fight — in Telegram, in your account, by your law, with your data never leaving your device.)*

**[Q&A armor — the three questions that will be asked (answers in v1 §11 + v2 §1–2)]**
- ToS? → personal automation, ~100× under flood limits, disclosed, conservative mode. *(Numbers.)*
- What stops it overcommitting? → the mandate card + 11-rule guard + unit tests + user taps. *(Show the tests.)*
- Why won't Sierra/Samsung/Telegram do this? → Sierra sells to companies, not citizens; Telegram sells the platform, not a UZ citizen's advocate; and the local maps + tone + trust are built by *being here*. The window for a local team is now, before enterprise platforms localize downmarket into a 3%-penetration, bazaar-trusting market.

---

## 7. Updated rubric scores (honest, post-v2)

| Criterion | v1 score | **v2 score** | What moved it |
|---|---|---|---|
| Core functionality | 4–4.5 | **4–4.5** | Same complexity core; the new features are small tools (dossier template, vision check, local STT) that add surface but not instability. The state-ladder's live submission is the only new external dependency → it has a paste-ready fallback, so it can't sink the demo. |
| Innovation & theme | 4.5–5 | **5** | v1's pattern was "mandated delegation." v2's pattern is **"the agent walks the citizen's regulatory ladder — company bot → supervisor → state agency bot — inside one messenger, citing the local law."** That is a *surprising new agent pattern whose central value could not be reproduced in a standalone chatbox* — word for word the rubric's 5. The state stamp (1159, @consumergovuz_bot) makes it un-ignorable to any judge, local or global. |
| Technical execution | 4.5 | **4.5** | Dual identity + 11-rule guard (two new rules are *testable guarantees*: no-hallucinated-citations, dossier completeness) + local Whisper + on-device vision verification + local legal corpus. The architecture now reads as a **civic-system design**, not a bot. |
| Usefulness & experience | 4.5 | **4.5–5** | The value chain now closes on *money, verified* (U2) — the agent's success is a timestamped green check, not a chat emoji. The dossier makes the agent useful on the *losing* path too (if the company wins the negotiation, the citizen still gets a state-grade complaint in 20 seconds). 33%-of-complaints stat + family guardian + price radar = usefulness across the week, not just the demo. |
| **Total** | 17–18.5 | **18–19 / 20** | The state ladder + verified delivery + legal corpus are the three deltas that take a strong entry to a front-runner. |

**Where v2 can still lose points (so you defend them):**
1. **Scope bloat in the pitch** — if the team demos U1–U6 as if all were fully production-ready, the judges discount everything. Rule: **U1, U2, U3 are "live"; U4 is "live for the law, partial for policies"; U5, U6 are "live-lite"; roadmap items are named as roadmap.** One sentence each, then move on.
2. **The state-bot live step wobbles** — the fallback (paste-ready dossier) must be *visible as a design choice*, not an apology. Rehearse the line: *"final submit — as with any state form — stays a human tap; the agent's job is to make that tap the only step left."*
3. **Legal citation accuracy** — if a judge asks "is Article 18 really 10 days?", the answer must be instant and sourced: "Yes — Art. 18, return/exchange within 10 days of purchase for good-quality non-food goods; here's the Kun.uz explainer and the 2023 re-issued law. And even if a specific article shifts, the guard would have blocked the citation — the corpus is versioned with fetch dates."

---

## 8. Updated 48-hour plan (v2 integrated — timeboxed)

Carry over v1's day structure; **new items are marked (v2)**. The golden rule is unchanged: *every new feature is a small, testable tool with a visible fallback — none of them may hold up the core loop.*

### Day 1 — Foundation + security story + the legal corpus
- [ ] MTProto session manager: login → code → 2FA check → **`edit_2fa` enable-wizard** (EOD-1 gate, unchanged)
- [ ] Bot face + Mini App shell: onboarding wizard, mandate form, live timeline, WIPE (unchanged)
- [ ] FastAPI + SQLite (new tables: `legal_corpus`, `dossiers`, `verifications`, `guardians`)
- [ ] 30-min spike: `resendBotCallbackQuery` button-press (unchanged)
- [ ] Flood-aware queue (unchanged)
- [ ] **(v2) U4 — legal corpus build (4h, D1 evening):** scrape/structure the 2023 Law's key articles (Art. 18 first) + Uzum 14-day policy + Beeline/Ucell public terms → embed → **citation guard rule #9 wired + unit tests** ("agent cannot cite an article not in the corpus"). *Exit: `cite(18)` returns text + source chip; a fake citation is blocked and logged.*
- [ ] **(v2) U3 — local Whisper `uz` + voice-note → slot extraction (2h)** → mandate card pre-population. *Exit: a 15s voice note becomes a filled card.*
- **EOD-1 gates (unchanged +):** stranger login w/ 2FA enforcement · corpus cites and blocks · voice note → card.

### Day 2 — Negotiation engine + the state ladder
- [ ] LangGraph mandate state machine (v2: + `L3_state`, `dossier_build`, `dossier_handoff`, `screenshot_vision_check`, `verified_close`)
- [ ] **BoundaryGuard: 11 rules + unit tests** (rules #9–11 new) — run the suite on the repo README
- [ ] Escalation push + live timeline with guard tags (unchanged)
- [ ] Teammate's simulated `@UzumSupport` bot (unchanged, script now includes the **below-min offer** and a **law-citation response** branch)
- [ ] Real-bot read-only nav (unchanged — `@UzumBank_Robot` / `@Ucell_bot` menu walk)
- [ ] **(v2) U1 — dossier builder (4h):** `python-docx` template over the case record (8 sections, §3-U1) + completeness rule #10 + **`@consumergovuz_bot` flow probe** (30 min: what does its menu actually do? record it in `official_bots.known_flows`; if opaque → paste-ready fallback, labeled)
- [ ] **(v2) U2 — verification loop (3h):** vision JSON schema + 5 fixture screenshots (match ×2, mismatch ×2, garbage ×1) + unit tests
- [ ] **(v2) U6 — guardian link (1h):** read-only session token → case page
- **EOD-2 gate (unchanged +):** full negotiation incl. below-min → guard → judge "hold" → **law citation in the live reply** → resolution → **screenshot → "Tasdiqlandi ✅"** → dossier exports as a real .docx.

### Day 3 — Learning, search-radar, rehearsal
- [ ] Learning loop: 👍/👎 + tags → typed prefs with provenance → second mandate pre-filled (unchanged)
- [ ] Search: `searchGlobal` + scoped + ranking + jump links (unchanged)
- [ ] **(v2) U5 — price extraction + price table + 30-day "cheapest seen" line (2h)** on pre-seeded channel fixtures
- [ ] Watchers (unchanged, 2-min cadence)
- [ ] Failure paths (unchanged +): vision mismatch escalation; corpus-missing citation (agent says "ma'lumotimda shu modda yo'q — tekshirib yuboraman" and logs); state-bot flow timeout → paste-ready fallback
- [ ] `make demo` (v2: seeds fixtures incl. 2 wallet screenshots, 4 channels, legal corpus)
- [ ] **6 rehearsals** (v2: one extra vs v1 — the state-ladder beat needs the most reps); record the 3-min backup
- [ ] Pitch dry-run ×2 against the §6 script, timed to 5:00

**Deliberate cuts (roadmap lines, unchanged + new):** multi-device sync, TTS voice replies (text-first), payment execution (never — verification only), Uzum Bank statement auto-nav (U2 roadmap tier), TON/Stars monetization, the vendor-side flip.

---

## 9. Source index v2 (all accessed 2026-09-12)

**Uzum scale & UZ e-commerce (the "why now" market clock):**
- Uzum 2025 results: 20M+ MAU, $176M net income, $500M+ GMV, $11.1B payments, 4M+ cards — https://new.intellinews.com/articles/uzbekistan-s-uzum-reports-2025-bottom-line-of-176mn-fintech-fastest-growing-vertical-425973
- Uzum profile (Tencent/VR Capital $70M round, $1.5B valuation, 17M+ MAU mid-2025) — https://en.wikipedia.org/wiki/Uzum
- Uzum FY2024 (16M MAU = 40% of population, $345M GMV, 700k cards) — https://www.prnewswire.com/ae/news-releases/uzum-holding-ltd-uzum-or-the-company-fy2024-results-302385292.html
- UZ e-commerce $2.649B 2025, 15–20% growth — https://ecdb.com/resources/sample-data/market/uz/all
- KPMG: up to 7× to $2.2B by 2027, 40%+ CAGR; 84% of retail still bazaar — https://www.forbes.com/councils/forbesbusinessdevelopmentcouncil/2026/03/02/unlocking-opportunity-how-e-commerce-is-empowering-every-uzbek/
- INFOLine via Kursiv: e-commerce = 3% of UZ retail (vs KZ 20%, BY 14%) — https://uz.kursiv.media/en/2025-04-29/e-commerce-accounts-for-just-3-of-uzbekistans-retail-market/
- UZ digital market 2026 (29.5M internet users, $1.2B e-com, Telegram 85%) — https://101digital.uz/en/blog/uzbekistan-digital-marketing-report-2026/

**The consumer-rights ladder (the "why now" legal clock + U1/U4):**
- 2023 re-issued Law "On Protection of Consumer Rights" (digital commerce) — https://cyberleninka.ru/article/n/o-zbekistonda-iste-molchilar-huquqlarini-himoya-qilish-to-g-risida-gi-qonunning-ahamiyati
- Art. 18 — 10-day return/exchange right; **33% of agency complaints = defective returns** — https://kun.uz/news/2021/08/14/sotilgan-tovar-qaytarib-olinmaydi-bu-qonuniymi
- Consumer Protection Agency: hotline **1159**, territorial hotlines — https://davlat.uz/en/raqobat/news/prezident-matbuot-xizmati-yangiliklari?activity_id=503 · https://khraqobat.uz/en/en-news/377-conveniences-of-electronic-payment-and-.html
- Agency's **Telegram bot `@consumergovuz_bot`** (verified live) — https://t.me/consumergovuz_bot · referenced in https://daryo.uz/2021/05/20/ozbekistonda-muddati-otgan-mahsulotlarni-sotganlik-uchun-sanksiyalarni-kuchaytirish-rejalashtirilmoqda
- Uzum 14-day return window (marketplace) — https://101digital.uz/en/blog/how-to-sell-on-uzum-market-2026/ · FBS/FBO return duties — https://chaika.uz/en/marketplace/uzum
- Refund timing norms (5–14 working days) in UZ marketplace policy texts — https://www.bazari.app/refund

**Official UZ service bots (arena verification, from v1 §8 — re-verified):**
- `@UzumBank_Robot` (24/7, ~78k monthly users) — https://t.me/UzumBank_Robot
- `@tezkorhelp_bot` — https://t.me/tezkorhelp_bot · `@umarket_business_bot` — https://t.me/umarket_business_bot
- Beeline UZ (`@BeelineUz_HelpBot`, `@BeelineTakliflari_bot`) — https://telegram.me/BeelineUzbekistan
- Ucell (`@Ucell_bot`, callback-from-specialist feature) — https://t.me/ucell
- Yandex Go UZ partner (`@Yapartnersupport`) — https://yapartner.uz/ · Yandex Market Go in UZ (2025) — https://www.sellerlab.uz/en/yandexmarket-uzbekistan/
- MFA consular bot — https://www.uzdaily.uz/en/uzbekistans-foreign-ministry-launches-telegram-bot-to-support-citizens-in-the-middle-east/

**Technology & prior art (why now clock 3 + differentiation):**
- Gartner: <1%→33% agentic software by 2028; 0%→15% autonomous decisions; >40% of agentic projects canceled by 2027 (value/risk) — https://www.hpcwire.com/bigdatawire/this-just-in/gartner-predicts-over-40-of-agentic-ai-projects-will-be-canceled-by-end-of-2027/
- AI refund-negotiation playbook (factual claims, policy citation, escalation, persistence) — https://www.19pine.ai/blog/ai-gets-subscription-refunds-no-refund-policy
- B2B refund agents (Sierra/Fini/Gorgias — company side) — https://www.usefini.com/guides/ai-customer-support-refund-processing · https://irisagent.com/blog/ai-refund-automation-returns-billing-disputes/
- Whisper language support (incl. Uzbek; self-hostable) — https://developers.deepgram.com/docs/deepgram-whisper-cloud
- v1 sources (MTProto, 2FA, search, flood limits, UZ Telegram stats) — see `idea1-wakil-deep-dive.md` §14

---

## 10. What we deliberately did NOT add (scope discipline — say it in the pitch)

1. **No payment execution.** wakil verifies money; it never moves it. (Safety + trust + scope.)
2. **No TTS replies in v1.** Text-first, voice-first *intake* (the high-value direction).
3. **No multi-device sync in v1.** One home server = the trust story; sync is roadmap.
4. **No cold-contact mode.** The agent never approaches a company or person the user hasn't specified. (ToS-safe by construction; also ethically the only defensible stance.)
5. **No "auto-accept below-min with a learned discount tolerance" in v1.** Learning pre-fills *parameters*; the guard still requires the user's tap on anything out of the current card. (Learning suggests; the mandate commands.)

---

*wakil v2 — "wakil — vakolat sizniki, kurash bizniki." (The authority is yours; the fight is ours.)*
