
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import ContactForm

def index(request):
    return render(request, './index.html')

def login(request):
    return render(request, './login.html')

def empresa(request):
    return render(request, './empresa.html')


def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Procesa el formulario, como enviar un correo electrónico
            send_mail(
                'Nuevo mensaje de contacto',
                form.cleaned_data['message'],
                form.cleaned_data['email'],
                ['tu_email@example.com'],  # Cambia esto por tu dirección de correo
            )
            return redirect('contact_success')  # Redirige a una página de éxito
    else:
        form = ContactForm()
    
    return render(request, 'contact_form.html', {'form': form})

def contact_success(request):
    return render(request, 'contact_success.html')
