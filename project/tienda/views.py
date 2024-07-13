from django.shortcuts import render
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