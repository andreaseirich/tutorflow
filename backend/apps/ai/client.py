"""
Low-Level-Client für LLM-API-Kommunikation.
"""
import json
import requests
from typing import Optional, Dict, Any
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _


class LLMClientError(Exception):
    """Basis-Exception für LLM-Client-Fehler."""
    pass


class LLMClient:
    """Client für die Kommunikation mit einer LLM-API (z. B. OpenAI)."""
    
    def __init__(self):
        """Initialisiert den LLM-Client mit Konfiguration aus Settings."""
        self.api_base_url = settings.LLM_API_BASE_URL
        self.api_key = settings.LLM_API_KEY
        self.model_name = settings.LLM_MODEL_NAME
        self.timeout = settings.LLM_TIMEOUT_SECONDS
        
        if not self.api_key:
            # In Entwicklung/Demo kann API_KEY leer sein (wird in Tests gemockt)
            pass
    
    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """
        Generiert Text mit der LLM-API.
        
        Args:
            prompt: Der Haupt-Prompt
            system_prompt: Optionaler System-Prompt
            max_tokens: Maximale Anzahl Tokens
            temperature: Temperature für die Generierung
        
        Returns:
            Generierter Text
        
        Raises:
            LLMClientError: Bei API-Fehlern, Timeouts oder Netzwerkproblemen
        """
        if not self.api_key:
            raise LLMClientError(
                _("LLM_API_KEY is not configured. Please set the LLM_API_KEY environment variable.")
            )
        
        try:
            # OpenAI-kompatibles Format
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            payload = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            response = requests.post(
                f"{self.api_base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extrahiere generierten Text
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                raise LLMClientError(_("Unexpected API response format"))
        
        except requests.exceptions.Timeout:
            raise LLMClientError(_("API timeout after {seconds} seconds").format(seconds=self.timeout))
        except requests.exceptions.RequestException as e:
            raise LLMClientError(_("API error: {error}").format(error=str(e)))
        except (KeyError, ValueError) as e:
            raise LLMClientError(_("Error parsing API response: {error}").format(error=str(e)))

