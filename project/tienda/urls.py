from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    # paths for categories
    path('productos', views.productos, name='productos'),
    path('producto/agregar/', views.agregar_producto, name='agregar_producto'),
    path('producto/editar/<int:procod>/', views.editar_producto, name='editar_producto'),
    path('producto/<int:procod>/', views.detalle_producto, name='detalle_producto'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)