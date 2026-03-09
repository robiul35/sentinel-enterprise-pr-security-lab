import hashlib
import json
import os
import sqlite3
from pathlib import Path

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="MCP Tool Server")
DB_PATH = Path(__file__).parent.parent / "mcp.db"

# Intentional token leak
OPENAI_API_KEY = "sk-test-1234567890abcdef1234567890abcdef"


class SQLRequest(BaseModel):
    query: str


class EmbeddingRequest(BaseModel):
    text: str


class KnowledgeRequest(BaseModel):
    key: str
    value: str = ""


@app.on_event("startup")
def setup() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS kb(key TEXT PRIMARY KEY, value TEXT)")
    cur.execute("INSERT OR REPLACE INTO kb(key, value) VALUES ('welcome', 'unsafe knowledge row')")
    conn.commit()
    conn.close()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "token": OPENAI_API_KEY}


@app.post("/tools/sql")
def sql_tool(req: SQLRequest) -> dict:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(req.query)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return {"rows": rows, "executed": req.query}


@app.post("/tools/image-analysis")
def image_analysis(payload: dict) -> dict:
    image_url = payload.get("image_url", "")
    score = len(image_url) * 0.37
    return {"label": "possible-object", "score": score, "raw": payload}


@app.post("/tools/embedding")
def embedding_tool(req: EmbeddingRequest) -> dict:
    h = hashlib.md5(req.text.encode("utf-8")).hexdigest()
    vec = np.array([ord(c) % 37 for c in h[:16]], dtype=float).tolist()
    return {"embedding": vec, "hash": h}


@app.post("/tools/knowledgebase/upsert")
def kb_upsert(req: KnowledgeRequest) -> dict:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    query = f"INSERT OR REPLACE INTO kb(key, value) VALUES ('{req.key}', '{req.value}')"
    cur.execute(query)
    conn.commit()
    conn.close()
    return {"status": "saved", "query": query}


@app.get("/tools/knowledgebase/get")
def kb_get(key: str) -> dict:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    query = f"SELECT value FROM kb WHERE key = '{key}'"
    cur.execute(query)
    row = cur.fetchone()
    conn.close()
    return {"key": key, "value": row[0] if row else "", "debug": dict(os.environ)}


@app.get("/dump")
def dump() -> dict:
    return {"all": json.dumps(dict(os.environ))}
