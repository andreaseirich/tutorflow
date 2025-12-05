"""
Template-Filter für Währungsformatierung.
"""
from django import template
from decimal import Decimal

register = template.Library()


@register.filter(name='euro')
def euro(value):
    """
    Formatiert einen Decimal-Wert als Euro-Betrag mit 2 Nachkommastellen.
    
    Beispiele:
        Decimal('90') -> "90,00 €"
        Decimal('544') -> "544,00 €"
        Decimal('90.5') -> "90,50 €"
        Decimal('1234.56') -> "1.234,56 €"
    """
    if value is None:
        return "0,00 €"
    
    # Konvertiere zu Decimal, falls nötig
    if not isinstance(value, Decimal):
        try:
            value = Decimal(str(value))
        except (ValueError, TypeError):
            return "0,00 €"
    
    # Formatiere mit 2 Nachkommastellen
    formatted = f"{value:.2f}"
    
    # Ersetze Punkt durch Komma (Dezimaltrennzeichen)
    formatted = formatted.replace('.', ',')
    
    # Füge Tausenderpunkte hinzu (von rechts nach links)
    parts = formatted.split(',')
    integer_part = parts[0]
    
    # Füge Tausenderpunkte hinzu
    if len(integer_part) > 3:
        integer_part = f"{int(integer_part):,}".replace(',', '.')
    
    formatted = f"{integer_part},{parts[1]}"
    
    # Füge Währungssymbol mit Leerzeichen hinzu
    return f"{formatted} €"

