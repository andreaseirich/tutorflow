# Architektur – TutorFlow

## Übersicht

TutorFlow ist eine Django-basierte Web-Anwendung, die nach modernen Best Practices strukturiert ist. Die Architektur folgt dem Prinzip der klaren Trennung von Verantwortlichkeiten und Modularität.

## Technische Architektur

### Backend

#### Framework
- **Django 5.2.9**: Modernes Python-Web-Framework
- **SQLite**: Standard-Datenbank für Entwicklung
- **PostgreSQL**: Optional für Produktion vorbereitet

#### Projektstruktur

```
backend/
├── tutorflow/          # Hauptprojektkonfiguration
│   ├── settings.py     # Django-Einstellungen
│   ├── urls.py         # URL-Routing
│   ├── wsgi.py         # WSGI-Konfiguration
│   └── asgi.py         # ASGI-Konfiguration
├── apps/               # Feature-spezifische Django-Apps
│   ├── students/       # Schülerverwaltung
│   ├── contracts/      # Vertragsverwaltung
│   ├── lessons/        # Unterrichtsplanung
│   ├── locations/      # Ortsverwaltung
│   ├── blocked_times/  # Blockzeiten-Verwaltung
│   ├── lesson_plans/   # KI-generierte Unterrichtspläne
│   └── core/           # Kernfunktionalität (User-Erweiterung, Income-Selector)
├── config/             # Zusätzliche Konfigurationsdateien
└── manage.py           # Django-Management-Script
```

### Domain-Modell (Implementiert)

Die folgenden Entitäten bilden das Kern-Domain-Modell und sind als Django-Models implementiert:

#### Location (apps.locations)
- **Felder**: name, address, latitude, longitude (optional)
- **Beziehungen**: One-to-Many zu Student (default_location)
- **Zweck**: Verwaltung von Unterrichtsorten mit optionalen Koordinaten

#### Student (apps.students)
- **Felder**: first_name, last_name, email, phone, school, grade, subjects, default_location (FK), notes
- **Beziehungen**: Many-to-One zu Location, One-to-Many zu Contract
- **Zweck**: Zentrale Verwaltung von Schülern mit Kontaktdaten und Schulinformationen

#### Contract (apps.contracts)
- **Felder**: student (FK), institute, hourly_rate, unit_duration_minutes, start_date, end_date, is_active, notes
- **Beziehungen**: Many-to-One zu Student, One-to-Many zu Lesson, One-to-Many zu ContractMonthlyPlan
- **Zweck**: Verwaltung von Verträgen mit Honorar, Dauer und Vertragszeitraum
- **Hinweis**: Geplante Einheiten pro Monat werden explizit pro Monat in `ContractMonthlyPlan` erfasst (nicht mehr über das alte Feld `planned_units_per_month`).

#### ContractMonthlyPlan (apps.contracts)
- **Felder**: contract (FK), year, month, planned_units
- **Beziehungen**: Many-to-One zu Contract
- **Unique Constraint**: (contract, year, month)
- **Zweck**: Explizite monatliche Planung von geplanten Einheiten pro Vertrag. Erlaubt ungleichmäßige Verteilung über das Jahr (z. B. mehr Einheiten in Prüfungsphasen).
- **Wichtig**: Monthly Plans werden stets für den gesamten Vertragszeitraum (start_date bis end_date) erzeugt, unabhängig vom aktuellen Datum. Dies ermöglicht die Planung für zukünftige Verträge sowie die Erfassung von Plänen für vergangene Zeiträume.

#### Lesson (apps.lessons)
- **Felder**: contract (FK), date, start_time, duration_minutes, status (choices), location (FK), travel_time_before_minutes, travel_time_after_minutes, notes
- **Status**: 'planned', 'taught', 'cancelled', 'paid'
- **Beziehungen**: Many-to-One zu Contract und Location
- **Zweck**: Planung und Verwaltung von Unterrichtsstunden mit Status-Tracking

#### BlockedTime (apps.blocked_times)
- **Felder**: title, description, start_datetime, end_datetime, is_recurring, recurring_pattern
- **Beziehungen**: Keine direkten Beziehungen
- **Zweck**: Verwaltung eigener Termine/Blockzeiten (z. B. Uni, Job, Gemeinde)

#### LessonPlan (apps.lesson_plans)
- **Felder**: student (FK), lesson (FK, optional), topic, subject, content, grade_level, duration_minutes, llm_model
- **Beziehungen**: Many-to-One zu Student und Lesson (optional)
- **Zweck**: Speicherung von KI-generierten Unterrichtsplänen

#### UserProfile (apps.core)
- **Felder**: user (OneToOne), is_premium, premium_since
- **Beziehungen**: One-to-One zu Django User
- **Zweck**: Erweiterung des Django-User-Models um Premium-Flag

#### IncomeSelector (apps.core.selectors)
- **Kein Model**: Service-Layer für Einnahmenberechnungen
- **Methoden**: 
  - `get_monthly_income()`: Einnahmen für einen Monat basierend auf tatsächlichen Lessons
  - `get_yearly_income()`: Einnahmen für ein Jahr
  - `get_income_by_status()`: Gruppierung nach Status
  - `get_monthly_planned_vs_actual()`: Vergleich geplanter vs. tatsächlicher Einheiten und Einnahmen pro Monat
- **Zweck**: Abgeleitete Monats-/Jahresauswertungen ohne eigenes Model. Unterstützt Vergleich zwischen geplanten (aus ContractMonthlyPlan) und tatsächlichen (aus Lessons) Werten.

### Architekturprinzipien

#### Modultrennung
- Code-Dateien sollen kurz und fokussiert sein (max. 300–400 Zeilen)
- Bei größeren Dateien: Aufteilung in services.py, selectors.py, validators.py
- Keine "God-Modules" mit zu vielen Verantwortlichkeiten

#### Naming Conventions
- **snake_case** für Python-Funktionen und -Variablen
- **PascalCase** für Klassen
- Sprechende Namen, keine Abkürzungen
- Django-Apps nach Domain benennen (students, contracts, lessons, billing, core)

#### Logging und Error Handling
- Gezielt und sparsam loggen
- Keine stummen Fehler
- Fehler möglichst früh validieren (Form-/Serializer-Validierung)

## Datenfluss

### Planung einer Unterrichtsstunde
1. Benutzer wählt Schüler und Vertrag
2. System prüft Konflikte (Blockzeiten, andere Lessons) inkl. Fahrtzeiten
3. **Konfliktprüfung**: 
   - Berechnung des Gesamtzeitblocks: `start = start_time - travel_before`, `ende = start_time + duration + travel_after`
   - Prüfung auf Überlappung mit anderen Lessons (inkl. deren Fahrtzeiten)
   - Prüfung auf Überlappung mit Blockzeiten
   - Konflikte werden als Warnung angezeigt
4. Lesson wird erstellt mit Status "geplant"
5. Bei Abschluss: Status auf "unterrichtet" → "ausgezahlt"

### Konfliktlogik (Phase 3)
- **LessonConflictService**: Zentrale Service-Klasse für Konfliktprüfung
- **Zeitblock-Berechnung**: Berücksichtigt Fahrtzeiten vor und nach der Stunde
- **Konflikttypen**:
  - `lesson`: Überschneidung mit anderen Unterrichtsstunden
  - `blocked_time`: Überschneidung mit Blockzeiten
- **Konfliktmarkierung**: Lessons haben `has_conflicts` Property und `get_conflicts()` Methode
- **UI-Darstellung**: Konflikte werden in Listen und Detailansichten als Warnung angezeigt

### Einnahmenberechnung (Phase 3)
1. System sammelt alle Lessons für einen Monat/Jahr (filterbar nach Status)
2. **IncomeSelector**: Service-Layer für Einnahmenberechnungen
   - `get_monthly_income()`: Monatliche Einnahmen nach Status
   - `get_yearly_income()`: Jährliche Einnahmen mit Monatsaufschlüsselung
   - `get_income_by_status()`: Gruppierung nach Status (geplant, unterrichtet, ausgezahlt)
3. Berechnung basierend auf Vertragshonorar × Dauer (in Stunden)
4. Aggregation nach Status und Monat
5. Darstellung in IncomeOverview-View mit Filterung nach Jahr/Monat

### KI-Unterrichtsplan-Generierung (Premium) - Phase 4
1. Premium-User wählt eine Lesson aus
2. **Premium-Check**: System prüft, ob User Premium-Zugang hat (`apps.core.utils.is_premium_user()`)
3. **Kontext-Sammlung**: System sammelt relevante Informationen:
   - Schüler: Name, Klasse, Fach, Notizen
   - Lesson: Datum, Dauer, Status, Notizen
   - Vorherige Lessons: Letzte 5 Lessons für Kontext
4. **Prompt-Bau**: `apps.ai.prompts.build_lesson_plan_prompt()` erstellt strukturierten Prompt
5. **LLM-Aufruf**: `apps.ai.client.LLMClient` kommuniziert mit LLM-API (OpenAI-kompatibel)
6. **Fehlerbehandlung**: Timeouts, Netzwerk- und API-Fehler werden sauber abgefangen
7. **Speicherung**: Ergebnis wird als `LessonPlan` gespeichert mit:
   - Verknüpfung zu Lesson und Student
   - Generiertem Inhalt (Markdown-Text)
   - Metadaten (Modell-Name, Erstellungszeitpunkt)
8. **UI-Anzeige**: LessonPlan wird in Lesson-Detail-Ansicht angezeigt
9. **Human-in-the-Loop**: Nachhilfelehrer prüft und passt den Plan an

### AI-Architektur (Phase 4)
- **apps.ai.client.LLMClient**: Low-Level-API-Kommunikation
  - OpenAI-kompatibles Format
  - Timeout-Handling
  - Fehlerbehandlung (LLMClientError)
- **apps.ai.prompts**: Prompt-Bau
  - Strukturierte System- und User-Prompts
  - Kontext-Aggregation
- **apps.ai.services.LessonPlanService**: High-Level-Service
  - Orchestriert Kontext-Sammlung, Prompt-Bau und LLM-Aufruf
  - Erstellt/aktualisiert LessonPlan-Model
- **Konfiguration**: LLM-Settings über Umgebungsvariablen (LLM_API_KEY, LLM_API_BASE_URL, LLM_MODEL_NAME)

## Zeitzonen-Handling

- **Zeitzone**: Europe/Berlin (gemäß Master Prompt)
- Django ist konfiguriert mit `TIME_ZONE = 'Europe/Berlin'` und `USE_TZ = True`
- Alle Zeitstempel, Datumsangaben und Log-Einträge verwenden die Zeitzone Europe/Berlin
- Models mit DateTimeField nutzen Django's timezone-aware Datetime-Felder
- Admin-Interfaces und Tests berücksichtigen die Zeitzone korrekt

## Sicherheit

- Django-Standard-Sicherheitsfeatures aktiviert
- CSRF-Schutz
- Authentifizierung über Django-Auth-System
- Validierung aller Eingaben
- Keine direkten SQL-Queries (ORM verwenden)

## Erweiterbarkeit

Die Architektur ist darauf ausgelegt, einfach erweitert zu werden:

- Neue Apps können in `backend/apps/` hinzugefügt werden
- Services können in separaten Modulen organisiert werden
- API-Endpoints können schrittweise hinzugefügt werden
- Frontend kann später integriert werden (Django-Templates, HTMX, React, etc.)

## Datenbank-Schema

### Beziehungen
- **Location** ← (1:N) → **Student** (default_location)
- **Student** ← (1:N) → **Contract**
- **Contract** ← (1:N) → **Lesson**
- **Location** ← (1:N) → **Lesson**
- **Student** ← (1:N) → **LessonPlan**
- **Lesson** ← (1:N) → **LessonPlan** (optional)
- **User** ← (1:1) → **UserProfile**

### Indizes
- Lesson: Index auf (date, start_time) und status für performante Abfragen
- BlockedTime: Index auf (start_datetime, end_datetime) für Konfliktprüfung

## Status

**Phase 2**: Domain-Models implementiert, Migrations erstellt und ausgeführt, Tests geschrieben.

- Alle 7 Domain-Models sind implementiert
- Migrations erfolgreich ausgeführt
- 14 Unit-Tests laufen erfolgreich
- IncomeSelector als Service-Layer implementiert

