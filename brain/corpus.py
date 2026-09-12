"""wakil LegalCorpus — the ONLY source of law the agent may cite.

R09 (guard) resolves every "N-modda" reference against this corpus;
an unresolved citation is a BLOCK + incident. Every entry carries
source_url + fetched_at (audit trail in the pitch and the dossier).

Stdlib only (sqlite3). Run: python corpus.py  → seeds + self-test.
"""
from __future__ import annotations

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

    def seed_default(self, fetched_at: str = "2026-09-12"):
        """Known-good seed (researched; sources in docs/v2-winning-edition.md §sources)."""
        self.upsert("18-modda",
                    "Iste'molchilar huquqlarini himoya qilish to'g'risidagi qonun (2023), 18-modda",
                    "Sifatli, ovqat-bozoxona mahsulotiga oid bo'lmagan tovar 10 kun ichida qaytarish yoki "
                    "almashtirish huquqi (narx pasayganda farq hisoblanadi).",
                    "https://www.kun.uz/uz/article/2023-05-02-iste-molchilar-huquqlari-qonuni-matn", fetched_at)
        self.upsert("uzum-14",
                    "Uzum Marketplace qaytarish siyosati",
                    "Marketplace tovarlari uchun 14 kunlik qaytarish/maydon qilish oynasi; "
                    "qaytarish muddati 5–14 ish kuni.",
                    "https://101digital.uz", fetched_at, kind="policy")
        self.upsert("1159",
                    "Iste'molchilar huquqlarini himoya qilish qo'mitasi — rasmiy kanallar",
                    "Davlat qo'mitasi ishonch telefoni 1159; Telegram bot: @consumergovuz_bot; "
                    "shikoyat daftari elektron tarzda.",
                    "https://www.davlat.uz", fetched_at, kind="agency")

    # -- read -------------------------------------------------------------
    def get(self, ref: str):
        row = self.db.execute("SELECT * FROM legal_corpus WHERE ref=?", (ref,)).fetchone()
        return dict(row) if row else None

    def all(self):
        return [dict(r) for r in self.db.execute("SELECT * FROM legal_corpus ORDER BY ref")]

    def find_refs(self, text: str):
        from guard import find_article_refs  # local import: corpus may be used standalone
        return find_article_refs(text)

    def check_text(self, text: str) -> tuple[list[str], list[str]]:
        """(resolved, missing) — missing = hallucinated citations."""
        resolved, missing = [], []
        for ref in self.find_refs(text):
            (resolved if self.get(ref) else missing).append(ref)
        return resolved, missing


if __name__ == "__main__":
    c = LegalCorpus()
    c.seed_default()
    print("corpus entries:", [e["ref"] for e in c.all()])
    ok, bad = c.check_text("18-moddaga ko'ra 10 kunlik huquqim bor, 99-moddani esa bilmayman")
    print("resolved:", ok, "missing:", bad)
    assert ok == ["18-modda"] and bad == ["99-modda"]
    print("corpus self-test OK")
