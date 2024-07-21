from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # General
    path('', views.index, name='index'),
    # Maria
    path('servicios', views.servicios, name='servicios'),
    path('servicios/<str:codigo>/', views.servicios, name='servicios_codigo'),
    path('crear_evento', views.crear_evento, name='crear_evento'),

    # Paola
    path('productos', views.productos, name='productos'),
    path('producto/<int:procod>/', views.detalle_producto, name='detalle_producto'),
    
    # Daniel
    path('calendar/', views.calendar_view, name='calendar'),

    # Mishel
    path('estado_registro/', views.estado_registro_list, name='estado_registro_list'),
    path('estado_registro/add/', views.estado_registro_add, name='estado_registro_add'),
    path('estado_registro/edit/<str:pk>/', views.estado_registro_edit, name='estado_registro_edit'),
    path('estado_registro/delete/<str:pk>/', views.estado_registro_delete, name='estado_registro_delete'),
    
    path('login_personal/', views.login_personal, name='login_personal'),
    path('inicio_tecnico/', views.inicio_tecnico, name='inicio_tecnico'),
    path('inicio_vendedor/', views.inicio_vendedor, name='inicio_vendedor'),
    path('inicio_administrador/', views.inicio_administrador, name='inicio_administrador'),

    path('actualizar_perfil_personal/', views.actualizar_perfil_personal, name='actualizar_perfil_personal'),

    path('personal/', views.gestion_personal, name='gestion_personal'),
    path('personal/list/', views.personal_list, name='personal_list'),
    path('personal/add/', views.personal_add, name='personal_add'),
    path('personal/edit/<int:pk>/', views.personal_edit, name='personal_edit'),
    path('personal/delete/<int:pk>/', views.personal_delete, name='personal_delete'),
    path('personal/toggle_status/<int:pk>/', views.toggle_personal_status, name='toggle_personal_status'),
    path('tipo_personal/', views.tipo_personal_list, name='tipo_personal_list'),
    path('tipo_personal/add/', views.tipo_personal_add, name='tipo_personal_add'),
    path('tipo_personal/edit/<str:pk>/', views.tipo_personal_edit, name='tipo_personal_edit'),
    path('tipo_personal/delete/<str:pk>/', views.tipo_personal_delete, name='tipo_personal_delete'),

    # Jhamil
    path('register/', views.register_view, name='cliente_register'),
    path('protected/', views.protected_view, name='protected'),
    path('login/', views.cliente_login, name='cliente_login'),
    path('logout/', views.cliente_logout, name='cliente_logout'),
    path('detail/', views.cliente_detail, name='cliente_detail'),
    path('update/', views.cliente_update, name='cliente_update'),
    path('delete/', views.cliente_delete, name='cliente_delete'),
    # path('change_username/', views.change_username, name='change_username'),
    # path('confirm_username/<uidb64>/<token>/', views.confirm_username, name='confirm_username'),
    path('solicitar-cambio-password/', views.solicitar_cambio_password, name='solicitar_cambio_password'),
    path('cambiar-password/<token>/', views.cambiar_password, name='cambiar_password'),
    # path('cambiar_usuario/', views.cambiar_usuario, name='cambiar_usuario'),
    # path('cambiar_contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),

    path('ventas/', views.venta_list, name='venta_list'),
    path('venta/<int:pk>/', views.venta_detail, name='venta_detail'),
    path('venta/<int:pk>/edit/', views.venta_edit, name='venta_edit'),
    path('venta/<int:pk>/delete/', views.venta_delete, name='venta_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
