from django import forms
from .models import *

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['pronom', 'prodes', 'procan', 'propreuni', 'estregcod', 'catprocod', 'proimg']
        widgets = {
            'pronom': forms.TextInput(attrs={'class': 'form-control'}),
            'prodes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'procan': forms.NumberInput(attrs={'class': 'form-control'}),
            'propreuni': forms.NumberInput(attrs={'class': 'form-control'}),
            'estregcod': forms.Select(attrs={'class': 'form-control'}),
            'catprocod': forms.Select(attrs={'class': 'form-control'}),
            'proimg': forms.FileInput(attrs={'class': 'form-control'}),
        }