# backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Cliente

class ClienteBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            cliente = Cliente.objects.get(cliusu=username)
            if cliente.clicon == password:  # Verifica la contraseña
                return cliente
        except Cliente.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Cliente.objects.get(pk=user_id)
        except Cliente.DoesNotExist:
            return None
