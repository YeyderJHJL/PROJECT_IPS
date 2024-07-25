from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.core.mail import send_mail
from django.db import IntegrityError
from .models import *
from .forms import *
import logging
from .utils import *
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .decorators import *
from django.db.models import Sum
from calendar import monthrange
from datetime import datetime
import datetime
# Create your views here.


# GENERAL ################################################

def index(request):
    return render(request, 'index.html')

def empresa(request):
    return render(request, './empresa.html')

def preguntas_frecuentes(request):
    return render(request, './preguntas_frecuentes.html')

#autenticación de login
def get_authenticated_cliente(request):
    cliente_id = request.session.get('cliente_id')
    if cliente_id:
        try:
            return Cliente.objects.get(pk=cliente_id)
        except Cliente.DoesNotExist:
            return None
    return None

def vendedor_home(request):
    return render(request, 'inicio_personal/vendedor_home.html')

#  FORMULARIO DE CONTACTO ################################################

# def contact_form(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             # Procesa el formulario, como enviar un correo electrónico
#             send_mail(
#                 'Nuevo mensaje de contacto',
#                 form.cleaned_data['message'],
#                 form.cleaned_data['email'],
#                 ['tu_email@example.com'],  # Cambia esto por tu dirección de correo
#             )
#             return redirect('contact_success')  # Redirige a una página de éxito
#     else:
#         form = ContactForm()
    
#     return render(request, 'consultas/contact_form.html', {'form': form})

# def contact_success(request):
#     return render(request, 'consultas/contact_success.html')

#  CONSULTAS ################################################

# Gestión Consulta
# personal
def gestion_consulta(request):
    consultas = Consulta.objects.all()
    return render(request, 'consultas/gestion_consulta.html', {'consultas': consultas})

# Consulta CRUD
# personal
def consulta_list(request):
    consultas = Consulta.objects.all()
    return render(request, 'consultas/consulta_list.html', {'consultas': consultas})

# personal
def consulta_edit(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            return redirect('gestion_consulta')
    else:
        form = ConsultaForm(instance=consulta)
    return render(request, 'consultas/consulta_form.html', {'form': form, 'return_url': 'gestion_consulta', 'title': 'Modificar Consulta'})

def consulta_delete(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        try:
            consulta.delete()
            return redirect('gestion_consulta')
        except IntegrityError:
            return render(request, 'consultas/consulta_confirm_delete.html', {'consulta': consulta, 'error': "No se puede eliminar la consulta porque tiene dependencias asociadas."})
    return render(request, 'consultas/consulta_confirm_delete.html', {'consulta': consulta})

@cliente_login_required
def consulta_cliente_list(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        messages.error(request, 'No está autorizado para realizar esta acción.')
        return redirect('login')  # Redirige si no hay cliente logueado
    
    try:
        cliente = Cliente.objects.get(pk=cliente_id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente no encontrado.')
        return redirect('login')  # Redirige si no se encuentra el cliente

    # Filtra las consultas por el cliente logueado
    consultas = Consulta.objects.filter(clidni=cliente.clidni)

    return render(request, 'consultas/consulta_cliente_list.html', {
        'consultas': consultas,
        'cliente': cliente,
        'return_url': 'consulta_list',  # Opcional, para navegación
    })

@cliente_login_required
def consulta_cliente_add(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        messages.error(request, 'No está autorizado para realizar esta acción.')
        return redirect('login')
    
    try:
        cliente = Cliente.objects.get(pk=cliente_id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente no encontrado.')
        return redirect('login')
    
    if request.method == 'POST':
        form = ConsultaClienteForm(request.POST, cliente_id=cliente_id)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.clidni = cliente  # Asigna el cliente internamente
            consulta.perdni = form.ultimo_personal  # Asigna el último personal internamente
            consulta.conres = ""
            consulta.confec = datetime.date.today()
            consulta.save()
            messages.success(request, 'Consulta registrada exitosamente.')
            return redirect('consulta_cliente_list')
    else:
        form = ConsultaClienteForm(cliente_id=cliente_id)

    return render(request, 'consultas/consulta_nueva_form.html', {
        'form': form,
        'cliente': cliente,
        'return_url': 'consulta_list',
        'title': 'Agregar Nueva Consulta'
    })

@cliente_login_required
def consulta_cliente_delete(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        try:
            consulta.delete()
            return redirect('consulta_cliente_list')
        except IntegrityError:
            return render(request, 'consultas/consulta_cliente_confirm_delete.html', {'consulta': consulta, 'error': "No se puede eliminar la consulta porque tiene dependencias asociadas."})
    return render(request, 'consultas/consulta_cliente_confirm_delete.html', {'consulta': consulta})

# Tipo Consulta CRUD
#personal 
def gestion_tipo_consulta(request):
    return render(request, 'consultas/gestion_tipo_consulta.html')

def tipo_consulta_list(request):
    consultas = TipoConsulta.objects.all()
    return render(request, 'consultas/tipo_consulta_list.html', {'consultas': consultas})
#personal 
def tipo_consulta_add(request):
    if request.method == 'POST':
        form = TipoConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save()
            return redirect('tipo_consulta_list')  # Redirigir a la lista de tipos de consulta
    else:
        form = TipoConsultaForm()
    return render(request, 'consultas/tipo_consulta_form.html', {'form': form, 'return_url': 'tipo_consulta_list', 'title': 'Agregar Tipo de Consulta'})
#personal 
def tipo_consulta_edit(request, pk):
    consulta = get_object_or_404(TipoConsulta, pk=pk)
    if request.method == 'POST':
        form = TipoConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            return redirect('tipo_consulta_list')
    else:
        form = TipoConsultaForm(instance=consulta)
    return render(request, 'consultas/tipo_consulta_form.html', {'form': form, 'return_url': 'tipo_consulta_list', 'title': 'Modificar Tipo de Consulta'})
#personal 
def tipo_consulta_delete(request, pk):
    consulta = get_object_or_404(TipoConsulta, pk=pk)
    if request.method == 'POST':
        consulta.delete()
        return redirect('tipo_consulta_list')
    return render(request, 'consultas/tipo_consulta_confirm_delete.html', {'consulta': consulta})

# ESTADO DE REGISTRO ################################################
#personal 
# Estado Registro CRUD
def estado_registro_list(request):
    estados = EstadoRegistro.objects.all()
    return render(request, 'estado_registro/estado_registro_list.html', {'estados': estados})

def estado_registro_add(request):
    if request.method == 'POST':
        form = EstadoRegistroForm(request.POST)
        if form.is_valid():
            estado = form.save()
            return redirect('estado_registro_list')  # Redirigir a la lista de estados
    else:
        form = EstadoRegistroForm()
    return render(request, 'estado_registro/estado_registro_form.html', {'form': form, 'return_url': 'estado_registro_list', 'title': 'Agregar '})

def estado_registro_edit(request, pk):
    estado = get_object_or_404(EstadoRegistro, pk=pk)
    if request.method == 'POST':
        form = EstadoRegistroForm(request.POST, instance=estado)
        if form.is_valid():
            form.save()
            return redirect('estado_registro_list')
    else:
        form = EstadoRegistroForm(instance=estado)
    return render(request, 'estado_registro/estado_registro_form.html', {'form': form, 'return_url': 'estado_registro_list', 'title': 'Modificar '})

def estado_registro_delete(request, pk):
    estado = get_object_or_404(EstadoRegistro, pk=pk)
    if request.method == 'POST':
        estado.delete()
        return redirect('estado_registro_list')
    return render(request, 'estado_registro/estado_registro_confirm_delete.html', {'estado': estado})

# PERSONAL ################################################

#@admin_required
def register_personal_view(request):
    if request.method == 'POST':
        form = PersonalRegisterForm(request.POST)
        
        if form.is_valid():
            personal = form.save()
            try:
                send_mail(
                    'Registro Exitoso',
                    f'Sus credenciales son:\nUsuario: {form.cleaned_data["perusu"]}\nContraseña: {form.cleaned_data["password2"]}',
                    'jhamilturpo2@gamil.com', 
                    [form.cleaned_data['percor']],
                    fail_silently=False,
                )
                print("12")
                messages.success(request, 'Registro de personal exitoso y correo enviado.')
            except Exception as e:
                messages.error(request, f'Error al enviar el correo: {e}')
            
            messages.success(request, 'Registro de personal exitoso y correo enviado.')
            return redirect('inicio_administrador')
    else:
        form = PersonalRegisterForm()
    return render(request, 'registration/register_personal.html', {'form': form})

# Login Personal
def personal_login(request):
    if request.method == 'POST':
        form = PersonalLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                personal = Personal.objects.get(perusu=username)
                if check_password(password, personal.percon):
                    request.session['personal_id'] = personal.perdni
                    messages.success(request, 'Inicio de sesión exitoso.')
                    return redirect_to_dashboard(personal.tippercod.tippernom)
                else:
                    messages.error(request, 'Contraseña incorrecta')
            except Personal.DoesNotExist:
                messages.error(request, 'Usuario no encontrado')
    else:
        form = PersonalLoginForm()
    return render(request, 'registration/personal_login.html', {'form': form})

def redirect_to_dashboard(tipo_personal):
    if tipo_personal == 'Técnico':
        return redirect('inicio_tecnico')
    elif tipo_personal == 'Vendedor':
        return redirect('inicio_vendedor')
    elif tipo_personal == 'Administrador':
        return redirect('inicio_administrador')
    else:
        return redirect('personal_login')

@multi_role_required('Administrador', 'Vendedor', 'Técnico')
def personal_logout(request):
    personal_id = request.session.get('personal_id')
    if not personal_id:
        messages.error(request, 'No está autorizado para realizar esta acción.')
        return redirect('personal_login') 
    
    try:
        del request.session['personal_id']
    except KeyError:
        pass
    return redirect('personal_login') 

#personal 
def inicio_tecnico(request):
    return render(request, 'inicio_personal/inicio_tecnico.html')

#personal 
def inicio_vendedor(request):
    return render(request, 'inicio_personal/inicio_vendedor.html')

#personal
def inicio_administrador(request):
    return render(request, 'inicio_administrador.html') ############## cambiar ubi

# Actualizar Perfil del Personal
#personal 
def actualizar_perfil_personal(request):
    username = request.user.username
    print(f"Username: {username}")
    
    try:
        personal = Personal.objects.get(perusu=username)
        print(f"Personal found: {personal}")
    except Personal.DoesNotExist:
        print("Personal does not exist")
        return redirect('inicio_administrador')

    if request.method == 'POST':
        print("POST request received")
        form = ActualizarPerfilPersonalForm(request.POST, instance=personal)
        if form.is_valid():
            print("Form is valid")
            form.save()
            return redirect('inicio_administrador')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = ActualizarPerfilPersonalForm(instance=personal)
        print("GET request received")

    return render(request, 'personal/actualizar_perfil_personal_form.html', {'form': form})

# Gestión Cliente
#personal 
def gestion_cliente(request):
    return render(request, 'cliente/gestion_cliente.html')

# Cliente CRUD
#personal 
def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/cliente_list.html', {'cliente': clientes})

#personal 
def cliente_add(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.clifecreg = datetime.date.today()  # Campo de fecha de registro
            cliente.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm(initial={
            'clifecreg': datetime.date.today(),
            'estregcod': EstadoRegistro.objects.get(estregnom='Activo'),
        })

    return render(request, 'cliente/cliente_form.html', {'form': form, 'return_url': 'cliente_list', 'title': 'Adicionar '})

#personal 
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, clidni=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'cliente/cliente_form.html', {'form': form, 'return_url': 'cliente_list', 'title': 'Modificar '})

def gestion_cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, clidni=pk)
    if request.method == 'POST':
        try:
            cliente.delete()
            return redirect('cliente_list')
        except IntegrityError:
            return render(request, 'cliente/cliente_confirm_delete.html', {'cliente': cliente, 'error': "No se puede eliminar el cliente porque tiene dependencias asociadas."})
    return render(request, 'cliente/cliente_confirm_delete.html', {'cliente': cliente})

def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        form = ClienteDeleteForm(request.POST)
        if form.is_valid():
            cliente.delete()
            messages.success(request, 'Cuenta eliminada exitosamente.')
            return redirect('cliente_list')
    else:
        form = ClienteDeleteForm()

    return render(request, 'cliente/cliente_confirm_delete.html', {'form': form})

#personal 
def vendedor_cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/vendedor_cliente_list.html', {'cliente': clientes})

def vendedor_cliente_add(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.clifecreg = datetime.date.today()  # Campo de fecha de registro
            cliente.save()
            return redirect('vendedor_cliente_list')
    else:
        form = ClienteForm(initial={
            'clifecreg': datetime.date.today(),
            'estregcod': EstadoRegistro.objects.get(estregnom='Activo'),
        })

    return render(request, 'cliente/vendedor_cliente_form.html', {'form': form, 'return_url': 'cliente_list', 'title': 'Adicionar Cliente'})

def vendedor_cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, clidni=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('vendedor_cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'cliente/vendedor_cliente_form.html', {'form': form, 'return_url': 'cliente_list', 'title': 'Modificar Cliente'})

def vendedor_cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, clidni=pk)
    if request.method == 'POST':
        try:
            cliente.delete()
            messages.success(request, 'Cliente eliminado correctamente.')
            return redirect('vendedor_cliente_list')
        except IntegrityError:
            messages.error(request, "No se puede eliminar el cliente porque tiene dependencias asociadas.")
            return render(request, 'cliente/vendedor_cliente_confirm_delete.html', {'cliente': cliente})
    return render(request, 'cliente/vendedor_cliente_confirm_delete.html', {'cliente': cliente})

def toggle_cliente_status(request, pk):
    cliente = get_object_or_404(Cliente, clidni=pk)
    activo_estado = EstadoRegistro.objects.get(estregnom='Activo')
    inactivo_estado = EstadoRegistro.objects.get(estregnom='Inactivo')
    cliente.estregcod = inactivo_estado if cliente.estregcod == activo_estado else activo_estado
    cliente.save()
    return redirect('vendedor_cliente_list')

# GESTION PERSONAL ###################################################################################################################
######################################################################################################################################

def gestion_personal(request):
    return render(request, 'personal/gestion_personal.html')

# Personal CRUD
def personal_list(request, codigo=None):
    instancia_clase = None
    personal = Personal.objects.all()
    tipo=TipoPersonal.objects.all()

    if codigo:
        instancia_clase = get_object_or_404(TipoPersonal, tippercod=codigo)
        personal=Personal.objects.filter(tippercod=codigo)

    if request.method == 'POST':
        formulario = TipoPersonalForm(request.POST, instance=instancia_clase)
        if formulario.is_valid():
            formulario.save()
            return redirect('personal_list')
    else:
        formulario = TipoPersonalForm(instance=instancia_clase)

    return render(request, 'personal/personal_list.html', {'formulario': formulario, 'personal': personal, 'tipo':tipo})

def personal_add(request):
    if request.method == 'POST':
        form = PersonalForm(request.POST)
        if form.is_valid():
            personal = form.save(commit=False)
            # Establece valores predeterminados para campos no visibles en el formulario
            personal.perfecreg = datetime.date.today()
            personal.pertel = ''  # Valor predeterminado
            personal.perdir = ''  # Valor predeterminado
            personal.percor = ''  # Valor predeterminado
            personal.save()
            return redirect('personal_list')
    else:
        form = PersonalForm(initial={
            'perfecreg': datetime.date.today(),
            'estregcod': EstadoRegistro.objects.get(estregnom='Activo'),
            'pertel': '',
            'perdir': '',
            'percor': ''
        })

    return render(request, 'personal/personal_form.html', {'form': form, 'return_url': 'personal_list', 'title': 'Adicionar '})

def personal_edit(request, pk):
    personal = get_object_or_404(Personal, pk=pk)
    if request.method == 'POST':
        form = PersonalForm(request.POST, instance=personal)
        if form.is_valid():
            form.save()
            return redirect('personal_list')
    else:
        form = PersonalForm(instance=personal)
    return render(request, 'personal/personal_form.html', {'form': form, 'return_url': 'personal_list', 'title': 'Modificar '})

def personal_delete(request, pk):
    personal = get_object_or_404(Personal, pk=pk)
    if request.method == 'POST':
        try:
            personal.delete()
            return redirect('personal_list')
        except IntegrityError:
            return render(request, 'personal/personal_confirm_delete.html', {'personal': personal, 'error': "No se puede eliminar el personal porque tiene dependencias asociadas."})
    return render(request, 'personal/personal_confirm_delete.html', {'personal': personal})

# TIPO PERSONAL #######################################################################################################################
######################################################################################################################################
#administrador
def tipo_personal_list(request):
    tipos = TipoPersonal.objects.all()
    return render(request, 'personal/tipo_personal_list.html', {'tipos': tipos})

def tipo_personal_add(request):
    if request.method == 'POST':
        form = TipoPersonalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tipo_personal_list')  # Redirige a la lista de tipos de personal
    else:
        form = TipoPersonalForm()
    return render(request, 'personal/tipo_personal_form.html', {'form': form, 'title': 'Agregar', 'return_url': 'tipo_personal_list'})

def tipo_personal_edit(request, pk):
    tipo_personal = get_object_or_404(TipoPersonal, pk=pk)
    if request.method == 'POST':
        form = TipoPersonalForm(request.POST, instance=tipo_personal)
        if form.is_valid():
            form.save()
            return redirect('tipo_personal_list')  # Redirige a la lista de tipos de personal
    else:
        form = TipoPersonalForm(instance=tipo_personal)
    return render(request, 'personal/tipo_personal_form.html', {'form': form, 'title': 'Modificar', 'return_url': 'tipo_personal_list'})

def tipo_personal_delete(request, pk):
    tipo = get_object_or_404(TipoPersonal, pk=pk)
    if request.method == 'POST':
        tipo.delete()
        return redirect('tipo_personal_list')
    return render(request, 'personal/tipo_personal_confirm_delete.html', {'tipo': tipo})

def toggle_personal_status(request, pk):
    personal = get_object_or_404(Personal, pk=pk)
    activo_estado = EstadoRegistro.objects.get(estregnom='Activo')
    inactivo_estado = EstadoRegistro.objects.get(estregnom='Inactivo')
    personal.estregcod = inactivo_estado if personal.estregcod == activo_estado else activo_estado  
    personal.save()
    return redirect('personal_list')

# CLIENTE ################################################

def register_view(request):
    if request.method == 'POST':
        form = ClienteRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso')
            return redirect('cliente_login')
    else:
        form = ClienteRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def cliente_login(request):
    if request.method == 'POST':
        form = ClienteLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"Username ingresado: {username}")
            print(f"Password ingresado: {password}") 
            try:
                cliente = Cliente.objects.get(cliusu=username)
                if check_password(password, cliente.clicon):
                    request.session['cliente_id'] = cliente.clidni
                    messages.success(request, 'Inicio de sesión exitoso.')
                    return redirect('index')
                else:
                    messages.error(request, 'Contraseña incorrecta')
            except Cliente.DoesNotExist:
                messages.error(request, 'Usuario no encontrado')
    else:
        form = ClienteLoginForm()
    return render(request, 'registration/login.html', {'form': form})

@cliente_login_required
def cliente_logout(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        messages.error(request, 'No está autorizado para realizar esta acción.')
        return redirect('login') 
    
    try:
        del request.session['cliente_id']
    except KeyError:
        pass
    return redirect('index') 

@cliente_login_required
def cliente_detail(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        messages.error(request, 'No está autorizado para realizar esta acción.')
        return redirect('login') 
    
    cliente = request.cliente
    return render(request, 'cliente/cliente_detail.html', {'cliente': cliente})

@cliente_login_required
def cliente_update(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        messages.error(request, 'No está autorizado para realizar esta acción.')
        return redirect('login') 
    
    cliente = request.cliente
    if request.method == 'POST':
        form = ClienteUpdateForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente')
            return redirect('cliente_detail')
    else:
        form = ClienteUpdateForm(instance=cliente)
    return render(request, 'cliente/cliente_update.html', {'form': form, 'title': 'Actualizar Datos'})

@cliente_login_required
def cliente_delete(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        messages.error(request, 'No está autorizado para realizar esta acción.')
        return redirect('cliente_login') 

    cliente = get_object_or_404(Cliente, clidni=cliente_id)

    if request.method == 'POST':
        form = ClienteDeleteForm(request.POST)
        if form.is_valid():
            cliente.delete()
            request.session.flush()
            messages.success(request, 'Cuenta eliminada exitosamente.')
            return redirect('cliente_login') 
    else:
        form = ClienteDeleteForm()

    return render(request, 'cliente/cliente_delete.html', {'form': form})
#no cuenta
from django.urls import reverse
def solicitar_cambio_password(request):
    if request.method == 'POST':
        cliusu = request.POST.get('cliusu')
        try:
            cliente = Cliente.objects.get(cliusu=cliusu)
            token = generate_token(cliente)
            reset_url = request.build_absolute_uri(
                reverse('cambiar_password', kwargs={'token': token})
            )
            email = cliente.clicor 
            send_mail(
                'Solicitud de cambio de contraseña',
                f'Usa este enlace para cambiar tu contraseña: {reset_url}',
                'noreply@tudominio.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Se ha enviado un email con instrucciones para cambiar tu contraseña.')
        except Cliente.DoesNotExist:
            messages.error(request, 'No existe un cliente con ese nombre de usuario.')
        return redirect('solicitar_cambio_password')
    return render(request, 'cliente/solicitar_cambio_password.html')

def cambiar_password(request, token):
    clidni = confirm_token(token)
    if not clidni:
        messages.error(request, 'El enlace de cambio de contraseña es inválido o ha expirado.')
        return redirect('solicitar_cambio_password')
    
    cliente = get_object_or_404(Cliente, clidni=clidni)
    
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password2 and password1 == password2:
            cliente.clicon = password1  # Asumiendo que 'clicon' es el campo de contraseña
            cliente.save()
            messages.success(request, 'Tu contraseña ha sido cambiada exitosamente.')
            return redirect('login')  # Asegúrate de tener una vista de login
        else:
            messages.error(request, 'Las contraseñas no coinciden o están vacías.')
    
    return render(request, 'cliente/cambiar_password.html')

def send_confirmation_email(request, cliente, new_value, field):
    token = generate_token(cliente)
    confirmation_url = request.build_absolute_uri(f'/confirm_change/{token}/')
    send_mail(
        'Confirmación de cambio de cuenta',
        f'Hola {cliente.cliusu},\n\nPor favor confirma el cambio de tu {field} haciendo clic en el siguiente enlace:\n{confirmation_url}\n\nGracias.',
        settings.DEFAULT_FROM_EMAIL,
        [cliente.clicor],
        fail_silently=False,
    )

def confirm_change(request, token):
    clidni = confirm_token(token)
    if not clidni:
        messages.error(request, 'El enlace de confirmación es inválido o ha expirado.')
        return redirect('index')
    
    cliente = get_object_or_404(Cliente, clidni=clidni)
    # Aquí puedes realizar las operaciones necesarias, por ejemplo, cambiar contraseña
    # Verifica si el cliente está logeado antes de hacer cualquier cambio
    
    if 'cliente_id' in request.session and request.session['cliente_id'] == cliente.clidni:
        # Realiza el cambio (por ejemplo, actualiza la contraseña o el usuario)
        messages.success(request, 'Cambio confirmado exitosamente.')
    else:
        messages.error(request, 'No estás autorizado para realizar este cambio.')

    messages.success(request, 'Cambio confirmado exitosamente.')
    return redirect('index')

def send_confirmation_email(request, cliente, new_value, field):
    token = generate_token(cliente)
    confirmation_url = request.build_absolute_uri(f'/confirm_change/{token}/')
    send_mail(
        'Confirmación de cambio de cuenta',
        f'Hola {cliente.cliusu},\n\nPor favor confirma el cambio de tu {field} haciendo clic en el siguiente enlace:\n{confirmation_url}\n\nGracias.',
        settings.DEFAULT_FROM_EMAIL,
        [cliente.clicor],
        fail_silently=False,
    )

def actualizar_cliente(request):
    cliente = get_object_or_404(Cliente, cliusu=request.user.username)
    if request.method == 'POST':
        form = ClienteUpdateForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tus datos han sido actualizados correctamente.')
            return redirect('perfil_cliente')
    else:
        form = ClienteUpdateForm(instance=cliente)
    
    return render(request, 'cliente/actualizar_cliente.html', {'form': form})

def cambiar_usuario(request):
    cliente = get_object_or_404(Cliente, cliusu=request.user.username)
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST)
        if form.is_valid():
            nuevo_usuario = form.cleaned_data['cliusu']
            # Enviar correo de confirmación (implementar envío real en producción)
            send_mail(
                'Cambio de Usuario en Tienda Online',
                f'Confirma tu nuevo usuario: {nuevo_usuario}',
                'jhamilturpo@gmail.com',
                [cliente.clicor],
                fail_silently=False,
            )
            messages.success(request, 'Revisa tu correo para confirmar el cambio de usuario.')
            return redirect('perfil_cliente')
    else:
        form = UsuarioUpdateForm()

    return render(request, 'cliente/cambiar_usuario.html', {'form': form})

def cambiar_contrasena(request):
    cliente = get_object_or_404(Cliente, cliusu=request.user.username)
    if request.method == 'POST':
        form = ContrasenaUpdateForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            if cliente.clicon != old_password:
                messages.error(request, 'La contraseña actual no es correcta.')
            else:
                cliente.clicon = new_password
                cliente.save()
                messages.success(request, 'Tu contraseña ha sido actualizada correctamente.')
                return redirect('perfil_cliente')
    else:
        form = ContrasenaUpdateForm()

    return render(request, 'cliente/cambiar_contrasena.html', {'form': form})

# PRODUCTO ##############################################################################################################33
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
    return render(request, 'productos/productos.html', context)

#general
def vendedor_gestionar_productos(request):
    categorias = CategoariaProducto.objects.all()  
    productos = Producto.objects.all()      
    categoria_id = request.GET.get('categoria')  
    if categoria_id:
        productos = productos.filter(catprocod=categoria_id)      
    context = {
        'categorias': categorias,
        'producto': productos,
    }
    return render(request, 'productos/vendedor_gestionar_productos.html', context)

def detalle_producto(request, procod):
    producto = get_object_or_404(Producto, procod=procod)
    cantidad_disponible = producto.inventario_set.aggregate(total_cantidad=models.Sum('invcan'))['total_cantidad'] or 0
    return render(request, 'productos/detalle_producto.html', {
        'producto': producto,
        'cantidad_disponible': cantidad_disponible
    })
# GESTIONAR LAS RESERVAS DE PRODUCTO (CLIENTE)
@cliente_login_required
def reserva_producto(request, procod):
    cliente = get_authenticated_cliente(request)
    producto = get_object_or_404(Producto, procod=procod)
    inventario = Inventario.objects.filter(procod=producto).first()
    cantidad_disponible = inventario.invcan if inventario else 0

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            fecha_reserva = form.cleaned_data['fecha_reserva']
            notas = form.cleaned_data['notas']
            forma_pago = form.cleaned_data['forma_pago']
            confirmacion = form.cleaned_data['confirmacion']
            if cantidad > cantidad_disponible:
                form.add_error('cantidad', 'La cantidad solicitada excede la disponible.')
            if fecha_reserva < timezone.now().date():
               form.add_error('fecha_reserva', 'La fecha de recogida no puede ser anterior a la fecha actual.')            
            else:
                EventoProducto.objects.create(
                    evedes=f'Reserva de {cantidad} unidades del producto {producto.pronom}',
                    evefec=fecha_reserva,
                    procod=producto,
                    cantidad=cantidad,
                    cliente=cliente,
                    notas=notas
                )                
                inventario.invcan -= cantidad
                inventario.save()
                messages.success(request, 'Reserva realizada con éxito.')
                return redirect('calendario')        
    else:
        form = ReservaForm()           
    form.fields['cantidad'].widget.attrs.update({'max': cantidad_disponible})
    context = {
        'cliente': cliente,
        'producto': producto,
        'cantidad_disponible': cantidad_disponible,
        'form': form
    }
    return render(request, 'productos/reservaProducto.html', context)

@login_required
def lista_reservas(request):
    cliente = get_authenticated_cliente(request)
    reservas = EventoProducto.objects.filter(cliente=cliente).select_related('procod')
    return render(request, 'productos/lista_reservas.html', {'reservas': reservas})

@cliente_login_required
def detalle_reserva(request, evecod):
    reserva = get_object_or_404(EventoProducto, evecod=evecod)  
    return render(request, 'productos/detalle_reserva.html', {'reserva': reserva})

@cliente_login_required
def editar_reserva(request, evecod):
    reserva = get_object_or_404(EventoProducto, evecod=evecod)
    cantidad_anterior = reserva.cantidad
    producto = reserva.procod
    inventario = Inventario.objects.filter(procod=producto).first()
    cantidad_disponible = inventario.invcan if inventario else 0
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            fecha_reserva = form.cleaned_data['fecha_reserva']
            notas = form.cleaned_data['notas']
            if cantidad > cantidad_disponible:
                form.add_error('cantidad', 'La cantidad solicitada excede la disponible.')
            if fecha_reserva < timezone.now().date():
                form.add_error('fecha_reserva', 'La fecha de recogida no puede ser anterior a la fecha actual.')                     
            if inventario:
                inventario.invcan += cantidad_anterior - cantidad
                inventario.save()     
            else:
                messages.error(request, 'No se encontró el producto en el inventario.')
                return render(request, 'productos/editar_reserva.html', {'form': form, 'reserva': reserva})       
            reserva.cantidad = cantidad
            reserva.evefec = fecha_reserva
            reserva.notas = notas
            reserva.save()
            messages.success(request, 'Reserva actualizada con éxito.')
            return redirect('detalle_reserva', evecod=reserva.evecod)
    else:
        initial_data = {
            'cantidad': reserva.cantidad,
            'fecha_reserva': reserva.evefec,
            'notas': reserva.notas,
        }
        form = ReservaForm(initial=initial_data)
    form.fields['cantidad'].widget.attrs.update({'max': cantidad_disponible})
    context = {
        'form': form,
        'reserva': reserva,
        'cantidad_disponible': cantidad_disponible
    }
    return render(request, 'productos/editar_reserva.html', {'form': form, 'reserva': reserva})

@cliente_login_required
def confirmar_eliminar_reserva(request, evecod):
    reserva = get_object_or_404(EventoProducto, evecod=evecod)
    if request.method == 'POST':
        cantidad = reserva.cantidad
        producto = reserva.procod
        inventario = Inventario.objects.filter(procod=producto).first()
        if inventario:
            inventario.invcan += cantidad
            inventario.save()
        reserva.delete()
        messages.success(request, 'Reserva eliminada con éxito.')
        return redirect('calendario')
    return render(request, 'productos/eliminar_reserva.html', {'reserva': reserva})

# GESTIONAR LOS PRODUCTOS CON INVENTARIO (TRABAJADOR)
def lista_productos(request):
    categorias = CategoariaProducto.objects.all()
    productos = Producto.objects.all()
    categoria_id = request.GET.get('categoria')    
    if categoria_id:
        productos = productos.filter(catprocod=categoria_id)    

    # Crear una lista de productos con sus cantidades disponibles
    productos_con_cantidad = []
    for producto in productos:
        # Obtener la cantidad total disponible para cada producto
        cantidad = Inventario.objects.filter(procod=producto.procod).aggregate(total_cantidad=Sum('invcan'))['total_cantidad'] or 0
        productos_con_cantidad.append({
            'producto': producto,
            'cantidad_disponible': cantidad
        })

    context = {
        'categorias': categorias,
        'productos_con_cantidad': productos_con_cantidad,
    }
    return render(request, 'productos/producto_lista.html', context)
#personal 
def producto_create(request):
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST, request.FILES)
        inventario_form = InventarioForm(request.POST)
        if producto_form.is_valid() and inventario_form.is_valid():
            producto = producto_form.save(commit=False)       
            try:
                activo_estado = EstadoRegistro.objects.get(estregnom='Activo')
                producto.estregcod = activo_estado
            except EstadoRegistro.DoesNotExist:
                return render(request, 'productos/producto_form.html', {
                    'producto_form': producto_form,
                    'inventario_form': inventario_form,
                    'error': 'Estado de registro "Activo" no encontrado.'
                })                    
            inventario = inventario_form.save(commit=False)
            inventario.procod = producto
            inventario.invfecha = datetime.date.today() 
            producto.save()   
            inventario.save()            
            messages.success(request, 'Producto registrado exitosamente.')
            return redirect('lista_productos')

    else:
        producto_form = ProductoForm(initial={
            'estregcod': EstadoRegistro.objects.get(estregnom='Activo'),
        })
        inventario_form = InventarioForm(initial={
            'invfecing': datetime.date.today(),
        })
    return render(request, 'productos/producto_form.html', {
        'producto_form': producto_form,
        'inventario_form': inventario_form
    })

def producto_update(request, procod):
    producto = Producto.objects.get(procod=procod)
    inventario = Inventario.objects.get(procod=producto)
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST, request.FILES, instance=producto)
        inventario_form = InventarioForm(request.POST, instance=inventario)
        if producto_form.is_valid() and inventario_form.is_valid():
            producto_form.save()
            inventario_form.save()
            return redirect(reverse('lista_productos'))
    else:
        producto_form = ProductoForm(instance=producto)
        inventario_form = InventarioForm(instance=inventario)
    return render(request, 'productos/producto_form.html', {
        'producto_form': producto_form,
        'inventario_form': inventario_form,
    })
#personal 
def confirmar_eliminacion(request, procod):
    producto = get_object_or_404(Producto, procod=procod)
    inventario = get_object_or_404(Inventario, procod=producto)
    # Renderizar el template de confirmación
    return render(request, 'productos/producto_eliminar.html', {
        'producto': producto,
        'inventario': inventario,
    })
#personal 
def producto_delete(request, procod):
    producto = get_object_or_404(Producto, procod=procod)
    inventario = get_object_or_404(Inventario, procod=producto)
    if EventoProducto.objects.filter(procod=producto).exists():
        messages.error(request, 'No se puede eliminar el producto porque tiene reservas asociadas.')
        return redirect(reverse('confirmar_eliminacion', kwargs={'procod': procod}))
    if request.method == 'POST':
        inventario.delete()
        producto.delete()
        messages.success(request, 'Producto eliminado con éxito.')
        return redirect(reverse('lista_productos'))

    return redirect(reverse('confirmar_eliminacion', kwargs={'procod': procod}))

# GESTION CATEGORIA SERVICIO #########################################################################################################
######################################################################################################################################

#personal
def gestionar_CategoriaProductos(request, codigo=None):
    instancia_clase = None
    categorias = CategoariaProducto.objects.all()

    if request.method == 'POST':
        formulario = CategoriaProductoForm(request.POST, instance=instancia_clase)
        if formulario.is_valid():
            formulario.save()
            return redirect('gestionar_CategoriaProductos')
    else:
        formulario = CategoriaProductoForm(instance=instancia_clase)

    return render(request, 'productos/gestionarCategoriaProductos.html', {'formulario': formulario, 'categorias': categorias})
#oersonal
def agregar_CategoriaProductos(request):
    if request.method == 'POST':
        form = CategoriaProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestionar_CategoriaProductos')  
    else:
        form = CategoriaProductoForm()
    
    return render(request, 'productos/agregarCategoriaProductos.html', {'form': form})
#personal
def modificar_CategoriaProductos(request, catprocod):
    producto = get_object_or_404(CategoariaProducto, catprocod=catprocod)
    if request.method == 'POST':
        form = CategoriaProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('gestionar_CategoriaProductos')  # Redirigir a la vista de listado de servicios
    else:
        form = CategoriaProductoForm(instance=producto)
    
    return render(request, 'productos/modificarCategoriaProductos.html', {'form': form, 'producto': producto})
#personal
def eliminar_CategoriaProductos(request, catprocod):
    categoria = get_object_or_404(CategoariaProducto, catprocod=catprocod)

    if request.method == 'POST':
        # Verificar si hay servicios asociados a la categoría
        if Producto.objects.filter(catprocod=categoria).exists():
            # Mostrar mensaje de error si hay servicios asociados
            messages.error(request, 'No se puede eliminar la categoría porque tiene productos asociados.')
            return redirect('gestionar_CategoriaProductos')
        
        # Si no hay servicios asociados, eliminar la categoría
        categoria.delete()
        messages.success(request, 'Categoría de Producto eliminada correctamente.')
        return redirect('gestionar_CategoriaProductos')

    # Redirigir si no es una solicitud POST
    return redirect('gestionar_CategoriaProductos')


# REGISTRO DE VENTAS #################################################################################################################
######################################################################################################################################
def vendedor_gestionar_productos(request):
    categorias = CategoariaProducto.objects.all()
    productos = Producto.objects.all()
    categoria_id = request.GET.get('categoria')    
    if categoria_id:
        productos = productos.filter(catprocod=categoria_id)    

    # Crear una lista de productos con sus cantidades disponibles
    productos_con_cantidad = []
    for producto in productos:
        # Obtener la cantidad total disponible para cada producto
        cantidad = Inventario.objects.filter(procod=producto.procod).aggregate(total_cantidad=Sum('invcan'))['total_cantidad'] or 0
        productos_con_cantidad.append({
            'producto': producto,
            'cantidad_disponible': cantidad
        })

    context = {
        'categorias': categorias,
        'productos_con_cantidad': productos_con_cantidad,
    }
    return render(request, 'productos/vendedor_gestionar_productos.html', context)

def vendedor_producto_create(request):
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST, request.FILES)
        inventario_form = InventarioForm(request.POST)
        if producto_form.is_valid() and inventario_form.is_valid():
            producto = producto_form.save(commit=False)       
            try:
                activo_estado = EstadoRegistro.objects.get(estregnom='Activo')
                producto.estregcod = activo_estado
            except EstadoRegistro.DoesNotExist:
                return render(request, 'productos/vendedor_producto_form.html', {
                    'producto_form': producto_form,
                    'inventario_form': inventario_form,
                    'error': 'Estado de registro "Activo" no encontrado.'
                })                    
            inventario = inventario_form.save(commit=False)
            inventario.procod = producto
            inventario.invfecha = datetime.date.today() 
            producto.save()   
            inventario.save()            
            messages.success(request, 'Producto registrado exitosamente.')
            return redirect('vendedor_gestionar_productos')

    else:
        producto_form = ProductoForm(initial={
            'estregcod': EstadoRegistro.objects.get(estregnom='Activo'),
        })
        inventario_form = InventarioForm(initial={
            'invfecing': datetime.date.today(),
        })
    return render(request, 'productos/vendedor_producto_form.html', {
        'producto_form': producto_form,
        'inventario_form': inventario_form
    })

def vendedor_producto_update(request, procod):
    producto = Producto.objects.get(procod=procod)
    inventario = Inventario.objects.get(procod=producto)
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST, request.FILES, instance=producto)
        inventario_form = InventarioForm(request.POST, instance=inventario)
        if producto_form.is_valid() and inventario_form.is_valid():
            producto_form.save()
            inventario_form.save()
            return redirect(reverse('vendedor_gestionar_productos'))
    else:
        producto_form = ProductoForm(instance=producto)
        inventario_form = InventarioForm(instance=inventario)
    return render(request, 'productos/vendedor_producto_form.html', {
        'producto_form': producto_form,
        'inventario_form': inventario_form,
    })

def vendedor_confirmar_eliminacion(request, procod):
    producto = get_object_or_404(Producto, procod=procod)
    inventario = get_object_or_404(Inventario, procod=producto)
    # Renderizar el template de confirmación
    return render(request, 'productos/vendedor_producto_eliminar.html', {
        'producto': producto,
        'inventario': inventario,
    })

def vendedor_producto_delete(request, procod):
    producto = get_object_or_404(Producto, procod=procod)
    inventario = get_object_or_404(Inventario, procod=producto)
    if EventoProducto.objects.filter(procod=producto).exists():
        messages.error(request, 'No se puede eliminar el producto porque tiene reservas asociadas.')
        return redirect(reverse('vendedor_confirmar_eliminacion', kwargs={'procod': procod}))
    if request.method == 'POST':
        inventario.delete()
        producto.delete()
        messages.success(request, 'Producto eliminado con éxito.')
        return redirect(reverse('vendedor_gestionar_productos'))

    return redirect(reverse('vendedor_confirmar_eliminacion', kwargs={'procod': procod}))

# registro de ventas

def venta_list(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas/venta_list.html', {'ventas': ventas})
#personal 
def venta_detail(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    return render(request, 'ventas/venta_detail.html', {'venta': venta})
#personal 
def venta_edit(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Venta actualizada exitosamente')
            return redirect('venta_detail', pk=venta.pk)
    else:
        form = VentaForm(instance=venta)
    return render(request, 'ventas/venta_form.html', {'form': form})
#personal 
def venta_delete(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        messages.success(request, 'Venta eliminada exitosamente')
        return redirect('venta_list')
    return render(request, 'ventas/venta_confirm_delete.html', {'venta': venta})

# REPORTES PRODUCTOS #################################################################################################################
######################################################################################################################################

def sales_report(request):
    form = SalesReportForm()
    sales = []
    total_sales = 0

    if request.method == 'POST':
        form = SalesReportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            if end_date:
                sales = Venta.objects.filter(venfecres__range=[start_date, end_date])
            else:
                sales = Venta.objects.filter(venfecres__gte=start_date)
            total_sales = sales.aggregate(total=Sum('venprotot'))['total']

    context = {
        'form': form,
        'sales': sales,
        'total_sales': total_sales,
    }
    return render(request, 'productos/sales_report.html', context)

# VER SERVICIO #######################################################################################################################
######################################################################################################################################

#general
def servicios(request, codigo=None):
    instancia_clase = None
    servicio = Servicio.objects.all()
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

    return render(request, 'servicios/servicios.html', {'formulario': formulario, 'servicio': servicio, 'categorias': categorias})

#Personal: Vendedor
def vendedor_servicios(request, codigo=None):
    instancia_clase = None
    servicio = Servicio.objects.all()
    categorias = CategoariaServicio.objects.all()

    if codigo:
        instancia_clase = get_object_or_404(CategoariaServicio, catsercod=codigo)
        servicio = Servicio.objects.filter(categoaria_servicio_catsercod=codigo)

    if request.method == 'POST':
        formulario = CategoriaServicioForm(request.POST, instance=instancia_clase)
        if formulario.is_valid():
            formulario.save()
            return redirect('vendedor_servicios')
    else:
        formulario = CategoriaServicioForm(instance=instancia_clase)

    return render(request, 'servicios/vendedor_servicios.html', {'formulario': formulario, 'servicio': servicio, 'categorias': categorias})

def detalle_servicio(request, sercod):
    servicio = get_object_or_404(Servicio, sercod=sercod)
    personal = Personal.objects.filter(tippercod='2')
    return render(request, 'servicios/detalle_servicio.html', {'servicio': servicio, 'personal':personal})


# GESTIONAR SERVICIOS ################################################################################################################
######################################################################################################################################

#personal
def gestionar_servicios(request, codigo=None):
    instancia_clase = None
    servicio = Servicio.objects.all()
    categorias = CategoariaServicio.objects.all()

    if codigo:
        instancia_clase = get_object_or_404(CategoariaServicio, catsercod=codigo)
        servicio = Servicio.objects.filter(categoaria_servicio_catsercod=codigo)

    if request.method == 'POST':
        formulario = CategoriaServicioForm(request.POST, instance=instancia_clase)
        if formulario.is_valid():
            formulario.save()
            return redirect('gestionar_servicios')
    else:
        formulario = CategoriaServicioForm(instance=instancia_clase)

    return render(request, 'servicios/gestionarServicios.html', {'formulario': formulario, 'servicio': servicio, 'categorias': categorias})

def vendedor_gestionar_servicios(request, codigo=None):
    instancia_clase = None
    servicio = Servicio.objects.all()
    categorias = CategoariaServicio.objects.all()

    if codigo:
        instancia_clase = get_object_or_404(CategoariaServicio, catsercod=codigo)
        servicio = Servicio.objects.filter(categoaria_servicio_catsercod=codigo)

    if request.method == 'POST':
        formulario = CategoriaServicioForm(request.POST, instance=instancia_clase)
        if formulario.is_valid():
            formulario.save()
            return redirect('gestionar_servicios')
    else:
        formulario = CategoriaServicioForm(instance=instancia_clase)

    return render(request, 'servicios/vendedor_gestionar_servicios.html', {'formulario': formulario, 'servicio': servicio, 'categorias': categorias})

#perosnal
def agregar_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestionar_servicios')  
    else:
        form = ServicioForm(initial={
            'estado_registro_estregcod': EstadoRegistro.objects.get(estregnom='Activo'),
        })
    
    return render(request, 'servicios/agregarServicios.html', {'form': form})

#perosnal: vendedor
def vendedor_agregar_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vendedor_gestionar_servicios')  
    else:
        form = ServicioForm(initial={
            'estado_registro_estregcod': EstadoRegistro.objects.get(estregnom='Activo'),
        })
    
    return render(request, 'servicios/vendedor_agregar_servicios.html', {'form': form})

#personal
def modificar_servicio(request, sercod):
    servicio = get_object_or_404(Servicio, sercod=sercod) 
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('gestionar_servicios')  # Redirigir a la vista de listado de servicios
    else:
        form = ServicioForm(instance=servicio)
    
    return render(request, 'servicios/modificarServicios.html', {'form': form, 'servicio': servicio})

#personal: vendedor
def vendedor_modificar_servicio(request, sercod):
    servicio = get_object_or_404(Servicio, sercod=sercod) 
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('vendedor_gestionar_servicios')  # Redirigir a la vista de listado de servicios
    else:
        form = ServicioForm(instance=servicio)
    
    return render(request, 'servicios/vendedor_modificar_servicios.html', {'form': form, 'servicio': servicio})

#personal
def eliminar_servicio(request, sercod):
    servicio = get_object_or_404(Servicio, sercod=sercod)
    if request.method == 'POST':
        servicio.delete()
        messages.success(request, 'Servicio eliminado correctamente.')
        return redirect('gestionar_servicios')

    return redirect('gestionar_servicios')


# GESTION CATEGORIA SERVICIO #########################################################################################################
######################################################################################################################################

#personal: vendedor
def vendedor_eliminar_servicio(request, sercod):
    servicio = get_object_or_404(Servicio, sercod=sercod)
    if request.method == 'POST':
        servicio.delete()
        messages.success(request, 'Servicio eliminado correctamente.')
        return redirect('vendedor_gestionar_servicios')

    return redirect('vendedor_gestionar_servicios')
#personal
def gestionar_CategoriaServicios(request, codigo=None):
    instancia_clase = None
    categorias = CategoariaServicio.objects.all()

    if request.method == 'POST':
        formulario = CategoriaServicioForm(request.POST, instance=instancia_clase)
        if formulario.is_valid():
            formulario.save()
            return redirect('gestionar_CategoriaServicios')
    else:
        formulario = CategoriaServicioForm(instance=instancia_clase)

    return render(request, 'servicios/gestionarCategoriaServicio.html', {'formulario': formulario, 'categorias': categorias})
#oersonal
def agregar_CategoriaServicio(request):
    if request.method == 'POST':
        form = CategoriaServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestionar_CategoriaServicios')  
    else:
        form = CategoriaServicioForm()
    
    return render(request, 'servicios/agregarCategoriaServicios.html', {'form': form})
#personal
def modificar_CategoriaServicio(request, catsercod):
    servicio = get_object_or_404(CategoariaServicio, catsercod=catsercod)
    if request.method == 'POST':
        form = CategoriaServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('gestionar_CategoriaServicios')  # Redirigir a la vista de listado de servicios
    else:
        form = CategoriaServicioForm(instance=servicio)
    
    return render(request, 'servicios/modificarCategoriaServicios.html', {'form': form, 'servicio': servicio})
#personal
def eliminar_CategoriaServicio(request, catsercod):
    categoria = get_object_or_404(CategoariaServicio, catsercod=catsercod)

    if request.method == 'POST':
        # Verificar si hay servicios asociados a la categoría
        if Servicio.objects.filter(categoaria_servicio_catsercod=categoria).exists():
            # Mostrar mensaje de error si hay servicios asociados
            messages.error(request, 'No se puede eliminar la categoría porque tiene servicios asociados.')
            return redirect('gestionar_CategoriaServicios')
        
        # Si no hay servicios asociados, eliminar la categoría
        categoria.delete()
        messages.success(request, 'Categoría de Servicio eliminada correctamente.')
        return redirect('gestionar_CategoriaServicios')

    # Redirigir si no es una solicitud POST
    return redirect('gestionar_CategoriaServicios')

@cliente_login_required
def crear_evento(request):
    servicio_id = request.GET.get('servicio_id')
    cliente = get_authenticated_cliente(request)

    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            if cliente:
                evento.clidni = cliente

            if servicio_id:
                try:
                    servicio = Servicio.objects.get(pk=servicio_id)
                    evento.sercod = servicio  # Asignar la instancia del objeto Servicio
                except Servicio.DoesNotExist:
                    form.add_error(None, 'El servicio seleccionado no existe.')
                    return render(request, 'servicios/reservaServicio.html', {
                        'form': form,
                        'servicio': None,
                        'cliente': cliente,
                    })
            else:
                form.add_error(None, 'No se ha proporcionado un servicio válido.')
                return render(request, 'servicios/reservaServicio.html', {
                    'form': form,
                    'servicio': None,
                    'cliente': cliente,
                })

            # Verificar disponibilidad del personal para la fecha seleccionada
            fecha_evento = evento.evefec

            # Encontrar personal que no tenga eventos en la fecha seleccionada
            personal_disponible = Personal.objects.exclude(
                pk__in=Evento.objects.filter(
                    evefec=fecha_evento
                ).values_list('perdni_id', flat=True)
            ).first()

            if personal_disponible:
                evento.perdni = personal_disponible
                evento.save()
                messages.success(request, 'Evento creado y personal asignado con éxito.')
                return redirect('calendario')
            else:
                # Mostrar mensaje de error si no hay personal disponible
                messages.warning(request, 'No hay personal disponible para la fecha seleccionada. Por favor, elija otra fecha.')
                form.add_error('evefec', 'No hay personal disponible para la fecha seleccionada.')
                return render(request, 'servicios/reservaServicio.html', {
                    'form': form,
                    'servicio': Servicio.objects.filter(pk=servicio_id).first(),
                    'cliente': cliente,
                })
    else:
        form = EventoForm()

    if servicio_id:
        try:
            servicio = Servicio.objects.get(pk=servicio_id)
        except Servicio.DoesNotExist:
            servicio = None
    else:
        servicio = None

    return render(request, 'servicios/reservaServicio.html', {
        'form': form,
        'servicio': servicio,
        'cliente': cliente,
    })

@login_required
def lista_eventos(request):
    cliente = get_authenticated_cliente(request)
    eventos = Evento.objects.filter(clidni=cliente).select_related('sercod', 'perdni')
    return render(request, 'servicios/lista_eventos.html', {'eventos': eventos})

@cliente_login_required
def detalle_reservaS(request, evecod):
    reserva = get_object_or_404(Evento, evecod=evecod)  
    return render(request, 'servicios/detalle_reservaS.html', {'reserva': reserva})

@cliente_login_required
def editar_reservaS(request, evecod):
    reserva = get_object_or_404(Evento, evecod=evecod)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva actualizada con éxito.')
            return redirect('servicios/detalle_reservaS', evecod=reserva.evecod)
    else:
        form = EventoForm(instance=reserva)
    
    return render(request, 'servicios/editar_reservaS.html', {'form': form, 'reserva': reserva})

@cliente_login_required
def eliminar_reservaS(request, evecod):
    reserva = get_object_or_404(Evento, evecod=evecod)
    
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva eliminada correctamente.')
        return redirect('calendario')
    
    return redirect('calendario')


#EVENTO ##############################################################################################################################
######################################################################################################################################

#CALENDARIO#######################################################################################################3
def generate_calendar(year, month):
    start_date = datetime.datetime(year, month, 1)
    end_date = datetime.datetime(year, month, monthrange(year, month)[1])
    calendar = []
    week = [''] * start_date.weekday()
    for day in range(1, monthrange(year, month)[1] + 1):
        week.append(datetime.datetime(year, month, day))
        if len(week) == 7:
            calendar.append(week)
            week = []
    while len(week) < 7:
        week.append('')
    if week:
        calendar.append(week)
    return calendar

@cliente_login_required
def calendario_view(request):
    today = timezone.now()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    if 'prev' in request.GET:
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1
    elif 'next' in request.GET:
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
    cliente = get_authenticated_cliente(request)
    eventos_producto = EventoProducto.objects.filter(cliente=cliente)
    eventos_servicio = Evento.objects.filter(clidni=cliente.clidni)  
    calendar = generate_calendar(year, month)
    month_names = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    month_name = month_names[month - 1]
    return render(request, 'calendario.html', {
        'eventos_producto': eventos_producto,
        'eventos_servicio': eventos_servicio,
        'calendar': calendar,
        'year': year,
        'month': month,
        'month_name': month_name
    })