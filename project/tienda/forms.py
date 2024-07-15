# forms.py
from django import forms
from .models import Cliente
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
    
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
