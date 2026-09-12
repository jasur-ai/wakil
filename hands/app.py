"""wakil Hands API — the only server. Local-only (D0-5).

Run:   make demo        (uvicorn app:app --host 0.0.0.0 --port 8000)
Spec:  contracts/03-miniapp-api.md
Face:  serves face/index.html at / (single-page mini app, no build step)
"""
from __future__ import annotations

import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

import db as D

DB = os.environ.get("WAKIL_DB", os.path.join(os.path.dirname(__file__), "wakil.db"))
D.init(DB)

FACE = os.path.join(os.path.dirname(__file__), os.pardir, "face", "index.html")

app = FastAPI(title="wakil Hands")


def _c():
    return D.conn(DB)


def _case_or_404(case_id: str):
    row = D.get_case(_c(), case_id)
    if not row:
        raise HTTPException(404, "case not found")
    return row


# -- face -------------------------------------------------------------------
@app.get("/", include_in_schema=False)
def face():
    return FileResponse(FACE)


@app.get("/health")
def health():
    c = _c()
    return {"ok": True,
            "cases": c.execute("SELECT COUNT(*) FROM cases").fetchone()[0],
            "events": c.execute("SELECT COUNT(*) FROM events").fetchone()[0]}


# -- cases --------------------------------------------------------------------
class CaseIn(BaseModel):
    mandate: dict


@app.post("/case")
def create_case(body: CaseIn):
    from guard_bridge import validate_mandate  # thin import of brain/guard.py
    errs = validate_mandate(body.mandate)
    if errs:
        raise HTTPException(422, {"errors": errs})
    c = _c()
    case_id = body.mandate.get("case_ref") or D.next_case_id(c)
    D.create_case(c, case_id, json.dumps(body.mandate, ensure_ascii=False))
    D.add_event(c, case_id, "case.created", {"mandate": body.mandate})
    return {"case_id": case_id}


@app.get("/case/{case_id}")
def get_case(case_id: str):
    row = _case_or_404(case_id)
    c = _c()
    events = D.events_since(c, case_id, 0, limit=50)
    esc = max((e["id"] for e in events if e["type"] == "guard.escalation"), default=0)
    dec = max((e["id"] for e in events if e["type"] == "user.decision"), default=0)
    return {"id": case_id,
            "status": row["status"],
            "mandate": json.loads(row["mandate_json"]),
            "timeline": events,
            "pending_decision": esc > dec}


@app.get("/case/{case_id}/events")
def events(case_id: str, since: int = 0):
    _case_or_404(case_id)
    return D.events_since(_c(), case_id, since)


class Decision(BaseModel):
    option: str  # accept_exception | hold | stop


@app.post("/case/{case_id}/decision", status_code=202)
def decision(case_id: str, body: Decision):
    if body.option not in ("accept_exception", "hold", "stop"):
        raise HTTPException(422, "option must be accept_exception|hold|stop")
    _case_or_404(case_id)
    D.add_event(_c(), case_id, "user.decision", {"option": body.option})
    return {"accepted": True}


# -- prefs ---------------------------------------------------------------------
class Pref(BaseModel):
    key: str
    value: object = None
    provenance: str = ""


@app.get("/prefs")
def prefs():
    return D.get_prefs(_c())


@app.post("/prefs")
def set_pref(body: Pref):
    D.upsert_pref(_c(), body.key, body.value, body.provenance)
    return {"ok": True}


@app.delete("/prefs/{key}")
def del_pref(key: str):
    D.delete_pref(_c(), key)
    return {"ok": True}


# -- search & watch ----------------------------------------------------------------
@app.get("/search")
def search(k: str = ""):
    # Real search needs the user session (Contract 01). Demo mode returns fixtures.
    import search as S
    return S.demo_search(k)


class Watch(BaseModel):
    keyword: str
    scope: str = "global"


@app.post("/watch")
def watch(body: Watch):
    c = _c()
    cur = c.execute("INSERT INTO watchers (keyword, scope) VALUES (?,?)",
                    (body.keyword, body.scope))
    c.commit()
    return {"watcher_id": cur.lastrowid}


# -- guardian & wipe ------------------------------------------------------------------
@app.get("/case/{case_id}/guardian")
def guardian(case_id: str, token: str = ""):
    c = _c()
    row = c.execute("SELECT * FROM guardians WHERE case_id=? AND token=?",
                    (case_id, token)).fetchone()
    if not row:
        raise HTTPException(404, "invalid guardian token")
    return {"id": case_id, "read_only": True,
            "timeline": D.events_since(c, case_id, 0, limit=50)}


@app.post("/wipe")
def wipe():
    return {"wiped": True, "tables": D.wipe_all(_c())}
