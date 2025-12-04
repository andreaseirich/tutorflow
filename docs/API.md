# API-Dokumentation – TutorFlow

## Übersicht

Diese Dokumentation beschreibt die API-Endpoints von TutorFlow. Die API wird in späteren Phasen implementiert.

## Status

**Phase 1**: API-Struktur wird in Phase 3 definiert und implementiert.

## Geplante Endpoints

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

### Premium-Funktionen
- `POST /api/lesson-plans/generate/` - KI-generierten Unterrichtsplan erstellen (Premium)
- `GET /api/lesson-plans/` - Liste aller Unterrichtspläne

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

