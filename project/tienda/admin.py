from django.contrib import admin
from .models import * # Importa tu modelo

admin.site.register(Servicio) 
admin.site.register(EstadoRegistro) 
admin.site.register(CategoariaServicio) 