from django.shortcuts import redirect
from django.urls import reverse
from .models import Cliente, Personal

class ClienteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cliente_id = request.session.get('cliente_id')
        if cliente_id:
            try:
                request.cliente = Cliente.objects.get(clidni=cliente_id)
            except Cliente.DoesNotExist:
                request.cliente = None
        else:
            request.cliente = None
        response = self.get_response(request)
        return response

class PersonalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        personal_id = request.session.get('personal_id')
        if personal_id:
            try:
                request.personal = Personal.objects.get(perdni=personal_id)
            except Personal.DoesNotExist:
                request.personal = None
        else:
            request.personal = None
        response = self.get_response(request)
        return response


class AdminRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and not (request.personal and request.personal.tippercod.tippernom == 'Administrador'):
            return redirect(reverse('personal_login'))
        response = self.get_response(request)
        return response
    
class VendedorRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/vendedor/') and not (request.personal and request.personal.tippercod.tippernom == 'Vendedor'):
            return redirect(reverse('personal_login')) 
        response = self.get_response(request)
        return response
    
class TecnicoRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/tecnico/') and not (request.personal and request.personal.tippercod.tippernom == 'Técnico'):
            return redirect(reverse('personal_login')) 
        response = self.get_response(request)
        return response
