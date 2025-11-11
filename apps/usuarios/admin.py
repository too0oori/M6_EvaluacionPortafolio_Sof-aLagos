from django.contrib import admin
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'telefono', 'direccion', 'fecha_registro')
    search_fields = ('usuario__username', 'telefono')
    readonly_fields = ('fecha_registro',)