from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def contactForm(request):
    return render(request, 'contactForm.html')

def empresa(request):
    return render(request, 'empresa.html')

def login(request):
    return render(request, 'login.html')