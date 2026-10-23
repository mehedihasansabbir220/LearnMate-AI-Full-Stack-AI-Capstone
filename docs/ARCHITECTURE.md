# Architecture

## Request flow
1. Browser submits `topic`, `notes`, and `level` to `POST /api/study-packs`.
2. FastAPI validates input.
3. `ai_service.py` calls Gemini with server-side `GEMINI_API_KEY`.
4. JSON is parsed and required fields are checked.
5. Result is stored in `study_sessions`.
6. Frontend renders the study pack and can reopen saved sessions.

## Data model
`study_sessions`: ID, topic, level, source notes, JSON result, creation timestamp.

## Security
Keep `GEMINI_API_KEY` only in backend environment variables. Do not commit `.env`. Set CORS to the deployed frontend origin. Add authentication and rate limiting before production use. Avoid sending confidential notes to an external AI provider.
