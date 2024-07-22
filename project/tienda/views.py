from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.db import IntegrityError
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
import logging
from django.urls import reverse
from django.db.models import Sum
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

###### PRODUCTOS ####################################################################################
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
    cantidad_disponible = producto.inventario_set.aggregate(total_cantidad=models.Sum('invcan'))['total_cantidad'] or 0
    return render(request, 'productos/detalle_producto.html', {
        'producto': producto,
        'cantidad_disponible': cantidad_disponible
    })

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
                # Actualizar inventario
                inventario.invcan -= cantidad
                inventario.save()
                messages.success(request, 'Reserva realizada con éxito.')
                return redirect('productos')        
    else:
        form = ReservaForm()    # Establecer el valor máximo de cantidad disponible en el formulario         
    form.fields['cantidad'].widget.attrs.update({'max': cantidad_disponible})
    context = {
        'cliente': cliente,
        'producto': producto,
        'cantidad_disponible': cantidad_disponible,
        'form': form
    }
    return render(request, 'productos/reservaProducto.html', context)

def lista_reservas(request):
    reservas = EventoProducto.objects.all()
    return render(request, 'productos/lista_reservas.html', {'reservas': reservas})

def detalle_reserva(request, evecod):
    reserva = get_object_or_404(EventoProducto, evecod=evecod)  
    return render(request, 'productos/detalle_reserva.html', {'reserva': reserva})

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
            # Validaciones adicionales
            if cantidad > cantidad_disponible:
                form.add_error('cantidad', 'La cantidad solicitada excede la disponible.')
            if fecha_reserva < timezone.now().date():
                form.add_error('fecha_reserva', 'La fecha de recogida no puede ser anterior a la fecha actual.')            
            # Actualiza el inventario según la diferencia en la cantidad            
            if inventario:
                inventario.invcan += cantidad_anterior - cantidad
                inventario.save()     
            else:
                messages.error(request, 'No se encontró el producto en el inventario.')
                return render(request, 'productos/editar_reserva.html', {'form': form, 'reserva': reserva})       
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
    form.fields['cantidad'].widget.attrs.update({'max': cantidad_disponible})
    context = {
        'form': form,
        'reserva': reserva,
        'cantidad_disponible': cantidad_disponible
    }
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

  #gestion productos con inventario

def lista_productos(request):
    productos = Producto.objects.all()
    inventarios = Inventario.objects.values('procod').annotate(total_can=Sum('invcan'))
    cantidad_dict = {inv['procod']: inv['total_can'] for inv in inventarios}
    context = {
        'productos': productos,
        'cantidad_dict': cantidad_dict,
    }
    return render(request, 'productos/producto_lista.html', context)


def producto_create(request):
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST, request.FILES)
        inventario_form = InventarioForm(request.POST)
        if producto_form.is_valid() and inventario_form.is_valid():
            producto = producto_form.save()
            inventario = inventario_form.save(commit=False)
            inventario.procod = producto
            inventario.save()
            return redirect('lista_productos')
    else:
        producto_form = ProductoForm()
        inventario_form = InventarioForm()

    context = {
        'producto_form': producto_form,
        'inventario_form': inventario_form
    }
    return render(request, 'productos/producto_form.html', context)


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

def producto_delete(request, procod):
    producto = Producto.objects.get(procod=procod)
    inventario = Inventario.objects.get(procod=producto)
    if request.method == 'POST':
        inventario.delete()
        producto.delete()
        return redirect(reverse('lista_productos'))
    return render(request, 'productos/producto_eliminar.html', {
        'producto': producto,
        'inventario': inventario,
    })

####################################################
def calendar_view(request):
    return render(request, 'calendar.html')

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
##########
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirige a la página de inicio u otra página después del login exitoso
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Formulario no válido.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

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

##########
