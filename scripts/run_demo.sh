#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}/backend"

export MOCK_LLM="${MOCK_LLM:-1}"
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-tutorflow.settings}"

python manage.py migrate
python manage.py loaddata fixtures/demo_data.json
python manage.py compilemessages

# Stelle sicher, dass die Demo-User existieren und das Passwort gesetzt ist.
python manage.py shell <<'PY'
from django.contrib.auth.models import User
from apps.core.models import UserProfile

def ensure_user(username, email, is_premium):
    user, _ = User.objects.get_or_create(username=username, defaults={"email": email, "is_staff": True})
    user.set_password("demo123")
    user.is_staff = True
    user.save()
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.is_premium = is_premium
    profile.save()

ensure_user("demo_premium", "demo_premium@example.com", True)
ensure_user("demo_user", "demo_user@example.com", False)
PY

python manage.py runserver 0.0.0.0:8000

