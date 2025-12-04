# TutorFlow

## Projektbeschreibung

TutorFlow ist eine Web-Anwendung für Nachhilfelehrer, die eine strukturierte Verwaltung von Schülern, Verträgen und Nachhilfestunden ermöglicht. Die Anwendung unterstützt Planung mit Blockzeiten und Fahrtzeiten, Auswertung von Einnahmen nach Monaten und Status, sowie optional das Hochladen von Auftragsbestätigungen (PDF) zur Datenextraktion.

## Problem

Nachhilfelehrer benötigen ein zuverlässiges Werkzeug zur Verwaltung ihrer Schüler, Verträge und Unterrichtsstunden. Die Planung muss Terminkonflikte vermeiden, Einnahmen müssen übersichtlich dargestellt werden, und die Verwaltung soll strukturiert und nachvollziehbar sein.

## Lösung

TutorFlow bietet eine vollständige Lösung für die Verwaltung von Nachhilfetätigkeiten:

- **Schülerverwaltung**: Zentrale Verwaltung von Schülern mit Kontaktdaten, Schule/Klasse, Fächern und Standard-Unterrichtsort
- **Vertragsverwaltung**: Verwaltung von Verträgen mit Honorar, Dauer, Vertragszeitraum
- **Unterrichtsplanung**: Planung von Nachhilfestunden mit Datum, Zeit, Ort und Fahrtzeiten
  - **Kalenderansicht**: Zentrale UI für die Stundenplanung - Lessons werden primär über die Kalenderansicht geplant und bearbeitet
  - **Serientermine**: Unterstützung für wiederholende Unterrichtsstunden (z. B. jeden Montag 14 Uhr)
- **Blockzeiten**: Verwaltung eigener Termine und Blockzeiten (z. B. Uni, Job, Gemeinde)
- **Einnahmenauswertung**: Monats- und Jahresauswertungen der Einnahmen nach Status
- **Automatische Status-Verwaltung**: Vergangene Lessons werden automatisch als unterrichtet markiert
- **Abrechnungssystem**: Rechnungen erstellen aus ausgewählten Unterrichtsstunden mit HTML-Dokument-Generierung
- **Premium-Funktion**: KI-gestützte Generierung von Unterrichtsplänen mithilfe einer LLM-API

## Features

### Basis-Features
- **Schülerverwaltung**: Zentrale Verwaltung mit Kontaktdaten, Schule, Fächern
- **Vertragsverwaltung**: Honorar, Dauer, Vertragszeitraum, geplante Einheiten
- **Unterrichtsplanung**: Planung mit Datum, Zeit, Ort, Fahrtzeiten
  - **Kalenderansicht**: Monatskalender als zentrale UI für Lesson-Verwaltung
  - **Serientermine**: Wiederholende Stunden (z. B. jeden Montag/Donnerstag) mit automatischer Generierung
- **Blockzeiten**: Verwaltung eigener Termine (Uni, Job, etc.)
- **Konfliktprüfung**: Automatische Erkennung von Überschneidungen (inkl. Fahrtzeiten)
- **Einnahmenübersicht**: Monats- und Jahresauswertungen nach Status (geplant, unterrichtet, ausgezahlt)
- **Dashboard**: Übersicht über heutige/nächste Stunden, Konflikte, Einnahmen

### Premium-Features
- **KI-gestützte Unterrichtspläne**: Automatische Generierung von detaillierten Unterrichtsplänen via LLM-API
- **Human-in-the-Loop**: Generierte Pläne können angepasst und verantwortet werden

## Tech Stack

### Backend
- **Framework**: Django 5.2.9
- **Datenbank**: SQLite (Entwicklung), PostgreSQL (optional für Produktion)
- **Python**: 3.11+
- **Abhängigkeiten**: Django, requests (siehe `requirements.txt`)

### Premium-Funktionen (KI)
- **LLM-Integration**: OpenAI-kompatible API für KI-generierte Unterrichtspläne
- **Konfiguration**: API-Keys über Umgebungsvariablen:
  ```bash
  export LLM_API_KEY="your-api-key"
  export LLM_API_BASE_URL="https://api.openai.com/v1"  # Optional
  export LLM_MODEL_NAME="gpt-3.5-turbo"  # Optional
  ```

### Frontend
- Wird in späteren Phasen definiert (z. B. Django-Templates, HTMX, Tailwind)

## Setup

### Voraussetzungen
- Python 3.11 oder höher
- pip

### Installation

1. Repository klonen:
```bash
git clone <repository-url>
cd tutorflow
```

2. Virtuelles Environment erstellen und aktivieren:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows
```

3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

4. Datenbank migrieren:
```bash
cd backend
python manage.py migrate
```

5. Entwicklungsserver starten:
```bash
python manage.py runserver
```

Die Anwendung ist dann unter `http://127.0.0.1:8000/` erreichbar.

### Demo-Daten laden

Um die Anwendung mit Demo-Daten zu testen, können Sie das Seed-Command ausführen:

```bash
cd backend
python manage.py seed_demo_data
```

Dies erstellt:
- 3 Demo-Schüler mit unterschiedlichen Profilen
- Zugehörige Verträge
- Mehrere Unterrichtsstunden (inkl. einem Konflikt zur Demonstration)
- Blockzeiten
- 1 Premium-User mit generiertem Unterrichtsplan

**Demo-Login:**
- Username: `demo_premium`
- Password: `demo123`

**Demo-Szenario:**
Die Demo-Daten zeigen ein realistisches Szenario mit:
- Mehreren Schülern in verschiedenen Klassenstufen
- Unterschiedlichen Verträgen (privat und über Institut)
- Einer Konfliktsituation zwischen zwei Lessons (zur Demonstration der Konfliktprüfung)
- Einer Blockzeit (Uni-Vorlesung)
- Einem Premium-User mit KI-generiertem Unterrichtsplan

## Projektstruktur

```
tutorflow/
├── backend/              # Django-Projekt
│   ├── apps/            # Feature-spezifische Apps
│   ├── config/          # Projektkonfiguration
│   ├── tutorflow/       # Django-Projektkonfiguration
│   └── manage.py
├── docs/                # Dokumentation
│   ├── ARCHITECTURE.md
│   ├── ETHICS.md
│   ├── PHASES.md
│   ├── CHECKPOINTS.md
│   └── API.md
├── scripts/             # Validierungsskripte
├── venv/                # Virtuelles Environment
├── requirements.txt
├── README.md
├── CHANGELOG.md
└── cursor_master_prompt.txt
```

## Entwicklung

Das Projekt wird in Phasen entwickelt. Siehe `docs/PHASES.md` für Details.

## Validierung

Ein Validierungsskript ist verfügbar, um das Projekt zu prüfen:

```bash
./scripts/validate.sh
```

Das Skript führt folgende Checks durch:
- Django System Check
- Testsuite
- Prüfung auf TODO-Kommentare
- Prüfung auf Debug-Ausgaben
- Dokumentationsprüfung

## Dokumentation

- **ARCHITECTURE.md**: Architekturübersicht und technische Details
- **ETHICS.md**: Ethisch-christliche Leitlinien und Datenschutzprinzipien
- **PHASES.md**: Übersicht über Entwicklungsphasen
- **CHECKPOINTS.md**: Fortschrittsprotokoll und Checkpoints
- **API.md**: API-Dokumentation
- **DEVPOST.md**: Inhalte für Devpost-Einreichung

## Lizenz

Dieses Projekt wird im Rahmen des Teca-Hacks-Hackathons entwickelt.

## Kontakt

Für Fragen oder Anregungen bitte ein Issue im Repository erstellen.

