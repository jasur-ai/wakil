"""The working agent: mandate-bound negotiation loop gated by the BoundaryGuard.

Runs as an asyncio task per case inside the FastAPI app. Demo mode uses
MockUzumGateway + ScriptedLLM (fully offline). Every outbound message passes the
BoundaryGuard; an ESCALATE/BLOCK pauses the loop until the user decides
(accept_exception | hold | stop). Verification -> dossier -> learning on close.
"""
from __future__ import annotations
import asyncio
import os
import sys

BRAIN = os.path.join(os.path.dirname(__file__), os.pardir, "brain")
if BRAIN not in sys.path:
    sys.path.insert(0, BRAIN)

import db as D
from guard import BoundaryGuard, Outbound, Verdict, parse_money, find_article_refs
from dossier import build as build_dossier


class CaseAgent:
    def __init__(self, db_path, case_id, mandate, gateway, llm, corpus):
        self.db = db_path
        self.case_id = case_id
        self.m = mandate
        self.gw = gateway
        self.llm = llm
        self.guard = BoundaryGuard(mandate, corpus)
        self.decision_event = asyncio.Event()
        self.decision = None
        self.turn = 0
        self.state = "negotiating"

    # -- case bus ---------------------------------------------------------
    def _emit(self, type_, payload):
        D.add_event(D.conn(self.db), self.case_id, type_, payload)

    def _first_citation(self, text):
        refs = find_article_refs(text)
        return refs[0] if refs else None

    def _send_guarded(self, text, intent="message", incoming_value=None, media=None):
        self.turn += 1
        o = Outbound(text=text, turn=self.turn, intent=intent,
                     incoming_value=incoming_value, media=media or [])
        res = self.guard.check_outbound(o)
        if res.verdict is Verdict.PASS:
            self._emit("turn.outbound", {"text": text, "guard_verdict": "PASS",
                                          "citation": self._first_citation(text)})
            return True, res
        # REWRITE / ESCALATE / BLOCK -> never send; ask the user
        self._emit("guard.escalation", {"rule": res.rule, "violation": res.detail,
                                         "options": res.options or ["hold", "stop"]})
        return False, res

    # -- user decision (from POST /case/{id}/decision) ---------------------
    def on_decision(self, option):
        self.decision = option
        self._emit("user.decision", {"option": option})
        self.decision_event.set()

    # -- main loop ---------------------------------------------------------
    async def run(self):
        try:
            await self._negotiate()
        finally:
            await self.gw.close()

    async def _negotiate(self):
        # 1) opening with disclosure (R07)
        text = self.llm.opening(self.m)
        sent, _ = self._send_guarded(text, intent="message")
        if not sent:
            await self._wait_and_stop()
            return
        await self.gw.send(text)

        # 2) counterparty replies: denial + below-floor offer
        inbound = await self.gw.next_inbound()
        if inbound is None:
            self._resolve("counterparty_silent")
            return
        self._emit("turn.inbound", {"text": inbound, "from": self.gw.dialog})

        # 3) agent reacts to the offer -> guard fires (below floor) -> user decides
        offer = parse_money(inbound)
        react = self.llm.react_to_offer(self.m, inbound)
        sent, _ = self._send_guarded(react, intent="react_to_offer", incoming_value=offer)
        if sent:  # offer was within bounds -> continue
            await self.gw.send(react)
            await self._maybe_close(inbound)
            return
        decision = await self._wait_decision()
        if decision == "stop":
            self._resolve("stopped_by_user")
            return
        if decision == "accept_exception":
            await self.gw.send(react)
            self._resolve("accepted_below_floor", amount=int(offer or 0))
            return
        # decision == "hold" -> hold the floor with the law move (R09 citation)
        law = self.llm.hold_reply(self.m)
        sent2, _ = self._send_guarded(law, intent="message")
        if not sent2:
            await self._wait_and_stop()
            return
        await self.gw.send(law)

        # 4) counterparty grants -> verify -> dossier -> learn -> close
        inbound2 = await self.gw.next_inbound()
        if inbound2:
            self._emit("turn.inbound", {"text": inbound2, "from": self.gw.dialog})
        await self._maybe_close(inbound2 or "")

    async def _wait_decision(self):
        self.decision_event.clear()
        await self.decision_event.wait()
        return self.decision

    async def _wait_and_stop(self):
        await self._wait_decision()
        self._resolve("stopped_by_user")

    async def _maybe_close(self, inbound):
        t = (inbound or "").lower()
        amount = parse_money(inbound)
        floor = float(self.m["bounds"]["min_value"])
        approved = ("tasdiqlan" in t or "qabul" in t) and (amount is None or amount >= floor)
        if approved:
            obs = int(amount or floor)
            self._emit("verification.result", {"expected": int(floor), "observed": obs,
                                                "verdict": "confirmed"})
            await asyncio.sleep(1.0)
            self._dossier()
            self._learn()
            close = self.llm.close(self.m)
            sent, _ = self._send_guarded(close, intent="close")
            if sent:
                await self.gw.send(close)
            self._resolve("resolved_verified", amount=obs)
        else:
            self._emit("guard.escalation", {"rule": "no-approval",
                                             "violation": "counterparty did not approve — your call",
                                             "options": ["hold", "stop"]})
            if (await self._wait_decision()) == "stop":
                self._resolve("stopped_by_user")

    # -- artifacts ---------------------------------------------------------
    def _dossier(self):
        m = self.m
        order = ((m.get("evidence") or [{}])[0].get("data") or {}).get("order", "—")
        minv = f"{int(m['bounds']['min_value']):,}".replace(",", " ")
        report = {
            "1. Citizen (Aholi)": "Foydalanuvchi (lokal akkaunt), vakil orqali ariza.",
            "2. Counterparty (Karshi tomon)": f"{m['counterpart'].get('name')} ({m['counterpart'].get('channel')})",
            "3. Order reference (Buyurtma)": order,
            "4. Narrative (Voqealar bayoni)": m["objective"],
            "5. Legal basis (Huquqiy asos)": "18-modda — sifatli tovarni 10 kun ichida qaytarish huquqi (Iste'molchilar huquqlarini himoya qilish to'g'risidagi qonun, 2023).",
            "6. Counterparty policy (Karshi tomon siyosati)": "uzum-14 — marketplace tovarlari uchun 14 kunlik qaytarish oynasi.",
            "7. Evidence (Islotlar ro'yxati)": f"order_ref: {order}; screenshot: photo1",
            "8. Demand & deadline (Talab va muddat)": f"To'liq qaytarish {minv} so'm, 3 ish kuni ichida.",
        }
        try:
            path = build_dossier({"id": self.case_id, "mandate": m}, report,
                                 outdir=os.path.join(os.path.dirname(__file__), "outputs"))
            self._emit("dossier.ready", {"path": path, "completeness": 8})
        except Exception as e:  # R10 or I/O
            self._emit("dossier.ready", {"path": "", "completeness": 0, "error": str(e)})

    def _learn(self):
        D.upsert_pref(D.conn(self.db), "qisman_tolov", "no", provenance=f"from {self.case_id}")

    def _resolve(self, outcome, amount=None):
        self.state = "resolved" if "resolved" in outcome or "accepted" in outcome else "stopped"
        self._emit("case.resolved", {"outcome": outcome,
                                     **({"amount": amount} if amount is not None else {})})
        c = D.conn(self.db)
        c.execute("UPDATE cases SET status=?, closed_at=datetime('now'), outcome=? WHERE id=?",
                  (self.state, outcome, self.case_id))
        c.commit()
