
# Legal Case Management System (FastAPI + Vanilla JS)

This project now uses a Python-only stack:
- Backend: FastAPI (`main.py`)
- Frontend: Static `index.html` served by FastAPI
- Deployment: Vercel Python runtime (`api/index.py`)

No Node.js or npm install is required.

## Environment Variables

Set these for DB connectivity:
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DATABASE`
- `FRONTEND_URL` (optional, for tighter CORS)

## Local Run

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000`.

## Vercel Deployment

1. Push repository to GitHub.
2. Import project in Vercel.
3. Add environment variables listed above.
4. Deploy.

`vercel.json` routes all traffic to `api/index.py`, which serves both the frontend (`/`) and API (`/api/*`).
