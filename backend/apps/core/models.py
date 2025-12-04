from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Erweiterung des Django-User-Models mit Premium-Flag."""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        help_text="Zugehöriger Django-User"
    )
    is_premium = models.BooleanField(
        default=False,
        help_text="Hat der Benutzer Premium-Zugang?"
    )
    premium_since = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Seit wann ist der Benutzer Premium-Mitglied?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Benutzerprofil'
        verbose_name_plural = 'Benutzerprofile'

    def __str__(self):
        premium_str = " (Premium)" if self.is_premium else ""
        return f"{self.user.username}{premium_str}"
