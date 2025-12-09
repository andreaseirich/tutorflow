# TutorFlow – Judging Guide

Eine einseitige Orientierung für Reviewer und Juroren (Teca Hacks). Fokus: schnell startbare Demo, klare Kernflows, Sicherheitshinweise.

## Start in < 2 Minuten
- **Setup:**
  ```bash
  cp .env.example .env
  ./scripts/run_demo.sh
  ```
- **Health-Check:** `curl http://127.0.0.1:8000/health/` → `{ "status": "ok" }`
- **Logins:**
  - Premium (AI): `demo_premium` / `demo123`
  - Standard: `demo_user` / `demo123`
- **Mock-Sicherheit:** `MOCK_LLM=1` verhindert externe API-Calls; alle AI-Antworten stammen aus `docs/llm_samples.json`.

## Demo-Storyboard (ca. 3 Minuten)
1. **Dashboard (30s):** Heute anstehende Termine + Konflikt-Summary zeigen.
2. **Week-View Kernloop (60s):** `/lessons/week/` öffnen, Drag-to-Create demonstrieren, Konflikt-Badges und Blocked Times markieren.
3. **AI-Lesson-Plan (30s):** Vorbefüllte Mock-Planung öffnen, Button „Generate AI Lesson Plan“ klicken, Mock-Hinweis betonen.
4. **Billing & Income (45s):** Rechnung aus `taught`-Lesson erzeugen, Invoice-Liste + Income-Übersicht (planned/taught/paid) zeigen.
5. **Safety & Reliability (15s):** Mock-Mode, PII-Scrubber, `/health/` und deterministische Fixtures nennen.

## Bewertungs-Shortcuts nach Kategorien
- **Best UI/Creativity:** Interaktive Week-View (Drag-to-Create, Konflikt-Icons, Blocked Times), Dark/Light-Design ansprechen falls aktiviert.
- **Best AI/ML:** AI-Lesson-Plan-Flow mit Mock-Mode + PII-Sanitizer; retries bei Rate-Limits erwähnt.
- **Best Solo Build:** Hinweis auf Solo-Umfang, deterministische Demo + CI (MOCK_LLM, Django check/tests, Ruff) als Qualitätsmerkmal.
- **Overall Excellence:** Klare Problem/Solution-Story, End-to-End-Flow (Planen → Konflikt → Billing → AI-Plan), stabile Demo ohne externe Abhängigkeiten.

## Troubleshooting
- Health-Check schlägt fehl → `./scripts/smoke_demo.sh` ausführen und Container-Logs prüfen.
- Übersetzungen fehlen → `python manage.py compilemessages` (bereits im Demo-Setup enthalten).
- Daten resetten → `python manage.py loaddata fixtures/demo_data.json`.
