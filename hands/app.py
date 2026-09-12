"""VAKIL Hands API — the only server. Local-only (D0-5).

Run:   make demo        (uvicorn app:app --host 0.0.0.0 --port 8000)
Spec:  contracts/03-miniapp-api.md
Face:  serves face/index.html at / (single-page mini app, no build step)

Demo mode (default): MockUzumGateway + ScriptedLLM -> the full negotiation runs
end-to-end offline. Set VAKIL_MODE=live to use the real Telethon gateway/LLM.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

HERE = os.path.dirname(__file__)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import db as D
from agent import CaseAgent
from gateway import MockUzumGateway
from llm import ScriptedLLM

DB = os.environ.get("WAKIL_DB", os.path.join(HERE, "wakil.db"))
D.init(DB)

# corpus: seeded legal sources (R09 gate)
_BRAIN = os.path.join(HERE, os.pardir, "brain")
if _BRAIN not in sys.path:
    sys.path.insert(0, _BRAIN)
from corpus import LegalCorpus
CORPUS = LegalCorpus(D.conn(DB))
CORPUS.seed_default()

MODE = os.environ.get("VAKIL_MODE", "demo")
FACE = os.path.join(HERE, os.pardir, "face", "index.html")
AGENTS: dict[str, CaseAgent] = {}

app = FastAPI(title="VAKIL Hands")


def _c():
    return D.conn(DB)


def _case_or_404(case_id: str):
    row = D.get_case(_c(), case_id)
    if not row:
        raise HTTPException(404, "case not found")
    return row


# -- face -----------------------------------------------------------------
@app.get("/", include_in_schema=False)
def face():
    return FileResponse(FACE)


@app.get("/health")
def health():
    c = _c()
    return {"ok": True, "mode": MODE,
            "cases": c.execute("SELECT COUNT(*) FROM cases").fetchone()[0],
            "events": c.execute("SELECT COUNT(*) FROM events").fetchone()[0]}


# -- cases --------------------------------------------------------------------
class CaseIn(BaseModel):
    mandate: dict


def _new_gateway():
    if MODE == "live":
        from gateway import RealTelegramGateway  # needs a logged-in session
        raise RuntimeError("VAKIL_MODE=live requires a wired Telethon session (AI3). Use demo mode.")
    return MockUzumGateway(branch="deny")


def _new_llm():
    if MODE == "live":
        from llm import RealLLM
        return RealLLM(api_key=os.environ.get("LLM_API_KEY", ""))
    return ScriptedLLM()


@app.post("/case")
async def create_case(body: CaseIn):
    from guard_bridge import validate_mandate
    m = body.mandate
    c = _c()
    case_id = m.get("case_ref")
    if not case_id or D.get_case(c, case_id):
        case_id = D.next_case_id(c)
    m["case_ref"] = case_id
    m.setdefault("created_at_ts", __import__("time").time())
    errs = validate_mandate(m)
    if errs:
        raise HTTPException(422, {"errors": errs})
    D.create_case(c, case_id, json.dumps(m, ensure_ascii=False))
    D.add_event(c, case_id, "case.created", {"mandate": m})
    # start the agent (demo: auto-runs the negotiation)
    agent = CaseAgent(DB, case_id, m, _new_gateway(), _new_llm(), CORPUS)
    AGENTS[case_id] = agent
    asyncio.create_task(agent.run())
    return {"case_id": case_id, "mode": MODE}


@app.get("/case/{case_id}")
def get_case(case_id: str):
    row = _case_or_404(case_id)
    c = _c()
    events = D.events_since(c, case_id, 0, limit=50)
    esc = max((e["id"] for e in events if e["type"] == "guard.escalation"), default=0)
    dec = max((e["id"] for e in events if e["type"] == "user.decision"), default=0)
    return {"id": case_id, "status": row["status"], "mode": MODE,
            "mandate": json.loads(row["mandate_json"]), "timeline": events,
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
    agent = AGENTS.get(case_id)
    if agent:
        agent.on_decision(body.option)  # resumes the paused loop
    else:
        D.add_event(_c(), case_id, "user.decision", {"option": body.option})
    return {"accepted": True}


@app.get("/case/{case_id}/dossier")
def dossier(case_id: str):
    _case_or_404(case_id)
    path = os.path.join(HERE, "outputs", f"dossier-{case_id}.docx")
    if not os.path.exists(path):
        raise HTTPException(404, "dossier not ready yet")
    return FileResponse(path, filename=f"dossier-{case_id}.docx",
                         media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")


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
    for cid, a in list(AGENTS.items()):
        a.on_decision("stop")  # stop any running loop
    return {"wiped": True, "tables": D.wipe_all(_c())}
