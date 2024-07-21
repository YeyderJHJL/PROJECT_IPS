from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # paths for categories
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar2/', views.calendar2, name='calendar2'),

    path('calendar/events/', views.calendar_events, name='calendar_events'),

    path('obtener_eventos/', views.obtener_eventos, name='obtener_eventos'),
    

]