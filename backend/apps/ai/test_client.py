"""
Tests für LLM-Client (mit Mock-Requests).
"""
from django.test import TestCase
from unittest.mock import patch, Mock
from django.conf import settings
from apps.ai.client import LLMClient, LLMClientError


class LLMClientTest(TestCase):
    """Tests für LLM-Client."""
    
    def setUp(self):
        """Set up test data."""
        # Temporäre Settings für Tests
        self.original_key = settings.LLM_API_KEY
        settings.LLM_API_KEY = 'test-key'
    
    def tearDown(self):
        """Restore original settings."""
        settings.LLM_API_KEY = self.original_key
    
    @patch('apps.ai.client.requests.post')
    def test_generate_text_success(self, mock_post):
        """Test: Erfolgreiche Text-Generierung."""
        # Mock API-Response
        mock_response = Mock()
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': 'Test generierter Text'
                }
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        client = LLMClient()
        result = client.generate_text("Test-Prompt")
        
        self.assertEqual(result, 'Test generierter Text')
        mock_post.assert_called_once()
    
    @patch('apps.ai.client.requests.post')
    def test_generate_text_timeout(self, mock_post):
        """Test: Timeout-Fehlerbehandlung."""
        import requests
        mock_post.side_effect = requests.exceptions.Timeout()
        
        client = LLMClient()
        
        with self.assertRaises(LLMClientError) as context:
            client.generate_text("Test-Prompt")
        
        self.assertIn("Timeout", str(context.exception))
    
    @patch('apps.ai.client.requests.post')
    def test_generate_text_api_error(self, mock_post):
        """Test: API-Fehlerbehandlung."""
        import requests
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")
        
        client = LLMClient()
        
        with self.assertRaises(LLMClientError) as context:
            client.generate_text("Test-Prompt")
        
        self.assertIn("API-Fehler", str(context.exception))
    
    def test_generate_text_no_api_key(self):
        """Test: Fehler wenn API-Key fehlt."""
        settings.LLM_API_KEY = ''
        
        client = LLMClient()
        
        with self.assertRaises(LLMClientError) as context:
            client.generate_text("Test-Prompt")
        
        self.assertIn("LLM_API_KEY", str(context.exception))

