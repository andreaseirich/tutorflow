# Datenbank zurücksetzen

## Datenbank neu erstellen

Falls die Datenbank gelöscht wurde:

```bash
cd backend
python manage.py migrate
```

## Demo-Daten löschen (behält Admin-User)

Um alle Demo-Daten (Schüler, Stunden, Verträge, Rechnungen) zu löschen, aber Admin-User zu behalten:

```bash
cd backend
python manage.py clear_demo_data --confirm
```

Dieses Command löscht:
- ✅ Alle Schüler (Students)
- ✅ Alle Verträge (Contracts)
- ✅ Alle Stunden (Lessons)
- ✅ Alle Blockzeiten (BlockedTimes)
- ✅ Alle Rechnungen (Invoices)
- ✅ Alle Lesson Plans

Behält:
- ✅ Admin-User (is_staff=True)
- ✅ System-Einstellungen

## Demo-Daten neu laden

Nach dem Löschen können Sie Demo-Daten neu laden:

```bash
python manage.py seed_demo_data
```
