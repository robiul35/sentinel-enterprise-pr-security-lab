# Sentinel Enterprise PR Security Lab

Monorepo with intentionally vulnerable and low-quality patterns to validate PR detection.

## Services
- `frontend/`: Next.js (TypeScript/TSX) dashboard + chart visualizer
- `backend/`: FastAPI backend with intentionally insecure endpoints
- `backend/services/mcp-server/`: FastAPI-based MCP-style tool service (SQL/Image/Embedding/KB stubs)

## Quick Start
1. Install Node.js 20+ and Python 3.11+
2. Web:
   - `cd frontend`
   - `npm install`
   - `npm run dev`
3. API:
   - `cd backend`
   - `python -m venv .venv`
   - `.venv\\Scripts\\activate` (Windows) or `source .venv/bin/activate` (Linux/macOS)
   - `pip install -r requirements.txt`
   - `uvicorn app.main:app --reload --port 8000`
4. MCP server:
   - `cd backend/services/mcp-server`
   - `python -m venv .venv`
   - `.venv\\Scripts\\activate` (Windows) or `source .venv/bin/activate` (Linux/macOS)
   - `pip install -r requirements.txt`
   - `uvicorn app.main:app --reload --port 8100`

## Docker Compose
- `docker compose up --build`

The code intentionally includes insecure and poor patterns for testing static analysis. Do not use in production.
