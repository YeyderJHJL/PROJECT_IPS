from django.shortcuts import render, get_object_or_404
from .models import *
# Create your views here.

def index(request):
    return render(request, 'index.html')

def productos(request):
    producto= Producto.objects.all()
    data={
        'producto':producto
    }
    return render (request, 'productos.html', data)

def detalle_producto(request, procod):
    producto = get_object_or_404(Producto, procod=procod)
    return render(request, 'detalle_producto.html', {'producto': producto})