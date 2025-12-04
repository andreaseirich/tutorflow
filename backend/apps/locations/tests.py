from django.test import TestCase
from apps.locations.models import Location


class LocationModelTest(TestCase):
    """Tests für das Location-Model."""

    def test_create_location(self):
        """Test: Location kann erstellt werden."""
        location = Location.objects.create(
            name="Zuhause",
            address="Musterstraße 1, 12345 Musterstadt"
        )
        self.assertEqual(location.name, "Zuhause")
        self.assertEqual(str(location), "Zuhause (Musterstraße 1, 12345 Musterstadt)")

    def test_location_with_coordinates(self):
        """Test: Location mit Koordinaten kann erstellt werden."""
        location = Location.objects.create(
            name="Schule XY",
            address="Schulstraße 5, 12345 Musterstadt",
            latitude=52.5200,
            longitude=13.4050
        )
        self.assertEqual(float(location.latitude), 52.5200)
        self.assertEqual(float(location.longitude), 13.4050)
