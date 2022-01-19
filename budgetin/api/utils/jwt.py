import jwt
import json

from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone


def generate_token(id, username):
    payload = {
        "id": id,
        "username": username,
        "iat": datetime.now(),
        "exp": datetime.now() + timedelta(hours=8),
    }
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_token(encoded_jwt):
    return jwt.decode(encoded_jwt, settings.SECRET_KEY, algorithms=["HS256"])
