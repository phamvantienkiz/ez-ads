# BAHA Ads Manager — Backend Service

Backend service for BAHA Ads Manager, integrating directly with official Meta Marketing API (v20.0).

## Architecture & Responsibilities
- **Framework**: FastAPI (Async)
- **Database**: SQLite 3 with WAL mode (via `aiosqlite`)
- **HTTP Client**: `httpx.AsyncClient`
- **Validation**: Pydantic V2 (`populate_by_name=True`)
- **Isolation**: Strictly isolated in `backend/.venv`

## Directory Structure
- `app/core`: Configuration & SQLite initialization
- `app/schemas`: Pydantic V2 models with Consistent Response Envelopes
- `app/repositories`: Data access for `meta_sessions` & `ad_creation_runs`
- `app/services`: Meta OAuth, Meta API Client (v20.0), and 5-step Ad Creation Orchestrator
- `app/middlewares`: Request ID, Access Logging, Safe Error Handling, CORS
- `app/api/v1`: REST Endpoints (`/api/v1/...` and alias `/api/...`)

## Running Locally
```bash
# In backend directory with isolated venv:
.venv\Scripts\uvicorn.exe app.main:app --reload --port 8000
```

## Running Tests
```bash
.venv\Scripts\pytest.exe
```
