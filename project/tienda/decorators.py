from django.shortcuts import redirect
from django.contrib import messages

def cliente_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.cliente:
            messages.warning(request, 'Para esta acción necesitas tener una cuenta y estar logueado.')
            return redirect('cliente_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
