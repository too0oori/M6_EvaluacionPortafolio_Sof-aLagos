from django.contrib import admin
from .models import Prestamo, Reserva
from django.utils.html import format_html

@admin.register(Prestamo)
class PrestamosAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'libro', 'fecha_prestamo', 'fecha_devolucion', 'estado')
    search_fields = ('usuario__username', 'libro__titulo')
    list_filter = ('estado', 'fecha_prestamo', 'fecha_devolucion')
    readonly_fields = ('fecha_prestamo',)

    def estado_visual(self, obj):
        colores = {
            'activo': 'blue',
            'devuelto': 'green',
            'retrasado': 'red',
        }
        color = colores.get(obj.estado, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_visual.short_description = 'Estado Visual'
    
@admin.register(Reserva)
class ReservasAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'libro', 'fecha_reserva', 'estado')
    search_fields = ('usuario__username', 'libro__titulo')
    list_filter = ('estado', 'fecha_reserva')
    readonly_fields = ('fecha_reserva',)

    def estado_visual(self, obj):
        colores = {
            'pendiente': 'orange',
            'cumplida': 'green',
            'cancelada': 'red',
        }
        color = colores.get(obj.estado, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_visual.short_description = 'Estado Visual'