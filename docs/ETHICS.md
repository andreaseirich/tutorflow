# Ethisch-christliche Leitlinien – TutorFlow

## Grundsätze

TutorFlow orientiert sich an ethisch-christlichen Werten, die sich in der Entwicklung, im Code und im Umgang mit Nutzerdaten widerspiegeln.

### Kernprinzipien

1. **Ehrlichkeit und Transparenz**
   - Keine versteckten Funktionen
   - Klare Kommunikation über Funktionalitäten
   - Transparente Datennutzung

2. **Ordnung und Klarheit**
   - Strukturierter, nachvollziehbarer Code
   - Klare Dokumentation
   - Übersichtliche Benutzeroberfläche

3. **Dienst am Nutzer**
   - Das Werkzeug soll dem Nutzer helfen, strukturierter und verantwortungsvoller zu arbeiten
   - Keine manipulative Logik
   - Respektvoller Umgang mit Benutzerdaten

4. **Kein Datenmissbrauch**
   - Minimale Datensammlung (nur was nötig ist)
   - Keine Weitergabe von Daten an Dritte ohne Zustimmung
   - Sichere Speicherung und Verarbeitung

5. **Respektvoller Umgang**
   - Respektvolle Sprache im Code und in der Benutzeroberfläche
   - Keine diskriminierenden oder verletzenden Inhalte

## Biblischer Bezug

Der Stil der Software soll von Ordnung und Zuverlässigkeit geprägt sein. Es werden keine theologischen Aussagen im Code erzwungen, aber Werte wie Treue, Klarheit und Verantwortlichkeit sollen sich im Produkt widerspiegeln.

## Datenschutz

### Datensparsamkeit
- Es werden nur die Daten gesammelt, die für die Funktionalität notwendig sind
- Keine unnötige Speicherung von persönlichen Informationen

### Transparenz
- Nutzer werden über die Datennutzung informiert
- Klare Datenschutzerklärung
- **Transparenz bei Zeitangaben und Logs**: Alle Zeitstempel und Datumsangaben in der Anwendung verwenden die Zeitzone Europe/Berlin. Dies wird in der Dokumentation klar kommuniziert, und alle Log-Einträge, Zeitstempel und Datumsangaben sind konsistent in dieser Zeitzone. Nutzer werden über die verwendete Zeitzone informiert, um Verwirrung zu vermeiden.

### Sicherheit
- Sichere Speicherung von Daten
- Verschlüsselung sensibler Informationen
- Regelmäßige Sicherheitsprüfungen

### Demo-Daten und Datenschutz
- **Keine echten Daten im Repository**: Das Repository enthält keine echten Schüler- oder Kundendaten
- **Demo-Daten sind fiktiv**: Alle Demo-Daten (z. B. via `seed_demo_data` Command) sind vollständig fiktiv und dienen nur zu Demonstrationszwecken
- **Verantwortungsvoller Umgang**: Nutzer werden ermutigt, verantwortungsvoll mit personenbezogenen Daten umzugehen und die Datenschutzbestimmungen einzuhalten

## KI-Einsatz (Premium-Funktion)

### Verantwortungsvoller KI-Einsatz
- KI wird nur für unterstützende Funktionen verwendet (Unterrichtsplan-Generierung)
- **Human-in-the-Loop**: KI-generierte Unterrichtspläne sind nur Vorschläge und müssen vom Nachhilfelehrer geprüft, angepasst und verantwortet werden
- Nutzer behalten die volle Kontrolle über generierte Inhalte
- Klare Kennzeichnung von KI-generierten Inhalten (Modell-Name wird gespeichert)
- Keine Manipulation oder Täuschung durch KI

### Transparenz
- Nutzer werden darüber informiert, wenn KI verwendet wird
- Generierte Inhalte können vom Nutzer überprüft und angepasst werden
- Das verwendete LLM-Modell wird dokumentiert

### Datenschutz bei KI-Nutzung
- **Minimale Datensammlung**: Es werden nur die notwendigsten Informationen an die LLM-API gesendet:
  - Name des Schülers (Vorname, Nachname)
  - Klassenstufe
  - Fach
  - Dauer der Stunde
  - Notizen zur Stunde (falls vorhanden)
- **Keine sensiblen Daten**: Folgende Daten werden NICHT an die API gesendet:
  - Vollständige Adressen
  - Telefonnummern oder E-Mail-Adressen
  - Persönliche Notizen, die nicht für die Unterrichtsplanung relevant sind
- **Lokale Speicherung**: Generierte Pläne werden lokal in der Datenbank gespeichert, nicht bei der LLM-API
- **API-Keys**: API-Keys werden über Umgebungsvariablen konfiguriert, nicht im Code gespeichert

## Hackathon-Konformität

### Urheberrecht
- Kein Kopieren kompletter Projekte oder größerer Codeblöcke aus fremden Repositories
- Open-Source-Bibliotheken werden verwendet, müssen aber im README genannt werden

### Fairness
- AI-Tools (Cursor, ChatGPT, etc.) sind erlaubt, aber es gibt eine sinnvolle menschliche Beteiligung
- Keine Verletzung von Urheberrecht oder geistigem Eigentum
- Kein verbotener oder unangemessener Content

## Umsetzung im Code

Diese Prinzipien sollen sich im Code widerspiegeln:

- Klare, verständliche Code-Struktur
- Gute Dokumentation
- Fehlerbehandlung ohne Verstecken von Problemen
- Validierung aller Eingaben
- Logging für Nachvollziehbarkeit (ohne Übermaß)

## Kontinuierliche Überprüfung

Diese Leitlinien werden regelmäßig überprüft und bei Bedarf angepasst, um sicherzustellen, dass TutorFlow den ethischen Standards entspricht.

