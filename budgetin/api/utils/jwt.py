import jwt

from datetime import datetime, timedelta
from django.conf import settings


def generate_token(id, username, role, eselon):
    payload = {
        "id": id,
        "username": username,
        "role": role,
        "eselon": eselon,
        "iat": datetime.now(),
        "exp": datetime.now() + timedelta(hours=8),
    }
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_token(encoded_jwt):
    try:
        return jwt.decode(encoded_jwt, settings.SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return None
