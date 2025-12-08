# TutorFlow – Devpost Submission

## Title
TutorFlow – AI-assisted tutoring ops with safe defaults

## Short Description
TutorFlow is a Django-based tutoring operations app with conflict-aware scheduling, billing, and AI lesson plans. For the hackathon, all demos run locally with mocked LLM responses, deterministic fixtures, and a one-command startup.

## Long Description
- Organize students, contracts, lessons, invoices, and conflicts in one place.
- Calendar-centric workflow with conflict checks (time + travel), recurring lessons, and blocked times.
- Income and billing views to track planned vs. taught vs. paid.
- AI lesson plans with **mock mode by default** (no external calls) and PII sanitization before prompting.
- One-command demo: `cp .env.example .env && ./scripts/run_demo.sh` loads stable fixtures and runs with `MOCK_LLM=1`.

## Tech Stack
- Backend: Django 6.0 (Python 3.12)
- DB: SQLite for development; PostgreSQL-ready for production
- AI: OpenAI-compatible client with mock mode + local samples
- CI: GitHub Actions (MOCK_LLM enforced), CodeQL, Ruff/Black

## Challenges
- Deterministic demos without external dependencies (LLM mock mode + fixtures).
- Privacy-by-default prompting (PII sanitizer before any AI call).
- Keeping calendar conflict detection deterministic for judges.
- Lightweight health check and smoke scripts for fast verification.

## What I built during the hackathon
- LLM mock mode with local `docs/llm_samples.json` and test coverage.
- PII sanitizer for AI context; prompts rebuilt to use sanitized data.
- Deterministic fixtures `backend/fixtures/demo_data.json` plus `scripts/run_demo.sh`.
- Health endpoint `/health/` and CI with `MOCK_LLM=1`.
- Documentation updates (README, SECURITY, ARCHITECTURE) for jury-readiness.

## How to run the demo
```bash
cp .env.example .env
./scripts/run_demo.sh
```
- Opens at `http://127.0.0.1:8000/` (health: `/health/`)
- Logins: `demo_premium` / `demo123`, `demo_user` / `demo123`
- AI responses are mocked; no external network calls required.

## Links
- Repository: https://github.com/andreaseirich/tutorflow
- Video Script: [docs/VIDEO_SCRIPT.md](VIDEO_SCRIPT.md)
