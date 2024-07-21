# tienda/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from .forms import ContactForm

def index(request):
    return render(request, 'index.html')

def contact_view(request):  # Cambiado el nombre de la vista a contact_view
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['name']
            correo_electronico = form.cleaned_data['email']
            mensaje = form.cleaned_data['message']

            # Enviar correo electrónico
            send_mail(
                f'Mensaje de {nombre}',
                mensaje,
                correo_electronico,
                ['destinatario@example.com'],
            )
            return redirect('contact_success')  # Redirigir a una página de éxito
    else:
        form = ContactForm()
    return render(request, 'ContactForm.html', {'form': form})

def empresa(request):
    return render(request, 'empresa.html')

def login(request):
    return render(request, 'login.html')

def contact_success(request):
    return render(request, 'contact_success.html')
