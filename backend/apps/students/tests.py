from apps.students.models import Student
from django.test import TestCase


class StudentModelTest(TestCase):
    """Tests für das Student-Model."""

    def test_create_student(self):
        """Test: Student kann erstellt werden."""
        student = Student.objects.create(
            first_name="Max",
            last_name="Mustermann",
            email="max@example.com",
            school="Gymnasium XY",
            grade="10. Klasse",
            subjects="Mathe, Deutsch",
        )
        self.assertEqual(student.full_name, "Max Mustermann")
        self.assertEqual(str(student), "Max Mustermann")
