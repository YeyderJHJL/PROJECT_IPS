from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('servicios', views.servicios, name='servicios'),
    path('servicios/<str:codigo>/', views.servicios, name='servicios_codigo'),
    path('crear_evento', views.crear_evento, name='crear_evento'),

    # paths for categories
    path('productos', views.productos, name='productos'),
    path('producto/<int:procod>/', views.detalle_producto, name='detalle_producto'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)