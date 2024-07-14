from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib import messages
from .forms import *
# Create your views here.

def index(request):
    return render(request, 'index.html')

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

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado exitosamente.')
            return redirect('productos')
    else:
        form = ProductoForm()
    return render(request, 'formulario_producto.html', {'form': form, 'titulo': 'Agregar Producto'})

def editar_producto(request, procod):
    producto = get_object_or_404(Producto, procod=procod)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'formulario_producto.html', {'form': form, 'titulo': 'Editar Producto'})