from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from .models import EstadoPersonal, Personal, TipoPersonal
from .forms import PersonalForm, EstadoRegistroForm, TipoPersonalForm  # Asegúrate de que el nombre de la forma esté corregido

# Create your views here.

def index(request):
    return render(request, 'index.html')

def gestion_personal(request):
    return render(request, 'gestion_personal.html')

def personal_list(request):
    personal = Personal.objects.all()
    return render(request, 'personal_list.html', {'personal': personal})

def personal_add(request):
    if request.method == 'POST':
        form = PersonalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('personal_list')
    else:
        form = PersonalForm()
    return render(request, 'personal_form.html', {'form': form, 'return_url': 'personal_list', 'title': 'Adicionar Personal'})

def personal_edit(request, pk):
    personal = get_object_or_404(Personal, pk=pk)
    if request.method == 'POST':
        form = PersonalForm(request.POST, instance=personal)
        if form.is_valid():
            form.save()
            return redirect('personal_list')
    else:
        form = PersonalForm(instance=personal)
    return render(request, 'personal_form.html', {'form': form, 'return_url': 'personal_list', 'title': 'Modificar Personal'})

def personal_delete(request, pk):
    personal = get_object_or_404(Personal, pk=pk)
    if request.method == 'POST':
        try:
            personal.delete()
            return redirect('personal_list')
        except IntegrityError:
            return render(request, 'personal_confirm_delete.html', {'personal': personal, 'error': "No se puede eliminar el personal porque tiene dependencias asociadas."})
    return render(request, 'personal_confirm_delete.html', {'personal': personal})

# Estado Personal CRUD
def estado_personal_list(request):
    estados = EstadoPersonal.objects.all()
    return render(request, 'estado_personal_list.html', {'estados': estados})

def estado_personal_add(request):
    if request.method == 'POST':
        form = EstadoRegistroForm(request.POST)  # Asegúrate de que el nombre de la forma sea el correcto
        if form.is_valid():
            form.save()
            return redirect('estado_personal_list')
    else:
        form = EstadoRegistroForm()
    return render(request, 'form.html', {'form': form, 'return_url': 'estado_personal_list', 'title': 'Adicionar Estado Personal'})

def estado_personal_edit(request, pk):
    estado = get_object_or_404(EstadoPersonal, pk=pk)
    if request.method == 'POST':
        form = EstadoRegistroForm(request.POST, instance=estado)  # Asegúrate de que el nombre de la forma sea el correcto
        if form.is_valid():
            form.save()
            return redirect('estado_personal_list')
    else:
        form = EstadoRegistroForm(instance=estado)
    return render(request, 'form.html', {'form': form, 'return_url': 'estado_personal_list', 'title': 'Modificar Estado Personal'})

def estado_personal_delete(request, pk):
    estado = get_object_or_404(EstadoPersonal, pk=pk)
    if request.method == 'POST':
        estado.delete()
        return redirect('estado_personal_list')
    return render(request, 'estado_personal_confirm_delete.html', {'estado': estado})

# Tipo Personal CRUD
def tipo_personal_list(request):
    tipos = TipoPersonal.objects.all()
    return render(request, 'tipo_personal_list.html', {'tipos': tipos})

def tipo_personal_add(request):
    if request.method == 'POST':
        form = TipoPersonalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tipo_personal_list')
    else:
        form = TipoPersonalForm()
    return render(request, 'form.html', {'form': form, 'return_url': 'tipo_personal_list', 'title': 'Adicionar Tipo Personal'})

def tipo_personal_edit(request, pk):
    tipo = get_object_or_404(TipoPersonal, pk=pk)
    if request.method == 'POST':
        form = TipoPersonalForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            return redirect('tipo_personal_list')
    else:
        form = TipoPersonalForm(instance=tipo)
    return render(request, 'form.html', {'form': form, 'return_url': 'tipo_personal_list', 'title': 'Modificar Tipo Personal'})

def tipo_personal_delete(request, pk):
    tipo = get_object_or_404(TipoPersonal, pk=pk)
    if request.method == 'POST':
        tipo.delete()
        return redirect('tipo_personal_list')
    return render(request, 'tipo_personal_confirm_delete.html', {'tipo': tipo})

def toggle_personal_status(request, pk):
    personal = get_object_or_404(Personal, pk=pk)
    activo_estado = EstadoPersonal.objects.get(estregnom='Activo')
    inactivo_estado = EstadoPersonal.objects.get(estregnom='Inactivo')
    personal.estregcod = inactivo_estado if personal.estregcod == activo_estado else activo_estado  # Asegúrate de que el campo sea `estregcod`
    personal.save()
    return redirect('personal_list')
