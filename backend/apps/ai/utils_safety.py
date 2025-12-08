"""
Hilfsfunktionen für Privacy/PII-Schutz im AI-Kontext.
"""

from copy import deepcopy
from typing import Any, Dict

PII_KEYS = {"full_name", "address", "email", "phone", "tax_id", "dob", "medical_info"}
REDACTED = "[REDACTED]"


def _sanitize_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: (REDACTED if key in PII_KEYS else _sanitize_value(val))
            for key, val in value.items()
        }
    if isinstance(value, list):
        return [_sanitize_value(item) for item in value]
    return value


def sanitize_context(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entfernt oder pseudonymisiert PII aus einem Kontext-Dict.

    Bekannte PII-Felder werden durch "[REDACTED]" ersetzt.
    """
    safe_copy = deepcopy(ctx)
    return _sanitize_value(safe_copy)
