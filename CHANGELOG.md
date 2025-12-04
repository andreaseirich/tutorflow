# Changelog – TutorFlow

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [0.7.0] - 2025-12-04

### Hinzugefügt
- **RecurringLesson Model**: Neue Entität für wiederholende Unterrichtsstunden (Serientermine)
  - Wochentage-Auswahl (Mo-So als Boolean-Felder)
  - Zeitraum (start_date, end_date)
  - Automatische Generierung von Lessons über einen Zeitraum
- **RecurringLessonService**: Service für Generierung von Lessons aus Serienterminen
  - Generiert Lessons für alle aktivierten Wochentage im Zeitraum
  - Überspringt bereits vorhandene Lessons
  - Prüft Konflikte optional
  - Vorschau-Funktion ohne Speicherung
- **Kalenderansicht**: Monatskalender für Lessons und Blockzeiten
  - CalendarView mit Monats-Grid (7 Spalten: Mo-So)
  - Anzeige von Lessons mit Zeit und Schüler
  - Markierung von Konflikten
  - Anzeige von Blockzeiten
  - Navigation zwischen Monaten
- **UI für Serientermine**: CRUD-Views und Templates
  - Liste, Detail, Form, Löschen
  - Button zum Generieren von Lessons aus Serie
  - Vorschau der zu erzeugenden Lessons

### Tests
- 8 neue Tests für RecurringLesson, RecurringLessonService und CalendarService
- Tests für einzelne/multiple Wochentage, Vertragsgrenzen, Konflikte, Kalender-Gruppierung

### Dokumentation
- ARCHITECTURE.md: RecurringLesson und CalendarService dokumentiert
- API.md: Endpoints für Serientermine und Kalender hinzugefügt

---

## [0.6.2] - 2025-12-04

### Entfernt
- **Contract.planned_units_per_month**: Feld vollständig entfernt
  - Migration erstellt, um Feld aus der Datenbank zu entfernen
  - Aus ContractForm, Templates und seed_demo_data entfernt
  - Geplante Einheiten werden ausschließlich über ContractMonthlyPlan verwaltet

---

## [0.6.1] - 2025-12-04

### Behoben
- **Monatliche Vertragsplanung**: Entfernung der Begrenzung auf das aktuelle Datum
  - Geplante Einheiten können nun für alle Monate zwischen start_date und end_date erfasst werden
  - Unabhängig davon, ob der Monat in der Vergangenheit oder Zukunft liegt
  - Neue Hilfsfunktion `iter_contract_months()` für konsistente Monatsgenerierung
  - Korrektur der Logik zum Löschen von Plänen außerhalb des Vertragszeitraums

### Tests
- 5 neue Tests für zukünftige, vergangene und übergreifende Verträge
- Tests prüfen explizit, dass keine Begrenzung auf das aktuelle Datum existiert

### Dokumentation
- ARCHITECTURE.md: Klarstellung, dass Monthly Plans für den gesamten Vertragszeitraum erzeugt werden

---

## [0.6.0] - 2025-12-04

### Hinzugefügt
- **ContractMonthlyPlan Model**: Neue Entität für explizite monatliche Planung von geplanten Einheiten pro Vertrag
  - Erlaubt ungleichmäßige Verteilung über das Jahr (z. B. mehr Einheiten in Prüfungsphasen)
  - Unique Constraint auf (contract, year, month)
- **Monatliche Planung in Contract-Views**: 
  - Formset-Integration für Bearbeitung von geplanten Einheiten pro Monat
  - Automatische Generierung von Monatszeilen beim Erstellen/Bearbeiten von Verträgen
  - Behandlung von Zeitraumänderungen (neue Monate werden ergänzt, alte entfernt)
- **IncomeSelector-Erweiterung**:
  - Neue Methode `get_monthly_planned_vs_actual()` für Vergleich geplant vs. tatsächlich
  - Berechnung von planned_units, planned_amount, actual_units, actual_amount pro Monat
- **Einnahmenübersicht erweitert**: 
  - Anzeige von geplanten vs. tatsächlichen Einheiten und Einnahmen in der Monatsansicht
  - Differenzberechnung (Differenz_units, Differenz_amount)

### Geändert
- `Contract.planned_units_per_month`: Als deprecated markiert (verwende ContractMonthlyPlan)
- `IncomeOverviewView`: Erweitert um planned_vs_actual Daten
- `contract_form.html`: Template erweitert um Formset für monatliche Planung

### Tests
- 8 neue Tests für ContractMonthlyPlan, Generierung von Monatsplänen und IncomeSelector-Vergleich

### Dokumentation
- `docs/ARCHITECTURE.md`: ContractMonthlyPlan dokumentiert, IncomeSelector erweitert
- Geplante Einheiten werden nicht mehr gleichmäßig verteilt, sondern explizit pro Monat erfasst

### Phase
- Neue Funktionalität: Monatliche Vertragsplanung

---

## [0.5.0] - 2025-12-04

### Hinzugefügt
- UI/UX-Polishing: Verbesserte Templates mit konsistenter Navigation, klarer Konfliktdarstellung, Premium-Badges
- Demo/Seed-Daten: Management Command `seed_demo_data` für Demo-Szenario
  - 3 Demo-Schüler mit unterschiedlichen Profilen
  - Zugehörige Verträge (privat und über Institut)
  - Mehrere Unterrichtsstunden (inkl. Konflikt zur Demonstration)
  - Blockzeiten
  - 1 Premium-User mit generiertem Unterrichtsplan
- Validierungsskript: `scripts/validate.sh` für automatische Checks (Django Check, Tests, TODO-Kommentare, Debug-Ausgaben)
- Dokumentation: DEVPOST.md für Hackathon-Einreichung erstellt

### Geändert
- README.md: Überarbeitet mit Demo-Daten-Anleitung, Validierungsskript, verbesserte Feature-Beschreibung
- docs/ETHICS.md: Erweitert um Abschnitt zu Demo-Daten und Datenschutz
- docs/PHASES.md: Phase 5 als abgeschlossen markiert
- docs/CHECKPOINTS.md: Checkpoint 5 hinzugefügt
- Templates: Verbesserte Darstellung von Konflikten, Premium-Badges, konsistente Buttons

### Phase
- Phase 5 – Polishing, Validierung & Hackathon-Feinschliff abgeschlossen

---

## [0.4.0] - 2025-12-04

### Hinzugefügt
- **Premium-Funktionen**:
  - `apps.core.utils.is_premium_user()` - Utility-Funktion für Premium-Checks
  - Premium-Gating in Views und Templates
  - UI-Hinweise für Nicht-Premium-User
- **AI-App** (`apps.ai`):
  - `apps.ai.client.LLMClient` - Low-Level-Client für LLM-API-Kommunikation (OpenAI-kompatibel)
  - `apps.ai.prompts` - Prompt-Bau für strukturierte Unterrichtspläne
  - `apps.ai.services.LessonPlanService` - High-Level-Service für LessonPlan-Generierung
- **LessonPlan-Generierung**:
  - Kontext-Sammlung (Schüler, Lesson, vorherige Lessons)
  - Strukturierter Prompt-Bau mit System- und User-Prompts
  - LLM-API-Integration mit Fehlerbehandlung
  - Speicherung als LessonPlan-Model mit Metadaten (Modell-Name, Erstellungszeitpunkt)
- **UI-Integration**:
  - Button "Unterrichtsplan mit KI generieren" in Lesson-Detail-Ansicht (nur Premium)
  - Anzeige generierter Pläne
  - Premium-Hinweis für Nicht-Premium-User
- **Konfiguration**:
  - LLM-Settings über Umgebungsvariablen (LLM_API_KEY, LLM_API_BASE_URL, LLM_MODEL_NAME, LLM_TIMEOUT_SECONDS)
  - Keine Secrets im Code
- **Tests**:
  - 12 Tests für Premium-Gating, Prompt-Bau, Services und Client
  - Mock-Tests für LLM-Aufrufe (keine echten API-Calls in Tests)
  - Fehlerszenarien getestet
- **Abhängigkeiten**:
  - `requests` für HTTP-API-Kommunikation

### Geändert
- `backend/tutorflow/settings.py` - LLM-Konfiguration hinzugefügt
- `apps/lessons/views.py` - LessonDetailView erweitert um LessonPlan-Anzeige
- `apps/lessons/templates/lessons/lesson_detail.html` - Template für LessonPlan-Generierung
- `docs/ARCHITECTURE.md` - AI-Architektur dokumentiert
- `docs/ETHICS.md` - KI-Einsatz, Datenschutz und Human-in-the-Loop dokumentiert
- `docs/API.md` - Premium-Endpoint dokumentiert
- `docs/PHASES.md` - Phase 4 als abgeschlossen markiert
- `docs/CHECKPOINTS.md` - Checkpoint 4 dokumentiert
- `requirements.txt` - requests hinzugefügt

### Phase
- Phase 4 – Premium & KI-Funktionen abgeschlossen

---

## [0.3.0] - 2025-12-04

### Hinzugefügt
- **CRUD-Funktionen** für alle Kern-Entitäten:
  - Student (List, Detail, Create, Update, Delete Views)
  - Contract (List, Detail, Create, Update, Delete Views)
  - Lesson (List, Detail, Create, Update, Delete, Month-View)
  - BlockedTime (List, Detail, Create, Update, Delete Views)
  - Location (List, Detail, Create, Update, Delete Views)
- **Konfliktprüfung**:
  - `apps.lessons.services.LessonConflictService` - Zentrale Service-Klasse für Konfliktprüfung
  - Zeitblock-Berechnung inkl. Fahrtzeiten
  - Prüfung auf Überlappung mit anderen Lessons und Blockzeiten
  - Konfliktmarkierung in Lesson-Model (`has_conflicts` Property, `get_conflicts()` Methode)
- **Planungslogik**:
  - `apps.lessons.services.LessonQueryService` - Service für Lesson-Abfragen
  - Monatsansicht für Lessons
  - Abfragen für heutige und kommende Lessons
- **Einnahmenübersicht**:
  - Dashboard-View mit Übersicht über heutige/kommende Stunden und Konflikte
  - IncomeOverview-View mit Monats-/Jahresansicht
  - Integration von IncomeSelector in Views
- **Basis-UI**:
  - Navigation zwischen allen Bereichen
  - Basis-Templates für alle CRUD-Operationen
  - Dashboard-Template mit Konfliktanzeige
- **Tests**:
  - 7 neue Tests für Konfliktprüfung und Services
  - Tests für Zeitblock-Berechnung, Konflikte mit Lessons und Blockzeiten, Abfragen

### Geändert
- `apps.lessons.models.Lesson` - Erweitert um Konfliktprüfungs-Methoden
- `backend/tutorflow/urls.py` - URLs für alle Apps eingebunden
- `docs/ARCHITECTURE.md` - Konfliktlogik und Einnahmenberechnung dokumentiert
- `docs/API.md` - Implementierte Views dokumentiert
- `docs/PHASES.md` - Phase 3 als abgeschlossen markiert
- `docs/CHECKPOINTS.md` - Checkpoint 3 dokumentiert

### Phase
- Phase 3 – Kernfunktionen (Planung & Einnahmen) abgeschlossen

---

## [0.2.1] - 2025-12-04

### Geändert
- Korrektur falscher Datumsangaben: Alle Vorkommen von `2025-01-27` in der Dokumentation wurden auf das korrekte Datum `2025-12-04` (Europe/Berlin) korrigiert
- `docs/CHECKPOINTS.md` - Datumsangaben in Checkpoint 1 und 2 korrigiert
- `CHANGELOG.md` - Versionsdatumsangaben korrigiert

---

## [0.2.0] - 2025-12-04

### Hinzugefügt
- Domain-Models implementiert:
  - `apps.locations.Location` - Unterrichtsort-Verwaltung mit optionalen Koordinaten
  - `apps.students.Student` - Schülerverwaltung mit Kontaktdaten, Schule, Fächern
  - `apps.contracts.Contract` - Vertragsverwaltung mit Honorar, Dauer, Zeitraum
  - `apps.lessons.Lesson` - Unterrichtsplanung mit Status-Tracking und Fahrtzeiten
  - `apps.blocked_times.BlockedTime` - Blockzeiten-Verwaltung
  - `apps.lesson_plans.LessonPlan` - KI-generierte Unterrichtspläne
  - `apps.core.UserProfile` - User-Erweiterung mit Premium-Flag
- `apps.core.selectors.IncomeSelector` - Service-Layer für Einnahmenberechnungen
- Admin-Interfaces für alle Models
- Migrations für alle Apps
- 14 Unit-Tests für Models und Services

### Geändert
- `docs/ARCHITECTURE.md` - Datenmodell-Details hinzugefügt
- `docs/PHASES.md` - Phase 2 als abgeschlossen markiert
- `docs/CHECKPOINTS.md` - Checkpoint 2 dokumentiert
- `backend/tutorflow/settings.py` - Alle Apps in INSTALLED_APPS registriert

### Phase
- Phase 2 – Domain-Datenmodell & Migrations abgeschlossen

---

## [0.1.0] - 2025-12-04

### Hinzugefügt
- Initiales Projekt-Setup
- Django 5.2.9 Projekt initialisiert
- Grundstruktur des Repositories angelegt:
  - `backend/` - Django-Projekt
  - `backend/apps/` - Platzhalter für Feature-Apps
  - `backend/config/` - Projektkonfiguration
  - `docs/` - Dokumentation
  - `scripts/` - Validierungsskripte
- Dokumentation erstellt:
  - `README.md` - Projektbeschreibung und Setup-Anleitung
  - `docs/ARCHITECTURE.md` - Architekturübersicht
  - `docs/ETHICS.md` - Ethisch-christliche Leitlinien
  - `docs/PHASES.md` - Entwicklungsphasen-Übersicht
  - `docs/CHECKPOINTS.md` - Fortschrittsprotokoll
  - `docs/API.md` - API-Dokumentation (Platzhalter)
- `requirements.txt` mit Django 5.2.9
- Virtuelles Environment Setup
- `CHANGELOG.md` - Diese Datei

### Phase
- Phase 1 – Projekt-Setup & Architekturgrundlagen gestartet
