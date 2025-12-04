# TutorFlow – Devpost-Einreichung

## Kurzbeschreibung

TutorFlow ist eine Web-Anwendung für Nachhilfelehrer zur strukturierten Verwaltung von Schülern, Verträgen, Unterrichtsstunden und Einnahmen. Die Anwendung bietet intelligente Konfliktprüfung, Einnahmenauswertung und optional KI-gestützte Unterrichtsplanung.

## Problem & Motivation

Nachhilfelehrer stehen vor der Herausforderung, ihre Tätigkeit professionell zu organisieren:
- **Terminplanung**: Überschneidungen vermeiden, Fahrtzeiten berücksichtigen, Blockzeiten einplanen
- **Verwaltung**: Schüler, Verträge, Honorare und Unterrichtsstunden strukturiert verwalten
- **Einnahmenübersicht**: Monatliche und jährliche Einnahmen nach Status (geplant, unterrichtet, ausgezahlt) nachvollziehen
- **Unterrichtsvorbereitung**: Zeitaufwändige Erstellung von Unterrichtsplänen

TutorFlow löst diese Probleme mit einer benutzerfreundlichen, strukturierten Lösung.

## Was TutorFlow macht

### Kernfunktionen

1. **Schülerverwaltung**
   - Zentrale Verwaltung mit Kontaktdaten, Schule, Klasse, Fächern
   - Standard-Unterrichtsort pro Schüler

2. **Vertragsverwaltung**
   - Honorar pro Einheit, Dauer, Vertragszeitraum
   - Geplante Einheiten pro Monat
   - Unterscheidung zwischen Privat- und Institut-Verträgen

3. **Intelligente Unterrichtsplanung**
   - Planung mit Datum, Zeit, Ort
   - **Automatische Konfliktprüfung**: Erkennt Überschneidungen inkl. Fahrtzeiten
   - **Blockzeiten**: Eigene Termine (Uni, Job, etc.) werden als belegt markiert
   - **Fahrtzeiten**: Vor und nach der Stunde werden berücksichtigt

4. **Einnahmenübersicht**
   - Monats- und Jahresauswertungen
   - Filterung nach Status (geplant, unterrichtet, ausgezahlt)
   - Aufschlüsselung nach Verträgen/Schülern

5. **Dashboard**
   - Übersicht über heutige und kommende Stunden
   - Konflikthinweise
   - Aktuelle Monatseinnahmen

### Premium-Funktion: KI-gestützte Unterrichtspläne

- **Automatische Generierung**: Detaillierte Unterrichtspläne via LLM-API
- **Human-in-the-Loop**: Generierte Pläne können angepasst und verantwortet werden
- **Datenschutz**: Nur notwendige Daten werden an die API gesendet (Name, Klasse, Fach, Dauer)
- **Transparenz**: Verwendetes Modell wird dokumentiert

## Tech Stack

### Backend
- **Framework**: Django 5.2.9
- **Datenbank**: SQLite (Entwicklung), PostgreSQL (Produktion)
- **Python**: 3.11+
- **Zeitzone**: Europe/Berlin (konsistent in allen Komponenten)

### Premium-Funktionen (KI)
- **LLM-Integration**: OpenAI-kompatible API
- **Konfiguration**: API-Keys über Umgebungsvariablen
- **Modell**: Konfigurierbar (Standard: gpt-3.5-turbo)

### Frontend
- **Templates**: Django-Templates mit modernem, responsivem Design
- **Styling**: Inline CSS für einfache Wartbarkeit

## Besonderheiten

### 1. Intelligente Konfliktprüfung
- Berücksichtigt nicht nur die Unterrichtszeit, sondern auch Fahrtzeiten vor und nach der Stunde
- Erkennt Überschneidungen mit anderen Lessons und Blockzeiten
- Visuelle Hervorhebung von Konflikten in der UI

### 2. Fahrtzeiten-Integration
- Jede Lesson kann individuelle Fahrtzeiten vor und nach der Stunde haben
- Der "Gesamtzeitblock" wird automatisch berechnet
- Konflikte werden basierend auf dem Gesamtzeitblock erkannt

### 3. Einnahmenberechnung
- Flexible Berechnung nach Status (geplant, unterrichtet, ausgezahlt)
- Monatliche und jährliche Übersichten
- Aufschlüsselung nach Verträgen/Schülern

### 4. KI-Integration mit Datenschutz
- Minimale Datensammlung: Nur notwendige Informationen werden an die LLM-API gesendet
- Keine sensiblen Daten (Adressen, Telefonnummern, E-Mails) werden übertragen
- Generierte Pläne werden lokal gespeichert

### 5. Ethisch-christliche Leitlinien
- Transparenz und Ehrlichkeit
- Ordnung und Klarheit
- Dienst am Nutzer
- Kein Datenmissbrauch
- Verantwortungsvoller KI-Einsatz

## Challenges & Learnings

### Herausforderungen

1. **Konfliktprüfung mit Fahrtzeiten**
   - Problem: Fahrtzeiten müssen in die Zeitblock-Berechnung einbezogen werden
   - Lösung: Zentrale Service-Funktion `LessonConflictService` berechnet Gesamtzeitblock inkl. Fahrtzeiten

2. **Zeitzonen-Handling**
   - Problem: Konsistente Verwendung von Europe/Berlin in allen Komponenten
   - Lösung: Django `TIME_ZONE` konfiguriert, alle DateTime-Operationen timezone-aware

3. **Modulare Architektur**
   - Problem: Code-Dateien sollen nicht zu groß werden (< 300-400 Zeilen)
   - Lösung: Klare Trennung in Services, Selectors, Views, Models

4. **KI-Integration mit Datenschutz**
   - Problem: Balance zwischen Funktionalität und Datenschutz
   - Lösung: Minimale Datensammlung, klare Dokumentation, Human-in-the-Loop

### Learnings

- **Django Best Practices**: Klare App-Struktur, Service-Layer für Business-Logik
- **Timezone-Handling**: Konsistente Verwendung von timezone-aware Datetime-Objekten
- **Modularität**: Kleine, fokussierte Dateien erleichtern Wartbarkeit
- **Ethik in der Entwicklung**: Ethische Prinzipien von Anfang an integrieren

## Demo

### Demo-Daten laden

```bash
cd backend
python manage.py seed_demo_data
```

**Demo-Login:**
- Username: `demo_premium`
- Password: `demo123`

### Demo-Szenario

Die Demo zeigt:
- 3 Schüler mit unterschiedlichen Profilen
- Verträge (privat und über Institut)
- Mehrere Unterrichtsstunden
- **Ein Konflikt** zwischen zwei Lessons (zur Demonstration)
- Blockzeiten (z. B. Uni-Vorlesung)
- Premium-User mit KI-generiertem Unterrichtsplan

## Setup

Siehe `README.md` für detaillierte Installationsanweisungen.

Kurzfassung:
1. Repository klonen
2. Virtuelles Environment erstellen
3. Abhängigkeiten installieren
4. Datenbank migrieren
5. Demo-Daten laden (optional)
6. Server starten

## Validierung

Ein Validierungsskript ist verfügbar:

```bash
./scripts/validate.sh
```

Prüft: Django Check, Tests, TODO-Kommentare, Debug-Ausgaben, Dokumentation.

## Dokumentation

- **README.md**: Projektübersicht, Setup, Features
- **docs/ARCHITECTURE.md**: Technische Architektur, Domain-Modell, Use-Cases
- **docs/ETHICS.md**: Ethisch-christliche Leitlinien, Datenschutz
- **docs/API.md**: API-Dokumentation
- **docs/PHASES.md**: Entwicklungsphasen
- **docs/CHECKPOINTS.md**: Fortschrittsprotokoll

## Zukunftsvision

- Mobile App (React Native)
- Kalender-Integration (iCal, Google Calendar)
- PDF-Upload für Auftragsbestätigungen mit Datenextraktion
- Erweiterte KI-Funktionen (z. B. Anpassung an Lernfortschritt)
- Multi-User-Support (mehrere Tutoren in einer Instanz)

## Team

Entwickelt im Rahmen des Teca-Hacks-Hackathons.

## Lizenz

Dieses Projekt wird im Rahmen des Teca-Hacks-Hackathons entwickelt.

