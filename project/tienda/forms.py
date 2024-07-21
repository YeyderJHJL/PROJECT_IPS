from django import forms
from .models import *
import datetime
from django.contrib.auth.forms import AuthenticationForm

class EventoForm(forms.ModelForm):
    evedes = forms.CharField(
        max_length=150, 
        label="Descripción",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    evefec = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    perdni = forms.ModelChoiceField(
        queryset=Personal.objects.all(),
        label="Personal Encargado",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Evento
        fields = ['evedes', 'evefec', 'perdni']
        labels = {
            'evedes': 'Agregar Otros datos',
            'evefec': 'Fecha',
            'perdni': 'Personal Encargado',
        }

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
    catsernom = forms.ModelChoiceField(
        queryset=CategoariaServicio.objects.all(),
        label="Seleccione una categoría",
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'this.form.submit();'})
    )

    class Meta:
        model = CategoariaServicio
        fields = ['catsernom']

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

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

    class Meta:
        model = Cliente
        fields = ['cliusu', 'clicon']  # Los campos que utilizarás para el inicio de sesión

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password) # type: ignore
            if not user:
                raise forms.ValidationError("Nombre de usuario o contraseña incorrectos.")
        
        return cleaned_data





    
class ClienteUpdateForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['clinom', 'cliape', 'clitel', 'clidir', 'clicor']

    def clean_clicor(self):
        clicor = self.cleaned_data.get('clicor')
        if Cliente.objects.filter(clicor=clicor).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return clicor

class UsuarioUpdateForm(forms.Form):
    cliusu = forms.CharField(max_length=60)

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
