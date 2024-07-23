from django import forms
from .models import *
import datetime
from django.utils import timezone
from datetime import date

#  CONSULTAS ################################################
class TipoConsultaForm(forms.ModelForm):
    class Meta:
        model = TipoConsulta
        fields = ['tipconnom']  # Solo incluir campos editables
        widgets = {
            'tipconnom': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'tipconnom': 'Nombre',
        }

    def __init__(self, *args, **kwargs):
        super(TipoConsultaForm, self).__init__(*args, **kwargs)
        if self.instance.pk:  # Solo para ediciones
            self.fields['tipconcod'] = forms.CharField(
                initial=self.instance.tipconcod,
                widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
                label='Código'
            )
            self.fields['tipconcod'].required = False

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['conpre', 'tipconcod', 'clidni']
        widgets = {
            'conpre': forms.Textarea(attrs={'class': 'form-control'}),
            'tipconcod': forms.Select(attrs={'class': 'form-control'}),
            # 'perdni': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'clidni': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'conpre': 'Pregunta',
            'tipconcod': 'Tipo de Consulta',
            # 'perdni': 'Personal Encargado',
            'clidni': 'Cliente',
        }
        error_messages = {
            'conpre': {
                'required': "La pregunta es obligatoria."
            },
            'tipconcod': {
                'required': "El tipo de consulta es obligatorio."
            },
            'clidni': {
                'required': "El cliente es obligatorio."
            },
        }

    def __init__(self, *args, **kwargs):
        super(ConsultaForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:  # Solo para nuevos registros
            # Establecer el cliente predeterminado como el último cliente creado
            try:
                ultimo_cliente = Cliente.objects.latest('clifecreg')
                self.fields['clidni'].initial = ultimo_cliente.pk
            except Cliente.DoesNotExist:
                pass

#  FORMULARIO DE CONTACTO ################################################

class ContactForm(forms.Form):
    name = forms.CharField(
        label='Nombre',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label='Mensaje',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )

# ESTADO DE REGISTRO ################################################################

class EstadoRegistroForm(forms.ModelForm):
    class Meta:
        model = EstadoRegistro
        fields = ['estregnom']  # Solo incluir campos editables
        widgets = {
            'estregnom': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'estregnom': 'Nombre',
        }

    def __init__(self, *args, **kwargs):
        super(EstadoRegistroForm, self).__init__(*args, **kwargs)
        if self.instance.pk:  # Solo para ediciones
            self.fields['estregcod'] = forms.CharField(
                initial=self.instance.estregcod,
                widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
                label='Código'
            )
            self.fields['estregcod'].required = False

# PERSONAL ################################################################

class LoginPersonalForm(forms.Form):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                personal = Personal.objects.get(perusu=username, percon=password)
                self.personal = personal
            except Personal.DoesNotExist:
                raise forms.ValidationError('Usuario o contraseña incorrectos.')
        return cleaned_data

    def get_personal(self):
        return self.personal

class ActualizarPerfilPersonalForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = ['pertel', 'perdir', 'percor']
        widgets = {
            'pertel': forms.TextInput(attrs={'class': 'form-control'}),
            'perdir': forms.TextInput(attrs={'class': 'form-control'}),
            'percor': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class PersonalForm(forms.ModelForm):
    perfecreg = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    
    class Meta:
        model = Personal
        fields = ['perdni', 'pernom', 'perape', 'pertel', 'perdir', 'perusu', 'percon', 'percor', 'perfecreg', 'estregcod', 'tippercod']
        widgets = {
            'perdni': forms.TextInput(attrs={'class': 'form-control'}),
            'pernom': forms.TextInput(attrs={'class': 'form-control'}),
            'perape': forms.TextInput(attrs={'class': 'form-control'}),
            'pertel': forms.TextInput(attrs={'class': 'form-control'}),
            'perdir': forms.TextInput(attrs={'class': 'form-control'}),
            'perusu': forms.TextInput(attrs={'class': 'form-control'}),
            'percon': forms.PasswordInput(attrs={'class': 'form-control'}),
            'percor': forms.EmailInput(attrs={'class': 'form-control'}),
            'perfecreg': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estregcod': forms.Select(attrs={'class': 'form-control'}),
            'tippercod': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'perdni': 'DNI',
            'pernom': 'Nombre',
            'perape': 'Apellido',
            'pertel': 'Teléfono',
            'perdir': 'Dirección',
            'perusu': 'Usuario',
            'percon': 'Contraseña',
            'percor': 'Correo',
            'perfecreg': 'Fecha de Registro',
            'estregcod': 'Estado de Registro',
            'tippercod': 'Tipo de Personal',
        }
        error_messages = {
            'perdni': {
                'unique': "Ya existe un personal con este DNI.",
                'required': "El DNI del personal es obligatorio."
            },
            'pernom': {
                'required': "El nombre del personal es obligatorio."
            },
            'perape': {
                'required': "El apellido del personal es obligatorio."
            },
            'perusu': {
                'required': "El usuario del personal es obligatorio."
            },
        }
    
    def __init__(self, *args, **kwargs):
        super(PersonalForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:  # Solo para nuevos registros
            self.fields['perfecreg'].initial = datetime.date.today()
            self.fields['estregcod'].initial = EstadoRegistro.objects.get(estregnom='Activo')
        else:
            self.fields['perdni'].widget.attrs['readonly'] = True

class TipoPersonalForm(forms.ModelForm):
    class Meta:
        model = TipoPersonal
        fields = ['tippernom']  # Solo incluir campos editables
        widgets = {
            'tippernom': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'tippernom': 'Nombre',
        }

    def __init__(self, *args, **kwargs):
        super(TipoPersonalForm, self).__init__(*args, **kwargs)
        if self.instance.pk:  # Solo para ediciones
            self.fields['tippercod'] = forms.CharField(
                initial=self.instance.tippercod,
                widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
                label='Código'
            )
            self.fields['tippercod'].required = False

class ActualizarPerfilPersonalForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = ['pertel', 'perdir', 'percor']  # Solo los campos que se pueden actualizar
        widgets = {
            'pertel': forms.TextInput(attrs={'class': 'form-control'}),
            'perdir': forms.TextInput(attrs={'class': 'form-control'}),
            'percor': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'pertel': 'Teléfono',
            'perdir': 'Dirección',
            'percor': 'Correo',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['perdni'].widget.attrs['readonly'] = True
        self.fields['pernom'].widget.attrs['readonly'] = True
        self.fields['perape'].widget.attrs['readonly'] = True
        self.fields['perusu'].widget.attrs['readonly'] = True
        self.fields['percon'].widget.attrs['readonly'] = True
        self.fields['perfecreg'].widget.attrs['readonly'] = True
        self.fields['estregcod'].widget.attrs['readonly'] = True
        self.fields['tippercod'].widget.attrs['readonly'] = True

# CLIENTE ################################################################

class ClienteForm(forms.ModelForm):
    clifecreg = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}), required=False)
    
    class Meta:
        model = Cliente
        fields = ['clidni', 'clinom', 'cliape', 'clitel', 'clidir', 'cliusu', 'clicon', 'clicor', 'clifecreg', 'estregcod']
        widgets = {
            'clidni': forms.TextInput(attrs={'class': 'form-control'}),
            'clinom': forms.TextInput(attrs={'class': 'form-control'}),
            'cliape': forms.TextInput(attrs={'class': 'form-control'}),
            'clitel': forms.TextInput(attrs={'class': 'form-control'}),
            'clidir': forms.TextInput(attrs={'class': 'form-control'}),
            'cliusu': forms.TextInput(attrs={'class': 'form-control'}),
            'clicon': forms.PasswordInput(attrs={'class': 'form-control'}),
            'clicor': forms.EmailInput(attrs={'class': 'form-control'}),
            'clifecreg': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estregcod': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'clidni': 'DNI',
            'clinom': 'Nombre',
            'cliape': 'Apellido',
            'clitel': 'Teléfono',
            'clidir': 'Dirección',
            'cliusu': 'Usuario',
            'clicon': 'Contraseña',
            'clicor': 'Correo',
            'clifecreg': 'Fecha de Registro',
            'estregcod': 'Estado de Registro',
        }
        error_messages = {
            'clidni': {
                'unique': "Ya existe un cliente con este DNI.",
                'required': "El DNI del cliente es obligatorio."
            },
            'clinom': {
                'required': "El nombre del cliente es obligatorio."
            },
            'cliape': {
                'required': "El apellido del cliente es obligatorio."
            },
            'cliusu': {
                'required': "El usuario del cliente es obligatorio."
            },
        }
    
    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:  # Solo para nuevos registros
            self.fields['clifecreg'].initial = datetime.date.today()
            self.fields['estregcod'].initial = EstadoRegistro.objects.get(estregnom='Activo')
        else:
            self.fields['clidni'].widget.attrs['readonly'] = True

class ClienteUpdateForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['clinom', 'cliape', 'clitel', 'clidir', 'clicor']

    def clean_clicor(self):
        clicor = self.cleaned_data.get('clicor')
        if Cliente.objects.filter(clicor=clicor).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return clicor

class ClienteDeleteForm(forms.Form):
    confirm = forms.BooleanField(label="Confirmo que deseo eliminar mi cuenta")


class UsuarioUpdateForm(forms.Form):
    cliusu = forms.CharField(
        label='Nuevo Nombre de Usuario',
        max_length=60,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    def clean_cliusu(self):
        cliusu = self.cleaned_data.get('cliusu')
        if Cliente.objects.filter(cliusu=cliusu).exists():
            raise forms.ValidationError("Este usuario ya está en uso.")
        return cliusu

class ContrasenaUpdateForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

class ClienteRegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Cliente
        fields = ['clidni', 'clinom', 'cliape', 'clitel', 'clidir', 'cliusu', 'clicon', 'clicor', 'clifecreg', 'estregcod']
        labels = {
            'clidni': 'DNI',
            'clinom': 'Nombre',
            'cliape': 'Apellido',
            'clitel': 'Teléfono',
            'clidir': 'Dirección',
            'cliusu': 'Usuario',
            'clicon': 'Contraseña',
            'clicor': 'Correo',
            'clifecreg': 'Fecha de Registro',
            'estregcod': 'Estado de Registro',
        }
        widgets = {
            'clicon': forms.PasswordInput(attrs={'class': 'form-control'}),
            'clifecreg': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'estregcod': forms.HiddenInput(),
        }
        error_messages = {
            'clidni': {
                'unique': "Este DNI ya está registrado.",
            },
            'cliusu': {
                'unique': "Este usuario ya está en uso.",
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("clicon")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        return cleaned_data

    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.clicon = make_password(self.cleaned_data['clicon'])  # Hashea la contraseña
        if commit:
            cliente.save()
        return cliente
    
    def __init__(self, *args, **kwargs):
        super(ClienteRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['estregcod'].initial = 1  # Asumiendo que 1 es 'activo'
    
class ClienteLoginForm(forms.Form):
    username = forms.CharField(
        label='Usuario',
        max_length=60,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

# PRODUCTO ################################################################

class ReservaForm(forms.Form):
    cantidad = forms.IntegerField(
        min_value=1,
        max_value=1000,  # se actualiza en el html
        label='Cantidad',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    fecha_reserva = forms.DateField(
        label='Fecha de Recogo',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    notas = forms.CharField(
        required=False,
        label='Notas Adicionales',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    forma_pago = forms.ChoiceField(
        choices=[
            ('tarjeta', 'Tarjeta de Crédito'),
            ('efectivo', 'Efectivo'),
            ('transferencia', 'Transferencia Bancaria')
        ],
        label='Forma de Pago',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    confirmacion = forms.BooleanField(
        required=True,
        label='Acepto las condiciones de la reserva.',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('cantidad')
        fecha_reserva = cleaned_data.get('fecha_reserva')
        # Validación personalizada para la cantidad
        if cantidad is not None and cantidad < 1:
            self.add_error('cantidad', 'La cantidad debe ser al menos 1.')
        # Validación personalizada para la fecha
        if fecha_reserva is not None and fecha_reserva < timezone.now().date():
            self.add_error('fecha_reserva', 'La fecha de recogida no puede ser anterior a la fecha actual.')
        return cleaned_data

class CategoriaProductoForm(forms.ModelForm):
    class Meta:
        model = CategoariaProducto
        fields = ['catpronom']  # Especifica los campos que quieres incluir en el formulario
        widgets = {
            'catpronom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'})
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['pronom', 'prodes', 'propreuni', 'proimg', 'proima', 'estregcod', 'catprocod']
        widgets = {
            'proimg': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'estregcod': forms.Select(attrs={'class': 'form-control'}),
            'catprocod': forms.Select(attrs={'class': 'form-control'}),
            'proima': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'pronom': 'Nombre del Producto',
            'prodes': 'Descripción del Producto',
            'propreuni': 'Precio Unitario',
            'proimg': 'Imagen del Producto',
            'proima': 'URL de la Imagen',
            'estregcod': 'Estado del Registro',
            'catprocod': 'Categoría del Producto',
        }

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['invcan', 'invfecing']
        widgets = {
            'invcan': forms.NumberInput(attrs={'class': 'form-control'}),
            'invfecing': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'invcan': 'Cantidad',
            'invfecing': 'Fecha de Ingreso',
        }

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['vencan', 'venprotot', 'venfecres', 'venclicod', 'veninvcod']
        widgets = {
            'venfecres': forms.DateInput(attrs={'type': 'date'}),
        }


# SERVICIO ################################################################

class ServicioForm(forms.ModelForm):
    sercod=forms.IntegerField(label="Codigo", disabled=True, widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}), required=False)
    sernom=forms.CharField(label="Nombre", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}))
    serdes=forms.CharField(label="Descripcion", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    serreqpre=forms.CharField(label="Prerequisitos", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    serdur=forms.CharField(label="Duración", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}))
    sercos=forms.FloatField(label= "Costo",widget=forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}), initial=0)
    serima=forms.CharField(label="URL de imagen", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}))
    serimg=forms.CharField(label="Directorio de Imagen", required=False)
    estado_registro_estregcod = forms.ModelChoiceField(queryset=EstadoRegistro.objects.all(), label="Estado de Registro", widget=forms.Select(attrs={'class': 'form-control'}))
    categoaria_servicio_catsercod=forms.ModelChoiceField(queryset=CategoariaServicio.objects.order_by('catsernom'), label="Categoria", widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model=Servicio
        fields = ['sercod', 'sernom', 'serdes', 'serreqpre', 'serdur', 'sercos', 'serima', 'serimg', 'estado_registro_estregcod', 'categoaria_servicio_catsercod']
        labels={
            'sernom' : 'Nombre de Servicio',
            'serdes' : 'Descripción',
            'serreqpre' : 'Prerequisitos',
            'serdur' : 'Duración',
            'sercos' : 'Costo',
            'serima' : 'Imagen URL',
            'serimg' : 'Imagen directorio',
            'estado_registro_estregcod' : 'Estado registro',
            'categoaria_servicio_catsercod' : 'Categoria', 
        }

class CategoriaServicioForm(forms.ModelForm):
    catsernom = forms.CharField(
        max_length=150, 
        label="Nombre de Categoria",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1})
    )

    class Meta:
        model = CategoariaServicio
        fields = ['catsernom']
        labels = {
            'catsernom': 'Nombre de Categoria',
        }

# EVENTO ################################################################
class EventoForm(forms.ModelForm):
    evecod = forms.IntegerField(
        label="Código",
        disabled=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
        required=False
    )
    evedes = forms.CharField(
        max_length=150, 
        label="Descripción",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    evefec = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Evento
        fields = ['evecod', 'evedes', 'evefec']
        labels = {
            'evecod': 'Número de Servicio',
            'evedes': 'Agregar Otros datos',
            'evefec': 'Fecha',
        }
    
    def clean_evefec(self):
        fecha = self.cleaned_data.get('evefec')
        if fecha < datetime.date.today():
            raise forms.ValidationError('La fecha no puede ser anterior a la fecha actual.')
        return fecha