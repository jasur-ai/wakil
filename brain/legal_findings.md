# VAKIL — legal & fact audit (ai1 / P1 BRAIN)

**Run:** 2026-09-12, before any D1 code was trusted. **Method:** every legal/policy claim in
`brain/`, `docs/` and `contracts/` checked against a primary source (lex.uz, the committee's own
site, Uzum's published offer + FAQ). Sources fetched 2026-09-12. This file is the audit trail —
it is what "no hallucinated law" (product rule 4) means in practice: **we do not trust our own
docs either.**

---

## 1. Two errors that would have cost us the demo

### 1a. "The 2023 Consumer Protection Law" — wrong law, wrong year
The repo says the return right comes from a **2023** law. The actual instrument is
**O'zR Qonuni № 221-I, 26.04.1996**, "Iste'molchilarning huquqlarini himoya qilish to'g'risida",
in force in its **current edition**, amended repeatedly (2002→2024) and again by
**O'RQ-1078 of 31.07.2025**. Source: https://lex.uz/docs/-4704 (fetched 2026-09-12).

Why it matters: the Mini App renders a source chip `[18-modda · Qonun, 2023]`
(`docs/wakil-v2-winning-edition.md:149`). A chip that misdates the law is the one detail a
lawyer-judge checks first, and our entire differentiator is "we don't invent law".
**Fix (lead / ai2):** chip → `[16-modda · 221-I, tahrir 2025]`.

> Still open: a new/updated consumer-protection law was reported adopted **15.11.2025,
> approved 20.11.2025, published 24.11.2025** (CyberLeninka abstract). I could not fetch the
> text. If that is a *new* law rather than an amendment, article numbers may shift.
> **Do not ship "2023" either way** — 221-I is the safe, verifiable citation. Needs a lex.uz
> check by a human before D2 standup.

### 1b. Art. 18 is not our case's article
Verified from lex.uz:

| Ref | Title (verbatim) | What it actually governs |
|---|---|---|
| 16-modda | Iste'molchining **nuqsonli** tovarning xarid narxini ... kamaytirishni yoki **shartnomani bekor qilishni** talab qilish huquqi | **defects** → price reduction or rescind + refund |
| 17-modda | Iste'molchiga **nuqsonli** tovar sotilgan taqdirda u bilan hisob-kitob qilish | **defects** → settlement; refund in the same form as payment |
| 18-modda | Iste'molchining **maqbul sifatli** tovarni almashtirib olish huquqi | **good-quality** item: 10-day exchange, refund only if no exchange stock |

Our demo case is `objective: "to'liq qaytarish: nosoz iPhone 15 (ekran defekti)"` — a
**defect**. Citing 18-moddа there claims a right to return a *faultless* item, and invites the
one reply that kills the scene: *"10 kun o'tdi / bu sizning aybingiz"*. The correct article
already existed in the corpus and nobody was using it.

**Fix shipped by me (this commit):** the corpus now records which kind of case each article
fits (`article_applies_to()`), the guard has advisory **R12 `check_article_fit()`**
(a mis-fitting article → REWRITE, never a silent send), and the prompt only ever shows the
agent the articles that fit the case. `test_brain.py` asserts both directions.
The demo line becomes: *"16-modda asosan, nosoz tovar bo'yicha shartnomani bekor qilib
450 000 so'mni qaytarishni talab qilamiz."*

### 1c. "Uzum 14-day policy" — the number is 10, and we were missing the better lever
`corpus.py` seeded `uzum-14` sourced to `101digital.uz` (a blog). Uzum's own published terms say:

* **10 calendar days** to return any good-quality item from the order date; extendable to **30**
  in some cases — `seller.uzum.uz/seller/agreement/uz/`, §5 (fetched 2026-09-12).
* **Seller silence for 20 calendar days after an objection = the claim is deemed ACCEPTED**
  (same section). *This is our strongest scripted move and it was not in the strategy.*
* For **quality objections** the return window is the **warranty period, or 6 months** when
  there is none, and the seller has **20 days** to fix the defect free of charge —
  `uzum.uz/uz/faq` (fetched 2026-09-12). This is what makes a day-30 defect claim still win.
* Support handle is **`@Uzum_Support_Bot`** (not `@UzumSupport`). Orders are held **8 days**
  at the pickup point.

Seeds are now `uzum-10` + `uzum-warranty`, each with a primary source. The mandate/corpus entry
for the counterparty's own policy is what R03/R09 check against, so this also fixed a
provenance bug, not just a number.

---

## 2. Corrections already applied in code (`brain/`)

| Was | Now |
|---|---|
| seeds sourced to `kun.uz` article link, `101digital.uz`, `davlat.uz` | primary sources only (lex.uz / Uzum offer+FAQ / committee site / gov.uz); `corpus.audit()` **fails the build** if any entry lacks an https source, a `YYYY-MM-DD` fetch date, ≥40 chars of body, or still carries a legacy source |
| "2023 law" framing | 221-I of 26.04.1996, current edition (O'RQ-1078) |
| `18-modda` used for everything | 16/17 for defects, 18 for good-quality; case kind detected from the mandate |
| no distinction between "we may name the source" and "we may quote it" | `quotable()` — `28-modda` and the Civil-Code note are in the corpus (so R09 resolves them) but **their text may not be quoted**, because I verified the title only. Corpus self-test enforces it. |
| R08 "language" accepted any Latin text (an English demand passed) | R08 now rejects foreign function-word signatures with no UZ/RU markers → REWRITE. Caught by `eval.py` case `english-draft-self-heals`. |
| a below-floor number phrased as a normal sentence left the device | `_classify` now treats **any number of ours that isn't their number** as a counter-offer → R01 BLOCK. Caught by `eval.py` case `agent-tries-to-go-below-floor`. That was a genuine rule-1 bypass in the demo path. |
| `open_case()` called `hands.send()` without the guard | every send goes through `Agent._turn()` — one gated path, no exceptions |
| disclosure matched only the dictionary word form | matches the brand form **and** the dictionary form (see §4.1) |

## 3. Facts that are now IN the corpus and are pitch-grade

* **30 070** consumer-rights complaints reached the committee in 2024; appeals **grew 65.7 %**
  in 2025; **837** in H1 2026 — committee's own page (fetched 2026-09-12). Our "33 % are
  defective-goods returns" line was not found in that source: **use the numbers above instead**,
  they are stronger and citable.
* **The state has already fined our counterparty.** The committee ordered **Uzum Market** to
  return **1.6+ млрд so'm** to consumers (mislabelled shelf life, ~145 000 units); courts upheld
  it — `gazeta.uz/oz/2025-09-11/uzum-market/`. This is the single best line in the pitch: it
  proves the escalation ladder actually bites.
* Escalation ladder, verified: company → **committee (1159 / (71) 207-48-00,
  info@antimon.gov.uz, e-xat antimon@exat.uz)** → **my.gov.uz** → **President's Virtual
  Reception**. Sector-specific: telecom (Beeline/Ucell/Artel) → **O'zkomnazorat, 1144**;
  banking/payments → **Central Bank, Bank nazorati qo'mitasi** (Art. 28 covers financial
  services). Source: `gov.uz/oz/uzkomnazorat/contacts`, `advice.uz/oz/documents/2263`,
  `cbu.uz`, `lex.uz`.
* **Art. 27^1**: appealing up the hierarchy does **not** waive the right to go to court → our
  ladder is parallel, not sequential. That answers the judge question "why not just sue?".
* Appeals have **no filing deadline** as a rule (O'RQ-445, Art. 22) — kills "you're too late".

## 4. Decisions and open items (post-consolidation)

1. **Spelling — settled, but it broke a guard.** Owner decision: single public repo `wakil`,
   `wakil` everywhere (AGENTS.md rule 1). Applied repo-wide by bulk rename — including
   `DISCLOSURE_MARKERS`, where the everyday Uzbek word form of "representative" was the
   *matching* pattern. With only the brand spelling left in that tuple, R07 REWRITEs a natural,
   correct disclosure sentence (the v-form of the word) into stilted Uzbek — the guard would be "fixing"
   valid language. **I restored the v-form as a matcher only** (`guard.py`, comment says so: it
   is input matching, never outbound copy). Every string the agent *sends* says `wakil`.
   Lead: veto in one line if you disagree, it is a 1-tuple change.
2. **`@consumergovuz_bot` is unverified** — it is asserted in `README.md`, `AGENTS.md` (30-second
   brief), `chat.md` §3, `contracts/00` (R11 description) and the runbook, but the committee's own
   page publishes **1159 / (71) 207-48-00 / info@antimon.gov.uz / e-xat antimon@exat.uz**, not that
   handle. **ai3's D3 probe must confirm it.** Until then the demo should not print the handle as
   fact — I marked the corpus entry as such, and `strategy_uz.md` now routes the state move to
   1159 + the e-xat inbox, which is real and still lands the punch.
3. **Whisper (uz) is NOT verified.** My D1 gate item says "3 fixture clips". There is no audio
   fixture in the repo (board row 9) and `faster-whisper` is not installed here. I built and
   tested the half that is ours — `slots.py` maps a transcript to a schema-valid mandate and
   reports what is missing, ASR injected like the LLM, on 3 written transcripts (uz digits, uz
   number-words, ru). **The STT leg is unverified and I am not claiming it.**
4. **LLM vendor undecided** (D0-4 says vendor-agnostic; nothing picks one). This blocks real-output
   prompt tuning — my next task after that. One line in `DECISIONS.md` unblocks me.
5. **Not verified by me — do not cite:** the 15/30-day appeal-review SLA, Beeline/Ucell public
   terms (D1 gate item, still to scrape), and whether the law reported adopted 15.11.2025 changed
   article numbering. Three one-line lookups for whoever has lex.uz access.
6. **Dead link:** `brain/README.md` pointed at `docs/battle-plan.md` → fixed to
   `docs/team-battle-plan.md` in this PR. `face/` and `voice/` are untouched by me (other owners).
7. **`make test` runs only `test_guard.py`.** Suggested 2-line Makefile change (lead-owned):
   `cd brain && $(PY) -m unittest test_brain && $(PY) eval.py`.

## 5. What ai1 shipped this block

`corpus.py` (verified seed + audit + `cite(query, case_kind)` + `article_applies_to`),
`guard.py` (R12 advisory + R08 fix + disclosure spellings), `graph.py` (finished loop: gated
`_turn` for every send, inbound classifier, defect-aware prompts from `strategy_uz.md`,
`verify()` money gate, exception → memory), `slots.py` (voice → mandate), `verify.py`
(5 fixtures), `learn.py` (typed prefs + provenance + prefill), `eval.py` (10 transcripts,
independent re-audit of every send), `test_brain.py` (**40 tests**), `legal_findings.md`.

`make test` equivalent for my files: `cd brain && python3 -m unittest test_brain` → `Ran 40 … OK`,
and `python3 eval.py` → `guard violations: 0 (must be 0)`.
