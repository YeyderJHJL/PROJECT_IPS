from django.contrib import admin
from django.urls import path
from tienda import views

urlpatterns = [
   path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Ruta para la vista index
    path('contactForm/', views.contactForm, name='contactForm'),
    path('empresa/', views.empresa, name='empresa'),
     path('login/', views.login, name='login'),
]