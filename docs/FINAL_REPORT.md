# LearnMate AI — Final Report
*Replace bracketed fields with actual tests and screenshots before submission.*

## 1. Abstract
LearnMate AI is a full-stack educational assistant that transforms a topic or pasted notes into a study guide, key points, a quiz, and revision suggestions. It combines a Next.js interface, FastAPI backend, Gemini AI, and database persistence.

## 2. Problem and objectives
Preparing revision guides and quizzes takes time. The project aims to make this workflow quicker through a responsive UI, AI-generated structured content, and saved study sessions.

## 3. System design
The frontend submits topic, notes, and learning level to FastAPI. The backend validates input, calls Gemini, parses the response, and stores it through SQLAlchemy. The frontend renders the pack and provides quiz checking and session history.

**Architecture:** Student → Next.js → FastAPI → Gemini API. FastAPI also writes to SQLite locally or PostgreSQL when deployed.

## 4. AI methodology
Prompt engineering asks Gemini to return JSON with a summary, key points, quiz questions, explanations, and revision tips. The backend checks required fields before persistence. This is generative inference, not model training. Structured output does not guarantee factual accuracy.

## 5. Implementation
Frontend: Next.js, React, TypeScript, responsive CSS. Backend: FastAPI and Pydantic. AI: Google Gemini API. Persistence: SQLAlchemy, SQLite locally, PostgreSQL/Neon in deployment. The API key is kept on the backend.

## 6. Testing and results
- Topics tested: [list at least five]
- Successful generations: [x/y]
- Average generation time: [measure it]
- Quiz answer quality: [observations]
- Save/reload: [pass/fail]
- Mobile layout: [pass/fail]
- Error handling: [missing key, invalid input, quota]
- Screenshots: [add screenshots or links]

Report only measurements you actually collected. Discuss incorrect answers or hallucinations observed.

## 7. Challenges and decisions
Potential challenges include provider quotas, variable model output, latency, and credential security. The project uses JSON-constrained prompting, backend validation, environment variables, and database abstraction.

## 8. Limitations and future work
No PDF upload, user accounts, source citations, or factual guarantee are included. Future improvements could include document ingestion, retrieval-augmented generation with citations, spaced repetition, multilingual output, and automated tests.

## 9. Conclusion
LearnMate AI demonstrates an end-to-end generative AI application with frontend interaction, backend APIs, structured model output, and persistence. The final submission should include real test results, screenshots, and a discussion of limitations.
