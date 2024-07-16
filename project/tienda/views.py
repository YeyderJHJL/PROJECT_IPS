from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def contactForm(request):
    return render(request, 'contactForm.html')

def InfoEmpresa(request):
    return render(request, 'InfoEmpresa.html')