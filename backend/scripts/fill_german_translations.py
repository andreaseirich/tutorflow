#!/usr/bin/env python
"""
Script to fill German translations in django.po file.
This script reads the English msgid and adds German translations.
"""
import re
import sys
from pathlib import Path

# Translation mapping: English -> German
TRANSLATIONS = {
    "Draft": "Entwurf",
    "Sent": "Versendet",
    "Paid": "Bezahlt",
    "Planned": "Geplant",
    "Taught": "Unterrichtet",
    "Cancelled": "Ausgefallen",
    "Name of the payer": "Name des Zahlungspflichtigen",
    "Address of the payer": "Adresse des Zahlungspflichtigen",
    "Associated contract (optional)": "Zugehöriger Vertrag (optional)",
    "Billing period start": "Beginn des Abrechnungszeitraums",
    "Billing period end": "Ende des Abrechnungszeitraums",
    "Invoice status": "Status der Rechnung",
    "Total invoice amount": "Gesamtbetrag der Rechnung",
    "Generated invoice document (HTML/PDF)": "Generiertes Rechnungsdokument (HTML/PDF)",
    "Invoice": "Rechnung",
    "Invoices": "Rechnungen",
    "Associated invoice": "Zugehörige Rechnung",
    "Associated lesson (may be deleted later)": "Zugehörige Lesson (kann später gelöscht werden)",
    "Item description": "Beschreibung des Postens",
    "Lesson date (copy)": "Datum der Unterrichtsstunde (Kopie)",
    "Duration in minutes (copy)": "Dauer in Minuten (Kopie)",
    "Amount for this item": "Betrag für diesen Posten",
    "Invoice Item": "Rechnungsposten",
    "Invoice Items": "Rechnungsposten",
    "Dashboard": "Dashboard",
    "Students": "Schüler",
    "Contracts": "Verträge",
    "Calendar": "Kalender",
    "Income": "Einnahmen",
    "Admin": "Admin",
    "Week View": "Wochenansicht",
    "Previous Week": "Vorige Woche",
    "Next Week": "Nächste Woche",
    "Create Recurring Lesson": "Serientermin anlegen",
    "Create Recurring Blocked Time": "Serien-Blockzeit erstellen",
    "Note:": "Hinweis:",
    "Drag a time range in the calendar to create a new appointment. Click on an existing appointment to edit it.": "Ziehen Sie einen Zeitbereich im Kalender, um einen neuen Termin anzulegen. Klicken Sie auf einen bestehenden Termin, um ihn zu bearbeiten.",
    "Time": "Zeit",
    "Create New Appointment": "Neuen Termin erstellen",
    "Tutoring Lesson": "Nachhilfeunterricht",
    "Blocked Time/Other Appointment": "Blockzeit/anderer Termin",
    "Create": "Erstellen",
    "Cancel": "Abbrechen",
    "Today's Lessons": "Heutige Stunden",
    "Student": "Schüler",
    "Status": "Status",
    "Conflicts": "Konflikte",
    "OK": "OK",
    "No lessons scheduled for today.": "Keine Stunden für heute geplant.",
    "Upcoming Lessons (7 days)": "Nächste Stunden (7 Tage)",
    "Date": "Datum",
    "No upcoming lessons.": "Keine kommenden Stunden.",
    "Paid:": "Ausgezahlt:",
    "lesson": "Stunde",
    "lessons": "Stunden",
    "conflict": "Konflikt",
    "conflicts": "Konflikte",
    "conflict in upcoming lessons!": "Konflikt in den nächsten Stunden!",
    "conflicts in upcoming lessons!": "Konflikte in den nächsten Stunden!",
    "Lessons": "Unterrichtsstunden",
    "New Lesson": "Neue Stunde",
    "Month View": "Monatsansicht",
    "Actions": "Aktionen",
    "Details": "Details",
    "Edit": "Bearbeiten",
    "No lessons available.": "Keine Stunden vorhanden.",
    "LLM_API_KEY is not configured. Please set the LLM_API_KEY environment variable.": "LLM_API_KEY ist nicht konfiguriert. Bitte setze die Umgebungsvariable LLM_API_KEY.",
    "LLM error: {error}": "LLM-Fehler: {error}",
    "Unexpected API response format": "Unerwartetes API-Response-Format",
    "API timeout after {seconds} seconds": "API-Timeout nach {seconds} Sekunden",
    "API error: {error}": "API-Fehler: {error}",
    "Error parsing API response: {error}": "Fehler beim Parsen der API-Antwort: {error}",
    # Add more translations as needed
}

def fill_translations(po_file_path):
    """Fill German translations in a .po file."""
    po_file = Path(po_file_path)
    if not po_file.exists():
        print(f"Error: {po_file_path} does not exist")
        return False
    
    content = po_file.read_text(encoding='utf-8')
    
    # Pattern to match msgid and msgstr pairs
    pattern = r'msgid "([^"]+)"\nmsgstr ""'
    
    def replace_func(match):
        english_text = match.group(1)
        if english_text in TRANSLATIONS:
            german_text = TRANSLATIONS[english_text]
            return f'msgid "{english_text}"\nmsgstr "{german_text}"'
        return match.group(0)
    
    new_content = re.sub(pattern, replace_func, content)
    
    # Also handle multi-line msgid (for blocktrans)
    # This is a simplified version - may need refinement
    po_file.write_text(new_content, encoding='utf-8')
    print(f"Updated {po_file_path}")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        po_file = Path(__file__).parent.parent / 'locale' / 'de' / 'LC_MESSAGES' / 'django.po'
    else:
        po_file = Path(sys.argv[1])
    
    fill_translations(po_file)

