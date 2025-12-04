from django.test import TestCase
from apps.locations.models import Location
from apps.students.models import Student


class StudentModelTest(TestCase):
    """Tests für das Student-Model."""

    def setUp(self):
        """Set up test data."""
        self.location = Location.objects.create(
            name="Zuhause",
            address="Musterstraße 1, 12345 Musterstadt"
        )

    def test_create_student(self):
        """Test: Student kann erstellt werden."""
        student = Student.objects.create(
            first_name="Max",
            last_name="Mustermann",
            email="max@example.com",
            school="Gymnasium XY",
            grade="10. Klasse",
            subjects="Mathe, Deutsch",
            default_location=self.location
        )
        self.assertEqual(student.full_name, "Max Mustermann")
        self.assertEqual(str(student), "Max Mustermann")
        self.assertEqual(student.default_location, self.location)

    def test_student_relationship_to_location(self):
        """Test: Beziehung zwischen Student und Location."""
        student = Student.objects.create(
            first_name="Anna",
            last_name="Schmidt",
            default_location=self.location
        )
        self.assertEqual(self.location.students.first(), student)
