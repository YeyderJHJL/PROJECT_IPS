from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Evento

def index(request):
    return render(request, 'index.html')

def calendar_view(request):
    return render(request, 'calendar.html')


def calendar2(request):
    return render(request, 'calendar2.html')

@csrf_exempt
def calendar_events(request):
    events = Evento.objects.all()
    event_list = []
    for event in events:
        event_list.append({
            'title': event.sercod.sernom,
            'start': event.evefec.isoformat(),
            'description': f"Cliente: {event.clidni}, Personal: {event.perdni}"
        })
    return JsonResponse(event_list, safe=False)

def obtener_eventos(request):
    eventos = Evento.objects.all().select_related('sercod', 'perdni')
    eventos_json = [
        {
            'fecha': evento.evefec.strftime('%Y-%m-%d'),
            'servicio': evento.sercod.sernom,
            'tecnico': evento.perdni.nombre_completo  # Asumiendo que tienes un campo nombre_completo en el modelo Personal
        }
    for evento in eventos]
    return JsonResponse(eventos_json, safe=False)