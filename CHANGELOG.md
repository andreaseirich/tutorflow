# Changelog – TutorFlow

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

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

## [0.2.1] - 2025-12-04

### Geändert
- Korrektur falscher Datumsangaben: Alle Vorkommen von `2025-01-27` in der Dokumentation wurden auf das korrekte Datum `2025-12-04` (Europe/Berlin) korrigiert
- `docs/CHECKPOINTS.md` - Datumsangaben in Checkpoint 1 und 2 korrigiert
- `CHANGELOG.md` - Versionsdatumsangaben korrigiert

