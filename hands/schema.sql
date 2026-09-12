-- wakil local schema (SQLite). The booth laptop is the ONLY server (D0-5).
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  phone TEXT UNIQUE NOT NULL,
  telegram_id INTEGER,
  session_path TEXT NOT NULL,          -- chmod 600, gitignored
  two_fa_enforced INTEGER NOT NULL DEFAULT 0,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS cases (
  id TEXT PRIMARY KEY,                 -- M-0001
  user_id INTEGER REFERENCES users(id),
  mandate_json TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open', -- open|negotiating|escalated|resolved|stopped|timeboxed
  started_at TEXT DEFAULT (datetime('now')),
  closed_at TEXT,
  outcome TEXT
);

CREATE TABLE IF NOT EXISTS events (     -- Case Bus (contracts/02); polling cursor = id
  id INTEGER PRIMARY KEY,
  case_id TEXT NOT NULL REFERENCES cases(id),
  type TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS message_log (
  id INTEGER PRIMARY KEY,
  case_id TEXT,
  direction TEXT NOT NULL,             -- in|out
  dialog TEXT,
  text TEXT,
  tg_msg_id INTEGER,
  guard_rule TEXT,
  guard_verdict TEXT,                  -- PASS|REWRITE|ESCALATED|BLOCK
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS prefs (      -- learned, typed, provenance-tagged
  key TEXT PRIMARY KEY,
  value_json TEXT NOT NULL,
  provenance TEXT,                     -- e.g. "from M-0007"
  updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS legal_corpus (
  ref TEXT PRIMARY KEY,
  kind TEXT NOT NULL DEFAULT 'law',
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  source_url TEXT NOT NULL,
  fetched_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dossiers (
  id INTEGER PRIMARY KEY,
  case_id TEXT NOT NULL,
  path TEXT NOT NULL,
  completeness INTEGER NOT NULL,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS verifications (
  id INTEGER PRIMARY KEY,
  case_id TEXT,
  expected_json TEXT,
  observed_json TEXT,
  verdict TEXT,                        -- confirmed|mismatch|unreadable
  screenshot_path TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS guardians (  -- family read-only links
  id INTEGER PRIMARY KEY,
  case_id TEXT NOT NULL,
  token TEXT UNIQUE NOT NULL,
  read_only INTEGER NOT NULL DEFAULT 1,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS watchers (   -- price radar
  id INTEGER PRIMARY KEY,
  case_id TEXT,
  keyword TEXT NOT NULL,
  scope TEXT NOT NULL DEFAULT 'global',
  cadence_sec INTEGER NOT NULL DEFAULT 120,
  last_seen_msg_id INTEGER,
  active INTEGER NOT NULL DEFAULT 1
);
