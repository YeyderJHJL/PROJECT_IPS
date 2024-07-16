from django.contrib import admin
from django.urls import path
from tienda import views

urlpatterns = [
   path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Ruta para la vista index
    path('contactForm/', views.contactForm, name='contactForm'),
    path('InfoEmpresa/', views.contactForm, name='InfoEmpresa'),
]