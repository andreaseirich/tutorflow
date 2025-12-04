# Entwicklungsphasen – TutorFlow

## Übersicht

Das Projekt TutorFlow wird in mehreren Phasen entwickelt, um eine strukturierte und kontrollierte Entwicklung zu gewährleisten.

## Phase 1 – Projekt-Setup & Architekturgrundlagen

**Status**: ✅ Gestartet

**Ziel**: Repository initialisieren, Django-Grundprojekt anlegen, erste App-Struktur definieren, Grunddokumentation schreiben.

**Akzeptanzkriterien**:
- ✅ Django-Projekt lauffähig
- ✅ Basis-Ordnerstruktur vorhanden
- ✅ README, ARCHITECTURE, ETHICS, CHANGELOG angelegt und befüllt
- ✅ PHASES.md und CHECKPOINTS.md angelegt

**Tests**:
- Start des Dev-Servers
- Mindestens 1 einfacher Smoke-Test (z. B. `python manage.py check`)

**Fortschritt**:
- Grundstruktur angelegt
- Django-Projekt initialisiert
- Dokumentation erstellt

---

## Phase 2 – Domain-Datenmodell & Migrations

**Status**: ✅ Abgeschlossen

**Ziel**: Zentrale Models (Student, Contract, Lesson, BlockedTime, Location, User-Erweiterung) definieren und migrieren.

**Akzeptanzkriterien**:
- ✅ Alle Models definiert (7 Models: Location, Student, Contract, Lesson, BlockedTime, LessonPlan, UserProfile)
- ✅ Migrationen erstellt und erfolgreich ausgeführt
- ✅ ARCHITECTURE.md mit Datenmodell-Details aktualisiert
- ✅ IncomeSelector als Service-Layer implementiert

**Tests**:
- ✅ 14 Unit-Tests implementiert und erfolgreich
- ✅ Tests für Model-Logik (CRUD, Beziehungen, Einnahmenberechnung)

**Fortschritt**:
- Alle 7 Django-Apps erstellt (locations, students, contracts, lessons, blocked_times, lesson_plans, core)
- Models mit korrekten Feldern, Beziehungen und Meta-Optionen
- Admin-Interfaces für alle Models
- IncomeSelector mit monatlicher/jährlicher Einnahmenberechnung

---

## Phase 3 – Kernfunktionen (Planung & Einnahmen)

**Status**: ✅ Abgeschlossen

**Ziel**: CRUD für Schüler, Verträge, Lessons, Blockzeiten; Monatsansicht + Einnahmenberechnungen; einfache Konfliktprüfung.

**Akzeptanzkriterien**:
- ✅ Vollständige CRUD-Views für alle Kern-Entitäten (Student, Contract, Lesson, BlockedTime, Location)
- ✅ Konfliktprüfung mit Fahrtzeiten und Blockzeiten implementiert
- ✅ Monatsansicht & Einnahmenübersicht funktionieren
- ✅ Dashboard mit Übersicht über heutige/kommende Stunden und Konflikte
- ✅ Basis-UI mit Navigation

**Tests**:
- ✅ 7 neue Tests für Konfliktprüfung und Services
- ✅ Tests für Planungslogik, Konfliktprüfung inkl. Fahrtzeiten und Blockzeiten
- ✅ Alle Tests laufen erfolgreich

**Fortschritt**:
- LessonConflictService für Konfliktprüfung implementiert
- LessonQueryService für Abfragen implementiert
- CRUD-Views für alle Entitäten mit Django Class-Based Views
- Dashboard und Einnahmenübersicht implementiert
- Basis-Templates erstellt

---

## Phase 4 – Premium & KI-Funktionen

**Status**: ⏳ Ausstehend

**Ziel**: Premium-Flag am User, Integration einer LLM-API für Unterrichtsplan-Erstellung, saubere Trennung von Basis- und Premium-Features.

**Akzeptanzkriterien**:
- KI-Unterrichtsplan kann für Premium-User erzeugt werden
- ETHICS.md enthält Hinweise zum KI-Einsatz

**Tests**:
- Mock-Tests/Integrationstests für KI-Aufrufe

---

## Phase 5 – Polishing, Validierung & Hackathon-Feinschliff

**Status**: ⏳ Ausstehend

**Ziel**: UI verbessern, Demo-Daten einpflegen, Doku finalisieren, Tests stabilisieren, alles auf Hackathon-Submission trimmen.

**Akzeptanzkriterien**:
- Vollständig laufendes System
- Aktuelle Dokumentation
- Klare Demo-Story

---

## Phasenwechsel

Vor dem Wechsel zu einer neuen Phase:
1. Alle Akzeptanzkriterien der aktuellen Phase erfüllt
2. Tests laufen erfolgreich
3. Dokumentation aktualisiert
4. Git-Commits erstellt
5. Checkpoint in CHECKPOINTS.md dokumentiert

