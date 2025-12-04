"""
Prompt-Bau für LessonPlan-Generierung.
"""
from typing import Dict, Any
from apps.lessons.models import Lesson


def build_lesson_plan_prompt(lesson: Lesson, context: Dict[str, Any]) -> tuple[str, str]:
    """
    Baut System- und User-Prompt für die LessonPlan-Generierung.
    
    Args:
        lesson: Lesson-Objekt
        context: Zusätzlicher Kontext (z. B. vorherige Lessons, Notizen)
    
    Returns:
        Tuple (system_prompt, user_prompt)
    """
    student = lesson.contract.student
    contract = lesson.contract
    
    # System-Prompt: Rolle und Aufgabe
    system_prompt = """Du bist ein erfahrener Nachhilfelehrer, der strukturierte Unterrichtspläne erstellt.
Erstelle einen klaren, praxisorientierten Unterrichtsplan für eine Nachhilfestunde.
Der Plan soll:
- Eine klare Struktur haben (Einstieg, Hauptteil, Abschluss)
- Konkrete Übungen und Aufgaben enthalten
- Auf die Bedürfnisse des Schülers eingehen
- Realistisch für die verfügbare Zeit sein"""
    
    # User-Prompt: Kontext und Details
    user_prompt_parts = [
        f"Erstelle einen Unterrichtsplan für eine Nachhilfestunde:",
        f"",
        f"**Schüler:**",
        f"- Name: {student.first_name} {student.last_name}",
    ]
    
    if student.grade:
        user_prompt_parts.append(f"- Klasse: {student.grade}")
    
    if student.subjects:
        # Versuche das Fach aus den Subjects zu extrahieren
        subjects = student.subjects.split(',')
        subject = subjects[0].strip() if subjects else "Allgemein"
        user_prompt_parts.append(f"- Fach: {subject}")
    
    user_prompt_parts.extend([
        f"",
        f"**Unterrichtsstunde:**",
        f"- Datum: {lesson.date}",
        f"- Dauer: {lesson.duration_minutes} Minuten",
        f"- Status: {lesson.get_status_display()}",
    ])
    
    if lesson.notes:
        user_prompt_parts.extend([
            f"- Notizen: {lesson.notes}",
        ])
    
    # Kontext aus vorherigen Lessons
    if context.get('previous_lessons'):
        user_prompt_parts.extend([
            f"",
            f"**Vorherige Stunden:**",
        ])
        for prev_lesson in context['previous_lessons'][:3]:  # Max 3 vorherige
            user_prompt_parts.append(
                f"- {prev_lesson.date}: {prev_lesson.notes or 'Keine Notizen'}"
            )
    
    if student.notes:
        user_prompt_parts.extend([
            f"",
            f"**Schüler-Notizen:** {student.notes}",
        ])
    
    user_prompt_parts.extend([
        f"",
        f"Erstelle einen strukturierten Unterrichtsplan für diese Stunde.",
    ])
    
    user_prompt = "\n".join(user_prompt_parts)
    
    return system_prompt, user_prompt


def extract_subject_from_student(student) -> str:
    """
    Extrahiert das Hauptfach aus den Student-Subjects.
    
    Args:
        student: Student-Objekt
    
    Returns:
        Fach-String (z. B. "Mathe", "Deutsch")
    """
    if not student.subjects:
        return "Allgemein"
    
    subjects = student.subjects.split(',')
    return subjects[0].strip() if subjects else "Allgemein"

