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
│   ├── students/       # Schülerverwaltung (geplant)
│   ├── contracts/      # Vertragsverwaltung (geplant)
│   ├── lessons/        # Unterrichtsplanung (geplant)
│   ├── billing/        # Einnahmenauswertung (geplant)
│   └── core/           # Kernfunktionalität (geplant)
├── config/             # Zusätzliche Konfigurationsdateien
└── manage.py           # Django-Management-Script
```

### Domain-Modell (Konzeptionell)

Die folgenden Entitäten bilden das Kern-Domain-Modell:

- **Student**: Name, Kontaktdaten, Schule/Klasse, Fächer, Standard-Unterrichtsort
- **Contract**: Student, Institut, Honorar pro Einheit, Dauer, Vertragszeitraum, geplante Einheiten/Monat
- **Lesson**: Datum, Startzeit, Dauer, Status (geplant/unterrichtet/ausgefallen/ausgezahlt), Ort, Fahrtzeit vorher/nachher
- **BlockedTime**: Eigene Termine/Blockzeiten (z. B. Uni, Job, Gemeinde)
- **Location**: Name, Adresse, optional Koordinaten
- **LessonPlan**: KI-generierter Unterrichtsplan (Text + Metadaten)
- **User**: Django-User mit Zusatzfeld für Premium-Status
- **IncomeOverview**: Abgeleitete Monats-/Jahresauswertungen

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
2. System prüft Konflikte (Blockzeiten, andere Lessons)
3. System berechnet Fahrtzeiten (optional)
4. Lesson wird erstellt mit Status "geplant"
5. Bei Abschluss: Status auf "unterrichtet" → "ausgezahlt"

### Einnahmenberechnung
1. System sammelt alle Lessons mit Status "ausgezahlt" für einen Monat
2. Berechnung basierend auf Vertragshonorar
3. Aggregation nach Status und Monat
4. Darstellung in IncomeOverview

### KI-Unterrichtsplan-Generierung (Premium)
1. Premium-User wählt Schüler und Thema
2. System sammelt Kontext (Fach, Klasse, bisherige Lessons)
3. API-Aufruf an LLM (z. B. ChatGPT)
4. Ergebnis wird als LessonPlan gespeichert
5. Optional: Verknüpfung mit einer Lesson

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

## Status

**Phase 1**: Grundstruktur angelegt, Django-Projekt initialisiert.

Weitere Details werden in den folgenden Phasen ausgearbeitet.

