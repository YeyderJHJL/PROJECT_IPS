from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # General
    path('', views.index, name='index'),
    path('empresa/', views.empresa, name='empresa'),
    path('preguntas_frecuentes/', views.preguntas_frecuentes, name='preguntas_frecuentes'),

    # Gabriela
    # path('contact/', views.contact_form, name='contact_form'),
    # path('contact/success/', views.contact_success, name='contact_success'),

    path('consulta/cliente/add', views.consulta_cliente_add, name='consulta_cliente_add'),
    path('consulta/cliente/list', views.consulta_cliente_list, name='consulta_cliente_list'),
    path('consulta/cliente/delete/<int:pk>/', views.consulta_cliente_delete, name='consulta_cliente_delete'),

    path('consulta/', views.gestion_consulta, name='gestion_consulta'),

    path('consulta/list/', views.consulta_list, name='consulta_list'),
    path('consulta/edit/<int:pk>/', views.consulta_edit, name='consulta_edit'),
    path('consulta/delete/<int:pk>/', views.consulta_delete, name='consulta_delete'),

    path('tipo_consulta/', views.tipo_consulta_list, name='tipo_consulta_list'),
    path('tipo_consulta/add/', views.tipo_consulta_add, name='tipo_consulta_add'),
    path('tipo_consulta/edit/<str:pk>/', views.tipo_consulta_edit, name='tipo_consulta_edit'),
    path('tipo_consulta/delete/<str:pk>/', views.tipo_consulta_delete, name='tipo_consulta_delete'),

    # Maria
    #cliente
    path('servicios', views.servicios, name='servicios'),
    path('servicios/<str:codigo>/', views.servicios, name='servicios_codigo'),
    path('servicios/detalle/<str:sercod>/', views.detalle_servicio, name='detalle_servicio'),
    path('crear_evento', views.crear_evento, name='crear_evento'),
    path('reservaServicio/detalle/<int:evecod>/', views.detalle_reservaS, name='detalle_reservaS'),
    path('reservaServicio/editar/<int:evecod>/', views.editar_reservaS, name='editar_reservaS'),
    path('reservaServicio/eliminar/<int:evecod>/', views.eliminar_reservaS, name='eliminar_reservaS'),
    #personal
    path('gestionar_servicios', views.gestionar_servicios, name='gestionar_servicios'),
    path('agregar_servicio/', views.agregar_servicio, name='agregar_servicio'),
    path('modificar_servicio/<str:sercod>/', views.modificar_servicio, name='modificar_servicio'),
    path('eliminar_servicio/<str:sercod>/', views.eliminar_servicio, name='eliminar_servicio'),
    path('gestionar_CategoriaServicios', views.gestionar_CategoriaServicios, name='gestionar_CategoriaServicios'),
    path('agregar_CategoriaServicio/', views.agregar_CategoriaServicio, name='agregar_CategoriaServicio'),
    path('modificar_CategoriaServicio/<str:catsercod>/', views.modificar_CategoriaServicio, name='modificar_CategoriaServicio'),
    path('eliminar_CategoriaServicio/<str:catsercod>/', views.eliminar_CategoriaServicio, name='eliminar_CategoriaServicio'),
    path('reservaServicio/detalle/<int:evecod>/', views.detalle_reservaS, name='detalle_reservaS'),
    path('reservaServicio/editar/<int:evecod>/', views.editar_reservaS, name='editar_reservaS'),
    path('reservaServicio/eliminar/<int:evecod>/', views.eliminar_reservaS, name='eliminar_reservaS'),

    # Paola
    #cliente
    path('productos', views.productos, name='productos'),
    path('producto/<int:procod>/', views.detalle_producto, name='detalle_producto'),
    path('reserva/<int:procod>/', views.reserva_producto, name='reserva_producto'),
    path('reservas/', views.lista_reservas, name='lista_reservas'),
    path('reserva/detalle/<int:evecod>/', views.detalle_reserva, name='detalle_reserva'),
    path('reserva/editar/<int:evecod>/', views.editar_reserva, name='editar_reserva'),
    path('reserva/eliminar/<int:evecod>/', views.eliminar_reserva, name='eliminar_reserva'),
    #personal
    path('productoslista', views.lista_productos, name='lista_productos'),
    path('producto/agregar/', views.producto_create, name='producto_create'),
    path('producto/editar/<int:procod>/', views.producto_update, name='producto_update'),
    path('producto/confirmar_eliminacion/<int:procod>/', views.confirmar_eliminacion, name='confirmar_eliminacion'),
    path('producto/eliminar/<int:procod>/', views.producto_delete, name='producto_delete'),

    # Daniel
    #cliente?
    path('calendar/', views.calendar_view, name='calendar'),
    #personal?
    path('calendar2/', views.calendar2, name='calendar2'),
    path('calendar/events/', views.calendar_events, name='calendar_events'),
    path('obtener_eventos/', views.obtener_eventos, name='obtener_eventos'),

    # Mishel
    # Estado registro
    path('estado_registro/', views.estado_registro_list, name='estado_registro_list'),
    path('estado_registro/add/', views.estado_registro_add, name='estado_registro_add'),
    path('estado_registro/edit/<str:pk>/', views.estado_registro_edit, name='estado_registro_edit'),
    path('estado_registro/delete/<str:pk>/', views.estado_registro_delete, name='estado_registro_delete'),
    
    path('login_personal/', views.login_personal, name='login_personal'),
    path('inicio_tecnico/', views.inicio_tecnico, name='inicio_tecnico'),
    path('inicio_vendedor/', views.inicio_vendedor, name='inicio_vendedor'),
    path('inicio_administrador/', views.inicio_administrador, name='inicio_administrador'),

    path('actualizar_perfil_personal/', views.actualizar_perfil_personal, name='actualizar_perfil_personal'),

    # Personal
    path('personal/', views.gestion_personal, name='gestion_personal'),
    path('personal/list/', views.personal_list, name='personal_list'),
    path('personal/add/', views.personal_add, name='personal_add'),
    path('personal/edit/<int:pk>/', views.personal_edit, name='personal_edit'),
    path('personal/delete/<int:pk>/', views.personal_delete, name='personal_delete'),
    path('personal/toggle_status/<int:pk>/', views.toggle_personal_status, name='toggle_personal_status'),
    
    # Tipo personal
    path('tipo_personal/', views.tipo_personal_list, name='tipo_personal_list'),
    path('tipo_personal/add/', views.tipo_personal_add, name='tipo_personal_add'),
    path('tipo_personal/edit/<str:pk>/', views.tipo_personal_edit, name='tipo_personal_edit'),
    path('tipo_personal/delete/<str:pk>/', views.tipo_personal_delete, name='tipo_personal_delete'),

    # Cliente
    path('cliente/', views.gestion_cliente, name='gestion_cliente'),
    path('cliente/list/', views.cliente_list, name='cliente_list'),
    path('cliente/add/', views.cliente_add, name='cliente_add'),
    path('cliente/edit/<int:pk>/', views.cliente_edit, name='cliente_edit'),
    path('cliente/delete/<int:pk>/', views.cliente_delete, name='cliente_delete'),
    
    path('cliente/toggle_status/<int:pk>/', views.toggle_cliente_status, name='toggle_cliente_status'),

    # Jhamil
    #cliente
    path('register/', views.register_view, name='cliente_register'),
    path('protected/', views.protected_view, name='protected'),
    path('login/', views.cliente_login, name='cliente_login'),
    path('logout/', views.cliente_logout, name='cliente_logout'),
    path('detail/', views.cliente_detail, name='cliente_detail'),
    path('update/', views.cliente_update, name='cliente_update'),
    path('delete/', views.cliente_delete, name='cliente_delete'),

    path('sales_report/', views.sales_report, name='sales_report'),

    path('orders/', views.cliente_orders, name='cliente_orders'),
    path('services/', views.cliente_services, name='cliente_services'),
    path('settings/', views.cliente_settings, name='cliente_settings'),
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
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
