# Entwicklungsphasen – TutorFlow

## Übersicht

Das Projekt TutorFlow wird in mehreren Phasen entwickelt, um eine strukturierte und kontrollierte Entwicklung zu gewährleisten.

## Phase 1 – Projekt-Setup & Architekturgrundlagen

**Status**: ✅ Gestartet

**Ziel**: Repository initialisieren, Django-Grundprojekt anlegen, erste App-Struktur definieren, Grunddokumentation schreiben.

**Akzeptanzkriterien**:
- ✅ Django-Projekt lauffähig
- ✅ Basis-Ordnerstruktur vorhanden
- ✅ README, ARCHITECTURE, ETHICS, CHANGELOG angelegt und befüllt
- ✅ PHASES.md und CHECKPOINTS.md angelegt

**Tests**:
- Start des Dev-Servers
- Mindestens 1 einfacher Smoke-Test (z. B. `python manage.py check`)

**Fortschritt**:
- Grundstruktur angelegt
- Django-Projekt initialisiert
- Dokumentation erstellt

---

## Phase 2 – Domain-Datenmodell & Migrations

**Status**: ✅ Abgeschlossen

**Ziel**: Zentrale Models (Student, Contract, Lesson, BlockedTime, Location, User-Erweiterung) definieren und migrieren.

**Akzeptanzkriterien**:
- ✅ Alle Models definiert (7 Models: Location, Student, Contract, Lesson, BlockedTime, LessonPlan, UserProfile)
- ✅ Migrationen erstellt und erfolgreich ausgeführt
- ✅ ARCHITECTURE.md mit Datenmodell-Details aktualisiert
- ✅ IncomeSelector als Service-Layer implementiert

**Tests**:
- ✅ 14 Unit-Tests implementiert und erfolgreich
- ✅ Tests für Model-Logik (CRUD, Beziehungen, Einnahmenberechnung)

**Fortschritt**:
- Alle 7 Django-Apps erstellt (locations, students, contracts, lessons, blocked_times, lesson_plans, core)
- Models mit korrekten Feldern, Beziehungen und Meta-Optionen
- Admin-Interfaces für alle Models
- IncomeSelector mit monatlicher/jährlicher Einnahmenberechnung

---

## Phase 3 – Kernfunktionen (Planung & Einnahmen)

**Status**: ✅ Abgeschlossen

**Ziel**: CRUD für Schüler, Verträge, Lessons, Blockzeiten; Monatsansicht + Einnahmenberechnungen; einfache Konfliktprüfung.

**Akzeptanzkriterien**:
- ✅ Vollständige CRUD-Views für alle Kern-Entitäten (Student, Contract, Lesson, BlockedTime, Location)
- ✅ Konfliktprüfung mit Fahrtzeiten und Blockzeiten implementiert
- ✅ Monatsansicht & Einnahmenübersicht funktionieren
- ✅ Dashboard mit Übersicht über heutige/kommende Stunden und Konflikte
- ✅ Basis-UI mit Navigation

**Tests**:
- ✅ 7 neue Tests für Konfliktprüfung und Services
- ✅ Tests für Planungslogik, Konfliktprüfung inkl. Fahrtzeiten und Blockzeiten
- ✅ Alle Tests laufen erfolgreich

**Fortschritt**:
- LessonConflictService für Konfliktprüfung implementiert
- LessonQueryService für Abfragen implementiert
- CRUD-Views für alle Entitäten mit Django Class-Based Views
- Dashboard und Einnahmenübersicht implementiert
- Basis-Templates erstellt

---

## Phase 4 – Premium & KI-Funktionen

**Status**: ✅ Abgeschlossen

**Ziel**: Premium-Flag am User, Integration einer LLM-API für Unterrichtsplan-Erstellung, saubere Trennung von Basis- und Premium-Features.

**Akzeptanzkriterien**:
- ✅ Premium-Flag vollständig integriert (`apps.core.utils.is_premium_user()`)
- ✅ KI-Unterrichtsplan kann für Premium-User erzeugt werden
- ✅ LLM-Integration gekapselt (client/prompts/services)
- ✅ API-Keys über Umgebungsvariablen konfiguriert
- ✅ Fehlerbehandlung für LLM-Aufrufe implementiert
- ✅ ETHICS.md enthält Hinweise zum KI-Einsatz und Datenschutz

**Tests**:
- ✅ 12 Tests für Premium-Gating, Prompt-Bau, Service-Layer und Client
- ✅ Mock-Tests für KI-Aufrufe (keine echten API-Calls in Tests)
- ✅ Fehlerszenarien getestet

**Fortschritt**:
- AI-App erstellt (`apps.ai`) mit modularer Struktur
- LLMClient für API-Kommunikation (OpenAI-kompatibel)
- Prompt-Bau für strukturierte Unterrichtspläne
- LessonPlanService für High-Level-Generierung
- UI-Integration in Lesson-Detail-Ansicht
- Premium-Gating in Views und Templates

---

## Phase 5 – Polishing, Validierung & Hackathon-Feinschliff

**Status**: ✅ Abgeschlossen

**Ziel**: UI verbessern, Demo-Daten einpflegen, Doku finalisieren, Tests stabilisieren, alles auf Hackathon-Submission trimmen.

**Akzeptanzkriterien**:
- ✅ UI ist einfach, aber klar und demo-tauglich
- ✅ Reproduzierbares Demo-Szenario (Seed-Daten) vorhanden
- ✅ Validierungsskript existiert und läuft
- ✅ README, ARCHITECTURE, ETHICS, API, PHASES, CHECKPOINTS, DEVPOST sind aktuell und konsistent
- ✅ Tests laufen fehlerfrei
- ✅ Codebasis wirkt für Hackathon-Juroren aufgeräumt, strukturiert und nachvollziehbar

**Tests**:
- ✅ Validierungsskript prüft Django Check, Tests, TODO-Kommentare, Debug-Ausgaben
- ✅ Alle Tests laufen erfolgreich

**Fortschritt**:
- UI/UX-Polishing: Templates verbessert, konsistente Navigation, klare Konfliktdarstellung, Premium-Badges
- Demo/Seed-Daten: Management Command `seed_demo_data` erstellt mit 3 Schülern, Verträgen, Lessons (inkl. Konflikt), Blockzeiten, Premium-User mit LessonPlan
- Validierungsskript: `scripts/validate.sh` erstellt für automatische Checks
- Dokumentation finalisiert: README überarbeitet, ETHICS erweitert (Demo-Daten), DEVPOST.md erstellt
- Code-Cleanup: Keine TODOs, keine Debug-Ausgaben, saubere Struktur

---

## Phasenwechsel

Vor dem Wechsel zu einer neuen Phase:
1. Alle Akzeptanzkriterien der aktuellen Phase erfüllt
2. Tests laufen erfolgreich
3. Dokumentation aktualisiert
4. Git-Commits erstellt
5. Checkpoint in CHECKPOINTS.md dokumentiert

