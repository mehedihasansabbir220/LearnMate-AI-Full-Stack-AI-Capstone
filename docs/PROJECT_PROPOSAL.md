# Project Proposal: LearnMate AI
**AI Capstone Project — Frontend, Backend, AI/ML**

## Problem statement
Students often have lengthy notes and unfamiliar topics, while creating concise revision guides and practice questions takes time. LearnMate AI helps students turn a topic or pasted notes into a study guide, key points, a multiple-choice quiz, and revision tips.

## Proposed solution
A student enters a topic, optionally pastes notes, and chooses a learning level. The web app sends this input to a backend API, which asks Gemini to generate structured learning material. The result is displayed and saved so the student can reopen previous study sessions.

## AI approach
The project uses a Google Gemini generative model through the Google AI Studio API. Prompt engineering specifies topic, level, notes, and a JSON output schema. The backend parses the response and checks required fields. This is model inference, not training a new model. Generated facts may be wrong and should be checked against course material.

## Tech stack
- Frontend: Next.js, React, TypeScript, responsive CSS.
- Backend: Python, FastAPI, REST endpoints, Pydantic.
- AI: Gemini API.
- Database: SQLAlchemy with SQLite locally and PostgreSQL/Neon for deployment.
- Version control: Git and GitHub.
- Deployment: frontend host supporting Next.js, FastAPI service, and Neon PostgreSQL where free tiers are available.

## Endpoints
`GET /api/health`, `POST /api/study-packs`, `GET /api/sessions`, and `GET /api/sessions/{id}`.

## Evaluation plan
Test five or more topics, check the content against class materials, verify quiz answers, test multiple learning levels, confirm saved sessions can be reopened, and test mobile layout and API-key/quota errors. Include actual screenshots and measurements in the final report.

## Scope and limitations
The MVP handles English text input. It does not upload PDFs, train a custom model, or guarantee correctness. Hosting plans and API quotas may change.
