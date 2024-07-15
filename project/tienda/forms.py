from django import forms
from .models import *

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
    perdni = forms.ModelChoiceField(
        queryset=Personal.objects.all(),
        label="Personal Encargado",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Evento
        fields = ['evecod', 'evedes', 'evefec', 'perdni']
        labels = {
            'evecod': 'Número de Servicio',
            'evedes': 'Agregar Otros datos',
            'evefec': 'Fecha',
            'perdni': 'Personal Encargado',
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
