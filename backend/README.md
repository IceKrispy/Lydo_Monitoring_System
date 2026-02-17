# LYDO Monitoring — Backend

Simple Python backend for the LYDO (Local Youth Development Organization) monitoring system.

## What this is
- Lightweight SQLite backend and CLI for managing barangays and youth program records.
- Primary backend script: `lydo_backend.py` (interactive CLI).
- Database file: `monitor.db` created in the `backend` folder.

## Requirements
- Python 3.8+
- No external packages required (uses the standard library `sqlite3`).

## Quick start
1. Open a terminal in the project root (or the `backend` folder).
2. Run:

```bash
python backend/lydo_backend.py
```

This launches an interactive text menu to add/list barangays and youth records.

## Database
- File: `backend/monitor.db`
- Tables:
  - `barangays` (id, name)
  - `youth` (id, barangay_id, name, email, age, gender, program, date_enrolled, notes)
- The code performs a safe migration: if `email` is missing, it will be added automatically on startup.

## CLI features
- Add / list barangays
- Add / list / update / delete youth records
- Seed sample data (menu option)

## Suggested next steps
- Add basic email validation before inserting records.
- Expose a REST API using Flask or FastAPI to allow remote access.
- Add CSV export/import for reporting.

## Files of interest
- `backend/lydo_backend.py` — CLI and user interaction
- `backend/db.py` — (if present) database utilities and schema management

If you want, I can add a small REST API now or add email validation next — which would you prefer?

## FastAPI (REST API)

A small FastAPI app is provided in `backend/api.py` that exposes CRUD endpoints for barangays and youth records.

Install dependencies and run the API server:

```bash
pip install -r requirements.txt
uvicorn backend.api:app --reload
```

Open `http://127.0.0.1:8000/docs` to view interactive API docs (Swagger UI).

### Alternative run (any working directory)

If you want to start the API server from any location (so Python can always import the `backend` package), you can run the project-root launcher:

```bash
python run_api.py
```

This script adds the project root to `sys.path` before starting Uvicorn.