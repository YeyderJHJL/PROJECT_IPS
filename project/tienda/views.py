from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

# Create your views here.

def index(request):
    return render(request, 'index.html')

def servicios(request, codigo=None):
    instancia_clase = None
    servicio = Servicio.objects.all()

    # Obtener todas las categorías
    categorias = CategoariaServicio.objects.all()

    if codigo:
        instancia_clase = get_object_or_404(CategoariaServicio, catsercod=codigo)
        servicio = Servicio.objects.filter(categoaria_servicio_catsercod=codigo)

    if request.method == 'POST':
        formulario = CategoriaServicioForm(request.POST, instance=instancia_clase)
        if formulario.is_valid():
            formulario.save()
            return redirect('servicios')
    else:
        formulario = CategoriaServicioForm(instance=instancia_clase)

    return render(request, 'servicios.html', {'formulario': formulario, 'servicio': servicio, 'categorias': categorias})

@login_required
def crear_evento(request):
    servicio_id = request.GET.get('servicio_id') 

    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index') 
    else:
        servicio = None
        if servicio_id:
            try:
                servicio = Servicio.objects.get(pk=servicio_id)
            except Servicio.DoesNotExist:
                servicio = None

        form = EventoForm()

    return render(request, 'reservaServicio.html', {'form': form, 'servicio': servicio})