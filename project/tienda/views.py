from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def calendar_view(request):
    return render(request, 'calendar.html')

