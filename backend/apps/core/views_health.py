from django.http import JsonResponse


def health_status(request):
    """Lightweight Health-Check-Endpunkt."""
    return JsonResponse({"status": "ok"})

