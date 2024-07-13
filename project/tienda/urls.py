from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('servicios', views.servicios, name='servicios'),
    path('servicios/<str:codigo>/', views.servicios, name='servicios_codigo'),
    path('crear_evento', views.crear_evento, name='crear_evento'),

    # paths for categories
]