from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    # paths for categories
    path('actualizar/', views.actualizar_cliente, name='actualizar_cliente'),
    path('cambiar_usuario/', views.cambiar_usuario, name='cambiar_usuario'),
    path('cambiar_contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
]