# utils.py

from itsdangerous import URLSafeTimedSerializer
from django.conf import settings

def generate_token(cliente):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(cliente.clidni, salt=settings.SECURITY_PASSWORD_SALT)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        clidni = serializer.loads(
            token,
            salt=settings.SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False
    return clidni
