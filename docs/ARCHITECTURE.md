# Architecture – TutorFlow

## Overview

TutorFlow is a Django-based web application structured according to modern best practices. The architecture follows the principle of clear separation of responsibilities and modularity.

## Internationalization (i18n)

TutorFlow is fully internationalized with English as the default language and German as a secondary language.

- **Default Language**: English (`en`)
- **Supported Languages**: English (`en`), German (`de`)
- **Implementation**: All templates use `{% trans %}` and `{% blocktrans %}` tags for translatable strings
- **Models**: All model fields, choices, and verbose names use `gettext_lazy()` for translation
- **Language Switching**: Available via dropdown in the navigation bar
- **Translation Files**: Located in `backend/locale/` with separate `.po` files for each language
- **Status**: All templates including billing, blocked time, and recurring scheduling views are fully internationalized with English as the source language
- **Coverage**: No hard-coded German or English text remains in templates - all UI strings are properly wrapped in translation tags

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
│   ├── blocked_times/  # Blockzeiten-Verwaltung
│   ├── lesson_plans/   # KI-generierte Unterrichtspläne
│   └── core/           # Kernfunktionalität (User-Erweiterung, Income-Selector)
├── config/             # Zusätzliche Konfigurationsdateien
└── manage.py           # Django-Management-Script
```

### Domain-Modell (Implementiert)

Die folgenden Entitäten bilden das Kern-Domain-Modell und sind als Django-Models implementiert:

#### Student (apps.students)
- **Felder**: first_name, last_name, email, phone, school, grade, subjects, notes
- **Beziehungen**: One-to-Many zu Contract
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
- **Felder**: contract (FK), date, start_time, duration_minutes, status (choices), travel_time_before_minutes, travel_time_after_minutes, notes
- **Status**: 'planned', 'taught', 'cancelled', 'paid'
- **Beziehungen**: Many-to-One zu Contract
- **Zweck**: Planung und Verwaltung von Unterrichtsstunden mit Status-Tracking

#### RecurringLesson (apps.lessons.recurring_models)
- **Felder**: contract (FK), start_date, end_date, start_time, duration_minutes, travel_time_before_minutes, travel_time_after_minutes, recurrence_type (weekly/biweekly/monthly), monday-sunday (Boolean), is_active, notes
- **Beziehungen**: Many-to-One zu Contract
- **Zweck**: Vorlage für wiederholende Unterrichtsstunden (Serientermine). Ermöglicht die Definition von Serien (z. B. "jeden Montag 14 Uhr") und automatische Generierung von Lessons über einen Zeitraum.
- **Wiederholungsarten**:
  - `weekly`: Wöchentlich - jede Woche an den ausgewählten Wochentagen
  - `biweekly`: Alle 2 Wochen - jede zweite Woche an den ausgewählten Wochentagen
  - `monthly`: Monatlich - jeden Monat am gleichen Kalendertag, wenn dieser Tag ein ausgewählter Wochentag ist
- **Service**: `RecurringLessonService` generiert Lessons aus RecurringLesson-Vorlagen basierend auf `recurrence_type`, prüft Konflikte und überspringt bereits vorhandene Lessons.

#### BlockedTime (apps.blocked_times)
- **Felder**: title, description, start_datetime, end_datetime, is_recurring, recurring_pattern
- **Beziehungen**: Keine direkten Beziehungen
- **Zweck**: Verwaltung eigener Termine/Blockzeiten (z. B. Uni, Job, Gemeinde)
- **Kalender-Integration**: Blockzeiten werden ausschließlich über den Kalender verwaltet (Erstellen, Bearbeiten, Anzeigen). Es gibt keine Listenansicht mehr.
- **Mehrtägige Blockzeiten**: Unterstützt durch start_datetime und end_datetime (z. B. Urlaub/Reise)
- **Anzeige**: Optisch unterscheidbar von Lessons (gelbe Hintergrundfarbe) im Kalender

#### RecurringBlockedTime (apps.blocked_times.recurring_models)
- **Felder**: title, description, start_date, end_date, start_time, end_time, recurrence_type (weekly/biweekly/monthly), monday-sunday (Boolean), is_active
- **Beziehungen**: Keine direkten Beziehungen
- **Zweck**: Vorlage für wiederholende Blockzeiten (Serientermine). Ermöglicht die Definition von Serien (z. B. "jeden Dienstag 18–20 Uhr") und automatische Generierung von BlockedTime-Einträgen über einen Zeitraum.
- **Wiederholungsarten**:
  - `weekly`: Wöchentlich - jede Woche an den ausgewählten Wochentagen
  - `biweekly`: Alle 2 Wochen - jede zweite Woche an den ausgewählten Wochentagen
  - `monthly`: Monatlich - jeden Monat am gleichen Kalendertag, wenn dieser Tag ein ausgewählter Wochentag ist
- **Service**: `RecurringBlockedTimeService` generiert BlockedTime-Einträge aus RecurringBlockedTime-Vorlagen basierend auf `recurrence_type`, prüft Konflikte und überspringt bereits vorhandene Blockzeiten.

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

#### LessonStatusService (apps.lessons.status_service)
- **Kein Model**: Service-Layer für automatische Status-Verwaltung von Lessons
- **Methoden**:
  - `update_status_for_lesson(lesson)`: Aktualisiert Status basierend auf Datum/Zeit
    - Vergangene Lessons (end_datetime < jetzt) mit Status PLANNED oder leer → TAUGHT
    - Zukünftige Lessons (start_datetime >= jetzt) ohne Status → PLANNED
    - PAID oder CANCELLED werden NICHT überschrieben
    - Speichert nur, wenn Lesson bereits Primary Key hat (sonst nur Status setzen)
  - `bulk_update_past_lessons()`: Setzt alle vergangenen PLANNED Lessons auf TAUGHT
- **Zweck**: Automatische Status-Setzung beim Anlegen/Aktualisieren von Lessons
- **Integration**: 
  - Wird in LessonCreateView und LessonUpdateView aufgerufen
  - Wird in RecurringLessonService.generate_lessons() aufgerufen (vor und nach Speichern)
- **Wichtig**: Status wird im normalen Lesson-Formular NICHT mehr manuell auswählbar - nur automatisch gesetzt

#### CalendarService (apps.lessons.calendar_service)
- **Kein Model**: Service-Layer für Monatskalender-Ansicht
- **Methoden**:
  - `get_calendar_data(year, month)`: Lädt Lessons und Blockzeiten für einen Monat und gruppiert sie nach Tagen
- **Zweck**: Bereitstellung von Daten für die Monatskalender-Ansicht. Gruppiert Lessons und Blockzeiten nach Datum und prüft Konflikte.

#### WeekService (apps.lessons.week_service)
- **Kein Model**: Service-Layer für Wochenansicht
- **Methoden**:
  - `get_week_data(year, month, day)`: Lädt Lessons und Blockzeiten für eine Woche (Montag bis Sonntag) und gruppiert sie nach Tagen
- **Zweck**: Bereitstellung von Daten für die interaktive Wochenansicht. Bestimmt automatisch den Wochenbereich (Montag bis Sonntag) basierend auf einem beliebigen Tag.
- **Wichtig**: 
  - **Wochenansicht ist die zentrale UI für Terminplanung** - Lessons und Blockzeiten werden primär über die Wochenansicht geplant und bearbeitet.
  - **Drag-to-Create**: Nutzer können Zeitbereiche im Wochenraster ziehen, um neue Termine anzulegen.
  - **Zeitachse**: 08:00-22:00 Uhr mit stündlichen Zeilen.
  - **Termin-Anzeige**: Lessons (blau), Blockzeiten (orange), Konflikte (roter Rahmen/Icon).
  - **Klick auf Termin**: Öffnet Bearbeitungsformular.

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
1. **Kalender als zentrale UI**: Benutzer öffnet Kalenderansicht
2. **Anlegen**: Klick auf Tag im Kalender → Formular mit voreingestelltem Datum
   - Benutzer wählt Schüler/Vertrag, Zeit, Fahrtzeiten
   - Blockzeiten können ebenfalls über Klick auf Tag erstellt werden (🚫-Symbol)
3. **Bearbeiten**: Klick auf bestehende Lesson oder Blockzeit → Bearbeitungsformular
4. **Serientermine**: Button "Serientermin anlegen" → RecurringLesson-Formular
   - Nach Speichern: Automatische Generierung aller Lessons im Zeitraum
5. System prüft Konflikte (Blockzeiten, andere Lessons) inkl. Fahrtzeiten
6. **Konfliktprüfung**: 
   - Berechnung des Gesamtzeitblocks: `start = start_time - travel_before`, `ende = start_time + duration + travel_after`
   - Prüfung auf Überlappung mit anderen Lessons (inkl. deren Fahrtzeiten)
   - Prüfung auf Überlappung mit Blockzeiten
   - Konflikte werden als Warnung angezeigt
7. Lesson wird erstellt (ohne manuelle Status-Auswahl im Formular)
8. **Automatische Status-Setzung**: `LessonStatusService.update_status_for_lesson()`
   - Vergangene Lessons → Status TAUGHT
   - Zukünftige Lessons → Status PLANNED
   - PAID/CANCELLED werden nicht überschrieben
   - Wird sowohl bei manueller Erstellung als auch bei Recurring Lessons angewendet
9. Bei Abschluss: Status auf "unterrichtet" → "ausgezahlt" (über Abrechnungssystem)
10. **Kalender zeigt alle Lessons**: Vergangene und zukünftige Lessons werden im Kalender angezeigt
    - Vergangene Lessons sind optisch ausgegraut, aber anklickbar
    - Alle Lessons sind bearbeitbar
11. **Kalender-Datum-Synchronisation**: 
    - CalendarView verwendet ausschließlich year/month aus URL-Parametern (kein 'heute' für Monatsberechnung)
    - Zentrale Variable `current_month_date = date(year, month, 1)` für alle Berechnungen
    - Monatsname (month_label) wird aus current_month_date abgeleitet
    - Default-Datum im Create-Formular entspricht dem angeklickten Tag (date Parameter) oder year/month
    - Redirect nach Create/Update führt zurück zum korrekten Monat (year/month aus Request)

### Abrechnungs-Workflow
1. **Zeitraum auswählen**: Benutzer wählt Zeitraum (period_start, period_end) und optional Vertrag
2. **Automatische Auswahl**: System wählt automatisch alle Lessons mit Status TAUGHT im Zeitraum
   - Lessons mit Status PLANNED oder PAID werden nicht berücksichtigt
   - Lessons, die bereits in einer Rechnung sind, werden ausgeschlossen
   - Eine Lesson kann nur in einer Rechnung vorkommen (1:1-Beziehung über invoice_items)
3. **Vorschau**: System zeigt Vorschau der verfügbaren Lessons (optional)
4. **Rechnung erstellen**: `InvoiceService.create_invoice_from_lessons()`
   - Erstellt Invoice mit period_start, period_end, payer_info
   - Erstellt InvoiceItems für alle verfügbaren TAUGHT Lessons im Zeitraum (mit Kopie der Daten)
   - **Berechnung**: `units = lesson_duration_minutes / contract_unit_duration_minutes`, `amount = units * hourly_rate`
   - Berechnet total_amount als Summe aller InvoiceItems
   - Markiert alle Lessons automatisch als "bezahlt" (Status TAUGHT → PAID)
5. **Rechnungsdokument**: Optional: Generierung eines HTML/PDF-Dokuments
6. **Rechnung löschen**: `Invoice.delete()` (überschrieben) oder `InvoiceService.delete_invoice()`
   - Die `delete()`-Methode des Invoice Models ist überschrieben, um automatisch alle Lessons mit Status PAID auf TAUGHT zurückzusetzen
   - Funktioniert sowohl bei direktem `invoice.delete()` als auch über `InvoiceService.delete_invoice()`
   - Löscht Invoice und alle InvoiceItems (CASCADE)
   - Setzt alle zugehörigen Lessons zurück auf TAUGHT (PAID → TAUGHT)
7. **Bulk-Reset bezahlter Lessons**: Management Command `reset_paid_lessons`
   - Setzt alle Lessons mit Status PAID auf TAUGHT zurück
   - Option `--delete-invoices`: Löscht auch die zugehörigen Rechnungen
   - Option `--dry-run`: Zeigt nur an, was geändert würde
   - Verwendung: `python manage.py reset_paid_lessons [--delete-invoices] [--dry-run]`
8. **Finanzansicht**: Unterscheidung zwischen abgerechneten und nicht abgerechneten Lessons

### Konfliktlogik (Phase 3)
- **LessonConflictService**: Zentrale Service-Klasse für Konfliktprüfung
- **Zeitblock-Berechnung**: Berücksichtigt Fahrtzeiten vor und nach der Stunde
- **Konflikttypen**:
  - `lesson`: Überschneidung mit anderen Unterrichtsstunden
  - `blocked_time`: Überschneidung mit Blockzeiten
  - `quota`: Vertragskontingent überschritten (siehe unten)
- **Konfliktmarkierung**: Lessons haben `has_conflicts` Property und `get_conflicts()` Methode
- **UI-Darstellung**: Konflikte werden in Listen und Detailansichten als Warnung angezeigt

### Vertragskontingent & Quoten-Konflikte
- **ContractQuotaService**: Service für Prüfung von Vertragskontingenten basierend auf ContractMonthlyPlan
- **Regel**: Man darf im Verlauf eines Vertragszeitraums nicht "vorarbeiten"
- **Prüfung**: Für jeden Monat M gilt:
  - Summe der tatsächlich gehalten/geplanten Lessons von Vertragsbeginn bis Ende Monat M
  - darf die Summe der geplanten Einheiten (ContractMonthlyPlan) von Vertragsbeginn bis Monat M NICHT überschreiten
- **Nachholen erlaubt**: Wenn in früheren Monaten weniger als geplant stattgefunden hat, darf nachgeholt werden
- **Status-Berücksichtigung**: Nur Lessons mit Status PLANNED, TAUGHT oder PAID werden gezählt (CANCELLED nicht)
- **Integration**: Quota-Konflikte werden automatisch in `LessonConflictService.check_conflicts()` geprüft und als Konflikttyp `quota` zurückgegeben
- **UI-Anzeige**: Quota-Konflikte werden in der Lesson-Detailansicht mit speziellem Warnhinweis angezeigt

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
- **Student** ← (1:N) → **Contract**
- **Contract** ← (1:N) → **Lesson**
- **Student** ← (1:N) → **LessonPlan**
- **Lesson** ← (1:N) → **LessonPlan** (optional)
- **User** ← (1:1) → **UserProfile**

### Indizes
- Lesson: Index auf (date, start_time) und status für performante Abfragen
- BlockedTime: Index auf (start_datetime, end_datetime) für Konfliktprüfung

### Entfernte Features
- **Location-App**: Die gesamte Location-App wurde entfernt. Unterrichtsort-Felder wurden aus allen Modellen (Lesson, RecurringLesson, Student) entfernt.
- **Blockzeiten-Listenansicht**: Blockzeiten werden ausschließlich über den Kalender verwaltet. Es gibt keine separate Listenansicht mehr.

## Status

**Phase 2**: Domain-Models implementiert, Migrations erstellt und ausgeführt, Tests geschrieben.

- Alle 7 Domain-Models sind implementiert
- Migrations erfolgreich ausgeführt
- 14 Unit-Tests laufen erfolgreich
- IncomeSelector als Service-Layer implementiert

