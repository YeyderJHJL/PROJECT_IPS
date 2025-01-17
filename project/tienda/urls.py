from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # General
    path('', views.index, name='index'),
     path('indexAdministrador', views.indexAdministrador, name='indexAdministrador'),
    path('empresa/', views.empresa, name='empresa'),
    path('preguntas_frecuentes/', views.preguntas_frecuentes, name='preguntas_frecuentes'),

    path('vendedor_home/', views.vendedor_home, name='vendedor_home'),
    # Gabriela
    # path('contact/', views.contact_form, name='contact_form'),
    # path('contact/success/', views.contact_success, name='contact_success'),

    path('consulta/cliente/add', views.consulta_cliente_add, name='consulta_cliente_add'),
    path('consulta/cliente/list', views.consulta_cliente_list, name='consulta_cliente_list'),
    path('consulta/cliente/delete/<int:pk>/', views.consulta_cliente_delete, name='consulta_cliente_delete'),

    path('gestion/consulta/', views.gestion_consulta, name='gestion_consulta'),
    path('gestion/tipo_consulta/', views.gestion_tipo_consulta, name='gestion_tipo_consulta'),

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
    path('vendedor/servicios/<str:codigo>/', views.vendedor_servicios, name='vendedor_servicios_codigo'),
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('servicios/detalle/<str:sercod>/', views.detalle_servicio, name='detalle_servicio'),
    path('crear_evento', views.crear_evento, name='crear_evento'),
    path('reserva/detalle/servicio/<int:evecod>/', views.detalle_reservaS, name='detalle_reservaS'),
    path('reservaServicio/editar/<int:evecod>/', views.editar_reservaS, name='editar_reservaS'),
    path('reservaServicio/eliminar/<int:evecod>/', views.eliminar_reservaS, name='eliminar_reservaS'),
    #personal
    path('gestionar_servicios', views.gestionar_servicios, name='gestionar_servicios'),
    path('gestionar_servicios/<str:codigo>/', views.gestionar_servicios, name='gestionar_servicios_codigo'),
    path('vendedor/gestionar_servicios', views.vendedor_gestionar_servicios, name='vendedor_gestionar_servicios'),
    path('agregar_servicio/', views.agregar_servicio, name='agregar_servicio'),
    path('vendedor/agregar_servicio/', views.vendedor_agregar_servicio, name='vendedor_agregar_servicio'),
    path('modificar_servicio/<str:sercod>/', views.modificar_servicio, name='modificar_servicio'),
    path('vendedor/modificar_servicio/<str:sercod>/', views.vendedor_modificar_servicio, name='vendedor_modificar_servicio'),
    path('eliminar_servicio/<str:sercod>/', views.eliminar_servicio, name='eliminar_servicio'),
    path('vendedor/eliminar_servicio/<str:sercod>/', views.vendedor_eliminar_servicio, name='vendedor_eliminar_servicio'),
    path('gestionar_CategoriaServicios', views.gestionar_CategoriaServicios, name='gestionar_CategoriaServicios'),
    path('agregar_CategoriaServicio/', views.agregar_CategoriaServicio, name='agregar_CategoriaServicio'),
    path('modificar_CategoriaServicio/<str:catsercod>/', views.modificar_CategoriaServicio, name='modificar_CategoriaServicio'),
    path('eliminar_CategoriaServicio/<str:catsercod>/', views.eliminar_CategoriaServicio, name='eliminar_CategoriaServicio'),
    path('reservaServicio/detalle/<int:evecod>/', views.detalle_reservaS, name='detalle_reservaS'),
    path('reservaServicio/editar/<int:evecod>/', views.editar_reservaS, name='editar_reservaS'),
    path('reservaServicio/eliminar/<int:evecod>/', views.eliminar_reservaS, name='eliminar_reservaS'),
    path('gestionar_CategoriaProductos', views.gestionar_CategoriaProductos, name='gestionar_CategoriaProductos'),
    path('agregar_CategoriaProductos/', views.agregar_CategoriaProductos, name='agregar_CategoriaProductos'),
    path('modificar_CategoriaProductos/<str:catprocod>/', views.modificar_CategoriaProductos, name='modificar_CategoriaProductos'),
    path('eliminar_CategoriaProductos/<str:catprocod>/', views.eliminar_CategoriaProductos, name='eliminar_CategoriaProductos'),
    path('calendarioAdministrador/', views.calendario_viewAdministrador, name='calendarioAdministrador'),
    path('perfil/', views.perfil, name='perfil'),

    # Paola
    #cliente
    path('productos', views.productos, name='productos'),
    path('producto/<int:procod>/', views.detalle_producto, name='detalle_producto'),
    path('reserva/<int:procod>/', views.reserva_producto, name='reserva_producto'),
    path('reservas/', views.lista_reservas, name='lista_reservas'),
    path('reserva/detalle/producto/<int:evecod>/', views.detalle_reserva, name='detalle_reserva'),
    path('reserva/editar/<int:evecod>/', views.editar_reserva, name='editar_reserva'),
    path('reserva/eliminar/<int:evecod>/', views.confirmar_eliminar_reserva, name='confirmar_eliminar_reserva'),
    path('calendario/', views.calendario_view, name='calendario'),
    #personal
    path('productoslista', views.lista_productos, name='lista_productos'),
    path('producto/agregar/', views.producto_create, name='producto_create'),
    path('producto/editar/<int:procod>/', views.producto_update, name='producto_update'),
    path('producto/confirmar_eliminacion/<int:procod>/', views.confirmar_eliminacion, name='confirmar_eliminacion'),
    path('producto/eliminar/<int:procod>/', views.producto_delete, name='producto_delete'),
    path('vendedor/gestionar_productos', views.vendedor_gestionar_productos, name='vendedor_gestionar_productos'),
    # path('vendedor/productoslista', views.vendedor_lista_productos, name='vendedor_lista_productos'),
    path('vendedor/producto/agregar/', views.vendedor_producto_create, name='vendedor_producto_create'),
    path('vendedor/producto/editar/<int:procod>/', views.vendedor_producto_update, name='vendedor_producto_update'),
    path('vendedor/producto/confirmar_eliminacion/<int:procod>/', views.vendedor_confirmar_eliminacion, name='vendedor_confirmar_eliminacion'),
    path('vendedor/producto/eliminar/<int:procod>/', views.vendedor_producto_delete, name='vendedor_producto_delete'),

    # Mishel
    # Estado registro
    path('estado_registro/', views.estado_registro_list, name='estado_registro_list'),
    path('estado_registro/add/', views.estado_registro_add, name='estado_registro_add'),
    path('estado_registro/edit/<str:pk>/', views.estado_registro_edit, name='estado_registro_edit'),
    path('estado_registro/delete/<str:pk>/', views.estado_registro_delete, name='estado_registro_delete'),
    
    path('inicio_tecnico/', views.inicio_tecnico, name='inicio_tecnico'),
    path('inicio_vendedor/', views.inicio_vendedor, name='inicio_vendedor'),
    path('inicio_administrador/', views.inicio_administrador, name='inicio_administrador'),

    path('actualizar_perfil_personal/', views.actualizar_perfil_personal, name='actualizar_perfil_personal'),

    # Personal
    path('personal/', views.gestion_personal, name='gestion_personal'),
    path('personal/list/', views.personal_list, name='personal_list'),
    path('personal/list/<int:codigo>/', views.personal_list, name='personal_list_codigo'),
    path('personal/add/', views.personal_add, name='personal_add'),
    path('personal/edit/<str:pk>/', views.personal_edit, name='personal_edit'),
    path('personal/delete/<str:pk>/', views.personal_delete, name='personal_delete'),
    path('personal/toggle_status/<str:pk>/', views.toggle_personal_status, name='toggle_personal_status'),
    
    # Tipo personal
    path('tipo_personal/', views.tipo_personal_list, name='tipo_personal_list'),
    path('tipo_personal/add/', views.tipo_personal_add, name='tipo_personal_add'),
    path('tipo_personal/edit/<str:pk>/', views.tipo_personal_edit, name='tipo_personal_edit'),
    path('tipo_personal/delete/<str:pk>/', views.tipo_personal_delete, name='tipo_personal_delete'),

    # Cliente
    path('cliente/', views.gestion_cliente, name='gestion_cliente'),
    path('cliente/list/', views.cliente_list, name='cliente_list'),
    path('cliente/add/', views.cliente_add, name='cliente_add'),
    path('cliente/edit/<str:pk>/', views.cliente_edit, name='cliente_edit'),
    path('cliente/delete/<str:pk>/', views.cliente_delete, name='cliente_delete'),
    path('gestion/cliente/delete/<str:pk>/', views.gestion_cliente_delete, name='gestion_cliente_delete'),
    
    path('vendedor/cliente/list/', views.vendedor_cliente_list, name='vendedor_cliente_list'),
    path('vendedor/cliente/add/', views.vendedor_cliente_add, name='vendedor_cliente_add'),
    path('vendedor/cliente/edit/<str:pk>/', views.vendedor_cliente_edit, name='vendedor_cliente_edit'),
    path('vendedor/cliente/delete/<str:pk>/', views.vendedor_cliente_delete, name='vendedor_cliente_delete'),

    path('cliente/toggle_status/<int:pk>/', views.toggle_cliente_status, name='toggle_cliente_status'),

    # Jhamil
    #cliente
    path('register/', views.register_view, name='cliente_register'),
    path('login/', views.cliente_login, name='cliente_login'),
    path('logout/', views.cliente_logout, name='cliente_logout'),
    path('detail/', views.cliente_detail, name='cliente_detail'),
    path('update/', views.cliente_update, name='cliente_update'),
    path('delete/', views.cliente_delete, name='cliente_delete'),
    # personal
    path('personal_register/', views.register_personal_view, name='personal_register'),
    path('personal_login/', views.personal_login, name='personal_login'),
    path('personal_logout/', views.personal_logout, name='personal_logout'),

    path('sales_report/', views.sales_report, name='sales_report'),

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
