
# Legal Case Management System (Flask + Jinja Templates)

This project is now a pure Python Flask application:
- Backend: Flask (`main.py`)
- Frontend: Server-rendered HTML templates (`templates/`)
- Database: SQLite (`legal_local.db`)

No React, Vite, Next.js, or npm tooling is required.

## Environment Variables

- `SQLITE_PATH` (optional, default: `legal_local.db`)
- `FLASK_SECRET_KEY` (optional)
- `COURT_USERNAME` (required for production)
- `COURT_PASSWORD` (required for production)
- `FLASK_DEBUG` (`0` by default)
- `HOST` (optional, default: `127.0.0.1`)
- `PORT` (optional, default: `8000`)

## Local Run

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Open `http://127.0.0.1:8000/login`.

## Login Roles

- Court: from env vars `COURT_USERNAME` and `COURT_PASSWORD`
- Lawyers and Clients: use registration screens, then login.

## Features in UI

- Login console
- Client registration and lawyer registration
- Forgot/reset password token flow
- Separate dashboards for court, lawyer, and client
- Create, edit, and delete controls for clients, lawyers, cases, and hearings (court role)
- Case history timeline and audit log screen
- CSV export for cases

## API (HTTP Basic Auth)

Court credentials are required as HTTP Basic Auth.

- `GET /api/cases`
- `GET /api/cases/<case_id>`
- `GET /api/hearings`
