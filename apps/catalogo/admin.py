from django.contrib import admin

from apps.catalogo.models import Autor, Categoria, Libro

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'isbn', 'editorial','ano_publicacion', 'categoria', 'copias_totales', 'copias_disponibles', 'disponibilidad')
    search_fields = ('titulo', 'autor__nombre', 'isbn')
    list_filter = ('categoria', 'ano_publicacion')
    readonly_fields = ('fecha_registro',)

    def disponibilidad(self, obj):
        return obj.copias_disponibles > 0
    disponibilidad.boolean = True
    disponibilidad.short_description = 'Disponible'
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais', 'fecha_nacimiento')
    search_fields = ('nombre', 'pais')


admin.site.site_header = "Administración de Biblioteca Digital"
admin.site.site_title = "Biblioteca Digital Admin"
admin.site.index_title = "Panel de Administración"