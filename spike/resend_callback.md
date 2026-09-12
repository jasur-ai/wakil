# Spike: can the user (MTProto) session press a bot's inline button?

**Status:** OPEN — **ai3** · **hard deadline D1 10:30** (decision D0-8). Result goes here AND into `DECISIONS.md`.

## Question
wakil's agent talks with official bots (e.g. @UzumSupport) through the **user's own MTProto session**.
Many bot menus require pressing an inline button (`callback_query`). Can the user session do that?

Candidate calls (verify in Telethon):
- `telethon.tl.functions.messages.SendBotCallbackQueryRequest` / `ResendBotCallbackQueryRequest`
- Telethon-level: `client.send_message(...)` then find the message's `reply_markup.inline_keyboard` → issue the callback from the user side.

## Test (15 min, test account)
1. Test account → any bot with inline buttons (e.g. @UzumSupport menu).
2. From a Telethon script: open the bot, read the latest message, extract button `data`, send the callback.
3. Observe: does the bot react (next menu / content)?

## Decision matrix
| Result | `press_button()` (Contract 01) | Demo impact |
|---|---|---|
| works | real callback send | zero — full autonomy |
| fails | **fallback A:** user taps the final confirm on their phone (visible, honest) · **fallback B:** text command path | beat 3 adds one user tap — script line ready |

**Rule:** whichever way, the demo is scripted for it BEFORE D2. Never discover on demo day.

## Result (ai3 fills by 10:30)
- call used:
- observed:
- decision (A/B/real):
- demo script line:
