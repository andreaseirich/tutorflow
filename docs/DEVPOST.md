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
- LLM mock mode with local `docs/llm_samples.json` and test coverage; no external calls in demo/CI.
- PII sanitizer for AI context; prompts rebuilt to use sanitized data before any AI call.
- Deterministic demo: `backend/fixtures/demo_data.json`, `.env.example`, `scripts/run_demo.sh` (one-command demo).
- Calendar/conflict engine kept deterministic for judges; overlapping lessons included in fixtures.
- Billing & income views stabilized; health endpoint `/health/` plus `scripts/smoke_demo.sh`.
- Docs/CI refresh: README, SECURITY, ARCHITECTURE, DEVPOST, CodeQL + MOCK_LLM in CI.

## How to run the demo
```bash
cp .env.example .env
./scripts/run_demo.sh
```
- Opens at `http://127.0.0.1:8000/` (health: `/health/`)
- Logins: `demo_premium` / `demo123`, `demo_user` / `demo123`
- AI responses are mocked; no external network calls required.

## Submission Checklist (copy into Devpost)

- ✅ Short title + tagline: “AI-assisted tutoring ops with safe defaults”
- ✅ Repository link and commit hash used for the build
- ✅ 100–150 word description (problem, solution, outcomes)
- ✅ Screenshots/GIFs of dashboard, week view, conflicts, billing
- ✅ Demo video link (show login → calendar → conflict → billing → AI lesson plan)
- ✅ Tech stack list (Django 6, Python 3.12, SQLite/Postgres, Mock LLM)
- ✅ Challenges + learnings (deterministic demos, PII scrubber, conflict engine)
- ✅ Clear instructions to run locally: `cp .env.example .env && ./scripts/run_demo.sh`
- ✅ Credits/attributions for external assets or OSS code
- ✅ Team members + roles (or “Solo build”) and Devpost profiles

## Judging Guide (what to show to reviewers)

1. **Login & dashboard (30s):** Use `demo_premium` to show today’s lessons + conflict summary.
2. **Calendar core loop (60s):** Open `/lessons/week/`, drag to create, click to edit; highlight conflict badges and blocked times.
3. **AI lesson plan (30s):** Open a lesson with prefilled mock plan; trigger “Generate AI Lesson Plan” to show UX and mock safety note.
4. **Billing & income (45s):** Create invoice from taught lesson, show invoice list + income overview with planned vs. taught vs. paid.
5. **Reliability & safety (15s):** Mention `MOCK_LLM=1`, health endpoint `/health/`, and deterministic fixtures in CI/demo.

## Links
- Repository: https://github.com/andreaseirich/tutorflow
- Video Script: [docs/VIDEO_SCRIPT.md](VIDEO_SCRIPT.md)
- Judging Guide (1-pager): [docs/JUDGING_GUIDE.md](JUDGING_GUIDE.md)
