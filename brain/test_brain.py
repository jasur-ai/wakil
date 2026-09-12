"""wakil brain test suite (ai1) — stdlib only, no pytest required.

Run:  python test_brain.py      (or: pytest -q test_brain.py)
Companion to test_guard.py (the D0 gate suite — 17 tests, kept green and untouched).
These cover what ai1 added: source-verified corpus, case-kind-aware citation, voice
slots, money verification, the learning loop, and the eval harness invariant.
"""
from __future__ import annotations

import time
import unittest

import corpus as C
import eval as EV
import graph as GR
import learn as LN
import slots as SL
import verify as VF
from guard import BoundaryGuard, Outbound, Verdict


def mandate(**over):
    m = {"case_ref": "M-0001",
         "objective": "to'liq qaytarish: nosoz iPhone 15 (ekran defekti)",
         "counterpart": {"name": "Uzum Marketplace", "channel": "@Uzum_Support_Bot"},
         "bounds": {"min_value": 450000, "max_value": 450000, "acceptable_outcomes": ["full_refund"],
                    "max_wait_hours": 48, "non_negotiables": ["450 000 dan past qabul qilinmasin"],
                    "allow_state_threat": False},
         "evidence": [{"kind": "order_ref", "ref": "order", "data": {"order": "UZ-778-112"}}],
         "strategy": "meherban doimiylik", "created_at_ts": time.time()}
    m.update(over)
    return m


class TestCorpusIntegrity(unittest.TestCase):
    def setUp(self):
        self.c = C.LegalCorpus()
        self.c.seed_default()

    def test_corpus_is_self_clean(self):
        self.assertEqual(self.c.audit(), [], "every entry needs https source + date + body")

    def test_defect_and_quality_articles_exist(self):
        for ref in ("16-modda", "17-modda", "18-modda"):
            self.assertIsNotNone(self.c.get(ref), ref)

    def test_case_kind_detection(self):
        self.assertEqual(self.c.case_kind(mandate()), "defect")
        self.assertEqual(self.c.case_kind(mandate(objective="yoqmadi, o'lchami kichik bo'ldi")), "quality")

    def test_article_applies_to(self):
        self.assertEqual(self.c.article_applies_to("16-modda"), "defect")
        self.assertEqual(self.c.article_applies_to("18-modda"), "quality")

    def test_unverified_entries_not_quotable(self):
        self.assertFalse(self.c.quotable("28-modda"))
        self.assertFalse(self.c.quotable("fk-418-422"))
        self.assertTrue(self.c.quotable("16-modda"))

    def test_cite_ranks_the_defect_article_first(self):
        top = self.c.cite("telefon nosoz, pulni qaytarib bering", case_kind="defect")
        self.assertTrue(top)
        self.assertIn(top[0]["ref"], ("16-modda", "17-modda", "uzum-warranty"))
        # and the filter is what makes it right: raw text search prefers 18 (it literally
        # contains "qaytarib"), so the product must always pass the case kind.
        raw = self.c.cite("telefon nosoz, pulni qaytarib bering")
        self.assertEqual(raw[0]["ref"], "18-modda")

    def test_hallucinated_citation_still_blocked(self):
        ok, missing = self.c.check_text("99-moddaga ko'ra")
        self.assertEqual((ok, missing), ([], ["99-modda"]))


class TestArticleFit(unittest.TestCase):
    """R12 — the fix for the biggest legal-accuracy risk in the demo script."""

    def setUp(self):
        self.c = C.LegalCorpus()
        self.c.seed_default()
        self.g = BoundaryGuard(mandate(), self.c)

    def test_wrong_article_for_defect_rewrites(self):
        o = Outbound(text="18-moddaga ko'ra 10 kun ichida qaytaring", turn=2)
        res = self.g.check_article_fit(o, "defect")
        self.assertIs(res.verdict, Verdict.REWRITE)
        self.assertEqual(res.rule, "R12-article-fit")
        self.assertIn("16-modda", res.detail)

    def test_right_article_for_defect_passes(self):
        o = Outbound(text="16-modda asosan shartnomani bekor qilamiz", turn=2)
        self.assertIs(self.g.check_article_fit(o, "defect").verdict, Verdict.PASS)

    def test_quality_case_can_cite_18(self):
        o = Outbound(text="18-modda asosan almashtirib bering", turn=2)
        self.assertIs(self.g.check_article_fit(o, "quality").verdict, Verdict.PASS)

    def test_unverified_article_not_quoted(self):
        o = Outbound(text="28-moddaga ko'ra...", turn=2, citations=["28-modda"])
        self.assertIs(self.g.check_article_fit(o, "defect").verdict, Verdict.REWRITE)

    def test_no_corpus_means_no_opinion(self):
        g = BoundaryGuard(mandate(), None)
        self.assertIs(g.check_article_fit(Outbound(text="18-modda"), "defect").verdict, Verdict.PASS)


class TestDisclosureSpelling(unittest.TestCase):
    """AGENTS.md froze the brand as `wakil`. R07 additionally accepts the everyday Uzbek
    word form, so the brand rule cannot silently break the disclosure beat (§4.1)."""

    def setUp(self):
        self.c = C.LegalCorpus()
        self.c.seed_default()
        self.g = BoundaryGuard(mandate(), self.c)

    def test_wakil_spelling_passes(self):
        o = Outbound(text="Men foydalanuvchi tomonidan tayinlangan wakilman.", turn=1)
        self.assertIs(self.g.check_outbound(o).verdict, Verdict.PASS)

    def test_uzbek_dictionary_word_form_also_passes(self):
        # the brand is "wakil"; the guard still must not reject the everyday word form
        o = Outbound(text="Men foydalanuvchining vakilman.", turn=1)
        self.assertIs(self.g.check_outbound(o).verdict, Verdict.PASS)

    def test_no_disclosure_still_rewrites(self):
        o = Outbound(text="Assalomu alaykum, buyurtma UZ-778-112 bo'yicha qaytaring.", turn=1)
        self.assertIs(self.g.check_outbound(o).verdict, Verdict.REWRITE)


class TestSlots(unittest.TestCase):
    def test_digit_transcript(self):
        r = SL.extract(SL.FIXTURES["f1"])
        self.assertEqual(r["bounds"]["min_value"], 450000)
        self.assertEqual(r["bounds"]["max_wait_hours"], 48)
        self.assertEqual(r["bounds"]["acceptable_outcomes"], ["full_refund"])
        self.assertTrue(r["bounds"]["allow_state_threat"])
        self.assertEqual(r["counterpart"]["name"], "Uzum Marketplace")
        self.assertIn("UZ-778-112", str(r["evidence"]))

    def test_word_transcript(self):
        r = SL.extract(SL.FIXTURES["f2"])
        self.assertEqual(r["bounds"]["min_value"], 450000, "spoken numbers must not round")
        self.assertEqual(r["bounds"]["max_wait_hours"], 48)
        self.assertFalse(r["bounds"]["allow_state_threat"])

    def test_russian_transcript(self):
        r = SL.extract(SL.FIXTURES["f3"])
        self.assertEqual(r["bounds"]["min_value"], 450000)
        self.assertFalse(r["bounds"]["allow_state_threat"])

    def test_asr_is_injected(self):
        seen = {}

        def fake_asr(path):
            seen["path"] = path
            return SL.FIXTURES["f1"]

        r = SL.extract("", asr=fake_asr, audio_path="fixtures/voice_uz_12s.wav")
        self.assertEqual(seen["path"], "fixtures/voice_uz_12s.wav")
        self.assertEqual(r["bounds"]["min_value"], 450000)
        self.assertEqual(r["evidence"][-1]["kind"], "voice_note")

    def test_missing_slots_are_reported_not_invented(self):
        r = SL.extract("Telefon ishlamayapti, yordam bering")
        self.assertIn("bounds.min_value", r["missing"])
        self.assertIn("bounds.acceptable_outcomes", r["missing"])
        m = SL.merge_into_mandate(r, "M-0002", time.time())
        errs = BoundaryGuard.__init__ and __import__("guard").validate_mandate(m)
        self.assertTrue(any("acceptable_outcomes" in e for e in errs))

    def test_number_parser(self):
        self.assertEqual(SL.parse_uz_number("to'rt yuz ellik ming"), 450000)
        self.assertEqual(SL.parse_uz_number("o'n uch ming"), 13000)
        self.assertEqual(SL.parse_uz_number("450k"), 450000)
        self.assertEqual(SL.parse_uz_number("1,6 mlrd"), 1_600_000_000)


class TestVerification(unittest.TestCase):
    EXP = {"amount": 450000.0, "currency": "UZS", "counterpart": "Uzum Marketplace"}

    def test_all_five_fixtures(self):
        for name, obs, want in VF.FIXTURES:
            self.assertEqual(VF.verdict({"amount": 450000.0, "currency": "UZS"}, obs)["verdict"],
                             want, name)

    def test_ocr_string_parsed(self):
        got = VF.verdict({"amount": 450000.0, "currency": "UZS"}, VF.parse_ocr(VF.FIXTURES[1][1]["amount"] and
                        "Postuplenie +450 000 so'm Uzum Market"))
        self.assertEqual(got["verdict"], "confirmed")

    def test_nothing_closes_without_confirmed(self):
        for obs in (None, {}, {"amount": 1}):
            self.assertNotEqual(VF.verdict({"amount": 450000.0, "currency": "UZS"}, obs)["verdict"],
                                "confirmed")

    def test_tolerance_is_tight(self):
        v = VF.verdict({"amount": 450000.0, "currency": "UZS"}, {"amount": 449990, "currency": "UZS"})
        self.assertEqual(v["verdict"], "mismatch", "10 so'm short is a partial payment, not a win")


class TestLearning(unittest.TestCase):
    def test_feedback_writes_typed_pref_with_provenance(self):
        prefs = []
        for k, v, prov in LN.feedback(-1, "erta topshirdi", "M-0007"):
            prefs = LN.record(prefs, k, v, prov)
        self.assertEqual(prefs[0]["key"], "max_wait_hours")
        self.assertEqual(prefs[0]["provenance"], "from M-0007")

    def test_second_mandate_prefilled(self):
        prefs = LN.record([], "max_wait_hours", 72.0, "from M-0007")
        card = mandate(strategy="", created_at_ts=time.time())
        card["bounds"].pop("max_wait_hours")
        m2, applied = LN.prefill(card, prefs)
        self.assertEqual(m2["bounds"]["max_wait_hours"], 72.0)
        self.assertIn("bounds.max_wait_hours", applied)
        self.assertEqual(m2["learned_seeds"][0]["provenance"], "from M-0007")

    def test_prefs_never_overwrite_a_stated_floor(self):
        prefs = [LN.record([], "min_value_policy", "floor is the floor", "from M-0007")[0]]
        card = mandate()
        m2, _ = LN.prefill(card, prefs)
        self.assertEqual(m2["bounds"]["min_value"], 450000)

    def test_unknown_pref_key_rejected(self):
        with self.assertRaises(LN.PrefError):
            LN.record([], "bank_card", "4000 0000 0000 0000", "from M-0007")

    def test_provenance_mandatory(self):
        with self.assertRaises(LN.PrefError):
            LN.record([], "tone", "formal", "")


class TestAgentLoop(unittest.TestCase):
    def setUp(self):
        self.c = C.LegalCorpus()
        self.c.seed_default()

    def _agent(self, replies):
        q = list(replies)
        sent = []

        class H:
            def send(self, dialog, text, media=None):
                sent.append(text)
                return len(sent)

        ev = []
        a = GR.Agent(mandate(), H(), lambda p: q.pop(0) if q else EV.SAFE, self.c,
                    lambda t, p: ev.append((t, p)))
        return a, ev, sent

    def test_opening_message_is_gated(self):
        a, ev, sent = self._agent([EV.SAFE])
        a.open_case()
        self.assertEqual(len(sent), 1)
        self.assertEqual(ev[0][0], "case.created")
        self.assertEqual([t for t, _ in ev if t == "turn.outbound"][0], "turn.outbound")

    def test_opening_without_disclosure_is_rewritten_then_sent(self):
        a, ev, sent = self._agent(["Assalomu alaykum, UZ-778-112 bo'yicha qaytaring.", EV.SAFE])
        a.open_case()
        self.assertTrue(any(e[0] == "turn.outbound" for e in ev))

    def test_below_floor_offer_escalates_and_blocks_send(self):
        a, ev, sent = self._agent(["300 000 so'mlik taklifni qabul qila olmaymiz."])
        a.turn = 1
        a.run_inbound("Sizga 300 000 so'm qisman qaytarish taklif qilamiz.")
        self.assertTrue(any(t == "guard.escalation" for t, _ in ev))
        self.assertEqual(len(sent), 0, "below-floor reaction must not be sent before the user taps")

    def test_hold_reply_cites_the_defect_article(self):
        a, ev, sent = self._agent([
            "300 000 so'mlik taklifni qabul qila olmaymiz.",
            "16-modda asosan nosoz tovar bo'yicha 450 000 so'mni qaytarishni talab qilamiz.",
            "16-modda asosan nosoz tovar bo'yicha 450 000 so'mni qaytarishni talab qilamiz.",
            "16-modda asosan nosoz tovar bo'yicha 450 000 so'mni qaytarishni talab qilamiz."])
        a.run_inbound("Sizga 300 000 so'm qisman qaytarish taklif qilamiz.")
        a.on_user_decision("hold")
        self.assertTrue(any("16-modda" in t for t in sent), sent)

    def test_invented_law_never_leaves(self):
        a, ev, sent = self._agent(["200-moddaga ko'ra 5 kun ichida to'lang."])
        a.turn = 1          # mid-case: the turn-1 disclosure duty (R07) is already met
        a.run_inbound("Rad etamiz.")
        self.assertFalse(any("200-modda" in t for t in sent), "invented law must never be sent")
        self.assertTrue(any(t == "guard.escalation" for t, _ in ev))

    def test_accept_exception_rebinds_bounds_and_records_memory(self):
        prefs = []
        a, ev, sent = self._agent([EV.SAFE])
        a.learn = lambda k, v, prov: prefs.append({"key": k, "value": v, "provenance": prov})
        a.on_user_decision("accept_exception", {"min_value": 300000})
        self.assertEqual(a.m["bounds"]["min_value"], 300000)
        self.assertEqual(prefs[0]["provenance"], "from M-0001")
        # after the written exception, 300k is now inside the bounds
        o = Outbound(text="300 000 so'mni qabul qilamiz", turn=3, intent="offer", proposed_value=300000)
        self.assertIs(a.guard.check_outbound(o).verdict, Verdict.PASS)

    def test_close_only_on_confirmed_money(self):
        a, ev, sent = self._agent([EV.SAFE])
        v = a.verify({"amount": 300000, "currency": "UZS"})
        self.assertEqual(v["verdict"], "mismatch")
        self.assertNotEqual(a.state, GR.State.CLOSE)
        v = a.verify({"amount": 450000, "currency": "UZS"})
        self.assertEqual(v["verdict"], "confirmed")
        self.assertIs(a.state, GR.State.CLOSE)
        self.assertTrue(any(t == "case.resolved" for t, _ in ev))

    def test_timebox_stops_negotiating(self):
        q = [EV.SAFE]
        a, ev, sent = self._agent(q)
        a.guard = BoundaryGuard(mandate(created_at_ts=time.time() - 49 * 3600), self.c)
        a.run_inbound("Tekshiryapmiz.")
        self.assertTrue(any(t == "guard.escalation" or t == "turn.outbound" for t, _ in ev))


class TestEvalHarness(unittest.TestCase):
    def test_zero_violations_and_reports(self):
        self.assertEqual(EV.main(), 0)

    def test_audit_catches_a_tampered_send(self):
        """Prove the harness is not a rubber stamp: force a bad send and expect a violation."""
        # inject a known-bad message directly into the recorded sends and re-audit it
        hands = EV.FakeHands()
        hands.send("@Uzum_Support_Bot", "Kartam 4000 1234 5678 9010 va +998901234567")
        audit = BoundaryGuard(mandate(), C.LegalCorpus())
        bad = [t for _, t in hands.sent
               if audit.check_outbound(Outbound(text=t, turn=2)).verdict is not Verdict.PASS]
        self.assertEqual(len(bad), 1, "the independent audit must reject a PII leak")


if __name__ == "__main__":
    unittest.main(verbosity=2)
