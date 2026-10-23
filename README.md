# LearnMate AI — Full-Stack AI Capstone

A study assistant that turns a topic or pasted notes into a study guide, key points, a multiple-choice quiz, and revision tips.

## Stack
- Frontend: Next.js 14, React, TypeScript
- Backend: FastAPI + Python
- AI: Google Gemini API from Google AI Studio
- Database: SQLite locally; PostgreSQL/Neon supported
- GitHub-ready documentation: proposal, architecture, final report template

## Run locally
Requirements: Node.js 18+ (tested with 22), Python 3.10+ (tested with 3.13), and a Google AI Studio API key from https://aistudio.google.com/app/apikey

### Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env       # only if backend/.env does not exist yet
```
Replace the placeholder in `backend/.env` with your key (`GEMINI_API_KEY=...`), then:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/api/health
- The SQLite database `backend/learnmate.db` and its tables are created automatically on startup. There are no migrations to run.

### Frontend (new terminal)
```bash
cd frontend
npm ci                     # or `npm install` if package-lock.json is missing
cp .env.local.example .env.local   # only if .env.local does not exist yet
npm run dev
```
Open http://localhost:3000.

### Checks
```bash
cd frontend && npm run lint && npm run build
curl http://localhost:8000/api/health
```

### Troubleshooting
| Symptom | Cause / fix |
|---|---|
| UI shows "Missing GEMINI_API_KEY" (HTTP 503) | `backend/.env` still has the placeholder key. Add your key and restart uvicorn. |
| UI shows "AI generation failed..." (HTTP 502) | Invalid key, quota exceeded, or the model isn't available to your key. Check the uvicorn terminal for the real error. Try a different `GEMINI_MODEL`. |
| UI shows "Gemini is busy or rate-limited" (HTTP 503) | Google returned 429/503 after 3 retries per model. Temporary on Google's side: wait and retry, or set `GEMINI_FALLBACK_MODELS`. |
| "Failed to fetch" / CORS error in browser console | Backend not running, or the frontend isn't on `FRONTEND_ORIGIN` (default `http://localhost:3000`). If Next picks another port (e.g. 3001), update `FRONTEND_ORIGIN` and restart the backend. |
| Changed `.env.local` but nothing changed | `NEXT_PUBLIC_*` values are baked in at startup. Restart `npm run dev`. |
| Port 8000 or 3000 in use | `lsof -nP -iTCP:8000 -sTCP:LISTEN` to find it, or run on another port and update `NEXT_PUBLIC_API_URL` / `FRONTEND_ORIGIN` to match. |

## Configuration
Backend `.env`:
- `GEMINI_API_KEY`: your Google AI Studio key (required)
- `GEMINI_MODEL`: defaults to `gemini-flash-latest`; change to a model available in your account if needed
- `GEMINI_FALLBACK_MODELS`: optional comma-separated models to try when the main model is overloaded (e.g. `gemini-flash-lite-latest`)
- `DATABASE_URL`: defaults to `sqlite:///./learnmate.db`; for Neon use `postgresql+psycopg://USER:PASSWORD@HOST/DBNAME?sslmode=require`
- `FRONTEND_ORIGIN`: defaults to `http://localhost:3000`

Frontend `.env.local`: `NEXT_PUBLIC_API_URL=http://localhost:8000`

## Free deployment outline
1. Deploy the FastAPI backend to a free web-service tier where available. Build: `pip install -r requirements.txt`; start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
2. Create a Neon PostgreSQL database and set `DATABASE_URL` on the backend.
3. Set backend `GEMINI_API_KEY`, `GEMINI_MODEL`, and `FRONTEND_ORIGIN` environment variables.
4. Deploy the Next.js frontend to a host supporting Next.js. Set `NEXT_PUBLIC_API_URL` to the deployed backend URL. Free tiers and limits change; free services may sleep.
5. Never put the Gemini API key in a `NEXT_PUBLIC_` variable or commit `.env`.

## GitHub
```bash
git init
git add .
git commit -m "Initial LearnMate AI capstone"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/learnmate-ai.git
git push -u origin main
```
Make meaningful commits during development if your course assesses commit history.

## AI methodology
The backend prompts Gemini to return JSON with a summary, key points, quiz questions, and revision tips. It validates required fields and stores each study pack. This is generative inference, not custom model training. Verify important facts against course materials.

## Deliverables
- `docs/PROJECT_PROPOSAL.md`
- `docs/FINAL_REPORT.md` (fill in actual test results; do not invent metrics)
- `docs/ARCHITECTURE.md`

The app sends submitted notes to Google when generating a study pack. Avoid confidential information. Google AI Studio quotas and terms may change.
# LearnMate-AI-Full-Stack-AI-Capstone
