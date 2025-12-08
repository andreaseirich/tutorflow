from apps.ai.utils_safety import REDACTED, sanitize_context
from django.test import SimpleTestCase


class SanitizeContextTest(SimpleTestCase):
    """Tests für den PII-Sanitizer."""

    def test_sanitize_context_removes_pii(self):
        ctx = {
            "student": {
                "full_name": "John Doe",
                "email": "john@example.com",
                "subjects": "Math",
                "notes": "Needs focus",
            },
            "lesson": {"notes": "harmless"},
            "list": [{"phone": "12345", "notes": "ok"}],
        }

        sanitized = sanitize_context(ctx)

        self.assertEqual(sanitized["student"]["full_name"], REDACTED)
        self.assertEqual(sanitized["student"]["email"], REDACTED)
        self.assertEqual(sanitized["student"]["subjects"], "Math")
        self.assertEqual(sanitized["list"][0]["phone"], REDACTED)
