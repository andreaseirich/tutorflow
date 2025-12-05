"""
Template-Filter für Währungsformatierung mit Lokalisierung.
"""
from django import template
from django.utils import numberformat
from django.utils.translation import get_language
from decimal import Decimal

register = template.Library()


@register.filter(name='euro')
def euro(value):
    """
    Formatiert einen Decimal-Wert als Euro-Betrag mit 2 Nachkommastellen.
    Berücksichtigt die aktuelle Sprache für Dezimal- und Tausendertrennzeichen.
    
    Beispiele (DE):
        Decimal('90') -> "90,00 €"
        Decimal('1234.56') -> "1.234,56 €"
    
    Beispiele (EN):
        Decimal('90') -> "90.00 €"
        Decimal('1234.56') -> "1,234.56 €"
    """
    if value is None:
        lang = get_language()
        if lang == 'de':
            return "0,00 €"
        else:
            return "0.00 €"
    
    # Konvertiere zu Decimal, falls nötig
    if not isinstance(value, Decimal):
        try:
            value = Decimal(str(value))
        except (ValueError, TypeError):
            lang = get_language()
            if lang == 'de':
                return "0,00 €"
            else:
                return "0.00 €"
    
    lang = get_language()
    
    # Formatiere mit 2 Nachkommastellen
    formatted = f"{value:.2f}"
    
    # Trenne Integer- und Dezimalteil
    parts = formatted.split('.')
    integer_part = parts[0]
    decimal_part = parts[1] if len(parts) > 1 else '00'
    
    # Füge Tausendertrennzeichen hinzu
    if len(integer_part) > 3:
        integer_part = f"{int(integer_part):,}"
    
    # Formatiere je nach Sprache
    if lang == 'de':
        # Deutsch: Punkt als Tausendertrennzeichen, Komma als Dezimaltrennzeichen
        integer_part = integer_part.replace(',', '.')
        formatted = f"{integer_part},{decimal_part}"
    else:
        # Englisch: Komma als Tausendertrennzeichen, Punkt als Dezimaltrennzeichen
        formatted = f"{integer_part}.{decimal_part}"
    
    # Füge Währungssymbol mit Leerzeichen hinzu
    return f"{formatted} €"

