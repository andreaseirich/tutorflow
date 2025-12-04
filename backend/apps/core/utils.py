"""
Utility-Funktionen für Core-Funktionalität.
"""
from django.contrib.auth.models import User


def is_premium_user(user: User) -> bool:
    """
    Prüft, ob ein User Premium-Zugang hat.
    
    Args:
        user: Django User-Objekt
    
    Returns:
        True wenn Premium, sonst False
    """
    if not user or not user.is_authenticated:
        return False
    
    try:
        return user.profile.is_premium
    except AttributeError:
        # Falls kein Profile existiert, erstelle es
        from apps.core.models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=user)
        return profile.is_premium

