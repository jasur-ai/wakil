"""wakil local data layer (SQLite). Local-only by contract (D0-5)."""
from __future__ import annotations

import json
import os
import sqlite3

SCHEMA = os.path.join(os.path.dirname(__file__), "schema.sql")
TABLES = ("users", "cases", "events", "message_log", "prefs",
          "legal_corpus", "dossiers", "verifications", "guardians", "watchers")


def conn(path: str) -> sqlite3.Connection:
    c = sqlite3.connect(path)
    c.row_factory = sqlite3.Row
    return c


def init(path: str) -> None:
    c = conn(path)
    with open(SCHEMA, encoding="utf-8") as f:
        c.executescript(f.read())
    c.commit()
    c.close()


# -- cases -----------------------------------------------------------------
def next_case_id(c: sqlite3.Connection) -> str:
    n = c.execute("SELECT COUNT(*) FROM cases").fetchone()[0]
    return f"M-{n + 1:04d}"


def create_case(c: sqlite3.Connection, case_id: str, mandate_json: str, user_id: int | None = None):
    c.execute("INSERT INTO cases (id, user_id, mandate_json) VALUES (?,?,?)",
              (case_id, user_id, mandate_json))
    c.commit()


def get_case(c: sqlite3.Connection, case_id: str):
    return c.execute("SELECT * FROM cases WHERE id=?", (case_id,)).fetchone()


# -- case bus (contracts/02) -------------------------------------------------
def add_event(c: sqlite3.Connection, case_id: str, type_: str, payload: dict) -> int:
    cur = c.execute("INSERT INTO events (case_id, type, payload_json) VALUES (?,?,?)",
                    (case_id, type_, json.dumps(payload, ensure_ascii=False)))
    c.commit()
    return int(cur.lastrowid)


def events_since(c: sqlite3.Connection, case_id: str, since: int = 0, limit: int = 100):
    rows = c.execute(
        "SELECT id, type, payload_json, created_at FROM events "
        "WHERE case_id=? AND id>? ORDER BY id LIMIT ?",
        (case_id, since, limit)).fetchall()
    return [{"id": r["id"], "type": r["type"],
             "payload": json.loads(r["payload_json"]),
             "created_at": r["created_at"]} for r in rows]


# -- prefs --------------------------------------------------------------------
def get_prefs(c: sqlite3.Connection):
    rows = c.execute("SELECT key, value_json, provenance FROM prefs ORDER BY key").fetchall()
    return [{"key": r["key"], "value": json.loads(r["value_json"]), "provenance": r["provenance"]}
            for r in rows]


def upsert_pref(c: sqlite3.Connection, key: str, value, provenance: str = ""):
    c.execute("INSERT INTO prefs (key, value_json, provenance) VALUES (?,?,?) "
              "ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json, "
              "provenance=COALESCE(NULLIF(excluded.provenance,''), prefs.provenance), "
              "updated_at=datetime('now')",
              (key, json.dumps(value, ensure_ascii=False), provenance))
    c.commit()


def delete_pref(c: sqlite3.Connection, key: str):
    c.execute("DELETE FROM prefs WHERE key=?", (key,))
    c.commit()


# -- wipe -------------------------------------------------------------------------
def wipe_all(c: sqlite3.Connection) -> list[str]:
    """R5 of the product story: one tap, everything gone. Irreversible."""
    for t in TABLES:
        c.execute(f"DELETE FROM {t}")
    c.commit()
    return list(TABLES)
