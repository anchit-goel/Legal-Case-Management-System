
# Legal Case Management System – Vercel Deployment

## Environment Variables

**Backend (.env):**
- MYSQL_HOST
- MYSQL_PORT
- MYSQL_USER
- MYSQL_PASSWORD
- MYSQL_DATABASE
- FRONTEND_URL (optional, for CORS)
- BACKEND_URL (optional, for CORS)

**Frontend (.env):**
- VITE_BACKEND_URL (default: /api)

See `.env.example` and `.env.example.frontend` for templates.

## Vercel Configuration

- Python version: 3.11 (see `runtime.txt`)
- Backend entry: `/api/index.py` (FastAPI app)
- Frontend: Vite React (see `package.json`)
- See `vercel.json` for build and routing config

## Cloud MySQL

Provision a managed MySQL database (e.g., PlanetScale, AWS RDS, Azure, Google Cloud SQL). Set credentials in Vercel project environment variables.

## Deployment Steps

1. Push code to GitHub.
2. Import repo in Vercel dashboard.
3. Set environment variables in Vercel:
	- Backend: MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
	- Frontend: VITE_BACKEND_URL (optional, defaults to `/api`)
4. Deploy.

## Local Development

1. Copy `.env.example` to `.env` and fill in values.
2. Copy `.env.example.frontend` to `.env` in `src/` if needed.
3. Run backend: `uvicorn main:app --reload`
4. Run frontend: `npm install && npm run dev`

---
For any DB connection errors, check your cloud MySQL credentials and Vercel environment variable settings.
