from django.contrib import admin
from .models import * # Importa tu modelo

admin.site.register(Servicio) 
admin.site.register(EstadoRegistro) 
admin.site.register(CategoariaServicio) 
admin.site.register(Evento) 
admin.site.register(Cliente)
admin.site.register(Personal)
admin.site.register(Producto) 
admin.site.register(CategoariaProducto) 
