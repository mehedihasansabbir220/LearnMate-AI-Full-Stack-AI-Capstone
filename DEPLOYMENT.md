# Deploying LearnMate AI for Free

This guide deploys the whole app on free plans, with no credit card and no Vercel:

| Part | Host | What it runs |
|---|---|---|
| Database | **Neon** (free plan) | PostgreSQL that stores saved study sessions |
| Backend | **Render** web service (free instance) | FastAPI app in `backend/` |
| Frontend | **Render** static site (free) | Next.js app in `frontend/`, built to static files |

Why this setup:
- **Neon instead of SQLite:** Render's free web services have no permanent disk, so a SQLite file would be wiped on every restart or redeploy.
- **Neon instead of Render Postgres:** Render's free Postgres databases are deleted 30 days after creation. Neon's free database doesn't expire.
- **Static frontend:** the frontend runs entirely in the browser, so `next.config.js` uses `output: "export"`. `npm run build` produces plain files in `frontend/out/` that any static host can serve.

> Free-plan limits change. The figures below were checked in October 2026; confirm them on [render.com/docs/free](https://render.com/docs/free) and [neon.com/pricing](https://neon.com/pricing) before you rely on them.

## What to expect on free plans

- **The backend sleeps.** A free Render web service spins down after 15 minutes without traffic. The next request wakes it, which takes up to about a minute. The first study pack after a quiet period will be slow; later ones are normal.
- **Render gives 750 free instance hours per month.** That's enough for one always-on service.
- **Neon's free plan:** 0.5 GB of storage and 100 compute-hours per project per month. The database pauses after 5 minutes idle and wakes automatically.
- **Gemini's free tier has rate limits.** You may see "Gemini is busy or rate-limited". The backend already retries automatically. Google may use free-tier prompts to improve its products, so don't paste confidential notes.
- **Not for production.** Render says not to use free instances for production apps. This setup is fine for a capstone demo.

## Before you start

You need:
1. A GitHub account with this project pushed to a repository.
2. A Google AI Studio API key from https://aistudio.google.com/app/apikey. If your key was ever pasted into a chat, an email, or a commit, create a new one and delete the old one first.
3. Free accounts on https://neon.com and https://render.com. Signing up with GitHub is easiest for Render.

Push the latest code:

```bash
git add .
git commit -m "Prepare free deployment on Render and Neon"
git push
```

`backend/.env` and `frontend/.env.local` are in `.gitignore`, so your key is never pushed. Check this with `git status` before every push: neither file should appear in the list.

## Step 1: Create the database (Neon)

1. In the Neon console, click **New project**.
2. Name it `learnmate`. Pick the region closest to where you'll run Render. For example, choose AWS US East (Ohio) for Render's Ohio region, or AWS Europe (Frankfurt) for Render's Frankfurt region.
3. When the project is ready, click **Connect** and copy the connection string. It looks like this:
   ```
   postgresql://USER:PASSWORD@ep-xxxx.REGION.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   ```
4. Keep this string private, because it contains your database password. You'll paste it into Render in Step 2.

You don't need to create any tables. The backend creates them automatically the first time it starts.

## Step 2: Deploy the backend (Render web service)

1. In the Render dashboard, click **New → Web Service**. Connect your GitHub account and select this repository.
2. Fill in the settings:

   | Setting | Value |
   |---|---|
   | Name | `learnmate-api` (this becomes part of the URL) |
   | Region | Same as, or near, your Neon region |
   | Branch | `master` (or whichever branch you push to) |
   | Root Directory | `backend` |
   | Language / Runtime | Python 3 |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
   | Instance Type | **Free** |

3. Under **Environment Variables**, add:

   | Key | Value |
   |---|---|
   | `PYTHON_VERSION` | `3.13.11` |
   | `GEMINI_API_KEY` | your Google AI Studio key |
   | `GEMINI_MODEL` | `gemini-flash-latest` |
   | `GEMINI_FALLBACK_MODELS` | optional, e.g. `gemini-flash-lite-latest` |
   | `DATABASE_URL` | the Neon connection string from Step 1 |
   | `FRONTEND_ORIGIN` | `http://localhost:3000` for now (you'll update it in Step 4) |

   You can paste the Neon string exactly as Neon gives it. The backend converts `postgresql://` to the driver it uses.
4. Under **Advanced**, set **Health Check Path** to `/api/health`.
5. Click **Create Web Service** and wait for the log to show `Application startup complete`.
6. Copy the service URL from the top of the page, e.g. `https://learnmate-api.onrender.com`.
7. Check that it works:
   - Open `https://learnmate-api.onrender.com/api/health` in a browser. It should show `{"status":"ok"}`.
   - Open `https://learnmate-api.onrender.com/docs` to see the API documentation.

## Step 3: Deploy the frontend (Render static site)

1. In the Render dashboard, click **New → Static Site** and select the same repository.
2. Fill in the settings:

   | Setting | Value |
   |---|---|
   | Name | `learnmate-web` |
   | Branch | same as the backend |
   | Root Directory | `frontend` |
   | Build Command | `npm ci && npm run build` |
   | Publish Directory | `out` |

3. Under **Environment Variables**, add:

   | Key | Value |
   |---|---|
   | `NEXT_PUBLIC_API_URL` | your backend URL from Step 2, e.g. `https://learnmate-api.onrender.com`, with **no trailing slash** |

   Never put the Gemini key in a `NEXT_PUBLIC_` variable, because those values are visible to anyone who opens the site.
4. Click **Create Static Site**. When the build finishes, copy the site URL, e.g. `https://learnmate-web.onrender.com`.

`NEXT_PUBLIC_API_URL` is baked into the files at build time. If you change it later, trigger a new deploy: **Manual Deploy → Clear build cache & deploy**.

## Step 4: Connect the frontend to the backend (CORS)

The backend only accepts browser requests from the origins listed in `FRONTEND_ORIGIN`.

1. Open the backend service (`learnmate-api`) and go to **Environment**.
2. Set `FRONTEND_ORIGIN` to your site URL. You can list several origins separated by commas, so local development keeps working too:
   ```
   https://learnmate-web.onrender.com,http://localhost:3000
   ```
   Use the exact origin: `https://`, no path, and no trailing slash.
3. Save. Render redeploys the backend with the new value.

## Step 5: Test the live app

1. Open the backend health URL first, to wake it up if it's asleep.
2. Open your frontend URL.
3. Create a study pack. For example, use the topic `Photosynthesis` at the `Beginner` level.
4. Check that it appears under **Recent study sessions**. Reload the page; it should still be there, because it's stored in Neon.
5. Optional: in the Neon console, open **Tables** and confirm that the `study_sessions` table has a row.

## Updating the app

Every `git push` to the connected branch automatically redeploys both services. To turn this off, set **Auto-Deploy** to off in each service's settings.

## Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| First request takes ~1 minute | The free backend was asleep. This is expected; later requests are fast. |
| Browser console shows a CORS error | `FRONTEND_ORIGIN` on the backend doesn't exactly match the site URL. Fix it as described in Step 4. |
| Frontend calls `localhost:8000` in production | `NEXT_PUBLIC_API_URL` wasn't set when the site was built. Set it, then **Clear build cache & deploy**. |
| Static site build says the publish directory isn't found | Make sure Root Directory is `frontend` and Publish Directory is `out`. If you left Root Directory empty, use `frontend/out`. |
| Backend deploy fails while installing packages | Check that `PYTHON_VERSION` is set to `3.13.11`, so Render doesn't pick a version some packages don't support yet. |
| `Missing GEMINI_API_KEY` | The key isn't set on the Render backend service. Your local `.env` is not uploaded. |
| `AI generation failed` (HTTP 502) | Check the backend **Logs** tab. A `404 NOT_FOUND` error means the model name is wrong: change `GEMINI_MODEL`. A `403` error means the key is invalid. |
| `Gemini is busy or rate-limited` (HTTP 503) | Google is overloaded, or you hit the free quota. Wait and retry, or set `GEMINI_FALLBACK_MODELS`. |
| Backend log shows a database connection error | Check `DATABASE_URL`: make sure the whole Neon string was copied, including `?sslmode=require`. |
| Sessions disappear after a redeploy | `DATABASE_URL` isn't set, so the backend fell back to a temporary SQLite file. Set it to the Neon string. |

## Other free options

- **Frontend:** `frontend/out/` is plain static files, so Netlify or Cloudflare Pages also work for free. Use build command `npm ci && npm run build`, base directory `frontend`, and publish directory `out`, and set `NEXT_PUBLIC_API_URL` the same way.
- **Backend:** any host that runs a Python web service from a start command works with the same build command, start command, and environment variables. Free backend tiers change often, so check the current terms before you choose one.
