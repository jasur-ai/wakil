# wakil pitch kit — deck (7 slides) + 5-min script + Q&A (owner: lead)

## Slides (cut from the poster — keep its words)
1. **wakil** — Your Personal Telegram Delegate. *"A chatbot answers. wakil closes the case."*
2. **Problem + why now.** UZ: e-com +40%/yr, 3% of retail online, 84% still bazaar. Defective goods, no one chases the refund — tired people don't file complaints. The law exists (2023 Consumer Protection Law, Art. 18 = 10-day return) but awareness + friction kill it. **The arena is already in Telegram:** company bots, the state agency's own bot (`@consumergovuz_bot`, 1159), 1B+ MAU, ~85% of UZ.
3. **Product + pattern.** Mandate → in-bounds negotiation (bot + human) → state ladder → verified close. One line: *"Mandated delegation: the agent is a delegate with a signed authority card, not a chatbot."*
4. **The demo** (hands off — 90s runbook).
5. **Why us.** (a) Built where the fight already happens (UZ Telegram ecosystem, native uz voice + text). (b) The state escalation ladder is OUR differentiator — nobody below the company level. (c) Trust architecture: local-only data, 2FA, 11-rule guard, no-hallucinated-law corpus. (d) Team: we shipped the trust parts before the AI (guard suite green on day 0).
6. **Numbers.** Uzum 20M MAU · 33% of agency complaints = our case · Gartner: >40% of agentic projects die by 2027 (unclear value, weak risk) — *"we are the 60%: the mandate is the value, the guard is the risk."*
7. **Roadmap.** Live Uzum Bank statement nav (auto-verification) · more company packs (Beeline/Ucell/Kun) · family guardian links · multilingual. Close: **"The arena is ready. The player was missing."**

## 5-minute script (timed; one pre-planned cut)
- 0:00–0:30 · Hook: "In Uzbekistan, e-com grows 40% a year. And when the iPhone arrives broken, the refund still dies in a support chat. Not because the law is weak — the 2023 Consumer Protection Law gives 10 days. But a tired person after work doesn't write a complaint. So we built a delegate who does."
- 0:30–1:30 · Why now: the four clocks (UZ e-com scale; the state agency already runs a Telegram bot; the 2023 law; Gartner's agentic wave + its failure modes). One line: "The arena is already in Telegram. Company bots, the state agency's bot — 85% of the country is on it."
- 1:30–2:30 · Product: the mandate card (floor, deadline, walk-away) → the agent negotiates in-bounds → escalation ladder → verified close. "A chatbot answers. wakil closes the case."
- 2:30–3:15 · Why us: native UZ (voice first, local Whisper), the state ladder, the trust architecture. "Gartner says 40% of agentic projects die from unclear value and weak risk controls. The mandate is our value statement. The guard is our risk control. We are the 60%."
- 3:15–5:00 · Demo + roadmap + close. **Cut line if over time:** drop the roadmap detail, keep the numbers slide.

## Q&A card (10 hardest, ~20s each)
1. **Is this ToS-safe?** User's own account, user-initiated, rate-limited (1 msg/s, auto-sleep), only user-scoped dialogs, visible waiting states. Gray zone acknowledged in docs (v1 §3) — we demo the user's consent flow, not mass automation.
2. **What stops overcommitting?** The 11-rule BoundaryGuard — deterministic, unit-tested (16 tests, green on day 0). The LLM drafts; the guard decides. Below-floor → user tap. Below-floor-by-agent → hard BLOCK + incident.
3. **Why won't Sierra/Telegram do this?** Sierra plays B2B enterprises; Telegram plays the platform. The UZ consumer-protection wedge (state ladder, Art. 18, uz voice, local-only trust) is a local product — exactly the gap in the market.
4. **Isn't it a chatbot?** No: it holds a mandate, walks a dispute ladder, produces a legal artifact (dossier), and only closes on verified money. "A chatbot answers. wakil closes the case."
5. **Is Art. 18 really 10 days?** Yes — 2023 re-issued Consumer Protection Law, Art. 18: 10-day return/exchange for good-quality non-food goods; 33% of agency complaints are defective returns. Citation in the corpus with source + fetch date (R09 blocks the rest).
6. **What if the state bot changes?** The dossier + hotline 1159 + the agency's public channels are the fallback — the agent degrades to a paste-ready dossier, never to silence.
7. **Why local-only?** Trust is the product in consumer advocacy. No cloud = no data risk story, no per-seat cost, works offline-first. The booth laptop is the only server — we show the network view at the booth.
8. **How do you verify the money?** Screenshot → local vision → structured JSON (expected vs observed). Only `confirmed` closes the case. Roadmap: live Uzum Bank statement nav.
9. **What if the counterparty is a human, not a bot?** Same loop: the agent messages the human manager chat (user-scoped), same guard, same discipline. Rehearsed in the demo on the counterparty phone.
10. **Team / division of labor?** Four tracks, frozen contracts, per-day gates (battle plan). Trust parts (guard, session, schema) were green on day 0 — the AI runs on top of them, not instead of them.
