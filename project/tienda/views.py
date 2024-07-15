from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib import messages

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

def productos(request):
    categorias = CategoariaProducto.objects.all()  
    productos = Producto.objects.all()  
    
    categoria_id = request.GET.get('categoria')  
    if categoria_id:
        productos = productos.filter(catprocod=categoria_id)  
    
    context = {
        'categorias': categorias,
        'producto': productos,
    }
    return render(request, 'productos.html', context)

def detalle_producto(request, procod):
    producto = get_object_or_404(Producto, procod=procod)
    return render(request, 'detalle_producto.html', {'producto': producto})
