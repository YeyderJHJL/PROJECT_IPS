from .models import Cliente

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
