"""wakil LegalCorpus — the ONLY source of law the agent may cite.

R09 (guard) resolves every "N-modda" reference against this corpus;
an unresolved citation is a BLOCK + incident. Every entry carries
source_url + fetched_at (audit trail in the pitch and the dossier).

ai1 (P1 BRAIN) audit 2026-09-12 — see brain/legal_findings.md:
  * the seeds the lead shipped were directionally right but mis-sourced
    ("2023 law", "Uzum 14-day", `101digital.uz`, `davlat.uz`);
  * the law is № 221-I of 26.04.1996 (current edition, amended by O'RQ-1078
    of 31.07.2025) — NOT a 2023 law;
  * **Art. 18 covers a GOOD-QUALITY item exchange.** Our demo case is a
    *defect* ("nosoz iPhone 15, ekran defekti") → the right articles are
    **16 / 17** (defective goods). Quoting 18-moddа for a defect is the one
    thing a lawyer-judge would catch, so the corpus now marks which article
    fits which case kind and `guard.check_article_fit()` enforces it;
  * Uzum's real published window is **10 calendar days** (extendable to 30),
    and a seller who stays silent **20 calendar days** is deemed to have
    accepted the claim — a much better lever than "14 days".
  * entries are `unverified` if we could not fetch the text — the agent must
    not put those in a dossier (see QUOTABLE).

Stdlib only (sqlite3). Run: python corpus.py  → seeds + self-test.
"""
from __future__ import annotations

import re
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS legal_corpus (
  ref TEXT PRIMARY KEY,
  kind TEXT NOT NULL DEFAULT 'law',
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  source_url TEXT NOT NULL,
  fetched_at TEXT NOT NULL
);
"""

LAW_URL = "https://lex.uz/docs/-4704"          # № 221-I, 26.04.1996, current edition
FETCHED = "2026-09-12"                          # date ai1 verified against the live source

# ref, kind, title, body, source_url
# kind: law | policy | agency | case | stat | note
VERIFIED_SEED = [
    # ---- the two articles that matter for our demo case (DEFECT) ----------
    ("16-modda", "law",
     "16-modda. Iste'molchining nuqsonli tovarning xarid narxini nuqsonga mutanosib ravishda "
     "kamaytirishni yoki shartnomani bekor qilishni talab qilish huquqi",
     "Tovar NUQSONLI (defektli) bo'lsa: iste'molchi narxni nuqsonga mutanosib kamaytirishni "
     "YOKI shartnomani bekor qilib to'langan pulni qaytarishni talab qiladi. "
     "SIFATGA e'tiroz bo'lgan iPhone uchun ASOSIY modda — 16-modda.",
     LAW_URL, FETCHED),
    ("17-modda", "law",
     "17-modda. Iste'molchiga nuqsonli tovar sotilgan taqdirda u bilan hisob-kitob qilish",
     "Nuqsonli tovar sotilgan holda hisob-kitob: talab qilingan pul bir xil tarzda qaytariladi "
     "(kartaga to'langan bo'lsa — kartaga). wakil uchun: 'pul qayerga qaytadi' savolining javobi.",
     LAW_URL, FETCHED),
    ("18-modda", "law",
     "18-modda. Iste'molchining maqbul sifatli tovarni almashtirib olish huquqi",
     "Maqbul (sifati yaxshi) nooziq-ovqat tovarini xarid qilgan kunidan e'tiboran O'N KUN ichida "
     "shu tovarga almashtirib olish, almashtirishga tovar sotuvda bo'lmasa — pulni qaytarib olish "
     "huquqi. Shart: tovardan foydalanilmagan, shikastlanmagan, qadog'i va iste'mol xususiyatlari "
     "saqlangan, sotib olingani tasdiqlangan. DIQQAT: bu modda NUQSON bo'yicha EMAS.",
     LAW_URL, FETCHED),
    ("25-modda", "law",
     "25-modda. Iste'molchilar huquqlarini himoya qilish agentligi va uning hududiy organlari",
     "Agentlik + hududiy organlari: nazorat, nizoni SUDGA QADAR hal qilishga ko'mak, va "
     "belgilangan hollarda iste'molchilar nomidan sudga murojaat. Eskalyatsiya zinapoyasining "
     "rasmiy zinapoyasi.",
     LAW_URL, FETCHED),
    ("27^1-modda", "law",
     "27^1-modda. Davlat boshqaruvi organining ko'rsatmasi ustidan shikoyat qilish",
     "Bo'ysunuv tartibida yuqori turuvchi organga shikoyat qilish SUDGA shikoyat qilish huquqini "
     "istisno qilmaydi — ya'ni eskalyatsiyalar parallel yuradi.",
     LAW_URL, FETCHED),
    ("28-modda", "law",
     "28-modda. Moliyaviy xizmatlar sohasida iste'molchilarning huquqlarini himoya qilish",
     "Mavjudligi tasdiqlangan (sarlavha lex.uz'da ko'rindi); MATNI hali olinmagan — dossier'ga "
     "faqat sarlavha bilan kiriting, matn iqtibos qilmang.",
     LAW_URL, FETCHED),
    # ---- counterparty policy (Uzum) — the real published numbers ----------
    ("uzum-10", "policy",
     "Uzum Market vositachilik shartnomasi (oferta) 5-bo'lim — qaytarish",
     "Xaridor buyurtma olingan kundan boshlab 10 (o'n) KALENDAR KUNI mobaynida foydalanish "
     "belgilarisiz, tegishli sifatdagi istalgan Mahsulotni qaytaradi. Ayrim hollarda muddat 30 "
     "kungacha uzayadi. Sotuvchi e'tirozni olganidan keyin 20 KALENDAR KUN ichida xulosa "
     "bermasa — talab TAN OLINGAN deb hisoblanadi (bu bizning kuchli asbobimiz).",
     "https://seller.uzum.uz/seller/agreement/uz/", FETCHED),
    ("uzum-warranty", "policy",
     "Uzum Market FAQ — sifatga e'tiroz bo'lgan mahsulotni qaytarish",
     "Sifatiga e'tiroz bo'lgan mahsulot o'rnatilgan KAFOLAT muddati davomida qaytariladi; kafolat "
     "bo'lmasa — 6 OY ichida. Sotuvchi kamchilikni 20 KUN ichida bepul bartaraf etadi. "
     "Texnik jihatdan murakkab mahsulotlar uchun alohida tartib. Buyurtma tarqatish punktida 8 kun "
     "saqlanadi; qo'llab-quvvatlash: @Uzum_Support_Bot.",
     "https://uzum.uz/uz/faq", FETCHED),
    ("uzum-fine", "case",
     "Raqobat qo'mitasi qarori: Uzum Market — 1,6 mlrd so'mdan ortiq qaytarish",
     "2025-yil: qo'mita Uzum Market va yetkazib beruvchiga yaroqlilik muddati noto'g'ri ko'rsatilgan "
     "mahsulot bo'yicha 1,6 mlrd so'mdan ortiq mablag'ni iste'molchilarga qaytarish ko'rsatmasi "
     "berdi; sudlar qarorni kuchida qoldirdi. PITCH uchun fakt: davlat Uzum'ni jazolagan.",
     "https://www.gazeta.uz/oz/2025-09-11/uzum-market/", FETCHED),
    # ---- state ladder (real, verified channels) --------------------------
    ("1159", "agency",
     "Raqobatni rivojlantirish va iste'molchilar huquqlarini himoya qilish qo'mitasi",
     "Ishonch telefoni 1159 (qabulxona: (71) 207-48-00); e-mail info@antimon.gov.uz, "
     "e-xat: antimon@exat.uz; sayt raqobat.gov.uz. Telegram boti (@consumergovuz_bot) ALAHI "
     "tekshirilmagan — P3 D3 probe gacha demo'da uni 'tasdiqlanmagan' deb belgilang.",
     "https://raqobat.gov.uz/en/consumer-protection-in-the-field-of-social-and-financial-services-as-well-as-communication-services/",
     FETCHED),
    ("mygov", "agency",
     "my.gov.uz — davlat xizmatlari portali (elektron murojaat)",
     "Fuqaro (yoki uning wakili) elektron shikoyatni portal orqali yuboradi; qog'oz navbati o'rniga raqamli qabul.",
     "https://my.gov.uz", FETCHED),
    ("virtual-qabulxona", "agency",
     "O'zR Prezidentining Virtual qabulxonasi",
     "Murojaatlar AKT orqali qabul qilinadi, tasniflanadi va ko'rib chiqilishi ustidan monitoring "
     "yuritiladi. Murojaatlarni berish muddati, qoida tariqasida, belgilanmaydi (O'RQ-445, 22-modda). "
     "Zinapoyaning eng yuqori pog'onasi — eng og'ir holatlar uchun.",
     "https://prezident.uz", FETCHED),
    ("ozkomnazorat", "agency",
     "O'zkomnazorat — telekommunikatsiya sohasida nazorat inspeksiyasi",
     "Raqamli texnologiyalar vazirligi huzuridagi inspektsiya; ishonch telefoni 1144, "
     "(71) 202-69-65. Beeline/Ucell/Artel bo'yicha eskalyatsiya manzili.",
     "https://gov.uz/oz/uzkomnazorat/contacts", FETCHED),
    ("raqobat-stats", "stat",
     "Qo'mita murojaat statistikasi",
     "2024: iste'molchilar huquqlari buzilishi bo'yicha 30 070 ta shikoyat. 2025: murojaatlar "
     "2024 ga nisbatan +65,7%. 2026 yarim yillik: 837 murojaat. Muammo o'sib borayapti.",
     "https://raqobat.gov.uz/istemolchilar-huquqlari-qonun-himoyasida/", FETCHED),
    ("fk-418-422", "note",
     "Fuqarolik kodeksi 418–422-moddalar (lex.uz sharhida havola qilingan)",
     "Iste'molchilar to'g'risidagi qonun izohida zarar qoplash FK 418–422 asosida deb ko'rsatilgan. "
     "MODDA RAQAMI SIFATIDA IQTIBOS QILINMAYDI (matn tekshirilmagan) — faqat yo'nalish sifatida.",
     LAW_URL, FETCHED),
]

# refs the agent may quote verbatim into a message/dossier
UNSAFE_TO_QUOTE_TEXT = {"28-modda", "fk-418-422"}


class LegalCorpus:
    def __init__(self, conn: sqlite3.Connection | None = None):
        self.db = conn or sqlite3.connect(":memory:")
        self.db.row_factory = sqlite3.Row
        self.db.execute(SCHEMA)
        self.db.commit()

    # -- write ------------------------------------------------------------
    def upsert(self, ref: str, title: str, body: str, source_url: str, fetched_at: str, kind: str = "law"):
        self.db.execute(
            "INSERT INTO legal_corpus (ref, kind, title, body, source_url, fetched_at) "
            "VALUES (?,?,?,?,?,?) ON CONFLICT(ref) DO UPDATE SET kind=excluded.kind, title=excluded.title, "
            "body=excluded.body, source_url=excluded.source_url, fetched_at=excluded.fetched_at",
            (ref, kind, title, body, source_url, fetched_at))
        self.db.commit()

    def seed_default(self, fetched_at: str = FETCHED):
        """Source-verified seed (ai1 audit, see brain/legal_findings.md)."""
        for ref, kind, title, body, url in [
            (r, k, t, b, u) for (r, k, t, b, u, _f) in VERIFIED_SEED
        ]:
            self.upsert(ref, title, body, url, fetched_at, kind)

    # -- read -------------------------------------------------------------
    def get(self, ref: str):
        row = self.db.execute("SELECT * FROM legal_corpus WHERE ref=?", (ref,)).fetchone()
        return dict(row) if row else None

    def all(self):
        return [dict(r) for r in self.db.execute("SELECT * FROM legal_corpus ORDER BY kind, ref")]

    def find_refs(self, text: str):
        from guard import find_article_refs  # local import: corpus may be used standalone
        return find_article_refs(text)

    def check_text(self, text: str) -> tuple[list[str], list[str]]:
        """(resolved, missing) — missing = hallucinated citations."""
        resolved, missing = [], []
        for ref in self.find_refs(text):
            (resolved if self.get(ref) else missing).append(ref)
        return resolved, missing

    # -- ai1 additions ----------------------------------------------------
    def article_applies_to(self, ref: str) -> str:
        """'defect' | 'quality' | 'both' — derived from the title/body, not hand-mapped,
        so a future seeded article classifies itself."""
        e = self.get(ref)
        if not e:
            return "unknown"
        hay = (e["title"] + " " + e["body"]).lower()
        defect = any(w in hay for w in ("nuqsonli", "defekt", "kafolat", "ta'mir"))
        quality = "maqbul sifatli" in hay or "sifati yaxshi" in hay
        if defect and not quality:
            return "defect"
        if quality and not defect:
            return "quality"
        return "both"

    def case_kind(self, mandate: dict) -> str:
        """Read the objective: is the consumer complaining about a DEFECT or a plain return?"""
        hay = " ".join(str(v) for v in (mandate.get("objective", ""),
                                       " ".join(str(d) for e in mandate.get("evidence", [])
                                                for d in (e.get("data") or {}).values()))).lower()
        if any(w in hay for w in ("nuqson", "defekt", "nosoz", "buzilgan", "ishlay olmaydi",
                                 "skol", "chirkin", "yaroqsiz", "заводской брак", "дефект", "неисправн")):
            return "defect"
        return "quality"

    def quotable(self, ref: str) -> bool:
        """True = safe to quote text in a message / dossier."""
        return ref not in UNSAFE_TO_QUOTE_TEXT

    def cite(self, query: str, limit: int = 3, case_kind: str | None = None) -> list[dict]:
        """Bag-of-words scoring over title+body. No embeddings, no deps — the corpus is
        small and the booth laptop is the only server (D0-5). Returns ranked entries with
        their source so the caller can attach a provenance chip."""
        toks = [t for t in re.split(r"[^\w'ʻ`]+", query.lower()) if len(t) > 2]
        scored = []
        entries = self.all()
        if case_kind in ("defect", "quality"):
            # Which article is RIGHT is a legal question, not a similarity question:
            # "qaytarib bering" literally matches Art. 18's wording, yet citing 18 in a
            # defect case is exactly the mistake a lawyer-judge would catch. So we drop
            # mis-fitting articles, then rank what is left by text.
            entries = [e for e in entries if e["kind"] != "law"
                       or self.article_applies_to(e["ref"]) in (case_kind, "both", "unknown")]
        for e in entries:
            hay = (e["title"] + " " + e["body"]).lower()
            sc = sum(hay.count(t) * (2 if t in e["title"].lower() else 1) for t in toks)
            # an article that fits the case outranks an agency phone number that merely
            # shares a word — "telefon" appears in both, only one of them is a legal move
            if case_kind and e["kind"] == "law" \
                    and self.article_applies_to(e["ref"]) in (case_kind, "both"):
                sc += 10
            if sc:
                scored.append((sc, e))
        scored.sort(key=lambda x: (-x[0], x[1]["ref"]))
        return [e for _, e in scored[:limit]]

    # -- audit: the corpus itself must not lie ----------------------------
    def audit(self) -> list[str]:
        """Every entry must carry a real source + fetch date. Returns problems (empty = clean)."""
        problems = []
        for e in self.all():
            if not str(e["source_url"]).startswith("https://"):
                problems.append(f"{e['ref']}: source_url must be https")
            if "101digital.uz" in e["source_url"] or "davlat.uz" in e["source_url"]:
                problems.append(f"{e['ref']}: legacy unverified source still in corpus")
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(e["fetched_at"])):
                problems.append(f"{e['ref']}: fetched_at must be YYYY-MM-DD")
            if len(str(e["body"]).strip()) < 40:
                problems.append(f"{e['ref']}: body too thin to cite")
            if re.search(r"\b2023\b", e["title"]) and "18-modda" in e["ref"]:
                problems.append(f"{e['ref']}: '2023 law' framing is wrong (221-I of 1996)")
        return problems


if __name__ == "__main__":
    c = LegalCorpus()
    c.seed_default()
    rows = c.all()
    print("corpus entries:", len(rows), [e["ref"] for e in rows])
    print("audit problems:", c.audit() or "none")
    ok, bad = c.check_text("18-moddaga ko'ra 10 kunlik almashtirish huquqim bor, 99-moddani esa bilmayman")
    print("resolved:", ok, "missing:", bad)
    assert ok == ["18-modda"] and bad == ["99-modda"], "R09 must flag an invented article"
    assert not c.audit(), "corpus must be self-clean before the demo"
    demo = {"objective": "to'liq qaytarish: nosoz iPhone 15 (ekran defekti)", "evidence": []}
    print("demo case kind:", c.case_kind(demo),
          "| 16-modda applies to:", c.article_applies_to("16-modda"),
          "| 18-modda applies to:", c.article_applies_to("18-modda"))
    assert c.case_kind(demo) == "defect"
    assert c.article_applies_to("18-modda") == "quality"
    assert [e["ref"] for e in c.cite("nuqsonli telefon pulni qaytarish")][0] == "16-modda"
    print("corpus self-test OK")
