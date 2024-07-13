from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # paths for categories
    path('productos', views.productos, name='productos'),
]