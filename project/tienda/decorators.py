from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def cliente_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.cliente:
            messages.warning(request, 'Para esta acción necesitas tener una cuenta y estar logueado.')
            return redirect('cliente_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request, 'personal') and request.personal and request.personal.tippercod.tippernom == 'Administrador':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('personal_login')
    return _wrapped_view

def vendedor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request, 'personal') and request.personal and request.personal.tippercod.tippernom == 'Vendedor':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('personal_login')
    return _wrapped_view

def tecnico_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request, 'personal') and request.personal and request.personal.tippercod.tippernom == 'Técnico':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('personal_login') 
    return _wrapped_view

def multi_role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request, 'personal') and request.personal and request.personal.tippercod.tippernom in roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('personal_login') 
        return _wrapped_view
    return decorator