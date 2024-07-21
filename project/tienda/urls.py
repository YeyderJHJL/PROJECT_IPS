# tienda/urls.py
from django.contrib import admin
from django.urls import path
from . import views  # Asegúrate de importar views correctamente

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Ruta para la vista index
    path('contact/', views.contact_view, name='ContactForm'),  # Ruta actualizada
    path('empresa/', views.empresa, name='empresa'),
    path('login/', views.login, name='login'),
    path('contact_success/', views.contact_success, name='contact_success'),
]
