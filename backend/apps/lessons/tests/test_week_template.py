from pathlib import Path

from django.test import SimpleTestCase


class WeekTemplateTest(SimpleTestCase):
    def test_note_text_mentions_click_instead_of_drag(self):
        template_path = Path(__file__).resolve().parents[1] / "templates" / "lessons" / "week.html"
        content = template_path.read_text()
        self.assertIn(
            "Lessons and blocked times can be created by clicking in a time block",
            content,
        )
        self.assertNotIn("Drag a time range in the calendar", content)
