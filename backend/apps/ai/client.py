"""
Low-Level-Client für LLM-API-Kommunikation.
"""
import json
import time
import logging
import requests
from typing import Optional, Dict, Any
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


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
        temperature: float = 0.7,
        max_retries: int = 2,
        retry_delay: int = 5
    ) -> str:
        """
        Generiert Text mit der LLM-API.
        
        Args:
            prompt: Der Haupt-Prompt
            system_prompt: Optionaler System-Prompt
            max_tokens: Maximale Anzahl Tokens
            temperature: Temperature für die Generierung
            max_retries: Maximale Anzahl Wiederholungsversuche bei Rate-Limit-Fehlern
            retry_delay: Wartezeit in Sekunden zwischen Wiederholungsversuchen
        
        Returns:
            Generierter Text
        
        Raises:
            LLMClientError: Bei API-Fehlern, Timeouts oder Netzwerkproblemen
        """
        if not self.api_key:
            raise LLMClientError(
                _("LLM_API_KEY is not configured. Please set the LLM_API_KEY environment variable.")
            )
        
        last_error = None
        for attempt in range(max_retries + 1):
            try:
                return self._make_api_request(prompt, system_prompt, max_tokens, temperature)
            except LLMClientError as e:
                last_error = e
                # Retry only for rate limit errors (429)
                error_msg = str(e)
                if "rate limit" in error_msg.lower() and attempt < max_retries:
                    wait_time = retry_delay * (attempt + 1)  # Exponential backoff
                    time.sleep(wait_time)
                    continue
                # For other errors or after max retries, raise immediately
                raise
        
        # Should not reach here, but just in case
        if last_error:
            raise last_error
    
    def _make_api_request(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """
        Führt einen einzelnen API-Request durch.
        
        Args:
            prompt: Der Haupt-Prompt
            system_prompt: Optionaler System-Prompt
            max_tokens: Maximale Anzahl Tokens
            temperature: Temperature für die Generierung
        
        Returns:
            Generierter Text
        
        Raises:
            LLMClientError: Bei API-Fehlern
        """
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
            
            # Log request details (without sensitive data)
            logger.debug(f"LLM API Request: URL={self.api_base_url}/chat/completions, Model={self.model_name}")
            
            response = requests.post(
                f"{self.api_base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            # Try to parse error response for better error messages
            error_details = None
            try:
                if response.status_code >= 400:
                    error_response = response.json()
                    if "error" in error_response:
                        error_details = error_response["error"]
                        if isinstance(error_details, dict):
                            error_msg = error_details.get("message", str(error_details))
                            error_type = error_details.get("type", "unknown")
                            logger.error(f"LLM API Error: Status={response.status_code}, Type={error_type}, Message={error_msg}")
                        else:
                            error_msg = str(error_details)
                            logger.error(f"LLM API Error: Status={response.status_code}, Error={error_msg}")
            except (ValueError, KeyError):
                # If we can't parse the error response, use the raw text
                error_details = response.text[:500]  # Limit to 500 chars
                logger.error(f"LLM API Error: Status={response.status_code}, Response={error_details}")
            
            # Handle specific HTTP status codes
            if response.status_code == 429:
                # Rate limit exceeded
                error_msg = _("API rate limit exceeded. Please try again in a few minutes.")
                if error_details and isinstance(error_details, dict) and "message" in error_details:
                    error_msg = _("API rate limit exceeded: {details}").format(details=error_details.get("message", ""))
                raise LLMClientError(error_msg)
            elif response.status_code == 401:
                # Unauthorized - invalid API key
                error_msg = _("Invalid API key. Please check your LLM_API_KEY configuration.")
                if error_details and isinstance(error_details, dict) and "message" in error_details:
                    error_msg = _("Invalid API key: {details}").format(details=error_details.get("message", ""))
                raise LLMClientError(error_msg)
            elif response.status_code == 402:
                # Payment required
                error_msg = _("Payment required. Please check your API account balance.")
                if error_details and isinstance(error_details, dict) and "message" in error_details:
                    error_msg = _("Payment required: {details}").format(details=error_details.get("message", ""))
                raise LLMClientError(error_msg)
            elif response.status_code >= 400:
                # Other 4xx/5xx errors
                if error_details and isinstance(error_details, dict) and "message" in error_details:
                    error_msg = error_details.get("message", _("API error occurred"))
                    error_type = error_details.get("type", "unknown")
                    raise LLMClientError(_("API error ({type}): {message}").format(type=error_type, message=error_msg))
                else:
                    raise LLMClientError(_("API error: HTTP {status} - {details}").format(
                        status=response.status_code,
                        details=error_details or response.text[:200]
                    ))
            
            response.raise_for_status()
            result = response.json()
            
            # Extrahiere generierten Text
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                raise LLMClientError(_("Unexpected API response format"))
        
        except requests.exceptions.Timeout:
            raise LLMClientError(_("API timeout after {seconds} seconds").format(seconds=self.timeout))
        except requests.exceptions.HTTPError as e:
            # Handle other HTTP errors
            if e.response.status_code == 429:
                raise LLMClientError(
                    _("API rate limit exceeded. Please try again in a few minutes.")
                )
            raise LLMClientError(_("API error: {error}").format(error=str(e)))
        except requests.exceptions.RequestException as e:
            raise LLMClientError(_("API error: {error}").format(error=str(e)))
        except (KeyError, ValueError) as e:
            raise LLMClientError(_("Error parsing API response: {error}").format(error=str(e)))

