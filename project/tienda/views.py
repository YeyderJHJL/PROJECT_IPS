from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.core.mail import send_mail
from django.db import IntegrityError
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
import logging
from .utils import *
from django.conf import settings

# Create your views here.

# GENERAL ################################################

def index(request):
    return render(request, 'index.html')

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

# PERSONAL ################################################

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


# Actualizar Perfil del Personal
logger = logging.getLogger(__name__)

@login_required
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

    return render(request, 'actualizar_perfil_personal_form.html', {'form': form})

# Gestion Personal 
def gestion_personal(request):
    return render(request, 'gestion_personal.html')

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

# CLIENTE ################################################

def register_view(request):
    if request.method == 'POST':
        form = ClienteRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso')
            return redirect('cliente_login')  # Cambia 'home' por el nombre de tu vista principal
    else:
        form = ClienteRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def protected_view(request):
    return render(request, 'protected.html')

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
                    return redirect('calendar')  # Cambia 'home' por la URL de redirección deseada
                else:
                    messages.error(request, 'Contraseña incorrecta')
            except Cliente.DoesNotExist:
                messages.error(request, 'Usuario no encontrado')
    else:
        form = ClienteLoginForm()
    return render(request, 'registration/login.html', {'form': form})

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

def cliente_detail(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        messages.error(request, 'No está autorizado para realizar esta acción.')
        return redirect('login') 
    
    cliente = request.cliente
    return render(request, 'cliente/cliente_detail.html', {'cliente': cliente})

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
    return render(request, 'cliente/cliente_update.html', {'form': form})

def cliente_delete(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        messages.error(request, 'No está autorizado para realizar esta acción.')
        return redirect('cliente_login') 

    cliente = get_object_or_404(Cliente, clidni=cliente_id)

    if request.method == 'POST':
        form = ClienteDeleteForm(request.PsOST)
        if form.is_valid():
            cliente.delete()
            request.session.flush()
            messages.success(request, 'Cuenta eliminada exitosamente.')
            return redirect('cliente_login') 
    else:
        form = ClienteDeleteForm()

    return render(request, 'cliente/cliente_delete.html', {'form': form})

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
            # Asumiendo que tienes un campo para el correo electrónico del cliente
            email = cliente.clicor  # Ajusta esto si el campo de correo es diferente
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

@login_required
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

@login_required
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

@login_required
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

# PRODUCTO ################################################

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

def detalle_producto(request, procod):
    producto = get_object_or_404(Producto, procod=procod)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})

def reserva_producto(request, procod):
    cliente = Cliente.objects.first()
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
            else:
                EventoProducto.objects.create(
                    evedes=f'Reserva de {cantidad} unidades del producto {producto.pronom}',
                    evefec=fecha_reserva,
                    procod=producto,
                    cantidad=cantidad,
                    cliente=cliente,
                    notas=notas
                )                
                # Actualizar inventario
                inventario.invcan -= cantidad
                inventario.save()
                messages.success(request, 'Reserva realizada con éxito.')
                return redirect('index')
        else:
            form.add_error(None, 'Por favor corrige los errores en el formulario.')
    else:
        form = ReservaForm()    # Establecer el valor máximo de cantidad disponible en el formulario     
    
    form.fields['cantidad'].max_value = cantidad_disponible

    context = {
        'cliente': cliente,
        'producto': producto,
        'cantidad_disponible': cantidad_disponible,
        'form': form
    }

    return render(request, 'productos/reservaProducto.html', context)

def detalle_reserva(request, evecod):
    reserva = get_object_or_404(EventoProducto, evecod=evecod)  
    return render(request, 'productos/detalle_reserva.html', {'reserva': reserva})

def editar_reserva(request, evecod):
    reserva = get_object_or_404(EventoProducto, evecod=evecod)
    cantidad_anterior = reserva.cantidad
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            fecha_reserva = form.cleaned_data['fecha_reserva']
            notas = form.cleaned_data['notas']
            # Actualiza el inventario según la diferencia en la cantidad
            producto = reserva.procod
            inventario = Inventario.objects.filter(procod=producto).first()
            if inventario:
                inventario.invcan += cantidad_anterior - cantidad
                inventario.save()            
            # Actualizar la reserva
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
    return render(request, 'productos/editar_reserva.html', {'form': form, 'reserva': reserva})

def eliminar_reserva(request, evecod):
    reserva = get_object_or_404(EventoProducto, evecod=evecod)
    cantidad = reserva.cantidad
    producto = reserva.procod
    inventario = Inventario.objects.filter(procod=producto).first()
    if inventario:
        # Ajustar el inventario sumando la cantidad de la reserva eliminada
        inventario.invcan += cantidad
        inventario.save()
    reserva.delete()
    messages.success(request, 'Reserva eliminada con éxito.')
    return redirect('index')


# registro de ventas

def venta_list(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas/venta_list.html', {'ventas': ventas})

def venta_detail(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    return render(request, 'ventas/venta_detail.html', {'venta': venta})

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

def venta_delete(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        messages.success(request, 'Venta eliminada exitosamente')
        return redirect('venta_list')
    return render(request, 'ventas/venta_confirm_delete.html', {'venta': venta})
# SERVICIO ################################################

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

def detalle_servicio(request, sercod):
    servicio = get_object_or_404(Servicio, sercod=sercod)
    personal = Personal.objects.filter(tippercod='2')
    return render(request, 'servicios/detalle_servicio.html', {'servicio': servicio, 'personal':personal})


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

def agregar_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestionar_servicios')  
    else:
        form = ServicioForm()
    
    return render(request, 'servicios/agregarServicios.html', {'form': form})

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

def eliminar_servicio(request, sercod):
    servicio = get_object_or_404(Servicio, sercod=sercod)
    if request.method == 'POST':
        servicio.delete()
        messages.success(request, 'Servicio eliminado correctamente.')
        return redirect('gestionar_servicios')

    return redirect('gestionar_servicios')

@login_required
def crear_evento(request):
    servicio_id = request.GET.get('servicio_id')
    cliente = Cliente.objects.first()  # Obtener el cliente autenticado o el cliente deseado

    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            if cliente:
                evento.clidni = cliente  # Asignar el cliente al evento

            if servicio_id:
                try:
                    servicio = Servicio.objects.get(pk=servicio_id)
                    evento.sercod = servicio  # Asignar la instancia del objeto Servicio
                except Servicio.DoesNotExist:
                    form.add_error(None, 'El servicio seleccionado no existe.')
                    return render(request, 'reservaServicio.html', {
                        'form': form,
                        'servicio': None,
                        'cliente': cliente,
                    })
            else:
                form.add_error(None, 'No se ha proporcionado un servicio válido.')
                return render(request, 'reservaServicio.html', {
                    'form': form,
                    'servicio': None,
                    'cliente': cliente,
                })

            evento.save()
            return redirect('index')
    else:
        if servicio_id:
            try:
                servicio = Servicio.objects.get(pk=servicio_id)
            except Servicio.DoesNotExist:
                servicio = None
        else:
            servicio = None

        form = EventoForm()

    return render(request, 'servicios/reservaServicio.html', {
        'form': form,
        'servicio': servicio,
        'cliente': cliente,
    })

def detalle_reservaS(request, evecod):
    reserva = get_object_or_404(Evento, evecod=evecod)  
    return render(request, 'servicios/detalle_reservaS.html', {'reserva': reserva})

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

def eliminar_reservaS(request, evecod):
    reserva = get_object_or_404(Evento, evecod=evecod)
    
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva eliminada correctamente.')
        return redirect('index')
    
    return redirect('index')

# EVENTO ################################################

def calendar_view(request):
    return render(request, 'calendar.html')

