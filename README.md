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
- **Blockzeiten**: Verwaltung eigener Termine und Blockzeiten (z. B. Uni, Job, Gemeinde)
- **Einnahmenauswertung**: Monats- und Jahresauswertungen der Einnahmen nach Status
- **Premium-Funktion**: KI-gestützte Generierung von Unterrichtsplänen mithilfe einer LLM-API

## Features

### Basis-Features
- Verwaltung von Schülern, Verträgen und Nachhilfestunden
- Planung mit Blockzeiten und Fahrtzeiten
- Monatsansicht und Einnahmenberechnungen
- Konfliktprüfung bei der Terminplanung
- Optional: PDF-Upload für Auftragsbestätigungen

### Premium-Features
- KI-gestützte Generierung von Unterrichtsplänen

## Tech Stack

### Backend
- **Framework**: Django 5.2.9
- **Datenbank**: SQLite (Entwicklung), PostgreSQL (optional für Produktion)
- **Python**: 3.11+

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

## Dokumentation

- **ARCHITECTURE.md**: Architekturübersicht und technische Details
- **ETHICS.md**: Ethisch-christliche Leitlinien und Datenschutzprinzipien
- **PHASES.md**: Übersicht über Entwicklungsphasen
- **CHECKPOINTS.md**: Fortschrittsprotokoll und Checkpoints
- **API.md**: API-Dokumentation (wird in späteren Phasen befüllt)

## Lizenz

Dieses Projekt wird im Rahmen des Teca-Hacks-Hackathons entwickelt.

## Kontakt

Für Fragen oder Anregungen bitte ein Issue im Repository erstellen.

