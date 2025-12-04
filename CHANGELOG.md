# Changelog – TutorFlow

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [0.8.5] - 2025-12-04

### Behoben
- **Rechnungsberechnung korrigiert**:
  - Berechnung basiert jetzt auf Einheiten statt Stunden
  - Formel: `units = lesson_duration_minutes / contract_unit_duration_minutes`, `amount = units * hourly_rate`
  - Beispiel: 90 Min bei 45 Min/Einheit und 12€/Einheit → 24€ (statt vorherige Stundenberechnung)
  - Gesamtsumme ist die Summe aller InvoiceItems

### Hinzugefügt
- **Status-Übergänge bei Rechnungen**:
  - Lessons werden automatisch auf PAID gesetzt beim Erstellen einer Rechnung
  - Lessons werden auf TAUGHT zurückgesetzt beim Löschen einer Rechnung (nur wenn nicht in anderen Rechnungen)
- **Rechnungen löschbar**:
  - InvoiceDeleteView mit Bestätigungsseite
  - Löschen-Button in Rechnungsdetailansicht
  - Sichere Delete-View (POST only, CSRF)

### Tests
- 5 neue Tests für Rechnungsberechnung und Status-Übergänge
- Tests für korrekte Einheitenberechnung (90 Min / 45 Min = 2 Einheiten)
- Tests für Status-Übergänge TAUGHT → PAID und PAID → TAUGHT
- Tests für korrekte Behandlung von Lessons in mehreren Rechnungen

---

## [0.8.4] - 2025-12-04

### Hinzugefügt
- **Erweiterte Wiederholungsmuster für Serientermine**:
  - `recurrence_type` Feld in RecurringLesson (weekly/biweekly/monthly)
  - Wöchentlich: wie bisher, jede Woche an den markierten Wochentagen
  - Alle 2 Wochen: jede zweite Woche an den markierten Wochentagen
  - Monatlich: jeden Monat am gleichen Kalendertag, wenn dieser Tag ein ausgewählter Wochentag ist
  - RecurringLessonService unterstützt alle drei Wiederholungsarten
  - Formular erweitert um Wiederholungsart-Auswahl mit Erklärungen

### Tests
- 6 Tests für verschiedene Wiederholungsmuster (weekly, biweekly, monthly)
- Tests für automatische Status-Setzung bei allen Wiederholungsarten

---

## [0.8.3] - 2025-12-04

### Hinzugefügt
- **Konflikt-Detailansicht**: 
  - ConflictDetailView zeigt alle kollidierenden Lessons und Blockzeiten
  - Anklickbarer "Details"-Link im Kalender bei Konflikten
  - Übersichtliche Liste mit Datum, Uhrzeit, Schüler, Ort und Bearbeiten-Links
- **Lesson-Detailansicht**:
  - LessonDetailView mit vollständigen Lesson-Informationen
  - Abschnitt "Konflikte" zeigt alle kollidierenden Lessons
  - Links zum Bearbeiten der kollidierenden Lessons

### Geändert
- **Kalender zeigt alle Lessons**: 
  - Filterung für vergangene Lessons entfernt
  - Vergangene und zukünftige Lessons werden angezeigt
  - Vergangene Lessons optisch ausgegraut (opacity: 0.7), aber anklickbar
  - Alle Lessons sind bearbeitbar

### Tests
- 4 Tests für Konflikt-Details und Kalender mit vergangenen Lessons

---

## [0.8.2] - 2025-12-04

### Behoben
- **Kalender-Monatsanzeige**: CalendarView verwendet jetzt ausschließlich year/month aus URL-Parametern
  - Zentrale Variable `current_month_date = date(year, month, 1)` für alle Berechnungen
  - Monatsname (month_label) wird korrekt aus angezeigtem Monat abgeleitet
  - Keine Verwendung von 'heute' für Monatsberechnung mehr
  - Template verwendet month_label statt month_names slice
  - CreateView verwendet year/month aus Request als Fallback für initiales Datum

### Tests
- 3 neue Tests für Kalender-Monatsanzeige (inkl. Dezember-Test)

---

## [0.8.1] - 2025-12-04

### Geändert
- **Status-Automatik für alle Lesson-Erzeugungen**:
  - RecurringLessonService nutzt jetzt LessonStatusService für automatische Status-Setzung
  - Lessons aus Serienterminen bekommen automatisch korrekten Status (Vergangenheit → TAUGHT, Zukunft → PLANNED)
  - Entfernt: Hart gesetzter Status 'planned' bei Recurring Lessons
- **Status nicht mehr manuell auswählbar**:
  - Status-Feld aus LessonForm entfernt (nur noch automatisch gesetzt)
  - Status wird nicht mehr im normalen Lesson-Formular angezeigt
  - Nur automatischer Mechanismus entscheidet Status beim Speichern
- **Kalender-Datum-Synchronisation**:
  - Monatsname im Kalender entspricht dem angezeigten Monat (year/month Parameter)
  - Default-Datum im Create-Formular entspricht dem angeklickten Tag (date Parameter)
  - Redirect nach Create/Update führt zurück zum korrekten Monat (year/month aus Request)

### Tests
- 6 neue Tests für Status-Automatik bei Recurring Lessons und manueller Erstellung
- 3 Tests für Kalender-Datum-Synchronisation

### Dokumentation
- ARCHITECTURE.md: Status-Automatik für alle Lesson-Erzeugungen dokumentiert
- ARCHITECTURE.md: Hinweis, dass Status im Formular nicht manuell wählbar ist
- README.md: Automatische Status-Verwaltung erwähnt

---

## [0.8.0] - 2025-12-04

### Hinzugefügt
- **LessonStatusService**: Automatische Status-Setzung für Lessons
  - Vergangene Lessons (end_datetime < jetzt) mit Status PLANNED → TAUGHT
  - Zukünftige Lessons ohne Status → PLANNED
  - PAID/CANCELLED werden nicht überschrieben
  - Integration in LessonCreateView und LessonUpdateView
  - bulk_update_past_lessons() für Batch-Updates
- **Billing-System**: Abrechnungssystem mit Rechnungen
  - Invoice und InvoiceItem Models
  - InvoiceService für Abrechnungs-Workflow
  - UI zum Auswählen von Lessons und Erstellen von Rechnungen
  - InvoiceDocumentService für HTML-Dokument-Generierung
  - Lessons werden nach Rechnungszuordnung auf Status PAID gesetzt
- **Erweiterte Finanzansicht**:
  - Unterscheidung zwischen abgerechneten und nicht abgerechneten Lessons
  - get_billing_status() im IncomeSelector
  - Anzeige in IncomeOverviewView

### Tests
- 5 Tests für LessonStatusService (vergangene/zukünftige Lessons, PAID/CANCELLED Schutz, bulk_update)
- 5 Tests für Billing (Invoice Model, InvoiceService, InvoiceItems Persistenz)

### Dokumentation
- ARCHITECTURE.md: LessonStatusService, Invoice/InvoiceItem, InvoiceService, InvoiceDocumentService dokumentiert
- ARCHITECTURE.md: Abrechnungs-Workflow beschrieben
- README.md: Automatische Status-Verwaltung und Abrechnungssystem erwähnt

---

## [0.7.1] - 2025-12-04

### Geändert
- **Kalender als zentrale UI**: Kalender ist jetzt die primäre Schnittstelle für Lesson-Verwaltung
  - Lessons-Listenansicht aus Navigation entfernt (Endpoints bleiben für API/Debugging)
  - Klick auf Tag im Kalender öffnet Formular zum Anlegen mit voreingestelltem Datum
  - Klick auf bestehende Lesson öffnet Bearbeitungsformular
  - Nach Create/Update Weiterleitung zurück zum Kalender
- **Kalender zeigt nur zukünftige Lessons**: 
  - Lessons in der Vergangenheit werden im Kalender nicht mehr angezeigt
  - Blockzeiten in der Vergangenheit werden ebenfalls ausgeblendet
  - Finanz-/Einnahmensichten zeigen weiterhin alle Lessons (inkl. vergangene)
- **Recurring Lessons besser integriert**:
  - Button "Serientermin anlegen" im Kalender-Header
  - Link "Serientermin erstellen" auf Contract-Detailseite
  - Automatische Generierung von Lessons nach Anlegen einer RecurringLesson
  - Weiterleitung zum Kalender nach Generierung
  - Hinweis im RecurringLesson-Formular erklärt Funktionalität

### Tests
- 3 neue Tests für Kalender-Filterung (vergangene Lessons werden ausgeblendet)
- Tests für Kalender-Integration (Create mit Datum-Parameter, Redirect)

### Dokumentation
- ARCHITECTURE.md: Kalender als zentrale UI dokumentiert
- README.md: Kalenderansicht und Serientermine erwähnt
- API.md: Kalender-Endpoints dokumentiert

---

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
