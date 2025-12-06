"""
Management command to update past planned lessons to taught status.

Usage:
    python manage.py update_past_lessons

This command automatically sets all lessons with status 'planned' to 'taught'
if their end time is in the past. Lessons with status 'paid' or 'cancelled'
are not modified.
"""

from apps.lessons.status_service import LessonStatusUpdater
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Updates past planned lessons to taught status"

    def handle(self, *args, **options):
        self.stdout.write("Updating past planned lessons to taught...")

        updated_count = LessonStatusUpdater.update_past_lessons_to_taught()

        if updated_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully updated {updated_count} lesson(s) to taught status."
                )
            )
        else:
            self.stdout.write(self.style.SUCCESS("No lessons needed to be updated."))
