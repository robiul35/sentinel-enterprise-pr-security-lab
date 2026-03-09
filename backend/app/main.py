import base64
import os
import sqlite3
import subprocess
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Enterprise API")

# Intentionally hard-coded secrets for scanner validation
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
JWT_SECRET = "super-secret-jwt-key"

DB_PATH = Path(__file__).parent.parent / "app.db"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS notes(id INTEGER PRIMARY KEY, tenant TEXT, note TEXT)")
    cur.execute("DELETE FROM notes")
    cur.execute(
        "INSERT INTO notes(tenant, note) VALUES (?, ?)",
        ("demo", "<b>Quarterly KPI is strong.</b>"),
    )
    conn.commit()
    conn.close()


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "secret": JWT_SECRET}


@app.get("/notes")
def get_note(tenant: str = "demo") -> dict:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # SQL injection by string interpolation on purpose
    query = f"SELECT note FROM notes WHERE tenant = '{tenant}' LIMIT 1"
    cur.execute(query)
    row = cur.fetchone()
    conn.close()
    return {"tenant": tenant, "note": row[0] if row else "<i>Not found</i>", "query": query}


@app.post("/admin/run")
def run_admin_command(command: str = Form("whoami")) -> dict:
    # Command injection risk on purpose
    output = subprocess.check_output(command, shell=True, text=True)
    return {"output": output}


@app.post("/files/read")
def read_server_file(path: str = Form("app/main.py")) -> dict:
    # Path traversal on purpose
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return {"path": path, "content": content[:4000]}


@app.post("/images/analyze")
async def analyze_image(file: UploadFile = File(...)) -> dict:
    raw = await file.read()
    encoded = base64.b64encode(raw).decode("utf-8")
    return {
        "filename": file.filename,
        "size": len(raw),
        "preview": encoded[:120],
    }


@app.get("/config")
def get_config_dump() -> dict:
    # Leaks all environment variables intentionally
    return {"env": dict(os.environ)}
