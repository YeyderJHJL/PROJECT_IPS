from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from .models import EstadoRegistro, Personal, TipoPersonal
from .forms import EstadoRegistroForm, LoginPersonalForm, PersonalForm, TipoPersonalForm  
from django.contrib.auth import authenticate, login

# Create your views here.

def index(request):
    return render(request, 'index.html')

def gestion_personal(request):
    return render(request, 'gestion_personal.html')

# Estado Registro CRUD
def estado_registro_list(request):
    estados = EstadoRegistro.objects.all()
    return render(request, 'estado_registro_list.html', {'estados': estados})

def estado_registro_add(request):
    if request.method == 'POST':
        form = EstadoRegistroForm(request.POST)
        if form.is_valid():
            estado = form.save()
            return redirect('estado_registro_list')  # Redirigir a la lista de estados
    else:
        form = EstadoRegistroForm()
    return render(request, 'estado_registro_form.html', {'form': form, 'return_url': 'estado_registro_list', 'title': 'Agregar Estado de Registro'})

def estado_registro_edit(request, pk):
    estado = get_object_or_404(EstadoRegistro, pk=pk)
    if request.method == 'POST':
        form = EstadoRegistroForm(request.POST, instance=estado)
        if form.is_valid():
            form.save()
            return redirect('estado_registro_list')
    else:
        form = EstadoRegistroForm(instance=estado)
    return render(request, 'estado_registro_form.html', {'form': form, 'return_url': 'estado_registro_list', 'title': 'Modificar Estado de Registro'})

def estado_registro_delete(request, pk):
    estado = get_object_or_404(EstadoRegistro, pk=pk)
    if request.method == 'POST':
        estado.delete()
        return redirect('estado_registro_list')
    return render(request, 'estado_registro_confirm_delete.html', {'estado': estado})

# Login Personal
def login_personal(request):
    if request.method == 'POST':
        form = LoginPersonalForm(request.POST)
        if form.is_valid():
            personal = form.get_personal()
            tipo_personal = personal.tippercod.tippernom  # Suponiendo que el campo es tippernom en TipoPersonal
            if tipo_personal == 'Técnico':
                return redirect('inicio_tecnico')
            elif tipo_personal == 'Vendedor':
                return redirect('inicio_vendedor')
            elif tipo_personal == 'Administrador':
                return redirect('inicio_administrador')
            else:
                form.add_error(None, 'Tipo de personal no reconocido.')
    else:
        form = LoginPersonalForm()
    return render(request, 'login_personal.html', {'form': form})

def inicio_tecnico(request):
    return render(request, 'inicio_tecnico.html')

def inicio_vendedor(request):
    return render(request, 'inicio_vendedor.html')

def inicio_administrador(request):
    return render(request, 'inicio_administrador.html')

# Personal CRUD
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

# Tipo Personal CRUD
def tipo_personal_list(request):
    tipos = TipoPersonal.objects.all()
    return render(request, 'tipo_personal_list.html', {'tipos': tipos})

def tipo_personal_add(request):
    if request.method == 'POST':
        form = TipoPersonalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tipo_personal_list')  # Redirige a la lista de tipos de personal
    else:
        form = TipoPersonalForm()
    return render(request, 'tipo_personal_form.html', {'form': form, 'title': 'Agregar Tipo de Personal', 'return_url': 'tipo_personal_list'})

def tipo_personal_edit(request, pk):
    tipo_personal = get_object_or_404(TipoPersonal, pk=pk)
    if request.method == 'POST':
        form = TipoPersonalForm(request.POST, instance=tipo_personal)
        if form.is_valid():
            form.save()
            return redirect('tipo_personal_list')  # Redirige a la lista de tipos de personal
    else:
        form = TipoPersonalForm(instance=tipo_personal)
    return render(request, 'tipo_personal_form.html', {'form': form, 'title': 'Modificar Tipo de Personal', 'return_url': 'tipo_personal_list'})

def tipo_personal_delete(request, pk):
    tipo = get_object_or_404(TipoPersonal, pk=pk)
    if request.method == 'POST':
        tipo.delete()
        return redirect('tipo_personal_list')
    return render(request, 'tipo_personal_confirm_delete.html', {'tipo': tipo})

def toggle_personal_status(request, pk):
    personal = get_object_or_404(Personal, pk=pk)
    activo_estado = EstadoRegistro.objects.get(estregnom='Activo')
    inactivo_estado = EstadoRegistro.objects.get(estregnom='Inactivo')
    personal.estregcod = inactivo_estado if personal.estregcod == activo_estado else activo_estado  
    personal.save()
    return redirect('personal_list')
