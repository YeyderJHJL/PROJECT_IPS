from django.shortcuts import redirect, render
from .forms import EventoForm
from .models import *

# Create your views here.

def index(request):
    return render(request, 'index.html')

def servicios(request):
    servicio= Servicio.objects.all()
    data={
        'servicio':servicio
    }
    return render (request, 'servicios.html', data)

def crear_evento(request):
    servicio_id = request.GET.get('servicio_id')  # Obtener el ID del servicio desde la URL

    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirigir a una página de confirmación o de lista
    else:
        servicio = None
        if servicio_id:
            try:
                servicio = Servicio.objects.get(pk=servicio_id)
            except Servicio.DoesNotExist:
                servicio = None

        form = EventoForm()

    return render(request, 'reservaServicio.html', {'form': form, 'servicio': servicio})