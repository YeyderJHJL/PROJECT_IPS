import datetime
from django import forms
from .models import Personal, EstadoRegistro, TipoPersonal

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
        fields = ['tippercod', 'tippernom']  # Incluye el campo 'tippercod'
        widgets = {
            'tippercod': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'tippernom': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'tippercod': 'Código',
            'tippernom': 'Nombre',
        }

    def __init__(self, *args, **kwargs):
        super(TipoPersonalForm, self).__init__(*args, **kwargs)
        if self.instance.pk:  # Solo para ediciones
            self.fields['tippercod'].widget.attrs['readonly'] = True
            self.fields['tippercod'].required = False