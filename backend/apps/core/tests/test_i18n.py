"""
Tests for internationalization (i18n) functionality.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import activate, get_language


class I18nTestCase(TestCase):
    """Test cases for i18n functionality."""
    
    def setUp(self):
        """Set up test client."""
        self.client = Client()
    
    def test_default_language_is_english(self):
        """Test that default language is English."""
        from django.conf import settings
        self.assertEqual(settings.LANGUAGE_CODE, 'en')
    
    def test_language_switching(self):
        """Test that language switching works."""
        # Test English (default)
        activate('en')
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.content)
        
        # Test German
        activate('de')
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 200)
        # Should contain German text if translations are loaded
        # Note: This test may need adjustment based on actual template content
    
    def test_set_language_view(self):
        """Test the set_language view."""
        # Test switching to German
        response = self.client.post(
            reverse('set_language'),
            {'language': 'de'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        
        # Test switching back to English
        response = self.client.post(
            reverse('set_language'),
            {'language': 'en'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
    
    def test_base_template_has_language_switcher(self):
        """Test that base template includes language switcher."""
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 200)
        # Check for language switcher form
        self.assertIn(b'set_language', response.content)
        self.assertIn(b'language', response.content)
    
    def test_english_texts_in_templates(self):
        """Test that templates use English as primary language."""
        activate('en')
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 200)
        # Check for English text
        self.assertIn(b'Dashboard', response.content)
        self.assertIn(b'Students', response.content)
        self.assertIn(b'Calendar', response.content)

