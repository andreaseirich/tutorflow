# API-Dokumentation – TutorFlow

## Übersicht

Diese Dokumentation beschreibt die API-Endpoints von TutorFlow. Die API wird in späteren Phasen implementiert.

## Status

**Phase 3**: CRUD-Views und Kernfunktionen implementiert. Django-basierte Views (keine REST-API).

## Implementierte Views (Phase 3)

### Dashboard
- `GET /` - Dashboard mit heutigen Stunden, Konflikten und Einnahmenübersicht

### Schülerverwaltung
- `GET /students/` - Liste aller Schüler
- `GET /students/<id>/` - Schüler-Details
- `GET /students/create/` - Formular zum Erstellen
- `POST /students/create/` - Neuen Schüler erstellen
- `GET /students/<id>/update/` - Formular zum Bearbeiten
- `POST /students/<id>/update/` - Schüler aktualisieren
- `GET /students/<id>/delete/` - Bestätigungsseite
- `POST /students/<id>/delete/` - Schüler löschen

### Vertragsverwaltung
- `GET /contracts/` - Liste aller Verträge
- `GET /contracts/<id>/` - Vertrag-Details
- `GET /contracts/create/` - Formular zum Erstellen
- `POST /contracts/create/` - Neuen Vertrag erstellen
- `GET /contracts/<id>/update/` - Formular zum Bearbeiten
- `POST /contracts/<id>/update/` - Vertrag aktualisieren
- `GET /contracts/<id>/delete/` - Bestätigungsseite
- `POST /contracts/<id>/delete/` - Vertrag löschen

### Unterrichtsplanung
- `GET /lessons/` - Liste aller Unterrichtsstunden
- `GET /lessons/<id>/` - Unterrichtsstunde-Details (mit Konflikten)
- `GET /lessons/create/` - Formular zum Erstellen
- `POST /lessons/create/` - Neue Unterrichtsstunde erstellen (mit Konfliktprüfung)
- `GET /lessons/<id>/update/` - Formular zum Bearbeiten
- `POST /lessons/<id>/update/` - Unterrichtsstunde aktualisieren (mit Konfliktprüfung)
- `GET /lessons/<id>/delete/` - Bestätigungsseite
- `POST /lessons/<id>/delete/` - Unterrichtsstunde löschen
- `GET /lessons/month/<year>/<month>/` - Monatsansicht aller Stunden

### Blockzeiten
- `GET /blocked-times/` - Liste aller Blockzeiten
- `GET /blocked-times/<id>/` - Blockzeit-Details
- `GET /blocked-times/create/` - Formular zum Erstellen
- `POST /blocked-times/create/` - Neue Blockzeit erstellen
- `GET /blocked-times/<id>/update/` - Formular zum Bearbeiten
- `POST /blocked-times/<id>/update/` - Blockzeit aktualisieren
- `GET /blocked-times/<id>/delete/` - Bestätigungsseite
- `POST /blocked-times/<id>/delete/` - Blockzeit löschen

### Orte
- `GET /locations/` - Liste aller Orte
- `GET /locations/<id>/` - Ort-Details
- `GET /locations/create/` - Formular zum Erstellen
- `POST /locations/create/` - Neuen Ort erstellen
- `GET /locations/<id>/update/` - Formular zum Bearbeiten
- `POST /locations/<id>/update/` - Ort aktualisieren
- `GET /locations/<id>/delete/` - Bestätigungsseite
- `POST /locations/<id>/delete/` - Ort löschen

### Einnahmenauswertung
- `GET /income/` - Einnahmenübersicht (aktueller Monat)
- `GET /income/?year=<year>&month=<month>` - Monatliche Einnahmen
- `GET /income/?year=<year>` - Jährliche Einnahmen mit Monatsaufschlüsselung

## Services

### LessonConflictService
- `calculate_time_block(lesson)`: Berechnet Gesamtzeitblock inkl. Fahrtzeiten
- `check_conflicts(lesson)`: Prüft Konflikte mit anderen Lessons und Blockzeiten
- `has_conflicts(lesson)`: Boolean-Prüfung auf Konflikte

### LessonQueryService
- `get_lessons_for_month(year, month)`: Gibt alle Lessons für einen Monat zurück
- `get_today_lessons()`: Gibt heutige Lessons zurück
- `get_upcoming_lessons(days=7)`: Gibt nächste Lessons zurück

### IncomeSelector (apps.core.selectors)
- `get_monthly_income(year, month, status='paid')`: Monatliche Einnahmen
- `get_yearly_income(year, status='paid')`: Jährliche Einnahmen
- `get_income_by_status(year=None, month=None)`: Einnahmen nach Status gruppiert

## Geplante Endpoints (Zukünftig)

### Schülerverwaltung
- `GET /api/students/` - Liste aller Schüler
- `POST /api/students/` - Neuen Schüler erstellen
- `GET /api/students/{id}/` - Schüler-Details
- `PUT /api/students/{id}/` - Schüler aktualisieren
- `DELETE /api/students/{id}/` - Schüler löschen

### Vertragsverwaltung
- `GET /api/contracts/` - Liste aller Verträge
- `POST /api/contracts/` - Neuen Vertrag erstellen
- `GET /api/contracts/{id}/` - Vertrag-Details
- `PUT /api/contracts/{id}/` - Vertrag aktualisieren
- `DELETE /api/contracts/{id}/` - Vertrag löschen

### Unterrichtsplanung
- `GET /api/lessons/` - Liste aller Unterrichtsstunden
- `POST /api/lessons/` - Neue Unterrichtsstunde erstellen
- `GET /api/lessons/{id}/` - Unterrichtsstunde-Details
- `PUT /api/lessons/{id}/` - Unterrichtsstunde aktualisieren
- `DELETE /api/lessons/{id}/` - Unterrichtsstunde löschen

### Blockzeiten
- `GET /api/blocked-times/` - Liste aller Blockzeiten
- `POST /api/blocked-times/` - Neue Blockzeit erstellen
- `GET /api/blocked-times/{id}/` - Blockzeit-Details
- `PUT /api/blocked-times/{id}/` - Blockzeit aktualisieren
- `DELETE /api/blocked-times/{id}/` - Blockzeit löschen

### Einnahmenauswertung
- `GET /api/income/` - Einnahmenübersicht
- `GET /api/income/monthly/` - Monatliche Einnahmen
- `GET /api/income/yearly/` - Jährliche Einnahmen

### Premium-Funktionen (Phase 4)
- `POST /ai/lessons/<lesson_id>/generate-plan/` - KI-generierten Unterrichtsplan erstellen (nur Premium-User)
  - Erfordert: Authentifizierung + Premium-Status
  - Generiert LessonPlan für die angegebene Lesson
  - Bei Fehlern: Fehlermeldung, keine Retries

## Authentifizierung

Die Authentifizierung wird über Django's Authentifizierungssystem erfolgen. Details werden in späteren Phasen definiert.

## Fehlerbehandlung

API-Fehler werden im JSON-Format zurückgegeben:

```json
{
  "error": "Fehlerbeschreibung",
  "code": "ERROR_CODE"
}
```

## Versionierung

Die API-Versionierung wird in späteren Phasen definiert.

